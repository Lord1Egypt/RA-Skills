# 更新日志

## v1.3.0 · 2026-11-18

ClawHub 审核复核：把清理范围收窄到官方缓存命令，消除「描述-行为不符」与危险参数命中。

- `scripts/clean.sh`：移除 5 个版本管理器整目录删除与 Xcode / Homebrew 缓存目录的递归删除命令，改为官方子命令（`brew cleanup` / `brew cleanup --scrub` / `npm cache clean --force` / `yarn cache clean` / `pnpm store prune` / `pip3 cache purge` / `uv cache clean`）
- `scripts/clean.sh`：去掉跳过逐项确认的开关，每项都必须单独确认；命令改为按 id 静态分派，取消动态求值
- `scripts/clean.sh`：缓存项要求对应工具仍在，工具已卸载的目录不再列出（避免误导与执行失败）
- `references/rules.md`：`~/.npm/_npx` 与 Homebrew 缓存改为官方命令表述；第二节明确版本管理器卸载属手动步骤
- `references/safety.md` / `report.md` / `README.md` / `SKILL.md`：删除范围、确认流程与免责表述同步收窄
- 行为变化：`clean` 不再删除版本管理器整目录；被判为残留的版本管理器只给官方手动步骤

## v1.2.5 · 2026-11-18

ClawHub 安全审查（suspicious 命中）修复，功能不变。

- `scripts/scan.sh`：只读声明改写，不再出现危险命令字面；只读承诺不变
- `references/rules.md`：nvm 卸载改为引用官方 Manual Uninstall（不复述命令）；npx 缓存路径改为 `"$HOME/..."` 形式，避免被截断成主目录；Playwright 固定 `npx playwright@1.56.1`
- `references/report.md`：报告模板不再出现危险命令字面，改为「见官方 README」占位
- `scripts/clean.sh`：Homebrew 下载缓存与旧版本拆成独立选项，清缓存不再连带删旧版本；删除前逐项打印路径并单独确认（当时支持跳过逐项确认的开关，已于 1.3.0 移除）；`--dry-run` 语义不变
- `SKILL.md`：description 如实声明「默认只读扫描；clean 逐项确认后删除缓存/旧版本；不读用户文档内容」

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
