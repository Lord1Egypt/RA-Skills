# 多模型提供商智能体分配系统

> **💼 开发说明**: 本 SKILL 由 **OpenClaw 的 AI 助手 Leo** 全程独立开发  
> **Developer**: This SKILL was developed entirely by **Leo, the OpenClaw AI Assistant**

**版本**: 1.0.0  
**创建日期**: 2026-03-04  
**开发者**: Leo (OpenClaw AI)  
**开发方式**: AI 自主开发、自主测试、自主文档化

---

## 🎯 简介

多模型提供商智能体分配系统是一个强大的大模型管理工具，支持：

- **多云厂商** - 阿里云百炼、OpenAI、Anthropic、智谱 AI、百度等
- **本地部署** - Ollama、LM Studio、vLLM 等本地模型服务
- **自动发现** - 自动扫描并发现本地运行的模型服务
- **零代码配置** - 纯 YAML 配置，无需修改任何代码
- **智能路由** - 根据任务类型自动选择最优模型
- **成本优化** - 自动选择最具性价比的模型组合

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install pyyaml requests
```

### 2. 查看可用模型

```bash
python skills/multi-provider-agents/scripts/provider_manager.py list-models
```

### 3. 扫描本地模型

```bash
python skills/multi-provider-agents/scripts/provider_manager.py scan
```

### 4. 配置厂商

编辑 `skills/multi-provider-agents/config/models.yaml` 添加厂商配置。

---

## 📋 功能特性

### 多厂商支持

支持任意数量的云厂商，只需在配置文件中添加：

```yaml
providers:
  openai:
    name: OpenAI
    type: openai-compatible
    enabled: true
    base_url: https://api.openai.com/v1
    api_key: sk-xxx
    models:
      - id: openai/gpt-4
        name: GPT-4
        context_window: 128000
```

### 本地模型支持

支持多种本地模型服务：

#### Ollama

```yaml
ollama:
  name: Ollama (本地)
  type: openai-compatible
  enabled: true
  base_url: http://localhost:11434/v1
  models:
    - id: ollama/llama3
      name: Llama 3
      local: true
```

#### LM Studio

```yaml
lmstudio:
  name: LM Studio (本地)
  type: openai-compatible
  enabled: true
  base_url: http://localhost:1234/v1
  models:
    - id: lmstudio/local-model
      name: 本地模型
      local: true
```

#### vLLM

```yaml
vllm:
  name: vLLM (本地)
  type: openai-compatible
  enabled: true
  base_url: http://localhost:8000/v1
  models:
    - id: vllm/mistral-7b
      name: Mistral 7B
      local: true
```

### 自动发现

系统会自动扫描本地运行的模型服务：

```yaml
local_discovery:
  enabled: true
  scan_interval: 300  # 扫描间隔（秒）
  endpoints:
    - name: Ollama
      url: http://localhost:11434/api/tags
      type: ollama
    - name: LM Studio
      url: http://localhost:1234/v1/models
      type: openai-compatible
```

### 智能路由

根据任务类型自动选择最优模型：

```yaml
routing:
  task_routing:
    coding: bailian/qwen3-coder-plus    # 编码任务
    reasoning: bailian/qwen3-max        # 推理任务
    long_text: bailian/kimi-k2.5        # 长文本
    agent: bailian/glm-5                # Agent 编排
    daily: bailian/qwen3.5-plus         # 日常任务
```

### 智能体模型分配

为每个智能体配置专属模型：

```yaml
agents:
  Agent_Coordinator:  # ⚠️ 请替换为您的智能体名称
    models:
      primary: bailian/glm-5
      fallback: bailian/qwen3.5-plus
    preferences:
      cost_optimize: false
      latency_optimize: true
      
  Agent_Frontend_Dev:  # ⚠️ 请替换为您的智能体名称
    models:
      primary: bailian/qwen3-coder-plus
      fallback: ollama/codellama
    preferences:
      code_quality: true
```
```

---

## 🔧 管理命令

### 列出所有厂商

```bash
python skills/multi-provider-agents/scripts/provider_manager.py list-providers
```

### 列出所有模型

```bash
python skills/multi-provider-agents/scripts/provider_manager.py list-models
```

### 扫描本地模型

```bash
python skills/multi-provider-agents/scripts/provider_manager.py scan
```

### 添加新厂商

```bash
python skills/multi-provider-agents/scripts/provider_manager.py add <厂商名称>
```

### 启用/禁用厂商

```bash
# 启用
python skills/multi-provider-agents/scripts/provider_manager.py enable <厂商名称>

# 禁用
python skills/multi-provider-agents/scripts/provider_manager.py disable <厂商名称>
```

---

## 📁 目录结构

```
skills/multi-provider-agents/
├── SKILL.md                 # 技能说明
├── scripts/
│   ├── provider_manager.py  # 提供商管理器
│   └── model_router_v2.py   # 模型路由器
├── config/
│   └── models.yaml          # 模型配置
├── docs/
│   ├── README_zh.md         # 中文文档
│   └── README_en.md         # 英文文档
└── examples/
    ├── add_openai.yaml      # OpenAI 配置示例
    ├── configure_ollama.yaml # Ollama 配置示例
    └── agent_assignment.yaml # 智能体分配示例
```

---

## 💡 使用场景

### 场景 1: 添加 OpenAI

1. 编辑 `config/models.yaml`
2. 取消注释 OpenAI 配置块
3. 填写 API Key
4. 运行 `python scripts/provider_manager.py list-models` 验证

### 场景 2: 配置本地 Ollama

1. 安装 Ollama：`https://ollama.ai`
2. 拉取模型：`ollama pull llama3`
3. 编辑配置添加 Ollama 块
4. 运行 `python scripts/provider_manager.py scan` 扫描

### 场景 3: 智能体使用本地模型

编辑 `config/models.yaml` 中的 `agents` 部分：

```yaml
agents:
  Agent_Frontend_Dev:  # ⚠️ 请替换为您的智能体名称
    models:
      primary: bailian/qwen3-coder-plus  # 云端
      fallback: ollama/codellama        # 本地备用
    preferences:
      local_first: true  # 优先使用本地
```

---

## 📊 成本优化

系统支持成本跟踪和优化：

```yaml
cost_tracking:
  enabled: true
  currency: CNY
  budget_monthly: 100.0      # 月度预算
  alert_threshold: 0.8       # 预警阈值（80%）

routing:
  cost_optimize: true        # 启用成本优化
```

---

## 🔒 安全建议

1. **不要提交 API Key 到 Git**
   ```bash
   # 使用环境变量
   api_key_env: OPENAI_API_KEY
   
   # 或在 .gitignore 中添加
   echo "config/models.yaml" >> .gitignore
   ```

2. **定期轮换 API Key**
   ```bash
   python scripts/provider_manager.py rotate-key <provider>
   ```

3. **使用本地模型降低成本**
   ```yaml
   routing:
     local_first: true
   ```

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License

---

**最后更新**: 2026-03-04  
**版本**: 3.0.0
