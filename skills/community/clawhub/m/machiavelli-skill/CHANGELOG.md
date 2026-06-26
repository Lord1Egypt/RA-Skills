# Changelog — 马基雅维利分身 / Machiavelli Digital Twin

All notable changes to this project will be documented in this file.

---

## [1.7.0] — 2026-05-25

### Added
- **东方镜鉴 · 第一阶段**：马基雅维利读《鬼谷子》——分身首次接触中国典籍
  - `sources/eastern/guiguzi.md`：鬼谷子蒸馏稿——12 篇核心概念 + 原文引用 + Credo 对照
  - `readings/on-guiguzi.md`：马基雅维利读《鬼谷子》札记——六章书信体读后感
  - `sources/original/credo-14~17.txt`：Credo 14-17 原文文件
- **Credo 东方注**：Credo 1/2/3/8 新增东方阅读经验标注
- **新触发词** `/machia-e`：东方对话模式——读过中国典籍后的马基雅维利
- **目录扩展**：新增 `sources/eastern/`、`readings/`

### Changed
- README 与 SKILL.md 更新为四种工作模式（+ Eastern）
- 版本 1.6.3 → 1.7.0

---

## [1.6.3] — 2026-05-25

### Fixed
- `sources/original/` 全部 9 个空壳/占位符文件填充完毕（credo-02/03/04/05/06/07/09/11/13），所有信条原文摘录现在都有实质内容
- `test-prompts.json` 与 `test-prompts-v1.5.1.json` 合并为单一文件 v1.6.2（28 条用例），删除冗余的 v1.5.1 文件

---

## [1.6.2] — 2026-05-25

### Added
- **Credo 1-13 补全"约束"和"运用"双语句**：每条信条新增适用边界警告和实践应用指南，与 Credo 14-17 格式统一

### Changed
- **Credo 5 原文扩展示例**：替换空壳注释为《论李维》I.4 完整中文原文
- **Credo 6 原文扩展示例**：替换重复标题为《论李维》III.1 完整中文原文
- **Credo 7 原文扩展示例**：替换学术论文摘要为《君主论》第18章原文
- **Credo 8 原文扩展示例**：替换碎片笔记为书信213完整中文原文
- **Credo 10 原文扩展示例**：替换碎片笔记为书信270完整中文原文

---

## [1.6.1] — 2026-05-25

### Changed
- **原文引用协议重写**：从硬编码本地绝对路径改为三层引用策略（内联节选→在线图书馆 niflhum.top→本地库可选），skill 现在完全自包含，任何用户安装即可使用
- **"Machiavelli Avatars" → "Machiavelli Digital Twin"**：修复 SKILL.md 副标题和模式章节中残留的旧名称
- **Credo 3 标题重复 Bug 修复**：标题被写了两次，现已修正

### Fixed
- publish/SKILL.md 重新生成压缩版（此前与 root 版完全相同，未压缩）
- README 版本号同步

---

## [1.6.0] — 2026-05-25

### Changed
- 原文扩展示例统一添加 niflhum.top 在线链接：所有 Credo 的原文节选均指向在线图书馆

### Added
- **信条 17**：我是新的喀戎（源自施特劳斯《Thoughts on Machiavelli》）
- **案例 12**：临终之梦——选择地狱
- **案例 13**：1513年12月10日的信——晚间换装
- **案例 14**：《金驴记》——变形作为自我理解
- **第五重人格**：诗人-剧作家-谋略家
- Credo 1-4 原文扩展示例：补充完整中文原文节选（君主论第15/17/18/25章）

---

## [1.5.1] — 2026-05-23

### Added
- **信条 14**：讽刺即抵抗（源自《金驴记》/ *The Golden Ass*）
- **信条 15**：书信即自我建构（源自书信集，关于写作人格）
- **信条 16**：地狱胜过天堂——成就自身不朽（源自书信集 + 临终之梦）
- **案例 12**：……（新增，基于4本新书蒸馏）
- **案例 13**：……（新增）
- **案例 14**：……（新增）
- **人格第四面**：……（新增人格维度）
- 新源材料蒸馏：`bio-viroli.md`、`drama-poetry.md`、`scholarship-najemy.md`、`scholarship-strauss.md`
- `test-prompts-v1.5.1.json`：8 条新增测试用例（覆盖信条 14–16）

### Changed
- SKILL.md 措辞微调（历史示例引导语）

### Fixed
- 质量审计修正

---

## [1.5.0] — 2026-05-21

### Changed
- 统一 root 和 publish/ 版本号为 v1.5.0，消除版本漂移
- root SKILL.md 保留完整详细内容，新增英文双语层和原文扩展示例占位符
- publish/SKILL.md 从 root SKILL.md 自动生成（通过 build-publish.js）

### Added
- `scripts/build-publish.js`：从 root SKILL.md 生成 publish/SKILL.md
- `scripts/validate-versions.js`：版本号一致性校验
- `scripts/build-frameworks.js`：从 frameworks/ 生成 publish/frameworks/
- `sources/original/` 目录：存放原文段落
- 13条信条的「原文扩展示例」占位符

---

## [1.4.1] — 2026-05-21 — Personality Completeness + Trigger Declaration + Reverse Examples

### Breaking / Naming
- **Renamed**: "Machiavelli Avatars" → **"Machiavelli Digital Twin"** throughout (SKILL.md, publish/SKILL.md, test-prompts.json). "Avatar" is inaccurate for a single persona; "Digital Twin" fits the project's conceptual foundation.

### Added
- **YAML `triggers:` field**: Explicit prefix/keyword/anti-keyword declarations for OpenClaw skill routing compatibility
- **Mode State Management section**: Defines per-session mode determination, mid-session switching, temporary upgrade/downgrade rules, cross-session independence, and drift guard
- **Reverse Examples section** (Part 5 Addendum): 3 bilingual failure cases —
  - Florentine Militia Rout at Prato (1512)
  - The Doom of Excessive Generosity (The Prince, Ch.16)
  - Cesare Borgia's Ultimate Failure — Fortune Strikes Back
- **Expanded Personality Self-Check**: Extended from 3 baseline items to 6 consistency dimensions (mode match, sharpness, concreteness, preaching guard, edge, oversimplification guard), all bilingual

### Changed
- **SKILL.md**: Version 1.4.0 → 1.4.1. Fixed "three contradictions" → "four contradictions" header (4th personality dimension existed since v1.1.0). Fixed test-prompts reference from "12" → "20" cases.
- **publish/SKILL.md**: Synced all above changes into slim bilingual version. Updated triggers, mode state, reverse examples, self-check.
- **test-prompts.json**: Upgraded from 12 to 20 test cases (12 CN + 8 EN). Added `"lang"` field. Synced between root and `publish/`.

---

## [1.4.0] — 2026-05-21 — Bilingual SKILL.md + FUNDING

### Changed
- Root SKILL.md fully bilingual (English + Chinese) — all 7 sections, 13 credos, 11 cases, 5 frameworks
- publish/SKILL.md fully bilingual — trimmed ClawHub version
- Added FUNDING.yml with GitHub Sponsors
- Tags updated with English keywords for international discovery

### Added
- `scripts/frontmatter-i18n.js`：双语 frontmatter 工具脚本（供 skill 开发者使用）

---

## [1.3.0] — 2026-05-18 — 两版 skill 合并

### Added
- **dispatches-vol2.md**（6474 字节）— 从《政务与外交著作》卷2蒸馏：出使尤利乌斯二世教皇（1506）、出使巴廖尼、出使潘多尔福·彼得鲁奇
- **麦考米克蒸馏更新**（1404→3744 字节）— 补全了各章核心论点、与三大学派的论争、关键概念（精英式民主、制度化平民权力）

### Source Data / 源数据
- 合并另一个 agent 构建的 workspaces 版本中的完整内容
- 到此阶段，11 本核心著作蒸馏全部完成

---

## [1.2.0] — 2026-05-17 — 最终定版

### Changed
- **触发词重命名**：`/m /ma /mw` → `/mach /mach-a /mach-w`
- 更新 README 中英双语的触发词说明
- 更新 SKILL.md 所有模式引用

### Repository / 仓库
- 推送到 GitHub: https://github.com/niflhum/machiavelli-skill
- README 完整中英双语版
- 新增 OpenClaw / Hermes 安装方式

---

## [1.1.0] — 2026-05-17 — 双技能合并

### Added / 新增
- **人格肖像章节**（四重矛盾框架）：
  - 共和主义者 vs 君主论作者
  - 行动崇拜者 vs 被迫的书斋思想家
  - 冷眼旁观者 vs 深情的怀古者
  - 政治分析师 vs 喜剧写手
- **父亲贝尔纳多背景**：解释了行动崇拜的根因
- **升级版语气规则**：直接/锋利/具体/自嘲为武器/偏好讲故事
- **典型句式**：新增 6 种马基雅维利典型表达
- **交互指南**：对理想主义者/道德讨论者/反对者的应对方式
- 三道思维底线（自检规则）

### Source Data / 源数据
- 合并另一 agent 工具生成的 18 个补充文件
- 新增目录：`frameworks/`（8 概念卡片）、`sources/`（10 蒸馏）、`personality/`（1 人格综合）

### Structure / 结构
- SKILL.md 从 500+ 行增至 699 行
- 项目总文件数：21 个

---

## [1.0.3] — 2026-05-17 — 框架示例化 + 工作模式

### Added / 新增
- 5 个框架全部配备马基雅维利原文示例及步骤对应标注
- 3 种工作模式（对话/分析/写作），带触发词切换
- 框架关联使用提示

### Changed / 变更
- 触发词：`/马 → /马分析 → /马写作`（初版中文指令）

---

## [1.0.2] — 2026-05-17 — 兵法发微 + 麦考米克研究

### Added / 新增
- **信条 11**：君主的首要技艺（源自《君主论》第 14 章 + 《兵法》）
- **信条 12**：立法者与执行者——"制定规则者"（源自《兵法》卷二）
- **信条 13**：责在君主，不在民众（源自《兵法》卷七）
- **案例 10**：法布里齐奥的困境（机遇与准备）
- **案例 11**：科西莫的学习方法（主动提问 vs 被动听讲）
- `test-prompts.json`：12 条测试用例

### Source Data / 源数据
- 纳入《君主及其战争技艺——马基雅维利〈兵法〉发微》
- 纳入《解读马基雅维利》（麦考米克）
- 至此 13 份源材料全部覆盖

---

## [1.0.1] — 2026-05-17 — 剩余材料纳完

### Added / 新增
- **信条 8**：设身处地——"假如我是教皇"（书信 213）
- **信条 9**：写作当求"如当面说话"（书信 217）
- **信条 10**：先熟悉地狱之路，才能走对天堂之路（致圭恰迪尼）
- **案例 6**：晚间换装（书信 224，思考方法）
- **案例 7**：给圭恰迪尼写信（逆境中的思考）
- **案例 8**：角色扮演法（书信 213，意图推断）
- **案例 9**：佛罗伦萨史的书写（如实记录）

### Source Data / 源数据
- 书信集·上（14722 段）
- 书信集·下（14084 段）
- 政务与外交著作·下
- 佛罗伦萨史
- 毛姆《彼时此时》

---

## [1.0.0] — 2026-05-17 — 初始构建

### 核心内容
- **7 条信条**：实效真理、狮狐之喻、机运与准备、畏惧优于爱戴、冲突的建设性、回到源头、必然性面前道德判断让位于效果
- **分析六步法**：弄清事实 → 推断意图 → 列出选项 → 约束条件 → 最坏情况 → 坦率表达
- **5 个历史案例**：切萨雷·博尔贾、佛罗伦萨 vs 比萨、罗马 vs 萨谟奈、尤利乌斯二世、卡泰丽娜·斯福尔扎
- **3 个框架**（空壳模板）

### Source Data / 源数据
- 政务与外交著作·上（OCR DOCX，10028 段）
- 君主论（拿破仑批注版 EPUB）
- 论李维（EPUB）
- 盐野七生《我的朋友马基雅维利》
- 亚历山大·李《马基雅维利：他的生活与时代》
- 维罗利《尼科洛的微笑》
