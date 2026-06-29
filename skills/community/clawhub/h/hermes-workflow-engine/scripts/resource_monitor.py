"""
Hermes Workflow Resource Monitor v1.0
资源监控 — token/时间/API调用预算控制
"""

import time
import json
from pathlib import Path
from datetime import datetime


class ResourceMonitor:
    """资源监控器 — 跟踪token、时间、API调用"""

    # 各步骤类型的默认token估算
    DEFAULT_TOKEN_ESTIMATES = {
        'terminal': 200,
        'skill': 3000,
        'subagent': 5000,
        'user_input': 100,
        'llm': 2000,
    }

    # 各步骤类型的默认时间估算（秒）
    DEFAULT_TIME_ESTIMATES = {
        'terminal': 5,
        'skill': 30,
        'subagent': 60,
        'user_input': 300,  # 用户输入可能等很久
        'llm': 15,
    }

    def __init__(self, budget: dict = None):
        self.budget = budget or {}
        self.max_tokens = self.budget.get('max_tokens', 100000)
        self.max_time = self.budget.get('max_time', 600)
        self.max_api_calls = self.budget.get('max_api_calls', 50)

        # 实际消耗
        self.tokens_used = 0
        self.time_elapsed = 0
        self.api_calls = 0
        self.start_time = None

        # 每步记录
        self.step_records = []

        # 预估
        self.estimated_tokens = 0
        self.estimated_time = 0

    def estimate_step(self, step_type: str, config: dict = None) -> dict:
        """预估单步资源消耗"""
        tokens = self.DEFAULT_TOKEN_ESTIMATES.get(step_type, 1000)
        time_est = self.DEFAULT_TIME_ESTIMATES.get(step_type, 30)

        # 根据prompt长度调整token估算
        if config:
            prompt = config.get('prompt', '') or config.get('goal', '') or config.get('command', '')
            if len(prompt) > 500:
                tokens = int(tokens * 1.5)
            if len(prompt) > 2000:
                tokens = int(tokens * 2)

        return {'tokens': tokens, 'time': time_est}

    def estimate_workflow(self, steps: dict) -> dict:
        """预估整个工作流资源消耗"""
        total_tokens = 0
        total_time = 0
        step_estimates = {}

        # 按层计算（并行步骤只算最慢的那个）
        for sid, step in steps.items():
            est = self.estimate_step(step.get('type', 'llm'), step.get('config'))
            step_estimates[sid] = est
            total_tokens += est['tokens']
            # 并行步骤取最大值，串行步骤累加
            total_time += est['time']

        self.estimated_tokens = total_tokens
        self.estimated_time = total_time

        return {
            'estimated_tokens': total_tokens,
            'estimated_time': total_time,
            'token_budget': self.max_tokens,
            'time_budget': self.max_time,
            'token_usage_pct': int(total_tokens / self.max_tokens * 100) if self.max_tokens else 0,
            'time_usage_pct': int(total_time / self.max_time * 100) if self.max_time else 0,
            'within_budget': total_tokens <= self.max_tokens and total_time <= self.max_time,
            'step_estimates': step_estimates,
        }

    def start(self):
        """开始监控"""
        self.start_time = time.time()
        self.tokens_used = 0
        self.api_calls = 0

    def record_step(self, sid: str, tokens: int = 0, api_calls: int = 1, success: bool = True):
        """记录步骤消耗"""
        elapsed = time.time() - self.start_time if self.start_time else 0
        self.tokens_used += tokens
        self.api_calls += api_calls
        self.time_elapsed = elapsed

        record = {
            'step_id': sid,
            'tokens': tokens,
            'api_calls': api_calls,
            'elapsed': round(elapsed, 1),
            'success': success,
            'timestamp': datetime.now().isoformat(),
        }
        self.step_records.append(record)
        return record

    def check_budget(self) -> dict:
        """检查是否超预算"""
        elapsed = time.time() - self.start_time if self.start_time else 0
        warnings = []

        if self.max_tokens and self.tokens_used > self.max_tokens * 0.8:
            warnings.append(f"⚠️ Token消耗已达{int(self.tokens_used/self.max_tokens*100)}%")
        if self.max_time and elapsed > self.max_time * 0.8:
            warnings.append(f"⚠️ 执行时间已达{int(elapsed/self.max_time*100)}%")
        if self.max_api_calls and self.api_calls > self.max_api_calls * 0.8:
            warnings.append(f"⚠️ API调用已达{int(self.api_calls/self.max_api_calls*100)}%")

        over_budget = (
            (self.max_tokens and self.tokens_used > self.max_tokens) or
            (self.max_time and elapsed > self.max_time) or
            (self.max_api_calls and self.api_calls > self.max_api_calls)
        )

        return {
            'tokens': {'used': self.tokens_used, 'max': self.max_tokens, 'pct': int(self.tokens_used/self.max_tokens*100) if self.max_tokens else 0},
            'time': {'used': round(elapsed, 1), 'max': self.max_time, 'pct': int(elapsed/self.max_time*100) if self.max_time else 0},
            'api_calls': {'used': self.api_calls, 'max': self.max_api_calls, 'pct': int(self.api_calls/self.max_api_calls*100) if self.max_api_calls else 0},
            'over_budget': over_budget,
            'warnings': warnings,
        }

    def get_status_bar(self) -> str:
        """生成状态栏"""
        budget = self.check_budget()
        t = budget['tokens']
        tm = budget['time']
        bar_len = 20

        def pct_bar(pct):
            filled = int(pct / 100 * bar_len)
            return '█' * filled + '░' * (bar_len - filled)

        lines = [
            f"Token: {pct_bar(t['pct'])} {t['pct']}% ({t['used']}/{t['max']})",
            f"时间:  {pct_bar(tm['pct'])} {tm['pct']}% ({tm['used']}s/{tm['max']}s)",
            f"API:   {budget['api_calls']['used']}/{budget['api_calls']['max']}",
        ]
        if budget['warnings']:
            lines.extend(budget['warnings'])
        return '\n'.join(lines)

    def save_report(self, run_dir: str):
        """保存资源报告"""
        report = {
            'budget': {
                'max_tokens': self.max_tokens,
                'max_time': self.max_time,
                'max_api_calls': self.max_api_calls,
            },
            'actual': {
                'tokens_used': self.tokens_used,
                'time_elapsed': round(self.time_elapsed, 1),
                'api_calls': self.api_calls,
            },
            'step_records': self.step_records,
            'check': self.check_budget(),
        }
        path = Path(run_dir) / 'resource_report.json'
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        return str(path)


def pre_check_workflow(steps: dict, budget: dict = None) -> str:
    """执行前预检查，返回可读报告"""
    monitor = ResourceMonitor(budget)
    estimate = monitor.estimate_workflow(steps)

    lines = [
        "═══ 资源预估 ═══",
        f"预计Token: {estimate['estimated_tokens']} / {estimate['token_budget']} ({estimate['token_usage_pct']}%)",
        f"预计时间: {estimate['estimated_time']}s / {estimate['time_budget']}s ({estimate['time_usage_pct']}%)",
    ]

    if not estimate['within_budget']:
        lines.append("❌ 超出预算！建议简化工作流或增加预算")
    else:
        lines.append("✅ 预算充足")

    # 各步骤预估
    lines.append("\n各步骤预估:")
    for sid, est in estimate['step_estimates'].items():
        lines.append(f"  {sid}: ~{est['tokens']} tokens, ~{est['time']}s")

    return '\n'.join(lines)
