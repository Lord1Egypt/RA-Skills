# 📋 任务生成规则系统 (Task Generation Rules)

**版本**：V1.0  
**创建日期**：2026-04-11  
**最后更新**：2026-04-11  
**大小**：17.4KB

---

## 一、概述

任务生成规则系统是 Investment Buddy 的**行为引擎**，包含 8 大触发规则 + 5 类任务的任务生成逻辑。

### 1.1 设计目标

- 🎯 **精准触发**：在合适的时机触发合适的任务
- 🤖 **自动化**：减少人工干预，系统自动运行
- 📊 **可量化**：每个规则有明确的触发条件
- 🔄 **可迭代**：基于反馈持续优化

### 1.2 系统架构

```
┌─────────────────────────────────────────────────┐
│              任务生成规则系统                      │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌─────────────┐    ┌─────────────┐            │
│  │  触发规则层  │ →  │  任务生成层  │            │
│  │  (8 大规则)  │    │  (5 类任务)  │            │
│  └─────────────┘    └─────────────┘            │
│         ↓                    ↓                  │
│  ┌─────────────┐    ┌─────────────┐            │
│  │  条件评估器  │ →  │  宠物过滤器  │            │
│  └─────────────┘    └─────────────┘            │
│                              ↓                  │
│                    ┌─────────────┐              │
│                    │  任务执行器  │              │
│                    └─────────────┘              │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 二、8 大触发规则

### 2.1 规则 1：市场波动触发 (Market Volatility Trigger)

**规则 ID**：R001

**触发条件**：
```python
{
    "condition": "market_change_percent >= threshold",
    "threshold": {
        "high_volatility": 3.0,    # 大幅波动
        "extreme_volatility": 5.0  # 极端波动
    },
    "time_window": "1d",  # 1 日内
    "market_indices": ["shanghai", "shenzhen", "chinext"]
}
```

**触发频率**：实时监测，每日最多触发 3 次

**生成任务**：
| 宠物类型 | 任务类型 | 优先级 |
|---------|---------|--------|
| 价值型（🐿️🐢🦉） | 风险提醒 | P0 |
| 趋势型（🐺🐎🦅） | 机会分析 | P0 |
| 情绪型（🐬🦊） | 情绪安抚 | P0 |
| 防御型（🐻🐘） | 配置检查 | P1 |
| 逆向型（🐪🦄） | 逆向机会 | P1 |

**任务示例**：
```json
{
    "task_id": "T001_20260411_001",
    "rule_id": "R001",
    "trigger_time": "2026-04-11T10:30:00+08:00",
    "trigger_data": {
        "market_index": "shanghai",
        "change_percent": -3.5,
        "volume_change": 1.8
    },
    "target_users": "all_active_users",
    "pet_filter": {
        "proactivity_level": ">=50",
        "intervention_threshold": "<=60"
    },
    "task_type": "risk_alert",
    "template_vars": {
        "market_change": -3.5,
        "market_index": "上证指数"
    },
    "priority": "P0",
    "status": "pending"
}
```

---

### 2.2 规则 2：估值极端触发 (Valuation Extreme Trigger)

**规则 ID**：R002

**触发条件**：
```python
{
    "condition": "valuation_percentile <= 20 OR valuation_percentile >= 80",
    "metrics": ["PE", "PB", "PS"],
    "scope": ["individual_stock", "industry", "market"],
    "time_window": "1d"
}
```

**触发场景**：
- 个股估值历史分位<20%（低估）
- 个股估值历史分位>80%（高估）
- 行业估值历史分位<20%（低估）
- 行业估值历史分位>80%（高估）
- 全市场估值历史分位<20%（低估）
- 全市场估值历史分位>80%（高估）

**生成任务**：
| 估值状态 | 宠物类型 | 任务类型 | 话术重点 |
|---------|---------|---------|---------|
| 低估 (<20%) | 🐿️🐺🦄 | 机会提示 | "好价格出现了" |
| 高估 (>80%) | 🐿️🐻🐪 | 风险提醒 | "安全边际不足" |
| 正常 (20-80%) | - | 不触发 | - |

**任务示例**：
```json
{
    "task_id": "T002_20260411_001",
    "rule_id": "R002",
    "trigger_time": "2026-04-11T15:00:00+08:00",
    "trigger_data": {
        "stock_code": "000001",
        "stock_name": "平安银行",
        "metric": "PE",
        "current_value": 4.5,
        "percentile": 15.2,
        "historical_median": 7.8
    },
    "target_users": "users_holding_000001",
    "pet_filter": {
        "expertise": ["valuation"]
    },
    "task_type": "opportunity_alert",
    "template_vars": {
        "stock_name": "平安银行",
        "pe_ratio": 4.5,
        "pe_percentile": 15.2,
        "margin_of_safety": 42.3
    },
    "priority": "P0",
    "status": "pending"
}
```

---

### 2.3 规则 3：用户行为异常触发 (User Behavior Anomaly Trigger)

**规则 ID**：R003

**触发条件**：
```python
{
    "anomaly_types": [
        {
            "name": "frequent_trading",
            "condition": "trade_count_last_7d >= 5",
            "description": "频繁交易"
        },
        {
            "name": "chase_rise",
            "condition": "buy_after_rise_percent >= 5",
            "description": "追涨"
        },
        {
            "name": "kill_fall",
            "condition": "sell_after_fall_percent >= 5",
            "description": "杀跌"
        },
        {
            "name": "position_too_high",
            "condition": "position_ratio >= 0.9",
            "description": "仓位过高"
        },
        {
            "name": "no_diversification",
            "condition": "max_single_stock_ratio >= 0.3",
            "description": "集中度过高"
        }
    ]
}
```

**生成任务**：
| 异常类型 | 宠物类型 | 任务类型 | 干预强度 |
|---------|---------|---------|---------|
| 频繁交易 | 🐢🐬 | 心态提醒 | 中 |
| 追涨 | 🐿️🐻 | 风险提醒 | 高 |
| 杀跌 | 🐬🐢 | 情绪安抚 | 高 |
| 仓位过高 | 🐻🐘 | 配置建议 | 高 |
| 集中度高 | 🐘🦉 | 分散建议 | 中 |

**任务示例**：
```json
{
    "task_id": "T003_20260411_001",
    "rule_id": "R003",
    "trigger_time": "2026-04-11T14:30:00+08:00",
    "trigger_data": {
        "user_id": "user_12345",
        "anomaly_type": "frequent_trading",
        "trade_count_7d": 8,
        "threshold": 5
    },
    "target_users": ["user_12345"],
    "pet_filter": {
        "pet_id": ["manman_001", "paopao_001"]
    },
    "task_type": "behavior_reminder",
    "template_vars": {
        "trade_count": 8,
        "suggested_max": 2
    },
    "priority": "P0",
    "status": "pending"
}
```

---

### 2.4 规则 4：持仓风险触发 (Holding Risk Trigger)

**规则 ID**：R004

**触发条件**：
```python
{
    "risk_metrics": [
        {
            "name": "max_drawdown",
            "condition": "drawdown_percent >= threshold",
            "threshold": {
                "warning": 10,
                "alert": 20,
                "critical": 30
            }
        },
        {
            "name": "single_stock_loss",
            "condition": "loss_amount >= threshold",
            "threshold": {
                "warning": 5000,
                "alert": 20000,
                "critical": 50000
            }
        },
        {
            "name": "risk_score_increase",
            "condition": "risk_score_change >= 20",
            "time_window": "7d"
        }
    ]
}
```

**生成任务**：
| 风险等级 | 宠物类型 | 任务类型 | 干预方式 |
|---------|---------|---------|---------|
| 警告 (10%) | 🐿️🐢 | 温和提醒 | 消息通知 |
| 警示 (20%) | 🐻🦉 | 风险建议 | 消息 + 弹窗 |
| 严重 (30%) | 🐻🐬🐘 | 紧急干预 | 消息 + 弹窗 + 电话 |

**任务示例**：
```json
{
    "task_id": "T004_20260411_001",
    "rule_id": "R004",
    "trigger_time": "2026-04-11T11:00:00+08:00",
    "trigger_data": {
        "user_id": "user_12345",
        "risk_type": "max_drawdown",
        "drawdown_percent": 22.5,
        "risk_level": "alert"
    },
    "target_users": ["user_12345"],
    "pet_filter": {
        "pet_id": ["ashou_001", "dashan_001"]
    },
    "task_type": "risk_intervention",
    "template_vars": {
        "drawdown_percent": 22.5,
        "suggested_action": "减仓 20%"
    },
    "priority": "P0",
    "status": "pending"
}
```

---

### 2.5 规则 5：市场情绪触发 (Market Sentiment Trigger)

**规则 ID**：R005

**触发条件**：
```python
{
    "sentiment_indicators": [
        {
            "name": "fear_greed_index",
            "condition": "index <= 20 OR index >= 80",
            "description": "恐惧贪婪指数"
        },
        {
            "name": "put_call_ratio",
            "condition": "ratio >= 1.5 OR ratio <= 0.5",
            "description": "Put/Call 比率"
        },
        {
            "name": "margin_balance",
            "condition": "change_percent >= 10",
            "description": "融资余额变化"
        },
        {
            "name": "northbound_flow",
            "condition": "net_flow >= 10B OR net_flow <= -10B",
            "description": "北向资金"
        }
    ]
}
```

**生成任务**：
| 情绪状态 | 宠物类型 | 任务类型 | 话术策略 |
|---------|---------|---------|---------|
| 极度恐惧 | 🐬🐪 | 逆向机会 | "别人恐惧我贪婪" |
| 极度贪婪 | 🐿️🐻 | 风险提醒 | "别人贪婪我恐惧" |
| 资金大幅流入 | 🐺🐎 | 趋势确认 | "资金正在进场" |
| 资金大幅流出 | 🐻🐘 | 防御建议 | "现金为王" |

---

### 2.6 规则 6：时间节点触发 (Time-based Trigger)

**规则 ID**：R006

**触发条件**：
```python
{
    "time_triggers": [
        {
            "name": "market_open",
            "schedule": "0 9 * * 1-5",  # 交易日 9:00
            "description": "开盘问候"
        },
        {
            "name": "market_close",
            "schedule": "0 15 * * 1-5",  # 交易日 15:00
            "description": "收盘总结"
        },
        {
            "name": "weekly_review",
            "schedule": "0 18 * * 5",  # 周五 18:00
            "description": "周度复盘"
        },
        {
            "name": "monthly_review",
            "schedule": "0 20 L * *",  # 月末 20:00
            "description": "月度复盘"
        },
        {
            "name": "user_inactive",
            "condition": "last_login_days >= 3",
            "description": "用户未登录"
        }
    ]
}
```

**生成任务**：
| 时间触发 | 宠物类型 | 任务类型 | 内容 |
|---------|---------|---------|------|
| 开盘问候 | 🐎🦅 | 市场前瞻 | 今日关注 |
| 收盘总结 | 🦉🐘 | 市场回顾 | 今日复盘 |
| 周度复盘 | 🦉🐢 | 周度总结 | 本周表现 |
| 月度复盘 | 🦅🐘 | 月度总结 | 月度表现 |
| 用户未登录 | 🐬🐿️ | 关怀提醒 | 好久不见 |

---

### 2.7 规则 7：宠物成长触发 (Pet Growth Trigger)

**规则 ID**：R007

**触发条件**：
```python
{
    "growth_events": [
        {
            "name": "pet_level_up",
            "condition": "pet_level_change >= 1",
            "description": "宠物升级"
        },
        {
            "name": "milestone_reached",
            "condition": "interaction_count IN [10, 50, 100, 500, 1000]",
            "description": "里程碑达成"
        },
        {
            "name": "achievement_unlocked",
            "condition": "achievement_id IS NOT NULL",
            "description": "成就解锁"
        }
    ]
}
```

**生成任务**：
| 成长事件 | 宠物类型 | 任务类型 | 奖励 |
|---------|---------|---------|------|
| 宠物升级 | 当前宠物 | 升级庆祝 | 解锁新能力 |
| 里程碑 | 当前宠物 | 里程碑庆祝 | 特殊对话 |
| 成就解锁 | 当前宠物 | 成就通知 | 成就徽章 |

---

### 2.8 规则 8：外部事件触发 (External Event Trigger)

**规则 ID**：R008

**触发条件**：
```python
{
    "external_events": [
        {
            "name": "policy_announcement",
            "source": "gov_website",
            "keywords": ["降准", "降息", "刺激政策"],
            "description": "政策发布"
        },
        {
            "name": "earnings_surprise",
            "source": "stock_announcement",
            "condition": "earnings_surprise_percent >= 30",
            "description": "业绩超预期"
        },
        {
            "name": "industry_news",
            "source": "news_api",
            "keywords": ["行业利好", "技术突破", "政策扶持"],
            "description": "行业重大新闻"
        },
        {
            "name": "black_swan",
            "source": "news_api",
            "keywords": ["黑天鹅", "突发事件", "重大风险"],
            "description": "黑天鹅事件"
        }
    ]
}
```

**生成任务**：
| 外部事件 | 宠物类型 | 任务类型 | 响应速度 |
|---------|---------|---------|---------|
| 政策发布 | 🦅🐎 | 政策解读 | 30 分钟内 |
| 业绩超预期 | 🦉🐺 | 个股分析 | 1 小时内 |
| 行业利好 | 🐎🦄 | 机会提示 | 1 小时内 |
| 黑天鹅 | 🐻🐬 | 紧急提醒 | 15 分钟内 |

---

## 三、5 类任务

### 3.1 任务类型 A：信息推送 (Information Push)

**任务 ID 前缀**：T-A

**任务特征**：
- 单向推送，无需用户响应
- 优先级：P1-P2
- 频率限制：每日最多 5 条/用户

**任务模板**：
```json
{
    "task_id": "T-A-{timestamp}-{seq}",
    "task_type": "information_push",
    "content": {
        "title": "{title}",
        "body": "{body}",
        "pet_id": "{pet_id}",
        "template_id": "{template_id}"
    },
    "target": {
        "user_ids": ["{user_id}"],
        "segment": "{user_segment}"
    },
    "delivery": {
        "channel": ["in_app", "push"],
        "schedule": "immediate",
        "priority": "P1"
    }
}
```

**适用场景**：
- 市场日报
- 行业资讯
- 宠物日常问候
- 知识分享

---

### 3.2 任务类型 B：风险提醒 (Risk Alert)

**任务 ID 前缀**：T-B

**任务特征**：
- 需要用户确认
- 优先级：P0
- 频率限制：无限制（风险无上限）

**任务模板**：
```json
{
    "task_id": "T-B-{timestamp}-{seq}",
    "task_type": "risk_alert",
    "content": {
        "title": "⚠️ 风险提醒",
        "body": "{risk_message}",
        "pet_id": "{pet_id}",
        "risk_level": "{risk_level}",
        "suggested_action": "{action}"
    },
    "target": {
        "user_ids": ["{user_id}"]
    },
    "delivery": {
        "channel": ["in_app", "push", "sms"],
        "schedule": "immediate",
        "priority": "P0"
    },
    "action_required": {
        "type": "confirmation",
        "options": ["知道了", "查看详情", "立即操作"],
        "timeout": "24h"
    }
}
```

**适用场景**：
- 市场大幅波动
- 持仓风险过高
- 用户行为异常
- 估值极端

---

### 3.3 任务类型 C：机会提示 (Opportunity Alert)

**任务 ID 前缀**：T-C

**任务特征**：
- 建议性质，无需强制响应
- 优先级：P0-P1
- 频率限制：每日最多 3 条/用户

**任务模板**：
```json
{
    "task_id": "T-C-{timestamp}-{seq}",
    "task_type": "opportunity_alert",
    "content": {
        "title": "💡 机会提示",
        "body": "{opportunity_message}",
        "pet_id": "{pet_id}",
        "opportunity_type": "{type}",
        "confidence": "{confidence}%"
    },
    "target": {
        "user_ids": ["{user_id}"]
    },
    "delivery": {
        "channel": ["in_app", "push"],
        "schedule": "immediate",
        "priority": "P0"
    },
    "action_required": {
        "type": "optional",
        "options": ["查看详情", "加入自选", "忽略"]
    }
}
```

**适用场景**：
- 估值低估
- 趋势形成
- 行业景气
- 政策利好

---

### 3.4 任务类型 D：互动任务 (Interaction Task)

**任务 ID 前缀**：T-D

**任务特征**：
- 需要用户参与
- 优先级：P1-P2
- 频率限制：每周最多 5 条/用户

**任务模板**：
```json
{
    "task_id": "T-D-{timestamp}-{seq}",
    "task_type": "interaction_task",
    "content": {
        "title": "{title}",
        "body": "{question}",
        "pet_id": "{pet_id}",
        "interaction_type": "{type}"
    },
    "target": {
        "user_ids": ["{user_id}"]
    },
    "delivery": {
        "channel": ["in_app"],
        "schedule": "immediate",
        "priority": "P1"
    },
    "action_required": {
        "type": "response",
        "options": ["{option_1}", "{option_2}", "{option_3}"],
        "timeout": "7d"
    },
    "reward": {
        "type": "pet_exp",
        "amount": 10
    }
}
```

**适用场景**：
- 投资性格评估
- 用户反馈收集
- 知识问答
- 宠物互动

---

### 3.5 任务类型 E：执行建议 (Action Recommendation)

**任务 ID 前缀**：T-E

**任务特征**：
- 具体操作建议
- 优先级：P0-P1
- 频率限制：每日最多 2 条/用户

**任务模板**：
```json
{
    "task_id": "T-E-{timestamp}-{seq}",
    "task_type": "action_recommendation",
    "content": {
        "title": "📝 操作建议",
        "body": "{recommendation}",
        "pet_id": "{pet_id}",
        "action_type": "{action_type}",
        "confidence": "{confidence}%",
        "reasoning": "{reasoning}"
    },
    "target": {
        "user_ids": ["{user_id}"]
    },
    "delivery": {
        "channel": ["in_app", "push"],
        "schedule": "immediate",
        "priority": "P0"
    },
    "action_required": {
        "type": "decision",
        "options": ["执行", "暂缓", "拒绝"],
        "timeout": "48h"
    },
    "tracking": {
        "track_adoption": true,
        "track_outcome": true
    }
}
```

**适用场景**：
- 调仓建议
- 再平衡建议
- 止损/止盈建议
- 定投建议

---

## 四、宠物过滤机制

### 4.1 过滤规则

```python
class PetFilter:
    def filter_pets(self, task, user_pets):
        """过滤出适合执行任务的宠物"""
        
        eligible_pets = []
        
        for pet in user_pets:
            # 检查宠物主动性
            if pet.proactivity_level < task.min_proactivity:
                continue
            
            # 检查宠物专长
            if task.required_expertise:
                if task.required_expertise not in pet.expertise:
                    continue
            
            # 检查干预阈值
            if task.intervention_threshold:
                if pet.intervention_threshold > task.intervention_threshold:
                    continue
            
            # 检查宠物状态
            if pet.status != 'active':
                continue
            
            eligible_pets.append(pet)
        
        return eligible_pets
```

### 4.2 宠物选择策略

| 策略 | 说明 | 适用场景 |
|------|------|---------|
| 单一宠物 | 选择最匹配的 1 只 | 日常任务 |
| 多宠物轮询 | 多只宠物轮流执行 | 避免单一宠物过度活跃 |
| 宠物辩论 | 多只宠物给出不同观点 | 复杂决策 |
| 宠物协作 | 多只宠物共同完成任务 | 综合分析 |

---

## 五、任务优先级系统

### 5.1 优先级定义

| 优先级 | 代码 | 响应时间 | 通知方式 | 示例 |
|--------|------|---------|---------|------|
| P0 | critical | 即时 | 推送 + 短信 + 弹窗 | 重大风险 |
| P1 | high | 5 分钟内 | 推送 + 弹窗 | 机会提示 |
| P2 | normal | 30 分钟内 | 推送 | 日常信息 |
| P3 | low | 2 小时内 | 应用内 | 宠物互动 |

### 5.2 优先级调整规则

```python
class PriorityAdjuster:
    def adjust_priority(self, task, context):
        """根据上下文调整任务优先级"""
        
        base_priority = task.base_priority
        
        # 用户风险评分高 → 提升优先级
        if context.user_risk_score > 70:
            base_priority = max(base_priority - 1, 0)
        
        # 市场波动大 → 提升优先级
        if context.market_volatility > 3.0:
            base_priority = max(base_priority - 1, 0)
        
        # 用户近期活跃 → 降低优先级
        if context.user_active_days >= 7:
            base_priority = min(base_priority + 1, 3)
        
        return base_priority
```

---

## 六、任务执行流程

### 6.1 完整流程

```
触发条件满足
    ↓
规则评估器 → 不满足 → 结束
    ↓ 满足
任务生成器
    ↓
宠物过滤器 → 无合适宠物 → 任务挂起
    ↓ 有合适宠物
优先级排序
    ↓
任务队列
    ↓
任务执行器
    ↓
结果追踪
    ↓
反馈学习
```

### 6.2 执行代码框架

```python
class TaskExecutionEngine:
    def execute_task(self, task):
        """执行任务"""
        
        # 1. 获取宠物
        pet = self.get_pet(task.pet_id)
        
        # 2. 填充模板
        content = self.fill_template(
            task.template_id,
            task.template_vars,
            pet
        )
        
        # 3. 发送消息
        result = self.send_message(
            user_id=task.target.user_id,
            content=content,
            channel=task.delivery.channel,
            priority=task.delivery.priority
        )
        
        # 4. 记录结果
        self.log_execution(task, result)
        
        # 5. 追踪反馈
        if task.action_required:
            self.track_user_response(task)
        
        return result
```

---

## 七、任务效果评估

### 7.1 评估指标

| 指标 | 定义 | 目标值 |
|------|------|--------|
| 触达率 | 成功送达/总任务数 | >95% |
| 阅读率 | 用户阅读/触达数 | >70% |
| 互动率 | 用户互动/阅读数 | >30% |
| 采纳率 | 用户采纳建议/互动数 | >40% |
| 负反馈率 | 用户投诉/触达数 | <5% |

### 7.2 A/B 测试框架

```python
class TaskABTest:
    def run_test(self, task_template_a, task_template_b, user_group):
        """运行任务 A/B 测试"""
        
        # 分组
        group_a, group_b = self.split_users(user_group)
        
        # 执行
        results_a = self.execute_tasks(group_a, task_template_a)
        results_b = self.execute_tasks(group_b, task_template_b)
        
        # 比较
        metrics_a = self.calculate_metrics(results_a)
        metrics_b = self.calculate_metrics(results_b)
        
        # 决策
        winner = self.compare_metrics(metrics_a, metrics_b)
        
        return {
            'winner': winner,
            'metrics_a': metrics_a,
            'metrics_b': metrics_b,
            'confidence': self.calculate_confidence(metrics_a, metrics_b)
        }
```

---

## 八、MVP 范围

### 8.1 MVP 规则（P0）

| 规则 ID | 规则名称 | 优先级 |
|--------|---------|--------|
| R001 | 市场波动触发 | P0 |
| R003 | 用户行为异常触发 | P0 |
| R004 | 持仓风险触发 | P0 |
| R006 | 时间节点触发（基础） | P0 |

### 8.2 MVP 任务类型（P0）

| 任务类型 | 任务名称 | 优先级 |
|---------|---------|--------|
| T-B | 风险提醒 | P0 |
| T-C | 机会提示 | P0 |
| T-A | 信息推送（基础） | P1 |

### 8.3 首期迭代（P1）

| 规则/任务 | 说明 | 优先级 |
|----------|------|--------|
| R002 | 估值极端触发 | P1 |
| R005 | 市场情绪触发 | P1 |
| T-D | 互动任务 | P1 |
| T-E | 执行建议 | P1 |

### 8.4 后续版本（P2）

| 规则/任务 | 说明 | 优先级 |
|----------|------|--------|
| R007 | 宠物成长触发 | P2 |
| R008 | 外部事件触发 | P2 |
| 宠物辩论 | 多宠物协作 | P2 |
| LLM 生成 | 个性化内容 | P2 |

---

*最后更新：2026-04-11 | Day 1/10 完成度 80%*
