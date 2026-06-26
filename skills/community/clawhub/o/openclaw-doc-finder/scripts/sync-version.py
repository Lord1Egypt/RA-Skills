#!/usr/bin/env python3
"""
openclaw-doc-finder 版本同步脚本
功能：核对 OpenClaw 版本与技能版本，不一致时自动刷新 doc-index.md 并更新 VERSION
用法：python3 sync-version.py [--dry-run]
"""

import json
import os
import sys
from pathlib import Path

# ── 配置 ──────────────────────────────────────────────────────
SKILL_DIR = Path(__file__).parent.parent.resolve()
VERSION_FILE = SKILL_DIR / "VERSION"
DOC_INDEX_FILE = SKILL_DIR / "references" / "doc-index.md"
OPENCLAW_DOCS = Path.home() / ".npm-global" / "lib" / "node_modules" / "openclaw" / "docs"

# 已知稳定版本（回退用）
OPENCLAW_VERSION_CACHE = "1.188"


def get_openclaw_version() -> str:
    """读取当前运行的 OpenClaw 版本号"""
    pkg_path = Path.home() / ".npm-global" / "lib" / "node_modules" / "openclaw" / "package.json"
    if pkg_path.exists():
        try:
            with open(pkg_path) as f:
                return json.load(f).get("version", OPENCLAW_VERSION_CACHE)
        except Exception:
            pass
    return OPENCLAW_VERSION_CACHE


def get_skill_version() -> str:
    """读取技能当前版本号"""
    if VERSION_FILE.exists():
        return VERSION_FILE.read_text().strip()
    return "v0.0.0"


def build_doc_index(oc_version: str) -> str:
    """
    扫描本地 docs/ 目录，构建 doc-index.md 内容
    只处理 .md 文件，跳过 assets/images/meta 文件
    """
    sections = [
        "# OpenClaw 文档索引",
        "",
        f"> ⚠️ **自动生成** — OpenClaw v{oc_version} | 生成时间：自动",
        "",
        "## 意图 → 文档路由表",
        "",
        "| 场景关键词 | 文档标题 | 完整 URL | 本地路径 |",
        "|----------|---------|---------|---------|",
    ]

    # URL 路径映射（相对路径 → docs.openclaw.ai URL）
    url_mappings = {
        "start/": "start/",
        "gateway/": "gateway/",
        "channels/": "channels/",
        "providers/": "providers/",
        "tools/": "tools/",
        "install/": "install/",
        "vps.md": "vps",
        "network.md": "network",
        "logging.md": "gateway/logging",
        "nodes/": "nodes/",
    }

    if not OPENCLAW_DOCS.exists():
        sections.append(f"\n⚠️ 本地文档目录不存在：`{OPENCLAW_DOCS}`")
        return "\n".join(sections)

    md_files = sorted(OPENCLAW_DOCS.rglob("*.md"))

    for md_path in md_files:
        # 跳过隐藏文件和非文档
        rel = md_path.relative_to(OPENCLAW_DOCS)
        if any(p.startswith(".") or p.startswith("_") for p in rel.parts):
            continue
        if md_path.name in ("index.md", "CNAME", "style.css"):
            continue
        if md_path.name.startswith("nav-tabs"):
            continue

        # 解析 frontmatter title
        title = md_path.stem.replace("-", " ").replace("_", " ").title()
        try:
            text = md_path.read_text(encoding="utf-8", errors="ignore")
            if text.startswith("---"):
                end = text.find("\n---", 4)
                if end > 0:
                    frontmatter = text[3:end]
                    for line in frontmatter.splitlines():
                        if line.startswith("title:"):
                            title = line.split(":", 1)[1].strip().strip('"').strip("'")
                            break
        except Exception:
            pass

        # 构造 URL
        parts = list(rel.parts)
        if parts[0] in url_mappings:
            url_path = url_mappings[parts[0]]
            if len(parts) > 1:
                url_path += parts[-1].replace(".md", "")
            url = f"https://docs.openclaw.ai/{url_path}"
        else:
            url = f"https://docs.openclaw.ai/{str(rel).replace('.md', '')}"

        local = str(rel)
        sections.append(f"| ... | {title} | {url} | {local} |")

    sections.append("")
    return "\n".join(sections)


def update_version(new_version: str):
    """更新 VERSION 文件"""
    VERSION_FILE.write_text(f"v{new_version}\n")


def main(dry_run: bool = False):
    oc_version = get_openclaw_version()
    skill_version = get_skill_version().lstrip("v")

    print(f"[openclaw-doc-finder] 版本检查")
    print(f"  OpenClaw 运行版本 : {oc_version}")
    print(f"  技能版本          : v{skill_version}")

    if oc_version == skill_version:
        print("  ✅ 版本一致，无需更新")
        return

    print(f"  🔄 版本不一致，开始同步文档索引...")

    new_index = build_doc_index(oc_version)

    if dry_run:
        print(f"\n[DRY-RUN] 将会写入以下内容到 {DOC_INDEX_FILE}:")
        print(new_index[:500] + "...")
        return

    # 写 doc-index.md
    DOC_INDEX_FILE.write_text(new_index, encoding="utf-8")
    update_version(oc_version)

    print(f"  ✅ doc-index.md 已刷新")
    print(f"  ✅ VERSION 已更新为 v{oc_version}")


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    main(dry_run=dry_run)
