# Changelog

`heyi-paid-api` Skill 的所有重要变更记录。版本遵循 [SemVer](https://semver.org/)。

## [1.2.0] - 2026-08-29 — npm 首次公开发布

> 1.1.0 及之前的版本从未发布到 npm registry。本版本是 `heyihub-skill` 的首个公开版本。

### Changed
- **包名 `heyiHub-skill` → `heyihub-skill`**。npm 自 2017 年起拒绝含大写字母的新包名，原名无法发布。
- **安装命令 `npx heyi-paid-api` → `npx heyihub-skill`**（README / SKILL.md / 安装脚本输出共 27 处）。npx 按包名解析，旧命令在新包名下会 404。全局安装后 `heyi-paid-api` 仍作为 bin 别名可用。
- `package.json#bin` 增加 `heyihub-skill` 入口，与包名同名。
- `repository` / `homepage` / `bugs` 指向 `github.com/heyi-byte/heyihub-skill`；移除 monorepo 专用的 `repository.directory`。
- `snapshots/catalog.json` 重新抓自生产 `https://bot.01011.top`（此前抓自 `http://127.0.0.1:8000`，含生产未部署字段，导致 `check` 对 68/68 接口误报 `changed`）。
- SKILL.md 公开目录章节改为列出生产实际返回的字段；`category` / `sub_title` 标注为「后端已实现、生产未部署」，不可依赖。

### Fixed
- `--dry-run` 在目标目录已存在时会直接 `exit 1`，看不到安装计划——现改为仅提示，计划照常打印。
- README「安装验证」称 Skill 目录应含 `snapshots/catalog.json`，与 `copyDir` 显式跳过 `snapshots/` 的实现矛盾——改为说明 `check` 读的是 npm 包内的快照。

## [1.1.0] - 2026-08-29

### Added
- SKILL.md 新增 frontmatter `triggers` / `inputs` / `outputs` / `dependencies`，便于 Agent 工作台按意图匹配加载。
- SKILL.md 新增 `## 客户端代码片段`：Node.js 18+ 原生 fetch 与 Python httpx 两个完整封装示例。
- SKILL.md 新增 `## 典型场景示例`：覆盖小红书 / 抖音 / B站 / 博主视角四类常用组合调用流程。
- SKILL.md `## 常见错误` 表格拆分 5xx 为 500/502/503/504；新增 DNS / SSL / 超时 / 连接重置网络异常行。
- SKILL.md 新增 `### 调试清单`（8 步排查流程：Key → 接口 → 价格 → 余额 → 限流 → 响应壳 → 扣费 → 客户端）。
- SKILL.md `## 安全要求` 下新增 `### API Key 轮换建议`（90 天一次 / 灰度切换 / 多环境隔离）。
- SKILL.md 新增 `## 常见问题（FAQ）` 8 条。
- SKILL.md 新增 `## 监控建议（生产级使用）` 表格（余额 / 当日消耗 / 错误率 / 429 / 5xx）。
- README.md 新增 `### 安装验证`、`### 升级`、`npm uninstall` 命令，控制台 URL 链接。
- README.md / SKILL.md 补 [API Key 飞书指南](https://my.feishu.cn/wiki/SzpMwQQ1Piw3rck0NAPc7la1npe) 引用。
- 新增 `LICENSE`（MIT），`package.json#files` 加入 LICENSE。

### Changed
- `package.json` 新增 `"author": "heyi"`、`"homepage": "https://github.com/heyi-byte/heyihub-skill/tree/main/docs/skills/heyi-paid-api"`。
- README.md §License 由 `Private（仅供业务方使用）` 改为 `[MIT](./LICENSE) © 2026 MiniMax-00`，消除与 `package.json#license` 的矛盾。
- SKILL.md `## 调用前提` 首条改为指向飞书指南。

### Notes
- 旧 V1 接口（`bilibili_search_all`、`bilibili_get_dynamic_detail`）已在后端标记 `[已废弃]`，下个版本（≥ 1.2.0）移除前请升级本 Skill 并切换到 V2。