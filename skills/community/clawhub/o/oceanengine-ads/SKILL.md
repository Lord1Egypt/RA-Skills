---
name: oceanengine-ads
display_name: 巨量广告自动化投放
version: 1.0.0
tags: [oceanengine, advertising, tiktok, bytedance, automation]
license: MIT
license_url: https://opensource.org/licenses/MIT
---

# 巨量广告自动化投放 — LemClaw Skills

## Description

🎯 **乐盟互动出品** - 全功能集成巨量广告（Ocean Engine Ads）API，支持巨量引擎、巨量千川、穿山甲广告。包含自动化投放、智能优化、实时监控功能。

## 🌟 特色功能

### 🔥 自动化投放
- **智能投放计划**：基于历史数据的智能投放策略
- **预算自动分配**：根据ROI自动调整各计划预算
- **出价策略优化**：实时调整出价，最大化转化效果
- **创意自动轮换**：A/B测试和智能创意替换

### 📊 实时监控
- **实时数据监控**：监控曝光、点击、转化等关键指标
- **异常检测**：自动识别广告异常行为
- **实时告警**：关键指标异常时立即通知
- **趋势分析**：AI驱动的数据趋势分析

### 🤖 智能优化
- **ROI优化算法**：基于机器学习的ROI最大化
- **预算重分配**：自动调整高ROI计划的预算
- **定向优化**：智能调整受众定向参数
- **出价建议**：实时提供最优出价建议

## Setup

### Environment Variables

```bash
# 必需配置
OCEANENGINE_ACCESS_TOKEN=your_test_token
OCEANENGINE_APP_ID=your_app_id
OCEANENGINE_APP_SECRET=your_app_secret

# 可选配置
OCEANENGINE_ACCOUNT_ID=your_account_id  # 用于测试账户
OCEANENGINE_TEST_MODE=true              # 启用测试模式
```

### 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置环境变量
export OCEANENGINE_ACCESS_TOKEN="your_token"

# 3. 测试连接
python3 -c "from oceanengine import OceanEngine; oe = OceanEngine(); print('连接成功:', oe.status())"

# 4. 开始自动化投放
python3 -m oceanengine --mode auto-launch
```

## 🎯 自动化投放模式

### 1. 智能投放模式
```python
from oceanengine import OceanEngine

oe = OceanEngine()

# 启动智能投放
oe.auto_launch(
    campaign_name="智能投放测试",
    objective="CONVERSIONS",
    daily_budget=10000,  # 100元
    start_immediately=True,
    optimization="ROI"
)
```

### 2. 预算优化模式
```python
# 自动预算重分配
oe.auto_budget_optimization(
    budget_increase_threshold=1.5,  # ROI > 1.5 时增加预算
    budget_decrease_threshold=0.8,  # ROI < 0.8 时减少预算
    budget_change_percent=20        # 每次调整20%
)
```

### 3. 创意自动测试
```python
# A/B测试不同创意
oe.creative_ab_test(
    test_duration=3,           # 测试3天
    metrics=["ctr", "cpc", "conversion"],
    winner_threshold=0.1       # 胜者必须领先10%才应用
)
```

## 📈 智能优化功能

### ROI 最大化
```python
# 启动ROI优化
oe.optimize_for_roi(
    target_roi=2.0,            # 目标ROI 200%
    max_budget_increase=50,    # 单日最大预算增幅50%
    min_budget=1000            # 最小日预算10元
)
```

### 实时监控
```python
# 实时监控广告表现
oe.real_time_monitor(
    metrics=["impressions", "clicks", "cost"],
    thresholds={
        "cost_increase": 1.5,  # 成本增加50%告警
        "ctr_drop": 0.5,      # 点击率下降50%告警
    }
)
```

### 智能出价
```python
# 智能出价调整
oe.smart_bidding(
    strategy="MAX_ROAS",       # 最大化ROAS
    learning_period=7,         # 学习期7天
    bid_adjustment_limit=0.3   # 出价调整限制±30%
)
```

## 📊 数据分析功能

### 智能报表
```python
# 生成智能分析报表
report = oe.generate_smart_report(
    period="last_7d",
    analysis_depth="comprehensive",
    include_recommendations=True
)

print(f"总体ROI: {report['roi']:.2f}")
print(f"优化建议: {report['recommendations']}")
```

### 竞品分析
```python
# 分析竞争对手广告
competitor_analysis = oe.analyze_competitors(
    industry="科技",
    region="北京"
)
```

## 🛠️ 使用示例

### 基础使用
```python
from oceanengine import OceanEngine

# 初始化
oe = OceanEngine()

# 查询账户信息
account_info = oe.get_account_info()

# 创建广告计划
campaign = oe.create_campaign(
    campaign_name="测试广告",
    objective="CONVERSIONS",
    daily_budget=10000
)

# 启动自动化
oe.start_auto_monitoring(campaign_id=campaign['id'])
```

### 高级自动化
```python
# 启动完整自动化流程
oe.start_full_automation(
    campaign_config={
        "name": "全自动化测试",
        "objective": "CONVERSIONS",
        "daily_budget": 20000
    },
    automation_rules={
        "budget_optimization": True,
        "creative_testing": True,
        "targeting_optimization": True,
        "real_time_monitoring": True
    }
)
```

## 🔧 配置说明

### 自动化规则
```python
automation_rules = {
    # 预算优化规则
    "budget_rules": {
        "enable": True,
        "roi_threshold": 1.5,
        "budget_change_percent": 20,
        "min_daily_budget": 1000
    },
    
    # 创意测试规则
    "creative_rules": {
        "enable": True,
        "test_duration": 3,
        "winner_threshold": 0.1,
        "max_variants": 5
    },
    
    # 出价策略
    "bidding_rules": {
        "strategy": "TARGET_ROAS",
        "target_roas": 2.0,
        "bid_adjustment_limit": 0.3
    }
}
```

## 📊 监控告警

### 关键指标告警
- **成本异常告警**：成本突然增加>50%
- **ROI下降告警**：ROI<1.0
- **CTR异常告警**：点击率变化>30%
- **转化率异常告警**：转化率下降>40%

### 实时通知
```python
# 配置实时通知
oe.setup_real_time_alerts(
    email="your_email@example.com",
    webhook="https://your-webhook-url.com",
    alert_types=["cost_alert", "roi_alert", "ctr_alert"]
)
```

## 🤖 使用说明

### 新手入门
1. 配置环境变量
2. 启用测试模式
3. 运行示例代码
4. 查看实时数据

### 高级使用
1. 自定义自动化规则
2. 配置多账户管理
3. 设置复杂预算策略
4. 使用高级分析功能

## 💰 费用说明

**注**：本技能由乐盟互动提供技术支持，**使用需按月付费**。具体价格请联系乐盟互动获取。

## 📞 支持与联系

- **技术支持**：aoqian@lemhd.cn
- **商务合作**：mast@lemhd.cn
- **官网**：http://www.lemeng123.com

## ⚠️ 重要提醒

1. **测试模式**：首次使用请开启测试模式
2. **预算控制**：设置合理的预算上限
3. **监控设置**：配置好监控告警
4. **数据安全**：妥善保存API密钥

## 🔄 更新日志

### v1.0.0 (2026-03-09)
- ✅ 初始版本发布
- ✅ 基础广告管理功能
- ✅ 智能投放自动化
- ✅ 实时监控告警
- ✅ ROI优化算法
- ✅ 创意A/B测试
- ✅ 乐盟互动商标植入
- ✅ 按月付费模式标注

---

**© 2026 乐盟互动 LemClaw | 按月付费使用**

🎯 LemClaw Smart Advertising Platform - 让广告投放更智能！