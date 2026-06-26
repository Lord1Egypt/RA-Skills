#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
-*--*--*--*--*--*--*--*--*--*--*-

createBy: wanghao

createTime: 2026-03-28 12:45:00

-*--*--*--*--*--*--*--*--*--*--*-

Excel工具套件 - 命令行接口
"""

import argparse
import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from openclawkit_excel import ExcelToolkit


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='Excel工具套件 - 命令行接口',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 查看帮助
  python main.py --help
  
  # 创建示例Excel文件
  python main.py demo
  
  # 检查文件是否存在
  python main.py check --file data.xlsx
  
  # 读取Excel文件
  python main.py read --file data.xlsx
  
  # 创建新Excel文件
  python main.py create --file output.xlsx --data "name,age,city"
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='子命令')
    
    # demo命令
    subparsers.add_parser('demo', help='创建示例Excel文件')
    
    # check命令
    check_parser = subparsers.add_parser('check', help='检查文件是否存在')
    check_parser.add_argument('--file', '-f', required=True, help='Excel文件路径')
    
    # read命令
    read_parser = subparsers.add_parser('read', help='读取Excel文件')
    read_parser.add_argument('--file', '-f', required=True, help='Excel文件路径')
    read_parser.add_argument('--sheet', '-s', help='工作表名称（默认第一个）')
    
    # create命令
    create_parser = subparsers.add_parser('create', help='创建新Excel文件')
    create_parser.add_argument('--file', '-f', required=True, help='输出文件路径')
    create_parser.add_argument('--data', '-d', help='数据（CSV格式）')
    
    # clean命令
    clean_parser = subparsers.add_parser('clean', help='数据清洗')
    clean_parser.add_argument('--input', '-i', required=True, help='输入文件路径')
    clean_parser.add_argument('--output', '-o', required=True, help='输出文件路径')
    
    # merge命令
    merge_parser = subparsers.add_parser('merge', help='合并多个Excel文件')
    merge_parser.add_argument('--files', '-f', required=True, help='文件列表（逗号分隔）')
    merge_parser.add_argument('--output', '-o', required=True, help='输出文件路径')
    
    return parser.parse_args()


def run_demo():
    """运行示例"""
    print("🎯 Excel工具套件示例")
    print("=" * 50)
    
    excel = ExcelToolkit(debug=True)
    
    # 创建示例数据
    data = {
        '姓名': ['张三', '李四', '王五', '赵六', '钱七'],
        '年龄': [25, 30, 35, 28, 32],
        '部门': ['技术部', '市场部', '销售部', '技术部', '市场部'],
        '工资': [8000, 9000, 8500, 9500, 8800],
        '入职日期': ['2023-01-15', '2022-08-20', '2021-05-10', '2023-03-01', '2022-11-15']
    }
    
    # 创建Excel文件
    output_file = '示例员工数据.xlsx'
    print(f"📝 创建示例Excel文件: {output_file}")
    excel.create_excel(output_file, data)
    
    # 读取文件
    print(f"📖 读取Excel文件: {output_file}")
    df = excel.read_excel(output_file)
    print(f"数据形状: {df.shape}")
    print(f"列名: {list(df.columns)}")
    
    # 显示前几行数据
    print("\n📊 数据预览:")
    print(df.head())
    
    # 数据清洗示例
    print("\n🧹 数据清洗示例:")
    cleaned_df = excel.clean_data(df)
    print(f"清洗后数据形状: {cleaned_df.shape}")
    
    # 保存清洗后的数据
    clean_file = '清洗后员工数据.xlsx'
    excel.write_excel(clean_file, cleaned_df)
    print(f"✅ 清洗后数据已保存: {clean_file}")
    
    print("\n🎉 示例完成！")
    print(f"生成的文件:")
    print(f"  - {output_file}")
    print(f"  - {clean_file}")


def run_check(args):
    """检查文件是否存在"""
    excel = ExcelToolkit()
    if excel.file_exists(args.file):
        print(f"✅ 文件存在: {args.file}")
        
        # 获取文件信息
        try:
            import os
            stat_info = os.stat(args.file)
            size_mb = stat_info.st_size / (1024 * 1024)
            print(f"📏 文件大小: {size_mb:.2f} MB")
            print(f"📅 修改时间: {os.path.getmtime(args.file)}")
        except:
            pass
    else:
        print(f"❌ 文件不存在: {args.file}")


def run_read(args):
    """读取Excel文件"""
    excel = ExcelToolkit()
    
    if not excel.file_exists(args.file):
        print(f"❌ 文件不存在: {args.file}")
        return
    
    try:
        df = excel.read_excel(args.file, sheet_name=args.sheet)
        print(f"✅ 成功读取文件: {args.file}")
        print(f"📊 数据形状: {df.shape} (行 x 列)")
        print(f"📋 列名: {list(df.columns)}")
        
        print("\n📄 数据预览 (前5行):")
        print(df.head())
        
        print("\n📈 数据统计:")
        print(df.describe())
        
    except Exception as e:
        print(f"❌ 读取文件出错: {e}")


def run_create(args):
    """创建新Excel文件"""
    excel = ExcelToolkit(debug=True)
    
    # 解析数据
    data = {}
    if args.data:
        # 简单的CSV格式解析
        lines = args.data.split(';')
        for line in lines:
            if ':' in line:
                key, values = line.split(':', 1)
                data[key.strip()] = [v.strip() for v in values.split(',')]
    
    if not data:
        # 使用默认数据
        data = {
            'ID': [1, 2, 3, 4, 5],
            '名称': ['项目A', '项目B', '项目C', '项目D', '项目E'],
            '状态': ['进行中', '已完成', '待开始', '进行中', '已取消']
        }
    
    print(f"📝 创建Excel文件: {args.file}")
    print(f"📊 数据内容: {data}")
    
    try:
        excel.create_excel(args.file, data)
        print(f"✅ 文件创建成功: {args.file}")
    except Exception as e:
        print(f"❌ 创建文件出错: {e}")


def run_clean(args):
    """数据清洗"""
    excel = ExcelToolkit(debug=True)
    
    if not excel.file_exists(args.input):
        print(f"❌ 输入文件不存在: {args.input}")
        return
    
    print(f"🧹 数据清洗")
    print(f"输入文件: {args.input}")
    print(f"输出文件: {args.output}")
    
    try:
        # 读取数据
        df = excel.read_excel(args.input)
        print(f"原始数据形状: {df.shape}")
        
        # 数据清洗
        cleaned_df = excel.clean_data(df)
        print(f"清洗后数据形状: {cleaned_df.shape}")
        
        # 保存清洗后的数据
        excel.write_excel(args.output, cleaned_df)
        print(f"✅ 数据清洗完成，已保存到: {args.output}")
        
    except Exception as e:
        print(f"❌ 数据清洗出错: {e}")


def run_merge(args):
    """合并多个Excel文件"""
    excel = ExcelToolkit(debug=True)
    
    files = [f.strip() for f in args.files.split(',')]
    
    # 检查所有文件是否存在
    missing_files = []
    for file in files:
        if not excel.file_exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ 以下文件不存在:")
        for file in missing_files:
            print(f"  - {file}")
        return
    
    print(f"🔗 合并Excel文件")
    print(f"输入文件: {files}")
    print(f"输出文件: {args.output}")
    
    try:
        # 合并文件
        merged_df = excel.merge_files(files)
        print(f"合并后数据形状: {merged_df.shape}")
        
        # 保存合并后的数据
        excel.write_excel(args.output, merged_df)
        print(f"✅ 文件合并完成，已保存到: {args.output}")
        
    except Exception as e:
        print(f"❌ 文件合并出错: {e}")


def main():
    """主函数"""
    args = parse_arguments()
    
    if not args.command:
        print("❌ 请指定一个子命令")
        print("使用 --help 查看可用命令")
        sys.exit(1)
    
    # 执行对应的命令
    if args.command == 'demo':
        run_demo()
    elif args.command == 'check':
        run_check(args)
    elif args.command == 'read':
        run_read(args)
    elif args.command == 'create':
        run_create(args)
    elif args.command == 'clean':
        run_clean(args)
    elif args.command == 'merge':
        run_merge(args)
    else:
        print(f"❌ 未知命令: {args.command}")
        sys.exit(1)


if __name__ == '__main__':
    main()