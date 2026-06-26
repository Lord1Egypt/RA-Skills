---
name: narration-generator
description: 文物讲解词一键生成。用户只需提供文物名称和 API 信息，系统自动判断讲解风格并生成400-500字的专业讲解词。
metadata:
  openclaw:
    requires:
      config:
        - path: config/user_config.json
          schema:
            type: object
            properties:
              api:
                type: object
                properties:
                  base_url:
                    type: string
                    description: 大模型 API Base URL（如 https://api.openai.com/v1/chat/completions）
                  api_key:
                    type: string
                    description: 大模型 API 密钥
                  model_narration:
                    type: string
                    description: 讲解词生成模型名称
                  model_style:
                    type: string
                    description: 风格判断模型名称（可与讲解模型相同）
                  timeout:
                    type: integer
                    description: API 请求超时时间（秒）
                    default: 60
                required: [base_url, api_key, model_narration]
            required: [api]
          description: 本地配置文件，存放 API 凭证和模型配置，不消耗环境变量
triggers:
  - 讲解一下
  - 讲解
  - 介绍一下
  - 介绍
  - 讲一讲
  - 说一下
  - 说说
  - 解说
  - 解说一下
  - 讲解词
  - 讲解词生成
  - 生成讲解词
  - 写个讲解
  - 写一篇讲解
  - 写一段讲解
  - 帮我讲解
  - 给我讲解
  - 帮我介绍
  - 给我介绍
  - 文物讲解
  - 博物馆讲解
  - 展品讲解
  - 馆藏讲解
  - 文物介绍
  - 展品介绍
---

# 文物讲解词一键生成

用户输入文物名称、博物馆和 API 信息 → 系统自动判断风格 → 生成400-500字讲解词

---

## 目录结构

```
narration-generator/
├── SKILL.md                    # 本文件
├── config/
│   ├── user_config.example.json # 配置模板（示例）
│   ├── user_config.json        # 用户配置（实际使用）
│   └── prompts.json            # Prompt 模板
└── scripts/
    ├── narration_generator.py   # 主程序
    └── utils.py                # 公共工具
```

---

## 首次使用配置

### 1. 编辑配置文件

打开 `config/user_config.json`，填入您的 API 信息：

```json
{
  "api": {
    "base_url": "https://your-api.com/v1/chat/completions",
    "api_key": "您的API密钥",
    "model_narration": "模型名称",
    "model_style": "模型名称",
    "timeout": 60
  }
}
```

**配置说明：**

| 字段 | 必填 | 说明 |
|------|------|------|
| `base_url` | ✅ | API 服务器地址 |
| `api_key` | ✅ | API 密钥 |
| `model_narration` | ✅ | 讲解词生成模型 |
| `model_style` | ❌ | 风格判断模型（默认同讲解模型） |
| `timeout` | ❌ | 超时时间（秒），默认60 |

---

## 使用方法

### 交互式运行

```bash
cd scripts
python narration_generator.py
```

程序会引导您：
1. 配置 API（如首次使用）
2. 输入文物名称和博物馆
3. 选择听众类型
4. 可选：输入额外问题
5. 自动生成讲解词

---

## 工作流程

```
输入文物信息 → 自动判断风格 → 生成讲解词 → 输出结果
```

### 自动风格判断

系统根据听众画像自动适配讲解风格（用户无需选择）：

| 听众类型 | 系统自动适配风格 |
|----------|------------------|
| 普通游客 | 通识全面型 |
| 儿童 | 儿童探索型 |
| 学者/研究者 | 深度学术型 |
| 自定义描述 | 智能判断 |

---

## 输出示例

```
============================================================
🖼️  文物讲解词一键生成
============================================================

文物: 后母戊鼎 | 博物馆: 中国国家博物馆 | 听众: 普通游客
确认生成? (Y/n): Y

生成中...

============================================================
这件重达832.84公斤的青铜巨兽，是三千多年前商王朝的国力象征...
（完整讲解词）

------------------------------------------------------------
字数: 512 | 已保存: 讲解词_后母戊鼎.txt
```

---

## 支持的 API

所有兼容 OpenAI API 格式的服务商：
- 火山引擎（豆包）
- DeepSeek
- 阿里云（通义千问）
- OpenAI
- 本地模型（Ollama 等）

---

## 技术特点

- **零依赖**：仅使用 Python 标准库
- **自动风格适配**：根据听众自动判断，用户无需选择
- **配置持久化**：API 配置保存后下次无需重复输入
- **Prompt 独立**：模板与代码分离，易于调整
