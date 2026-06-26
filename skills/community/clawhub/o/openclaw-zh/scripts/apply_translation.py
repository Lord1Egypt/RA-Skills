#!/usr/bin/env python3
"""
OpenClaw Control UI 中文翻译应用脚本

用法:
    python3 apply_translation.py              # 应用中文翻译
    python3 apply_translation.py --restore    # 恢复英文（从备份）
    python3 apply_translation.py --dry-run    # 预览更改，不实际修改
"""

import json
import os
import re
import shutil
from pathlib import Path
from datetime import datetime

# 配置
OPENCLAW_ROOT = Path("/usr/lib/node_modules/openclaw")
CONTROL_UI_JS = OPENCLAW_ROOT / "dist/control-ui/assets"
SKILL_ROOT = Path(__file__).parent.parent
TRANSLATIONS_FILE = SKILL_ROOT / "translations/control-ui-zh.json"
BACKUP_DIR = SKILL_ROOT / "backups"


def load_translations() -> dict:
    """加载翻译映射"""
    if not TRANSLATIONS_FILE.exists():
        print(f"❌ 翻译文件不存在: {TRANSLATIONS_FILE}")
        return {}
    with open(TRANSLATIONS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def find_js_file() -> Path | None:
    """查找 Control UI 的 JS 文件"""
    if not CONTROL_UI_JS.exists():
        print(f"❌ Control UI 目录不存在: {CONTROL_UI_JS}")
        return None

    for f in CONTROL_UI_JS.iterdir():
        if f.suffix == '.js' and not f.name.endswith('.map'):
            return f
    return None


def backup_file(file_path: Path) -> Path:
    """备份原始文件"""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"{file_path.name}.{timestamp}.bak"
    shutil.copy2(file_path, backup_path)
    print(f"📦 备份保存到: {backup_path}")
    return backup_path


def find_latest_backup(js_file: Path) -> Path | None:
    """找到最新的备份文件"""
    if not BACKUP_DIR.exists():
        return None

    backups = sorted(
        BACKUP_DIR.glob(f"{js_file.name}.*.bak"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )
    return backups[0] if backups else None


def apply_translations(js_file: Path, translations: dict, dry_run: bool = False) -> int:
    """应用翻译到 JS 文件"""
    with open(js_file, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    changes = 0

    # 按长度降序排序，避免短字符串误匹配
    sorted_translations = sorted(translations.items(), key=lambda x: -len(x[0]))

    for english, chinese in sorted_translations:
        # 精确匹配带引号的字符串
        patterns = [
            f'"{re.escape(english)}"',
            f"'{re.escape(english)}'",
        ]
        for pattern in patterns:
            matches = list(re.finditer(pattern, content))
            for match in matches:
                old_text = match.group()
                new_text = old_text.replace(english, chinese)
                if old_text != new_text:
                    if dry_run:
                        print(f"  '{english}' → '{chinese}'")
                    else:
                        content = content.replace(old_text, new_text, 1)
                    changes += 1

    if not dry_run and changes > 0:
        with open(js_file, 'w', encoding='utf-8') as f:
            f.write(content)

    return changes


def restore_from_backup(js_file: Path) -> bool:
    """从备份恢复"""
    backup = find_latest_backup(js_file)
    if not backup:
        print("❌ 未找到备份文件")
        return False

    shutil.copy2(backup, js_file)
    print(f"✅ 已从备份恢复: {backup}")
    return True


def main():
    import sys

    dry_run = '--dry-run' in sys.argv
    restore = '--restore' in sys.argv

    print("🦞 OpenClaw Control UI 中文翻译工具")
    print("=" * 40)

    js_file = find_js_file()
    if not js_file:
        print("❌ 未找到 Control UI JS 文件")
        sys.exit(1)

    print(f"📁 目标文件: {js_file}")

    if restore:
        if restore_from_backup(js_file):
            print("✅ 已恢复英文界面")
        sys.exit(0)

    translations = load_translations()
    if not translations:
        print("❌ 无翻译数据")
        sys.exit(1)

    print(f"📝 加载了 {len(translations)} 条翻译")

    if not dry_run:
        backup_file(js_file)

    if dry_run:
        print("\n🔍 预览模式 - 以下字符串将被翻译:\n")

    changes = apply_translations(js_file, translations, dry_run)

    if dry_run:
        print(f"\n📊 将更改 {changes} 处")
    elif changes > 0:
        print(f"✅ 已应用 {changes} 处翻译")
        print("💡 重启 OpenClaw 或刷新浏览器以查看更改")
    else:
        print("⚠️ 未找到需要翻译的内容（可能已翻译）")


if __name__ == "__main__":
    main()
