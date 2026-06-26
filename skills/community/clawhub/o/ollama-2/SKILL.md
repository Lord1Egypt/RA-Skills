---
name: ollama
description: |
  Ollama 本地大模型调用技能。支持通过 API 与 Ollama 实例交互进行文本生成。
  Use when: (1) 需要调用本地或远程 Ollama 模型 (2) 需要执行 LLM 推理任务 (3) 需要通过 Python 脚本与特定 Ollama 实例 (如 qwen3.5:9b) 交互。
---

# Ollama 技能

通过 API 方式调用 Ollama 模型。支持自定义 Host、模型名称以及 Prompt 提示词。

## 核心配置

- **环境变量**: 见 `.env.example`
- **默认地址**: `http://100.66.1.2:11434`
- **默认模型**: `qwen3.5:9b` (推荐)

## 使用方法

### 调用示例

```bash
# 基本调用（使用默认模型）
python scripts/ollama_query.py "请简述量子力学"

# 指定模型调用
python scripts/ollama_query.py "写一首关于春天的诗" qwen2.5:7b
```

## 安装说明

使用 `npx skills` 工具安装：

```bash
npx skills add ayflying/ai-skills --skill ollama
```

## 文件结构

```
ollama/
├── SKILL.md              # 技能说明
├── scripts/
│   ├── ollama_query.py   # 模型查询核心脚本
│   └── test_ollama.py    # 连通性测试脚本
├── .env.example          # 环境变量模板
└── assets/               # 资源目录
```

## 注意事项

1. **环境准备**: 确保本地已安装 Ollama 且服务已启动 (`ollama serve`)。
2. **模型下载**: 使用前需先下载模型，例如 `ollama pull qwen3.5:9b`。
3. **Python 依赖**: 需要安装 `requests` 库 (`pip install requests`)。
