#!/usr/bin/env python3
"""parse_outline.py - 从小说大纲解析出逐章prompt"""
import argparse, json, os, re, sys

CONSTRAINTS = """1. 纯中文！所有数字用中文写法(一、二、三十)，零阿拉伯数字零英文
2. 零AI标记词汇（"暗思涌起""心理描写""环境描写""命运齿轮"等禁止出现）
3. 禁止模板化结尾（"真正的危机才刚刚开始""未完待续"）
4. 直接输出正文，不输出说明
5. 字数必须12000+，忠于大纲"""

def parse_text(text):
    chs, cur, title, plot = {}, None, "", []
    for line in text.split('\n'):
        line = line.strip()
        m = re.match(r'(?:第|Chapter\s+)(\d+)[章节回]*(?:[：:\s]+(.*))?', line, re.IGNORECASE)
        if m:
            if cur and plot:
                chs[cur] = {"title": title, "plot": '\n'.join(plot)}
            cur = int(m.group(1)); title = m.group(2) or f"第{cur}章"; plot = []
        elif cur and line:
            plot.append(line)
    if cur and plot:
        chs[cur] = {"title": title, "plot": '\n'.join(plot)}
    return chs

def parse_json_outline(text):
    data = json.loads(text)
    d = data.get("chapters", data.get("volume", data))
    r = {}
    for k, v in d.items():
        try:
            r[int(k)] = v if isinstance(v, dict) else {"title": str(v), "plot": ""}
        except Exception:
            pass
    return r

def detect_format(text):
    if text.strip().startswith('{') or text.strip().startswith('['):
        return "json"
    if re.search(r'^#{1,3}\s+(?:第|Chapter)', text, re.MULTILINE):
        return "markdown"
    return "text"

def gen_prompt(n, info, prev=""):
    t = info.get("title", f"第{n}章"); p = info.get("plot", "")
    parts = [f"你是网文主笔，正在写第{n}章：{t}。"]
    if p:
        parts.append(f"\n【本章剧情】\n{p}")
    if prev:
        parts.append(f"\n【前章结尾】\n{prev}\n\n从结尾自然续写，不重复。")
    parts.append(f"\n【硬性约束】\n{CONSTRAINTS}")
    return '\n'.join(parts)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outline", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    with open(args.outline, 'r', encoding='utf-8') as f:
        text = f.read()
    fmt = detect_format(text)
    chs = parse_json_outline(text) if fmt == "json" else parse_text(text)
    if not chs:
        print("❌ 0章节"); sys.exit(1)
    print(f"✅ 解析 {len(chs)} 章（格式: {fmt}）")
    os.makedirs(args.output, exist_ok=True)
    for n, info in sorted(chs.items()):
        prompt = gen_prompt(n, info)
        fn = f"{n:04d}_{info.get('title', '章')}.txt"
        fn = re.sub(r'[<>:"/\\|?*]', '_', fn)
        with open(os.path.join(args.output, fn), 'w', encoding='utf-8') as f:
            f.write(prompt)
        print(f"  ✅ {fn}")
    out = {str(k): {"title": v["title"], "plot": v.get("plot", "")} for k, v in sorted(chs.items())}
    with open(os.path.join(args.output, "chapters.json"), 'w', encoding='utf-8') as f:
        json.dump({"chapters": out}, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 完成: {len(out)} 个prompt + chapters.json")

if __name__ == "__main__":
    main()
