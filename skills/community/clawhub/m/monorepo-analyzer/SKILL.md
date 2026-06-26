---
name: monorepo-analyzer
description: Analyze monorepo structure — detect workspace tools (npm/yarn/pnpm/lerna/nx/turbo/cargo/go), map inter-package dependencies, find unused packages, detect version inconsistencies, compute build order, and identify circular dependencies.
---

# Monorepo Analyzer

Understand and audit monorepo structure. Detects workspace configuration, maps package dependencies, finds problems (circular deps, version mismatches, unused packages), and computes optimal build order.

Use when: "analyze this monorepo", "show package dependencies", "find unused packages", "check for circular deps", "what's the build order", "monorepo health check", or when onboarding to a large monorepo.

## Commands

### 1. `discover` — Detect Monorepo Configuration

Identify the workspace tool and enumerate all packages.

```bash
# Detect workspace tool
echo "Checking workspace configuration..."

# npm workspaces (package.json)
if [ -f "package.json" ]; then
  python3 -c "
import json, glob
d = json.load(open('package.json'))
ws = d.get('workspaces', [])
if isinstance(ws, dict): ws = ws.get('packages', [])
if ws:
    print('Tool: npm workspaces')
    print(f'Workspace globs: {ws}')
    for pattern in ws:
        for p in glob.glob(pattern + '/package.json'):
            name = json.load(open(p)).get('name', p)
            print(f'  Package: {name} ({p})')
" 2>/dev/null
fi

# pnpm workspaces
if [ -f "pnpm-workspace.yaml" ]; then
  echo "Tool: pnpm workspaces"
  cat pnpm-workspace.yaml
fi

# Yarn workspaces (package.json or .yarnrc.yml)
if [ -f ".yarnrc.yml" ]; then
  echo "Tool: Yarn (Berry)"
  grep "nodeLinker" .yarnrc.yml 2>/dev/null
fi

# Lerna
if [ -f "lerna.json" ]; then
  echo "Tool: Lerna"
  cat lerna.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'Version: {d.get(\"version\")}, Packages: {d.get(\"packages\")}')" 2>/dev/null
fi

# Nx
if [ -f "nx.json" ]; then
  echo "Tool: Nx"
  cat nx.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'Affected default base: {d.get(\"affected\",{}).get(\"defaultBase\",\"main\")}')" 2>/dev/null
fi

# Turborepo
if [ -f "turbo.json" ]; then
  echo "Tool: Turborepo"
  cat turbo.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'Pipeline tasks: {list(d.get(\"pipeline\",d.get(\"tasks\",{})).keys())}')" 2>/dev/null
fi

# Cargo workspaces (Rust)
if [ -f "Cargo.toml" ]; then
  grep -A20 "\[workspace\]" Cargo.toml 2>/dev/null && echo "Tool: Cargo workspace"
fi

# Go workspaces
if [ -f "go.work" ]; then
  echo "Tool: Go workspace"
  cat go.work
fi
```

Output: workspace tool, total package count, package names and paths.

### 2. `deps` — Inter-Package Dependency Graph

Map which packages depend on which other packages within the monorepo.

```bash
# For JS/TS monorepos: extract internal dependencies
python3 -c "
import json, glob, os

# Collect all package names
packages = {}
for pj in glob.glob('**/package.json', recursive=True):
    if 'node_modules' in pj: continue
    try:
        d = json.load(open(pj))
        name = d.get('name')
        if name:
            packages[name] = {
                'path': os.path.dirname(pj),
                'deps': list(d.get('dependencies', {}).keys()),
                'devDeps': list(d.get('devDependencies', {}).keys()),
                'peerDeps': list(d.get('peerDependencies', {}).keys())
            }
    except: pass

# Filter to internal deps only
internal_names = set(packages.keys())
print(f'Total packages: {len(packages)}')
print()
for name, info in sorted(packages.items()):
    internal_deps = [d for d in info['deps'] if d in internal_names]
    internal_dev = [d for d in info['devDeps'] if d in internal_names]
    internal_peer = [d for d in info['peerDeps'] if d in internal_names]
    if internal_deps or internal_dev or internal_peer:
        print(f'{name}:')
        for d in internal_deps: print(f'  → {d} (dependency)')
        for d in internal_dev: print(f'  → {d} (devDependency)')
        for d in internal_peer: print(f'  → {d} (peerDependency)')
    else:
        print(f'{name}: (no internal deps — leaf package)')
" 2>/dev/null
```

For Cargo/Go workspaces, parse respective config files similarly.

Generate a Mermaid dependency diagram:

```
graph LR
  A[app] --> B[ui-lib]
  A --> C[api-client]
  B --> D[utils]
  C --> D
```

### 3. `circular` — Detect Circular Dependencies

```bash
python3 -c "
import json, glob, os

packages = {}
for pj in glob.glob('**/package.json', recursive=True):
    if 'node_modules' in pj: continue
    try:
        d = json.load(open(pj))
        name = d.get('name')
        if name:
            all_deps = set(d.get('dependencies', {}).keys()) | set(d.get('devDependencies', {}).keys())
            packages[name] = all_deps
    except: pass

internal = set(packages.keys())

# DFS cycle detection
def find_cycles(graph, internal):
    cycles = []
    visited = set()
    path = []
    path_set = set()

    def dfs(node):
        if node in path_set:
            cycle_start = path.index(node)
            cycles.append(path[cycle_start:] + [node])
            return
        if node in visited:
            return
        visited.add(node)
        path.append(node)
        path_set.add(node)
        for dep in graph.get(node, set()):
            if dep in internal:
                dfs(dep)
        path.pop()
        path_set.discard(node)

    for node in graph:
        if node in internal:
            dfs(node)
    return cycles

cycles = find_cycles(packages, internal)
if cycles:
    print(f'⚠️  Found {len(cycles)} circular dependency chain(s):')
    for c in cycles:
        print(f'  {\" → \".join(c)}')
else:
    print('✅ No circular dependencies found')
" 2>/dev/null
```

### 4. `versions` — Version Consistency Check

Find cases where different packages specify different versions of the same external dependency.

```bash
python3 -c "
import json, glob
from collections import defaultdict

dep_versions = defaultdict(dict)

for pj in glob.glob('**/package.json', recursive=True):
    if 'node_modules' in pj: continue
    try:
        d = json.load(open(pj))
        name = d.get('name', pj)
        for dep_type in ['dependencies', 'devDependencies']:
            for dep, ver in d.get(dep_type, {}).items():
                dep_versions[dep][name] = ver
    except: pass

# Find inconsistencies
mismatches = {}
for dep, consumers in dep_versions.items():
    versions = set(consumers.values())
    if len(versions) > 1:
        mismatches[dep] = consumers

if mismatches:
    print(f'⚠️  Found {len(mismatches)} dependencies with version mismatches:')
    for dep, consumers in sorted(mismatches.items()):
        print(f'  {dep}:')
        for pkg, ver in sorted(consumers.items()):
            print(f'    {pkg}: {ver}')
else:
    print('✅ All shared dependencies use consistent versions')
" 2>/dev/null
```

### 5. `unused` — Find Unused Packages

Packages defined in the workspace but not depended on by any other package (and not the root app).

```bash
python3 -c "
import json, glob

packages = {}
all_internal_deps = set()

for pj in glob.glob('**/package.json', recursive=True):
    if 'node_modules' in pj: continue
    try:
        d = json.load(open(pj))
        name = d.get('name')
        if name:
            packages[name] = d
            for dt in ['dependencies', 'devDependencies', 'peerDependencies']:
                all_internal_deps.update(d.get(dt, {}).keys())
    except: pass

internal_names = set(packages.keys())
unused = internal_names - all_internal_deps

# Filter: packages with 'start' or 'serve' scripts are likely apps, not libraries
true_unused = []
for name in unused:
    scripts = packages[name].get('scripts', {})
    is_app = any(k in scripts for k in ['start', 'serve', 'dev'])
    if is_app:
        print(f'  {name} (app entry point — not counted as unused)')
    else:
        true_unused.append(name)

if true_unused:
    print(f'⚠️  {len(true_unused)} potentially unused packages:')
    for name in sorted(true_unused):
        print(f'  {name}')
else:
    print('✅ No unused packages found')
" 2>/dev/null
```

### 6. `build-order` — Compute Topological Build Order

```bash
python3 -c "
import json, glob
from collections import defaultdict, deque

packages = {}
for pj in glob.glob('**/package.json', recursive=True):
    if 'node_modules' in pj: continue
    try:
        d = json.load(open(pj))
        name = d.get('name')
        if name:
            deps = set(d.get('dependencies', {}).keys()) | set(d.get('devDependencies', {}).keys())
            packages[name] = deps
    except: pass

internal = set(packages.keys())

# Topological sort (Kahn's algorithm)
in_degree = defaultdict(int)
graph = defaultdict(list)
for name in internal:
    if name not in in_degree: in_degree[name] = 0
    for dep in packages.get(name, set()):
        if dep in internal:
            graph[dep].append(name)
            in_degree[name] += 1

queue = deque([n for n in internal if in_degree[n] == 0])
order = []
while queue:
    node = queue.popleft()
    order.append(node)
    for neighbor in graph[node]:
        in_degree[neighbor] -= 1
        if in_degree[neighbor] == 0:
            queue.append(neighbor)

if len(order) == len(internal):
    print('Build order (leaf dependencies first):')
    for i, name in enumerate(order, 1):
        print(f'  {i}. {name}')
else:
    print('⚠️  Cannot determine full build order — circular dependencies exist')
    print(f'  Ordered: {len(order)}/{len(internal)} packages')
" 2>/dev/null
```

### 7. `stats` — Monorepo Statistics

```bash
# Package count and sizes
echo "=== Package Stats ==="
find . -maxdepth 3 -name "package.json" -not -path '*/node_modules/*' 2>/dev/null | wc -l
echo "packages found"

# Lines of code per package
for pj in $(find . -maxdepth 3 -name "package.json" -not -path '*/node_modules/*' 2>/dev/null); do
  DIR=$(dirname "$pj")
  NAME=$(python3 -c "import json; print(json.load(open('$pj')).get('name','$DIR'))" 2>/dev/null)
  LOC=$(find "$DIR" -type f \( -name "*.ts" -o -name "*.js" -o -name "*.tsx" -o -name "*.jsx" \) \
    -not -path '*/node_modules/*' -not -path '*/dist/*' 2>/dev/null | xargs wc -l 2>/dev/null | tail -1 | awk '{print $1}')
  echo "  $NAME: ${LOC:-0} lines"
done

# Git activity per package (last 30 days)
echo "=== Recent Activity (30 days) ==="
for pj in $(find . -maxdepth 3 -name "package.json" -not -path '*/node_modules/*' 2>/dev/null); do
  DIR=$(dirname "$pj")
  NAME=$(python3 -c "import json; print(json.load(open('$pj')).get('name','$DIR'))" 2>/dev/null)
  COMMITS=$(git log --since="30 days ago" --oneline -- "$DIR" 2>/dev/null | wc -l)
  if [ "$COMMITS" -gt 0 ]; then
    echo "  $NAME: $COMMITS commits"
  fi
done
```

## Output Formats

- **text** (default): Human-readable report with sections
- **json**: Machine-readable `{tool, packages: [{name, path, deps, devDeps}], graph: {edges}, cycles: [], mismatches: {}, unused: []}`
- **markdown**: Wiki-ready document with Mermaid diagrams
- **mermaid**: Pure Mermaid dependency graph

## CI Integration

Exit codes:
- 0: No issues found
- 1: Circular dependencies detected
- 2: Version mismatches exceed threshold (default: 5)

```yaml
# GitHub Actions
- name: Check monorepo health
  run: |
    # Agent runs: monorepo-analyzer circular
    # Agent runs: monorepo-analyzer versions
    # Exits 1 if circular deps or too many mismatches
```

## Notes

- Supports JS/TS (npm/yarn/pnpm/lerna/nx/turbo), Rust (cargo), and Go (go.work) monorepos
- Does not install dependencies — works from config files only
- For very large monorepos (500+ packages), the full scan may take a minute
- Build order assumes no circular deps — run `circular` first
- Version consistency check covers external deps only — internal workspace deps use `workspace:*` protocol
