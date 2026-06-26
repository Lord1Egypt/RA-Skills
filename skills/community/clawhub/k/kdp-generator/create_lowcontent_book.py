#!/usr/bin/env python3
"""
KDP低内容书籍内页生成器 - 完整版
生成日记、计划本、工作簿等内页PDF
"""

import argparse
import sys
import json
from pathlib import Path

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from kdp_book_factory import KDPBookFactory, BookConfig, BookType
from pdf_generator import generate_interior_pdf

BOOK_TYPES = {
    'guided_journal': BookType.GUIDED_JOURNAL,
    'daily_planner': BookType.DAILY_PLANNER,
    'gratitude_journal': BookType.GRATITUDE_JOURNAL,
    'workbook': BookType.WORKBOOK,
    'log_book': BookType.LOG_BOOK,
    'activity_book': BookType.ACTIVITY_BOOK,
    'notebook': BookType.NOTEBOOK,
}


def main():
    parser = argparse.ArgumentParser(
        description='生成KDP低内容书籍内页PDF',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  %(prog)s --title "My Journal" --type guided_journal --pages 108
  %(prog)s --title "Planner" --type daily_planner --size 6x9 --output ./books/
  %(prog)s --title "Gratitude Journal" --type gratitude_journal --days 90
        '''
    )
    
    parser.add_argument('--title', required=True, help='书籍标题')
    parser.add_argument('--subtitle', default='', help='副标题')
    parser.add_argument('--type', required=True, 
                       choices=list(BOOK_TYPES.keys()),
                       help='书籍类型')
    parser.add_argument('--pages', type=int, default=108,
                       help='页数（默认108）')
    parser.add_argument('--days', type=int, default=90,
                       help='天数（默认90，用于日记/计划本）')
    parser.add_argument('--size', default='6x9',
                       choices=['6x9', '8.5x11', 'A5'],
                       help='书籍尺寸（默认6x9英寸）')
    parser.add_argument('--paper', default='cream',
                       choices=['cream', 'white'],
                       help='纸张颜色（默认cream护眼纸）')
    parser.add_argument('--style', default='minimalist',
                       choices=['minimalist', 'watercolor', 'geometric', 
                               'photographic', 'illustration', '3d_render'],
                       help='封面风格（默认minimalist）')
    parser.add_argument('--output', default='./output',
                       help='输出目录（默认./output）')
    parser.add_argument('--author', default='Luna & Boss',
                       help='作者名称')
    parser.add_argument('--list-types', action='store_true',
                       help='列出所有支持的书籍类型')
    parser.add_argument('--preview-only', action='store_true',
                       help='只生成预览，不生成PDF')
    
    args = parser.parse_args()
    
    if args.list_types:
        print("支持的书籍类型：")
        for t in BOOK_TYPES:
            print(f"  - {t}")
        return
    
    # 创建输出目录
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"🚀 开始生成KDP书籍...")
    print(f"   标题: {args.title}")
    print(f"   副标题: {args.subtitle or '(无)'}")
    print(f"   类型: {args.type}")
    print(f"   页数: {args.pages}")
    print(f"   天数: {args.days}")
    print(f"   尺寸: {args.size}")
    print(f"   纸张: {args.paper}")
    print(f"   风格: {args.style}")
    print()
    
    # 初始化工厂
    factory = KDPBookFactory()
    
    # 创建书籍配置
    config = BookConfig(
        title=args.title,
        subtitle=args.subtitle,
        book_type=BOOK_TYPES[args.type],
        page_count=args.pages,
        cover_style=args.style
    )
    
    # 1. 生成书籍结构规划
    print("📋 Step 1: 生成书籍结构规划...")
    book = factory.create_book(config)
    book_id = book['id']
    book_dir = output_dir / book_id
    book_dir.mkdir(exist_ok=True)
    
    # 2. 生成内页PDF
    if not args.preview_only:
        print("\n📄 Step 2: 生成内页PDF...")
        try:
            interior_path = generate_interior_pdf(
                title=args.title,
                subtitle=args.subtitle or f"A {args.days}-Day Guided Workbook",
                book_type=args.type,
                days=args.days,
                output_dir=str(book_dir)
            )
            # 重命名为标准文件名
            final_interior = book_dir / "interior.pdf"
            Path(interior_path).rename(final_interior)
            print(f"✅ 内页PDF: {final_interior}")
        except Exception as e:
            print(f"❌ PDF生成失败: {e}")
            import traceback
            traceback.print_exc()
            return
    else:
        print("\n📄 Step 2: [预览模式] 跳过PDF生成")
    
    # 3. 保存封面提示词
    print("\n🎨 Step 3: 生成封面Prompt...")
    prompt_path = book_dir / "cover_prompt.md"
    with open(prompt_path, 'w') as f:
        f.write(f"# {args.title} - 封面Prompt\n\n")
        f.write(f"## Midjourney\n```\n{book['cover_prompt']['midjourney']}\n```\n\n")
        if 'stable_diffusion' in book['cover_prompt']:
            f.write(f"## Stable Diffusion\n```\n{book['cover_prompt']['stable_diffusion']}\n```\n")
        f.write(f"\n## 风格说明\n{book['cover_prompt']['recommendation']}\n")
    print(f"✅ 封面Prompt: {prompt_path}")
    
    # 4. 保存元数据
    print("\n🏷️  Step 4: 生成KDP元数据...")
    metadata_path = book_dir / "metadata.json"
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(book['metadata'], f, ensure_ascii=False, indent=2)
    print(f"✅ 元数据: {metadata_path}")
    
    # 5. 生成README
    print("\n📝 Step 5: 生成使用说明...")
    readme_path = book_dir / "README.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(f"# {args.title}\n\n")
        f.write(f"**副标题**: {args.subtitle or 'N/A'}\n\n")
        f.write(f"**类型**: {args.type}\n\n")
        f.write(f"**规格**: {args.size} 英寸, {args.pages}页\n\n")
        f.write(f"**纸张**: {args.paper}\n\n")
        f.write(f"---\n\n")
        f.write(f"## 文件说明\n\n")
        f.write(f"- `interior.pdf` - 内页PDF（上传到KDP）\n")
        f.write(f"- `cover_prompt.md` - AI封面绘画提示词\n")
        f.write(f"- `metadata.json` - KDP元数据（标题/关键词/分类等）\n\n")
        f.write(f"---\n\n")
        f.write(f"## KDP填写信息\n\n")
        f.write(f"| 字段 | 内容 |\n")
        f.write(f"|------|------|\n")
        f.write(f"| Title | {args.title} |\n")
        f.write(f"| Subtitle | {args.subtitle or '(无)'} |\n")
        f.write(f"| Author | {args.author} |\n")
        f.write(f"| Keywords | {', '.join(book['metadata']['keywords'][:3])}... |\n")
        f.write(f"| Price | {book['metadata']['price_recommendation']} |\n\n")
        f.write(f"---\n\n")
        f.write(f"## 下一步操作\n\n")
        f.write(f"1. 用Midjourney生成封面（参考cover_prompt.md）\n")
        f.write(f"2. 登录KDP，创建新Paperback\n")
        f.write(f"3. 上传interior.pdf作为内页\n")
        f.write(f"4. 上传封面图片\n")
        f.write(f"5. 按metadata.json填写信息\n")
        f.write(f"6. 发布！\n")
    print(f"✅ 使用说明: {readme_path}")
    
    # 完成
    print(f"\n" + "="*60)
    print(f"✅ 书籍生成完成！")
    print(f"="*60)
    print(f"\n📁 输出目录: {book_dir}")
    print(f"\n📊 书籍信息:")
    print(f"   - 标题: {args.title}")
    print(f"   - 类型: {args.type}")
    print(f"   - 页数: {args.pages}")
    print(f"   - 建议定价: {book['metadata']['price_recommendation']}")
    print(f"\n💡 提示: 查看 {readme_path} 获取详细使用说明")


if __name__ == '__main__':
    main()
