#!/usr/bin/env python3
"""
Continuity Check — 连通性补充与校验
- check: 章内子结构首尾3行连续性（时间词重叠）
- cross-chapter: 跨章承诺链检查（上一章尾的关键词是否在下一章头被续接）
- auto-fix: 生成过渡信息
"""
import json, sys, re
from pathlib import Path

# Windows 终端编码修复：强制 stdout 使用 UTF-8，避免 Git Bash 输出中文乱码
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


def check_continuity(chapter_dir, chapter, state_path):
    """章内子结构首尾3行连续性（时间词重叠）
    返回结构化问题列表: [{"file", "problem", "position", "severity", "suggestion"}, ...]

    智能路径：如果 chapter_dir 不是有效目录，自动从 state_path 推导：
      {state_path.parent.parent}/chapters/{chapter}
    """
    cd = Path(chapter_dir)
    if not cd.exists():
        # 从 state_path 自动推导
        fallback = Path(state_path).parent.parent / "chapters" / chapter
        if fallback.exists():
            print(f"[路径] chapter_dir \"{chapter_dir}\" 无效，自动推导为 {fallback}")
            cd = fallback
        else:
            print(f"[连通性] {chapter}: 目录不存在 (tried \"{chapter_dir}\" and \"{fallback}\")")
            return []
    files = sorted(cd.glob("S*.txt"))
    if not files:
        print(f"[连通性] {chapter}: 无子结构文件")
        return []

    result = []
    issues = []
    for i in range(1, len(files)):
        prev_content = files[i-1].read_text(encoding="utf-8-sig").strip()
        curr_content = files[i].read_text(encoding="utf-8-sig").strip()
        prev_lines = [l for l in prev_content.split("\n") if l.strip() and not re.match(rf'{chapter}S\d+', l.strip())]
        curr_lines = [l for l in curr_content.split("\n") if l.strip() and not re.match(rf'{chapter}S\d+', l.strip())]
        prev_tail = "\n".join(prev_lines[-3:]) if len(prev_lines) >= 3 else "\n".join(prev_lines)
        curr_head = "\n".join(curr_lines[:3]) if len(curr_lines) >= 3 else "\n".join(curr_lines)

        time_pattern = re.compile(r'(新元历|星期|周|上午|下午|晚上|清晨|中午|傍晚|深夜)')
        prev_times = time_pattern.findall(prev_tail)
        curr_times = time_pattern.findall(curr_head)

        time_ok = len(set(prev_times) & set(curr_times)) > 0

        # 角色连续性：在尾和头中检查角色名重叠
        # 用双字滑动窗口替代 {2,4} 贪婪匹配，避免"铁心说得对"吞掉"铁心"
        def char_bigrams(text):
            chars = re.findall(r'[\u4e00-\u9fff]', text)
            return set(chars[i] + chars[i+1] for i in range(len(chars)-1))
        prev_chars = char_bigrams(prev_tail)
        curr_chars = char_bigrams(curr_head)
        char_ok = len(prev_chars & curr_chars) > 0

        has_issue = not time_ok or not char_ok
        entry = {
            "from": files[i-1].stem,
            "to": files[i].stem,
            "prev_tail": prev_tail[:100],
            "curr_head": curr_head[:100],
            "time_overlap": time_ok,
            "char_overlap": char_ok
        }
        issues.append(entry)

        if has_issue:
            problems = []
            if not time_ok:
                problems.append("时间词无重叠")
            if not char_ok:
                problems.append("角色名无重叠")
            result.append({
                "file": f"{files[i-1].stem} → {files[i].stem}",
                "problem": "；".join(problems),
                "position": f"{files[i].stem} 开头3行",
                "severity": "HARD" if (not time_ok and not char_ok) else "SOFT",
                "suggestion": f"在{files[i].stem}开头补充时间定位或角色承接（当前文风不变）"
            })

    print(f"[连通性报告] {chapter}")
    for entry in issues:
        status = "[OK]" if entry["time_overlap"] else "[WARN]"
        status += "[角色OK]" if entry["char_overlap"] else "[角色WARN]"
        print(f"  {status} {entry['from']} -> {entry['to']}")
        print(f"    前段尾: {entry['prev_tail'][:60]}...")
        print(f"    后段头: {entry['curr_head'][:60]}...")

    sp = Path(state_path)
    if sp.exists():
        data = json.loads(sp.read_text(encoding="utf-8-sig"))
        for ch in data.get("chapters", []):
            if ch["id"] == chapter:
                ch["continuity_notes"] = issues
                break
        sp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[连通性] {chapter} 检查完成 ({len(issues)} 处, {len(result)} 个问题)")
    return result


def auto_fix(chapter_dir, chapter):
    """生成子结构间过渡信息"""
    cd = Path(chapter_dir)
    files = sorted(cd.glob("S*.txt"))
    transitions = []
    for i in range(1, len(files)):
        prev_content = files[i-1].read_text(encoding="utf-8-sig").strip()
        prev_lines = [l for l in prev_content.split("\n") if l.strip()]
        prev_tail = prev_lines[-1] if prev_lines else ""
        transitions.append({
            "from": files[i-1].stem,
            "to": files[i].stem,
            "prev_last_line": prev_tail
        })
    out_path = cd / f"_{chapter}_transitions.json"
    out_path.write_text(json.dumps(transitions, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[auto-fix] 过渡信息写入 {out_path}")
    return transitions


def _extract_keywords(data):
    """
    从 novel_state.json 动态提取关键词，无需硬编码。
    来源：
      1. characters[].name（角色名）
      2. technical_notes 的 key 和 value（技术概念）
      3. chapters[].overview（章概述中的话题词，≥2字非虚词）
    """
    import re
    kws = set()

    # 角色名
    for c in data.get("characters", []):
        name = c.get("name", "")
        if len(name) >= 2:
            kws.add(name)
        # 如果 name 包含其他角色名（如 "归元会散人"），
        # 取 members 内的具体名字
        if "members" in c:
            for m in c["members"]:
                mn = m.get("name", "")
                if len(mn) >= 2:
                    kws.add(mn)

    # 技术概念
    tn = data.get("technical_notes", {})
    for k, v in tn.items():
        if len(k) >= 2:
            kws.add(k)
        if len(v) >= 2:
            # 滑动窗口提取2-4字片段，避免整段中文被当单个关键词
            text = re.sub(r'[^\u4e00-\u9fff]', '', v)
            for wlen in range(4, 1, -1):
                for i in range(len(text) - wlen + 1):
                    kws.add(text[i:i+wlen])

    # 章概述
    for ch in data.get("chapters", []):
        ov = ch.get("overview", "")
        text = re.sub(r'[^\u4e00-\u9fff]', '', ov)
        for wlen in range(4, 1, -1):
            for i in range(len(text) - wlen + 1):
                kws.add(text[i:i+wlen])

    return kws


def cross_chapter(state_path, chapters_dir):
    """
    跨章承诺链检查（通用版，无硬编码）：
    从 novel_state.json 动态提取关键词，检测上章尾 vs 下章头的匹配度。
    """
    sp = Path(state_path)
    data = json.loads(sp.read_text(encoding="utf-8-sig"))
    chs = [c["id"] for c in data.get("chapters", []) if c.get("status") == "completed"]

    # 动态提取关键词
    kw_set = _extract_keywords(data)
    # 按长度降序排列（避免长词被短词的前缀覆盖）
    kw_list = sorted(kw_set, key=len, reverse=True)
    if not kw_list:
        print("[跨章检查] 无可用关键词（characters/technical_notes 为空）")
        return []
    key_pattern = re.compile('|'.join(re.escape(p) for p in kw_list))

    issues = []
    for i in range(len(chs) - 1):
        prev_ch = chs[i]
        next_ch = chs[i + 1]
        prev_dir = Path(chapters_dir) / prev_ch
        next_dir = Path(chapters_dir) / next_ch

        prev_files = sorted(prev_dir.glob("S*.txt"))
        if not prev_files:
            continue
        last_file = prev_files[-1]
        last_content = last_file.read_text(encoding="utf-8-sig").strip()
        last_lines = [l for l in last_content.split("\n") if l.strip() and not re.match(rf'{prev_ch}S\d+', l.strip())]
        prev_tail = "\n".join(last_lines[-3:]) if len(last_lines) >= 3 else "\n".join(last_lines)

        next_files = sorted(next_dir.glob("S*.txt"))
        if not next_files:
            continue
        first_file = next_files[0]
        first_content = first_file.read_text(encoding="utf-8-sig").strip()
        first_lines = [l for l in first_content.split("\n") if l.strip() and not re.match(rf'{next_ch}S\d+', l.strip())]
        next_head = "\n".join(first_lines[:3]) if len(first_lines) >= 3 else "\n".join(first_lines)

        tail_keys = set(key_pattern.findall(prev_tail))
        head_keys = set(key_pattern.findall(next_head))

        # 只报告实际缺失的语义关键词（排除单字/通用语气词）
        missing = tail_keys - head_keys
        missing = {w for w in missing if len(w) >= 2}

        print(f"\n--- {prev_ch} -> {next_ch} ---")
        print(f"  尾: {prev_tail[:80]}...")
        print(f"  头: {next_head[:80]}...")

        if missing:
            print(f"  [WARN] 未续接的承诺: {missing}")
            issues.append({
                "from_chapter": prev_ch,
                "to_chapter": next_ch,
                "prev_tail": prev_tail[:100],
                "next_head": next_head[:100],
                "unresolved_promises": list(missing)
            })
        else:
            print(f"  [OK] 承诺链完整")

    sp = Path(state_path)
    if sp.exists():
        data = json.loads(sp.read_text(encoding="utf-8-sig"))
        data["cross_chapter_check"] = issues
        sp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    if not issues:
        print("\n[跨章检查] 全部通过")
    else:
        print(f"\n[跨章检查] 发现 {len(issues)} 处断点")
        for iss in issues:
            print(f"  [WARN] {iss['from_chapter']} -> {iss['to_chapter']}: {iss['unresolved_promises']}")

    # 转为结构化结果（带 severity + suggestion）
    structured = []
    for iss in issues:
        missing_str = ", ".join(iss["unresolved_promises"][:5])
        structured.append({
            "file": f"{iss['from_chapter']} → {iss['to_chapter']}",
            "problem": f"上章承诺关键词 [{missing_str}] 未在 {iss['to_chapter']} 开头续接",
            "position": f"{iss['to_chapter']} 开头3行",
            "severity": "SOFT",
            "suggestion": f"在{iss['to_chapter']}开头通过叙事自然提及 [{missing_str}]"
        })

    return structured


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("用法:")
        print("  章内: python novel_continuity.py check <chapter_dir> <chapter> <state_path>")
        print("    → chapter_dir 可省略（用 . 占位），自动从 state_path 推导: {state_path}/../chapters/<chapter>")
        print("    → 示例: python novel_continuity.py check L02 <state_path>")
        print("  跨章: python novel_continuity.py cross-chapter <state_path> <chapters_dir>")
        print("  fix:  python novel_continuity.py auto-fix <chapter_dir> <chapter> <state_path>")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "check":
        check_continuity(sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd == "cross-chapter":
        cross_chapter(sys.argv[2], sys.argv[3])
    elif cmd == "auto-fix":
        auto_fix(sys.argv[2], sys.argv[3])
        if len(sys.argv) > 4:
            # 也跑个章内检查作为辅助
            check_continuity(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print(f"[错误] 未知命令: {cmd}")
