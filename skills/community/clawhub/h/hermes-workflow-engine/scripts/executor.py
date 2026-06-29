"""
Hermes Workflow Executor v3.0
并行执行 — 同层步骤用delegate_task batch模式并行
"""

import json
from pathlib import Path
from datetime import datetime
from engine import (
    DAGParser, WorkflowRunner, WorkflowStatus, StepStatus, TemplateEngine
)


# ─── 同类工具备选映射 ────────────────────────────────────────

TOOL_FALLBACKS = {
    'web_search': ['tavily-search', 'firecrawl', 'hermes-cli'],
    'tavily-search': ['web_search', 'firecrawl'],
    'firecrawl': ['web_search', 'tavily-search'],
    'baoyu-infographic': ['sn-infographic', 'claude-design'],
    'sn-infographic': ['baoyu-infographic'],
    'read_file': ['terminal:cat'],
    'write_file': ['terminal:echo'],
    'terminal': ['execute_code'],
    'execute_code': ['terminal'],
    'browser': ['web_fetch', 'terminal:curl'],
    'web_fetch': ['terminal:curl', 'browser'],
}


class FallbackConfig:
    def __init__(self, step_config: dict, workflow_config: dict = None):
        self.max_attempts = step_config.get('max_attempts', 1)
        self.backoff = step_config.get('backoff', 2)
        self.fallbacks = step_config.get('fallbacks', [])
        self.on_fail = step_config.get('on_fail', 'abort')
        if workflow_config:
            self.on_fail = self.on_fail or workflow_config.get('on_step_fail', 'abort')

    def get_chain(self, primary_type: str, primary_skill: str = None) -> list:
        chain = [{'type': primary_type, 'skill': primary_skill, 'source': 'primary'}]
        for fb in self.fallbacks:
            chain.append({
                'type': fb.get('type', primary_type),
                'skill': fb.get('skill'),
                'command': fb.get('command'),
                'source': 'explicit_fallback'
            })
        lookup_key = primary_skill or primary_type
        auto_fallbacks = TOOL_FALLBACKS.get(lookup_key, [])
        existing = {c['skill'] or c['type'] for c in chain}
        for fb in auto_fallbacks:
            if fb not in existing:
                if ':' in fb:
                    t, cmd = fb.split(':', 1)
                    chain.append({'type': t, 'command': cmd, 'source': 'auto_fallback'})
                else:
                    chain.append({'type': 'skill', 'skill': fb, 'source': 'auto_fallback'})
        chain.append({'type': 'degrade', 'source': 'degrade'})
        return chain


class StepExecutor:
    def __init__(self, runner: WorkflowRunner):
        self.runner = runner
        self.template = TemplateEngine()

    def prepare_step(self, sid: str) -> dict:
        step = self.runner.steps[sid]
        context = self._build_context()
        config = step.get('config', {})
        rendered = {}
        for key, val in config.items():
            if isinstance(val, str):
                rendered[key] = self.template.render(val, context)
            else:
                rendered[key] = val

        fallback_cfg = FallbackConfig(
            step.get('retry', {}),
            self.runner.spec.get('error_handling', {})
        )
        primary_skill = rendered.get('skill_name')
        chain = fallback_cfg.get_chain(step.get('type', 'llm'), primary_skill)

        return {
            'step_id': sid,
            'step_name': step.get('name', sid),
            'step_type': step.get('type', 'llm'),
            'depends': step.get('depends', []),
            'config': rendered,
            'output_config': step.get('output', {}),
            'timeout': step.get('timeout', 120),
            'fallback_chain': chain,
            'fallback_config': {
                'max_attempts': fallback_cfg.max_attempts,
                'on_fail': fallback_cfg.on_fail,
            },
        }

    def _build_context(self) -> dict:
        ctx = {}
        for inp in self.runner.spec.get('inputs', []):
            ctx.setdefault('input', {})[inp['name']] = inp.get('default', '')
        for sid, output in self.runner.step_outputs.items():
            ctx[sid] = {'output': output, 'status': self.runner.step_status[sid].value}
        return ctx


class Scheduler:
    def __init__(self, runner: WorkflowRunner, executor: StepExecutor):
        self.runner = runner
        self.executor = executor

    def get_next_batch(self) -> list:
        ready = self.runner.get_ready_steps()
        return [self.executor.prepare_step(sid) for sid in ready]

    def get_parallel_layers(self) -> list:
        """获取可并行执行的分层计划"""
        layers = self.runner.parser.topological_sort()
        executable = []
        for layer in layers:
            ready_in_layer = []
            for sid in layer:
                if self.runner.step_status[sid] != StepStatus.PENDING:
                    continue
                deps = self.runner.steps[sid].get('depends', [])
                if all(self.runner.step_status[d] == StepStatus.SUCCESS for d in deps):
                    ready_in_layer.append(self.executor.prepare_step(sid))
            if ready_in_layer:
                executable.append(ready_in_layer)
        return executable

    def get_execution_plan(self) -> dict:
        layers = self.runner.parser.topological_sort()
        plan = {
            'workflow': self.runner.spec.get('name'),
            'version': self.runner.spec.get('version'),
            'run_id': self.runner.run_id,
            'total_steps': len(self.runner.steps),
            'total_layers': len(layers),
            'layers': [],
        }
        for i, layer in enumerate(layers):
            layer_info = {'layer': i + 1, 'parallel': len(layer) > 1, 'steps': []}
            for sid in layer:
                step = self.runner.steps[sid]
                layer_info['steps'].append({
                    'id': sid, 'name': step.get('name', sid),
                    'type': step.get('type', 'llm'),
                    'depends': step.get('depends', []),
                })
            plan['layers'].append(layer_info)
        return plan

    def mark_running(self, sid: str):
        self.runner.mark_step_running(sid)

    def mark_success(self, sid: str, output=None):
        self.runner.mark_step_success(sid, output)

    def mark_failed(self, sid: str, error: str):
        self.runner.mark_step_failed(sid, error)

    def mark_paused(self, sid: str):
        self.runner.mark_step_paused(sid)

    def is_complete(self) -> bool:
        return self.runner.is_complete()

    def get_progress(self) -> dict:
        return self.runner.get_progress()

    def handle_failure(self, sid: str, step_info: dict, error: str) -> dict:
        on_fail = step_info.get('fallback_config', {}).get('on_fail', 'abort')
        if on_fail == 'skip':
            self.runner.step_status[sid] = StepStatus.SKIPPED
            self.runner.step_errors[sid] = f"Skipped: {error}"
            self.runner._save_state()
            return {'action': 'skip', 'reason': error}
        elif on_fail == 'pause':
            self.mark_paused(sid)
            return {'action': 'pause', 'reason': error}
        else:
            self.mark_failed(sid, error)
            return {'action': 'abort', 'reason': error}


def load_and_plan(yaml_path: str, inputs: dict = None) -> dict:
    parser = DAGParser(yaml_path=yaml_path)
    if inputs:
        for inp in parser.spec.get('inputs', []):
            if inp['name'] in inputs:
                inp['default'] = inputs[inp['name']]
    runner = WorkflowRunner(parser)
    executor = StepExecutor(runner)
    scheduler = Scheduler(runner, executor)
    return {
        'plan': scheduler.get_execution_plan(),
        'first_batch': scheduler.get_next_batch(),
        'parallel_layers': scheduler.get_parallel_layers(),
        'render': runner.render_plan(),
        'scheduler': scheduler,
        'runner': runner,
    }


def generate_delegate_task_batch(batch: list) -> list:
    """将一批并行步骤转化为delegate_task的tasks格式"""
    tasks = []
    for step in batch:
        stype = step['step_type']
        config = step['config']

        if stype == 'terminal':
            goal = f"执行shell命令: {config.get('command', '')}"
            toolsets = ['terminal']
        elif stype == 'skill':
            skill = config.get('skill_name', '')
            prompt = config.get('prompt', '')
            goal = f"使用技能 {skill} 执行: {prompt}"
            toolsets = ['terminal', 'file', 'web']
        elif stype == 'subagent':
            goal = config.get('goal', '')
            toolsets = config.get('toolsets', ['terminal', 'file', 'web'])
        elif stype == 'llm':
            goal = config.get('prompt', '')
            toolsets = []
        else:
            goal = f"执行步骤 {step['step_name']}"
            toolsets = ['terminal']

        tasks.append({
            'goal': goal,
            'context': json.dumps({
                'step_id': step['step_id'],
                'step_name': step['step_name'],
                'step_type': stype,
                'config': config,
            }, ensure_ascii=False),
            'toolsets': toolsets,
        })
    return tasks


def generate_agent_instructions(plan: dict, batch: list) -> str:
    lines = [
        f"═══ 工作流执行指令 ═══",
        f"工作流: {plan['workflow']} v{plan.get('version', '?')}",
        f"Run ID: {plan['run_id']}",
        f"总步骤: {plan['total_steps']}, 总层数: {plan['total_layers']}",
        "",
    ]
    for layer in plan['layers']:
        tag = "⚡并行" if layer['parallel'] else "→串行"
        lines.append(f"── 第{layer['layer']}层 [{tag}] ──")
        for step in layer['steps']:
            lines.append(f"  [{step['type']}] {step['name']} (id: {step['id']})")
        lines.append("")

    if batch:
        lines.append("── 当前可执行步骤 ──")
        for step in batch:
            lines.append(f"  → {step['step_name']} ({step['step_type']})")

    return '\n'.join(lines)
