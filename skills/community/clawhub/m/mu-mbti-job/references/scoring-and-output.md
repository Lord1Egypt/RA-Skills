# 计分与输出技术细节

Agent 在计分、出报告、使用网页模式前读取本文件。SKILL.md 只管流程，本文件管契约。

## 1. 答案 JSON 完整格式

用户答题完毕后，AI 助手整理成如下格式写入临时文件（如 `./answers_<timestamp>.json`）：

```json
{
  "version": "standard",
  "language": "zh",
  "started_at": "2025-01-01T10:00:00",
  "finished_at": "2025-01-01T10:16:30",
  "answers": [
    {"id": 1, "choice": "A"},
    {"id": 2, "choice": "B"}
  ]
}
```

字段说明：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| version | string | 是 | quick / standard / pro，须与实际抽题版本一致 |
| language | string | 否 | zh / en，答题界面语言，默认 zh |
| started_at / finished_at | string | 否 | ISO 8601，仅记录用 |
| answers | array | 是 | 每条含 id（题库中的题目 id）与 choice（"A" 或 "B"） |

三个版本的示例片段：

```json
// quick（70 题，id 集为 version_added <= quick 标记的题目）
{"version": "quick", "answers": [{"id": 3, "choice": "A"}, {"id": 17, "choice": "B"}]}

// standard（93 题）
{"version": "standard", "answers": [{"id": 3, "choice": "A"}, {"id": 88, "choice": "B"}]}

// pro（144 题，全量超集）
{"version": "pro", "answers": [{"id": 3, "choice": "A"}, {"id": 140, "choice": "B"}]}
```

**关键**：`id` 必须是 `./data/questions.json` 中的题目 id 原值，`choice` 必须是用户所选项的 "A"/"B" 原值。score.py 凭 id 回查题库获取该题的计分维度与方向。

## 2. score.py 输入输出契约

```bash
python3 scripts/score.py <answers.json> [output.json]
```

- 输入：answers.json（上述格式）；第二参数可选，缺省输出 `./result.json`。
- 输出：result.json（见下）+ stdout 摘要（类型代码、四维百分比）。

**退出码**：

| 退出码 | 含义 | 排查方向 |
|---|---|---|
| 0 | 成功 | 正常读取 result.json |
| 2 | 题库校验失败 | data/questions.json 被改动/损坏/缺失计分键；确认未违反铁律 4 |
| 3 | 答案异常 | answers 缺字段、id 不在所选版本题集、choice 非 A/B、题数与版本不符（缺答/多答） |

### result.json 字段逐个说明

| 字段 | 类型 | 说明 |
|---|---|---|
| version | string | 所用题库版本 |
| type | string | 4 字母类型代码，如 "INFP" |
| dimensions | object | 四维结果，键为 E/I、S/N、T/F、J/P 每维的两侧字母 |
| dimensions.<X> | object | 每维含：letter（倾向侧）、score（倾向侧题数）、total（该维总题数）、percent（归一化倾向强度 0-100） |
| clarity | object | 四维清晰度，键同上，值含 level（低/中/高/极清晰 0-3）与 label（中英对照档名） |
| type_profile | object | 从 data/type_profiles.json 提取的该类型画像摘要 |
| careers | array | 从 data/career_mapping.json 提取的推荐职业岗位列表 |
| similar_types | array | Top3 相似类型（曼哈顿距离最近），含类型代码、距离、差异维度 |
| disclaimer | string | 免责声明文本（报告与口头摘要必须携带） |

## 3. 计分算法细节

### 维度计数

每题在题库中标注计分维度（E/I、S/N、T/F、J/P 之一）与方向（A/B 各指向哪一侧）。逐题累加：用户选的选项对应侧 +1。四维分别统计两侧票数。

### 平票规则

某维两侧票数相等（偶数题时可能出现）时，按固定默认侧落位：**I、N、F、P**。即平票时类型代码取 I**N**FP 侧。result.json 中该维 percent 记为 50，clarity 记为最低档。

### 逐维归一百分比

设某维倾向侧票数为 s、该维总题数为 t（两侧票数之和），则：

```
percent = round(50 + (s - t/2) / t * 100)   // 值域 [50, 100]，50 即无倾向
```

倾向侧的相反侧强度即 100 - percent。

### 清晰度公式与四档中英对照

清晰度衡量倾向强度，基于归一化偏离量：

```
d = |percent - 50| / 50        // 0 ~ 1
level: d < 0.15 → 0；0.15 ≤ d < 0.35 → 1；0.35 ≤ d < 0.60 → 2；d ≥ 0.60 → 3
```

| level | 中文 | English |
|---|---|---|
| 0 | 轻微倾向 | Slight |
| 1 | 中等清晰 | Moderate |
| 2 | 明显清晰 | Clear |
| 3 | 极度清晰 | Very Clear |

level 0（边界倾向）维度在口头摘要与报告中必须注明："该维度倾向较弱，重测可能变化"。

### Top3 相似类型（曼哈顿距离）

把每型四维表示为数值向量（如 INFP = [I, N, F, P] 侧各维取 1，另一侧取 0），计算与用户结果向量的逐维差绝对值之和：

```
distance(T) = Σ_i |user_vec[i] - type_vec[i]|，i ∈ {EI, SN, TF, JP}
```

用户向量取各维倾向侧（平票取默认侧）。全 16 型按距离升序取前 3（自身距离 0 排除），并列时按类型代码字母序。距离为 1 的类型即只差一维，报告中的"人际匹配"章节即基于此。

## 4. generate_report.py 三级回退机制

```bash
python3 scripts/generate_report.py <result.json> [output.pdf]
```

缺省输出 `./MBTI_Report_<TYPE>_<timestamp>.pdf`。生成引擎按顺序尝试：

1. **weasyprint**：首选，排版质量最高。失败常见原因：未安装、系统缺少 pango/cairo 动态库。
2. **Chrome headless**：调本机 Chrome `--headless --print-to-pdf`。失败常见原因：未安装 Chrome、路径探测失败、沙箱环境禁止拉起浏览器进程。
3. **reportlab**：纯 Python 兜底，无外部依赖但排版较朴素。

**排查指引**（PDF 生成失败时逐级看什么）：

1. 先看 stdout：脚本会打印当前尝试到第几级引擎及每级的具体报错。
2. 第 1 级失败：看是否 `ModuleNotFoundError: weasyprint` 或 pango 缺库报错——属环境问题，直接观察是否自动落到第 2 级。
3. 第 2 级失败：看是否找不到 Chrome 可执行文件（macOS 默认路径 /Applications/Google Chrome.app、Linux 的 google-chrome/chromium）。沙箱内浏览器被禁时亦在此级失败。
4. 第 3 级失败：reportlab 为脚本内置依赖兜底，若仍失败多为 result.json 格式异常——回看 score.py 是否正常退出（退出码 0）。
5. 三级全失败：向用户如实说明环境受限，保留 result.json 供环境恢复后重试；不得伪称已生成 PDF（违反铁律 3 的精神：宁可明说失败，不可假报成功）。

任何一级成功后，脚本 stdout 输出最终 PDF 路径；AI 助手必须执行 `open <pdf路径>` 交给用户预览。

## 5. build_quiz_page.py 参数与 quiz.html 功能

```bash
python3 scripts/build_quiz_page.py --version <quick|standard|pro> [--language <zh|en>] [--output <path>]
```

| 参数 | 说明 |
|---|---|
| --version | 必填。抽题版本：quick 70 题 / standard 93 题 / pro 144 题 |
| --language | 可选，默认 zh。页面初始语言 |
| --output | 可选，缺省输出 `./quiz.html` |

生成后 `open quiz.html` 交给用户。quiz.html 功能：

- **断点续答**：答题进度实时写入浏览器 localStorage，中途关闭重开自动恢复到上次题目。
- **双语切换**：页面右上角可随时切换中/英文题干（题库自带双语字段）。
- **答案 JSON 下载**：全部答完点"完成测评"，浏览器下载答案文件 `mbti_answers_<version>.json`，格式即第 1 节契约格式。
- 用户把下载的 JSON 交给 AI 助手后，走正常计分流程：`python3 scripts/score.py <该文件>`。

## 6. 团队场景预告（v1.1）

v1.1 将支持团队模式：多名成员各自完成测评（推荐 L3 网页式各自作答），收集各人的答案 JSON 文件，逐个运行 score.py 得到各自 result.json，再汇总生成团队报告（类型分布、四维热力、人际匹配矩阵）。v1.0 不实现，收到团队需求时告知用户此为路线图功能，可先用单次流程逐人测评。
