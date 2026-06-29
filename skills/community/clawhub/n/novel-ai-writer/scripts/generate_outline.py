#!/usr/bin/env python3
"""
Novel Outline Generator
小说大纲生成器 - 帮助快速生成小说大纲

用法：
    python3 generate_outline.py                    # 交互式生成
    python3 generate_outline.py --genre 都市 --theme 逆袭  # 指定参数生成
"""

import sys
import json
import os
from pathlib import Path

# 添加父目录到路径以便导入
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def load_template(name):
    """加载模板文件"""
    skill_dir = Path(__file__).parent.parent
    template_path = skill_dir / "assets" / "templates" / name
    if template_path.exists():
        return template_path.read_text(encoding='utf-8')
    return None

def generate_outline(genre=None, theme=None, target_len=None):
    """生成大纲"""
    
    # 如果没有提供参数，交互式询问
    if genre is None:
        print("\n🎭 小说大纲生成器")
        print("=" * 40)
        genre = input("📚 小说类型（都市/玄幻/科幻/悬疑/言情/历史/其他）: ").strip() or "都市"
        theme = input("💡 主题/核心冲突（逆袭/复仇/成长/爱情/冒险/其他）: ").strip() or "逆袭"
        target_len = input("📏 目标篇幅（短篇/中篇/长篇/超长篇）: ").strip() or "长篇"
    
    # 根据类型和主题生成大纲框架
    outline = f"""# {genre}小说大纲

## 基本信息
- **类型**：{genre}
- **主题**：{theme}
- **篇幅**：{target_len}

## 核心设定

### 世界观
[描述故事发生的世界/环境]

### 主要角色

**主角**：
- 姓名：[主角名字]
- 背景：[起点状态]
- 目标：[想要达成的事]
- 性格：[核心性格特点]
- 金手指/特点：[特殊能力或优势]

**配角1**：
- 姓名：
- 与主角关系：
- 作用：

**配角2**：
- 姓名：
- 与主角关系：
- 作用：

### 核心冲突
[主角面临的主要矛盾/挑战]

## 故事结构

### 第一幕（开篇）
- **激励事件**：[打破主角平静生活的事件]
- **进入新世界**：[主角开始面对挑战]
- **第一关卡**：[第一个小高潮/冲突]

### 第二幕（发展）
- **中点**：[情节转折，主角获得新信息或能力]
- **升级挑战**：[困难加剧，冲突升级]
- **配角弧线**：[配角的故事线展开]
- **第二关卡**：[主角面临重大选择]

### 第三幕（高潮）
- **最低点**：[主角遭遇最大挫折]
- **最终准备**：[积蓄力量，准备决战]
- **高潮对决**：[最终冲突]
- **结局**：[解决核心矛盾]

## 章节规划

### 第一卷：[卷名]
- 第1章：[章节名] - [核心内容]
- 第2章：[章节名] - [核心内容]
- ...

### 第二卷：[卷名]
- ...

## 伏笔与回收

| 伏笔 | 位置 | 回收位置 | 效果 |
|------|------|---------|------|
| [伏笔1] | 第X章 | 第Y章 | [描述效果] |
| [伏笔2] | 第X章 | 第Y章 | [描述效果] |

## 写作提示

1. 开篇要快：尽快进入核心冲突
2. 节奏控制：每3-5章设置一个小高潮
3. 人物塑造：让人物通过行动展现性格
4. 埋设伏笔：提前铺垫重要设定
5. 逻辑自洽：检查时间线、人物关系的一致性

---
*由 Novel AI Writer 辅助生成*
*生成时间：{__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""
    
    return outline

def main():
    # 解析命令行参数
    args = sys.argv[1:]
    
    genre = None
    theme = None
    target_len = None
    
    for i, arg in enumerate(args):
        if arg == '--genre' and i + 1 < len(args):
            genre = args[i + 1]
        elif arg == '--theme' and i + 1 < len(args):
            theme = args[i + 1]
        elif arg == '--len' and i + 1 < len(args):
            target_len = args[i + 1]
        elif arg == '--help':
            print(__doc__)
            return
        elif arg == '--output' and i + 1 < len(args):
            output_path = args[i + 1]
            outline = generate_outline(genre, theme, target_len)
            Path(output_path).write_text(outline, encoding='utf-8')
            print(f"✅ 大纲已保存到: {output_path}")
            return
    
    # 生成大纲
    outline = generate_outline(genre, theme, target_len)
    
    # 输出
    print("\n" + "=" * 40)
    print("📄 生成的大纲：")
    print("=" * 40)
    print(outline)
    
    # 询问是否保存
    save = input("\n💾 是否保存到文件？(y/n): ").strip().lower()
    if save == 'y':
        filename = input("📁 文件名（默认: outline.md）: ").strip() or "outline.md"
        Path(filename).write_text(outline, encoding='utf-8')
        print(f"✅ 已保存到: {filename}")

if __name__ == "__main__":
    main()