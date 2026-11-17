---
name: structure-mapping
description: >-
  Map directory layout, languages and large files before choosing
  where tests go, so generated tests sit beside the code they cover.
---

# Structure Mapping

Run this before test discovery on an unfamiliar codebase, or when a
change spans several packages. Test placement follows the source
layout, so a wrong guess about the layout puts tests where the runner
never collects them.

## Root

Confirm the root with `pwd`. Note monorepo boundaries, workspace
roots and subproject paths, and read the project type from its
manifest (`package.json`, `Cargo.toml`, `pyproject.toml`).

## Layout

Capture the top-level directories with `tree -L 2 -d`, or
`find . -type d -maxdepth 2` where `tree` is absent. Locate `src/`,
`lib/`, `tests/`, `docs/` and `scripts/`, and note any layout that
departs from them, since the test runner's collection paths depend on
it.

## Languages

Count files by extension, excluding `.venv`, `__pycache__`,
`node_modules` and `.git`:

```bash
find . -name "*.py" -not -path "*/.venv/*" -not -path "*/__pycache__/*" \
  -not -path "*/node_modules/*" -not -path "*/.git/*" | wc -l
```

Note configuration, generated and vendored files. Generated and
vendored code gets no new tests.

## Hotspots

List the largest files, which are the likeliest to lack focused
tests:

```bash
find . -type f -name "*.py" -not -path "*/.venv/*" -exec wc -l {} + \
  | sort -rn | head -10
```

Flag deeply nested directories and files with unusual names or
placement.

## Exit Criteria

- [ ] The root, project type and test directory are named
- [ ] File counts per dominant language are recorded
- [ ] The ten largest source files are listed, with the ones that
      have no matching test file marked
