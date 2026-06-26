#!/usr/bin/env python3
import argparse, json, os, sys
from pathlib import Path

def load_article(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def format_wechat(text):
    lines = []
    for p in text.split('\n\n'):
        p = p.strip()
        if p.startswith('#'):
            lines.append(p)
        else:
            line, words = "", list(p)
            for w in words:
                if len(line.encode('utf-8')) > 60:
                    lines.append(line)
                    line = w
                else:
                    line += w
            if line: lines.append(line)
        lines.append("")
    return "\n".join(lines)

def format_xiaohongshu(text):
    lines = ["✨ 精彩内容 ✨", ""]
    for p in text.split('\n\n')[:5]:
        p = p.strip()
        if not p.startswith('#'):
            lines.append(p[:200] + ("..." if len(p) > 200 else ""))
            lines.append("")
    lines.append("#干货 #分享 #笔记")
    return "\n".join(lines)

def format_zhihu(text):
    lines = []
    for p in text.split('\n\n'):
        p = p.strip()
        if p.startswith('#'):
            lines.append(p)
        else:
            if len(p) > 100 and "。" in p:
                s = p.split("。")[0] + "。"
                if len(s) > 20:
                    p = f"**{s[:20]}**{s[20:]}{p[len(s):]}"
            lines.append(p)
        lines.append("")
    return "\n".join(lines)

def format_douyin(text):
    lines = ["🔥 精彩 🔥", ""]
    for i, p in enumerate([p.strip() for p in text.split('\n\n') if not p.startswith('#')][:3], 1):
        lines.append(f"{i}. {p[:50]}")
        lines.append("")
    lines.append("👇 关注获取更多！")
    lines.append("#干货 #分享")
    return "\n".join(lines)

def main():
    p = argparse.ArgumentParser(description="OmniPublisher - 一键多平台内容适配")
    p.add_argument("input", help="文章文件")
    p.add_argument("--platforms", default="wechat,xiaohongshu,zhihu,douyin")
    p.add_argument("--output-dir", default=".")
    args = p.parse_args()

    if not os.path.exists(args.input):
        print(f"❌ 不存在: {args.input}")
        sys.exit(1)

    platforms = [x.strip() for x in args.platforms.split(",")]
    article = load_article(args.input)
    outdir = Path(args.output_dir)
    outdir.mkdir(exist_ok=True)
    stem = Path(args.input).stem

    for platform in platforms:
        outpath = outdir / f"{stem}_{platform}.md"
        try:
            if platform == "wechat":
                content = format_wechat(article)
            elif platform == "xiaohongshu":
                content = format_xiaohongshu(article)
            elif platform == "zhihu":
                content = format_zhihu(article)
            elif platform == "douyin":
                content = format_douyin(article)
            else:
                continue
            with open(outpath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ {platform}: {outpath}")
        except Exception as e:
            print(f"❌ {platform} 失败: {e}")

    print("\n🎉 完成！")

if __name__ == "__main__":
    main()
