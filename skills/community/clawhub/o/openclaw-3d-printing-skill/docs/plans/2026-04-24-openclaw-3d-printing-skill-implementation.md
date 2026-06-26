# OpenClaw 3D Printing Skill Implementation Plan

> **For implementer:** Use TDD throughout. Write failing test first. Watch it fail. Then implement.

**Goal:** Publish the local parametric 3D printing skill as a clean standalone open source GitHub project with docs, examples, MIT licensing, packaging validation, and explicit inspiration credit.

**Architecture:** Keep the installable skill at repo root so the repository itself can be used directly as an OpenClaw skill. Add lightweight `examples/` and `docs/` folders around it, then verify the public project by packaging the skill and showing the resulting artifact plus repo tree.

**Tech Stack:** Markdown, Python helper scripts, git, GitHub CLI, OpenClaw skill packaging script.

---

### Task 1: Establish repository metadata and ignore rules

**Files:**
- Create: `.gitignore`
- Create: `LICENSE`
- Modify: `docs/plans/2026-04-24-openclaw-3d-printing-skill-design.md`
- Test: repo root file presence check

**Step 1: Write the failing test**
Command:
```bash
python3 - <<'PY'
from pathlib import Path
required = [Path('.gitignore'), Path('LICENSE')]
missing = [str(p) for p in required if not p.exists()]
assert not missing, f"Missing files: {missing}"
PY
```
Expected: FAIL because `.gitignore` and `LICENSE` do not exist yet.

**Step 2: Run test — confirm it fails**
Command:
```bash
python3 - <<'PY'
from pathlib import Path
required = [Path('.gitignore'), Path('LICENSE')]
missing = [str(p) for p in required if not p.exists()]
assert not missing, f"Missing files: {missing}"
PY
```
Expected: FAIL with missing file paths.

**Step 3: Write minimal implementation**
- Add a minimal Python-friendly `.gitignore`
- Add MIT license text with Antonio as copyright holder
- Keep the design doc unchanged except for any tiny consistency fix if needed

**Step 4: Run test — confirm it passes**
Command:
```bash
python3 - <<'PY'
from pathlib import Path
required = [Path('.gitignore'), Path('LICENSE')]
missing = [str(p) for p in required if not p.exists()]
assert not missing, f"Missing files: {missing}"
print('ok')
PY
```
Expected: PASS and print `ok`.

**Step 5: Commit**
```bash
git add .gitignore LICENSE docs/plans/2026-04-24-openclaw-3d-printing-skill-design.md
git commit -m "chore: add repo metadata for open source release (issue #1)
demo: verified root metadata files exist"
```

### Task 2: Move the skill into the repository root structure

**Files:**
- Create: `SKILL.md`
- Create: `scripts/mesh_io.py`
- Create: `scripts/preview.py`
- Create: `scripts/run_cadquery_model.py`
- Create: `scripts/stl_to_3mf.py`
- Create: `references/design-review.md`
- Create: `references/requirements.txt`
- Test: Python syntax compile for scripts

**Step 1: Write the failing test**
Command:
```bash
bash -lc 'python3 -m py_compile scripts/*.py'
```
Expected: FAIL because the files do not exist yet.

**Step 2: Run test — confirm it fails**
Command:
```bash
bash -lc 'python3 -m py_compile scripts/*.py'
```
Expected: FAIL with missing file errors.

**Step 3: Write minimal implementation**
- Copy the working local skill contents into root-level `SKILL.md`, `scripts/`, and `references/`
- Keep wording OpenClaw-native
- Preserve lightweight helper scripts and references

**Step 4: Run test — confirm it passes**
Command:
```bash
bash -lc 'python3 -m py_compile scripts/*.py'
```
Expected: PASS with no output.

**Step 5: Commit**
```bash
git add SKILL.md scripts references
git commit -m "feat: add installable root skill files (issue #1)
demo: py_compile passed for all helper scripts"
```

### Task 3: Add public README with attribution and install guidance

**Files:**
- Create: `README.md`
- Test: README content assertions

**Step 1: Write the failing test**
Command:
```bash
python3 - <<'PY'
from pathlib import Path
text = Path('README.md').read_text()
needles = [
    'Inspired by',
    'https://github.com/flowful-ai/cad-skill',
    'MIT',
    'SKILL.md',
    'CadQuery',
]
missing = [n for n in needles if n not in text]
assert not missing, f"Missing README content: {missing}"
PY
```
Expected: FAIL because `README.md` does not exist yet.

**Step 2: Run test — confirm it fails**
Command:
```bash
python3 - <<'PY'
from pathlib import Path
text = Path('README.md').read_text()
needles = [
    'Inspired by',
    'https://github.com/flowful-ai/cad-skill',
    'MIT',
    'SKILL.md',
    'CadQuery',
]
missing = [n for n in needles if n not in text]
assert not missing, f"Missing README content: {missing}"
PY
```
Expected: FAIL with file not found.

**Step 3: Write minimal implementation**
README sections:
- project overview
- what the skill does
- install into OpenClaw
- Python and CadQuery dependency expectations
- packaging/validation instructions
- inspiration credit with link to Flowful repo
- explicit note that this is an OpenClaw-native adaptation, not an official fork

**Step 4: Run test — confirm it passes**
Command:
```bash
python3 - <<'PY'
from pathlib import Path
text = Path('README.md').read_text()
needles = [
    'Inspired by',
    'https://github.com/flowful-ai/cad-skill',
    'MIT',
    'SKILL.md',
    'CadQuery',
]
missing = [n for n in needles if n not in text]
assert not missing, f"Missing README content: {missing}"
print('ok')
PY
```
Expected: PASS and print `ok`.

**Step 5: Commit**
```bash
git add README.md
git commit -m "docs: add public README with attribution (issue #1)
demo: verified README includes install and credit sections"
```

### Task 4: Add examples and lightweight docs structure

**Files:**
- Create: `examples/simple-bracket.md`
- Create: `examples/enclosure-brief.md`
- Modify: `README.md`
- Test: examples existence and README references

**Step 1: Write the failing test**
Command:
```bash
python3 - <<'PY'
from pathlib import Path
checks = {
    'examples/simple-bracket.md': Path('examples/simple-bracket.md').exists(),
    'examples/enclosure-brief.md': Path('examples/enclosure-brief.md').exists(),
}
missing = [name for name, ok in checks.items() if not ok]
readme = Path('README.md').read_text() if Path('README.md').exists() else ''
assert not missing, f"Missing example files: {missing}"
assert 'examples/' in readme, 'README does not mention examples/'
PY
```
Expected: FAIL because the examples do not exist yet.

**Step 2: Run test — confirm it fails**
Command:
```bash
python3 - <<'PY'
from pathlib import Path
checks = {
    'examples/simple-bracket.md': Path('examples/simple-bracket.md').exists(),
    'examples/enclosure-brief.md': Path('examples/enclosure-brief.md').exists(),
}
missing = [name for name, ok in checks.items() if not ok]
readme = Path('README.md').read_text() if Path('README.md').exists() else ''
assert not missing, f"Missing example files: {missing}"
assert 'examples/' in readme, 'README does not mention examples/'
PY
```
Expected: FAIL.

**Step 3: Write minimal implementation**
- Add two short example prompt briefs
- Update README to point readers to the examples folder
- Keep examples concise and practical

**Step 4: Run test — confirm it passes**
Command:
```bash
python3 - <<'PY'
from pathlib import Path
checks = {
    'examples/simple-bracket.md': Path('examples/simple-bracket.md').exists(),
    'examples/enclosure-brief.md': Path('examples/enclosure-brief.md').exists(),
}
missing = [name for name, ok in checks.items() if not ok]
readme = Path('README.md').read_text()
assert not missing, f"Missing example files: {missing}"
assert 'examples/' in readme, 'README does not mention examples/'
print('ok')
PY
```
Expected: PASS and print `ok`.

**Step 5: Commit**
```bash
git add examples README.md
git commit -m "docs: add usage examples for the skill (issue #1)
demo: verified example files and README references"
```

### Task 5: Validate packaging and repo shape for public release

**Files:**
- Modify: `README.md` if validation reveals a mismatch
- Test: skill packaging command

**Step 1: Write the failing test**
Command:
```bash
python3 /home/berry/.nvm/versions/node/v24.13.0/lib/node_modules/openclaw/skills/skill-creator/scripts/package_skill.py . ./dist
```
Expected: FAIL initially if any root layout or metadata issue remains.

**Step 2: Run test — confirm it fails**
Command:
```bash
python3 /home/berry/.nvm/versions/node/v24.13.0/lib/node_modules/openclaw/skills/skill-creator/scripts/package_skill.py . ./dist
```
Expected: either FAIL and reveal the last packaging mismatch, or PASS immediately if prior tasks already satisfied it.

**Step 3: Write minimal implementation**
- Fix any packaging issues only if validation finds them
- Keep changes minimal

**Step 4: Run test — confirm it passes**
Command:
```bash
python3 /home/berry/.nvm/versions/node/v24.13.0/lib/node_modules/openclaw/skills/skill-creator/scripts/package_skill.py . ./dist
```
Expected: PASS and emit a `.skill` artifact in `dist/`.

**Step 5: Commit**
```bash
git add .
git commit -m "chore: validate package for initial release (issue #1)
demo: packaged root skill successfully"
```

### Task 6: Demo the initial release and push the branch

**Files:**
- Modify: none unless demo reveals a final issue
- Test: repo tree plus packaging artifact demonstration

**Step 1: Write the failing test**
Command:
```bash
python3 - <<'PY'
from pathlib import Path
assert Path('dist').exists(), 'dist directory missing'
artifacts = list(Path('dist').glob('*.skill'))
assert artifacts, 'No packaged skill artifact found'
print(artifacts[0])
PY
```
Expected: FAIL until packaging has succeeded.

**Step 2: Run test — confirm it fails**
Command:
```bash
python3 - <<'PY'
from pathlib import Path
assert Path('dist').exists(), 'dist directory missing'
artifacts = list(Path('dist').glob('*.skill'))
assert artifacts, 'No packaged skill artifact found'
print(artifacts[0])
PY
```
Expected: FAIL if the packaging artifact is missing.

**Step 3: Write minimal implementation**
- Ensure packaging output exists
- Capture repo tree, README attribution, and artifact path for demo
- Push commits to GitHub after the demo is approved

**Step 4: Run test — confirm it passes**
Command:
```bash
python3 - <<'PY'
from pathlib import Path
assert Path('dist').exists(), 'dist directory missing'
artifacts = list(Path('dist').glob('*.skill'))
assert artifacts, 'No packaged skill artifact found'
print(artifacts[0])
PY
```
Expected: PASS and print the packaged artifact path.

**Step 5: Commit**
```bash
git add .
git commit -m "release: prepare initial public skill release (issue #1)
demo: showed repo tree, attribution, and packaged artifact"
```
