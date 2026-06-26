---
report_schema: 1
skill_name: kai-business-blueprint
skill_version: 0.0.0
profile: kingdee-cloud-agent
validator_version: 1.0.0
generated_at: 2026-04-29T00:44:13.700759+00:00
total_score: 75
static_score: 80
realtime_score: 69
verdict: fail
block_count: 2
error_count: 0
warning_count: 5
content_hash: sha256:3934ccf824bfbcf9e0b8ab2914a135382bac5555bf902c9116b695fe653c0073
---
# Validate Report — `kai-business-blueprint` v0.0.0

## 总评

| 项 | 值 |
| --- | --- |
| **结论** | 🟥 Fail |
| **总分** | **75 / 100** (static 80 × 0.55 + realtime 69 × 0.45) |
| **档位** | 70-84 — conditional, fix required |
| **Block 命中** | 2 |
| **Error 命中** | 0 |
| **Warning 命中** | 5 |
| **Profile** | kingdee-cloud-agent |
| **Validator 版本** | 1.0.0 (rule set `sha256:e619686…`) |

## 9+1 维评分

| 维度 | 当前 | 满分 | Block / Error / Warning |
| --- | ---: | ---: | --- |
| V1 | 8 | 8 | 0 / 0 / 0 |
| V2 | 3 | 8 | 0 / 0 / 5 |
| V3 | 10 | 10 | 0 / 0 / 0 |
| V4 | 10 | 10 | 0 / 0 / 0 |
| V5 | 8 | 8 | 0 / 0 / 0 |
| V6 | 0 | 10 | 1 / 0 / 0 |
| V7 | 14 | 14 | 0 / 0 / 0 |
| V8 | 0 | 8 | 1 / 0 / 0 |
| V9 | 6 | 6 | 0 / 0 / 0 |
| V10 | 18 | 18 | 0 / 0 / 0 |

## Block / Error 详情（按修复优先级）

### #1 ⛔ R50  insufficient golden cases  [block]
- machine_id: `SCK-EVAL-50`
- 域: V6 · 层: static
- 位置: `evals/golden_cases.yaml`
- 信息: found 0, need ≥ 10

### #2 ⛔ R80  lockfile missing  [block]
- machine_id: `SCK-DEP-080`
- 域: V8 · 层: static
- 信息: scripts/ contains source but no requirements.lock / package-lock.json
- 修复: Generate `pip-compile --generate-hashes` or `npm ci`-compatible lockfile.


## Warning 列表

| # | Rule | 文件 | 信息 |
| --- | --- | --- | --- |
| 1 | R12 | `references/domain-knowledge-design-adversarial-review.md` | references/domain-knowledge-design-adversarial-review.md: 22.4KB |
| 2 | R12 | `references/domain-knowledge-entities-extension-design.md` | references/domain-knowledge-entities-extension-design.md: 46.3KB |
| 3 | R12 | `references/schema-refactor-v2-actionable.md` | references/schema-refactor-v2-actionable.md: 28.4KB |
| 4 | R12 | `references/test-and-eval-strategy.md` | references/test-and-eval-strategy.md: 34.1KB |
| 5 | R16 | `-` | - references/architecture-diagram-design.md
- references/authoring-rules.md
- references/blueprint-schema.md
- references/blueprint-skill-optimization-proposal.md
- references/domain-knowledge-design-adversarial-review.md
- references/domain-knowledge-entities-extension-design.md
- references/implementation-plan.md
- references/industry-packs.md
- references/layout-quality-check.md
- references/prompt-orchestration-templates.md
- references/schema-refactor-proposal.md
- references/schema-refactor-v2-actionable.md
- references/test-and-eval-strategy.md
- references/theme-dark.md
- references/visual-enhancement-plan.md |

## Informational（未在 enforce 列表内）

| Rule | Severity | 文件 | 信息 |
| --- | --- | --- | --- |
| R2 | block | `SKILL.md` | description must include both: Do not use ... |
| R3 | block | `-` | skill.yaml not found at skill root |
| R5 | block | `SKILL.md` | frontmatter name 'kai-business-blueprint' != directory 'business-blueprint-skill' |
| R13 | error | `-` | non-asset content is 2673.3 KB |
| R13b | error | `-` | estimated 47670 tokens — too large for 200k-context budget hygiene |
| R14 | error | `-` | - scripts/tests/__pycache__/test_theme_and_cards.cpython-311-pytest-8.3.5.pyc
- scripts/tests/__pycache__/test_cli_cross_platform.cpython-311-pytest-8.3.5.pyc
- scripts/tests/__pycache__/test_export_integrity.cpython-311-pytest-8.3.5.pyc
- scripts/tests/__pycache__/test_prompt_generation.cpython-311-pytest-8.3.5.pyc
- scripts/tests/__pycache__/test_validate.cpython-311-pytest-8.3.5.pyc
- scripts/tests/__pycache__/test_svg_quality.cpython-311-pytest-8.3.5.pyc
- scripts/tests/__pycache__/test_exporters.cpython-311-pytest-8.3.5.pyc
- scripts/tests/__pycache__/test_cli_smoke.cpython-311-pytest-8.3.5.pyc
- scripts/tests/__pycache__/test_e2e.cpython-311-pytest-8.3.5.pyc
- scripts/tests/__pycache__/test_export_routes.cpython-311-pytest-8.3.5.pyc |
| R22 | error | `SKILL.md` | only 0 business terms detected (threshold ≥ 3) |
| R24 | block | `-` | missing: examples/when-to-use.md, examples/do-not-use.md |
| R32 | error | `-` | UnicodeDecodeError: 'utf-8' codec can't decode byte 0x87 in position 23: invalid start byte |
| R40 | error | `-` | references directory has files but no INDEX.md |
| R51 | block | `evals/exception_cases.yaml` | found 0, need ≥ 5 |
| R52 | block | `evals/permission_cases.yaml` | found 0, need ≥ 3 |
| R53 | block | `evals/adversarial_cases.yaml` | found 0, need ≥ 3 |
| R54 | block | `evals/tool_failure_cases.yaml` | found 0, need ≥ 3 |
| R55 | error | `evals/context_bloat_cases.yaml` | found 0, need ≥ 1 |
| R56 | error | `evals/multi_skill_cases.yaml` | found 0, need ≥ 1 |
| R73 | block | `scripts/business_blueprint/export_svg.py` | scripts/business_blueprint/export_svg.py: http://www.w3.org |
| R73 | block | `scripts/business_blueprint/export_svg.py` | scripts/business_blueprint/export_svg.py: http://www.w3.org |
| R73 | block | `scripts/business_blueprint/export_svg.py` | scripts/business_blueprint/export_svg.py: http://www.w3.org |
| R73 | block | `scripts/business_blueprint/export_svg.py` | scripts/business_blueprint/export_svg.py: http://www.w3.org |
| R73 | block | `scripts/business_blueprint/export_svg.py` | scripts/business_blueprint/export_svg.py: http://www.w3.org |
| R73 | block | `scripts/business_blueprint/export_svg.py` | scripts/business_blueprint/export_svg.py: http://www.w3.org |
| R73 | block | `scripts/business_blueprint/export_svg.py` | scripts/business_blueprint/export_svg.py: http://www.w3.org |
| R73 | block | `scripts/business_blueprint/export_svg.py` | scripts/business_blueprint/export_svg.py: http://www.w3.org |
| R73 | block | `scripts/business_blueprint/export_svg.py` | scripts/business_blueprint/export_svg.py: http://www.w3.org |
| R73 | block | `scripts/business_blueprint/export_svg.py` | scripts/business_blueprint/export_svg.py: http://www.w3.org |
| R73 | block | `scripts/business_blueprint/export_svg.py` | scripts/business_blueprint/export_svg.py: http://www.w3.org |
| R73 | block | `scripts/business_blueprint/export_svg.py` | scripts/business_blueprint/export_svg.py: http://www.w3.org |
| R73 | block | `scripts/business_blueprint/export_svg.py` | scripts/business_blueprint/export_svg.py: http://www.w3.org |
| R73 | block | `scripts/business_blueprint/fixtures/baseline/common.svg` | scripts/business_blueprint/fixtures/baseline/common.svg: http://www.w3.org |
| R73 | block | `scripts/business_blueprint/fixtures/baseline/finance.svg` | scripts/business_blueprint/fixtures/baseline/finance.svg: http://www.w3.org |
| R73 | block | `scripts/business_blueprint/fixtures/baseline/manufacturing.svg` | scripts/business_blueprint/fixtures/baseline/manufacturing.svg: http://www.w3.org |
| R73 | block | `scripts/business_blueprint/fixtures/baseline/retail.svg` | scripts/business_blueprint/fixtures/baseline/retail.svg: http://www.w3.org |
| R73 | block | `scripts/business_blueprint/renderers.py` | scripts/business_blueprint/renderers.py: http://www.w3.org |
| R73 | block | `scripts/tests/test_export_integrity.py` | scripts/tests/test_export_integrity.py: http://www.w3.org |
| R73 | block | `scripts/tests/test_export_integrity.py` | scripts/tests/test_export_integrity.py: http://www.w3.org |
| R73 | block | `scripts/tests/test_export_integrity.py` | scripts/tests/test_export_integrity.py: http://www.w3.org |
| R73 | block | `scripts/tests/test_export_integrity.py` | scripts/tests/test_export_integrity.py: http://www.w3.org |
| R73 | block | `scripts/tests/test_export_integrity.py` | scripts/tests/test_export_integrity.py: http://www.w3.org |
| R73 | block | `scripts/tests/test_export_integrity.py` | scripts/tests/test_export_integrity.py: http://www.w3.org |
| R73 | block | `scripts/tests/test_exporters.py` | scripts/tests/test_exporters.py: http://www.w3.org |
| R73 | block | `scripts/tests/test_visual_enhancement.py` | scripts/tests/test_visual_enhancement.py: https://fonts |
| R73 | block | `scripts/tests/test_visual_enhancement.py` | scripts/tests/test_visual_enhancement.py: https://fonts |
| R75 | block | `scripts/business_blueprint/tests/test_utils.py` | scripts/business_blueprint/tests/test_utils.py: subprocess.run( |
| R75 | block | `scripts/tests/test_cli_cross_platform.py` | scripts/tests/test_cli_cross_platform.py: subprocess.run( |
| R75 | block | `scripts/tests/test_cli_smoke.py` | scripts/tests/test_cli_smoke.py: subprocess.run( |
| R75 | block | `scripts/tests/test_e2e.py` | scripts/tests/test_e2e.py: subprocess.run( |
| R75 | block | `scripts/tests/test_generate.py` | scripts/tests/test_generate.py: subprocess.run( |
| R75 | block | `scripts/tests/test_theme_and_cards.py` | scripts/tests/test_theme_and_cards.py: subprocess.run( |
| R75 | block | `scripts/tests/test_visual_enhancement.py` | scripts/tests/test_visual_enhancement.py: subprocess.run( |

## Freshness（实时层依赖快照）

（实时层未跑或无外部依赖）

## Sign-off

```
Generated by lingee-skill-creator 1.0.0
Generated at 2026-04-29T00:44:13.700759+00:00
Rule set hash: sha256:e619686b3ea02349ea6dfb8a8e8c9601
Report content hash: sha256:3934ccf824bfbcf9e0b8ab2914a135382bac5555bf902c9116b695fe653c0073
Spec compliance: report_schema 1
```
