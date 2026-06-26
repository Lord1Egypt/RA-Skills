#!/usr/bin/env bash
# git-guardian.sh — Track agent work in git with diff-first workflow
set -euo pipefail

CMD="${1:-help}"
shift || true

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

case "$CMD" in
  start)
    DESC="${*:-agent-work}"
    BRANCH="agent/$(echo "$DESC" | tr ' ' '-' | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]//g')"
    BRANCH="${BRANCH:0:60}-$(date +%m%d)"
    
    # Ensure we're in a git repo
    if ! git rev-parse --is-inside-work-tree &>/dev/null; then
      echo -e "${RED}Error: Not in a git repository${NC}"
      exit 1
    fi
    
    # Stash any uncommitted changes
    if ! git diff --quiet || ! git diff --cached --quiet; then
      echo -e "${YELLOW}Stashing existing changes...${NC}"
      git stash push -m "git-guardian: stash before branch $BRANCH"
    fi
    
    # Create and switch to branch
    git checkout -b "$BRANCH" 2>/dev/null || git checkout "$BRANCH"
    
    # Pop stash if we stashed
    if git stash list | head -1 | grep -q "git-guardian: stash before branch"; then
      git stash pop
    fi
    
    echo -e "${GREEN}✅ Started tracked work on branch: ${BLUE}$BRANCH${NC}"
    echo -e "   Make your changes, then run: ${YELLOW}git-guardian.sh diff${NC}"
    ;;
    
  diff)
    echo -e "${BLUE}=== Unstaged Changes ===${NC}"
    if git diff --quiet 2>/dev/null; then
      echo "(none)"
    else
      git diff --stat
      echo ""
      git diff
    fi
    
    echo ""
    echo -e "${BLUE}=== Staged Changes ===${NC}"
    if git diff --cached --quiet 2>/dev/null; then
      echo "(none)"
    else
      git diff --cached --stat
      echo ""
      git diff --cached
    fi
    
    echo ""
    echo -e "${BLUE}=== Untracked Files ===${NC}"
    UNTRACKED=$(git ls-files --others --exclude-standard)
    if [ -z "$UNTRACKED" ]; then
      echo "(none)"
    else
      echo "$UNTRACKED"
      echo ""
      # Show content of new files
      while IFS= read -r file; do
        echo -e "${GREEN}+++ $file (new file)${NC}"
        head -50 "$file"
        LINES=$(wc -l < "$file")
        if [ "$LINES" -gt 50 ]; then
          echo -e "${YELLOW}... ($LINES total lines, showing first 50)${NC}"
        fi
        echo ""
      done <<< "$UNTRACKED"
    fi
    
    # Summary
    echo -e "${BLUE}=== Summary ===${NC}"
    MODIFIED=$(git diff --name-only | wc -l | tr -d ' ')
    STAGED=$(git diff --cached --name-only | wc -l | tr -d ' ')
    NEW=$(echo "$UNTRACKED" | grep -c . || true)
    echo "Modified: $MODIFIED | Staged: $STAGED | New: $NEW"
    echo -e "\nTo approve: ${YELLOW}git-guardian.sh commit \"description\"${NC}"
    ;;
    
  commit)
    MSG="${*:-Agent work}"
    BRANCH=$(git branch --show-current)
    
    # Stage everything
    git add -A
    
    # Show what we're about to commit
    echo -e "${BLUE}Committing on branch: ${GREEN}$BRANCH${NC}"
    git diff --cached --stat
    echo ""
    
    # Commit
    git commit -m "$MSG"
    
    HASH=$(git rev-parse --short HEAD)
    echo -e "\n${GREEN}✅ Committed: ${BLUE}$HASH${NC} — $MSG"
    ;;
    
  finish)
    BRANCH=$(git branch --show-current)
    
    if [ "$BRANCH" = "main" ] || [ "$BRANCH" = "master" ]; then
      echo -e "${YELLOW}Already on main branch. Nothing to push.${NC}"
      exit 0
    fi
    
    # Push
    git push origin "$BRANCH" 2>&1
    
    # Get remote URL for PR link
    REMOTE=$(git remote get-url origin 2>/dev/null || echo "")
    
    echo -e "\n${GREEN}✅ Pushed branch: ${BLUE}$BRANCH${NC}"
    echo -e "\n${BLUE}=== Commit Log (branch only) ===${NC}"
    git log main.."$BRANCH" --oneline 2>/dev/null || git log --oneline -5
    
    if [[ "$REMOTE" == *github.com* ]]; then
      REPO=$(echo "$REMOTE" | sed 's/.*github.com[:/]\(.*\)\.git/\1/' | sed 's/.*github.com[:/]\(.*\)/\1/')
      echo -e "\n📎 Create PR: https://github.com/$REPO/compare/$BRANCH"
    fi
    ;;
    
  status)
    BRANCH=$(git branch --show-current)
    echo -e "${BLUE}Branch:${NC} $BRANCH"
    echo -e "${BLUE}Status:${NC}"
    git status --short
    echo -e "\n${BLUE}Recent commits:${NC}"
    git log --oneline -5
    ;;
    
  help|*)
    echo "git-guardian — Track agent work in git with diff-first workflow"
    echo ""
    echo "Usage: git-guardian.sh <command> [args]"
    echo ""
    echo "Commands:"
    echo "  start <description>    Create a feature branch for tracked work"
    echo "  diff                   Show all pending changes (staged, unstaged, new)"
    echo "  commit <message>       Stage all changes and commit with message"
    echo "  finish                 Push branch and show review link"
    echo "  status                 Show current branch and status"
    echo "  help                   Show this help"
    ;;
esac
