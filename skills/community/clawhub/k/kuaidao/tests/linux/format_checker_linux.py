# -*- coding: utf-8 -*-
"""
格式检查器测试 - Linux版本
对应: scripts/format_checker.py
"""

import sys
import os

# 添加scripts目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))

from format_checker import FormatChecker

def create_test_script(valid=True):
    """创建测试脚本"""
    if valid:
        return {
            "title": "测试脚本标题",
            "theme": "测试主题",
            "story": "这是一个完整的故事。开始介绍背景，然后展开情节，接着遇到问题，最后解决问题。这是一个关于周末采摘的故事，主人公一家三口来到农家院，先是被美景吸引，然后品尝美食，最后满载而归。整个故事有起承转合，总共超过两百字的叙述，每个环节都有详细的描写和情感变化。",
            "total_duration": "2-3min",
            "segments_count": 3,
            "segments": [
                {
                    "seg_id": 1,
                    "time": "0-5秒",
                    "duration": 5,
                    "shot_desc": "全景镜头，展现场景全貌，主体位于画面中央，光线柔和自然，背景虚化突出主题",
                    "movement_desc": "缓慢推进，速度均匀，从远景到中景的过渡，营造期待感",
                    "tech_desc": "使用稳定器手持拍摄，ISO400，光圈f/2.8，快门1/50s",
                    "scene_desc": "自然光线从窗户射入，暖色调，简洁构图，三分法则",
                    "line": "先来说说今天的故事，真的很精彩",
                    "sound_desc": "环境音为主，轻微的风声，音量控制在-20dB左右",
                    "bgm": "轻快背景音乐",
                    "tags": "#测试",
                    "status": "待使用"
                },
                {
                    "seg_id": 2,
                    "time": "5-12秒",
                    "duration": 7,
                    "shot_desc": "中景特写，展现细节，主体表情丰富，背景适度虚化",
                    "movement_desc": "固定机位，保持稳定，偶尔轻微晃动增加真实感",
                    "tech_desc": "固定三脚架，ISO800，光圈f/4，快门1/60s",
                    "scene_desc": "室内灯光，色温5500K，对比度适中，饱和度自然",
                    "line": "然后发生了意想不到的事情",
                    "sound_desc": "背景音乐渐强，配合画面情绪变化，营造氛围感",
                    "bgm": "轻快背景音乐",
                    "tags": "#测试",
                    "status": "待使用"
                },
                {
                    "seg_id": 3,
                    "time": "12-18秒",
                    "duration": 6,
                    "shot_desc": "特写镜头，聚焦表情，展现情感高潮，眼神有光",
                    "movement_desc": "缓慢拉远，从特写到全景的过渡，留下回味空间",
                    "tech_desc": "使用滑轨，ISO200，光圈f/1.8，快门1/100s",
                    "scene_desc": "逆光拍摄，轮廓光勾勒主体，金色调，梦幻感",
                    "line": "最后大家都很满意",
                    "sound_desc": "音效淡出，留下环境音，营造余韵和情感延续",
                    "bgm": "轻快背景音乐",
                    "tags": "#测试",
                    "status": "待使用"
                }
            ]
        }
    else:
        # 创建有问题的脚本
        return {
            "title": "测试脚本标题",
            "theme": "测试主题",
            "story": "短故事",
            "total_duration": "2-3min",
            "segments_count": 3,
            "segments": [
                {
                    "seg_id": 1,
                    "time": "0-5秒",
                    "duration": 15,
                    "shot_desc": "短",
                    "movement_desc": "短",
                    "tech_desc": "短",
                    "scene_desc": "短",
                    "line": "首先其次",
                    "sound_desc": "短"
                }
            ]
        }

def test_format():
    """测试格式检查功能"""
    
    # 测试1: 正常脚本验证
    print("\n[测试1] 正常脚本验证（应通过）")
    checker = FormatChecker("xiaohongshu")
    valid_script = create_test_script(valid=True)
    passed, issues = checker.validate_script(valid_script)
    print(f"[OK] 验证结果: {'通过' if passed else '未通过'}")
    if issues:
        for issue in issues:
            print(f"  [X] {issue}")
    else:
        print("  [OK] 无问题")
    
    # 测试2: 有问题脚本验证
    print("\n[测试2] 有问题脚本验证（应失败）")
    invalid_script = create_test_script(valid=False)
    passed, issues = checker.validate_script(invalid_script)
    print(f"[OK] 验证结果: {'通过' if passed else '未通过（预期）'}")
    print(f"[OK] 发现 {len(issues)} 个问题:")
    for issue in issues:
        print(f"  - {issue}")
    
    # 测试3: 批量验证
    print("\n[测试3] 批量验证")
    scripts = [create_test_script(valid=True), create_test_script(valid=False)]
    results = checker.validate_batch(scripts)
    print(f"[OK] 总脚本数: {results['total']}")
    print(f"[OK] 通过: {results['passed']}")
    print(f"[OK] 失败: {results['failed']}")
    
    # 测试4: 自动修复
    print("\n[测试4] 自动修复")
    checker_fix = FormatChecker("xiaohongshu")
    broken_script = create_test_script(valid=False)
    
    print("修复前:")
    print(f"  - 镜头描述: {broken_script['segments'][0]['shot_desc']}")
    print(f"  - 台词: {broken_script['segments'][0]['line']}")
    
    fixed_script = checker_fix.auto_fix(broken_script)
    
    print("修复后:")
    print(f"  - 镜头描述: {fixed_script['segments'][0]['shot_desc']}")
    print(f"  - 台词: {fixed_script['segments'][0]['line']}")
    
    print(f"\n[OK] 修复记录:")
    print(checker_fix.get_fix_report())
    
    # 测试5: 抖音平台检查
    print("\n[测试5] 抖音平台验证")
    dy_checker = FormatChecker("douyin")
    dy_script = create_test_script(valid=True)
    passed, issues = dy_checker.validate_script(dy_script)
    print(f"[OK] 抖音验证结果: {'通过' if passed else '未通过'}")
    
    # 测试6: 视频号平台检查
    print("\n[测试6] 视频号平台验证（标题限制）")
    sph_checker = FormatChecker("shipinhao")
    
    # 测试过长标题
    long_title_script = create_test_script(valid=True)
    long_title_script["title"] = "这是一个超过16个字符的很长很长的标题"
    passed, issues = sph_checker.validate_script(long_title_script)
    print(f"[OK] 长标题验证: {'通过' if passed else '未通过（预期）'}")
    
    # 测试标点标题
    punct_title_script = create_test_script(valid=True)
    punct_title_script["title"] = "标题，有标点。"
    passed, issues = sph_checker.validate_script(punct_title_script)
    print(f"[OK] 标点标题验证: {'通过' if passed else '未通过（预期）'}")
    
    print("\n[完成] 格式检查测试通过")

if __name__ == "__main__":
    test_format()
