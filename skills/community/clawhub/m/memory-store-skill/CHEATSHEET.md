# Memory Store v1.1.0 — 速查表

要求 Node.js 18+。人类用户只需记住：

```bash
npx memory-store
```

真实终端会打开数字菜单；非 TTY 环境输出精简帮助并立即退出。

## 四个高频短命令

```bash
# 默认 workspace + shared + explicit
memory-store remember decision "数据库选型" "采用 SQLite，适合本地单用户部署" --workspace

# 文本搜索；传 mem_... ID 时读取单条
memory-store recall "数据库选型" --json
memory-store recall mem_xxx --json

# 查看和调整档位
memory-store mode
memory-store mode balanced --global
memory-store mode explicit --workspace
memory-store mode --reset --workspace

# 版本、有效档位、存储路径与数量
memory-store status
memory-store status --json
```

`remember` 可用类型：`fact`、`decision`、`preference`、`workflow`、`debug_solution`、`state`、`event`、`relation`。加 `--global` 写全局记忆，加 `--private --agent-id <id>` 写私有记忆。

## 安装、更新与维护

```bash
npm i memory-store-skill
memory-store setup --agent codex --mode explicit

npm i memory-store-skill@latest
memory-store setup --sync

# 默认只预览；--apply 才归档候选
memory-store maintain
memory-store maintain --apply
```

`setup` 只使用当前本地包，不联网、不启动子进程。npm 安装没有生命周期安装器，不会自动修改 Agent 目录。

## Agent 与自动化

- 传入明确命令永不打开菜单。
- JSON 消费方使用 `--json`。
- 策略触发的自动存储使用 `remember ... --auto --source-conv-id <id>`。
- `off` / `explicit` 会拒绝自动操作；用户显式命令不受自动额度限制。

## 高级兼容接口

```bash
memory-store help --advanced
```

v1.x 的 `store`、`search`、`config`、`archive`、`restore`、`merge`、`migrate` 等命令保持兼容。完整参数见 [references/cli.md](references/cli.md)。

## 安全边界

- 所有交互式写入先展示目标和影响，确认默认为否。
- `private` 是 Agent 身份过滤，不是加密；不要存密钥、凭据、令牌或原始个人信息。
- `maintain` 默认只预览。批量归档、合并或删除前先备份。
