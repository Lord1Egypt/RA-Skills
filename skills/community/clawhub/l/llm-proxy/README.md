# LLM Proxy Skill

LLM API 代理服务，统一管理多个 LLM Provider，支持内容安全审计。

---

## 安装

### 方式一：直接使用

Skill 已安装在 `~/.agents/skills/llm-proxy/`，可直接使用。

### 方式二：复制到其他位置

```bash
cp -r ~/.agents/skills/llm-proxy /目标路径/
```

---

## 配置

### 配置文件位置

```
scripts/llm-proxy-config.json
```

### 基本配置

| 字段 | 默认值 | 说明 |
|------|--------|------|
| `listen_host` | `127.0.0.1` | 监听地址 |
| `proxy_port` | `18888` | 代理端口 |
| `read_timeout` | `60` | 读取超时（秒） |
| `max_body_size_mb` | `10` | 最大请求体（MB） |
| `max_threads` | `50` | 最大线程数 |

### 安全检测配置

| 字段 | 说明 |
|------|------|
| `rules_file` | 内容过滤规则文件 |
| `quick_check_keywords` | 快速检测关键词列表 |

### 修改端口

编辑 `llm-proxy-config.json`：

```json
{
  "proxy_port": 18888
}
```

修改后重启服务生效。

---

## 使用方法

### 启动代理

```
启动llm-proxy
```

或手动执行：

```bash
cd ~/.agents/skills/llm-proxy
./scripts/llm-proxy-ctl.sh start
```

### 停止代理

```
停止llm-proxy
```

或手动执行：

```bash
./scripts/llm-proxy-ctl.sh stop
```

### 查看状态

```
llm-proxy状态
```

或手动执行：

```bash
./scripts/llm-proxy-ctl.sh status
```

### 重启代理

```
重启llm-proxy
```

或手动执行：

```bash
./scripts/llm-proxy-ctl.sh restart
```

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

## 添加新 Provider

编辑 `scripts/llm-proxy-config.json`，在 `providers` 节点添加：

```json
"/your-provider": {
  "url": "https://api.your-provider.com/v1",
  "name": "Your Provider",
  "description": "描述信息",
  "pricing": "paid"
}
```

**路由规则：**
- 前缀 `/your-provider` 会路由到对应的 `url`
- 例如：`POST http://127.0.0.1:18888/your-provider/chat/completions`
- 会转发到：`https://api.your-provider.com/v1/chat/completions`

---

## 安全检测机制

### 三层审核

1. **L1 - 恶意指令检测**：危险命令、提权操作、SQL注入、后门等
2. **L2 - 敏感内容检测**：个人身份信息、凭证密钥、违法内容
3. **快速关键词检测**：流式响应实时检测风险关键词

### 流式响应检测

- 每 100 字符检测一次
- 发现风险关键词时注入警告提醒
- 严重违规时阻断响应并返回错误

### 自定义关键词

编辑 `scripts/llm-proxy-config.json`：

```json
{
  "quick_check_keywords": [
    "关闭防火墙",
    "禁用防火墙",
    "socketfilterfw",
    "你的自定义关键词"
  ]
}
```

---

## 日志

### 日志目录

```
~/.openclaw/logs/llm-proxy/
```

### 日志文件

| 文件 | 说明 |
|------|------|
| `proxy-YYYY-MM-DD.jsonl` | 请求日志（JSON Lines 格式） |
| `ctl-service.log` | 服务日志（手动启动时） |

### 查看日志

```bash
# 查看今天的请求日志
cat ~/.openclaw/logs/llm-proxy/proxy-$(date +%Y-%m-%d).jsonl

# 实时查看服务日志
tail -f ~/.openclaw/logs/llm-proxy/ctl-service.log
```

---

## 支持的 Provider

### 免费/免费额度

| 前缀 | Provider | 说明 |
|------|----------|------|
| `/ollama` | Ollama | 本地部署，完全免费 |
| `/gemini` | Google Gemini | 60次/分钟，1500次/天 |
| `/groq` | Groq | 免费快速推理 |
| `/cloudflare` | Workers AI | 10万次/天 |
| `/deepseek` | DeepSeek | 新用户免费额度 |
| `/moonshot` | 月之暗面 | 新用户免费额度 |
| `/zhipu` | 智谱 | 新用户免费额度 |
| `/siliconflow` | SiliconFlow | 免费额度 |

### 付费

| 前缀 | Provider | 说明 |
|------|----------|------|
| `/openai` | OpenAI | GPT-4, GPT-3.5 |
| `/anthropic` | Anthropic | Claude 系列 |
| `/openrouter` | OpenRouter | 多模型聚合 |
| `/nvd` | NVIDIA NIM | 企业级 GPU |
| `/bailian` | 阿里百炼 | 通义千问 |
| `/baidu` | 百度文心 | 文心一言 |
| `/spark` | 讯飞星火 | 讯飞大模型 |
| `/minimax` | MiniMax | 海螺AI |
| `/yi` | 零一万物 | Yi 系列 |
| `/baichuan` | 百川 | Baichuan |
| `/together` | Together AI | 开源模型托管 |
| `/fireworks` | Fireworks AI | 快速推理 |
| `/replicate` | Replicate | 按次计费 |

---

## 请求示例

### OpenAI 兼容格式

```bash
curl http://127.0.0.1:18888/openai/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Hello"}],
    "stream": true
  }'
```

### 阿里百炼

```bash
curl http://127.0.0.1:18888/bailian/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -d '{
    "model": "qwen-turbo",
    "messages": [{"role": "user", "content": "你好"}]
  }'
```

---

## 故障排查

### 端口被占用

```bash
# 查看占用进程
lsof -i :18888

# 终止进程
kill -9 <PID>

# 或使用脚本清理
./scripts/llm-proxy-ctl.sh stop
```

### 代理无响应

1. 检查服务状态：
   ```bash
   ./scripts/llm-proxy-ctl.sh status
   ```

2. 查看日志：
   ```bash
   tail -50 ~/.openclaw/logs/llm-proxy/ctl-service.log
   ```

3. 重启服务：
   ```bash
   ./scripts/llm-proxy-ctl.sh restart
   ```

### 配置不生效

修改配置后必须重启服务：

```bash
./scripts/llm-proxy-ctl.sh restart
```

---

## 注意事项

- 默认端口 `18888`
- 仅监听本地 `127.0.0.1`（不暴露到外网）
- 无自动监控，需手动管理
- 修改配置后需重启服务
- 内容安全检测仅记录和提醒，不自动拦截（可配置）

---

## 文件清单

```
llm-proxy/
├── SKILL.md              # Skill 说明（Agent 读取）
├── README.md             # 本文件（安装配置说明）
└── scripts/
    ├── llm-proxy-config.json    # 配置文件
    ├── llm-proxy.py             # 主程序
    ├── llm-proxy-ctl.sh         # 控制脚本
    ├── llm-proxy-common.sh      # 公共函数
    └── content-filter-rules.json # 内容过滤规则
```
