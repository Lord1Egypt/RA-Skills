# Model Router · OpenClaw

> 本地优先的智能模型选择器 — 根据任务复杂度自动路由到本地或服务商模型

## 核心原则

1. **模型选择只在任务入口做一次**
2. **同一任务中途不切换模型**（保护上下文连续性）
3. **简单任务用本地，复杂任务用服务商**

---

## 功能

### 任务复杂度判断

- **简单任务** → 本地模型（Ollama / llama.cpp）
  - 单次回答即可完成
  - 不需要多步推理或迭代
  - 类型：翻译、格式转换、查定义、简单写作、文本润色

- **复杂任务** → 服务商模型（MiniMax / OpenRouter / 其他）
  - 需要深度推理、多次迭代
  - 长上下文理解
  - 类型：代码调试、架构设计、战略分析、长文撰写

### 模型配置

```yaml
providers:
  local:
    ollama:
      endpoint: "http://localhost:11434"
      default_model: "qwen2.5-coder:7b"
    llama.cpp:
      endpoint: "http://localhost:8080"
      default_model: "qwen2.5-coder-7b-q4"
  cloud:
    minmax:
      endpoint: "https://api.minimax.chat"
      default_model: "MiniMax-Text-01"
    openrouter:
      endpoint: "https://openrouter.ai/api/v1"
      default_model: "anthropic/claude-sonnet-4-5"
```

---

## 使用方式

### 交互式分类

```bash
python3 scripts/classify_task.py "帮我把这段中文翻译成英文"
```

输出示例：
```
复杂度：简单
路由：本地模型（Ollama/qwen2.5-coder:7b）
理由：单次完成，无需迭代
```

### 批量分类

```bash
python3 scripts/classify_task.py "分析这个产品的市场策略" --verbose
```

---

## 上下文连续性保护

| 情况 | 处理方式 |
|---|---|
| 任务内切换 | ❌ 不允许 |
| 新任务开始 | ✅ 重新判断 |
| 模型不可用 | 自动降级到同级别模型 |

---

## 扩展服务商

新增服务商只需在配置中添加：

```yaml
providers:
  cloud:
    新服务商:
      endpoint: "API地址"
      default_model: "默认模型"
```

---

## 决策示例

| 任务描述 | 判断 | 路由 |
|---|---|---|
| "翻译成英文" | 简单 | 本地模型 |
| "写一个快速排序" | 简单 | 本地模型 |
| "调试内存泄漏" | 复杂 | 服务商模型 |
| "分析市场策略" | 复杂 | 服务商模型 |
| "润色邮件" | 简单 | 本地模型 |
| "设计后端架构" | 复杂 | 服务商模型 |

---

## 文件结构

```
openclaw-model-router/
├── SKILL.md           # 本文件
├── package.json       # OpenClaw 清单
├── install.sh         # 安装脚本
└── scripts/
    ├── classify_task.py    # 任务分类器
    └── setup_wizard.py     # 配置向导
```

---

**版本**：v1.0.1
**许可证**：MIT
**作者**：freepengyang
