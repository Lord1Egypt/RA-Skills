# Language Pair Template: SOURCE → TARGET

> Copy this file to `references/lang-pairs/source-target.md` and fill in all sections.
> This module is loaded during P0 Bootstrap and stays in context for all subsequent phases.

---

## Paradigm Difference Classification

**Difficulty tier**: [ ] Similar (Java→Kotlin) | [ ] Moderate (Python→Go) | [ ] High (Python→Rust) | [ ] Extreme (Python→Haskell)

**Key differences**:
- Memory model: SOURCE uses ___ / TARGET uses ___
- Type system: SOURCE is ___ / TARGET is ___
- Concurrency model: SOURCE uses ___ / TARGET uses ___
- Error handling: SOURCE uses ___ / TARGET uses ___
- OOP model: SOURCE is ___ / TARGET is ___

---

## Pre-Mapped Ecosystem Symbols

### Core Types

| Source Type | Target Type | Equivalence | Notes |
|---|---|---|---|
| | | | |

### Standard Library

| Source Module.Symbol | Target Equivalent | Equivalence | Package | Notes |
|---|---|---|---|---|
| | | | | |

### Common Third-Party Libraries

| Source Package | Target Package | Equivalence | Notes |
|---|---|---|---|
| | | | |

---

## Known Translation Patterns

### Pattern 1: [Name]

**Source:**
```
(source language snippet)
```

**Target:**
```
(target language snippet)
```

**Notes:** Why this pattern is the correct structural equivalent.

---

## Known Anti-Patterns (Do NOT Do These)

| Wrong approach | Why wrong | Correct approach |
|---|---|---|
| | | |

---

## Ecosystem Gaps (Require Compensation)

| Source feature | Gap description | Compensation strategy |
|---|---|---|
| | | |

---

## Memory / Ownership Migration Notes

(Describe the key difference in memory model and how to adapt idioms)

---

## Error Handling Migration

| Source pattern | Target pattern | Notes |
|---|---|---|
| | | |

---

## Concurrency Migration

(Describe how to translate concurrent patterns)

---

## Testing Toolchain

| Source tool | Target equivalent | Config notes |
|---|---|---|
| pytest | | |
| mypy / type checker | | |
| linter | | |
| formatter | | |

---

## Build System Migration

| Source config | Target config | Notes |
|---|---|---|
| | | |

---

## CI Adaptation

Replace in `.github/workflows/` or equivalent:
```yaml
# Source:
run: <source build/test command>

# Target:
run: <target build/test command>
```
