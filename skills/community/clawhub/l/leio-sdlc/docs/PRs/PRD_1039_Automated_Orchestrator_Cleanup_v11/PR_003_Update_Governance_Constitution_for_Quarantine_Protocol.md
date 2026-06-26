status: closed

# PR-003: Update Governance Constitution for Quarantine Protocol

## 1. Objective
Amend the organization governance documentation to mandate the new WIP Commit & Rename Quarantine protocol for aborted/crashed pipelines.

## 2. Scope (Functional & Implementation Freedom)
- Update Section 4.2 ("Toxic Branch Anti-Manual Merge") in the governance constitution document to reflect the new lock-aware forensic quarantine `--cleanup` protocol.
- Mandate the WIP commit and rename sequence for aborted/crashed pipelines, ensuring it clearly contrasts with the successful merge deletion mandate in Section 4.1.
*The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
- The governance constitution document is updated accurately according to the PRD requirements.
- The document formatting remains correct and valid markdown.
- Any document validation tests must pass (100% GREEN) before submitting.