---
name: ielts-reading-review
description: "IELTS Reading passage review, scoring, and progress tracking skill. Generates structured review data (JSON) and deploys to www.liuxue.online via saveReview API. The server's review.html template renders JSON into unified pages. No standalone HTML generation needed. Supports batch import of legacy reviews with auto-discovery of review folders. Trigger phrases: 雅思复盘, 帮我复盘阅读, IELTS reading review, 分析错题, 阅读错题分析, 成绩单, 打分, 统计, 进步趋势, 批量导入历史复盘, 历史笔记转 JSON, 把文件夹里的复盘都生成 JSON, 扫一下我电脑里的复盘, 帮我找出所有历史笔记, 自动发现复盘, score, band, progress, batch import, auto scan."
---

# IELTS Reading Review Skill

## Purpose

帮用户把雅思阅读做题结果变成结构化数据（JSON），通过 saveReview API 入库后由后端 review.html 模板统一渲染页面。

## 🔴🔴🔴 最高铁律 (v5.5.2 — Cannot Be Skipped)

**只要主人在对话里发了雅思阅读题（截图 / 文字答案 / 错题列表 / 任何阅读相关材料），就必须一气呵成跑完以下闭环，不允许中途停在文字分析阶段：**

```
读截图 → 错题确认 → 写错题分析 → ★生成 v4.0 JSON★ → ★saveReview/upload 入库★ → ★getReviews 回查 ✅★ → 汇报线上链接
```

**判定"复盘完成"的唯一标准 = `getReviews` 回查显示该篇已入库（不是"我写完文字分析了"）。**

**绝对禁止的"假完成"模式（历史血泪）：**
- ❌ 写完错题分析就交卷，不生成 JSON → 主人在 www.liuxue.online 看不到记录
- ❌ 生成 JSON 但忘了 saveReview / upload.js → 文件部署 ≠ 数据入库
- ❌ 调了 saveReview 但没 getReviews 回查 → API 静默失败也不知道
- ❌ 等主人催"怎么没上传"才补救 → 这就是失败

**本铁律覆盖所有其他流程**。即使主人只说"帮我看看这题对不对""分析这道错题""这套该几分"，**只要内容是雅思阅读，就走完整闭环**。

> 历史教训（2026-05-22）：剑8 T3P1+T3P2 复盘只在聊天里写了文字分析没入库，主人在 dashboard 看不到，22:49 提醒后才补救。**这种事再也不能发生**。

## Architecture (v5.5.2 — Locked-in Closed Loop)

**⚠️ v5.5.2 变更**（2026-06-23）：**域名迁移** tuyaya.online → www.liuxue.online。旧域名因 ICP 备案审核已全站 403 不可用。所有脚本（setup-client-mode.sh 含 CORS Allow-Origin）、文档默认域名全部切到 www.liuxue.online。SSH 隧道 `ssh.tuyaya.online` 保留不变（cloudflared 隧道不经 nginx，不受影响）。

**⚠️ v5.5.1 变更**（2026-06-01）：选择题和判断题错题新增 `rejectedOptions[]` 字段，在 review.html 中以红色边框卡片渲染"为什么不选"区域，逐个排除错误选项。

**⚠️ v5.4.2 最重大变更**（2026-05-22）：将"必须入库"提升为最高铁律。SKILL.md 顶部新增「最高铁律」段，加入 Step 8 Final Gate 强制 checklist——任何复盘任务，未通过 `getReviews` 回查 ✅ 不允许结束，不允许只交付文字分析。

**⚠️ v5.1 新增三道防线**（防 saveReview 漏调 / 本地副本陈旧）：
1. **发布脚本自动同步本地副本**：publish-clawhub.sh 跑完后自动 `clawhub install --force` 到 `~/.workbuddy/skills/`
2. **Step 7g 强制入库回归验证**：调 saveReview 后必须再用 getReviews 回查确认入库，**部署 ≠ 入库**
3. **Step 0 强制展示版本横幅**：每次激活时输出本地+远程版本号，落后必告警

**⚠️ v5.0 重大简化**：服务端已预置 C4-C20 全量 answer-key（204条 reading）+ bilingual_data（100条核心双语），**复盘流程不再需要更新这两个文件**，部署清单大幅缩减。

**⚠️ 不再生成复盘 HTML！** 后端 `review.html` 模板页统一渲染 JSON，单独生成的 HTML 完全无用。

产出物：
1. **结构化 JSON（v4.0）** — 成绩、错题、词汇、同义替换的全量数据。通过 saveReview API 入库后，`review.html?file=xxx.json` 在线渲染

> **v5.1 变更（2026-05-11 晚）**：三道防线避免再犯 saveReview 漏调 + 本地副本不更新的坑。

> **v5.0 变更（2026-05-11）**：服务端预置 C4-C20 全量 answer-key + bilingual_data，复盘流程不再需要本地维护这两个文件。仅当复盘 C20 之后的新书才需要扩展。部署清单从 5 个文件缩减到 4 个（仅 JSON + 词汇相关）。

> **v4.0 变更**：不再生成复盘 HTML。后端 review.html 模板页统一渲染 JSON，单独生成 HTML 无用。复盘只需 JSON + saveReview API 入库。

> **v3.9.1 新增**：Step 0 自动版本检查（scripts/check-update.js），每次激活时比对本地与 ClawHub 版本。

> **v3.9.0 新增**：词库覆盖校验（dict_full.json 缺词 = 词卡展开不工作）、saveReview API 入库步骤、answers[] 字段名规范、线上词卡验证步骤。

## When to Activate

- 用户发做题截图/答案，提到"复盘""错题分析""阅读复盘"
- 用户问成绩、分数、进步趋势
- 用户要生成复盘笔记或 PDF

## Step 0a: 运行模式检测 (Auto — Run on Every Activation)

**第一件事**：判断当前是「作者模式」还是「客户端模式」。两种模式行为完全不同，绝不能搞错。

```bash
# 模式判定逻辑（执行下列检测）：
test -f ~/.ssh/workbuddy.pem && grep -q "openclaw-tunnel" ~/.ssh/config 2>/dev/null && echo "作者机" || echo "客户端机"
```

| 信号 | 模式 | 行为 |
|---|---|---|
| 检测到 `~/.ssh/workbuddy.pem` + `openclaw-tunnel` SSH 别名 | **作者模式** | Step 7 走完整 SSH 部署链路（gzip 流、cat 管道、systemctl restart） |
| 找不到上述凭据，但有 `IELTS_USER_TOKEN` 环境变量 | **客户端模式** | Step 7 跳过所有 SSH 操作，只走 HTTPS batchImport 入库 |
| 都没有 | **未配置客户端模式** | 提示用户先配 `IELTS_USER_TOKEN`（详见客户端 onboarding 章节），然后切到客户端模式 |

**模式横幅必须输出**（每次激活时）：

```
🎯 IELTS Reading Review · vX.Y.Z
🔐 运行模式：作者模式 / 客户端模式
👤 token 主体：dengjiawei / lishuzhuo / (匿名)
```

**作者模式与客户端模式的关键差异**（必读）：

| 步骤 | 作者模式 | 客户端模式 |
|---|---|---|
| Step 7a 词库覆盖校验 | ✅ 必跑（要部署 dict_full.json） | ⏭️ 跳过（词库由作者维护，客户端无写权限） |
| Step 7b 部署 site/reviews/ JSON | ✅ SCP 到服务器 | ⏭️ 跳过（batchImport 已写入数据库） |
| Step 7b 部署 dict_full.json + synonym_data.json | ✅ gzip 流推送 | ⏭️ 跳过 |
| Step 7c saveReview API | ✅ ssh + localhost:3100 | ⏭️ 改用 batchImport（HTTPS + token） |
| Step 7d 后端代码部署 | ✅ 必要时执行 | 🚫 严禁触碰 |
| Step 7e 后端重启 | ✅ systemctl restart | 🚫 严禁触碰 |
| Step 7g 入库回查 | ✅ getReviews 校验 | ✅ getReviews 校验（HTTPS） |
| 本地保存 JSON | ✅ `site/reviews/` | ✅ 用户自选目录（如 `~/Documents/雅思复盘/`） |

> **客户端模式下绝对禁止**：执行 `ssh openclaw-tunnel`、`scp`、`gzip -c | ssh`、`systemctl restart`、修改 `/var/www/ielts/` 任何文件。

## Step 0b: Version Check (Auto — Run on Every Activation)

**每次 Skill 被激活时，第一件事必须显式输出当前版本横幅**：

```bash
node ~/.workbuddy/skills/ielts-reading-review/scripts/check-update.js
```

**强制行为规范**：
1. **必须把 check-update.js 的输出原样展示给用户**（包含本地版本号 + 远程版本号），不能省略
2. 如果输出包含 `🆕 有新版本可用` → **立即提示用户并询问是否更新**：
   ```
   ⚠️ ielts-reading-review 有新版本 vX.Y.Z（当前 vA.B.C），强烈建议先更新再开始复盘。
   现在更新？
   ```
3. 用户同意后执行 `node ~/.workbuddy/skills/ielts-reading-review/scripts/check-update.js --auto`，等待安装完成后**让用户重新激活 Skill**（已加载的 context 不会热更）
4. 用户拒绝更新 → 在回复开头加红字告警：`⚠️ 正在使用旧版本 vA.B.C，可能错过 v5.0+ 的简化流程`

> 如果 `check-update.js` 不存在（旧版本安装），跳过版本检查继续工作。
> **绝对禁止**：不输出版本号、隐瞒版本差距、用户没同意就开始复盘流程。

## Workflow

### Step 1: Collect Input

确保以下信息齐全（缺什么问什么）：

- **来源**：哪本书、哪套题、哪篇（如剑5 Test1 Passage2）
- **原文**或答题上下文
- **正确答案**
- **用户答案**及错题
- **🔴 用时（MUST ASK）**：做题用时（格式 `MM:SS`，如 `28:01`）。**必问项**，不能标"可选"——Web 端进步趋势图依赖此字段。用户若没计时，明确询问"这套大概做了多久"让其估算，别直接跳过
- **可选**：翻译、自我反思

### Step 1b: Screenshot Wrong Answer Protocol (CRITICAL)

**用户发答题截图时必须执行 3 步**：

1. **逐题读截图标记**：识别每题的对/错状态（参考下方多平台标记规则），不能跳题，不能用自己的判断代替截图标记
2. **先报错题清单等确认**：输出"根据截图，错题为 QX/QY/QZ（共N道），请确认"，**确认后才能写分析**
3. **截图标记是唯一真相**：截图 vs 自己判断冲突时，信截图

**禁止**：跳过确认直接写分析、用 answer comparison 覆盖截图标记。

#### 多平台截图标记识别规则

不同 App/平台的答案标记方式各不相同，AI 必须能识别以下所有变体：

| 平台/场景 | 正确标记 | 错误标记 | 额外特征 |
|-----------|---------|---------|---------|
| 官方答题卡手批 | 绿色/✓ | 红色/✗ | 手写批注 |
| **雅思哥 (IELTSBro)** | 绿色圆圈/✓/对号 | 红色圆圈/✗/叉号 | 界面有"答案解析"按钮；题号左侧有状态图标；底部显示得分统计（如 8/13）；可能同时显示"你的答案"和"正确答案"两列 |
| 雅思哥成绩单复制文本 | 格式可能为：`1. D ✓` 或 `Q1: D (正确)` | `2. A ✗ → 正确: C` 或 `Q2: A (错误，正确答案: C)` | 复制文本可能包含：题号、用户答案、对错标记、正确答案 |
| 小站雅思 | 蓝色/✓ | 橙色/✗ | 卡片式布局 |
| 新东方雅思 | 绿色背景 | 红色背景 | 答案对比表格 |
| 剑桥官方 CBT | 显示最终得分 | — | 不逐题标记 |
| 其他 App（通用） | ✓/✔/☑/✅/绿色/蓝色 | ✗/✘/☒/❌/红色/橙色 | — |

**识别策略（按优先级）**：

1. **先找得分统计**：截图中如果有 "8/13"、"得分：8"、"Score: 8/13" 等信息，先记下总分
2. **再找逐题标记**：逐题看状态图标/颜色/符号，判断每题对错
3. **提取用户答案**：如果截图同时显示了用户答案和正确答案，直接记录两列数据
4. **处理模糊情况**：如果某题标记看不清楚，输出 "Q7 标记不确定（看起来像 ✓），请确认"
5. **利用 answer-key 交叉验证**：识别出来源（如 剑5 Test1）后，从 `site/answer-key.json` 读取正确答案，可辅助验证截图识别结果是否合理（但截图仍是第一真相）

**🔴 当截图来自第三方 App 时的特殊处理**：

- **不要假设标记规则**——不同 App 版本可能改 UI，先观察截图整体布局再判断哪个是"对"哪个是"错"
- **看图例/得分摘要**——很多 App 顶部或底部有总分（如 8/13），用它来验证你逐题识别的正确率是否对得上
- **如果实在识别不了**——直接告诉用户："这张截图的标记方式我不太确定，能告诉我哪些题错了吗？或者告诉我你用的是什么 App？"

#### 雅思哥复制文本解析规则

用户可能直接从雅思哥 App 复制答案记录粘贴过来，常见格式：

```
# 格式 A：逐题结果（最常见）
1. TRUE ✓
2. FALSE ✗ (正确答案: NOT GIVEN)
3. NOT GIVEN ✓
4. B ✗ (正确答案: D)
...

# 格式 B：成绩概要
Cambridge 5 Test 1 Reading Passage 1
得分：10/13
错题：Q2, Q7, Q11

# 格式 C：答案对照表
题号 | 我的答案 | 正确答案 | 结果
1    | TRUE     | TRUE     | ✓
2    | FALSE    | NG       | ✗
...
```

**解析要点**：
1. 先识别来源（哪套题哪篇）——从标题/文件名/用户说明中提取
2. 从文本中提取每题的：用户答案 + 对错状态 + 正确答案（如果有）
3. 如果复制文本没有正确答案，从 `site/answer-key.json` 补充
4. 格式不在上述三种之内 → 尽力解析，解析不了就问用户

### Step 2: Generate Review Data JSON (v4.0)

**⚠️ 不再生成复盘 HTML！** 后端 `review.html` 模板页统一渲染 JSON，单独生成 HTML 无用。

直接生成结构化 JSON 文件，供 saveReview API 入库 + 后端 review.html 模板渲染。

**输出文件命名规则**：`剑X-TestX-PassageX-中文主题复盘.json`

示例：
- JSON: `剑5-Test1-Passage2-鲸鱼感官复盘.json`
- `source.titleCN`: `"鲸鱼感官"`

> **命名说明**：文件名使用中文标题（`source.titleCN`），方便用户在文件管理器中一眼识别内容。Web 端导入时通过 JSON 内的 `source.book/test/passage` 识别篇目，不依赖文件名。

**🔴 timing 字段必须填充**：
- `minutes`：数值型分钟（支持小数，如 `28.0` / `35.4`）
- `formatted`：`"MM:SS"` 字符串（如 `"28:01"`）
- MM:SS → minutes 换算：`分钟 + 秒/60`，保留 1 位小数
- 用户实在给不出用时，才能置 `null`，但必须在回复里提醒"缺用时，进步图将缺一个点"

```json
{
  "version": "4.0.0",
  "generatedAt": "2026-04-28T10:00:00.000Z",
  "source": {
    "book": 7,
    "test": 1,
    "passage": 3,
    "title": "English Title",
    "titleCN": "中文标题"
  },
  "score": {
    "correct": 9,
    "total": 14,
    "band": "6.0",
    "breakdown": {
      "fillBlank": { "correct": 4, "total": 6 },
      "tfng": { "correct": 3, "total": 4 },
      "matching": { "correct": 2, "total": 4 }
    }
  },
  "timing": {
    "minutes": 25,
    "formatted": "25:00"
  },
  "date": "2026-04-28",
  "progressNote": "简短进步总评（如'比上次提升2分'）",
  "alertNote": "核心告警信息（如'Summary填空全军覆没'，可选）",
  "answers": [
    { "q": 1, "my": "TRUE", "correct": "TRUE", "result": "correct" },
    { "q": 2, "my": "FALSE", "correct": "NOT GIVEN", "result": "wrong" }
  ],
  "wrongQuestions": [
    {
      "q": 3,
      "type": "tfng",
      "badge": "TFNG",
      "myAnswer": "TRUE",
      "correctAnswer": "NOT GIVEN",
      "errorCategory": "ng-false-confusion",
      "analysis": "错因分析文字",
      "lesson": "教训一句话",
      "quote": "原文引用（英文）",
      "quoteRef": "Para B, Line 3",
      "analysisPoints": ["分析要点1", "分析要点2"],
      "rejectedOptions": [
        { "option": "A", "reason": "原文未提及该关系，属于无中生有" },
        { "option": "C", "reason": "与原文事实矛盾，原文说的是..." },
        { "option": "D", "reason": "范围扩大/信息不匹配" }
      ]
    }
  ],
  "actionItems": [
    "下次做 TFNG 前必须标注否定词",
    "Summary 填空必须三步走"
  ],
  "synonyms": [
    {
      "original": "原文表达",
      "replacement": "题目表达",
      "meaning": "中文释义",
      "questionRef": "Q3"
    }
  ],
  "vocabulary": [
    {
      "word": "exemplify",
      "phonetic": "/ɪɡˈzemplɪfaɪ/",
      "pos": "v.",
      "definition": "举例说明",
      "ieltsFreq": 3,
      "source": "538 #42",
      "appearance": "剑7T1P3"
    }
  ],
  "problems": [
    {
      "type": "同义替换识别失败",
      "detail": "具体表现",
      "questions": "Q3, Q7",
      "improvement": "改进方法"
    }
  ]
}
```

**v4.0 相对 v3.0 新增字段**（均可选，v3.0 JSON 仍能被模板页渲染）：
- `progressNote`：进步总评
- `alertNote`：告警信息
- `answers[]`：全部答案对照表（含 result: correct/wrong/skipped）
- `actionItems[]`：行动清单
- `wrongQuestions[].badge`：**错误分类**简写标签（如 "NG/FALSE混淆"、"过度推理选TRUE"、"Summary填空定位错误"），与 `type`（题型）区分开
- `wrongQuestions[].quote` / `quoteRef`：原文引用 + 定位
- `wrongQuestions[].analysisPoints[]`：分析要点列表
- `wrongQuestions[].rejectedOptions[]`：**选择题和判断题专用**——为什么不选其他选项。仅 `type === "multipleChoice"` 或 `type === "tfng"` 时填写。数组每项 `{ option: "A", reason: "原因..." }`（选择题用 A/B/C/D，判断题用 Y/N/NG），列出除正确答案外所有错误选项的排除理由。review.html 会以红色边框卡片渲染（标题"为什么不选"，每个选项带圆圈字母+排除原因）

**🔴 wrongQuestions 中 type 与 badge 的区别（MUST FOLLOW）**：
- `type`：**题型**标识，使用标准 ID（`tfng` / `fillBlank` / `summary` / `multipleChoice` / `matching` / `heading` / `sentenceCompletion`）
- `badge`：**错误分类**标签（如 "NG/FALSE混淆"、"过度推理"、"Summary填空没回原文"）
- 两者含义不同，**禁止互相赋值**。旧格式 JSON 中 `error_analysis` 只有 `error_type`（错误分类），没有题型信息，review.html 会从 `questions[]` 交叉获取题型

**🔴 answers[] 字段名规范（MUST FOLLOW）**：

`answers` 数组中每条记录的字段名**必须**严格使用以下格式：
```json
{ "q": 1, "my": "TRUE", "correct": "TRUE", "result": "correct" }
```
- `my`：用户答案（不是 `myAnswer`）
- `correct`：正确答案字符串（不是布尔值）
- `result`：`"correct"` / `"wrong"` / `"skipped"`（字符串，不是布尔值）

> **注意**：`wrongQuestions[]` 里用的是 `myAnswer` / `correctAnswer`（全拼），和 `answers[]` 的缩写不同。这是历史设计，review.html 模板已做兼容处理，两种格式都能正确渲染。

### Step 3b: Bilingual Data (v5.0 — 已预置，无需操作)

> **⚠️ v5.0 变更（2026-05-11）**：服务端已预置 C4-C20 100 篇核心双语数据，复盘流程**不再需要**生成或维护 bilingual_data.json。
>
> 仅以下场景需要扩展：
> - 复盘 C20 之后的新书（C21+）
> - 用户明确要求为某篇生成精翻双语
>
> 默认跳过此步骤。

#### ~~3b-2: 双语 HTML 文件~~（已废弃）

> **v3.8 起不再需要**。旧 `bilingual/*.html` 已清理，Web 端通过 `bilingual.html` 模板页动态加载 `bilingual_data.json` 渲染。

### Step 4: Generate PDF (Optional — Rarely Used)

如果用户明确需要 PDF，可从线上复盘页面打印。本地不再生成 HTML，因此也不支持 puppeteer PDF 生成。

### Step 5: Update Memory

复盘完成后更新 working memory：新增的错误模式、词汇、成绩数据。

### Step 6: Apply to Web (Automatic — saveReview API)

复盘 JSON 生成后，**必须立即通过 saveReview API 入库**（Step 7c），不需要用户手动操作。

完成后输出：

---

📤 **复盘完成！**

JSON 已入库，线上查看 👉 [review.html?file=剑X-TestX-PassageX-主题复盘.json](https://www.liuxue.online/ielts/review.html?file=剑X-TestX-PassageX-主题复盘.json)

---

#### 其他同步方式（备选）

**方式 B：Skill 伴侣脚本**（私有部署场景）

如果有 `ielts-server-sync` skill（个人专用），可命令行批量上传：

```bash
# 单文件上传
node ~/.workbuddy/skills/ielts-server-sync/scripts/upload.js 剑5-T1-P2.json

# 批量上传目录
node ~/.workbuddy/skills/ielts-server-sync/scripts/upload.js --batch ./reviews/
```

**方式 C：手动上传**

打开 [submit.html?mode=json](https://www.liuxue.online/ielts/submit.html?mode=json) 拖入 JSON 文件。

### Step 7: Deploy Checklist (MANDATORY — DO NOT SKIP)

**🔴 每次复盘完成后，必须逐项执行以下检查清单。不能靠记忆，必须逐条过。**

**🔀 先看 Step 0a 模式横幅，按模式走对应分支**：
- **作者模式** → 走下面的 7a-7g 完整部署链路
- **客户端模式** → 跳到本节末尾的「Step 7-Client」客户端简化流程，**不要碰 7a-7g 的 SSH 操作**

---

#### 7a. 本地文件归位（仅作者模式）

- [ ] 复盘 JSON 已复制到 `site/reviews/`
- [ ] `generate_vocab_synonym.py` 已运行，更新 dict_full.json + synonym_data.json
- [ ] **🔴 词库覆盖校验（MUST — 否则词卡展开不工作）**：运行以下检查，确保本篇所有 vocabulary 词汇都在 `dict_full.json` 中有完整条目（含 meaning_cn + examples）

> **v5.0 变更**：~~answer-key.json 更新~~ 和 ~~bilingual_data.json 更新~~ 已从清单中移除。服务端已预置 C4-C20 全量数据，复盘流程无需再维护这两个文件。复盘 C21+ 时才需要扩展 answer-key（参考末尾「扩展新书」章节）。

```python
# 词库覆盖校验（复盘生成后必跑）
import json
with open('site/dict_full.json') as f:
    dmap = {w['word'].lower(): w for w in json.load(f) if 'word' in w}
with open('site/reviews/剑X-TestX-PassageX-主题复盘.json') as f:
    vocab = json.load(f).get('vocabulary', [])
missing = [v['word'] for v in vocab if v['word'].lower() not in dmap]
if missing:
    print(f'❌ dict_full.json 缺失 {len(missing)} 词：{missing}')
    print('→ 必须补充这些词（含 meaning_cn/examples/synonyms）后再部署')
else:
    print('✅ 词库覆盖完整')
```

如果有缺失词：**立即补充到 dict_full.json**（每词需含 meaning_cn、phonetic、root、examples、synonyms、antonyms），补完重新部署。
**绝不能跳过此步**——缺词 = 线上词卡点击无响应 = 用户体验崩坏。

#### 7b. 部署到线上

**v5.0 精简后只需部署以下 3 个文件**（answer-key/bilingual 已服务端预置）：

```
site/reviews/剑X-TestX-PassageX-主题复盘.json    → /var/www/ielts/reviews/
site/dict_full.json                              → /var/www/ielts/
site/synonym_data.json                           → /var/www/ielts/
```

**🔴 大文件传输规则（>1MB 用 gzip 流，不要分块！）**：

大于 1MB 的文件（如 dict_full.json ~6MB）**禁止直接 SCP，禁止 split 分块**，必须用 gzip 管道一行秒传：

```bash
# 🔴 唯一正确方式：gzip 流 + 先落临时文件再 mv（原子写，防止中途断流留下 0 字节空文件）
gzip -c site/dict_full.json | ssh openclaw-tunnel "gunzip > /var/www/ielts/dict_full.json.tmp && mv /var/www/ielts/dict_full.json.tmp /var/www/ielts/dict_full.json"

# 验证完整性（🔴 必须显式加 encoding='utf-8'，否则服务器 locale 非 UTF-8 时会误报 UnicodeDecodeError）
ssh openclaw-tunnel "python3 -c \"import json; d=json.load(open('/var/www/ielts/dict_full.json', encoding='utf-8')); print(f'OK: {len(d)} words')\""
```

> **⚠️ 教训（2026-06-23）**：直接 `gunzip > 目标文件` 若管道中途失败，会把目标文件清成 0 字节（覆盖了原好文件）。务必走 `.tmp` + `mv` 原子替换，验证报错时也只丢临时文件。

> **⚠️ 教训（2026-06-23 二）**：服务器 `python3 open()` 不指定 `encoding='utf-8'` 时会按系统 locale 解码，含中文的 dict_full.json 会抛 `UnicodeDecodeError`，让人误以为文件损坏。验证 JSON 一律加 `encoding='utf-8'`。文件大小本地/服务器一致(`wc -c`)即证明传输无误，别被解码报错骗了。

> **⚠️ 历史教训**：split 分块传输复杂且易出错（分批 SCP 超时、拼合顺序错乱），已于 2026-05-08 彻底弃用。gzip 流利用 SSH 隧道的持久连接，一次性完成压缩传输，稳定可靠。

**小文件（<1MB）仍可直接 SCP**：
```bash
scp -o ConnectTimeout=15 \
    -o StrictHostKeyChecking=accept-new \
    -o UserKnownHostsFile=~/.ssh/known_hosts_cfd \
    -o "ProxyCommand=/Users/dengjiawei/bin/cloudflared access tcp --hostname ssh.tuyaya.online" \
    -i ~/.ssh/workbuddy.pem \
    <本地文件> ubuntu@ssh.tuyaya.online:/var/www/ielts/
```

**或用 SSH stdin 管道（<500KB 的文件最快）**：
```bash
ssh openclaw-tunnel "cat > /var/www/ielts/synonym_data.json" < site/synonym_data.json
```

#### 7c. saveReview API 入库（MANDATORY）

复盘数据必须写入后端数据库，否则首页进度图看不到这篇：

```bash
ssh openclaw-tunnel 'python3 -c "
import json, urllib.request
payload = json.dumps({
    \"action\": \"saveReview\",
    \"token\": \"<USER_TOKEN>\",
    \"book\": X, \"test\": Y, \"passage\": Z,
    \"score\": <correct>, \"total\": <total>, \"duration\": <minutes>,
    \"date\": \"YYYY-MM-DD\",
    \"answers\": {}
})
req = urllib.request.Request(\"http://localhost:3100/api/ielts\", data=payload.encode(), headers={\"Content-Type\": \"application/json\"})
resp = urllib.request.urlopen(req)
print(resp.read().decode())
"'
```

> API 路径是 `POST /api/ielts`，通过 `action` 字段分发（不是 `/api/ielts/saveReview`）。

#### 7d. 后端代码部署（仅当 server/index.js 有改动时）

如果本次涉及 server 代码变更，需同步后端：

```bash
# 后端小文件可直接 stdin 传
ssh openclaw-tunnel "cat > /home/ubuntu/ielts-api/index.js" < server/index.js

# 新增的 lib/ 目录
ssh openclaw-tunnel "mkdir -p /home/ubuntu/ielts-api/lib"
ssh openclaw-tunnel "cat > /home/ubuntu/ielts-api/lib/llmExtractor.js" < server/lib/llmExtractor.js
ssh openclaw-tunnel "cat > /home/ubuntu/ielts-api/lib/schemaUpgrader.js" < server/lib/schemaUpgrader.js
ssh openclaw-tunnel "cat > /home/ubuntu/ielts-api/lib/tencentOcr.js" < server/lib/tencentOcr.js

# 如有新 npm 依赖
ssh openclaw-tunnel "cd /home/ubuntu/ielts-api && npm install"
```

**🔴 部署红线**：
- **严禁覆盖 `/etc/systemd/system/ielts-api.service`**——里面有 AI_API_URL/KEY/MODEL 等生产密钥
- 新密钥只通过 drop-in 追加：`/etc/systemd/system/ielts-api.service.d/secrets.conf`
- 详见 `.workbuddy/upload-upgrade-ops.md`

#### 7e. 后端重启

```bash
ssh openclaw-tunnel "sudo systemctl restart ielts-api"
```

**必须重启**——后端启动时 `buildReviewFileIndex()` 扫描 `reviews/` 目录建索引。不重启 = 新文件不出现在首页。

#### 7f. 线上验证

- [ ] `getReadingPageData` API 返回新篇目数据（`POST /api/ielts` + `action: getReadingPageData`）
- [ ] 复盘链接可正常访问：`review.html?file=剑X-TestX-PassageX-主题复盘.json`
- [ ] **🔴 词卡展开验证**：打开复盘页面，点击词汇表中至少 1 个词，确认能弹出详情卡（含释义/例句/近义词）。如果点击无反应 → dict_full.json 缺词，回 7a 补词
- [ ] （v5.0 已预置）双语数据 C4-C20 已服务端预置，无需逐篇验证；C21+ 新书需手动确认 `bilingual.html?book=X&test=Y&passage=Z`

#### 7g. 🔴 强制入库回归验证（v5.1 新增 — 防止 saveReview 漏调）

**血泪教训（2026-05-11）**：复盘 JSON 部署成功了，但 saveReview API 没调通，导致首页看不到新篇。**部署 ≠ 入库**，必须**回查数据库**验证。

完成 7c 后必须立即执行以下检查：

```bash
# 用 getReviews 回查本篇是否真的入库（替换 BOOK/TEST/PASSAGE）
curl -s https://www.liuxue.online/api/ielts -H 'Content-Type: application/json' \
  -d '{"action":"getReviews","token":"<USER_TOKEN>","book":<BOOK>,"test":<TEST>}' \
  | python3 -c "
import json,sys
d = json.load(sys.stdin)
records = [r for r in d.get('data',[]) if r['book']==<BOOK> and r['test']==<TEST> and r['passage']==<PASSAGE>]
if records:
    print('✅ 入库成功:', records[0])
else:
    print('❌ 入库失败！必须重新调 saveReview API')
    sys.exit(1)
"
```

**如果验证失败**：立即重新调 saveReview API，再回查，直到 ✅。**绝对不能跳过此步**——本步骤 PASS 才算复盘真正完成。

**曾犯的典型遗漏**（引以为戒）：
1. 文件生成在根目录没 cp 到 site/reviews/
2. 没重启后端导致 review 索引没刷新
3. JSON 文件没 SCP 到 reviews/
4. **dict_full.json 缺词导致词卡展开不工作**——复盘新增词汇不在词库中，必须做词库覆盖校验
5. **没调 saveReview API 导致首页进度图缺数据**——文件部署 ≠ 数据入库，两者都要做
6. **answers[] 用了错误字段名**——必须用 `my`/`correct`(字符串)/`result`(字符串)，不能用布尔值
7. **不要生成复盘 HTML**——后端 review.html 模板统一渲染 JSON，单独生成 HTML 无用
8. **dict_full.json 大文件传输用 gzip 流**——禁止 split 分块（复杂且易错），一行 `gzip -c | ssh gunzip >` 搞定
9. **旧格式 JSON 错题重复渲染**——`questions[]` 和 `error_analysis[]` 都有错题时，review.html 会去重。但生成 v4.0 JSON 时应**只用 wrongQuestions[]**，不要同时写两种格式
10. **type/badge 混用导致标签重复**——`type` 是题型（tfng/fillBlank），`badge` 是错误分类（NG/FALSE混淆）。禁止互相赋值

---

## Step 7-Client: 客户端模式部署流程（NO SSH）

**何时走这条**：Step 0a 检测到「客户端模式」（如老婆机器、外部用户机器）。

**核心原则**：客户端没 SSH 凭据、没 `/var/www/ielts/` 写权限，**只能通过 HTTPS 接口写数据库**。词库、模板、双语数据全部由作者机维护，客户端不参与。

### 7-Client-a. 本地保存 JSON

让用户选个保存目录（推荐 `~/Documents/雅思复盘/` 或当前工作目录的 `reviews/`），把生成的 JSON 写进去。**不要往 `site/reviews/` 写**——客户端没这个目录或者目录是别人的。

### 7-Client-b. 通过 batchImport 入库（替代 saveReview）

batchImport 是带 token 的官方 HTTPS 通道，能吃 v4.0 富 JSON（服务端 schemaUpgrader 自动转换扁平字段写入），最适合客户端：

```bash
# 单篇上传（推荐用 review-upload skill 的脚本）
bash ~/.workbuddy/skills/ielts-review-upload/scripts/sync-review.sh \
  ~/Documents/雅思复盘/剑X-TestX-PassageX-主题复盘.json
```

或者直接 curl：

```bash
TOKEN="$IELTS_USER_TOKEN"  # 从环境变量读
JSON_FILE="~/Documents/雅思复盘/剑X-TestX-PassageX-主题复盘.json"

PAYLOAD=$(python3 -c "
import json, sys
with open(sys.argv[1]) as f:
    review = json.load(f)
print(json.dumps({
    'action': 'batchImport',
    'token': sys.argv[2],
    'reviews': [review]
}, ensure_ascii=False))
" "$JSON_FILE" "$TOKEN")

curl -s -X POST https://www.liuxue.online/api/ielts \
  -H 'Content-Type: application/json' \
  -d "$PAYLOAD"
```

预期返回：
```json
{"code":0,"message":"导入完成：1 条成功，0 条跳过","data":{"imported":1,"skipped":0,"upgraded":1}}
```

`upgraded:1` 表示服务端识别到 v4.0 富格式并跑了 schemaUpgrader。

### 7-Client-c. 入库回查（必做）

```bash
curl -s https://www.liuxue.online/api/ielts \
  -H 'Content-Type: application/json' \
  -d "{\"action\":\"getReviews\",\"token\":\"$IELTS_USER_TOKEN\",\"book\":<BOOK>,\"test\":<TEST>}" \
  | python3 -m json.tool | head -30
```

确认返回的 data 数组里有刚上传那篇（`book`/`test`/`passage` 三元组匹配），并且 `username` 是登录账号（如 `lishuzhuo`），不是 `dengjiawei`。

### 7-Client-d. 给用户的最终输出

```
✅ 复盘已入库

📊 在主页查看进度图、词汇本、错题本：
👉 https://www.liuxue.online/ielts/reading.html
   （登录账号：<username>）

📄 复盘详情页：
👉 https://www.liuxue.online/ielts/review.html?file=剑X-TestX-PassageX-主题复盘.json
```

> **客户端模式注意**：复盘详情页 `review.html?file=...` 依赖服务端 `/var/www/ielts/reviews/` 下的 JSON 文件。客户端模式只把数据写进数据库，**不上传 JSON 文件到服务器**，所以详情页可能 404。但首页进度图、词汇本、错题本能正常工作（这些数据都从数据库读）。
>
> 如果用户特别想要详情页可访问，提醒他把 JSON 发给作者人工部署，或者作者机用 `ielts-server-sync` skill 同步。

### 7-Client 红线（绝对禁止）

- 🚫 `ssh openclaw-tunnel ...`
- 🚫 `scp ... ubuntu@ssh.tuyaya.online:...`
- 🚫 `gzip -c | ssh openclaw-tunnel "gunzip > /var/www/..."`
- 🚫 `sudo systemctl restart ielts-api`
- 🚫 修改 `dict_full.json` / `synonym_data.json` / `bilingual_data.json` / `answer-key.json` 后试图部署
- 🚫 部署 `site/reviews/` 下的 JSON 文件到服务器

**客户端只做两件事**：本地存 JSON + HTTPS batchImport 入库。

### 7-Client onboarding（首次配置）

如果用户首次跑客户端模式，缺 `IELTS_USER_TOKEN`，按以下流程引导：

1. 浏览器登录 https://www.liuxue.online/ielts/login.html
2. F12 打开 DevTools → Console
3. 输入 `localStorage.token`，回车，复制返回字符串（一长串 base64）
4. 在 `~/.zshrc` 末尾加：
   ```bash
   export IELTS_USER_TOKEN='粘贴token'
   ```
5. `source ~/.zshrc` 或重开终端
6. 验证：`echo "${IELTS_USER_TOKEN:0:20}..."` 应输出前 20 个字符

token 默认有效期 10 年，配一次基本一劳永逸。

## 扩展新书（C21+）

服务端预置数据仅覆盖 C4-C20。复盘剑21及以后的书时，需要额外做：

1. 在 `site/answer-key.json` 追加条目（格式：`C{book}-T{test}-R{passage}`，**R 不是 P**）
2. SCP 到 `/var/www/ielts/answer-key.json`
3. （可选）追加 `site/bilingual_data.json` 并 SCP
4. 重启后端：`ssh openclaw-tunnel "sudo systemctl restart ielts-api"`

C4-C20 范围内的复盘**不需要**这一步。

## Batch Import Mode (v3.8 — Legacy Review Folder → JSON)

**触发场景**：用户说"帮我把 XX 目录下的历史复盘都转成 JSON"、"批量导入我以前的复盘笔记"、"扫一下我电脑里的复盘"、"帮我找出所有历史笔记"等。

此模式下 Buddy 自主循环，**无需用户自己找路径、无需一篇篇喂**。

### Step B0: Auto-Discovery（🔍 推荐默认起点）

**不要开口就问用户"复盘文件夹在哪？"**——先自动扫常见位置：

```bash
node ~/.workbuddy/skills/ielts-reading-review/scripts/scan-legacy-reviews.js --auto
```

脚本会扫描以下位置并按命中数推荐：
- 当前工作目录 (cwd)
- `~/Documents`、`~/Documents/个人`、`~/Documents/个人/WorkBuddy`
- `~/Desktop`、`~/Downloads`
- `~/Library/Mobile Documents/com~apple~CloudDocs`（iCloud）
- `~/WorkBuddy`、`~/WorkBuddy/Claw`

输出 `discoveries`（去重后的真实命中目录，命中数多的子目录优先）和 `recommended`（首选目录）。

**把发现结果呈现给用户**：

```
我扫了你电脑常见位置，找到你的复盘应该在这里：

🎯 推荐：/Users/xxx/Documents/个人/WorkBuddy/雅思学习（60 个候选文件）
   样例：剑6-Test3-Passage3-抗衰老药物复盘.html / 剑4-Test1-听力Part2-河滨工业村复盘.html …

其他候选：
  - /Users/xxx/Downloads（4 个）

要用推荐目录还是选其他的？
```

用户点头后进入 Step B1 做精扫。**只有当自动发现完全找不到候选（discoveries 为空）时**，才问用户要具体路径。

### Step B1: Scan the Folder

调用扫描脚本生成候选清单：

```bash
# 默认只扫顶层
node ~/.workbuddy/skills/ielts-reading-review/scripts/scan-legacy-reviews.js <目录> --out=/tmp/ielts-scan.json

# 需要递归子目录
node ~/.workbuddy/skills/ielts-reading-review/scripts/scan-legacy-reviews.js <目录> --deep --out=/tmp/ielts-scan.json
```

输出 JSON 结构（groups 按篇目聚合）：

```json
{
  "totalFiles": 18,
  "identifiedPassages": 6,
  "groups": [
    {
      "passage": "C5-T1-P2",
      "fileCount": 3,
      "files": [
        { "path": "...", "ext": ".html", "hints": { "book": 5, "test": 1, "passage": 2, "title": "鲸鱼感官" } },
        { "path": "...", "ext": ".md" },
        { "path": "...", "ext": ".png" }
      ]
    },
    { "passage": "__unknown__", "files": [...] }
  ]
}
```

### Step B2: Show Plan & Confirm

读取 scan 结果后，**必须先给用户一份执行计划**，不要直接开干：

```
扫描完成，找到 18 个候选文件，识别出 6 篇复盘：

✅ 可识别：
  1. 剑5-T1-P2 · 鲸鱼感官（HTML + MD + 截图，共 3 个文件）
  2. 剑5-T1-P3 · 儿童认知（HTML）
  3. 剑6-T2-P1 · ...
  ...

⚠️ 无法识别篇目（需你人工分配）：
  - notes-2026-03-15.md
  - 错题整理.docx

我将逐篇处理可识别的 6 篇，每篇生成一个 JSON。预计 10-15 分钟。
确认开始？
```

用户点头后才进入 Step B3。

### Step B3: Loop — Generate JSON for Each Passage

**逐篇循环**，每次处理一组：

1. 读取该组所有文件内容（HTML 提纯文字、MD 直读、图片用视觉 OCR）
2. 从内容中提取：原文/正确答案/用户答案/错题/时长/日期
3. **关键兜底**：
   - 内容里找不到"正确答案" → 查 `site/answer-key.json`（本地答案库，401 题全覆盖）
   - 找不到用户答案 → 标注 `score.correct = null` 让用户后续补
   - 错题列表不清晰 → 只生成基础成绩单 JSON，`wrongQuestions: []`
4. 按 v4.0 schema 生成 JSON（v3.0 新增字段可选），文件名 `剑X-TestX-PassageX-中文主题复盘.json`
5. 写入用户指定的输出目录（默认 `./batch-output/`）
6. 输出一行进度：`✅ [3/6] 剑5-T1-P3 · 儿童认知 → 剑5-Test1-Passage3-儿童认知复盘.json`

### Step B4: Summary Report

全部完成后输出总结：

```
批量导入完成！

✅ 成功：5 篇（已生成 5 个 JSON 到 ./batch-output/）
⚠️ 部分数据缺失：1 篇（剑6-T2-P1 找不到用户答案，score.correct 置空）
❌ 跳过：0 篇

下一步：
👉 打开 https://www.liuxue.online/ielts/submit.html?mode=json
👉 把 ./batch-output/ 里所有 JSON 拖进去，一键导入
```

### Batch Mode Rules (MUST FOLLOW)

1. **永远先 scan + confirm，绝不跳过计划确认**
2. **每篇独立处理，失败不阻塞下一篇**（捕获异常，记录到 skip 列表）
3. **绝不编造数据**：用户答案缺失就置 null 或空数组，不要瞎填
4. **同义替换/词汇/错因分析是可选项**：老笔记里没有就不生成，不要硬凑
5. **答案库优先**：正确答案一律从 `site/answer-key.json` 核对，笔记里的可能是老婆写错的
6. **产物隔离**：批量输出统一放 `./batch-output/`，不污染用户工作目录

## Error Analysis Rules

### TRUE / FALSE / NOT GIVEN 三步法

1. **找话题** — 文章有没有讨论题目中的对象？→ 没讨论 = **NOT GIVEN**
2. **找立场** — 讨论了的话，是同意还是矛盾？→ **TRUE** / **FALSE**
3. **验证** — "如果选 TRUE/FALSE，能指出原文哪句话吗？" 指不出来 → 大概率 **NOT GIVEN**

关键区分：
- FALSE 需要**直接矛盾证据**，"没提到"= NG 不是 FALSE
- 概括性表达覆盖题目对象 = 算讨论过，不是 NG
- `however + adj` = `no matter how`（让步），不是因果

### Fill-in-the-blank

- 答案不能重复题干已有的词
- 填完必须通读：语法/词性/语义/字数 四项检查
- `such as ___` → 必须填具体例子
- `the ___ of X` → 必须填能和 "of X" 搭配的名词

### Common Pitfalls

- **过度推理**：只看作者明确写了什么，不推导
- **被绝对词吓到**：all/never 不一定错，看原文证据
- **人名观点混淆**：先在文中标注每个人说了什么
- **邻近干扰词**：从定位句提取答案，不要被旁边的句子污染
- **Heading 复用 Example**：做 Heading 题第一步永远是划掉 Example 已用的选项
- **Although 从句看错重点**：主句才是作者立场，让步从句只是背景
- **双重否定读反了**：not unusual=usual, not uncommon=common, rarely+isn't=几乎总是。看到双重否定立刻翻译成肯定
- **Summary 填空凭感觉**：必须先回原文找对应句，再从选项中匹配。不回原文 = 全靠蒙
- **对比信号词忽略**："difference from X" 本身就是对比框架，后面的内容就是证据
- **选择题选了和全文论点相反的**：选完后反问"这个选项和作者核心主张一致吗？"
- **段落匹配被信息密度干扰**：题目问 "term"（定义），选了有数字的段落而非有 "refer to as" 的段落。精确锁定每个关键词含义
- **Summary 填空近义词混用**：同段落两个近义表达，看题目限定词（如 Britain）对应原文哪个子语境
- **Summary 填空专有名称不完整**：看到引号/大写开头名称，先数字数，限制内写全称不缩写

## Error Categories

参见 `references/error-taxonomy.md`，共 18 类错误分类。JSON 中 `errorCategory` 字段使用以下 ID：

| ID | 错误类型 |
|----|---------|
| `synonym-failure` | 同义替换识别失败 |
| `ng-false-confusion` | NOT GIVEN / FALSE 混淆 |
| `over-inference` | 过度推理 |
| `stem-repetition` | 填空重复题干词 |
| `grammar-mismatch` | 语法/让步句理解错 |
| `incomplete-option` | 选项不完全匹配 |
| `vocab-gap` | 词汇缺口 |
| `carelessness` | 粗心/时间压力 |
| `word-form-error` | 填空词形/词性错 |
| `scope-confusion` | 跨代/范围混淆 |
| `category-reasoning` | 类别推理误判 |
| `adjacent-distractor` | 邻近干扰词 |
| `heading-example-reuse` | Heading匹配复用Example已用选项 |
| `concessive-clause-confusion` | Although/While让步从句混淆主句 |
| `double-negative-misread` | 双重否定读不出肯定 |
| `summary-no-source` | Summary填空没回原文定位 |
| `comparison-signal-ignored` | 对比信号词(difference from等)忽略 |
| `selection-contradicts-thesis` | 选择题选了和全文论点矛盾的选项 |

## Style Guidelines

- 简洁直接，不废话
- 错题分析直说问题，不糖衣炮弹
- 中文为主，英语术语保留原文

## 🔴 Step 8: Final Gate (v5.5.2 — Mandatory before any ending)

**任何复盘对话，在你即将给出收尾回复（"复盘完成 / 总结 / 错题分析全部跑完"）之前，必须先逐条过完以下 4 个 Gate。任何一条 ❌ 一律返回继续干，禁止结束。**

| Gate | 自检问题 | 判定来源 |
|---|---|---|
| **Gate 1** | 我有没有为本次每一篇生成 v4.0 富 JSON 写到 `site/reviews/`？ | `ls site/reviews/` 看到对应文件 |
| **Gate 2** | 我有没有调 `saveReview`（作者模式）或 `upload.js`/`batchImport`（客户端模式）？ | 看上面命令的返回值是 `success/code:0` |
| **Gate 3** | 我有没有用 `getReviews` 回查确认入库 ✅？ | 回查 JSON 里有匹配 book/test/passage 的 record |
| **Gate 4** | 我有没有把线上链接（`www.liuxue.online/ielts/review.html?file=...`）写进给主人的最终回复？ | 检查最终回复文本 |

**自检模板（在收尾前内部默念一遍）：**

```
Gate 1: site/reviews/剑X-TestX-PassageX-主题复盘.json  ✅ / ❌
Gate 2: saveReview / upload.js  ✅ / ❌
Gate 3: getReviews 回查命中  ✅ / ❌
Gate 4: 最终回复包含线上链接  ✅ / ❌
```

**若任意一条 ❌**：立即回到对应 Step 补做，绝不允许"先交付文字版，再说"。

**作者机一键回查命令（复制即用）：**

```bash
TOKEN=$(cat ~/.ielts-tuyaya-token | python3 -c "import json,sys; print(json.load(sys.stdin)['token'])")
curl -s 'https://www.liuxue.online/api/ielts' -H 'Content-Type: application/json' \
  -d "{\"action\":\"getReviews\",\"token\":\"$TOKEN\",\"book\":<BOOK>,\"test\":<TEST>}" \
  | python3 -c "import json,sys; d=json.load(sys.stdin); recs=[r for r in d.get('data',[]) if r['book']==<BOOK> and r['test']==<TEST>]; print('✅ 已入库篇目:', [(r['passage'], r['score'], r['total']) for r in recs])"
```

**若主人对话里只发了某一两篇阅读题**：完成那几篇的 4 个 Gate 即可，不要扩展到整个 Test。

**若做完一篇主人立刻发下一篇**：先把当前篇 4 Gate 全过 ✅，再开下一篇。绝对不允许积压。

> 这道 Gate 是 v5.5.2 的灵魂。其他所有 step 都可以小幅偷懒，唯独这道 Gate 必须 100% 过完。

## 客户端模式参考

外部用户/老婆机器首次配置看这里：[`references/CLIENT_MODE_ONBOARDING.md`](references/CLIENT_MODE_ONBOARDING.md)

一键脚本：`bash ~/.workbuddy/skills/ielts-reading-review/scripts/setup-client-mode.sh`
