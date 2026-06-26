# PromptBuddy Lite

> ⚡ 纯 Shell 版 Prompt 优化技能

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Shell](https://img.shicks.io/badge/Shell-Bash-green.svg)]()

**零依赖，极快响应，轻量级**

---

## 为什么选择 Lite 版？

| 特性 | Lite 版 |
|------|---------|
| 依赖 | **零依赖** |
| 速度 | **~12ms** |
| 大小 | **3KB** |
| 兼容性 | 所有 Linux/macOS |

---

## 安装

```bash
clawhub install promptbuddy-lite
```

---

## 使用

```bash
pb "火箭如何上天"
```

**输出示例**：
```json
{
  "need_optimization": true,
  "intent": "cot",
  "confidence": 1,
  "optimized_prompt": "[角色设定] 你是一位专业的推理专家 [指令] 火箭如何上天..."
}
```

---

## 意图识别

| 意图 | 触发词 | 模板 |
|------|--------|------|
| **CoT 推理** | 如何、为什么、原理 | 逐步思考 |
| **Decompose 分解** | 步骤、流程、方案 | 任务拆解 |
| **Criticize 审核** | 检查、审核、评估 | 问题发现 |
| **Base 基础** | 写一个、生成、帮我 | 直接回答 |

---

## 与 PromptBuddy 对比

| 特性 | PromptBuddy | PromptBuddy Lite |
|------|-------------|------------------|
| 实现 | Python + Shell | **纯 Shell** |
| 依赖 | Python, numpy | **无** |
| 速度 | ~125ms | **~12ms (10倍快)** |
| 语义分析 | TF-IDF | 关键词匹配 |
| 精度 | 更精准 | 够用 |
| 适用场景 | 专业用户 | 轻量用户 |

---

## 技术架构

```
用户输入
    ↓
关键词匹配（~1ms）
    ↓
意图识别（~5ms）
    ↓
模板填充（~5ms）
    ↓
优化后的 Prompt
```

**总耗时：~12ms**

---

## 文件结构

```
promptbuddy-lite/
├── SKILL.md           # 技能说明
├── README.md          # 本文档
├── LICENSE            # MIT 许可证
├── scripts/
│   └── promptbuddy.sh # 核心脚本（3KB）
└── config/
    └── config.json    # 配置
```

---

## 许可证

[MIT License](LICENSE)

---

## 作者

**曾鹏祥**
GitHub: https://github.com/Steventsang18/promptbuddy-lite

---

**PromptBuddy Lite - 零依赖，极快响应**