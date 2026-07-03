# 模型吞吐率测试器

测试 LLM 模型的吞吐率（tokens/s）。支持两种模式：

- **Auto 模式**：通过 `openclaw infer model run` 测试当前模型，**无需 API Key**
- **API 模式**：直接调用 OpenAI 兼容 API，需要 URL 和 Key

## 触发规则

**适用场景：** 用户明确要求测试模型吞吐率时使用。

**推荐触发词：**
- 测一下吞吐率、测速、模型测速、tokens/s
- 跑个 benchmark、吞吐率测试、模型测试

**不适用：** 宽泛的性能讨论词（如「模型性能」「benchmark」单独出现）不应自动触发执行。

## 核心能力

### 1. Auto 模式（无 Key，推荐）

自动检测当前 session 的模型并测试吞吐率，无需任何配置。

```bash
python3 throughput.py --auto
```

指定模型测试：
```bash
python3 throughput.py --auto --model "zai/glm-5-turbo"
```

### 2. API 模式（直接调用 API）

```bash
python3 throughput.py \
  --url https://api.example.com/v1 \
  --key sk-xxx \
  --models gpt-4o-mini,gpt-4o
```

### 3. 通用参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--iterations` | `3` | 每个模型测试次数 |
| `--max-tokens` | `512` | 最大输出 token 数 |
| `--test-prompt` | 英文散文（夏天的田野） | 测试提示词 |
| `--timeout` | `60` | 单次请求超时（秒） |
| `--output` | `throughput-report.md` | 输出报告文件名 |
| `--csv` | false | 同时生成 CSV |

## 工作流程

### Auto 模式

```
1. 从 openclaw.json 读取当前 session 模型（provider/model）
2. 通过 openclaw infer model run 发送测试 prompt
3. 计时：命令开始 → 输出完成
4. 从返回文本估算 token 数（英文 0.75 word/token，中文 1.5 字/token）
5. 计算 tokens/s
6. 汇总输出报告
```

### API 模式

```
1. 构造 /v1/chat/completions 请求
2. 计时：请求开始 → 最后一个 token
3. 从响应中提取 usage.completion_tokens（精确）
4. 计算 tokens/s、错误率
5. 汇总输出报告
```

## 指标说明

| 指标 | 说明 |
|------|------|
| **Tokens/s** | 吞吐率 = Output Tokens / Elapsed Time |
| **Avg Latency** | 平均单次请求延迟 |
| **Avg Output Tokens** | 平均输出 token 数 |
| **Error Rate** | 错误请求占比 |

## 使用示例

### 安装后立即测试（Auto 模式）

```bash
# agent 触发时应传入当前模型
python3 ~/.openclaw/workspace/skills/model-throughput-tester/throughput.py --auto --model "<当前session模型>"

# 或使用自动检测（可能不是 session 覆盖的模型）
python3 ~/.openclaw/workspace/skills/model-throughput-tester/throughput.py --auto
```

### 测试多个模型（API 模式）

```bash
python3 throughput.py \
  --url "https://api.openai.com/v1" \
  --key "sk-xxx" \
  --models "gpt-4o-mini,gpt-4o" \
  --iterations 5
```

### 自定义提示词

```bash
python3 throughput.py --auto \
  --test-prompt "Explain quantum computing in detail." \
  --iterations 5
```

## 技术实现

- **Auto 模式**：`openclaw infer model run --json`，Python `subprocess` 调用
- **API 模式**：`urllib`（Python 内置），OpenAI 兼容 `/v1/chat/completions`
- **计时精度**：`time.perf_counter()` 纳秒级精度
- **Token 计数**：API 模式优先 `usage.completion_tokens`（精确），Auto 模式按字符估算
- **URL 拼接**：智能检测 `/v1`、`/v4`、`/chat/completions` 路径

## 注意事项

- Auto 模式的吞吐率包含网关路由开销，会比直接 API 略低（约 1-3%）
- Auto 模式 Token 数为估算值，API 模式为精确值
- 建议使用英文 prompt 以获得更准确的 token 估算
- 防缓存：每次迭代自动附加随机 seed 后缀
