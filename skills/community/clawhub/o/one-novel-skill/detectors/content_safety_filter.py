#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
one-novel-skill 内容安全过滤器

用法:
  python content_safety_filter.py --input 正文/第001章.txt [--json]

等级:
  PASS    无风险
  WARN    低风险（建议检查）
  FLAG    中风险（必须修改）
  BLOCK   高风险（不可发布）
"""

import sys, re, json
from pathlib import Path


SAFETY_P0 = [
    "分裂国家","颠覆政权","鼓吹独立","抹黑英烈",
    "泄露国家机密","恐怖袭击","极端主义","煽动仇恨",
    "恋童","幼女","幼男",
    "制作冰毒","海洛因制作","注射毒品","毒品配方",
    "真实事件改编","真人真事",
]

SAFETY_P1 = [
    r"裸露[的着地]体",r"一丝不挂",r"[裸赤]身",r"胴体",
    r"性[感交爱事行]",r"[淫荡猥亵]",
    r"抚摸[着]?[他她]的[胸乳臀腿]",
    r"进入[了他她]的身体",r"插入",r"抽送",r"呻吟",r"娇喘",
    r"血肉模糊",r"肠子流出",r"肢解",r"碎尸",r"凌迟",r"开膛破肚",
    r"吸毒",r"吸毒过程",r"嗑药",r"摇头丸",r"K粉",
    r"未成年",
]

SAFETY_P2 = [
    r"强奸",r"强暴",r"轮奸",r"迷奸",
    r"毒品",r"贩毒",r"制毒",r"黑社会",r"黑帮",
    r"贩卖人口",r"诈骗集团",r"裸贷",r"传销",
    r"自杀",r"自残",r"自虐",r"邪教",r"洗脑",
]

# 上下文豁免名单：以下非敏感语境中降低匹配敏感等级
CONTEXT_WHITELIST = {
    "裸身": ["地面","岩石","山体","土地","土石","树根","钢筋","管道","电线"],
    "插入": ["图片","文件","数据","目录","钥匙","插头","接口","芯片","槽位","卡槽"],
    "呻吟": ["病","就医","医院","受伤","摔倒","疼痛","救护"],
    "吸毒": ["反","禁","戒","救","防"],
    "自残": ["反","禁","戒","救","防","防止"],
}

NEGATION_TERMS = [
    "反对","禁止","打击","痛恨","严惩","防止","预防",
    "拒绝","抵制","严禁","杜绝",
    "绝不","不屑于","唾弃","谴责","揭露","检举",
    "严厉打击","依法查处",
    "拒不","否认","驳斥","整治","扫除",
]

def has_negation_near(text, pos, kw_len):
    start = max(0, pos - 30)
    context = text[start:pos + kw_len + 10]
    return any(neg in context for neg in NEGATION_TERMS)

def check_safety(text):
    issues = []; severity = "PASS"
    for w in SAFETY_P0:
        idx = 0
        while True:
            pos = text.find(w, idx)
            if pos == -1:
                break
            # P0 关键词也做否定词豁免（防止批判性语境被封杀）
            if has_negation_near(text, pos, len(w)):
                issues.append({"level":"WARN","match":w})
                if severity not in ("BLOCK","FLAG"): severity = "WARN"
            else:
                issues.append({"level":"BLOCK","match":w})
                severity = "BLOCK"
            idx = pos + 1
    for pat in SAFETY_P1:
        m = re.search(pat,text)
        if m:
            match_text = m.group(0)
            # 语境感知检查：CONTEXT_WHITELIST + 未成年特殊处理
            if match_text == "未成年":
                context_start = max(0, m.start() - 40)
                context_end = min(len(text), m.end() + 40)
                ctx = text[context_start:context_end]
                protective_terms = ["保护","救助","关爱","防止","预防","保障","维权","救",
                    "学校","教育","学生","老师","家长","义务","成长","健康",
                    "法","制度","规范","引导","课","班","学"]
                matched = [t for t in protective_terms if t in ctx]
                if len(matched) >= 2:  # 收紧: 需要至少2个保护词同时命中
                    issues.append({"level":"WARN","match":match_text[:25]})
                    if severity not in ("BLOCK","FLAG"): severity = "WARN"
                    continue
            # 通用语境豁免：匹配关键词后40字范围内有豁免词则降级
            whitelisted = False
            for kw, safe_terms in CONTEXT_WHITELIST.items():
                if kw in match_text:
                    context_start = max(0, m.start() - 20)
                    context_end = min(len(text), m.end() + 40)
                    ctx = text[context_start:context_end]
                    if any(t in ctx for t in safe_terms):
                        whitelisted = True
                        break
            if whitelisted:
                continue  # 豁免，跳过此匹配
            issues.append({"level":"FLAG","match":match_text[:25]})
            if severity != "BLOCK": severity = "FLAG"
    def _check_whitelist_local(m, text):
        """检查匹配上下文是否命中豁免词（局部函数，避免与内联重复）"""
        match_text = m.group(0)
        for kw, safe_terms in CONTEXT_WHITELIST.items():
            if kw in match_text:
                ctx_start = max(0, m.start() - 20)
                ctx_end = min(len(text), m.end() + 40)
                ctx = text[ctx_start:ctx_end]
                if any(t in ctx for t in safe_terms):
                    return True
        return False

    for pat in SAFETY_P2:
        m = re.search(pat,text)
        if m:
            if _check_whitelist_local(m, text):
                continue  # 豁免，跳过
            issues.append({"level":"WARN","match":m.group(0)[:25]})
            if severity not in ("BLOCK","FLAG"): severity = "WARN"
    return severity, issues


def run_safety(text, title="未知"):
    severity, issues = check_safety(text)
    tc = sum(1 for c in text if "\u4e00"<=c<="\u9fff")
    sev_map = {"PASS":"无风险","WARN":"低风险(建议检查)","FLAG":"中风险(必须修改)","BLOCK":"高风险(不可发布)"}
    print(f"\n{'='*50}")
    print(f"  内容安全过滤 文件:{title} 字数:{tc}")
    print(f"{'='*50}")
    print(f"  结果: [{severity}] {sev_map.get(severity,'?')}")
    if issues:
        for iss in issues: print(f"    {iss['match']} [{iss['level']}]")
        if severity=="BLOCK": print(f"  !! 阻断: 发现P0红线，删除后再发布")
        elif severity=="FLAG": print(f"  !! 警告: 发现P1中风险，发布前需修改")
        else: print(f"  !! 提示: 建议人工复核")
    else:
        print(f"  OK 未检测到红线内容")
    print(f"{'-'*50}\n")
    return {"severity":severity,"total_issues":len(issues),"issues":issues}

def main():
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--input","-i",required=True)
    p.add_argument("--json",action="store_true")
    p.add_argument("--chapter","-c")
    a = p.parse_args()
    ip = Path(a.input)
    if not ip.exists(): print(f"[ERR] 文件不存在: {ip}"); sys.exit(1)
    with open(ip,"r",encoding="utf-8",errors="ignore") as f: t = f.read()
    r = run_safety(t, a.chapter or ip.stem)
    if a.json: print(json.dumps(r,ensure_ascii=False,indent=2))

if __name__=="__main__": main()
