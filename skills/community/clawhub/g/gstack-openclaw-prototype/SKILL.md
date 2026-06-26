---
name: gstack-openclaw-prototype
description: "Build throwaway code to answer a design question fast. Routes between two modes: Logic (interactive terminal app for state machines and data models) or UI (multiple radically different variations switchable via URL param). Use when: user says prototype this, let me play with it, try a few designs, does this state model work, mock up a UI, or wants to validate a design before committing."
---

# Prototype

A prototype is **throwaway code that answers a question**. The question decides the shape.

## Pick a branch

Identify which question is being answered — from the user's prompt, the codebase, or by asking:

- **"Does this logic / state model feel right?"** → **Logic mode.** Build a tiny interactive terminal app that pushes the state machine through cases hard to reason about on paper.
- **"What should this look like?"** → **UI mode.** Generate several radically different UI variations on a single route, switchable via URL search param and a floating bottom bar.

If ambiguous and user is AFK, default to whichever matches the surrounding code (backend module → logic, page/component → UI). State the assumption at the top.

## Rules (both modes)

1. **Throwaway from day one.** Name it so a reader knows it's not production: `prototype-{slug}/`, `_proto_{name}.py`, etc. Place it near the code it's prototyping, not in a separate top-level directory.
2. **One command to run.** Whatever the project uses — `python`, `pnpm`, `bun`, `node`. Zero setup steps.
3. **No persistence.** State lives in memory. If the question involves a database, use a scratch file with a clear "PROTOTYPE — wipe me" name.
4. **Skip the polish.** No tests, no error handling beyond what makes it runnable, no abstractions.
5. **Surface the state.** After every action (logic) or variant switch (UI), print/render the full relevant state so the user sees what changed.
6. **Delete or absorb when done.** Either delete it or fold the validated decision into real code — don't leave it rotting.

## Logic mode

Build a minimal interactive terminal app:
- Present the state machine's current state
- Offer numbered actions the user can take
- Execute the transition and show the new state
- Focus on edge cases and transitions that are hard to reason about statically
- In-memory only — no files, no databases

## UI mode

Generate **3+ radically different** variations, not minor tweaks:
- All variations on a single route, switchable via `?variant=1`, `?variant=2`, etc.
- Add a floating bottom bar with variant labels for quick switching
- Each variation should represent a genuinely different design direction
- Use the project's existing framework/styles — don't introduce new dependencies
- If the project has no frontend framework, use vanilla HTML

## When done

The answer is the only thing worth keeping. Capture it:
- What question was asked
- What the prototype revealed
- Which variant/approach won and why

Save this in the commit message, a brief note next to the prototype, or the conversation. Then delete the prototype code or mark it clearly for cleanup.
