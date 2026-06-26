# Feishu Card Sender Skill

飞书卡片消息发送技能包 - 专业级interactive卡片发送解决方案

## 🎯 功能概述

本技能包提供完整的飞书interactive卡片发送能力，绕过OpenClaw内置限制，直接调用飞书OpenAPI实现专业级卡片消息发送。

## ✨ 核心特性

- **完整API支持**: 直接调用飞书OpenAPI，支持所有卡片类型
- **Schema 2.0标准**: 严格遵循飞书interactive卡片规范
- **多种卡片模板**: 新闻简报、机票特价、任务管理、基础信息等
- **智能错误处理**: 完整的异常捕获和错误码处理机制
- **大小自动验证**: 30KB限制自动检测，避免发送失败
- **Token自动管理**: tenant_access_token自动获取和缓存
- **群组/单聊支持**: 同时支持群组和一对一私人消息

## 🛠️ 核心工具

### 1. 高级卡片发送器 (`feishu_card_sender_advanced.py`)
```python
from feishu_card_sender_advanced import AdvancedFeishuCardSender

sender = AdvancedFeishuCardSender(app_id, app_secret)
result = sender.send_simple_card(
    receive_id="ou_xxx",
    receive_id_type="open_id", 
    title="🎯 测试卡片",
    content="**精彩内容**展示"
)
```

### 2. 基础发送器 (`direct_feishu_card_sender.py`)
```python
from direct_feishu_card_sender import FeishuCardSender

sender = FeishuCardSender(app_id, app_secret)
card = sender.build_interactive_card("标题", "内容")
result = sender.send_interactive_card("ou_xxx", "open_id", card)
```

### 3. 卡片模板库 (`feishu_card_templates.py`)
```python
from feishu_card_templates import (
    build_news_card,
    build_flight_deal_card,
    build_task_management_card
)

# 新闻简报卡片
news_card = build_news_card([
    {"category": "国际新闻", "title": "重大事件", "source": "路透社", "time": "2024-02-28 15:30"}
])

# 机票特价卡片
flight_card = build_flight_deal_card({
    "route": "上海 → 东京",
    "price": 899,
    "original_price": 2500,
    "date": "2024-03-15",
    "discount": "3.6折"
})
```

## 📋 支持的卡片类型

### 📰 新闻简报卡片
- 多段落布局
- 时间线展示
- 来源标注
- 分隔线组织

### ✈️ 机票特价卡片
- 双列字段布局
- 价格对比显示
- 折扣信息突出
- 预订按钮集成

### 📊 任务管理卡片
- 进度状态指示
- 多字段信息展示
- 优先级颜色标识
- 操作按钮支持

### 🎯 基础信息卡片
- 简洁标题+内容
- 主题颜色选择
- 图标装饰支持
- 灵活内容布局

## 🔧 使用方法

### 环境配置
```bash
export FEISHU_APP_ID="your_app_id"
export FEISHU_APP_SECRET="your_app_secret"
```

### 快速开始
```python
# 导入发送器
from feishu_card_sender_advanced import AdvancedFeishuCardSender

# 初始化发送器
sender = AdvancedFeishuCardSender(
    app_id="cli_xxx",
    app_secret="your_secret"
)

# 发送基础卡片
result = sender.send_simple_card(
    receive_id="ou_xxx",
    receive_id_type="open_id",
    title="🎉 欢迎使用",
    content="**飞书卡片**发送成功！"
)

print(f"消息ID: {result['message_id']}")
```

### 高级用法
```python
# 构建复杂卡片
card = sender.build_news_card([
    {
        "category": "科技新闻",
        "title": "AI技术突破",
        "source": "TechNews",
        "time": "2024-02-28 16:00"
    },
    {
        "category": "财经动态",
        "title": "市场分析",
        "source": "财经网",
        "time": "2024-02-28 15:30"
    }
])

# 发送到群组
result = sender.send_interactive_card(
    receive_id="oc_xxx",
    receive_id_type="chat_id",
    card=card
)
```

## 🎨 卡片设计指南

### 颜色主题
- `blue`: 蓝色主题（信息类）
- `green`: 绿色主题（成功类）
- `red`: 红色主题（警告类）
- `yellow`: 黄色主题（提醒类）
- `grey`: 灰色主题（中性类）

### 内容格式
- 支持Markdown语法
- 支持@用户功能
- 支持超链接
- 支持emoji图标
- 支持代码块

### 布局建议
- 标题简洁明了
- 内容层次清晰
- 重要信息突出
- 按钮操作明确

## ⚠️ 注意事项

1. **权限要求**: 需要`im:message:send_as_bot`权限
2. **大小限制**: 卡片内容不超过30KB
3. **频率限制**: 5 QPS（每秒5次）
4. **用户范围**: 接收者必须在应用可用范围内
5. **群组要求**: 机器人必须在目标群组中

## 🔍 错误处理

常见错误码及解决方案：

- `230013`: 用户不在应用可用范围内 → 检查应用权限设置
- `230002`: 机器人不在群组中 → 将机器人添加到群组
- `230099`: JSON格式错误 → 检查卡片结构是否正确
- `230020`: 频率限制 → 降低发送频率
- `230025`: 内容超出大小限制 → 简化卡片内容

## 📚 相关资源

- [飞书API文档](https://open.larkoffice.com/document/server-docs/im-v1/message/create)
- [Interactive卡片格式](https://open.larkoffice.com/document/uAjLw4CM/ukTMukTMukTM/im-v1/message/create_json)
- [OpenClaw飞书扩展源码](https://github.com/openclaw/openclaw/tree/main/extensions/feishu)

## 🚀 更新日志

### v1.0.0 (2026-02-28)
- ✅ 基础卡片发送功能
- ✅ 多种卡片模板支持
- ✅ 错误处理机制
- ✅ 大小验证功能
- ✅ 群组和单聊支持
- ✅ 完整文档和使用指南

---

**技能状态**: 生产就绪 ✅  
**维护状态**: 活跃维护 🔄  
**最后更新**: 2026-02-28