#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📋 Meeting Assistant - 会议助手（优化版）
功能：会议纪要、待办事项、日程安排、会议模板、语音转文字
"""

import json
import re
from pathlib import Path
from datetime import datetime, timedelta

DATA_DIR = Path(__file__).parent
MEETINGS_FILE = DATA_DIR / "meetings.json"
TASKS_FILE = DATA_DIR / "tasks.json"

# ========== 会议模板 ==========

MEETING_TEMPLATES = {
    "周会": {
        "title": "周会纪要",
        "duration": 60,
        "attendees": ["团队成员"],
        "agenda": [
            "上周工作回顾",
            "本周工作计划",
            "问题和困难",
            "其他事项"
        ]
    },
    "项目启动": {
        "title": "项目启动会",
        "duration": 90,
        "attendees": ["项目经理", "团队成员", "相关方"],
        "agenda": [
            "项目背景介绍",
            "项目目标",
            "项目计划",
            "角色分工",
            "风险评估"
        ]
    },
    "评审会": {
        "title": "项目评审会",
        "duration": 60,
        "attendees": ["项目经理", "评审专家", "团队成员"],
        "agenda": [
            "项目成果展示",
            "问题质询",
            "评审意见",
            "改进建议"
        ]
    },
    "头脑风暴": {
        "title": "头脑风暴会议",
        "duration": 90,
        "attendees": ["创意团队"],
        "agenda": [
            "主题介绍",
            "自由发散",
            "想法整理",
            "方案评估"
        ]
    }
}

# ========== 会议纪要模板 ==========

MINUTES_TEMPLATE = """
# 📋 {title}

## 📅 会议信息
- **时间**：{date}
- **地点**：{location}
- **主持**：{host}
- **记录**：{recorder}
- **参会**：{attendees}
- **缺席**：{absent}

## 📝 会议议程
{agenda}

## 💬 讨论要点
{discussion}

## ✅ 决议事项
{decisions}

## 📋 待办事项
{action_items}

## 📅 下次会议
- **时间**：{next_meeting_time}
- **议题**：{next_meeting_agenda}

---
*纪要生成时间：{generated_time}*
"""


def load_json(filepath):
    """加载 JSON 文件"""
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"meetings": [], "tasks": []}


def save_json(filepath, data):
    """保存 JSON 文件"""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def generate_meeting_id():
    """生成会议 ID"""
    return f"mtg_{datetime.now().strftime('%Y%m%d%H%M%S')}"


def create_meeting(title, date_time=None, duration=60, attendees=None, location="线上", template=None):
    """创建会议"""
    data = load_json(MEETINGS_FILE)
    
    if date_time is None:
        date_time = datetime.now().isoformat()
    
    meeting = {
        "id": generate_meeting_id(),
        "title": title,
        "date_time": date_time,
        "duration": duration,
        "location": location,
        "attendees": attendees or [],
        "template": template,
        "status": "scheduled",  # scheduled/completed/cancelled
        "created": datetime.now().isoformat()
    }
    
    data["meetings"].append(meeting)
    save_json(MEETINGS_FILE, data)
    
    return meeting


def update_meeting_status(meeting_id, status, notes=None, action_items=None):
    """更新会议状态"""
    data = load_json(MEETINGS_FILE)
    
    for meeting in data["meetings"]:
        if meeting["id"] == meeting_id:
            meeting["status"] = status
            if notes:
                meeting["notes"] = notes
            if action_items:
                meeting["action_items"] = action_items
            meeting["updated"] = datetime.now().isoformat()
            save_json(MEETINGS_FILE, data)
            return True
    
    return False


def generate_minutes(title, content, attendees=None, host="未指定", location="未指定"):
    """
    生成会议纪要（智能解析）
    
    Args:
        title: 会议主题
        content: 会议内容
        attendees: 参会人员
        host: 主持人
        location: 地点
    """
    data = load_json(MEETINGS_FILE)
    
    # 智能解析内容
    parsed = parse_meeting_content(content)
    
    meeting = {
        "id": generate_meeting_id(),
        "title": title,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "host": host,
        "location": location,
        "attendees": attendees or parsed.get("attendees", []),
        "absent": parsed.get("absent", []),
        "agenda": parsed.get("agenda", []),
        "discussion": parsed.get("discussion", ""),
        "decisions": parsed.get("decisions", []),
        "action_items": parsed.get("action_items", []),
        "next_meeting": parsed.get("next_meeting", {}),
        "created": datetime.now().isoformat()
    }
    
    data["meetings"].append(meeting)
    save_json(MEETINGS_FILE, data)
    
    return meeting


def parse_meeting_content(content):
    """
    智能解析会议内容
    
    从内容中提取：
    - 参会人员
    - 议程
    - 讨论要点
    - 决议事项
    - 待办事项
    """
    result = {
        "attendees": [],
        "absent": [],
        "agenda": [],
        "discussion": "",
        "decisions": [],
        "action_items": [],
        "next_meeting": {}
    }
    
    lines = content.split('\n')
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 识别段落
        if "参会" in line or "出席" in line:
            current_section = "attendees"
            # 提取人名
            names = re.findall(r'[\u4e00-\u9fa5]{2,4}', line)
            result["attendees"].extend(names)
        elif "缺席" in line or "请假" in line:
            current_section = "absent"
            names = re.findall(r'[\u4e00-\u9fa5]{2,4}', line)
            result["absent"].extend(names)
        elif "议程" in line or "流程" in line:
            current_section = "agenda"
        elif "待办" in line or "任务" in line or "TODO" in line:
            current_section = "action_items"
            # 提取待办
            if re.search(r'[-•*]\s*\[?\s*\]?\s*', line):
                task = re.sub(r'^[-•*]\s*\[?\s*\]?\s*', '', line)
                result["action_items"].append(task)
        elif "决议" in line or "决定" in line:
            current_section = "decisions"
            if re.search(r'[-•*]', line):
                decision = re.sub(r'^[-•*]\s*', '', line)
                result["decisions"].append(decision)
        elif "下次" in line or "下一次" in line:
            current_section = "next_meeting"
            # 提取时间
            time_match = re.search(r'(\d{1,2}月 \d{1,2}日|\d{4}-\d{2}-\d{2})', line)
            if time_match:
                result["next_meeting"]["time"] = time_match.group(1)
        else:
            # 添加到讨论内容
            if current_section == "agenda" and re.search(r'^\d+[\.,]', line):
                result["agenda"].append(line)
            elif current_section == "discussion":
                result["discussion"] += line + "\n"
    
    # 如果没有明确段落，整个内容作为讨论要点
    if not result["discussion"] and not result["agenda"]:
        result["discussion"] = content
    
    return result


def extract_action_items(text):
    """提取待办事项（增强版）"""
    action_items = []
    lines = text.split('\n')
    
    keywords = ['待办', '需要', '负责', '完成', '截止', '任务', 'TODO', 'Action']
    
    for line in lines:
        line = line.strip()
        if any(kw in line for kw in keywords):
            # 清理格式
            task = re.sub(r'^[-•*]\s*\[?\s*\]?\s*', '', line)
            action_items.append(task)
    
    return action_items


def get_meeting_templates():
    """获取会议模板"""
    return MEETING_TEMPLATES


def get_upcoming_meetings(days=7):
    """获取未来 N 天的会议"""
    data = load_json(MEETINGS_FILE)
    now = datetime.now()
    future = now + timedelta(days=days)
    
    upcoming = []
    for meeting in data["meetings"]:
        if meeting.get("status") != "scheduled":
            continue
        
        meeting_time = datetime.fromisoformat(meeting["date_time"])
        if now <= meeting_time <= future:
            upcoming.append(meeting)
    
    upcoming.sort(key=lambda x: x["date_time"])
    
    return upcoming


def get_meeting_stats():
    """获取会议统计"""
    data = load_json(MEETINGS_FILE)
    meetings = data.get("meetings", [])
    
    stats = {
        "total": len(meetings),
        "scheduled": sum(1 for m in meetings if m.get("status") == "scheduled"),
        "completed": sum(1 for m in meetings if m.get("status") == "completed"),
        "cancelled": sum(1 for m in meetings if m.get("status") == "cancelled"),
        "this_week": 0,
        "this_month": 0
    }
    
    now = datetime.now()
    week_start = now - timedelta(days=now.weekday())
    month_start = now.replace(day=1)
    
    for meeting in meetings:
        # 兼容 date_time 和 date 字段
        date_str = meeting.get("date_time") or meeting.get("date")
        if not date_str:
            continue
        
        try:
            if "T" in date_str:
                meeting_time = datetime.fromisoformat(date_str)
            else:
                meeting_time = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        except:
            continue
        
        if meeting_time >= week_start:
            stats["this_week"] += 1
        if meeting_time >= month_start:
            stats["this_month"] += 1
    
    return stats


def format_meeting(meeting):
    """格式化会议信息"""
    response = f"📋 **{meeting['title']}**\n"
    response += f"📅 {meeting.get('date_time', meeting.get('date', '未定'))}\n"
    
    if meeting.get("location"):
        response += f"📍 {meeting['location']}\n"
    
    if meeting.get("attendees"):
        response += f"👥 {'、'.join(meeting['attendees'])}\n"
    
    response += f"📊 状态：{meeting.get('status', '未知')}\n"
    
    return response


def format_minutes(meeting):
    """格式化会议纪要"""
    response = f"📋 **会议纪要** - {meeting['title']}\n\n"
    response += f"📅 时间：{meeting.get('date', meeting.get('date_time', '未定'))}\n"
    
    if meeting.get("host"):
        response += f"👤 主持：{meeting['host']}\n"
    
    if meeting.get("location"):
        response += f"📍 地点：{meeting['location']}\n"
    
    if meeting.get("attendees"):
        response += f"👥 参会：{'、'.join(meeting['attendees'])}\n"
    
    if meeting.get("absent"):
        response += f"❌ 缺席：{'、'.join(meeting['absent'])}\n"
    
    response += "\n"
    
    if meeting.get("agenda"):
        response += "📝 **议程**\n"
        for item in meeting["agenda"]:
            response += f"{item}\n"
        response += "\n"
    
    if meeting.get("discussion"):
        response += "💬 **讨论要点**\n"
        response += f"{meeting['discussion']}\n\n"
    
    if meeting.get("decisions"):
        response += "✅ **决议事项**\n"
        for decision in meeting["decisions"]:
            response += f"- {decision}\n"
        response += "\n"
    
    if meeting.get("action_items"):
        response += "📋 **待办事项**\n"
        for item in meeting["action_items"]:
            response += f"- [ ] {item}\n"
        response += "\n"
    
    if meeting.get("next_meeting"):
        response += "📅 **下次会议**\n"
        if meeting["next_meeting"].get("time"):
            response += f"时间：{meeting['next_meeting']['time']}\n"
        if meeting["next_meeting"].get("agenda"):
            response += f"议题：{meeting['next_meeting']['agenda']}\n"
    
    return response


def main(query):
    """主函数"""
    query_lower = query.lower()
    
    # ========== 创建会议 ==========
    
    if "安排会议" in query_lower or "创建会议" in query_lower:
        # 简单实现
        return """📋 **会议安排**

请提供以下信息：
1. 会议主题
2. 会议时间
3. 参会人员
4. 会议地点

例如：「安排明天下午 3 点的项目会议，参加人有张三、李四、王五，地点会议室 A」"""
    
    # ========== 会议纪要 ==========
    
    if "纪要" in query_lower or "整理会议" in query_lower:
        # 检查是否有会议内容
        if len(query) > 50:
            # 有内容，生成纪要
            meeting = generate_minutes(
                title="会议纪要",
                content=query,
                host="未指定"
            )
            return format_minutes(meeting)
        else:
            # 无内容，返回模板
            return """📋 **会议纪要模板**

**会议主题：** [填写]
**会议时间：** [填写]
**会议地点：** [填写]
**主持人：** [填写]
**记录人：** [填写]

**参会人员：** [填写]
**缺席人员：** [填写]

**会议议程：**
1. [议程 1]
2. [议程 2]

**讨论要点：**
[详细记录讨论内容]

**决议事项：**
- [决议 1]
- [决议 2]

**待办事项：**
- [ ] [任务 1] - [负责人] - [截止日期]
- [ ] [任务 2] - [负责人] - [截止日期]

**下次会议：**
- 时间：[填写]
- 议题：[填写]

把会议内容发给我，我帮你智能整理！👻"""
    
    # ========== 会议模板 ==========
    
    if "模板" in query_lower:
        templates = get_meeting_templates()
        response = "📋 **会议模板**\n\n"
        for name, template in templates.items():
            response += f"**{name}**\n"
            response += f"时长：{template['duration']}分钟\n"
            response += f"议程：{' → '.join(template['agenda'][:3])}...\n\n"
        return response
    
    # ========== 查看会议 ==========
    
    # 即将到来的会议
    if " upcoming" in query_lower or "即将" in query_lower or "下周会议" in query_lower:
        days = 7
        if "周" in query_lower:
            days = 7
        elif "月" in query_lower:
            days = 30
        
        meetings = get_upcoming_meetings(days)
        if not meetings:
            return f"📅 未来{days}天暂无会议安排"
        
        response = f"📅 **未来{days}天的会议** ({len(meetings)}个)\n\n"
        for meeting in meetings:
            response += format_meeting(meeting) + "\n"
        return response
    
    # 会议列表
    if "列表" in query_lower or "所有会议" in query_lower:
        data = load_json(MEETINGS_FILE)
        if not data["meetings"]:
            return "📋 暂无会议记录"
        
        response = "📋 **会议列表**\n\n"
        for meeting in data["meetings"][-10:]:
            response += format_meeting(meeting) + "\n"
        return response
    
    # ========== 会议统计 ==========
    
    if "统计" in query_lower or "总结" in query_lower:
        stats = get_meeting_stats()
        response = "📊 **会议统计**\n\n"
        response += f"总计：{stats['total']}个\n"
        response += f"待召开：{stats['scheduled']}个\n"
        response += f"已完成：{stats['completed']}个\n"
        response += f"已取消：{stats['cancelled']}个\n"
        response += f"本周：{stats['this_week']}个\n"
        response += f"本月：{stats['this_month']}个\n"
        return response
    
    # ========== 待办提取 ==========
    
    if "待办" in query_lower or "任务" in query_lower:
        if len(query) > 50:
            # 有内容，提取待办
            action_items = extract_action_items(query)
            if action_items:
                response = "📋 **提取的待办事项**\n\n"
                for item in action_items:
                    response += f"- [ ] {item}\n"
                return response
            return "😅 未找到待办事项"
        else:
            return "📋 请提供会议内容，我帮你提取待办事项"
    
    # ========== 默认回复 ==========
    
    return """📋 会议助手（优化版）

**功能**：

📅 会议管理
1. 创建会议 - "安排明天下午 3 点的会议"
2. 查看会议 - "下周有什么会议"
3. 会议列表 - "所有会议记录"

📝 会议纪要
4. 生成纪要 - "整理会议纪要"（附内容）
5. 会议模板 - "会议模板"

✅ 待办管理
6. 提取待办 - "从内容中提取待办"
7. 待办列表 - "查看待办事项"

📊 会议统计
8. 会议统计 - "本周会议统计"

**模板类型**：周会、项目启动、评审会、头脑风暴

发送会议内容，我帮你智能整理！👻"""


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    
    print("=" * 60)
    print("📋 会议助手 - 测试")
    print("=" * 60)
    
    print("\n测试 1: 会议模板")
    print(main("会议模板"))
    
    print("\n" + "=" * 60)
    print("测试 2: 会议纪要")
    test_content = """
    参会人员：张三、李四、王五
    议程：
    1. 上周工作回顾
    2. 本周工作计划
    3. 问题讨论
    
    讨论内容：
    张三完成了项目 A 的开发，李四负责测试，王五负责部署。
    需要解决的问题：服务器资源不足。
    
    待办事项：
    - 张三完成项目 A 的文档
    - 李四负责测试报告
    - 王五负责申请服务器资源
    
    下次会议：下周一上午 10 点
    """
    print(main(f"整理会议纪要 {test_content}"))
    
    print("\n" + "=" * 60)
    print("测试 3: 会议统计")
    print(main("会议统计"))
