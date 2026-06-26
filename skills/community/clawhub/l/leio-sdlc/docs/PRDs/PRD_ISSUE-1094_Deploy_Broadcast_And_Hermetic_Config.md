---
Affected_Projects: [leio-sdlc]
---

# PRD: ISSUE-1094_Deploy_Path_And_Broadcast

## 1. Context & Problem
This PRD addresses two critical operational stability issues:
1. **Deploy Path Drift**: Deployment scripts (`deploy.sh`, `kit-deploy.sh`) rely on `$PWD` to extract the `SLUG` (skill name). If executed from outside the target project directory, they package the wrong parent folder.
2. **Missing Execution Traceability**: Agents frequently launch `orchestrator.py` or `spawn_auditor.py` using incorrect workspace paths. The Boss needs these scripts to broadcast their full launch command line to Slack as their first message to allow immediate interception.

## 2. Requirements & User Stories
- **Self-Locating Scripts**: `deploy.sh` and `kit-deploy.sh` MUST automatically `cd` to their physical file directory before executing any logic.
- **Auditor & Orchestrator Broadcast**: `spawn_auditor.py` and `orchestrator.py` MUST include their full command line invocation in their initial Slack notifications.

## 3. Architecture & Technical Strategy
1. **Deployment Scripts**:
   - Insert `cd "$(dirname "$0")" || exit 1` at the beginning of `kit-deploy.sh`, `deploy.sh`, and `TEMPLATES/scaffold/profiles/skill/deploy.sh`.
2. **CLI Extraction & Broadcast**:
   - Use `import shlex, sys` and `full_cmd = shlex.join([sys.executable] + sys.argv)` to capture the exact invocation.
   - Update `notification_formatter.py` to accept the `command` key in `kwargs` for `sdlc_start`, `sdlc_resume`, and a new `auditor_start` event type.
   - Inject `notify_channel(..., "auditor_start", {"prd_file": args.prd_file, "command": full_cmd})` into `spawn_auditor.py`.
   - Inject `{"command": full_cmd}` into `notify_channel` calls for `sdlc_start` and `sdlc_resume` in `orchestrator.py`.

## 4. Acceptance Criteria
- **Scenario 1 (Deploy Path)**: Running `/root/path/to/kit-deploy.sh` from `/` successfully extracts the skill slug as `leio-sdlc` instead of `root`.
- **Scenario 2 (Broadcast)**: Running `spawn_auditor.py` or `orchestrator.py` sends a Slack message showing the exact command line used.

## 5. Overall Test Strategy & Quality Goal
- **Unit Test (Formatter)**: Create or update a test for `notification_formatter.py` verifying that `auditor_start` and `sdlc_start` correctly append the command string.

## 6. Framework Modifications
- `kit-deploy.sh`
- `deploy.sh`
- `TEMPLATES/scaffold/profiles/skill/deploy.sh`
- `scripts/spawn_auditor.py`
- `scripts/orchestrator.py`
- `scripts/notification_formatter.py`

## 7. Hardcoded Content
### Exact Text Replacements:

**In `scripts/notification_formatter.py` (Append this logic):**
```python
    elif event_type == "sdlc_start":
        cmd = kwargs.get("command", "unknown")
        return f"🚀 1. [{prd_match}] SDLC 启动\n💻 Command: `{cmd}`"
    elif event_type == "sdlc_resume":
        cmd = kwargs.get("command", "unknown")
        return f"🚀 1. [{prd_match}] SDLC 恢复执行\n💻 Command: `{cmd}`"
    elif event_type == "auditor_start":
        cmd = kwargs.get("command", "unknown")
        return f"🚀 [Auditor] 启动审批流程\n💻 Command: `{cmd}`"
```
