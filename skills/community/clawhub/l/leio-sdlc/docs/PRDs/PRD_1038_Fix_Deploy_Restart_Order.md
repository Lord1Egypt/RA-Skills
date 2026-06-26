# PRD: Fix deploy.sh Gateway Restart Order (ISSUE-1038)

## Context
Currently, the `deploy.sh` script executes `openclaw gateway restart` at Step 4. Because the deployment script itself is spawned as a child process of the gateway daemon, restarting the gateway immediately sends a `SIGTERM` signal to the `deploy.sh` script, instantly killing it mid-execution. 

As a result, any trailing steps located after the restart command (e.g., Step 5 Cleanup, Step 6 GitHub Auto-Sync, and Step 7 Git Pre-commit Hook installation) are never executed, breaking critical pipeline infrastructure.

## Requirements
- Identify the `openclaw gateway restart` execution block within `deploy.sh` and `TEMPLATES/AgentSkill_Archetype/deploy.sh`.
- Move this entire block (including its `echo` and condition checks) to the absolute bottom of the `perform_hard_copy_deployment` function, making it the final command executed by the script.
- Ensure that Steps 5, 6, and 7 are shifted above the restart command.

## Framework Modifications
- `deploy.sh`
- `TEMPLATES/AgentSkill_Archetype/deploy.sh`

## Architecture
This is a purely sequential script modification to prevent process suicide before cleanup and initialization tasks are completed. By fixing the template, we ensure all future skills generated from this framework inherit the corrected logic.

## Acceptance Criteria
- [ ] The `openclaw gateway restart` block is verified to be the final action within `deploy.sh` and the Archetype template.
- [ ] All cleanup, sync, and hook installation logic precedes the restart.