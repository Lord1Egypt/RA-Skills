"""
时长计算器 - 智能计算分镜建议时长
基于台词、运镜类型自动计算合理的分镜时长
"""

from typing import Dict, List, Any, Tuple


class DurationCalculator:
    """智能时长计算器"""
    
    def __init__(self, config: dict):
        """
        初始化时长计算器
        
        Args:
            config: 平台配置字典，包含 duration_policy 和 calculation_rules
        """
        self.config = config
        self.policy = config.get('duration_policy', config)  # 兼容两种配置结构
        self.rules = self.policy.get('calculation_rules', {
            'speech_rate': 0.25,
            'motion_base': {
                'static': 2,
                'push_pull': 3,
                'pan_tilt': 4,
                'complex': 6,
                'drone': 8
            },
            'buffer_seconds': 1,
            'min_motion_time': 2
        })
    
    def calculate_speech_time(self, line: str) -> float:
        """
        计算台词所需时长
        
        Args:
            line: 台词内容
            
        Returns:
            建议时长（秒）
        """
        if not line or not isinstance(line, str):
            return 0
        
        char_count = len(line.strip())
        speech_rate = self.rules.get('speech_rate', 0.25)
        
        return char_count * speech_rate
    
    def calculate_motion_time(self, movement: str) -> float:
        """
        根据运镜类型计算所需时长
        
        Args:
            movement: 运镜描述
            
        Returns:
            建议时长（秒）
        """
        if not movement or not isinstance(movement, str):
            return self.rules.get('motion_base', {}).get('static', 2)
        
        movement = movement.lower()
        motion_base = self.rules.get('motion_base', {})
        
        # 运镜类型匹配规则
        movement_patterns = {
            'static': ['固定', '定', '静止', 'static'],
            'push_pull': ['推', '拉', '推近', '推远', 'zoom'],
            'pan_tilt': ['摇', '移', '跟随', '跟随', 'pan', 'tilt'],
            'complex': ['环绕', '升降', '复杂', '复杂运镜', 'orbit', 'crane'],
            'drone': ['航拍', '俯视', '无人机', 'drone', 'aerial']
        }
        
        # 匹配运镜类型
        for motion_type, keywords in movement_patterns.items():
            for keyword in keywords:
                if keyword in movement:
                    return motion_base.get(motion_type, 3)
        
        # 默认使用固定镜头时长
        return motion_base.get('static', 2)
    
    def calculate_scene_duration(self, scene: dict) -> dict:
        """
        计算单个分镜的建议时长
        
        Args:
            scene: 分镜数据字典，包含 line, movement_desc, time 等字段
            
        Returns:
            计算结果字典
        """
        # 提取字段（支持多种字段名）
        line = scene.get('line', scene.get('台词', scene.get('narration', '')))
        movement = scene.get('movement_desc', scene.get('运镜', scene.get('movement', '')))
        time_str = scene.get('time', scene.get('时间段', ''))
        
        # 计算各项时长
        speech_time = self.calculate_speech_time(line)
        motion_time = self.calculate_motion_time(movement)
        
        # 基础时长 = max(台词时长, 运镜时长) + 缓冲
        buffer_seconds = self.rules.get('buffer_seconds', 1)
        base_duration = max(speech_time, motion_time) + buffer_seconds
        
        # 检查是否在平台限制范围内
        segment_limits = self.policy.get('segment_duration', {})
        min_duration = segment_limits.get('min', 3)
        max_duration = segment_limits.get('max', 12)
        
        # 最终建议时长
        recommended = max(min_duration, min(max_duration, base_duration))
        
        # 解析当前标注的时长
        labeled_duration = self._parse_labeled_duration(time_str)
        
        # 检查是否匹配
        match = self._check_duration_match(labeled_duration, recommended)
        
        return {
            'speech_time': round(speech_time, 1),
            'motion_time': round(motion_time, 1),
            'buffer': buffer_seconds,
            'recommended': round(recommended, 1),
            'labeled': labeled_duration,
            'match': match,
            'suggestion': self._generate_suggestion(labeled_duration, recommended, match)
        }
    
    def _parse_labeled_duration(self, time_str: str) -> float:
        """
        解析当前标注的时长
        
        Args:
            time_str: 时间段字符串，如 "0-5s", "5-10s"
            
        Returns:
            时长（秒）
        """
        if not time_str or not isinstance(time_str, str):
            return 0
        
        # 提取数字范围，如 "0-5s" -> [0, 5]
        import re
        numbers = re.findall(r'(\d+)', time_str)
        
        if len(numbers) >= 2:
            try:
                start = int(numbers[0])
                end = int(numbers[1])
                return end - start
            except (ValueError, IndexError):
                return 0
        
        return 0
    
    def _check_duration_match(self, labeled: float, recommended: float) -> bool:
        """
        检查标注时长是否与建议时长匹配
        
        规则：
        - 建议时长 ≥ 标注时长的60%
        - 建议时长可以更长（允许慢节奏）
        
        Args:
            labeled: 标注时长
            recommended: 建议时长
            
        Returns:
            是否匹配
        """
        if labeled == 0:
            return True  # 无标注时视为匹配
        
        return recommended >= labeled * 0.6
    
    def _generate_suggestion(self, labeled: float, recommended: float, match: bool) -> str:
        """生成调整建议"""
        if match:
            return "✓ 时长匹配"
        
        if labeled == 0:
            return f"建议设置为 {recommended}s"
        
        if recommended < labeled:
            return f"建议缩短至 {recommended}s 或补充内容以支撑 {labeled}s"
        
        return f"当前标注 {labeled}s，建议时长 {recommended}s"
    
    def optimize_script(self, scenes: List[dict], target_min: int = None, target_max: int = None) -> dict:
        """
        优化脚本时长 - 默认自动调整
        
        Args:
            scenes: 分镜列表
            target_min: 目标总时长最小值（可选）
            target_max: 目标总时长最大值（可选）
            
        Returns:
            优化结果字典
        """
        # 获取目标时长范围
        if target_min is None:
            target_min = self.policy.get('target_duration', {}).get('min', 120)
        if target_max is None:
            target_max = self.policy.get('target_duration', {}).get('max', 180)
        
        optimized_scenes = []
        current_time = 0
        total_labeled = 0
        
        for scene in scenes:
            calc = self.calculate_scene_duration(scene)
            
            # 自动调整：使用建议时长作为最终时间段
            if self.policy.get('auto_adjust', True):
                start_time = current_time
                end_time = current_time + int(calc['recommended'])
                
                # 更新时间段
                scene['time'] = f"{start_time}-{end_time}s"
                current_time = end_time
                
                # 保留计算详情到备注
                scene['_duration_calc'] = calc
            else:
                # 手动模式：仅添加计算结果
                scene['_duration_calc'] = calc
                current_time += calc['labeled'] if calc['labeled'] > 0 else calc['recommended']
            
            total_labeled += calc['labeled'] if calc['labeled'] > 0 else calc['recommended']
            optimized_scenes.append(scene)
        
        total_duration = current_time
        
        # 验证总时长
        total_match = target_min <= total_duration <= target_max
        
        # 生成建议
        suggestions = []
        if not total_match:
            if total_duration < target_min:
                suggestions.append(f"总时长 {total_duration}s 不足，建议增加分镜或延长单镜")
            elif total_duration > target_max:
                suggestions.append(f"总时长 {total_duration}s 超出，建议精简内容")
        
        return {
            'scenes': optimized_scenes,
            'total_duration': total_duration,
            'total_labeled': total_labeled,
            'target_range': f"{target_min}-{target_max}s",
            'match': total_match,
            'suggestions': suggestions
        }
    
    def get_duration_report(self, scenes: List[dict]) -> str:
        """
        生成时长计算报告
        
        Args:
            scenes: 分镜列表
            
        Returns:
            Markdown 格式报告
        """
        lines = [
            "## 时长计算报告",
            "",
            "| 分镜 | 台词(秒) | 运镜(秒) | 缓冲(秒) | 建议时长 | 标注时长 | 匹配 |",
            "|:---:|:---:|:---:|:---:|:---:|:---:|:---:|"
        ]
        
        total_recommended = 0
        total_labeled = 0
        all_match = True
        
        for i, scene in enumerate(scenes, 1):
            calc = self.calculate_scene_duration(scene)
            total_recommended += calc['recommended']
            total_labeled += calc['labeled'] if calc['labeled'] > 0 else calc['recommended']
            if not calc['match']:
                all_match = False
            
            lines.append(
                f"| {i} | {calc['speech_time']:.1f} | {calc['motion_time']:.1f} | {calc['buffer']} | "
                f"{calc['recommended']:.1f}s | {calc['labeled']:.1f}s | {'✓' if calc['match'] else '✗'} |"
            )
        
        lines.extend([
            "",
            f"**总计**: 建议 {total_recommended:.1f}s | 标注 {total_labeled:.1f}s | 整体 {'✓ 匹配' if all_match else '✗ 不匹配'}"
        ])
        
        return "\n".join(lines)


# 测试代码
if __name__ == "__main__":
    # 示例配置
    config = {
        'target_duration': {'min': 120, 'max': 180},
        'segment_duration': {'min': 6, 'max': 15},
        'auto_adjust': True,
        'calculation_rules': {
            'speech_rate': 0.25,
            'motion_base': {
                'static': 2,
                'push_pull': 3,
                'pan_tilt': 4,
                'complex': 6,
                'drone': 8
            },
            'buffer_seconds': 1
        }
    }
    
    calculator = DurationCalculator(config)
    
    # 示例分镜
    scenes = [
        {
            'line': '欢迎来到嘉泰苑，这里是太平枇杷第一镇。',
            'movement_desc': '固定镜头',
            'time': '0-5s'
        },
        {
            'line': '看这一树金黄的枇杷，又大又甜，每一颗都是阳光的味道。',
            'movement_desc': '缓慢推近特写',
            'time': '5-12s'
        }
    ]
    
    print(calculator.get_duration_report(scenes))
    print()
    print("优化结果:", calculator.optimize_script(scenes))
