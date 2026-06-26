# Scan Project

Systematically analyze an existing codebase for spec recovery.

## Inputs

| Input | Source |
|-------|--------|
| Project root | `.platonic.yml` or user-provided |
| Language | `.platonic.yml` or auto-detected |
| Framework | `.platonic.yml` or auto-detected |

## Scan Phases (5 phases, in order)

### Phase 1: Project Discovery
Read README, build files, existing docs. Extract: purpose, language, framework, dependencies, entry points, directory structure.

**Build files**: `Cargo.toml` (Rust), `package.json` (JS/TS), `pyproject.toml` (Python), `go.mod` (Go), `pom.xml`/`build.gradle` (Java).

**Output**: Project metadata.

### Phase 2: Structural Analysis
Identify modules, build dependency graph, detect layers (foundation/middle/leaf), find config patterns.

**Output**: Module list with dependency graph, layer classification.

### Phase 3: Type and Interface Analysis
Catalog public types (structs, enums, type aliases) and interfaces (traits, exported functions, public methods). Focus on cross-module boundaries. Extract naming conventions.

**Output**: Type catalog, interface catalog, shared types, naming conventions.

### Phase 4: Behavioral Analysis
Trace data flow from entry points. Extract invariants (assertions, validation, immutability). Identify design patterns (repository, factory, observer, pipeline, strategy, middleware). Note error handling.

**Output**: Data flows, invariants, patterns, error handling.

### Phase 5: Synthesis
Group findings into conceptual clusters. Identify subsystem boundaries and API surfaces. Prepare summary: system overview, subsystems, patterns, data flows, terminology. **Present to user for validation**.

## Scan Guidelines

- Focus on public API surfaces, not implementation details
- Read module entry points (lib.rs, index.ts, __init__.py)
- Skim implementation files for patterns
- Prioritize cross-module interactions
- Time-box: thorough but not exhaustive

## Output

In-memory scan synthesis ready for `init-plan-modular-specs`.
