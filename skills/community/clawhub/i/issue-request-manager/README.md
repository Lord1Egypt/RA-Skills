# Issue Request Manager Skill

这是一个完整的Issue Request管理技能，提供了创建、跟踪和回复Issue的功能。

## 功能特性

### 1. Issue Request 创建 (IR Creator)
- 创建新的Issue Request
- 设置问题类型、优先级、标签
- 分配给相关人员
- 添加详细描述和附件

### 2. Issue Request 跟踪 (IR Tracker)
- 实时监控Issue状态变化
- 跟踪解决进度
- 自动提醒相关方
- 生成问题报告

### 3. Issue Request 回复 (IR Responder)
- 回复问题描述
- 更新问题状态
- 添加评论和附件
- 关闭已解决问题

### 4. 微信通知 (WeChat Notifier)
- 新Issue创建通知
- Issue状态变更通知
- Issue分配通知
- Issue关闭通知
- 可配置的通知接收者

## 安装和使用

### 安装依赖
```bash
pip install -r requirements.txt
```

### 基本使用
```python
from skills.issue_request_manager import *

# 创建Issue
issue = create_issue(
    title="登录页面样式问题",
    description="用户登录页面的按钮样式在移动端显示不正确",
    issue_type="bug",
    priority="high",
    assignee="developer1",
    labels=["frontend", "mobile"]
)

# 跟踪Issue
tracked = track_issue(issue['id'])

# 回复Issue
reply = reply_to_issue(issue['id'], "正在处理中...", "developer1")

# 分配Issue
assigned = assign_issue(issue['id'], "developer2")

# 设置优先级
prioritized = set_priority(issue['id'], "critical")

# 关闭Issue
closed = close_issue(issue['id'], "问题已修复并验证")
```

## 微信通知配置

要启用微信通知功能，您需要在配置文件中设置企业微信参数：

```json
{
  "wechat_notification": {
    "enabled": true,
    "corp_id": "your_corp_id",
    "secret": "your_secret",
    "agent_id": 1000001
  }
}
```

然后在代码中使用：
```python
# 初始化微信通知器
notifier = init_wechat_notifier(
    corp_id="your_corp_id",
    secret="your_secret",
    agent_id=1000001
)

# 发送新Issue通知
notify_new_issue(notifier, issue, ["user1", "user2"])

# 发送Issue更新通知
notify_issue_update(notifier, issue, "status_changed", ["user1"])
```

## 配置

配置文件位于 `config.json` 中，可以自定义默认设置、支持的平台等。

## 数据持久化

使用 `ir_database.py` 模块进行数据持久化，确保Issue信息不会因程序重启而丢失。

## 扩展性

该技能采用模块化设计，易于扩展：
- 可以轻松集成到GitHub、GitLab、Jira等平台
- 支持自定义通知机制
- 可以添加更多分析和报告功能

## API 接口

技能提供了RESTful API接口：
- POST `/api/issues/create` - 创建Issue
- GET `/api/issues/{id}/track` - 跟踪Issue
- POST `/api/issues/{id}/reply` - 回复Issue
- PUT `/api/issues/{id}/update` - 更新Issue