"""
脚本生成器 - 基于AI生成短视频脚本
整合提示词模板和平台配置
"""

import json
from typing import Dict, List, Any, Optional

# 尝试相对导入，失败则使用绝对导入
try:
    from .config_manager import ConfigManager, get_config_manager
except ImportError:
    from config_manager import ConfigManager, get_config_manager


class ScriptGenerator:
    """生成短视频脚本的AI驱动引擎"""
    
    def __init__(self, 
                 platform: str,
                 duration: str = None,
                 keywords: List[str] = None,
                 trending_titles: List[str] = None,
                 avoid_themes: List[str] = None):
        """
        初始化脚本生成器
        
        Args:
            platform: 平台标识（xiaohongshu/douyin/shipinhao）
            duration: 总时长描述（如"2-3min"）
            keywords: 搜索关键词列表
            trending_titles: 爆款标题列表
            avoid_themes: 需避开的主题列表
        """
        self.platform = platform
        self.duration = duration
        self.keywords = keywords or []
        self.trending_titles = trending_titles or []
        self.avoid_themes = avoid_themes or []
        
        self.config_mgr = get_config_manager()
        self.platform_config = self.config_mgr.get_platform_config(platform)
        
        # 计算分镜数量
        self.segments_count = self._calculate_segments()
    
    def _calculate_segments(self) -> int:
        """计算分镜数量"""
        duration_config = self.platform_config.get("duration", {})
        
        # 获取分镜时长范围
        segment_range = duration_config.get("segment_seconds", {})
        min_seg = segment_range.get("min", 3)
        max_seg = segment_range.get("max", 12)
        avg_seg = (min_seg + max_seg) / 2
        
        # 获取总时长
        if self.duration:
            # 从duration参数解析
            total_seconds = self._parse_duration(self.duration)
        else:
            total_config = duration_config.get("total_seconds", {})
            min_total = total_config.get("min", 120)
            max_total = total_config.get("max", 180)
            total_seconds = (min_total + max_total) / 2
        
        # 计算分镜数量
        segments_count = int(total_seconds / avg_seg)
        return max(segments_count, 1)
    
    def _parse_duration(self, duration_str: str) -> int:
        """解析时长字符串为秒数"""
        duration_str = duration_str.lower().replace(" ", "")
        
        # 解析 "2-3min" 格式
        if "min" in duration_str:
            parts = duration_str.replace("min", "").split("-")
            if len(parts) == 2:
                avg_min = (float(parts[0]) + float(parts[1])) / 2
                return int(avg_min * 60)
            else:
                return int(float(parts[0]) * 60)
        
        # 解析 "120s" 格式
        if "s" in duration_str:
            return int(duration_str.replace("s", ""))
        
        return 120  # 默认2分钟
    
    def generate(self, count: int = 5) -> List[Dict[str, Any]]:
        """
        生成指定数量的脚本
        
        Args:
            count: 脚本数量
            
        Returns:
            脚本列表
        """
        scripts = []
        
        for i in range(count):
            script = self._generate_single_script(i + 1)
            scripts.append(script)
        
        return scripts
    
    def _generate_single_script(self, script_num: int) -> Dict[str, Any]:
        """生成单个脚本"""
        # 计算分镜时长分配
        segment_durations = self._distribute_duration()
        
        # 构建提示词
        prompt = self._build_prompt(script_num)
        
        # 构建脚本结构
        script = {
            "script_id": script_num,
            "title": f"脚本{script_num}",
            "theme": self.trending_titles[script_num - 1] if script_num <= len(self.trending_titles) else "",
            "story": "",  # 由AI生成
            "total_duration": self.duration or self.platform_config["duration"]["total"],
            "segments_count": self.segments_count,
            "segments": self._build_segments_structure(segment_durations)
        }
        
        return script
    
    def _distribute_duration(self) -> List[int]:
        """
        分配分镜时长
        遵循"开头快、中间稳、结尾慢"原则
        """
        duration_config = self.platform_config.get("duration", {})
        segment_range = duration_config.get("segment_seconds", {})
        min_seg = segment_range.get("min", 3)
        max_seg = segment_range.get("max", 12)
        
        n = self.segments_count
        
        # 分段：开场(20%)、主体(60%)、结尾(20%)
        intro_count = max(1, int(n * 0.2))
        ending_count = max(1, int(n * 0.2))
        body_count = n - intro_count - ending_count
        
        durations = []
        
        # 开场：较短，快速吸引
        for i in range(intro_count):
            duration = min_seg + (max_seg - min_seg) * 0.2 * (i + 1) / intro_count
            durations.append(int(duration))
        
        # 主体：中等，内容展开
        for i in range(body_count):
            duration = (min_seg + max_seg) / 2
            durations.append(int(duration))
        
        # 结尾：较长，升华收尾
        for i in range(ending_count):
            duration = max_seg - (max_seg - min_seg) * 0.3 * (ending_count - i) / ending_count
            durations.append(int(duration))
        
        return durations
    
    def _build_segments_structure(self, durations: List[int]) -> List[Dict[str, Any]]:
        """构建分镜结构"""
        segments = []
        current_time = 0
        
        content_req = self.platform_config.get("content_requirements", {}).get("columns", {})
        
        for i, duration in enumerate(durations, 1):
            start_time = current_time
            end_time = current_time + duration
            
            segment = {
                "seg_id": i,
                "time": f"{start_time}-{end_time}秒",
                "duration": duration,
                "shot_desc": "",  # C列-镜头，需满足min_chars
                "movement_desc": "",  # D列-运镜
                "tech_desc": "",  # E列-技巧
                "scene_desc": "",  # F列-画面
                "line": "",  # G列-台词
                "sound_desc": "",  # H列-音效
                "bgm": "",  # I列-BGM
                "tags": "",  # J列-标签
                "status": "待使用",  # K列-状态
                "activity": "",  # L列-活动
                "date": "",  # M列-日期
                "notes": ""  # N列-备注
            }
            
            segments.append(segment)
            current_time = end_time
        
        return segments
    
    def _build_prompt(self, script_num: int) -> str:
        """构建AI提示词"""
        # 读取模板
        import json
        
        config_path = self.config_mgr.skill_path / "config" / "templates.json"
        with open(config_path, 'r', encoding='utf-8') as f:
            templates = json.load(f)
        
        template = templates.get("prompt_templates", {}).get("subtask6_generate", {}).get("template", "")
        
        # 获取字数要求
        content_req = self.platform_config.get("content_requirements", {}).get("columns", {})
        
        # 替换变量
        prompt = template
        prompt = prompt.replace("[TRENDING_TITLES]", ", ".join(self.trending_titles[:5]))
        prompt = prompt.replace("[PLATFORM_RULES]", "从规则文档读取")
        prompt = prompt.replace("[PLATFORM_CONFIG]", json.dumps(self.platform_config, ensure_ascii=False))
        prompt = prompt.replace("[SEGMENTS_COUNT]", str(self.segments_count))
        prompt = prompt.replace("[TOTAL_DURATION]", self.duration or self.platform_config["duration"]["total"])
        prompt = prompt.replace("[SEGMENT_DURATION_RANGE]", self.platform_config["duration"]["segment"])
        prompt = prompt.replace("[AVOID_THEMES]", ", ".join(self.avoid_themes))
        prompt = prompt.replace("[PLATFORM_NAME]", self.platform_config["name"])
        prompt = prompt.replace("[TARGET_AUDIENCE]", self.platform_config["user_profile"])
        prompt = prompt.replace("[CONTENT_STYLE]", self.platform_config["content_style"])
        prompt = prompt.replace("[SCRIPT_COUNT]", "5")
        
        # 替换字数要求
        prompt = prompt.replace("[MIN_CHARS_SHOT]", str(content_req.get("C", {}).get("min_chars", 20)))
        prompt = prompt.replace("[MIN_CHARS_MOVEMENT]", str(content_req.get("D", {}).get("min_chars", 15)))
        prompt = prompt.replace("[MIN_CHARS_TECHNIQUE]", str(content_req.get("E", {}).get("min_chars", 15)))
        prompt = prompt.replace("[MIN_CHARS_SCENE]", str(content_req.get("F", {}).get("min_chars", 20)))
        prompt = prompt.replace("[MIN_CHARS_LINE]", str(content_req.get("G", {}).get("min_chars", 30)))
        prompt = prompt.replace("[MIN_CHARS_SOUND]", str(content_req.get("H", {}).get("min_chars", 15)))
        
        return prompt
    
    def get_prompt_for_script(self, script_num: int) -> str:
        """获取指定脚本的生成提示词（供外部调用）"""
        return self._build_prompt(script_num)


class ScriptValidationError(Exception):
    """脚本验证错误"""
    pass
