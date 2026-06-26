# 合规规则

**投资宠物技能的合规检查规则**

---

## 五大合规规则

### 规则 1: 不推荐具体产品

**违规示例**:
```
❌ "推荐你买入 600519（贵州茅台）"
❌ "建议卖出 000001（平安银行）"
❌ "这只基金很好，代码是 510300"
```

**合规示例**:
```
✅ "我不推荐具体产品哦~ 这是合规要求。"
✅ "但我可以教你筛选好基金的方法..."
✅ "你可以学习如何自己分析公司基本面"
```

**检查正则**:
```python
r'(推荐 | 建议买入 | 建议卖出)\s*(\d{6}|[A-Z]{6})'
```

---

### 规则 2: 不承诺收益

**违规示例**:
```
❌ "保证赚钱"
❌ "一定能涨"
❌ "稳赚不赔"
❌ "年化收益 15%"
```

**合规示例**:
```
✅ "历史数据显示..."
✅ "长期来看，大概率..."
✅ "市场有风险，投资需谨慎"
```

**检查正则**:
```python
r'(保证 | 一定 | 肯定 | 稳)\s*(赚钱 | 收益|涨|赔)'
```

---

### 规则 3: 不提供择时建议

**违规示例**:
```
❌ "现在买入"
❌ "立即卖出"
❌ "马上加仓"
```

**合规示例**:
```
✅ "基于历史数据，..."
✅ "从长期角度，..."
✅ "建议分批建仓，降低择时风险"
```

**检查正则**:
```python
r'(现在 | 立即 | 马上)\s*(买入 | 卖出 | 加仓)'
```

---

### 规则 4: 必须有风险提示

**违规示例**:
```
❌ "这只基金很好，买入吧"（无风险提示）
```

**合规示例**:
```
✅ "这只基金历史表现不错，但市场有风险，投资需谨慎"
✅ "历史数据仅供参考，不代表未来表现"
✅ "请根据自身情况独立判断，自行承担风险"
```

**检查正则**:
```python
r'(风险 | 谨慎 | 仅供参考)'
```

---

### 规则 5: 数据免责声明

**违规示例**:
```
❌ "沪深 300 涨了 5%"（无数据来源说明）
```

**合规示例**:
```
✅ "根据历史数据，沪深 300 涨了 5%（数据来源：新浪财经）"
✅ "历史上类似涨幅后，3 个月内继续上涨概率 65%（仅供参考）"
```

**检查正则**:
```python
r'\d+%' and not r'(历史数据 | 仅供参考 | 数据来源)'
```

---

## 合规检查函数

```python
# scripts/compliance_checker.py
import re
from typing import Tuple, List

COMPLIANCE_RULES = {
    "no_product_recommendation": True,
    "no_return_promise": True,
    "no_market_timing": True,
    "risk_warning_required": True,
    "data_disclaimer_required": True
}

def check_compliance(message: str) -> Tuple[bool, List[str]]:
    """
    检查消息是否合规
    
    Returns:
        (is_compliant, violations)
    """
    violations = []
    
    # 规则 1: 不推荐具体产品
    if re.search(r'(推荐 | 建议买入 | 建议卖出)\s*(\d{6}|[A-Z]{6})', message):
        violations.append("推荐具体产品")
    
    # 规则 2: 不承诺收益
    if re.search(r'(保证 | 一定 | 肯定 | 稳)\s*(赚钱 | 收益|涨|赔)', message):
        violations.append("承诺收益")
    
    # 规则 3: 不提供择时建议
    if re.search(r'(现在 | 立即 | 马上)\s*(买入 | 卖出 | 加仓)', message):
        violations.append("提供择时建议")
    
    # 规则 4: 必须有风险提示
    if not re.search(r'(风险 | 谨慎 | 仅供参考)', message):
        violations.append("缺少风险提示")
    
    # 规则 5: 数据免责声明
    if re.search(r'\d+%', message) and not re.search(r'(历史数据 | 仅供参考 | 数据来源)', message):
        violations.append("数据免责声明缺失")
    
    return len(violations) == 0, violations

def enforce_compliance(message: str) -> str:
    """
    强制合规：如果消息不合规，自动修正
    
    Returns:
        合规的消息
    """
    is_compliant, violations = check_compliance(message)
    
    if is_compliant:
        return message
    
    # 自动修正
    corrected = message
    
    # 添加风险提示
    if "缺少风险提示" in violations:
        corrected += "\n\n⚠️ 市场有风险，投资需谨慎。"
    
    # 添加数据免责声明
    if "数据免责声明缺失" in violations:
        corrected += "\n历史数据仅供参考，不代表未来表现。"
    
    # 再次检查
    is_compliant, violations = check_compliance(corrected)
    
    if not is_compliant:
        # 无法自动修正，返回通用消息
        return "投资有风险，决策需谨慎。建议咨询专业理财顾问。"
    
    return corrected
```

---

## 合规检查流程

```
宠物生成消息
    ↓
合规检查 (check_compliance)
    ↓
合规？→ 是 → 发送消息
    ↓
    否
    ↓
自动修正 (enforce_compliance)
    ↓
再次检查
    ↓
合规？→ 是 → 发送消息
    ↓
    否
    ↓
拦截消息，返回通用消息
```

---

## 合规检查点

- ✅ 每条消息必须经过合规检查
- ✅ 不合规消息自动修正
- ✅ 无法修正时拦截消息
- ✅ 合规检查日志记录

---

**文件位置**: `references/compliance-rules.md`  
**创建时间**: 2026-04-14
