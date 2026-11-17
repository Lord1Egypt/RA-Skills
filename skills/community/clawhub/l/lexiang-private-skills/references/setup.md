# 乐享 MCP 配置向导（私有化部署版）

> **触发场景**：
> - 用户说 "配置乐享"、"setup lexiang"、"连接乐享"
> - 用户首次安装乐享 skill 后
> - MCP 连接失败或返回 401 错误时

---

## 🚀 配置步骤

### Step 1: 获取配置参数

引导用户打开乐享 MCP 配置页面：

```
{乐享私有化域名}/ai/claw
```

> **注意**：私有化版本的域名由企业自定义，请询问用户其乐享访问地址，拼接 `/ai/claw` 路径即可。
> 例如：用户的乐享地址是 `https://lexiang.mycompany.com`，则配置页为 `https://lexiang.mycompany.com/ai/claw`

登录后，用户可在页面上看到：
- **MCP Endpoint**：MCP 服务地址（用于 mcp.json 的 `url` 字段）
- **LEXIANG_TOKEN**：访问令牌（格式 `lxmcp_xxx`）

### Step 2: 确定 mcp.json 路径

| 客户端/平台 | 路径 |
|-------------|------|
| 通用（mcporter） | `~/.mcporter/mcporter.json` |
| WorkBuddy | `~/.workbuddy/mcp.json` |
| Windows | `%USERPROFILE%\.mcporter\mcporter.json` |
| WSL | `~/.mcporter/mcporter.json`（Linux 侧路径） |

### Step 3: 写入 mcp.json

将用户提供的 **MCP Endpoint** 和 **LEXIANG_TOKEN** 填入：

```json
{
  "mcpServers": {
    "lexiang": {
      "url": "用户的MCP_ENDPOINT值",
      "transportType": "streamable-http",
      "headers": {
        "Authorization": "Bearer 用户的LEXIANG_TOKEN值"
      }
    }
  }
}
```

> 如果配置文件已存在且包含其他 mcpServers 条目，应**合并**而非覆盖整个文件。
> **编码要求**：文件必须以 UTF-8 无 BOM 编码保存。

### Step 4: 验证连接

配置完成后，**立即调用** `whoami()` 验证连接。

**成功时**展示欢迎消息：

```
✅ 乐享 MCP 连接成功！

👤 当前用户：{用户姓名}
🏢 绑定乐享：{企业/租户名称}

🎉 配置已就绪，你现在可以这样使用乐享知识库：

💡 试试这样提问：
• "看看我最近访问的知识库有什么更新"
• "我要记录今天的工作内容，为我创建一个乐享文档"
• "搜索关于 XXX 的知识文档"
• "帮我总结一下这个知识库的内容：{知识库链接}"
```

> ⚠️ 不要在输出中回显 LEXIANG_TOKEN 的完整值（安全考虑）

---

## 🔑 AccessToken 生命周期管理

### 阶段 1：未配置 Token

当 MCP 连接失败或无认证信息时：

1. 告知用户需要获取乐享 MCP 的 `LEXIANG_TOKEN`
2. 引导用户打开 `{乐享私有化域名}/ai/claw` 获取配置信息
3. 用户获取后，帮助完成 mcp.json 配置（参见上方步骤）

### 阶段 2：Token 即将过期

当 MCP 返回正常结果但附带过期预警时：

1. **先正常返回本次结果**
2. 在结果末尾附加提醒：

```
⚠️ 您的乐享访问令牌即将过期。请打开以下链接，点击「续期」按钮即可延长有效期（需已登录）：
{乐享私有化域名}/ai/claw
```

### 阶段 3：Token 已过期（401 响应）

1. **不要反复重试**
2. 引导用户续期，原 token 即可恢复，**无需重新获取新 token**：

```
🔒 您的乐享访问令牌已过期。请打开以下链接，点击「续期」按钮即可恢复（无需重新配置）：
{乐享私有化域名}/ai/claw
```

> `{乐享私有化域名}` 从当前 mcp.json 的 `url` 字段中提取主机部分。

---

## 🔄 MCP 连接中断处理

1. **先自动重连一次**：使用 mcp.json 中已有的配置静默重连
2. **重连成功**：继续执行未完成的任务
3. **重连失败**：引导用户确认 mcp.json 配置是否正确，或重新访问 `/ai/claw` 页面检查 token 状态

---

## ❓ 故障排查

| 问题 | 解决方案 |
|------|---------|
| 连接无响应 | 确认 mcp.json 中 `url` 填写的是 MCP Endpoint（非乐享访问域名） |
| 401 未授权 | token 过期，参见上方「Token 已过期」处理步骤 |
| 参数报错 | 执行 `get_tool_schema(tool_name="xxx")` 获取最新参数定义 |
