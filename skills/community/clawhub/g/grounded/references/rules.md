# Rules reference

Condensed checker semantics for agents. Full prose lives in the
[rules documentation](https://grounded.readthedocs.io/en/latest/rules/).

| ID | Severity | Reports | Never reports |
|---|---|---|---|
| `stale-symbol-ref` | lie | comment names a call resolving nowhere | builtins, keywords, imports, params, locals, Sphinx/JSDoc fields |
| `stale-import` | lie | resolvable import to a missing module or name | stdlib, deps, guarded imports, star imports, dunders |
| `stale-file-ref` | lie | comment claims an in-repo path that does not exist | external paths, placeholders, examples, ticketed history |
| `number-drift` | drift | magic number disagreeing with adjacent code | matching numbers, example sentences |
| `fragile-anchor` | smell | line anchors, bare see-above/below, untracked workarounds | ticketed or conditioned markers |
| `stale-doc-ref` | lie, opt-in only (`--enable stale-doc-ref`) | fenced code example calls a symbol defined nowhere in the repo | bare fences, console blocks, `...` blocks, placeholders, bound locals |
| `stale-contract-ref` | lie/drift, opt-in only | deprecation target / lock claim / env default contradicting the repo | bare prose, ticketed claims, matching defaults |
| `ghost-export` | smell, opt-in only | public symbol with no importers, no in-file use, no API marking | methods, dunders, `__init__`, `__all__`, exports, Go-exported names |
| `stale-entrypoint` | lie | scripts/bin/main pointing at nothing in-repo | malformed files, build-output dirs, external targets |
| `stale-mock-ref` | lie | @patch string naming an absent in-repo symbol | external paths, create=True, method/meta attrs |
| `unclosed-fence` | lie | Markdown fence that never closes, or is swallowed by an open block (content renders as code) | declared nesting scaffolds (` ````markdown ` around ` ```python `), bare fences inside a block |
| `phantom-package` | drift, opt-in only | import declared in no manifest | stdlib, in-repo, all dep groups, @types-covered hosts |
| `stale-cli-ref` | lie, opt-in only | documented `grounded` call with unknown subcommand/flag | prose mentions, synopsis meta-syntax, program output |

Exit codes: `0` clean, `1` a finding at or above `--fail-on` (default
`lie`), `2` usage or environment error, `3` an enabled checker raised
(scan incomplete — never reported as clean).

Suppress one accepted finding where it sits:

```python
# Calls `legacy_parse()` for old dumps.  # grounded-disable: stale-symbol-ref
```

Unknown ids in a marker warn on stderr without changing the exit code.
