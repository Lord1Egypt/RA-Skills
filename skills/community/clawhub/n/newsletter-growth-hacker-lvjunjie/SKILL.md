---
name: newsletter-growth-hacker
description: |
  Newsletter 增长黑客工具。提供订阅者获取策略、内容优化、A/B 测试主题行生成、数据分析和增长预测。
  Use when: 需要增长 Newsletter 订阅者、优化邮件内容、设计 A/B 测试、分析邮件营销数据、追踪增长趋势
---

# Newsletter Growth Hacker

专业的邮件通讯（Newsletter）增长黑客工具，整合订阅者获取、内容优化、A/B 测试和数据分析四大核心功能。

## 快速开始

```bash
cd skills/newsletter-growth-hacker/scripts
python main.py
```

## 核心功能

### 1. 订阅者获取策略

提供 6 大类经过验证的订阅者获取策略：

| 策略 | 转化率 | 投入 | ROI |
|------|--------|------|-----|
| 内容升级策略 | 3-8% | 中等 | 高 |
| 社会证明策略 | 2-5% | 低 | 中高 |
| 推荐计划 | 15-25% | 高 | 非常高 |
| 交叉推广 | 5-12% | 中等 | 高 |
| SEO 引流磁铁 | 2-6% | 高（前期） | 长期非常高 |
| 付费广告 | 1-4% | 中等 | 取决于 CPC |

**使用场景**：
- 制定订阅者增长计划
- 选择适合预算和资源的获取渠道
- 预测不同策略的增长效果

**示例**：
```python
from subscriber_acquisition import SubscriberAcquisition

acquisition = SubscriberAcquisition()

# 获取所有策略
strategies = acquisition.get_strategies()

# 计算增长预测
projection = acquisition.calculate_projection(
    current_subscribers=1000,
    strategy="referral_program",
    months=6
)
# 输出：6 个月后订阅者数量、总增长、月增长率
```

### 2. 内容优化建议

基于邮件营销最佳实践的内容分析和优化建议。

**分析维度**：
- 内容长度和段落结构
- 可读性评分
- 主题行检测
- CTA（行动号召）检测
- 移动友好度

**优化原则**：
1. **价值先行** - 开篇展示核心价值
2. **可扫描性** - 小标题、短段落、列表
3. **个性化** - 细分受众、个人故事
4. **行动导向** - 单一清晰 CTA
5. **移动优先** - 单栏布局、大字体

**使用场景**：
- 发送前检查邮件内容
- 优化现有邮件模板
- 学习邮件写作最佳实践

**示例**：
```python
from content_optimizer import ContentOptimizer

optimizer = ContentOptimizer()

content = """
【主题行】

正文内容...

行动号召...
"""

analysis = optimizer.analyze_content(content)
# 输出：字数、段落数、可读性评分、优化建议
```

### 3. A/B 测试主题行生成

生成多种风格的 A/B 测试主题行，包含性能预测。

**主题行风格**：
- **好奇型** - 制造信息缺口
- **紧迫型** - 限时限量
- **利益型** - 强调好处
- **社会证明型** - 展示人数/权威
- **提问型** - 引发思考
- **列表型** - 数字清单
- **故事型** - 叙述经历

**性能预测基准**：
| 风格 | 预测打开率 | 预测点击率 |
|------|------------|------------|
| 好奇型 | 22-28% | 3-5% |
| 紧迫型 | 25-35% | 4-7% |
| 利益型 | 20-26% | 5-8% |
| 社会证明型 | 23-29% | 4-6% |
| 提问型 | 21-27% | 3-5% |
| 列表型 | 24-30% | 4-7% |
| 故事型 | 22-28% | 5-9% |

**A/B 测试最佳实践**：
- 样本量：至少 1000 订阅者/变体
- 测试时长：24-48 小时
- 成功指标：打开率
- 次要指标：点击率

**示例**：
```python
from content_optimizer import SubjectLineGenerator

generator = SubjectLineGenerator()

# 生成 A/B 测试方案
ab_test = generator.create_ab_test(
    topic="邮件营销",
    goal="提升打开率",
    variants=3
)

# 输出：3 个不同风格的主题行变体 + 测试设置
```

### 4. 数据分析与报告

全面的邮件营销指标分析和洞察生成。

**核心指标**：
- 送达率（Delivery Rate）
- 打开率（Open Rate）
- 点击率（Click Rate）
- 点开比（Click-to-Open Rate）
- 退订率（Unsubscribe Rate）
- 退回率（Bounce Rate）
- 垃圾邮件投诉率（Spam Rate）

**行业基准**：
| 指标 | 差 | 平均 | 好 | 优秀 |
|------|----|----|----|----|
| 打开率 | <15% | 21% | 25% | 30%+ |
| 点击率 | <2% | 3.5% | 5% | 7%+ |
| 点开比 | <10% | 15% | 20% | 25%+ |
| 退订率 | >1% | 0.5% | 0.3% | <0.1% |
| 退回率 | >5% | 2% | 1% | <0.5% |

**自动洞察**：
- 指标评级（优秀/好/平均/差）
- 问题诊断和建议
- 历史数据对比
- 行动项优先级排序

**示例**：
```python
from analytics_engine import AnalyticsEngine, NewsletterMetrics

engine = AnalyticsEngine()

metrics = NewsletterMetrics(
    sent=10000,
    delivered=9850,
    opened=2462,
    clicked=493,
    unsubscribed=15,
    bounced=150,
    spam_complaints=5
)

report = engine.create_report(
    campaign_name="月度通讯",
    metrics=metrics
)
# 输出：完整报告 + 洞察 + 行动项
```

### 5. 增长追踪与预测

追踪订阅者增长趋势，预测未来增长。

**功能**：
- 按月追踪新增/流失订阅者
- 计算净增长和增长率
- 分析订阅来源分布
- 识别最佳/最差周期
- 基于历史数据预测未来

**预测模型**：
使用最近 3 期数据计算平均增长率，进行线性预测。

**示例**：
```python
from analytics_engine import GrowthTracker

tracker = GrowthTracker()

# 添加历史数据
tracker.add_period("2026-01", 5000, 320, 45, {"organic": 150, "referral": 100, "paid": 70})
tracker.add_period("2026-02", 5275, 380, 52, {"organic": 180, "referral": 120, "paid": 80})
tracker.add_period("2026-03", 5603, 410, 48, {"organic": 200, "referral": 130, "paid": 80})

# 获取增长摘要
summary = tracker.get_growth_summary()

# 预测未来 6 个月
projections = tracker.project_growth(6)
```

## 完整工作流

### 场景 1：新 Newsletter 冷启动

```
1. 使用「订阅者获取策略」选择 2-3 个低成本高 ROI 渠道
2. 设置增长目标和时间线
3. 使用「内容优化」确保首封邮件质量
4. 生成 5-7 个主题行进行 A/B 测试
5. 发送后使用「数据分析」评估表现
6. 根据洞察优化下一期
```

### 场景 2：提升现有 Newsletter 表现

```
1. 使用「数据分析」诊断当前问题
2. 根据洞察优先级执行优化
3. 使用「A/B 测试」持续优化主题行
4. 使用「内容优化」改进邮件结构
5. 使用「增长追踪」监控改进效果
```

### 场景 3：制定季度增长计划

```
1. 分析历史增长数据
2. 选择主要获取策略组合
3. 设定月度增长目标
4. 规划内容和发送频率
5. 设置 A/B 测试计划
6. 定义成功指标和检查点
```

## 行业基准参考

### 按行业划分的打开率基准

| 行业 | 平均 | 好 | 优秀 |
|------|------|----|----|
| 科技 | 21.5% | 25% | 30% |
| 金融 | 23.0% | 27% | 32% |
| 健康 | 19.0% | 23% | 28% |
| 营销 | 22.0% | 26% | 31% |
| 教育 | 24.0% | 28% | 33% |
| 电商 | 18.0% | 22% | 27% |

### 最佳发送时间

- **B2B**：周二至周四，上午 10-11 点
- **B2C**：周末，下午 2-4 点
- **全球受众**：根据时区分段发送

### 最佳发送频率

- **每日**：适合新闻类、高价值内容
- **每周**：最常见，平衡价值和频率
- **每两周**：适合深度内容
- **每月**：适合汇总类、高价值报告

## 脚本说明

| 脚本 | 功能 |
|------|------|
| `main.py` | 主入口，交互式菜单 |
| `subscriber_acquisition.py` | 订阅者获取策略引擎 |
| `content_optimizer.py` | 内容分析和主题行生成 |
| `analytics_engine.py` | 数据分析和增长追踪 |

## 集成示例

### 与邮件服务平台集成

```python
# 从 ESP 导出数据后分析
import csv
from analytics_engine import AnalyticsEngine, NewsletterMetrics

# 读取 CSV 数据
with open('campaign_data.csv') as f:
    reader = csv.DictReader(f)
    data = next(reader)

metrics = NewsletterMetrics(
    sent=int(data['Sent']),
    delivered=int(data['Delivered']),
    opened=int(data['Opened']),
    clicked=int(data['Clicked']),
    unsubscribed=int(data['Unsubscribed']),
    bounced=int(data['Bounced']),
    spam_complaints=int(data['Spam Complaints'])
)

# 生成报告
engine = AnalyticsEngine()
report = engine.create_report("活动名称", metrics)
print(report)
```

### 自动化报告

```python
# 定期生成报告并保存
import json
from datetime import datetime
from analytics_engine import AnalyticsEngine

# ... 获取数据 ...

report = engine.create_report("月度报告", metrics)

# 保存为 JSON
with open(f"report_{datetime.now().strftime('%Y%m')}.json", 'w') as f:
    json.dump(report, f, indent=2, ensure_ascii=False)
```

## 定价与商业模式

本技能定位为专业邮件营销工具，建议定价 **$49/月**，目标用户：

- Newsletter 创作者
- 内容营销人员
- 独立开发者
- 小型企业营销负责人

**价值主张**：
- 节省策略研究时间
- 基于数据的决策
- 系统化增长方法
- 持续优化框架

**预期收益**：
- 保守估计：40 订阅者 × $49 = $1,960/月
- 中等估计：80 订阅者 × $49 = $3,920/月
- 乐观估计：120 订阅者 × $49 = $5,880/月

## 更新日志

### v1.0.0 (2026-03-15)
- 初始版本发布
- 订阅者获取策略（6 大类）
- 内容优化分析引擎
- A/B 测试主题行生成器（7 种风格）
- 数据分析与报告系统
- 增长追踪与预测

## 相关资源

- 邮件营销最佳实践：`references/email_marketing_best_practices.md`
- 主题行模板库：`references/subject_line_templates.md`
- 行业基准数据：`references/industry_benchmarks.md`
