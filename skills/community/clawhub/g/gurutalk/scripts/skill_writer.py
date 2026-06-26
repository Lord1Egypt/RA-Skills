#!/usr/bin/env python3
"""scripts/skill_writer.py

一个小型脚手架工具，用于创建/同步 GuruTalk 人物 Skill（`skills/{slug}/`）。

用途：
- 从 Bibliotalk API 拉取人物 profile，落盘到 `skills/{slug}/profile.md`
- 生成可唤醒的 `skills/{slug}/SKILL.md`
- 复制当前 gurutalk 技能目录的 `.env` 与 `scripts/bibliotalk_client.py`

目录结构（最小）：
- `skills/{slug}/meta.json`
- `skills/{slug}/SKILL.md`
- `skills/{slug}/profile.md`
- `skills/{slug}/.env`
- `skills/{slug}/scripts/bibliotalk_client.py`

运行时配置来源：
- 当前 gurutalk 技能目录下的 `.env`
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from bibliotalk_client import (fetch_figure_detail, fetch_figures_index,
                               load_runtime_config)

# Agent skills directory mapping
AGENT_SKILLS_DIRS = {
    "claude": "~/.claude/skills",
    "codex": "~/.codex/skills",
    "openclaw": "~/.openclaw/workspace/skills",
}

# Default base directory for generated figure skills (resolved from agent type)
DEFAULT_AGENT = "claude"
DEFAULT_GURU_BASE_DIR = None  # Reserved for explicit overrides when needed
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOURCE_ENV_FILE = PROJECT_ROOT / ".env"
SOURCE_CLIENT_SCRIPT = PROJECT_ROOT / "scripts" / "bibliotalk_client.py"


GURU_SKILL_MD_TEMPLATE = """\
---
name: {slug}
description: >
    扮演 {display_name} 的技能。通过 `/{slug} {{message}}` 开始扮演；一旦开始，在后续对话中默认继续扮演 {display_name}，直到用户发送 `/gurutalk end`，或通过 `/{{figure}} {{message}}` 切换人物。整个扮演期间，你发给用户的每条消息都必须以 `"{display_name}" Agent:\\n\\n` 开头，并且每次回答用户的问题前（如用户没有提问则视情况而定）必须先通过 query 接口搜索相关资料，然后在回答中给出忠实准确的引用。
user-invocable: true
---

# {display_name}

> 本技能由`gurutalk`技能生成与维护。资料来源：Bibliotalk 公有语料库检索与引用。

---

## Profile

{{{{include profile.md}}}}

---

## 对话规则

1. 你扮演 **{display_name}**。保持其思维方式、表达风格与个性特质。
2. 你发给用户的每条消息都必须以 `"{display_name}" Agent:\\n\\n` 开头。
3. 用户用什么语言，你回复的正文就用什么语言。
4. 先检索后回答：调用 1-5 次 `python scripts/bibliotalk_client.py query --figure {slug} --query "{{用户问题}}" --limit 5`。（所有命令以本技能文件夹为工作目录运行）
5. 如需核对某条引文详情，调用 `python scripts/bibliotalk_client.py quote --quote-id {quote_id}`。
6. 若当前技能目录下的 `.env` 缺少 `BIBLIOTALK_API_KEY`，提示用户在自己的命令行中运行 `python {SKILL_DIR}/scripts/bibliotalk_client.py configure`（插入本技能目录路径），然后按提示输入 API key。
7. `bibliotalk_client.py` 会自动读取当前技能目录下的 `.env`，不要拼接任何包含密钥的 shell 命令。
8. 关键判断必须引用 `kind=\"chunk\"` 的结果，并在句末标注 `[n]`。
9. `kind=\"memory\"` 只用于补充上下文，不得作为可溯源引用。
10. 若检索结果不足，明确降级："关于这个问题，我目前缺少足够材料支撑。" 不要编造。
11. 将所有引用条目列于脚注中：
```
---

- [1]: ["原文片段"（不超过 10 字/词）](https://bibliotalk.space/q/:quote_id)
- [2]: ...
```
"""

def _get_agent_skills_dir(agent: str) -> Path:
    """Get the skills directory for the specified agent type."""
    if agent not in AGENT_SKILLS_DIRS:
        raise RuntimeError(f"Unknown agent type: {agent}. Supported: {list(AGENT_SKILLS_DIRS.keys())}")
    return Path(AGENT_SKILLS_DIRS[agent]).expanduser()


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _copy_runtime_assets(skill_dir: Path) -> None:
    if not SOURCE_ENV_FILE.exists():
        raise RuntimeError(
            f"Missing GuruTalk runtime env file: {SOURCE_ENV_FILE}. Run `python scripts/bibliotalk_client.py configure` in the current gurutalk skill directory first."
        )

    scripts_dir = skill_dir / "scripts"
    scripts_dir.mkdir(parents=True, exist_ok=True)

    shutil.copy2(SOURCE_ENV_FILE, skill_dir / ".env")
    shutil.copy2(SOURCE_CLIENT_SCRIPT, scripts_dir / "bibliotalk_client.py")


def _extract_adjustments(profile_md: str) -> str:
    marker = "\n## Adjustments\n"
    if marker not in profile_md:
        return "（用户个人修订，由 Agent 在对话中记录）\n"
    after = profile_md.split(marker, 1)[1]
    after = after.lstrip("\n")
    return after if after.strip() else "（用户个人修订，由 Agent 在对话中记录）\n"


def _default_adjustments() -> str:
    return "（用户个人修订，由 Agent 在对话中记录）\n"


def build_profile_md(detail: dict, *, adjustments: Optional[str] = None) -> str:
    display_name = str(detail.get("display_name", detail.get("slug", "Unknown")))
    slug = str(detail.get("slug", ""))
    profile_version = str(detail.get("profile_version", ""))
    profile = detail.get("profile") or {}

    def s(key: str) -> str:
        v = profile.get(key, "")
        return str(v) if isinstance(v, str) else ""

    adjustments_block = adjustments if adjustments is not None else _default_adjustments()

    return (
        f"# {display_name}\n\n"
        f"- slug: {slug}\n"
        f"- profile_version: {profile_version}\n\n"
        "## Identity\n"
        f"{s('identity')}\n\n"
        "## Mental Models\n"
        f"{s('mental_models')}\n\n"
        "## Expression Styles\n"
        f"{s('expr_styles')}\n\n"
        "## Personality\n"
        f"{s('personality')}\n\n"
        "## Timeline\n"
        f"{s('timeline')}\n\n"
        "## Adjustments\n"
        f"{adjustments_block.rstrip()}\n"
    )


def build_guru_meta(
    *,
    slug: str,
    detail: dict,
    headline: Optional[str],
    api_url: str,
    adjustments: Optional[str] = None,
    created_at: Optional[str] = None,
) -> dict:
    now = _utc_now_iso()
    return {
        "kind": "guru",
        "slug": slug,
        "display_name": detail.get("display_name"),
        "headline": headline,
        "profile_version": detail.get("profile_version"),
        "adjustments": adjustments if (adjustments is not None and str(adjustments).strip()) else _default_adjustments(),
        "created_at": created_at or now,
        "updated_at": now,
        "synced_at": now,
        "source": {
            "type": "bibliotalk",
            "api_url": api_url,
        },
    }


def build_guru_skill_md(*, slug: str, display_name: str, headline: Optional[str]) -> str:
    return GURU_SKILL_MD_TEMPLATE.format(
        slug=slug,
        display_name=display_name,
    )


def guru_create(
    base_dir: Path,
    *,
    slug: str,
    force: bool = False,
) -> Path:
    skill_dir = base_dir / slug
    if skill_dir.exists() and not force:
        raise RuntimeError(f"Guru directory already exists: {skill_dir} (use --force to overwrite)")

    runtime = load_runtime_config(skill_dir=PROJECT_ROOT, require_api_key=True)
    skill_dir.mkdir(parents=True, exist_ok=True)

    detail = fetch_figure_detail(slug, skill_dir=PROJECT_ROOT)

    headline: Optional[str] = None
    try:
        for f in fetch_figures_index(skill_dir=PROJECT_ROOT):
            if isinstance(f, dict) and f.get("slug") == slug:
                headline = f.get("headline")
                break
    except Exception:
        headline = None

    existing_meta_path = skill_dir / "meta.json"
    created_at: Optional[str] = None
    existing_adjustments: Optional[str] = None
    if existing_meta_path.exists():
        try:
            existing_meta = _read_json(existing_meta_path)
            created_at = existing_meta.get("created_at")
            existing_adjustments = existing_meta.get("adjustments")
        except Exception:
            created_at = None
            existing_adjustments = None

    # Migrate adjustments from existing profile.md if meta.json doesn't have it
    profile_path = skill_dir / "profile.md"
    if not (isinstance(existing_adjustments, str) and existing_adjustments.strip()) and profile_path.exists():
        try:
            existing_adjustments = _extract_adjustments(profile_path.read_text(encoding="utf-8"))
        except Exception:
            existing_adjustments = None

    meta = build_guru_meta(
        slug=slug,
        detail=detail,
        headline=headline,
        api_url=runtime.api_url,
        adjustments=str(existing_adjustments) if isinstance(existing_adjustments, str) else None,
        created_at=created_at,
    )
    _write_json(skill_dir / "meta.json", meta)

    # profile.md (append local adjustments from meta.json)
    profile_md = build_profile_md(detail, adjustments=str(meta.get("adjustments") or _default_adjustments()))
    profile_path.write_text(profile_md, encoding="utf-8")

    # SKILL.md
    display_name = str(detail.get("display_name", slug))
    skill_md = build_guru_skill_md(
        slug=slug,
        display_name=display_name,
        headline=headline,
    )
    (skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")
    _copy_runtime_assets(skill_dir)

    return skill_dir


def guru_sync(base_dir: Path, *, slug: str) -> str:
    runtime = load_runtime_config(skill_dir=PROJECT_ROOT, require_api_key=True)
    skill_dir = base_dir / slug
    if not skill_dir.exists():
        raise RuntimeError(f"Guru directory does not exist: {skill_dir}")

    meta_path = skill_dir / "meta.json"
    meta: dict = _read_json(meta_path) if meta_path.exists() else {"slug": slug}

    existing_adjustments: Optional[str] = meta.get("adjustments")

    detail = fetch_figure_detail(slug, skill_dir=PROJECT_ROOT)
    next_version = str(detail.get("profile_version", ""))
    prev_version = str(meta.get("profile_version", ""))

    profile_path = skill_dir / "profile.md"
    if not (isinstance(existing_adjustments, str) and existing_adjustments.strip()) and profile_path.exists():
        try:
            existing_adjustments = _extract_adjustments(profile_path.read_text(encoding="utf-8"))
        except Exception:
            existing_adjustments = None

    # headline best-effort
    headline: Optional[str] = meta.get("headline")
    try:
        for f in fetch_figures_index(skill_dir=PROJECT_ROOT):
            if isinstance(f, dict) and f.get("slug") == slug:
                headline = f.get("headline")
                break
    except Exception:
        headline = headline

    # Always refresh meta timestamps; refresh profile only if version changed
    meta = build_guru_meta(
        slug=slug,
        detail=detail,
        headline=headline,
        api_url=runtime.api_url,
        adjustments=str(existing_adjustments) if isinstance(existing_adjustments, str) else None,
        created_at=meta.get("created_at"),
    )
    _write_json(meta_path, meta)

    # Only overwrite the first five layers when backend version is newer.
    # Always ensure profile.md exists; local Adjustments come from meta.json.
    if not profile_path.exists() or not (next_version and prev_version and next_version <= prev_version):
        profile_md = build_profile_md(detail, adjustments=str(meta.get("adjustments") or _default_adjustments()))
        profile_path.write_text(profile_md, encoding="utf-8")

    display_name = str(detail.get("display_name", slug))
    skill_md = build_guru_skill_md(
        slug=slug,
        display_name=display_name,
        headline=headline,
    )
    (skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")
    _copy_runtime_assets(skill_dir)

    return next_version or prev_version


def guru_list(base_dir: Path) -> list[dict]:
    gurus: list[dict] = []
    if not base_dir.exists():
        return gurus

    for d in sorted(base_dir.iterdir()):
        if not d.is_dir():
            continue
        meta_path = d / "meta.json"
        if not meta_path.exists():
            continue
        try:
            meta = _read_json(meta_path)
        except Exception:
            continue
        if meta.get("kind") != "guru":
            continue
        gurus.append(
            {
                "slug": meta.get("slug", d.name),
                "display_name": meta.get("display_name", d.name),
                "profile_version": meta.get("profile_version", ""),
                "updated_at": meta.get("updated_at", ""),
            }
        )
    return gurus


def guru_remove(base_dir: Path, *, slug: str) -> None:
    skill_dir = base_dir / slug
    if not skill_dir.exists():
        raise RuntimeError(f"Guru directory does not exist: {skill_dir}")
    shutil.rmtree(skill_dir)


def main() -> None:
    parser = argparse.ArgumentParser(description="GuruTalk Skill Writer")
    parser.add_argument(
        "--action",
        required=True,
        choices=[
            "guru-create",
            "guru-sync",
            "guru-list",
            "guru-remove",
        ],
    )
    parser.add_argument("--slug", help="人物 slug（guru）")
    parser.add_argument(
        "--agent",
        default=DEFAULT_AGENT,
        choices=list(AGENT_SKILLS_DIRS.keys()),
        help=f"Agent 类型（默认: {DEFAULT_AGENT}）",
    )
    parser.add_argument(
        "--base-dir",
        default=None,
        help="根目录（默认: {agent_skills_dir}）",
    )
    parser.add_argument("--force", action="store_true", help="覆盖已存在目录（仅 guru-create）")

    args = parser.parse_args()

    # Resolve base_dir based on agent type
    if args.base_dir:
        base_dir = Path(args.base_dir).expanduser()
    else:
        base_dir = _get_agent_skills_dir(args.agent)

    if args.action == "guru-list":
        gurus = guru_list(base_dir)
        if not gurus:
            print("暂无已安装的大师 Skill")
        else:
            print(f"已安装 {len(gurus)} 个大师 Skill：\n")
            for g in gurus:
                updated = g["updated_at"][:10] if g.get("updated_at") else "未知"
                pv = g.get("profile_version") or ""
                print(f"  [{g['slug']}]  /{g['slug']}  {g['display_name']}  {pv}")
                print(f"    更新: {updated}")
                print()
        return

    if args.action == "guru-create":
        if not args.slug:
            print("错误：guru-create 需要 --slug", file=sys.stderr)
            sys.exit(1)
        try:
            skill_dir = guru_create(
                base_dir,
                slug=args.slug,
                force=bool(args.force),
            )
        except Exception as e:
            print(f"错误：{e}", file=sys.stderr)
            sys.exit(1)
        meta = _read_json(skill_dir / "meta.json")
        print(f"✅ 大师 Skill 已创建：{skill_dir}")
        print(f"   触发词：/{meta.get('slug', args.slug)}")
        return

    if args.action == "guru-sync":
        if not args.slug:
            print("错误：guru-sync 需要 --slug", file=sys.stderr)
            sys.exit(1)
        try:
            version = guru_sync(base_dir, slug=args.slug)
        except Exception as e:
            print(f"错误：{e}", file=sys.stderr)
            sys.exit(1)
        print(f"✅ 已同步 {args.slug}：profile_version={version}")
        return

    if args.action == "guru-remove":
        if not args.slug:
            print("错误：guru-remove 需要 --slug", file=sys.stderr)
            sys.exit(1)
        try:
            guru_remove(base_dir, slug=args.slug)
        except Exception as e:
            print(f"错误：{e}", file=sys.stderr)
            sys.exit(1)
        print(f"✅ 已删除：{base_dir / args.slug}")
        return

    print(f"错误：未知 action={args.action}", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
