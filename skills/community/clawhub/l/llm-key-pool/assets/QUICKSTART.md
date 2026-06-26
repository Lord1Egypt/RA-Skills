# LLM Key Pool - 快速开始指南

## 5分钟快速上手

### 1. 获取API Key

您需要至少一个平台的API Key。推荐平台：

**免费/赠送额度大的平台：**
- 阿里云百炼：[https://bailian.console.aliyun.com/](https://bailian.console.aliyun.com/)
- 智谱AI：[https://open.bigmodel.cn/](https://open.bigmodel.cn/)
- 硅基流动：[https://siliconflow.cn/](https://siliconflow.cn/)

### 2. 创建配置文件

```bash
# 复制模板
cp assets/llm_config.yaml.example ./llm_config.yaml

# 编辑配置
vim ./llm_config.yaml
```

### 3. 最简配置（只需1个平台）

```yaml
providers:
  siliconflow:
    tier: fallback  # 兜底层
    model: "Qwen/Qwen2.5-7B-Instruct"
    api_keys:
      - "sk-你的真实API-Key"
    base_url: "https://api.siliconflow.cn/v1"

global:
  max_retries: 3
  cooldown_seconds: 300
```

### 4. 立即测试

```bash
python -m llm_key_pool.llm_client \
  --config ./llm_config.yaml \
  --prompt "你好，请介绍一下自己"
```

## 配置多个平台（推荐）

### 最小配置（3个平台）

```yaml
providers:
  # 主力层
  alibaba_bailian:
    tier: primary
    model: "qwen-max"
    api_keys: ["sk-你的API-Key"]
    base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"

  # 每日回血层
  volcengine:
    tier: daily
    model: "doubao-pro-256k"
    api_keys: ["你的API-Key"]
    base_url: "https://ark.cn-beijing.volces.com/api/v3"

  # 兜底层
  siliconflow:
    tier: fallback
    model: "Qwen/Qwen2.5-7B-Instruct"
    api_keys: ["sk-你的API-Key"]
    base_url: "https://api.siliconflow.cn/v1"
```

## 常用命令

### 查看帮助
```bash
python -m llm_key_pool.llm_client --help
```

### 查看Key池状态
```bash
python -m llm_key_pool.llm_client \
  --config ./llm_config.yaml \
  --status
```

### 测试配置
```bash
python -m llm_key_pool.llm_client \
  --config ./llm_config.yaml \
  --test
```

## 在Python代码中使用

```python
from llm_key_pool import TieredLLMClient

# 初始化
client = TieredLLMClient('./llm_config.yaml')

# 调用
result, usage_info = client.call_llm(
    prompt="你好",
    temperature=0.7,
    max_tokens=100
)

print(result)
```

## 分层轮询说明

1. **主力层（primary）**：优先使用，额度大
2. **每日回血层（daily）**：主力层不可用时切换
3. **兜底层（fallback）**：最后保障

系统会自动在层级间切换，无需手动干预。

## 故障转移

- **429错误**：立即冷却Key，切换下一个
- **401错误**：永久禁用无效Key
- **500错误**：短暂重试

## 注意事项

1. API Key敏感，不要提交到版本控制
2. 配置文件名为 `llm_config.yaml`
3. 确保网络连接正常
4. 查看日志了解调用详情

## 获取帮助

详细文档：
- 配置格式：`references/config_format.md`
- 支持平台：`references/supported_providers.md`
- 使用说明：`SKILL.md`
