# 常见问题

## 1. 什么问题会触发记忆检索？

涉及之前的讨论、决策、进度、偏好、惯例、排障历史，或 Agent 接手既有任务时，必须先搜索。新会话明显延续旧工作、当前上下文缺历史依据时按需搜索。一次性且自包含的问题无需为了形式而检索。

详见 [SKILL.md](SKILL.md#先判断是否检索)。

## 2. working memory 已有内容，还要搜索吗？

对**具体历史**仍要搜索。working memory 是当前会话摘要，可能省略细节，也不一定供其他 Agent 使用；结构化记忆库才提供 scope、visibility、type 与衰减等过滤信息。若搜索无命中，再查代码或项目文档，并说明来源。

## 3. global 与 workspace 有什么区别？

| scope | 默认位置 | 默认 visibility | 适用内容 |
|---|---|---|---|
| `global` | `~/.memory-store/` | `global` | 跨项目稳定偏好、通用知识 |
| `workspace` | `{workspace}/.agents/memory-store/` | `shared` | 项目决策、进度、排障、交接 |

工作区为只读或受管目录时，默认路径可能不可写。不要为了绕过权限而把项目私有信息错误放进 global。

## 4. `private` 能保护密钥和个人信息吗？

不能。`private` 只是 CLI 基于 `owner_agent` 与 `--as-agent` 的协作过滤。JSON 文件没有加密，拥有文件读取权限的进程仍能直接打开。CLI 也不会自动识别、脱敏或锁定密钥、凭据、令牌和个人信息。

不要把秘密写入记忆库；真正的机密应放在受权限控制的密钥管理系统。详见 [隐私边界](references/operations.md#visibility-is-not-a-security-boundary)。

## 5. 不传 Agent 身份会怎样？

公开的 `shared` / `global` 记录仍可按命令规则返回；`private` 默认不返回。要读取或修改自己的 private 记录，使用同一身份：存储时 `--agent-id agent-a`，读取或修改时 `--as-agent agent-a`，也可设置 `MEMORY_AGENT_ID`。

## 6. 为什么存了却搜不到？

依次检查：

1. 查询词是否过窄，尝试 2–3 个更稳定的关键词。
2. `--scope`、`--type`、`--visibility` 是否排除了目标。
3. private 记录的身份是否与 `owner_agent` 一致。
4. 记录是否已归档；普通 search 只查 active 主库。
5. 存储文件是否存在且 JSON 完整。

命令失败时查看 stderr 与退出码，不要把失败误认为“没有记忆”。

## 7. 搜索会更新访问次数吗？

默认不会，搜索是只读的。只有显式传入 `--touch` 时，CLI 才更新实际返回结果的 `access_count` 与 `last_accessed`。`recall` 会记录访问。

```bash
node scripts/memory_cli.js search --query "部署流程" --scope all \
  --as-agent agent-a --limit 5 --touch --stdout
```

## 8. 输出必须写文件吗？

不需要。v1.1.0 默认把 JSON 写到 stdout；短命令可使用 `--json` 明确要求机器可读输出。只有确实需要中间文件时才用 `--output result.json`。

```bash
node scripts/memory_cli.js search --query "部署" --scope all --stdout
```

## 9. 可以一次过滤多个类型吗？

可以，使用逗号分隔：

```bash
node scripts/memory_cli.js search --query "数据库" \
  --type decision,debug_solution --scope all --stdout
```

非法 type、visibility、priority、scope、importance 或 TTL 会报错并以非零状态退出。

## 10. 如何查看和恢复归档记忆？

```bash
node scripts/memory_cli.js list --scope all --status archived \
  --as-agent agent-a --stdout
node scripts/memory_cli.js recall --id mem_xxx --as-agent agent-a --stdout
node scripts/memory_cli.js restore --id mem_xxx --as-agent agent-a --stdout
```

`revive` 是 `restore` 的兼容别名。普通 search 不包含归档记录，不要依赖不存在或未文档化的 `--include-archived`。完整流程见 [CLI 归档说明](references/cli.md#archive-and-revive)。

## 11. `archive --scope all` 支持吗？

支持，v1.1.0 会处理 global 与 workspace 两层。也可以分别执行，便于使用不同阈值：

```bash
node scripts/memory_cli.js archive --scope all \
  --apply-decay --min-decay 0.15 --stdout
```

归档不是物理删除。永久删除前先备份并检查重要的 P1 记录。

## 12. 多个 Agent 同时写会丢数据吗？

有可能。唯一临时文件加原子替换能避免半文件和临时文件互撞，但没有锁住完整的 read-modify-write 周期。两个写者读取同一个旧快照时，后写者可能覆盖先写者的修改。

高并发场景应串行化同一 scope 的写入，并在批量 merge、archive、delete 前备份。详见 [并发限制](references/operations.md#concurrent-access)。

## 13. JSON 损坏时会发生什么？

CLI 会失败关闭并返回非零退出码，不会把损坏文件当成空库继续覆盖。先停止写入并复制损坏文件，再从备份恢复或在单独文件中修复、验证。详见 [恢复步骤](references/operations.md#backups-and-corrupt-json)。

## 14. 没有 Node.js 能直接编辑 JSON 吗？

只读检查相对安全，直接写入风险较高，因为会绕过校验、可见性、索引和原子写规则。确需写入时先备份、确认没有并发写者，并按 [memory_schema.json](references/memory_schema.json) 校验。不要用直读 JSON 绕过 private 过滤。

## 15. `compress` 会自动生成安全的记忆吗？

不会。`compress` 只从 transcript 中提取候选片段。Agent 仍需判断价值、摘要、分类和脱敏，再调用 `store`。它不是后台扫描器，也不负责敏感信息检测。

## 16. 如何安装和更新？

当前版本已发布到 npm：

```bash
npm i memory-store-skill
npx memory-store setup --agent codex --mode explicit

# 更新时
npm i memory-store-skill@latest
npx memory-store setup --sync
```

npm 安装本身不运行生命周期脚本，也不修改 Agent 目录。`memory-store setup` / `setup --sync` 只复用当前本地包的安装器，不下载远程代码、不启动子进程，也不修改记忆数据。可用 `--dry-run` 预览，或用 `--agent codex`、`--target <path>` 限定目标。旧 `memory-store-install` / `memory-store-update` 入口在 v1.x 中继续兼容。更新后请新开 Agent 会话。

从源码安装或更新：

```bash
git clone https://github.com/Revolves/memory-store-skill.git
cd memory-store-skill
node scripts/install.js --all
node scripts/install.js --update
```

## 17. 性能有保证吗？

没有固定 SLA。性能受 Node.js 版本、CPU、磁盘、文件大小、记忆内容与查询分布影响。旧基准数据不是当前版本保证；对容量或延迟敏感时，应在目标环境使用当前 Node.js CLI 重新测试。

## 18. 如何调整自动记忆力度？

安装时传入 `--memory-profile off|explicit|balanced|proactive`；未指定时使用安全默认值 `explicit`，而且安装器不会创建记忆数据文件。

```bash
npx memory-store mode
npx memory-store mode balanced --global
npx memory-store mode explicit --workspace
npx memory-store mode --reset --workspace
```

工作区策略优先于全局策略。`off` 和 `explicit` 会拒绝 `--intent automatic` 的访问；`balanced` 每次对话最多自动保留 3 条精选类型，`proactive` 最多 5 条。用户明确要求的操作使用 `--intent explicit`，不受自动策略限制。

## 19. 无参数命令会不会阻塞 Agent 或 CI？

不会。只有 stdin 和 stdout 都连接真实 TTY 时，`memory-store` 无参数才打开数字菜单。管道、CI 和 Agent 工具调用等非 TTY 环境会输出不超过 10 行的精简帮助并退出。传入 `remember`、`recall`、`mode`、`status`、`setup` 或 `maintain` 时也不会进入菜单。

交互菜单中的安装、添加记忆、档位修改和归档都会先显示摘要，并以 `[y/N]` 确认；直接回车不会写入。

## 更多资料

- [SKILL.md](SKILL.md)：Agent 的最小行为规则
- [CLI Reference](references/cli.md)：完整命令与参数
- [Operations and Safety](references/operations.md)：维护、隐私、并发与恢复
- [CHEATSHEET.md](CHEATSHEET.md)：一页速查
