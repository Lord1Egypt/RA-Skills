# 连接和认证

已有独行录 MCP 工具时直接使用。只有用户需要接入、切换账户或恢复独行录授权时才读本页。先保存现有 opcmenu 配置以便恢复，合并自己的条目，不覆盖其他服务器，不同时保留 OAuth 和过期的 Authorization 头。

## 匿名与 OAuth

端点：`https://mcp.opcmenu.com/mcp`，传输为 Streamable HTTP。公开查询可以匿名执行；本人数据和写操作需要登录。授权由宿主引导浏览器执行，OAuth 凭证由宿主管理；不要代收密码、token 或完整 OAuth 回调链接到聊天里。

以下为 2026-09-07 核对的官方配置形式。宿主支持这些形式不等于独行录在每个版本上都通过登录测试；接入后验证工具发现、一次公开查询及用户需要时的一次本人只读查询，再报告哪些已成功。

### Codex

注册远程服务：

```sh
codex mcp add opcmenu --url https://mcp.opcmenu.com/mcp
```

需要账户能力时，由用户完成登录：

```sh
codex mcp login opcmenu
```

Codex 支持 OAuth，也支持静态 Bearer 环境变量；不是只能使用环境变量。已有 `bearer_token_env_var` / `http_headers.Authorization` 时先检查是否在覆盖 OAuth。静态模式所用环境变量必须能被启动 Codex 的进程继承；终端 shell 与桌面启动环境可能不同。

[Codex 官方 MCP 文档](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)

### Claude Code

```sh
claude mcp add --transport http opcmenu https://mcp.opcmenu.com/mcp --scope user
```

需要登录时在 Claude Code 的 `/mcp` 中选 opcmenu 并完成认证。已经设置的静态 Authorization 头失效时，应修复或移除该头，不能假定宿主自动切回 OAuth。

[Claude Code 官方 MCP 文档](https://code.claude.com/docs/en/mcp)

### OpenClaw

匿名公开查询配置：

```sh
openclaw mcp set opcmenu '{"url":"https://mcp.opcmenu.com/mcp","transport":"streamable-http"}'
```

需要账户能力时切到 OAuth，然后登录：

```sh
openclaw mcp configure opcmenu --auth oauth
openclaw mcp login opcmenu
```

配置位于 `mcp.servers`；当前官方支持 headers 的 `${ENV_VAR}` 插值。不要沿用“OpenClaw 只能明文写 token”的旧说法。多人网关不能共享某个人的账户密钥；账户隔离应按宿主官方 per-requester 文档配置。

[OpenClaw 官方 MCP CLI](https://docs.openclaw.ai/cli/mcp) · [配置参考](https://docs.openclaw.ai/gateway/configuration-reference)

### WorkBuddy

在 WorkBuddy 的 MCP 配置入口添加以下服务器，或合并到用户级 `~/.workbuddy/mcp.json` 的 `mcpServers` 中：

```json
{
  "mcpServers": {
    "opcmenu": {
      "type": "streamableHttp",
      "url": "https://mcp.opcmenu.com/mcp"
    }
  }
}
```

公开查询不放凭证；需要登录时按宿主的 OAuth 流程授权。原生市场连接器的 Token 表单由连接器包声明，不能把其 `${VAR}` 形式随意搬到不同的手工配置入口。装好一个 SKILL.md 也不代表已配置 MCP 或已登录。

[WorkBuddy MCP 使用文档](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/MCP-Guide) · [连接器规范](https://open.workbuddy.cn/docs/connector)

### TRAE / TraeWork

TraeCode（TRAE IDE 中国版）支持官方 `trae-cn://` MCP 导入链接；链接配置只包含公开端点，不包含密钥。用户需在客户端检查配置并确认导入。TraeWork 是不同客户端，使用设置 → MCP → 选择本地或云端 → 创建 → 手动配置，不能套用 IDE 导入链接。

两者均先添加 Streamable HTTP 端点 `https://mcp.opcmenu.com/mcp`；账户授权方式以该客户端当前界面为准，不能把导入成功当成 OAuth 已验证。

[TraeCode 官方导入链接说明](https://docs.trae.cn/ide_mcp-server-install-links)

### Hermes 与其他客户端

Hermes 的 `~/.hermes/config.yaml` 支持：

```yaml
mcp_servers:
  opcmenu:
    url: https://mcp.opcmenu.com/mcp
    auth: oauth
```

由宿主浏览器完成授权。其他客户端使用其官方远程 MCP 入口填入同一个端点；字段名称随宿主变化，不假设存在统一的 JSON 配置。

[Hermes 官方 MCP 配置](https://hermes-agent.nousresearch.com/docs/reference/mcp-config-reference)

## 静态设备密钥备用方式

OAuth 不可用或用户指定静态配置时，让用户在 `https://opcmenu.com/connect` 登录、生成设备密钥并填入其信任的宿主凭证表单。也可由用户在本地交互终端运行官网 `install.sh` 的静态密钥模式。不要要求用户将密钥贴回聊天，不扫描其他客户端配置或凭据文件来找密钥。

设备可在独行录的已接入设备界面或 `revoke_my_device` 中吊销。失效后重新授权或换发对应设备，不尝试其他账户的凭证。

维护自建登录集成时，`POST /v1/auth/agent` 的 `client` 只能是 `codex`、`claude-code`、`openclaw`、`hermes`、`workbuddy`、`web`、`app`、`other`；通用集成用 `other`，**不能用 `agent`**。`x-opc-client: agent` 是请求头，与该枚举不是同一字段。手机验证码在用户本地输入，返回 token 直接存入受保护的本地凭据存储，不能写入工具输出、终端日志或聊天。

## 故障定位

- 没有可用工具：区分“技能已安装”“MCP 已配置”“连接已建立”，重新发现工具后再判断。
- 401 / 未登录 / invalid_token：本人操作需要授权；在宿主重新登录或更换设备密钥。公开只读任务可继续匿名完成。
- 406：HTTP 客户端需要 `Accept: application/json, text/event-stream`。
- SSH / 远程宿主：浏览器回调必须回到运行 MCP 客户端的环境；按宿主远程授权文档处理，不把回调 token 或验证码发布到聊天。
- 查询成功不等于写权限已验证；未运行的步骤要明确保留为未验证。
