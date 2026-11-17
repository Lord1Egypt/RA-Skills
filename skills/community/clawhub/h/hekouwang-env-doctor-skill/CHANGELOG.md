# 更新日志

## v1.2.2 · 2026-08-12

ClawHub 分类：`development`

## v1.2.1 · 2026-08-12

P2：doctor-suite 互链 + 商业化可发现性。

- `scripts/run-all-doctors.sh`、`references/doctor-suite.md`
- README：30 秒验收、免费/付费表、@huiyonghkw CTA
- summary 补英文 SEO 关键词

## v1.2.0 · 2026-08-12

AI 开发机快扫 + 体检器家族互链。

- `scripts/scan.sh`：`--profile ai-dev` 快扫档（跳过大户发现，强化 Agent 宿主目录）
- 新增 `AI_AGENTS` 节：`.claude` / `.cursor` / `.codex` 体积、skills 数量、MCP 配置有无
- `references/rules.md` **v1.1**：第七节 AI 开发与 Agent 宿主（Claude/Cursor/Codex、npx 缓存、Playwright、uv）
- 报告互链：`md-doctor`（配置）· `skill-doctor`（技能）· 本器只管环境

## v1.1.0 · 2026-07-18

新增清理选择器。

- `scripts/clean.sh`：交互式勾选清理。空格勾选 / ↑↓移动 / a全选 / n全不选 / 回车确认 / q退出；
  **默认全不选**、**数据类 🔒 锁死不可勾选**、只执行白名单内写死的命令、确认页逐条列出命令与代价、输入 `yes` 才动手、支持 `--dry-run`
- 安全铁律第 1 条由「永不执行删除」修订为「删除只能来自用户逐项勾选」（底线不变：用户必须知道自己删了什么）
- 扫描改并行 `du`：15 个目录从 30 秒+ 降到约 6 秒
- 修 bash 3.2 兼容：macOS 自带 bash 不支持 `read -t` 小数超时，方向键此前完全失效
- README 换成 Claude Code 真机实录 GIF + 选择器演示 GIF

## v1.0.0 · 2026-07-18

首个版本。

- 只读扫描器 `scan.sh`：磁盘大盘（macOS 走数据卷）/ 候选目录体积 / 版本管理器四信号 / 运行时实际来源 / 家目录大户发现
- 规则库 v1.0：三分法（数据·缓存·残留）+ 四信号判活表 + 11 类版本管理器 + 11 类包管理器缓存 + 容器/模拟器/AI 模型，官方清理命令逐条核自官方文档或工具自带 `--help`
- 安全铁律：永不代删 / 只读 / 不确定不猜 / 数据类不进建议 / 清理后遗症必交代 / 不联网上报
- 报告四步对话流程：先给结论 → 分三组 → 逐组问 → 确认后才出命令
