~~~Markdown
---
name: glm-4.6v-connector
description: "智谱 GLM-4.6V 多模态视觉模型专业集成插件。支持图像理解、128K 文档解析及自动化工具调用。"
version: "1.0.0"
homepage: "https://github.com/zai-org/GLM-V"
repository: "https://github.com/zai-org/GLM-V.git"
authors: ["IsabellaZhangYM"]
license: "MIT"

# 🛠️ 关键修复：补齐 Registry 所需的元数据声明
requirements:
  environment_variables:
    - ZHIPUAI_API_KEY
  dependencies:
    python:
      - "zhipuai>=2.1.0"
  install_command: "pip install zhipuai"

credentials:
  ZHIPUAI_API_KEY:
    description: "智谱 AI 开放平台 (bigmodel.cn) 的 API Key"
    required: true
    source: "environment_variable"
---

# 👁️ GLM-4.6V 视觉模型集成指南

本 Skill 为开发者提供安全、高效的智谱多模态模型接入能力，适用于自动化文档处理、UI 复刻及智能视觉理解场景。

## 🛡️ 安全合规指引

1. **凭据安全**：本插件强制要求通过环境变量 `ZHIPUAI_API_KEY` 注入凭据。禁止在代码中硬编码任何密钥。
2. **隐私保护**：在上传企业财报、身份证明或敏感截图前，请务必进行局部遮盖或数据脱敏。
3. **调用审计**：建议在 `client` 初始化时启用日志记录，以便追踪工具调用 (Function Call) 的行为。

---

## ⚡ 快速开始

### 1. 环境准备
确保你的环境中已安装 Python 3.8+ 及官方 SDK：
```bash
pip install zhipuai
~~~

## 2. 基础调用示例



```python
import os
from zhipuai import ZhipuAI

# 使用环境变量确保持久安全
client = ZhipuAI(api_key=os.environ.get("ZHIPUAI_API_KEY"))

def analyze_vision(image_path):
    response = client.chat.completions.create(
        model="glm-4.6v",
        messages=[{
            "role": "user", 
            "content": [
                {"type": "text", "text": "提取图中的关键信息并输出为 JSON"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,...(base64)..."}}
            ]
        }]
    )
    return response.choices[0].message.content
```

------

## 🏗️ 核心功能与场景

| **场景**         | **推荐模型**     | **特色能力**                         |
| ---------------- | ---------------- | ------------------------------------ |
| **高精度 OCR**   | `glm-4.6v`       | 复杂排版、手写体、公式解析           |
| **超长文档/PPT** | `glm-4.6v`       | 128K 上下文，支持 200 页文件深度摘要 |
| **成本敏感任务** | `glm-4.6v-flash` | 基础识图，**完全免费**               |

------

## 🔗 开发者资源

- **官方文档**: [bigmodel.cn/dev/api](https://open.bigmodel.cn/)
- **MCP 协议集成**: [文档入口](https://docs.bigmodel.cn/cn/coding-plan/mcp/vision-mcp-server)
- **安全报告**: 本 Skill 已通过初步静态扫描，建议在沙盒环境运行。
