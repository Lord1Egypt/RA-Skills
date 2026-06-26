#!/usr/bin/env python3
"""
Generate volume_02 chapters 4-7 to bridge the gap.
Continuity from existing Ch03_初战告捷.md to Ch08_决赛前夕.md.
"""
import json, os, re, sys, time, urllib.request
from pathlib import Path

DEEPSEEK_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
API_URL = "https://api.deepseek.com/v1/chat/completions"
MODEL = "deepseek-chat"
NOVEL_DIR = Path(os.environ.get("NOVEL_DIR", "."))
CHAPTER_DIR = NOVEL_DIR / "chapters" / "volume_02"
PLAN_PATH = NOVEL_DIR / "plans" / "volume_02_plan.json"
BIBLE_PATH = NOVEL_DIR / "bible.json"
QC_SCRIPT = NOVEL_DIR / "review" / "quality_check.py"

plan_data = json.loads(PLAN_PATH.read_text("utf-8"))
bible_data = json.loads(BIBLE_PATH.read_text("utf-8"))
CHAPTERS_INFO = {ch["number"]: ch for ch in plan_data["chapters"]}

SYSTEM_PROMPT = """你是一个优秀的长篇中文网文作者，擅长「蓝晶翻译体」风格的西幻写作。

## 核心风格要求：
1. **翻译体语感**：大量使用破折号（——）做句中停顿和场景过渡，营造翻译体特有的叙事韵律
2. **纯中文写作**：不使用任何英文词汇
3. **对话格式**：对话不使用引号，用破折号+直角引号——「对话内容」——这样写
4. **第三人称有限视角**：主要从主角「理查德」的视角出发
5. **段落控制**：段落不宜太长，多用短段和空行分隔不同场景/动作/情绪
6. **暖丽细腻的场景描写 + 幽默诙谐的对话 + 人物鲜活的动作细节**
7. **章节字数**：每章4000-5000汉字
8. **章末钩子**：每章结尾必须留悬念（问句/意外事件/紧急状况）

## 角色性格：
- 理查德（嘴硬乐观/天生蛮力/有正义感也有私心/18岁/灰港镇出身）
- 梅丽安（外冷内热/博学冷静/38岁/帝国魔法学院叛逃学者）
- 托德（朴实忠诚/爱喝酒/23岁/理查德发小）
- 卡斯特（铁冠城佣兵公会执事/观察力敏锐）
- 艾德温·灰石勋爵（铁冠城贵族/对龙血有企图）
- 莉安娜·灰石（勋爵之女/对理查德异常热情）
- 铁牙（北地佣兵/行踪可疑）

## 已有章节内容回顾：
第1-3章已经写完：理查德抵达铁冠城→注册佣兵→完成第一个战斗任务（变异野猪）→完成多件D级任务→升至C级佣兵→接取B级任务（北山矿场盗匪+商道狼群）→建立名声→报名参加铁冠城竞技场"""


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


def get_existing_chapter(num):
    for f in CHAPTER_DIR.glob(f"Ch{num:02d}_*.md"):
        return f.read_text("utf-8")
    return ""


def run_qc(path):
    import subprocess
    r = subprocess.run(["python3", str(QC_SCRIPT), str(path), "--json"],
                       capture_output=True, text=True, timeout=30)
    if r.returncode == 0 and r.stdout.strip():
        return json.loads(r.stdout)
    return None


def generate_chapter(chapter_num, prev_text):
    """Generate a chapter with continuity from prev_text."""
    info = CHAPTERS_INFO.get(chapter_num, {})
    title = info.get("title", "")
    summary = info.get("summary", "")
    scenes = info.get("scenes", 3)
    location = info.get("location", "")
    char_focus = info.get("character_focus", [])
    
    chars = bible_data.get("characters", {})
    char_summary = "\n".join([
        f"- {k}: {'、'.join(v.get('traits',[]))}"
        for k, v in chars.items()
    ])
    
    prompt = (
        f"# 第{chapter_num}章「{title}」\n\n"
        f"## 本章概要\n{summary}\n\n"
        f"## 场景数\n{scenes}个场景\n\n"
        f"## 地点\n{location}\n\n"
        f"## 重点角色\n{', '.join(char_focus)}\n\n"
        f"## 上一章结尾（关键连续性）\n{prev_text}\n\n"
        f"## 角色设定\n{char_summary}\n\n"
        f"---\n"
        f"请写出完整的第{chapter_num}章「{title}」文本。章末留悬念钩子。"
    )
    
    print(f"\n{'='*60}")
    print(f"Generating Ch{chapter_num:02d}: {title}...")
    sys.stdout.flush()
    
    text = call_deepseek([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ])
    
    if not text.startswith("# 第"):
        text = f"# 第{chapter_num}章 {title}\n\n---\n\n{text}"
    
    cn_count = count_chinese(text)
    text += f"\n\n【字数：约{cn_count}字】"
    
    safe_title = re.sub(r'[\\/:*?"<>|]', '', title)
    filename = f"Ch{chapter_num:02d}_{safe_title}.md"
    filepath = CHAPTER_DIR / filename
    filepath.write_text(text, "utf-8")
    print(f"  ✓ Saved: {filename} ({cn_count} Chinese chars)")
    sys.stdout.flush()
    
    # Quality check
    time.sleep(2)
    try:
        report = run_qc(filepath)
        if report:
            issues = report.get("issues", [])
            p0 = [i for i in issues if i.get("severity") == "P0"]
            p1 = [i for i in issues if i.get("severity") == "P1"]
            p2 = [i for i in issues if i.get("severity") == "P2"]
            print(f"  QC: P0={len(p0)}, P1={len(p1)}, P2={len(p2)}")
    except Exception as e:
        print(f"  QC error: {e}")
    
    return filepath


def main():
    # Continuity: read Ch03 ending
    ch03 = get_existing_chapter(3)
    prev_text = ch03[-1500:] if ch03 else "理查德完成了竞技场报名，准备迎接挑战。"
    
    chapters = list(range(4, 8))  # Ch04~Ch07
    results = {}
    
    for cn in chapters:
        try:
            path = generate_chapter(cn, prev_text)
            results[cn] = {"status": "ok", "path": str(path)}
            # Update prev_text for next chapter
            if path.exists():
                prev_text = path.read_text("utf-8")[-1500:]
        except Exception as e:
            print(f"  ✗ Ch{cn:02d} FAILED: {e}")
            import traceback; traceback.print_exc()
            results[cn] = {"status": "error", "error": str(e)}
        time.sleep(3)
    
    # Summary
    print(f"\n{'='*60}")
    print("COMPLETION REPORT (Ch04-Ch07):")
    total = 0
    for cn in chapters:
        p = Path(results.get(cn, {}).get("path", ""))
        if p.exists():
            t = p.read_text("utf-8")
            c = count_chinese(t)
            total += c
            print(f"  Ch{cn:02d}: {p.name} — {c}字")
        else:
            print(f"  Ch{cn:02d}: NOT WRITTEN")
    print(f"  Subtotal: {total} Chinese chars")
    print("Done.")

if __name__ == "__main__":
    main()
