# Archived CLI Packaging Note

> **Archived:** This document records an early packaging discussion from before
> the released `mbs` CLI command surface. It is not a command contract, command
> tree, command map, endpoint map, or execution reference.

For current usage, discover the installed public surface with:

```bash
mbs --help
mbs <public-group> --help
mbs <public-group> <public-command> --help
```

Generate only commands shown by public root or nested `--help`. Do not infer
a command from this archived note, an old package name, an endpoint name, or a
legacy script; do not generate hidden compatibility commands.

Use `SKILL.md` and `references/cli-commands.md` for current agent guidance.
