# 领星官方 MCP 安装引导

本文件只用于安装和鉴权配置。不要扩展为业务工具清单、接口参考或数据操作教程。

## 必须向用户展示的图文引导

在请求用户提供 MCP Server URL 或 `X-Mcp-Key` 前，按顺序发送下面的文字和领星官方截图。即使图片无法显示，也要保留完整文字步骤。

### 第 1 步：打开管理 MCP

请用户登录领星 ERP，进入【AI助手】，点击输入框附近的【MCP】，再点击【管理MCP】。此操作必须由用户本人完成。

![进入领星 AI 助手](../assets/mcp-install/01-open-ai-assistant.png)

![在领星 AI 助手中点击管理 MCP](../assets/mcp-install/02-open-manage-mcp.png)

### 第 2 步：进入第三方应用配置

在【管理MCP】窗口找到【领星MCP】，点击“复制链接到第三方APP使用”一类入口。页面文案若已更新，以当前领星页面为准。

![在管理 MCP 中进入第三方应用配置](../assets/mcp-install/03-third-party-app-config.png)

### 第 3 步：分别复制 URL 和 X-Mcp-Key

在第三方配置页分别点击【复制服务器 URL】与【复制鉴权密钥（X-Mcp-Key）】。两项缺一不可；密钥与当前领星帐号绑定，不要分享给其他人。

以上三张截图均来自领星官方 MCP 指引，已保存在 skill 内，不依赖远程图片 URL。

## 告诉用户如何安全提供给 Agent

优先使用以下话术：

> 请不要把完整 `X-Mcp-Key` 发在普通聊天、群聊或工单里。若当前客户端弹出安全凭据/Secret 输入框，请把从领星复制的服务器 URL 与密钥分别粘贴到对应字段；密钥字段名为 `X-Mcp-Key`。如果没有安全输入框，请在本机 MCP 配置中自行填入下面的占位位置，保存后只回复“已配置”，无需把密钥发给我。

若当前客户端提供安全凭据输入，收集：

- `MCP Server URL`：用户从【管理MCP】复制的完整 HTTPS URL；
- `X-Mcp-Key`：用户从同一页面复制的完整鉴权密钥。

Agent 接收后只显示掩码，例如 `****abcd`，不要复述完整值。

## 通用配置形状

不同客户端的字段名可能略有差异，优先使用客户端原生的 MCP 配置界面。需要向用户展示本地填写示例时，只使用占位符：

```json
{
  "mcpServers": {
    "lingxing-mcp": {
      "type": "streamableHttp",
      "url": "<从领星复制的 MCP Server URL>",
      "headers": {
        "X-Mcp-Key": "<仅在本机安全填写，不要发送到普通聊天>"
      }
    }
  }
}
```

若客户端使用 `transport` 字段，则选择或填写 `streamable_http`；不要同时猜测多个不受客户端支持的字段。

## 连接验证

只验证以下结果：

1. MCP 服务器可连接；
2. `X-Mcp-Key` 鉴权通过；
3. 客户端能完成工具发现。

不要调用任何工具读取库存、订单、Listing、销售、利润、广告或其他业务数据，也不要执行新增、修改、删除等写操作。

## 官方信息摘要

- 超级管理员需在【业务配置】→【开放接口】→【MCP】启用功能，仅限付费用户。
- MCP Server URL 与当前领星帐号的数据权限绑定。
- 传输方式为 Streamable HTTP（HTTP Streaming）。
- 只配置 URL 而未配置 `X-Mcp-Key` 会导致鉴权失败。
- 密钥泄露时，由用户在【管理MCP】页面手动重新生成。

来源：<https://www.lingxing.com/help/article/mcp>
