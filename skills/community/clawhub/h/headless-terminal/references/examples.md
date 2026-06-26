# Examples

## Quick decision rules

Use `ht` when the terminal behaves like a screen, not a stream. Avoid hammer/nail overuse: installing `ht` does not make it the default answer for ordinary shell work.

Install the expected CLI from Montana Flynn's headless-terminal project:

```bash
brew install montanaflynn/tap/ht
```

If trust posture matters, name the repo/owner explicitly and prefer the tap or official release artifacts over random packages or pasted scripts.

Known false friends:
- Homebrew core `ht` is HTE, an executable viewer/editor/analyzer.
- npm `headless-terminal` is an old library package and may not install an `ht` command.

Good fits:
- `vim`, `nvim`, `emacs`
- `top`, `htop`, `watch`
- `git add -p`
- SSH sessions that lead into a TUI
- auth or installer flows that redraw the terminal
- REPLs where prompt timing matters

Poor fits:
- `uptime`, `ls`, `cat`, `grep`, `git status`
- one-shot commands with plain line output
- commands where `exec` with `pty=true` is sufficient
- long-lived human workspaces better handled in tmux

## Example: read a file in vim

```bash
ht run --name notes vim /tmp/notes.md
ht view notes
ht send notes ":q<CR>" --wait-exit
ht remove notes
```

## Example: remote `top` over SSH

```bash
ht run --name remote ssh user@host.example
ht send remote "top<CR>" --wait-idle 500ms --view
ht send remote "q" --wait-idle 200ms
ht send remote "exit<CR>" --wait-exit
ht remove remote
```

## Example: inspect patch mode safely

```bash
ht run --name addp git add -p
ht view addp
```

Then send one response at a time:

```bash
ht send addp "y" --wait-idle 200ms --view
```

or:

```bash
ht send addp "n" --wait-idle 200ms --view
```

## Example: choose a better wait

Prefer:
- `--wait-text "READY"` when a stable marker exists
- `--wait-idle 200ms` after redraw-heavy keys
- `--wait-exit` when closing the program

Avoid piling on arbitrary sleeps unless there is no real signal.

## Example: recover from uncertainty

If the last key had an unclear effect:
1. stop sending input
2. run `ht view <name>`
3. decide from the actual screen state
4. continue with one small keystroke sequence

## Example: avoid stale sessions

Use a name that will not collide with an older run:

```bash
session="vim-notes-$(date +%s)"
ht run --name "$session" vim /tmp/notes.md
ht view "$session"
ht send "$session" ":q<CR>" --wait-exit
ht remove "$session"
```

If cleanup is important, write the command sequence so `ht stop` / `ht remove` still happens after a failure.

## Example: when to abandon `ht`

If the task becomes mostly human-supervised or needs a persistent collaborative shell, switch to tmux.
If the task turns out to be normal command I/O, switch back to `exec` / `process`.