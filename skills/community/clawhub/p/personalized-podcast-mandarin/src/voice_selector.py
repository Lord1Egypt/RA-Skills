# -*- coding: utf-8 -*-
"""
音色选择器
加载完整 TTS 音色列表，为 Persona Extractor 提供动态选择能力
"""

import json
from pathlib import Path
from typing import List, Dict, Optional


class VoiceSelector:
    """TTS 音色选择器"""

    def __init__(self, voice_list_path: Optional[Path] = None):
        """
        初始化音色选择器

        Args:
            voice_list_path: 音色列表 JSON 文件路径，默认使用 api/TTS-voice-list.json
        """
        if voice_list_path is None:
            self.voice_list_path = Path(__file__).parent.parent / "api" / "TTS-voice-list.json"
        else:
            self.voice_list_path = voice_list_path

        self._voices: List[Dict] = []
        self._loaded = False

    def load_voices(self) -> List[Dict]:
        """
        加载音色列表

        Returns:
            音色列表
        """
        if self._loaded:
            return self._voices

        try:
            with open(self.voice_list_path, 'r', encoding='utf-8') as f:
                self._voices = json.load(f)
            self._loaded = True
        except Exception as e:
            print(f"[Warning] 加载音色列表失败: {e}")
            self._voices = []

        return self._voices

    def get_voices_by_gender(self, gender: str) -> List[Dict]:
        """
        按性别筛选音色

        Args:
            gender: "male" 或 "female"

        Returns:
            符合条件的音色列表
        """
        voices = self.load_voices()

        if gender not in ["male", "female"]:
            return voices

        result = []
        for v in voices:
            voice_type = v.get("voice_type", "")

            # 根据 voice_type 判断性别
            # female: zh_female_... , male: zh_male_... , en_male_... , en_female_...
            if gender == "female":
                if "_female_" in voice_type or "女" in v.get("音色名称", ""):
                    result.append(v)
            else:  # male
                if "_male_" in voice_type and "_female_" not in voice_type:
                    # 排除像 "zh_male_sophie_uranus_bigtts" 这种历史遗留命名
                    # 但 sophie 实际是女声，需要额外判断
                    name = v.get("音色名称", "")
                    if "女" not in name:  # 确保名称中没有"女"字
                        result.append(v)

        return result

    def build_selection_prompt(self, gender: str = "female", max_voices: int = 15) -> str:
        """
        构建音色选择 prompt，供 Persona Extractor 使用

        Args:
            gender: 性别筛选 ("male" 或 "female")
            max_voices: 最多返回多少条音色（避免 prompt 过长）

        Returns:
            格式化的音色列表文本
        """
        voices = self.get_voices_by_gender(gender)

        if not voices:
            return ""

        lines = []
        lines.append("## 可用 TTS 音色列表")
        lines.append(f"（根据 gender='{gender}' 筛选，共 {len(voices)} 个音色）")
        lines.append("")

        # 按场景分组
        scenes = {}
        for v in voices:
            scene = v.get("场景", "其他")
            if scene not in scenes:
                scenes[scene] = []
            scenes[scene].append(v)

        # 构建输出
        count = 0
        for scene, scene_voices in scenes.items():
            if count >= max_voices:
                break

            lines.append(f"### {scene}")

            for v in scene_voices:
                if count >= max_voices:
                    break

                name = v.get("音色名称", "")
                voice_type = v.get("voice_type", "")
                abilities = v.get("支持能力", "")

                lines.append(f"- {name} | `{voice_type}` | {abilities}")
                count += 1

            lines.append("")

        lines.append("## 音色选择规则")
        lines.append("根据 archetype 和 attitude 选择最合适的音色：")
        lines.append("- 观察者 + curious → 选择知性、沉稳风格的音色（如 知性灿灿、云舟）")
        lines.append("- 讲故事的人 + playful → 选择活泼、亲和风格的音色（如 爽快思思、小天）")
        lines.append("- 追问者 + skeptical → 选择专业、理性风格的音色（如 刘飞、知性灿灿）")
        lines.append("- 吐槽者 + playful → 选择幽默、直率风格的音色（如 猴哥、佩奇猪）")
        lines.append("- 理想主义者 + passionate → 选择富有表现力的音色（如 Vivi、少年梓辛）")
        lines.append("")
        lines.append("选择后，将 voice_type 填入 expression.voice_id 字段。")

        return "\n".join(lines)

    def suggest_voice(self, archetype: str, attitude: str, gender: str = "female") -> str:
        """
        根据 archetype 和 attitude 推荐默认音色
        用于后端兜底逻辑

        Args:
            archetype: 原型角色
            attitude: 态度
            gender: 性别

        Returns:
            推荐的 voice_type
        """
        voices = self.get_voices_by_gender(gender)

        # 构建推荐映射
        recommendations = {
            ("观察者", "curious"): ["zh_female_cancan_uranus_bigtts", "zh_male_m191_uranus_bigtts"],
            ("讲故事的人", "playful"): ["zh_female_shuangkuaisisi_uranus_bigtts", "zh_male_taocheng_uranus_bigtts"],
            ("追问者", "skeptical"): ["zh_female_cancan_uranus_bigtts", "zh_male_liufei_uranus_bigtts"],
            ("吐槽者", "playful"): ["zh_female_shuangkuaisisi_uranus_bigtts", "zh_male_taocheng_uranus_bigtts"],
            ("理想主义者", "passionate"): ["zh_female_vv_uranus_bigtts", "zh_male_shaonianzixin_uranus_bigtts"],
            ("观察者", "playful"): ["zh_female_linjianvhai_uranus_bigtts", "zh_male_taocheng_uranus_bigtts"],
            ("讲故事的人", "curious"): ["zh_female_xiaohe_uranus_bigtts", "zh_male_ruyayichen_uranus_bigtts"],
        }

        # 查找推荐
        key = (archetype, attitude)
        if key in recommendations:
            for voice_type in recommendations[key]:
                # 检查是否存在于列表中
                if any(v.get("voice_type") == voice_type for v in voices):
                    return voice_type

        # 默认回退
        default_map = {
            "female": "zh_female_vv_uranus_bigtts",
            "male": "zh_male_shaonianzixin_uranus_bigtts"
        }
        return default_map.get(gender, "zh_female_vv_uranus_bigtts")


