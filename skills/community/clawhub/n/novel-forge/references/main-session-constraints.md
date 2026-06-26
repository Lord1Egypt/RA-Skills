# Main Session Constraints

This file defines what the **main session** may and may not do in novel-forge.

## Allowed
- Collect high-level requirements from the user.
- Create or update the project shell and state files.
- Choose execution mode only when the user has not already fixed it.
- Read the model inventory first, then ask the user for a role→model mapping when multi-agent is desired.
- Route work to the designated stage agent(s) with `sessions_spawn` when the environment supports them.
- Treat `project.json.models` as the project’s role assignment state; do not confuse it with the runtime payload used by the spawning layer.
- Verify stage outputs against the request and the current project state.
- Write back accepted state, summaries, and checkpoints.

## Forbidden
- Do **not** author final canon content in the main session.
- Do **not** fill `worldbuilding`, `characters`, `outline`, `style`, or `chapter` content from raw user facts.
- Do **not** invent names, relationships, lore, rules, or prose when a dedicated stage exists.
- Do **not** collapse a stage into the main session just because it is convenient.
- Do **not** treat `agents_list` as the model inventory.
- Do **not** proceed silently if the required stage agent is unavailable.

## Required behavior
- Treat canon generation as delegated work.
- If the user requests a stage that has its own agent, hand it off instead of drafting it yourself.
- If delegation is impossible, stop and report the missing capability.
- If the user explicitly asks for a lightweight shell only, keep the shell minimal and wait for the stage workflow.

## Practical rule
The main session may prepare the board, but it does not play the game.
