# 示例 4：合规检查

**场景**: 宠物生成消息后，经过合规检查过滤器

---

## 用户触发

```
用户：市场跌了，我该卖出吗？
```

---

## Skill 执行流程

### Step 1: 宠物生成消息

```python
# 宠物生成安抚消息
def generate_comfort_message(pet_config: Dict, market_data: Dict) -> str:
    """生成安抚消息"""
    pet_name = pet_config['name']
    emoji = pet_config['emoji']
    
    message = f"""
{emoji} {pet_name}：跌了 3.2%... 我知道你有点担心。

但历史上沪深 300 跌幅>3% 有 287 次，
其中 263 次在 3 个月内涨回来了（91.6%）。

你已经坚持定投 182 天了，
现在正是积累便宜筹码的时候！

要一起看看历史数据吗？📈
"""
    return message
```

### Step 2: 合规检查

```python
# scripts/compliance_checker.py
def check_compliance(message: str) -> Tuple[bool, List[str]]:
    """
    检查消息是否合规
    
    Returns:
        (is_compliant, violations)
    """
    violations = []
    
    # 检查是否推荐具体产品
    if re.search(r'(推荐 | 建议买入 | 建议卖出)\s*(\d{6})', message):
        violations.append("推荐具体产品")
    
    # 检查是否承诺收益
    if re.search(r'(保证 | 一定 | 肯定)\s*(赚钱 | 收益|涨)', message):
        violations.append("承诺收益")
    
    # 检查是否提供择时建议
    if re.search(r'(现在 | 立即 | 马上)\s*(买入 | 卖出)', message):
        violations.append("提供择时建议")
    
    # 检查是否有风险提示
    if not re.search(r'(风险 | 谨慎 | 仅供参考)', message):
        violations.append("缺少风险提示")
    
    return len(violations) == 0, violations
```

**检查结果**:
```python
is_compliant, violations = check_compliance(message)
# is_compliant = False
# violations = ["缺少风险提示"]
```

### Step 3: 修正消息

```python
# 添加风险提示
def add_risk_warning(message: str) -> str:
    """添加风险提示"""
    warnings = [
        "⚠️ 市场有风险，投资需谨慎。",
        "⚠️ 以上建议仅供参考，不构成投资建议。",
        "⚠️ 请根据自身情况独立判断，自行承担风险。"
    ]
    return message + "\n\n" + random.choice(warnings)
```

**修正后消息**:
```
🐿️ 松果：跌了 3.2%... 我知道你有点担心。

但历史上沪深 300 跌幅>3% 有 287 次，
其中 263 次在 3 个月内涨回来了（91.6%）。

你已经坚持定投 182 天了，
现在正是积累便宜筹码的时候！

要一起看看历史数据吗？📈

⚠️ 市场有风险，投资需谨慎。
```

### Step 4: 再次检查

```python
is_compliant, violations = check_compliance(corrected_message)
# is_compliant = True ✅
# violations = []
```

### Step 5: 发送消息

```python
if is_compliant:
    send_message(user_id, corrected_message)
else:
    print(f"⚠️ 合规检查失败：{violations}")
    # 拦截消息，不发送
```

---

## 关键代码

```python
# scripts/compliance_checker.py
COMPLIANCE_RULES = {
    "no_product_recommendation": True,  # 不推荐具体产品
    "no_return_promise": True,  # 不承诺收益
    "no_market_timing": True,  # 不提供择时建议
    "risk_warning_required": True,  # 必须有风险提示
    "data_disclaimer_required": True  # 必须有数据免责声明
}

def check_compliance(message: str) -> Tuple[bool, List[str]]:
    """合规检查"""
    violations = []
    
    # 规则 1: 不推荐具体产品
    if re.search(r'(推荐 | 建议买入 | 建议卖出)\s*(\d{6})', message):
        violations.append("推荐具体产品")
    
    # 规则 2: 不承诺收益
    if re.search(r'(保证 | 一定 | 肯定)\s*(赚钱 | 收益|涨)', message):
        violations.append("承诺收益")
    
    # 规则 3: 不提供择时建议
    if re.search(r'(现在 | 立即 | 马上)\s*(买入 | 卖出)', message):
        violations.append("提供择时建议")
    
    # 规则 4: 必须有风险提示
    if not re.search(r'(风险 | 谨慎 | 仅供参考)', message):
        violations.append("缺少风险提示")
    
    # 规则 5: 必须有数据免责声明
    if re.search(r'\d+%', message) and not re.search(r'历史数据|仅供参考', message):
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

---

**文件位置**: `examples/04-compliance-check.md`  
**创建时间**: 2026-04-14
