---
name: hallucinated-paths
description: Reply cites file paths, directories, or module locations that do not exist in the current project.
emoji: 🗺️
metadata:
  clawdis:
    os: [macos, linux, windows]
---

# hallucinated-paths

The reply references files or directories that aren't on disk. The agent invented a plausible-sounding location (e.g., `src/utils/helpers.ts`) because similar paths usually exist in projects like this one.

## Symptoms

- A quoted path doesn't exist when you check the filesystem.
- The reply uses a path structure that matches convention but the specific file is absent (e.g., `src/components/Button.tsx` in a project that actually puts components elsewhere).
- Imports reference modules that cannot be resolved.
- "Edit X file at path Y" instructions fail because Y is not there.

## What to do

- Before quoting a path, verify it with a real file-existence check (`ls`, `stat`, a glob search). Do not rely on memory or convention.
- When unsure where something lives, search first: grep for the symbol, glob for the filename, read the repo layout.
- If the answer requires a path that doesn't exist, say so explicitly — don't fabricate. "I couldn't find a file for X" is correct; inventing one is not.
- When proposing to create a new file, state clearly that it is new, and justify why it belongs at that path given the repo's actual conventions.
- After editing, verify the edited file is the one that exists, not a hallucinated sibling.
