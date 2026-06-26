---
name: personal-finance-pro
description: 个人财务管理助手 - 银行账单分析、消费分类、预算管理、财务报表、储蓄建议
metadata:
  openclaw:
    emoji: "💳"
    install:
      - id: shell-check
        kind: shell
        label: "检查 Shell 环境"
keywords:
  - 个人理财
  - 记账
  - 消费分析
  - 预算管理
  - 银行账单
  - 财务报表
---

# 个人财务管理助手

## 功能特性

- CSV 账单导入（支持多种格式）
- 基础数据验证
- 收支汇总（按月/季度/年）
- 智能消费分类
- 预算管理
- 财务健康评分
- 储蓄建议
- 定期报表推送
- **隐私保护**（账号脱敏）
- **离线处理**（无需网络）

## 快速开始

```bash
# 克隆技能
git clone <repo> ~/.openclaw/workspace/skills/personal-finance

# 测试
./personal-finance.sh validate --csv sample-data/sample-transactions.csv
```

## 数据验证

```bash
./personal-finance.sh validate --csv your_bank_export.csv
```

检查 CSV 格式是否正确：
- 必需字段：date, description, amount, account_number
- 金额必须为数字
- 日期格式验证

### 2. 收支汇总

```bash
# 按月汇总
./personal-finance.sh summarize --period month --csv your_bank_export.csv

# 按季度汇总
./personal-finance.sh summarize --period quarter --csv your_bank_export.csv

# 按年汇总
./personal-finance.sh summarize --period year --csv your_bank_export.csv
```

输出示例：
```
📊 月度收支汇总

月份        收入        支出        净收入
2024-01    ¥15,000    ¥12,000    ¥3,000
2024-02    ¥15,500    ¥11,000    ¥4,500
2024-03    ¥16,000    ¥13,500    ¥2,500
```

### 3. 基础分类

```bash
./personal-finance.sh categorize --csv your_bank_export.csv --output categorized.csv
```

使用 `config/category-rules.json` 中的规则进行关键词匹配分类。

## 智能消费分类

基于机器学习的自动分类：

```python
def smart_categorize(transactions):
    """智能消费分类"""
    categories = {
        '餐饮': ['美团', '饿了么', '肯德基', '麦当劳', '星巴克', '海底捞'],
        '交通': ['滴滴', '地铁', '公交', '加油', '停车', '高铁', '机票'],
        '购物': ['淘宝', '京东', '拼多多', '天猫', '唯品会'],
        '娱乐': ['电影', '游戏', 'KTV', '健身', '旅游'],
        '居住': ['房租', '水电', '物业', '宽带', '房贷'],
        '医疗': ['医院', '药店', '体检', '保险'],
        '教育': ['学费', '培训', '书籍', '课程'],
        '社交': ['红包', '礼物', '聚餐', '转账']
    }
    
    results = []
    for _, row in transactions.iterrows():
        desc = row['description'].lower()
        category = '其他'
        
        for cat, keywords in categories.items():
            if any(kw in desc for kw in keywords):
                category = cat
                break
        
        results.append({
            'date': row['date'],
            'description': row['description'],
            'amount': row['amount'],
            'category': category
        })
    
    return pd.DataFrame(results)
```

### 2. 预算管理

```python
def budget_analysis(transactions, budgets):
    """预算执行分析"""
    monthly = transactions.groupby([
        transactions['date'].dt.to_period('M'),
        'category'
    ])['amount'].sum().reset_index()
    
    results = []
    for _, row in monthly.iterrows():
        budget = budgets.get(row['category'], 0)
        actual = abs(row['amount']) if row['amount'] < 0 else 0
        usage = (actual / budget * 100) if budget > 0 else 0
        
        status = '✅' if usage <= 100 else '⚠️' if usage <= 120 else '🚨'
        
        results.append({
            '月份': row['date'],
            '类别': row['category'],
            '预算': budget,
            '实际': actual,
            '使用率': f"{usage:.1f}%",
            '状态': status
        })
    
    return pd.DataFrame(results)

# 预算配置示例
budgets = {
    '餐饮': 3000,
    '交通': 1000,
    '购物': 2000,
    '娱乐': 1500,
    '居住': 5000,
    '医疗': 500,
    '教育': 1000,
    '社交': 1000
}
```

### 3. 财务健康评分

```python
def financial_health_score(transactions, income, savings):
    """财务健康评分"""
    score = 100
    issues = []
    
    # 1. 储蓄率
    monthly_income = income
    monthly_expense = abs(transactions[transactions['amount'] < 0]['amount'].sum())
    savings_rate = (monthly_income - monthly_expense) / monthly_income
    
    if savings_rate < 0.1:
        score -= 20
        issues.append("⚠️ 储蓄率过低 (<10%)")
    elif savings_rate < 0.2:
        score -= 10
        issues.append("⚡ 储蓄率偏低 (10-20%)")
    elif savings_rate >= 0.3:
        score += 10
        issues.append("✅ 储蓄率优秀 (>30%)")
    
    # 2. 消费结构
    categories = transactions[transactions['amount'] < 0].groupby('category')['amount'].sum()
    total_expense = abs(categories.sum())
    
    # 必要支出占比
    essential = abs(categories.get('居住', 0) + categories.get('餐饮', 0) + categories.get('交通', 0))
    essential_ratio = essential / total_expense if total_expense > 0 else 0
    
    if essential_ratio > 0.7:
        score -= 15
        issues.append("⚠️ 必要支出占比过高 (>70%)")
    
    # 3. 消费波动
    monthly_expenses = transactions[transactions['amount'] < 0].groupby(
        transactions['date'].dt.to_period('M')
    )['amount'].sum()
    
    cv = monthly_expenses.std() / abs(monthly_expenses.mean()) if len(monthly_expenses) > 1 else 0
    
    if cv > 0.5:
        score -= 10
        issues.append("⚠️ 消费波动较大")
    
    # 4. 应急储备
    emergency_months = savings / monthly_expense if monthly_expense > 0 else 0
    
    if emergency_months < 3:
        score -= 15
        issues.append("⚠️ 应急储备不足 (<3个月)")
    elif emergency_months >= 6:
        score += 10
        issues.append("✅ 应急储备充足 (>6个月)")
    
    # 评级
    if score >= 90:
        rating = "⭐⭐⭐⭐⭐ 优秀"
    elif score >= 75:
        rating = "⭐⭐⭐⭐ 良好"
    elif score >= 60:
        rating = "⭐⭐⭐ 一般"
    elif score >= 40:
        rating = "⭐⭐ 需改善"
    else:
        rating = "⭐ 警告"
    
    return {
        '评分': score,
        '评级': rating,
        '问题': issues,
        '建议': generate_savings_advice(issues)
    }
```

### 4. 储蓄建议

```python
def generate_savings_advice(issues):
    """生成储蓄建议"""
    advice = []
    
    for issue in issues:
        if '储蓄率' in issue:
            advice.append("💡 设置自动转账，工资到账后立即转出20%到储蓄账户")
            advice.append("💡 使用52周存钱法，每周递增存入金额")
        
        if '必要支出' in issue:
            advice.append("💡 考虑合租或搬到更便宜的住处")
            advice.append("💡 多做饭少点外卖，每月可节省500-1000元")
        
        if '消费波动' in issue:
            advice.append("💡 设置每月消费预算，使用信封法管理")
            advice.append("💡 大额消费前等待24小时冷静期")
        
        if '应急储备' in issue:
            advice.append("💡 优先建立3-6个月的应急基金")
            advice.append("💡 将应急资金存入货币基金，兼顾流动性和收益")
    
    return advice
```

### 5. 定期报表推送

```json
{
  "cron": {
    "jobs": [
      {
        "id": "monthly-report",
        "schedule": "0 9 1 * *",
        "prompt": "生成上月个人财务报表",
        "channel": "feishu"
      },
      {
        "id": "budget-alert",
        "schedule": "0 10 * * 1",
        "prompt": "检查本周预算执行情况",
        "channel": "feishu"
      }
    ]
  }
}
```

## CSV 格式要求

```csv
date,description,amount,account_number
2024-01-15,美团外卖,-35.50,****1234
2024-01-15,工资收入,15000.00,****1234
2024-01-16,滴滴出行,-25.00,****1234
```
