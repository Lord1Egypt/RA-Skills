"""
格式检查器 - 验证脚本内容和Excel格式
提供9维度合理性检查和格式修复功能
"""

import re
from typing import Dict, List, Any, Tuple

# 尝试相对导入
try:
    from .config_manager import get_config_manager
except ImportError:
    from config_manager import get_config_manager


class FormatChecker:
    """脚本格式检查和修复工具"""
    
    def __init__(self, platform: str):
        """
        初始化格式检查器
        
        Args:
            platform: 平台标识
        """
        self.platform = platform
        self.config_mgr = get_config_manager()
        self.platform_config = self.config_mgr.get_platform_config(platform)
        self.issues = []
        self.fixes = []
    
    def validate_script(self, script: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        验证单个脚本（Step 7: 合理性检查）
        
        Args:
            script: 脚本数据
            
        Returns:
            (是否通过, 问题列表)
        """
        self.issues = []
        
        # 9维度检查
        checks = [
            ("时间合理性", self._check_time),
            ("内容合理性", self._check_content),
            ("场景合理性", self._check_scene),
            ("台词合理性", self._check_lines),
            ("分镜时长限制", self._check_segment_duration),
            ("技术描述合理性", self._check_technical),
            ("标题合理性", self._check_title),
            ("格式合理性", self._check_format),
            ("故事叙述", self._check_story)
        ]
        
        for check_name, check_func in checks:
            try:
                check_func(script)
            except Exception as e:
                self.issues.append(f"{check_name}: {str(e)}")
        
        passed = len(self.issues) == 0
        return passed, self.issues
    
    def validate_batch(self, scripts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        批量验证脚本
        
        Args:
            scripts: 脚本列表
            
        Returns:
            验证结果字典
        """
        results = {
            "total": len(scripts),
            "passed": 0,
            "failed": 0,
            "details": []
        }
        
        for i, script in enumerate(scripts, 1):
            passed, issues = self.validate_script(script)
            
            if passed:
                results["passed"] += 1
            else:
                results["failed"] += 1
            
            results["details"].append({
                "script_id": i,
                "passed": passed,
                "issues": issues
            })
        
        return results
    
    def auto_fix(self, script: Dict[str, Any]) -> Dict[str, Any]:
        """
        自动修复脚本问题
        
        Args:
            script: 原始脚本
            
        Returns:
            修复后的脚本
        """
        self.fixes = []
        fixed_script = script.copy()
        
        # 修复字数不足
        fixed_script = self._fix_min_chars(fixed_script)
        
        # 修复口语化问题
        fixed_script = self._fix_colloquial(fixed_script)
        
        # 修复格式问题
        fixed_script = self._fix_format_issues(fixed_script)
        
        return fixed_script
    
    def _check_time(self, script: Dict[str, Any]):
        """检查时间合理性"""
        segments = script.get("segments", [])
        if not segments:
            raise ValueError("分镜数据为空")
        
        # 检查时间连续性
        prev_end = 0
        for seg in segments:
            time_str = seg.get("time", "")
            match = re.match(r'(\d+)-(\d+)秒', time_str)
            if not match:
                raise ValueError(f"时间段格式错误: {time_str}")
            
            start, end = int(match.group(1)), int(match.group(2))
            if start != prev_end:
                raise ValueError(f"时间不连续: 期望{prev_end}秒开始，实际{start}秒")
            
            prev_end = end
    
    def _check_content(self, script: Dict[str, Any]):
        """检查内容合理性"""
        segments = script.get("segments", [])
        
        # 检查内容连贯性
        for i in range(len(segments) - 1):
            current = segments[i]
            next_seg = segments[i + 1]
            
            # 检查是否有内容
            if not current.get("shot_desc"):
                raise ValueError(f"第{i+1}分镜镜头描述为空")
    
    def _check_scene(self, script: Dict[str, Any]):
        """检查场景合理性"""
        segments = script.get("segments", [])
        
        for i, seg in enumerate(segments):
            scene_desc = seg.get("scene_desc", "")
            # 检查场景描述是否具体
            if len(scene_desc) < 10:
                raise ValueError(f"第{i+1}分镜场景描述过短")
    
    def _check_lines(self, script: Dict[str, Any]):
        """检查台词合理性"""
        segments = script.get("segments", [])
        
        for i, seg in enumerate(segments):
            line = seg.get("line", "")
            
            # 检查书面语
            formal_words = ["首先", "其次", "综上所述", "由此可见"]
            for word in formal_words:
                if word in line:
                    raise ValueError(f"第{i+1}分镜台词包含书面语: {word}")
    
    def _check_segment_duration(self, script: Dict[str, Any]):
        """检查分镜时长限制"""
        segments = script.get("segments", [])
        duration_config = self.platform_config.get("duration", {})
        segment_range = duration_config.get("segment_seconds", {})
        min_dur = segment_range.get("min", 3)
        max_dur = segment_range.get("max", 12)
        
        for i, seg in enumerate(segments):
            duration = seg.get("duration", 0)
            if duration < min_dur or duration > max_dur:
                raise ValueError(
                    f"第{i+1}分镜时长{duration}秒超出范围[{min_dur}-{max_dur}]"
                )
    
    def _check_technical(self, script: Dict[str, Any]):
        """检查技术描述合理性"""
        segments = script.get("segments", [])
        content_req = self.platform_config.get("content_requirements", {}).get("columns", {})
        
        # 检查各列字数
        column_checks = [
            ("C", "shot_desc", "镜头描述"),
            ("D", "movement_desc", "运镜描述"),
            ("E", "tech_desc", "技巧描述"),
            ("F", "scene_desc", "画面描述"),
            ("H", "sound_desc", "音效描述")
        ]
        
        for col_key, field, name in column_checks:
            min_chars = content_req.get(col_key, {}).get("min_chars", 0)
            
            for i, seg in enumerate(segments):
                content = seg.get(field, "")
                if len(content) < min_chars:
                    raise ValueError(
                        f"第{i+1}分镜{name}不足{min_chars}字，实际{len(content)}字"
                    )
    
    def _check_title(self, script: Dict[str, Any]):
        """检查标题合理性"""
        title_rules = self.platform_config.get("title_rules", {})
        max_length = title_rules.get("max_length", 50)
        no_punctuation = title_rules.get("no_punctuation", False)
        
        title = script.get("title", "")
        
        # 检查长度
        if len(title) > max_length:
            raise ValueError(f"标题过长: {len(title)}字 > 限制{max_length}字")
        
        # 检查标点
        if no_punctuation and re.search(r'[，。？！,\.\?!]', title):
            raise ValueError("标题包含标点符号")
    
    def _check_format(self, script: Dict[str, Any]):
        """检查格式合理性"""
        required_fields = [
            "title", "theme", "story", "total_duration",
            "segments_count", "segments"
        ]
        
        for field in required_fields:
            if field not in script:
                raise ValueError(f"缺少必需字段: {field}")
    
    def _check_story(self, script: Dict[str, Any]):
        """检查故事叙述"""
        story = script.get("story", "")
        
        # 检查是否有起承转合结构
        # 简化检查：至少包含200字以上的叙述
        if len(story) < 200:
            raise ValueError(f"故事叙述过短: {len(story)}字，建议200字以上")
        
        # 检查是否包含完整叙述
        if not any(word in story for word in ["后来", "然后", "最后", "结果"]):
            raise ValueError("故事叙述可能不完整，缺少承接词")
    
    def _fix_min_chars(self, script: Dict[str, Any]) -> Dict[str, Any]:
        """修复字数不足问题"""
        content_req = self.platform_config.get("content_requirements", {}).get("columns", {})
        segments = script.get("segments", [])
        
        column_fixes = [
            ("C", "shot_desc", "镜头", "特写镜头，展现细节"),
            ("D", "movement_desc", "运镜", "缓慢推近，营造氛围"),
            ("E", "tech_desc", "技巧", "使用稳定器，确保画面平稳"),
            ("F", "scene_desc", "画面", "自然光线，柔和色调"),
            ("H", "sound_desc", "音效", "环境音为主，配合轻音乐")
        ]
        
        for col_key, field, name, default_text in column_fixes:
            min_chars = content_req.get(col_key, {}).get("min_chars", 0)
            
            for seg in segments:
                content = seg.get(field, "")
                if len(content) < min_chars:
                    # 补充默认文本
                    seg[field] = content + " " + default_text
                    self.fixes.append(f"补充{name}描述至{min_chars}字")
        
        return script
    
    def _fix_colloquial(self, script: Dict[str, Any]) -> Dict[str, Any]:
        """修复口语化问题"""
        formal_to_colloquial = {
            "首先": "先",
            "其次": "再说",
            "综上所述": "总之",
            "由此可见": "所以说"
        }
        
        for seg in script.get("segments", []):
            line = seg.get("line", "")
            for formal, colloquial in formal_to_colloquial.items():
                if formal in line:
                    line = line.replace(formal, colloquial)
                    self.fixes.append(f"替换书面语'{formal}'为'{colloquial}'")
            seg["line"] = line
        
        return script
    
    def _fix_format_issues(self, script: Dict[str, Any]) -> Dict[str, Any]:
        """修复格式问题"""
        # 确保所有必需字段存在
        if "story" not in script or not script["story"]:
            script["story"] = "这是一个关于" + script.get("theme", "主题") + "的故事"
            self.fixes.append("补充故事叙述")
        
        return script
    
    def get_fix_report(self) -> str:
        """获取修复报告"""
        if not self.fixes:
            return "无需修复"
        
        return "\n".join([f"- {fix}" for fix in self.fixes])
    
    def validate_activity(self, activity: str, config: dict = None) -> dict:
        """
        验证关联活动字段
        
        Args:
            activity: 活动字段内容
            config: 配置字典（可选）
            
        Returns:
            验证结果字典
        """
        errors = []
        
        # 获取当前配置的活动
        if config is None:
            config = self.platform_config
        
        activities = config.get('activities', {}).get('list', [])
        valid_names = [a.get('name') for a in activities if a.get('id') != 'example']
        
        # 禁止值检查（任务标识）
        forbidden_values = ["天选之子", "step", "流程", "task", "流程"]
        for forbidden in forbidden_values:
            if forbidden.lower() in activity.lower():
                errors.append(f"关联活动不能包含'{forbidden}'")
        
        # 检查是否在有效活动列表中（仅当用户配置了活动时）
        if valid_names and activity not in valid_names:
            # 允许"日常推广"或默认提示
            if not activity.startswith("日常推广"):
                errors.append(f"关联活动'{activity}'不在配置的活动列表中")
        
        # 未配置活动时，检查是否显示默认提示
        if not valid_names:
            if "当前未设置activities" not in activity:
                errors.append("未配置活动时，应显示'日常推广，当前未设置activities'")
        
        return {"valid": len(errors) == 0, "errors": errors}
    
    def validate_bgm(self, bgm_text: str) -> dict:
        """
        验证BGM字段格式
        
        Args:
            bgm_text: BGM字段内容
            
        Returns:
            验证结果字典
        """
        errors = []
        
        # 检查是否为占位符
        placeholder_values = ["推荐音乐", "BGM", "音乐", "", " "]
        if bgm_text.strip() in placeholder_values:
            errors.append("BGM不能只是占位符，需生成具体内容（音乐名+风格+使用时机）")
        
        # 检查是否包含必需字段
        required_parts = ["音乐名：", "风格：", "使用时机："]
        for part in required_parts:
            if part not in bgm_text:
                errors.append(f"BGM缺少'{part}'描述")
        
        return {"valid": len(errors) == 0, "errors": errors}
    
    def validate_duration_match(self, script: dict, platform_config: dict = None) -> dict:
        """
        验证时长匹配（台词、画面与时间段匹配）
        
        Args:
            script: 脚本数据
            platform_config: 平台配置（可选）
            
        Returns:
            验证结果字典
        """
        if platform_config is None:
            platform_config = self.platform_config
        
        # 导入时长计算器
        try:
            from .duration_calculator import DurationCalculator
        except ImportError:
            from duration_calculator import DurationCalculator
        
        calculator = DurationCalculator(platform_config)
        scenes = script.get('segments', [])
        
        results = []
        all_match = True
        
        for i, scene in enumerate(scenes, 1):
            calc = calculator.calculate_scene_duration(scene)
            results.append({
                'scene_num': i,
                **calc
            })
            if not calc['match']:
                all_match = False
        
        return {
            'all_match': all_match,
            'scenes': results,
            'total_labeled': sum(r['labeled'] for r in results),
            'total_recommended': sum(r['recommended'] for r in results)
        }


class ValidationIssue:
    """验证问题详情"""
    
    def __init__(self, dimension: str, description: str, severity: str = "error"):
        self.dimension = dimension
        self.description = description
        self.severity = severity
    
    def __str__(self):
        return f"[{self.severity}] {self.dimension}: {self.description}"
