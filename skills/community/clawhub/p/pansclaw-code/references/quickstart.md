# 快速入门

## 构建二进制（仅首次需要）

```bash
cd "/Users/dashi/.openclaw-pansclaw/claw-code-main/rust"
cargo build -p rusty-claude-cli --release
```

二进制位置：`~/.local/bin/claw`（符号链接到 release 构建）

## 首次健康检查

```bash
cd "/Users/dashi/.openclaw-pansclaw/claw-code-main/rust"
./target/release/claw
# 进入 REPL 后执行
/doctor
```

## 交互模式

```bash
~/.local/bin/claw
```

## 单次任务模式

```bash
~/.local/bin/claw --provider ollama --model mistral-small:24b --dangerously-skip-permissions "你的任务"
```

## 配置 API 密钥

**本地 Ollama（推荐，无需 API 密钥）**

```bash
ollama list
# 可用模型：mistral-small:24b, qwen3, llama3, codellama
```

**云端 API**

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export MINIMAX_API_KEY="your-key"
export OPENAI_API_KEY="your-key"
```

## 常用命令

| 命令 | 说明 |
|------|------|
| `/doctor` | 健康检查和诊断 |
| `/status` | 查看状态 |
| `/help` | 帮助信息 |
| `/model <name>` | 切换模型 |
| `/skills` | 查看技能列表 |
| `/mcp` | MCP 服务器管理 |
| `/agents` | 子代理管理 |
