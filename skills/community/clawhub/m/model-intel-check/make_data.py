"""下载并构建 intel_check.py 所需的题库文件（data/ 目录）。

- AIME 2025 / 2026：math-ai/aime25、math-ai/aime26（HuggingFace，公开匿名可下），
  各 30 题，行序与官方一致；默认两年都构建，产出 aime2025.jsonl / aime2026.jsonl。
- GPQA Diamond：Idavidrein/gpqa 在 HF 上是 gated 数据集，需要先在该数据集页面
  同意协议、然后 export HF_TOKEN=hf_xxx 才能下载；没有 token 则跳过（可只跑 AIME）。

用法:
    python make_data.py            # 下载全部能下的
    python make_data.py --only aime
"""
import argparse
import csv
import io
import json
import os
import sys
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"

MIRRORS = ["https://hf-mirror.com", "https://huggingface.co"]


def fetch(relpath, token=None):
    """依次尝试镜像站下载, 返回 bytes。"""
    headers = {"User-Agent": "curl/8.0.1"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    last = None
    for base in MIRRORS:
        url = f"{base}/datasets/{relpath}"
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as e:
            last = e
            print(f"  {url} 失败: {e}")
    raise RuntimeError(f"所有镜像均失败: {relpath}: {last}")


AIME_SOURCES = {  # year -> (仓库, 文件名)
    2025: ("math-ai/aime25", "test.jsonl"),
    2026: ("math-ai/aime26", "aime2026.jsonl"),
}


def build_aime(year):
    repo, fname = AIME_SOURCES[year]
    print(f"下载 AIME {year} ({repo}) ...")
    raw = fetch(f"{repo}/resolve/main/{fname}")
    rows = [json.loads(l) for l in raw.decode("utf-8").splitlines() if l.strip()]
    out = [{"id": str(i), "index": i, "problem": r["problem"], "answer": str(r["answer"])}
           for i, r in enumerate(rows)]
    dest = DATA / f"aime{year}.jsonl"
    with open(dest, "w", encoding="utf-8") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"  -> {dest}  ({len(out)} 题)")


def build_gpqa():
    """GPQA Diamond 前 50 条 -> data/gpqa_diamond_50.jsonl

    输出 schema: {"id", "question", "choices": [正确项, 干扰项x3], "correct_index": 0, "domain"}
    注意 choices[0] 永远是正确答案; 洗牌由 intel_check.py 用固定种子在运行时完成。
    """
    token = os.environ.get("HF_TOKEN", "")
    if not token:
        print("跳过 GPQA: 未设置 HF_TOKEN（Idavidrein/gpqa 是 gated 数据集，需先在")
        print("  https://huggingface.co/datasets/Idavidrein/gpqa 页面同意协议并创建 token）。")
        print("  也可以手工把 gpqa_diamond_50.jsonl 放进 data/ —— schema 见 data/README.md")
        return
    print("下载 GPQA Diamond (Idavidrein/gpqa) ...")
    raw = fetch("Idavidrein/gpqa/resolve/main/gpqa_diamond.csv", token=token)
    rows = list(csv.DictReader(io.StringIO(raw.decode("utf-8"))))[:50]
    out = []
    for r in rows:
        choices = [r["Correct Answer"], r["Incorrect Answer 1"],
                   r["Incorrect Answer 2"], r["Incorrect Answer 3"]]
        out.append({"id": r["Record ID"], "question": r["Question"],
                    "choices": choices, "correct_index": 0,
                    "domain": r.get("Subdomain") or r.get("Domain") or ""})
    dest = DATA / "gpqa_diamond_50.jsonl"
    with open(dest, "w", encoding="utf-8") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"  -> {dest}  ({len(out)} 题)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=["aime", "gpqa"], default=None)
    ap.add_argument("--aime-year", type=int, choices=sorted(AIME_SOURCES), default=None,
                    help="只构建某一年的 AIME; 默认两年都构建")
    args = ap.parse_args()
    DATA.mkdir(exist_ok=True)
    if args.only in (None, "aime"):
        years = [args.aime_year] if args.aime_year else sorted(AIME_SOURCES)
        for y in years:
            build_aime(y)
    if args.only in (None, "gpqa"):
        build_gpqa()


if __name__ == "__main__":
    main()
