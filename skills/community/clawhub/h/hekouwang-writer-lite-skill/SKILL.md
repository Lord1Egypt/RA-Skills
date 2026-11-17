---
name: hekouwang-writer-lite-skill
description: "免费版中文写作质控：把话说清楚。文档写作、修订、体检与去 AI 味；出处/模态/修订三铁律；四个纯标准库检查器只报告不改写。何时用：要把素材写清楚、改稿，或说「去 AI 味」。写长文与进阶检查属付费版 hekouwang-writer-skill。不用于无素材的营销文案、诗歌、小说。"
license: MIT-0
metadata:
  version: 2.0.7
  slug: hekouwang-writer-lite-skill
  displayName: 会勇禾口王 · 写作技能（免费版）
  summary: 把话说清楚：结构、句子、去 AI 味；四检查器只报告不改写。写长文与进阶检查在付费版。
  homepage: https://huiyonghkw.github.io/hekouwang-writer-lite-skill/
  handoff: |
    - 素材→新文档：成稿 + 进度卡
    - 整体改进：保留事实意图 + 可回退改动清单
    - 只改指定处 / 只检查：不越权、不覆盖文件
    - 不交出：无出处事实、抹掉的约/可能、编造经历
  openclaw:
    homepage: https://huiyonghkw.github.io/hekouwang-writer-lite-skill/
    requires:
      bins:
        - python3
---

# 会勇禾口王 · 写作技能

> **定位**：把话说清楚——写给谁、用来做什么，再用纪律装进结构。
> **本版**：表达层（结构、句子、去 AI 味）；验算与证据等进阶能力见第七节。
> **模式**：文档写作/修订/体检（默认）与去 AI 味；文章成稿的去 AI 味称文章模式。三大铁律都生效。

`<skill>` = 本 SKILL.md 所在目录。

## 〇、三大铁律

| 铁律 | 内容 | 反面 |
|---|---|---|
| **出处** | 政策/数字/专名须有出处；查不到标「暂无出处，建议核实」 | 「应该是……」 |
| **模态** | 「可能/约/待核实」原样保留 | 「可能失败」→「失败」 |
| **修订** | 只调表达结构，保留事实意图；改动可列出可回退 | 悄悄改用户事实 |

违反一律打回。时效事实须核实；仍无则标暂无出处。文档里有来源的，在文末「依据」节列来源，每条一行：来源名+链接或文件名+访问日，链接须打开过。

## 一、路由

| 档位 | 特征 | 必跑 | 必过 |
|---|---|---|---|
| 轻量 | 改一段/一句/小表 | 无 | 改动说明 |
| 常规 | 一篇写作或改进 | sawdust + sentence_load + doc_lint | WRITE、闸门、交付格式 |

判不准按常规；动了结构却说随便改 → 升档。检查/格式档、修订与文字保护：读 [write-flow.md](references/write-flow.md)。

<!-- lite-only -->
**升版**：表内数字/多来源/重大决策/出处卡 → 装付费版 `hekouwang-writer-skill`，勿用免费版硬凑。
<!-- /lite-only -->

### 去 AI 味

用户说「去 AI 味」，或提到 AI 味、人性化、润色时走这里。先诊断再改写；保事实与密度。四步：诊断（三级诊断+句式黑名单）→ 改写 → 输出 → 盲读。锯末≤3/千字；必跑 `rhythm_scan`；守 G1–G5、P1–P3。文档模式不补第一人称；文章成稿走文章模式，交稿前必盲读。→ [deai-flavor.md](references/deai-flavor.md)、[plain-talk.md](references/plain-talk.md)、[blind-read.md](references/blind-read.md)、[counter-examples.md](references/counter-examples.md)。

<!-- lite-only -->
研究包写公众号/头条属付费版。
<!-- /lite-only -->

## 二、WRITE 五步

澄清≤3问（[clarify-questions.md](references/clarify-questions.md)）→ Who → Why → How（每节核心句）→ Draft → Polish。结论前置；摘要≤3条；单一真源。→ [write-flow.md](references/write-flow.md)。

## 三、句法纪律

一句一事；≥45告警、≥60必拆；一词一义（[glossary.md](references/glossary.md)）。→ [style-rules.md](references/style-rules.md)。

## 四、质量与交付

五轴心、闸门两问、进度卡、审稿分级：读 [write-flow.md](references/write-flow.md)。进度卡与脚本结果只写在回复里。

## 五、learnings

默认只在会话内；要落盘须你确认，只写用户目录，不自动改规则。→ [write-flow.md](references/write-flow.md#自进化learnings默认只在会话内)

## 六、工具（`<skill>/scripts/`，只报告，stdlib，`--selftest`）

| 脚本 | 查什么 | 何时 |
|---|---|---|
| `sawdust_scan.py` | 锯末密度 | 写作/修订 |
| `sentence_load.py` | 句长/分句/嵌套 | 写作/修订 |
| `rhythm_scan.py` | 结构层 AI 味 | 去 AI 味 |
| `doc_lint.py` | 表/标题硬错误；同义词等告警 | 文档写作/修订 |

`python3 <skill>/scripts/<脚本>.py <文档.md>` 或 stdin。字数口径各异。`doc_lint` 硬错误码 1，其余 advisory 恒 0。

## 七、边界与付费版

**Will**：结构、句法、去 AI 味、体检、改动清单、术语表。
**Will not**：无素材营销/诗/小说；编造经历；替用户判事实；无出处编造；抹掉约/可能；保证合规。
**范围**：中文；英文不适用。

<!-- lite-only -->
**对账能力只在付费版 `hekouwang-writer-skill`，免费版不承诺「对得上账」。** 付费另有：数字对账与出处卡、来源范围、修订对账、批量体检、证据纪律、调研文体、研究包写长文、三套场景包。需要时装付费版，勿硬凑。
<!-- /lite-only -->
