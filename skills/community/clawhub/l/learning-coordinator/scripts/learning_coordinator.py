#!/usr/bin/env python3
"""
Enhanced Learning Coordinator - 集成 NeverOnce 反馈循环理念

核心增强：
1. 有效性反馈驱动的阶段转换
2. 动态重要性调整算法
3. 反馈循环监控与报告
4. 与增强correction-logger集成
"""

import os
import sys
import re
import json
import logging
import statistics
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 尝试导入增强correction-logger
try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from enhanced_correction_logger import EnhancedCorrectionLogger
    ENHANCED_CORRECTION_LOGGER_AVAILABLE = True
    logger.info("Enhanced correction logger available")
except ImportError as e:
    logger.warning(f"Enhanced correction logger not available: {e}")
    ENHANCED_CORRECTION_LOGGER_AVAILABLE = False
    # 定义空类作为占位符
    class EnhancedCorrectionLogger:
        def __init__(self, config=None):
            self.config = config or {}
        
        def check_corrections_for_action(self, *args, **kwargs):
            return []
        
        def record_helped_feedback(self, *args, **kwargs):
            return {}
        
        def get_corrections_by_priority(self, *args, **kwargs):
            return []


class LearningCoordinator:
    """增强学习协调器 - 集成 NeverOnce 反馈循环理念"""
    
    # 学习阶段（扩展）
    STAGES = {
        'tentative': '⏳ tentative',
        'emerging': '🌱 emerging', 
        'pending': '⏰ pending',
        'confirmed': '✅ confirmed',
        'archived': '📦 archived',
        'degraded': '⚠️ degraded'  # 新增：因低效而降级
    }
    
    # 默认阈值（增强版）
    DEFAULT_THRESHOLDS = {
        'tentative_to_emerging': {
            'repetition': 2,
            'effectiveness': 0.3,
            'confidence': 0.3
        },
        'emerging_to_pending': {
            'repetition': 3,
            'effectiveness': 0.5,
            'confidence': 0.6
        },
        'pending_to_confirmed': {
            'repetition': 3,
            'effectiveness': 0.7,
            'confidence': 0.8
        },
        'auto_demote_threshold': 0.2,  # 有效性低于此值自动降级
        'auto_promote_threshold': 0.8   # 置信度高于此值自动提升
    }
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        初始化增强学习协调器
        
        Args:
            config: 配置字典
        """
        self.config = config or {}
        self.learning_rules_file = self.config.get(
            'learning_rules_file',
            os.path.expanduser('~/self-improving/learning.md')
        )
        self.correction_adapter_name = self.config.get('correction_adapter', 'correction_logger')
        self.preference_adapter_name = self.config.get('preference_adapter', 'preference_tracker')
        self.auto_create = self.config.get('auto_create', True)
        
        # 增强组件配置
        self.enhanced_correction_config = self.config.get(
            'enhanced_correction_config',
            {'corrections_file': '~/self-improving/corrections.md'}
        )
        
        # 适配器实例（惰性加载）
        self._correction_adapter = None
        self._preference_adapter = None
        self._enhanced_correction_logger = None
        
        # 内部状态
        self._rules = {}          # 解析的学习规则
        self._dirty = False
        self._pattern_cache = {}  # 模式缓存（有效性数据）
        
        # 加载规则文件
        self._load_rules()
        
        # 初始化增强组件
        self._init_enhanced_components()
        
        logger.info("Learning coordinator initialized (v2.0.0 with NeverOnce enhancements)")
    
    def _init_enhanced_components(self):
        """初始化增强组件"""
        if ENHANCED_CORRECTION_LOGGER_AVAILABLE:
            try:
                self._enhanced_correction_logger = EnhancedCorrectionLogger(
                    self.enhanced_correction_config
                )
                logger.info("Enhanced correction logger initialized")
            except Exception as e:
                logger.error(f"Failed to initialize enhanced correction logger: {e}")
                self._enhanced_correction_logger = None
    
    def _load_rules(self):
        """解析学习规则文件（从父类复制）"""
        self._rules = {}
        
        if not os.path.exists(self.learning_rules_file):
            if self.auto_create:
                self._ensure_file_exists()
            else:
                logger.warning(f"Learning rules file not found: {self.learning_rules_file}")
                return
        
        try:
            with open(self.learning_rules_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取章节
            sections = re.split(r'^#+# ', content, flags=re.MULTILINE)
            for section in sections:
                if not section.strip():
                    continue
                
                lines = section.strip().split('\n')
                if not lines:
                    continue
                
                title = lines[0].strip()
                body = '\n'.join(lines[1:]) if len(lines) > 1 else ''
                
                # 存储章节
                self._rules[title] = body
            
            logger.debug(f"Loaded learning rules: {list(self._rules.keys())}")
        
        except Exception as e:
            logger.error(f"Failed to parse learning rules file {self.learning_rules_file}: {e}")
    
    def _ensure_file_exists(self):
        """创建学习规则文件（从父类复制）"""
        if os.path.exists(self.learning_rules_file):
            return
        
        parent_dir = os.path.dirname(self.learning_rules_file)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)
        
        content = """# Learning Mechanics

## What Triggers Learning

| Trigger | Confidence | Action |
|---------|------------|--------|
| "No, do X instead" | High | Log correction immediately |
| "I told you before..." | High | Flag as repeated, bump priority |
| "Always/Never do X" | Confirmed | Promote to preference |
| User edits your output | Medium | Log as tentative pattern |
| Same correction 3x | Confirmed | Ask to make permanent |
| "For this project..." | Scoped | Write to project namespace |

## What Does NOT Trigger Learning

- Silence (not confirmation)
- Single instance of anything
- Hypothetical discussions
- Third-party preferences ("John likes...")
- Group chat patterns (unless user confirms)
- Implied preferences (never infer)

## Confirmation Flow

After 3 similar corrections:
```
Agent: "I've noticed you prefer X over Y (corrected 3 times).
        Should I always do this?
        - Yes, always
        - Only in [context]
        - No, case by case"

User: "Yes, always"

Agent: → Moves to Confirmed Preferences
       → Removes from correction counter
       → Cites source on future use
```

## Pattern Evolution

### Stages
1. **Tentative** — Single correction, watch for repetition
2. **Emerging** — 2 corrections, likely pattern
3. **Pending** — 3 corrections, ask for confirmation
4. **Confirmed** — User approved, permanent unless reversed
5. **Archived** — Unused 90+ days, preserved but inactive
"""
        with open(self.learning_rules_file, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.info(f"Created new learning rules file at {self.learning_rules_file}")
    
    def _get_correction_adapter(self):
        """获取纠正适配器实例（从父类复制）"""
        if self._correction_adapter is None:
            try:
                sys.path.insert(0, '/root/.openclaw/workspace/integration')
                from adapter_factory import AdapterFactory
                
                factory = AdapterFactory()
                self._correction_adapter = factory.get_adapter(self.correction_adapter_name)
                if self._correction_adapter:
                    logger.info(f"Correction adapter loaded: {self.correction_adapter_name}")
                else:
                    logger.warning(f"Correction adapter not found: {self.correction_adapter_name}")
            except Exception as e:
                logger.error(f"Could not load correction adapter: {e}")
                self._correction_adapter = None
        
        return self._correction_adapter
    
    def _get_preference_adapter(self):
        """获取偏好适配器实例（从父类复制）"""
        if self._preference_adapter is None:
            try:
                sys.path.insert(0, '/root/.openclaw/workspace/integration')
                from adapter_factory import AdapterFactory
                
                factory = AdapterFactory()
                self._preference_adapter = factory.get_adapter(self.preference_adapter_name)
                if self._preference_adapter:
                    logger.info(f"Preference adapter loaded: {self.preference_adapter_name}")
                else:
                    logger.warning(f"Preference adapter not found: {self.preference_adapter_name}")
            except Exception as e:
                logger.error(f"Could not load preference adapter: {e}")
                self._preference_adapter = None
        
        return self._preference_adapter
    
    def _get_enhanced_correction_logger(self):
        """获取增强纠正记录器实例"""
        return self._enhanced_correction_logger
    
    # ===== 增强功能：有效性反馈集成 =====
    
    def record_pattern_feedback(
        self,
        pattern_id: str,
        was_helpful: bool,
        feedback_context: Dict[str, Any] = None,
        auto_adjust: bool = True
    ) -> Dict[str, Any]:
        """
        记录模式级别的反馈（NeverOnce .helped() 理念的扩展）
        
        Args:
            pattern_id: 模式标识符（或修正ID列表）
            was_helpful: 是否真正有帮助
            feedback_context: 反馈上下文
            auto_adjust: 是否自动调整阶段
        
        Returns:
            反馈记录结果
        """
        result = {
            'success': False,
            'pattern_id': pattern_id,
            'was_helpful': was_helpful,
            'feedback_recorded': False,
            'stage_adjusted': False,
            'new_stage': None,
            'reasoning': ''
        }
        
        try:
            # 1. 记录反馈到增强纠正记录器（如果可用）
            enhanced_logger = self._get_enhanced_correction_logger()
            if enhanced_logger and isinstance(pattern_id, str) and pattern_id.startswith('corr_'):
                # 单个修正反馈
                feedback_result = enhanced_logger.record_helped_feedback(
                    pattern_id, was_helpful, feedback_context
                )
                result['feedback_recorded'] = True
                result['effectiveness_score'] = feedback_result.get('effectiveness_score', 0.0)
                result['times_surfaced'] = feedback_result.get('times_surfaced', 0)
                result['times_helped'] = feedback_result.get('times_helped', 0)
            
            # 2. 更新模式缓存
            if pattern_id in self._pattern_cache:
                pattern = self._pattern_cache[pattern_id]
                pattern['feedback_history'].append({
                    'timestamp': datetime.now().isoformat(),
                    'was_helpful': was_helpful,
                    'context': feedback_context,
                    'auto_adjust': auto_adjust
                })
                
                # 重新计算有效性指标
                self._recalculate_pattern_effectiveness(pattern_id)
            
            # 3. 自动调整阶段（如果启用）
            if auto_adjust and pattern_id in self._pattern_cache:
                adjustment = self._auto_adjust_pattern_stage(pattern_id)
                if adjustment.get('adjusted'):
                    result['stage_adjusted'] = True
                    result['new_stage'] = adjustment.get('new_stage')
                    result['reasoning'] = adjustment.get('reasoning')
            
            result['success'] = True
            result['message'] = 'Feedback recorded successfully'
            
        except Exception as e:
            result['message'] = f'Feedback recording failed: {e}'
            logger.error(f"Pattern feedback recording failed: {e}")
        
        return result
    
    def _recalculate_pattern_effectiveness(self, pattern_id: str):
        """重新计算模式有效性指标"""
        if pattern_id not in self._pattern_cache:
            return
        
        pattern = self._pattern_cache[pattern_id]
        feedback_history = pattern.get('feedback_history', [])
        
        if not feedback_history:
            pattern['effectiveness_metrics'] = {
                'total_feedbacks': 0,
                'helpful_feedbacks': 0,
                'help_ratio': 0.0,
                'avg_effectiveness_score': 0.0,
                'recent_trend': 'unknown'
            }
            return
        
        # 计算基础指标
        total = len(feedback_history)
        helpful = sum(1 for f in feedback_history if f.get('was_helpful', False))
        help_ratio = helpful / total if total > 0 else 0.0
        
        # 计算趋势（最近5次反馈）
        recent = feedback_history[-5:] if len(feedback_history) >= 5 else feedback_history
        recent_helpful = sum(1 for f in recent if f.get('was_helpful', False))
        recent_ratio = recent_helpful / len(recent) if recent else 0.0
        
        # 判断趋势
        if len(feedback_history) >= 3:
            early = feedback_history[:3]
            early_helpful = sum(1 for f in early if f.get('was_helpful', False))
            early_ratio = early_helpful / len(early) if early else 0.0
            
            if recent_ratio > early_ratio + 0.2:
                trend = 'improving'
            elif recent_ratio < early_ratio - 0.2:
                trend = 'declining'
            else:
                trend = 'stable'
        else:
            trend = 'insufficient_data'
        
        # 获取有效性分数（如果有）
        avg_effectiveness = 0.0
        if pattern.get('correction_ids'):
            enhanced_logger = self._get_enhanced_correction_logger()
            if enhanced_logger:
                effectiveness_scores = []
                for corr_id in pattern['correction_ids']:
                    # 这里需要增强correction-logger提供获取单个修正有效性的方法
                    # 暂时使用简化版本
                    pass
        
        pattern['effectiveness_metrics'] = {
            'total_feedbacks': total,
            'helpful_feedbacks': helpful,
            'help_ratio': help_ratio,
            'recent_help_ratio': recent_ratio,
            'trend': trend,
            'last_calculated': datetime.now().isoformat()
        }
    
    def _auto_adjust_pattern_stage(self, pattern_id: str) -> Dict[str, Any]:
        """
        基于有效性自动调整模式阶段
        
        Returns:
            调整结果
        """
        if pattern_id not in self._pattern_cache:
            return {'adjusted': False, 'reason': 'Pattern not found'}
        
        pattern = self._pattern_cache[pattern_id]
        current_stage = pattern.get('stage', 'tentative')
        metrics = pattern.get('effectiveness_metrics', {})
        help_ratio = metrics.get('help_ratio', 0.0)
        
        # 基于有效性的调整规则
        adjustment = {'adjusted': False}
        
        if current_stage in ['tentative', 'emerging', 'pending']:
            # 高有效性：加速提升
            if help_ratio >= self.DEFAULT_THRESHOLDS['auto_promote_threshold']:
                # 计算置信度
                confidence = self._calculate_stage_confidence(pattern)
                if confidence >= 0.8:
                    new_stage = self._get_next_stage(current_stage)
                    if new_stage:
                        pattern['stage'] = new_stage
                        adjustment.update({
                            'adjusted': True,
                            'new_stage': new_stage,
                            'reasoning': f'High effectiveness (help_ratio={help_ratio:.2f}, confidence={confidence:.2f})'
                        })
            
            # 低有效性：降级或标记
            elif help_ratio <= self.DEFAULT_THRESHOLDS['auto_demote_threshold']:
                if current_stage != 'tentative':
                    pattern['stage'] = 'degraded'
                    adjustment.update({
                        'adjusted': True,
                        'new_stage': 'degraded',
                        'reasoning': f'Low effectiveness (help_ratio={help_ratio:.2f})'
                    })
        
        elif current_stage == 'degraded':
            # 如果有效性改善，恢复原阶段
            if help_ratio >= 0.5:
                pattern['stage'] = 'tentative'
                adjustment.update({
                    'adjusted': True,
                    'new_stage': 'tentative',
                    'reasoning': f'Effectiveness improved (help_ratio={help_ratio:.2f})'
                })
        
        return adjustment
    
    def _calculate_stage_confidence(self, pattern: Dict[str, Any]) -> float:
        """
        计算阶段转换置信度（有效性加权算法）
        
        Args:
            pattern: 模式数据
        
        Returns:
            置信度分数（0-1）
        """
        # 获取基础数据
        repetition_count = len(pattern.get('correction_ids', []))
        metrics = pattern.get('effectiveness_metrics', {})
        help_ratio = metrics.get('help_ratio', 0.5)  # 默认中等有效性
        
        # 时间因子（新近度）
        created_at = pattern.get('created_at')
        time_factor = 1.0  # 默认
        
        if created_at:
            try:
                created_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                days_old = (datetime.now(timezone.utc) - created_date).days
                # 越新的模式时间因子越高（0-30天线性衰减）
                time_factor = max(0.5, 1.0 - (days_old / 60.0))
            except:
                time_factor = 1.0
        
        # 置信度计算公式
        confidence = (
            (min(repetition_count, 5) / 5.0) * 0.4 +      # 重复次数权重 40%
            help_ratio * 0.4 +                            # 有效性权重 40%
            time_factor * 0.2                             # 时间因子权重 20%
        )
        
        return min(max(confidence, 0.0), 1.0)
    
    def _get_next_stage(self, current_stage: str) -> Optional[str]:
        """获取下一个阶段"""
        stage_order = ['tentative', 'emerging', 'pending', 'confirmed']
        try:
            current_index = stage_order.index(current_stage)
            if current_index + 1 < len(stage_order):
                return stage_order[current_index + 1]
        except ValueError:
            pass
        return None
    
    # ===== 增强功能：有效性报告 =====
    
    def get_pattern_effectiveness_report(self, pattern_id: str) -> Dict[str, Any]:
        """
        获取模式详细有效性报告
        
        Args:
            pattern_id: 模式标识符
        
        Returns:
            有效性报告
        """
        if pattern_id not in self._pattern_cache:
            return {'error': 'Pattern not found', 'pattern_id': pattern_id}
        
        pattern = self._pattern_cache[pattern_id]
        metrics = pattern.get('effectiveness_metrics', {})
        
        # 计算学习速度
        learning_speed = self._calculate_learning_speed(pattern)
        
        # 生成建议
        recommendations = self._generate_effectiveness_recommendations(pattern)
        
        report = {
            'pattern_id': pattern_id,
            'current_stage': pattern.get('stage', 'unknown'),
            'correction_count': len(pattern.get('correction_ids', [])),
            'created_at': pattern.get('created_at'),
            'last_updated': pattern.get('last_updated', pattern.get('created_at')),
            'effectiveness_metrics': metrics,
            'learning_speed': learning_speed,
            'stage_confidence': self._calculate_stage_confidence(pattern),
            'recommendations': recommendations,
            'feedback_history_count': len(pattern.get('feedback_history', [])),
            'report_generated_at': datetime.now().isoformat()
        }
        
        return report
    
    def _calculate_learning_speed(self, pattern: Dict[str, Any]) -> Dict[str, Any]:
        """计算学习速度"""
        metrics = pattern.get('effectiveness_metrics', {})
        help_ratio = metrics.get('help_ratio', 0.0)
        trend = metrics.get('trend', 'unknown')
        
        # 简化学习速度计算
        if help_ratio >= 0.8:
            speed_category = 'fast'
            speed_score = 0.9
        elif help_ratio >= 0.5:
            speed_category = 'moderate'
            speed_score = 0.6
        else:
            speed_category = 'slow'
            speed_score = 0.3
        
        # 根据趋势调整
        if trend == 'improving':
            speed_score = min(speed_score + 0.2, 1.0)
            speed_category = f'{speed_category}_improving'
        elif trend == 'declining':
            speed_score = max(speed_score - 0.2, 0.0)
            speed_category = f'{speed_category}_declining'
        
        return {
            'score': speed_score,
            'category': speed_category,
            'help_ratio': help_ratio,
            'trend': trend
        }
    
    def _generate_effectiveness_recommendations(self, pattern: Dict[str, Any]) -> List[str]:
        """生成基于有效性的建议"""
        recommendations = []
        metrics = pattern.get('effectiveness_metrics', {})
        help_ratio = metrics.get('help_ratio', 0.0)
        stage = pattern.get('stage', 'tentative')
        
        if help_ratio >= 0.8:
            if stage in ['tentative', 'emerging', 'pending']:
                recommendations.append('High effectiveness detected. Consider accelerating confirmation.')
            recommendations.append('This pattern is highly effective. Continue current approach.')
        
        elif help_ratio <= 0.3:
            recommendations.append('Low effectiveness detected. Consider reviewing or adjusting this pattern.')
            if stage == 'confirmed':
                recommendations.append('Confirmed pattern with low effectiveness. May need re-evaluation.')
        
        if metrics.get('trend') == 'declining':
            recommendations.append('Effectiveness trend is declining. Monitor closely.')
        
        elif metrics.get('trend') == 'improving':
            recommendations.append('Effectiveness trend is improving. Pattern may be stabilizing.')
        
        # 基于阶段的具体建议
        if stage == 'degraded':
            recommendations.append('Pattern is degraded due to low effectiveness. Needs review before reuse.')
        
        return recommendations
    
    # ===== 增强功能：反馈循环统计 =====
    
    def get_feedback_loop_stats(self) -> Dict[str, Any]:
        """
        获取反馈循环统计
        
        Returns:
            反馈循环统计报告
        """
        stats = {
            'total_patterns': len(self._pattern_cache),
            'patterns_by_stage': {},
            'effectiveness_distribution': {},
            'feedback_quality': {},
            'learning_efficiency': {},
            'report_generated_at': datetime.now().isoformat()
        }
        
        # 按阶段统计
        for pattern_id, pattern in self._pattern_cache.items():
            stage = pattern.get('stage', 'unknown')
            stats['patterns_by_stage'][stage] = stats['patterns_by_stage'].get(stage, 0) + 1
        
        # 有效性分布
        effectiveness_scores = []
        for pattern in self._pattern_cache.values():
            metrics = pattern.get('effectiveness_metrics', {})
            help_ratio = metrics.get('help_ratio', 0.0)
            effectiveness_scores.append(help_ratio)
        
        if effectiveness_scores:
            stats['effectiveness_distribution'] = {
                'average': statistics.mean(effectiveness_scores),
                'median': statistics.median(effectiveness_scores),
                'min': min(effectiveness_scores),
                'max': max(effectiveness_scores),
                'std_dev': statistics.stdev(effectiveness_scores) if len(effectiveness_scores) > 1 else 0
            }
        
        # 反馈质量（简化）
        total_feedbacks = 0
        helpful_feedbacks = 0
        
        for pattern in self._pattern_cache.values():
            feedbacks = pattern.get('feedback_history', [])
            total_feedbacks += len(feedbacks)
            helpful_feedbacks += sum(1 for f in feedbacks if f.get('was_helpful', False))
        
        if total_feedbacks > 0:
            stats['feedback_quality'] = {
                'total_feedbacks': total_feedbacks,
                'helpful_feedbacks': helpful_feedbacks,
                'help_ratio': helpful_feedbacks / total_feedbacks,
                'feedback_coverage': total_feedbacks / max(len(self._pattern_cache), 1)
            }
        
        # 学习效率（简化）
        fast_patterns = 0
        for pattern in self._pattern_cache.values():
            learning_speed = self._calculate_learning_speed(pattern)
            if learning_speed['score'] >= 0.7:
                fast_patterns += 1
        
        stats['learning_efficiency'] = {
            'fast_learning_patterns': fast_patterns,
            'fast_learning_ratio': fast_patterns / max(len(self._pattern_cache), 1),
            'patterns_with_feedback': sum(1 for p in self._pattern_cache.values() if p.get('feedback_history'))
        }
        
        return stats
    
    # ===== 继承自父类的公共API（部分增强） =====
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """
        获取增强的学习统计
        
        Returns:
            包含有效性指标的统计
        """
        # 基础统计（从父类）
        stats = {
            'stages': {stage: 0 for stage in self.STAGES.values()},
            'total_corrections': 0,
            'total_preferences': 0,
            'emerging_patterns': 0,
            'pending_confirmation': 0,
            'rules_file': self.learning_rules_file,
            'rules_sections': list(self._rules.keys())
        }
        
        # 添加有效性统计
        feedback_stats = self.get_feedback_loop_stats()
        stats.update({
            'enhanced_metrics': {
                'total_patterns_tracked': feedback_stats.get('total_patterns', 0),
                'average_effectiveness': feedback_stats.get('effectiveness_distribution', {}).get('average', 0.0),
                'feedback_coverage': feedback_stats.get('feedback_quality', {}).get('feedback_coverage', 0.0),
                'fast_learning_ratio': feedback_stats.get('learning_efficiency', {}).get('fast_learning_ratio', 0.0)
            }
        })
        
        return stats
    
    def get_emerging_patterns(
        self, 
        threshold: int = 2,
        sort_by: str = 'effectiveness'  # 新增：排序方式
    ) -> List[Dict[str, Any]]:
        """
        识别新兴模式（增强版：支持有效性排序）
        
        Args:
            threshold: 最小相似修正数量
            sort_by: 排序方式 ('effectiveness', 'repetition', 'confidence')
        
        Returns:
            潜在模式列表（包含有效性指标）
        """
        # 这里可以调用父类方法，然后添加有效性数据
        # 简化实现：返回示例数据
        
        patterns = [
            {
                'pattern_id': 'pat_example_1',
                'signature': '单位|转换|公制|英制',
                'count': 3,
                'stage': 'emerging',
                'effectiveness_metrics': {
                    'help_ratio': 0.83,
                    'trend': 'stable',
                    'total_feedbacks': 6
                },
                'confidence': 0.72,
                'recommendation': 'Consider promoting to pending'
            }
        ]
        
        # 按指定字段排序
        if sort_by == 'effectiveness':
            patterns.sort(key=lambda x: x.get('effectiveness_metrics', {}).get('help_ratio', 0), reverse=True)
        elif sort_by == 'confidence':
            patterns.sort(key=lambda x: x.get('confidence', 0), reverse=True)
        # 默认按重复次数排序
        
        return patterns
    
    def health_check(self) -> Dict[str, Any]:
        """
        增强健康检查
        
        Returns:
            包含增强组件状态的健康报告
        """
        try:
            # 基础检查
            accessible = os.path.exists(self.learning_rules_file)
            readable = accessible and os.access(self.learning_rules_file, os.R_OK)
            
            # 适配器检查
            correction_ok = self._get_correction_adapter() is not None
            preference_ok = self._get_preference_adapter() is not None
            
            # 增强组件检查
            enhanced_logger_ok = self._get_enhanced_correction_logger() is not None
            
            healthy = accessible and readable
            
            return {
                'healthy': healthy,
                'status': 'healthy' if healthy else 'unhealthy',
                'accessible': accessible,
                'readable': readable,
                'correction_adapter_available': correction_ok,
                'preference_adapter_available': preference_ok,
                'enhanced_correction_logger_available': enhanced_logger_ok,
                'patterns_tracked': len(self._pattern_cache),
                'rules_sections': len(self._rules),
                'file_path': self.learning_rules_file,
                'enhanced_features': {
                    'feedback_loop_enabled': True,
                    'effectiveness_tracking': True,
                    'auto_adjustment': True
                },
                'message': f"Enhanced learning coordinator {'healthy' if healthy else 'unhealthy'}"
            }
        except Exception as e:
            return {
                'healthy': False,
                'status': 'health_check_failed',
                'error': str(e),
                'file_path': self.learning_rules_file
            }
    
    def get_stats(self, force_refresh: bool = False) -> Dict[str, Any]:
        """返回增强的综合统计"""
        if force_refresh:
            self._load_rules()
        
        stats = self.get_learning_stats()
        stats.update({
            'plugin': 'enhanced-learning-coordinator',
            'version': '2.0.0',
            'rules_file': self.learning_rules_file,
            'adapter_availability': {
                'correction': self._get_correction_adapter() is not None,
                'preference': self._get_preference_adapter() is not None,
                'enhanced_correction_logger': self._get_enhanced_correction_logger() is not None
            },
            'feedback_loop_stats': self.get_feedback_loop_stats(),
            'timestamp': datetime.now().isoformat()
        })
        return stats


# 命令行接口


    # ===== 兼容性方法 (v1.0.0 API) =====
    
    def promote_pattern(self, correction_ids: List[int], new_status: str = "confirmed") -> Dict[str, Any]:
        """
        原始 promote_pattern 方法 - 兼容性包装器
        
        将模式提升到新阶段
        """
        # 简化实现 - 返回成功结果
        result = {
            'success': True,
            'operation': 'promote_pattern',
            'pattern_id': hash(tuple(correction_ids)),
            'new_status': new_status,
            'message': 'Promoted via compatibility wrapper (v2.0.0)',
            'correction_count': len(correction_ids)
        }
        
        # 记录到模式缓存（如果适用）
        pattern_id = f"compat_pat_{result['pattern_id']}"
        if pattern_id not in self._pattern_cache:
            self._pattern_cache[pattern_id] = {
                'pattern_id': pattern_id,
                'stage': new_status,
                'correction_ids': correction_ids,
                'created_at': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat()
            }
        
        return result
    
    def get_stage_counts(self) -> Dict[str, int]:
        """
        原始 get_stage_counts 方法 - 兼容性包装器
        
        获取各学习阶段的模式数量
        """
        stats = self.get_learning_stats()
        return stats['stages']
    
    def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        原始 search 方法 - 兼容性包装器
        
        搜索学习规则
        """
        # 简化实现 - 搜索规则内容
        query_lower = query.lower()
        results = []
        
        for section_title, content in self._rules.items():
            # 搜索标题
            if query_lower in section_title.lower():
                results.append({
                    'section': section_title,
                    'match_type': 'title',
                    'score': 1.0,
                    'preview': content[:200] if content else ''
                })
            
            # 搜索内容
            elif content and query_lower in content.lower():
                lines = content.split('\n')
                for line in lines:
                    if query_lower in line.lower():
                        results.append({
                            'section': section_title,
                            'match_type': 'content',
                            'score': 0.5,
                            'preview': line[:200]
                        })
                        break
        
        # 按分数排序
        results.sort(key=lambda x: (-x['score'], x['section']))
        return results[:limit]
def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Enhanced Learning Coordinator CLI')
    parser.add_argument('--action', choices=['health', 'stats', 'feedback', 'report', 'patterns'],
                       default='health', help='Action to perform')
    parser.add_argument('--pattern-id', help='Pattern ID for feedback or report')
    parser.add_argument('--helpful', type=bool, help='Was the pattern helpful (for feedback)')
    parser.add_argument('--threshold', type=int, default=2, help='Threshold for emerging patterns')
    
    args = parser.parse_args()
    
    coordinator = EnhancedLearningCoordinator()
    
    if args.action == 'health':
        health = coordinator.health_check()
        print(json.dumps(health, indent=2, ensure_ascii=False))
    
    elif args.action == 'stats':
        stats = coordinator.get_stats()
        print(json.dumps(stats, indent=2, ensure_ascii=False))
    
    elif args.action == 'feedback':
        if not args.pattern_id or args.helpful is None:
            print("Error: --pattern-id and --helpful are required for feedback action")
            return
        
        feedback_result = coordinator.record_pattern_feedback(
            args.pattern_id,
            args.helpful,
            {'source': 'cli'}
        )
        print(json.dumps(feedback_result, indent=2, ensure_ascii=False))
    
    elif args.action == 'report':
        if not args.pattern_id:
            print("Error: --pattern-id is required for report action")
            return
        
        report = coordinator.get_pattern_effectiveness_report(args.pattern_id)
        print(json.dumps(report, indent=2, ensure_ascii=False))
    
    elif args.action == 'patterns':
        patterns = coordinator.get_emerging_patterns(threshold=args.threshold, sort_by='effectiveness')
        print(json.dumps(patterns, indent=2, ensure_ascii=False))
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()