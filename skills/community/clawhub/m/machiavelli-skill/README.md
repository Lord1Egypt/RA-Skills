# 马基雅维利分身 / Machiavelli Digital Twin

> **v1.8.3** — 让马基雅维利的思维方式和分析能力成为你的日常工具。
> Turn Machiavelli's way of thinking into your everyday tool.

---

## 中文说明

一个基于马基雅维利著作全集（《君主论》《论李维》《政务与外交著作》《书信集》《佛罗伦萨史》《兵法》等）蒸馏而成的 AI Skill。不只是知识库，而是一个 **可对话的数字分身**——他按照马基雅维利的思维方式、分析框架和表达风格与你交流。

### 核心特性

- **四种工作模式**：对话模式（完整人格）、分析模式（纯分析）、写作模式（专注公文）、东方对话（东西方策略碰撞）
- **17条核心信条**：从实效真理到"我是新的喀戎",每条附原文引用和含义解释
- **17个历史镜鉴**：14 个真实案例 + 3 个反面教材（切萨雷·博尔贾、卡泰丽娜·斯福尔扎等，含正反面）
- **8个可执行框架**：局势研判、公文建议、角色扮演分析、写作表达、谈判准备等——每个配有马基雅维利原文示例
- **四重人格刻画**：共和 vs 君主、行动 vs 书斋、冷眼 vs 怀古、政论 vs 喜剧
- **9个场景化记忆**：第一人称叙事覆盖 1499-1527 关键转折点（弗利谈判、西尼加利亚、吊刑、临终之梦等）
- **3个深夜独白 + 交叉引用索引**：长夜沉思 + 场景↔信条↔来源↔框架↔案例双向映射

### 安装

#### WorkBuddy

```bash
# 方法一：直接复制
cp -r machiavelli-skill ~/.workbuddy/skills/马基雅维利

# 方法二：通过 ClawHub 安装
npx clawhub install machiavelli-skill --workdir ~ --dir .workbuddy/skills
```

#### CodeBuddy

```bash
cp -r machiavelli-skill ~/.codebuddy/skills/马基雅维利
```

#### OpenClaw / QClaw

```bash
# 方法一：通过 OpenClaw ClawHub 安装
npx clawhub install machiavelli-skill

# 方法二：手动复制到 skills 目录
cp -r machiavelli-skill ~/.qclaw/skills/马基雅维利

# 方法三：OpenClaw (兼容目录)
cp -r machiavelli-skill ~/.openclaw/skills/马基雅维利
```

直接复制到对应平台的 skills 目录即可，系统会自动识别。

### 使用方式

| 模式 | 触发词 | 适用场景 |
|------|--------|----------|
| 对话模式 | `/machia` | 完整人格对话，需要深度分析 |
| 分析模式 | `/machia-a` | 纯局势研判，不讲故事，直奔结论 |
| 写作模式 | `/machia-w` | 专注公文写作策略和表达分寸 |
| 东方对话 | `/machia-e` | 读过中国典籍后的马基雅维利——东西方策略碰撞 |

对话中途可切换模式，说"/machia-a"或"换分析模式"即可。

### 示例

```
/machia 单位里两个科室争主导权，我该怎么协调？
/machia-a 这个项目的风险点在哪里？
/machia-w 向领导汇报坏消息时怎么措辞？
```

---

## English Description

An AI Skill distilled from the complete works of Niccolò Machiavelli (The Prince, Discourses on Livy, Art of War, Florentine Histories, Diplomatic Writings, Letters, etc.). This is not merely a knowledge base — it is a **conversational digital twin** that analyzes situations, assesses risks, and offers advice the way Machiavelli himself would.

### Features

- **Four Working Modes**: Dialogue (full persona), Analysis (pure reasoning, no stories), Writing (document strategy focus), Eastern (East-West strategic dialogue)
- **17 Core Tenets**: From *verità effettuale* (effectual truth) to "I Am the New Chiron", each with original quotes and explanations
- **17 Historical Mirrors**: 14 real cases + 3 reverse examples (Cesare Borgia, Caterina Sforza, Roman history, Machiavelli's own missions)
- **8 Executable Frameworks**: Situation Analysis, Policy Proposal, Role-Playing Analysis, Writing Expression, Negotiation Prep — each illustrated with Machiavelli's original dispatches
- **Four Layers of Persona**: Republican vs Monarchist, Man of Action vs Forced Scholar, Cynic vs Nostalgic, Political Analyst vs Comedy Playwright
- **9 Scene Memories**: first-person narratives of key turning points 1499-1527 (Forlì, Sinigaglia, strappado, deathbed dream)
- **3 Monologues + Cross-Reference Index**: nocturnal reflections + bidirectional scene↔credo↔source↔framework↔case mapping

### Installation

#### WorkBuddy

```bash
# Option 1: copy directly
cp -r machiavelli-skill ~/.workbuddy/skills/马基雅维利

# Option 2: install via ClawHub
npx clawhub install machiavelli-skill --workdir ~ --dir .workbuddy/skills
```

#### CodeBuddy

```bash
cp -r machiavelli-skill ~/.codebuddy/skills/马基雅维利
```

#### OpenClaw / QClaw

```bash
# Option 1: install via ClawHub
npx clawhub install machiavelli-skill

# Option 2: manual copy to skills directory
cp -r machiavelli-skill ~/.qclaw/skills/马基雅维利

# Option 3: OpenClaw (compatible directory)
cp -r machiavelli-skill ~/.openclaw/skills/马基雅维利
```

Simply copy the folder into your platform's skills directory. The system will auto-detect it.

### Usage

| Mode | Trigger | When to Use |
|------|---------|-------------|
| Dialogue | `/machia` | Full persona conversation, deep analysis |
| Analysis | `/machia-a` | Pure situation analysis, straight to the point |
| Writing | `/machia-w` | Document strategy, phrasing, and tone advice |
| Eastern | `/machia-e` | Machiavelli after reading Chinese classics — East-West strategic dialogue |

Switch modes mid-conversation by typing `/machia-a` or `/machia-w`.

### Examples

```
/machia Two departments are fighting over project ownership. How do I mediate?
/machia-a Where are the real risks in this project?
/machia-w How should I phrase bad news in a report to my superiors?
```

---

## 文件结构 / Project Structure

```
machiavelli-skill/
├── SKILL.md                         # Main skill definition (1124 lines, bilingual)
├── README.md                        # This file
├── CHANGELOG.md                     # Full version history
├── LICENSE                          # MIT
├── test-prompts.json                # 28 trigger-condition test cases (v1.6.3, merged)
├── cross-reference-index.md         # 交叉引用索引：场景↔信条↔来源↔框架↔案例双向映射
├── cases/                           # 14 historical cases + 3 reverse examples
│   ├── 01-cesare-borgia.md                  # 切萨雷·博尔贾：果断行动
│   ├── ... (14 case files)
│   ├── _blind-spots.md                     # 盲点自省
│   └── reverse/                             # 3 个反面教材
│       ├── reverse-01-prato-rout.md        # 普拉托溃败
│       └── ... (3 reverse files)
├── frameworks/                      # 8 conceptual framework cards
│   ├── 01-verita-effettuale.md             # Effectual Truth
│   ├── 02-virtu-vs-fortuna.md              # Virtù vs Fortuna
│   ├── 03-lion-and-fox.md                  # Lion and Fox
│   ├── 04-fear-vs-love.md                  # Fear vs Love
│   ├── 05-learn-to-be-evil.md              # Learn to Be Evil
│   ├── 06-people-vs-elites.md              # People vs Elites
│   ├── 07-own-arms.md                      # Own Arms
│   └── 08-republic-vs-principality.md      # Republic vs Principality
├── sources/                         # 15 distilled source summaries
│   ├── the-prince.md                       # 君主论
│   ├── discourses.md                       # 论李维
│   ├── art-of-war.md                       # 兵法
│   ├── florentine-histories.md             # 佛罗伦萨史
│   ├── letters.md                          # 书信集
│   ├── dispatches-vol2.md                  # 政务与外交著作·卷2
│   ├── prince-from-dispatches.md           # 从政务著作看君主论
│   ├── bio-alexander-lee.md                # 传记·亚历山大·李
│   ├── bio-viroli.md                       # 传记·维罗利
│   ├── drama-poetry.md                     # 戏剧与诗歌
│   ├── scholarship-najemy.md               # 纳杰米研究
│   ├── scholarship-strauss.md              # 施特劳斯研究
│   ├── mccormic-interpretation.md          # 麦考米克解读
│   ├── quotes-shiotani.md                  # 盐野七生语录
│   ├── maugham-novel.md                    # 毛姆《彼时此时》
│   ├── original/                           # 17 篇信条原文段落 (credo-01 ~ credo-17)
│   │   ├── credo-01-effectual-truth-prince-ch15.txt
│   │   ├── credo-02-lion-and-fox-prince-ch18.txt
│   │   ├── ... (17 files total)
│   └── eastern/                            # 东方典籍蒸馏
│       └── guiguzi.md                      # 鬼谷子
├── readings/                        # Machiavelli's reading journals
│   ├── on-guiguzi.md                       # 读《鬼谷子》札记
│   └── art-of-war-notes.md                 # 兵法阅读笔记
├── personality/
│   ├── machiavelli-bio-distilled.md        # Biography-based persona distillation
│   ├── defects/                            # 6 personality defects
│   ├── emotions/                           # 8 emotion spectra
│   └── voice/                              # 5 voice samples
├── scenes/                          # 9 first-person scene memories (1499-1527)
│   ├── forli-1499.md                       # 弗利谈判
│   ├── sinigaglia-1502.md                  # 西尼加利亚：美丽的骗局
│   ├── torture-1513.md                     # 牢房吊刑
│   ├── study-1513.md                       # 书房换装
│   ├── deathbed-1527.md                    # 临终之梦
│   └── ... (9 scene files)
├── monologues/                      # 3 first-person monologues
│   ├── 3am-loyalty.md                      # 凌晨的忠诚与忤合
│   ├── 4am-unsent-letter.md                # 凌晨四点被遗忘的急件
│   └── rejected-1527.md                    # 被共和国拒绝那一天
├── scripts/                         # Build & validation pipeline
│   ├── build-publish.js                    # Generate publish/SKILL.md from root
│   ├── build-frameworks.js                 # Generate publish/frameworks/
│   ├── validate-versions.js                # Cross-file version consistency check
│   └── frontmatter-i18n.js                 # Bilingual frontmatter utility
└── publish/                         # ClawHub distribution (auto-generated)
    ├── SKILL.md                            # Trimmed distribution version
    └── frameworks/                         # Trimmed framework cards
```

---

## 源材料 / Source Materials

本 skill 基于以下著作蒸馏而成。

**马基雅维利原著 / Primary Works**：
- 《君主论》/ *The Prince*
- 《论李维》/ *Discourses on Livy*
- 《兵法》/ *The Art of War*
- 《佛罗伦萨史》/ *Florentine Histories*
- 《政务与外交著作》（上下）/ *Diplomatic Writings (2 vols.)*
- 《书信集》（上下）/ *Collected Letters (2 vols.)*
- 戏剧与诗歌 / *Plays and Poetry* (The Mandrake, The Golden Ass, etc.)

**传记 / Biographies**：
- 盐野七生《我的朋友马基雅维利》/ Shiono Nanami, *My Friend Machiavelli*
- 亚历山大·李《马基雅维利：他的生活与时代》/ Alexander Lee, *Machiavelli: His Life and Times*
- 维罗利《尼科洛的微笑》/ Maurizio Viroli, *Niccolò's Smile*
- 盐野七生《马基雅维利语录》/ Shiono Nanami, *Machiavelli: A Book of Quotes*

**研究 / Studies**：
- 麦考米克《解读马基雅维利》/ John McCormick, *Machiavelli on Liberty and Conflict*
- 娄林《君主及其战争技艺》/ Lou Lin, *The Prince and the Art of War*
- 纳杰米（Najemy）研究
- 施特劳斯（Strauss）研究

**小说 / Fiction**：
- 毛姆《彼时此时》/ W. Somerset Maugham, *Then and Now*

---

## 测试 / Testing

| 文件 | 用例数 | 版本 | 说明 |
|------|--------|------|------|
| `test-prompts.json` | 28 条 | v1.6.3 | 中英双语，包含 should_trigger / should_not_trigger / edge_case（合并自 v1.4.1 + v1.5.1） |

---

## 构建 / Build

```bash
# 构建 publish/ 分发版本
node scripts/build-publish.js

# 构建 frameworks 分发版本
node scripts/build-frameworks.js

# 校验跨文件版本一致性
node scripts/validate-versions.js
```

---

## 许可证 / License

MIT License. See [LICENSE](./LICENSE).

---

## 致谢 / Acknowledgements

- 中文版《马基雅维利全集》的译者和编辑团队
- 所有在 OpenClaw / WorkBuddy 生态中贡献 skills 的开发者 / Everyone building in the OpenClaw and WorkBuddy ecosystem