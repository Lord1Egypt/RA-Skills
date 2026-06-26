#!/usr/bin/env bash
# ============================================================
#  Hermes Skills — Auto-Installer
#  المهارات المرسلة عبر hermes-share
# ============================================================
#  طريقة الاستخدام:
#    1. فك الملف المضغوط
#    2. شغّل: bash install.sh
# ============================================================

set -e

HERMES_SKILLS="${HERMES_HOME:-$HOME/.hermes}/skills"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# ─── الألوان ──────────────────────────────────────────────
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

echo ""
echo -e "${CYAN}🜔  Hermes Skills Installer${NC}"
echo -e "${CYAN}==========================${NC}"
echo ""

# ─── التأكد من وجود مجلد المهارات ─────────────────────────
if [[ ! -d "$HERMES_SKILLS" ]]; then
    echo -e "${YELLOW}📁 إنشاء مجلد المهارات: $HERMES_SKILLS${NC}"
    mkdir -p "$HERMES_SKILLS"
fi

INSTALLED=0
SKIPPED=0
FAILED=0

# ─── تثبيت كل مجلد مهارة ──────────────────────────────────
for skill_dir in "$SCRIPT_DIR"/*/; do
    skill_name=$(basename "$skill_dir")

    # تخطي الملفات
    [[ ! -d "$skill_dir" ]] && continue

    # تخطي السكريبت نفسه
    [[ "$skill_name" == "install.sh" ]] && continue

    # التأكد من وجود SKILL.md
    if [[ ! -f "$skill_dir/SKILL.md" ]]; then
        echo -e "${YELLOW}⚠️  $skill_name — لا تحتوي على SKILL.md، تخطي...${NC}"
        SKIPPED=$((SKIPPED + 1))
        continue
    fi

    # البحث عن مجلد موجود مسبقاً (قد يكون في تصنيف فرعي)
    target="$HERMES_SKILLS/$skill_name"
    existing=$(find "$HERMES_SKILLS" -name "$skill_name" -type d -maxdepth 4 2>/dev/null | head -1)

    if [[ -n "$existing" ]]; then
        echo -e "${YELLOW}⏭️  $skill_name — موجودة مسبقاً في: $(basename $(dirname $existing))/"
        echo -e "    للتحديث: احذف المهارة القديمة أولاً ثم أعد التثبيت${NC}"
        SKIPPED=$((SKIPPED + 1))
    else
        # تحديد التصنيف من المسار الأصلي (إن وجد)
        skill_md="$skill_dir/SKILL.md"
        category=""
        if [[ -f "$skill_md" ]]; then
            # محاولة استخراج التصنيف من أول سطر تعليق في SKILL.md
            category_line=$(head -20 "$skill_md" | grep -i "category:" | head -1 || true)
            if [[ -n "$category_line" ]]; then
                category=$(echo "$category_line" | sed 's/.*category:[[:space:]]*//i' | xargs)
            fi
        fi

        if [[ -n "$category" && "$category" != "general" ]]; then
            target="$HERMES_SKILLS/$category/$skill_name"
        fi

        echo -e "📦 ${GREEN}تثبيت${NC} $skill_name..."
        mkdir -p "$(dirname "$target")"
        cp -r "$skill_dir" "$target"
        echo -e "   ${GREEN}✓ تم${NC}"
        INSTALLED=$((INSTALLED + 1))
    fi
done

# ─── الملخص ───────────────────────────────────────────────
echo ""
echo -e "${CYAN}==========================${NC}"
echo -e "${GREEN}✓ تم تثبيت: $INSTALLED مهارة${NC}"
if [[ $SKIPPED -gt 0 ]]; then
    echo -e "${YELLOW}⏭️  تم تخطي: $SKIPPED مهارة (موجودة مسبقاً)${NC}"
fi
if [[ $FAILED -gt 0 ]]; then
    echo -e "${RED}✗ فشل: $FAILED مهارة${NC}"
fi
echo ""

# ─── الخطوة التالية ───────────────────────────────────────
if [[ $INSTALLED -gt 0 ]]; then
    echo -e "${CYAN}📋 للتحقق من المهارات المثبتة:${NC}"
    echo "   hermes skills list"
    echo ""
    echo -e "${CYAN}💡 لتحميل المهارات الجديدة في جلستك الحالية:${NC}"
    echo "   /reset"
    echo "   أو ابدأ جلسة جديدة"
fi

echo ""
