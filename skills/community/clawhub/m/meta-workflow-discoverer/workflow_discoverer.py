"""
Workflow Discoverer - Auto-detect and create workflows
"""
import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import re


class WorkflowDiscoverer:
    """Discover and create workflows from patterns"""
    
    def __init__(
        self,
        user_id: str = "default",
        min_occurrences: int = 3,
        storage_path: str = None
    ):
        self.user_id = user_id
        self.min_occurrences = min_occurrences
        
        # Storage
        self.storage_path = storage_path or f"~/.workflow_discoverer/{user_id}.json"
        self.data = self._load()
        
        # Initialize
        self.data.setdefault('tasks', [])
        self.data.setdefault('sequences', [])
        self.data.setdefault('workflows', [])
        self.data.setdefault('automations', [])
    
    def _load(self) -> Dict:
        """Load data"""
        path = os.path.expanduser(self.storage_path)
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return {}
    
    def _save(self):
        """Save data"""
        path = os.path.expanduser(self.storage_path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    # ==================== Recording ====================
    
    def record_task(
        self,
        task: str,
        steps: List[str] = None,
        context: Dict = None,
        result: str = "success"
    ):
        """Record task execution"""
        record = {
            'task': task,
            'steps': steps or [],
            'context': context or {},
            'result': result,
            'timestamp': datetime.now().isoformat()
        }
        
        self.data['tasks'].append(record)
        
        # Update sequence if multiple steps
        if steps and len(steps) > 1:
            self._update_sequence(steps)
        
        self._save()
        
        return {'status': 'recorded'}
    
    def _update_sequence(self, steps: List[str]):
        """Update step sequence"""
        seq = tuple(steps[:5])  # First 5 steps
        
        sequences = self.data.get('sequences', [])
        
        # Find existing
        found = False
        for s in sequences:
            if s['sequence'] == seq:
                s['count'] += 1
                s['last_seen'] = datetime.now().isoformat()
                found = True
                break
        
        if not found:
            sequences.append({
                'sequence': list(seq),
                'count': 1,
                'first_seen': datetime.now().isoformat(),
                'last_seen': datetime.now().isoformat()
            })
        
        self.data['sequences'] = sequences
    
    def import_history(self, tasks: List[Dict]):
        """Import task history"""
        for t in tasks:
            self.record_task(
                task=t.get('task', ''),
                steps=t.get('steps', []),
                context=t.get('context', {}),
                result=t.get('result', 'unknown')
            )
        
        return {'imported': len(tasks)}
    
    # ==================== Discovery ====================
    
    def discover_workflows(self) -> List[Dict]:
        """Discover potential workflows"""
        workflows = []
        
        # 1. Discover from sequences
        seq_workflows = self._discover_sequence_workflows()
        workflows.extend(seq_workflows)
        
        # 2. Discover from similar tasks
        task_workflows = self._discover_task_workflows()
        workflows.extend(task_workflows)
        
        # 3. Discover from time patterns
        time_workflows = self._discover_time_workflows()
        workflows.extend(time_workflows)
        
        # Remove duplicates and sort
        workflows = self._deduplicate_workflows(workflows)
        
        return sorted(workflows, key=lambda x: x['confidence'], reverse=True)
    
    def _discover_sequence_workflows(self) -> List[Dict]:
        """Discover workflows from step sequences"""
        workflows = []
        
        for seq in self.data.get('sequences', []):
            if seq['count'] >= self.min_occurrences:
                # Create workflow
                workflow = {
                    'id': f"seq_{hash(seq['sequence']) % 100000}",
                    'name': self._generate_workflow_name(seq['sequence']),
                    'type': 'sequence',
                    'steps': list(seq['sequence']),
                    'confidence': min(1.0, seq['count'] / 10),
                    'occurrences': seq['count'],
                    'pattern': 'repeated_sequence',
                    'time_saved_estimate': len(seq['sequence']) * 5  # 5 min per step
                }
                
                workflows.append(workflow)
        
        return workflows
    
    def _discover_task_workflows(self) -> List[Dict]:
        """Discover workflows from similar tasks"""
        workflows = []
        
        # Group tasks by similarity
        task_groups = defaultdict(list)
        
        for task in self.data.get('tasks', []):
            task_name = self._normalize_task(task['task'])
            task_groups[task_name].append(task)
        
        # Find groups with multiple similar tasks
        for task_name, instances in task_groups.items():
            if len(instances) >= self.min_occurrences:
                # Extract common steps
                all_steps = []
                for inst in instances:
                    all_steps.extend(inst.get('steps', []))
                
                step_counts = Counter(all_steps)
                common_steps = [s for s, c in step_counts.most_common(5)]
                
                if common_steps:
                    workflow = {
                        'id': f"task_{hash(task_name) % 100000}",
                        'name': task_name,
                        'type': 'task_template',
                        'steps': common_steps,
                        'confidence': min(1.0, len(instances) / 10),
                        'occurrences': len(instances),
                        'pattern': 'similar_tasks',
                        'time_saved_estimate': len(common_steps) * 3
                    }
                    
                    workflows.append(workflow)
        
        return workflows
    
    def _discover_time_workflows(self) -> List[Dict]:
        """Discover time-based workflows"""
        workflows = []
        
        # Group by hour
        hour_counts = defaultdict(list)
        
        for task in self.data.get('tasks', []):
            try:
                dt = datetime.fromisoformat(task['timestamp'])
                hour = dt.hour
                hour_counts[hour].append(task)
            except:
                pass
        
        # Find regular hours
        for hour, tasks in hour_counts.items():
            if len(tasks) >= self.min_occurrences:
                # Check if same task
                task_names = [self._normalize_task(t['task']) for t in tasks]
                most_common = Counter(task_names).most_common(1)
                
                if most_common:
                    workflow = {
                        'id': f"time_{hour}",
                        'name': f"{most_common[0][0]} (scheduled)",
                        'type': 'scheduled',
                        'trigger': {'hour': hour, 'minute': 0},
                        'confidence': min(1.0, len(tasks) / 10),
                        'occurrences': len(tasks),
                        'pattern': 'time_based',
                        'time_saved_estimate': 10
                    }
                    
                    workflows.append(workflow)
        
        return workflows
    
    def _normalize_task(self, task: str) -> str:
        """Normalize task name"""
        # Remove specific identifiers
        normalized = re.sub(r'\d+', '#', task)
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        return normalized
    
    def _generate_workflow_name(self, steps: List[str]) -> str:
        """Generate workflow name from steps"""
        if not steps:
            return "unnamed_workflow"
        
        # Use first and last step
        if len(steps) == 1:
            return f"{steps[0]}_workflow"
        
        return f"{steps[0]}_to_{steps[-1]}"
    
    def _deduplicate_workflows(self, workflows: List[Dict]) -> List[Dict]:
        """Remove duplicate workflows"""
        seen = set()
        unique = []
        
        for wf in workflows:
            key = frozenset(wf.get('steps', []))
            if key not in seen:
                seen.add(key)
                unique.append(wf)
        
        return unique
    
    # ==================== Automation ====================
    
    def create_automation(
        self,
        workflow_id: str = None,
        workflow: Dict = None,
        trigger: Dict = None,
        enabled: bool = True,
        params: Dict = None
    ) -> Dict:
        """Create automation from workflow"""
        if workflow:
            wf = workflow
        else:
            # Find workflow
            wf = None
            for w in self.data.get('workflows', []):
                if w['id'] == workflow_id:
                    wf = w
                    break
            
            if not wf:
                return {'error': 'Workflow not found'}
        
        # Create automation
        automation = {
            'id': f"auto_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'workflow_id': wf.get('id'),
            'name': wf.get('name'),
            'steps': wf.get('steps', []),
            'trigger': trigger or {'type': 'manual'},
            'enabled': enabled,
            'params': params or {},
            'created_at': datetime.now().isoformat(),
            'last_run': None,
            'run_count': 0,
            'success_count': 0
        }
        
        self.data['automations'].append(automation)
        
        # Add to workflows if new
        if workflow and workflow['id'] not in [w['id'] for w in self.data.get('workflows', [])]:
            self.data['workflows'].append(wf)
        
        self._save()
        
        return automation
    
    def enable_automation(self, automation_id: str) -> Dict:
        """Enable automation"""
        for auto in self.data.get('automations', []):
            if auto['id'] == automation_id:
                auto['enabled'] = True
                self._save()
                return {'status': 'enabled', 'id': automation_id}
        
        return {'error': 'Automation not found'}
    
    def disable_automation(self, automation_id: str) -> Dict:
        """Disable automation"""
        for auto in self.data.get('automations', []):
            if auto['id'] == automation_id:
                auto['enabled'] = False
                self._save()
                return {'status': 'disabled', 'id': automation_id}
        
        return {'error': 'Automation not found'}
    
    def run_automation(self, automation_id: str) -> Dict:
        """Run automation manually"""
        for auto in self.data.get('automations', []):
            if auto['id'] == automation_id:
                auto['run_count'] += 1
                auto['last_run'] = datetime.now().isoformat()
                
                # In production, would execute steps
                # Here, simulate success
                auto['success_count'] += 1
                
                self._save()
                
                return {
                    'status': 'success',
                    'automation': auto['name'],
                    'steps_executed': len(auto.get('steps', []))
                }
        
        return {'error': 'Automation not found'}
    
    # ==================== Analysis ====================
    
    def analyze_sequences(self) -> Dict:
        """Analyze task sequences"""
        sequences = self.data.get('sequences', [])
        
        # Sort by count
        sorted_seqs = sorted(sequences, key=lambda x: x['count'], reverse=True)
        
        return {
            'total_sequences': len(sequences),
            'top_sequences': [
                {
                    'steps': list(s['sequence']),
                    'count': s['count']
                }
                for s in sorted_seqs[:10]
            ]
        }
    
    def detect_triggers(self) -> List[Dict]:
        """Detect trigger patterns"""
        triggers = []
        
        # Time-based triggers
        time_triggers = self._detect_time_triggers()
        triggers.extend(time_triggers)
        
        # Event-based triggers
        event_triggers = self._detect_event_triggers()
        triggers.extend(event_triggers)
        
        return triggers
    
    def _detect_time_triggers(self) -> List[Dict]:
        """Detect time-based triggers"""
        triggers = []
        
        hour_counts = defaultdict(list)
        
        for task in self.data.get('tasks', []):
            try:
                dt = datetime.fromisoformat(task['timestamp'])
                hour_counts[dt.hour].append(task)
            except:
                pass
        
        for hour, tasks in hour_counts.items():
            if len(tasks) >= 3:
                triggers.append({
                    'type': 'schedule',
                    'schedule': f"{hour}:00 daily",
                    'confidence': min(1.0, len(tasks) / 10),
                    'tasks': len(tasks)
                })
        
        return triggers
    
    def _detect_event_triggers(self) -> List[Dict]:
        """Detect event-based triggers"""
        triggers = []
        
        # Find tasks that follow other tasks
        task_after = defaultdict(list)
        
        tasks = self.data.get('tasks', [])
        for i in range(len(tasks) - 1):
            curr = tasks[i]['task']
            next_task = tasks[i + 1]['task']
            task_after[curr].append(next_task)
        
        # Find strong patterns
        for task, next_tasks in task_after.items():
            if len(next_tasks) >= 3:
                most_common = Counter(next_tasks).most_common(1)
                if most_common:
                    triggers.append({
                        'type': 'event',
                        'trigger': f"after: {task}",
                        'action': most_common[0][0],
                        'confidence': min(1.0, len(next_tasks) / 10)
                    })
        
        return triggers
    
    # ==================== Learning ====================
    
    def track_results(self) -> Dict:
        """Track automation results"""
        automations = self.data.get('automations', [])
        
        if not automations:
            return {'status': 'no_automations'}
        
        total_runs = sum(a.get('run_count', 0) for a in automations)
        total_success = sum(a.get('success_count', 0) for a in automations)
        
        return {
            'total_automations': len(automations),
            'total_runs': total_runs,
            'success_rate': total_success / total_runs if total_runs > 0 else 0,
            'automations': [
                {
                    'name': a['name'],
                    'runs': a.get('run_count', 0),
                    'success': a.get('success_count', 0)
                }
                for a in automations
            ]
        }
    
    def improve_workflow(self, workflow_id: str, feedback: Dict) -> Dict:
        """Improve workflow based on feedback"""
        # Find workflow
        for wf in self.data.get('workflows', []):
            if wf['id'] == workflow_id:
                # Apply feedback
                if 'add_steps' in feedback:
                    wf['steps'].extend(feedback['add_steps'])
                
                if 'remove_steps' in feedback:
                    for step in feedback['remove_steps']:
                        if step in wf['steps']:
                            wf['steps'].remove(step)
                
                if 'reorder' in feedback:
                    wf['steps'] = feedback['reorder']
                
                wf['version'] = wf.get('version', 1) + 1
                
                self._save()
                
                return {'status': 'improved', 'workflow': wf}
        
        return {'error': 'Workflow not found'}
    
    # ==================== Export ====================
    
    def export_workflows(self) -> Dict:
        """Export all workflows"""
        return {
            'user_id': self.user_id,
            'workflows': self.data.get('workflows', []),
            'automations': self.data.get('automations', []),
            'exported_at': datetime.now().isoformat()
        }


def main():
    """Demo"""
    print("Workflow Discoverer")
    print("=" * 50)
    
    # Create discoverer
    discoverer = WorkflowDiscoverer("demo_user")
    
    # Record some tasks
    discoverer.record_task(
        task="analyze stock 600519",
        steps=["fetch_data", "compute_indicators", "generate_signal"],
        result="success"
    )
    
    discoverer.record_task(
        task="analyze stock 000858",
        steps=["fetch_data", "compute_indicators", "generate_signal"],
        result="success"
    )
    
    discoverer.record_task(
        task="analyze stock 600036",
        steps=["fetch_data", "compute_indicators", "generate_signal"],
        result="success"
    )
    
    # Discover workflows
    workflows = discoverer.discover_workflows()
    
    print(f"Discovered {len(workflows)} workflows:")
    for wf in workflows:
        print(f"  - {wf['name']} (confidence: {wf['confidence']:.0%})")
    
    # Create automation
    if workflows:
        auto = discoverer.create_automation(workflow=workflows[0])
        print(f"\nCreated automation: {auto['id']}")


if __name__ == "__main__":
    main()
