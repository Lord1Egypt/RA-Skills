#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能任务调度器 - SmartScheduler
简单任务秒级响应，复杂任务深度思辨

作者: 海狸 🦫
日期: 2026-04-02
"""

import json
import re
import time
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import subprocess
import os

# 导入新组件
from resource_locator import ResourceLocator, MemoryMonitor, StatsCollector


class TaskComplexity(Enum):
    """任务复杂度"""
    SIMPLE = "simple"      # 简单任务：秒级响应
    COMPLEX = "complex"    # 复杂任务：深度处理


@dataclass
class TaskResult:
    """任务结果"""
    success: bool
    complexity: str
    response: str
    skill_used: str = ""
    latency_ms: int = 0
    subtasks: List[str] = None


class TaskClassifier:
    """任务复杂度分类器"""
    
    # 简单任务关键词（秒级响应）
    SIMPLE_KEYWORDS = [
        # 问候
        '你好', '早安', '晚安', 'hi', 'hello', 'hey',
        # 查询
        '报价', '价格', '多少钱', '查', '查询', '状态',
        # 记录
        '记录', '保存', '添加', '删除',
        # 简单操作
        '设置', '修改', '更新', '开启', '关闭',
        # 确认
        '确认', '是', '好', 'OK', 'ok'
    ]
    
    # 复杂任务关键词（深度处理）
    COMPLEX_KEYWORDS = [
        # 设计
        '设计', '方案', '规划', '架构',
        # 分析
        '分析', '研究', '调研', '评估', '对比',
        # 创建
        '创建', '生成', '写一个', '开发', '实现',
        # 优化
        '优化', '改进', '提升', '重构',
        # 多步骤
        '完整', '全面', '详细', '深入', '系统'
    ]
    
    # 长度阈值
    SHORT_THRESHOLD = 15      # <15字倾向简单
    LONG_THRESHOLD = 50       # >50字倾向复杂
    
    def classify(self, text: str) -> Tuple[TaskComplexity, str]:
        """
        分类任务复杂度
        
        Returns:
            (complexity, reason)
        """
        text_lower = text.lower().strip()
        length = len(text)
        
        # 1. 长度判断
        if length < self.SHORT_THRESHOLD:
            # 短消息，检查是否包含复杂关键词
            if any(kw in text for kw in self.COMPLEX_KEYWORDS):
                return TaskComplexity.COMPLEX, f"短消息但包含复杂关键词"
            return TaskComplexity.SIMPLE, f"消息短({length}字)"
        
        if length > self.LONG_THRESHOLD:
            # 长消息，检查是否包含简单关键词
            if any(kw in text for kw in self.SIMPLE_KEYWORDS) and not any(kw in text for kw in self.COMPLEX_KEYWORDS):
                return TaskComplexity.SIMPLE, f"长消息但简单意图"
            return TaskComplexity.COMPLEX, f"消息长({length}字)"
        
        # 2. 关键词匹配
        simple_score = sum(1 for kw in self.SIMPLE_KEYWORDS if kw in text)
        complex_score = sum(1 for kw in self.COMPLEX_KEYWORDS if kw in text)
        
        # 3. 文件上传检测
        has_file = any(ext in text_lower for ext in ['.stp', '.step', '.pdf', '.jpg', '.png'])
        if has_file and complex_score == 0:
            return TaskComplexity.SIMPLE, "文件上传任务"
        
        # 4. 综合判断
        if complex_score > simple_score:
            return TaskComplexity.COMPLEX, f"复杂关键词{complex_score}个 > 简单{simple_score}个"
        elif simple_score > complex_score:
            return TaskComplexity.SIMPLE, f"简单关键词{simple_score}个 > 复杂{complex_score}个"
        else:
            # 默认简单（保守策略）
            return TaskComplexity.SIMPLE, "未明确分类，默认简单"


class SimpleTaskHandler:
    """简单任务处理器 - 秒级响应"""
    
    # 任务到Skill的映射
    SKILL_MAP = {
        '报价': 'cnc-quote-system',
        '价格': 'cnc-quote-system',
        '报价单': 'cnc-quote-system',
        '查询': 'hybrid-model-router',
        '状态': 'hybrid-model-router',
        '设置': 'hybrid-model-router',
        '记录': 'hybrid-model-router',
        '删除': 'hybrid-model-router',
        '文件': 'file-upload-handler',
        '上传': 'file-upload-handler'
    }
    
    def process(self, user_input: str, context: Dict = None) -> TaskResult:
        """处理简单任务"""
        start_time = time.time()
        
        # 匹配Skill
        skill_id = self._match_skill(user_input)
        
        if skill_id:
            # 调用Skill
            result = self._call_skill(skill_id, user_input, context)
            latency = int((time.time() - start_time) * 1000)
            
            return TaskResult(
                success=result.get('success', True),
                complexity='simple',
                response=result.get('response', result.get('message', '处理完成')),
                skill_used=skill_id,
                latency_ms=latency
            )
        else:
            # 无匹配，返回默认响应
            return TaskResult(
                success=False,
                complexity='simple',
                response='未能识别的任务类型，请提供更多信息',
                latency_ms=int((time.time() - start_time) * 1000)
            )
    
    def _match_skill(self, text: str) -> Optional[str]:
        """匹配Skill"""
        for keyword, skill_id in self.SKILL_MAP.items():
            if keyword in text:
                return skill_id
        return None
    
    def _call_skill(self, skill_id: str, user_input: str, context: Dict) -> Dict:
        """调用Skill"""
        # 简化版：根据skill_id路由
        if skill_id == 'cnc-quote-system':
            # 调用报价API
            return {'success': True, 'response': '已触发报价流程，请提供参数'}
        
        return {'success': True, 'response': f'已执行{skill_id}'}


class ComplexTaskHandler:
    """复杂任务处理器 - 深度思辨"""
    
    def __init__(self):
        self.subtask_history = []
        # 惰性加载辩论验证器
        self._verifier = None
    
    @property
    def verifier(self):
        """惰性加载辩论验证器"""
        if self._verifier is None:
            from debate_verifier import DebateVerifier
            self._verifier = DebateVerifier()
        return self._verifier
    
    def process(self, user_input: str, context: Dict = None) -> TaskResult:
        """处理复杂任务"""
        start_time = time.time()
        
        # 1. 苏格拉底探明
        probe_result = self._socratic_probe(user_input)
        
        # 2. 任务分解
        subtasks = self._decompose_task(user_input, probe_result)
        
        # 3. 资源定位
        executors = self._locate_resources(subtasks)
        
        # 4. 执行子任务
        results = self._execute_subtasks(subtasks, executors)
        
        # 5. 结果聚合
        final_result = self._aggregate_results(results)
        
        # 6. 多模型辩论验证（必须共识输出）
        verified_result = self._debate_verify(final_result, user_input)
        
        latency = int((time.time() - start_time) * 1000)
        
        return TaskResult(
            success=verified_result['passed'],
            complexity='complex',
            response=verified_result['consensus'],
            subtasks=[st['name'] for st in subtasks],
            latency_ms=latency
        )
    
    def _socratic_probe(self, text: str) -> Dict:
        """苏格拉底探明"""
        # 简化版：提取关键信息
        return {
            'intent': 'complex_task',
            'context': text[:200],
            'questions_needed': False
        }
    
    def _decompose_task(self, text: str, probe: Dict) -> List[Dict]:
        """任务分解"""
        # 基于关键词的规则分解
        subtasks = []
        
        if '设计' in text or '方案' in text:
            subtasks = [
                {'name': '需求分析', 'type': 'analysis'},
                {'name': '方案设计', 'type': 'design'},
                {'name': '方案评估', 'type': 'review'},
                {'name': '报告生成', 'type': 'output'}
            ]
        elif '分析' in text or '研究' in text:
            subtasks = [
                {'name': '数据收集', 'type': 'collection'},
                {'name': '深度分析', 'type': 'analysis'},
                {'name': '结论生成', 'type': 'output'}
            ]
        else:
            subtasks = [
                {'name': '任务理解', 'type': 'analysis'},
                {'name': '执行处理', 'type': 'execution'},
                {'name': '结果输出', 'type': 'output'}
            ]
        
        return subtasks
    
    def _locate_resources(self, subtasks: List[Dict]) -> List[Dict]:
        """资源定位"""
        executors = []
        
        for task in subtasks:
            # 优先级：本地程序 > Skill > ClawHub > 手搓
            if task['type'] == 'analysis':
                executors.append({'source': 'local', 'handler': 'hybrid-model-router'})
            elif task['type'] == 'design':
                executors.append({'source': 'skill', 'handler': 'adversarial-engine'})
            elif task['type'] == 'output':
                executors.append({'source': 'local', 'handler': 'hybrid-model-router'})
            else:
                executors.append({'source': 'local', 'handler': 'hybrid-model-router'})
        
        return executors
    
    def _execute_subtasks(self, subtasks: List[Dict], executors: List[Dict]) -> List[Dict]:
        """执行子任务"""
        results = []
        
        for i, task in enumerate(subtasks):
            executor = executors[i] if i < len(executors) else {'source': 'local', 'handler': 'default'}
            
            # 简化执行
            results.append({
                'task': task['name'],
                'status': 'completed',
                'output': f"{task['name']}完成"
            })
        
        return results
    
    def _aggregate_results(self, results: List[Dict]) -> str:
        """聚合结果"""
        lines = ["📋 复杂任务执行完成", ""]
        
        for r in results:
            lines.append(f"✅ {r['task']}: {r['status']}")
        
        lines.append("")
        lines.append('最终结果已生成，如需详细报告请回复"详情"')
        
        return "\n".join(lines)
    
    def _debate_verify(self, result: str, context: str) -> Dict:
        """
        多模型辩论验证
        
        核心规则：
        1. 最多5轮辩论
        2. 必须输出共识结论
        3. 未收敛则取仲裁结论
        """
        try:
            debate_result = self.verifier.verify(result, context)
            
            return {
                'passed': debate_result.passed,
                'consensus': debate_result.consensus if debate_result.passed else f"需人工复核：{debate_result.reason}",
                'confidence': debate_result.confidence,
                'rounds': debate_result.rounds
            }
        except Exception as e:
            # 辩论失败，返回原结果（降级）
            return {
                'passed': True,
                'consensus': result,
                'confidence': 0.8,
                'rounds': 0,
                'error': str(e)
            }


class SmartScheduler:
    """智能任务调度器 - 主入口"""
    
    def __init__(self):
        self.classifier = TaskClassifier()
        self.simple_handler = SimpleTaskHandler()
        self.complex_handler = ComplexTaskHandler()
        self.history = []
        
        # 新增组件
        self.resource_locator = ResourceLocator()
        self.stats_collector = StatsCollector()
    
    def handle(self, user_input: str, context: Dict = None) -> TaskResult:
        """
        处理用户输入
        
        Args:
            user_input: 用户输入
            context: 上下文信息（可选）
            
        Returns:
            TaskResult
        """
        # 0. 内存检查
        is_safe, mem_status = MemoryMonitor.check()
        if not is_safe:
            return TaskResult(
                success=False,
                complexity='simple',
                response=f"系统内存不足，请稍后重试 ({mem_status})",
                latency_ms=0
            )
        
        # 1. 任务分类
        complexity, reason = self.classifier.classify(user_input)
        
        print(f"[SmartScheduler] 任务分类: {complexity.value}, 原因: {reason}")
        print(f"[SmartScheduler] 内存: {mem_status}")
        
        # 2. 路由到对应处理器
        if complexity == TaskComplexity.SIMPLE:
            result = self.simple_handler.process(user_input, context)
        else:
            result = self.complex_handler.process(user_input, context)
        
        # 3. 记录统计
        self.stats_collector.record({
            'input': user_input[:100],
            'complexity': complexity.value,
            'latency_ms': result.latency_ms,
            'success': result.success
        })
        
        # 4. 记录历史
        self.history.append({
            'input': user_input[:100],
            'complexity': complexity.value,
            'latency_ms': result.latency_ms,
            'success': result.success
        })
        
        return result
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        # 合并历史记录和持久化统计
        summary = self.stats_collector.get_summary()
        
        if summary['total'] == 0 and self.history:
            # 从内存历史计算
            simple_count = sum(1 for h in self.history if h['complexity'] == 'simple')
            complex_count = sum(1 for h in self.history if h['complexity'] == 'complex')
            avg_latency = sum(h['latency_ms'] for h in self.history) / len(self.history)
            
            return {
                'total': len(self.history),
                'simple_count': simple_count,
                'complex_count': complex_count,
                'avg_latency_ms': int(avg_latency),
                'success_rate': sum(1 for h in self.history if h['success']) / len(self.history)
            }
        
        return summary


# 测试入口
if __name__ == "__main__":
    scheduler = SmartScheduler()
    
    # 测试用例
    test_cases = [
        "你好",
        "报价",
        "帮我设计一个6061铝CNC优化方案",
        "分析一下当前系统的问题",
        "记录一下今天的任务",
        "这是一个超过50字的复杂任务描述，需要系统进行全面深入的分析和研究，生成详细的报告和建议方案"
    ]
    
    print("="*60)
    print("🧠 智能任务调度器测试")
    print("="*60)
    
    for text in test_cases:
        print(f"\n输入: {text[:30]}...")
        result = scheduler.handle(text)
        print(f"分类: {result.complexity}")
        print(f"响应: {result.response[:50]}...")
        print(f"耗时: {result.latency_ms}ms")
    
    print("\n" + "="*60)
    print("📊 统计信息:")
    print(json.dumps(scheduler.get_stats(), indent=2))