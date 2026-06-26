# Meeting Notes Integration & Tools Guide

## Tool Integrations

### 飞书（Lark）集成

**飞书文档模板设置：**
1. 飞书文档 → 模板库 → 新建模板
2. 使用 SKILL.md 中的会议纪要模板
3. 设置权限：参会人均可编辑

**飞书会议纪要自动创建：**
```
飞书日历 → 会议事件 → 关联文档
→ 会后自动提醒创建纪要
→ 纪要链接自动同步到日历事件
```

**飞书Bot发送摘要：**
```json
{
  "msg_type": "interactive",
  "card": {
    "header": {
      "title": { "content": "📋 会议纪要｜{会议主题}", "tag": "plain_text" },
      "template": "blue"
    },
    "elements": [
      {
        "tag": "div",
        "text": { "content": "**日期：** {日期}\n**参会：** {人员列表}", "tag": "lark_md" }
      },
      {
        "tag": "div",
        "text": { "content": "**核心决议：**\n{决议列表}", "tag": "lark_md" }
      },
      {
        "tag": "action",
        "actions": [
          {
            "tag": "button",
            "text": { "content": "查看完整纪要", "tag": "plain_text" },
            "url": "{纪要链接}",
            "type": "primary"
          }
        ]
      }
    ]
  }
}
```

---

### Notion 集成

**Database 结构：**
```
会议记录数据库字段：
- 会议名称 (Title)
- 日期 (Date)
- 参会人 (Multi-select / People)
- 会议类型 (Select: 例会/评审/复盘/一对一)
- 项目 (Relation → 项目数据库)
- 行动项数量 (Formula: length(行动项))
- 状态 (Select: 草稿/已发送/已归档)
- 标签 (Multi-select)
```

**关联行动项数据库：**
```
行动项数据库字段：
- 任务描述 (Title)
- 来源会议 (Relation → 会议记录)
- 负责人 (Person)
- 截止日期 (Date)
- 优先级 (Select: P0/P1/P2/P3)
- 状态 (Select: 待开始/进行中/已完成/已取消)
- 备注 (Text)
```

---

### Jira / Linear 集成

**会议行动项 → Jira Issue 映射：**

```
行动项字段 → Jira字段
任务描述 → Summary
负责人 → Assignee
截止日期 → Due Date
优先级 P0 → Priority: Blocker
优先级 P1 → Priority: Critical
优先级 P2 → Priority: Major
优先级 P3 → Priority: Minor
来源会议 → Description（附链接）
```

**批量创建 Jira Issues（Python示例）：**
```python
import requests

def create_jira_issues_from_meeting(action_items, jira_config):
    headers = {
        "Authorization": f"Bearer {jira_config['token']}",
        "Content-Type": "application/json"
    }
    
    for item in action_items:
        payload = {
            "fields": {
                "project": {"key": jira_config["project_key"]},
                "summary": item["task"],
                "assignee": {"accountId": item["owner_id"]},
                "duedate": item["deadline"],
                "priority": {"name": map_priority(item["priority"])},
                "description": {
                    "type": "doc",
                    "content": [{
                        "type": "paragraph",
                        "content": [{"type": "text", "text": f"来自会议：{item['meeting_link']}"}]
                    }]
                }
            }
        }
        
        response = requests.post(
            f"{jira_config['base_url']}/rest/api/3/issue",
            json=payload,
            headers=headers
        )
        print(f"Created: {response.json().get('key')} - {item['task']}")
```

---

## AI-Assisted Meeting Notes Workflow

### Step-by-Step with AI

```
1. 录音/转录 → Otter.ai / 飞书妙记 / Zoom AI Summary

2. 粘贴转录文本，使用此 Prompt：
   "请将以下会议转录整理为结构化纪要，
    包含：核心决议3-5条、行动项表格（含负责人/截止/优先级）、
    待确认问题列表。语言：中文。"

3. 检查并补充遗漏项

4. 发送给参会人确认（24小时内）

5. 将行动项同步到项目管理工具
```

---

## Meeting Notes Quality Checklist

发送前自查：
- [ ] 每个行动项都有明确负责人
- [ ] 每个行动项都有截止日期（或标注TBD+原因）
- [ ] 核心决议已用粗体/标注突出
- [ ] 参会人姓名无错别字
- [ ] 文档权限已设置（参会人可访问）
- [ ] 已在48小时内发送
- [ ] 下次会议时间已确认并发出邀请
