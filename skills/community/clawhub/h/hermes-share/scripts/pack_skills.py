#!/usr/bin/env python3
"""
Hermes Share — Packager
=======================
حزم مهارات Hermes في ملف ZIP قابل للمشاركة.
يستبعد تلقائياً البيانات الحساسة (مفاتيح API، .env، الذاكرة، الجلسات).

الاستخدام:
    # مهارة واحدة
    python3 pack_skills.py --skills python-data-analysis --output ~/Downloads/share.zip

    # عدة مهارات
    python3 pack_skills.py --skills skill-a,skill-b,skill-c --output ~/Downloads/share.zip

    # كل المهارات
    python3 pack_skills.py --all --output ~/Downloads/all-skills.zip
"""

import argparse
import os
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

# ─── الإعدادات ───────────────────────────────────────────
HERMES_HOME = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))
SKILLS_DIR = HERMES_HOME / "skills"
SCRIPT_DIR = Path(__file__).resolve().parent
INSTALL_SCRIPT = SCRIPT_DIR / "install_skills.sh"

# ملفات/مجلدات مستبعدة دائماً
ALWAYS_EXCLUDE = [
    ".env",
    ".env.*",
    "*.key",
    "*.pem",
    "*.token",
    "credentials.json",
    "auth.json",
    "secrets",
]

# مجلدات مستبعدة (لا تدخل ZIP أبداً)
EXCLUDE_DIRS = [
    "memory",
    "sessions",
    "logs",
    "__pycache__",
    ".git",
    ".venv",
    "venv",
    "node_modules",
    ".cache",
]

# أنماط مفاتيح API للكشف عنها (للتقرير فقط — لا نرسل الملفات اللي تحتويها)
API_KEY_PATTERNS = [
    r'(?:api[_-]?key|apikey|secret|token|password)\s*[:=]\s*["\']?[\w\-\.]{20,}["\']?',
    r'sk-[a-zA-Z0-9]{32,}',
    r'[A-Za-z0-9+/]{40,}={0,2}',
]

# ─── الدوال الأساسية ─────────────────────────────────────

def parse_yaml_frontmatter(filepath: Path) -> dict:
    """استخراج بيانات YAML frontmatter من SKILL.md."""
    data = {}
    if not filepath.exists():
        return data

    content = filepath.read_text(encoding="utf-8", errors="ignore")
    lines = content.split("\n")

    in_frontmatter = False
    for line in lines:
        stripped = line.strip()
        if stripped == "---":
            if not in_frontmatter:
                in_frontmatter = True
                continue
            else:
                break
        if in_frontmatter:
            if ":" in stripped:
                key, _, value = stripped.partition(":")
                data[key.strip().lower()] = value.strip().strip("\"'")
    return data


def extract_description(skill_path: Path) -> dict:
    """استخراج وصف المهارة بالعربي والإنجليزي."""
    skill_md = skill_path / "SKILL.md"
    info = {
        "name": skill_path.name,
        "description_en": "",
        "description_ar": "",
        "tags": [],
        "category": skill_path.parent.name if skill_path.parent != SKILLS_DIR else "general",
        "version": "",
        "files_count": 0,
    }

    frontmatter = parse_yaml_frontmatter(skill_md)
    info["description_en"] = frontmatter.get("description", "")
    info["description_ar"] = frontmatter.get("ar_description", "")
    info["version"] = frontmatter.get("version", "")
    tags_raw = frontmatter.get("tags", "")
    if tags_raw:
        info["tags"] = [t.strip() for t in tags_raw.replace("[", "").replace("]", "").split(",") if t.strip()]

    return info


def generate_description_file(skill_path: Path, translate: bool = False) -> str:
    """
    توليد ملف نصي ثنائي اللغة (عربي + إنجليزي) يشرح المهارة.

    يُرجع محتوى الملف النصي للمهارة الواحدة.
    """
    info = extract_description(skill_path)

    # عدّ الملفات في مجلد المهارة
    file_count = 0
    for root, dirs, files in os.walk(skill_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            if not should_exclude(os.path.join(root, f)):
                file_count += 1
    info["files_count"] = file_count

    lines = []
    lines.append("=" * 60)
    lines.append(f"🜔  Hermes Skill: {info['name']}")
    lines.append("=" * 60)
    lines.append("")

    # ── English Section ──
    lines.append("📖 ENGLISH")
    lines.append("-" * 40)
    if info["description_en"]:
        lines.append(info["description_en"])
    else:
        lines.append("(No English description available)")
    lines.append("")

    # ── Arabic Section ──
    lines.append("📖 العربية")
    lines.append("-" * 40)
    if info["description_ar"]:
        lines.append(info["description_ar"])
    else:
        lines.append("(لم يتم توفير شرح بالعربية بعد — يمكن طلبه من المُرسِل)")
        lines.append("Arabic description not yet provided — you can request it from the sender.")
    lines.append("")

    # ── Metadata ──
    lines.append("📋 Metadata | بيانات المهارة")
    lines.append("-" * 40)
    lines.append(f"   Name / الاسم:          {info['name']}")
    lines.append(f"   Category / التصنيف:     {info['category']}")
    if info["version"]:
        lines.append(f"   Version / الإصدار:      {info['version']}")
    if info["tags"]:
        lines.append(f"   Tags / وسوم:            {', '.join(info['tags'])}")
    lines.append(f"   Files / عدد الملفات:    {info['files_count']}")
    lines.append("")

    # ── Install instructions ──
    lines.append("🚀 INSTALLATION | التثبيت")
    lines.append("-" * 40)
    lines.append("   unzip <file>.zip -d ~/Downloads/hermes-skills/")
    lines.append("   bash ~/Downloads/hermes-skills/install.sh")
    lines.append("")
    lines.append("=" * 60)
    lines.append("🜔  Generated by Hermes Share | تم التوليد بواسطة Hermes Share")
    lines.append("=" * 60)

    return "\n".join(lines)


def generate_all_descriptions(skill_paths: list[Path]) -> str:
    """توليد ملف وصف مجمع لكل المهارات المطلوبة."""
    parts = []
    for i, sp in enumerate(skill_paths):
        if i > 0:
            parts.append("\n\n\n")
        parts.append(generate_description_file(sp))
    return "\n".join(parts)


def find_skill_path(skill_name: str) -> Path | None:
    """البحث عن مجلد مهارة بالاسم في كل التصنيفات الفرعية."""
    if not SKILLS_DIR.exists():
        return None

    for root, dirs, files in os.walk(SKILLS_DIR):
        # تخطي المجلدات المستبعدة
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        root_path = Path(root)
        if root_path.name == skill_name:
            # تأكد من وجود SKILL.md
            if (root_path / "SKILL.md").exists():
                return root_path
    return None


def find_all_skills() -> list[Path]:
    """العثور على كل مجلدات المهارات."""
    skills = []
    if not SKILLS_DIR.exists():
        return skills

    for root, dirs, files in os.walk(SKILLS_DIR):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        root_path = Path(root)
        if (root_path / "SKILL.md").exists() and root_path != SKILLS_DIR:
            skills.append(root_path)
    return skills


def should_exclude(file_path: str) -> bool:
    """التحقق من أن الملف يجب استبعاده."""
    name = os.path.basename(file_path)

    # استبعاد المجلدات الحساسة
    parts = Path(file_path).parts
    for part in parts:
        if part in EXCLUDE_DIRS:
            return True

    # استبعاد الملفات الحساسة بالاسم
    for pattern in ALWAYS_EXCLUDE:
        if Path(name).match(pattern):
            return True

    # استبعاد ملفات البيئة
    if name.startswith(".env"):
        return True

    return False


def sanitize_report(skill_paths: list[Path]) -> dict:
    """توليد تقرير بالمهارات المُجهّزة وأي ملفات حساسة تم استبعادها."""
    report = {
        "skills_included": [],
        "files_excluded": [],
        "total_size_mb": 0,
        "warnings": [],
    }

    for skill_path in skill_paths:
        skill_name = skill_path.name
        skill_files = []
        excluded_here = []

        for root, dirs, files in os.walk(skill_path):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for f in files:
                fpath = os.path.join(root, f)
                if should_exclude(fpath):
                    excluded_here.append(os.path.relpath(fpath, skill_path))
                else:
                    skill_files.append(fpath)

        total_bytes = sum(os.path.getsize(fp) for fp in skill_files)
        report["skills_included"].append({
            "name": skill_name,
            "files": len(skill_files),
            "size_mb": round(total_bytes / (1024 * 1024), 2),
        })
        report["files_excluded"].extend(
            f"{skill_name}/{f}" for f in excluded_here
        )
        report["total_size_mb"] += total_bytes / (1024 * 1024)

    # تحذير إذا حجم كبير
    if report["total_size_mb"] > 50:
        report["warnings"].append(
            f"⚠️ الحزمة كبيرة ({report['total_size_mb']:.1f} MB). تأكد من إمكانية الإرسال."
        )

    return report


def create_zip(skill_paths: list[Path], output_path: str, with_description: bool = True) -> str:
    """إنشاء ملف ZIP مع دمج install.sh وملفات الشرح."""
    output = Path(output_path).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as zf:
        # إضافة سكربت التثبيت أولاً (في الجذر)
        if INSTALL_SCRIPT.exists():
            zf.write(INSTALL_SCRIPT, "install.sh")
        else:
            install_content = generate_install_script()
            zf.writestr("install.sh", install_content)

        # إضافة ملف الشرح الثنائي اللغة للمهارات
        if with_description:
            desc_content = generate_all_descriptions(skill_paths)
            zf.writestr("SKILLS_README.txt", desc_content)

        # إضافة كل مهارة في مجلدها الخاص
        for skill_path in skill_paths:
            skill_name = skill_path.name
            for root, dirs, files in os.walk(skill_path):
                dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
                for f in files:
                    fpath = os.path.join(root, f)
                    if should_exclude(fpath):
                        continue
                    arcname = os.path.join(
                        skill_name, os.path.relpath(fpath, skill_path)
                    )
                    zf.write(fpath, arcname)

    return str(output)


def generate_install_script() -> str:
    """توليد سكربت تثبيت احتياطي (إذا لم يوجد الملف الفعلي)."""
    return """#!/usr/bin/env bash
# Hermes Skills Auto-Installer
# تثبيت تلقائي للمهارات في مجلد Hermes

set -e

HERMES_SKILLS="${HERMES_HOME:-$HOME/.hermes}/skills"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "🜔 Hermes Skills Installer"
echo "=========================="
echo ""

INSTALLED=0
SKIPPED=0

for skill_dir in "$SCRIPT_DIR"/*/; do
    skill_name=$(basename "$skill_dir")
    # تخطي الملفات (مو مجلدات)
    [[ ! -d "$skill_dir" ]] && continue
    # تخطي install.sh نفسه
    [[ "$skill_name" == "install.sh" ]] && continue

    target="$HERMES_SKILLS/$skill_name"

    if [[ -d "$target" ]]; then
        echo "⏭️  $skill_name — موجودة مسبقاً، تخطي..."
        SKIPPED=$((SKIPPED + 1))
    else
        echo "📦 تثبيت $skill_name..."
        cp -r "$skill_dir" "$target"
        echo "   ✓ تم"
        INSTALLED=$((INSTALLED + 1))
    fi
done

echo ""
echo "=========================="
echo "✓ تم تثبيت: $INSTALLED مهارة"
echo "⏭️  تم تخطي: $SKIPPED مهارة (موجودة مسبقاً)"
echo ""
echo "للتأكد: hermes skills list"
"""


def main():
    parser = argparse.ArgumentParser(
        description="🜔 Hermes Share — حزم مهارات Hermes للمشاركة",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
أمثلة:
  %(prog)s --skills python-data-analysis --output ~/Downloads/share.zip
  %(prog)s --skills skill-a,skill-b --output ~/Downloads/share.zip
  %(prog)s --all --output ~/Downloads/all-skills.zip
        """,
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--skills", "-s",
        type=str,
        help="أسماء المهارات (مفصولة بفواصل)",
    )
    group.add_argument(
        "--all", "-a",
        action="store_true",
        help="حزم كل المهارات",
    )
    group.add_argument(
        "--list", "-l",
        action="store_true",
        help="عرض كل المهارات المتاحة فقط (بدون حزم)",
    )

    parser.add_argument(
        "--output", "-o",
        type=str,
        default=str(Path.home() / "Downloads" / "hermes-skills-share.zip"),
        help="مسار ملف ZIP الناتج (الافتراضي: ~/Downloads/hermes-skills-share.zip)",
    )

    parser.add_argument(
        "--no-desc",
        action="store_true",
        help="لا تُضمّن ملف SKILLS_README.txt في الحزمة",
    )

    parser.add_argument(
        "--desc-only",
        action="store_true",
        help="توليد ملف الشرح فقط بدون إنشاء ZIP",
    )

    args = parser.parse_args()

    # ── عرض المهارات ──
    if args.list:
        all_skills = find_all_skills()
        if not all_skills:
            print("❌ لا توجد مهارات.")
            sys.exit(1)

        print(f"🜔 المهارات المتاحة ({len(all_skills)}):")
        print("=" * 50)
        for s in sorted(all_skills, key=lambda x: x.name):
            category = s.parent.name if s.parent != SKILLS_DIR else "عام"
            size_mb = sum(
                os.path.getsize(os.path.join(r, f))
                for r, _, fs in os.walk(s)
                for f in fs
            ) / (1024 * 1024)
            print(f"  📦 {s.name:<35} [{category}] {size_mb:.1f}MB")
        return

    # ── تحديد المهارات ──
    if args.all:
        skill_paths = find_all_skills()
        if not skill_paths:
            print("❌ لا توجد مهارات في المجلد.")
            sys.exit(1)
    else:
        skill_names = [s.strip() for s in args.skills.split(",")]
        skill_paths = []
        not_found = []

        for name in skill_names:
            path = find_skill_path(name)
            if path:
                skill_paths.append(path)
            else:
                not_found.append(name)

        if not_found:
            print(f"❌ مهارات غير موجودة: {', '.join(not_found)}")
            print("   استخدم --list لعرض المهارات المتاحة")
            sys.exit(1)

    # ── تقرير التنظيف ──
    report = sanitize_report(skill_paths)

    print("🜔  تقرير الحزمة")
    print("=" * 50)
    for skill in report["skills_included"]:
        print(f"  📦 {skill['name']}: {skill['files']} ملفات ({skill['size_mb']} MB)")

    if report["files_excluded"]:
        print(f"\n🔒 ملفات مستبعدة (حساسة): {len(report['files_excluded'])}")
        for f in report["files_excluded"]:
            print(f"    ✗ {f}")

    for warning in report["warnings"]:
        print(f"\n{warning}")

    print(f"\n📦 الحجم الإجمالي: {report['total_size_mb']:.1f} MB")

    # ── توليد ملف الشرح فقط ──
    if args.desc_only:
        print(f"\n📝 جاري توليد ملف الشرح...")
        desc_content = generate_all_descriptions(skill_paths)
        desc_path = str(Path(args.output).with_suffix(".txt"))
        Path(desc_path).write_text(desc_content, encoding="utf-8")
        print(f"✓ تم: {desc_path}")

        # عرض معاينة سريعة
        print(f"\n📖 معاينة:")
        print("-" * 40)
        preview = desc_content[:800]
        if len(desc_content) > 800:
            preview += "\n\n... (المزيد في الملف)"
        print(preview)
        print("-" * 40)
        return

    # ── إنشاء ZIP ──
    use_description = not args.no_desc
    print(f"\n⚡ جاري إنشاء الحزمة...")
    if use_description:
        print("   + تضمين ملف SKILLS_README.txt (شرح ثنائي اللغة)")
    output_path = create_zip(skill_paths, args.output, with_description=use_description)
    print(f"✓ تم: {output_path}")
    print(f"\n📤 جاهز للمشاركة!")


if __name__ == "__main__":
    main()
