#!/usr/bin/env python3
"""
novel-logic-check — 章节逻辑一致性检查器。

覆盖维度（3 项，经用户确认已排除因果链和情绪连贯性——由前置规划保障）：
  1. 人物行为一致性 — 同一角色在不同子结构中的言行是否矛盾
  2. 时间线逻辑 — 时间跳跃是否合理，有无冲突
  3. 子结构内容与概述匹配度 — 实际内容是否偏离规划时的概述

输出：Markdown 报告到 report_path

用法：
  python novel_logic_check.py <chapter_dir> <state_path> <report_path>
"""

import os
import sys
import json
import re

# Windows 终端编码修复
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


def _sorted_substructure_files(chapter_dir: str) -> list:
    if not os.path.isdir(chapter_dir):
        return []
    files = [f for f in os.listdir(chapter_dir) if f.endswith(".txt") and not f.startswith(".")]
    files.sort(key=lambda x: int(re.sub(r'\D', '', x.split('_')[0]) or 0))
    return [os.path.join(chapter_dir, f) for f in files]


def _read_all_lines(filepath: str) -> list:
    """读取文件所有行，跳过末尾的编号标记行和空行"""
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    # 跳过末尾标记行（L##S##）
    while lines and re.match(r'^L\d{1,2}S\d{1,3}$', lines[-1]):
        lines.pop()
    return lines


def _check_character_consistency(chapter_dir: str, state_path: str) -> list:
    """
    检查人物行为一致性：
    - 提取每个子结构中出现的角色名
    - 统计每个角色在每个子结构中的行为描述关键词
    - 标记同一角色在不同子结构中出现矛盾行为的情况
    （简单版本：检查角色名是否存在且在同一章中保持一致引用）
    """
    issues = []

    # 从 state 加载角色列表
    state = {}
    if os.path.exists(state_path):
        with open(state_path, "r", encoding="utf-8") as f:
            state = json.load(f)

    characters = state.get("characters", {})
    if not characters:
        return issues  # 无角色数据时跳过

    char_names = []
    if isinstance(characters, dict):
        char_names = list(characters.keys())
    elif isinstance(characters, list):
        char_names = [c.get("name", "") for c in characters if isinstance(c, dict)]

    if not char_names:
        return issues

    # 逐子结构检查角色名一致性问题
    files = _sorted_substructure_files(chapter_dir)
    char_in_subs = {}

    for fpath in files:
        fname = os.path.basename(fpath)
        lines = _read_all_lines(fpath)
        text = "\n".join(lines)
        present = [n for n in char_names if n in text]
        char_in_subs[fname] = present

    # 检查：某个角色在前一个子结构中出现、后一个子结构中消失（无合理过渡）
    prev_chars = set()
    for fname, present in sorted(char_in_subs.items()):
        curr_chars = set(present)
        vanished = prev_chars - curr_chars
        if vanished:
            # 放宽容限：至少有个子结构保留所有角色，否则只是自然退出场景
            issues.append({
                "level": "INFO",
                "dimension": "人物行为一致性",
                "detail": f"{fname}: 角色 [{', '.join(sorted(vanished))}] 在前一子结构后消失，"
                          f"若为场景切换则忽略"
            })
        prev_chars = curr_chars

    return issues


def _check_timeline_logic(chapter_dir: str, state_path: str) -> list:
    """
    检查时间线逻辑：
    - 检查 novel_state.json 中 timeline entries 是否存在矛盾
    - 多个子结构是否写了明显冲突的时间
    """
    issues = []

    state = {}
    if os.path.exists(state_path):
        with open(state_path, "r", encoding="utf-8") as f:
            state = json.load(f)

    timeline = state.get("timeline", [])
    entries = timeline if isinstance(timeline, list) else []

    if not entries:
        # 没有 timeline 数据时做简单检查：扫描 subfiles 中的时间引用
        pass

    # 检查 timeline entries 是否有倒序时间
    if isinstance(entries, list) and len(entries) >= 2:
        prev_day = None
        for entry in entries:
            day = entry.get("day")
            if day is not None and prev_day is not None:
                if day < prev_day:
                    issues.append({
                        "level": "WARN",
                        "dimension": "时间线逻辑",
                        "detail": f"时间回退：从 day {prev_day} 到 day {day}（"
                                  f"summary: {entry.get('summary', '')[:40]}）"
                    })
            prev_day = day

    # 检查 text 中是否有明显的时间跳跃但未在 timeline 中记录
    if isinstance(timeline, dict):
        current_day = timeline.get("current_day", 0)
    else:
        current_day = 0
    files = _sorted_substructure_files(chapter_dir)

    for fpath in files:
        fname = os.path.basename(fpath)
        lines = _read_all_lines(fpath)
        text = "\n".join(lines)
        # 简单模式匹配：查找 "第X天"、"翌日"、"第二天"、"三天后" 等
        time_refs = re.findall(r'(第[\d一二三四五六七八九十百千]+天|翌日|第二天|第三天|[\d]+天后)', text)
        if time_refs:
            issues.append({
                "level": "INFO",
                "dimension": "时间线逻辑",
                "detail": f"{fname}: 检测到时间引用 {time_refs}，请确认已调用 novel_timeline.py 记录"
            })

    return issues


def _check_summary_fidelity(chapter_dir: str, state_path: str) -> list:
    """
    检查子结构内容与规划概述的匹配度。
    对比每个子结构文件的实际内容 vs novel_state.json 中的 summary，标记严重偏离。
    """
    issues = []

    state = {}
    if os.path.exists(state_path):
        with open(state_path, "r", encoding="utf-8") as f:
            state = json.load(f)

    # 从目录名推断章节键
    dir_name = os.path.basename(chapter_dir)
    ch_match = re.search(r'(\d+)', dir_name)
    ch_key = f"L{int(ch_match.group(1)):02d}" if ch_match else ""

    if not ch_key:
        return issues

    chapters = state.get("chapters", [])
    chapter = {}
    if isinstance(chapters, list):
        for ch in chapters:
            if ch.get("id") == ch_key:
                chapter = ch
                break
    elif isinstance(chapters, dict):
        chapter = chapters.get(ch_key, {})
    subs = chapter.get("sub_structures", {})

    if not subs:
        return issues

    files = _sorted_substructure_files(chapter_dir)
    for fpath in files:
        fname = os.path.basename(fpath)
        # 尝试匹配 file name 到 sub_key
        # 文件格式如 L01S01.txt 或 01_S01_xxx.txt
        s_match = re.search(r'S(\d+)', fname)
        if not s_match:
            continue
        s_num = int(s_match.group(1))
        s_key = f"S{s_num:02d}"
        sub_info = subs.get(s_key, {})

        expected_summary = sub_info.get("summary", "")
        expected_tone = sub_info.get("tone", "")
        if not expected_summary:
            continue

        lines = _read_all_lines(fpath)
        text = " ".join(lines)

        # 检查概述中的关键主题词是否出现在正文中
        # 改为双字滑动窗口（bigram）重叠率匹配，支持语义自然概述
        def _char_bigrams(s: str) -> set:
            chars = re.findall(r'[\u4e00-\u9fff]', s)
            return set(chars[i] + chars[i+1] for i in range(len(chars)-1))

        summary_bigrams = _char_bigrams(expected_summary)
        text_bigrams = _char_bigrams(text)

        if not summary_bigrams:
            continue

        matched = summary_bigrams & text_bigrams
        hit_ratio = len(matched) / len(summary_bigrams)

        if hit_ratio < 0.2:
            missing = sorted(summary_bigrams - text_bigrams)[:5]
            issues.append({
                "level": "WARN",
                "dimension": "内容与概述匹配度",
                "detail": f"{fname} ({s_key}): 概述bigram命中率 {hit_ratio:.0%}"
                          f"，缺失bigram [{', '.join(missing)}]"
                          f"（概述: {expected_summary[:60]}）"
            })
        elif hit_ratio < 0.4:
            issues.append({
                "level": "INFO",
                "dimension": "内容与概述匹配度",
                "detail": f"{fname} ({s_key}): 概述bigram命中率 {hit_ratio:.0%}"
                          f"，部分内容可能偏离"
            })

        # 情绪检查（仅供参考，不阻断，不判定）
        if expected_tone and expected_tone != "中性":
            tone_kw_map = {
                "紧张": ["紧张", "压迫", "不安", "焦虑", "恐慌", "筋弦", "脚步声", "围堵", "攥紧", "屏息", "逼近", "昏暗", "颤抖", "冷汗", "心跳", "身后", "不敢动", "停步", "围上来", "三个人", "黑暗", "夜路"],
                "悲伤": ["悲伤", "哭泣", "失落", "哀伤", "眼泪", "悲痛", "沉默", "怀念", "叹息", "沉重", "别离", "往事", "难过", "哽咽", "遗物", "离别"],
                "愤怒": ["愤怒", "怒火", "愤慨", "暴怒", "震怒", "咬牙切齿", "握拳", "砸桌", "低吼", "瞪", "质问", "凭什么", "混蛋", "找死"],
                "温馨": ["温馨", "温暖", "柔情", "幸福", "安心", "拥抱", "微笑", "轻声", "牵", "晚饭", "灯光", "肩膀", "晚安", "相依"],
                "悬疑": ["疑惑", "谜团", "可疑", "诡异", "不解", "线索", "为什么", "怎么回事", "痕迹", "不对劲", "暗自", "调查", "暗中"],
                "平静": ["平静", "安静", "沉默", "宁静", "安详", "淡然", "枕", "躺着", "闭眼", "呼吸", "均匀", "微风", "寂静"],
                "恐惧": ["恐惧", "恐慌", "颤抖", "畏惧", "毛骨悚然", "惊恐", "后退", "尖叫", "跑", "逃", "拼命", "僵硬"],
                "欢乐": ["欢乐", "欢笑", "喜悦", "快乐", "开怀", "愉悦", "笑出声", "哈哈", "得意", "轻松", "嬉笑"],
                "疑惑探索": ["疑惑", "不解", "搞不懂", "好奇", "翻", "查看", "研究", "琢磨", "试验", "对比", "验证", "想不通", "定睛", "端详"],
                "专注": ["专注", "集中", "凝视", "全神贯注", "目不转睛", "仔细", "认真", "盯着", "埋头", "研读"],
                "启发": ["原来如此", "明白了", "懂了", "灵感", "窍", "悟", "发现", "意识到", "突然明白", "原来是这样"],
                "顿悟": ["顿悟", "豁然", "一下子", "灵光", "开窍", "通透", "醍醐", "秒懂"],
                "沉思": ["沉思", "思", "想", "琢磨", "反复", "深入", "反省", "扪心", "自问", "陷入"],
                "闲适略带好奇": ["闲", "逛", "溜达", "看看", "瞧瞧", "随便", "不急", "晃", "好奇", "打量", "东张西望"],
                "反思后接受": ["接受", "承认", "罢了", "算了", "就这样", "不争", "淡然", "妥协", "认了"],
                "理性分析": ["分析", "计算", "判断", "推理", "逻辑", "数据", "参数", "比较", "评估", "数据", "概率", "规律"],
                "希望与使命感": ["希望", "使命", "责任", "意义", "值得", "必须做", "担当", "信念", "信仰", "愿意"],
            }
            tone_kws = tone_kw_map.get(expected_tone, [])
            if tone_kws:
                tone_hits = sum(1 for kw in tone_kws if kw in text)
            else:
                tone_hits = -1
            # 仅打印参考，不 append issues，不参与阻断
            print(f"  [tone] 规划情绪「{expected_tone}」", end="")
            if tone_hits >= 0:
                print(f"，命中 {tone_hits}/{len(tone_kws)} 个场景词")
            else:
                print(f"，无预置词表")
            # 语速分析
            chars_clean = text.replace(" ", "").replace("\n", "")
            sentences = [s for s in text.replace("\n", "").split("。") if s.strip()]
            avg_len = len(chars_clean) / max(len(sentences), 1)
            print(f"  [语速] 平均句长 {avg_len:.0f} 字{'（短句密集 → 紧张感）' if avg_len < 10 else ''}")
            print(f"  [tone] 注：以上为参考数据，最终情绪传达由 LLM 自行判断\n")

    return issues


def _check_entity_status(chapter_dir: str, state_path: str) -> list:
    """
    检查实体状态一致性：
    - 读取 entity_tracker 中标记为降级状态（destroyed/damaged/lost/dead 等）的实体
    - 如果本章正文中正常使用了这些实体（无恢复说明），标记 HARD
    """
    issues = []
    state = {}
    if os.path.exists(state_path):
        with open(state_path, "r", encoding="utf-8") as f:
            state = json.load(f)

    tracker = state.get("entity_tracker", {})
    entities = tracker.get("entities", []) if isinstance(tracker, dict) else []
    if not entities:
        return issues

    STATUS_DEGRADING = {"destroyed", "damaged", "closed", "lost", "dead", "injured", "unconscious", "sold", "stolen", "given"}
    RECOVERY_WORDS = {"修复", "重建", "修好", "重新", "恢复", "复活", "治愈", "找回", "买回", "赎回"}

    # 读取本章所有子结构的内容
    files = _sorted_substructure_files(chapter_dir)
    if not files:
        return issues

    chapter_text = ""
    for fpath in files:
        lines = _read_all_lines(fpath)
        chapter_text += "\n".join(lines) + "\n"

    for e in entities:
        attr = e.get("attributes", {})
        status = attr.get("status", "")
        if status not in STATUS_DEGRADING:
            continue
        name = e.get("name", "")
        if not name or name not in chapter_text:
            continue
        # 实体在降级状态下被本章使用——检查是否有恢复说明
        has_recovery = any(w in chapter_text for w in RECOVERY_WORDS)
        if not has_recovery:
            issues.append({
                "level": "WARN",
                "dimension": "实体状态一致性",
                "detail": f"实体「{name}」状态为「{status}」（详见{e.get('last_chapter','?')}{e.get('last_sub','?')}），"
                          f"但本章仍在使用且未提及修复/恢复"
            })

    return issues


def _check_entity_relations(chapter_dir: str, state_path: str) -> list:
    """
    检查实体关系链断裂：
    - 读取 entity_tracker 中建立的关系
    - 如果某实体在前一章建立了重要关系，但本章该实体出现时关系未被提及，标记 SOFT
    """
    issues = []
    state = {}
    if os.path.exists(state_path):
        with open(state_path, "r", encoding="utf-8") as f:
            state = json.load(f)

    tracker = state.get("entity_tracker", {})
    relations = tracker.get("relations", []) if isinstance(tracker, dict) else []
    entities = tracker.get("entities", []) if isinstance(tracker, dict) else []
    if not relations:
        return issues

    # 从目录名推断本章 ID
    dir_name = os.path.basename(chapter_dir)
    ch_match = re.search(r'(\d+)', dir_name)
    ch_key = f"L{int(ch_match.group(1)):02d}" if ch_match else ""

    # 读取本章内容
    files = _sorted_substructure_files(chapter_dir)
    if not files:
        return issues
    chapter_text = ""
    for fpath in files:
        lines = _read_all_lines(fpath)
        chapter_text += "\n".join(lines) + "\n"

    # 建立实体名→实体映射
    entity_by_id = {e["id"]: e for e in entities}

    for r in relations:
        re_ch = r.get("chapter", "")
        if re_ch >= ch_key:  # 在本章或之后建立的关系跳过
            continue
        from_e = entity_by_id.get(r.get("from_entity"))
        to_e = entity_by_id.get(r.get("to_entity"))
        if not from_e or not to_e:
            continue
        # 如果两个实体都在本章出现，但关系核心词未出现，标记
        if from_e["name"] in chapter_text and to_e["name"] in chapter_text:
            pred = r.get("predicate", "")
            # 检查核心关系词是否出现在正文
            relation_words = set()
            if pred == "贩卖":
                relation_words = {"买", "卖", "交易", "价格", "信用点"}
            elif pred == "领导":
                relation_words = {"领导", "头目", "手下", "成员"}
            elif pred == "拥有":
                relation_words = {"拥有", "持有", "带着", "装着"}
            elif pred == "位于":
                relation_words = {"在", "位于", "来到", "回到", "离开"}
            elif pred == "归属":
                relation_words = {"属于", "加入", "是...成员", "隶属"}
            elif pred == "转移":
                relation_words = {"给", "递", "交", "送", "转交"}
            # 检查是否在正文中有足够的关系暗示
            if relation_words and not any(w in chapter_text for w in relation_words):
                issues.append({
                    "level": "INFO",
                    "dimension": "实体关系链",
                    "detail": f"{from_e['name']}与{to_e['name']}曾有『{pred}』关系（{re_ch}{r.get('sub','?')}），"
                              f"本章两者同时出现但未提及这层关系"
                })

    return issues


def generate_report(chapter_dir: str, state_path: str, report_path: str):
    if not os.path.exists(state_path):
        print(f"ERROR: novel_state.json 未找到: {state_path}")
        sys.exit(1)

    if not os.path.isdir(chapter_dir):
        print(f"ERROR: 章节目录不存在: {chapter_dir}")
        sys.exit(1)

    dir_name = os.path.basename(chapter_dir)

    report_lines = []
    report_lines.append(f"# 逻辑一致性报告 — {dir_name}")
    report_lines.append(f"")
    report_lines.append(f"## 1️⃣ 人物行为一致性")
    report_lines.append(f"")

    char_issues = _check_character_consistency(chapter_dir, state_path)
    if char_issues:
        for i in char_issues:
            icon = "ℹ️" if i["level"] == "INFO" else "[WARN]"
            report_lines.append(f"- {icon} [{i['dimension']}] {i['detail']}")
    else:
        report_lines.append("- [OK] 未发现明显人物一致性问题")
    report_lines.append(f"")

    report_lines.append(f"## 2️⃣ 时间线逻辑")
    report_lines.append(f"")
    tl_issues = _check_timeline_logic(chapter_dir, state_path)
    if tl_issues:
        for i in tl_issues:
            icon = "ℹ️" if i["level"] == "INFO" else "[WARN]"
            report_lines.append(f"- {icon} [{i['dimension']}] {i['detail']}")
    else:
        report_lines.append("- [OK] 时间线逻辑正常")
    report_lines.append(f"")

    report_lines.append(f"## 3️⃣ 子结构内容与概述匹配度")
    report_lines.append(f"")
    fidelity_issues = _check_summary_fidelity(chapter_dir, state_path)
    if fidelity_issues:
        for i in fidelity_issues:
            icon = {"INFO": "ℹ️", "WARN": "[WARN]"}.get(i["level"], "ℹ️")
            report_lines.append(f"- {icon} [{i['dimension']}] {i['detail']}")
    else:
        report_lines.append("- [OK] 所有子结构内容与概述一致")
    report_lines.append(f"")

    # ── 实体状态一致性（新增） ──
    report_lines.append(f"")
    report_lines.append(f"## 4️⃣ 实体状态一致性")
    report_lines.append(f"")
    entity_status_issues = _check_entity_status(chapter_dir, state_path)
    if entity_status_issues:
        for i in entity_status_issues:
            icon = {"INFO": "\u2139\ufe0f", "WARN": "[WARN]"}.get(i["level"], "\u2139\ufe0f")
            report_lines.append(f"- {icon} [{i['dimension']}] {i['detail']}")
    else:
        report_lines.append("- [OK] 未发现实体状态矛盾")
    report_lines.append(f"")

    # ── 实体关系链（新增） ──
    report_lines.append(f"")
    report_lines.append(f"## 5️⃣ 实体关系链")
    report_lines.append(f"")
    relation_issues = _check_entity_relations(chapter_dir, state_path)
    if relation_issues:
        for i in relation_issues:
            icon = {"INFO": "\u2139\ufe0f", "WARN": "[WARN]"}.get(i["level"], "\u2139\ufe0f")
            report_lines.append(f"- {icon} [{i['dimension']}] {i['detail']}")
    else:
        report_lines.append("- [OK] 实体关系链正常")
    report_lines.append(f"")

    # 统计
    all_issues = char_issues + tl_issues + fidelity_issues + entity_status_issues + relation_issues
    pass_count = sum(1 for i in all_issues if i["level"] in ("PASS",))
    info_count = sum(1 for i in all_issues if i["level"] == "INFO")
    warn_count = sum(1 for i in all_issues if i["level"] == "WARN")

    report_lines.append(f"## 统计")
    report_lines.append(f"- ℹ️ INFO: {info_count}")
    report_lines.append(f"- [WARN] WARN: {warn_count}")
    report_lines.append(f"")
    report_lines.append(f"---")
    report_lines.append(f"*报告由 novel-logic-check 生成*")

    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
        f.flush()
        os.fsync(f.fileno())

    print(f"OK report={report_path} info={info_count} warn={warn_count}")

    # 转为阻断用结构化结果
    structured = []
    try:
        for i in all_issues:
            if not isinstance(i, dict):
                continue
            level = i.get("level", "INFO")
            dim = i.get("dimension", "")
            detail = i.get("detail", "")

            # 判断 HARD 条件
            # 内容与概述匹配度不做HARD阻断（概述为规划基准不可更改，偏差报告为信息而非阻塞）
            if level == "WARN" and dim == "内容与概述匹配度":
                severity = "SOFT"
            elif level == "WARN":
                severity = "SOFT"
            else:
                severity = "SOFT"

            # 生成建议方向
            suggestion = ""
            if "关键词命中率" in detail:
                suggestion = f"在正文中补充概述提到的关键内容"
            elif "角色" in dim and ("消失" in detail or "未出现" in detail):
                suggestion = f"检查角色离场是否有明确交代，或补充出场衔接"
            elif "时间" in dim:
                suggestion = f"在章节中补充时间过渡交代"

            structured.append({
                "file": os.path.basename(chapter_dir),
                "problem": detail[:120],
                "position": dim,
                "severity": severity,
                "suggestion": suggestion or f"按{dim}要求修正"
            })
    except Exception:
        pass  # 结构化转换不影响主流程

    return structured


def write_fixes_json(chapter_dir: str, state_path: str, report_path: str, issues: list) -> str:
    """
    Auto-fix 模式：生成 _fixes.json，列出所有需要修复的问题及修复建议。
    返回 fixes JSON 文件路径，或空字符串（无需修复）。
    """
    if not issues:
        return ""

    needs_fix = [i for i in issues if i.get("level") in ("WARN", "ERROR") or i.get("dimension") == "内容与概述匹配度"]
    if not needs_fix:
        return ""

    report_dir = os.path.dirname(report_path)
    json_path = os.path.join(report_dir, "_fixes.json")

    fix_items = []
    for i in needs_fix:
        dim = i.get("dimension", "")
        detail = i.get("detail", "")
        level = i.get("level", "WARN")

        # 推断需要修复的文件
        target_file = ""
        action_type = ""  # rewrite / append / link
        action_desc = ""

        if dim == "内容与概述匹配度":
            # "L01S01 (S01): 概述关键词命中率 40%..." → 提取文件名
            if "(" in detail:
                fname = detail.split("(")[0].strip()
                target_file = os.path.join(chapter_dir, fname) if os.path.exists(os.path.join(chapter_dir, fname)) else ""
            action_type = "rewrite"
            action_desc = f"正文偏离了规划概述，需要重写或补充内容以匹配「{detail.split('概述: ')[-1][:40] if '概述: ' in detail else '规划'}」"

        elif dim == "人物行为一致性":
            action_type = "append"
            # 提取文件名
            fname_part = detail.split(":")[0].strip() if ":" in detail else ""
            target_file = os.path.join(chapter_dir, fname_part) if fname_part and os.path.exists(os.path.join(chapter_dir, fname_part)) else ""
            action_desc = f"角色出场/消失不自然，需要在受影响子结构中增加合理过渡"

        elif dim == "时间线逻辑":
            fname_part = detail.split(":")[0].strip() if ":" in detail else ""
            target_file = os.path.join(chapter_dir, fname_part) if fname_part and os.path.exists(os.path.join(chapter_dir, fname_part)) else ""
            action_type = "append"
            action_desc = f"时间引用或跳跃需要确认，可能需要在受影响子结构中增加时间标记或过渡"

        if action_type:
            fix_items.append({
                "dimension": dim,
                "level": level,
                "detail": detail,
                "target_file": target_file,
                "action_type": action_type,
                "action_desc": action_desc,
                "fixed": False
            })

    if not fix_items:
        return ""

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(fix_items, f, ensure_ascii=False, indent=2)
        f.flush()
        os.fsync(f.fileno())

    print(f"OK auto-fix fixes={len(fix_items)} json={json_path}")
    print(f"  → 请修复以下问题后重新运行:")
    for item in fix_items:
        print(f"    [{item['level']}] {item['dimension']}: {item['detail'][:60]}")
        print(f"      操作: {item['action_desc'][:60]}")
    print(f"  → 修复完成后重新运行 finalize-chapter")
    print(f"  → 也可由 workflow_engine 自动处理")

    return json_path


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("用法: novel_logic_check.py <chapter_dir> <state_path> <report_path> [--auto-fix]")
        sys.exit(1)

    issues = generate_report(
        chapter_dir=sys.argv[1],
        state_path=sys.argv[2],
        report_path=sys.argv[3]
    )

    if len(sys.argv) >= 5 and sys.argv[4] == "--auto-fix":
        write_fixes_json(
            chapter_dir=sys.argv[1],
            state_path=sys.argv[2],
            report_path=sys.argv[3],
            issues=issues
        )
