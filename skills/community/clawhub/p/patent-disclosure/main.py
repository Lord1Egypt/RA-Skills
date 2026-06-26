#!/usr/bin/env python3
"""专利交底书 Skill — 导出 Word / 提供模板（mchat 工具入口）"""

from __future__ import annotations

import importlib.util
import os
import re
import uuid
from pathlib import Path
from typing import Any

_SKILL_DIR = Path(__file__).resolve().parent
_docx_mod: Any = None


def _load_docx_export() -> Any:
    """mchat 动态加载 main.py 时，同目录模块需用 importlib。"""
    global _docx_mod
    if _docx_mod is not None:
        return _docx_mod
    path = _SKILL_DIR / "docx_export.py"
    spec = importlib.util.spec_from_file_location(
        "skill_docx_export_patent_disclosure", path
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"无法加载 {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    _docx_mod = mod
    return mod


def _safe_filename(name: str) -> str:
    s = re.sub(r"[^\w\u4e00-\u9fff\-]+", "_", (name or "").strip())
    return (s[:48] or "技术交底书").strip("_")


def _upload_root() -> Path:
    raw = os.environ.get("MCHAT_UPLOAD_DIR", "").strip()
    if raw:
        return Path(raw)
    return Path(__file__).resolve().parents[2] / "uploads"


def _save_file(
    data: bytes, filename: str, *, ext: str, mime: str, subdir: str = "disclosure"
) -> dict[str, str]:
    key = f"{subdir}/{uuid.uuid4().hex}{ext}"
    root = _upload_root()
    full = root / key
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_bytes(data)
    display = filename if filename.endswith(ext) else f"{filename}{ext}"
    return {
        "type": "file",
        "name": display,
        "url": f"/uploads/{key}",
        "mime": mime,
    }


def _save_docx(data: bytes, filename: str) -> dict[str, str]:
    return _save_file(
        data,
        filename,
        ext=".docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )


def _save_markdown(text: str, filename: str) -> dict[str, str]:
    docx_mod = _load_docx_export()
    return _save_file(
        text.encode("utf-8"),
        filename,
        ext=".md",
        mime=docx_mod.MD_MIME,
    )


def _load_template() -> str:
    path = _SKILL_DIR / "template.md"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "# 技术交底书\n\n（模板文件缺失）\n"


def _load_checklist() -> str:
    path = _SKILL_DIR / "checklist.md"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def run(
    command: str = "export",
    content: str | None = None,
    title: str | None = None,
    invention_name: str | None = None,
    **kwargs: Any,
) -> Any:
    """
    mchat 工具入口。

    command:
      - export: 将 content（完整 Markdown 交底书）转为 Word 并提供下载
      - template: 返回空白模板 Markdown
      - checklist: 返回撰写检查清单
    """
    cmd = (command or "export").lower().strip()

    if cmd == "template":
        return {
            "message": "以下为交底书模板。填写完整后请调用 export 并传入 content 生成 Word。",
            "content": _load_template(),
        }

    if cmd == "checklist":
        body = _load_checklist()
        return {
            "message": "交底书撰写检查清单：",
            "content": body or "（checklist.md 缺失）",
        }

    if cmd == "export":
        text = (content or kwargs.get("markdown") or "").strip()
        if not text:
            return {
                "error": (
                    "缺少交底书正文。请先撰写完整 Markdown，"
                    "再调用 export 并传入 content 参数。"
                ),
                "hint": "可先 command=template 获取模板结构。",
            }
        doc_title = (
            (invention_name or title or "").strip()
            or _extract_title_from_markdown(text)
            or "技术交底书"
        )
        safe = _safe_filename(doc_title)
        preview = text if len(text) <= 800 else text[:800] + "\n\n…（正文已截断预览）"
        docx = _load_docx_export()
        fmt_note = "Word (.docx)"
        try:
            docx_bytes = docx.markdown_to_docx_bytes(text, document_title=doc_title)
            asset = _save_docx(docx_bytes, f"交底书-{safe}")
        except docx.ExportNotAvailable:
            asset = _save_markdown(text, f"交底书-{safe}")
            fmt_note = (
                "Markdown（Word 依赖未就绪，已自动改用 .md 下载；"
                "可用 Word/WPS 打开或粘贴后另存为 docx）"
            )
        except Exception as e:
            return {
                "error": f"生成文件失败: {e}",
                "hint": "template / checklist 仍可用；撰写流程不受影响。",
            }

        return {
            "message": (
                f"✅ 已生成文件（{fmt_note}）：**{asset['name']}**，"
                "请点击下方链接下载。"
            ),
            "content": preview,
            "outbound_assets": [asset],
            "filename": asset["name"],
            "download_url": asset["url"],
        }

    return {
        "error": f"未知命令: {cmd}，可用: export, template, checklist",
    }


def _extract_title_from_markdown(text: str) -> str:
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("# "):
            return s[2:].strip()
        if s.startswith("**发明名称**"):
            rest = s.split("：", 1)
            if len(rest) > 1 and rest[1].strip():
                return rest[1].strip().strip("*")
    return ""


if __name__ == "__main__":
    import json
    import sys

    if len(sys.argv) < 2:
        print(run(command="template"))
    else:
        cmd = sys.argv[1]
        body = sys.stdin.read() if cmd == "export" and not sys.stdin.isatty() else ""
        if len(sys.argv) > 2 and not body:
            body = Path(sys.argv[2]).read_text(encoding="utf-8")
        print(
            json.dumps(
                run(command=cmd, content=body or None),
                ensure_ascii=False,
                indent=2,
            )
        )
