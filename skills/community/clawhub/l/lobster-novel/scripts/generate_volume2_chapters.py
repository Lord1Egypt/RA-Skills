#!/usr/bin/env python3
"""
Generate volume_02 chapters 2-11 with quality checks.
Uses DeepSeek API directly.
"""
import json, os, re, sys, time, urllib.request
from pathlib import Path

# ── Config ──────────────────────────────────────────────────
DEEPSEEK_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
API_URL = "https://api.deepseek.com/v1/chat/completions"
MODEL = "deepseek-chat"  # DeepSeek V4 Flash
NOVEL_DIR = Path(os.environ.get("NOVEL_DIR", "."))
CHAPTER_DIR = NOVEL_DIR / "chapters" / "volume_02"
PLAN_PATH = NOVEL_DIR / "plans" / "volume_02_plan.json"
BIBLE_PATH = NOVEL_DIR / "bible.json"
QC_SCRIPT = NOVEL_DIR / "review" / "quality_check.py"

# ── Load reference files ────────────────────────────────────
plan_data = json.loads(PLAN_PATH.read_text("utf-8"))
bible_data = json.loads(BIBLE_PATH.read_text("utf-8"))
CHAPTERS_INFO = {ch["number"]: ch for ch in plan_data["chapters"]}

# Read existing chapters
EXISTING_TEXTS = {}
for f in sorted(CHAPTER_DIR.glob("*.md")):
    EXISTING_TEXTS[f.stem] = f.read_text("utf-8")

# ── System Prompt (蓝晶翻译体风格) ───────────────────────────
SYSTEM_PROMPT = """你是一个优秀的长篇中文网文作者，擅长「蓝晶翻译体」风格的西幻写作。

## 核心风格要求：
1. **翻译体语感**：大量使用破折号（——）做句中停顿和场景过渡，营造翻译体特有的叙事韵律
2. **纯中文写作**：不使用任何英文词汇
3. **对话格式**：对话不使用引号，用破折号+直角引号——「对话内容」——这样写
4. **第三人称有限视角**：主要从主角「理查德」的视角出发，偶尔可切换到「梅丽安」
5. **段落控制**：段落不宜太长，多用短段和空行分隔不同场景/动作/情绪
6. **描写风格**：暖丽细腻的场景描写 + 幽默诙谐的对话 + 人物鲜活的动作细节
7. **章末钩子**：每章结尾必须留悬念（问句/意外事件/紧急状况），让读者想看下一章
8. **章节字数**：每章4000-5000汉字

## 角色性格：
- 理查德（嘴硬乐观/天生蛮力/有正义感也有私心/会弹鲁特琴但弹得很烂）
- 梅丽安（外冷内热/博学冷静/背负家族仇恨/帝国魔法学院叛逃学者）
- 托德（朴实忠诚/爱喝酒/理查德发小）

## 剧情要求：
1. 推进角色弧：理查德从不熟练使用龙血到逐渐掌控
2. 每章至少包含：场景描写 + 对话互动 + 动作/战斗场面 + 情感觉知
3. 注意前后照应和伏笔埋设
4. 保持DND 5e战斗风格感"""


def call_deepseek(messages, temp=0.75, max_tokens=8192, timeout=300):
    payload = json.dumps({
        "model": MODEL,
        "messages": messages,
        "temperature": temp,
        "max_tokens": max_tokens,
    }).encode("utf-8")
    req = urllib.request.Request(
        API_URL, data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPSEEK_KEY}",
        })
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"]


def count_chinese(text):
    return len([c for c in text if '\u4e00' <= c <= '\u9fff'])


def get_continuity(chapter_num):
    """Get end of previous chapter or existing files"""
    prev_num = chapter_num - 1
    # Check if previous chapter was already written
    for f in sorted(CHAPTER_DIR.glob(f"Ch{prev_num:02d}_*.md")):
        text = f.read_text("utf-8")
        return text[-1000:]
    return ""


def get_chapter_text(chapter_num):
    """Get full text of an existing chapter"""
    for f in sorted(CHAPTER_DIR.glob(f"Ch{chapter_num:02d}_*.md")):
        return f.read_text("utf-8")
    return ""


def run_quality_check(chapter_path):
    import subprocess
    result = subprocess.run(
        ["python3", str(QC_SCRIPT), str(chapter_path), "--json"],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode == 0 and result.stdout.strip():
        return json.loads(result.stdout)
    return None


def fix_p0_issues(text, chapter_num, issues):
    p0 = [i for i in issues if i.get("severity") == "P0"]
    if not p0:
        return text
    
    instructions = []
    for i in p0[:5]:
        desc = i.get("description", "")
        suggestion = i.get("suggestion", "")
        instructions.append(f"- 问题: {desc}\n  建议: {suggestion}")
    
    fix_prompt = (
        f"以下是第{chapter_num}章质量检查发现的P0问题，请修复。\n"
        + "\n".join(instructions) +
        "\n\n输出完整的修复后章节文本，保留原标题、风格和叙事节奏。"
    )
    try:
        fixed = call_deepseek([
            {"role": "system", "content": "你是一个专业网文编辑。直接输出修复后的完整章节文本，不要额外说明。"},
            {"role": "user", "content": f"{fix_prompt}\n\n原文：\n{text[:7000]}"},
        ], temp=0.3, max_tokens=8192, timeout=180)
        if fixed and len(fixed) > 1000 and "修复" not in fixed[:50]:
            return fixed
    except Exception as e:
        print(f"    Fix failed: {e}")
    return text


def generate_chapter(chapter_num):
    info = CHAPTERS_INFO.get(chapter_num, {})
    title = info.get("title", "")
    summary = info.get("summary", "")
    location = info.get("location", "")
    char_focus = info.get("character_focus", [])
    scenes = info.get("scenes", 3)
    
    # Read continuity from previous chapter
    prev_text = get_continuity(chapter_num)
    
    # Bible characters
    chars = bible_data.get("characters", {})
    char_summary = "\n".join([
        f"- {k}: {'、'.join(v.get('traits',[]))}；背景：{v.get('background','')[:80]}"
        for k, v in chars.items()
    ])
    
    # Build the generation prompt
    user_prompt = (
        f"# 第{chapter_num}章「{title}」\n\n"
        f"## 本章概要\n{summary}\n\n"
        f"## 场景数\n{scenes}个场景\n\n"
        f"## 地点\n{location}\n\n"
        f"## 重点角色\n{', '.join(char_focus)}\n\n"
        f"## 上章结尾（连续性参考）\n{prev_text}\n\n"
        f"## 角色设定\n{char_summary}\n\n"
        f"---\n"
        f"请写出完整的第{chapter_num}章「{title}」文本。标题格式：# 第X章 [标题]，然后空行、分隔线、正文。章末留悬念钩子。"
    )
    
    print(f"\n{'='*60}")
    print(f"Generating Ch{chapter_num:02d}: {title}...")
    sys.stdout.flush()
    
    text = call_deepseek([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ], temp=0.75, max_tokens=8192, timeout=300)
    
    # Ensure proper format
    if not text.startswith("# 第"):
        text = f"# 第{chapter_num}章 {title}\n\n---\n\n{text}"
    
    cn_count = count_chinese(text)
    text += f"\n\n【字数：约{cn_count}字】"
    
    # Save
    safe_title = re.sub(r'[\\/:*?"<>|]', '', title)
    filename = f"Ch{chapter_num:02d}_{safe_title}.md"
    filepath = CHAPTER_DIR / filename
    filepath.write_text(text, "utf-8")
    print(f"  ✓ Saved: {filename} ({cn_count} Chinese chars)")
    sys.stdout.flush()
    
    # Quality check
    time.sleep(1)
    try:
        report = run_quality_check(filepath)
        if report:
            issues = report.get("issues", [])
            scores = report.get("scores", {})
            p0 = [i for i in issues if i.get("severity") == "P0"]
            p1 = [i for i in issues if i.get("severity") == "P1"]
            p2 = [i for i in issues if i.get("severity") == "P2"]
            print(f"  QC: P0={len(p0)}, P1={len(p1)}, P2={len(p2)} | Scores: {scores.get('综合','?')}/100")
            
            if p0:
                print(f"  🔧 Fixing {len(p0)} P0 issues...")
                sys.stdout.flush()
                fixed = fix_p0_issues(text, chapter_num, issues)
                if fixed and fixed != text and count_chinese(fixed) > 1000:
                    filepath.write_text(fixed, "utf-8")
                    cn2 = count_chinese(fixed)
                    print(f"  ✓ Re-saved ({cn2} chars)")
                    time.sleep(1)
                    r2 = run_quality_check(filepath)
                    if r2:
                        p0a = len([i for i in r2.get("issues", []) if i.get("severity") == "P0"])
                        print(f"  QC after fix: P0={p0a}")
                else:
                    print(f"  ⚠ Fix produced invalid result, keeping original")
        else:
            print(f"  QC: No report")
    except Exception as e:
        print(f"  QC error: {e}")
    
    return filepath


def main():
    chapters = list(range(2, 12))
    results = {}
    
    for cn in chapters:
        try:
            path = generate_chapter(cn)
            results[cn] = {"status": "ok", "path": str(path)}
        except Exception as e:
            print(f"  ✗ Ch{cn:02d} FAILED: {e}")
            import traceback
            traceback.print_exc()
            results[cn] = {"status": "error", "error": str(e)}
        time.sleep(3)
    
    print(f"\n{'='*60}")
    print("COMPLETION REPORT:")
    print(f"{'='*60}")
    total_chars = 0
    for cn in chapters:
        r = results.get(cn, {})
        if r.get("status") == "ok":
            p = Path(r["path"])
            if p.exists():
                t = p.read_text("utf-8")
                c = count_chinese(t)
                total_chars += c
                print(f"  Ch{cn:02d}: {p.name} — {c}字 ✅")
            else:
                print(f"  Ch{cn:02d}: File not found ❌")
        else:
            print(f"  Ch{cn:02d}: {r.get('error')} ❌")
    print(f"\n Total: {total_chars} Chinese characters across {len(chapters)} chapters")
    
    # Save manifest
    manifest = {
        "volume": 2,
        "chapters_written": [cn for cn in chapters if results.get(cn, {}).get("status") == "ok"],
        "total_chinese_chars": total_chars,
        "results": {str(k): v["status"] for k, v in results.items()},
    }
    manifest_path = CHAPTER_DIR / ".generation_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), "utf-8")
    print(f"\nManifest saved: {manifest_path}")
    print(f"\nDone.")

if __name__ == "__main__":
    main()
