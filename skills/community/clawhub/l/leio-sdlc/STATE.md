# STATE.md - leio-sdlc Development State (Kanban)

- **Project**: leio-sdlc (Automated SDLC Orchestrator)
- **Current Version**: 0.9.2
- **Status**: [SDLC Hardening] - Implementing native notifications, fail-fast git hygiene, and deterministic state tracking.
- **Active Branch**: `master`

## 🏆 Recently Completed
- [x] **[ISSUE-1107] Planner Slice Numbering Prompt Hardening**: Modified `config/prompts.json` to strictly enforce the static pass-through of the `--insert-after` argument, fixing the double-nested sub-numbering hallucination bug.
- [x] **[ISSUE-1094] Deploy Path and Broadcast Fix**: Injected absolute path anchors to deploy scripts to prevent SLUG extraction drift. Injected CLI `shlex.join` full command broadcast into Orchestrator and Auditor Slack notifications to ensure immediate execution traceability.
- [x] **[HOTFIX-1094] Config Pollution & Path Chaos Recovery**: Decoupled `RUNTIME_DIR`, `GLOBAL_DIR`, and `WORKDIR` across all engine scripts. Enforced `SDLC_TEST_MODE=true` strict guardrails to prevent `load_or_merge_config` from physically writing `config/sdlc_config.json` into the target source tree, fully eradicating false-positive dirty state pipeline crashes.
- [x] **[PRD-Workspace-Cleanup] Hard Cleanup and Rsync Rule Fix**: Eradicated the infinite nesting `.dist/dist/` bug by propagating `.gitignore` natively into `build_release.sh` using `rsync --exclude-from`. Executed a physical scrub of hundreds of stale `.sdlc_runs/` sandboxes.
- [x] **[ISSUE-1088] Fix Planner Template Adherence and Refine Coder Review Retry Logic**: Successfully implemented Four-Path Resilience (Green/Yellow/Red/Black), Scaffold-then-Fill PR generation, and Hot-Preservation for configuration during deployment.
- [x] **[ISSUE-1071] Automated Test Discovery in Preflight**: Refactored `preflight.sh` to dynamically discover and execute all bash (`scripts/test_*.sh`) and python (`tests/test_*.py`) tests instead of hardcoding them.
- [x] **[ISSUE-1058] Prevent SDLC_TEST_MODE Leakage in Production**: Added context-aware guardrails to `orchestrator.py` to fatally terminate if `SDLC_TEST_MODE=true` is detected in the production runtime, physically blocking hallucinated mock approvals.
- [x] **[ISSUE-1065/1082/1086] Formalize PRD Commit, Template Validation & Auditor Downgrade**: Decoupled auto-commit from orchestrator, implemented `commit_state.py` as the sole explicit state gateway. Downgraded Auditor from independent AgentSkill to internal native script to physically eradicate Reward Hacking bypasses.
- [x] **[ISSUE-1079/1080] Path Resolution Guardrails**: Implemented mandatory `{workdir}/` prefixing for native tools and added Context_Workdir to PRD templates to solve CWD drift.
- [x] **[ISSUE-1085] Fix Planner Path Traversal Defense Deadlock**: Refined path security in `create_pr_contract.py` to allow PRs to be legally sliced into isolated external `job_dir` paths without throwing SecurityError.
- [x] **[ISSUE-1077] Anti-YOLO Guardrail Hardening**: Auditor Playbook 2.0 and structural enhancements to prevent Catch-22 deadlocks in PR slicing and reviewer scopes.
- [x] **[ISSUE-1074] Upgrade Reviewer Playbook**: Integrated IADF-ADE 7 Key Focus Areas and structured findings into the SDLC Reviewer template using a Zero-Blast-Radius approach.
- [x] **[ISSUE-1013] Planner Tech Lead Upgrade**: Upgraded Planner persona to Architect, integrated Target Working Set & TDD Blueprint blackbox testing logic into PR templates, preventing explicit file path hallucination.
- [x] **[ISSUE-1050] PRD-1050 v9: Universal Agent Adaptation**: Natively support Gemini via openclaw CLI, implement agent_driver abstraction, JIT filesystem guardrails, and isolated integration tests (removed network calls from preflight).
- [x] **[ISSUE-1052] SDLC Init and Isolated Runs**: Successfully implemented `.sdlc_runs` artifact isolation, `.gitignore` guardrail fixes, and forensic quarantine tracking (State 5 `git add -f`).
- [x] **[PRD-1041] JIT Prompt De-biasing v6**: Refactored startup and boundary handoff prompts to strictly use non-destructive git operations and full paths for skills. Eliminated LLM attention bias. (v0.9.1)
- [x] **[PRD-1040] Global Pipeline Lock v4**: Implemented static frontmatter parsing, atomic lexicographical lock acquisition, and fail-fast rollback with manifest-based cleanup. (v0.9.0)
- [x] **[ISSUE-1039] PRD-1039 v11: Automated Orchestrator Cleanup Forensic Quarantine**: Implemented crash-proof process group isolation and lock-aware `--cleanup` flag for robust agent teardown. (v0.8.0)
- [x] **[ISSUE-1036] PRD-033: SDLC Observability & Ignition Guardrail**: Implemented mandatory ignition handshake, real-time Slack intermediate pulses (Coder/Reviewer/Merge), and full migration of the review protocol from `[LGTM]` string matching to structured JSON parsing. (v0.7.0)
- [x] **[ISSUE-1026/1033] PRD-032 v2: Strict Execution Boundary**: Enforced `~/.openclaw/skills/` as the only allowed runtime directory. Blocking source code execution from the workspace unless `--enable-exec-from-workspace` is provided. (v0.6.1)
- [x] **[ISSUE-1025] PRD-1025: Reviewer LGTM Bypass**: Refactored orchestrator to parse strict JSON status and physically isolated history diffs in reviewer prompt.
- [x] **[ISSUE-1018] PRD-1018: Enforce Channel Parameter**: Orchestrator now strictly requires --channel and fails-fast on missing notification target. (v0.5.5)
- [x] **[ISSUE-1015] PRD-1015: Hard-Copy Deployment Strategy**: Replaced symlink Blue/Green deploy with atomic directory swapping for AgentSkills. (v0.5.4)
- [x] **[ISSUE-1019] PRD-1019: Clean Workspace Escalation**: Git reset --hard and clean -fd on State 5 Tier 1 recovery. (v0.5.3)
- [x] **[ISSUE-1010] PRD-1010: Orchestrator Self-Explanation**: Enforced strict CLI parameters and implemented the 5 Tool-as-Prompt handoff exit points. (v0.5.2)
- [x] **[ISSUE-1011 & 1012] PRD-1011: Global Lock & Deadlock Fix**: Implemented fcntl global singleton lock and resolved the reviewer guardrail deadlock. (v0.5.1)
- [x] **[ISSUE-067] Migrate SDLC to Gemini ACP**: Coder now uses persistent sandboxed ACP sessions via openclaw agent CLI.
- [x] **[ISSUE-054] State 0: PRD Ingestion & Auto-Slicing**: Orchestrator can now accept a raw PRD and automatically trigger the Planner.
- [x] **[ISSUE-1010] PRD-1010: Orchestrator Self-Explanation**: Enforced strict CLI parameters and implemented the 5 Tool-as-Prompt handoff exit points. (v0.5.2)
- [x] **[ISSUE-1007] PRD-079: SDLC Slack Notifications & Git Hygiene**: Native channel broadcast and Semantic Commit Enforcement. (v0.4.0)
- [x] **[ISSUE-077] CLI Command Mismatch for ACP**: Replaced internal Tool APIs with valid OpenClaw CLI commands (`openclaw agent --session-id`).
- [x] **[ISSUE-074] Information Silo & Dependency Injection**: Orchestrator now serves as Single Source of Truth for Review Report artifact paths.
- [x] **[ISSUE-075] Robust Git State Management**: Implemented `safe_git_checkout` and automatic explicit state commits, eliminating dirty-tree branch crashes.
- [x] **[ISSUE-064] Anti-Reward Hacking Isolation (PRD-064)**: Refactored `orchestrator.py` to use `__file__` absolute paths (`RUNTIME_DIR`), physically preventing the Coder from hijacking the testing framework or Reviewer via relative path execution from the workspace. (v0.2.6)
- [x] **[ISSUE-063] Planner Micro-Slicing & Test Fixes**: Resolves issue tracker/artifact hang bugs. (v0.2.5)
- [x] **[ISSUE-057] PR Directory Isolation by PRD**: Micro-PRs are now physically isolated in `docs/PRs/<PRD_Name>/`. Engine processes isolated queues flawlessly.

## 🚀 Active Milestones & Next in Queue

- **M3: End-to-End Orchestrator Autonomy (State 0 to State 6)** [IN PROGRESS]
  - [ ] **[ISSUE-055] Global Control Tower**: A dashboard/snapshot tool to track the engine's real-time state.

## 📜 History
- **2026-04-09**: ISSUE-1088 Hierarchical Resilience implemented.
- **2026-03-25**: Massive issue board cleanup. Synced stale resolved issues (011, 036, 037, 066, 1003, 1005, 1007, 1010) to closed state.
- **2026-03-22**: Handbook rewritten. Issue System declared as SSOT.
- **2026-03-17**: Engine upgraded to v0.2.6. Reward Hacking & Prompt Injection physically blocked via absolute path isolation.
- **2026-03-17**: Engine stabilized (v0.2.3). Autonomous loop (Coder -> Reviewer -> Merge -> Teardown) successfully executed without human intervention for PRD-057.
- **2026-03-13**: Project promoted to workspace root. SDLC for SDLC initiated (v0.0.1).
