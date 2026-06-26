# 安装与部署参考

## 安装方式

### npm (推荐)
```bash
npm install -g openclaw
openclaw setup
openclaw onboard
```

### 更新
```bash
openclaw update
# 或
npm update -g openclaw
```

### 卸载
```bash
openclaw uninstall --all --yes
npm uninstall -g openclaw
```

## 环境变量

### 优先级 (从高到低)
1. 进程环境 (父shell/守护进程)
2. 当前目录 `.env`
3. `~/.openclaw/.env` (全局)
4. 配置 `env` 块 (openclaw.json)
5. 登录shell导入 (可选)

规则: 永不覆盖现有值。

### 配置中设置环境变量
```json5
{ env: { OPENROUTER_API_KEY: "sk-or-...", vars: { GROQ_API_KEY: "gsk-..." } } }
```

### 配置中引用环境变量
```json5
{ models: { providers: { "my-api": { apiKey: "${MY_API_KEY}" } } } }
```

### Shell环境导入
```json5
{ env: { shellEnv: { enabled: true, timeoutMs: 15000 } } }
```
或: `OPENCLAW_LOAD_SHELL_ENV=1`

## 目录结构
```
~/.openclaw/
├── openclaw.json              # 主配置
├── openclaw.json.bak          # 自动备份
├── .env                       # 全局环境变量
├── agents/
│   └── <agentId>/
│       ├── agent/
│       │   └── auth-profiles.json  # 认证凭证
│       ├── sessions/
│       │   ├── sessions.json       # 会话状态
│       │   └── <sessionId>.jsonl   # 对话记录
│       └── models.json             # 自定义提供商
├── credentials/               # 渠道凭证
│   └── whatsapp/
├── cron/
│   ├── jobs.json              # 定时任务
│   └── runs/                  # 运行历史
├── hooks/                     # 用户Hooks
├── skills/                    # 用户Skills
├── logs/                      # 日志
├── memory/
│   └── <agentId>.sqlite       # 记忆索引
├── sandboxes/                 # 沙箱工作区
└── workspace/                 # 默认工作区(或自定义路径)
```

## 平台特殊说明

### macOS
- 服务: LaunchAgent `~/Library/LaunchAgents/bot.molt.gateway.plist`
- 安装: `openclaw gateway install`
- 日志: `~/.openclaw/logs/gateway.log`
- 权限: 可能需要辅助功能/完全磁盘访问权限
- 重置权限: `tccutil reset All bot.molt.mac.debug`

### Linux
- 服务: systemd用户单元
- 需要lingering: `sudo loginctl enable-linger $USER`
- 安装: `openclaw gateway install`
- 日志: `journalctl --user -u openclaw-gateway.service`
- 浏览器: 推荐安装Google Chrome替代Snap Chromium

### Docker
```bash
docker run -v ~/.openclaw:/root/.openclaw openclaw/openclaw
```

### Raspberry Pi
- 支持ARM64
- 推荐Node.js 20+
- 内存有限时用较小模型

## 初始化流程
```bash
openclaw setup                 # 创建配置+工作区
openclaw onboard               # 交互式引导(模型+认证+渠道)
openclaw configure              # 交互式配置向导
openclaw gateway install        # 安装系统服务
openclaw gateway start          # 启动网关
```

## 诊断
```bash
openclaw doctor [--deep] [--fix]   # 健康检查+修复
openclaw status [--all] [--deep]   # 状态诊断
openclaw health                    # 网关健康
```

## 重要环境变量
| 变量 | 说明 |
|------|------|
| `OPENCLAW_CONFIG_PATH` | 配置文件路径 |
| `OPENCLAW_STATE_DIR` | 状态目录(默认~/.openclaw) |
| `OPENCLAW_GATEWAY_PORT` | 网关端口 |
| `OPENCLAW_GATEWAY_TOKEN` | 网关认证令牌 |
| `OPENCLAW_SKIP_CRON` | 禁用定时任务 |
| `OPENCLAW_LOAD_SHELL_ENV` | 启用shell环境导入 |

## Docker 部署

### 适用场景
- 需要隔离环境
- VPS/云服务器部署
- 不想在主机安装Node.js

### 快速启动
```bash
docker run -it --name openclaw \
  -v ~/.openclaw:/root/.openclaw \
  -p 18789:18789 \
  openclaw/openclaw:latest
```

### docker-compose
```yaml
services:
  openclaw:
    image: openclaw/openclaw:latest
    volumes:
      - ~/.openclaw:/root/.openclaw
    ports:
      - "18789:18789"
    restart: unless-stopped
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
```

### 注意事项
- WhatsApp需要持久化 `~/.openclaw/credentials/`
- 浏览器需要额外Chrome安装
- 使用 `--network host` 访问本地Ollama

## 更新

### 推荐方式
```bash
openclaw update          # 自动更新
# 或
npm update -g openclaw   # npm更新
```

### 回滚
```bash
npm install -g openclaw@<version>   # 安装指定版本
```

### 更新前检查
```bash
openclaw --version       # 当前版本
openclaw doctor          # 健康检查
```

## 迁移到新机器

### 步骤
1. 旧机器: 停止网关 `openclaw gateway stop`
2. 复制整个 `~/.openclaw/` 到新机器
3. 新机器: 安装openclaw `npm install -g openclaw`
4. 新机器: `openclaw doctor --fix` 修复路径
5. 新机器: `openclaw gateway install && openclaw gateway start`

### 最小迁移(仅配置)
```bash
# 旧机器
scp ~/.openclaw/openclaw.json user@new:~/.openclaw/
scp -r ~/.openclaw/credentials/ user@new:~/.openclaw/
# 新机器
openclaw setup
openclaw channels login   # 重新配对WhatsApp等
```

### 工作区迁移
```bash
# 如果用了git
cd ~/.openclaw/workspace && git push
# 新机器
git clone <repo> ~/.openclaw/workspace
```

## 卸载

### 完全卸载
```bash
openclaw uninstall --all --yes   # 停止服务+删除状态
npm uninstall -g openclaw        # 删除CLI
```

### 仅停止服务
```bash
openclaw gateway stop
openclaw gateway uninstall
```

### 手动清理
```bash
trash ~/.openclaw                # 删除所有状态
trash ~/Library/LaunchAgents/bot.molt.gateway.plist  # macOS服务
```
