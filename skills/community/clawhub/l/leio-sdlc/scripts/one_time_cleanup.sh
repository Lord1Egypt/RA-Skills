#!/bin/bash
set -e

echo "Starting one-time workspace cleanup..."

# Ensure guardrails: explicitly preserve core files by not including them in deletion
# No wildcards are used to ensure safety.
CORE_FILES=("README.md" "STATE.md" "SKILL.md" "ARCHITECTURE.md")

# 1. Tracked Ghost Directories
echo "Removing tracked ghost directories..."
git rm -rf --ignore-unmatch AMS/ projects/ || true

# 2. Untracked Ghost Directories
echo "Removing untracked ghost directories..."
rm -rf root/ || true

# 3. PR Fragments
echo "Removing PR fragments..."
PR_FRAGMENTS=(
    "content_pr1.md" "content_pr2.md" "final_pr_contracts.md" "pr_001.md" "pr001_tmp.md" 
    "pr_002.md" "pr002_tmp.md" "pr1_draft.md" "pr1_temp.md" "pr2_draft.md" "pr2_temp.md" 
    "pr3_temp.md" "pr4.md" "pr4_temp.md" "tmp_pr1_final.md" "tmp_pr3.md" "tmp_pr4.md"
)
for f in "${PR_FRAGMENTS[@]}"; do
    git rm -rf --ignore-unmatch "$f" || true
    rm -f "$f"
done

# 4. Legacy Logs/Reports
echo "Removing legacy logs and reports..."
LEGACY_LOGS=(
    "Architectural_Audit_Report_v5.md" "independent_audit_report.md" "native_audit_report.md" 
    "polyrepo_audit_report.md" "polyrepo_v4_audit_report.md" "polyrepo_v5_audit_report.md" 
    "polyrepo_v6_audit_report.md" "polyrepo_v7_audit_report.md" "arbitration_report.txt" 
    "audit_prompt.txt" "audit_verdict.json" "dummy_chat_context_074.txt" "polyrepo_plan.md"
)
for f in "${LEGACY_LOGS[@]}"; do
    git rm -rf --ignore-unmatch "$f" || true
    rm -f "$f"
done

# 5. One-off Scripts
echo "Removing one-off debug scripts..."
ONE_OFFS=(
    "debug_orchestrator.py" "hello.py" "patch_guardrails.sh" "patch_test_branch_isolation.sh" 
    "rollback.sh" "run_independent_audit.sh" "server.py" "spawn_native_auditor.sh"
)
for f in "${ONE_OFFS[@]}"; do
    git rm -rf --ignore-unmatch "$f" || true
    rm -f "$f"
done

echo "Cleanup complete. Verifying core files..."
for f in "${CORE_FILES[@]}"; do
    if [ ! -f "$f" ]; then
        echo "ERROR: Guardrail failed. $f is missing!"
        exit 1
    fi
done

echo "All specified garbage files removed and core architecture files preserved."
