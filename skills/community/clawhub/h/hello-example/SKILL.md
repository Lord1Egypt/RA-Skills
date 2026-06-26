---
name: hello-example
description: A minimal example skill demonstrating .clawhubignore — the secret.md file should NOT appear in the published version.
---

# Hello Example

This is a test skill to verify `.clawhubignore` works correctly.

## What this skill does

Nothing useful. It exists to test whether `secret.md` gets excluded on publish.

If you downloaded this skill from ClawHub and can see `secret.md` in the folder — the ignore mechanism is broken.
If `secret.md` is absent — it works correctly.
