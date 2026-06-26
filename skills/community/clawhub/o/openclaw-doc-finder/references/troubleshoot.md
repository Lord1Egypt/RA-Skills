# OpenClaw 故障排除速查

> 摘录自 `gateway/troubleshooting.md` + `channels/troubleshooting.md`

---

## 诊断命令阶梯（必按顺序执行）

```bash
openclaw status
openclaw gateway status
openclaw logs --follow
openclaw doctor
openclaw channels status --probe
```

**健康信号：**
- `openclaw gateway status` 显示 `Runtime: running` + `RPC probe: ok`
- `openclaw doctor` 无 blocking 级别报错
- `openclaw channels status --probe` 显示 connected/ready

---

## 常见报错与解决方案

### 1. Anthropic 429 / Extra Usage Required

**症状：** 日志出现 `HTTP 429: rate_limit_error: Extra usage is required for long context requests`

**排查：**
```bash
openclaw logs --follow
openclaw models status
openclaw config get agents.defaults.models
```

**原因：** 使用的模型启用了 `context1m` 但凭证无 long-context 权限

**解法（三选一）：**
1. 关闭该模型的 `context1m` 参数
2. 使用有 `Extra Usage` 权限的 Anthropic API key
3. 配置 fallback 模型

→ 详细：[Anthropic Provider](https://docs.openclaw.ai/providers/anthropic)

---

### 2. Channel 连接失败（Discord/Telegram/飞书等）

**症状：** `openclaw channels status` 显示 channel 未连接

**排查：**
```bash
openclaw channels status --probe
openclaw logs --follow --channel discord
```

**常见原因：**
- Bot token 过期或权限不足
- Webhook URL 不可达
- OAuth 授权过期（飞书/Telegram）

**解法：**
1. 重新配置 channel token：`openclaw config set channels.<name>.token <token>`
2. 检查 bot 权限（Discord 需要 `Gateway Intent`）
3. 飞书：重新触发 OAuth 授权流程

→ 详细：[Channel Troubleshooting](https://docs.openclaw.ai/channels/troubleshooting)

---

### 3. Gateway 无法启动

**症状：** `openclaw gateway start` 失败

**排查：**
```bash
openclaw doctor
openclaw logs
cat ~/.openclaw/openclaw.json | python3 -m json.tool  # 验证 JSON 格式
```

**常见原因：**
- 端口 18789 被占用 → `lsof -i :18789`
- 配置文件 JSON 格式错误
- Node 版本不兼容（需要 Node 22+）

→ 详细：[Gateway Troubleshooting](https://docs.openclaw.ai/gateway/troubleshooting)

---

### 4. 技能安装失败（clawhub rate limit）

**症状：** `clawhub install <skill>` 报 rate limit

**解法：**
1. 加延迟重试：`sleep 60 && clawhub install <skill>`
2. 手动从 GitHub 安装：`npx skills add <owner/repo@skill>`
3. 使用 skillhub 内部搜索

→ 详细：[ClawHub 工具](https://docs.openclaw.ai/tools/clawhub)

---

### 5. 凭证/secrets 问题

**症状：** API 调用报 401/403，或 `secrets plan contract` 相关报错

**排查：**
```bash
openclaw config get providers
# 检查环境变量
env | grep -i api
```

**解法：**
1. 确认 `.env` 文件存在且包含正确 key
2. 验证 API key 有对应产品权限
3. 使用 `openclaw secrets list` 查看已加载凭证

→ 详细：[Secrets Management](https://docs.openclaw.ai/gateway/secrets)

---

### 6. 远程访问/VPS 连接问题

**症状：** 远程无法连接 gateway

**排查：**
```bash
openclaw gateway status
openclaw config get gateway.host
```

**解法：**
1. 确认 gateway host 设为 `0.0.0.0`（而非 `127.0.0.1`）
2. 检查防火墙/安全组放行 18789 端口
3. 建议配合 Tailscale：见 `gateway/tailscale.md`

→ 详细：[Remote Gateway](https://docs.openclaw.ai/gateway/remote) | [VPS 部署](https://docs.openclaw.ai/vps)

---

### 7. openclaw doctor 报 scope missing

**症状：** `openclaw doctor` 警告 `gateway probe missing scope`

**原因：** 使用的 token 没有完整的 scopes

**解法：**
1. 生成带显式 scopes 的新 token
2. 或忽略该警告（仅影响部分诊断功能）

→ 详细：[Gateway Doctor](https://docs.openclaw.ai/gateway/doctor)

---

### 8. image_generate 报 "No image-generation provider registered"

**症状：** `image_generate` 工具报错 `No image-generation provider registered for <provider>`

**排查：**
```bash
# 确认 provider 插件是否完整加载
openclaw config get plugins.allow
openclaw config get plugins.entries.<provider>.enabled

# 确认 API key 是否在 .env
cat ~/.openclaw/.env | grep -i API_KEY

# 确认 imageGenerationModel 配置
openclaw config get agents.defaults.imageGenerationModel
```

**根因：** `plugins.allow` 是白名单机制——当非空时，只有列表内的插件会完整加载（包括 image generation provider 注册）。即使 `entries.<provider>.enabled: true` 也会被 allow 列表覆盖。

**修复步骤（以 Google 为例）：**

1. **添加 API key 到 `.env`**（daemon 环境不读 openclaw.json 的 env 块）：
   ```bash
   echo 'GEMINI_API_KEY=your_key' >> ~/.openclaw/.env
   ```

2. **把 provider 加入 `plugins.allow`**：
   ```bash
   openclaw config set plugins.allow '["telegram","discord","openclaw-weixin","firecrawl","tavily","exa","openclaw-lark","google"]'
   ```

3. **配置 imageGenerationModel**：
   ```bash
   openclaw config set agents.defaults.imageGenerationModel.primary 'google/gemini-3.1-flash-image-preview'
   ```

4. **重启 gateway**：
   ```bash
   openclaw gateway restart
   ```

**坑点：**
- `gemini-3-flash-image-preview` 不存在，正确模型名是 `gemini-3.1-flash-image-preview`
- `BUILTIN_IMAGE_GENERATION_PROVIDERS` 为空数组，所有 image gen provider 由插件 `register()` 注册
- Google 插件的 image generation 源码位于 `extensions/google/image-generation-provider.ts`

**验证：**
```bash
# 测试生图
openclaw config get agents.defaults.imageGenerationModel
# 然后调用 image_generate 工具测试
```

→ 详细：[Configuration Reference - plugins.allow](https://docs.openclaw.ai/gateway/configuration-reference) | [Google Provider](https://docs.openclaw.ai/providers/google)

---

## 诊断决策树

```
用户报告问题
    │
    ├─ CLI 命令报错    → openclaw doctor → 读对应报错章节
    │
    ├─ Channel 连接问题 → openclaw channels status --probe
    │                       │
    │                       ├─ Token 问题 → channels/<name>.md
    │                       └─ 网络问题   → network.md
    │
    ├─ 配置问题         → gateway/configuration.md
    │
    ├─ 模型/供应商问题  → providers/<name>.md
    │
    └─ 性能/日志问题    → gateway/logging.md → gateway/troubleshooting.md
```
