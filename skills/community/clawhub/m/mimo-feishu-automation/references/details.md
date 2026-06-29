# 飞书自动化工具 - 详细内容

## 一、飞书开放平台接入指南

### 1.1 应用创建流程

```
1. 访问 https://open.feishu.cn/app
2. 点击「创建企业自建应用」
3. 填写应用信息：
   - 应用名称：{你的应用名}
   - 应用描述：{功能说明}
   - 应用图标：上传PNG/JPG 256x256
4. 获取凭证：
   - App ID: cli_xxxxxxxxxxxxxxxx
   - App Secret: ****************
5. 配置权限
6. 发布应用
```

### 1.2 权限配置清单

| 权限类型 | 权限标识 | 用途 |
|----------|----------|------|
| 消息权限 | im:message:send_as_bot | 发送消息 |
| 消息权限 | im:message:receive_v1 | 接收消息 |
| 消息权限 | im:message.p2p_msg:readonly | 读取私聊消息 |
| 日历权限 | calendar:calendar:readonly | 读取日历 |
| 日历权限 | calendar:calendar | 读写日历 |
| 云文档权限 | docx:document:readonly | 读取文档 |
| 云文档权限 | docx:document | 读写文档 |
| 多维表格权限 | bitable:app:readonly | 读取多维表格 |
| 多维表格权限 | bitable:app | 读写多维表格 |
| 审批权限 | approval:instance:readonly | 读取审批 |
| 审批权限 | approval:instance | 提交审批 |
| 通讯录权限 | contact:user.base:readonly | 读取用户基础信息 |
| 通讯录权限 | contact:user.id:readonly | 读取用户ID |

### 1.3 获取Tenant Access Token

```python
import requests

def get_tenant_token(app_id, app_secret):
    """获取tenant_access_token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {"Content-Type": "application/json"}
    payload = {
        "app_id": app_id,
        "app_secret": app_secret
    }
    
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()
    
    if result.get("code") == 0:
        return result["tenant_access_token"]
    else:
        raise Exception(f"获取token失败: {result}")

# 使用示例
app_id = "cli_xxxxxxxxxxxxxxxx"
app_secret = "your_app_secret"
token = get_tenant_token(app_id, app_secret)
print(f"Tenant Token: {token}")
```

### 1.4 Token自动刷新机制

```python
import time
from datetime import datetime, timedelta

class FeishuTokenManager:
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self._token = None
        self._expires_at = None
    
    def get_token(self):
        """获取有效token，自动刷新"""
        if self._token is None or self._is_expired():
            self._refresh_token()
        return self._token
    
    def _is_expired(self):
        """检查token是否过期"""
        if self._expires_at is None:
            return True
        # 提前5分钟刷新
        return datetime.now() >= (self._expires_at - timedelta(minutes=5))
    
    def _refresh_token(self):
        """刷新token"""
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        response = requests.post(url, json=payload)
        result = response.json()
        
        if result.get("code") == 0:
            self._token = result["tenant_access_token"]
            # token有效期24小时
            self._expires_at = datetime.now() + timedelta(hours=23)
        else:
            raise Exception(f"Token刷新失败: {result}")
```

## 二、消息推送完整指南

### 2.1 发送文本消息

```python
def send_text_message(token, receive_id_type, receive_id, content):
    """发送文本消息"""
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    
    params = {
        "receive_id_type": receive_id_type  # open_id/user_id/union_id/email/chat_id
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "receive_id": receive_id,
        "msg_type": "text",
        "content": json.dumps({"text": content})
    }
    
    response = requests.post(url, headers=headers, params=params, json=payload)
    return response.json()

# 使用示例
token = get_tenant_token(app_id, app_secret)
# 通过open_id发送
send_text_message(token, "open_id", "ou_xxxxx", "这是一条测试消息")
# 通过user_id发送
send_text_message(token, "user_id", "user_xxxxx", "这是一条测试消息")
# 通过email发送
send_text_message(token, "email", "test@example.com", "这是一条测试消息")
```

### 2.2 发送富文本消息（卡片）

```python
def send_interactive_message(token, receive_id, receive_id_type, card_content):
    """发送卡片消息"""
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    
    params = {"receive_id_type": receive_id_type}
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "receive_id": receive_id,
        "msg_type": "interactive",
        "content": json.dumps(card_content)
    }
    
    response = requests.post(url, headers=headers, params=params, json=payload)
    return response.json()

# 卡片消息模板：项目提醒
def create_project_reminder_card(project_name, deadline, task_list):
    """创建项目提醒卡片"""
    tasks_html = ""
    for task in task_list:
        status_emoji = "✅" if task["done"] else "⬜"
        tasks_html += f'<li>{status_emoji} {task["name"]}</li>'
    
    card = {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": f"📋 {project_name} - 进度提醒"},
            "template": "blue"
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**截止时间**: {deadline}\n**负责人**: {task_list[0].get('owner', '待分配')}"
                }
            },
            {"tag": "hr"},
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**待办事项**:\n<ul>{tasks_html}</ul>"
                }
            },
            {
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {"tag": "plain_text", "content": "查看详情"},
                        "type": "primary",
                        "url": "https://feishu.cn/task/link"
                    }
                ]
            }
        ]
    }
    return card

# 使用示例
card = create_project_reminder_card(
    "Q2季度OKR",
    "2026-06-30",
    [
        {"name": "完成技术方案设计", "done": True, "owner": "张三"},
        {"name": "开发核心模块", "done": False, "owner": "李四"},
        {"name": "UAT测试", "done": False, "owner": "王五"}
    ]
)
send_interactive_message(token, "ou_xxxxx", "open_id", card)
```

### 2.3 发送Markdown消息

```python
def send_markdown_message(token, receive_id_type, receive_id, content):
    """发送Markdown消息"""
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    
    params = {"receive_id_type": receive_id_type}
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "receive_id": receive_id,
        "msg_type": "post",
        "content": json.dumps({
            "zh_cn": {
                "title": "消息标题",
                "content": [[{
                    "tag": "text",
                    "text": content
                }]]
            }
        })
    }
    
    response = requests.post(url, headers=headers, params=params, json=payload)
    return response.json()

# Markdown支持格式
markdown_example = """
**加粗文本**
_斜体文本_
~~删除线~~
`行内代码`
[链接文字](https://feishu.cn)
"""
send_markdown_message(token, "open_id", "ou_xxxxx", markdown_example)
```

## 三、多维表格操作指南

### 3.1 获取多维表格数据

```python
def get_bitable_records(token, app_token, table_id, filter_conditions=None):
    """获取多维表格记录"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records"
    
    headers = {"Authorization": f"Bearer {token}"}
    
    params = {}
    if filter_conditions:
        # 飞书过滤语法
        params["filter"] = filter_conditions
    
    response = requests.get(url, headers=headers, params=params)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]["items"]
    else:
        raise Exception(f"获取记录失败: {result}")

# 使用示例
records = get_bitable_records(
    token, 
    "bascnxxxxxxx",  # 多维表格App Token
    "tblxxxxxxx"     # 数据表ID
)
for record in records:
    print(record["fields"])
```

### 3.2 创建/更新记录

```python
def create_bitable_record(token, app_token, table_id, fields_data):
    """创建多维表格记录"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "fields": fields_data
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def update_bitable_record(token, app_token, table_id, record_id, fields_data):
    """更新多维表格记录"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "fields": fields_data
    }
    
    response = requests.put(url, headers=headers, json=payload)
    return response.json()

# 创建记录示例
new_record = create_bitable_record(
    token,
    "bascnxxxxxxx",
    "tblxxxxxxx",
    {
        "任务名称": "完成需求文档",
        "负责人": "张三",
        "截止日期": "2026-06-15",
        "优先级": "高",
        "状态": "进行中"
    }
)

# 更新记录示例
update_bitable_record(
    token,
    "bascnxxxxxxx",
    "tblxxxxxxx",
    "recxxxxxxx",  # 记录ID
    {
        "状态": "已完成",
        "完成时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
)
```

### 3.3 批量操作

```python
def batch_create_records(token, app_token, table_id, records_list):
    """批量创建记录"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "records": [{"fields": r} for r in records_list]
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def batch_delete_records(token, app_token, table_id, record_ids):
    """批量删除记录"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_delete"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "records": record_ids
    }
    
    response = requests.delete(url, headers=headers, json=payload)
    return response.json()
```

## 四、日历事件管理

### 4.1 创建日历事件

```python
def create_calendar_event(token, calendar_id, summary, start_time, end_time, 
                         attendees=None, description="", location=""):
    """创建日历事件"""
    url = "https://open.feishu.cn/open-apis/calendar/v4/calendars/{}/events".format(calendar_id)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "summary": summary,
        "description": description,
        "location": {"name": location},
        "start_time": {
            "timestamp": str(int(start_time.timestamp())),
            "timezone": "Asia/Shanghai"
        },
        "end_time": {
            "timestamp": str(int(end_time.timestamp())),
            "timezone": "Asia/Shanghai"
        },
        "attendees": {
            "attendees": [{"type": "user", "user_id": a} for a in (attendees or [])]
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# 使用示例
from datetime import datetime, timedelta

start = datetime.now() + timedelta(hours=1)
end = start + timedelta(hours=1)

event = create_calendar_event(
    token,
    "primary",  # 主日历
    "团队周会",
    start,
    end,
    attendees=["user_id_1", "user_id_2"],
    description="讨论本周进度和下周计划",
    location="会议室A"
)
```

### 4.2 查询和更新事件

```python
def get_calendar_events(token, calendar_id, start_time, end_time):
    """查询日历事件"""
    url = f"https://open.feishu.cn/open-apis/calendar/v4/calendars/{calendar_id}/events"
    
    headers = {"Authorization": f"Bearer {token}"}
    
    params = {
        "start_time": str(int(start_time.timestamp())),
        "end_time": str(int(end_time.timestamp())),
        "page_size": 50
    }
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def update_calendar_event(token, calendar_id, event_id, update_data):
    """更新日历事件"""
    url = f"https://open.feishu.cn/open-apis/calendar/v4/calendars/{calendar_id}/events/{event_id}"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.patch(url, headers=headers, json=update_data)
    return response.json()

def delete_calendar_event(token, calendar_id, event_id):
    """删除日历事件"""
    url = f"https://open.feishu.cn/open-apis/calendar/v4/calendars/{calendar_id}/events/{event_id}"
    
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.delete(url, headers=headers)
    return response.json()
```

## 五、审批流程自动化

### 5.1 发起审批

```python
def create_approval_instance(token, approval_code, form_data, approvers):
    """发起审批实例"""
    url = "https://open.feishu.cn/open-apis/approval/v4/instances"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 表单数据格式
    form = []
    for item in form_data:
        form.append({
            "id": item["id"],  # 表单控件ID
            "value": [{"type": "text", "text": item["value"]}]
        })
    
    payload = {
        "approval_code": approval_code,
        "form": form,
        "approvers": [{"id": a, "type": "user"} for a in approvers]
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# 使用示例
form_data = [
    {"id": "控件ID_1", "name": "申请人", "value": "张三"},
    {"id": "控件ID_2", "name": "申请金额", "value": "5000"},
    {"id": "控件ID_3", "name": "申请原因", "value": "购买办公设备"}
]

instance = create_approval_instance(
    token,
    "approval_code_xxx",  # 审批定义CODE
    form_data,
    ["user_id_1", "user_id_2"]  # 审批人ID列表
)
```

### 5.2 查询审批状态

```python
def get_approval_instance(token, instance_id):
    """查询审批实例"""
    url = f"https://open.feishu.cn/open-apis/approval/v4/instances/{instance_id}"
    
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    return response.json()

def get_approval_tasks(token, user_id):
    """获取待我审批的任务"""
    url = "https://open.feishu.cn/open-apis/approval/v4/tasks/query"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "user_id": user_id,
        "task_status": "PENDING"
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def approve_task(token, task_id, comment=""):
    """审批通过"""
    url = f"https://open.feishu.cn/open-apis/approval/v4/tasks/{task_id}/approve"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "comment": comment
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def reject_task(token, task_id, comment=""):
    """审批拒绝"""
    url = f"https://open.feishu.cn/open-apis/approval/v4/tasks/{task_id}/reject"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "comment": comment
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()
```

## 六、定时任务实现

### 6.1 Cron表达式详解

| 表达式 | 含义 | 示例 |
|--------|------|------|
| `0 0 * * * *` | 每小时整点 | 每天9:00, 10:00, 11:00 |
| `0 0 9 * * *` | 每天9点 | 每日早报 |
| `0 0 9 * * 1-5` | 工作日9点 | 工作日提醒 |
| `0 30 18 * * 5` | 每周五18:30 | 周报提醒 |
| `0 0 10 1 * *` | 每月1号10点 | 月度汇总 |
| `0 0/30 * * * *` | 每30分钟 | 数据同步 |

### 6.2 定时任务框架

```python
import schedule
import time
from threading import Thread

def daily_report_job():
    """每日报告任务"""
    try:
        token = get_tenant_token(app_id, app_secret)
        report_data = generate_daily_report()
        message = format_report_message(report_data)
        send_text_message(token, "chat_id", "group_xxx", message)
    except Exception as e:
        print(f"任务执行失败: {e}")

def weekly_summary_job():
    """每周汇总任务"""
    try:
        token = get_tenant_token(app_id, app_secret)
        summary = generate_weekly_summary()
        message = format_summary_message(summary)
        # 发送到指定用户
        send_interactive_message(token, "open_id", "user_xxx", message)
    except Exception as e:
        print(f"任务执行失败: {e}")

def run_schedule():
    """运行定时任务"""
    # 每日9点发送早报
    schedule.every().day.at("09:00").do(daily_report_job)
    
    # 每周五18点发送周报
    schedule.every().friday.at("18:00").do(weekly_summary_job)
    
    # 每30分钟同步数据
    schedule.every(30).minutes.do(sync_data_job)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

# 后台启动定时任务
def start_scheduler():
    thread = Thread(target=run_schedule, daemon=True)
    thread.start()
    return thread
```

## 七、常见场景模板

### 7.1 日报自动生成

```python
DAILY_REPORT_CARD = {
    "config": {"wide_screen_mode": True},
    "header": {
        "title": {"tag": "plain_text", "content": "📊 每日工作日报"},
        "template": "purple"
    },
    "elements": [
        {
            "tag": "div",
            "text": {"tag": "lark_md", "content": "**日报日期**: {date}"}
        },
        {"tag": "hr"},
        {
            "tag": "div",
            "text": {"tag": "lark_md", "content": "**今日完成**:\n{task_list}"}
        },
        {
            "tag": "div",
            "text": {"tag": "lark_md", "content": "**明日计划**:\n{plan_list}"}
        },
        {
            "tag": "div",
            "text": {"tag": "lark_md", "content": "**问题/阻塞**:\n{blockers}"}
        }
    ]
}
```

### 7.2 会议提醒

```python
MEETING_REMINDER_CARD = {
    "config": {"wide_screen_mode": True},
    "header": {
        "title": {"tag": "plain_text", "content": "⏰ 会议提醒"},
        "template": "orange"
    },
    "elements": [
        {
            "tag": "div",
            "text": {"tag": "lark_md", "content": "**会议名称**: {meeting_name}"}
        },
        {
            "tag": "div",
            "text": {"tag": "lark_md", "content": "**会议时间**: {time}"}
        },
        {
            "tag": "div",
            "text": {"tag": "lark_md", "content": "**参会人员**: {attendees}"}
        },
        {
            "tag": "div",
            "text": {"tag": "lark_md", "content": "**会议链接**: [点击加入]({link})"}
        },
        {
            "tag": "note",
            "elements": [{"tag": "plain_text", "content": "请提前5分钟进入会议室"}]
        }
    ]
}
```

### 7.3 审批催办

```python
APPROVAL_REMINDER_CARD = {
    "config": {"wide_screen_mode": True},
    "header": {
        "title": {"tag": "plain_text", "content": "🔔 审批催办提醒"},
        "template": "red"
    },
    "elements": [
        {
            "tag": "div",
            "text": {"tag": "lark_md", "content": "**申请人**: {applicant}"}
        },
        {
            "tag": "div",
            "text": {"tag": "lark_md", "content": "**申请类型**: {type}"}
        },
        {
            "tag": "div",
            "text": {"tag": "lark_md", "content": "**提交时间**: {submit_time}"}
        },
        {
            "tag": "div",
            "text": {"tag": "lark_md", "content": "⏳ **已等待**: {waiting_hours}小时"}
        },
        {
            "tag": "action",
            "actions": [
                {
                    "tag": "button",
                    "text": {"tag": "plain_text", "content": "立即审批"},
                    "type": "primary",
                    "url": "{approval_link}"
                }
            ]
        }
    ]
}
```

## 八、错误码处理

| 错误码 | 说明 | 处理建议 |
|--------|------|----------|
| 99991663 | 无权限 | 检查应用权限配置 |
| 99991664 | 接口调用频率超限 | 添加请求间隔 |
| 99991400 | 参数错误 | 检查请求参数格式 |
| 230001 | 用户不存在 | 检查user_id是否正确 |
| 230002 | 群聊不存在 | 检查chat_id是否正确 |
| 230003 | 应用不在群聊中 | 将应用添加到群聊 |

## 九、API调用频率限制

| 接口类型 | QPS限制 | 日限额 |
|----------|--------|--------|
| 发消息 | 50 | 无 |
| 读消息 | 60 | 无 |
| 读日历 | 60 | 无 |
| 写日历 | 10 | 无 |
| 多维表格读 | 30 | 无 |
| 多维表格写 | 10 | 无 |

## 十、安全最佳实践

1. **Token安全存储**：使用环境变量或加密存储App Secret
2. **最小权限原则**：只申请业务必需的权限
3. **请求验证**：对外部输入进行校验
4. **日志脱敏**：敏感信息（手机号、身份证）打码处理
5. **错误处理**：不向用户暴露内部错误详情
6. **IP白名单**：生产环境配置IP访问限制
