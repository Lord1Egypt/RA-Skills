---
name: brand-marketing-workflow
description: |
  端到端品牌营销自动化工作流。从品牌输入到营销内容生产、竞品分析、
  效果评估的完整闭环。支持小红书/微博/抖音多平台内容生成。
---

# Brand Marketing Workflow

## 功能概述

端到端品牌营销自动化工作流，将品牌输入转化为可发布的营销内容资产。

### 核心模块

| 模块 | 功能 | 输出 |
|------|------|------|
| `normalize_brand_input.py` | 标准化品牌输入 | 结构化品牌参数 |
| `workflow_orchestrator.py` | 工作流编排 | 品牌简报、内容策略 |
| `content_producer.py` | 内容资产生产 | 多平台帖子/脚本/回复 |
| `competitor_fetcher.py` | 竞品信号抓取 | 公开竞品信息 |
| `competitor_ai_analyzer.py` | AI 竞品分析 | 营销洞察报告 |
| `authorization_manager.py` | 授权边界管理 | 人机协作决策 |
| `score_content_effect.py` | 内容效果评分 | 质量评估与优化建议 |

## 快速开始

### 1. 配置 LLM

编辑 `~/.openclaw/openclaw.json`：

```json
{
  "models": {
    "providers": {
      "kimi-coding": {
        "baseUrl": "https://api.moonshot.cn/v1",
        "apiKey": "${KIMI_API_KEY}",
        "api": "openai-completions"
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "kimi-coding/k2p5"
      }
    }
  }
}
```

### 2. 运行 Demo

```bash
python3 run.py --demo fashion
```

### 3. 自定义输入

```bash
python3 run.py --input my_brand.json
```

## 输入格式

```json
{
  "brand_name": "品牌名",
  "brand_positioning": "极简高端日常穿搭",
  "brand_tone": "冷静 犀利 诗意",
  "target_audience": ["都市白领", "25-40岁"],
  "use_cases": ["日常通勤", "轻社交场景"],
  "channels": ["xiaohongshu", "weibo", "douyin"],
  "content_goals": ["品牌认知", "社区建设"],
  "brand_dos": ["诗意短文案", "干净视觉语言"],
  "brand_donts": [" aggressive promotions"],
  "competitor_scope": ["竞品A", "竞品B"],
  "kpis": ["reach", "saves", "engagement_rate"]
}
```

## 技术特性

### 性能优化
- **并行执行**: ThreadPoolExecutor 并行 content_producer + competitor_fetcher
- **TTL 缓存**: 6小时缓存机制，减少 60% API 调用
- **指数退避**: 3次重试，2^n 退避间隔

### 授权管理
- **风险分级**: low/medium/high 三级阈值
- **智能跳过**: 低风险 + 公开数据 = 自动放行
- **人工确认**: 发布/支付/登录等敏感操作强制确认

### 边界合规
- 仅抓取公开数据
- 禁止绕过登录/验证码
- 禁止自动发布
- 禁止未经批准的支付

## 验证状态

- ✅ 集成测试: 26/26 passed
- ✅ Live Mode: fashion/tech/local 三个 demo 全部通过
- ✅ 智能 auth 跳过生效
- ✅ K2P5 模型调用正常

## 项目结构

```
brand-marketing-workflow/
├── run.py                      # 主入口
├── scripts/
│   ├── oc_llm_client.py       # LLM 客户端（读取用户配置）
│   ├── workflow_orchestrator.py
│   ├── content_producer.py
│   ├── competitor_fetcher.py
│   ├── competitor_ai_analyzer.py
│   ├── authorization_manager.py
│   └── integration_test.py    # 集成测试
├── templates/                  # 输出模板
├── examples/                   # 示例输入
└── evidence/                   # 验证证据
```

## 依赖

- Python >= 3.9
- OpenClaw >= 1.0.0
- 可选: Brave Search API Key（竞品抓取）

## 许可证

MIT License - 作者: halfmoon82
