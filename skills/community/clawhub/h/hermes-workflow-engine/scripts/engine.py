"""
Hermes Workflow Engine v1.0
DAG编排引擎 — 解析工作流定义、拓扑排序、并行调度
"""

import yaml
import json
import time
import uuid
from pathlib import Path
from datetime import datetime
from collections import defaultdict, deque
from enum import Enum


class StepStatus(Enum):
    PENDING = "pending"
    WAITING = "waiting"      # 等待依赖完成
    READY = "ready"          # 依赖满足，可执行
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"
    PAUSED = "paused"        # 等待用户输入


class WorkflowStatus(Enum):
    CREATED = "created"
    RUNNING = "running"
    PAUSED = "paused"
    SUCCESS = "success"
    FAILED = "failed"
    ABORTED = "aborted"


# ─── DAG Parser ─────────────────────────────────────────────

class DAGParser:
    """解析工作流YAML，构建DAG，检测环"""

    def __init__(self, yaml_path: str = None, yaml_str: str = None):
        if yaml_path:
            with open(yaml_path, 'r', encoding='utf-8') as f:
                self.spec = yaml.safe_load(f)
        elif yaml_str:
            self.spec = yaml.safe_load(yaml_str)
        else:
            raise ValueError("Must provide yaml_path or yaml_str")

        self.steps = {}
        self.adj = defaultdict(list)    # 邻接表: step_id -> [dependent_ids]
        self.in_degree = defaultdict(int)
        self._build_graph()

    def _build_graph(self):
        """构建DAG图"""
        for step_def in self.spec.get('steps', []):
            sid = step_def['id']
            self.steps[sid] = step_def
            self.in_degree[sid] = self.in_degree.get(sid, 0)
            deps = step_def.get('depends', [])
            for dep in deps:
                if dep not in [s['id'] for s in self.spec.get('steps', [])]:
                    raise ValueError(f"Step '{sid}' depends on unknown step '{dep}'")
                self.adj[dep].append(sid)
                self.in_degree[sid] += 1

        # 检测环
        if self._has_cycle():
            raise ValueError("Workflow DAG contains a cycle!")

    def _has_cycle(self) -> bool:
        """Kahn算法检测环"""
        in_deg = dict(self.in_degree)
        queue = deque([n for n in in_deg if in_deg[n] == 0])
        visited = 0
        while queue:
            node = queue.popleft()
            visited += 1
            for neighbor in self.adj[node]:
                in_deg[neighbor] -= 1
                if in_deg[neighbor] == 0:
                    queue.append(neighbor)
        return visited != len(self.steps)

    def topological_sort(self) -> list:
        """拓扑排序，返回分层执行计划（每层可并行）"""
        in_deg = dict(self.in_degree)
        layers = []
        remaining = set(self.steps.keys())

        while remaining:
            # 当前层: 所有入度为0的节点
            layer = [n for n in remaining if in_deg.get(n, 0) == 0]
            if not layer:
                raise ValueError("Cannot resolve DAG — cycle detected during sort")
            layers.append(layer)
            for node in layer:
                remaining.discard(node)
                for neighbor in self.adj[node]:
                    in_deg[neighbor] -= 1
        return layers

    def get_execution_plan(self) -> list:
        """返回可执行的分层计划"""
        layers = self.topological_sort()
        plan = []
        for i, layer in enumerate(layers):
            plan.append({
                'layer': i,
                'parallel': len(layer) > 1,
                'steps': [
                    {
                        'id': sid,
                        'name': self.steps[sid].get('name', sid),
                        'type': self.steps[sid].get('type', 'llm'),
                        'depends': self.steps[sid].get('depends', []),
                    }
                    for sid in layer
                ]
            })
        return plan

    def validate(self) -> dict:
        """验证工作流定义"""
        errors = []
        warnings = []

        # 检查必填字段
        if not self.spec.get('name'):
            errors.append("Missing required field: 'name'")
        if not self.spec.get('steps'):
            errors.append("Missing required field: 'steps'")

        # 检查步骤ID唯一性
        ids = [s['id'] for s in self.spec.get('steps', [])]
        if len(ids) != len(set(ids)):
            errors.append("Duplicate step IDs found")

        # 检查依赖有效性
        for step in self.spec.get('steps', []):
            for dep in step.get('depends', []):
                if dep not in ids:
                    errors.append(f"Step '{step['id']}' depends on unknown step '{dep}'")

            # 检查步骤类型
            valid_types = ['skill', 'terminal', 'subagent', 'user_input', 'llm']
            stype = step.get('type', 'llm')
            if stype not in valid_types:
                errors.append(f"Step '{step['id']}' has invalid type '{stype}'")

            # 检查user_input类型必须有prompt
            if stype == 'user_input' and not step.get('config', {}).get('prompt'):
                warnings.append(f"Step '{step['id']}' is user_input but has no prompt")

        return {'valid': len(errors) == 0, 'errors': errors, 'warnings': warnings}


# ─── Workflow Runner ─────────────────────────────────────────

class WorkflowRunner:
    """执行工作流DAG"""

    def __init__(self, parser: DAGParser, run_dir: str = None):
        self.parser = parser
        self.spec = parser.spec
        self.steps = parser.steps
        self.run_id = datetime.now().strftime('%Y%m%d_%H%M%S') + '_' + uuid.uuid4().hex[:6]
        self.run_dir = run_dir or str(Path.home() / '.hermes' / 'workflow-engine' / 'runs' / self.run_id)
        Path(self.run_dir).mkdir(parents=True, exist_ok=True)

        # 状态
        self.status = WorkflowStatus.CREATED
        self.step_status = {sid: StepStatus.PENDING for sid in self.steps}
        self.step_outputs = {}
        self.step_errors = {}
        self.start_time = None
        self.end_time = None

    def get_ready_steps(self) -> list:
        """获取当前可执行的步骤（依赖已满足）"""
        ready = []
        for sid, step in self.steps.items():
            if self.step_status[sid] != StepStatus.PENDING:
                continue
            deps = step.get('depends', [])
            if all(self.step_status[d] == StepStatus.SUCCESS for d in deps):
                ready.append(sid)
        return ready

    def get_parallel_layers(self) -> list:
        """获取可并行执行的步骤分组"""
        layers = self.parser.topological_sort()
        executable = []
        for layer in layers:
            ready_in_layer = [s for s in layer if self.step_status[s] == StepStatus.PENDING]
            if ready_in_layer:
                # 检查依赖是否都满足
                truly_ready = []
                for sid in ready_in_layer:
                    deps = self.steps[sid].get('depends', [])
                    if all(self.step_status[d] == StepStatus.SUCCESS for d in deps):
                        truly_ready.append(sid)
                if truly_ready:
                    executable.append(truly_ready)
        return executable

    def mark_step_running(self, sid: str):
        self.step_status[sid] = StepStatus.RUNNING
        self._save_state()

    def mark_step_success(self, sid: str, output=None):
        self.step_status[sid] = StepStatus.SUCCESS
        if output is not None:
            self.step_outputs[sid] = output
        self._save_state()

    def mark_step_failed(self, sid: str, error: str):
        self.step_status[sid] = StepStatus.FAILED
        self.step_errors[sid] = error
        self._save_state()

    def mark_step_paused(self, sid: str):
        self.step_status[sid] = StepStatus.PAUSED
        self._save_state()

    def is_complete(self) -> bool:
        return all(
            s in (StepStatus.SUCCESS, StepStatus.SKIPPED)
            for s in self.step_status.values()
        )

    def has_failed(self) -> bool:
        return any(s == StepStatus.FAILED for s in self.step_status.values())

    def get_progress(self) -> dict:
        total = len(self.step_status)
        done = sum(1 for s in self.step_status.values() if s == StepStatus.SUCCESS)
        failed = sum(1 for s in self.step_status.values() if s == StepStatus.FAILED)
        running = sum(1 for s in self.step_status.values() if s == StepStatus.RUNNING)
        paused = sum(1 for s in self.step_status.values() if s == StepStatus.PAUSED)
        return {
            'total': total, 'done': done, 'failed': failed,
            'running': running, 'paused': paused,
            'percent': int(done / total * 100) if total else 0,
        }

    def render_plan(self) -> str:
        """渲染执行计划为可读文本"""
        layers = self.parser.topological_sort()
        lines = [
            f"═══ 工作流: {self.spec.get('name', 'unnamed')} ═══",
            f"版本: {self.spec.get('version', '?')}",
            f"描述: {self.spec.get('description', '无')}",
            f"步骤: {len(self.steps)} 步, {len(layers)} 层",
            ""
        ]
        for i, layer in enumerate(layers):
            parallel = len(layer) > 1
            tag = "⚡并行" if parallel else "→串行"
            lines.append(f"第{i+1}层 [{tag}]:")
            for sid in layer:
                step = self.steps[sid]
                deps = step.get('depends', [])
                dep_str = f" (← {', '.join(deps)})" if deps else ""
                lines.append(f"  • [{step.get('type', 'llm')}] {step.get('name', sid)}{dep_str}")
            lines.append("")
        return '\n'.join(lines)

    def _save_state(self):
        """保存运行状态到文件"""
        state = {
            'run_id': self.run_id,
            'workflow': self.spec.get('name'),
            'status': self.status.value,
            'step_status': {k: v.value for k, v in self.step_status.items()},
            'step_outputs': {k: str(v)[:200] for k, v in self.step_outputs.items()},
            'step_errors': self.step_errors,
            'progress': self.get_progress(),
            'updated_at': datetime.now().isoformat(),
        }
        state_path = Path(self.run_dir) / 'state.json'
        with open(state_path, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

    def save_run_log(self):
        """保存完整运行日志"""
        log = {
            'run_id': self.run_id,
            'workflow': self.spec.get('name'),
            'version': self.spec.get('version'),
            'status': self.status.value,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'step_status': {k: v.value for k, v in self.step_status.items()},
            'step_outputs': {k: str(v)[:500] for k, v in self.step_outputs.items()},
            'step_errors': self.step_errors,
            'progress': self.get_progress(),
        }
        log_path = Path(self.run_dir) / 'run_log.json'
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(log, f, ensure_ascii=False, indent=2)
        return str(log_path)


# ─── Template Engine ─────────────────────────────────────────

class TemplateEngine:
    """简单的模板变量替换"""

    @staticmethod
    def render(template: str, context: dict) -> str:
        """替换 {{xxx}} 模板变量"""
        import re
        def replacer(match):
            key = match.group(1).strip()
            parts = key.split('.')
            val = context
            for p in parts:
                if isinstance(val, dict) and p in val:
                    val = val[p]
                else:
                    return match.group(0)  # 找不到就保留原样
            return str(val)
        return re.sub(r'\{\{(.+?)\}\}', replacer, template)


# ─── Public API ──────────────────────────────────────────────

def load_workflow(path: str) -> DAGParser:
    """加载工作流定义"""
    return DAGParser(yaml_path=path)


def validate_workflow(path: str) -> dict:
    """验证工作流定义"""
    parser = DAGParser(yaml_path=path)
    return parser.validate()


def create_runner(path: str) -> WorkflowRunner:
    """创建工作流运行器"""
    parser = load_workflow(path)
    return WorkflowRunner(parser)
