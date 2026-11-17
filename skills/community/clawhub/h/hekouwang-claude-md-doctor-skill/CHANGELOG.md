# Changelog

本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [1.3.3] - 2026-10-12

### 修复
- `docs/` 指针识别带上前面的目录段：`free/docs/index.html` 不再被截成 `docs/index.html` 误报死链

## [1.3.2] - 2026-08-12

### 变更
- ClawHub 分类：`development`

## [1.3.1] - 2026-08-12

### 新增
- `scripts/run-all-doctors.sh`：hekouwang-doctor-suite 三件套一键体检
- `references/doctor-suite.md`：套件说明与免费/付费对照

### 变更
- `check.py`：无 `HEKOUWANG_CONTENT_FACTORY` 时提示付费报告卡 CTA
- README：30 秒验收 + 三件套互链；summary 补英文 SEO 关键词

## [1.3.0] - 2026-08-12

### 新增
- **`check.py` 支持 AGENTS.md**：根目录优先体检 `AGENTS.md`，其次 `CLAUDE.md` / `CLAUDE.local.md`；
  子目录扫描同时认两份本地配置。
- **#0b 双文件去重**：根目录 `AGENTS.md` + `CLAUDE.md` 同时存在且都不是薄指针 → WARN（双倍上下文费）。
- **#4c Skill 路由**：正文应把细则指针到 `.agents/skills/`（或 `.cursor/skills/`），别堆在常驻正文。
- 报告标题改为 **AGENT CONFIG DOCTOR**；JSON 输出增加 `root_configs` 字段。

### 文档
- `SKILL.md` 触发词补 `AGENTS.md` / `agents.md` / `运行时配置体检`；评分表扩至 12 项。
- 新增测试夹具 `tests/fixtures/good-agents/`、`tests/fixtures/dual/`。

## [1.2.2] - 2026-07-09

### 文档
- **新增「与内置 `/doctor` 命令的分工」小节**：两者名字都带 doctor 但体检对象完全不同——
  内置 `/doctor` 查整套 Claude Code 运行环境（安装/未用扩展/上下文膨胀/权限/版本），
  本 skill 只查一份 CLAUDE.md 的写法质量。给出对比表 + 唯一交集（`/doctor` Check 2/3 碰 CLAUDE.md
  但只从上下文成本看、不评质量）+ 用法建议（先 `/doctor` 发现文档偏大，再用本 skill 深度评 + 重构）。
- **README.md / README.en.md 同步**：两份 README 也各补一节「这不是内置的 `/doctor` 命令」
  （精简对比表 + 唯一交集 + 组合用法），中英一致。

## [1.2.1] - 2026-06-22

自体检（用姊妹工具 skill-doctor 跑）后的两处打磨：

### 优化
- **SKILL.md 声明 `allowed-tools`**：收敛到本 skill 真正需要的工具集，减小越权面。
- **补「本 skill 自检会触发 #10 误报」豁免说明**：正文里的"教程/如何使用/step by step"是
  待检测的黑名单词本身（评分表/盲区/修复清单都要举例），机检会误报教学冗余——
  与 skill-doctor 对齐，注明定性时直接放行，别删那些词（删了体检器就不工作）。

## [1.2.0] - 2026-06-21

对照社区教程 `luongnv89/claude-howto` 的 Memory 最佳实践逐条比对后，补上三个真空白
（只取它的"安全 + 机制正确性"，不取它"把文件写全"的加法倾向）。

### 新增
- **安全红线检查「无硬编码密钥」(#0)**：扫正文里的 `sk-`/`AKIA`/`AIza`/`gh*_`/`xox*`/
  JWT / 私钥块 / `password=`/`secret=` 等指纹，命中即 **FAIL**（权重 1.5、资损级）。
  报告对命中值脱敏（前 4 位 + 长度）。占位/示例值（`<your-pwd>`/`${VAR}`/`example` 等）自动豁免。
  补齐教程头号 Don't "Never store secrets in CLAUDE.md"——此前脚本只防自己读 .env，
  却不查被体检文件本身是否藏密钥。
- **指针死链检查 (#4b)**：`docs/` 文本指针与原生 `@import` 路径都校验目标文件是否存在，
  死链 → WARN（指向不存在的文件比没指针更糟）。

### 变更
- **#4 路由器检查认原生 `@import` 语法**：此前只认纯文本 `docs/...`，用官方 `@path` 导入
  反而不给"下沉指针"加分；现在两种写法都算合格指针。

### 文档 / 测试
- `SKILL.md` 评分表补 #0 与 #4b，加权说明与修复动作清单同步（拔密钥 + 轮换提醒、修死链）。
- good 夹具补 `docs/architecture.md`、`docs/api.md` 桩文件，示范"指针均可解析"。

## [1.1.0] - 2026-06-18

把 Claude Code 之父 Boris Cherny / Cat Wu 的"context minimalism · 别跟模型较劲做加法"
立场接进体检逻辑。

### 新增
- **第 10 项检查「别替模型补它已经会的」**：扫教学型措辞(如何使用 / 使用教程 /
  step by step / how to use)，命中即 WARN——这类通用写法随模型升级自动变强，
  写进常驻正文只是为"很快过时的东西"每次付上下文费。
- **「减法优先」元判据**：写进 `SKILL.md`，凌驾 9 项之上——加任何一段前先问
  "能不能不写在常驻正文里"。

### 变更
- **评分改为按重要度加权**：减法核心项(#1 篇幅 / #3 可操作 / #4 路由器 / #10)权重 1.5，
  加内容项(#6 Hook / #7 记忆 / #8 人格)降到 0.6。修掉旧逻辑"一边喊越短越好、
  一边因缺工作风格块扣分、逼用户把文件写长"的自相矛盾。
- **#8 工作风格块加上限护栏**：限 3–5 行，每行须对应一个"不写就会犯的具体错"，别写性格小作文。

### 文档
- `README` / `README.en` 同步「10 项检查」并写明「减法优先 · 别跟模型较劲做加法」立场。
- `SKILL.md` 顶部署名补 GitHub 仓库地址
  （<https://github.com/huiyonghkw/hekouwang-claude-md-doctor-skill>），方便 skillhub 溯源。

## [1.0.0] - 2026-06-17

首个正式版本。把"CLAUDE.md 当运行时配置、不是项目说明书"的最佳实践做成可跑在任意项目上的体检器。

### 功能
- **9 项检查的命令行体检器 `check.py`**：篇幅 / 禁止清单 / 规则可操作 / 路由非图书馆 /
  高危模块本地 CLAUDE.md / Hook 强制 / MEMORY.md 回路 / 工作风格 / 30 秒三问。
- 输出彩色文本报告或 `--json`；评分 0–100（A/B/C/D）；有 FAIL → 退出码 1（可 CI 卡关）。
- 零运行时依赖（仅 Python 3 标准库）；只读，绝不读取 `.env` / `*.key` / `*.pem`。
- **`SKILL.md` 定性复核层**：在 Claude Code 内说「检查我的 CLAUDE.md」即可机检 + 模型复核 + 代修复。
- **Docker**：`docker run --rm -v "$PWD:/work" claude-md-doctor`，免装 Python。
- **GitHub Actions CI**：语法 + good/bad 夹具 + JSON 合法性。
- 中英双语 README、MIT LICENSE、CONTRIBUTING、示例动图（CLI 实录 + 动效报告卡）。

### 商业模型
- 命令行体检器开源免费（MIT）；品牌可视化报告卡为付费增值，依赖未公开字体/版式，不在仓库内。

[1.0.0]: https://github.com/huiyonghkw/hekouwang-claude-md-doctor-skill/releases/tag/v1.0.0
