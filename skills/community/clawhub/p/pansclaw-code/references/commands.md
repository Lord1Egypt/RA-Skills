# CLI 命令参考

## 二进制位置

```
~/.local/bin/claw
```

符号链接到：`/Users/dashi/.openclaw-pansclaw/claw-code-main/rust/target/release/claw`

## 顶层命令

```bash
claw [OPTIONS] [COMMAND]

# 常用选项
--model <MODEL>              # 选择模型
--output-format text|json    # 输出格式
--permission-mode <MODE>     # 权限模式
--dangerously-skip-permissions  # 跳过权限确认
--provider <NAME>           # 提供商：ollama, minimax, anthropic, openai
--resume [SESSION]           # 恢复会话
```

## 子命令

### prompt - 单次任务

```bash
claw prompt "总结这个仓库"
claw --model sonnet prompt "review this diff"
claw --output-format json prompt "status"
```

### 交互模式

```bash
claw
```

### 认证

```bash
claw login     # OAuth 登录
claw logout    # 登出
```

### 状态和调试

```bash
claw status           # 查看状态
claw sandbox         # 沙盒模式
claw agents          # 列出代理
claw mcp             # MCP 服务器
claw skills          # 技能列表
claw system-prompt   # 系统提示
```

## 配置文件优先级

1. `~/.claw.json`
2. `~/.config/claw/settings.json`
3. `<repo>/.claw.json`
4. `<repo>/.claw/settings.json`
5. `<repo>/.claw/settings.local.json`

## REPL 内命令

| 命令 | 说明 |
|------|------|
| `/help` | 帮助 |
| `/status` | 状态 |
| `/doctor` | 健康检查 |
| `/model <name>` | 切换模型 |
| `/permissions` | 权限管理 |
| `/session` | 会话管理 |
| `/cost` | 成本统计 |
| `/skills` | 技能管理 |
| `/mcp` | MCP 管理 |
| `/agents` | 代理管理 |
| `/compact` | 压缩上下文 |
| `/diff` | Git 差异 |
| `/commit` | Git 提交 |
| `/export` | 导出会话 |
| `/hooks` | 钩子管理 |
