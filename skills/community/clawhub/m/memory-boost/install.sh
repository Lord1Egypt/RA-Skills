#!/bin/bash
# Memory Boost - Auto Install Script
# Automatically configures memory system for AI assistants

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"

echo "🧠 Memory Boost Installer"
echo "========================="
echo ""

# 1. Create MEMORY.md
MEMORY_FILE="$WORKSPACE_DIR/MEMORY.md"
if [ ! -f "$MEMORY_FILE" ]; then
    echo "✓ Creating MEMORY.md..."
    cat > "$MEMORY_FILE" << 'EOF'
# MEMORY.md - AI Assistant Shared Memory

**Created:** 2026-04-01
**Maintained By:** Your Name

---

## 🎯 Active Projects

| Project | Status | Links | Last Updated |
|---------|--------|-------|--------------|
| Project A | 🟡 In Progress | [Link]() | 2026-04-01 |

---

## 👤 User Preferences

| Aspect | Preference |
|--------|------------|
| Communication | Direct, concise |
| Response Style | Structured, tables first |

---

## 📚 Important Decisions

### 2026-04-01
- **Decision:** What was decided
- **Reason:** Why this choice

---

*Last updated: 2026-04-01*
EOF
else
    echo "✓ MEMORY.md already exists, skipping"
fi

# 2. Create memory/ directory
MEMORY_DIR="$WORKSPACE_DIR/memory"
if [ ! -d "$MEMORY_DIR" ]; then
    echo "✓ Creating memory/ directory..."
    mkdir -p "$MEMORY_DIR"

    # Create today's log
    TODAY=$(date +%Y-%m-%d)
    cat > "$MEMORY_DIR/$TODAY.md" << EOF
# $TODAY

## Completed
- [ ]

## In Progress
-

## Notes
-

## Links
-
EOF
else
    echo "✓ memory/ directory already exists, skipping"
fi

# 3. Create MEMORY_INDEX.md (optional quick index)
INDEX_FILE="$WORKSPACE_DIR/MEMORY_INDEX.md"
if [ ! -f "$INDEX_FILE" ]; then
    echo "✓ Creating MEMORY_INDEX.md..."
    cat > "$INDEX_FILE" << 'EOF'
# Memory Index - Quick Reference

**Created:** 2026-04-01
**Maintained By:** Your AI Assistant

---

## 🎯 Active Projects

| Project | Status | Links |
|---------|--------|-------|
| Project A | ✅ Completed | [Repo]() |

---

## 📚 Recent Decisions

### 2026-04-01
- Brief decision summary

---

## 👤 Quick Preferences

- Style: Direct, concise
- Focus: Web dev, AI skills

---

*Last updated: 2026-04-01*
EOF
else
    echo "✓ MEMORY_INDEX.md already exists, skipping"
fi

echo ""
echo "========================="
echo "✅ Memory Boost Installed!"
echo ""
echo "Created:"
echo "  - MEMORY.md (long-term memory)"
echo "  - MEMORY_INDEX.md (quick reference)"
echo "  - memory/$TODAY.md (today's log)"
echo ""
echo "AI assistants will now automatically read/write these files!"
