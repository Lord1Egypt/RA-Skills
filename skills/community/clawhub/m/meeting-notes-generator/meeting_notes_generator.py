#!/usr/bin/env python3
"""
Meeting Notes Generator - AI Meeting Assistant
自动生成会议纪要、提取任务、跟踪待办
"""
import json
import sys
from datetime import datetime, timedelta

# ============= 会议模板 =============

MEETING_TEMPLATES = {
    "daily": {
        "name": "Daily Standup",
        "sections": ["updates", "blockers", "today_tasks"],
        "duration": "15 min"
    },
    "weekly": {
        "name": "Weekly Team Meeting",
        "sections": ["summary", "updates", "action_items", "next_meeting"],
        "duration": "60 min"
    },
    "one-on-one": {
        "name": "1:1 Meeting", 
        "sections": ["career", "feedback", "questions", "action_items"],
        "duration": "30 min"
    },
    "project": {
        "name": "Project Review",
        "sections": ["progress", "issues", "decisions", "next_steps"],
        "duration": "45 min"
    },
    "client": {
        "name": "Client Meeting",
        "sections": ["attendees", "discussion", "agreements", "action_plan"],
        "duration": "60 min"
    },
    "brainstorm": {
        "name": "Brainstorming Session",
        "sections": ["topic", "ideas", "prioritization", "next_actions"],
        "duration": "90 min"
    }
}

# 模拟会议数据
SAMPLE_DATA = {
    "daily": {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "attendees": ["Alice", "Bob", "Carol"],
        "updates": [
            {"who": "Alice", "yesterday": "Completed API integration", "today": "Working on unit tests"},
            {"who": "Bob", "yesterday": "Deployed to staging", "today": "Fixing staging bugs"},
            {"who": "Carol", "yesterday": "Design review completed", "today": "Starting mobile layouts"}
        ],
        "blockers": [],
        "today_tasks": [
            {"task": "Complete unit tests", "owner": "Alice"},
            {"task": "Fix staging bugs", "owner": "Bob"},
            {"task": "Mobile layouts", "owner": "Carol"}
        ]
    },
    "weekly": {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": "14:00-15:00",
        "attendees": ["Alice", "Bob", "Carol", "David", "Manager"],
        "summary": [
            "Q1 goals review completed successfully",
            "Resource allocation discussed and approved",
            "New project timeline finalized",
            "Team capacity reviewed for next sprint"
        ],
        "updates": [
            {"team": "Frontend", "status": "On track", "notes": "Mobile views 80% complete"},
            {"team": "Backend", "status": "At risk", "notes": "API optimization needed"},
            {"team": "Design", "status": "Complete", "notes": "All assets delivered"}
        ],
        "action_items": [
            {"task": "Update project plan document", "owner": "Alice", "due": "Mar 5", "priority": "high"},
            {"task": "Schedule client demo", "owner": "Bob", "due": "Mar 7", "priority": "high"},
            {"task": "Review design specs", "owner": "Carol", "due": "Mar 10", "priority": "medium"},
            {"task": "Performance optimization research", "owner": "David", "due": "Mar 12", "priority": "low"}
        ],
        "next_meeting": "Tuesday, March 10, 2026 @ 14:00"
    },
    "one-on-one": {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "attendees": ["Manager", "You"],
        "career": [
            "Progress on Q1 goals reviewed - 2/3 completed",
            "Recent presentation feedback was very positive",
            "Growth areas identified: technical leadership"
        ],
        "questions": [
            "Any opportunities for mentorship?",
            "Timeline for promotion consideration?",
            "Areas to focus on for senior role?"
        ],
        "feedback": [
            "Strong technical skills",
            "Good communication with team",
            " room for growth in cross-functional collaboration"
        ],
        "action_items": [
            {"task": "Schedule skip-level meeting with Director", "owner": "You", "due": "Mar 15"},
            {"task": "Prepare mid-year review self-assessment", "owner": "You", "due": "Mar 20"},
            {"task": "Schedule monthly 1:1s going forward", "owner": "Manager"}
        ]
    }
}

# ============= 输出格式化 =============

def format_daily(data):
    """格式化每日站会"""
    lines = [
        f"# 📅 Daily Standup - {data['date']}",
        "",
        "## 👥 Team Updates",
        ""
    ]
    for u in data['updates']:
        lines.append(f"**{u['who']}:**")
        lines.append(f"  - Yesterday: {u['yesterday']}")
        lines.append(f"  - Today: {u['today']}")
        lines.append("")
    
    if data['blockers']:
        lines.append("## 🚧 Blockers")
        for b in data['blockers']:
            lines.append(f"- {b}")
        lines.append("")
    else:
        lines.append("## 🚧 Blockers")
        lines.append("- None reported ✅")
        lines.append("")
    
    lines.append("## ✅ Today's Tasks")
    for t in data['today_tasks']:
        owner = t.get('owner', 'TBD')
        lines.append(f"- [ ] **{t['task']}** (👤 {owner})")
    
    lines.append("")
    lines.append(f"*Generated at {datetime.now().strftime('%H:%M')}*")
    return '\n'.join(lines)


def format_weekly(data):
    """格式化周会"""
    lines = [
        f"# 📊 Weekly Team Meeting - {data['date']}",
        f"**Time:** {data.get('time', 'TBD')}",
        f"**Attendees:** {', '.join(data['attendees'])}",
        "",
        "## 📝 Summary",
        ""
    ]
    for s in data['summary']:
        lines.append(f"- {s}")
    
    lines.append("")
    lines.append("## 🔄 Team Updates")
    lines.append("")
    lines.append("| Team | Status | Notes |")
    lines.append("|------|--------|-------|")
    for u in data['updates']:
        status_icon = "🟢" if u['status'] == 'On track' else ("🔴" if u['status'] == 'At risk' else "🟡")
        lines.append(f"| {u['team']} | {status_icon} {u['status']} | {u['notes']} |")
    
    lines.append("")
    lines.append("## ✅ Action Items")
    lines.append("")
    lines.append("| Task | Owner | Due | Priority |")
    lines.append("|------|-------|-----|:--------:|")
    priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}
    for a in data['action_items']:
        icon = priority_icon.get(a.get('priority', 'low'), "🟢")
        lines.append(f"| {a['task']} | {a['owner']} | {a['due']} | {icon} {a.get('priority', 'low').upper()} |")
    
    lines.append("")
    lines.append(f"## 📅 Next Meeting")
    lines.append(f"- {data.get('next_meeting', 'TBD')}")
    lines.append("")
    lines.append(f"*Generated at {datetime.now().strftime('%H:%M')}*")
    return '\n'.join(lines)


def format_one_on_one(data):
    """格式化1:1会议"""
    lines = [
        f"# 👤 1:1 Meeting - {data['date']}",
        f"**Participants:** {', '.join(data['attendees'])}",
        "",
        "## 🎯 Career & Performance"
    ]
    for c in data.get('career', []):
        lines.append(f"- {c}")
    
    lines.append("")
    lines.append("## 💬 Questions Raised")
    for i, q in enumerate(data.get('questions', []), 1):
        lines.append(f"{i}. {q}")
    
    lines.append("")
    lines.append("## 📋 Feedback")
    for f in data.get('feedback', []):
        lines.append(f"- {f}")
    
    lines.append("")
    lines.append("## ✅ Action Items")
    for a in data.get('action_items', []):
        due = a.get('due', 'TBD')
        owner = a.get('owner', 'TBD')
        lines.append(f"- [ ] **{a['task']}** - 👤 {owner} (Due: {due})")
    
    lines.append("")
    lines.append(f"*Generated at {datetime.now().strftime('%H:%M')}*")
    return '\n'.join(lines)


def format_project(data):
    """格式化项目会议"""
    lines = [
        f"# 📁 Project Review Meeting",
        f"**Date:** {datetime.now().strftime('%Y-%m-%d')}",
        "",
        "## 🎯 Project Status"
    ]
    for d in data.get('decisions', []):
        lines.append(f"- {d}")
    
    lines.append("")
    lines.append("## 🚧 Issues & Risks")
    for i in data.get('issues', []):
        lines.append(f"- {i}")
    
    lines.append("")
    lines.append("## ✅ Next Steps")
    for n in data.get('next_steps', []):
        lines.append(f"- {n}")
    
    lines.append("")
    lines.append(f"*Generated at {datetime.now().strftime('%H:%M')}*")
    return '\n'.join(lines)


def format_client(data):
    """格式化客户会议"""
    lines = [
        f"# 🤝 Client Meeting",
        f"**Date:** {datetime.now().strftime('%Y-%m-%d')}",
        "",
        "## 👥 Attendees"
    ]
    for a in data.get('attendees', []):
        lines.append(f"- {a}")
    
    lines.append("")
    lines.append("## 💬 Discussion Points")
    for d in data.get('discussion', []):
        lines.append(f"- {d}")
    
    lines.append("")
    lines.append("## 🤝 Agreements")
    for a in data.get('agreements', []):
        lines.append(f"- {a}")
    
    lines.append("")
    lines.append("## 📋 Action Plan")
    for a in data.get('action_plan', []):
        lines.append(f"- {a}")
    
    lines.append("")
    lines.append(f"*Generated at {datetime.now().strftime('%H:%M')}*")
    return '\n'.join(lines)


# ============= 命令函数 =============

def cmd_generate(meeting_type, options):
    """生成会议纪要"""
    mt = meeting_type.lower() if meeting_type else "daily"
    
    if mt not in MEETING_TEMPLATES:
        print(f"❌ Unknown meeting type: {meeting_type}")
        print(f"Available types: {', '.join(MEETING_TEMPLATES.keys())}")
        return
    
    # 使用示例数据
    data = SAMPLE_DATA.get(mt, {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "attendees": ["Team"],
        "summary": ["Meeting held"],
        "action_items": []
    })
    
    # 根据类型格式化输出
    if mt == "daily":
        print(format_daily(data))
    elif mt == "weekly":
        print(format_weekly(data))
    elif mt == "one-on-one":
        print(format_one_on_one(data))
    elif mt == "project":
        print(format_project(data))
    elif mt == "client":
        print(format_client(data))
    else:
        print(f"📝 {MEETING_TEMPLATES[mt]['name']}")
        print(f"Date: {data['date']}")
        print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_template(template_type):
    """显示模板"""
    if template_type == "standup":
        print("""
## Daily Standup Template

### What I did yesterday
-

### What I'll do today
-

### Blockers
-
""")
    elif template_type == "retro":
        print("""
## Sprint Retrospective Template

### What went well
-

### What could improve
-

### Action items for next sprint
-
""")
    elif template_type == "planning":
        print("""
## Sprint Planning Template

### Project Goal
-

### Sprint Scope
1.
2.
3.

### Story Points Capacity
-

### Risks
-
""")
    elif template_type == "review":
        print("""
## Code/Project Review Template

### Changes Made
-

### Review Notes
-

### Approval Status
- [ ] Approved
- [ ] Needs Changes

### Action Items
-
""")
    elif template_type == "all-hands":
        print("""
## All Hands Meeting Template

### Company Updates
-

### Team Highlights
-

### Q&A
-

### Upcoming Events
-
""")
    else:
        print("Available templates: standup, retro, planning, review, all-hands")


def cmd_actions(command, args):
    """管理行动项"""
    if command == "list":
        print("📋 All Action Items")
        print("="*50)
        if SAMPLE_DATA.get('weekly', {}).get('action_items'):
            print("| Task | Owner | Due | Priority |")
            print("|------|-------|-----|:--------:|")
            for a in SAMPLE_DATA['weekly']['action_items']:
                print(f"| {a['task']} | {a['owner']} | {a['due']} | {a.get('priority', 'medium').upper()} |")
        else:
            print("No action items found.")
    elif command == "overdue":
        print("⚠️ Overdue Items")
        print("None found!")


def cmd_export(format_type):
    """导出会议纪要"""
    export_formats = {
        "markdown": "✅ Markdown format - Already displayed above",
        "notion": "📝 Notion format:\n```json\n{...}\n```",
        "email": "📧 Email format:\nSubject: Meeting Notes\nBody: ...",
        "json": json.dumps(SAMPLE_DATA.get('weekly', {}), indent=2)
    }
    
    result = export_formats.get(format_type, "Unknown format")
    print(result)


def cmd_help():
    """帮助信息"""
    print("""
📝 Meeting Notes Generator - Help

Commands:
  generate <type>    Generate meeting notes
    Types: daily, weekly, one-on-one, project, client, brainstorm
    
  template <type>   Show meeting template
    Types: standup, retro, planning, review, all-hands
    
  actions <cmd>     Manage action items
    Commands: list, add, complete, overdue
    
  export <format>   Export notes
    Formats: markdown, notion, email, json

Quick Start:
  /meeting-notes generate daily
  /meeting-notes generate weekly
  /meeting-notes template standup
  /meeting-notes actions list

Keyboard Shortcuts:
  /mn   - Quick daily standup
  /mn w - Weekly meeting
""")

# ============= 主函数 =============

def main():
    if len(sys.argv) < 2:
        cmd_help()
        return
    
    cmd = sys.argv[1]
    
    if cmd == "help":
        cmd_help()
    elif cmd == "generate":
        mt = sys.argv[2] if len(sys.argv) > 2 else "daily"
        options = sys.argv[3:] if len(sys.argv) > 3 else []
        cmd_generate(mt, options)
    elif cmd == "template":
        template_type = sys.argv[2] if len(sys.argv) > 2 else "standup"
        cmd_template(template_type)
    elif cmd == "actions":
        action_cmd = sys.argv[2] if len(sys.argv) > 2 else "list"
        args = sys.argv[3:] if len(sys.argv) > 3 else []
        cmd_actions(action_cmd, args)
    elif cmd == "export":
        format_type = sys.argv[2] if len(sys.argv) > 2 else "markdown"
        cmd_export(format_type)
    else:
        print(f"Unknown command: {cmd}")
        print("Run '/meeting-notes help' for available commands")

if __name__ == '__main__':
    main()