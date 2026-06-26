---
name: maskclaw-core
version: 1.0.0
type: skill
description: MaskClaw - 端侧隐私保护 Skill 套件，提供智能打码、行为监控与规则自进化能力
author: MaskClaw Team
homepage: https://github.com/your-org/maskclaw
license: MIT
tags:
  - privacy
  - security
  - visual-masking
  - behavior-monitoring
  - self-evolution
  - on-device
keywords:
  - PII detection
  - visual obfuscation
  - privacy-preserving
  - mobile UI agent
  - tool-use
minicpm_version: ">= 4.5"
platform:
  - android
  - windows
  - macos
dependencies:
  - rapidocr
  - opencv-python
  - numpy
  - transformers
  - chromadb
---

# MaskClaw Core Skills

> 端侧隐私保护 Skill 套件 —— 智能打码 · 行为监控 · 规则自进化

---

## 1. 项目概述

**MaskClaw** 是一个基于端侧 Tool-Use 的隐私前置代理框架，充当云端 Agent (AutoGLM) 与手机/桌面 UI 之间的"安全保镖"。

系统通过端侧 MiniCPM-V 大模型调度一组原子化工具 (Skills)，在执行前对敏感数据进行实时识别、动态脱敏，并通过用户行为反馈实现隐私防护策略的**自进化**。

```
┌────────────────────────────────────────────────────────────────┐
│                      MaskClaw 四层协同架构                      │
├────────────────────────────────────────────────────────────────┤
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   │
│  │  感知层   │ → │  认知层   │ → │  工具层   │ → │  进化层   │   │
│  │Perception│   │Cognition │   │Tool-Use  │   │Evolution │   │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘   │
│                                                                │
│  ┌────────────────────────────────────────────────────────┐   │
│  │              ChromaDB RAG 规则知识库                     │   │
│  └────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────┘
```

---

## 2. 核心 Skills

| Skill | 功能 | 核心能力 |
|:------|:-----|:---------|
| **Smart_Masker** | 智能视觉打码 | 基于 RapidOCR 识别敏感文本，支持高斯模糊/马赛克/色块覆盖 |
| **Behavior_Monitor** | 行为监控 | 持续监听 Agent 操作，捕获用户主动干预动作 |
| **Skill_Evolution** | 规则自进化 | 基于爬山法持续优化 SOP，沙盒测试验证后自动挂载 |

---

## 3. 快速开始

### 3.1 环境要求

```bash
# Python >= 3.10
pip install rapidocr opencv-python numpy transformers chromadb
```

### 3.2 启动模型服务

```bash
cd model_server
python minicpm_api.py
# 模型服务将监听 http://127.0.0.1:8000
```

### 3.3 使用 Smart Masker

```python
from skills.smart_masker import VisualMasker

masker = VisualMasker()
keywords = ["手机号", "身份证", "银行卡"]

result = masker.process_image(
    image_path="test.jpg",
    sensitive_keywords=keywords,
    method="blur"
)

print(f"检测到 {result['regions_count']} 个敏感区域")
print(f"脱敏图片: {result['masked_image_path']}")
```

### 3.4 使用 Behavior Monitor

```python
from skills.behavior_monitor import log_action_to_chain

log_action_to_chain(
    user_id="user_001",
    action="share_or_send",
    resolution="block",
    scenario_tag="钉钉发送病历截图",
    app_context="钉钉",
    field="medical_record",
    pii_type="MedicalRecord",
    correction_type="user_denied",
    auto_flush=True,
)
```

### 3.5 使用 Skill Evolution

```python
from skills.evolution_mechanic import SOPEvolution

engine = SOPEvolution()
result = engine.run_pipeline(
    user_id="user_001",
    draft_name="钉钉隐私规则",
    step="all",
)
```

---

## 4. 目录结构

```
maskclaw-core/
├── SKILL.md                    # 本文件
├── scripts/
│   ├── smart_masker.py          # 智能打码核心模块
│   ├── smart_masker_demo.py    # 打码演示脚本
│   ├── behavior_monitor.py     # 行为监控核心模块
│   ├── behavior_monitor_demo.py # 监控演示脚本
│   ├── evolution_mechanic.py  # 进化引擎核心模块
│   └── evolution_demo.py       # 进化演示脚本
├── references/
│   ├── ARCHITECTURE.md         # 系统架构文档
│   ├── SKILLS_API.md           # Skills API 契约
│   ├── RAG_SCHEMA.md           # 向量数据库设计
│   ├── PROMPT_TEMPLATES.md     # Prompt 模板
│   └── SELF_EVOLUTION.md       # 自进化机制设计
├── assets/
│   ├── rule_schema.json        # 规则 Schema 模板
│   └── sop_template.md         # SOP 模板
└── evals/
    └── evals.json              # 测试用例定义
```

---

## 5. API 契约

### 5.1 Smart Masker

**方法**: `process_image(image_path, sensitive_keywords, method='blur')`

| 参数 | 类型 | 必填 | 说明 |
|:-----|:-----|:----:|:-----|
| `image_path` | `str` | ✅ | 图片路径 |
| `sensitive_keywords` | `List[str]` | ✅ | 敏感关键词列表 |
| `method` | `str` | ❌ | `blur`(默认) / `mosaic` / `block` |

**返回值**:
```json
{
  "success": true,
  "masked_image_path": "temp/masked_xxx.jpg",
  "detected_regions": [{"text": "138****5678", "bbox": [x1, y1, x2, y2]}],
  "regions_count": 1,
  "processing_time_ms": 45
}
```

### 5.2 Behavior Monitor

**方法**: `log_action_to_chain(user_id, action, resolution, scenario_tag, ...)`

| 参数 | 类型 | 必填 | 说明 |
|:-----|:-----|:----:|:-----|
| `user_id` | `str` | ✅ | 用户标识 |
| `action` | `str` | ✅ | 操作类型 |
| `resolution` | `str` | ✅ | 决策结果 |
| `scenario_tag` | `str` | ✅ | 场景标签 |
| `correction_type` | `str` | ❌ | 纠错类型 |

**返回值**:
```json
{
  "chain_id": "user_001_钉钉发送病历_1700000001",
  "action_count": 1,
  "has_correction": false
}
```

### 5.3 Skill Evolution

**方法**: `run_pipeline(user_id, draft_name, step='all', ...)`

| 参数 | 类型 | 必填 | 说明 |
|:-----|:-----|:----:|:-----|
| `user_id` | `str` | ✅ | 用户标识 |
| `draft_name` | `str` | ✅ | 草稿名称 |
| `step` | `str` | ❌ | `rebuild`/`init`/`evolve`/`sandbox`/`publish`/`all` |

**返回值**:
```json
{
  "success": true,
  "evolve": {
    "total_iterations": 5,
    "final_score": 92.5,
    "reached_threshold": true
  },
  "sandbox": {"passed": true},
  "publish": {"skill_name": "dingtalk-privacy-rule", "version": "v1.0.0"}
}
```

---

## 6. 五级置信度判决

| 判决 | 条件 | 系统行为 |
|:----:|:-----|:---------|
| **Allow** | 规则库完整匹配，安全 | 直接放行 |
| **Block** | 规则库完整匹配，风险明确 | 直接拦截 |
| **Mask** | 规则库完整匹配，需脱敏 | 执行打码后放行 |
| **Ask** | 规则库信息不完整 | 主动向用户确认 |
| **Unsure** | 新场景无记录 | 标记并等待用户教授 |

---

## 7. 自进化机制 (爬山法)

```
┌─────────────────────────────────────────────────────────────┐
│  第 1 步：agent 对 skill 做一个小改动                         │
│         （比如：加一条"必须核对输入数据"的规则）               │
├─────────────────────────────────────────────────────────────┤
│  第 2 步：用改动后的 skill 跑 10 个测试用例                   │
├─────────────────────────────────────────────────────────────┤
│  第 3 步：用 checklist 给每个输出打分                         │
│         （4 个检查项全过 = 100 分，3 个过 = 75 分...）        │
├─────────────────────────────────────────────────────────────┤
│  第 4 步：算平均分                                           │
│         - 比上一轮高 → 保留改动                               │
│         - 比上一轮低 → 撤销改动                               │
├─────────────────────────────────────────────────────────────┤
│  第 5 步：重复，直到连续 3 轮分数超过 90% 或你喊停            │
└─────────────────────────────────────────────────────────────┘
```

---

## 8. 错误码

| 错误码 | 说明 | 处理建议 |
|:------:|:-----|:---------|
| `MASK_001` | 图片解码失败 | 检查图片格式 |
| `MASK_002` | 图片过大 | 压缩后重试 |
| `MASK_003` | OCR 识别失败 | 检查图片质量 |
| `MONITOR_001` | 日志写入失败 | 检查存储权限 |
| `EVOLUTION_001` | 规则生成失败 | 减少测试用例批次 |
| `EVOLUTION_002` | 沙盒测试超时 | 检查测试环境 |

---

## 9. 许可

MIT License

## 10. 更新日志

### v1.0.0 (2026-03-25)
- 初始版本发布
- 包含 Smart_Masker, Behavior_Monitor, Skill_Evolution 三大核心模块
- 支持 MiniCPM-V 4.5
- 集成 ChromaDB RAG 知识库
