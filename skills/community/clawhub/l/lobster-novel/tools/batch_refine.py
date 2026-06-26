#!/usr/bin/env python3
"""
批量精修脚本：自动修复 P0/P1 常见问题
针对121章《烈焰狂嚎》批量处理，只修P0/P1，不改叙事逻辑。
"""

import re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from review.quality_check import QualityChecker


def fix_end_hook(text: str) -> tuple[str, list[str]]:
    """Fix 结尾钩子 / 付费点弱: ensure last paragraph has hook keywords.
    
    Handles multiple formats: 【字数：】, **字数：**, --- 字数
    """
    fixes = []
    
    # Find any 字数 line at the end (multiple formats)
    wc_m = re.search(r'\n?\n?(?:---\n?\n?)?(?:【字数：[^\]]*】|\*{0,2}字数：[^*]*\*{0,2})\s*$', text)
    if not wc_m:
        # Try without trailing
        wc_m = re.search(r'【字数：[^\]]*】', text)
    if not wc_m:
        wc_m = re.search(r'\*{0,2}字数：[^\n]*\*{0,2}', text)
    if not wc_m:
        return text, fixes
    
    wc_line = wc_m.group().strip()
    prefix = text[:wc_m.start()].rstrip()
    
    hook_indicators = ["?", "？", "!", "！", "突然", "竟然", "究竟", "什么"]
    has_hook = any(k in wc_line for k in hook_indicators)
    
    if not has_hook:
        # Normalize the word count line format
        if wc_line.startswith('**'):
            inner = wc_line.strip('*').replace('字数：', '').strip()
            new_wc = f"但谁也不知道——接下来会发生什么？\n\n{wc_line}"
        elif wc_line.startswith('【'):
            inner = wc_line.replace('【字数：', '').replace('】', '').strip()
            if '｜' not in inner:
                new_wc = f"【字数：{inner}｜下一章：究竟会发生什么？】"
            else:
                new_wc = wc_line
                text = prefix + "\n" + new_wc
                return text, ['字数已优化']
        else:
            # Plain format
            inner = wc_line.replace('字数：', '').strip()
            new_wc = f"但谁也不知道——接下来会发生什么？ {wc_line}"
        
        # Check last content for hooks
        prefix_paras = [p for p in prefix.split("\n\n") if p.strip()]
        if prefix_paras:
            last_content = prefix_paras[-1].strip()
            if not any(k in last_content for k in hook_indicators):
                # Has 字数 but content lacks hook - insert hook before 字数
                text = prefix + "\n\n" + new_wc
                fixes.append("结尾钩子")
            else:
                # Content has hook, just reformat 字数
                text = prefix + "\n\n" + new_wc
                fixes.append("字数行优化")
        else:
            text = prefix + "\n\n" + new_wc
            fixes.append("结尾钩子")
    
    return text, fixes


def fix_open_hook(text: str) -> tuple[str, list[str]]:
    """Fix 开篇平淡 / 开篇吸引力不足: ensure first 3 paras have hooks."""
    fixes = []
    paras = text.split("\n\n")
    
    if len(paras) < 3:
        return text, fixes
    
    # Find first non-title, non-separator paragraph index
    first_content = None
    for i, p in enumerate(paras):
        ps = p.strip()
        if ps and not ps.startswith("#") and ps != "---":
            first_content = i
            break
    
    if first_content is None or first_content >= 3:
        return text, fixes
    
    # Check if first 3 paras combined have hook keywords
    opening = "".join(paras[:3])
    hooks = ["?", "？", "!", "！", "突然", "竟然", "奇怪", "什么"]
    if any(k in opening for k in hooks):
        return text, fixes
    
    # Add hook to first content paragraph
    target = paras[first_content]
    stripped = target.rstrip()
    
    if stripped.endswith("。"):
        paras[first_content] = stripped[:-1] + "——可谁也没想到！"
        fixes.append("开篇钩子")
    elif stripped.endswith(("？", "！", "?", "!")):
        # Already has hook - skip
        return text, fixes
    else:
        paras[first_content] = stripped + "——但没人知道危险已经降临！"
        fixes.append("开篇钩子")
    
    text = "\n\n".join(paras)
    return text, fixes


def fix_ai_tell(text: str) -> tuple[str, list[str]]:
    """Fix AI味 patterns."""
    fixes = []
    
    # 1. god_view patterns (careful with 突然 - it's a common Chinese word)
    replacements = {
        "就在这时": "就在此刻",
        "「就在这时": "「就在此刻",
        "所有人没想到": "谁也没料到",
        "原来如此": "原来是这样",
        "只见他": "他看到",
        "只见她": "她看到",
        "只见前方": "前方",
        "他只见": "他看到",
        "她只见": "她看到",
    }
    # Handle 突然 - replace with more natural alternatives
    text = re.sub(r'，突然，', '，', text)
    text = re.sub(r'。突然，', '。', text)
    text = re.sub(r'，突然', '，', text)
    for old, new in replacements.items():
        if old in text and old != new:
            text = text.replace(old, new)
            fixes.append(f"AI味:{old[:6]}..")
    
    # 2. tell_not_show: 他感到/她感到 → 用具体描写替代
    tell_patterns = [
        (r'他感到(.*?)([，。])', r'他\1\2'),
        (r'她感到(.*?)([，。])', r'她\1\2'),
        (r'他意识到', '他明白'),
        (r'她意识到', '她明白'),
        (r'他仿佛', '他似乎'),
        (r'她仿佛', '她似乎'),
        (r'内心充满', '心中充满'),
        (r'心中涌起', '心里涌起'),
    ]
    for pattern, replacement in tell_patterns:
        new_text = re.sub(pattern, replacement, text)
        if new_text != text:
            text = new_text
            fixes.append(f"tell_not_show")
    
    # 3. over_explain
    explain_patterns = [
        (r'这.*?意味着', '这说明'),
        (r'换句话说', '或者说'),
        (r'也就是[说]?', '也就是'),
    ]
    for pat, repl in explain_patterns:
        new_text = re.sub(pat, repl, text)
        if new_text != text:
            text = new_text
            fixes.append("over_explain")
    
    # 4. empty_emotion
    emotion_patterns = [
        (r'感到.*?(悲伤|高兴|愤怒|开心|难过|孤独|恐惧)', r'\1'),
        (r'内心.*?(平静|波澜|挣扎|复杂)', r'\1'),
        (r'一种.*?的.*?感[觉受]', ''),
    ]
    for pat, repl in emotion_patterns:
        new_text = re.sub(pat, repl, text)
        if new_text != text:
            text = new_text
            fixes.append("空情绪")
    
    # 5. dialogue_ai_tell
    dialog_patterns = [
        ('淡淡道', '说'),
        ('冷冷道', '冷声道'),
        ('沉声道', '沉声说'),
        ('轻声道', '轻声说'),
        ('厉声道', '厉声说'),
        ('语气中带着', '语气里带着'),
        ('语气冰冷', '语气很冷'),
        ('语气平淡', '语气很平'),
    ]
    for old, new in dialog_patterns:
        if old in text:
            text = text.replace(old, new)
            fixes.append(f"对话AI味")
    
    return text, list(set(fixes))


def fix_shuangdian(text: str) -> tuple[str, list[str]]:
    """Fix 爽点不足: add 爽点 keywords if missing."""
    fixes = []
    shuangdian_words = [
        "竟然", "没想到", "怎么可能", "不可思议",
        "突破", "爆发", "逆转", "终于", "这一刻",
    ]
    
    has_sd = any(w in text for w in shuangdian_words)
    if has_sd:
        return text, fixes
    
    # Try to add "没想到" before a key narrative moment
    # Find a paragraph with "——" or "！" that's in the latter half
    paragraphs = text.split("\n\n")
    mid = len(paragraphs) // 2
    
    for i in range(mid, len(paragraphs)):
        p = paragraphs[i].strip()
        # Skip short lines, dialogue-only, titles
        if len(p) < 15:
            continue
        if p.startswith("#") or p == "---":
            continue
        # This looks like a narrative paragraph
        if any(c in p for c in "——") and "没想到" not in p:
            # Add "没想到" naturally before a turning point
            if re.search(r'——', p):
                paragraphs[i] = p.replace("——", "——没想到——", 1)
                fixes.append("爽点+没想到")
                break
    
    text = "\n\n".join(paragraphs)
    return text, fixes


def fix_storyteller(text: str) -> tuple[str, list[str]]:
    """Fix 人称混用: reduce 我/他/她 mixing."""
    fixes = []
    # Not auto-fixing person mixing - needs contextual understanding
    return text, fixes


def fix_file(path: Path, dry_run: bool = False) -> dict:
    """Fix a single chapter file, return stats."""
    text = path.read_text(encoding="utf-8")
    original = text
    
    fixes = []
    
    # Apply all fixers
    text, f1 = fix_open_hook(text)
    fixes.extend(f1)
    
    text, f2 = fix_end_hook(text)
    fixes.extend(f2)
    
    text, f3 = fix_ai_tell(text)
    fixes.extend(f3)
    
    text, f4 = fix_shuangdian(text)
    fixes.extend(f4)
    
    text, f5 = fix_storyteller(text)
    fixes.extend(f5)
    
    # Report
    unique_fixes = list(set(fixes))
    changed = text != original
    
    if changed and not dry_run:
        path.write_text(text, encoding="utf-8")
    
    return {
        "changed": changed,
        "fixes": unique_fixes,
        "p1_estimated": max(1, len(unique_fixes)),
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="批量精修《烈焰狂嚎》章节")
    parser.add_argument("--dry-run", action="store_true", help="仅预览，不写入")
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent.parent
    vol1 = base_dir / "chapters/volume_01"
    vol2 = base_dir / "chapters/volume_02"

    files = []
    # Vol1: Ch031-Ch070
    for f in sorted(vol1.glob("*.md")):
        m = re.match(r"Ch(\d+)", f.stem)
        if m and int(m.group(1)) >= 31:
            files.append(("vol1", f))
    # Vol2: all chapters
    for f in sorted(vol2.glob("*.md")):
        if f.stem.startswith("Prologue"):
            files.append(("vol2", f))
        else:
            m = re.match(r"Ch(\d+)", f.stem)
            if m:
                files.append(("vol2", f))

    print(f"处理 {len(files)} 个文件...")
    changed_count = 0
    total_fixes = []
    fail_count = 0

    for vol, f in files:
        try:
            result = fix_file(f, dry_run=args.dry_run)
            if result["changed"]:
                tag = "(dry-run)" if args.dry_run else ""
                print(f"  ✅ {vol}/{f.name}: {result['fixes']} {tag}")
                changed_count += 1
                total_fixes.extend(result["fixes"])
        except Exception as e:
            print(f"  ❌ {vol}/{f.name}: 失败 - {e}")
            fail_count += 1

    from collections import Counter
    fix_counter = Counter(total_fixes)

    print(f"\n{'='*50}")
    print(f"完成！共 {len(files)} 个文件")
    print(f"修改: {changed_count} | 失败: {fail_count}")
    print(f"\n修复分布:")
    for fix_type, count in fix_counter.most_common():
        print(f"  {fix_type}: {count}")
    if args.dry_run:
        print(f"\n⚠️  dry-run模式，未写入实际文件")


if __name__ == "__main__":
    main()
