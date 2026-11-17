# 迭代日志

## 1.2.1 · 元数据对齐（2026-09-06）

- 版本晋升，重新提交以触发平台 AI 评估
- 内容无破坏性变更，与 1.2.0 功能一致

## 1.2.0 · skillhub 发布版（2026-09-06）

围绕 skillhub 的 **TRACE 五维评分**做的系统性发布打磨：

- **frontmatter 补齐 skillhub 必填字段**：`category=education`、`platforms=[WorkBuddy, claude-code, codex, deepseek-harness]`、`author`、`homepage`、`keywords`
- **description 收紧到 41 字**（skillhub 上架建议 ≤ 50 字），长描述迁移到正文 Overview
- **SKILL.md 渐进式披露**：十多项 CLI 开关→一张对照表，详细参数迁到 `references/activity-spec.md`（符合 TRACE-C 加分维度）
- **新增安全红线清单（TRACE-T 维度）**：SKILL.md 明确"零外网 / 零凭证 / 零高危函数 / 最小权限 / HTML 转义 / 字节级可复现"
- **新增 `scripts/preflight.py`**：发布前合规自检（frontmatter / 文件 / 安全 / zip 合规），自动输出 `SHIP_REPORT.md`（29 项）
- **修正阻塞性 zip bug**：`package_skill.py` 会把 SKILL.md 嵌进子文件夹（skillhub 硬要求根目录），改为手动重打包
- **README 首屏可视化**：`assets/preview.png`（真实 L1 样张）+ `assets/gallery.png`（四级课程体系画廊，L1-L4 主题色）+ `assets/preview.svg`（架构图）
- **新增 `assets/icon.png`**：扁平风拼图脑图标（skillhub 卡片缩略图用）
- **新增 `metadata.json`**：双格式支持（Skill + Plugin 双通路提交），含 30+ 条触发词、5 条核心命令、文件映射
- **README 姊妹 Skill 预告**：`math-course` / `english-course` / `pinyin-course` 组成 K12 启蒙系列；MIT 可自由改造商用
- 安全扫描结果：`scripts/*.py` 零外网、零凭证、零 eval/exec、零 shell 注入

## 1.1.0 · 上架前打磨（2026-09-06）

新增面向通用模板发版的工程化能力：

- **`scripts/batch_roster.py`** — 花名册 → 全班卷子批量；同名同 seed 横向可比
- **`scripts/test_skill.py`** — 19 项上架自检脚本，`--quiet` 适合 CI
- **`README.md`** — 5 秒入门 + 完整命令清单 + 项目结构
- **`LICENSE` (MIT)** + **`CHANGELOG.md`**
- **`--no-name`** — 强制姓名栏空白（覆盖 JSON/CLI 任何预填），批量打印全班场景必备
- **HTML 转义** — 学生姓名经 `&`/`<`/`>` 转义，防止注入
- **打印 CSS 增强** — `@media print { .ans { page-break-before: always } }`；全局 `print-color-adjust: exact`

## 1.0.0 · 核心交付（2026-09-06）

四轮迭代沉淀的功能：

- **四级等级体系**：L1 基础分类对应 / L2 排序规律方位 / L3 模式推理等量代换 / L4 综合逻辑
- **11 类题型**：classify / match / same / diff / order / pattern / shape / position / compare / maze / swap
- **A4 可打印 HTML + 答案 JSON**
- **能力诊断**：`--preset diagnostic` 自动覆盖全部题型
- **批改进阶**：对比 `activities[].answer`，错题一键重练（`--review --wrong`）
- **插件化题型系统**：`scripts/generators/` 目录自动发现 `g_*.py`
- **中英文双语**：`--lang en`
- **页眉姓名可填 + 评分栏可选**：`--name` / `--no-name` / `--score`
- **完整可复现**：seed + JSON 双保险，`--regen` 字节级一致
- **CLI 友好**：未传路径/拼错参数/超纲题型都不会崩溃
