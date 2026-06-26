"""
Meta Skill Optimizer - Self-improving AI capability
"""
import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from collections import defaultdict
import numpy as np


class SkillOptimizer:
    """Self-improving skill optimizer"""
    
    def __init__(
        self,
        skill_name: str,
        learning_rate: float = 0.1,
        storage_path: str = None
    ):
        self.skill_name = skill_name
        self.learning_rate = learning_rate
        
        # Storage
        self.storage_path = storage_path or f"~/.meta_optimizer/{skill_name}.json"
        self.data = self._load()
        
        # Initialize data structures
        self.data.setdefault('successes', [])
        self.data.setdefault('failures', [])
        self.data.setdefault('patterns', {})
        self.data.setdefault('prompts', {'effective': [], 'ineffective': []})
        self.data.setdefault('tools', defaultdict(list))
        self.data.setdefault('capabilities', {})
        self.data.setdefault('version', 1)
    
    def _load(self) -> Dict:
        """Load knowledge base"""
        path = os.path.expanduser(self.storage_path)
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return {}
    
    def _save(self):
        """Save knowledge base"""
        path = os.path.expanduser(self.storage_path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    # ==================== Feedback Learning ====================
    
    def record_success(
        self,
        task: str,
        approach: str,
        context: Dict = None,
        outcome: Dict = None
    ):
        """Record successful execution"""
        record = {
            'task': task,
            'approach': approach,
            'context': context or {},
            'outcome': outcome or {},
            'timestamp': datetime.now().isoformat(),
            'version': self.data['version']
        }
        
        self.data['successes'].append(record)
        
        # Learn pattern
        self._learn_pattern(task, approach, True)
        
        self._save()
        
        return {'status': 'recorded', 'insights': self._generate_insights(task)}
    
    def record_failure(
        self,
        task: str,
        approach: str,
        error: str = None,
        lesson: str = None,
        context: Dict = None
    ):
        """Record failed execution"""
        record = {
            'task': task,
            'approach': approach,
            'error': error,
            'lesson': lesson,
            'context': context or {},
            'timestamp': datetime.now().isoformat(),
            'version': self.data['version']
        }
        
        self.data['failures'].append(record)
        
        # Learn what not to do
        self._learn_pattern(task, approach, False)
        
        self._save()
        
        return {'status': 'recorded', 'lesson': lesson or self._extract_lesson(error)}
    
    def _learn_pattern(self, task: str, approach: str, success: bool):
        """Learn from execution"""
        task_type = self._categorize_task(task)
        
        if task_type not in self.data['patterns']:
            self.data['patterns'][task_type] = {'successes': {}, 'failures': {}}
        
        key = approach[:50]  # Truncate for grouping
        
        if success:
            count = self.data['patterns'][task_type]['successes'].get(key, 0)
            self.data['patterns'][task_type]['successes'][key] = count + 1
        else:
            count = self.data['patterns'][task_type]['failures'].get(key, 0)
            self.data['patterns'][task_type]['failures'][key] = count + 1
    
    def _categorize_task(self, task: str) -> str:
        """Categorize task type"""
        task_lower = task.lower()
        
        if any(kw in task_lower for kw in ['analyze', 'analysis', 'data']):
            return 'data_analysis'
        elif any(kw in task_lower for kw in ['write', 'create', 'generate']):
            return 'content_creation'
        elif any(kw in task_lower for kw in ['search', 'find', 'lookup']):
            return 'research'
        elif any(kw in task_lower for kw in ['code', 'program', 'debug']):
            return 'coding'
        elif any(kw in task_lower for kw in ['trade', 'invest', 'stock']):
            return 'trading'
        else:
            return 'general'
    
    def _extract_lesson(self, error: str) -> str:
        """Extract lesson from error"""
        if not error:
            return "Unknown error - needs investigation"
        
        error_lower = error.lower()
        
        lessons = {
            'timeout': "Increase timeout or optimize approach",
            'not found': "Verify resource exists before using",
            'permission': "Check access permissions",
            'rate limit': "Add rate limiting or caching",
            'invalid': "Validate inputs before processing",
            'memory': "Reduce data size or use streaming"
        }
        
        for key, lesson in lessons.items():
            if key in error_lower:
                return lesson
        
        return "Analyze error and adjust approach"
    
    # ==================== Insights ====================
    
    def get_insights(self) -> Dict:
        """Get learned insights"""
        insights = {
            'total_successes': len(self.data.get('successes', [])),
            'total_failures': len(self.data.get('failures', [])),
            'success_rate': self._calculate_success_rate(),
            'patterns': self._summarize_patterns(),
            'top_approaches': self._get_top_approaches(),
            'common_errors': self._get_common_errors()
        }
        
        return insights
    
    def _calculate_success_rate(self) -> float:
        """Calculate overall success rate"""
        successes = len(self.data.get('successes', []))
        failures = len(self.data.get('failures', []))
        
        total = successes + failures
        if total == 0:
            return 0.0
        
        return successes / total
    
    def _summarize_patterns(self) -> Dict:
        """Summarize learned patterns"""
        patterns = self.data.get('patterns', {})
        
        summary = {}
        for task_type, data in patterns.items():
            success_count = sum(data.get('successes', {}).values())
            failure_count = sum(data.get('failures', {}).values())
            
            if success_count + failure_count > 0:
                summary[task_type] = {
                    'success_rate': success_count / (success_count + failure_count),
                    'total_attempts': success_count + failure_count
                }
        
        return summary
    
    def _get_top_approaches(self) -> List[Dict]:
        """Get most successful approaches"""
        patterns = self.data.get('patterns', {})
        
        approaches = []
        for task_type, data in patterns.items():
            for approach, count in data.get('successes', {}).items():
                approaches.append({
                    'task_type': task_type,
                    'approach': approach,
                    'success_count': count
                })
        
        # Sort by success count
        approaches.sort(key=lambda x: x['success_count'], reverse=True)
        
        return approaches[:10]
    
    def _get_common_errors(self) -> List[Dict]:
        """Get most common errors"""
        errors = defaultdict(int)
        
        for failure in self.data.get('failures', []):
            error = failure.get('error', 'Unknown')
            errors[error] += 1
        
        return [
            {'error': k, 'count': v}
            for k, v in sorted(errors.items(), key=lambda x: x[1], reverse=True)[:10]
        ]
    
    # ==================== Optimization ====================
    
    def get_best_approach(
        self,
        task_type: str,
        context: Dict = None
    ) -> Dict:
        """Get best approach for task"""
        patterns = self.data.get('patterns', {}).get(task_type, {})
        
        successes = patterns.get('successes', {})
        
        if not successes:
            return {
                'approach': 'default',
                'confidence': 0.0,
                'note': 'No prior data - using default approach'
            }
        
        # Find best approach
        best_approach = max(successes.items(), key=lambda x: x[1])
        
        # Calculate confidence
        total = sum(successes.values())
        confidence = best_approach[1] / total if total > 0 else 0
        
        return {
            'approach': best_approach[0],
            'confidence': confidence,
            'success_count': best_approach[1],
            'alternatives': list(successes.keys())[:3]
        }
    
    def optimize_prompt(
        self,
        original_prompt: str,
        outcome: str = None,
        feedback: str = None
    ) -> str:
        """Optimize prompt based on feedback"""
        # Add to effective/ineffective lists
        if outcome in ['success', 'good', 'high']:
            self.data['prompts']['effective'].append(original_prompt)
        elif outcome in ['failure', 'bad', 'low']:
            self.data['prompts']['ineffective'].append(original_prompt)
        
        # Apply feedback
        optimized = original_prompt
        
        if feedback:
            feedback_lower = feedback.lower()
            
            # Specificity improvements
            if 'specific' in feedback_lower or 'vague' in feedback_lower:
                optimized = self._make_specific(optimized)
            
            # Context improvements
            if 'context' in feedback_lower or 'ambiguous' in feedback_lower:
                optimized = self._add_context(optimized)
            
            # Actionability
            if 'action' in feedback_lower or 'unclear' in feedback_lower:
                optimized = self._make_actionable(optimized)
        
        self._save()
        
        return optimized
    
    def _make_specific(self, prompt: str) -> str:
        """Make prompt more specific"""
        # Add specific request
        if 'analyze' in prompt.lower():
            prompt += " Specifically, identify key trends, patterns, and anomalies."
        elif 'summarize' in prompt.lower():
            prompt += " Provide structured bullet points with key takeaways."
        
        return prompt
    
    def _add_context(self, prompt: str) -> str:
        """Add context to prompt"""
        prompt += " Consider the context: user background, goals, and constraints."
        return prompt
    
    def _make_actionable(self, prompt: str) -> str:
        """Make prompt more actionable"""
        prompt += " Output should be actionable with clear next steps."
        return prompt
    
    def generate_examples(self, task: str, n: int = 3) -> List[str]:
        """Generate few-shot examples"""
        task_type = self._categorize_task(task)
        
        # Get similar successful tasks
        examples = []
        
        for success in self.data.get('successes', [])[-50:]:
            if self._categorize_task(success['task']) == task_type:
                examples.append(success['approach'])
                if len(examples) >= n:
                    break
        
        return examples
    
    # ==================== Tool Optimization ====================
    
    def suggest_tools(
        self,
        task: str,
        context: Dict = None
    ) -> List[Dict]:
        """Suggest best tools for task"""
        task_type = self._categorize_task(task)
        
        # Map task types to tools
        tool_map = {
            'data_analysis': [
                {'tool': 'pandas', 'score': 0.9},
                {'tool': 'auto-data-analyzer', 'score': 0.85}
            ],
            'coding': [
                {'tool': 'cursor', 'score': 0.9},
                {'tool': 'claude-code', 'score': 0.85}
            ],
            'research': [
                {'tool': 'tavily', 'score': 0.9},
                {'tool': 'browser', 'score': 0.8}
            ],
            'content_creation': [
                {'tool': 'gpt', 'score': 0.9},
                {'tool': 'image-generation', 'score': 0.8}
            ],
            'trading': [
                {'tool': 'quant-research-platform', 'score': 0.9},
                {'tool': 'quant-trading-api', 'score': 0.85}
            ]
        }
        
        # Check for learned preferences
        learned_tools = self.data.get('tools', {}).get(task_type, [])
        
        if learned_tools:
            return learned_tools[:5]
        
        return tool_map.get(task_type, [{'tool': 'default', 'score': 0.5}])
    
    def optimize_params(
        self,
        tool: str,
        task: str,
        params: Dict,
        result: Dict
    ) -> Dict:
        """Optimize tool parameters based on result"""
        key = f"{tool}:{task}"
        
        if 'param_history' not in self.data:
            self.data['param_history'] = {}
        
        if key not in self.data['param_history']:
            self.data['param_history'][key] = []
        
        # Record this attempt
        self.data['param_history'][key].append({
            'params': params,
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
        
        # Analyze and optimize
        optimized = self._optimize_params_analysis(key)
        
        self._save()
        
        return optimized
    
    def _optimize_params_analysis(self, key: str) -> Dict:
        """Analyze parameter history and optimize"""
        history = self.data['param_history'].get(key, [])
        
        if len(history) < 3:
            return {'status': 'insufficient_data', 'recommendation': params}
        
        # Find best params
        best = max(history, key=lambda x: x['result'].get('score', 0))
        
        return {
            'recommended_params': best['params'],
            'best_score': best['result'].get('score', 0),
            'attempts': len(history)
        }
    
    # ==================== Self-Diagnosis ====================
    
    def assess_capability(
        self,
        task: str,
        context: Dict = None
    ) -> Dict:
        """Assess if capable of task"""
        task_type = self._categorize_task(task)
        
        # Check history
        patterns = self.data.get('patterns', {}).get(task_type, {})
        
        success_count = sum(patterns.get('successes', {}).values())
        failure_count = sum(patterns.get('failures', {}).values())
        
        total = success_count + failure_count
        
        if total == 0:
            return {
                'capable': True,  # Assume capable until proven otherwise
                'confidence': 0.3,
                'reason': 'No prior experience - default to try'
            }
        
        success_rate = success_count / total
        
        if success_rate > 0.8:
            return {
                'capable': True,
                'confidence': 0.9,
                'reason': f'High success rate ({success_rate:.0%})'
            }
        elif success_rate > 0.5:
            return {
                'capable': True,
                'confidence': 0.6,
                'reason': f'Moderate success rate ({success_rate:.0%})'
            }
        else:
            return {
                'capable': False,
                'confidence': 0.8,
                'reason': f'Low success rate ({success_rate:.0%}) - recommend human help'
            }
    
    def identify_gaps(self) -> List[Dict]:
        """Identify knowledge gaps"""
        gaps = []
        
        patterns = self.data.get('patterns', {})
        
        for task_type, data in patterns.items():
            success_count = sum(data.get('successes', {}).values())
            failure_count = sum(data.get('failures', {}).values())
            
            if failure_count > success_count:
                gaps.append({
                    'task_type': task_type,
                    'failure_rate': failure_count / (success_count + failure_count),
                    'recommendation': f'Need more training on {task_type}'
                })
        
        # Sort by failure rate
        gaps.sort(key=lambda x: x['failure_rate'], reverse=True)
        
        return gaps
    
    def calibrate_confidence(
        self,
        predicted_confidence: float,
        actual_outcome: bool
    ) -> float:
        """Calibrate confidence based on actual outcomes"""
        # Simple calibration
        error = (predicted_confidence - (1.0 if actual_outcome else 0.0))
        
        # Adjust learning rate
        calibrated = predicted_confidence - (self.learning_rate * error)
        
        return max(0.0, min(1.0, calibrated))
    
    # ==================== Evolution ====================
    
    def track_improvement(self) -> Dict:
        """Track improvement over time"""
        successes = self.data.get('successes', [])
        failures = self.data.get('failures', [])
        
        if not successes and not failures:
            return {'status': 'no_data'}
        
        # Group by week
        from datetime import datetime
        
        weekly = defaultdict(lambda: {'success': 0, 'failure': 0})
        
        for s in successes:
            week = datetime.fromisoformat(s['timestamp']).isocalendar()[1]
            weekly[week]['success'] += 1
        
        for f in failures:
            week = datetime.fromisoformat(f['timestamp']).isocalendar()[1]
            weekly[week]['failure'] += 1
        
        # Calculate trend
        weeks = sorted(weekly.keys())
        
        if len(weeks) < 2:
            return {'trend': 'insufficient_data'}
        
        early_rate = (
            weekly[weeks[0]]['success'] / 
            (weekly[weeks[0]]['success'] + weekly[weeks[0]]['failure'])
        )
        late_rate = (
            weekly[weeks[-1]]['success'] / 
            (weekly[weeks[-1]]['success'] + weekly[weeks[-1]]['failure'])
        )
        
        return {
            'early_success_rate': early_rate,
            'late_success_rate': late_rate,
            'improvement': late_rate - early_rate,
            'trend': 'improving' if late_rate > early_rate else 'declining'
        }
    
    def export_knowledge(self) -> Dict:
        """Export learned knowledge"""
        return {
            'skill_name': self.skill_name,
            'version': self.data.get('version', 1),
            'patterns': self.data.get('patterns', {}),
            'insights': self.get_insights(),
            'exported_at': datetime.now().isoformat()
        }
    
    def merge_experiences(self, other_optimizer: 'SkillOptimizer'):
        """Merge experiences from another optimizer"""
        # Merge successes
        self.data['successes'].extend(other_optimizer.data.get('successes', []))
        
        # Merge failures
        self.data['failures'].extend(other_optimizer.data.get('failures', []))
        
        # Merge patterns
        for task_type, patterns in other_optimizer.data.get('patterns', {}).items():
            if task_type not in self.data['patterns']:
                self.data['patterns'][task_type] = {'successes': {}, 'failures': {}}
            
            for approach, count in patterns.get('successes', {}).items():
                key = approach[:50]
                self.data['patterns'][task_type]['successes'][key] = (
                    self.data['patterns'][task_type]['successes'].get(key, 0) + count
                )
        
        # Increment version
        self.data['version'] += 1
        
        self._save()
        
        return {'status': 'merged', 'new_version': self.data['version']}


def main():
    """Demo"""
    print("Meta Skill Optimizer")
    print("=" * 50)
    
    # Create optimizer
    optimizer = SkillOptimizer("demo_skill")
    
    # Record some experiences
    optimizer.record_success(
        task="analyze sales data",
        approach="used pandas groupby and aggregation",
        context={"data_size": "10MB"},
        outcome={"success": True, "quality": "high"}
    )
    
    optimizer.record_failure(
        task="predict stock price",
        approach="used linear regression",
        error="insufficient features",
        lesson="need more technical indicators"
    )
    
    # Get insights
    insights = optimizer.get_insights()
    print(f"Success Rate: {insights['success_rate']:.1%}")
    
    # Get best approach
    best = optimizer.get_best_approach("data_analysis")
    print(f"Best approach: {best}")
    
    # Assess capability
    cap = optimizer.assess_capability("analyze data")
    print(f"Capability: {cap}")


if __name__ == "__main__":
    main()
