# Multi-Provider Agent Model Assignment System

> **💼 Developer Note**: This SKILL was developed entirely by **Leo, the OpenClaw AI Assistant**

**Version**: 1.0.0  
**Created**: 2026-03-04  
**Developer**: Leo (OpenClaw AI)  
**Development**: AI autonomous development, testing, and documentation

---

## 🎯 Overview

The Multi-Provider Agent Model Assignment System is a powerful LLM management tool supporting:

- **Multi-Cloud Providers** - Alibaba Cloud, OpenAI, Anthropic, Zhipu AI, Baidu, etc.
- **Local Deployments** - Ollama, LM Studio, vLLM local model services
- **Auto-Discovery** - Automatically scan and discover local model services
- **Zero-Code Configuration** - Pure YAML config, no code changes needed
- **Smart Routing** - Auto-select optimal model based on task type
- **Cost Optimization** - Auto-select most cost-effective model combination

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install pyyaml requests
```

### 2. List Available Models

```bash
python skills/multi-provider-agents/scripts/provider_manager.py list-models
```

### 3. Scan Local Models

```bash
python skills/multi-provider-agents/scripts/provider_manager.py scan
```

### 4. Configure Providers

Edit `skills/multi-provider-agents/config/models.yaml` to add provider configurations.

---

## 📋 Features

### Multi-Provider Support

Support unlimited cloud providers, just add to config:

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

### Local Model Support

Support multiple local model services:

#### Ollama

```yaml
ollama:
  name: Ollama (Local)
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
  name: LM Studio (Local)
  type: openai-compatible
  enabled: true
  base_url: http://localhost:1234/v1
  models:
    - id: lmstudio/local-model
      name: Local Model
      local: true
```

#### vLLM

```yaml
vllm:
  name: vLLM (Local)
  type: openai-compatible
  enabled: true
  base_url: http://localhost:8000/v1
  models:
    - id: vllm/mistral-7b
      name: Mistral 7B
      local: true
```

### Auto-Discovery

System automatically scans local model services:

```yaml
local_discovery:
  enabled: true
  scan_interval: 300  # Scan interval (seconds)
  endpoints:
    - name: Ollama
      url: http://localhost:11434/api/tags
      type: ollama
    - name: LM Studio
      url: http://localhost:1234/v1/models
      type: openai-compatible
```

### Smart Routing

Auto-select optimal model by task type:

```yaml
routing:
  task_routing:
    coding: bailian/qwen3-coder-plus    # Coding tasks
    reasoning: bailian/qwen3-max        # Reasoning tasks
    long_text: bailian/kimi-k2.5        # Long text
    agent: bailian/glm-5                # Agent orchestration
    daily: bailian/qwen3.5-plus         # Daily tasks
```

### Agent Model Assignment

Configure dedicated models for each agent:

```yaml
agents:
  Agent_Coordinator:  # ⚠️ Replace with your agent name
    models:
      primary: bailian/glm-5
      fallback: bailian/qwen3.5-plus
    preferences:
      cost_optimize: false
      latency_optimize: true
      
  Agent_Frontend_Dev:  # ⚠️ Replace with your agent name
    models:
      primary: bailian/qwen3-coder-plus
      fallback: ollama/codellama
    preferences:
      code_quality: true
```

---

## 🔧 Management Commands

### List All Providers

```bash
python skills/multi-provider-agents/scripts/provider_manager.py list-providers
```

### List All Models

```bash
python skills/multi-provider-agents/scripts/provider_manager.py list-models
```

### Scan Local Models

```bash
python skills/multi-provider-agents/scripts/provider_manager.py scan
```

### Add New Provider

```bash
python skills/multi-provider-agents/scripts/provider_manager.py add <provider-name>
```

### Enable/Disable Provider

```bash
# Enable
python skills/multi-provider-agents/scripts/provider_manager.py enable <provider-name>

# Disable
python skills/multi-provider-agents/scripts/provider_manager.py disable <provider-name>
```

---

## 📁 Directory Structure

```
skills/multi-provider-agents/
├── SKILL.md                 # Skill description
├── scripts/
│   ├── provider_manager.py  # Provider manager
│   └── model_router_v2.py   # Model router
├── config/
│   └── models.yaml          # Model configuration
├── docs/
│   ├── README_zh.md         # Chinese documentation
│   └── README_en.md         # English documentation
└── examples/
    ├── add_openai.yaml      # OpenAI config example
    ├── configure_ollama.yaml # Ollama config example
    └── agent_assignment.yaml # Agent assignment example
```

---

## 💡 Use Cases

### Use Case 1: Add OpenAI

1. Edit `config/models.yaml`
2. Uncomment OpenAI configuration block
3. Fill in API Key
4. Run `python scripts/provider_manager.py list-models` to verify

### Use Case 2: Configure Local Ollama

1. Install Ollama: `https://ollama.ai`
2. Pull model: `ollama pull llama3`
3. Edit config to add Ollama block
4. Run `python scripts/provider_manager.py scan` to scan

### Use Case 3: Agent Uses Local Model

Edit `agents` section in `config/models.yaml`:

```yaml
agents:
  Agent_Frontend_Dev:  # ⚠️ Replace with your agent name
    models:
      primary: bailian/qwen3-coder-plus  # Cloud
      fallback: ollama/codellama        # Local fallback
    preferences:
      local_first: true  # Prefer local
```

---

## 📊 Cost Optimization

System supports cost tracking and optimization:

```yaml
cost_tracking:
  enabled: true
  currency: CNY
  budget_monthly: 100.0      # Monthly budget
  alert_threshold: 0.8       # Alert threshold (80%)

routing:
  cost_optimize: true        # Enable cost optimization
```

---

## 🔒 Security Recommendations

1. **Don't commit API Keys to Git**
   ```bash
   # Use environment variables
   api_key_env: OPENAI_API_KEY
   
   # Or add to .gitignore
   echo "config/models.yaml" >> .gitignore
   ```

2. **Rotate API Keys Regularly**
   ```bash
   python scripts/provider_manager.py rotate-key <provider>
   ```

3. **Use Local Models to Reduce Costs**
   ```yaml
   routing:
     local_first: true
   ```

---

## 🤝 Contributing

Issues and Pull Requests are welcome!

---

## 📄 License

MIT License

---

**Last Updated**: 2026-03-04  
**Version**: 3.0.0
