#!/usr/bin/env python3
"""
大纲完整性验证工具
用法：python3 validate_outline.py <outline.md>
"""

import sys
from pathlib import Path
import re

def check_basic_info(outline):
    """检查基本信息是否完整"""
    print("🔍 检查基本信息...")
    required_fields = ['小说类型', '核心主题', '目标读者', '预计篇幅']
    missing = []
    for field in required_fields:
        if field not in outline:
            missing.append(field)
    
    if missing:
        print(f"  ⚠️  缺少字段：{', '.join(missing)}")
        return False
    else:
        print("  ✅ 基本信息完整")
        return True

def check_structure(outline):
    """检查故事结构是否完整"""
    print("🔍 检查故事结构...")
    
    # 检查三幕式结构
    act_keywords = ['第一幕', '第二幕', '第三幕']
    acts_found = [kw for kw in act_keywords if kw in outline]
    
    if len(acts_found) == 3:
        print("  ✅ 三幕式结构完整")
        return True
    elif len(acts_found) > 0:
        print(f"  ⚠️  结构不完整，只找到：{', '.join(acts_found)}")
        return False
    else:
        print("  ⚠️  未识别到标准结构（三幕式/英雄之旅等）")
        print("     建议：添加明确的章节结构划分")
        return False

def check_chapter_outline(outline):
    """检查章节大纲是否完整"""
    print("🔍 检查章节大纲...")
    
    # 查找章节标题
    chapter_pattern = r'第[一二三四五六七八九十\d]+章'
    chapters = re.findall(chapter_pattern, outline)
    
    if not chapters:
        print("  ⚠️  未找到章节大纲")
        print("     建议：添加分章大纲，至少包含主要情节点")
        return False
    
    print(f"  ✅ 找到 {len(chapters)} 个章节引用")
    
    # 检查关键情节点
    key_points = ['激励事件', '中点', '灵魂黑夜', '高潮']
    found_points = [kp for kp in key_points if kp in outline]
    
    if len(found_points) == len(key_points):
        print("  ✅ 关键情节点完整")
        return True
    else:
        missing = set(key_points) - set(found_points)
        print(f"  ⚠️  缺少关键情节点：{', '.join(missing)}")
        return False

def check_character_arc(outline):
    """检查人物成长弧是否设计"""
    print("🔍 检查人物成长弧...")
    
    arc_keywords = ['成长', '变化', '转变', '弧', '缺陷', '弱点']
    found = [kw for kw in arc_keywords if kw in outline]
    
    if len(found) >= 2:
        print(f"  ✅ 检测到人物成长相关描述（{len(found)}处）")
        return True
    else:
        print("  ⚠️  未检测到明确的人物成长弧设计")
        print("     建议：添加人物从XX到XX的变化过程")
        return False

def check_foreshadowing(outline):
    """检查伏笔和回收计划"""
    print("🔍 检查伏笔设计...")
    
    if '伏笔' in outline or '回收' in outline:
        print("  ✅ 检测到伏笔/回收计划")
        return True
    else:
        print("  ⚠️  未检测到伏笔和回收计划")
        print("     建议：添加伏笔列表和回收计划")
        return False

def main():
    if len(sys.argv) != 2:
        print("用法：python3 validate_outline.py <outline.md>")
        print("\n示例：")
        print("  python3 validate_outline.py my-outline.md")
        sys.exit(1)
    
    outline_file = Path(sys.argv[1])
    if not outline_file.exists():
        print(f"❌ 文件不存在：{outline_file}")
        sys.exit(1)
    
    print(f"📂 读取大纲文件：{outline_file}\n")
    with open(outline_file, 'r', encoding='utf-8') as f:
        outline = f.read()
    
    print("=" * 50)
    print("开始大纲完整性验证...")
    print("=" * 50 + "\n")
    
    # 执行检查
    results = []
    results.append(("基本信息", check_basic_info(outline)))
    results.append(("故事结构", check_structure(outline)))
    results.append(("章节大纲", check_chapter_outline(outline)))
    results.append(("人物成长弧", check_character_arc(outline)))
    results.append(("伏笔设计", check_foreshadowing(outline)))
    print()
    
    # 输出总结
    print("=" * 50)
    print("验证结果总结")
    print("=" * 50)
    
    passed = sum(1 for _, v in results if v)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通过" if result else "⚠️  需改进"
        print(f"  {name}：{status}")
    
    print(f"\n总体评分：{passed}/{total} 项通过")
    
    if passed == total:
        print("\n🎉 大纲完整性良好！可以开始创作了。")
    else:
        print(f"\n💡 建议改进 {total - passed} 处后再开始创作。")
    
    print("\n⚠️  注意：此为辅助工具，最终判断需要人工完成")

if __name__ == '__main__':
    main()
