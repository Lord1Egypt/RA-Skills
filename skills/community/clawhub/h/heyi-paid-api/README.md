# heyi-paid-api · Skill 部署工具

> 所属项目：[`bot-backend`](../../../README.md)（合一中枢 API 平台后端）
> 部署目标：Cursor / Claude Code / Codex / OpenClaw 等 Agent 工作台

一行命令把 `heyi-paid-api` Skill 部署到本机 — Cursor / Claude Code / Codex / OpenClaw。

## 用途

这个 npm 包提供 `heyi-paid-api` Skill 的安装脚本。Skill 内容来自
[bot-backend 仓库](https://github.com/heyi-byte/heyihub-skill) 的
[`docs/skills/heyi-paid-api/SKILL.md`](https://github.com/heyi-byte/heyihub-skill/blob/main/SKILL.md)。

### 如何获取 API Key

申请与使用 API Key 的完整流程请参见飞书指南：
<https://my.feishu.cn/wiki/SzpMwQQ1Piw3rck0NAPc7la1npe>

控制台地址：<https://bot.01011.top>（用户控制台 → 「API Key」管理页）。

## 安装

```bash
npx heyihub-skill
```

或全局：

```bash
npm install -g heyihub-skill
heyi-paid-api
```

脚本会自动：

1. 拉取最新的 `SKILL.md` 等 Skill 资源
2. 根据当前 Agent 工作台识别目标目录（`~/.claude/skills/` / `~/.codex/skills/` / `~/.cursor/skills/` / `~/.mavis/skills/` / `~/.openclaw/skills/` 等）
3. 复制到对应 `skills/heyi-paid-api/` 目录
4. 提示重启 Agent 以加载 Skill

### 安装验证

```bash
# Claude Code
ls -la ~/.claude/skills/heyi-paid-api/SKILL.md
# Cursor
ls -la ~/.cursor/skills/heyi-paid-api/SKILL.md
# 通用：检查目录里至少应有 SKILL.md + LICENSE
ls -la ~/.claude/skills/heyi-paid-api/
```

输出包含 `SKILL.md`、`LICENSE` 即视为安装成功。然后**重启 Agent 工作台**让 Skill 生效。

> `snapshots/catalog.json` 不复制到 Skill 目录——`check` 子命令读的是 npm 包内的那份快照，不是 Skill 目录里的。

### 升级

```bash
# 重跑 npx 会拉最新版本覆盖本地 Skill 资源
npx heyihub-skill@latest

# 全局用户也可：
npm update -g heyihub-skill && heyi-paid-api
```

升级后建议跑一次 `npx heyihub-skill check` 确认与远端目录对齐，再重启 Agent。

## 运行期自检（check / snapshot）

每个 npm release 会嵌入一份 `snapshots/catalog.json`（从远端公开目录抓取）。用户的 Agent 工作台装好 Skill 后，可以随时拉远端公开目录对比，定位"接口已下线 / 新增 / 价格或路径变动"：

```bash
npx heyihub-skill check              # 默认 soft：仅 retired / changed 退出码 1
npx heyihub-skill check --strict     # 让 added 也退出码 1
npx heyihub-skill check --base-url https://bot.01011.top
```

输出示例：

```text
heyi-paid-api Skill 运行期自检
================================
  Base URL:    https://bot.01011.top
  快照文件:    /.../node_modules/heyihub-skill/snapshots/catalog.json
  模式:        soft

  本地快照: 41 个接口（2026-08-29T00:00:00Z）
  远端目录: 42 个接口（2026-08-29T12:00:00Z）

  ⚠ retired（已下线，本地快照有但远端缺） 1 项：
    - bilibili_search_all  GET /api/external/bili/search_all  (B站综合搜索)
  ⚠ changed（契约字段变动） 1 项：
    - search_notes (小红书笔记搜索)
        original_price_points: 2 → 3
  ℹ added（新增，远端有但本地快照没有） 1 项：
    + bilibili_get_dynamic_detail_v2  GET /api/external/bili/get_dynamic_detail_v2  (B站动态详情 V2)
```

退出码：

| 码 | 含义 |
| --- | --- |
| `0` | 一致，或仅有 `added`（soft） |
| `1` | 发现 `retired` / `changed`；`--strict` 时 `added` 也算 |
| `2` | 网络/HTTP/JSON 解析失败，或快照文件缺失 |

### 重新生成快照（开发者）

维护侧修改了后端接口目录后，重新生成 `snapshots/catalog.json` 并发布新版本 npm 包：

```bash
cd docs/skills/heyi-paid-api
node bin/install.js snapshot --base-url https://bot.01011.top
git diff snapshots/catalog.json
# 提交、发布 v1.1.x
```

也支持覆盖路径：

```bash
node bin/install.js snapshot --base-url https://staging.example.com --snapshot /tmp/staging-catalog.json
```

> **首次安装提示**：`snapshots/catalog.json` 是从生产环境实时抓取的。如果某个 release 因为发布时机问题带了过期快照，用户机器上的 `check` 会立刻报 `retired` / `changed`——这是预期行为，请按上述自检流程确认。

## 部署目标

| 平台 | Skill 目录 |
| --- | --- |
| Cursor | `~/.cursor/skills/heyi-paid-api/` |
| Claude Code | `~/.claude/skills/heyi-paid-api/` |
| Codex | `~/.codex/skills/heyi-paid-api/` |
| OpenClaw | `~/.openclaw/skills/heyi-paid-api/` |
| 通用 Agents | `~/.agents/skills/heyi-paid-api/` |

## 业务背景

`heyi-paid-api` 是给 Agent 用的 **bot-backend 付费 API 客户端 Skill**：

- 在 Agent 对话中可调用 [`bot-backend`](../..//README.md) 提供的付费 API（视频解析、内容分析等）
- 自动管理 API Key 注入、用量统计、错误重试
- 用户在控制台 → 「API Key」页签生成 Key

## 卸载

```bash
# 1. 卸 npm 包（如曾全局安装）
npm uninstall -g heyihub-skill

# 2. 删除 Skill 目录
rm -rf ~/.cursor/skills/heyi-paid-api
rm -rf ~/.claude/skills/heyi-paid-api
rm -rf ~/.codex/skills/heyi-paid-api
rm -rf ~/.mavis/skills/heyi-paid-api
rm -rf ~/.openclaw/skills/heyi-paid-api
```

只删 Skill 目录也可正常工作，但 npm 缓存里的 `snapshots/catalog.json` 会残留；建议两步都做。

## License

[MIT](./LICENSE) © 2026 MiniMax-00
