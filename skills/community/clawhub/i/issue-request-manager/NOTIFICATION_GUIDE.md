# 微信通知功能使用指南

## 功能概述

Issue Request Manager技能现在集成了微信通知功能，可以在Issue创建、状态变更、分配和关闭时向指定用户发送通知。

## 配置步骤

### 1. 获取企业微信配置信息

要在企业微信中使用通知功能，您需要以下信息：

- **CorpID**: 企业微信的企业ID
- **Secret**: 应用的Secret密钥
- **AgentID**: 应用的Agent ID

### 2. 配置文件设置

编辑 `config.json` 文件，添加微信通知配置：

```json
{
  "default_settings": {
    "wechat_notification": {
      "enabled": true,
      "corp_id": "your_corp_id_here",
      "secret": "your_secret_here",
      "agent_id": 1000001
    }
  }
}
```

### 3. 企业微信配置说明

#### CorpID
- 登录企业微信管理后台
- 进入"我的企业"页面获取企业ID

#### Secret
- 进入"应用管理" -> "自建应用"
- 选择对应应用，点击"查看详情"
- 获取应用的Secret密钥

#### AgentID
- 在应用详情页面可以看到AgentID
- 通常是一个数字ID

## 使用方法

### 1. 基本通知发送

```python
from skills.issue_request_manager import *

# 初始化微信通知器
notifier = init_wechat_notifier(
    corp_id="your_corp_id",
    secret="your_secret", 
    agent_id=1000001
)

# 发送新Issue通知
issue = create_issue("测试Issue", "测试描述")
notify_new_issue(notifier, issue, ["user1", "user2"])

# 发送状态变更通知
notify_issue_update(notifier, issue, "status_changed", ["user1"])

# 发送关闭通知
notify_issue_closed(notifier, issue, ["user1", "user2"])
```

### 2. 通知类型

#### 新Issue创建通知
```python
notify_new_issue(notifier, issue, recipients)
```

#### Issue状态变更通知
```python
notify_issue_update(notifier, issue, "status_changed", recipients)
```

#### Issue分配通知
```python
notify_issue_update(notifier, issue, "assigned", recipients)
```

#### Issue评论通知
```python
notify_issue_update(notifier, issue, "commented", recipients)
```

#### Issue关闭通知
```python
notify_issue_closed(notifier, issue, recipients)
```

## 注意事项

### 1. 用户标识
- 接收者列表中的用户名必须是企业微信中的真实用户账号
- 用户名通常是企业微信中的员工账号或部门名称

### 2. 权限要求
- 企业微信应用需要有发送消息的权限
- 需要确保应用已启用"应用管理"中的消息发送功能

### 3. 网络要求
- 需要能够访问企业微信API服务器
- 确保防火墙允许相关端口通信

### 4. 错误处理
```python
try:
    success = notify_new_issue(notifier, issue, ["user1"])
    if success:
        print("通知发送成功")
    else:
        print("通知发送失败")
except Exception as e:
    print(f"通知发送异常: {e}")
```

## 最佳实践

### 1. 条件通知
```python
# 只对高优先级Issue发送通知
if issue['priority'] in ['high', 'critical']:
    notify_new_issue(notifier, issue, high_priority_recipients)
```

### 2. 分组通知
```python
# 根据Issue类型发送给不同团队
if issue['type'] == 'bug':
    notify_new_issue(notifier, issue, developers)
elif issue['type'] == 'feature':
    notify_new_issue(notifier, issue, product_team)
```

### 3. 通知模板
```python
def create_notification_template(issue, action_type):
    templates = {
        "new_issue": f"🆕 新建Issue!\nID: {issue['id']}\n标题: {issue['title']}",
        "status_change": f"🔄 状态变更!\nID: {issue['id']}\n新状态: {issue['status']}",
        "assigned": f"🎯 已分配!\nID: {issue['id']}\n分配给: {issue['assignee']}"
    }
    return templates.get(action_type, "通知内容")
```

## 故障排除

### 1. 通知发送失败
- 检查企业微信配置是否正确
- 确认用户账号是否存在且可用
- 检查网络连接和防火墙设置

### 2. Token获取失败
- 确认CorpID和Secret是否正确
- 检查应用权限是否足够
- 确认时间戳没有偏差

### 3. 消息格式问题
- 确保接收者列表格式正确
- 检查消息长度限制（企业微信有消息长度限制）

## 安全建议

1. **密钥保护**: 不要在代码中硬编码Secret，建议使用环境变量
2. **权限最小化**: 仅授予应用必要的权限
3. **日志记录**: 记录通知发送状态以便排查问题
4. **频率限制**: 注意企业微信的消息发送频率限制

## 扩展功能

### 1. 多渠道通知
```python
# 可以同时发送到多个平台
def send_all_notifications(issue, recipients):
    # 发送微信通知
    wechat_notifier = init_wechat_notifier(...)
    notify_new_issue(wechat_notifier, issue, recipients)
    
    # 发送邮件通知
    # 发送Slack通知
    # 等等...
```

### 2. 自定义通知内容
```python
def customize_notification(issue, custom_message, recipients):
    # 自定义通知内容
    message = f"{custom_message}\n\n{issue['title']}\n状态: {issue['status']}"
    notifier = init_wechat_notifier(...)
    notifier.send_notification(recipients, message, "自定义通知标题")
```

这个指南提供了完整的微信通知功能使用指导，帮助您快速集成和使用这一功能。