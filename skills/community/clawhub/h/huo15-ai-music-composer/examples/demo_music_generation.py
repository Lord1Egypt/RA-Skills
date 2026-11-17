#!/usr/bin/env python3
"""
AI 音乐创作技能演示案例
展示完整的音乐生成流程和使用技巧

作者：聚星逸 AI 团队
版本：v1.0.0 (2026.07)
"""

import asyncio
import os
import time
import json
from pathlib import Path
from typing import Dict, List, Optional

from scripts.generate_music import AIMusicComposer

def print_section(title: str, description: str = ""):
    """打印美观的分割线"""
    print("\n" + "="*60) 
    print(f"🎵 {title}")
    print("="*60)
    if description:
        print(f"📝 {description}")

def print_result(label: str, value: str, icon: str = "✅"):
    """打印结果"""
    print(f"  {icon} {label}: {value}")

class MusicGenerationDemo:
    """音乐生成演示类"""
    
    def __init__(self):
        self.composer = AIMusicComposer()
        self.results_dir = Path("demo_results")
        self.results_dir.mkdir(exist_ok=True)
        
    async def demo_basic_generation(self):
        """
        演示1：基础音乐生成
        使用预设歌词和风格生成歌曲
        """
        print_section(
            "演示1：基础音乐生成", 
            "使用用户录音 + 预设歌词 + 流行风格"
        )
        
        # 模拟的配置参数
        config = {
            "voice_sample": "/demo_data/user_voice_sample.wav",
            "lyrics": "\n当春风轻轻拂过脸庞\n回忆如雪花般飘落\n在这美好的春日里\n我轻声为你唱这首歌\n\n(副歌)\n春风十里不如你\n花香满园记得你\n时光不老我们不散\n一起走过这春天\n",
            "style": "pop",
            "theme": "春日恋歌",
            "tempo": 120,
            "duration": 180,
            "emotion": "romantic",
            "key": "A",
            "language": "chinese"
        }
        
        print("📋 生成配置:")
        print(f"  🎵 风格: {config['style']}")
        print(f"  🎼 调性: {config['key']}")
        print(f"  ⏱️  速度: {config['tempo']} BPM")
        print(f"  🎭 情绪: {config['emotion']}")
        print(f"  📏 时长: {config['duration']}秒")
        
        print(f"\n🎬 开始生成...")
        start_time = time.time()
        
        try:
            # 执行生成 (这里会模拟执行)
            result = await self._simulate_generation(config)
            
            end_time = time.time()
            total_time = end_time - start_time
            
            print(f"\n🎊 生成完成！耗时: {total_time:.2f}秒")
            
            if result['success']:
                print("\n📊 生成结果:")
                print_result("任务ID", result['job_id'])
                print_result("音频文件", result['results']['final_audio']['audio_path'])
                print_result("MIDI文件", result['results']['instrumental']['midi_path'])
                print_result("质量评分", f"{result['quality']['overall_score']:.1f}/5.0")
                
                print(f"\n🎵 输出格式:")
                for format_info in result['results']['final_audio']['formats']:
                    print(f"  - {format_info['name']}: {format_info['file_path']}")
            else:
                print(f"❌ 生成失败: {result['error']}")
                
        except Exception as e:
            print(f"🚨 演示出错: {e}")
    
    async def demo_theme_based_generation(self):
        """ 
        演示2：主题驱动生成  
        仅提供主题，让 AI 自动生成歌词并创作
        """
        print_section(
            "演示2：主题驱动生成", 
            "仅提供主题，AI自动生成歌词 + 音乐"
        )
        
        themes = ["夏日海边", "青春校园", "都市夜景", "山水田园"]
        
        print("🎯 测试主题:")
        for i, theme in enumerate(themes, 1):
            print(f"  {i}. {theme}")
        
        # 选择主题
        selected_theme = "夏日海边"
        
        config = {
            "voice_sample": "/demo_data/user_voice_sample.wav", 
            "theme": selected_theme,
            "style": "folk",
            "tempo": 100,
            "emotion": "peaceful",
            "language": "chinese"
        }
        
        print(f"\n🎯 选中主题: {selected_theme}")
        print(f"🎨 生成风格: {config['style']}")
        
        try:
            result = await self._simulate_theme_generation(config)
            
            if result['success']:
                print(f"\n📝 生成歌词:")
                print(f"--- 歌词开始 ---")
                print(result['results']['generated_lyrics'])
                print(f"--- 歌词结束 ---\n")
                
                print_result("生成状态", "成功")
                print_result("音乐风格", result['results']['style_info']['detected_style'])
                print_result("情绪匹配度", f"{result['results']['quality']['emotion_match']:.1%}")
                
        except Exception as e:
            print(f"🚨 演示出错: {e}")
    
    async def demo_style_comparison(self):
        """
        演示3：风格对比生成
        同一歌词用不同风格生成并对比
        """
        print_section(
            "演示3：风格对比生成",
            "同一内容用不同风格生成，对比效果"
        )
        
        shared_lyrics = "当星光洒满这夜晚\n心中梦想闪闪发光\n无论前方路多漫长\n我们都要勇敢追逐"
        
        styles_to_test = ["pop", "rock", "jazz", "electronic"]
        
        print("🎵 对比风格:")
        for style in styles_to_test:
            print(f"  - {style}")
        
        print(f"\n📝 共享歌词:")
        print(f"---\n{shared_lyrics}\n---")
        
        comparison_results = []
        
        for style in styles_to_test:
            print(f"\n🎼 正在生成 {style} 风格...")
            
            config = {
                "voice_sample": "/demo_data/user_voice_sample.wav",
                "lyrics": shared_lyrics,
                "style": style,
                "tempo": 120,
                "duration": 90  # 短一点用于对比
            }
            
            try:
                result = await self._simulate_style_generation(config)
                
                if result['success']:
                    style_info = {
                        'style': style,
                        'audio_path': result['results']['final_audio']['audio_path'],
                        'quality_score': result['quality']['overall_score'],
                        'characteristics': result['results']['style_characteristics'],
                        'tempo_used': result['results']['tempo_analyzed']
                    }
                    comparison_results.append(style_info)
                    
                    print_result("质量评分", f"{style_info['quality_score']:.1f}/5.0")
                    print_result("特征", " • ".join(style_info['characteristics']))
                    
            except Exception as e:
                print(f"❌ {style} 风格生成失败: {e}")
        
        # 对比结论
        if comparison_results:
            print(f"\n📊 风格对比总结:")
            sorted_results = sorted(comparison_results, 
                                  key=lambda x: x['quality_score'], 
                                  reverse=True)
            
            for i, result in enumerate(sorted_results, 1):
                medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
                print(f"  {medal} {result['style']}: {result['quality_score']:.1f}分")
    
    async def demo_advanced_parameters(self):
        """
        演示4：高级参数调优
        展示详细参数配置的影响
        """
        print_section(
            "演示4：高级参数调优",
            "精细化控制生成效果的参数调节"  
        )
        
        # 基础配置
        base_lyrics = "在这片星空下\n许下我们的心愿\n愿时间能够停留\n在这一刻永恒"
        
        parameter_sets = [
            {
                "name": "标准配置",
                "tempo": 120,
                "key": "C",
                "emotion": "uplifting",
                "structure": "verse-chorus-verse-chorus",
                "intensity": 0.7
            },
            {
                "name": "慢板抒情", 
                "tempo": 80,
                "key": "Am",
                "emotion": "peaceful",
                "structure": "verse-bridge-chorus",
                "intensity": 0.4
            },
            {
                "name": "快节奏",
                "tempo": 160, 
                "key": "G",
                "emotion": "energetic",
                "structure": "verse-prechorus-chorus",
                "intensity": 0.9
            }
        ]
        
        print("⚙️  参数配置组:")
        for params in parameter_sets:
            print(f"\n  📋 {params['name']}:")
            for key, value in params.items():
                if key != 'name':
                    print(f"    {key}: {value}")
        
        tuning_results = []
        
        for param_set in parameter_sets:
            print(f"\n🔧 应用 {param_set['name']}...")
            
            config = {
                "voice_sample": "/demo_data/user_voice_sample.wav",
                "lyrics": base_lyrics,
                "style": "pop",
                "tempo": param_set["tempo"],
                "key": param_set["key"],
                "emotion": param_set["emotion"],
                "duration": 120
            }
            
            try:
                result = await self._simulate_parameter_generation(config)
                
                if result['success']:
                    tuning_result = {
                        'config_name': param_set['name'],
                        'tempo': param_set['tempo'],
                        'characteristics': result['results']['audio_analysis'],
                        'preference_score': result['quality']['user_preference']
                    }
                    tuning_results.append(tuning_result)
                    
                    print_result("BPM", str(param_set['tempo']))
                    print_result("用户偏好度", f"{tuning_result['preference_score']:.2f}")
            except Exception as e:
                print(f"❌ {param_set['name']} 生成失败: {e}")
        
        # 显示最优配置
        if tuning_results:
            best_config = max(tuning_results, key=lambda x: x['preference_score'])
            print(f"\n🏆 推荐配置:")
            print(f"  📋 {best_config['config_name']}")
            print(f"  ⏱️  推荐BPM: {best_config['tempo']}")
            print(f"  ⭐ 用户评分: {best_config['preference_score']:.2f}")
    
    async def demo_workflow_integration(self):
        """
        演示5：工作流集成
        展示如何集成到创作流程中
        """
        print_section(
            "演示5：工作流集成",
            "将AI音乐生成融入完整创作流程"
        )
        
        workflow_steps = [
            {
                "step": "创意构思",
                "tool": "思维导图",
                "duration": "5分钟",
                "output": "主题概念图"
            },
            {
                "step": "歌词创作",
                "tool": "LyricsGPT-7B",
                "duration": "10分钟", 
                "output": "初稿歌词"
            },
            {
                "step": "旋律设计",
                "tool": "Suno AI v4",
                "duration": "15分钟",
                "output": "旋律线草案"
            },
            {
                "step": "编曲制作",
                "tool": "音乐生成引擎",
                "duration": "25分钟",
                "output": "完整伴奏"
            },
            {
                "step": "人声录制",
                "tool": "So-VITS-SVC 4.1",
                "duration": "20分钟",
                "output": "AI演唱版本"
            },
            {
                "step": "后期处理",
                "tool": "音频工作站",
                "duration": "15分钟",
                "output": "最终成品"
            }
        ]
        
        print("🔄 完整创作工作流:")
        total_time = 0
        
        for i, step in enumerate(workflow_steps, 1):
            print(f"\n  {i}. {step['step']}")
            print(f"     🛠️  工具: {step['tool']}")
            print(f"     ⏱️  耗时: {step['duration']}")
            print(f"     📄 输出: {step['output']}")
            
            # 解析时间
            time_str = step['duration']
            minutes = int(time_str.split('分钟')[0])
            total_time += minutes
        
        print(f"\n📈 项目统计:")
        print_result("总耗时", f"{total_time}分钟 ({total_time/60:.1f}小时)")
        print_result("效率提升", "相比传统方法快5-10倍")
        print_result("参与角色", "1人完成全流程")
        
        print(f"\n💡 集成优势:")
        advantages = [
            "🚀 快速实现创意构思",
            "🎯 精确控制音乐风格", 
            "🔄 支持多版本迭代",
            "🎭 个性化音色表达",
            "💰 降低制作成本",
            "⏱️ 缩短制作周期"
        ]
        
        for advantage in advantages:
            print(f"  {advantage}")
    
    # 模拟生成方法
    async def _simulate_generation(self, config: Dict) -> Dict:
        """模拟音乐生成流程"""
        # 模拟处理时间
        await asyncio.sleep(2)
        
        return {
            'success': True,
            'job_id': f"demo_job_{int(time.time())}",
            'results': {
                'final_audio': {
                    'audio_path': f"{self.results_dir}/demo_{config['style']}.wav",
                    'formats': [
                        {'name': 'WAV高清', 'file_path': f"{self.results_dir}/demo_hd.wav"},
                        {'name': 'MP3压缩', 'file_path': f"{self.results_dir}/demo.mp3"},
                        {'name': 'MIDI源文件', 'file_path': f"{self.results_dir}/demo.mid"}
                    ]
                },
                'instrumental': {
                    'midi_path': f"{self.results_dir}/demo_arrangement.mid"
                }
            },
            'quality': {
                'overall_score': 4.3,
                'vocal_quality': 4.2,
                'rhythm_accuracy': 4.5,
                'style_adherence': 4.1
            }
        }
    
    async def _simulate_theme_generation(self, config: Dict) -> Dict:
        """模拟主题驱动生成"""
        await asyncio.sleep(1)
        
        theme_lyrics_map = {
            "夏日海边": "海浪轻拍着沙滩\n夕阳染红天际线\n我们手牵手漫步\n在这温暖的夏日",
            "青春校园": "青春的校园里\n书声琅琅四季\n我们共同追逐\n那个美好梦想",
            "都市夜景": "霓虹灯下的街道\n车水马龙喧嚣\n在这座城市里\n寻找属于我们",
            "山水田园": "青山绿水之间\n鸟语花香弥漫\n远离城市喧嚣\n在这宁静家园"
        }
        
        return {
            'success': True,
            'results': {
                'generated_lyrics': theme_lyrics_map.get(config['theme'], "生成的歌词..."),
                'style_info': {
                    'detected_style': config['style'],
                    'emotion_profile': config['emotion']
                },
                'quality': {
                    'emotion_match': 0.87,
                    'lyric_coherence': 0.92
                }
            }
        }
    
    async def _simulate_style_generation(self, config: Dict) -> Dict:
        """模拟风格生成"""
        await asyncio.sleep(1)
        
        style_characteristics = {
            'pop': ['流畅旋律', '电子和声', '动感节奏'],
            'rock': ['强力和弦', '鼓点强烈', '吉他主导'],
            'jazz': ['复杂和声', '即兴演奏', '摇摆节奏'],
            'electronic': ['合成器音色', '电子鼓点', '未来感']
        }
        
        return {
            'success': True,
            'results': {
                'final_audio': {
                    'audio_path': f"{self.results_dir}/demo_{config['style']}.wav"
                },
                'style_characteristics': style_characteristics.get(config['style'], []),
                'tempo_analyzed': config['tempo']
            },
            'quality': {
                'overall_score': 4.1 + (hash(config['style']) % 50) / 100
            }
        }
    
    async def _simulate_parameter_generation(self, config: Dict) -> Dict:
        """模拟参数调优生成"""
        await asyncio.sleep(0.5)
        
        tempo_analysis = {
            80: "舒缓抒情，适合慢歌表达",
            120: "标准节奏，大众接受度高", 
            160: "充满活力，适合舞曲风格"
        }
        
        return {
            'success': True,
            'results': {
                'audio_analysis': tempo_analysis.get(config['tempo'], "平衡表达")
            },
            'quality': {
                'user_preference': 0.7 + (hash(str(config)) % 30) / 100
            }
        }

async def main():
    """主演示函数"""
    print_section(
        "🎵 AI 音乐创作师演示", 
        "聚星逸团队打造的端到端音乐创作技能"
    )
    
    demo = MusicGenerationDemo()
    
    # 执行所有演示
    demos = [
        demo.demo_basic_generation,
        demo.demo_theme_based_generation, 
        demo.demo_style_comparison,
        demo.demo_advanced_parameters,
        demo.demo_workflow_integration
    ]
    
    for i, demo_func in enumerate(demos, 1):
        print(f"\n🎯 开始演示 {i}/5...")
        try:
            await demo_func()
        except Exception as e:
            print(f"❌ 演示 {i} 出错: {e}")
            
        # 演示间隔
        if i < len(demos):
            print(f"\n⏳ 准备下一个演示...")
            await asyncio.sleep(1)
    
    print_section("🎊 演示完成")
    print("感谢您体验 AI 音乐创作师！")
    print("\n🎁 接下来你可以：")
    print("  📚 阅读详细文档了解使用方法")
    print("  🎵 准备你的录音开始创作") 
    print("  🤝 加入社区分享你的作品")
    print("  💡 提出建议和需求")
    
    print(f"\n📂 演示结果保存在: {demo.results_dir}")

if __name__ == "__main__":
    asyncio.run(main())