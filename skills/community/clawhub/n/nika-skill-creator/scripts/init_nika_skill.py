#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_SUBDOCS = ["步骤", "模板", "示例"]


def _die(msg: str, code: int = 2) -> None:
    print(f"error: {msg}", file=sys.stderr)
    raise SystemExit(code)


def _parse_subdocs(raw: str | None) -> list[str]:
    if not raw:
        return list(DEFAULT_SUBDOCS)
    parts = [p.strip() for p in raw.split(",")]
    parts = [p for p in parts if p]
    if not parts:
        return list(DEFAULT_SUBDOCS)
    # Deduplicate while preserving order
    seen: set[str] = set()
    out: list[str] = []
    for p in parts:
        if p in seen:
            continue
        seen.add(p)
        out.append(p)
    return out


def _validate_name(name: str) -> None:
    if not name.strip():
        _die("skill name must be non-empty")
    if any(ch in name for ch in ["/", "\\"]):
        _die("skill name must not contain path separators ('/' or '\\\\')")
    if name.strip() != name:
        _die("skill name must not have leading/trailing whitespace")


def _write_text(path: Path, content: str, *, force: bool) -> None:
    if path.exists() and not force:
        _die(f"refusing to overwrite existing file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _main_doc_content(skill_name_cn: str, subdocs: list[str]) -> str:
    # Nika constraints: generated doc content must avoid file paths and extensions.
    subdoc_lines = "\n".join([f"- @{n}" for n in subdocs])
    return f"""---
name: {skill_name_cn}
description: 【一句话说明何时使用本技能。避免依赖用户自定义文件名；写清触发场景与用户说法示例。】
---

# {skill_name_cn}

【一句话说明本技能解决什么问题。】

## 触发条件

当用户出现以下需求时使用本技能：
- 【触发语示例 1】
- 【触发语示例 2】
- 【触发语示例 3】

## 必要输入

必须明确“必要输入内容、形式”。建议用表格：

| 输入项 | 文件类型（设定/章节/笔记） | 推荐文件名或命名模式 | 最低内容要求 |
|---|---|---|---|
| 【例如：核心设定】 | 【设定】 | 【例如：设定】 | 【必须包含：世界观、人物关系、力量体系】 |
| 【例如：待处理正文】 | 【章节】 | 【例如：第X章】 | 【必须包含：完整章节文本】 |

## 输入获取规则（先查找，找不到再问）

按固定优先级执行：
1. 优先使用用户在对话中已提供或已引用的内容
2. 否则按“文件类型 + 文件名/命名模式”查找所需输入
3. 找不到再向用户提问，并一次只问关键缺口

## 交付物

必须同时定义两类交付：

### 持久交付（文件）

| 交付物 | 文件类型（设定/章节） | 文件名规则 | 内容结构 |
|---|---|---|---|
| 【例如：分析报告】 | 【设定】 | 【例如：分析报告】 | 【标题层级或固定模板】 |
| 【例如：优化后的正文】 | 【章节】 | 【例如：第X章】 | 【保留原结构，仅修改指定段落】 |

### 临时交付（屏幕输出）

在对话中输出：
- 【摘要：做了什么】
- 【检查结果：关键问题列表】
- 【下一步指引：用户应该做什么】

## 使用流程

1. 【检查输入是否齐全；缺失则按输入获取规则补齐】
2. 【执行任务核心步骤（可把细节下沉到子文档）】
3. 【产出持久交付文件】
4. 【屏幕输出临时交付】

## 子文档索引

当需要更详细步骤、清单、模板、示例时，引用子文档：
{subdoc_lines}

## 注意事项

- 不要出现文件路径或文件扩展名的引用形式
- 文档内 `@` 只用于引用子文档
- 不要用 `@` 引用用户自定义名称的文件；需要时用自然语言澄清或约定固定命名规则
"""


def _subdoc_content(subdoc_name: str) -> str:
    # Keep this generic; users will customize.
    return f"""# {subdoc_name}

## 适用场景

- 【什么时候需要读这个子文档】

## 内容

【把可复用的步骤、清单、模板或示例放在这里。主文档只保留导航与契约。】
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="init_nika_skill.py",
        description="Initialize a Nika-compliant target skill skeleton under the repo (SKILL.md + references/*.md).",
    )
    parser.add_argument("skill_name_cn", help="Target skill Chinese name (used as folder name and main doc name).")
    parser.add_argument("--out-dir", default="skills", help="Output base directory (default: skills).")
    parser.add_argument(
        "--subdocs",
        default=None,
        help="Comma-separated list of sub doc names (default: 步骤,模板,示例).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files if they already exist.",
    )

    args = parser.parse_args(argv)
    skill_name_cn = args.skill_name_cn
    _validate_name(skill_name_cn)

    out_dir = Path(args.out_dir)
    subdocs = _parse_subdocs(args.subdocs)
    for s in subdocs:
        _validate_name(s)

    skill_dir = out_dir / skill_name_cn
    main_doc = skill_dir / "SKILL.md"
    refs_dir = skill_dir / "references"

    refs_dir.mkdir(parents=True, exist_ok=True)

    _write_text(main_doc, _main_doc_content(skill_name_cn, subdocs), force=args.force)
    created: list[Path] = [main_doc]

    for s in subdocs:
        p = refs_dir / f"{s}.md"
        _write_text(p, _subdoc_content(s), force=args.force)
        created.append(p)

    print(f"Initialized target skill: {skill_dir}")
    for p in created:
        print(f"- wrote {p}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

