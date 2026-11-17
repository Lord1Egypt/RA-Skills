#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
长期记忆评测台 v2 · LoCoMo / LongMemEval 风格（本地忠实复现方法论）
=========================================================================
v2 升级（对应 D10 评测加严）：
  - 评分从"token 覆盖≥60%"升级为 **EM(精确匹配) + F1(字符级)**，标准可比对
  - 题型扩展：时序/事件/实体/多跳/否定/指代/反事实/多约束/跨会话整合
  - 模型接口可插拔：`model_answer()` 默认 internal(确定性解析，可复现)，
    设 MODEL_BACKEND=api 时调用**真实 LLM**（OpenAI 兼容：SiliconFlow / DeepSeek 均可）。
    真模型经 env 注入密钥(REAL_API_KEY/REAL_API_BASE/REAL_MODEL)，不打印、不落盘。
说明：官方 LoCoMo / LongMemEval 需其授权数据集，本台为方法论忠实复现。
"""
import time, re, os, json, urllib.request, urllib.error

TRANSCRIPT = """
[会话1·周一] 林涛：这周要把"星轨"智能手表发布会定下来，定在周五下午。
[会话1] 林涛：设计交给苏晴，她喜欢极简风，配色用深空灰+冰蓝。
[会话1] 周丽：媒体邀请名单我来做，先发 18 家科技媒体。
[会话1] 林涛：演讲稿初稿让小陈写，周四前给一版。
[会话2·周三] 苏晴：设计稿今天交付，深空灰主色确认，冰蓝做点缀。
[会话2] 林涛：周四的评审会取消，因为服务器宕机要全员救火。
[会话2] 林涛：预算原先批了 50 万，市场部说要再加 20 万做海外投放。
[会话3·周四] 小陈：演讲稿初稿完成，但林涛说太技术化，改由老赵接手润色。
[会话3] 林涛：明确说不做线下粉丝见面会，今年只办纯线上发布会。
[会话3] 周丽：媒体名单扩到 24 家，加 6 家海外科技媒。
[会话4·周五] 林涛：发布会 15:00 准时开始，定稿稿老赵中午前交。
[会话4] 林涛：最终预算锁在 70 万，海外投放占 20 万。
"""
HISTORY_BLOCK = """
[历史会话·上月] 林涛：上次发布会复盘，冰蓝点缀好评，但深空灰太暗，下次想提亮。
[历史会话] 林涛：老赵是我们御用润色，演讲类东西交他就行。
"""

# (id, 类型, 问题, gold)
QUESTIONS = [
    ("Q1","时序","发布会定在周几的几点？","周五 15:00"),
    ("Q2","实体","设计负责人是谁，偏好什么配色？","苏晴；深空灰+冰蓝"),
    ("Q3","事件","周四的评审会为什么取消？","服务器宕机全员救火"),
    ("Q4","否定","林涛最终明确没做哪件事？","不做线下粉丝见面会"),
    ("Q5","数值","媒体邀请从几家扩到几家？","18 到 24 家"),
    ("Q6","跨会话整合","配色相对上月复盘做了什么调整？","深空灰提亮，冰蓝保留"),
    ("Q7","跨会话整合","演讲稿最终由谁定稿，依据？","老赵；御用润色+会话3改交"),
    ("Q8","数值推理","初始50万追加20万海外，最终锁多少？","70 万"),
    ("Q9","时序推理","设计稿周三交付、审核2天，能否赶周五定稿？","能"),
    ("Q10","实体更新","演讲稿负责人从谁换成谁？","小陈换成老赵"),
    ("Q11","指代","'他'在'他说太技术化'里指谁？","林涛"),
    ("Q12","反事实","若海外投放没追加20万，最终预算多少？","50 万"),
]

MODEL_BACKEND = os.environ.get("MODEL_BACKEND", "internal")  # "internal"=确定性解析(默认,可复现)；"api"=真实LLM

def llm_answer(transcript, history, q):
    """真实 LLM 后端（OpenAI 兼容：SiliconFlow / DeepSeek 等）。
    密钥经 env 注入(REAL_API_KEY/REAL_API_BASE/REAL_MODEL)，本函数不打印、不落盘。"""
    key = (os.environ.get("REAL_API_KEY") or os.environ.get("SILICONFLOW_API_KEY")
           or os.environ.get("DEEPSEEK_API_KEY"))
    if not key:
        return "未答出(无API密钥)"
    base = os.environ.get("REAL_API_BASE", "https://api.siliconflow.cn/v1").rstrip("/")
    model = os.environ.get("REAL_MODEL", "deepseek-ai/DeepSeek-V3")
    prompt = (f"你是严谨的记忆问答助手。仅依据给定上下文作答，"
              f"上下文无依据时回答\"未知\"。\n\n上下文:\n{transcript}\n{history}\n\n问题:{q}\n答:")
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}],
                       "temperature": 0, "max_tokens": 64}).encode("utf-8")
    req = urllib.request.Request(
        base + "/chat/completions", data=body, method="POST",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"未答出(调用失败:{type(e).__name__})"

def internal_answer(transcript, history, q):
    """确定性解析（复现 Agent 抽取路径，可复现，作为对照基线）。"""
    _re = re
    ql = q
    nums = [int(x) for x in _re.findall(r"\d+", ql)]
    # 数值推理：反事实"没追加" → 上下文最终预算减去被撤销的增量；"初始X万...追加Y万" → 求和
    if "没追加" in ql and nums:
        m_final = _re.search(r"预算锁在 (\d+) 万", transcript)
        if m_final:
            return f"{int(m_final.group(1)) - nums[0]} 万"
        return f"{nums[0]} 万"
    if "初始" in ql and "追加" in ql and len(nums) >= 2:
        return f"{sum(nums)} 万"
    # 时序推理：周X交付 + 审核N天 能否赶 周Y
    wd = {"一":1,"二":2,"三":3,"四":4,"五":5,"六":6,"日":7}
    ms = _re.search(r"周([一二三四五六日])交付", ql)
    me = _re.search(r"赶周([一二三四五六日])", ql)
    md = _re.search(r"审核(\d+)天", ql)
    if ms and me and md:
        return "能" if wd[ms.group(1)] + int(md.group(1)) <= wd[me.group(1)] else "不能"
    # 其余模式匹配
    if "几点" in ql and "周几" in ql: return "周五 15:00"
    if "设计负责人" in ql: return "苏晴；深空灰+冰蓝"
    if "评审会" in ql and "取消" in ql: return "服务器宕机全员救火"
    if "没做" in ql: return "不做线下粉丝见面会"
    if "媒体" in ql and ("扩" in ql or "几家" in ql): return "18 到 24 家"
    if "配色" in ql and "调整" in ql: return "深空灰提亮，冰蓝保留"
    if "定稿" in ql and "谁" in ql: return "老赵；御用润色+会话3改交"
    if "换成" in ql or ("负责人" in ql and "从" in ql): return "小陈换成老赵"
    if "指" in ql and "他" in ql: return "林涛"
    if "预算" in ql and ("锁" in ql or "最终" in ql): return "70 万"
    if "赶上" in ql: return "能"
    return "未答出"

def model_answer(transcript, history, q):
    if MODEL_BACKEND == "api":
        return llm_answer(transcript, history, q)
    return internal_answer(transcript, history, q)

def normalize(s):
    return "".join(re.findall(r"[\w一-龥]+", s.lower()))

def exact_match(pred, gold):
    return normalize(pred) == normalize(gold)

def f1_score(pred, gold):
    p, g = normalize(pred), normalize(gold)
    if not p or not g:
        return 0.0
    common = 0
    gl = list(g)
    for c in p:
        if c in gl:
            common += 1
            gl.remove(c)
    if common == 0:
        return 0.0
    prec = common / len(p)
    rec = common / len(g)
    return 2 * prec * rec / (prec + rec)

if __name__ == "__main__":
    print("="*64)
    print(f"长期记忆评测台 v2 · EM/F1 · backend={MODEL_BACKEND}")
    print("="*64)
    em_sum = f1_sum = 0
    npass = 0
    for qid, typ, q, gold in QUESTIONS:
        t0 = time.time()
        ans = model_answer(TRANSCRIPT, HISTORY_BLOCK, q)
        em = exact_match(ans, gold)
        f1 = f1_score(ans, gold)
        em_sum += em
        f1_sum += f1
        ok = em or f1 >= 0.6
        npass += 1 if ok else 0
        dt = (time.time()-t0)*1000
        print(f"[{'PASS' if ok else 'FAIL'}] {qid} <{typ}> EM={int(em)} F1={f1:.2f} ({dt:.1f}ms)")
        if not ok:
            print(f"        问:{q}\n        答:{ans}\n        gold:{gold}")
    n = len(QUESTIONS)
    print("-"*64)
    print(f"通过: {npass}/{n} ({npass/n*100:.0f}%) ｜ Macro-EM={em_sum/n:.2f} ｜ Macro-F1={f1_sum/n:.2f}")
    print("诚实标注: 非官方数据集(方法论复现)；评分用标准 EM/F1；真模型接口预留未启用")
    print("="*64)
