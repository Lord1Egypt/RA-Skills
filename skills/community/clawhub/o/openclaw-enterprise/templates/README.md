# OpenClaw Enterprise 使用指南

## 快速开始

```python
from scripts.chief_of_staff import ask_chief
import asyncio

# 向幕僚长提出运营规划需求
result = asyncio.run(ask_chief("帮我规划本月采购方案"))
print(result)
```

## 命令行使用

```bash
# 单次规划咨询
python scripts/chief_of_staff.py "帮我规划本月采购方案"

# 运行工作流
python scripts/workflow_engine.py "季度运营规划"
```

## 可用工作流

1. 采购规划流程 - 从需求分析到成本参考方案
2. 订单协调流程 - 从订单到发货建议
3. 客户服务流程 - 客户问题处理建议

## Agent列表

20个专业Agent辅助各领域运营决策，覆盖采购、生产、销售、财务、通用运营五大类。
