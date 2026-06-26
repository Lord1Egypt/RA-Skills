# Quality Framework

## 6 Quality Dimensions

### 1. Frontmatter Quality (35%)

**Weight:** 35% (highest)

**Checks:**
- ✓ Has name/title field
- ✓ Description adequate (>20 chars, ideally 50-150)
- ✓ Has trigger phrase ("Use when...")

**Scoring:**
| Check | Points |
|-------|--------|
| Name present | 30 |
| Description good | 40 |
| Trigger present | 30 |

---

### 2. Orchestration Wiring (25%)

**Weight:** 25%

**Checks:**
- ✓ Documents input (what the skill needs)
- ✓ Documents output (what it produces)
- ✓ Has code examples

**Scoring:**
| Check | Points |
|-------|--------|
| Input documented | 35 |
| Output documented | 35 |
| Examples present | 30 |

---

### 3. Progressive Disclosure (15%)

**Weight:** 15%

**Checks:**
- ✓ Skill concise (<400 lines)
- ✓ Uses references/ for details
- ✓ Layered information

**Scoring:**
| Size | Score |
|------|-------|
| <200 lines | 100 |
| 200-400 lines | 90 |
| 400-800 lines | 70 |
| >800 lines | 50 |

---

### 4. Structural Completeness (10%)

**Weight:** 10%

**Checks:**
- ✓ Good heading structure (H2/H3 hierarchy)
- ✓ Has code examples
- ✓ Has examples section

**Scoring:**
| Check | Points |
|-------|--------|
| Headings good | 40 |
| Code examples | 30 |
| Examples section | 30 |

---

### 5. Token Efficiency (6%)

**Weight:** 6%

**Checks:**
- ✓ Appropriate directive count (<15 MUST/ALWAYS/NEVER)
- ✓ Minimal duplication

**Scoring:**
| Factor | Impact |
|--------|--------|
| >15 directives | -10% |
| High duplication | -10% |

---

### 6. Ecosystem Coherence (2%)

**Weight:** 2%

**Checks:**
- ✓ Has cross-references to related skills
- ✓ Links to documentation

---

## Final Score Calculation

```
weighted_score = (dim1 * 0.35) + (dim2 * 0.25) + (dim3 * 0.15) + 
                 (dim4 * 0.10) + (dim5 * 0.06) + (dim6 * 0.02)

final_score = weighted_score * penalty
```

**Penalty:** Applied for anti-patterns (see anti-pattern-catalog.md)
