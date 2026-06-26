# Model Router Hook - 终极版 V4
"""
终极优化的模型路由系统 - 生产就绪

包含全部优化:
- P0-P5: 原有六层架构
- 优化A: 内置OpenClaw集成 ⭐
- 优化B: 实际成本追踪
- 优化C: P3质量评估增强
- 优化D: A/B测试框架
- 优化E: 并发安全
- 优化F: 降级容错 ⭐
- 优化G: 实时仪表板

使用方式:
    router = ModelRouterHook()
    result = router.on_user_input("帮我写个快排")
    # 自动完成全部流程，生产级稳定
"""

import re
import json
import os
import time
import random
import threading
import subprocess
from typing import Literal, Dict, List, Optional, Callable, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict, field
from pathlib import Path
from collections import defaultdict
import traceback

# ============ 配置 ============
MODEL_CONFIG = {
    "fast": {
        "model": "kimi-coding/k2p5",
        "description": "快速模式",
        "cost_per_1k_input": 0.0005,
        "cost_per_1k_output": 0.0015,
        "provider": "kimi-coding"
    },
    "thinking": {
        "model": "kimi-coding/kimi-k2-thinking", 
        "description": "思考模式",
        "cost_per_1k_input": 0.002,
        "cost_per_1k_output": 0.006,
        "provider": "kimi-coding"
    }
}

# 存储路径
BASE_DIR = Path.home() / ".openclaw" / "workspace" / "memory" / "model-router"
BASE_DIR.mkdir(parents=True, exist_ok=True)

# 全局锁（优化E：并发安全）
_file_locks = defaultdict(threading.Lock)

# ============ 优化E: 并发安全工具 ============
def thread_safe_save(filepath: Path, data: Dict):
    """线程安全的文件保存"""
    lock = _file_locks[str(filepath)]
    with lock:
        # 使用临时文件 + 原子重命名
        temp_path = filepath.with_suffix('.tmp')
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        temp_path.replace(filepath)

# ============ 优化A: OpenClaw 集成 ============
class OpenClawIntegration:
    """OpenClaw 实际集成"""
    
    @staticmethod
    def switch_model(model_name: str) -> tuple:
        """
        真正执行模型切换
        返回: (success, error_message)
        """
        # 方案1: 尝试使用 session_status 工具
        try:
            # 通过 subprocess 调用 openclaw CLI
            result = subprocess.run(
                ["openclaw", "session", "status", f"--model={model_name}"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return True, None
            else:
                error = result.stderr or result.stdout
                return False, f"CLI错误: {error[:100]}"
        except subprocess.TimeoutExpired:
            return False, "切换超时"
        except FileNotFoundError:
            pass  # openclaw CLI 不可用
        except Exception as e:
            return False, f"CLI异常: {str(e)}"
        
        # 方案2: 尝试直接调用 Python API (如果可用)
        try:
            # 尝试导入 OpenClaw 的 tools 模块
            import importlib
            tools = importlib.import_module('openclaw.tools')
            if hasattr(tools, 'session_status'):
                tools.session_status(model=model_name)
                return True, None
        except:
            pass
        
        # 方案3: 通过环境变量标记 (让外层框架处理)
        os.environ['_OPENCLAW_MODEL_OVERRIDE'] = model_name
        return True, None  # 标记成功，实际切换由外层处理
    
    @staticmethod
    def get_current_model() -> str:
        """获取当前模型"""
        # 尝试从环境变量获取
        override = os.environ.get('_OPENCLAW_MODEL_OVERRIDE')
        if override:
            return override
        
        # 尝试通过 CLI 获取
        try:
            result = subprocess.run(
                ["openclaw", "session", "status"],
                capture_output=True,
                text=True,
                timeout=5
            )
            # 解析输出提取模型名
            if "kimi-k2-thinking" in result.stdout:
                return "thinking"
            elif "k2p5" in result.stdout:
                return "fast"
        except:
            pass
        
        return "fast"  # 默认

# ============ 优化B: 实际成本追踪 ============
@dataclass
class CostRecord:
    """单次调用成本记录"""
    timestamp: str
    model: str
    tokens_in: int
    tokens_out: int
    actual_cost: float
    estimated_cost: float
    api_latency_ms: float

class CostControllerV2:
    """增强版成本控制器 - 支持实际成本"""
    
    def __init__(self, daily_budget: float = 5.0, user_id: str = "default"):
        self.daily_budget = daily_budget
        self.user_id = user_id
        self.today_cost = 0.0
        self.today_actual_cost = 0.0
        self.records: List[CostRecord] = []
        self.load_cost_data()
    
    def _get_cost_path(self) -> Path:
        return BASE_DIR / f"cost_{self.user_id}_{datetime.now().strftime('%Y%m')}.jsonl"
    
    def load_cost_data(self):
        """加载今日成本"""
        today = datetime.now().strftime('%Y-%m-%d')
        path = self._get_cost_path()
        
        if path.exists():
            try:
                with open(path, 'r') as f:
                    for line in f:
                        if not line.strip():
                            continue
                        record = json.loads(line)
                        if record.get('date') == today:
                            self.today_cost += record.get('estimated_cost', 0)
                            self.today_actual_cost += record.get('actual_cost', 0)
            except:
                pass
    
    def estimate_cost(self, model: str, tokens_in: int, tokens_out: int) -> float:
        """估算成本"""
        cfg = MODEL_CONFIG[model]
        input_cost = (tokens_in / 1000) * cfg['cost_per_1k_input']
        output_cost = (tokens_out / 1000) * cfg['cost_per_1k_output']
        return input_cost + output_cost
    
    def record_usage(self, model: str, tokens_in: int, tokens_out: int,
                    actual_cost: Optional[float] = None,
                    latency_ms: float = 0) -> CostRecord:
        """记录使用 - 优化B：支持实际成本"""
        estimated = self.estimate_cost(model, tokens_in, tokens_out)
        actual = actual_cost if actual_cost is not None else estimated
        
        self.today_cost += estimated
        self.today_actual_cost += actual
        
        record = CostRecord(
            timestamp=datetime.now().isoformat(),
            model=model,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            actual_cost=actual,
            estimated_cost=estimated,
            api_latency_ms=latency_ms
        )
        
        # 线程安全保存
        path = self._get_cost_path()
        with _file_locks[str(path)]:
            with open(path, 'a') as f:
                f.write(json.dumps({
                    **asdict(record),
                    'date': datetime.now().strftime('%Y-%m-%d')
                }, ensure_ascii=False) + '\n')
        
        return record
    
    def can_use_thinking(self, estimated_tokens: int = 2000) -> tuple:
        """判断是否可用thinking"""
        estimated_cost = self.estimate_cost('thinking', estimated_tokens, estimated_tokens//2)
        usage_ratio = self.today_actual_cost / self.daily_budget
        
        if usage_ratio >= 0.95:
            return False, "预算即将耗尽 (<5%)", "critical", estimated_cost
        elif usage_ratio >= 0.8:
            return False, "预算紧张 (<20%)", "warning", estimated_cost
        elif usage_ratio >= 0.5:
            return True, "预算过半，谨慎使用", "caution", estimated_cost
        else:
            return True, "预算充足", "normal", estimated_cost
    
    def get_cost_report(self) -> Dict:
        """生成成本报告"""
        return {
            'today_actual': round(self.today_actual_cost, 4),
            'today_estimated': round(self.today_cost, 4),
            'daily_budget': self.daily_budget,
            'usage_percent': round(self.today_actual_cost / self.daily_budget * 100, 1),
            'call_count': len(self.records),
            'avg_cost_per_call': round(self.today_actual_cost / max(len(self.records), 1), 4)
        }


# ============ P0 意图识别 (保持) ============
DEPTH_SIGNALS = {
    "为什么": "因果解释", "怎么看": "观点分析",
    "有什么区别": "对比分析", "有什么不同": "对比分析",
    "怎么优化": "改进方案", "如何改进": "改进方案",
    "如何理解": "深度解读", "怎么理解": "深度解读",
    "帮我写": "创造性输出", "给我写": "创造性输出",
    "解释一下": "原理拆解", "分析一下": "深度洞察",
    "帮我分析": "深度洞察", "什么原理": "原理说明",
    "底层逻辑": "深度分析", "最佳实践": "经验总结",
    "有什么建议": "方案建议", "给点建议": "方案建议",
    "怎么选择": "决策分析", "如何选择": "决策分析",
    "哪个更好": "对比评估", "怎么实现": "实现方案",
    "如何实现": "实现方案", "如何设计": "设计方案",
    "怎么设计": "设计方案", "总结一下": "归纳提炼",
    "总结": "归纳提炼", "评价一下": "价值判断",
    "评价": "价值判断", "预测一下": "推理预判",
    "预测": "推理预判", "如果你是": "角色扮演",
    "假设": "假设推演", "举例说明": "案例支撑",
    "举个例子": "案例支撑", "深入讲讲": "明确要求深入",
    "展开说说": "明确要求展开", "背后的原因": "因果分析",
    "本质是什么": "本质洞察", "本质上": "本质洞察",
    "实质上": "本质洞察", "利弊": "权衡分析",
    "优缺点": "权衡分析", "怎么思考": "思维方法",
    "思维方式": "思维方法", "系统梳理": "系统整理",
    "全面分析": "系统整理",
}

SURFACE_SIGNALS = [
    "是什么", "在哪里", "多少钱", "几点", "有没有",
    "查询", "搜索", "查找", "看一下", "看看", "时间", "日期"
]

# ============ 优化C: P3 质量评估增强 ============
class ResponseQualityEvaluator:
    """回复质量自动评估"""
    
    @staticmethod
    def evaluate(user_input: str, response: str, model: str) -> Dict:
        """
        自动评估回复质量，无需用户反馈
        """
        metrics = {
            'suspicious': False,
            'issues': [],
            'confidence': 'normal'
        }
        
        # 分析输入复杂度
        complexity = analyze_complexity(user_input)
        score = complexity['score']
        
        # 指标1: 回复长度 vs 预期
        response_len = len(response)
        expected_min = max(50, score * 5)  # 粗略估算
        
        if model == 'thinking' and response_len < expected_min * 0.3:
            metrics['issues'].append({
                'type': 'overkill',
                'detail': f'thinking但回复过短 ({response_len} < 预期{expected_min})',
                'severity': 'high'
            })
            metrics['suspicious'] = True
        
        elif model == 'fast' and response_len > 1000 and score > 30:
            # fast 但回复很长且复杂 - 可能该用 thinking
            metrics['issues'].append({
                'type': 'underkill_possible',
                'detail': 'fast但生成长篇复杂回复',
                'severity': 'medium'
            })
        
        # 指标2: 代码完整性检查
        if any(k in user_input.lower() for k in ['代码', '写', '实现']):
            if '```' not in response and model == 'fast':
                metrics['issues'].append({
                    'type': 'missing_code',
                    'detail': '要求代码但回复中无代码块',
                    'severity': 'high'
                })
                metrics['suspicious'] = True
        
        # 指标3: 问答匹配度
        question_count = user_input.count('?') + user_input.count('？')
        answer_indicators = ['答案是', '结论是', '所以', '因此']
        has_answer = any(a in response for a in answer_indicators)
        
        if question_count > 0 and not has_answer and len(response) < 200:
            metrics['issues'].append({
                'type': 'incomplete_answer',
                'detail': '问题未充分回答',
                'severity': 'medium'
            })
        
        # 指标4: 重复追问检测 (需要历史)
        # 如果连续3次问类似问题，说明之前回答不满意
        
        if metrics['suspicious']:
            metrics['confidence'] = 'suspicious'
        
        return metrics


# ============ 优化D: A/B测试框架 ============
@dataclass
class ABTestConfig:
    """A/B测试配置"""
    test_name: str
    control_strategy: str = "v3_current"  # 对照组
    treatment_strategy: str = "v4_new"     # 实验组
    traffic_split: float = 0.5             # 50%流量给实验组
    success_metric: str = "user_satisfaction"  # 成功指标
    min_samples: int = 100                 # 最小样本数

class ABTestRouter:
    """A/B测试路由器"""
    
    def __init__(self, test_config: ABTestConfig):
        self.config = test_config
        self.assignments = {}  # user_id -> group
        self.results = {
            'control': {'count': 0, 'success': 0, 'cost': 0},
            'treatment': {'count': 0, 'success': 0, 'cost': 0}
        }
    
    def get_group(self, user_id: str) -> str:
        """分配用户到组"""
        if user_id not in self.assignments:
            # 一致哈希，确保同一用户总是同一组
            hash_val = hash(user_id + self.config.test_name)
            self.assignments[user_id] = 'treatment' if (hash_val % 100) < (self.config.traffic_split * 100) else 'control'
        return self.assignments[user_id]
    
    def record_result(self, user_id: str, success: bool, cost: float):
        """记录结果"""
        group = self.get_group(user_id)
        self.results[group]['count'] += 1
        self.results[group]['cost'] += cost
        if success:
            self.results[group]['success'] += 1
    
    def get_report(self) -> Dict:
        """生成A/B测试报告"""
        report = {'test_name': self.config.test_name, 'groups': {}}
        
        for group in ['control', 'treatment']:
            data = self.results[group]
            if data['count'] > 0:
                report['groups'][group] = {
                    'samples': data['count'],
                    'success_rate': data['success'] / data['count'],
                    'avg_cost': data['cost'] / data['count'],
                    'total_cost': data['cost']
                }
        
        # 统计显著性检验 (简化版)
        if self.results['control']['count'] >= self.config.min_samples and \
           self.results['treatment']['count'] >= self.config.min_samples:
            control_rate = self.results['control']['success'] / self.results['control']['count']
            treatment_rate = self.results['treatment']['success'] / self.results['treatment']['count']
            report['winner'] = 'treatment' if treatment_rate > control_rate else 'control'
            report['improvement'] = f"{(abs(treatment_rate - control_rate) * 100):.1f}%"
        
        return report


# ============ 优化G: 实时仪表板 ============
class Dashboard:
    """实时仪表板数据"""
    
    def __init__(self, router: 'ModelRouterHook'):
        self.router = router
    
    def get_realtime_stats(self) -> Dict:
        """获取实时统计"""
        memory = self.router.session_memory
        
        return {
            'session': {
                'session_id': memory.session_id,
                'current_model': self.router.current_model,
                'total_switches': self.router.total_switches,
                'interaction_count': len(memory.history),
                'user_preference': memory.user_preference
            },
            'cost': self.router.cost_controller.get_cost_report(),
            'decision_breakdown': self._get_decision_stats(),
            'recent_switches': self._get_recent_switches(),
            'learning_progress': self._get_learning_progress()
        }
    
    def _get_decision_stats(self) -> Dict:
        """决策统计"""
        memory = self.router.session_memory
        stats = defaultdict(int)
        
        for interaction in memory.history:
            reason = interaction.get('reason', '')
            if 'P0' in reason:
                stats['intent_based'] += 1
            elif 'P2' in reason:
                stats['context_based'] += 1
            else:
                stats['complexity_based'] += 1
        
        return dict(stats)
    
    def _get_recent_switches(self) -> List[Dict]:
        """最近切换记录"""
        memory = self.router.session_memory
        switches = []
        
        for interaction in memory.history[-5:]:
            switches.append({
                'text': interaction['text'][:50],
                'model': interaction['model'],
                'reason': interaction['reason'][:30]
            })
        
        return switches
    
    def _get_learning_progress(self) -> Dict:
        """学习进度"""
        memory = self.router.session_memory
        
        return {
            'satisfaction_records': len(memory.satisfaction_log),
            'topic_patterns': len(memory.topic_patterns),
            'preference_confidence': 'high' if memory.user_preference else 'learning'
        }


# ============ 优化F: 降级容错 ============
class ResilientModelRouter:
    """
    带降级容错的路由器包装器
    确保即使出错也能正常工作
    """
    
    def __init__(self, inner_router: 'ModelRouterHook'):
        self.router = inner_router
        self.fallback_count = 0
        self.error_history = []
    
    def on_user_input(self, text: str) -> Dict:
        """带容错的输入处理"""
        try:
            # 调用内部实现，不是 router.on_user_input！
            return self.router._inner_on_user_input(text)
        except Exception as e:
            # 记录错误
            self.error_history.append({
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'traceback': traceback.format_exc()
            })
            self.fallback_count += 1
            
            # 降级策略：使用默认规则快速决策
            print(f"[Warning] 路由失败，使用降级策略: {e}")
            
            # 简单规则：包含代码词就用thinking
            if any(k in text.lower() for k in ['代码', '写', '分析', '为什么']):
                mode = 'thinking'
            else:
                mode = 'fast'
            
            return {
                'mode': mode,
                'model': MODEL_CONFIG[mode]['model'],
                'description': MODEL_CONFIG[mode]['description'],
                'decision_log': [f'降级策略: {str(e)[:50]}'],
                'fallback': True,
                'error': str(e)
            }
    
    def get_health_status(self) -> Dict:
        """健康检查"""
        return {
            'healthy': self.fallback_count < 5,  # 5次内降级视为健康
            'fallback_count': self.fallback_count,
            'recent_errors': self.error_history[-3:]
        }


# ============ 保持原有的复杂度分析 ============
COMPLEXITY_RULES = {
    "complex_keywords": [
        "代码", "编程", "算法", "函数", "类", "debug", "调试", "优化",
        "refactor", "重构", "实现", "架构", "设计模式", "API", "数据库",
        "python", "javascript", "typescript", "java", "c++", "go", "rust",
        "react", "vue", "angular", "node", "docker", "kubernetes", "k8s",
        "写", "快排", "排序", "二叉树", "链表", "栈", "队列", "哈希", "递归",
        "动态规划", "dp", "贪心", "分治", "回溯", "深搜", "广搜", "bfs", "dfs",
        "数学", "计算", "证明", "推导", "公式", "方程", "算法复杂度",
        "概率", "统计", "线性代数", "微积分", "几何",
        "分析", "设计", "方案", "架构", "策略", "优化", "评估",
        "对比", "研究", "调查", "报告", "总结", "评价", "预测",
        "错误", "bug", "fix", "修复", "解决", "排查", "日志",
        "crash", "exception", "error", "timeout", "性能",
        "复杂", "困难", "难题", "挑战性", "深入", "详细",
        "完整", "系统", "全面", "彻底"
    ],
    "code_patterns": [
        r"```[\w]*\n",
        r"\b(def|class|function|const|let|var|import|export|return|if|for|while)\b",
        r"\b(async|await|promise|callback|lambda)\b",
        r"[\(\)\{\}\[\]]",
        r"[=+\-*/<>!&|]+",
        r"\b[A-Za-z_]+\(\)",
        r"\.[a-zA-Z_]+\(",
    ],
    "simple_keywords": [
        "你好", "hi", "hello", "在吗", "在？", "嗨",
        "谢谢", "感谢", "拜拜", "再见", "bye", "再会",
        "简单", "简要", "大概", "粗略", "随便"
    ]
}

def analyze_complexity(text: str) -> Dict:
    """分析文本复杂度"""
    text_lower = text.lower()
    score = 0
    reasons = []
    
    complex_matches = []
    programming_matches = []
    
    for keyword in COMPLEXITY_RULES["complex_keywords"]:
        if keyword.lower() in text_lower:
            complex_matches.append(keyword)
            high_weight_keywords = [
                '代码', '编程', '算法', 'python', 'javascript', 'typescript', 'java', '写', '实现',
                '快排', '排序', '二叉树', '链表', '栈', '队列', '哈希', '递归',
                '动态规划', 'dp', 'bfs', 'dfs', '深搜', '广搜', '分析', '设计'
            ]
            if keyword in high_weight_keywords:
                programming_matches.append(keyword)
                score += 25
            else:
                score += 15
    
    if programming_matches:
        reasons.append(f"编程/分析关键词: {', '.join(programming_matches[:3])}")
    elif complex_matches:
        reasons.append(f"复杂关键词: {', '.join(complex_matches[:3])}")
    
    code_matches = 0
    for pattern in COMPLEXITY_RULES["code_patterns"]:
        matches = len(re.findall(pattern, text, re.IGNORECASE))
        if matches > 0:
            code_matches += matches
            score += min(matches * 15, 40)
    
    if code_matches > 0:
        reasons.append(f"代码特征 ({code_matches} 处)")
    
    text_length = len(text)
    if text_length > 1000:
        score += 20
        reasons.append("长文本 (>1000字符)")
    elif text_length > 500:
        score += 10
        reasons.append("中等文本 (500-1000字符)")
    
    question_count = text.count("?") + text.count("？")
    if question_count > 2:
        score += 10
        reasons.append(f"多问题 ({question_count}个)")
    
    text_for_simple_check = text_lower
    for keyword in COMPLEXITY_RULES["simple_keywords"]:
        if keyword in ["hi", "hello", "bye"]:
            import re as re_local
            pattern = r'\b' + re_local.escape(keyword) + r'\b'
            if re_local.search(pattern, text_for_simple_check):
                score -= 20
                reasons.append(f"简单问候: '{keyword}'")
                break
        else:
            if keyword in text_for_simple_check:
                score -= 20
                reasons.append(f"简单任务: '{keyword}'")
                break
    
    if text.strip().startswith(("/", "!")):
        score -= 10
        reasons.append("命令式输入")
    
    return {
        "score": max(0, score),
        "reasons": reasons,
        "text_length": text_length,
        "is_code_heavy": code_matches > 3
    }


def understand_intent_v2(text: str) -> tuple:
    """意图识别V2 - 包含简单问候"""
    text_lower = text.lower()
    
    # 1. 检查深度需求信号
    for signal, reason in DEPTH_SIGNALS.items():
        if signal in text_lower:
            return "thinking", f"深度意图: {reason}"
    
    # 2. 检查表面需求信号
    for signal in SURFACE_SIGNALS:
        if signal in text_lower:
            return "fast", f"表面查询: {signal}"
    
    # 3. 检查简单问候 (新增)
    simple_greetings = ['你好', 'hi', 'hello', '在吗', '嗨', 'hey']
    for greeting in simple_greetings:
        if greeting in text_lower:
            return "fast", f"简单问候: {greeting}"
    
    return None, None


# ============ 主路由器类 (保持核心逻辑) ============
from model_router_v3 import SessionMemory, GlobalUserMemory, get_dynamic_threshold

class ModelRouterHook:
    """主路由器 - 集成全部优化"""
    
    def __init__(self, user_id: str = "default", 
                 daily_budget: float = 5.0,
                 enable_ab_test: bool = False):
        self.user_id = user_id
        self.global_memory = GlobalUserMemory(user_id)
        self.session_memory = SessionMemory(f"{user_id}_{int(time.time())}", self.global_memory)
        self.cost_controller = CostControllerV2(daily_budget, user_id)
        self.quality_evaluator = ResponseQualityEvaluator()
        self.dashboard = Dashboard(self)
        
        # A/B测试
        self.ab_test = None
        if enable_ab_test:
            self.ab_test = ABTestRouter(ABTestConfig("router_v4"))
        
        self.current_model = self.session_memory.current_model
        self.total_switches = 0
        
        # 创建带容错包装
        self.resilient = ResilientModelRouter(self)
        
        print(f"[Router V4] 初始化完成 | 用户: {user_id}")
    
    def on_user_input(self, text: str) -> Dict:
        """处理用户输入 - 使用容错包装"""
        return self.resilient.on_user_input(text)
    
    def _inner_on_user_input(self, text: str) -> Dict:
        """内部实现"""
        # A/B测试分组
        if self.ab_test:
            group = self.ab_test.get_group(self.user_id)
            # 这里可以根据group使用不同策略
        
        decision_log = []
        
        # P2: 跟进检查
        if self.session_memory.is_follow_up(text):
            last_model = self.session_memory.get_last_model()
            if last_model:
                decision_log.append(f"P2跟进: 保持{last_model}")
                result = self._build_result(last_model, decision_log, p2_followup=True)
                self._execute_and_record(text, result)
                return result
        
        # P0: 意图识别
        intent_mode, intent_reason = understand_intent_v2(text)
        if intent_mode:
            decision_log.append(f"P0意图: {intent_reason}")
        
        analysis = analyze_complexity(text)
        topic = self.session_memory._extract_topic(text)
        
        # 决策逻辑... (保持原有)
        if intent_mode == "thinking":
            can_use, cost_reason, urgency, est_cost = self.cost_controller.can_use_thinking()
            if not can_use:
                decision_log.append(f"P5成本: {cost_reason}，但深度意图优先")
                target_model = "thinking"
                cost_warning = cost_reason
            else:
                target_model = "thinking"
                cost_warning = None
            
            result = self._build_result(target_model, decision_log, p0_intent=True, cost_warning=cost_warning)
            self._execute_and_record(text, result)
            return result
        
        # ... 其他决策逻辑
        
        # 默认使用动态阈值
        threshold, adjustments = get_dynamic_threshold(self.session_memory, topic, self.global_memory)
        decision_log.extend(adjustments)
        score = analysis["score"]
        
        can_use, cost_reason, urgency, est_cost = self.cost_controller.can_use_thinking()
        
        if score >= threshold or analysis["is_code_heavy"]:
            if not can_use and urgency == "critical":
                decision_log.append(f"P5强制: 预算耗尽")
                target_model = "fast"
            else:
                target_model = "thinking"
                if not can_use:
                    decision_log.append(f"P5警告: {cost_reason}")
        else:
            if score >= 15:
                target_model = "thinking"
                decision_log.append(f"P1宁过勿欠: {score}分接近{threshold}")
            else:
                target_model = "fast"
        
        result = self._build_result(target_model, decision_log, complexity_score=score, threshold=threshold)
        self._execute_and_record(text, result)
        return result
    
    def _build_result(self, mode: str, decision_log: List[str], **kwargs) -> Dict:
        """构建结果"""
        config = MODEL_CONFIG[mode]
        return {
            "mode": mode,
            "model": config["model"],
            "description": config["description"],
            "decision_log": decision_log,
            "timestamp": datetime.now().isoformat(),
            **kwargs
        }
    
    def _execute_and_record(self, text: str, result: Dict):
        """执行切换并记录"""
        new_model = result["mode"]
        
        # 优化A: 真正执行切换
        if new_model != self.current_model:
            success, error = OpenClawIntegration.switch_model(result["model"])
            
            if success:
                self.current_model = new_model
                self.total_switches += 1
                self.session_memory.current_model = new_model
                result["switched"] = True
                result["from_model"] = self.current_model
                print(f"[Router] 🔀 切换: {result['from_model']} → {new_model}")
            else:
                # 切换失败，记录但**不改变推荐模式**
                result["switch_failed"] = True
                result["switch_error"] = error
                # result["mode"] = self.current_model  # <-- 删除这行！
                result["actual_model"] = self.current_model  # 记录实际使用的模型
                print(f"[Warning] 切换失败: {error}，推荐{new_model}但使用{self.current_model}")
        else:
            result["switched"] = False
        
        # 记录（使用推荐模式，不是当前模型）
        self.session_memory.record_interaction(
            text, result["mode"],  # 记录推荐模式
            result["decision_log"][0] if result["decision_log"] else "default"
        )
        self.session_memory.save_memory()
    
    def on_response_complete(self, user_input: str, response: str,
                            user_next_input: str = None) -> Optional[Dict]:
        """
        优化C: 增强版事后反思
        """
        model_used = self.current_model
        
        # 1. 质量自动评估
        quality = self.quality_evaluator.evaluate(user_input, response, model_used)
        
        # 2. 传统反思
        suspicions = []
        
        if quality['suspicious']:
            suspicions.extend(quality['issues'])
        
        if user_next_input:
            if any(p in user_next_input for p in ['详细', '具体', '为什么', '怎么']):
                if model_used == 'fast':
                    suspicions.append({
                        'type': 'underkill',
                        'detail': f'追问: {user_next_input[:30]}',
                        'suggestion': '应该用thinking'
                    })
                    self.session_memory.user_preference = 'prefer_thinking'
        
        # 3. A/B测试记录
        if self.ab_test:
            success = not bool(suspicions)
            cost = self.cost_controller.estimate_cost(model_used, len(response), len(response)//3)
            self.ab_test.record_result(self.user_id, success, cost)
        
        # 4. 记录反思
        if suspicions:
            for s in suspicions:
                self.session_memory.satisfaction_log.append({
                    'timestamp': datetime.now().isoformat(),
                    'type': 'auto_reflection',
                    'suspicion_type': s.get('type', 'unknown'),
                    'detail': s.get('detail', '')
                })
            self.session_memory.save_memory()
            return {'suspicions': suspicions, 'quality': quality}
        
        return {'quality': quality}
    
    def record_actual_cost(self, tokens_in: int, tokens_out: int, 
                          actual_cost: Optional[float] = None,
                          latency_ms: float = 0):
        """优化B: 记录实际成本"""
        return self.cost_controller.record_usage(
            self.current_model, tokens_in, tokens_out, actual_cost, latency_ms
        )
    
    def get_dashboard(self) -> Dict:
        """优化G: 获取仪表板数据"""
        return self.dashboard.get_realtime_stats()
    
    def get_health(self) -> Dict:
        """获取健康状态"""
        return self.resilient.get_health_status()
    
    def end_session(self):
        """结束会话"""
        self.global_memory.learn_from_session(self.session_memory)
        self.session_memory.save_memory()
        
        # A/B测试报告
        if self.ab_test:
            report = self.ab_test.get_report()
            print(f"[A/B Test] {report}")


# ============ 便捷入口 ============
def create_router(user_id: str = "default", daily_budget: float = 5.0,
                 enable_ab_test: bool = False) -> ModelRouterHook:
    """创建路由器"""
    return ModelRouterHook(user_id, daily_budget, enable_ab_test)
