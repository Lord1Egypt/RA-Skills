---
report_schema: 1
skill_name: kai-export-ppt-lite
skill_version: 1.6.1
profile: kingdee-cloud-agent
validator_version: 1.0.0
generated_at: 2026-04-29T02:14:38.071287+00:00
total_score: 78
static_score: 86
realtime_score: 69
verdict: fail
block_count: 2
error_count: 0
warning_count: 0
content_hash: sha256:208a885408b6d37814d2a8aa6716f825734982599bdcfe29b7a23451ff5bc245
---
# Validate Report — `kai-export-ppt-lite` v1.6.1

## 总评

| 项 | 值 |
| --- | --- |
| **结论** | 🟥 Fail |
| **总分** | **78 / 100** (static 86 × 0.55 + realtime 69 × 0.45) |
| **档位** | 70-84 — conditional, fix required |
| **Block 命中** | 2 |
| **Error 命中** | 0 |
| **Warning 命中** | 0 |
| **Profile** | kingdee-cloud-agent |
| **Validator 版本** | 1.0.0 (rule set `sha256:e619686…`) |

## 9+1 维评分

| 维度 | 当前 | 满分 | Block / Error / Warning |
| --- | ---: | ---: | --- |
| V1 | 8 | 8 | 0 / 0 / 0 |
| V2 | 8 | 8 | 0 / 0 / 0 |
| V3 | 10 | 10 | 0 / 0 / 0 |
| V4 | 10 | 10 | 0 / 0 / 0 |
| V5 | 8 | 8 | 0 / 0 / 0 |
| V6 | 0 | 10 | 1 / 0 / 0 |
| V7 | 14 | 14 | 0 / 0 / 0 |
| V8 | 0 | 8 | 1 / 0 / 0 |
| V9 | 6 | 6 | 0 / 0 / 0 |
| V10 | 18 | 18 | 0 / 0 / 0 |

## Block / Error 详情（按修复优先级）

### #1 ⛔ R50  evals/ directory missing  [block]
- machine_id: `SCK-EVAL-50`
- 域: V6 · 层: static
- 信息: No evals directory; required eval categories are absent.
- 修复: Create evals/ with the 7 required case YAML files.

### #2 ⛔ R80  lockfile missing  [block]
- machine_id: `SCK-DEP-080`
- 域: V8 · 层: static
- 信息: scripts/ contains source but no requirements.lock / package-lock.json
- 修复: Generate `pip-compile --generate-hashes` or `npm ci`-compatible lockfile.


## Warning 列表

（无）

## Informational（未在 enforce 列表内）

| Rule | Severity | 文件 | 信息 |
| --- | --- | --- | --- |
| R2 | block | `SKILL.md` | description must include both: Do not use ... |
| R3 | block | `-` | skill.yaml not found at skill root |
| R13 | block | `-` | non-asset content is 62752.0 KB |
| R14 | error | `-` | - scripts/__pycache__/compare-html-ppt-visual.cpython-311.pyc
- scripts/__pycache__/export-sandbox-pptx.cpython-311.pyc
- scripts/__pycache__/rigorous-eval.cpython-311.pyc
- scripts/__pycache__/test-export.cpython-311.pyc
- scripts/__pycache__/compare-visual-comprehensive.cpython-311.pyc
- scripts/__pycache__/run-skill-export.cpython-311.pyc
- scripts/__pycache__/sync-slide-creator-contracts.cpython-311.pyc |
| R22 | error | `SKILL.md` | only 0 business terms detected (threshold ≥ 3) |
| R24 | block | `-` | missing: examples/when-to-use.md, examples/do-not-use.md |
| R51 | block | `-` | No evals directory; required eval categories are absent. |
| R52 | block | `-` | No evals directory; required eval categories are absent. |
| R53 | block | `-` | No evals directory; required eval categories are absent. |
| R54 | block | `-` | No evals directory; required eval categories are absent. |
| R55 | error | `-` | No evals directory; required eval categories are absent. |
| R56 | error | `-` | No evals directory; required eval categories are absent. |
| R73 | block | `scripts/_debug.py` | scripts/_debug.py: http://schemas.openxmlformats.org |
| R73 | block | `scripts/_debug.py` | scripts/_debug.py: http://schemas.openxmlformats.org |
| R73 | block | `scripts/_debug.py` | scripts/_debug.py: http://schemas.openxmlformats.org |
| R73 | block | `scripts/_debug.py` | scripts/_debug.py: http://schemas.openxmlformats.org |
| R73 | block | `scripts/_debug.py` | scripts/_debug.py: http://schemas.openxmlformats.org |
| R73 | block | `scripts/_debug.py` | scripts/_debug.py: http://schemas.openxmlformats.org |
| R73 | block | `scripts/_debug.py` | scripts/_debug.py: http://www.w3.org |
| R73 | block | `scripts/_debug.py` | scripts/_debug.py: http://schemas.openxmlformats.org |
| R73 | block | `scripts/_debug_export.py` | scripts/_debug_export.py: http://schemas.openxmlformats.org |
| R73 | block | `scripts/_debug_export.py` | scripts/_debug_export.py: http://schemas.openxmlformats.org |
| R73 | block | `scripts/_debug_export.py` | scripts/_debug_export.py: http://schemas.openxmlformats.org |
| R73 | block | `scripts/_debug_export.py` | scripts/_debug_export.py: http://schemas.openxmlformats.org |
| R73 | block | `scripts/_debug_export.py` | scripts/_debug_export.py: http://schemas.openxmlformats.org |
| R73 | block | `scripts/_debug_export.py` | scripts/_debug_export.py: http://schemas.openxmlformats.org |
| R73 | block | `scripts/_debug_export.py` | scripts/_debug_export.py: http://www.w3.org |
| R73 | block | `scripts/_debug_export.py` | scripts/_debug_export.py: http://schemas.openxmlformats.org |
| R73 | block | `scripts/compare-visual-comprehensive.py` | scripts/compare-visual-comprehensive.py: http://schemas.openxmlformats.org |
| R73 | block | `scripts/compare-visual-comprehensive.py` | scripts/compare-visual-comprehensive.py: http://schemas.openxmlformats.org |
| R73 | block | `scripts/export-sandbox-pptx.py` | scripts/export-sandbox-pptx.py: http://schemas.openxmlformats.org |
| R73 | block | `scripts/export-sandbox-pptx.py` | scripts/export-sandbox-pptx.py: http://schemas.openxmlformats.org |
| R73 | block | `scripts/export-sandbox-pptx.py` | scripts/export-sandbox-pptx.py: http://schemas.openxmlformats.org |
| R73 | block | `scripts/export-sandbox-pptx.py` | scripts/export-sandbox-pptx.py: http://schemas.openxmlformats.org |
| R73 | block | `scripts/export-sandbox-pptx.py` | scripts/export-sandbox-pptx.py: http://schemas.openxmlformats.org |
| R73 | block | `scripts/export-sandbox-pptx.py` | scripts/export-sandbox-pptx.py: http://schemas.openxmlformats.org |
| R73 | block | `scripts/export-sandbox-pptx.py` | scripts/export-sandbox-pptx.py: http://www.w3.org |
| R73 | block | `scripts/export-sandbox-pptx.py` | scripts/export-sandbox-pptx.py: http://schemas.openxmlformats.org |
| R73 | block | `scripts/export-sandbox-pptx.py.bak` | scripts/export-sandbox-pptx.py.bak: http://schemas.openxmlformats.org |
| R73 | block | `scripts/export-sandbox-pptx.py.bak` | scripts/export-sandbox-pptx.py.bak: http://schemas.openxmlformats.org |
| R73 | block | `scripts/export-sandbox-pptx.py.bak` | scripts/export-sandbox-pptx.py.bak: http://schemas.openxmlformats.org |
| R73 | block | `scripts/export-sandbox-pptx.py.bak` | scripts/export-sandbox-pptx.py.bak: http://schemas.openxmlformats.org |
| R73 | block | `scripts/export-sandbox-pptx.py.bak` | scripts/export-sandbox-pptx.py.bak: http://schemas.openxmlformats.org |
| R73 | block | `scripts/export-sandbox-pptx.py.bak` | scripts/export-sandbox-pptx.py.bak: http://schemas.openxmlformats.org |
| R73 | block | `scripts/export-sandbox-pptx.py.bak` | scripts/export-sandbox-pptx.py.bak: http://www.w3.org |
| R73 | block | `scripts/export-sandbox-pptx.py.bak` | scripts/export-sandbox-pptx.py.bak: http://schemas.openxmlformats.org |
| R73 | block | `scripts/test-export.py` | scripts/test-export.py: https://example.com |
| R73 | block | `scripts/test-export.py` | scripts/test-export.py: https://example.com |
| R73 | block | `scripts/test-export.py` | scripts/test-export.py: https://github.com |
| R73 | block | `scripts/test-export.py` | scripts/test-export.py: https://github.com |
| R73 | block | `scripts/test-export.py` | scripts/test-export.py: https://github.com |
| R75 | block | `scripts/compare-html-ppt-visual.py` | scripts/compare-html-ppt-visual.py: subprocess.run( |
| R75 | block | `scripts/export-sandbox-pptx.py` | scripts/export-sandbox-pptx.py: subprocess.run( |
| R75 | block | `scripts/rigorous-eval.py` | scripts/rigorous-eval.py: subprocess.run( |
| R75 | block | `scripts/sync-slide-creator-contracts.py` | scripts/sync-slide-creator-contracts.py: subprocess.run( |

## Freshness（实时层依赖快照）

（实时层未跑或无外部依赖）

## Sign-off

```
Generated by lingee-skill-creator 1.0.0
Generated at 2026-04-29T02:14:38.071287+00:00
Rule set hash: sha256:e619686b3ea02349ea6dfb8a8e8c9601
Report content hash: sha256:208a885408b6d37814d2a8aa6716f825734982599bdcfe29b7a23451ff5bc245
Spec compliance: report_schema 1
```
