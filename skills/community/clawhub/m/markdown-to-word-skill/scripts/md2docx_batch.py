#!/usr/bin/env python3
"""
批量Markdown转Word转换器
"""

import argparse
import os
import sys
import json
import time
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

# 导入主转换器
from md2docx import convert_markdown_to_docx


class BatchConverter:
    """批量转换器"""
    
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.report = {
            'start_time': None,
            'end_time': None,
            'total_files': 0,
            'successful': 0,
            'failed': 0,
            'files': []
        }
    
    def convert_directory(self, input_dir: str, output_dir: str, 
                         template: Optional[str] = None,
                         image_dir: Optional[str] = None,
                         recursive: bool = False,
                         skip_existing: bool = False) -> Dict[str, Any]:
        """
        转换目录中的所有Markdown文件
        
        Args:
            input_dir: 输入目录
            output_dir: 输出目录
            template: 模板文件路径
            image_dir: 图片目录路径
            recursive: 是否递归处理子目录
            skip_existing: 是否跳过已存在的输出文件
            
        Returns:
            Dict: 转换报告
        """
        self.report['start_time'] = datetime.now().isoformat()
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 查找Markdown文件
        markdown_files = self._find_markdown_files(input_dir, recursive)
        self.report['total_files'] = len(markdown_files)
        
        print(f"📁 找到 {len(markdown_files)} 个Markdown文件")
        
        # 转换每个文件
        for i, input_file in enumerate(markdown_files, 1):
            print(f"\n[{i}/{len(markdown_files)}] 处理: {input_file}")
            
            # 确定输出文件路径
            output_file = self._get_output_path(input_file, input_dir, output_dir)
            
            # 检查是否跳过已存在的文件
            if skip_existing and os.path.exists(output_file):
                print(f"  ⏭️  跳过已存在的文件: {output_file}")
                self.report['files'].append({
                    'input': input_file,
                    'output': output_file,
                    'status': 'skipped',
                    'reason': '文件已存在'
                })
                self.report['successful'] += 1
                continue
            
            # 执行转换
            start_time = time.time()
            success = convert_markdown_to_docx(
                input_file=input_file,
                output_file=output_file,
                template=template,
                image_dir=image_dir,
                debug=self.debug
            )
            elapsed_time = time.time() - start_time
            
            # 记录结果
            file_result = {
                'input': input_file,
                'output': output_file,
                'status': 'success' if success else 'failed',
                'elapsed_time': round(elapsed_time, 2)
            }
            
            if success:
                self.report['successful'] += 1
                print(f"  ✅ 转换成功 ({elapsed_time:.2f}秒)")
            else:
                self.report['failed'] += 1
                file_result['reason'] = '转换失败'
                print(f"  ❌ 转换失败")
            
            self.report['files'].append(file_result)
        
        self.report['end_time'] = datetime.now().isoformat()
        
        return self.report
    
    def _find_markdown_files(self, directory: str, recursive: bool = False) -> List[str]:
        """查找Markdown文件"""
        markdown_extensions = ['.md', '.markdown', '.mdown', '.mkd', '.mkdn']
        files = []
        
        if recursive:
            # 递归查找
            for root, _, filenames in os.walk(directory):
                for filename in filenames:
                    if any(filename.lower().endswith(ext) for ext in markdown_extensions):
                        files.append(os.path.join(root, filename))
        else:
            # 仅当前目录
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                if os.path.isfile(filepath):
                    if any(filename.lower().endswith(ext) for ext in markdown_extensions):
                        files.append(filepath)
        
        # 按文件名排序
        files.sort()
        
        return files
    
    def _get_output_path(self, input_file: str, input_dir: str, output_dir: str) -> str:
        """获取输出文件路径"""
        # 获取相对路径
        if input_dir:
            rel_path = os.path.relpath(input_file, input_dir)
        else:
            rel_path = os.path.basename(input_file)
        
        # 更改扩展名为 .docx
        base_name = os.path.splitext(rel_path)[0]
        output_file = os.path.join(output_dir, f"{base_name}.docx")
        
        # 确保目录存在
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        return output_file
    
    def save_report(self, report_path: str):
        """保存转换报告"""
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(self.report, f, ensure_ascii=False, indent=2)
            print(f"📊 报告已保存: {report_path}")
        except Exception as e:
            print(f"❌ 保存报告失败: {e}")
    
    def print_summary(self):
        """打印转换摘要"""
        print("\n" + "="*60)
        print("📈 转换摘要")
        print("="*60)
        
        total = self.report['total_files']
        successful = self.report['successful']
        failed = self.report['failed']
        
        print(f"总文件数: {total}")
        print(f"成功: {successful} ({successful/total*100:.1f}%)")
        print(f"失败: {failed} ({failed/total*100:.1f}%)")
        
        if 'start_time' in self.report and 'end_time' in self.report:
            start = datetime.fromisoformat(self.report['start_time'])
            end = datetime.fromisoformat(self.report['end_time'])
            duration = (end - start).total_seconds()
            print(f"总耗时: {duration:.2f}秒")
        
        # 显示失败的文件
        if failed > 0:
            print("\n❌ 失败的文件:")
            for file_info in self.report['files']:
                if file_info['status'] == 'failed':
                    print(f"  - {file_info['input']}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='批量Markdown转Word转换器')
    parser.add_argument('--input-dir', '-i', required=True, help='输入目录路径')
    parser.add_argument('--output-dir', '-o', required=True, help='输出目录路径')
    parser.add_argument('--template', '-t', help='Word模板文件路径')
    parser.add_argument('--image-dir', '-d', help='图片目录路径')
    parser.add_argument('--recursive', '-r', action='store_true', help='递归处理子目录')
    parser.add_argument('--skip-existing', '-s', action='store_true', help='跳过已存在的输出文件')
    parser.add_argument('--report', help='保存转换报告到JSON文件')
    parser.add_argument('--debug', action='store_true', help='启用调试模式')
    
    args = parser.parse_args()
    
    # 检查输入目录
    if not os.path.exists(args.input_dir):
        print(f"❌ 输入目录不存在: {args.input_dir}")
        sys.exit(1)
    
    # 创建批量转换器
    converter = BatchConverter(debug=args.debug)
    
    # 执行批量转换
    report = converter.convert_directory(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        template=args.template,
        image_dir=args.image_dir,
        recursive=args.recursive,
        skip_existing=args.skip_existing
    )
    
    # 打印摘要
    converter.print_summary()
    
    # 保存报告
    if args.report:
        converter.save_report(args.report)
    
    # 根据结果退出
    if report['failed'] > 0:
        print(f"\n⚠️  有 {report['failed']} 个文件转换失败")
        sys.exit(1)
    else:
        print(f"\n✅ 所有文件转换成功！")
        sys.exit(0)


if __name__ == '__main__':
    main()