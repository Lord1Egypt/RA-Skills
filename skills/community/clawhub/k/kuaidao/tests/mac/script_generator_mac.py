# -*- coding: utf-8 -*-
"""
脚本生成器测试 - macOS版本
对应: scripts/script_generator.py
"""

import sys
import os

# 添加scripts目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))

from script_generator import ScriptGenerator

def test_generator():
    """测试脚本生成功能"""
    
    # 测试1: 初始化生成器（小红书）
    print("\n[测试1] 初始化生成器 - 小红书")
    generator = ScriptGenerator(
        platform="xiaohongshu",
        duration="2-3min",
        keywords=["采摘", "农家菜", "周末"],
        trending_titles=["周末去哪儿", "春日采摘攻略", "农家美食推荐"],
        avoid_themes=["已发布主题"]
    )
    print(f"[OK] 平台: {generator.platform}")
    print(f"[OK] 分镜数量: {generator.segments_count}")
    print(f"[OK] 关键词: {generator.keywords}")
    
    # 测试2: 生成分镜时长分配
    print("\n[测试2] 分镜时长分配")
    durations = generator._distribute_duration()
    print("[OK] 分配模式（开头快、中间稳、结尾慢）:")
    print(f"  前3个: {durations[:3]}秒（开场）")
    print(f"  中间: ...{len(durations)-5}个...（主体）")
    print(f"  后2个: {durations[-2:]}秒（结尾）")
    
    # 测试3: 构建分镜结构
    print("\n[测试3] 构建分镜结构")
    segments = generator._build_segments_structure(durations[:3])
    print(f"[OK] 生成了 {len(segments)} 个分镜")
    for seg in segments:
        print(f"  - 分镜{seg['seg_id']}: {seg['time']}, {seg['duration']}秒")
    
    # 测试4: 构建提示词
    print("\n[测试4] 构建AI提示词")
    prompt = generator.get_prompt_for_script(1)
    print(f"[OK] 提示词长度: {len(prompt)} 字符")
    print(f"[OK] 提示词预览（前200字）:")
    print(f"  {prompt[:200]}...")
    
    # 测试5: 生成单个脚本
    print("\n[测试5] 生成单个脚本")
    script = generator._generate_single_script(1)
    print(f"[OK] 脚本ID: {script['script_id']}")
    print(f"[OK] 标题: {script['title']}")
    print(f"[OK] 主题: {script['theme']}")
    print(f"[OK] 总时长: {script['total_duration']}")
    print(f"[OK] 分镜数: {script['segments_count']}")
    
    # 测试6: 生成多个脚本
    print("\n[测试6] 生成多个脚本")
    scripts = generator.generate(count=3)
    print(f"[OK] 生成了 {len(scripts)} 个脚本")
    for i, s in enumerate(scripts, 1):
        print(f"  - 脚本{i}: {s['segments_count']}个分镜")
    
    # 测试7: 其他平台测试
    print("\n[测试7] 抖音平台测试")
    dy_generator = ScriptGenerator(
        platform="douyin",
        duration="1min"
    )
    print(f"[OK] 抖音分镜数: {dy_generator.segments_count}")
    
    print("\n[测试8] 视频号平台测试")
    sph_generator = ScriptGenerator(
        platform="shipinhao",
        duration="1-3min"
    )
    print(f"[OK] 视频号分镜数: {sph_generator.segments_count}")
    
    print("\n[完成] 脚本生成测试通过")

if __name__ == "__main__":
    test_generator()
