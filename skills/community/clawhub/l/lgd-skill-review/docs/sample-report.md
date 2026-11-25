# Sample report — what a review actually looks like

This is a real, unedited run against a third-party skill published on ClawHub
(`z-zihan/skill-review-pro` v2.3.1). It is shown as a sample of output format, not as a
verdict on that package — see *Scope* at the bottom.

文末有中文说明。

---

## Subject

| | |
|---|---|
| Package | `skill-review-pro` |
| Version | 2.3.1 |
| Files | 14 |
| Size | 88 KB |
| SKILL.md | 43.1 KB / 532 lines |

## Verdict — two rulers, never merged

```
结构制  54/100（54%） FAIL
语义制  88/120（73%） C
判读    语义有料但交付不完整：有真判断，缺测试/分层/复跑入口，装上容易踩坑
```

Two conclusions that answer different questions:

- **Structure (100)** — can this package be used at all?
- **Semantics (120)** — is it worth using?

They disagree by 34 points here. A single blended score would have hidden exactly the thing
worth knowing: the content is substantive, the delivery is not finished.

## Structure, dimension by dimension

| Dimension | Score | Reading |
|---|---|---|
| structure | 20/20 | frontmatter complete, SemVer valid, single root |
| consistency | 15/25 | declared commands mostly backed by scripts |
| reproducible | **0/20** | no tests, no runner, no demo — nobody can re-run it |
| hygiene | 15/15 | no leaked secrets, no stray artifacts |
| discoverable | 4/15 | no tags, no cross-links, no ai-index |
| licensing | **0/5** | no author field, no license field, no LICENSE file |

## Findings — every one carries a semantic key and a place

```
[P1] R01·reproducible:no-golden      包内不存在（tests/）        no test cases (tests/*.json)
[P1] R02·reproducible:no-runner      包内不存在（tests/）        no test runner, no way to re-run
[P1] R03·reproducible:no-demo        包内不存在                 no demo, first-time users can't verify
[P1] R04·discoverable:no-tags        属判断项（无文件可指）      tags: 0 (recommend ≥3)
[P1] R05·discoverable:no-links       包内不存在                 no cross-link section
[P1] R06·discoverable:no-ai-index    包内不存在（ai-index.json） no ai-index.json / llms.txt
[P1] R07·licensing:no-author         包内不存在                 missing author
[P1] R08·licensing:no-license-field  包内不存在                 missing license field
[P1] R09·licensing:no-license        包内不存在                 no standalone license file
```

Three kinds of place, none left blank:

- `SKILL.md:18` — an exact line
- `包内不存在（tests/）` — the thing genuinely is not there
- `属判断项（无文件可指）` — a count, not a file; saying "no file to point at" is more honest
  than inventing a path

## Semantics, 120-point scale

| | Dimension | Score | Reading |
|---|---|---|---|
| D1 | Knowledge Delta | 20/20 | narration 25% — mostly substance, not restatement |
| D2 | Mindset + Procedures | 15/15 | decision tree present, 72 ordered steps |
| D3 | Anti-Patterns | **7/15** | 7 hard rules, **0 carry a reason** |
| D4 | Specification | 10/15 | 3/3 fields, description 460 chars |
| D5 | Progressive Disclosure | **1/15** | 532-line body, 0 `references/` — one flat file |
| D6 | Freedom Calibration | 15/15 | 2 scripts, params declared |
| D7 | Pattern Recognition | 5/10 | over the 360-line pattern threshold |
| D8 | Practical Usability | 15/15 | 13 code blocks, boundaries stated |

The two weak spots are the same root: it is one long file with no layered references, and its
rules say "do this" without saying "because otherwise this breaks". Both are fixable in an
afternoon — which is why the 54 is a statement about delivery, not about competence.

## Token check (reported, not scored)

```
chars 32,456  ·  ≈11,427 tokens
E:A:R  30:38:1   (examples : operations : rules)
narration 25%
```

## How this report can be disputed

Every finding above has a semantic key. If one is wrong, file the appeal form with a path
and a check:

```json
{"items":[{"id":"reproducible:no-runner","claim":"a runner exists under tests/",
           "path":"tests/run_all.py","expect":"file_exists"}]}
```

The engine opens the file, rules OVERTURNED or UPHELD, and writes the ruling to
`appeal_log.json`. It never changes the score by itself — a reviewer that raises a score on
appeal has made its scores meaningless.

## Scope — read this before quoting the numbers

This ruler measures **verifiable delivery**: can someone install it, run it, find it, license
it. It does **not** measure the depth of industry judgment inside the text.

A package scoring 54 here may still contain professional insight this ruler cannot see. Rank
these packages by "coverage of strategy" instead and the order would likely flip. The score is
right; the conclusion drawn from it alone would be wrong.

---

## 中文说明

这是一次真实评测的原始输出，对象是 ClawHub 上一个第三方技能包（`z-zihan/skill-review-pro` v2.3.1）。**它是格式样例，不是对该包的判决。**

两个数回答两个不同问题：

- **结构制 54/100**：能不能用？缺测试、缺复跑入口、缺许可文件。
- **语义制 88/120**：值不值得用？知识密度高、流程清楚，但反模式不带理由、整份文档是一个平铺文件。

两者差 34 分，说明「有真本事，但交付没做完」。如果合成一个数，恰好把这个最值得知道的信息抹掉。

每条发现都带语义键（`reproducible:no-runner`）和位置（`SKILL.md:18` / `包内不存在（tests/）` / `属判断项（无文件可指）`）。指不到的就说指不到，不编路径。

**边界**：这把尺子量的是「可验证交付」，不量文本里的行业判断有多深。换成「策略覆盖度」这把尺子，排序很可能翻转。分数是对的，单看分数得出的结论可能是错的。
