#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数字人配置生成脚本
Digital Human Configuration Generator

功能：一键生成数字人配置参数，支持预设模板和自定义参数
平台：digital-avatar-voice-cloner / 飞影数字人 / 火山引擎

使用方法：
    python create_digital_human.py --config config.json --output ./output/
    python create_digital_human.py --template 老胡说 --output ./output/
    python create_digital_human.py --interactive

作者：胡田-OPC导师
版本：v1.0
日期：2026年5月19日
"""

import json
import os
import argparse
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

# ============================================================
# 常量定义
# ============================================================

# 预设音色
PRESET_VOICES = {
    "沉稳男声": {"pitch": 120, "speed": 130, "emotion": 0.5},
    "温柔女声": {"pitch": 220, "speed": 165, "emotion": 0.7},
    "活力少年": {"pitch": 300, "speed": 200, "emotion": 0.9},
    "知性女声": {"pitch": 230, "speed": 175, "emotion": 0.5},
    "磁性男声": {"pitch": 140, "speed": 120, "emotion": 0.6},
    "俏皮女生": {"pitch": 330, "speed": 210, "emotion": 0.95},
    "儒雅男声": {"pitch": 180, "speed": 130, "emotion": 0.45},
    "爽朗女声": {"pitch": 280, "speed": 200, "emotion": 0.85},
}

# 预设语言风格
PRESET_LANGUAGE_STYLES = {
    "正式报告": {"terminology_density": "高", "colloquial_level": "低", "interaction": "弱"},
    "轻松聊天": {"terminology_density": "低", "colloquial_level": "高", "interaction": "强"},
    "学术研讨": {"terminology_density": "极高", "colloquial_level": "极低", "interaction": "弱"},
    "实战分享": {"terminology_density": "中", "colloquial_level": "中", "interaction": "中"},
    "幽默脱口": {"terminology_density": "低", "colloquial_level": "极高", "interaction": "极强"},
    "故事叙述": {"terminology_density": "低", "colloquial_level": "低", "interaction": "弱"},
}

# 预设背景
PRESET_BACKGROUNDS = {
    "办公室": {"lighting_type": "自然光", "temperature": 4500},
    "实验室": {"lighting_type": "冷色灯光", "temperature": 6000},
    "书房": {"lighting_type": "暖色调", "temperature": 3500},
    "演播厅": {"lighting_type": "影视灯光", "temperature": 4500},
    "城市天际线": {"lighting_type": "城市灯光", "temperature": 4000},
    "工厂车间": {"lighting_type": "工业照明", "temperature": 4500},
    "大学讲堂": {"lighting_type": "讲台灯光", "temperature": 4200},
    "山水意境": {"lighting_type": "自然光", "temperature": 3500},
    "科技蓝": {"lighting_type": "冷光+发光", "temperature": 8000},
    "深色商务": {"lighting_type": "聚光灯", "temperature": 4500},
    "白板前": {"lighting_type": "均匀正面光", "temperature": 4500},
    "直播棚": {"lighting_type": "直播灯光", "temperature": 4500},
    "会议室": {"lighting_type": "会议室灯光", "temperature": 4200},
    "户外场景": {"lighting_type": "自然阳光", "temperature": 5500},
    "虚拟空间": {"lighting_type": "可调灯光", "temperature": 5000},
}

# 时长档位
DURATION_PRESETS = {
    "30秒": {"seconds": 30, "words": "150-200"},
    "1分钟": {"seconds": 60, "words": "300-500"},
    "3分钟": {"seconds": 180, "words": "800-1200"},
    "5分钟": {"seconds": 300, "words": "1500-2000"},
    "8分钟": {"seconds": 480, "words": "2500-3500"},
    "15分钟": {"seconds": 900, "words": "4000-6000"},
}

# 平台选项
PLATFORMS = {
    "digital-avatar": {
        "name": "digital-avatar-voice-cloner",
        "cost": "免费",
        "quality": "高保真",
        "output_format": "图片 + 音频",
        "resolution": "可自定义",
    },
    "feiying": {
        "name": "飞影数字人",
        "cost": "云服务",
        "quality": "专业级",
        "output_format": "MP4视频",
        "resolution": "1080P",
    },
    "volcengine": {
        "name": "火山引擎",
        "cost": "云服务",
        "quality": "商业级",
        "output_format": "MP4视频",
        "resolution": "最高4K",
    },
}


# ============================================================
# OPC专属模板定义
# ============================================================

OPC_TEMPLATES = {
    "老胡说": {
        "description": "技术成果转化实战派，OPC导师",
        "appearance": {
            "gender": "男",
            "age": "45-50岁",
            "style": "商务休闲",
            "prompt": "A mature Chinese business professional, 45-50 years old, with short neat hair featuring distinguished grey temples, wearing smart casual business attire - light blue dress shirt under a casual navy blazer, dark trousers, and leather shoes. Round professional glasses, classic wristwatch. Warm approachable smile.",
        },
        "voice": {
            "preset": "沉稳男声",
            "pitch": 120,
            "speed": 130,
            "emotion": 0.5,
            "catchphrase": ["大家好我是老胡", "关注老胡懂技术转化"],
        },
        "language": {
            "style": "实战分享",
            "terminology_density": "中",
            "colloquial_level": "中等",
            "interaction": "中",
        },
        "background": {
            "scene": "书房",
            "lighting": "自然光",
            "temperature": 3500,
        },
        "duration": "3-8分钟",
        "platform": "飞影数字人",
    },
    "OPC虚拟主播": {
        "description": "专业知识传播者，OPC平台官方主播",
        "appearance": {
            "gender": "女",
            "age": "25-35岁",
            "style": "科技专业",
            "prompt": "A young professional Chinese woman, 25-35 years old, with stylish modern hairstyle in black or brown. Wearing contemporary professional attire - a simple elegant blouse or knit top with tailored skirt or trousers. Subtle earrings and modern watch. Friendly warm smile, professional broadcast focus.",
        },
        "voice": {
            "preset": "知性女声",
            "pitch": 230,
            "speed": 175,
            "emotion": 0.6,
            "catchphrase": ["OPC头条AI日报", "关注OPC智库"],
        },
        "language": {
            "style": "轻松聊天",
            "terminology_density": "低-中",
            "colloquial_level": "高",
            "interaction": "高",
        },
        "background": {
            "scene": "演播厅",
            "lighting": "影视灯光",
            "temperature": 4500,
        },
        "duration": "1-3分钟",
        "platform": "火山引擎",
    },
    "王阳明": {
        "description": "心学大师，明代思想家",
        "appearance": {
            "gender": "男",
            "age": "45-55岁",
            "style": "国风儒雅",
            "prompt": "A distinguished Chinese scholar from Ming Dynasty, 45-55 years old, wearing traditional Hanfu - dark blue or charcoal changshan (long robe), with a traditional Chinese hairstyle. Holding a folding fan. Scholarly and refined appearance with wise penetrating eyes.",
        },
        "voice": {
            "preset": "儒雅男声",
            "pitch": 180,
            "speed": 130,
            "emotion": 0.45,
            "catchphrase": ["知行合一", "致良知", "事上练"],
        },
        "language": {
            "style": "学术研讨",
            "terminology_density": "高",
            "colloquial_level": "低",
            "interaction": "弱",
        },
        "background": {
            "scene": "书房",
            "lighting": "暖色调",
            "temperature": 3500,
        },
        "duration": "5-10分钟",
        "platform": "digital-avatar",
    },
    "曾国藩": {
        "description": "实战派领袖，清代名臣",
        "appearance": {
            "gender": "男",
            "age": "50-60岁",
            "style": "稳重内敛",
            "prompt": "A senior Qing Dynasty official and military leader, 50-60 years old, wearing formal Qing Dynasty官服 (mandarin robe) in deep blue or dark grey, with traditional hairstyle. Dignified and authoritative presence.",
        },
        "voice": {
            "preset": "沉稳男声",
            "pitch": 120,
            "speed": 120,
            "emotion": 0.4,
            "catchphrase": ["结硬寨打呆仗", "稳扎稳打", "耐烦"],
        },
        "language": {
            "style": "实战分享",
            "terminology_density": "中",
            "colloquial_level": "中",
            "interaction": "中",
        },
        "background": {
            "scene": "书房",
            "lighting": "暖色调",
            "temperature": 3500,
        },
        "duration": "5-8分钟",
        "platform": "digital-avatar",
    },
    "苏轼": {
        "description": "旷达智者，北宋文学家",
        "appearance": {
            "gender": "男",
            "age": "40-50岁",
            "style": "文艺潇洒",
            "prompt": "A celebrated Song Dynasty poet and scholar, 40-50 years old, wearing traditional Chinese scholar robes in earth tones or muted blue, with a relaxed traditional hairstyle. Wise but carefree expression. Holding a wine cup or brush for calligraphy.",
        },
        "voice": {
            "preset": "儒雅男声",
            "pitch": 175,
            "speed": 140,
            "emotion": 0.55,
            "catchphrase": ["竹杖芒鞋轻胜马", "也无风雨也无晴"],
        },
        "language": {
            "style": "故事叙述",
            "terminology_density": "低",
            "colloquial_level": "中",
            "interaction": "中",
        },
        "background": {
            "scene": "山水意境",
            "lighting": "自然光",
            "temperature": 3500,
        },
        "duration": "3-5分钟",
        "platform": "digital-avatar",
    },
}


# ============================================================
# 配置生成器类
# ============================================================

class DigitalHumanConfigGenerator:
    """数字人配置生成器"""
    
    def __init__(self, output_dir: str = "./output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.config = {}
    
    def load_template(self, template_name: str) -> Optional[Dict[str, Any]]:
        """加载预设模板"""
        return OPC_TEMPLATES.get(template_name)
    
    def generate_config(
        self,
        template_name: Optional[str] = None,
        appearance: Optional[Dict] = None,
        voice: Optional[Dict] = None,
        language: Optional[Dict] = None,
        background: Optional[Dict] = None,
        duration: Optional[str] = None,
        platform: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """生成完整配置"""
        
        # 如果指定了模板，从模板开始
        if template_name and template_name in OPC_TEMPLATES:
            self.config = OPC_TEMPLATES[template_name].copy()
        else:
            self.config = {
                "description": "自定义数字人",
                "appearance": {},
                "voice": {},
                "language": {},
                "background": {},
            }
        
        # 合并自定义参数
        if appearance:
            self.config["appearance"].update(appearance)
        if voice:
            self.config["voice"].update(voice)
        if language:
            self.config["language"].update(language)
        if background:
            self.config["background"].update(background)
        if duration:
            self.config["duration"] = duration
        if platform:
            self.config["platform"] = platform
        
        # 添加元数据
        self.config["_meta"] = {
            "generated_at": datetime.now().isoformat(),
            "generator": "胡田-OPC导师-数字人工坊",
            "version": "v1.0",
        }
        
        return self.config
    
    def save_config(self, filename: str = None) -> str:
        """保存配置到文件"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"digital_human_config_{timestamp}.json"
        
        filepath = self.output_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
        
        return str(filepath)
    
    def generate_avatar_prompt(self) -> str:
        """生成形象提示词"""
        if "appearance" in self.config and "prompt" in self.config["appearance"]:
            return self.config["appearance"]["prompt"]
        return ""
    
    def generate_summary(self) -> str:
        """生成配置摘要"""
        lines = [
            "=" * 60,
            "数字人配置摘要",
            "=" * 60,
        ]
        
        if "description" in self.config:
            lines.append(f"\n描述: {self.config['description']}")
        
        if "appearance" in self.config:
            app = self.config["appearance"]
            lines.extend([
                "\n【外观配置】",
                f"  性别: {app.get('gender', '未设置')}",
                f"  年龄: {app.get('age', '未设置')}",
                f"  风格: {app.get('style', '未设置')}",
            ])
        
        if "voice" in self.config:
            voice = self.config["voice"]
            lines.extend([
                "\n【声音配置】",
                f"  音色: {voice.get('preset', '未设置')}",
                f"  音高: {voice.get('pitch', '未设置')} Hz",
                f"  语速: {voice.get('speed', '未设置')} 字/分钟",
                f"  情感: {voice.get('emotion', '未设置')}",
            ])
        
        if "language" in self.config:
            lang = self.config["language"]
            lines.extend([
                "\n【语言风格】",
                f"  风格: {lang.get('style', '未设置')}",
                f"  术语密度: {lang.get('terminology_density', '未设置')}",
                f"  口语化: {lang.get('colloquial_level', '未设置')}",
            ])
        
        if "background" in self.config:
            bg = self.config["background"]
            lines.extend([
                "\n【背景配置】",
                f"  场景: {bg.get('scene', '未设置')}",
                f"  光照: {bg.get('lighting', '未设置')}",
                f"  色温: {bg.get('temperature', '未设置')} K",
            ])
        
        if "duration" in self.config:
            lines.append(f"\n【时长】: {self.config['duration']}")
        
        if "platform" in self.config:
            lines.append(f"\n【平台】: {self.config['platform']}")
        
        lines.append("\n" + "=" * 60)
        return "\n".join(lines)


# ============================================================
# 交互式配置生成
# ============================================================

def interactive_mode() -> Dict[str, Any]:
    """交互式配置生成"""
    
    print("\n" + "=" * 60)
    print("数字人配置生成器 - 交互模式")
    print("=" * 60)
    
    generator = DigitalHumanConfigGenerator()
    
    # 检查是否有预设模板
    print("\n【步骤1】选择人物模板")
    print("可选模板:")
    for i, name in enumerate(OPC_TEMPLATES.keys(), 1):
        desc = OPC_TEMPLATES[name]["description"]
        print(f"  {i}. {name} - {desc}")
    print(f"  {len(OPC_TEMPLATES) + 1}. 自定义模板")
    
    choice = input("\n请选择模板编号: ").strip()
    try:
        choice_num = int(choice)
        if 1 <= choice_num <= len(OPC_TEMPLATES):
            template_name = list(OPC_TEMPLATES.keys())[choice_num - 1]
        elif choice_num == len(OPC_TEMPLATES) + 1:
            template_name = None
        else:
            template_name = None
    except ValueError:
        template_name = None
    
    # 生成基础配置
    if template_name:
        config = generator.generate_config(template_name=template_name)
        print(f"\n已加载模板: {template_name}")
    else:
        config = generator.generate_config()
        print("\n自定义配置模式")
    
    # 声音配置
    print("\n【步骤2】声音配置")
    print("可选音色:")
    for i, name in enumerate(PRESET_VOICES.keys(), 1):
        params = PRESET_VOICES[name]
        print(f"  {i}. {name} (音高:{params['pitch']}Hz, 语速:{params['speed']}字/分)")
    
    voice_choice = input(f"\n请选择音色编号 (直接回车使用模板默认值): ").strip()
    if voice_choice:
        try:
            voice_num = int(voice_choice)
            if 1 <= voice_num <= len(PRESET_VOICES):
                voice_name = list(PRESET_VOICES.keys())[voice_num - 1]
                config["voice"]["preset"] = voice_name
                config["voice"].update(PRESET_VOICES[voice_name])
        except ValueError:
            pass
    
    # 背景配置
    print("\n【步骤3】背景配置")
    print("可选背景:")
    for i, name in enumerate(PRESET_BACKGROUNDS.keys(), 1):
        params = PRESET_BACKGROUNDS[name]
        print(f"  {i}. {name} (色温:{params['temperature']}K)")
    
    bg_choice = input(f"\n请选择背景编号 (直接回车使用模板默认值): ").strip()
    if bg_choice:
        try:
            bg_num = int(bg_choice)
            if 1 <= bg_num <= len(PRESET_BACKGROUNDS):
                bg_name = list(PRESET_BACKGROUNDS.keys())[bg_num - 1]
                config["background"]["scene"] = bg_name
                config["background"].update(PRESET_BACKGROUNDS[bg_name])
        except ValueError:
            pass
    
    # 时长配置
    print("\n【步骤4】时长配置")
    print("可选时长档位:")
    for i, (name, params) in enumerate(DURATION_PRESETS.items(), 1):
        print(f"  {i}. {name} ({params['words']}字)")
    
    dur_choice = input(f"\n请选择时长编号 (直接回车使用模板默认值): ").strip()
    if dur_choice:
        try:
            dur_num = int(dur_choice)
            if 1 <= dur_num <= len(DURATION_PRESETS):
                dur_name = list(DURATION_PRESETS.keys())[dur_num - 1]
                config["duration"] = dur_name
        except ValueError:
            pass
    
    # 平台配置
    print("\n【步骤5】平台配置")
    print("可选平台:")
    for i, (key, platform) in enumerate(PLATFORMS.items(), 1):
        print(f"  {i}. {platform['name']} ({platform['cost']}, {platform['quality']})")
    
    plat_choice = input(f"\n请选择平台编号 (直接回车使用模板默认值): ").strip()
    if plat_choice:
        try:
            plat_num = int(plat_choice)
            if 1 <= plat_num <= len(PLATFORMS):
                plat_key = list(PLATFORMS.keys())[plat_num - 1]
                config["platform"] = PLATFORMS[plat_key]["name"]
        except ValueError:
            pass
    
    generator.config = config
    return config


# ============================================================
# 主程序入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="数字人配置生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 使用预设模板生成配置
  python create_digital_human.py --template 老胡说 --output ./output/
  
  # 使用配置文件生成
  python create_digital_human.py --config config.json --output ./output/
  
  # 交互式配置
  python create_digital_human.py --interactive
  
  # 自定义参数
  python create_digital_human.py --template 老胡说 --duration 5分钟 --platform 火山引擎
        """
    )
    
    parser.add_argument("--template", "-t", type=str, help="选择预设模板")
    parser.add_argument("--config", "-c", type=str, help="配置文件路径")
    parser.add_argument("--output", "-o", type=str, default="./output/", help="输出目录")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互式配置")
    parser.add_argument("--duration", "-d", type=str, help="设置时长")
    parser.add_argument("--platform", "-p", type=str, help="设置平台")
    
    args = parser.parse_args()
    
    generator = DigitalHumanConfigGenerator(output_dir=args.output)
    
    # 交互式模式
    if args.interactive:
        config = interactive_mode()
        generator.config = config
    # 从文件加载
    elif args.config and os.path.exists(args.config):
        with open(args.config, "r", encoding="utf-8") as f:
            generator.config = json.load(f)
    # 从模板生成
    elif args.template:
        generator.generate_config(
            template_name=args.template,
            duration=args.duration,
            platform=args.platform,
        )
    else:
        parser.print_help()
        return
    
    # 输出配置
    print(generator.generate_summary())
    
    # 保存配置
    filepath = generator.save_config()
    print(f"\n配置已保存到: {filepath}")
    
    # 生成形象提示词
    prompt = generator.generate_avatar_prompt()
    if prompt:
        prompt_file = generator.output_dir / "avatar_prompt.txt"
        with open(prompt_file, "w", encoding="utf-8") as f:
            f.write(prompt)
        print(f"形象提示词已保存到: {prompt_file}")


if __name__ == "__main__":
    main()
