# Changelog

本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

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
