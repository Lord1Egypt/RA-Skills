<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-21 | Updated: 2026-04-21 -->

# evals

## Purpose
Evaluation test cases for validating the skill's Q&A accuracy, citation quality, and safety boundaries. Contains structured test prompts with expected outputs and assertions.

## Key Files
| File | Description |
|------|-------------|
| `evals.json` | 12 test cases covering academic Q&A, clinical reasoning, safety boundaries, and citation requirements |

## For AI Agents

### Working In This Directory
- Test cases validate skill behavior - do not modify expected outputs casually
- Add new test cases when extending skill capabilities
- Run evaluation after any changes to `../scripts/ask.py` or `../SKILL.md`

### Test Case Categories
| Category | Count | Purpose |
|----------|-------|---------|
| 学术问答 | 3 | Academic Q&A on constitution theory |
| 临床思路学习 | 1 | Clinical reasoning and treatment approaches |
| 理论体系梳理 | 1 | Theoretical framework understanding |
| 方药知识查询 | 1 | Formula and herb knowledge |
| 安全边界测试 | 2 | Safety boundary enforcement (no prescriptions) |
| 证据溯源测试 | 1 | Citation and evidence tracing |
| 不确定回答测试 | 1 | Proper handling of unknown topics |
| 综合对比 | 1 | Comparative analysis |
| 证据层级区分测试 | 1 | Evidence level differentiation |

### Assertion Types
| Type | Description | Example |
|------|-------------|---------|
| `contains` | Response must contain text | `{"type": "contains", "value": "痰湿质"}` |
| `not_contains` | Response must not contain text | `{"type": "not_contains", "value": "处方"}` |
| `contains_any` | Response must contain one of list | `{"type": "contains_any", "value": ["玉屏风散", "过敏煎"]}` |
| `contains_all` | Response must contain all items | `{"type": "contains_all", "value": ["黄芪", "白术", "防风"]}` |
| `regex` | Response must match pattern | `{"type": "regex", "value": "\\[论文\\]|\\[诊疗经验\\]"}` |
| `not_regex` | Response must not match pattern | `{"type": "not_regex", "value": "建议.*[克g]"}` |
| `count_contains` | Count of occurrences | `{"type": "count_contains", "value": "质", "min_count": 9}` |

### Testing Requirements
- Run all test cases against current skill implementation
- Check assertion pass rate
- Review failures for skill improvement opportunities

## Dependencies

### Internal
- `../SKILL.md` - Skill definition being tested
- `../scripts/ask.py` - Q&A implementation being tested

### External
- None (test data only)

<!-- MANUAL: -->
