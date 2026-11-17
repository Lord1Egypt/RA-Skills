# HumorUp 🎭

*English first · [中文版在下方](#humorup--中文版)*

An [OpenClaw](https://openclaw.ai) skill that punches up your writing with
actual wit — toasts, bios, birthday messages, Slack posts, presentation
openers — in English and Chinese. Anti-cringe by design: it knows when NOT
to be funny.

## Install

```bash
clawhub install humor-up
```

## What it does

| Job | Say something like |
|---|---|
| Punch-up | "Make this toast funnier: …" |
| Occasion writer | "Write a funny birthday message for Sam — he's always on his Peloton" |
| Witty daily brief | (auto) appends one topical one-liner to news/calendar briefs |
| Joke on demand | "Tell me a joke about Mondays" |
| Icebreakers & openers | "Give me an opener for my 9am presentation to finance" |
| Caption this | "Caption this photo" *(attach an image)* |
| Joke doctor | "Is this funny?" · "Score this joke and fix it" |

Built on one principle: **a joke is a controlled expectation violation.**
The skill ships a bilingual pattern library (misdirection, literal reading,
escalation, understatement, rule of three, and more — plus Chinese-only
patterns), five craft laws, and a scoring rubric.

**File structure is bilingual-transparent:** in `SKILL.md` and `patterns.md`,
English content comes first and a self-contained Chinese section follows —
readers of either language get a coherent read with no interleaved fragments
of the other.

## Safety & privacy

Pure-prompt skill: **no scripts, no environment variables, no CLI
dependencies, no network access.** Markdown files only. Humor targets systems
and the self, never people ("target up or inward, never down"), and the skill
declines to joke about death, illness, grief, or anyone's bad day.

## Files

- `SKILL.md` — the skill: jobs, laws, rubric, calibration bar (English craft
  first, Chinese guide at the end)
- `patterns.md` — pattern construction detail (universal patterns in English,
  then a Chinese section with build notes and Chinese-only patterns)
- `CHANGELOG.md` — version history

## Feedback & issues

Found a bug, a cringe joke, or a pattern that doesn't land? Open an issue:
**https://github.com/KimmyPlusLi/HumorUp/issues**

## License

MIT-0 (as with all ClawHub skills).

---

# HumorUp 🎭 — 中文版

一个 [OpenClaw](https://openclaw.ai) 技能:给你的文字加上真正的笑点——
祝酒词、个人简介、生日祝福、群发言、演讲开场白——中英文双语。反尬为先:
它知道什么时候**不该**搞笑。

## 安装

```bash
clawhub install humor-up
```

## 能做什么

| 任务 | 这样说 |
|---|---|
| 加梗润色 | "这段年会发言帮我加点梗" |
| 场合文案 | "帮我写个好笑又暖的生日祝福,给总迟到的室友" |
| 日报彩蛋 | (自动)在新闻/日程简报结尾加一句应景段子 |
| 现写段子 | "用『加班』讲个段子" · "来个关于内卷的一句话笑话" |
| 开场白/破冰 | "帮我想个早会开场白" |
| 配文字 | "给这张图配个文案"(附图) |
| 段子医生 | "帮我看看这个段子哪里不好笑" |

核心原则只有一条:**笑点是一次受控的预期违背。**技能内置双语模式库
(误导反转、字面理解、顺势夸张、轻描淡写、三段式等,外加谐音梗、歇后语、
对仗泄气等中文专属模式)、五条铁律和评分标准。

**文件结构对双语读者透明:**`SKILL.md` 和 `patterns.md` 均为英文在前、
文末附完整独立的中文部分(中文指南 / 中文部分)——两种语言的读者都能
连贯阅读,互不干扰。

## 安全与隐私

纯提示词技能:**无脚本、无环境变量、无命令行依赖、无网络访问**,只有
Markdown 文件。幽默只向上(制度、强者)或向内(自嘲),从不向下;涉及
死亡、疾病、悲伤或他人倒霉事时一律不开玩笑。

## 文件

- `SKILL.md` — 技能本体:任务、铁律、评分、校准(英文在前,文末为中文指南)
- `patterns.md` — 模式构造细节(通用模式为英文,中文部分含中文构造要点与
  中文专属模式)
- `CHANGELOG.md` — 版本历史

## 反馈与问题

发现 bug、尬住的段子、或不成立的模式?欢迎提 issue:
**https://github.com/KimmyPlusLi/HumorUp/issues**

## 许可

MIT-0(与所有 ClawHub 技能一致)。

---
*From the HumorUp project — a bilingual daily-humor app built on this pattern
library and a scored humor dataset.*
