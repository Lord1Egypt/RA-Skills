# OpenClaw CNC Core

> CNC加工智能报价系统 | Intelligent CNC Machining Quote System

## 简介

OpenClaw CNC Core 是面向CNC加工行业的智能报价引擎，提供：
- 📐 STEP/STL 图纸解析
- 💰 智能报价计算
- ⚠️ 风险控制预警
- 🔍 历史案例检索

## 在线演示

🌐 **演示地址**: http://47.253.101.130/

> 🔒 安全防护：Nginx限流 (20次/分钟/IP) + 安全头 + 50MB上传限制

## 快速开始

```python
from core.quote_engine import OpenClawQuoteEngine

# 初始化引擎
engine = OpenClawQuoteEngine(config_dir="./config/examples")

# 计算报价
order = {
    "material": "铝6061",
    "volume_cm3": 100,
    "area_dm2": 20,
    "quantity": 10,
    "surface_treatment": "阳极氧化"
}
result = engine.calculate_quote(order)
print(f"报价: ¥{result.total_price}")
```

## 支持的LLM平台

| 平台 | 标识符 | 需要API Key |
|------|--------|-------------|
| DashScope | `dashscope` | ✅ |
| OpenAI | `openai` | ✅ |
| DeepSeek | `deepseek` | ✅ |
| 智谱AI | `zhipu` | ✅ |
| Moonshot | `moonshot` | ✅ |
| Ollama (本地) | `local` | ❌ |

## 版本

- **社区版**: MIT License，免费使用
- **商业版**: 预训练模型 + 行业价格库 + 定制服务

## 联系方式

- 🌐 官网: https://openclaw.ai/cnc
- 📧 邮箱: miscdd@163.com
- 💬 QQ: 849355070
- GitHub: https://github.com/Timo2026/openclaw-cnc-core

---

**开源日期**: 2026-03-26  
**版本**: v1.2.0  
**许可证**: MIT