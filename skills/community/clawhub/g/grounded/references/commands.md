# Commands reference

Condensed CLI surface for agents. Flags not listed here do not exist;
do not invent invocations.

```console
grounded scan [PATH] [--format terminal|json|sarif|html] [--output FILE]
              [--fail-on lie|drift|smell|never]
              [--enable ID,...] [--disable ID,...]
              [--baseline FILE] [--show-baselined]
              [--changed [BASE]] [--cache [FILE]] [--jobs N]
              [--config FILE] [--no-color] [--quiet]
grounded baseline [PATH] [--output FILE]
grounded fix [PATH] [--dry-run]
grounded impact SYMBOL [PATH] [--format terminal|json]
grounded list [PATH]
grounded explain [CHECKER]
grounded init [--force]
grounded init-agent [--claude|--cursor|--aider] [--skill] [--skill-project]
               [--pre-commit] [--force] [--dry-run]
grounded mcp [--root .]
grounded lsp
```

Contracts:

* `scan <file>` checks one file, exit 1 on findings, 0 when clean, 3 when an enabled checker raised (incomplete scan).
* `scan` never writes. Only `fix` (without `--dry-run`) writes, and only
  the lines of unambiguous findings.
* `--changed` reports on-diff findings plus rename fallout: verified
  findings anywhere that name a diff-touched symbol.
* `impact` never writes. `mcp` and `lsp` never write.
* Machine output: `--format json` (scripts), `--format sarif` (code
  scanning). Terminal output is for humans; parse JSON instead.
* `stale-doc-ref` is opt-in: `--enable stale-doc-ref`. Never assume it
  ran; default scans exclude it.
* `init-agent --skill` installs this skill to `~/.claude/skills/grounded`
  (all projects); `--skill-project` installs to `.claude/skills/grounded`
  (this repo only). Bare `init-agent` never writes outside the repo.
