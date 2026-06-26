#!/usr/bin/env python3
"""
Generate volume_02 chapters 2-7, plan-aligned.
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

STYLE_GUIDE = """
## 核心风格要求：
1. **翻译体语感**：大量使用破折号（——）做句中停顿和场景过渡
2. **纯中文写作**
3. **对话格式**：对话用破折号+直角引号——「对话内容」——写法
4. **第三人称有限视角**：主理查德
5. **段落不宜太长**，多用短段和空行
6. **暖丽细腻场景描写 + 幽默诙谐对话 + 人物鲜活**
7. **每章4000-5000汉字**
8. **章末留悬念钩子**

## 角色性格：
- 理查德（18岁/嘴硬乐观/天生蛮力/有正义感也有私心）
- 梅丽安（38岁/外冷内热/博学冷静/帝国魔法学院叛逃学者）
- 托德（23岁/朴实忠诚/爱喝酒/理查德发小）

## 已有章节：序章+Ch01
理查德从辉光城返回铁冠城，在梅丽安的秘密老屋安顿，次日前往佣兵公会注册，接取第一个任务（变异野猪清剿）。"""


def call_ds(messages, temp=0.75, max_tokens=8192, timeout=300):
    payload = json.dumps({
        "model": MODEL, "messages": messages,
        "temperature": temp, "max_tokens": max_tokens,
    }).encode("utf-8")
    req = urllib.request.Request(API_URL, data=payload, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_KEY}",
    })
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))["choices"][0]["message"]["content"]


def cn_count(text):
    return len([c for c in text if '\u4e00' <= c <= '\u9fff'])


def get_chapter(num):
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


def gen(num):
    info = CHAPTERS_INFO.get(num, {})
    title = info.get("title", "")
    summary = info.get("summary", "")
    scenes = info.get("scenes", 3)
    location = info.get("location", "")
    char_focus = info.get("character_focus", [])
    
    # Get previous chapter ending for continuity
    prev = ""
    for i in range(num-1, 0, -1):
        prev = get_chapter(i)
        if prev:
            prev = prev[-1500:]
            break
    
    chars = bible_data.get("characters", {})
    char_summary = "\n".join([
        f"- {k}: {'、'.join(v.get('traits',[]))}；{v.get('background','')[:60]}"
        for k, v in chars.items()
    ])
    
    prompt = (
        f"# 第{num}章「{title}」\n\n"
        f"## 本章概要\n{summary}\n\n"
        f"## 地点\n{location}\n\n"
        f"## 重点角色\n{', '.join(char_focus)}\n\n"
        f"## 上章结尾（连续性参考）\n{prev or '理查德初到铁冠城，刚注册成为D级佣兵。'}\n\n"
        f"## 角色设定\n{char_summary}\n\n"
        f"请写出完整的第{num}章「{title}」。格式：# 第X章 [标题]，空行，分隔线，正文。"
    )
    
    print(f"\n{'='*60}")
    print(f"Generating Ch{num:02d}: {title}...")
    sys.stdout.flush()
    
    text = call_ds([
        {"role": "system", "content": f"你是优秀长篇西幻网文作者，擅长蓝晶翻译体。" + STYLE_GUIDE},
        {"role": "user", "content": prompt},
    ])
    
    if not text.startswith("# 第"):
        text = f"# 第{num}章 {title}\n\n---\n\n{text}"
    
    cc = cn_count(text)
    text += f"\n\n【字数：约{cc}字】"
    
    stitle = re.sub(r'[\\/:*?"<>|]', '', title)
    fname = f"Ch{num:02d}_{stitle}.md"
    fpath = CHAPTER_DIR / fname
    fpath.write_text(text, "utf-8")
    print(f"  ✓ {fname} ({cc} Chinese chars)")
    sys.stdout.flush()
    
    time.sleep(2)
    try:
        qc = run_qc(fpath)
        if qc:
            issu = qc.get("issues", [])
            p0 = len([i for i in issu if i.get("severity")=="P0"])
            p1 = len([i for i in issu if i.get("severity")=="P1"])
            p2 = len([i for i in issu if i.get("severity")=="P2"])
            print(f"  QC: P0={p0}, P1={p1}, P2={p2}")
    except Exception as e:
        print(f"  QC err: {e}")
    
    return fpath


def fix_p0(text, num, issues):
    p0 = [i for i in issues if i.get("severity")=="P0"]
    if not p0:
        return text
    instrs = "\n".join([f"- {i.get('description','')}\n  建议: {i.get('suggestion','')}" for i in p0[:3]])
    try:
        fixed = call_ds([
            {"role": "system", "content": "修复章节P0问题后输出完整章节。"},
            {"role": "user", "content": f"修复以下P0问题，输出完整章节：\n{instrs}\n\n原文：\n{text[:7000]}"},
        ], temp=0.3, max_tokens=8192, timeout=180)
        if fixed and cn_count(fixed) > 1000 and "修复" not in fixed[:30]:
            return fixed
    except:
        pass
    return text


def main():
    chapters = list(range(2, 8))  # Ch02~Ch07
    results = {}
    
    for cn in chapters:
        try:
            path = gen(cn)
            results[cn] = {"status": "ok", "path": str(path)}
        except Exception as e:
            print(f"  ✗ Ch{cn:02d} FAILED: {e}")
            import traceback; traceback.print_exc()
            results[cn] = {"status": "error", "error": str(e)}
        time.sleep(3)
    
    print(f"\n{'='*60}")
    print("Ch02-Ch07 GENERATION REPORT:")
    total = 0
    for cn in chapters:
        p = Path(results.get(cn, {}).get("path", ""))
        if p.exists():
            t = p.read_text("utf-8")
            c = cn_count(t)
            total += c
            print(f"  Ch{cn:02d}: {p.name} — {c}字")
        else:
            print(f"  Ch{cn:02d}: FAILED ❌")
    print(f"\n  Total: {total} Chinese chars across 6 chapters")
    print("Done.")

if __name__ == "__main__":
    main()
