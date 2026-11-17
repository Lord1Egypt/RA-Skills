#!/usr/bin/env bash
#
# validate-structure.sh - Automated build validation script for k12-teacher skill
#
# Purpose: Verify project structure, file content quality, and constraint compliance
#          against the quality gates defined in README_FOR_AI.md Section 11.
#
# Usage:   ./scripts/validate-structure.sh [root_dir]
#   If root_dir is not provided, defaults to the directory containing this script's parent.
#
# Exit codes:
#   0 - All checks passed
#   1 - One or more checks failed
#
# Note: This script must be set as executable before running:
#   chmod +x scripts/validate-structure.sh
#
# Constraints:
#   C-01  No emoji in any compiled file
#   C-02  All source and documentation files in English
#   C-05  prompts/ files are copy-paste deliverables (no agent-autoinvoke markers)
#   C-08  Single Responsibility per file
#   C-09  Each file under 300 lines unless justified

set -euo pipefail

# ============================================================
# Configuration
# ============================================================

# Determine project root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${1:-${SCRIPT_DIR}/..}"

# Color codes for terminal output (disabled if not a tty)
if [ -t 1 ]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[0;33m'
    BLUE='\033[0;34m'
    NC='\033[0m'
else
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    NC=''
fi

# Counters
CHECKS_PASSED=0
CHECKS_FAILED=0
CHECKS_TOTAL=0

# ============================================================
# Helper Functions
# ============================================================

# Print a passing check result
pass() {
    local check_id="$1"
    local message="$2"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
    CHECKS_TOTAL=$((CHECKS_TOTAL + 1))
    echo -e "${GREEN}[PASS]${NC} ${check_id}: ${message}"
}

# Print a failing check result with optional file/line reference
fail() {
    local check_id="$1"
    local message="$2"
    local detail="${3:-}"
    CHECKS_FAILED=$((CHECKS_FAILED + 1))
    CHECKS_TOTAL=$((CHECKS_TOTAL + 1))
    echo -e "${RED}[FAIL]${NC} ${check_id}: ${message}"
    if [ -n "$detail" ]; then
        echo -e "       ${YELLOW}Detail:${NC} ${detail}"
    fi
}

# Print a warning (non-fatal)
warn() {
    local check_id="$1"
    local message="$2"
    echo -e "${YELLOW}[WARN]${NC} ${check_id}: ${message}"
}

# Print the header banner
print_header() {
    echo ""
    echo -e "${BLUE}============================================${NC}"
    echo -e "${BLUE} k12-teacher Skill - Structure Validation${NC}"
    echo -e "${BLUE}============================================${NC}"
    echo -e "${BLUE} Project Root:${NC} ${PROJECT_ROOT}"
    echo -e "${BLUE} Timestamp:${NC} $(date -u '+%Y-%m-%d %H:%M:%S UTC' 2>/dev/null || date '+%Y-%m-%d %H:%M:%S')"
    echo ""
}

# Print the summary report
print_summary() {
    echo ""
    echo -e "${BLUE}============================================${NC}"
    echo -e "${BLUE} Validation Summary${NC}"
    echo -e "${BLUE}============================================${NC}"
    echo -e " Total checks: ${CHECKS_TOTAL}"
    echo -e " ${GREEN}Passed:${NC} ${CHECKS_PASSED}"
    echo -e " ${RED}Failed:${NC} ${CHECKS_FAILED}"
    echo ""

    if [ "${CHECKS_FAILED}" -eq 0 ]; then
        echo -e "${GREEN}All quality gates passed. Build is valid.${NC}"
    else
        echo -e "${RED}Build validation failed. Please fix the issues above.${NC}"
    fi
    echo ""
}

# ============================================================
# Pre-flight Checks
# ============================================================

# Verify the project root directory exists
if [ ! -d "$PROJECT_ROOT" ]; then
    echo -e "${RED}ERROR: Project root directory not found: ${PROJECT_ROOT}${NC}"
    echo "Usage: $0 [root_dir]"
    exit 2
fi

# Verify the scripts directory exists (this script should be inside it)
if [ ! -d "${PROJECT_ROOT}/scripts" ]; then
    echo -e "${RED}ERROR: scripts/ directory not found in project root.${NC}"
    exit 2
fi

print_header

# ============================================================
# Quality Gate G-01: All required files exist and are non-empty
# ============================================================

echo -e "${BLUE}--- Quality Gate G-01: Required Files Existence ---${NC}"

# Define required files (core project files)
REQUIRED_FILES=(
    ".gitignore"
    ".editorconfig"
    "LICENSE"
    "CONTRIBUTING.md"
    "CODE_OF_CONDUCT.md"
    "CHANGELOG.md"
    "SECURITY.md"
    "README.md"
    "README_FOR_AI.md"
    "SKILL.md"
    "references/method-patterns.md"
    "references/knowledge-base.md"
    "references/syllabus-registry.md"
    "references/grade-crosswalk.md"
    "prompts/01-implement-method.md"
    "prompts/02-robustness-checks.md"
    "tests/test-cases.md"
    "scripts/validate-structure.sh"
    "scripts/knowledge-base-update.sh"
)

# Optional files (should warn but not fail if missing)
OPTIONAL_FILES=(
    "downloads/syllabus"
    ".gitattributes"
    "SUPPORT.md"
    "GOVERNANCE.md"
    ".github/workflows"
    ".github/ISSUE_TEMPLATE"
    ".github/PULL_REQUEST_TEMPLATE.md"
    ".github/CODEOWNERS"
    ".github/dependabot.yml"
)

for file in "${REQUIRED_FILES[@]}"; do
    full_path="${PROJECT_ROOT}/${file}"
    if [ ! -f "$full_path" ]; then
        fail "G-01" "Required file missing: ${file}" "Path: ${full_path}"
    elif [ ! -s "$full_path" ]; then
        fail "G-01" "Required file is empty: ${file}" "Path: ${full_path}"
    else
        pass "G-01" "File exists and is non-empty: ${file}"
    fi
done

# Check optional files
for file in "${OPTIONAL_FILES[@]}"; do
    full_path="${PROJECT_ROOT}/${file}"
    if [ ! -e "$full_path" ]; then
        warn "G-01" "Optional file/directory missing: ${file} (not a build failure)"
    fi
done

echo ""

# ============================================================
# Quality Gate G-02: SKILL.md is under 200 lines
# ============================================================

echo -e "${BLUE}--- Quality Gate G-02: SKILL.md Line Count ---${NC}"

SKILL_FILE="${PROJECT_ROOT}/SKILL.md"
if [ -f "$SKILL_FILE" ]; then
    LINE_COUNT=$(wc -l < "$SKILL_FILE")
    if [ "$LINE_COUNT" -le 200 ]; then
        pass "G-02" "SKILL.md line count: ${LINE_COUNT} (limit: 200)"
    else
        fail "G-02" "SKILL.md exceeds 200 lines" "Current: ${LINE_COUNT} lines, limit: 200 lines. Please reduce content or split into quick-reference format."
    fi
else
    fail "G-02" "SKILL.md not found (also caught by G-01)"
fi

echo ""

# ============================================================
# Quality Gate G-03: No emoji characters in any file
# ============================================================

echo -e "${BLUE}--- Quality Gate G-03: No Emoji Characters ---${NC}"

# Emoji Unicode ranges to check:
#   U+1F600-U+1F64F  (Emoticons)
#   U+1F300-U+1F5FF  (Miscellaneous Symbols and Pictographs)
#   U+1F680-U+1F6FF  (Transport and Map Symbols)
#   U+1F900-U+1F9FF  (Supplemental Symbols and Pictographs)
#   U+2600-U+26FF    (Miscellaneous Symbols)
#   U+2700-U+27BF    (Dingbats)
#   U+FE00-U+FEFF    (Variation Selectors / Zero Width No-Break Space)
#   U+200D            (Zero Width Joiner - used in emoji sequences)
#   U+20E3            (Combining Enclosing Keycap)
#   U+FE0F            (Variation Selector-16)

EMOJI_FOUND=0
while IFS= read -r file; do
    # Use grep with Perl-compatible regex to find emoji characters
    matches=$(grep -Pn '[\x{1F600}-\x{1F64F}\x{1F300}-\x{1F5FF}\x{1F680}-\x{1F6FF}\x{1F900}-\x{1F9FF}\x{2600}-\x{26FF}\x{2700}-\x{27BF}\x{FE00}-\x{FEFF}\x{200D}\x{20E3}\x{FE0F}]' "$file" 2>/dev/null || true)
    if [ -n "$matches" ]; then
        fail "G-03" "Emoji characters found in: ${file}"
        # Show first few matches (limit to 3 lines)
        detail=$(echo "$matches" | head -3)
        fail "G-03" "" "Lines with emoji: $(echo "$detail" | tr '\n' '| ')"
        EMOJI_FOUND=1
    fi
done < <(find "$PROJECT_ROOT" -type f \( -name "*.md" -o -name "*.sh" -o -name "*.txt" -o -name "*.py" -o -name "*.json" -o -name "*.yaml" -o -name "*.yml" -o -name "*.toml" -o -name "*.cfg" -o -name "*.ini" -o -name "LICENSE" -o -name "*.css" -o -name "*.html" -o -name "*.js" \) -not -path "*/node_modules/*" -not -path "*/.git/*" -print0 | xargs -0 -I{} echo "{}")

if [ "$EMOJI_FOUND" -eq 0 ]; then
    pass "G-03" "No emoji characters detected in any project file"
fi

echo ""

# ============================================================
# Quality Gate G-04: All files are in English (basic heuristic)
# ============================================================

echo -e "${BLUE}--- Quality Gate G-04: English Language Check ---${NC}"

# Heuristic: Check for common non-English words/phrases that would indicate
# a file is not in English. We allow parenthetical references to proper nouns
# (e.g., Ministry of Education) and curriculum terminology as per C-02 exception.
# We check markdown and shell files primarily.

NON_ENGLISH_FOUND=0
while IFS= read -r file; do
    # Skip binary files and files already known to contain non-English glossary terms
    case "$file" in
        */node_modules/*|*/.git/*) continue ;;
    esac

    # Check for common non-English sentence patterns (not individual words which may be proper nouns)
    # We look for paragraphs that are clearly in another language
    # This is a basic heuristic - not exhaustive
    if grep -qiP '(?<!\w)(der|die|das|ein|eine|und|ist|auf|mit|den|dem|des|nicht|schon|aber|werden|durch|für|aus|bei|nach|von|zu|hat|war|hatte|wird|kann|sich|als|hatte|sein|werden|können|müssen|sollen|mögen|wollen)\s+(ist|hat|wird|kann|sich|hatte|war|sein|werden|können|müssen|sollen|mögen|wollen)\b' "$file" 2>/dev/null; then
        # Found potential German text - but verify it's not just a proper noun context
        warn "G-04" "Possible non-English content detected in: ${file}"
        NON_ENGLISH_FOUND=1
    fi
done < <(find "$PROJECT_ROOT" -type f \( -name "*.md" -o -name "*.sh" \) -not -path "*/node_modules/*" -not -path "*/.git/*" -print0 | xargs -0 -I{} echo "{}")

if [ "$NON_ENGLISH_FOUND" -eq 0 ]; then
    pass "G-04" "No obvious non-English content detected (basic heuristic)"
else
    warn "G-04" "Some files may contain non-English content. Please review manually."
fi

echo ""

# ============================================================
# Quality Gate G-05: No code templates outside references/method-patterns.md
# ============================================================

echo -e "${BLUE}--- Quality Gate G-05: Code Template Isolation ---${NC}"

# Code templates should only exist in references/method-patterns.md
# We look for common template markers and structured pseudocode blocks
# in files other than method-patterns.md

TEMPLATE_VIOLATIONS=0
while IFS= read -r file; do
    # Skip the allowed file
    case "$file" in
        *method-patterns.md) continue ;;
        *validate-structure.sh) continue ;;  # This script itself contains patterns
    esac

    # Check for template-like content: structured pseudocode blocks, Template X-Y markers
    if grep -qP 'Template\s+[A-Z]-\d+' "$file" 2>/dev/null; then
        fail "G-05" "Code template marker found outside method-patterns.md: ${file}"
        TEMPLATE_VIOLATIONS=$((TEMPLATE_VIOLATIONS + 1))
    fi

    # Check for structured template sections that look like instructional templates
    if grep -qP '^\*\*Template\s' "$file" 2>/dev/null; then
        fail "G-05" "Structured template pattern found outside method-patterns.md: ${file}"
        TEMPLATE_VIOLATIONS=$((TEMPLATE_VIOLATIONS + 1))
    fi

    # Check for Template A-X, Template B-X, Template C-X, Template D-X patterns
    if grep -qP 'Template\s+[A-D]-\d+' "$file" 2>/dev/null; then
        fail "G-05" "Instructional strategy template reference found outside method-patterns.md: ${file}"
        TEMPLATE_VIOLATIONS=$((TEMPLATE_VIOLATIONS + 1))
    fi

done < <(find "$PROJECT_ROOT" -type f \( -name "*.md" -o -name "*.sh" -o -name "*.txt" \) -not -path "*/node_modules/*" -not -path "*/.git/*" -print0 | xargs -0 -I{} echo "{}")

if [ "$TEMPLATE_VIOLATIONS" -eq 0 ]; then
    pass "G-05" "No code templates found outside references/method-patterns.md"
fi

echo ""

# ============================================================
# Quality Gate G-06: prompts/ files contain no agent-autoinvoke syntax
# ============================================================

echo -e "${BLUE}--- Quality Gate G-06: No agent-autoinvoke in prompts/ ---${NC}"

AUTOINVOKE_VIOLATIONS=0
PROMPTS_DIR="${PROJECT_ROOT}/prompts"

if [ -d "$PROMPTS_DIR" ]; then
    while IFS= read -r file; do
        # Check for agent-autoinvoke markers
        if grep -qP 'agent-autoinvoke' "$file" 2>/dev/null; then
            fail "G-06" "agent-autoinvoke marker found in: ${file}"
            AUTOINVOKE_VIOLATIONS=$((AUTOINVOKE_VIOLATIONS + 1))
        fi

        # Check for system prompt syntax that should not be in user-facing prompts
        if grep -qP '^\s*<system>' "$file" 2>/dev/null; then
            fail "G-06" "System prompt syntax (<system>) found in user-facing file: ${file}"
            AUTOINVOKE_VIOLATIONS=$((AUTOINVOKE_VIOLATIONS + 1))
        fi

        # Check for other auto-invoke markers
        if grep -qP '(auto_invoke|autoinvoke|__auto|_AUTO_|SKILL_AUTO)' "$file" 2>/dev/null; then
            fail "G-06" "Auto-invoke marker found in: ${file}"
            AUTOINVOKE_VIOLATIONS=$((AUTOINVOKE_VIOLATIONS + 1))
        fi

    done < <(find "$PROMPTS_DIR" -type f -name "*.md" -print0 | xargs -0 -I{} echo "{}")
else
    warn "G-06" "prompts/ directory not found"
fi

if [ "$AUTOINVOKE_VIOLATIONS" -eq 0 ]; then
    pass "G-06" "No agent-autoinvoke syntax found in prompts/ files"
fi

echo ""

# ============================================================
# Quality Gate G-07: LICENSE contains GPLv3 canonical text
# ============================================================

echo -e "${BLUE}--- Quality Gate G-07: LICENSE Contains GPLv3 Text ---${NC}"

LICENSE_FILE="${PROJECT_ROOT}/LICENSE"
if [ -f "$LICENSE_FILE" ]; then
    GPLv3_CHECKS=(
        "GNU GENERAL PUBLIC LICENSE"
        "Version 3"
        "Copyright (C)"
        "This program is free software"
        "General Public License"
        "no warranty"
        "Free Software Foundation"
    )

    LICENSE_PASSED=0
    LICENSE_TOTAL=${#GPLv3_CHECKS[@]}

    for check in "${GPLv3_CHECKS[@]}"; do
        if grep -q "$check" "$LICENSE_FILE" 2>/dev/null; then
            LICENSE_PASSED=$((LICENSE_PASSED + 1))
        else
            fail "G-07" "LICENSE file missing expected text: '${check}'"
        fi
    done

    if [ "$LICENSE_PASSED" -eq "$LICENSE_TOTAL" ]; then
        pass "G-07" "LICENSE contains all required GPLv3 canonical text elements (${LICENSE_PASSED}/${LICENSE_TOTAL} checks passed)"
    else
        fail "G-07" "LICENSE file incomplete: ${LICENSE_PASSED}/${LICENSE_TOTAL} GPLv3 elements found"
    fi
else
    fail "G-07" "LICENSE file not found (also caught by G-01)"
fi

echo ""

# ============================================================
# Quality Gate G-08: All five capability tiers defined in SKILL.md
# ============================================================

echo -e "${BLUE}--- Quality Gate G-08: Five Capability Tiers in SKILL.md ---${NC}"

SKILL_FILE="${PROJECT_ROOT}/SKILL.md"
if [ -f "$SKILL_FILE" ]; then
    TIER_CHECKS=(
        "Tier 0"
        "Tier 1"
        "Tier 2"
        "Tier 3"
        "Tier 4"
    )

    TIER_PASSED=0
    TIER_TOTAL=${#TIER_CHECKS[@]}

    for tier in "${TIER_CHECKS[@]}"; do
        if grep -q "$tier" "$SKILL_FILE" 2>/dev/null; then
            TIER_PASSED=$((TIER_PASSED + 1))
        else
            fail "G-08" "Capability tier not found in SKILL.md: ${tier}"
        fi
    done

    if [ "$TIER_PASSED" -eq "$TIER_TOTAL" ]; then
        pass "G-08" "All five capability tiers defined in SKILL.md (${TIER_PASSED}/${TIER_TOTAL} tiers found)"
    else
        fail "G-08" "SKILL.md missing capability tiers: ${TIER_PASSED}/${TIER_TOTAL} found"
    fi
else
    fail "G-08" "SKILL.md not found (also caught by G-01)"
fi

echo ""

# ============================================================
# Quality Gate G-09: All five workflow phases defined in SKILL.md
# ============================================================

echo -e "${BLUE}--- Quality Gate G-09: Five Workflow Phases in SKILL.md ---${NC}"

SKILL_FILE="${PROJECT_ROOT}/SKILL.md"
if [ -f "$SKILL_FILE" ]; then
    PHASE_CHECKS=(
        "Diagnose"
        "Select"
        "Deliver"
        "Assess"
        "Remediate"
    )

    PHASE_PASSED=0
    PHASE_TOTAL=${#PHASE_CHECKS[@]}

    for phase in "${PHASE_CHECKS[@]}"; do
        if grep -qi "$phase" "$SKILL_FILE" 2>/dev/null; then
            PHASE_PASSED=$((PHASE_PASSED + 1))
        else
            fail "G-09" "Workflow phase not found in SKILL.md: ${phase}"
        fi
    done

    if [ "$PHASE_PASSED" -eq "$PHASE_TOTAL" ]; then
        pass "G-09" "All five workflow phases defined in SKILL.md (${PHASE_PASSED}/${PHASE_TOTAL} phases found)"
    else
        fail "G-09" "SKILL.md missing workflow phases: ${PHASE_PASSED}/${PHASE_TOTAL} found"
    fi
else
    fail "G-09" "SKILL.md not found (also caught by G-01)"
fi

echo ""

# ============================================================
# Quality Gate G-10: Knowledge base files exist with skeleton content
# ============================================================

echo -e "${BLUE}--- Quality Gate G-10: Knowledge Base Skeleton ---${NC}"

# Check references/knowledge-base.md exists and contains syllabus-based skeleton
KB_FILE="${PROJECT_ROOT}/references/knowledge-base.md"
if [ -f "$KB_FILE" ]; then
    pass "G-10" "references/knowledge-base.md exists"

    # Check for syllabus-based structure markers
    KB_SKELETON_CHECKS=(
        "Syllabus"
        "syllabus"
    )

    KB_HAS_CONTENT=0
    for check in "${KB_SKELETON_CHECKS[@]}"; do
        if grep -q "$check" "$KB_FILE" 2>/dev/null; then
            KB_HAS_CONTENT=1
            break
        fi
    done

    if [ "$KB_HAS_CONTENT" -eq 1 ]; then
        pass "G-10" "knowledge-base.md contains syllabus-based structure"
    else
        warn "G-10" "knowledge-base.md exists but may not contain syllabus-based skeleton (Phase 3 may populate later)"
    fi
else
    fail "G-10" "references/knowledge-base.md not found"
fi

# Check references/syllabus-registry.md exists
SR_FILE="${PROJECT_ROOT}/references/syllabus-registry.md"
if [ -f "$SR_FILE" ]; then
    pass "G-10" "references/syllabus-registry.md exists"
else
    fail "G-10" "references/syllabus-registry.md not found"
fi

echo ""

# ============================================================
# Additional Structural Checks
# ============================================================

echo -e "${BLUE}--- Additional Structural Checks ---${NC}"

# Check file size sanity (warn if any markdown file is unusually large)
LARGE_FILES=0
while IFS= read -r file; do
    # Skip binary files
    case "$file" in
        *.png|*.jpg|*.jpeg|*.gif|*.ico|*.pdf) continue ;;
    esac
    # Check file size in bytes
    file_size=$(wc -c < "$file" 2>/dev/null || echo 0)
    if [ "$file_size" -gt 1048576 ]; then  # 1MB threshold
        warn "SIZE" "Unusually large file: ${file} (${file_size} bytes)"
        LARGE_FILES=$((LARGE_FILES + 1))
    fi
done < <(find "$PROJECT_ROOT" -type f -name "*.md" -not -path "*/node_modules/*" -not -path "*/.git/*" -print0 | xargs -0 -I{} echo "{}")

if [ "$LARGE_FILES" -eq 0 ]; then
    pass "SIZE" "No unusually large files detected"
fi

# Check that validate-structure.sh is executable
VALIDATE_SCRIPT="${PROJECT_ROOT}/scripts/validate-structure.sh"
if [ -f "$VALIDATE_SCRIPT" ]; then
    if [ -x "$VALIDATE_SCRIPT" ]; then
        pass "EXEC" "validate-structure.sh is executable"
    else
        warn "EXEC" "validate-structure.sh is not executable. Run: chmod +x scripts/validate-structure.sh"
    fi
fi

# Check knowledge-base-update.sh exists
KB_UPDATE_SCRIPT="${PROJECT_ROOT}/scripts/knowledge-base-update.sh"
if [ -f "$KB_UPDATE_SCRIPT" ]; then
    pass "EXEC" "knowledge-base-update.sh exists"
else
    warn "EXEC" "knowledge-base-update.sh not found (referenced in file tree)"
fi

echo ""

# ============================================================
# Final Summary
# ============================================================

print_summary

# Exit with appropriate code
if [ "${CHECKS_FAILED}" -gt 0 ]; then
    exit 1
else
    exit 0
fi
