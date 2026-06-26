# When Junie setup needs headless-terminal

Short answer: usually it does not.

## Why `ht` is usually unnecessary

Junie already has first-class non-interactive control surfaces for the work that matters during setup:
- installation via installer script, Homebrew, or npm
- authentication via `--auth` or environment variables
- persistent defaults via `~/.junie/config.json` or project `.junie/config.json`
- runtime targeting via flags like `--model`, `--project`, and config discovery flags

That means most install/configure tasks are ordinary shell and file-editing work, not TUI automation.

## Use `ht` only when the UI itself is the task

Reach for `headless-terminal` if:
- the user explicitly wants Junie's interactive welcome screen or in-app account flow driven by the agent
- the step cannot be expressed with documented flags, env vars, or config files
- the program redraws aggressively enough that plain PTY handling becomes unreliable
- you need a stable screen snapshot while debugging the Junie TUI

Examples:
- navigate welcome-screen auth choices
- drive `/account` interactively to add a provider key
- capture the current Junie screen for documentation or debugging

## Do not use `ht` for these

- downloading and running the installer
- checking `junie --version`
- writing `config.json`
- exporting `JUNIE_API_KEY`
- running headless CI prompts

## If `ht` is needed

Switch to the `headless-terminal` skill and use a named session. Prefer deterministic waits such as `--wait-text`, `--wait-idle`, or `--wait-exit` instead of blind sleeps.

Suggested first-run probe:
1. Start Junie from the project root: `cd <project-root> && junie`.
2. If it opens to `What shall we build today?`, the local interactive account flow is already satisfied; it may not ask for sign-in.
3. To verify repo guidance, prompt Junie to read only the project guidance and confirm the relevant rule. Example: `Read only the project Junie guidance/guidelines needed to understand your operating rules for this repo. Confirm whether you are allowed to inspect <path>. Do not inspect <path> itself.`
4. If Junie asks to run a narrow read-only command such as `ls -R .junie` or to open `.junie/AGENTS.md`, allowing once is reasonable when the task is explicitly guidance verification. Do not allow broad repo scans when investigating sensitive denylisted paths.
5. Capture the result and exit the TUI. If Ctrl-C only focuses the prompt or asks for confirmation, send Ctrl-C again or terminate the session.
