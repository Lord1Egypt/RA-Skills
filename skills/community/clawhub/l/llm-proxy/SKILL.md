# LLM Proxy Skill

LLM API 代理服务，统一管理多个 LLM Provider，支持内容安全审计。

## 功能

- 多 Provider 统一代理（22+ 提供商）
- 内容安全审计（恶意指令检测、敏感内容过滤）
- 流式响应实时检测
- 健康状态监控

---

## 使用方法

### 启动代理

```
启动llm-proxy
```

### 停止代理

```
停止llm-proxy
```

### 查看状态

```
llm-proxy状态
```

### 重启代理

```
重启llm-proxy
```

---

## 手动操作

进入 skill 目录后执行：

### 启动

```bash
./scripts/llm-proxy-ctl.sh start
```

### 停止

```bash
./scripts/llm-proxy-ctl.sh stop
```

### 状态

```bash
./scripts/llm-proxy-ctl.sh status
```

### 重启

```bash
./scripts/llm-proxy-ctl.sh restart
```

---

## 配置说明

配置文件：`scripts/llm-proxy-config.json`

### 基本配置

| 字段 | 默认值 | 说明 |
|------|--------|------|
| `listen_host` | `127.0.0.1` | 监听地址 |
| `proxy_port` | `18888` | 代理端口 |
| `read_timeout` | `60` | 读取超时（秒） |
| `max_body_size_mb` | `10` | 最大请求体（MB） |
| `max_threads` | `50` | 最大线程数 |

### 安全检测配置

| 配置项 | 说明 |
|--------|------|
| `rules_file` | 内容过滤规则文件 |
| `quick_check_keywords` | 快速检测关键词列表 |

### 修改端口

编辑 `llm-proxy-config.json` 中的 `proxy_port` 字段，重启服务生效。

---

## 支持的 Provider

### 免费/免费额度

- `ollama` - 本地 Ollama
- `gemini` - Google Gemini
- `groq` - Groq
- `cloudflare` - Workers AI
- `deepseek` - DeepSeek
- `moonshot` - 月之暗面
- `zhipu` - 智谱
- `siliconflow` - SiliconFlow

### 付费

- `openai` - OpenAI
- `anthropic` - Anthropic
- `openrouter` - OpenRouter
- `nvd` - NVIDIA NIM
- `bailian` - 阿里百炼
- `baidu` - 百度文心
- `spark` - 讯飞星火
- `minimax` - MiniMax
- `yi` - 零一万物
- `baichuan` - 百川
- `together` - Together AI
- `fireworks` - Fireworks AI
- `replicate` - Replicate

---

## 健康检查

```bash
curl http://127.0.0.1:18888/health
```

响应示例：

```json
{
  "status": "ok",
  "uptime": 3600,
  "rules_loaded": {
    "layer1": 10,
    "layer2": 7,
    "whitelist": 6
  },
  "stats": {
    "total_requests": 100,
    "total_responses": 98,
    "blocked": 0,
    "errors": 2
  }
}
```

---

## 安全检测机制

### 三层审核

1. **L1 - 恶意指令检测**：危险命令、提权操作、SQL注入、后门等
2. **L2 - 敏感内容检测**：个人身份信息、凭证密钥、违法内容
3. **快速关键词检测**：流式响应实时检测风险关键词

### 流式响应检测

- 每 100 字符检测一次
- 发现风险关键词时注入警告提醒
- 严重违规时阻断响应

### 自定义关键词

编辑 `llm-proxy-config.json` 中的 `quick_check_keywords` 数组添加新关键词。

---

## 日志

日志目录：`~/.openclaw/logs/llm-proxy/`

- `proxy-YYYY-MM-DD.jsonl` - 请求日志
- `ctl-service.log` - 服务日志（手动启动时）

---

## 注意事项

- 默认端口 `18888`
- 仅监听本地 `127.0.0.1`
- 无自动监控，需手动管理
- 修改配置后需重启服务
