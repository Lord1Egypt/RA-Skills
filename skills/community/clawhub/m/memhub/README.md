# MemHub Skill

MemHub 是一个无服务端、Git-first 的个人 AI 记忆协议。本 Skill 让任意支持 Skill 的 Agent 能够读写、归档和同步用户的跨 Agent 统一记忆仓库。

## 能力

- 读取长期记忆上下文：`context --pack brief|standard|full|project`
- 写入默认 inbox：`remember`
- 检查与展示 inbox：`inbox list/show`
- 半自动归档到 canonical memory：`promote --dry-run/--apply`
- 导出给 chatbot 的上下文：`export chatbot`
- GitHub/Gitee 同步：OAuth、token fallback、SSH fallback

## 安装到任意支持 Skill 的 Agent

将本目录 `skills/memhub/` 复制到对应 skills 目录，或通过 SkillHub/ClawHub 安装。

## 配置仓库路径

```bash
export MEMHUB_REPO=~/memhub-data
```

必须通过 `--repo` 或 `MEMHUB_REPO` 明确指定专用记忆仓库；CLI 不会把当前目录隐式当作记忆仓库。

## 首次初始化

```bash
python scripts/memhub.py --repo "$MEMHUB_REPO" init --name dateng --role "Product Manager"
```

## 配置 GitHub/Gitee 同步

推荐使用 OAuth setup 命令，而不是手动配置 remote。GitHub 默认走官方 Device Flow。
Gitee 交互式配置会先展示内置 Broker 域名并请求确认；非交互环境需明确提供可信 Broker，
或使用自己的 OAuth 配置。

### GitHub / Gitee 授权

```bash
python scripts/memhub.py --repo "$MEMHUB_REPO" sync setup github --repo-name mymemhub
python scripts/memhub.py --repo "$MEMHUB_REPO" sync setup gitee --repo-name mymemhub --broker-url https://<trusted-broker>
```

GitHub 使用 Device Flow。明确选择 Broker 时，流程为：

1. CLI 调 broker 创建授权 session，拿到 `auth_url`；
2. CLI 打开该 URL，用户在 GitHub/Gitee 页面点击确认授权；
3. broker 在服务端用 `client_secret` 换取 token；
4. CLI 轮询 broker 拿到 token，存入记忆仓库之外的本机凭据目录（0600）。

无浏览器环境加 `--no-browser`，CLI 会打印 URL 供手动打开。

### 高级覆盖 / Fallback

可选配置项：`MEMHUB_OAUTH_BROKER_URL`、`MEMHUB_GITEE_OAUTH_BROKER_URL`、
`MEMHUB_GITHUB_CLIENT_ID`、`MEMHUB_GITEE_CLIENT_ID`、
`MEMHUB_GITEE_CLIENT_SECRET`。只放在进程环境或显式 `--env-file` 中，
不要写进仓库、文档示例或聊天。

### Token / SSH Fallback

```bash
# Token fallback
python scripts/memhub.py --repo "$MEMHUB_REPO" sync setup github --auth token --repo-name mymemhub

# SSH fallback
python scripts/memhub.py --repo "$MEMHUB_REPO" sync setup github --auth ssh --remote-method ssh --owner <login> --repo-name mymemhub --no-create
```

OAuth/token 保存在记忆仓库**之外**的本机目录（macOS 默认 `~/Library/Application Support/memhub/secrets/`，Linux 默认 `~/.local/state/memhub/secrets/`，可用 `MEMHUB_SECRETS_DIR` 覆盖），文件权限 0600、目录 0700。仓库因此永远不含凭据，clone 与同步也不会带走它们。

不要把 OAuth app 的 client secret、token 或 authorization code 提交到仓库或在聊天中复述。第三方 OAuth broker 不会被隐式使用，必须由 `--broker-url` 或 `MEMHUB_*_OAUTH_BROKER_URL` 明确指定。`doctor` 默认离线，只有 `--network` 才会探测 broker。

## 常用命令

```bash
python scripts/memhub.py --repo "$MEMHUB_REPO" context --pack brief
python scripts/memhub.py --repo "$MEMHUB_REPO" remember "要记住的内容" --type fact --source agent
python scripts/memhub.py --repo "$MEMHUB_REPO" inbox list
python scripts/memhub.py --repo "$MEMHUB_REPO" inbox show <filename-or-id-fragment>
python scripts/memhub.py --repo "$MEMHUB_REPO" promote --dry-run
python scripts/memhub.py --repo "$MEMHUB_REPO" promote --apply
python scripts/memhub.py --repo "$MEMHUB_REPO" export chatbot
python scripts/memhub.py --repo "$MEMHUB_REPO" sync status
python scripts/memhub.py --repo "$MEMHUB_REPO" sync
```

## Agent 使用原则

- 读取前：如果任务依赖长期记忆，先 `sync`，再 `context --pack brief`。
- 写入时：用户明确要求记忆，或形成稳定决策/偏好/事实时，写入 inbox。
- 写入后：已授权 auto-sync 时由节流逻辑处理；manual-sync 模式只在用户要求时执行 `sync`。
- 归档时：先 `promote --dry-run`，确认后再 `promote --apply`，然后 `sync`。
- setup：只有用户明确要求配置或切换同步服务时才执行。
- 自动同步：用户明确运行 setup/onboard 后默认启用；如只想手动同步，添加 `--manual-sync`。
- 失败：同步失败时不要删除本地数据；报告错误并保留本地文件。

CLI 不会隐式读取 cwd 或 home 的 `.env`。需要文件配置时使用
`--env-file /path/to/memhub.env`，且只加载受支持的 `MEMHUB_*` 键。

## 发布包内容

发布到 SkillHub/ClawHub 时应包含：

```text
SKILL.md
README.md
permissions.json
scripts/memhub.py
templates/context-pack.md.j2
```

不应包含：

```text
__pycache__/
*.pyc
.git/
本机凭据目录下的 secrets 文件
用户个人记忆数据
```

## License

MIT-0
