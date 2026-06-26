#!/usr/bin/env python3
"""
parse_meeting.py -- 将会议/聊天记录解析为结构化待办事项。

用法:
    python parse_meeting.py --input <文本>
    python parse_meeting.py --input @文件路径
    python parse_meeting.py --interactive  （交互模式）

输出: 结构化会议摘要、待办事项、决策、风险和里程碑。
"""

import json, re, sys, argparse
from datetime import datetime, timedelta

# -- Chinese surnames --
SURNAMES = "王李张刘陈杨黄赵周吴徐孙马胡朱郭何罗高林郑梁谢唐许冯宋韩邓彭曾曹田萧潘袁蔡蒋余于杜叶程魏苏吕丁沈任姚卢傅钟崔伍廖谭翟熊纪舒屈项祝梁阮蓝闵席季麻强贾路娄危盛梅郭钱秦邱尹万常贺龚文"
CN = r"(?:\u5c0f[" + SURNAMES + r"]|[" + SURNAMES + r"][\u4e00-\u9fff]?)"
NAME = r"(?:" + CN + r"|[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)"

TASK_VERBS = "负责|完成|做|搞定|准备|整理|跟进|处理|写|制作|修改|查|检查|联系|通知|做好|安排|推进|发送|提交"

WEEKDAYS = {"周一":0,"礼拜一":0,"星期一":0,"周二":1,"礼拜二":1,"星期二":1,"周三":2,"礼拜三":2,"星期三":2,"周四":3,"礼拜四":3,"星期四":3,"周五":4,"礼拜五":4,"星期五":4,"周六":5,"礼拜六":5,"星期六":5,"周日":6,"礼拜天":6,"礼拜日":6,"星期日":6}
ENGDAYS = {"monday":0,"tuesday":1,"wednesday":2,"thursday":3,"friday":4,"saturday":5,"sunday":6}

def resolve_date(expr, base=None):
    if base is None: base = datetime.now()
    e = expr.strip()
    for k, d in {"今天":0,"今日":0,"明天":1,"明日":1,"后天":2,"後天":2,"大后天":3,"大後天":3,"昨天":-1,"昨日":-1,"前天":-2,"前日":-2}.items():
        if k in e: return (base+timedelta(days=d)).strftime("%Y-%m-%d")
    m = re.search(r"下个?(\w+)", e)
    if m:
        p = m.group(1)
        if "月" in p:
            mth = base.month+1; y = base.year
            if mth>12:
                mth=1
                y+=1
            return datetime(y, mth, min(base.day,28)).strftime("%Y-%m-%d")
        if "周" in p or "星期" in p:
            return (base+timedelta(days=(7-base.weekday()))).strftime("%Y-%m-%d")
        n = WEEKDAYS.get(p)
        if n is not None:
            d = (n-base.weekday())%7
            if d<=0:
                d+=7
            return (base+timedelta(days=d)).strftime("%Y-%m-%d")
    m = re.search(r"(?:这|这个)(\w+)", e)
    if m:
        n = WEEKDAYS.get(m.group(1))
        if n is not None:
            return (base+timedelta(days=(n-base.weekday())%7)).strftime("%Y-%m-%d")
    for k, n in WEEKDAYS.items():
        if k in e:
            d = (n-base.weekday())%7
            if d==0:
                d=7
            return (base+timedelta(days=d)).strftime("%Y-%m-%d")
    for k, n in ENGDAYS.items():
        if k in e.lower():
            d = (n-base.weekday())%7
            if d==0: d=7
            return (base+timedelta(days=d)).strftime("%Y-%m-%d")
    return None

# Patterns
TASK_A = re.compile(rf"({NAME})(?:.{{0,15}}?)(?:{TASK_VERBS})\s*(.+?)(?:[，。\.；！!;\n]|$)")
TASK_P = re.compile(rf"(.+?)(?:让|由|交给)\s*({NAME})\s*(?:来)?\s*(?:负责|做|完成|搞定)(?:[，。\.；！!;\n]|$)")
TASK_E = re.compile(rf"({NAME})\s+(?:will|should|must|needs to|has to|is responsible for|is in charge of)\s+(.+?)(?:[\.;!]|$)")
DL_P = re.compile(r"(?:截止|deadline|DDL|ddl|due|by|之前|前|以内)\s*[：: ]?\s*(.+?)(?=[，。\.；！;!]|$)")
DL_E = re.compile(r"(下周[一二三四五六日]?|下个月|明天|后天|今天|周[一二三四五六]|星期[一二三四五六日]|本周五|这周五|这个周五)(?:之前|前)?")

def deadline(sent):
    m = DL_P.search(sent)
    if m and resolve_date(m.group(1)): return resolve_date(m.group(1))
    m = DL_E.search(sent)
    if m and resolve_date(m.group(1)): return resolve_date(m.group(1))
    m = re.search(r"(?:by|before|due)\s+(.+?)(?:[\.;!]|$)", sent, re.I)
    if m and resolve_date(m.group(1)): return resolve_date(m.group(1))
    return None

def classify(s):
    if any(k in s for k in ["决定","确定","确认","同意","就按","批准","approved","agreed","confirmed"]): return "decision"
    if any(k in s for k in ["但","不过","担心","不确定","还没","没有","问题","风险","blocker","stuck","pending"]): return "risk"
    if re.search(r"(?:再|下周|下个月|周五|周[一二三四五六])\s*(?:确认|讨论|碰|看)", s): return "followup"
    if re.search(r"(?:负责|完成|做|搞定|will|should|must|needs to)", s): return "task"
    return "discussion"

def priority(s):
    if any(k in s for k in ["马上","赶紧","立刻","urgent","important","紧急","重要"]): return "P1"
    if any(k in s for k in ["有空","不着急","sometime","whenever"]): return "P3"
    return "P2"

def extract(text):
    tasks = []
    # Split on Chinese periods, exclamation marks, newlines, AND Chinese commas
    for sent in re.split(r"(?:[。！\n\r，]+|(?<=[\.!;])\s+)", text):
        sent = sent.strip()
        if not sent: continue
        m = TASK_A.search(sent)
        if m:
            p, t = m.group(1).strip(), m.group(2).strip()
            t = re.sub(r"[，。\.；！;!了）\)]$", "", t).strip()
            if p not in ("下周","本周","这周") and t:
                tasks.append({"person":p,"task":t,"deadline":deadline(sent) or "待确认","priority":priority(sent),"type":classify(sent),"source":sent})
                continue
        m = TASK_P.search(sent)
        if m:
            tp, pp = m.group(1).strip(), m.group(2).strip()
            tp = re.sub(r"^(那|好的|好\s*[,，]?\s*)", "", tp).strip()
            # If task part is just a pronoun / filler, skip (passive likely handled elsewhere)
            if tp and len(tp) > 1:
                tasks.append({"person":pp,"task":tp,"deadline":deadline(sent) or "待确认","priority":priority(sent),"type":classify(sent),"source":sent})
                continue
        m = TASK_E.search(sent)
        if m:
            p, t = m.group(1).strip(), re.sub(r"[\.;!]$","",m.group(2).strip())
            tasks.append({"person":p,"task":t,"deadline":deadline(sent) or "待确认","priority":priority(sent),"type":classify(sent),"source":sent})
    return tasks

def summary(text, tasks):
    topics = [k for k in ["数据","分析","报告","项目","产品","计划","实验","PPT","设计","开发","测试","客户"] if k in text]
    topic = "、".join(topics[:3]) or "相关工作"
    persons = set(t["person"] for t in tasks)
    person_str = ' | '.join(persons) if persons else ''
    decisions = [t["source"] for t in tasks if t["type"]=="decision"]
    return f"讨论了{topic}的安排与分工。{' 决定：'+'；'.join(decisions)+'。' if decisions else ''} {'（'+person_str+'）' if persons else ''}"

def format_output(text, tasks):
    u = [{"id":i,"person":t["person"],"task":t["task"],"deadline":t["deadline"],"priority":t["priority"]} for i,t in enumerate(tasks,1) if t["type"] in ("task","decision")]
    dec = []
    for t in tasks:
        if t["type"]=="decision" and t["source"] not in [d["source"] for d in tasks[:tasks.index(t)]]:
            dec.append(t["source"])
    ris = list(set(t["source"] for t in tasks if t["type"]=="risk"))
    fol = []
    for t in tasks:
        if t["type"]=="followup" and t["source"] not in fol: fol.append(t["source"])
    for s in re.split(r"[。！\n\r，]+", text):
        s = s.strip()
        if re.search(r"(?:再|下周|下个月|周五|周[一二三四五六])\s*(?:确认|讨论|碰|看)", s) and s not in fol:
            fol.append(s)
    return {"meeting_summary":summary(text,tasks),"todo_items":u,"decisions":dec,"follow_ups":fol,"risks":ris}

if __name__=="__main__":
    ap = argparse.ArgumentParser(description="解析会议记录为结构化待办事项")
    ap.add_argument("--input","-i"); ap.add_argument("--interactive","-t",action="store_true",help="交互模式：粘贴或输入文本，Ctrl+D 结束")
    ap.add_argument("--json","-j",action="store_true")
    args = ap.parse_args()
    text = None
    if args.input:
        if args.input.startswith("@"):
            with open(args.input[1:],encoding="utf-8") as f: text = f.read()
        else: text = args.input
    elif args.interactive: text = sys.stdin.read()
    else: ap.print_help(); sys.exit(1)
    if not text.strip(): print("未提供输入文本"); sys.exit(1)
    tasks = extract(text); r = format_output(text, tasks)
    if args.json: print(json.dumps(r,ensure_ascii=False,indent=2)); sys.exit(0)
    print("="*60)
    print("  会议摘要")
    print("="*60)
    print(f"  {r['meeting_summary']}")
    if r["todo_items"]:
        print()
        print("="*60)
        print("  待办事项")
        print("="*60)
        print(f"  {'负责人':<12} {'任务':<22} {'截止时间':<10} {'优先级'}")
        print(f"  {'─'*10:<12} {'─'*20:<22} {'─'*8:<10} {'─'*6}")
        for i in r["todo_items"]:
            owner = i["person"][:10]
            task = i["task"][:18]
            print(f"  {owner:<12} {task:<22} {i['deadline']:<10} {i['priority']}")
    if r["decisions"]:
        print()
        print("="*60)
        print("  决策事项")
        print("="*60)
        for d in r["decisions"]:
            print(f"  - {d}")
    if r["risks"]:
        print()
        print("="*60)
        print("  风险")
        print("="*60)
        for rk in r["risks"]:
            print(f"  - {rk}")
    if r["follow_ups"]:
        print()
        print("="*60)
        print("  里程碑")
        print("="*60)
        for f in r["follow_ups"]:
            print(f"  - {f}")
    if not tasks:
        print("\n  未检测到待办事项。")
    print("="*60)
