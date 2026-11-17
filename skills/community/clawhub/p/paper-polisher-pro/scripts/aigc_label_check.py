#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aigc_label_check — AIGC 合规标识检查层（v3 新增，政策红利方向）。

依据《人工智能生成合成内容标识办法》（2025-09-01 施行）：生成合成内容服务提供者
应添加显式标识（文本/音频提示；元数据属隐式标识）或隐式标识（水印/溯源）。本脚本检查文档中的:

  A. 元数据标识  docx core properties / PDF XMP(Producer/Creator/Keywords) 中的 AI 工具名
  B. 隐式水印    C2PA/JUMBF 清单字节（jpg/png/pdf/webp）、PNG tEXt 隐写键
  C. 显式提示    文本层的"AI生成/AIGC/本文由...生成"等声明

与统计检测互为印证：统计层说"像AI" + 标识层找到工具名 = 高置信；
标识层命中而统计层不 suspect → 可能是合规声明或误标，需人工看。

用法: python aigc_label_check.py <文件...> [--json]
支持: .docx .pdf .txt .md .png .jpg .jpeg .webp
"""
import os, re, sys, json, zipfile, argparse, struct

AI_TOOLS = {
    "chatgpt": "OpenAI ChatGPT", "gpt-4": "OpenAI GPT-4", "gpt-5": "OpenAI GPT-5",
    "openai": "OpenAI", "claude": "Anthropic Claude", "anthropic": "Anthropic Claude",
    "gemini": "Google Gemini", "deepseek": "DeepSeek", "glm-": "智谱 GLM",
    "glm4": "智谱 GLM", "glm5": "智谱 GLM", "zhipu": "智谱 GLM", "kimi": "月之暗面 Kimi",
    "moonshot": "月之暗面 Kimi", "qwen": "阿里 Qwen", "通义": "阿里 Qwen",
    "doubao": "字节豆包", "豆包": "字节豆包", "minimax": "MiniMax", "海螺": "MiniMax",
    "文心": "百度文心", "ernie": "百度文心", "grok": "xAI Grok", "llama": "Meta LLaMA",
    "mistral": "Mistral", "copilot": "Microsoft Copilot", "midjourney": "Midjourney",
}
EXPLICIT_LABELS = [
    "本文由人工智能生成", "本文由AI生成", "由大模型生成", "AI生成内容", "AIGC标识",
    "人工智能生成合成内容", "本内容为AI", "AI辅助生成", "本图由AI", "此图片由AI",
]


def check_docx(path):
    ev = []
    try:
        with zipfile.ZipFile(path) as z:
            core = z.read("docProps/core.xml").decode("utf-8", "ignore") if "docProps/core.xml" in z.namelist() else ""
            app = z.read("docProps/app.xml").decode("utf-8", "ignore") if "docProps/app.xml" in z.namelist() else ""
            for blob, field in ((core, "core.xml"), (app, "app.xml")):
                for key, name in AI_TOOLS.items():
                    if key in blob.lower():
                        tag = re.search(r"<dc:creator>([^<]{0,60})", blob) or re.search(
                            r"<cp:lastModifiedBy>([^<]{0,60})", blob)
                        ev.append({"type": "metadata", "where": "docx/" + field,
                                   "hit": name, "detail": tag.group(1) if tag else key})
                        break
    except Exception as e:
        ev.append({"type": "error", "detail": str(e)[:80]})
    return ev


def check_pdf(path):
    ev = []
    try:
        raw = open(path, "rb").read(200000)
        head = raw[:60000].decode("latin-1", "ignore")
        for key, name in AI_TOOLS.items():
            if key in head.lower():
                m = re.search(r"/Producer\s*\(([^)]{0,80})", head) or re.search(
                    r"/Creator\s*\(([^)]{0,80})", head)
                ev.append({"type": "metadata", "where": "pdf/Producer-Creator",
                           "hit": name, "detail": m.group(1) if m else key})
                break
        if b"JUMBF" in raw or b"c2pa" in raw.lower():
            ev.append({"type": "watermark", "where": "pdf", "hit": "C2PA/JUMBF 清单存在"})
    except Exception as e:
        ev.append({"type": "error", "detail": str(e)[:80]})
    return ev


def check_image(path):
    ev = []
    try:
        raw = open(path, "rb").read()
        if b"JUMBF" in raw or b"c2pa" in raw.lower() or burn_marker(raw):
            ev.append({"type": "watermark", "where": os.path.splitext(path)[1],
                       "hit": "C2PA/JUMBF 隐式标识存在"})
        if path.lower().endswith(".png"):
            m = re.search(rb"tEXt([a-zA-Z0-9 _-]{0,30})\x00", raw[:50000])
            if m:
                tag = m.group(1).decode("latin-1", "ignore")
                for key, name in AI_TOOLS.items():
                    if key in tag.lower():
                        ev.append({"type": "watermark", "where": "png/tEXt", "hit": name})
                        break
    except Exception as e:
        ev.append({"type": "error", "detail": str(e)[:80]})
    return ev


def burn_marker(raw):
    # Google SynthID 等 invisible watermark 常见锚点（探测性，非解码）
    return b"SynthID" in raw or b"synthid" in raw


def check_text(path):
    ev = []
    try:
        txt = open(path, encoding="utf-8", errors="ignore").read()
        for lab in EXPLICIT_LABELS:
            if lab in txt:
                pos = txt.find(lab)
                ev.append({"type": "explicit", "where": "text@%d" % pos, "hit": lab,
                           "detail": txt[max(0, pos - 20):pos + 40].replace("\n", " ")})
    except Exception as e:
        ev.append({"type": "error", "detail": str(e)[:80]})
    return ev


def main():
    ap = argparse.ArgumentParser(description="AIGC合规标识检查(《标识办法》2025-09)")
    ap.add_argument("files", nargs="+")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    out = []
    for path in a.files:
        if not os.path.exists(path):
            out.append({"file": path, "verdict": "missing"})
            continue
        ext = os.path.splitext(path)[1].lower()
        ev = []
        if ext == ".docx":
            ev = check_docx(path) + check_text(path)
        elif ext == ".pdf":
            ev = check_pdf(path) + check_text(path)
        elif ext in (".png", ".jpg", ".jpeg", ".webp"):
            ev = check_image(path)
        else:
            ev = check_text(path)
        has_label = any(e["type"] in ("metadata", "watermark", "explicit") for e in ev)
        out.append({"file": os.path.basename(path), "verdict": "labeled" if has_label else "no_label",
                    "evidence": ev})
    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        for r in out:
            flag = "✅ 发现标识" if r["verdict"] == "labeled" else ("❓ 无标识" if r["verdict"] == "no_label" else r["verdict"])
            print("[%s] %s" % (flag, r["file"]))
            for e in r.get("evidence", []):
                if e["type"] == "error":
                    print("    error:", e["detail"])
                else:
                    print("    %s | %s | %s %s" % (e["type"], e["where"], e["hit"],
                                                   (":: " + e["detail"][:40]) if e.get("detail") else ""))
    sys.exit(0 if any(r["verdict"] == "labeled" for r in out) else 1)


if __name__ == "__main__":
    import sys as _sys
    try:  # v3.5: 中文 Windows 默认 GBK 控制台会因 emoji/警示符崩溃 stdout——统一 UTF-8
        _sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        _sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    main()
