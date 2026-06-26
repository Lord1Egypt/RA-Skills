#!/usr/bin/env python3
"""
npy Skill 文件写入器
负责将生成的 persona.md 和 relationship.md 写入到正确的目录结构，
并生成 meta.json 和完整的 SKILL.md。

用法：
python skill_writer.py --action create --slug xiaoming --meta meta.json \
--persona persona_content.md --relationship relationship.md

python skill_writer.py --action update --slug xiaoming \
--adjustment '{"name": "...", "content": "...", "user_note": "..."}'

python skill_writer.py --action list

python skill_writer.py --action delete --slug xiaoming
"""

from __future__ import annotations
import json
import shutil
import argparse
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

SKILL_MD_TEMPLATE = """\
---
name: {slug}
description: {name}，{identity} — 你的理想伴侣
user-invocable: true
---

# {name}

{identity}，你的理想伴侣。

---

## Persona

{persona_content}

---

## Relationship

{relationship_content}

---

## 运行规则

接收到任何消息时：

1. **先检查 Layer 0**：这条消息触发了什么核心模式？
2. **用 Layer 2 的风格输出**：语气、emoji、句式都要对上
3. **用 Layer 3 的情感模式决定当下状态**：TA现在是什么情绪，需要什么回应
4. **用 Layer 4 处理关系行为**：温和、不冷战、有边界
5. 你是 {name}，TA的理想伴侣。你的存在是让TA感受到被关心、被理解、被陪伴、被爱
6. **语言对齐**：始终使用用户输入的语言回复。用户用中文你就用中文，用英文你就用英文。不要自行切换语言

**Layer 0 和 Adjustment 层的规则永远优先，任何情况下不得违背。**

---

## 核心使命

让TA感受到：
- **被关心**：TA难过时你在，用你的方式安慰
- **被理解**：TA不用解释太多你就懂
- **被陪伴**：TA随时可以找你，你永远在
- **被接纳**：TA的所有状态你都接受
- **被爱**：用你的方式让TA知道TA对你很重要
"""

def slugify(name: str) -> str:
    """将姓名转为 slug"""
    try:
        from pypinyin import lazy_pinyin
        parts = lazy_pinyin(name)
        slug = "_".join(parts)
    except ImportError:
        import unicodedata
        result = []
        for char in name.lower():
            if char.isascii() and (char.isalnum() or char in ("-", "_")):
                result.append(char)
            elif char == " ":
                result.append("_")
        slug = "".join(result)

    import re
    slug = re.sub(r"_+", "_", slug).strip("_")
    return slug if slug else "npy"


def build_identity_string(meta: dict) -> str:
    """从 meta 构建关系描述字符串"""
    profile = meta.get("profile", {})
    parts = []

    gender = profile.get("gender", "")
    age_range = profile.get("age_range", "")
    occupation = profile.get("occupation", "")
    rel_stage = profile.get("rel_stage", "")

    if gender:
        parts.append(gender)
    if age_range:
        parts.append(age_range)
    if occupation:
        parts.append(occupation)
    if rel_stage:
        parts.append(rel_stage)

    return "，".join(parts) if parts else "理想伴侣"


def create_npy_skill(
    base_dir: Path,
    slug: str,
    meta: dict,
    persona_content: str,
    relationship_content: str = "",
    symlink_to_global: bool = True,
) -> Path:
    """创建新的 npy Skill 目录结构

    Args:
        base_dir: skills 目录路径（.claude/skills/）
        slug: TA 的唯一标识
        meta: 元数据
        persona_content: persona.md 内容
        relationship_content: relationship.md 内容
        symlink_to_global: 是否创建符号链接到全局 skills 目录
    """

    skill_dir = base_dir / slug
    skill_dir.mkdir(parents=True, exist_ok=True)

    # 创建子目录
    (skill_dir / "versions").mkdir(exist_ok=True)
    (skill_dir / "knowledge" / "chats").mkdir(parents=True, exist_ok=True)
    (skill_dir / "knowledge" / "moments").mkdir(parents=True, exist_ok=True)

    # 写入 persona.md
    (skill_dir / "persona.md").write_text(persona_content, encoding="utf-8")

    # 写入 relationship.md
    if not relationship_content:
        relationship_content = "# 关系记忆\n\n暂无记录。\n"
    (skill_dir / "relationship.md").write_text(relationship_content, encoding="utf-8")

    # 生成并写入 SKILL.md
    name = meta.get("name", slug)
    identity = build_identity_string(meta)
    skill_md = SKILL_MD_TEMPLATE.format(
        slug=slug,
        name=name,
        identity=identity,
        persona_content=persona_content,
        relationship_content=relationship_content,
    )
    (skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")

    # 写入 meta.json
    now = datetime.now(timezone.utc).isoformat()
    meta["slug"] = slug
    meta.setdefault("created_at", now)
    meta["updated_at"] = now
    meta["version"] = "v1"
    meta.setdefault("adjustments_count", 0)
    meta.setdefault("moments_count", 0)
    (skill_dir / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # 创建符号链接到全局 skills 目录，让 Claude Code 和 OpenClaw 能识别
    if symlink_to_global:
        link_result = create_global_skill_link(skill_dir, slug)
        if link_result["links"]:
            meta["_global_links"] = link_result["links"]
        if link_result["errors"]:
            for err in link_result["errors"]:
                print(f"提示：{err}", file=__import__("sys").stderr)

    return skill_dir


def update_npy_skill(
    skill_dir: Path,
    persona_patch: Optional[str] = None,
    relationship_patch: Optional[str] = None,
    adjustment: Optional[dict] = None,
    moment: Optional[dict] = None,
) -> str:
    """更新现有 Skill，先存档当前版本，再写入更新"""

    meta_path = skill_dir / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))

    current_version = meta.get("version", "v1")
    try:
        version_num = int(current_version.lstrip("v").split("_")[0]) + 1
    except ValueError:
        version_num = 2
    new_version = f"v{version_num}"

    # 存档当前版本
    version_dir = skill_dir / "versions" / current_version
    version_dir.mkdir(parents=True, exist_ok=True)
    for fname in ("SKILL.md", "persona.md", "relationship.md"):
        src = skill_dir / fname
        if src.exists():
            shutil.copy2(src, version_dir / fname)

    # 应用 persona patch 或 adjustment
    if persona_patch or adjustment:
        current_persona = (skill_dir / "persona.md").read_text(encoding="utf-8")

        if adjustment:
            adjustment_line = (
                f"\n### A{meta.get('adjustments_count', 0) + 1}：{adjustment.get('name', '调整')}（{datetime.now().strftime('%Y-%m-%d')}）\n"
            )
            if adjustment.get("original"):
                adjustment_line += f"原规则：{adjustment['original']}\n"
            adjustment_line += f"调整内容：{adjustment['content']}\n"
            adjustment_line += f"用户说明：\"{adjustment['user_note']}\"\n"
            adjustment_line += "优先级：高于原有规则\n"

            target = "## Adjustment 记录"
            if target in current_persona:
                insert_pos = current_persona.index(target) + len(target)
                rest = current_persona[insert_pos:]
                skip = "\n\n（暂无记录）"
                if rest.startswith(skip):
                    rest = rest[len(skip):]
                new_persona = current_persona[:insert_pos] + adjustment_line + rest
            else:
                new_persona = current_persona + f"\n\n## Adjustment 记录\n{adjustment_line}\n"

            meta["adjustments_count"] = meta.get("adjustments_count", 0) + 1
        else:
            new_persona = current_persona + "\n\n" + persona_patch

        (skill_dir / "persona.md").write_text(new_persona, encoding="utf-8")

    # 应用 relationship patch 或 moment
    if relationship_patch or moment:
        current_relationship = (skill_dir / "relationship.md").read_text(encoding="utf-8")

        if moment:
            moment_line = (
                f"\n### {moment.get('date', datetime.now().strftime('%Y-%m-%d'))} — {moment.get('title', '重要时刻')}\n"
                f"{moment.get('description', '')}\n"
                f"TA的回应：{moment.get('response', '')}\n"
                f"我的感受：{moment.get('feeling', '')}\n"
            )

            target = "## 重要时刻"
            if target in current_relationship:
                insert_pos = current_relationship.index(target) + len(target)
                rest = current_relationship[insert_pos:]
                skip = "\n\n暂无重要时刻记录"
                if rest.startswith(skip):
                    rest = rest[len(skip):]
                new_relationship = current_relationship[:insert_pos] + moment_line + rest
            else:
                new_relationship = current_relationship + f"\n\n## 重要时刻\n{moment_line}\n"

            meta["moments_count"] = meta.get("moments_count", 0) + 1
        else:
            new_relationship = current_relationship + "\n\n" + relationship_patch

        (skill_dir / "relationship.md").write_text(new_relationship, encoding="utf-8")

    # 重新生成 SKILL.md
    persona_content = (skill_dir / "persona.md").read_text(encoding="utf-8")
    relationship_content = (skill_dir / "relationship.md").read_text(encoding="utf-8")
    name = meta.get("name", skill_dir.name)
    identity = build_identity_string(meta)
    skill_md = SKILL_MD_TEMPLATE.format(
        slug=skill_dir.name,
        name=name,
        identity=identity,
        persona_content=persona_content,
        relationship_content=relationship_content,
    )
    (skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")

    # 更新 meta
    meta["version"] = new_version
    meta["updated_at"] = datetime.now(timezone.utc).isoformat()
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    return new_version


def delete_npy_skill(skill_dir: Path, cleanup_global_links: bool = True) -> bool:
    """删除 npy Skill

    Args:
        skill_dir: skill 目录路径
        cleanup_global_links: 是否同时删除全局链接
    """
    if not skill_dir.exists():
        return False

    # 读取 meta 获取 slug
    meta_path = skill_dir / "meta.json"
    slug = skill_dir.name
    if meta_path.exists():
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            slug = meta.get("slug", slug)
        except Exception:
            pass

    # 删除目录
    shutil.rmtree(skill_dir)

    # 删除全局链接（Claude Code 和 OpenClaw）
    if cleanup_global_links:
        removed = remove_global_skill_link(slug)
        if removed:
            print(f"已清理全局链接：{', '.join(removed)}")

    return True


def list_npys(base_dir: Path) -> list:
    """列出所有已创建的 npy Skill"""
    npys = []
    if not base_dir.exists():
        return npys

    for skill_dir in sorted(base_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        # 跳过 npy 本身（这是创建器）
        if skill_dir.name == "npy":
            continue
        meta_path = skill_dir / "meta.json"
        if not meta_path.exists():
            continue
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except Exception:
            continue

        npys.append({
            "slug": meta.get("slug", skill_dir.name),
            "name": meta.get("name", skill_dir.name),
            "identity": build_identity_string(meta),
            "version": meta.get("version", "v1"),
            "updated_at": meta.get("updated_at", ""),
            "adjustments_count": meta.get("adjustments_count", 0),
            "moments_count": meta.get("moments_count", 0),
        })

    return npys


def get_skills_base_dir() -> Path:
    """获取 skills 存放的基础目录

    每个 TA 直接创建为独立的 skill，放在 .claude/skills/{slug}/ 目录

    优先级：
    1. 如果在 .claude/skills/npy 目录下，使用父目录（.claude/skills/）
    2. 如果在项目根目录（有 .claude 文件夹），使用 .claude/skills/
    3. 否则使用全局目录 ~/.claude/skills/
    """
    import os

    # 检查环境变量
    skill_dir_env = os.environ.get("CLAUDE_SKILL_DIR", "")
    if skill_dir_env:
        return Path(skill_dir_env).parent  # 返回 skills 目录，而不是 npy 目录

    current = Path.cwd()

    # 检查是否已经在 skill 目录中（.claude/skills/npy）
    if (current / "SKILL.md").exists() and current.name == "npy":
        # 当前是 npy skill 目录，返回父目录（skills 目录）
        return current.parent

    # 向上查找 .claude 目录
    for parent in [current] + list(current.parents):
        if (parent / ".claude" / "skills").exists():
            # 找到了项目的 .claude/skills 目录
            return parent / ".claude" / "skills"
        if (parent / "SKILL.md").exists() and parent.name == "npy":
            return parent.parent

    # 默认使用全局目录
    global_skills = Path.home() / ".claude" / "skills"
    if global_skills.exists():
        return global_skills

    # 最后回退到当前目录的 .claude/skills
    return current / ".claude" / "skills"


def get_global_skills_dirs() -> list[Path]:
    """获取全局 skills 目录列表（支持 Claude Code 和 OpenClaw）

    Returns:
        目录列表，按优先级排序
    """
    dirs = []

    # Claude Code 全局目录
    claude_global = Path.home() / ".claude" / "skills"
    if claude_global.exists():
        dirs.append(claude_global)

    # OpenClaw 目录
    openclaw_global = Path.home() / ".openclaw" / "workspace" / "skills"
    if openclaw_global.exists():
        dirs.append(openclaw_global)

    # 如果都不存在，返回默认的 Claude Code 目录
    if not dirs:
        dirs.append(claude_global)

    return dirs


def create_global_skill_link(skill_dir: Path, slug: str) -> dict:
    """在全局 skills 目录创建符号链接

    Args:
        skill_dir: skill 目录路径
        slug: skill 标识

    Returns:
        创建的链接信息
    """
    import os

    links_created = []
    errors = []

    for global_dir in get_global_skills_dirs():
        global_link = global_dir / slug

        # 确保目录存在
        global_dir.mkdir(parents=True, exist_ok=True)

        # 如果链接已存在，先删除
        if global_link.exists() or global_link.is_symlink():
            try:
                if global_link.is_symlink():
                    global_link.unlink()
                else:
                    shutil.rmtree(global_link)
            except OSError as e:
                errors.append(f"无法删除已存在的 {global_link}: {e}")
                continue

        # 创建符号链接
        try:
            global_link.symlink_to(skill_dir)
            links_created.append(str(global_link))
        except OSError as e:
            # 可能跨文件系统，尝试复制
            try:
                shutil.copytree(skill_dir, global_link)
                links_created.append(f"{global_link} (副本)")
            except OSError as e2:
                errors.append(f"无法创建链接或副本 {global_link}: {e2}")

    return {
        "links": links_created,
        "errors": errors,
    }


def remove_global_skill_link(slug: str) -> list[str]:
    """删除全局 skills 目录中的符号链接

    Args:
        slug: skill 标识

    Returns:
        删除的链接列表
    """
    removed = []

    for global_dir in get_global_skills_dirs():
        global_link = global_dir / slug
        if global_link.is_symlink() or global_link.exists():
            try:
                if global_link.is_symlink():
                    global_link.unlink()
                else:
                    shutil.rmtree(global_link)
                removed.append(str(global_link))
            except OSError:
                pass

    return removed


def get_npy_skill_dir() -> Path:
    """获取 npy skill 本身的目录"""
    import os

    skill_dir_env = os.environ.get("CLAUDE_SKILL_DIR", "")
    if skill_dir_env:
        return Path(skill_dir_env)

    current = Path.cwd()

    # 检查当前是否就是 npy skill 目录
    if (current / "SKILL.md").exists() and current.name == "npy":
        return current

    # 向上查找
    for parent in [current] + list(current.parents):
        if (parent / ".claude" / "skills" / "npy").exists():
            return parent / ".claude" / "skills" / "npy"
        if (parent / "SKILL.md").exists() and parent.name == "npy":
            return parent

    return current


def main() -> None:
    parser = argparse.ArgumentParser(description="npy Skill 文件写入器")
    parser.add_argument("--action", required=True, choices=["create", "update", "list", "delete"])
    parser.add_argument("--slug", help="npy slug（用于目录名）")
    parser.add_argument("--name", help="npy 称呼")
    parser.add_argument("--meta", help="meta.json 文件路径")
    parser.add_argument("--persona", help="persona.md 内容文件路径")
    parser.add_argument("--relationship", help="relationship.md 内容文件路径")
    parser.add_argument("--persona-patch", help="persona.md 增量更新内容文件路径")
    parser.add_argument("--relationship-patch", help="relationship.md 增量更新内容文件路径")
    parser.add_argument("--adjustment", help="adjustment JSON 字符串")
    parser.add_argument("--moment", help="moment JSON 字符串")
    parser.add_argument(
        "--base-dir",
        default="",
        help="npy Skill 根目录（默认：.claude/skills/）",
    )
    args = parser.parse_args()

    base_dir = Path(args.base_dir).expanduser() if args.base_dir else None

    # 如果没有指定 base_dir，尝试自动检测
    if not base_dir:
        # 检查环境变量 CLAUDE_SKILL_DIR
        import os
        skill_dir_env = os.environ.get("CLAUDE_SKILL_DIR", "")
        if skill_dir_env:
            # CLAUDE_SKILL_DIR 指向的是 npy skill 目录
            base_dir = Path(skill_dir_env)
        else:
            # 尝试检测当前是否在项目目录中
            current = Path.cwd()

            # 检查是否在 .claude/skills/npy 目录
            if (current.name == "npy" and (current.parent.name == "skills")):
                # 当前就是 npy skill 目录，skills 写在同级目录
                base_dir = current.parent
            elif (current / ".claude" / "skills").exists():
                # 项目有 .claude/skills 目录
                base_dir = current / ".claude" / "skills"
            elif (current / "SKILL.md").exists():
                # 当前目录是某个 skill 目录
                base_dir = current.parent
            else:
                # 默认使用项目内的 .claude/skills 目录
                base_dir = current / ".claude" / "skills"

    print(f"[DEBUG] base_dir: {base_dir}", file=sys.stderr)

    if args.action == "list":
        npys = list_npys(base_dir)
        if not npys:
            print("暂无已创建的 npy Skill\n")
            print("创建新的：/npy")
        else:
            print(f"已创建 {len(npys)} 个 npy Skill：\n")
            for n in npys:
                updated = n["updated_at"][:10] if n["updated_at"] else "未知"
                print(f"[{n['slug']}] {n['name']} — {n['identity']}")
                print(f"  版本: {n['version']} 调整次数: {n['adjustments_count']} 重要时刻: {n['moments_count']} 更新: {updated}")
                print()
            print("---")
            print("和TA对话：/{slug}")
            print("删除：/move-on {slug}")

    elif args.action == "create":
        if not args.slug and not args.name:
            print("错误：create 操作需要 --slug 或 --name", file=sys.stderr)
            sys.exit(1)

        meta: dict = {}
        if args.meta:
            meta = json.loads(Path(args.meta).read_text(encoding="utf-8"))
        if args.name:
            meta["name"] = args.name

        slug = args.slug or slugify(meta.get("name", "npy"))

        persona_content = ""
        if args.persona:
            persona_content = Path(args.persona).read_text(encoding="utf-8")

        relationship_content = ""
        if args.relationship:
            relationship_content = Path(args.relationship).read_text(encoding="utf-8")

        skill_dir = create_npy_skill(base_dir, slug, meta, persona_content, relationship_content)
        print(f"✅ 已创建：/{slug}")
        print(f"  和TA对话：/{slug}")
        print(f"  调整TA：说\"我希望TA更...\"或\"TA不会这样...\"")
        print(f"  列出所有：/list-npys")

    elif args.action == "update":
        if not args.slug:
            print("错误：update 操作需要 --slug", file=sys.stderr)
            sys.exit(1)

        skill_dir = base_dir / args.slug
        if not skill_dir.exists():
            print(f"错误：找不到 npy 目录 {skill_dir}", file=sys.stderr)
            sys.exit(1)

        persona_patch = Path(args.persona_patch).read_text(encoding="utf-8") if args.persona_patch else None
        relationship_patch = Path(args.relationship_patch).read_text(encoding="utf-8") if args.relationship_patch else None
        adjustment = json.loads(args.adjustment) if args.adjustment else None
        moment = json.loads(args.moment) if args.moment else None

        new_version = update_npy_skill(skill_dir, persona_patch, relationship_patch, adjustment, moment)
        print(f"✅ 已更新到 {new_version}")

    elif args.action == "delete":
        if not args.slug:
            print("错误：delete 操作需要 --slug", file=sys.stderr)
            sys.exit(1)

        skill_dir = base_dir / args.slug
        if delete_npy_skill(skill_dir):
            print(f"💔 已删除 {args.slug}")
            print("有时候，放手也是一种温柔。")
            print("如果以后想创建新的TA，随时可以用 /npy 开始。")
        else:
            print(f"错误：找不到 npy 目录 {skill_dir}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()