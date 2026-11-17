<!-- Default template: infrastructure (modules, references, scripts, docs, .github).
     For novel content (chapters, setting, character) use ?template=content.md -->

## Description of Changes

<!-- What changed, and why. One paragraph. -->

## Affected Module(s)

- [ ] modules/worldbuilding/
- [ ] modules/character-design/
- [ ] modules/chapter-writing/
- [ ] modules/continuity-check/
- [ ] modules/publishing-workflow/
- [ ] modules/continuity-tracker/
- [ ] references/
- [ ] prompts/
- [ ] scripts/
- [ ] .github/
- [ ] Other (please specify)

## Type of Change

- [ ] Bug fix
- [ ] New module / script / capability
- [ ] Documentation
- [ ] Licensing or compliance
- [ ] Housekeeping (hygiene, labels, CI)

## Checklist

- [ ] I have read CONTRIBUTING.md
- [ ] My changes follow the coding style guidelines
- [ ] I have updated documentation where needed
- [ ] I have updated CHANGELOG.md
- [ ] My changes do not introduce breaking changes
- [ ] I have added tests to cover my changes (if applicable)
- [ ] All existing tests pass
- [ ] License files are up to date (GPL-3.0 in LICENSE, CC BY-NC-SA 4.0 in LICENSES/)

## Gates

Run from the repository root and paste the result:

```
python scripts/scan_hygiene.py --root . --max-lines 500 \
    --allow "README FOR AI.md,CHANGELOG.md,LICENSE,LICENSES/CC-BY-NC-SA-4.0.txt" \
    --fail-on crlf,junk,mojibake
python scripts/check_refs.py --root . --kind MISSING --kind NONRELEASE
```

- [ ] `scan_hygiene.py` — no finding in `crlf` / `junk` / `mojibake`
- [ ] `check_refs.py` — `NONRELEASE` is zero; new `MISSING` entries explained
- [ ] New or changed Python: writes text with `newline='\n'` (see scripts/README.md)

## Harness Compliance Confirmation

- [ ] Constraint before generation: Rules are defined before workflow steps
- [ ] Structured memory: State is persisted in structured files
- [ ] Verification gates: Checks are in place before publish
- [ ] Modular decomposition: No circular dependencies
- [ ] Feedback loops: Structured feedback mechanism exists
- [ ] Progressive disclosure: Content is layered appropriately
- [ ] Context budget management: Files are under line limits, or exempted via `--allow`
- [ ] Human-in-the-loop: Manual oversight steps are present
- [ ] Error recovery: State snapshots are maintained
- [ ] Role isolation: Each module has single responsibility
- [ ] License compliance: GPL-3.0 and CC BY-NC-SA 4.0 headers present where required

## Related Issues

Closes #
