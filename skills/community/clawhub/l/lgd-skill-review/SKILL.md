---
name: lgd-skill-review
description: 'Use when reviewing, auditing or scoring any AI skill package, or when a skill was rejected and you need to know why. A dual-ruler reviewer: reports a structure score (100) and a semantics score (120) as two orthogonal verdicts instead of merging them, and flags the case when the two disagree by 20 points or more. Structure asks whether the package can be used at all (tests, declared-vs-implemented consistency, reproducibility, hygiene, discovery, licensing); semantics asks whether it is worth using (knowledge delta, procedures, anti-patterns with reasons, specification, progressive disclosure, freedom calibration, pattern fit, usability). Every finding carries a stable ID and is traceable to a specific file. Accepts evidence-based appeals: the appellant supplies a path and a check, the engine opens it and rules OVERTURNED / UPHELD, and records the ruling in appeal_log.json. Appeals never silently change a score - they turn a deduction into a verifiable dispute.'
license: MIT
allowed-tools: Read, Glob, Grep, Bash
metadata:
  displayName: 技能评测官
  displayNameEn: Skill Reviewer
  display_name: 技能评测官
  display_name_en: Skill Reviewer
  slug: lgd-skill-review
  author: 诺声(Logos)@SynomosAI
  copyright: SynomosAI
  version: 1.1.21
  description_zh: 技能体检 / 评测 / 打分 / 为什么被拒 / 对评分不服 —— 对任意 AI 技能包做双制评测：结构制（100 分，量能不能用）与语义制（120 分，量值不值得用）各自出结论、绝不加权成一个数，两者背离 ≥20 分时会明确标出。每条整改项带稳定 ID、可指到具体文件；支持证据驱动的申诉（给出路径与核验方式，引擎自己打开判断），裁决推翻/维持并写入 appeal_log.json，但**不会因为申诉直接改分**——申诉的作用是把扣分变成可核验的争议点，不是让人自己给自己加分。
  description_en: 'A six-dimension, evidence-based reviewer for any AI skill package: scores structure, declared-vs-implemented consistency, reproducibility, hygiene, AI discoverability and licensing on a weighted 100-point scale, emits a prioritized fix list (P0 blocking / P1 improvement) and a rerun command, closing the review -> fix -> re-review loop. Every point is traceable to a file and finding.'
  tags:
  - 技能评测
  - 质量门禁
  - SKILL 审查
  - 整改闭环
  - lgd-skill-review
  category: developer-tools
  display_name_zh: 技能评测官
---

# lgd-skill-review · 技能评测官

## Triggers（触发词）

| 场景 | 用户会这么说 |
|---|---|
| 中文口语 | 帮我评一下这个技能 / 给我打个分 / 技能体检 / 技能质检 / 能不能上架 / 上架前检查一遍 / 为什么被拒 / 怎么改才能过 / 给份整改清单 / 改完再复核 / 复测一下 / 有没有泄露密钥 / 结构有没有问题 / 文档写的命令脚本都有吗 |
| 中文术语 | 评审 skill / 测评 skill / skill 评分 / 技能审查 / 质量门禁 / 发布核验 / 上架检查 / 稳定性测试 / skill benchmark / repo audit / publish check |
| English | review my skill / audit this skill package / score this skill / is it releasable / why was my skill rejected / skill quality check / give me a fix list / does the doc match the script / skill vetting |
| 间接场景 | 拿到别人的包想知道值不值得装；刚改完想确认没改坏；按我们的标准看 |

**Not for**：评测一段文字（那是写作评审）、评测模型回答质量（那是评测集）、评测商业方案（那是尽调）。

## 为什么值得用（与同类工具的差别）

多数「技能检查」给的是清单式建议：有没有 icon、有没有 license、描述够不够长。
本技能给的是**能指到行的判定**，且专抓一类别人不查的硬伤：

**声明与实现不符**——文档写了 `--draft`，脚本里只有 `--file`。这类缺陷在真实包里反复出现，
人眼几乎查不出来，但它会让使用者第一次调用就失败。本技能把它设为**阻断项**：命中即 BLOCK，分数再高也不给过。

## 六维评分口径（合计 100）

| 维度 | 权重 | 查什么 | 怎么扣分 |
|---|---|---|---|
| `structure` | 20 | frontmatter 必填、SemVer、层级 ≤3、无 .pyc/.zip/__pycache__、展示名 | 缺一项扣一段 |
| `consistency` | 25 | **声明 vs 实现**：文档提到的 `--flag` / 子命令，脚本里是否真有 `add_argument` / `add_parser` | 命中未实现 → 阻断 |
| `reproducible` | 20 | tests/*.json、tests/run_*.py、demo/；`--run` 时实跑并以退出码计分 | 缺证据扣分，实跑失败不给分 |
| `hygiene` | 15 | API Key、手机号、真实邮箱、本机绝对路径；有无安全边界声明 | 命中 → 阻断 |
| `discoverable` | 15 | tags ≥3、触发词段、互链段、`ai-index.json` 或 `llms.txt` | 逐项扣 |
| `licensing` | 5 | author、license 字段、独立 LICENSE 文件 | 逐项扣 |

判定：有阻断项 → `BLOCK`；<60 `FAIL`；<80 `WARN`；否则 `PASS`。

## 类型策略（按技能类型提不同建议）

同一套尺子量所有技能，但**不同类型的技能该有的东西不同**。所以本技能先判类型，再按类型补一类建议（P2，不参与计分——避免用类型给分数注水）：

| 类型 | 自动识别依据 | 该类该有 | 缺了会怎样 |
|---|---|---|---|
| `meeting` 会议纪要 | 纪要/逐字稿/transcript/minutes | 来源适配说明、证据溯源、黄金集 | 只能处理一种导出格式；数字无法核验 |
| `debug` 调试 | 报错/堆栈/debug/troubleshoot | 证据纪律声明、复现分级、失败样例 | 会输出像样但错误的原因 |
| `content` 内容选题 | 选题/标题/公众号/topic | 合规红线单列、不作虚假承诺 | 踩线或承诺阅读量 |
| `reviewer` 评测 | 评测/评审/打分/质量 | 自检套件、评分口径公开、闭环演示 | 评测器本身不可信 |
| `general` 通用 | 上述都不命中 | — | — |

指定类型：`--type meeting|debug|content|reviewer|general`；不指定则自动识别（两类关键词命中 ≥2 才判定，否则归 general）。

## 什么时候不用（Not for）

- **不评代码正确性**：只评交付结构与声明一致性，不做单元测试、不查业务逻辑对错。
- **不做安全渗透**：只做敏感信息与危险调用的静态排查，不做漏洞利用验证。
- **不替代人工评审**：输出的是证据化清单，不是终审结论；策略厚度、行业洞察需人判断。
- **不适用于非技能目录**：普通代码仓库、文档集、数据目录请勿套用本评分体系。

## 怎么用

```bash
# 人读报告
python scripts/review.py <技能目录>

# 机读（固定 ok/error_id/data 三字段，便于上层脚本串联）
python scripts/review.py <技能目录> --json

# 连测试一起实跑（推荐：不实跑，reproducible 拿不满）
python scripts/review.py <技能目录> --run

# 指定类型（不指定则自动识别）
python scripts/review.py <技能目录> --run --type meeting
```

输出含四块：总分与判定、六维分数、阻断项、**整改清单（P0 阻断 / P1 改进）**、以及 `rerun` 复测命令。

## 闭环怎么走（这是本技能的核心用法）

1. **评测**：拿到分数与整改清单；
2. **整改**：按 P0 先修阻断项，再修 P1；
3. **复测**：直接执行输出里的 `rerun` 命令，分数应上升；
4. **记账**：把「改前分 → 改后分 → 改了什么」写进 CHANGELOG，形成可审计轨迹。

实测案例（本包 demo 可复跑）：一个缺字段、且含明文密钥的包，首评 `BLOCK`；补字段、去密钥、加 tests 后复测 `PASS`。
分数上升的每一步都能指到那一条整改项。

## 输出示例

一份完整评测报告的节选（六维分项 + 阻断项 + 整改清单），见 `references/output-example.md`。

## 包内文件（渐进式披露）

| 路径 | 内容 | 何时读 |
|---|---|---|
| `SKILL.md` | 主文件：口径、用法、闭环 | 默认只读这一份 |
| `references/scoring.md` | 每一维的判定细则与扣分点（可对外引用） | 要解释某一分为何这么扣 |
| `references/faq.md` | 本评测器自己被推翻过五次的经过、常见误判识别法、已知边界 | 怀疑被误判，或要判断这个分数能不能信 |
| `references/appeal.md` | 申诉规则：怎么提、引擎怎么裁、为什么不改分、留痕在哪 | 对某条扣分不服 |
| `scripts/review.py` | 评测引擎（零依赖） | 直接跑 |
| `tests/golden.json` + `tests/run_golden.py` | 评测器自检：好包应 PASS、坏包应 BLOCK | 想验证评测器本身没坏 |
| `demo/run_demo.py` | 闭环演示：造坏包 → 出整改 → 修复 → 复测 | 第一次了解怎么用 |
| `ai-index.json` / `llms.txt` | 机器可读索引（给 AI 检索与路由） | AI 自动发现时 |

## 安全边界与降级

- **只读被测包**：评测过程不修改被评目录；需要「修复演示」时在临时目录复制后再改。
- **不评人**：只评包的结构与声明一致性，不评价作者水平、不猜测动机，也**不编造**未观察到的缺陷；
  每一条扣分都必须能在报告里指到具体文件。
- **不联网**：全部本地静态检查 + 本地实跑，不上传任何被评内容。
- **降级**：`--run` 需要被测包有可执行测试；无测试时该维度按证据缺失计分并说明，不伪造通过。
- **不替代人工终审**：分数是门禁的第一道闸，最终是否上架仍需人判断。

## 硬规则清单（MUST / NEVER）

1. **MUST** 每个扣分点都给出证据：文件 + 行号或规则名。
2. **NEVER** 无证据扣分。
3. **MUST** 输出复跑命令，让人能自己验一遍。
4. **NEVER** 把建议写成阻断（阻断只给会直接导致失败的项）。
5. **MUST** 阻断项优先于总分呈现。
6. **NEVER** 因技能类型不同而改变同一条规则的口径——否则同一份包换个类型就换个分数，尺子就废了。
7. **MUST** 计分维度只认可验证事实，不认宣传词——因为宣传词无法复跑，复跑不了的分等于没分。
8. **NEVER** 用「优秀」「专业」这类形容词替代证据——否则报告读完仍不知道该改哪一行。
9. **MUST** 整改项标 P0/P1/P2 优先级——否则一堆问题平铺，改的人不知道先动哪个，会漏掉阻断项。
10. **NEVER** 隐藏局限：边界、未覆盖项、判定口径必须写在报告里——否则分数被当成全能背书，出事时反噬的是评测方。

## 治理与许可

本技能承载 SynomosAI 治理体系（AI 护照机制 / A³ 法则 / XCGS / AI 世界共生论），版权 © 2026 SynomosAI，
依 MIT License 提供。按「原样」提供，评分为启发式判定，不构成任何形式的担保。

## 输出之后交给谁（链式路由）

本包不是孤岛。收尾时按下列条件把活交给下一个技能，并把指定材料一起递过去——
路由数据在 `chain.json`，机器可读：

| 当… | 交给 | 递什么 |
|---|---|---|
| when tests fail（被测包测试跑不通） | `debug-pro` | 失败输出 + 包路径 |
| when the target is minutes/transcript（被测对象是纪要/摘要） | `summarize-pro` | 用其黄金集交叉验证证据链 |
| when the target is content/topic（被测对象是内容/选题） | `wechat-viral-topic` | 用其红线清单查合规边界 |

这条链是双向的：其余三个技能也各有一份 `chain.json` 指回本包。

## 同系列技能（互链）

| 技能 | 什么时候接过来 |
|---|---|
| `summarize-pro` | 评测通过后，需要把长材料压成带出处的纪要 |
| `debug-pro` | 发现的问题是运行时故障，需要压成可复现步骤 |
| `wechat-viral-topic` | 需要把素材压成可传播的选题 |

完整英文描述见 `references/ecosystem.md`。

