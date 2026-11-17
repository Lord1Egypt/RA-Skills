# nvidia-llm

英伟达 NIM 大模型智能路由 Skill — 一行代码调用 50+ 前沿模型，自动处理限流/超时/降级。

**作者**: 用户 | **版本**: 1.0.0

---

## 核心特性

- **智能路由** — 自动选择效果/速度最优的可用模型
- **自动降级** — 限流(429)/超时/服务不可用时自动切换备用模型
- **熔断器** — 连续失败自动熔断，探测恢复后自动启用
- **延迟追踪** — 实时统计各模型延迟，优先使用最快的
- **并发请求** — 同时向多个模型发请求，取最快响应（Hedge 模式）
- **场景感知** — 编码/推理/创意/快速 自动匹配最优模型组

---

## 快速开始

```bash
pip install nvidia-llm
```

```python
from nvidia_llm import chat, stream, AutoRouter

# 最简单 — 一行调用
print(chat("你好"))

# 编码场景 — 自动路由到最优代码模型
print(chat("写一个 Python 爬虫", scene="code"))

# 流式输出
for text in stream("讲个科幻故事", scene="creative"):
    print(text, end="", flush=True)

# 智能路由器 — 查看用了哪个模型、延迟多少
router = AutoRouter(scene="code")
result = router.chat("写快速排序")
print(f"模型: {result['model_alias']}, 延迟: {result['latency']:.2f}s")
print(result["content"])
```

---

## 场景列表

| 场景 | 说明 | 默认降级链 |
|------|------|-----------|
| `default` | 通用对话 | ultra → deepseek → mistral675b → llama33-70b → ... |
| `code` | 代码生成 | ultra → deepseek → codestral → codellama → ... |
| `fast` | 极速响应 | deepseek-fast → nano9b → mini4b → ... |
| `reasoning` | 推理/数学 | ultra → qwen397b → deepseek → glm → ... |
| `creative` | 创意写作 | creative → ultra → glm → qwen397b → ... |
| `chinese` | 中文优化 | qwen397b → glm → deepseek → kimi → ... |
| `multimodal` | 图像/视频 | qwen397b → llama4 → minimax → llama32-90b → ... |
| `finance` | 金融分析 | finance → ultra → deepseek → ... |
| `medical` | 医疗诊断 | medical → ultra → deepseek → ... |
| `translate` | 翻译 | translate → ultra → deepseek → ... |
| `edge` | 边缘部署 | nano9b → mini4b → gemma4b → ... |

---

## 高级用法

### 并发 Hedge 模式

```python
router = AutoRouter(hedge_mode=True, hedge_top_n=2)
result = router.chat("你好")  # 同时向2个模型发请求，取最快
```

### 健康状态监控

```python
from nvidia_llm import status
print(status())
```

### 单模型实例

```python
from nvidia_llm import LLM

llm = LLM(model="ultra", system="你是一位Python专家")
llm.say("写个装饰器")     # 第一轮
llm.say("加个类型提示")    # 自动带历史
llm.clear()                # 清空历史
```

---

## CLI 命令行

```bash
# 对话
nvidia-llm chat "你好"
nvidia-llm chat "写爬虫" --scene code

# 流式
nvidia-llm stream "讲个故事" --scene creative

# 查看模型健康状态
nvidia-llm status

# 列出所有模型
nvidia-llm models
nvidia-llm models --tag code

# 测试连通性
nvidia-llm test --model ultra
```

---

## 环境变量

```bash
export NVIDIA_API_KEY="your-api-key"
```

---

## 安装

```bash
pip install nvidia-llm
# 或从源码安装
pip install -e .
```

---

## 许可证

MIT License