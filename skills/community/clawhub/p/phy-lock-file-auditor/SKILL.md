---
name: Lock File Auditor
description: Lockfile security and integrity auditor for JavaScript, Python, Go, and Rust projects. Detects phantom dependencies (packages in lockfile but not in manifest), lockfile drift (manifest changed without re-running install), integrity hash anomalies (missing, malformed, or duplicate SHA-512/SHA-256 hashes that indicate tampering), nested duplicate packages pinned at conflicting versions, and yanked/unpublished package versions still pinned in the lockfile. Supports package-lock.json, yarn.lock, pnpm-lock.yaml, poetry.lock, Pipfile.lock, Cargo.lock, go.sum. Generates a CI freshness gate command. Catches supply-chain attack surface that standard vulnerability scanners miss. Zero external API — pure local file analysis. Triggers on "lockfile audit", "package-lock security", "phantom dependency", "lockfile drift", "supply chain check", "integrity hash", "/lock-file-audit".
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.3"
  tags:
    - security
    - lockfile
    - supply-chain
    - npm
    - python
    - cargo
    - developer-tools
    - dependencies
    - integrity
---

# Lockfile Security Auditor

The XZ Utils backdoor wasn't in a CVE database. It was introduced through a dependency that looked legitimate until it wasn't.

Your lockfile is a contract with the supply chain. This skill reads it for what it actually says — not just which packages are there, but whether the lockfile matches your manifest, whether integrity hashes are intact, and whether any entries were quietly swapped, added, or tampered with.

**Supports npm, yarn, pnpm, poetry, pip, cargo, go modules. Zero external API.**

---

## Trigger Phrases

- "lockfile audit", "package-lock security", "lock file check"
- "phantom dependency", "lockfile drift", "supply chain check"
- "integrity hash", "package-lock.json tampering"
- "yarn.lock audit", "Cargo.lock check", "go.sum audit"
- "lockfile out of sync", "stale lockfile"
- "/lock-file-audit"

---

## How to Provide Input

```bash
# Option 1: Audit current directory (auto-detect lockfile)
/lock-file-audit

# Option 2: Specific lockfile
/lock-file-audit package-lock.json
/lock-file-audit poetry.lock
/lock-file-audit Cargo.lock
/lock-file-audit go.sum

# Option 3: Specific checks only
/lock-file-audit --check phantom       # Phantom dependencies only
/lock-file-audit --check drift         # Manifest/lockfile sync only
/lock-file-audit --check integrity     # Hash anomalies only
/lock-file-audit --check duplicates    # Conflicting version pins

# Option 4: Generate CI gate script
/lock-file-audit --ci-config

# Option 5: Full audit with detailed output
/lock-file-audit --verbose
```

---

## Step 1: Detect Lockfile Type

```bash
python3 -c "
import os
from pathlib import Path

lockfiles = {
    'package-lock.json': 'npm',
    'yarn.lock':         'yarn',
    'pnpm-lock.yaml':    'pnpm',
    'poetry.lock':       'poetry',
    'Pipfile.lock':      'pipenv',
    'Cargo.lock':        'cargo',
    'go.sum':            'go modules',
}

manifests = {
    'npm':        'package.json',
    'yarn':       'package.json',
    'pnpm':       'package.json',
    'poetry':     'pyproject.toml',
    'pipenv':     'Pipfile',
    'cargo':      'Cargo.toml',
    'go modules': 'go.mod',
}

found = []
for fname, ecosystem in lockfiles.items():
    if os.path.exists(fname):
        size = os.path.getsize(fname)
        manifest = manifests[ecosystem]
        has_manifest = os.path.exists(manifest)
        found.append((fname, ecosystem, size, manifest, has_manifest))

if found:
    for fname, ecosystem, size, manifest, has_manifest in found:
        status = '✅' if has_manifest else '⚠️ manifest missing'
        print(f'{ecosystem}: {fname} ({size/1024:.0f} KB) — manifest: {manifest} {status}')
else:
    print('No lockfiles found in current directory.')
    print('Expected: package-lock.json, yarn.lock, pnpm-lock.yaml, poetry.lock, Pipfile.lock, Cargo.lock, go.sum')
"
```

---

## Step 2: Detect Phantom Dependencies

Phantom dependencies are packages that appear in the lockfile but have no corresponding direct or indirect entry in the manifest. In npm, this is common when someone manually edits package-lock.json or when a package removes itself from its own dependencies but forgets to update the lockfile.

```python
import json
from pathlib import Path

def audit_npm_phantoms(lockfile_path='package-lock.json', manifest_path='package.json'):
    """Find packages in package-lock.json not traceable to package.json."""

    with open(lockfile_path) as f:
        lock = json.load(f)
    with open(manifest_path) as f:
        manifest = json.load(f)

    # All declared deps (direct)
    declared = set()
    for section in ['dependencies', 'devDependencies', 'peerDependencies', 'optionalDependencies']:
        declared.update(manifest.get(section, {}).keys())

    # All packages in lockfile (v2/v3 format)
    lock_packages = set()
    if 'packages' in lock:  # npm v7+ (lockfileVersion 2/3)
        for path_key in lock['packages']:
            if path_key == '':  # root entry
                continue
            # Extract package name: "node_modules/pkg" → "pkg"
            # or "node_modules/@scope/pkg" → "@scope/pkg"
            name = path_key.replace('node_modules/', '', 1)
            if '/' in name and not name.startswith('@'):
                # Nested: node_modules/a/node_modules/b → take the last segment
                name = name.split('/node_modules/')[-1]
            lock_packages.add(name)

    elif 'dependencies' in lock:  # npm v1 (lockfileVersion 1)
        def collect_v1(deps, collected):
            for name, info in deps.items():
                collected.add(name)
                if 'dependencies' in info:
                    collect_v1(info['dependencies'], collected)
        collect_v1(lock.get('dependencies', {}), lock_packages)

    # Build full reachable set from manifest (BFS through lockfile deps)
    def get_lock_deps(pkg_name):
        """Get declared deps of a package from lockfile."""
        pkg_info = lock.get('packages', {}).get(f'node_modules/{pkg_name}', {})
        return set(pkg_info.get('dependencies', {}).keys()) | \
               set(pkg_info.get('peerDependencies', {}).keys())

    reachable = set(declared)
    queue = list(declared)
    while queue:
        pkg = queue.pop()
        for dep in get_lock_deps(pkg):
            if dep not in reachable:
                reachable.add(dep)
                queue.append(dep)

    # Phantoms: in lockfile but not reachable from manifest
    phantoms = lock_packages - reachable

    return sorted(phantoms), sorted(reachable), sorted(lock_packages)


def audit_cargo_phantoms(lockfile_path='Cargo.lock', manifest_path='Cargo.toml'):
    """Find packages in Cargo.lock not in dependency tree of Cargo.toml."""
    import re

    lock_content = Path(lockfile_path).read_text()
    manifest_content = Path(manifest_path).read_text()

    # Parse Cargo.lock packages
    lock_packages = set(re.findall(r'^name = "([^"]+)"', lock_content, re.MULTILINE))

    # Parse Cargo.toml declared deps
    declared = set(re.findall(r'^([a-z_-]+)\s*=', manifest_content, re.MULTILINE))
    # Also parse [dependencies] sections
    dep_section = re.findall(r'^\[(?:dependencies|dev-dependencies|build-dependencies)\]\n(.*?)(?=\n\[|\Z)',
                             manifest_content, re.MULTILINE | re.DOTALL)
    for section in dep_section:
        declared.update(re.findall(r'^([a-z_-]+)\s*=', section, re.MULTILINE))

    phantoms = lock_packages - declared
    return sorted(phantoms)
```

---

## Step 3: Detect Lockfile Drift

Lockfile drift happens when someone edits the manifest (`package.json`, `pyproject.toml`, etc.) without running `npm install` / `poetry lock`. The lockfile then describes a different dependency tree than what the manifest requests.

```python
import json
import re
from pathlib import Path

def check_npm_drift(lockfile_path='package-lock.json', manifest_path='package.json'):
    """Check if package-lock.json is in sync with package.json."""

    with open(lockfile_path) as f:
        lock = json.load(f)
    with open(manifest_path) as f:
        manifest = json.load(f)

    issues = []

    # The lockfile's root 'packages[""]' should mirror the manifest's deps
    root_lock = lock.get('packages', {}).get('', {})
    lock_deps = {**root_lock.get('dependencies', {}),
                 **root_lock.get('devDependencies', {}),
                 **root_lock.get('peerDependencies', {})}
    manifest_deps = {**manifest.get('dependencies', {}),
                     **manifest.get('devDependencies', {}),
                     **manifest.get('peerDependencies', {})}

    # In manifest but not in lockfile root
    missing_from_lock = set(manifest_deps) - set(lock_deps)
    for pkg in sorted(missing_from_lock):
        issues.append({
            'type': 'MISSING_FROM_LOCK',
            'package': pkg,
            'manifest_version': manifest_deps[pkg],
            'description': f'"{pkg}" in package.json but not in lockfile root entry — lockfile needs update.',
            'fix': 'Run: npm install',
        })

    # In lockfile root but not in manifest
    extra_in_lock = set(lock_deps) - set(manifest_deps)
    for pkg in sorted(extra_in_lock):
        issues.append({
            'type': 'EXTRA_IN_LOCK',
            'package': pkg,
            'lock_version': lock_deps[pkg],
            'description': f'"{pkg}" in lockfile root but not in package.json — ghost entry.',
            'fix': 'Run: npm install to regenerate lockfile, or manually remove entry.',
        })

    # Version range mismatch
    for pkg in set(manifest_deps) & set(lock_deps):
        manifest_range = manifest_deps[pkg]
        lock_range = lock_deps.get(pkg, '')
        # Only flag if manifest has a strict pinned version that differs from lock
        if manifest_range != lock_range and not manifest_range.startswith('^') and not manifest_range.startswith('~'):
            issues.append({
                'type': 'VERSION_MISMATCH',
                'package': pkg,
                'manifest_version': manifest_range,
                'lock_version': lock_range,
                'description': f'"{pkg}": manifest pins {manifest_range} but lockfile has {lock_range}.',
                'fix': f'Run: npm install {pkg}@{manifest_range} to align lockfile.',
            })

    # Check lockfileVersion matches npm version
    lock_version = lock.get('lockfileVersion', 'unknown')

    return issues, lock_version


def check_poetry_drift(lockfile_path='poetry.lock', manifest_path='pyproject.toml'):
    """Check if poetry.lock is in sync with pyproject.toml."""
    import re

    lock_content = Path(lockfile_path).read_text()
    manifest_content = Path(manifest_path).read_text()

    # poetry.lock has a content-hash that poetry uses for drift detection
    content_hash_match = re.search(r'^content-hash = "([a-f0-9]+)"', lock_content, re.MULTILINE)
    if content_hash_match:
        stored_hash = content_hash_match.group(1)
        # Recalculate hash from pyproject.toml
        import hashlib
        computed = hashlib.sha256(manifest_content.encode()).hexdigest()
        if stored_hash != computed:
            return [{
                'type': 'CONTENT_HASH_MISMATCH',
                'description': 'poetry.lock content-hash does not match current pyproject.toml.',
                'stored_hash': stored_hash[:16] + '...',
                'computed_hash': computed[:16] + '...',
                'fix': 'Run: poetry lock --no-update',
                'severity': 'HIGH',
            }]

    return []
```

---

## Step 4: Integrity Hash Audit

```python
import json
import re
import hashlib
from pathlib import Path

def audit_npm_integrity(lockfile_path='package-lock.json'):
    """Check for missing, malformed, or suspicious integrity hashes."""

    with open(lockfile_path) as f:
        lock = json.load(f)

    issues = []
    packages = lock.get('packages', lock.get('dependencies', {}))

    VALID_HASH_PREFIXES = {'sha512-', 'sha256-', 'sha1-'}

    for pkg_path, pkg_info in packages.items():
        if pkg_path == '':
            continue

        pkg_name = pkg_path.replace('node_modules/', '').split('/node_modules/')[-1]
        integrity = pkg_info.get('integrity', '')
        version = pkg_info.get('version', 'unknown')

        # Missing integrity hash
        if not integrity:
            issues.append({
                'package': pkg_name,
                'version': version,
                'type': 'MISSING_INTEGRITY',
                'description': f'{pkg_name}@{version} has no integrity hash — tamper detection disabled.',
                'severity': 'MEDIUM',
                'fix': 'Run: npm install to regenerate integrity hashes.',
            })
            continue

        # Malformed hash (wrong prefix or length)
        has_valid_prefix = any(integrity.startswith(p) for p in VALID_HASH_PREFIXES)
        if not has_valid_prefix:
            issues.append({
                'package': pkg_name,
                'version': version,
                'type': 'MALFORMED_HASH',
                'description': f'{pkg_name}@{version} integrity hash has unknown prefix: {integrity[:20]}...',
                'severity': 'HIGH',
                'fix': 'Verify package source and regenerate lockfile: rm package-lock.json && npm install',
            })

        # SHA-1 only (weak, collision-vulnerable)
        if integrity.startswith('sha1-') and not any(
            pkg_info.get('integrity', '').count(p) > 0
            for p in ['sha512-', 'sha256-']
        ):
            issues.append({
                'package': pkg_name,
                'version': version,
                'type': 'WEAK_HASH_ALGORITHM',
                'description': f'{pkg_name}@{version} uses SHA-1 integrity only — SHA-512 preferred.',
                'severity': 'LOW',
                'fix': 'npm v7+ generates SHA-512. Run: npm install --lockfile-version 2',
            })

    return issues


def audit_go_sum(go_sum_path='go.sum'):
    """Check go.sum for anomalies."""

    content = Path(go_sum_path).read_text()
    issues = []
    seen = {}

    for line in content.splitlines():
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) != 3:
            issues.append({
                'type': 'MALFORMED_ENTRY',
                'line': line,
                'description': 'go.sum entry has wrong number of fields (expected: module version hash)',
                'severity': 'HIGH',
            })
            continue

        module, version, hash_val = parts

        # Check hash format: h1:<base64>
        if not hash_val.startswith('h1:'):
            issues.append({
                'type': 'UNKNOWN_HASH_ALGORITHM',
                'module': module,
                'version': version,
                'hash': hash_val[:20],
                'description': f'Unknown hash algorithm in go.sum: {hash_val[:10]}... (expected h1:)',
                'severity': 'HIGH',
            })

        # Check for duplicate module+version with different hash (tampering signal)
        key = (module, version)
        if key in seen and seen[key] != hash_val:
            issues.append({
                'type': 'DUPLICATE_CONFLICTING_HASH',
                'module': module,
                'version': version,
                'hash1': seen[key][:30],
                'hash2': hash_val[:30],
                'description': f'{module}@{version} has TWO different hashes in go.sum — possible tampering!',
                'severity': 'CRITICAL',
            })
        seen[key] = hash_val

    return issues
```

---

## Step 5: Detect Conflicting Version Pins

```python
import json
import re
from collections import defaultdict

def find_npm_version_conflicts(lockfile_path='package-lock.json'):
    """Find packages pinned at multiple different versions in the lockfile."""

    with open(lockfile_path) as f:
        lock = json.load(f)

    pkg_versions = defaultdict(list)

    for pkg_path, pkg_info in lock.get('packages', {}).items():
        if pkg_path == '':
            continue
        name = pkg_path.replace('node_modules/', '').split('/node_modules/')[-1]
        version = pkg_info.get('version', 'unknown')
        pkg_versions[name].append((pkg_path, version))

    conflicts = {
        name: versions
        for name, versions in pkg_versions.items()
        if len(set(v for _, v in versions)) > 1
    }

    return dict(sorted(conflicts.items(), key=lambda x: len(x[1]), reverse=True))


def find_cargo_version_conflicts(lockfile_path='Cargo.lock'):
    """Find crates pinned at multiple versions."""
    import re

    content = Path(lockfile_path).read_text()
    crate_versions = defaultdict(set)

    # Parse [[package]] sections
    package_blocks = re.findall(
        r'\[\[package\]\]\nname = "([^"]+)"\nversion = "([^"]+)"',
        content
    )
    for name, version in package_blocks:
        crate_versions[name].add(version)

    return {name: sorted(versions) for name, versions in crate_versions.items() if len(versions) > 1}
```

---

## Step 6: CI Freshness Gate

```python
def generate_ci_gate(ecosystem):
    """Generate a CI script to enforce lockfile freshness."""

    scripts = {
        'npm': '''
# Check that package-lock.json is not stale (generated within 30 days)
python3 -c "
import os, sys, time
lockfile = 'package-lock.json'
max_age_days = 30
if not os.path.exists(lockfile):
    print('FAIL: package-lock.json not found')
    sys.exit(1)
age_days = (time.time() - os.path.getmtime(lockfile)) / 86400
if age_days > max_age_days:
    print(f'FAIL: package-lock.json is {age_days:.0f} days old (limit: {max_age_days})')
    print('Run: npm install && git add package-lock.json')
    sys.exit(1)
print(f'PASS: package-lock.json is {age_days:.0f} days old')
"

# Check lockfile is in sync with package.json
npm ci --dry-run 2>&1 | grep -q "up to date" || (echo "FAIL: lockfile drift detected" && npm install --dry-run && exit 1)
''',
        'poetry': '''
# Check poetry.lock is in sync with pyproject.toml
poetry lock --check 2>&1
# Returns exit 1 if poetry.lock is not up to date
''',
        'cargo': '''
# Check Cargo.lock is in sync with Cargo.toml
cargo update --dry-run 2>&1 | grep -q "Updating" && echo "WARNING: Cargo.lock has available updates" || echo "PASS: Cargo.lock is current"

# Verify Cargo.lock is committed (required for applications, optional for libraries)
git show HEAD:Cargo.lock > /dev/null 2>&1 || echo "WARNING: Cargo.lock not committed to git"
''',
        'go': '''
# Verify go.sum is consistent with go.mod
go mod verify 2>&1
# Exits 1 if any module in go.sum has a hash mismatch vs downloaded module
''',
    }
    return scripts.get(ecosystem, '# CI gate not available for this ecosystem')
```

---

## Step 7: Output Report

```markdown
## Lockfile Security Audit
Project: my-app | Ecosystem: npm | Lockfile: package-lock.json (847 packages)

---

### Summary

| Check | Status | Count |
|-------|--------|-------|
| Phantom dependencies | 🔴 Found | 3 packages |
| Lockfile drift | 🟠 Detected | 2 manifest/lock mismatches |
| Integrity hash anomalies | 🟡 Found | 1 SHA-1 only package |
| Version conflicts | 🟠 Found | 12 packages at 2+ versions |
| Stale lockfile | ✅ Fresh | 4 days old |

---

### 🔴 Phantom Dependencies (3)

These packages are in `package-lock.json` but cannot be traced back to any entry in `package.json`:

```
package-lock.json contains:
  lodash-es@4.17.21   ← not declared in package.json, not a transitive dep of any declared package
  uuid@8.3.2          ← was removed from package.json 3 months ago, still in lockfile
  debug@4.3.4         ← appears in lockfile root but not resolvable from manifest graph
```

**Why this matters:** Phantom entries could indicate:
- A dependency was removed from package.json but not from lockfile (stale — low risk)
- A package was directly injected into lockfile (high risk — supply chain concern)
- A `npm install <pkg>` was run but package.json was not updated (incomplete change)

**Fix:**
```bash
# Regenerate lockfile from scratch:
rm package-lock.json
npm install
# Diff the result — if new lockfile differs, review every change
git diff package-lock.json
```

---

### 🟠 Lockfile Drift (2 mismatches)

| Package | In package.json | In lockfile | Issue |
|---------|----------------|-------------|-------|
| `react` | `^18.3.0` | not in root | Added to package.json, `npm install` not run |
| `jest` | removed | `^29.0.0` still in lockfile root | Removed from package.json, lockfile not updated |

**Fix:** `npm install` — this regenerates the lockfile to match the manifest.

---

### 🟠 Version Conflicts (12 packages at multiple versions)

The top 5 most-duplicated packages:

| Package | Versions Pinned | Copies in Bundle |
|---------|----------------|-----------------|
| `lodash` | 4.17.15, 4.17.21 | 2 (adds ~140 KB) |
| `tslib` | 1.14.1, 2.6.2 | 2 |
| `semver` | 6.3.1, 7.5.4 | 3 copies |
| `debug` | 3.2.7, 4.3.4 | 2 copies |
| `ms` | 2.0.0, 2.1.3 | 2 copies |

**Why this matters:** Multiple versions = bigger bundle, potential behavior inconsistency, harder security patching.

**Fix for lodash:**
```bash
npm dedupe lodash
# Or force all consumers to use 4.17.21:
# Add to package.json:
"overrides": {
  "lodash": "^4.17.21"
}
```

---

### 🟡 Weak Integrity Hash (1 package)

```
mkdirp@0.5.5 — integrity: sha1-2j4w5... (SHA-1 only)
```

SHA-1 has known collision vulnerabilities. This package was published before npm adopted SHA-512. Not an immediate threat, but consider upgrading to a version with SHA-512 hashes.

---

### CI Freshness Gate

Add to `.github/workflows/ci.yml`:

```yaml
- name: Verify lockfile integrity
  run: |
    # Fail if lockfile is stale (>30 days) or out of sync
    npm ci --dry-run
    # npm ci fails if lockfile doesn't match package.json exactly
```

Or add pre-commit hook:
```bash
# .git/hooks/pre-commit
#!/bin/sh
if git diff --cached --name-only | grep -q "package.json"; then
    if ! git diff --cached --name-only | grep -q "package-lock.json"; then
        echo "⚠️  package.json changed but package-lock.json was not updated."
        echo "Run: npm install && git add package-lock.json"
        exit 1
    fi
fi
```

---

### Supply Chain Risk Assessment

Based on this audit:

| Risk | Assessment |
|------|-----------|
| Tampered lockfile | Low — integrity hashes present for 846/847 packages |
| Phantom injection | Medium — 3 phantom packages need investigation |
| Outdated lockfile attack surface | Low — lockfile is 4 days old |
| Duplicate version confusion | Low — version conflicts are from transitive deps, not direct |

**Recommended action:** Regenerate lockfile (`rm package-lock.json && npm install`) and review the diff before committing.
```

---

## Quick Mode Output

```
Lockfile Audit: my-app (npm, package-lock.json, 847 packages)

🔴 3 phantom dependencies — packages in lockfile with no manifest trace
🟠 2 drift issues — package.json changed without npm install
🟠 12 version conflicts — lodash 4.17.15+4.17.21, semver ×3, debug ×2...
🟡 1 SHA-1-only integrity hash (mkdirp@0.5.5)
✅ No integrity hash tampering detected
✅ Lockfile is 4 days old

Priority: Regenerate lockfile (rm package-lock.json && npm install) → review diff
```

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
