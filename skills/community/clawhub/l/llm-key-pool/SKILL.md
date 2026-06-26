---
name: llm-key-pool
description: 多平台API Key分层轮询与智能故障转移；当用户需要绕过单一API Key速率限制、实现高可用大模型调用或管理多厂商API密钥池时使用
dependency:
  python:
    - pyyaml>=6.0.0
    - requests>=2.28.0
---

# LLM Key Pool - 分层轮询多平台API Key管理

## 任务目标
- 本Skill用于：多平台API Key智能管理，实现分层轮询、跨层切换和自动故障转移
- 能力包含：分层配置管理、自动轮询、跨层切换、429错误智能处理、统一OpenAI兼容接口
- 触发条件：当Agent需要稳定调用大模型API且面临速率限制或单点故障风险时

## 前置准备

### 依赖安装
SKILL依赖以下Python包：
```
pyyaml>=6.0.0
```

### 配置文件准备
在使用前需要创建配置文件 `llm_config.yaml`，支持分层配置：
- **主力层（primary）**：高额度平台（阿里云百炼、智谱AI）
- **每日回血层（daily）**：每日刷新平台（火山引擎、Google AI Studio）
- **兜底层（fallback）**：开源/聚合平台（硅基流动、OpenRouter等）

配置文件格式见 [references/config_format.md](references/config_format.md)

支持的AI平台及配置方法见 [references/supported_providers.md](references/supported_providers.md)

## 操作步骤

### 标准流程

1. **准备配置文件**
   - 在当前目录创建 `llm_config.yaml`
   - 按分层策略配置各平台的API Key
   - 优先配置主力层，然后是每日回血层，最后是兜底层

2. **调用LLM服务**
   - 执行脚本：`python -m llm_key_pool.llm_client`
   - 参数说明：
     - `--config`: 配置文件路径（默认：./llm_config.yaml）
     - `--prompt`: 用户提示词
     - `--system-prompt`: 系统提示词（可选）
     - `--temperature`: 温度参数（可选，默认：0.7）
     - `--max-tokens`: 最大Token数（可选，默认：2000）

3. **自动分层轮询**
   - 优先使用主力层API Key
   - 主力层所有Key不可用时，自动切换到每日回血层
   - 每日回血层也不可用时，切换到兜底层
   - 跨层切换对上层应用透明

4. **智能故障转移**
   - 监听429 Too Many Requests错误
   - 立即标记当前Key为冷却中
   - 无缝切换到下一个Key或下一层
   - 冷却结束后自动恢复

### 可选分支

- **当需要测试配置是否正确**：使用 `--test` 参数进行配置验证
- **当需要查看Key池状态**：使用 `--status` 参数查看各层级Key的使用情况

## 资源索引

### 核心脚本
- [llm_key_pool/config_loader.py](llm_key_pool/config_loader.py) - 配置文件加载和验证
- [llm_key_pool/key_pool.py](llm_key_pool/key_pool.py) - 分层API Key池管理和轮询逻辑
- [llm_key_pool/llm_client.py](llm_key_pool/llm_client.py) - 统一LLM调用接口（OpenAI兼容）

### 参考文档
- [references/config_format.md](references/config_format.md) - 配置文件格式说明（分层版）
- [references/supported_providers.md](references/supported_providers.md) - 支持的AI平台列表

## 注意事项

- API Key信息敏感，请勿将配置文件提交到版本控制系统
- 建议按分层策略配置至少3个平台（主力层、每日回血层、兜底层各1个）
- 429错误会触发立即冷却，冷却时间可通过配置调整
- 故障转移和跨层切换对上层应用透明，但会略微增加延迟
- 优先选择支持OpenAI兼容接口的平台，简化配置

## 使用示例

### 示例1：基本调用
```bash
python -m llm_key_pool.llm_client \
  --config ./llm_config.yaml \
  --prompt "解释什么是量子计算" \
  --temperature 0.7 \
  --max-tokens 500
```

### 示例2：带系统提示词
```bash
python -m llm_key_pool.llm_client \
  --config ./llm_config.yaml \
  --prompt "写一个关于AI的短故事" \
  --system-prompt "你是一个创意写作专家"
```

### 示例3：查看Key池状态
```bash
python -m llm_key_pool.llm_client \
  --config ./llm_config.yaml \
  --status
```

### 示例4：验证配置
```bash
python -m llm_key_pool.llm_client \
  --config ./llm_config.yaml \
  --test
```

## 分层轮询策略

### 主力层（primary）
- **特点**：初始赠送额度极大
- **推荐平台**：阿里云百炼、智谱AI
- **用途**：处理大部分日常任务

### 每日回血层（daily）
- **特点**：额度每日刷新
- **推荐平台**：火山引擎、Google AI Studio
- **用途**：主力层耗尽后保证基本可用性

### 兜底层（fallback）
- **特点**：开源模型/聚合平台
- **推荐平台**：硅基流动、OpenRouter、GitHub Models、Groq
- **用途**：大厂API都限流时保证服务不中断
