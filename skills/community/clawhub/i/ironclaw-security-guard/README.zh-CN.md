# OpenClaw IronClaw Security Guard

给 OpenClaw 加上一层轻量但实用的防御：拦危险调用、识别 prompt injection、发送前脱敏，并留下审计日志。

English README: [README.md](./README.md)

## 这个插件解决什么问题

在开源模型、本地工具和自动化 agent 工作流里，最常见的风险通常是：

- 危险 shell 命令过早执行
- 敏感路径或凭据被带进工具参数
- 外部内容试图劫持系统行为
- agent 把 token、密钥或私密信息发到外部

`ironclaw-security-guard` 通过 OpenClaw 的插件 hook 层增加防护，而不是假装自己是完整沙箱。

## 它会做什么

- 拦截高风险 shell 命令
- 保护敏感路径
- 识别 prompt injection 模式
- 阻止向外部发送明显的 secret
- 在消息发送前自动脱敏
- 记录 JSONL 审计日志
- 提供手动检查工具 `ironclaw_security_scan`

## 快速安装

把仓库路径加入 OpenClaw 的 `plugins.load.paths`，允许 `ironclaw-security-guard`，再在 `plugins.entries` 里启用。

可直接复制的配置例子见 [examples/openclaw-config.example.json](./examples/openclaw-config.example.json)。

为社区发布准备的 npm 包名：

```bash
@wd041216-bit/openclaw-ironclaw-security-guard
```

## 60 秒验证

先跑一轮轻量回归：

```bash
npm test
```

再跑一次手动安全扫描示例：

```bash
node --input-type=module -e "import('./src/config.ts').then(async ({ normalizeSecurityConfig }) => { const { createSecurityScanTool } = await import('./src/tool.ts'); const writes = []; const tool = createSecurityScanTool({ config: normalizeSecurityConfig({}), audit: { write: async (event) => writes.push(event) } }); const result = await tool.execute('demo', { toolName: 'shell', content: 'rm -rf /tmp/demo', redactPreview: true }); console.log(result.content[0].text); })"
```

## 典型能力

- 拦截 `rm -rf`、`git reset --hard`、`curl ... | sh` 等危险模式
- 标记 `.env`、SSH key、`.pypirc`、`.npmrc`、云凭据等敏感路径
- 识别 “ignore previous instructions” 这类注入模式
- 在发消息前把敏感 token 替换成 `[REDACTED:...]`
- 可选地只允许访问 allowlist 中的外部 host

完整示例见 [examples/manual-scan-example.md](./examples/manual-scan-example.md)。

## 配置项

核心配置来自 [openclaw.plugin.json](./openclaw.plugin.json)：

- `enabled`
- `monitorOnly`
- `blockDestructiveShell`
- `protectSensitivePaths`
- `redactSecretsInMessages`
- `networkDenyByDefault`
- `allowedOutboundHosts`
- `auditLogPath`
- `protectedPathPatterns`
- `blockedCommandPatterns`

如果你想把它作为本地 agent 的默认安全兜底，推荐开启外联 allowlist，并保持 `monitorOnly=false`：

```json
{
  "plugins": {
    "entries": [
      {
        "id": "ironclaw-security-guard",
        "config": {
          "monitorOnly": false,
          "networkDenyByDefault": true,
          "allowedOutboundHosts": ["localhost", "127.0.0.1"]
        }
      }
    ]
  }
}
```

## 设计边界

它受 [IronClaw](https://github.com/nearai/ironclaw) 启发，但不是完整运行时隔离方案。

它适合做：

- 轻量安全兜底
- prompt / tool 参数层面的前置扫描
- agent 工作流里的防误操作保护

它不负责：

- 提供 WASM sandbox
- 容器级隔离
- 替代系统级安全控制
