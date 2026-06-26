#!/bin/bash
for dir in PRD_032_Create_PM_AgentSkill \
PRD_054_State_0_Ingestion \
PRD_060_Hotfix_Merge_and_Regex \
PRD_065_Runtime_Path_Decoupling \
PRD_070_Planner_Template_Standardization \
PRD_072_Strict_Status_Parsing \
PRD_074_Dependency_Injection_Review_Report \
PRD_075_Robust_Git_State_Management \
PRD_077_Fix_CLI_Command_Mismatch_For_ACP; do
  if [ -d "docs/PRs/$dir" ]; then
    find "docs/PRs/$dir" -name "*.md" -type f -exec sed -i -E 's/^status: (open|in_progress|in_review)$/status: completed/g' {} +
    echo "Cleaned up $dir"
  fi
done
