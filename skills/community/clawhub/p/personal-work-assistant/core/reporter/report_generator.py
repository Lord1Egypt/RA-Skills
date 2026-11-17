import datetime

class ReportGenerator:
    def __init__(self, config):
        self.config = config
        self.user_name = config.get('user', {}).get('name', 'Azusa')

    def generate_markdown_report(self, active_tasks, closed_tasks, announcements):
        """
        生成极致极简、行动导向的个人工作晨报
        """
        now = datetime.datetime.now()
        date_str = now.strftime('%Y-%m-%d')
        
        # 分组任务
        urgent_pending = []
        in_progress = []
        
        for t in active_tasks:
            # 计算停留天数
            first_seen = datetime.datetime.strptime(t['first_seen_at'], '%Y-%m-%d %H:%M:%S')
            days = (now - first_seen).days
            t['days_open'] = days
            
            if t['priority'] in ['urgent', 'high'] or t['status'] == 'pending' or t.get('due_date'):
                urgent_pending.append(t)
            else:
                in_progress.append(t)

        lines = []
        lines.append(f"📋 **【{self.user_name}】个人工作晨报 | {date_str}**\n")

        # 1. 今日需处理 / 待决策
        lines.append("### 🔴 今日需我处理 / 待决策")
        if urgent_pending:
            for i, t in enumerate(urgent_pending, 1):
                due_info = f" ⏰ 截止: {t['due_date']}" if t.get('due_date') else ""
                days_info = f" `[已跟进 {t['days_open']} 天]`" if t['days_open'] > 0 else ""
                lines.append(f"{i}. **{t['title']}**{due_info}{days_info}")
                lines.append(f"   - **来源**：{t['source_name']}")
                if t.get('detail'):
                    lines.append(f"   - **详情**：{t['detail']}")
                if t.get('resolution_note'):
                    lines.append(f"   - **最新进展**：{t['resolution_note']}")
        else:
            lines.append("暂无高优先级待处理事项，状态良好 ✨")
        lines.append("")

        # 2. 进行中 / 持续推进
        lines.append("### 🟡 进行中 / 持续推进")
        if in_progress:
            for i, t in enumerate(in_progress, 1):
                days_info = f" `[第 {t['days_open'] + 1} 天]`"
                lines.append(f"{i}. **{t['title']}** ({t['source_name']}){days_info}")
                if t.get('detail'):
                    lines.append(f"   - **内容**：{t['detail']}")
                if t.get('resolution_note'):
                    lines.append(f"   - **进展**：{t['resolution_note']}")
        else:
            lines.append("暂无长线推进中事项。")
        lines.append("")

        # 3. 近期已闭环 / 已解决
        lines.append("### 🟢 近期已闭环 / 已解决")
        if closed_tasks:
            for i, t in enumerate(closed_tasks, 1):
                closed_time = t.get('closed_at', '')[11:16] if t.get('closed_at') else ''
                lines.append(f"{i}. **{t['title']}** ({t['source_name']}) ✅ {closed_time}")
                if t.get('resolution_note'):
                    lines.append(f"   - **闭环说明**：{t['resolution_note']}")
        else:
            lines.append("近 24 小时暂无新闭环事项。")
        lines.append("")

        # 4. 全员通知 / 需知悉
        if announcements:
            lines.append("### 📢 需知悉通知")
            for i, a in enumerate(announcements, 1):
                lines.append(f"{i}. **[{a['source_name']}]** {a['content']}")
            lines.append("")

        return "\n".join(lines)
