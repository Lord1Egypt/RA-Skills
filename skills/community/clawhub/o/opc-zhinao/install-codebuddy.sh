#!/usr/bin/env bash
# ============================================================
# OPC ZhiNao - CodeBuddy / WorkBuddy Install Script (Bash)
# Author: 李屹镒 (WeChat: 科技新潮, Channel: 小李君与AI)
# Usage: bash install-codebuddy.sh [target-project-path] [--skip-backup]
# Desc: Auto-copy AGENTS.md and Skills to target project
# Examples:
#   bash install-codebuddy.sh                            # Install to current directory
#   bash install-codebuddy.sh /path/to/my-app            # Install to specified project
#   bash install-codebuddy.sh /path/to/my-app --skip-backup
# ============================================================

set -euo pipefail

TARGET_DIR="${1:-.}"
SKIP_BACKUP=false

# Parse --skip-backup flag from any argument position
for arg in "$@"; do
    if [[ "$arg" == "--skip-backup" ]]; then
        SKIP_BACKUP=true
    fi
done

# If first arg is a valid path (not a flag), use it as target
if [[ "${1:-}" != "--skip-backup" && -n "${1:-}" ]]; then
    TARGET_DIR="$1"
fi

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
GRAY='\033[0;90m'
NC='\033[0m' # No Color

# ============================================================
# Detect source directory (opc_skills root — dir of this script)
# ============================================================
SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo -e "${CYAN}========================================"
echo -e "  OPC Skills - CodeBuddy/WorkBuddy Install"
echo -e "========================================${NC}"
echo ""

# ============================================================
# Pre-check: verify source directory structure
# ============================================================
AGENTS_SOURCE="$SOURCE_DIR/AGENTS.md"
SKILLS_SOURCE_DIR="$SOURCE_DIR/skills"

if [[ ! -f "$AGENTS_SOURCE" ]]; then
    echo -e "${RED}[ERROR] AGENTS.md not found. Run this script from opc_skills directory.${NC}"
    echo -e "${RED}  Expected: $AGENTS_SOURCE${NC}"
    exit 1
fi

if [[ ! -d "$SKILLS_SOURCE_DIR" ]]; then
    echo -e "${RED}[ERROR] skills/ directory not found. Run this script from opc_skills directory.${NC}"
    echo -e "${RED}  Expected: $SKILLS_SOURCE_DIR${NC}"
    exit 1
fi

# ============================================================
# Resolve target directory
# ============================================================
if [[ ! -d "$TARGET_DIR" ]]; then
    echo -e "${YELLOW}Target directory not found, creating: $TARGET_DIR${NC}"
    mkdir -p "$TARGET_DIR"
fi

TARGET_DIR="$(cd "$TARGET_DIR" 2>/dev/null && pwd || realpath "$TARGET_DIR")"

echo -e "Source:    ${WHITE}$SOURCE_DIR${NC}"
echo -e "Target:    ${WHITE}$TARGET_DIR${NC}"
echo ""

# ============================================================
# [0/6] Pre-check: warn if AGENTS.md already exists
# ============================================================
EXISTING_AGENTS="$TARGET_DIR/AGENTS.md"
EXISTING_REGISTRY="$TARGET_DIR/.codebuddy/skills-registry.json"

if [[ -f "$EXISTING_AGENTS" ]] || [[ -f "$EXISTING_REGISTRY" ]]; then
    echo -e "${YELLOW}[0/6] Existing installation detected${NC}"

    if [[ "$SKIP_BACKUP" == false ]]; then
        BACKUP_DIR="$TARGET_DIR/.codebuddy/skills-backup-$(date +%Y%m%d-%H%M%S)"
        echo -e "${YELLOW}  Backing up to: $BACKUP_DIR${NC}"

        mkdir -p "$BACKUP_DIR"

        # Only backup AGENTS.md if it looks like an OPC file
        if [[ -f "$EXISTING_AGENTS" ]]; then
            if grep -qE 'OPC智脑|opc-skills|OPC Skills' "$EXISTING_AGENTS" 2>/dev/null; then
                cp "$EXISTING_AGENTS" "$BACKUP_DIR/AGENTS.md"
            fi
        fi

        if [[ -f "$EXISTING_REGISTRY" ]]; then
            cp "$EXISTING_REGISTRY" "$BACKUP_DIR/skills-registry.json"
        fi

        # Backup existing skills directory
        EXISTING_SKILLS_DIR="$TARGET_DIR/.codebuddy/skills"
        if [[ -d "$EXISTING_SKILLS_DIR" ]]; then
            cp -r "$EXISTING_SKILLS_DIR" "$BACKUP_DIR/skills"
        fi

        echo -e "${GREEN}  Old installation backed up${NC}"
    else
        echo -e "${YELLOW}  Overwriting existing installation (backup skipped)${NC}"
    fi
fi

# ============================================================
# [1/6] Create .codebuddy/skills directory
# ============================================================
echo -e "${CYAN}[1/6] Creating .codebuddy/skills directory...${NC}"

SKILLS_TARGET_DIR="$TARGET_DIR/.codebuddy/skills"
mkdir -p "$SKILLS_TARGET_DIR"
echo -e "${GREEN}  OK  Directory created${NC}"

# ============================================================
# [2/6] Copy AGENTS.md
# ============================================================
echo -e "${CYAN}[2/6] Copying AGENTS.md...${NC}"

AGENTS_TARGET="$TARGET_DIR/AGENTS.md"
cp "$AGENTS_SOURCE" "$AGENTS_TARGET"
echo -e "${GREEN}  OK  AGENTS.md -> $AGENTS_TARGET${NC}"

# ============================================================
# [3/6] Copy all Skills (only SKILL.md files)
# ============================================================
echo -e "${CYAN}[3/6] Copying Skills...${NC}"

SKILL_COUNT=0
SKILL_SKIPPED=0

for dir in "$SKILLS_SOURCE_DIR"/*/; do
    [[ -d "$dir" ]] || continue
    SKILL_NAME="$(basename "$dir")"
    SKILL_MD="$dir/SKILL.md"

    if [[ ! -f "$SKILL_MD" ]]; then
        echo -e "  ${GRAY}SKIP  $SKILL_NAME (no SKILL.md)${NC}"
        ((SKILL_SKIPPED++)) || true
        continue
    fi

    TARGET_SKILL_DIR="$SKILLS_TARGET_DIR/$SKILL_NAME"
    mkdir -p "$TARGET_SKILL_DIR"
    
    # Only copy SKILL.md (not entire directory)
    cp "$SKILL_MD" "$TARGET_SKILL_DIR/"

    echo -e "  ${GREEN}OK   $SKILL_NAME/SKILL.md${NC}"
    ((SKILL_COUNT++)) || true
done

if [[ $SKILL_COUNT -eq 0 ]]; then
    echo -e "${RED}  [ERROR] No Skills copied. Aborting.${NC}"
    exit 1
fi

echo -e "${GREEN}  Total: $SKILL_COUNT Skills${NC}"
if [[ $SKILL_SKIPPED -gt 0 ]]; then
    echo -e "${GRAY}  Skipped: $SKILL_SKIPPED (missing SKILL.md)${NC}"
fi

# ============================================================
# [4/6] Generate skills-registry.json
# ============================================================
echo -e "${CYAN}[4/6] Generating skills-registry.json...${NC}"

# Build JSON array from installed skill names
REGISTRY_PATH="$TARGET_DIR/.codebuddy/skills-registry.json"
SKILLS_JSON=""

for dir in "$SKILLS_TARGET_DIR"/*/; do
    [[ -d "$dir" ]] || continue
    name="$(basename "$dir")"
    if [[ -n "$SKILLS_JSON" ]]; then
        SKILLS_JSON+=$'\n'
    fi
    SKILLS_JSON+="    \"$name\""
done

# Join with commas
SKILLS_JSON_LINES=""
FIRST=true
while IFS= read -r line; do
    if [[ "$FIRST" == true ]]; then
        FIRST=false
    else
        SKILLS_JSON_LINES+=$'\n'
    fi
    SKILLS_JSON_LINES+="$line"
done <<< "$SKILLS_JSON"

cat > "$REGISTRY_PATH" << EOF
{
  "name": "opc-skills",
  "version": "1.2.0",
  "ide": "codebuddy",
  "skills": [
${SKILLS_JSON_LINES}
  ]
}
EOF

echo -e "${GREEN}  OK  skills-registry.json -> $REGISTRY_PATH${NC}"

# ============================================================
# [5/6] Verify installation (SKILL.md frontmatter)
# ============================================================
echo -e "${CYAN}[5/6] Verifying Skill frontmatter...${NC}"

VERIFY_ERRORS=0

# Verify AGENTS.md
if [[ -f "$TARGET_DIR/AGENTS.md" ]]; then
    echo -e "${GREEN}  OK   AGENTS.md exists${NC}"
else
    echo -e "${RED}  [ERROR] AGENTS.md missing${NC}"
    ((VERIFY_ERRORS++)) || true
fi

# Verify each installed Skill
for dir in "$SKILLS_TARGET_DIR"/*/; do
    [[ -d "$dir" ]] || continue
    SKILL_NAME="$(basename "$dir")"
    SKILL_MD="$dir/SKILL.md"

    if [[ -f "$SKILL_MD" ]]; then
        HAS_NAME=false
        HAS_DESC=false
        if grep -qE '^name:\s*.+' "$SKILL_MD" 2>/dev/null; then
            HAS_NAME=true
        fi
        if grep -qE '^description:\s*.+' "$SKILL_MD" 2>/dev/null; then
            HAS_DESC=true
        fi

        if [[ "$HAS_NAME" == true ]] && [[ "$HAS_DESC" == true ]]; then
            echo -e "${GREEN}  OK   $SKILL_NAME/SKILL.md (frontmatter valid)${NC}"
        else
            MISSING_PARTS=""
            [[ "$HAS_NAME" == false ]] && MISSING_PARTS+="name"
            [[ "$HAS_DESC" == false ]] && MISSING_PARTS+="${MISSING_PARTS:+, }description"
            echo -e "${YELLOW}  WARN $SKILL_NAME/SKILL.md missing frontmatter: $MISSING_PARTS${NC}"
        fi
    else
        echo -e "${RED}  [ERROR] $SKILL_NAME/SKILL.md missing${NC}"
        ((VERIFY_ERRORS++)) || true
    fi
done

# ============================================================
# [6/6] Verify registry integrity
# ============================================================
echo -e "${CYAN}[6/6] Verifying registry integrity...${NC}"

# Get installed skills from directory
INSTALLED_SKILLS=()
for dir in "$SKILLS_TARGET_DIR"/*/; do
    [[ -d "$dir" ]] || continue
    INSTALLED_SKILLS+=("$(basename "$dir")")
done

# Get registry skills from JSON (simple grep approach, no jq required)
REGISTRY_SKILLS=()
if [[ -f "$REGISTRY_PATH" ]]; then
    while IFS= read -r line; do
        # Extract skill name from lines like:    "skill-name"
        if [[ "$line" =~ \"([^\"]+)\" ]]; then
            REGISTRY_SKILLS+=("${BASH_REMATCH[1]}")
        fi
    done < <(sed -n '/"skills"/,/]/p' "$REGISTRY_PATH")
fi

REGISTRY_COUNT=${#REGISTRY_SKILLS[@]}

if [[ $REGISTRY_COUNT -gt 0 ]]; then
    # Check for orphan directories (in filesystem but not registry)
    ORPHANS=()
    for skill in "${INSTALLED_SKILLS[@]}"; do
        FOUND=false
        for reg_skill in "${REGISTRY_SKILLS[@]}"; do
            [[ "$skill" == "$reg_skill" ]] && FOUND=true && break
        done
        [[ "$FOUND" == false ]] && ORPHANS+=("$skill")
    done

    # Check for missing directories (in registry but not filesystem)
    MISSING_DIRS=()
    for reg_skill in "${REGISTRY_SKILLS[@]}"; do
        FOUND=false
        for skill in "${INSTALLED_SKILLS[@]}"; do
            [[ "$skill" == "$reg_skill" ]] && FOUND=true && break
        done
        [[ "$FOUND" == false ]] && MISSING_DIRS+=("$reg_skill")
    done

    if [[ ${#ORPHANS[@]} -eq 0 ]] && [[ ${#MISSING_DIRS[@]} -eq 0 ]]; then
        echo -e "${GREEN}  OK   Registry matches installed Skills ($REGISTRY_COUNT entries)${NC}"
    else
        if [[ ${#ORPHANS[@]} -gt 0 ]]; then
            echo -e "${YELLOW}  WARN Orphan directories (not in registry): ${ORPHANS[*]}${NC}"
        fi
        if [[ ${#MISSING_DIRS[@]} -gt 0 ]]; then
            echo -e "${YELLOW}  WARN Registry entries without directory: ${MISSING_DIRS[*]}${NC}"
        fi
    fi
else
    echo -e "${RED}  [ERROR] skills-registry.json has no skills${NC}"
    ((VERIFY_ERRORS++)) || true
fi

# ============================================================
# Result
# ============================================================
echo ""
if [[ $VERIFY_ERRORS -eq 0 ]]; then
    echo -e "${GREEN}========================================"
    echo -e "  OPC Skills - Install Complete!"
    echo -e "========================================${NC}"
else
    echo -e "${YELLOW}========================================"
    echo -e "  Install complete with $VERIFY_ERRORS error(s)"
    echo -e "========================================${NC}"
fi

echo ""
echo -e "${CYAN}Installed files:${NC}"
echo "  $TARGET_DIR/"
echo "  +-- AGENTS.md"
echo "  +-- .codebuddy/"
echo "      +-- skills-registry.json"
echo "      +-- skills/"
for dir in "$SKILLS_TARGET_DIR"/*/; do
    [[ -d "$dir" ]] || continue
    SKILL_NAME="$(basename "$dir")"
    FILE_COUNT=$(find "$dir" -maxdepth 1 -type f | wc -l | tr -d ' ')
    echo "          +-- $SKILL_NAME/ ($FILE_COUNT files)"
done

echo ""
echo -e "${CYAN}Next steps:${NC}"
echo "  1. Open project in CodeBuddy IDE: $TARGET_DIR"
echo "  2. IDE will auto-load all Skills from .codebuddy/skills/"
echo "  3. Start by describing your startup idea"
echo ""

# ============================================================
# Cleanup prompt (interactive mode only, safe check)
# ============================================================
if [[ -t 0 ]]; then
    echo -e "${CYAN}========================================"
    echo -e "  Cleanup Source Files"
    echo -e "========================================${NC}"
    echo ""

    # Only offer cleanup if source != target AND source looks like opc_skills
    if [[ "$SOURCE_DIR" != "$TARGET_DIR" ]]; then
        if [[ -f "$SOURCE_DIR/AGENTS.md" ]] && [[ -d "$SOURCE_DIR/skills" ]]; then
            SOURCE_NAME="$(basename "$SOURCE_DIR")"
            echo -e "${YELLOW}Source: $SOURCE_DIR${NC}"
            echo -e "${YELLOW}Delete source directory to keep project clean?${NC}"
            echo -e "${RED}WARNING: This will delete ALL files in '$SOURCE_NAME'${NC}"
            read -r -p "Type DELETE to confirm, any other key to keep: " CONFIRM

            if [[ "$CONFIRM" == "DELETE" ]]; then
                rm -rf "$SOURCE_DIR"
                echo -e "${GREEN}OK  $SOURCE_NAME directory removed${NC}"
            else
                echo -e "${CYAN}Keeping $SOURCE_NAME directory${NC}"
            fi
        else
            echo -e "${YELLOW}Source does not appear to be opc_skills, skipping cleanup${NC}"
        fi
    else
        echo -e "${YELLOW}Running inside opc_skills directory, skipping cleanup${NC}"
    fi
fi

echo ""
