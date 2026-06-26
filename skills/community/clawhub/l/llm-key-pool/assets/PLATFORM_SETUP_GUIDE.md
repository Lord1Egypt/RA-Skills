# 平台集成安装指南

## 目录
- [小龙虾（XiaoLongXia）](#小龙虾xiaolongxia)
- [OpenCode](#opencode)
- [Qwen独立API](#qwen独立api)
- [ClaudeCode](#claudecode)

---

## 小龙虾（XiaoLongXia）

### 1. 获取API Key

**步骤：**
1. 访问小龙虾官网
2. 注册账号并登录
3. 进入控制台或API管理页面
4. 创建新的API Key
5. 复制生成的API Key

**API Key格式示例：**
```
xiaolongxia_sk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 2. 配置Skill

在 `llm_config.yaml` 中添加以下配置：

```yaml
providers:
  xiaolongxia:
    tier: primary  # 或 daily/fallback
    model: "xiaolongxia-72b"  # 或 xiaolongxia-34b, xiaolongxia-14b
    api_keys:
      - "xiaolongxia_sk_你的真实API-Key-1"
      - "xiaolongxia_sk_你的真实API-Key-2"  # 可选，配置多个Key实现负载均衡
    base_url: "https://api.xiaolongxia.com/v1"
```

### 3. 测试连接

```bash
python -m llm_key_pool.llm_client \
  --config ./llm_config.yaml \
  --prompt "你好，请介绍一下小龙虾模型的特点" \
  --temperature 0.7
```

### 4. 验证配置

```bash
# 查看Key池状态
python -m llm_key_pool.llm_client \
  --config ./llm_config.yaml \
  --status
```

### 5. 支持的模型

| 模型名称 | 参数量 | 适用场景 |
|---------|--------|---------|
| xiaolongxia-72b | 72B | 复杂推理、长文本 |
| xiaolongxia-34b | 34B | 平衡性能与速度 |
| xiaolongxia-14b | 14B | 快速响应、简单任务 |

---

## OpenCode

### 1. 获取API Key

**步骤：**
1. 访问OpenCode官网
2. 注册开发者账号
3. 进入API密钥管理页面
4. 生成新的API Key
5. 保存API Key（仅显示一次）

**API Key格式示例：**
```
opencode_sk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 2. 配置Skill

在 `llm_config.yaml` 中添加以下配置：

```yaml
providers:
  opencode:
    tier: fallback  # 或 primary/daily
    model: "opencode-72b"  # 或 opencode-34b, opencode-14b
    api_keys:
      - "opencode_sk_你的真实API-Key"
    base_url: "https://api.opencode.com/v1"
```

### 3. 测试代码生成能力

```bash
python -m llm_key_pool.llm_client \
  --config ./llm_config.yaml \
  --prompt "用Python写一个快速排序算法" \
  --system-prompt "你是一个专业的代码助手，请提供完整的、可直接运行的代码" \
  --temperature 0.3  # 代码生成建议使用较低的温度
```

### 4. 代码审查示例

```bash
python -m llm_key_pool.llm_client \
  --config ./llm_config.yaml \
  --prompt "请审查以下代码并提出优化建议：
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)" \
  --system-prompt "你是一个代码审查专家，请指出代码的问题并提供优化方案" \
  --max-tokens 500
```

### 5. 支持的模型

| 模型名称 | 参数量 | 代码能力 |
|---------|--------|---------|
| opencode-72b | 72B | 复杂架构设计、大型项目重构 |
| opencode-34b | 34B | 模块开发、功能实现 |
| opencode-14b | 14B | 快速补全、Bug修复 |

---

## Qwen独立API

### 1. 获取API Key

**步骤：**
1. 访问通义千问官网（[https://qwen.ai](https://qwen.ai)）
2. 注册/登录阿里云账号
3. 进入API密钥管理
4. 创建AccessKey
5. 复制生成的AccessKey

**API Key格式示例：**
```
sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**注意：** 这与阿里云百炼的API Key不同，是独立的服务。

### 2. 配置Skill

在 `llm_config.yaml` 中添加以下配置：

```yaml
providers:
  qwen:
    tier: fallback  # 或 primary/daily
    model: "qwen-max"  # 或 qwen-plus, qwen-turbo, qwen-long
    api_keys:
      - "sk-你的真实API-Key"
    base_url: "https://api.qwen.ai/v1"
```

### 3. 测试长文本能力（qwen-long）

```yaml
qwen:
  tier: fallback
  model: "qwen-long"  # 长文本模型
  api_keys: ["sk-你的API-Key"]
  base_url: "https://api.qwen.ai/v1"
```

```bash
python -m llm_key_pool.llm_client \
  --config ./llm_config.yaml \
  --prompt "请总结以下长篇文章的核心观点..." \
  --max-tokens 10000  # 支持更长的输出
```

### 4. 支持的模型

| 模型名称 | 特点 | 适用场景 |
|---------|------|---------|
| qwen-max | 最强性能 | 复杂推理、创意写作 |
| qwen-plus | 性能平衡 | 日常对话、知识问答 |
| qwen-turbo | 快速响应 | 实时交互、简单任务 |
| qwen-long | 长文本 | 文档处理、长对话 |

### 5. 对比阿里云百炼

| 特性 | 阿里云百炼 | Qwen独立API |
|------|-----------|-------------|
| API端点 | dashscope.aliyuncs.com | api.qwen.ai |
| 功能 | 全套百炼功能 | 纯模型API |
| 价格 | 可能更低 | 可能更高 |
| 适用 | 企业用户 | 开发者 |

---

## ClaudeCode

### 1. 获取API Key

**步骤：**
1. 访问Anthropic控制台（[https://console.anthropic.com](https://console.anthropic.com)）
2. 登录账号（如果没有则注册）
3. 进入API Keys页面
4. 点击"Create Key"
5. 选择用途（可选）
6. 复制生成的API Key（仅显示一次！）

**API Key格式示例：**
```
sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**重要提示：**
- API Key只显示一次，请妥善保存
- 如果丢失，需要删除并重新创建
- 建议设置使用限额和日期范围

### 2. 配置Skill

在 `llm_config.yaml` 中添加以下配置：

```yaml
providers:
  claudecode:
    tier: fallback  # 或 primary/daily
    model: "claude-3-5-sonnet-20241022"  # 推荐版本
    api_keys:
      - "sk-ant-api03-你的真实API-Key"
    base_url: "https://api.anthropic.com/v1"
```

### 3. 测试代码能力

```bash
python -m llm_key_pool.llm_client \
  --config ./llm_config.yaml \
  --prompt "用JavaScript实现一个React组件，实现一个待办事项列表" \
  --system-prompt "你是一个React专家，请提供完整的代码和说明" \
  --temperature 0.5
```

### 4. 代码调试示例

```bash
python -m llm_key_pool.llm_client \
  --config ./llm_config.yaml \
  --prompt "帮我找出以下代码中的bug：
async function fetchData() {
  const response = await fetch('https://api.example.com/data');
  const data = await response.json();
  console.log(data.items.map(item => item.name));
}

fetchData();" \
  --system-prompt "你是一个调试专家，请分析代码问题并提供修复方案"
```

### 5. 支持的模型

| 模型名称 | 发布日期 | 特点 |
|---------|---------|------|
| claude-3-5-sonnet-20241022 | 2024年10月 | 最新最强，推荐使用 |
| claude-3-opus-20240229 | 2024年2月 | 高质量，但较慢 |
| claude-3-sonnet-20240229 | 2024年2月 | 平衡性能与速度 |

### 6. 特殊注意事项

**ClaudeCode与其他平台的不同：**
- 使用 `x-api-key` 请求头而非 `Authorization: Bearer`
- 使用 `/messages` 端点而非 `/chat/completions`
- 响应格式为 `content[0].text`
- 需要添加 `anthropic-version: 2023-06-01` 请求头

**这些差异已由Skill自动处理，您只需按标准格式配置即可。**

### 7. 价格提示

ClaudeCode是付费服务，价格相对较高，建议：
- 作为兜底层使用（fallback）
- 仅在代码相关任务中使用
- 监控使用量避免超支

---

## 完整配置示例（包含所有4个平台）

```yaml
providers:
  # 主力层
  xiaolongxia:
    tier: primary
    model: "xiaolongxia-72b"
    api_keys:
      - "xiaolongxia_sk_你的Key-1"
      - "xiaolongxia_sk_你的Key-2"
    base_url: "https://api.xiaolongxia.com/v1"

  # 兜底层
  opencode:
    tier: fallback
    model: "opencode-72b"
    api_keys:
      - "opencode_sk_你的Key"
    base_url: "https://api.opencode.com/v1"

  qwen:
    tier: fallback
    model: "qwen-max"
    api_keys:
      - "sk-你的Key"
    base_url: "https://api.qwen.ai/v1"

  claudecode:
    tier: fallback
    model: "claude-3-5-sonnet-20241022"
    api_keys:
      - "sk-ant-api03-你的Key"
    base_url: "https://api.anthropic.com/v1"

global:
  max_retries: 3
  retry_delay: 1
  error_threshold: 5
  cooldown_seconds: 300
  quota_check_enabled: true
```

---

## 验证安装

### 1. 测试所有平台

```bash
# 测试小龙虾
python -m llm_key_pool.llm_client \
  --config ./llm_config.yaml \
  --prompt "测试小龙虾" \
  --max-tokens 50

# 测试OpenCode
python -m llm_key_pool.llm_client \
  --config ./llm_config.yaml \
  --prompt "print('hello')" \
  --max-tokens 50

# 测试Qwen
python -m llm_key_pool.llm_client \
  --config ./llm_config.yaml \
  --prompt "测试Qwen" \
  --max-tokens 50

# 测试ClaudeCode
python -m llm_key_pool.llm_client \
  --config ./llm_config.yaml \
  --prompt "print('hello')" \
  --max-tokens 50
```

### 2. 查看状态

```bash
python -m llm_key_pool.llm_client \
  --config ./llm_config.yaml \
  --status
```

### 3. 完整测试

```bash
python -m llm_key_pool.llm_client \
  --config ./llm_config.yaml \
  --test
```

---

## 常见问题

### Q1: API Key在哪里获取？

**A:** 每个平台的获取方式不同：
- 小龙虾：访问小龙虾官网控制台
- OpenCode：访问OpenCode官网API管理页面
- Qwen：访问通义千问官网
- ClaudeCode：访问Anthropic控制台

### Q2: 配置后无法调用？

**A:** 检查以下几点：
1. API Key是否正确复制（无多余空格）
2. base_url是否正确
3. 模型名称是否正确
4. 账户是否有足够额度
5. 网络连接是否正常

### Q3: 如何选择合适的层级？

**A:**
- primary：主力层，高额度，优先使用
- daily：每日回血层，额度刷新
- fallback：兜底层，开源/聚合，最后保障

### Q4: ClaudeCode为什么特殊？

**A:** ClaudeCode使用Anthropic的Messages API，与OpenAI兼容格式略有不同，但Skill已自动处理这些差异。

### Q5: 可以同时使用多个平台的多个Key吗？

**A:** 可以！在 `api_keys` 数组中添加多个Key即可实现负载均衡。

---

## 下一步

1. ✅ 注册各平台账号
2. ✅ 获取API Key
3. ✅ 配置 `llm_config.yaml`
4. ✅ 测试连接
5. ✅ 开始使用

需要帮助？查看详细文档：
- `references/supported_providers.md`
- `references/config_format.md`
- `SKILL.md`
