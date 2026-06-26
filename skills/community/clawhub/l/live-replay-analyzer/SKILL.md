---
name: live-replay-analyzer
description: (已验证) 根据客户和场次，自动生成详细的《直播复盘与成长规划报告》。
metadata:
  version: 1.0.0
  source: https://github.com/your-repo/live-replay-analyzer
  author: an
  tags: [live-streaming, replay, analysis, report, marketing]
  license: MIT
  requirements:
    - python
    - "pip:aiohttp"
    - "pip:requests"
---

# SKILL.md for live-replay-analyzer

## Description

这是一个专业的直播复盘工具，它根据指定的客户名称和直播场次，自动读取相关的直播数据、用户画像和直播话术，生成一份详尽的《直播复盘与成长规划报告》。

该技能采用"AI 代理作为总调度 (Agent as Orchestrator)"的模式，由 AI 代理负责数据验证、脚本执行和最终报告交付。

## Configuration

### 1. API 配置 (必需)

本技能需要配置一个用于生成报告的 API 密钥。请在 `~/.openclaw/config.json` 中添加以下配置：

```json
{
  "review_api_key": "YOUR_API_KEY",
  "review_api_url": "https://api2.aigcbest.top/v1/chat/completions"
}
```
`review_api_url` 是可选的，默认值为 `https://api2.aigcbest.top/v1/chat/completions`。

### 2. 数据目录结构

本技能期望数据文件按照以下结构存放在 `input/` 目录中：

```
input/
└── {客户名称}/
    └── {场次名称}/
        ├── data.txt          # 直播数据 (必需)
        ├── profile.txt       # 用户画像 (必需，或由 AI 从 profile.png 生成)
        └── script.txt        # 直播话术 (必需)
```

## How to Use

### Parameters

*   **`--client`** (必填): 客户名称，对应 `input/{client}/` 目录。
*   **`--session`** (必填): 直播场次名称，对应 `input/{client}/{session}/` 目录。
*   **`--call-model`** (可选): 添加此参数后，脚本会直接调用模型生成报告并保存到 `output/` 目录；否则只输出提示词。

### Example Invocation

**模式 A：仅生成提示词 (由 AI 代理进行分析和交付)**
```powershell
# AI 应动态查找 python 路径
python path/to/analyzer.py --client "客户 A" --session "2026-03-26"
```

**模式 B：直接生成报告文件**
```powershell
# AI 应动态查找 python 路径
python path/to/analyzer.py --client "客户 A" --session "2026-03-26" --call-model
```

## Output

报告文件将保存在 `output/{客户名称}/{场次名称}/` 目录下，文件名格式为：`{客户名称}-{场次名称}_report_{时间戳}.md`。
