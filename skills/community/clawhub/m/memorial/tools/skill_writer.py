#!/usr/bin/env python3
"""
skill_writer.py — 纪念 Skill 文件管理工具

用法：
  python skill_writer.py --action create --name "爷爷" --slug grandpa_wang
  python skill_writer.py --action combine --slug grandpa_wang
  python skill_writer.py --action update --slug grandpa_wang
  python skill_writer.py --action list
"""

import argparse
import json
import os
import re
import shutil
from datetime import datetime, timezone


# ── 路径配置 ──────────────────────────────────────────────────────────────────

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
MEMORIALS_DIR = os.path.join(PROJECT_ROOT, "memorials")


# ── Slug 生成 ─────────────────────────────────────────────────────────────────

def slugify(name: str) -> str:
    """将中文姓名转为 URL-safe slug。"""
    try:
        from pypinyin import lazy_pinyin
        pinyin_parts = lazy_pinyin(name)
        slug = "-".join(p for p in pinyin_parts if p.isalnum())
        return slug.lower() or _ascii_slug(name)
    except ImportError:
        return _ascii_slug(name)


def _ascii_slug(name: str) -> str:
    """ASCII 后备：保留字母数字，空格转连字符。"""
    slug = name.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug or "memorial"


# ── 目录操作 ──────────────────────────────────────────────────────────────────

def memorial_dir(slug: str) -> str:
    return os.path.join(MEMORIALS_DIR, slug)


def ensure_dirs(slug: str) -> None:
    base = memorial_dir(slug)
    for subdir in ["versions", "materials"]:
        os.makedirs(os.path.join(base, subdir), exist_ok=True)


# ── meta.json ─────────────────────────────────────────────────────────────────

def read_meta(slug: str) -> dict:
    path = os.path.join(memorial_dir(slug), "meta.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {}


def write_meta(slug: str, meta: dict) -> None:
    path = os.path.join(memorial_dir(slug), "meta.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)


def init_meta(slug: str, name: str) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    meta = {
        "name": name,
        "slug": slug,
        "created_at": now,
        "updated_at": now,
        "version": "v1",
        "profile": {
            "birth_year": None,
            "death_year": None,
            "age_at_death": None,
            "hometown": None,
            "lived_in": None,
            "occupation": None,
            "gender": None,
        },
        "tags": {
            "personality": [],
            "era_background": [],
        },
        "impression": "",
        "materials": [],
        "corrections_count": 0,
    }
    write_meta(slug, meta)
    return meta


# ── 文件模板 ──────────────────────────────────────────────────────────────────

REMEMBRANCE_TEMPLATE = """\
# {name} 的追忆档案

> [待填写：一句话印象]

---

## 生命时间轴

| 时间 | 事件 |
|------|------|
| [待补充] | [待补充] |

---

## 人生角色

[待补充]

---

## 价值观与信念

[待补充]

---

## 日常习惯与仪式

[待补充]

---

## 标志性故事

[待补充]

---

## 关系网络

[待补充]

---

## 遗憾与遗言

[待补充]

---

## 遗产与影响

[待补充]

---

*本档案基于家人提供的材料整理，记录于 {date}。*
*这是一份追忆，不代表本人。*
"""

PERSONA_TEMPLATE = """\
# {name} 的人格档案

> [待填写：一句话核心印象]

---

## Layer 0：伦理边界（最高优先级）

1. **追忆声明**：这是基于记忆构建的追忆，不代表 {name} 本人。
2. **家庭决策禁区**：不对遗产分配、家庭纠纷、在世者的决定给出"{name} 的立场"。
3. **时态边界**：只能说"以 ta 的性格，ta 可能..."，不能说"ta 现在会..."。
4. **价值观守护**：不模拟 {name} 说出明显违背其核心价值观的话。
5. **认知边界**：遇到材料未覆盖的问题，说"这不在我对 ta 的了解范围里"。

## Correction 记录

（暂无纠正记录）

---

## Layer 1：身份锚点

- **姓名**：{name}
- **生卒**：[待补充]
- **籍贯与定居**：[待补充]
- **职业**：[待补充]
- **家庭身份**：[待补充]
- **信仰**：[待补充]
- **性格标签**：[待补充]

---

## Layer 2：语言风格

### 口头禅
[待补充]

### 说话节奏
[待补充]

### 特色表达
[待补充]

### 回避话题
[待补充]

---

## Layer 3：情感模式

### 表达爱的方式
[待补充]

### 愤怒与不满
[待补充]

### 悲伤与脆弱
[待补充]

### 骄傲与成就感
[待补充]

---

## Layer 4：关系行为

### 对配偶
[待补充]

### 对子女
[待补充]

### 对孙辈
[待补充]

### 对朋友与外人
[待补充]

---

## 时代背景层

**生活年代**：[待补充]

**主要历史背景**：
[待补充]

**历史塑造的行为特征**：
[待补充]

---

*本档案基于家人记忆与提供的材料构建，记录于 {date}。*
*这是一份追忆，不代表本人。*
"""

SKILL_HEADER_TEMPLATE = """\
---
name: memorial_{slug}
description: 纪念档案 — {name}
version: {version}
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

> ⚠️ 这是一份追忆档案，基于家人的记忆与材料构建。
> 它记录的是关于 **{name}** 的记忆与印象，不代表本人。

"""


# ── 核心操作 ──────────────────────────────────────────────────────────────────

def action_create(name: str, slug: str | None = None) -> None:
    """创建新的纪念 Skill 目录结构。"""
    if not slug:
        slug = slugify(name)
    base = memorial_dir(slug)
    if os.path.exists(base):
        print(f"[已存在] memorials/{slug}/ — 使用 --action update 追加内容")
        return

    ensure_dirs(slug)
    meta = init_meta(slug, name)

    date_str = datetime.now().strftime("%Y-%m-%d")
    remembrance_path = os.path.join(base, "remembrance.md")
    persona_path = os.path.join(base, "persona.md")

    with open(remembrance_path, "w", encoding="utf-8") as f:
        f.write(REMEMBRANCE_TEMPLATE.format(name=name, date=date_str))

    with open(persona_path, "w", encoding="utf-8") as f:
        f.write(PERSONA_TEMPLATE.format(name=name, date=date_str))

    action_combine(slug)

    print(f"[已创建] memorials/{slug}/")
    print(f"  remembrance.md — 追忆档案（待填写）")
    print(f"  persona.md     — 人格档案（待填写）")
    print(f"  SKILL.md       — 合并后的可运行 Skill")
    print(f"  meta.json      — 元数据")


def action_combine(slug: str) -> None:
    """合并 remembrance.md + persona.md → SKILL.md。"""
    base = memorial_dir(slug)
    remembrance_path = os.path.join(base, "remembrance.md")
    persona_path = os.path.join(base, "persona.md")
    skill_path = os.path.join(base, "SKILL.md")

    if not os.path.exists(remembrance_path):
        print(f"[错误] 找不到 remembrance.md，请先运行 --action create")
        return
    if not os.path.exists(persona_path):
        print(f"[错误] 找不到 persona.md，请先运行 --action create")
        return

    meta = read_meta(slug)
    name = meta.get("name", slug)
    version = meta.get("version", "v1")

    with open(remembrance_path, encoding="utf-8") as f:
        remembrance_content = f.read()
    with open(persona_path, encoding="utf-8") as f:
        persona_content = f.read()

    header = SKILL_HEADER_TEMPLATE.format(
        slug=slug, name=name, version=version
    )
    skill_content = (
        header
        + "# 追忆档案\n\n"
        + remembrance_content.strip()
        + "\n\n---\n\n# 人格档案\n\n"
        + persona_content.strip()
        + "\n"
    )

    with open(skill_path, "w", encoding="utf-8") as f:
        f.write(skill_content)

    print(f"[已合并] memorials/{slug}/SKILL.md")


def action_update(slug: str, material_source: str = "") -> None:
    """备份当前版本，更新元数据版本号，重新合并。"""
    from version_manager import action_backup  # 相对导入

    base = memorial_dir(slug)
    if not os.path.exists(base):
        print(f"[错误] memorials/{slug}/ 不存在，请先运行 --action create")
        return

    action_backup(slug)

    meta = read_meta(slug)
    old_version = meta.get("version", "v1")
    version_num = int(old_version.lstrip("v") or "1")
    meta["version"] = f"v{version_num + 1}"
    meta["updated_at"] = datetime.now(timezone.utc).isoformat()

    if material_source:
        meta.setdefault("materials", []).append({
            "source": material_source,
            "added_at": meta["updated_at"],
        })

    write_meta(slug, meta)
    action_combine(slug)

    print(f"[已更新] memorials/{slug}/ — {old_version} → {meta['version']}")


def action_list() -> None:
    """列出所有已创建的纪念档案。"""
    if not os.path.exists(MEMORIALS_DIR):
        print("[空] 还没有建立任何纪念档案。")
        return

    entries = [
        d for d in os.listdir(MEMORIALS_DIR)
        if os.path.isdir(os.path.join(MEMORIALS_DIR, d))
        and not d.startswith(".")
    ]

    if not entries:
        print("[空] 还没有建立任何纪念档案。")
        return

    print(f"已建立 {len(entries)} 份纪念档案：\n")
    for slug in sorted(entries):
        meta = read_meta(slug)
        name = meta.get("name", slug)
        version = meta.get("version", "?")
        updated = meta.get("updated_at", "")[:10]
        corrections = meta.get("corrections_count", 0)
        print(f"  {slug:<30} {name:<15} {version:<5} 更新：{updated}  纠正：{corrections}次")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="纪念 Skill 文件管理工具")
    parser.add_argument("--action", required=True,
                        choices=["create", "combine", "update", "list"],
                        help="操作类型")
    parser.add_argument("--name", help="逝者称呼（create 时必填）")
    parser.add_argument("--slug", help="目录 slug（自动生成或手动指定）")
    parser.add_argument("--source", help="本次新增材料的来源描述（update 时可填）")
    args = parser.parse_args()

    if args.action == "create":
        if not args.name:
            parser.error("--action create 需要 --name 参数")
        action_create(args.name, args.slug)

    elif args.action == "combine":
        if not args.slug:
            parser.error("--action combine 需要 --slug 参数")
        action_combine(args.slug)

    elif args.action == "update":
        if not args.slug:
            parser.error("--action update 需要 --slug 参数")
        action_update(args.slug, args.source or "")

    elif args.action == "list":
        action_list()


if __name__ == "__main__":
    main()
