# ClawAgent鉴权检查

ClawAgent授权流程，**必须按以下步骤执行**：

> 💡 **说明**：授权成功后，Token 会配置到 `ClawAgent` 服务，通过 mcporter 管理。

## 第零步：检查并安装 mcporter（已安装则跳过）

```bash
bash ./setup.sh
```

| 输出 | 处理方式 |
|------|---------|
| `✅ mcporter 已安装` | ✅ 已安装，继续执行第一步 |
| `✅ mcporter 安装完成` | ✅ 安装成功，继续执行第一步 |
| `❌ ERROR: no_npm` | 告知用户：「请先安装 Node.js 和 npm 后重试」 |

## 第一步：检查授权状态（立即返回）

```bash
bash ./setup.sh check_auth
```

| 输出 | 处理方式 |
|------|---------|
| `READY` | ✅ 服务已就绪，直接执行用户任务，**无需后续步骤** |
| `NOT_CONFIGURED` | 向用户展示授权引导模板（见下方），**等待用户提供 Token** |
| `ERROR:*` | 告知用户具体错误信息，并引导用户提供 Token |

> ⛔ **严格禁止**：收到 `NOT_CONFIGURED` 后，必须先向用户展示引导信息，**等待用户回复 Token**，才能进行第二步。

## 第二步：用户提供 Token 后，自动保存

> ✅ **触发条件**：用户在新消息中提供了 Token（如一串字符、密钥等），**才执行本步骤**。

```bash
bash ./setup.sh save_token <用户提供的Token>
```

| 输出 | 处理方式 |
|------|---------|
| `TOKEN_SAVED` | ✅ Token 已保存，继续执行第三步验证 |
| `ERROR:no_token` | 告知用户：「未收到 Token，请重新提供。」 |
| `ERROR:save_failed` | 告知用户：「Token 保存失败，请重试。」 |
| `ERROR:mcporter_not_found` | 告知用户：「缺少依赖，请先安装 Node.js。」 |

## 第三步：验证 Token 是否有效

```bash
bash ./setup.sh verify_token
```

| 输出 | 处理方式 |
|------|---------|
| `TOKEN_VALID` | ✅ Token 有效，继续执行用户任务 |
| `ERROR:token_invalid` | 告知用户：「您提供的 Token 无效，请检查后重新提供。」 |
| `ERROR:save_failed` | 告知用户：「Token 配置异常，请重试。」 |

## 授权引导模板

当第一步输出 `NOT_CONFIGURED` 时，向用户展示：

> 🔑 **需要配置ClawAgent Token**
>
> 请先获取您的ClawAgent Token：
>
> 1. 登录并打开系统左侧菜单**龙虾**获取 Token
> 2. 复制您的 Token
> 3. **直接将 Token 发送给我**，我会自动帮您配置
>
> ⚠️ Token 是您的私密凭证，请勿泄露给他人
>
> ✅ **提供 Token 后，我会自动保存并验证，验证通过后即可使用ClawAgent的所有功能**

> ⛔ **AI 注意**：展示上方引导信息后，**必须停止等待**，不得自动执行任何配置命令。只有当用户在下一条新消息中提供了 Token 后，才能继续执行第二步。

## 人工兜底

如果自动保存失败，可手动配置 Token：

```bash
# 使用用户提供的 Token 写入 mcporter ClawAgent
mcporter config add ClawAgent "https://mcp.jiadouai.com/mcp" \
    --header "Authorization=<用户提供的Token>" \
    --transport http \
    --scope home
```

配置完成后，执行 `bash ./setup.sh verify_token` 验证。

## 错误说明

| 错误 | 含义 |
|------|------|
| `ERROR:mcporter_not_found` | 缺少依赖，请先安装 Node.js |
| `ERROR:not_configured` | 用户尚未配置 Token，等待用户提供 |
| `ERROR:no_token` | 未提供 Token 参数 |
| `ERROR:token_invalid` | Token 鉴权失败，需用户提供有效 Token |
| `ERROR:save_failed` | Token 写入配置失败，需重试 |
| `ERROR:network` | 网络请求失败，检查网络后重试 |
