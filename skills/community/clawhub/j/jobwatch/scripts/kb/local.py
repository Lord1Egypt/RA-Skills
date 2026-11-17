"""Local Markdown KB adapter —— 零依赖默认后端。

文档写入 workspace 的 kb_local/ 目录（按日期分子目录），并维护 kb_local/index.jsonl
（一行一个文档的元数据），方便 grep / 喂给任何本地 RAG。

没有 2brain 账号的用户开箱即用；之后想换 2brain，只改 config.json 的 kb.backend。
"""
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import ROOT, now_iso  # noqa: E402

KB_DIR = ROOT / "kb_local"


def upload_doc(filename, content_md):
    """Write one doc to local KB. Returns dict with the stored path."""
    if not filename.endswith((".md", ".txt")):
        filename += ".md"
    day_dir = KB_DIR / datetime.now().strftime("%Y-%m-%d")
    day_dir.mkdir(parents=True, exist_ok=True)
    path = day_dir / filename
    if path.exists():  # 与 2brain 拒绝重名文件的语义保持一致（幂等）
        raise RuntimeError(f"local kb: duplicate file name {filename}")
    path.write_text(content_md)
    with (KB_DIR / "index.jsonl").open("a") as f:
        f.write(json.dumps({"ts": now_iso(), "file": str(path.relative_to(ROOT)),
                            "chars": len(content_md)}, ensure_ascii=False) + "\n")
    return {"code": 0, "path": str(path)}


if __name__ == "__main__":
    p = Path(sys.argv[1])
    print(upload_doc(p.name, p.read_text()))
