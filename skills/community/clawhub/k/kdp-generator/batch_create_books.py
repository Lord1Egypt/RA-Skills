#!/usr/bin/env python3
"""
KDP低内容书籍批量生成器
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from kdp_book_factory import KDPBookFactory, BookConfig, BookType

BOOK_TYPES = {
    'guided_journal': BookType.GUIDED_JOURNAL,
    'daily_planner': BookType.DAILY_PLANNER,
    'gratitude_journal': BookType.GRATITUDE_JOURNAL,
    'workbook': BookType.WORKBOOK,
    'log_book': BookType.LOG_BOOK,
    'activity_book': BookType.ACTIVITY_BOOK,
    'notebook': BookType.NOTEBOOK,
}


def load_config(config_path):
    """加载批量配置文件"""
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(
        description='批量生成KDP低内容书籍',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  %(prog)s --config batch_config.json
  %(prog)s --books "[{title:'Book1',type:'guided_journal',pages:108}]"
        '''
    )
    
    parser.add_argument('--config', '-c', help='批量配置文件路径')
    parser.add_argument('--books', '-b', help='JSON格式的书籍配置列表')
    parser.add_argument('--output', '-o', default='./production',
                       help='输出目录（默认./production）')
    
    args = parser.parse_args()
    
    if not args.config and not args.books:
        parser.print_help()
        print("\n错误: 必须提供 --config 或 --books 参数")
        sys.exit(1)
    
    # 加载配置
    if args.config:
        config = load_config(args.config)
        books_config = config.get('books', [])
        output_dir = Path(config.get('output_dir', args.output))
    else:
        books_config = json.loads(args.books)
        output_dir = Path(args.output)
    
    # 创建输出目录
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 初始化工厂
    factory = KDPBookFactory()
    
    # 转换配置
    configs = []
    for book_data in books_config:
        book_type = BOOK_TYPES.get(book_data['type'], BookType.GUIDED_JOURNAL)
        config = BookConfig(
            title=book_data['title'],
            subtitle=book_data.get('subtitle', ''),
            book_type=book_type,
            page_count=book_data.get('pages', 108),
            cover_style=book_data.get('style', 'minimalist')
        )
        configs.append(config)
    
    print(f"准备批量生成 {len(configs)} 本书籍...\n")
    
    # 批量生成
    results = factory.batch_create(configs)
    
    # 保存所有结果
    for book in results:
        book_id = book['id']
        book_dir = output_dir / book_id
        book_dir.mkdir(exist_ok=True)
        
        # 保存内页
        if 'interior' in book and book['interior']:
            with open(book_dir / f"{book_id}_interior.pdf", 'wb') as f:
                f.write(book['interior'])
        
        # 保存Prompt
        if 'cover_prompt' in book:
            with open(book_dir / f"{book_id}_cover_prompt.md", 'w') as f:
                f.write(f"# {book['title']} - 封面Prompt\n\n")
                f.write(f"## Midjourney\n```\n{book['cover_prompt']['midjourney']}\n```\n")
        
        # 保存元数据
        if 'metadata' in book:
            with open(book_dir / f"{book_id}_metadata.json", 'w', encoding='utf-8') as f:
                json.dump(book['metadata'], f, ensure_ascii=False, indent=2)
    
    # 导出生产清单
    list_path = output_dir / 'production_list.md'
    factory.export_production_list(str(list_path))
    
    print(f"\n✅ 批量生成完成！")
    print(f"生成书籍: {len(results)} 本")
    print(f"输出目录: {output_dir}")
    print(f"生产清单: {list_path}")


if __name__ == '__main__':
    main()
