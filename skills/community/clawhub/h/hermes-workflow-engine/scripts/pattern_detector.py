"""
Hermes Workflow Pattern Detector v1.0
模式检测 — 扫描历史对话，发现重复任务，生成工作流提案
"""

import json
import re
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter, defaultdict


# ─── 任务关键词提取 ─────────────────────────────────────────

# 工具使用模式
TOOL_PATTERNS = {
    'web_search': ['搜索', 'search', '查找', '找一下', '查一下'],
    'baoyu-infographic': ['信息图', 'infographic', '可视化', '图表'],
    'wechat-article': ['公众号', '文章', '推文', 'wechat article'],
    'wechat-publisher': ['发布', 'publish', '草稿箱', '公众号发布'],
    'terminal': ['执行', '运行', 'run', '命令', '脚本'],
    'delegate_task': ['并行', 'parallel', '子任务', '同时做'],
    'browser': ['打开网页', '浏览', '截图', 'screenshot'],
    'read_file': ['读取', '查看文件', 'read'],
    'write_file': ['写入', '保存', '创建文件', 'write'],
}

# 任务类型模式
TASK_PATTERNS = {
    'news_report': ['新闻', 'news', '速报', '日报', '早报'],
    'research': ['调研', '研究', '分析', 'research', '深度研究'],
    'content_creation': ['写文章', '写报告', '创作', '撰写', '写公众号'],
    'data_analysis': ['数据分析', '统计', '图表', 'Excel', '报表'],
    'code_review': ['代码审查', 'review', 'PR', 'pull request'],
    'deployment': ['部署', 'deploy', '上线', '发布'],
    'monitoring': ['监控', '巡检', '检查状态', 'health check'],
    'backup': ['备份', 'backup', '同步', '迁移'],
}


class PatternDetector:
    """模式检测器"""

    def __init__(self, sessions_dir: str = None):
        self.sessions_dir = sessions_dir or str(
            Path.home() / '.hermes' / 'data' / 'sessions'
        )
        self.patterns = []
        self.proposals = []

    def scan_sessions(self, days: int = 7) -> list:
        """扫描最近N天的session记录"""
        sessions_path = Path(self.sessions_dir)
        if not sessions_path.exists():
            return []

        cutoff = datetime.now() - timedelta(days=days)
        session_files = []

        for f in sessions_path.glob('*.json'):
            try:
                mtime = datetime.fromtimestamp(f.stat().st_mtime)
                if mtime >= cutoff:
                    session_files.append(f)
            except:
                continue

        return session_files

    def extract_task_features(self, session_data: dict) -> dict:
        """从session数据中提取任务特征"""
        messages = session_data.get('messages', []) if isinstance(session_data, dict) else []

        # 提取用户消息
        user_msgs = [m for m in messages if m.get('role') == 'user']
        user_text = ' '.join(m.get('content', '') for m in user_msgs)

        # 提取工具调用
        tool_calls = []
        for m in messages:
            if m.get('role') == 'assistant':
                for tc in m.get('tool_calls', []):
                    tool_calls.append(tc.get('function', {}).get('name', ''))

        # 匹配任务类型
        matched_tasks = []
        for task_type, keywords in TASK_PATTERNS.items():
            for kw in keywords:
                if kw in user_text:
                    matched_tasks.append(task_type)
                    break

        # 匹配工具模式
        matched_tools = []
        for tool, keywords in TOOL_PATTERNS.items():
            for kw in keywords:
                if kw in user_text:
                    matched_tools.append(tool)
                    break

        # 实际使用的工具
        actual_tools = list(set(tool_calls))

        return {
            'user_text': user_text[:500],
            'matched_tasks': matched_tasks,
            'matched_tools': matched_tools,
            'actual_tools': actual_tools,
            'tool_sequence': tool_calls,
        }

    def analyze_patterns(self, features_list: list) -> list:
        """分析重复模式"""
        # 统计任务类型频次
        task_counter = Counter()
        tool_counter = Counter()
        tool_combo_counter = Counter()

        for features in features_list:
            for task in features['matched_tasks']:
                task_counter[task] += 1
            for tool in features['actual_tools']:
                tool_counter[tool] += 1
            # 工具组合（前3个工具的组合）
            combo = tuple(features['actual_tools'][:3])
            if len(combo) >= 2:
                tool_combo_counter[combo] += 1

        patterns = []

        # 高频任务类型
        for task, count in task_counter.most_common(5):
            if count >= 2:
                confidence = min(count / len(features_list), 1.0)
                patterns.append({
                    'type': 'recurring_task',
                    'task': task,
                    'count': count,
                    'confidence': round(confidence, 2),
                    'description': TASK_PATTERNS.get(task, [task])[0],
                })

        # 高频工具组合
        for combo, count in tool_combo_counter.most_common(5):
            if count >= 2:
                confidence = min(count / len(features_list), 1.0)
                patterns.append({
                    'type': 'tool_sequence',
                    'tools': list(combo),
                    'count': count,
                    'confidence': round(confidence, 2),
                    'description': ' → '.join(combo),
                })

        return patterns

    def generate_proposal(self, pattern: dict) -> dict:
        """根据模式生成工作流提案"""
        if pattern['type'] == 'recurring_task':
            task = pattern['task']
            return {
                'name': f"auto-{task}",
                'description': f"自动生成的{pattern['description']}工作流",
                'confidence': pattern['confidence'],
                'trigger_count': pattern['count'],
                'suggested_steps': self._suggest_steps_for_task(task),
                'yaml_hint': self._generate_yaml_hint(task),
            }
        elif pattern['type'] == 'tool_sequence':
            tools = pattern['tools']
            return {
                'name': f"auto-{'-'.join(tools[:3])}",
                'description': f"工具链: {pattern['description']}",
                'confidence': pattern['confidence'],
                'trigger_count': pattern['count'],
                'suggested_steps': [
                    {'id': f'step{i+1}', 'type': 'skill' if t in TOOL_PATTERNS else 'terminal', 'skill': t}
                    for i, t in enumerate(tools)
                ],
            }
        return {}

    def _suggest_steps_for_task(self, task: str) -> list:
        """根据任务类型建议步骤"""
        step_templates = {
            'news_report': [
                {'id': 'search', 'type': 'skill', 'skill': 'web-tools-guide', 'name': '搜索新闻'},
                {'id': 'infographic', 'type': 'skill', 'skill': 'baoyu-infographic', 'name': '生成信息图'},
                {'id': 'article', 'type': 'skill', 'skill': 'wechat-article', 'name': '撰写文章'},
                {'id': 'publish', 'type': 'skill', 'skill': 'wechat-publisher', 'name': '发布'},
            ],
            'research': [
                {'id': 'search', 'type': 'skill', 'skill': 'web-tools-guide', 'name': '搜索资料'},
                {'id': 'analyze', 'type': 'llm', 'name': '分析总结'},
                {'id': 'report', 'type': 'skill', 'skill': 'sn-research-report', 'name': '生成报告'},
            ],
            'content_creation': [
                {'id': 'outline', 'type': 'llm', 'name': '生成大纲'},
                {'id': 'write', 'type': 'skill', 'skill': 'wechat-article', 'name': '撰写内容'},
                {'id': 'publish', 'type': 'skill', 'skill': 'wechat-publisher', 'name': '发布'},
            ],
            'data_analysis': [
                {'id': 'load', 'type': 'skill', 'skill': 'sn-da-excel-workflow', 'name': '加载数据'},
                {'id': 'analyze', 'type': 'llm', 'name': '分析数据'},
                {'id': 'visualize', 'type': 'skill', 'skill': 'baoyu-infographic', 'name': '生成图表'},
            ],
            'monitoring': [
                {'id': 'check', 'type': 'terminal', 'name': '执行检查'},
                {'id': 'report', 'type': 'llm', 'name': '生成报告'},
            ],
        }
        return step_templates.get(task, [
            {'id': 'step1', 'type': 'llm', 'name': '执行任务'}
        ])

    def _generate_yaml_hint(self, task: str) -> str:
        """生成YAML提示"""
        steps = self._suggest_steps_for_task(task)
        lines = [f"name: auto-{task}", f'version: "1.0"', f'description: "自动生成的{task}工作流"', "", "steps:"]
        for step in steps:
            lines.append(f'  - id: {step["id"]}')
            lines.append(f'    name: "{step["name"]}"')
            lines.append(f'    type: {step["type"]}')
            if step.get('skill'):
                lines.append(f'    config:')
                lines.append(f'      skill_name: "{step["skill"]}"')
            lines.append(f'    depends: []')
        return '\n'.join(lines)

    def run_detection(self, days: int = 7, min_confidence: float = 0.3) -> dict:
        """运行完整检测流程"""
        # 1. 扫描session
        session_files = self.scan_sessions(days)

        # 2. 提取特征
        features_list = []
        for sf in session_files:
            try:
                with open(sf) as f:
                    data = json.load(f)
                features = self.extract_task_features(data)
                features_list.append(features)
            except:
                continue

        if not features_list:
            return {'patterns': [], 'proposals': [], 'sessions_scanned': len(session_files), 'features_extracted': 0}

        # 3. 分析模式
        patterns = self.analyze_patterns(features_list)

        # 4. 过滤低置信度
        patterns = [p for p in patterns if p['confidence'] >= min_confidence]

        # 5. 生成提案
        proposals = [self.generate_proposal(p) for p in patterns]

        return {
            'sessions_scanned': len(session_files),
            'features_extracted': len(features_list),
            'patterns': patterns,
            'proposals': proposals,
        }


def format_detection_report(result: dict) -> str:
    """格式化检测报告"""
    lines = [
        "═══ 模式检测报告 ═══",
        f"扫描会话: {result['sessions_scanned']} 个",
        f"提取特征: {result['features_extracted']} 个",
        f"发现模式: {len(result['patterns'])} 个",
        "",
    ]

    if not result['patterns']:
        lines.append("未发现足够高频的重复模式")
        return '\n'.join(lines)

    for i, pattern in enumerate(result['patterns']):
        lines.append(f"── 模式 {i+1} ──")
        lines.append(f"  类型: {pattern['type']}")
        lines.append(f"  描述: {pattern['description']}")
        lines.append(f"  频次: {pattern['count']} 次")
        lines.append(f"  置信度: {pattern['confidence']}")
        lines.append("")

    if result['proposals']:
        lines.append("═══ 工作流提案 ═══")
        for proposal in result['proposals']:
            lines.append(f"  📋 {proposal['name']}")
            lines.append(f"     {proposal['description']}")
            lines.append(f"     置信度: {proposal['confidence']}, 触发次数: {proposal['trigger_count']}")
            if proposal.get('yaml_hint'):
                lines.append(f"     YAML模板:")
                for line in proposal['yaml_hint'].split('\n')[:8]:
                    lines.append(f"       {line}")
            lines.append("")

    return '\n'.join(lines)
