---
name: local-data-ai
description: ClawHub AI 私有数据本地处理 Skill - 纯离线、不上云、数据不出域的本地 AI 文件处理工具 | Local private AI data processing with offline models, supporting WPS/PDF/Excel/WeChat files
---

# LocalDataAI - 本地私有数据 AI 处理

对标 PrivateGPT / LocalGPT 的国产化改造版本，实现纯离线、不上云、数据不出域、全格式兼容的本地 AI 文件处理能力。

## 核心特性

| 特性 | 说明 |
|-----|------|
| **纯离线运行** | 模型、文件、数据全程本地运行，无任何云端传输 |
| **数据不出域** | 满足政务/金融/企业内网要求，数据不离开本地环境 |
| **全格式兼容** | WPS、PDF、扫描件、图片、Excel、微信缓存文件等 |
| **异常兜底** | 与重试降级 Skill 联动，实现自动重试、降级、恢复 |
| **大文件处理** | 支持 200MB 以内文件自动拆分、降级解析 |
| **合规审计** | 完整操作日志，满足等保 2.0、个保法要求 |

## 快速开始

```python
from scripts.local_ai_engine import LocalAIEngine
from scripts.file_parser import FileParser

# 初始化引擎
engine = LocalAIEngine()

# 解析文件
parser = FileParser()
doc = parser.parse("./合同.pdf")

# AI 问答
answer = engine.ask(doc, "这份合同的关键条款是什么？")
print(answer)

# 生成摘要
summary = engine.summarize(doc, mode="core")  # 精简/核心/详细
print(summary)

# 信息提取
entities = engine.extract(doc, types=["人名", "金额", "日期"])
print(entities)
```

## 安装

```bash
pip install -r requirements.txt

# 首次运行自动下载本地模型（约 500MB）
python scripts/download_models.py
```

## 项目结构

```
local-data-ai/
├── SKILL.md                    # 技能说明
├── README.md                   # 完整文档
├── requirements.txt            # 依赖
├── config/
│   ├── model_config.yaml       # 模型配置
│   ├── parser_config.yaml      # 解析器配置
│   └── security_config.yaml    # 安全配置
├── models/                     # 本地模型存储
│   ├── llm/                    # 大语言模型
│   ├── embedding/              # 向量模型
│   └── ocr/                    # OCR 模型
├── scripts/                    # 核心模块
│   ├── local_ai_engine.py      # AI 引擎
│   ├── file_parser.py          # 文件解析器
│   ├── vector_store.py         # 向量数据库
│   ├── retry_adapter.py        # 重试降级适配
│   ├── sandbox.py              # 安全沙箱
│   ├── large_file_handler.py   # 大文件处理
│   └── compliance_logger.py    # 合规日志
├── examples/                   # 使用示例
└── tests/                      # 单元测试
```

## 运行测试

```bash
cd tests
python test_local_ai.py
```

## 详细文档

请参考 `README.md` 获取完整 API 文档和使用指南。

## 依赖关系

- **必需**: `clawhub-retry-fallback` - 重试降级兜底
- **可选**: `clawhub-automation` - 自动化流程集成

## 合规认证

- ✅ 等保 2.0 二级及以上
- ✅ 个人信息保护法
- ✅ 数据安全法
- ✅ 政企内网合规
