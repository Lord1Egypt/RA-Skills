# Changelog

本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [1.8.6] - 2026-11-10

### 发布
- 重发 1.8.5 安全修复（先前版本号占用但未落成可打 tag 的正式版）

## [1.8.5] - 2026-11-10

### 安全（ClawHub 复查）
- 入口读取统一走 `_read_text_inside`：`SKILL.md` / `agents/openai.yaml` 若为越界软链则拒绝打开。

## [1.8.4] - 2026-11-10

### 安全（ClawHub 复查）
- `check.py` 遍历与读文件不再跟随越界软链；目录软链不进入；指向受保护文件名的软链跳过。
- `trigger_eval` 明确披露会把 query/description 发给外部模型服务。

## [1.8.3] - 2026-11-10

### 安全（ClawHub 复查）
- description 写明可选套件会检查项目说明文档与本机开发环境，以及可选 SkillSpector / trigger_eval。
- SkillSpector 指引改为：外来 skill 全量扫；自维护 skill 用基线只看 NEW——不再写成「自研豁免」。
- Docker 示例改为 digest 钉死镜像 + 工作目录 `:ro` 挂载。

## [1.8.2] - 2026-10-15

### 安全（ClawHub 审查）
- `trigger_eval.py`：子进程改为 `--tools Skill,Read` + `--strict-mcp-config`，只开放判定所需工具、不加载 MCP；
  环境变量从「全量继承」改为白名单，额外变量用 `--pass-env` 显式放行；
  探针正文不再嵌入被测 description，frontmatter 中的 description 按 JSON 字符串写入；
  运行前确认费用与来源（非交互需 `--yes`）。
- SKILL.md 声明 `allowed-tools` 与 `metadata.openclaw.requires`，收窄 description 触发边界。
- Dockerfile 基础镜像按 digest 固定。

## [1.8.1] - 2026-10-12

### 修复
- **#4b 指针死链误报**：扩展名交替里 `js` 排在 `json` 前且没有词尾边界，
  `references/x.json` 被截成 `references/x.js` 判为死链。扩展名后加边界，按完整扩展名匹配。

### Tests
- `test-dead-pointer.sh` 新增 `.json` 指针不被截断的回归用例。

## [1.8.0] - 2026-08-30

### 新增
- **Codex 严格基础 Profile**：新增 `--profile codex`，以零依赖方式迁入 Codex
  `skill-creator` 的基础契约：字段白名单、≤64 字符 kebab-case name、description 限制与正文
  未完成 TODO 检查。该 Profile 可用于单个 Skill 或 `--scan` 批量门禁。
- JSON/文本报告明确输出本次 `profile`；报告 schema 升至 v3，避免自动化把默认跨宿主检查和
  严格 Codex 验收混为一谈。

### 兼容性
- 默认 `agent` Profile 保持原行为，允许 Claude/其他宿主合法的扩展字段（如 `slug`、`version`）；
  只有显式传入 `--profile codex` 才执行严格白名单，避免跨宿主 Skill 被错误阻断。

### Tests
- 新增合法 Codex Skill、严格拒绝扩展字段与 TODO、默认跨宿主扩展字段可通过的正反例回归；CI 同步执行。

## [1.7.0] - 2026-08-30

### 新增
- **多 Skill 扫描**：新增 `--scan`，递归发现隐藏宿主目录，按真实 SKILL.md 去重，
  报告断开的软链、重复 name、遍历错误和每个 Skill 的门禁结果；新增 `--direct`
  供宿主根目录只盘点直接入口，递归模式跳过测试夹具和构建目录。
- **显式门禁字段**：文本和 JSON 报告新增 Doctor 版本、schema 版本、PASS/WARN/FAIL/INFO
  计数与 `gate`；自动化不再用 score/grade 猜是否放行。
- **宿主调用策略检查**：读取 `disable-model-invocation` 与 `agents/openai.yaml` 的
  `policy.allow_implicit_invocation`，发现冲突时阻断。

### Fixed
- frontmatter 解析支持 UTF-8 BOM、嵌套 mapping、布尔值和 YAML 解析错误，不再把嵌套
  `metadata.openclaw` 静默当成不存在；兼容跨行 JSON 风格的 flow mapping/list。
- 指针检查只认 Markdown link destination 或显式 `doctor:resource`，并校验 glob、
  brace expansion、软链目标和根目录 containment；修复教学示例路径误报。
- 文本扫描覆盖 YAML/HTML/TypeScript 等逻辑文件，但继续严格跳过 `.env`、`*.key`、
  `*.pem` 和包含 secret 的文件名；读取失败改为 FAIL，不再静默跳过。
- 三件套聚合器改为 fail-closed：doctor 崩溃、JSON 损坏和 env-doctor 非零退出都会
  让套件失败；外部软链 Skill 仍可只做提示。

### Tests
- 新增 frontmatter、保护文件、扫描、断链、重名、示例路径和越根路径回归。

## [1.6.0] - 2026-08-27

### 变更
- **#4b 指针死链从 WARN 升为 FAIL**：死链是确定性事实，不是风格建议。此前一个被 SKILL.md
  引用却漏提交的 reference，在 pre-push 快照里只扣 3 分（97/100、退出码 0），于是「Doctor
  失败禁止推送」形同虚设。现在死链直接判失败并卡退出码。

### 新增
- `tests/test-dead-pointer.sh`：死链应失败、指针齐全应放过的正反例。

## [1.5.2] - 2026-08-12

### 变更
- ClawHub 分类：`development`

## [1.5.1] - 2026-08-12

### 新增
- `scripts/run-all-doctors.sh`、`references/doctor-suite.md`（与 md-doctor / env-doctor 同版）

### 变更
- `check.py`：付费报告卡 CTA；README 30 秒验收 + 免费/付费表 + 三件套互链
- summary 补英文 SEO 关键词（skill lint / SKILL.md doctor）

## [1.5.0] - 2026-08-12

### 新增
- **#11 paths / globs**：识别 Cursor 2.4+ 文件作用域 frontmatter，减少无关文件时的误触发。
- **#12 OpenClaw 兼容声明**：轻量检查 `metadata.openclaw`、`requires`、`install`（有 scripts/ 时提示）。

### Fixed
- **指针扫描误报**：只匹配带扩展名的捆绑资源路径（`references/foo.md`），表格里的
  `references/scripts/assets` 不再被判死链。
- **可移植性自检误报**：`ABS_PATH_RE` 用字符串拼接构建，避免 `check.py` 源码里的
  正则说明行被当成硬编码路径。
- **#10a 元层面误报**：评分表/检查项表格行里的黑名单示例词不再计为教学冗余。

## [1.4.1] - 2026-08-01

修 #0 安全红线的两处假阳性。**假阳性会让红线失去意义**——被误报训练过的人下次看到真 FAIL 也只会挥手放过。

### Fixed
- **`sk-` 密钥正则缺左词界**：`sk-(?:ant-)?[\w-]{20,}` 会从 `generate-ask-user-format.ts`
  里抠出 `sk-user-format` 判成 key。同一份 `SECRET_PATTERNS` 里 `AKIA` / `AIza` / `JWT`
  三条都带 `\b`，只有这条漏了。实测某第三方 skill 因此被判资损级 FAIL（62 分），
  命中源全是 `ask-user-*` 文件名。
- **测试夹具里的假密钥降级 WARN**：安全基准/回归夹具（`test/ tests/ fixtures/ golden/ snapshots/`
  等目录）里的 key 是刻意载荷，不是泄露。现在只在夹具命中时判 WARN 并提示"翻一眼确认"，
  正文/脚本命中照旧 FAIL；两类同时命中时 FAIL 优先，detail 里标明夹具那几处已降级。

### 验证（A/B 基准分辨力自检）
三类样本必须判出三种结果，否则说明改完的判据分不开对和错：
真密钥 `sk-proj-…` → **FAIL**；夹具里 `sk-ant-api03-…` → **WARN**；`aREDACTED-SECRET` → **PASS**。
回归夹具分数不变（`tests/fixtures/bad` 67、`good` 100）。

## [1.4.0] - 2026-07-28

补上本器最大的盲区：**#2 触发质量以前只能拍脑袋，现在能实测**。
静态检查只看得出 description 里有没有"当…时"这类信号词，判不了写得准不准——
而 description 写不准 = 这个 skill 永远不被唤醒，正文写得再好也白搭。

### Added
- **`scripts/trigger_eval.py` · 触发力实测（可选第二引擎）**：把待测 description 装成临时探针 skill，
  跑 `claude -p` 看模型会不会去调它，输出触发力分数 + **漏触发 / 误触发**两个计数。跑完即删，
  不碰任何已装的 skill。改自官方 `anthropics/skills · skill-creator/run_eval.py`。
- **`--distractors` 干扰项**：把其它 skill 的 description 一起放进探针环境当竞争者。
  不加的话环境里只有被测探针一个候选，模型"没得选"就会勉强用它，**负例系统性假阳性**。
  实测同一段 description、同一套 query：无竞争者 **83 分**（那条"翻页演示版"负例误触发），
  放 5 个兄弟 skill 后 **100 分**（正确避开）——**什么都没改，差 17 分**。
  按 83 分去修边界，修的是一个不存在的问题。
  干扰项名字同样中性化成 `alt-xxx`，否则模型看名字就能认出对手，等于开外挂。
- **`references/trigger-eval.md`**：query 怎么设计（**负例必须是 near-miss**）、
  **负例必须带干扰项跑**、两种失败各自怎么改 description、结果不对劲怎么翻原始流、成本表。
- 工作流新增步骤 **2c**；检查项 #2 与「机检的盲区」#2 同步改写。

### Changed
- 免费/付费边界补一档：`trigger_eval.py` **脚本开源随便用，但 API 费用走用户自己的额度**
  （约 $0.09–0.15/次调用）。因此它是**可选叠加档、不进默认流程**，
  `check.py` 的零依赖卖点不受影响，不跑也能出完整体检报告。

### 踩坑记录：官方脚本原样搬过来测不出任何东西

官方那版思路对，但在 Claude Code 2.1.220 上四处全错，**改完才有分辨力**
（实测：真 description 100 分 vs "生成内容。"50 分；不改第 4 条时两者都是 100，等于白测）。
四处里**前三处都表现为"跑通了、只是分数低"**，不做 A/B 基准根本发现不了：

1. 不加 `--setting-sources project` → 子进程继承 `~/.claude/skills/` 里已装的真 skill（实测 32 个），
   模型触发真身、名字对不上探针 → **全部正例假阴性**。官方没料到"被测 skill 已装在机器上"。
2. 官方"第一个 tool_use 不是 Skill/Read 就判否" → 但模型碰到陌生 skill 名**会先 `Bash: ls` 探查**，
   Skill 往往是第二三个动作（实测序列 `['Bash','Bash','Skill']`）。改为扫完整个流、命中即收工。
3. 并发 worker 共用一个 project root → 模型调到**别人的**探针
   （实测：期望 `-d795b59f`，实际调 `-4ac07ae5`）。改为每条 query 一个一次性 root。
4. ⭐ 探针放 `.claude/commands/` 且沿用原 skill 名 → init 事件里 `skills` / `slash_commands`
   两个列表**都只给名字、不给 description**，模型光看名字就去 Read 它，
   **description 全程没参与决策**。改为装成 project 级真 skill + 中性名 `probe-xxxxxxxx`。

⭐ 因此文档把「**先做 A/B 基准分辨力自检，分不开就别信分数**」写成了跑之前的强制前置步骤，
不是建议。

## [1.3.0] - 2026-07-15

**版本号说明**：本次内容即原定的 1.2.0（见下方 Changed/Added），因发布事故改号为 1.3.0——
ClawHub 上 `hekouwang-claude-skill-doctor-skill` 这个 slug 于 2026-07-09 被误发成 **md-doctor 的内容**
并占用了 1.2.2 这个版本号（check.py 与 md-doctor 逐字节同 hash `5f0d3613`、测试夹具是 `CLAUDE.md`
而非 `SKILL.md`）。该 slug 在 2026-06-24 的 1.0.2 / 1.0.3 是正确的 skill-doctor 内容，
即**误发覆盖了正确版本**。需发一个高于 1.2.2 的版本才能把 latest 拨正，故跳到 1.3.0。
误发的 1.2.2 已从该 slug 永久删除，版本史现为 1.0.2 → 1.0.3 → 1.3.0。

### Fixed
- **ClawHub 发布事故更正**：`hekouwang-claude-skill-doctor-skill@1.2.2` 实为 md-doctor，已删除；
  latest 拨回真正的 Agent Skill 体检器。
- **发布纪律**：以后 `clawhub skill publish` **一律显式传 `--version`**——
  ClawHub 不读 SKILL.md 的 `version`，只在线上版本上 +1（实测会把本地 1.2.2 发成 1.1.3、
  本地 1.1.0 发成 0.1.2，即**降级**）。自动推断不可信。

拿真数据校准步骤 2b 的 SkillSpector。全量扫 7 个 `hekouwang-*` skill、逐条翻源码核实，
结论推翻 1.1.0 的乐观假设：**对自研 skill 它 100% 误报**，且**分数完全不可信**。
2b 从"可选加跑的安全维"收紧为"只对外来 skill 跑的入库审查"。

### Changed
- **2b 定位收紧：只对"别人写的、要装进来的" skill 跑。** 7 个自研 skill 全扫、逐条翻源码，
  无一为真。自研 skill 改走**回归检测**（存基线 → 只看 NEW），不再全量看告警。
- **新增铁律「分数不是门禁，只看条目 + 翻源码」。** `Score/Severity` 是逐条**累加**的：
  yandu-deck / iterm2 / cc-prod 三个判 `100/100 CRITICAL · DO NOT INSTALL`，
  但报告里**一条 CRITICAL 发现都没有**——纯粹是十几条 MEDIUM/HIGH 累加撞顶。
  且评分随版本通胀：content-factory 代码一行没改，v2.3.5 `19/100 SAFE` → v2.3.13 `40/100 CAUTION`。
- **推翻 1.1.0 的「低可信度才是误报」说法**：95% 高可信度的照样是误报。改为附**高置信度误报样本表**：
  `rm -f "$写死路径"` → `TM1` 95%；`subprocess.run([...], check=True)` 硬编码列表 →
  `OH1 Unvalidated Output Injection` 95% + `AST4`（其 remediation 建议的恰恰就是这个写法）；
  docstring 写"本脚本**绝不读取** .env/*.key" → `PE3 Credential Access`；
  字体文件名列表 → `MP2 Context Window Stuffing`；中文 frontmatter → `P2 Hidden Instructions` 21%；
  中文触发词 → `AS3 Mixed script`。

### Added
- **rsync `--exclude` 顺序坑**：必须排在 `--include='*/'` 前面（rsync 首次匹配生效，
  否则 `*/` 先吃掉 `.venv/`，整个 site-packages 被当自己的代码扫）。实测 stock-data-reader 264M→176K。
- **SOCKS 代理绕法**：代理下扫描直接崩（`'socksio' package is not installed`），
  需 `env -u ALL_PROXY -u all_proxy -u HTTPS_PROXY -u https_proxy`。OSV.dev 连不上只降级静态库，不影响结论。
- **`--baseline` 正确用法 + 反例**：`fingerprints` 按「路径+内容 hash」锁定、只对同一 skill 生效；
  能跨 skill 的 glob `rules`（如 `id: "TM1"`）**恰恰不能在扫外来 skill 时开**——
  同一规则在自研 `rm` 上是误报、在恶意 skill 里可能是真的，全局关掉等于拆探头。
- content-factory / yandu-deck / stock-data-reader 三个常改的 skill 各存一份归零基线
  （`.skillspector-baseline.yaml`，A/B 验证：yandu-deck `100 CRITICAL DO_NOT_INSTALL` → `0 LOW SAFE`）。
- 记录唯一有信号的结构性告警 **LP1「代码有 network/env/shell 能力但没声明权限」**（7 个中 5 个命中）——
  不是漏洞，与 `check.py` 自检的「未声明 allowed-tools」指向同一缺口。

## [1.1.0] - 2026-06-24

接入外部安全扫描、消化业界 skill 写作最佳实践，扩展体检维度。

### Added
- **工作流新增步骤 2b · 深度安全扫描（可选）**：叠加 [NVIDIA SkillSpector](https://github.com/NVIDIA/skillspector)，
  覆盖提示注入 / 数据外泄 / 隐藏指令 / 供应链 / 过度授权 / MCP 越权等 68 类模式，
  补 `check.py` #0 密钥正则之外的深度安全维。含实战铁律：**只扫逻辑文件、别扫 assets**
  （直接扫会把字体/图片二进制当代码，刷出几十条假 `TM1 Tool Parameter Abuse`）；
  低可信度（<30%）`Hidden Instructions` 多是中文/零宽字符误报，人工复核。
- **评分维度 #8 触发方式匹配（model vs user invoked）**：只靠人手敲名字触发的 skill
  应设 `disable-model-invocation: true`，省掉每轮 `description` 的 context load。
- **`references/skill-writing-vocab.md`**：消化 mattpocock/skills 的 *writing-great-skills*，
  把"好 skill"的判据沉淀成可命名的诊断词汇——两种载荷（context/cognitive load）、
  信息阶梯、branch 拆分测试、完成判据（防 premature completion）、no-op 测试、
  sediment/sprawl/duplication 失败模式、leading word。出报告时用这些词点破问题。

### Changed
- **#10a 锐化为 no-op 测试**：判据明确为「这段相对模型默认行为改变了什么？没有就删」，
  比原先"别替模型补它已经会的"更可操作。

## [1.0.2] - 2026-06-22

实战体检三个品牌 skill 时暴露的机检缺陷修复（dogfooding）：

### Fixed
- **#7 allowed-tools 兼容逗号字符串**：原先只认 YAML 列表（`- a` / `[a,b]`），
  把官方 frontmatter 标准的逗号字符串写法（`allowed-tools: Bash, Read, Write`）
  误判为「未声明」。现在两种写法都解析、非空即 PASS。

## [1.0.1] - 2026-06-21

实战体检 14 个 skill 时暴露的两个机检缺陷修复（dogfooding）：

### Fixed
- **glob 指针不再误报死链**：`reference/deck-engine-*.html` 这类通配符指针，
  现在用 `glob` 解析、能匹配到真实文件就算存在；`{a,b}` brace 简写跳过不误报。
  （原正则在 `*` 处截断成 `reference/deck-engine-`，当字面路径判死。）
- **指针 / 教学词行号还原为文件绝对行号**：原先报的是正文相对行号（少算了
  frontmatter 行数），定位会偏。`parse_frontmatter` 现返回 `body_offset` 补正。

## [1.0.0] - 2026-06-21

首个版本。给 Agent Skill（SKILL.md）做体检的零依赖检查器。

### 检查项（12 项加权）
- **安全**：SKILL.md 及捆绑文件无硬编码密钥（命中即 FAIL，资损级）。
- **触发**：frontmatter 必填合法（name/description）；description 含「何时用」且 ≤1024 字符。
- **减法**：SKILL.md ≤500 行；长内容下沉 references/（渐进披露）；大段脚本外置 scripts/。
- **可移植**：无硬编码 `/Users/`、`/home/` 绝对路径。
- **取舍**：别替模型补它已会的（教学冗余检测）；allowed-tools 最小化；配套 README/CHANGELOG。

### 特性
- 零依赖（Python3 标准库），文本 + `--json` 双输出，退出码随 FAIL。
- 按重要度加权评分（触发/减法核心项 1.5，标准项 1.0，加内容项 0.6），A/B/C/D 分档。
- 极简零依赖 frontmatter 解析（块标量 / 行内 list / 缩进 list）。
- 密钥扫描双档豁免：指纹型用窄填充表、赋值型用宽占位表，避免误杀真 key。
- 报告口吻与署名沿用「会勇禾口王的AI笔记」品牌人设。
