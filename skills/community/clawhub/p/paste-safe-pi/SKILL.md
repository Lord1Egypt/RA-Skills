---
name: paste-safe-pi
description: Emit shell commands that survive being pasted into a remote terminal (e.g. SSH to a Raspberry Pi) that garbles non-ASCII input and mangles multi-line or long pastes. Use short, pure-ASCII, single-line commands and pattern-addressed seds instead of heredocs or multi-line blocks. Use when the user pastes commands by hand into a Pi/remote shell, when the user says input is garbled/mojibake, or when the user cannot copy multi-line blocks.
license: MIT
metadata:
  version: 1.0.0
  author: dicky
---

# Paste-Safe Pi Commands

You are helping a user who **pastes commands by hand** from your chat into a remote
terminal (most often an SSH session to a Raspberry Pi). That terminal has two
failure modes you must design around:

1. **Garbled non-ASCII (mojibake).** The user types or you emit Chinese / wide
   chars / smart quotes → they arrive as garbage bytes on the Pi, corrupting
   strings inside scripts and breaking `sed` patterns. Assume *anything* outside
   plain ASCII is destroyed in transit.
2. **Broken multi-line pastes.** When the user pastes a block of several lines,
   the terminal injects a 2-space indent on continuation lines, or wraps a long
   line by inserting a real newline in the middle. Both silently corrupt the
   command. The user often reports "复制不了" (can't copy multi-line blocks).

Your job: produce commands that are **robust to hand-pasting under these two
failure modes.**

## Hard rules

- **Pure ASCII only.** No Chinese, no smart quotes (`""`/`''`/`—`), no box-drawing
  chars, no emoji — not even inside a string literal or a comment. If you must
  refer to a Chinese label in output, let the *existing script on the Pi* print
  it; do not type Chinese into a command.
- **One logical command per line, short.** Keep each line under ~80 characters
  (hard cap 90). If a command would be longer, split it into two separate
  single-line commands, or fold it with a backslash `\` continuation — but
  prefer splitting, because a wrapped long line can still get a stray newline.
- **No heredocs, no multi-line `for`/`while`/`if` blocks.** A pasted heredoc is
  the single most reliable way to corrupt a file: every body line gains a
  2-space indent. Instead:
  - Edit files with **`sed -i` pattern-addressed replacements** (one per line).
  - Append single lines with `echo 'line' >> file`.
- **Give the user one line at a time, starting from `sed` / the command verb.**
  The user has said they only want to copy "from sed onward" — skip any
  `VAR=...` setup line that precedes it; bake the value into the command.
- **Verify after editing.** Always follow an edit with a read-back
  (`sed -n 'Np' file`) so the user can confirm the line changed as intended.

## Pattern-addressed sed (your main tool)

To change a line you cannot safely retype, address it by line number or by a
short ASCII fragment of its content, then replace a short ASCII fragment:

```
sed -i '64s/CH_OPEN/120/' tune_grasp.py          # by line number
sed -i '/place_and_home/,/^$/s/ch4_grab-20/ch4_grab/' tune_grasp.py   # by range
```

Rules for the pattern:
- Keep the address pattern **short and ASCII**. Prefer a fragment like
  `ch4_grab); _s(2.0)` over the full line.
- Use a **narrow** replacement (`s/old/new/`) so you don't fight quoting.
- If the target contains `/`, pick a different delimiter: `s|old|new|`.

## Long-line folding

Prefer **splitting** over folding. If you must fold, backslash-continue and keep
each segment short:

```
python3 tune_grasp.py 5 \
  --ch4p 160 --ch5p 185
```

Two short single-line commands are still safer:

```
# instead of one 110-char line, run two:
sed -i '126s/ch4-20/ch4p/' tune_grasp.py
sed -i '139s/ch4, ch6p/ch4p, ch6p/' tune_grasp.py
```

## What to send the user

For each change, emit exactly two single-line commands:

```
sed -i '64s/CH_OPEN/120/' tune_grasp.py
sed -n '64p' tune_grasp.py
```

Optionally a third to run the result:

```
python3 tune_grasp.py 5 --ch4p 160
```

Tell the user to paste each line separately and report the read-back output.

## When NOT to use this

If the user is on a local machine with a clean terminal and can run a script
file, or if you can write the file directly with your file-writing tool, do that
instead — this skill is specifically for the hand-paste-into-remote-shell case.

## Checklist before emitting any command

1. Pure ASCII? (no CJK, smart quotes, box chars)
2. Under ~80 chars per line?
3. Single line, no heredoc / multi-line block?
4. Followed by a `sed -n` read-back if it edits a file?
5. Starts at the command verb (no leading `VAR=` setup the user must also copy)?
