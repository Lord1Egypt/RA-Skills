# Supply Chain Audit & Reproducibility

This document helps auditors verify that the pinned `inkwell-press==0.8.1` wheel
corresponds to the reviewed source code at commit `d1842ba` on the main branch of
`github.com/lijinhongucl-pixel/inkwell`.

## 1. Reproducible Build

The wheel hash in `requirements.txt` can be reproduced locally from the pinned commit:

```bash
git clone https://github.com/lijinhongucl-pixel/inkwell.git
cd inkwell
git checkout --detach d1842ba
python3 -m build --wheel
shasum -a 256 dist/*.whl
```

The output SHA-256 should match:

```
a4e7439a70b1804d84391749dd46a2e1af599f549d697f119c5a434bc2615165
```

If the hashes differ, **do not install** — the published wheel may not match the
reviewed source.

## 2. Software Bill of Materials (SBOM)

### Direct Python dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `inkwell-press` | 0.8.1 | Core CLI + pipeline |
| `Pillow` | >=12.3.0 | Image compression (transitive via inkwell-press) |

### Transitive dependency verification

`inkwell-press` has one runtime dependency: `Pillow`. To lock transitive
dependencies with hashes:

```bash
pip3 install pip-tools
echo "inkwell-press==0.8.1" > requirements.in
pip-compile --generate-hashes requirements.in --output-file requirements-lock.txt
pip3 install --require-hashes -r requirements-lock.txt
```

This produces a fully-hashed lock file covering all transitive dependencies.

### npm dependencies

ClawHub CLI (`clawhub@0.23.3`) is used **only for publishing this skill**, not at
runtime. To verify its integrity:

```bash
# Project-local install (preferred over global)
mkdir clawhub-audit && cd clawhub-audit
npm init -y
npm install clawhub@0.23.3 --save-exact
# npm generates package-lock.json with integrity hashes
cat package-lock.json | grep -A2 '"clawhub"'
```

## 3. Audit Checklist

Before treating the documented data-handling guarantees as verified:

- [ ] Reproduce the wheel hash locally (Section 1)
- [ ] Review `src/inkwell/` source at commit `d1842ba`
- [ ] Generate a full transitive lock file (Section 2)
- [ ] Confirm no post-install hooks in `pyproject.toml`
- [ ] Confirm `Pillow` is imported only for image processing (`grep -r "from PIL" src/`)
- [ ] Run the test suite: `pytest tests/ --basetemp=/tmp/inkwell-qa -q`

## 4. Post-Install Verification

```bash
# Verify the installed version matches the pin
python3 -c "import inkwell; print(inkwell.__version__)"
# Expected: 0.8.1

# Verify no unexpected network calls on a simple local run
inkwell run test.md --theme graphite-minimal --no-embed-external
# Check: no outbound requests should occur
```
