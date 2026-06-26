---
name: quick-draft
version: 1.0.0
description: 快速草稿 - 说几个要点自动生成结构化邮件/消息/周报草稿，内置多种模板(followup/thankyou/request/report)
tags: [draft, email, writing, productivity, communication, template]
author: laosi
source: original
---

# Quick Draft - 快速草稿

> 激活词: 草稿 / 写邮件 / 写消息 / 生成

## 功能

- 输入要点自动生成完整草稿
- 多种模板：跟进 / 感谢 / 请求 / 周报 / 通知
- 支持邮件和消息格式
- 保存草稿历史

## Python 实现

```python
import os, json
from datetime import datetime

DRAFT_FILE = os.path.join(os.path.dirname(__file__), "quick_drafts.json")

class QuickDraft:
    TEMPLATES = {
        "followup": {
            "name": "跟进邮件",
            "format": "email",
            "subject": "关于 {topic} 的跟进",
            "body": "Hi {name},\n\n"
                    "关于 {topic} 的事情，想跟您确认一下进度。\n\n"
                    "方便的话请回复，谢谢！\n\n"
                    "Best,\n{sender}"
        },
        "thankyou": {
            "name": "感谢信",
            "format": "email",
            "subject": "感谢 {reason}",
            "body": "Hi {name},\n\n"
                    "非常感谢您 {reason}！这对我帮助很大。\n\n"
                    "期待后续继续合作。\n\n"
                    "Best,\n{sender}"
        },
        "request": {
            "name": "请求协助",
            "format": "email",
            "subject": "请求协助: {topic}",
            "body": "Hi {name},\n\n"
                    "想请您帮忙 {request}。\n\n"
                    "如果方便的话，请在 {deadline or '方便时'} 回复。\n\n"
                    "提前感谢！\n\n"
                    "Best,\n{sender}"
        },
        "weekly": {
            "name": "周报",
            "format": "report",
            "subject": "周报 {week_start} - {week_end}",
            "body": "# {name} 周报 ({week_start} - {week_end})\n\n"
                    "## 本周完成\n"
                    "{completed}\n\n"
                    "## 下周计划\n"
                    "{planned}\n\n"
                    "## 问题与风险\n"
                    "{risks}"
        },
        "meeting": {
            "name": "会议纪要",
            "format": "note",
            "body": "# 会议纪要 - {topic}\n\n"
                    "**时间**: {date}\n"
                    "**参与人**: {attendees}\n\n"
                    "## 讨论内容\n"
                    "{discussion}\n\n"
                    "## 行动项\n"
                    "{actions}"
        }
    }
    
    def __init__(self):
        os.makedirs(os.path.dirname(DRAFT_FILE), exist_ok=True)
        self.drafts = self._load()
    
    def _load(self):
        if os.path.exists(DRAFT_FILE):
            with open(DRAFT_FILE, encoding="utf-8") as f:
                return json.load(f)
        return []
    
    def _save(self):
        with open(DRAFT_FILE, "w", encoding="utf-8") as f:
            json.dump(self.drafts, f, ensure_ascii=False, indent=2)
    
    def generate(self, template_key: str, params: dict) -> dict:
        """根据模板生成草稿"""
        if template_key not in self.TEMPLATES:
            available = list(self.TEMPLATES.keys())
            return {"error": f"Unknown template '{template_key}'. Available: {', '.join(available)}"}
        
        tmpl = self.TEMPLATES[template_key]
        
        # 填充模板变量
        try:
            subject = tmpl.get("subject", "").format(**params) if "subject" in tmpl else None
            body = tmpl["body"].format(**params)
        except KeyError as e:
            return {"error": f"Missing parameter: {e}"}
        
        draft = {
            "id": len(self.drafts) + 1,
            "template": template_key,
            "format": tmpl["format"],
            "subject": subject,
            "body": body,
            "params": params,
            "created": datetime.now().isoformat(),
            "finalized": False
        }
        
        self.drafts.append(draft)
        self._save()
        return draft
    
    def list_recent(self, limit: int = 5) -> list:
        return [{"id": d["id"], "template": d["template"], "subject": d.get("subject"),
                 "created": d["created"], "finalized": d["finalized"]}
                for d in self.drafts[-limit:]]

# 使用示例
draft = QuickDraft()

# 生成跟进邮件
email = draft.generate("followup", {
    "name": "张三",
    "topic": "项目方案评审",
    "sender": "李四"
})
print(f"📧 {email['subject']}")
print(email['body'])

# 生成周报
report = draft.generate("weekly", {
    "name": "李四",
    "week_start": "2026-05-22",
    "week_end": "2026-05-28",
    "completed": "- FlashAttention 调研完成\n- 性能测试框架搭建",
    "planned": "- 集成测试\n- 文档撰写",
    "risks": "- 依赖库版本兼容性问题"
})
print(f"📋 {report['subject']}")
print(report['body'])

# 生成会议纪要
meeting = draft.generate("meeting", {
    "topic": "Q2 OKR Review",
    "date": "2026-05-28",
    "attendees": "全员",
    "discussion": "- KR1 完成 80%，预计下月交付\n- KR2 延期2周，需要协调资源",
    "actions": "- 张三: 补充KR2资源申请\n- 李四: 周五前更新排期"
})
print(f"📝 {meeting['subject'] if meeting.get('subject') else meeting['body'][:50]}")
```

## 可用模板

| 模板 | 适用场景 | 格式 |
|------|---------|------|
| followup | 跟进客户/同事 | 邮件 |
| thankyou | 感谢信 | 邮件 |
| request | 请求资源/协助 | 邮件 |
| weekly | 周报 | 报告 |
| meeting | 会议纪要 | 笔记 |

## 命令行用法

```bash
# 生成跟进邮件
python -c "
from quick_draft import QuickDraft
d = QuickDraft().generate('followup', {'name': '王总', 'topic': '合同', 'sender': '我'})
print(d['subject'] + '\n---\n' + d['body'])
"
```

## 使用场景

1. **跟进客户**: 快速生成专业跟进邮件，不遗漏要点
2. **感谢同事**: 别人帮了忙，一键生成感谢信
3. **每周周报**: 填几个要点生成完整周报
4. **会议纪要**: 会后5分钟出纪要
5. **日常沟通**: 请假、通知、邀请等常用场景

## 依赖

- Python 3.8+
- 无第三方依赖
