#!/usr/bin/env python3
"""
Hermes AGI Supervisor - 核心执行引擎
自动分解模糊指令为可执行任务，并监督执行闭环
"""
import json
import sys
import os
import re
from datetime import datetime

HERMES_DIR = os.path.expanduser("~/.hermes")
TASKS_DIR = os.path.join(HERMES_DIR, "tasks")
os.makedirs(TASKS_DIR, exist_ok=True)

TEMPLATE_DB = {
    "赚钱": [
        ("目标定义", "明确核心赚钱目标和衡量标准", "SMART目标:具体/可衡量/可达成/相关/有时限"),
        ("竞品调研", "在3个平台搜索同类成功案例并整理", "平台/标题/粉丝数/变现方式,各≥10条"),
        ("最小可行产品", "设计MVP方案(最小可交付版本)", "含目标用户/核心功能/上线时间/预期收益"),
        ("推广计划", "制定推广节奏和渠道分配", "含渠道/预算/时间节点/预期ROI"),
        ("数据复盘", "定期收集关键数据并分析", "含曝光/转化率/收入/用户反馈"),
    ],
    "职场": [
        ("任务拆解", "将大目标拆为可执行的日/周任务", "每周任务≤7条,每条可独立交付"),
        ("周报生成", "自动生成结构化工作周报", "含本周完成/下周计划/风险点/资源需求"),
        ("会议纪要", "整理会议核心结论和待办事项", "含决议/负责人/截止时间/行动项"),
        ("晋升规划", "制定3-6个月能力提升计划", "含技能差距/学习资源/里程碑"),
    ],
    "内容创作": [
        ("选题策划", "生成5个符合定位的内容选题", "每个含:标题/角度/核心观点/目标人群"),
        ("文案撰写", "按结构写完整内容(开头/正文/结尾)", "开头:3秒吸引;正文:逻辑清晰;结尾:有CTA"),
        ("标签优化", "选取最佳发布标签组合", "1个主标签+4个辅标签,说明理由"),
        ("数据复盘", "分析内容表现并提出改进建议", "含曝光/完播率/互动率/转化率"),
    ],
    "学习": [
        ("知识点拆解", "将大主题拆为3个可学的小主题", "每个含:定义+例子+练习题"),
        ("复习计划", "制定艾宾浩斯记忆复习表", "生成1/3/7/14/30天复习节点"),
        ("输出整理", "将输入内容转化为可分享笔记", "格式:标题/要点/感悟/行动项"),
    ]
}

TASK_COUNTER_FILE = os.path.join(HERMES_DIR, "counter.json")

def get_counter():
    if os.path.exists(TASK_COUNTER_FILE):
        with open(TASK_COUNTER_FILE) as f:
            return json.load(f)
    return {"seq": 0}

def inc_counter():
    c = get_counter()
    c["seq"] += 1
    with open(TASK_COUNTER_FILE, "w") as f:
        json.dump(c, f)
    return c["seq"]

def detect_category(text):
    t = text.lower()
    if any(k in t for k in ["赚钱", "副业", "创业", "收入", "项目", "粉丝", "账号", "变现", "推广"]): return "赚钱"
    if any(k in t for k in ["抖音", "小红书", "视频", "内容", "文案", "笔记", "发帖", "TikTok", "快手"]): return "内容创作"
    if any(k in t for k in ["工作", "职场", "上班", "任务", "报告", "会议", "晋升", "老板"]): return "职场"
    return "学习"

def decompose(raw_input, category=None):
    cat = category or detect_category(raw_input)
    templates = TEMPLATE_DB.get(cat, TEMPLATE_DB["学习"])
    task_id = f"HERMES-{datetime.now().strftime('%m%d')}-{inc_counter():03d}"
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    subtasks = []
    for i, (title, desc, criteria) in enumerate(templates, 1):
        subtasks.append({
            "id": f"{task_id}-{i}",
            "title": title,
            "description": desc,
            "done_criteria": criteria,
            "status": "pending",
            "reward": 10,
            "penalty": 5,
            "quality_bonus": 20,
            "quality_penalty": 10
        })

    task = {
        "id": task_id,
        "raw_input": raw_input,
        "category": cat,
        "status": "decomposed",
        "created_at": now,
        "completed_at": None,
        "subtasks": subtasks,
        "score": {"total": 0, "base": 0, "bonus": 0},
        "penalty_log": []
    }

    task_file = os.path.join(TASKS_DIR, f"{task_id}.json")
    with open(task_file, "w", encoding="utf-8") as f:
        json.dump(task, f, ensure_ascii=False, indent=2)

    index_file = os.path.join(HERMES_DIR, "index.json")
    if os.path.exists(index_file):
        with open(index_file) as f: index = json.load(f)
    else:
        index = {"tasks": []}
    index["tasks"].insert(0, {"id": task_id, "file": task_file, "category": cat})
    index["tasks"] = index["tasks"][:100]
    with open(index_file, "w") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    return task

def score_task(task_file, completed_ids, failed_ids):
    with open(task_file, encoding="utf-8") as f:
        task = json.load(f)

    base = len(completed_ids) * 10 - len(failed_ids) * 5
    quality_bonus = 20 if len(failed_ids) == 0 and len(completed_ids) >= len(task["subtasks"]) * 0.8 else 0
    total = base + quality_bonus

    for st in task["subtasks"]:
        st["status"] = "completed" if st["id"] in completed_ids else ("failed" if st["id"] in failed_ids else "pending")

    task["score"] = {"total": total, "base": base, "bonus": quality_bonus}
    task["completed_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    with open(task_file, "w", encoding="utf-8") as f:
        json.dump(task, f, ensure_ascii=False, indent=2)

    status = "excellent" if quality_bonus > 0 else ("good" if base >= 10 else ("partial" if base > 0 else "failed"))
    return {"task_id": task["id"], "base_score": base, "quality_bonus": quality_bonus, "total": total, "status": status, "task_file": task_file}

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "decompose"
    if cmd == "decompose":
        text = sys.argv[2] if len(sys.argv) > 2 else ""
        result = decompose(text)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif cmd == "score":
        task_file = sys.argv[2]
        completed = json.loads(sys.argv[3]) if len(sys.argv) > 3 else []
        failed = json.loads(sys.argv[4]) if len(sys.argv) > 4 else []
        print(json.dumps(score_task(task_file, completed, failed), ensure_ascii=False))
    elif cmd == "list":
        index_file = os.path.join(HERMES_DIR, "index.json")
        if os.path.exists(index_file):
            with open(index_file) as f: print(f.read())
        else:
            print("[]")
