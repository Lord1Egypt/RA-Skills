"""
Hermes Workflow Auto-Trigger v1.0
六模式自动触发系统 — 关键词/意图/工具序列/时间规律/历史模式/事件驱动
"""

import re
import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter, defaultdict


# ─── 意图分类器 ─────────────────────────────────────────────

INTENT_PATTERNS = {
    'news_report': {
        'keywords': ['新闻', 'news', '速报', '日报', '早报', '晚报', '资讯', '动态', '热点'],
        'phrases': ['今天有什么', '最新消息', 'AI新闻', '行业动态', '帮我搜.*新闻'],
        'workflow': 'ai-news-daily',
        'confidence_boost': 0.2,
    },
    'research': {
        'keywords': ['调研', '研究', '分析', 'research', '深入了解', '全面研究', '深度'],
        'phrases': ['帮我研究一下', '深入分析', '做个调研', '了解一下', '分析一下'],
        'workflow': 'auto-research',
        'confidence_boost': 0.1,
    },
    'content_creation': {
        'keywords': ['写文章', '公众号', '推文', '撰写', '创作', '写报告', '写一篇'],
        'phrases': ['帮我写', '写个公众号', '发公众号', '公众号文章', '写篇文章'],
        'workflow': 'auto-content',
        'confidence_boost': 0.2,
    },
    'data_analysis': {
        'keywords': ['数据', 'Excel', '报表', '统计', '图表', '可视化', '分析数据'],
        'phrases': ['分析一下数据', '做个图表', '生成报表', '数据可视化'],
        'workflow': 'auto-data',
        'confidence_boost': 0.1,
    },
    'deployment': {
        'keywords': ['部署', 'deploy', '上线', '发布', '部署到'],
        'phrases': ['帮我部署', '发布到', '上线到'],
        'workflow': 'auto-deploy',
        'confidence_boost': 0.2,
    },
    'monitoring': {
        'keywords': ['检查', '巡检', '状态', '监控', '健康检查', 'health'],
        'phrases': ['检查一下', '看看状态', '系统巡检', '运行正常吗'],
        'workflow': 'auto-monitor',
        'confidence_boost': 0.1,
    },
    'backup': {
        'keywords': ['备份', 'backup', '同步', '迁移', '导出'],
        'phrases': ['帮我备份', '同步一下', '导出数据'],
        'workflow': 'auto-backup',
        'confidence_boost': 0.15,
    },
    'image_gen': {
        'keywords': ['图片', '生成图', '封面', '海报', '信息图', 'infographic'],
        'phrases': ['生成一张图', '做个封面', '设计海报', '生成信息图'],
        'workflow': 'auto-image',
        'confidence_boost': 0.15,
    },
    'email': {
        'keywords': ['邮件', 'email', '邮箱', '发邮件', '查邮件'],
        'phrases': ['帮我发邮件', '查一下邮件', '发送邮件'],
        'workflow': 'auto-email',
        'confidence_boost': 0.2,
    },
    'code_review': {
        'keywords': ['代码', 'review', '审查', 'PR', 'pull request', '代码质量'],
        'phrases': ['帮我看看代码', '审查一下', 'review这个PR'],
        'workflow': 'auto-code-review',
        'confidence_boost': 0.15,
    },
}


class IntentClassifier:
    """意图分类器 — 分析用户消息匹配工作流"""

    def __init__(self):
        self.intent_cache = {}

    def classify(self, message: str) -> list:
        """分类用户消息，返回匹配的意图列表"""
        message_lower = message.lower()
        results = []

        for intent, config in INTENT_PATTERNS.items():
            score = 0
            matched_by = []

            # 关键词匹配
            for kw in config['keywords']:
                if kw.lower() in message_lower:
                    score += 0.3
                    matched_by.append(f'keyword:{kw}')

            # 短语匹配
            for phrase in config['phrases']:
                if re.search(phrase, message, re.IGNORECASE):
                    score += 0.4
                    matched_by.append(f'phrase:{phrase}')

            # 置信度提升
            if score > 0:
                score += config.get('confidence_boost', 0)

            # 限制在0-1范围
            score = min(score, 1.0)

            if score >= 0.3:
                results.append({
                    'intent': intent,
                    'confidence': round(score, 2),
                    'workflow': config['workflow'],
                    'matched_by': matched_by,
                })

        # 按置信度排序
        results.sort(key=lambda x: x['confidence'], reverse=True)
        return results


# ─── 工具序列检测器 ─────────────────────────────────────────

TOOL_SEQUENCES = {
    ('web_search', 'write_file', 'terminal'): {
        'name': '搜索→写文件→执行',
        'workflow': 'auto-search-write-execute',
        'min_occurrences': 2,
    },
    ('web_search', 'send_message'): {
        'name': '搜索→发送',
        'workflow': 'auto-search-send',
        'min_occurrences': 2,
    },
    ('read_file', 'write_file'): {
        'name': '读取→写入',
        'workflow': 'auto-transform',
        'min_occurrences': 3,
    },
    ('browser', 'write_file', 'send_message'): {
        'name': '浏览→写入→发送',
        'workflow': 'auto-browse-report',
        'min_occurrences': 2,
    },
    ('terminal', 'terminal', 'terminal'): {
        'name': '连续执行命令',
        'workflow': 'auto-pipeline',
        'min_occurrences': 2,
    },
}


class ToolSequenceDetector:
    """工具序列检测器 — 检测连续使用特定工具组合"""

    def __init__(self):
        self.tool_history = []

    def record_tool(self, tool_name: str):
        """记录工具使用"""
        self.tool_history.append({
            'tool': tool_name,
            'timestamp': datetime.now().isoformat(),
        })
        # 只保留最近50个
        if len(self.tool_history) > 50:
            self.tool_history = self.tool_history[-50:]

    def detect_sequences(self) -> list:
        """检测匹配的工具序列"""
        if len(self.tool_history) < 2:
            return []

        results = []
        tools = [t['tool'] for t in self.tool_history]

        # 检查最近的工具序列
        for seq_len in range(2, min(6, len(tools) + 1)):
            recent = tuple(tools[-seq_len:])
            for pattern, config in TOOL_SEQUENCES.items():
                if recent == pattern:
                    results.append({
                        'sequence': list(pattern),
                        'name': config['name'],
                        'workflow': config['workflow'],
                        'confidence': 0.7,
                    })

        return results

    def get_tool_frequency(self) -> dict:
        """获取工具使用频率"""
        counter = Counter(t['tool'] for t in self.tool_history)
        return dict(counter.most_common(10))


# ─── 时间规律检测器 ─────────────────────────────────────────

class TimePatternDetector:
    """时间规律检测器 — 发现固定时间做固定事的模式"""

    def __init__(self, schedule_file: str = None):
        self.schedule_file = schedule_file or str(
            Path.home() / '.hermes' / 'workflow-engine' / 'schedules.json'
        )
        self.schedules = self._load_schedules()

    def _load_schedules(self) -> dict:
        if Path(self.schedule_file).exists():
            return json.loads(Path(self.schedule_file).read_text())
        return {}

    def _save_schedules(self):
        Path(self.schedule_file).write_text(
            json.dumps(self.schedules, ensure_ascii=False, indent=2)
        )

    def record_execution(self, workflow_name: str):
        """记录工作流执行时间"""
        now = datetime.now()
        if workflow_name not in self.schedules:
            self.schedules[workflow_name] = []

        self.schedules[workflow_name].append({
            'executed_at': now.isoformat(),
            'hour': now.hour,
            'minute': now.minute,
            'weekday': now.weekday(),
        })

        # 只保留最近30次
        if len(self.schedules[workflow_name]) > 30:
            self.schedules[workflow_name] = self.schedules[workflow_name][-30:]

        self._save_schedules()

    def detect_patterns(self) -> list:
        """检测时间规律"""
        results = []

        for wf_name, executions in self.schedules.items():
            if len(executions) < 2:
                continue

            # 分析时间分布
            hours = [e['hour'] for e in executions]
            weekdays = [e['weekday'] for e in executions]

            # 检查是否有固定时间
            hour_counter = Counter(hours)
            most_common_hour, hour_count = hour_counter.most_common(1)[0]

            if hour_count >= len(executions) * 0.6:  # 60%以上在同一小时
                results.append({
                    'workflow': wf_name,
                    'pattern': f'每天{most_common_hour}点执行',
                    'confidence': round(hour_count / len(executions), 2),
                    'suggested_cron': f'0 {most_common_hour} * * *',
                    'executions': len(executions),
                })

            # 检查是否有固定星期
            weekday_counter = Counter(weekdays)
            most_common_day, day_count = weekday_counter.most_common(1)[0]

            if day_count >= len(executions) * 0.6:
                day_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
                results.append({
                    'workflow': wf_name,
                    'pattern': f'每{day_names[most_common_day]}执行',
                    'confidence': round(day_count / len(executions), 2),
                    'suggested_cron': f'0 {most_common_hour} * * {most_common_day}',
                    'executions': len(executions),
                })

        return results

    def should_auto_execute(self) -> list:
        """检查当前是否有工作流应该自动执行"""
        now = datetime.now()
        should_run = []

        for pattern in self.detect_patterns():
            if pattern['confidence'] >= 0.7:
                cron = pattern['suggested_cron']
                # 简单解析cron（只检查小时）
                parts = cron.split()
                if len(parts) >= 2 and parts[1].isdigit():
                    target_hour = int(parts[1])
                    if now.hour == target_hour and now.minute < 15:
                        should_run.append({
                            'workflow': pattern['workflow'],
                            'reason': pattern['pattern'],
                            'confidence': pattern['confidence'],
                        })

        return should_run


# ─── 历史模式检测器 ─────────────────────────────────────────

class HistoryPatternDetector:
    """历史模式检测器 — 从session历史发现重复模式"""

    def __init__(self, sessions_dir: str = None):
        self.sessions_dir = sessions_dir or str(
            Path.home() / '.hermes' / 'data' / 'sessions'
        )

    def scan_and_detect(self, days: int = 7, min_occurrences: int = 2) -> list:
        """扫描历史session发现重复模式"""
        sessions_path = Path(self.sessions_dir)
        if not sessions_path.exists():
            return []

        # 读取最近N天的session
        cutoff = datetime.now() - timedelta(days=days)
        session_data = []

        for f in sessions_path.glob('*.json'):
            try:
                mtime = datetime.fromtimestamp(f.stat().st_mtime)
                if mtime >= cutoff:
                    data = json.loads(f.read_text())
                    session_data.append(data)
            except:
                continue

        if not session_data:
            return []

        # 提取任务模式
        task_counter = Counter()
        for data in session_data:
            messages = data.get('messages', [])
            user_msgs = [m.get('content', '') for m in messages if m.get('role') == 'user']
            user_text = ' '.join(user_msgs)

            # 匹配意图
            classifier = IntentClassifier()
            intents = classifier.classify(user_text)
            for intent in intents:
                task_counter[intent['intent']] += 1

        # 过滤高频模式
        results = []
        for task, count in task_counter.most_common():
            if count >= min_occurrences:
                config = INTENT_PATTERNS.get(task, {})
                results.append({
                    'task': task,
                    'count': count,
                    'workflow': config.get('workflow', f'auto-{task}'),
                    'description': config.get('keywords', [task])[0],
                    'confidence': min(count / len(session_data), 1.0),
                })

        return results


# ─── 事件驱动触发器 ─────────────────────────────────────────

EVENT_MAPPINGS = {
    'email_received': {
        'keywords': ['邮件', 'email'],
        'workflow': 'auto-email',
        'description': '收到邮件时触发',
    },
    'pr_opened': {
        'keywords': ['PR', 'pull request'],
        'workflow': 'auto-code-review',
        'description': '收到PR时触发',
    },
    'alert_fired': {
        'keywords': ['告警', 'alert', '错误'],
        'workflow': 'auto-monitor',
        'description': '收到告警时触发',
    },
    'schedule_reminder': {
        'keywords': ['提醒', 'reminder', '定时'],
        'workflow': 'auto-reminder',
        'description': '定时提醒触发',
    },
}


class EventTrigger:
    """事件驱动触发器"""

    def __init__(self):
        self.event_handlers = {}

    def register_event(self, event_type: str, workflow_name: str):
        """注册事件处理"""
        self.event_handlers[event_type] = workflow_name

    def match_event(self, event_type: str, event_data: dict = None) -> dict:
        """匹配事件到工作流"""
        if event_type in self.event_handlers:
            return {
                'matched': True,
                'workflow': self.event_handlers[event_type],
                'event': event_type,
                'data': event_data,
            }

        # 检查内置映射
        if event_type in EVENT_MAPPINGS:
            mapping = EVENT_MAPPINGS[event_type]
            return {
                'matched': True,
                'workflow': mapping['workflow'],
                'event': event_type,
                'description': mapping['description'],
            }

        return {'matched': False}


# ─── 触发器总控 ─────────────────────────────────────────────

class AutoTrigger:
    """六模式自动触发总控"""

    def __init__(self):
        self.intent_classifier = IntentClassifier()
        self.tool_detector = ToolSequenceDetector()
        self.time_detector = TimePatternDetector()
        self.history_detector = HistoryPatternDetector()
        self.event_trigger = EventTrigger()

    def analyze_message(self, message: str) -> dict:
        """分析用户消息，返回触发建议"""
        results = {
            'should_trigger': False,
            'confidence': 0,
            'suggestions': [],
            'mode': None,
        }

        # 模式1: 关键词匹配（在INTENT_PATTERNS中）
        intents = self.intent_classifier.classify(message)
        if intents:
            top = intents[0]
            if top['confidence'] >= 0.5:
                results['should_trigger'] = True
                results['confidence'] = top['confidence']
                results['mode'] = 'intent_match'
                results['suggestions'].append({
                    'workflow': top['workflow'],
                    'intent': top['intent'],
                    'confidence': top['confidence'],
                    'reason': f"检测到{top['intent']}意图",
                })

        # 模式2: 工具序列检测
        self.tool_detector.record_tool('user_message')
        sequences = self.tool_detector.detect_sequences()
        for seq in sequences:
            if seq['confidence'] >= 0.6:
                results['suggestions'].append({
                    'workflow': seq['workflow'],
                    'sequence': seq['sequence'],
                    'confidence': seq['confidence'],
                    'reason': f"检测到工具序列: {seq['name']}",
                })

        # 模式3: 时间规律
        time_patterns = self.time_detector.should_auto_execute()
        for tp in time_patterns:
            results['suggestions'].append({
                'workflow': tp['workflow'],
                'confidence': tp['confidence'],
                'reason': f"时间规律: {tp['reason']}",
            })

        # 模式4: 历史模式
        history = self.history_detector.scan_and_detect()
        for h in history:
            if h['confidence'] >= 0.5:
                results['suggestions'].append({
                    'workflow': h['workflow'],
                    'confidence': h['confidence'],
                    'reason': f"历史模式: {h['description']}({h['count']}次)",
                })

        # 去重并排序
        seen = set()
        unique_suggestions = []
        for s in results['suggestions']:
            key = s.get('workflow')
            if key not in seen:
                seen.add(key)
                unique_suggestions.append(s)
        results['suggestions'] = sorted(
            unique_suggestions,
            key=lambda x: x.get('confidence', 0),
            reverse=True
        )

        # 更新总置信度
        if results['suggestions']:
            results['should_trigger'] = True
            results['confidence'] = results['suggestions'][0].get('confidence', 0)

        return results

    def record_tool_use(self, tool_name: str):
        """记录工具使用"""
        self.tool_detector.record_tool(tool_name)

    def record_workflow_execution(self, workflow_name: str):
        """记录工作流执行"""
        self.time_detector.record_execution(workflow_name)

    def check_scheduled_workflows(self) -> list:
        """检查是否有应该自动执行的工作流"""
        return self.time_detector.should_auto_execute()

    def handle_event(self, event_type: str, event_data: dict = None) -> dict:
        """处理外部事件"""
        return self.event_trigger.match_event(event_type, event_data)


def format_trigger_analysis(analysis: dict) -> str:
    """格式化触发分析结果"""
    lines = [
        "═══ 触发分析 ═══",
        f"是否触发: {'✅ 是' if analysis['should_trigger'] else '❌ 否'}",
        f"置信度: {analysis['confidence']}",
        f"触发模式: {analysis.get('mode', '无')}",
    ]

    if analysis['suggestions']:
        lines.append("\n建议:")
        for i, s in enumerate(analysis['suggestions'][:3]):
            lines.append(f"  {i+1}. [{s.get('workflow')}] {s.get('reason')} (置信度: {s.get('confidence')})")

    return '\n'.join(lines)
