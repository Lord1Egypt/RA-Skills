# MAGI Decision Matrix Templates

## Purpose

Transform ambiguous strategic decisions into quantifiable, traceable structured evaluations. Supports both single-option feasibility validation and multi-optionside-by-side comparison.

## 1. Single-Option Evaluation Matrix

### Template Structure

| Dimension | Weight | Score (1-10) | Weighted Score | Source | Notes |
|-----------|--------|-------------|---------------|--------|-------|
| Revenue Potential | 0.15 | | | MELCHIOR | |
| Data Support | 0.10 | | | MELCHIOR | |
| Logical Feasibility | 0.10 | | | MELCHIOR | |
| Risk Controllability | 0.15 | | | BALTHASAR | |
| Ethical Compliance | 0.10 | | | BALTHASAR | |
| Long-term Safety | 0.10 | | | BALTHASAR | |
| Timing Alignment | 0.10 | | | CASPER | |
| Team Acceptance | 0.10 | | | CASPER | |
| Trend Fit | 0.10 | | | CASPER | |
| **Total** | **1.00** | — | **___** | — | — |

### Verdict Rules

| Weighted Score | Verdict | Action |
|---------------|---------|--------|
| >= 8.0 | Strongly recommend | Proceed immediately, allocate resources |
| 6.5 - 7.9 | Conditionally recommend | Proceed after addressing weaknesses |
| 5.0 - 6.4 | Redesign needed | Core assumptions require validation |
| < 5.0 | Not recommended | Suspend or abandon |

## 2. Multi-Option Comparison Matrix

### Template Structure

| Evaluation Dimension | Weight | Option A | Option B | Option C |
|---------------------|--------|----------|----------|----------|
| **MELCHIOR (Rational)** | | | | |
| Revenue Potential | 0.15 | /10 | /10 | /10 |
| Data Support | 0.10 | /10 | /10 | /10 |
| Logical Feasibility | 0.10 | /10 | /10 | /10 |
| MELCHIOR Subtotal | 0.35 | __/10 | __/10 | __/10 |
| **BALTHASAR (Prudent)** | | | | |
| Risk Controllability | 0.15 | /10 | /10 | /10 |
| Ethical Compliance | 0.10 | /10 | /10 | /10 |
| Long-term Safety | 0.10 | /10 | /10 | /10 |
| BALTHASAR Subtotal | 0.35 | __/10 | __/10 | __/10 |
| **CASPER (Intuitive)** | | | | |
| Timing Alignment | 0.10 | /10 | /10 | /10 |
| Team Acceptance | 0.10 | /10 | /10 | /10 |
| Trend Fit | 0.10 | /10 | /10 | /10 |
| CASPER Subtotal | 0.30 | __/10 | __/10 | __/10 |
| **Weighted Total** | **1.00** | **__** | **__** | **__** |
| **Vote Result** | — | recommend/conditional/not | recommend/conditional/not | recommend/conditional/not |

### Comparison Rules

1. Sort by weighted total score descending
2. If the top-scoring option scores < 4 in any dimension, flag as "critical weakness"
3. If top three scores differ by < 0.5, recommend gathering more information
4. Final recommendation requires: highest total + no critical weaknesses + at least 2 votes in favor

## 3. Veto Checklist

The following conditions trigger automatic rejection regardless of total score:

- Irreversible legal or compliance risk exists
- Worst-case scenario exceeds organizational tolerance threshold
- Core assumptions unverified and verification cost is prohibitively high
- Key stakeholders explicitly oppose and positions cannot be reconciled
- Time window has closed or resource gap cannot be bridged

## 4. Filling Guidelines

1. **Scoring Standards**: 1-3 = Poor, 4-6 = Moderate, 7-10 = Excellent
2. **Weight Adjustment**: Default weights suit most scenarios; increase BALTHASAR to 0.45 for high-risk scenarios; increase CASPER to 0.35 for innovation-driven scenarios
3. **Source Attribution**: Each dimension score must be attributed to a specific persona for traceability
4. **Discrepancy Recording**: If three personas differ by > 3 points on the same dimension, record the reason in the notes column
