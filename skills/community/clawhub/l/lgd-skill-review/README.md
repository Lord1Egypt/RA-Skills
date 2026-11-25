# lgd-skill-review

**A reviewer whose verdicts can be appealed.**

Most skill reviewers hand you a score and stop. This one hands you a score, tells you which line of which file produced it, and lets you bring evidence to overturn it.

---

## What makes it different

| | Typical reviewer | This one |
|---|---|---|
| Verdict | one number | **two orthogonal numbers** — structure (100) and semantics (120), never merged |
| Disagreement | hidden inside one score | **flagged** when the two rulers diverge by ≥20 points |
| Findings | "missing tests" | **`SKILL.md:18 declared --draft, script has no such flag`** — every finding points at a file and a line |
| Challenge | none | **`--appeal`** — you supply a path and a check, the engine opens it and rules |
| Ruling | — | written to `appeal_log.json`, publicly auditable |
| Score change from appeal | — | **never.** An appeal overturns the *basis*, not the *number* |

### Why appeals never change the score

Because a reviewer that raises its own score when challenged has stopped being a reviewer. The appeal turns a deduction into a **verifiable dispute** — the appellant must produce something the engine can open and read. If the basis really was wrong, the next run shows it. If not, the ruling stands and is on record.

## What a review looks like

See a real, unedited run against a third-party package: [`docs/sample-report.md`](docs/sample-report.md) — dual verdict, every finding with a semantic key and a place, and the scope note that keeps the score from being over-read.

一次真实评测的完整输出见 [`docs/sample-report.md`](docs/sample-report.md)。

## Quick start

```bash
python scripts/review.py path/to/skill              # dual verdict + fix list
python scripts/review.py path/to/skill --run        # also execute the test runner
python scripts/review.py path/to/skill --eight      # show the 120-point breakdown
python scripts/review.py path/to/skill --appeal appeal.json
```

Zero dependency. Standard library only. Offline.

### Filing an appeal

```json
{
  "items": [
    {
      "id": "reproducible:no-runner",
      "claim": "the test runner exists; its name is outside the recognizer's pattern",
      "path": "tests/test_runner.py",
      "expect": "file_exists"
    }
  ]
}
```

`id` takes either a per-report number (`R03`) or a **semantic key** (`reproducible:no-runner`). Semantic keys are stable across reports — use them. `expect` accepts `file_exists`, `contains:<text>`, `regex:<pattern>`. The engine rules **OVERTURNED**, **UPHELD** or **UNKNOWN_ID**, and appends the ruling to `appeal_log.json`.

Read the full rules: [`references/appeal.md`](references/appeal.md).

### File an appeal

Use the issue form — it asks for exactly two things, a path and a check:

`https://github.com/zhaoxinghua09-cell/lgd-skill-review/issues/new?template=appeal.yml`

If you cannot name a path the engine can open, that is a rule discussion, not an appeal — open a plain issue instead.

提交申诉请用 Issue 表单，它只问两件事：一个路径、一个核验方式。指不出路径的属于规则讨论，另开普通 issue。

### How an appeal gets handled

```bash
python scripts/handle_appeal.py path/to/skill appeal.json
```

It prints a ready-to-paste ruling — a table of every claim with its verdict and reason, plus what to do next. Same engine, same rules as `--appeal`, just formatted for replying in an issue thread. The ruling is appended to `appeal_log.json`; identical re-runs do not create duplicate log entries.

接受申诉的一方用这一条命令即可回帖，不需要手工整理。

## Measured, not claimed

Same ruler, eleven packages, all scored by this code (competitors installed from ClawHub, not from their landing pages):

| Package | Structure | Semantics |
|---|---|---|
| lgd-skill-review 1.1.8 | **100** | **116** |
| summarize-pro 2.0.7 | **100** | 115 |
| debug-pro 2.1.4 | **100** | 115 |
| wechat-viral-topic 2.1.4 | **100** | 113 |
| cue-skill-review-cn 0.1.4 | 61 | 84 |
| skill-review-pro 2.3.1 | 54 | 88 |
| meeting-decision-receipt 1.0.1 | 40 | 91 |
| skill-evaluator 1.0.0 | 37 | 75 |
| skill-trust-auditor 1.1.5 | 33 | 71 |

Seven competitors were source-grepped for appeal capability (`appeal` / `overturn` / `reconsider` / 申诉 / 复核): **zero hits**. The only "appeal" match was the phrase *broad appeal*, describing attack surface.

### The limit of this ruler, stated plainly

Structure measures **whether a package can be verified and delivered** — tests exist, documented commands actually exist in the script, a rerun reproduces the result, nothing leaks, an agent can find it, licensing is present.

It does **not** measure how much industry judgment the package carries. skill-review-pro ships 43 KB of policy documents that this ruler cannot see. Its 54 means "hard to verify", not "bad". Under a ruler that measured judgment depth, the ranking would likely flip. Semantics is a heuristic, not an LLM judgment.

## Rejected a score? Do this

1. Look at the fix list. Every item has an ID (`R01`, `R02`…) and, where locatable, a `file:line` anchor.
2. Check whether the basis is actually wrong. If it is, write the appeal JSON above and run with `--appeal`.
3. If the appeal is overturned, rerun. The number will move only if the basis is genuinely gone.

Found a defect in the reviewer itself? That counts too — the current runner-recognition rule (`run_*.py` / `test_*.py` / `*_test.py`) exists because an appeal exposed it.

## Layout

```
SKILL.md                      the skill contract
scripts/review.py             the engine (single file, no deps)
references/appeal.md          appeal rules
references/scoring.md         how the six dimensions are scored
references/faq.md             five times this reviewer was itself overturned
tests/run_golden.py           self-check (5 cases)
demo/run_demo.py              a deliberately bad package, 16 → 100
```

## License

MIT.

---

# 技能评测官

**一个结论可以被反驳的评测器。**

多数评测器给你一个分就结束了。这个会告诉你这个分来自哪个文件的哪一行，并且允许你带着证据来推翻它。

## 和别人不一样的地方

- **双制判分**：结构制 100（能不能用）+ 语义制 120（值不值得用），两个正交结论，**绝不加权成一个数**；两者背离 ≥20 分时会明确标出。
- **每条发现挂原文**：不是"缺少测试"，而是 `SKILL.md:18 声明了未实现的参数 --draft`——指到文件和行号。
- **可以申诉**：给出文件路径与核验方式，引擎自己去打开、自己匹配，裁决「推翻 / 维持」，并写进公开的 `appeal_log.json`。
- **申诉不改分**：推翻的是依据，不是分数。会因申诉自动加分的评测器，分数立刻贬值。

## 快速开始

```bash
python scripts/review.py 包目录              # 双制结论 + 整改清单
python scripts/review.py 包目录 --run        # 额外实跑测试执行器
python scripts/review.py 包目录 --eight      # 看 120 分制明细
python scripts/review.py 包目录 --appeal 申诉.json
```

零依赖，只用标准库，离线可跑。

## 被打了低分怎么办

整改清单里每条都有 ID（`R01`、`R02`…），能定位的会附 `文件:行号`。如果你认为某条依据不成立，写一份申诉 JSON（见 `references/appeal.md`），带 `path` 和 `expect`，用 `--appeal` 跑一次。

裁决推翻了就复测——分数只有在依据确实消失时才会变。

**发现评测器自己判错了，也算一种申诉。** 现在的测试执行器识别规则（`run_*.py` / `test_*.py` / `*_test.py`）就是被一条申诉逼出来的。

## 这把尺子不量什么

结构制量的是「能不能被验证地交付」：有没有测试、文档承诺的命令脚本里到底有没有、能不能复跑、有没有泄露、AI 能否发现、许可是否齐。

**它不量策略厚度。** skill-review-pro 有 43 KB 九份策略文档，这把尺子看不见——它 54 分不代表它做得差，只代表它不好验证。换成量「判断深度」的尺子，排序很可能翻转。语义制是启发式评分，不含 LLM 复核。

## 许可

MIT。

## 自证

- 已知偏差：加 `--run` 复跑时会真正执行 5 个黄金用例，它们被判为薄用例，总分扣四分。这是尺子对自己偏严，不是包有问题。

- 自检 5/5 PASS（python tests/run_golden.py）
- 结构制 100/100 PASS（python scripts/review.py <包>）


## 取代关系

本包取代此前分散的三个闸门包（skill-quality-gate / skill-admission-gate / skill-release-gate）。
四关判据（分数 / 数字 / 反作弊 / 规格）现在只在这里维护一处；
那三个包已标注退役，仅作为已安装用户的入口保留。

一条命令看它做什么：python demo/run_demo.py（造坏包 → 17 项整改 → 复测通过）。

