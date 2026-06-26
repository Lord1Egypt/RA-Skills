#!/usr/bin/env python3
"""
批量提取多个Kettle作业中的SQL脚本
支持.kjb和.ktr文件，可以按目录或文件列表批量处理
"""

import os
import sys
import re
import json
import yaml
from pathlib import Path
from typing import List, Dict, Optional, Set
from datetime import datetime
import logging
import shutil

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BatchKettleSQLExtractor:
    """批量Kettle SQL提取器"""
    
    def __init__(self, output_base_dir: str = "batch_kettle_analysis"):
        self.output_base_dir = Path(output_base_dir)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.batch_output_dir = self.output_base_dir / f"batch_{self.timestamp}"
        self.batch_summary = {
            'batch_id': self.timestamp,
            'start_time': datetime.now().isoformat(),
            'total_files': 0,
            'processed_files': 0,
            'success_files': 0,
            'failed_files': [],
            'total_sql_components': 0,
            'file_summaries': [],
            'unique_tables': set(),
            'unique_keywords': set(),
            'sql_statistics': {
                'total_sql_length': 0,
                'avg_sql_length': 0,
                'max_sql_length': 0,
                'min_sql_length': float('inf'),
            }
        }
    
    def extract_kettle_sql_complete(self, file_path: str) -> List[Dict]:
        """从单个Kettle文件中完全提取所有SQL，解决截断问题"""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # 尝试其他编码
            try:
                with open(file_path, 'r', encoding='gbk') as f:
                    content = f.read()
            except:
                with open(file_path, 'r', encoding='latin-1') as f:
                    content = f.read()
        
        # 修复1: 先替换XML特殊字符（常见问题来源）
        content = content.replace('&lt;', '<').replace('&gt;', '>')
        content = content.replace('&amp;', '&').replace('&quot;', '"').replace('&apos;', "'")
        
        # 修复2: 使用正则表达式提取完整<entry>标签
        entries = re.findall(r'<entry>[\s\S]*?</entry>', content)
        
        sql_components = []
        
        for i, entry in enumerate(entries, 1):
            # 修复3: 使用非贪婪匹配提取步骤名称
            name_match = re.search(r'<name>([^<]+)</name>', entry)
            step_name = name_match.group(1).strip() if name_match else f"步骤_{i}"
            
            # 修复4: 使用[\s\S]确保匹配完整的SQL内容
            sql_match = re.search(r'<sql>([\s\S]*?)</sql>', entry)
            if sql_match:
                sql_content = sql_match.group(1).strip()
                
                # 修复5: 清理CDATA标记
                sql_content = re.sub(r'<!\[CDATA\[|\]\]>', '', sql_content)
                
                # 修复6: 处理可能的XML注释
                sql_content = re.sub(r'<!--.*?-->', '', sql_content, flags=re.DOTALL)
                
                sql_content = sql_content.strip()
                
                if sql_content:
                    sql_components.append({
                        'step': step_name,
                        'sql': sql_content,
                        'length': len(sql_content),
                        'component_index': i
                    })
        
        return sql_components
    
    def analyze_sql_content(self, sql_content: str) -> Dict:
        """分析SQL内容，提取关键信息"""
        analysis = {
            'tables': [],
            'columns_mentioned': [],
            'joins': [],
            'filters': [],
            'operations': [],
            'has_cte': False,
            'has_window': False,
            'has_subquery': False,
            'create_table': False,
            'insert_into': False,
            'update': False,
            'delete': False,
            'select': False,
            'key_keywords': [],
        }
        
        sql_upper = sql_content.upper()
        
        # 提取表名
        table_patterns = [
            r'FROM\s+([\w\.]+)',  # FROM table
            r'JOIN\s+([\w\.]+)',  # JOIN table
            r'INTO\s+([\w\.]+)',  # INSERT INTO table
            r'UPDATE\s+([\w\.]+)',  # UPDATE table
            r'CREATE\s+TABLE\s+([\w\.]+)',  # CREATE TABLE
            r'DROP\s+TABLE\s+([\w\.]+)',  # DROP TABLE
        ]
        
        for pattern in table_patterns:
            matches = re.findall(pattern, sql_upper)
            analysis['tables'].extend(matches)
        
        # 检查操作类型
        if 'CREATE TABLE' in sql_upper:
            analysis['create_table'] = True
        if 'INSERT INTO' in sql_upper:
            analysis['insert_into'] = True
        if 'UPDATE ' in sql_upper:
            analysis['update'] = True
        if 'DELETE FROM' in sql_upper:
            analysis['delete'] = True
        if 'SELECT ' in sql_upper:
            analysis['select'] = True
        
        # 检查CTE
        if re.search(r'WITH\s+\w+\s+AS', sql_upper):
            analysis['has_cte'] = True
        
        # 检查窗口函数
        if re.search(r'OVER\s*\(', sql_upper):
            analysis['has_window'] = True
        
        # 检查子查询
        if re.search(r'SELECT\s+.+?\s+FROM\s*\(', sql_upper, re.IGNORECASE):
            analysis['has_subquery'] = True
        
        # 提取关键关键字
        keywords = ['NVL', 'COALESCE', 'CASE', 'WHEN', 'SUM', 'COUNT', 'AVG', 'MAX', 'MIN', 
                   'GROUP BY', 'ORDER BY', 'WHERE', 'HAVING', 'DISTINCT', 'UNION']
        for keyword in keywords:
            if keyword in sql_upper:
                analysis['key_keywords'].append(keyword)
        
        # 去重
        analysis['tables'] = list(set(analysis['tables']))
        analysis['key_keywords'] = list(set(analysis['key_keywords']))
        
        return analysis
    
    def process_single_file(self, kettle_file: Path) -> Dict:
        """处理单个Kettle文件"""
        file_info = {
            'file_path': str(kettle_file),
            'file_name': kettle_file.name,
            'file_size': kettle_file.stat().st_size,
            'file_type': kettle_file.suffix,
            'sql_components': [],
            'analysis': {},
            'status': 'pending',
            'error': None,
        }
        
        try:
            logger.info(f"📄 开始处理: {kettle_file.name}")
            
            # 提取SQL
            sql_components = self.extract_kettle_sql_complete(str(kettle_file))
            file_info['sql_components'] = sql_components
            
            # 分析每个SQL组件
            sql_analyses = []
            for sql_comp in sql_components:
                analysis = self.analyze_sql_content(sql_comp['sql'])
                sql_analyses.append(analysis)
                
                # 更新批处理统计
                self.batch_summary['total_sql_components'] += 1
                self.batch_summary['sql_statistics']['total_sql_length'] += sql_comp['length']
                self.batch_summary['sql_statistics']['max_sql_length'] = max(
                    self.batch_summary['sql_statistics']['max_sql_length'], sql_comp['length']
                )
                self.batch_summary['sql_statistics']['min_sql_length'] = min(
                    self.batch_summary['sql_statistics']['min_sql_length'], sql_comp['length']
                )
                
                # 收集唯一表名和关键字
                self.batch_summary['unique_tables'].update(analysis['tables'])
                self.batch_summary['unique_keywords'].update(analysis['key_keywords'])
            
            file_info['analysis'] = {
                'sql_count': len(sql_components),
                'sql_analyses': sql_analyses,
                'has_create_table': any(a['create_table'] for a in sql_analyses),
                'has_insert_into': any(a['insert_into'] for a in sql_analyses),
                'has_complex_query': any(a['has_cte'] or a['has_window'] or a['has_subquery'] for a in sql_analyses),
            }
            
            file_info['status'] = 'success'
            self.batch_summary['success_files'] += 1
            
            logger.info(f"✅ 完成处理: {kettle_file.name} ({len(sql_components)}个SQL组件)")
            
        except Exception as e:
            file_info['status'] = 'failed'
            file_info['error'] = str(e)
            self.batch_summary['failed_files'].append({
                'file': str(kettle_file),
                'error': str(e)
            })
            logger.error(f"❌ 处理失败: {kettle_file.name} - {e}")
        
        return file_info
    
    def save_file_results(self, file_info: Dict, output_subdir: Path):
        """保存单个文件的处理结果"""
        file_name = Path(file_info['file_path']).stem
        file_output_dir = output_subdir / file_name
        file_output_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. 保存基本信息
        basic_info = {
            'file_info': {
                'name': file_info['file_name'],
                'path': file_info['file_path'],
                'size': file_info['file_size'],
                'type': file_info['file_type'],
            },
            'processing_info': {
                'status': file_info['status'],
                'error': file_info['error'],
                'sql_count': len(file_info['sql_components']),
            },
            'analysis_summary': file_info['analysis'],
        }
        
        with open(file_output_dir / 'basic_info.json', 'w', encoding='utf-8') as f:
            json.dump(basic_info, f, ensure_ascii=False, indent=2)
        
        # 2. 保存SQL组件
        if file_info['sql_components']:
            # 保存为JSON
            with open(file_output_dir / 'sql_components.json', 'w', encoding='utf-8') as f:
                json.dump(file_info['sql_components'], f, ensure_ascii=False, indent=2)
            
            # 保存为文本文件（便于查看）
            with open(file_output_dir / 'extracted_sql.txt', 'w', encoding='utf-8') as f:
                f.write(f"Kettle文件: {file_info['file_name']}\n")
                f.write(f"SQL组件数量: {len(file_info['sql_components'])}\n")
                f.write("=" * 80 + "\n\n")
                
                for i, comp in enumerate(file_info['sql_components'], 1):
                    f.write(f"SQL组件 {i}: {comp['step']}\n")
                    f.write(f"长度: {comp['length']} 字符\n")
                    
                    # 分析信息
                    analysis = file_info['analysis']['sql_analyses'][i-1]
                    f.write(f"操作类型: ")
                    types = []
                    if analysis['create_table']: types.append('CREATE TABLE')
                    if analysis['insert_into']: types.append('INSERT INTO')
                    if analysis['update']: types.append('UPDATE')
                    if analysis['delete']: types.append('DELETE')
                    if analysis['select']: types.append('SELECT')
                    f.write(', '.join(types) + "\n")
                    
                    if analysis['tables']:
                        f.write(f"涉及表: {', '.join(analysis['tables'])}\n")
                    
                    if analysis['key_keywords']:
                        f.write(f"关键关键字: {', '.join(analysis['key_keywords'])}\n")
                    
                    f.write("-" * 40 + "\n")
                    f.write(comp['sql'])
                    f.write("\n\n" + "=" * 80 + "\n\n")
        
        # 3. 保存详细分析
        if file_info['sql_components']:
            detailed_analysis = []
            for i, (comp, analysis) in enumerate(zip(file_info['sql_components'], file_info['analysis']['sql_analyses']), 1):
                detailed_analysis.append({
                    'component_index': i,
                    'step_name': comp['step'],
                    'sql_length': comp['length'],
                    'analysis': analysis,
                })
            
            with open(file_output_dir / 'detailed_analysis.json', 'w', encoding='utf-8') as f:
                json.dump(detailed_analysis, f, ensure_ascii=False, indent=2)
        
        return str(file_output_dir)
    
    def process_files(self, file_paths: List[str], output_subdir_name: Optional[str] = None) -> Dict:
        """批量处理多个Kettle文件"""
        
        # 创建输出目录
        if output_subdir_name:
            output_subdir = self.batch_output_dir / output_subdir_name
        else:
            output_subdir = self.batch_output_dir / "kettle_files"
        
        output_subdir.mkdir(parents=True, exist_ok=True)
        
        # 处理每个文件
        file_summaries = []
        
        for file_path_str in file_paths:
            file_path = Path(file_path_str)
            if not file_path.exists():
                logger.warning(f"文件不存在: {file_path}")
                continue
            
            self.batch_summary['total_files'] += 1
            self.batch_summary['processed_files'] += 1
            
            file_info = self.process_single_file(file_path)
            file_summaries.append(file_info)
            
            # 保存结果
            if file_info['status'] == 'success':
                output_path = self.save_file_results(file_info, output_subdir)
                file_info['output_path'] = output_path
        
        self.batch_summary['file_summaries'] = file_summaries
        
        # 更新统计信息
        if self.batch_summary['total_sql_components'] > 0:
            self.batch_summary['sql_statistics']['avg_sql_length'] = (
                self.batch_summary['sql_statistics']['total_sql_length'] / 
                self.batch_summary['total_sql_components']
            )
        
        # 转换set为list以便JSON序列化
        self.batch_summary['unique_tables'] = list(self.batch_summary['unique_tables'])
        self.batch_summary['unique_keywords'] = list(self.batch_summary['unique_keywords'])
        
        # 保存批处理总结
        self.batch_summary['end_time'] = datetime.now().isoformat()
        self.batch_summary['duration_seconds'] = (
            datetime.fromisoformat(self.batch_summary['end_time']) - 
            datetime.fromisoformat(self.batch_summary['start_time'])
        ).total_seconds()
        
        self.save_batch_summary()
        
        return self.batch_summary
    
    def process_directory(self, directory_path: str, patterns: List[str] = None) -> Dict:
        """处理目录中的所有Kettle文件"""
        if patterns is None:
            patterns = ['*.kjb', '*.ktr']
        
        dir_path = Path(directory_path)
        if not dir_path.is_dir():
            logger.error(f"目录不存在: {directory_path}")
            return {}
        
        file_paths = []
        for pattern in patterns:
            file_paths.extend(dir_path.glob(pattern))
        
        if not file_paths:
            logger.warning(f"在目录 {directory_path} 中未找到Kettle文件")
            return {}
        
        logger.info(f"在目录 {directory_path} 中找到 {len(file_paths)} 个Kettle文件")
        
        # 使用目录名作为输出子目录名
        output_subdir_name = dir_path.name
        
        return self.process_files([str(p) for p in file_paths], output_subdir_name)
    
    def save_batch_summary(self):
        """保存批处理总结"""
        summary_file = self.batch_output_dir / "batch_summary.json"
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(self.batch_summary, f, ensure_ascii=False, indent=2)
        
        # 也保存为可读的文本格式
        text_summary_file = self.batch_output_dir / "batch_summary.txt"
        with open(text_summary_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("批量Kettle SQL提取总结报告\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"批次ID: {self.batch_summary['batch_id']}\n")
            f.write(f"开始时间: {self.batch_summary['start_time']}\n")
            f.write(f"结束时间: {self.batch_summary['end_time']}\n")
            f.write(f"处理时长: {self.batch_summary['duration_seconds']:.2f} 秒\n\n")
            
            f.write("文件处理统计:\n")
            f.write(f"  总文件数: {self.batch_summary['total_files']}\n")
            f.write(f"  已处理文件: {self.batch_summary['processed_files']}\n")
            f.write(f"  成功文件: {self.batch_summary['success_files']}\n")
            f.write(f"  失败文件: {len(self.batch_summary['failed_files'])}\n\n")
            
            f.write("SQL组件统计:\n")
            f.write(f"  总SQL组件数: {self.batch_summary['total_sql_components']}\n")
            stats = self.batch_summary['sql_statistics']
            f.write(f"  总SQL长度: {stats['total_sql_length']} 字符\n")
            f.write(f"  平均SQL长度: {stats['avg_sql_length']:.1f} 字符\n")
            f.write(f"  最大SQL长度: {stats['max_sql_length']} 字符\n")
            if stats['min_sql_length'] != float('inf'):
                f.write(f"  最小SQL长度: {stats['min_sql_length']} 字符\n")
            f.write("\n")
            
            f.write("发现的关键信息:\n")
            f.write(f"  唯一表名: {len(self.batch_summary['unique_tables'])} 个\n")
            if self.batch_summary['unique_tables']:
                f.write(f"  表名列表: {', '.join(sorted(self.batch_summary['unique_tables']))}\n")
            
            f.write(f"  唯一关键字: {len(self.batch_summary['unique_keywords'])} 个\n")
            if self.batch_summary['unique_keywords']:
                f.write(f"  关键字列表: {', '.join(sorted(self.batch_summary['unique_keywords']))}\n")
            f.write("\n")
            
            if self.batch_summary['failed_files']:
                f.write("失败文件列表:\n")
                for fail in self.batch_summary['failed_files']:
                    f.write(f"  - {Path(fail['file']).name}: {fail['error']}\n")
            
            f.write("\n" + "=" * 80 + "\n")
            f.write(f"详细结果请查看: {self.batch_output_dir}\n")
            f.write("=" * 80 + "\n")
        
        # 生成HTML报告（可选）
        self.generate_html_report()
        
        logger.info(f"批处理总结已保存到: {summary_file}")
        logger.info(f"文本总结已保存到: {text_summary_file}")
    
    def generate_html_report(self):
        """生成HTML报告"""
        html_file = self.batch_output_dir / "batch_report.html"
        
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>批量Kettle SQL提取报告 - {self.batch_summary['batch_id']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background-color: #f5f5f5; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
        .summary {{ background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px; }}
        .stat-card {{ background-color: white; padding: 15px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .stat-value {{ font-size: 24px; font-weight: bold; color: #2c3e50; }}
        .stat-label {{ font-size: 14px; color: #7f8c8d; }}
        .file-list {{ margin-top: 20px; }}
        .file-item {{ border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; border-radius: 5px; }}
        .file-success {{ border-left: 5px solid #2ecc71; }}
        .file-failed {{ border-left: 5px solid #e74c3c; }}
        .table-list {{ background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        .keyword-list {{ background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        .keyword-item {{ display: inline-block; background-color: #3498db; color: white; padding: 5px 10px; margin: 5px; border-radius: 3px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>批量Kettle SQL提取报告</h1>
            <p>批次ID: {self.batch_summary['batch_id']}</p>
            <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="summary">
            <h2>处理摘要</h2>
            <p>从 {self.batch_summary['start_time']} 到 {self.batch_summary['end_time']}</p>
            <p>处理时长: {self.batch_summary['duration_seconds']:.2f} 秒</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">{self.batch_summary['total_files']}</div>
                <div class="stat-label">总文件数</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{self.batch_summary['success_files']}</div>
                <div class="stat-label">成功文件</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{self.batch_summary['total_sql_components']}</div>
                <div class="stat-label">SQL组件数</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len(self.batch_summary['failed_files'])}</div>
                <div class="stat-label">失败文件</div>
            </div>
        </div>
        
        <div class="table-list">
            <h2>发现的唯一表名 ({len(self.batch_summary['unique_tables'])}个)</h2>
            <ul>
                {"".join([f'<li>{table}</li>' for table in sorted(self.batch_summary['unique_tables'])])}
            </ul>
        </div>
        
        <div class="keyword-list">
            <h2>发现的SQL关键字 ({len(self.batch_summary['unique_keywords'])}个)</h2>
            <div>
                {"".join([f'<span class="keyword-item">{keyword}</span>' for keyword in sorted(self.batch_summary['unique_keywords'])])}
            </div>
        </div>
        
        <div class="file-list">
            <h2>文件处理详情</h2>
            {"".join([
                f'<div class="file-item {"file-success" if file["status"] == "success" else "file-failed"}">'
                f'<h3>{file["file_name"]} - {file["status"]}</h3>'
                f'<p>SQL组件数: {len(file["sql_components"]) if "sql_components" in file else 0}</p>'
                f'{"<p>输出路径: " + file.get("output_path", "") + "</p>" if file.get("output_path") else ""}'
                f'{"<p style=\"color:red;\">错误: " + file["error"] + "</p>" if file.get("error") else ""}'
                f'</div>'
                for file in self.batch_summary['file_summaries']
            ])}
        </div>
        
        <div style="margin-top: 30px; padding: 20px; background-color: #f5f5f5; border-radius: 5px;">
            <p><strong>输出目录:</strong> {self.batch_output_dir}</p>
            <p>每个成功处理的文件都有一个独立的目录，包含:</p>
            <ul>
                <li>basic_info.json - 基本信息</li>
                <li>sql_components.json - SQL组件(JSON格式)</li>
                <li>extracted_sql.txt - SQL组件(文本格式)</li>
                <li>detailed_analysis.json - 详细分析</li>
            </ul>
        </div>
    </div>
</body>
</html>"""
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"HTML报告已生成: {html_file}")
    
    def generate_consolidated_sql_file(self):
        """生成合并的SQL文件，包含所有提取的SQL"""
        consolidated_file = self.batch_output_dir / "all_extracted_sql.txt"
        
        with open(consolidated_file, 'w', encoding='utf-8') as f:
            f.write("=" * 100 + "\n")
            f.write("批量提取的Kettle SQL脚本汇总\n")
            f.write(f"批次: {self.batch_summary['batch_id']}\n")
            f.write(f"总文件数: {self.batch_summary['total_files']}\n")
            f.write(f"总SQL组件数: {self.batch_summary['total_sql_components']}\n")
            f.write("=" * 100 + "\n\n")
            
            for file_info in self.batch_summary['file_summaries']:
                if file_info['status'] == 'success' and file_info['sql_components']:
                    f.write(f"【文件】{file_info['file_name']}\n")
                    f.write(f"【路径】{file_info['file_path']}\n")
                    f.write(f"【SQL组件数】{len(file_info['sql_components'])}\n")
                    f.write("-" * 80 + "\n\n")
                    
                    for i, comp in enumerate(file_info['sql_components'], 1):
                        f.write(f"组件 {i}: {comp['step']}\n")
                        f.write(f"长度: {comp['length']} 字符\n")
                        f.write("-" * 40 + "\n")
                        f.write(comp['sql'])
                        f.write("\n\n" + "=" * 80 + "\n\n")
        
        logger.info(f"合并SQL文件已生成: {consolidated_file}")
        
        return consolidated_file


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='批量提取多个Kettle作业中的SQL脚本',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 处理单个文件
  python batch_extract_kettle_sql.py --file job1.kjb job2.ktr
  
  # 处理目录中的所有.kjb和.ktr文件
  python batch_extract_kettle_sql.py --dir /path/to/kettle/jobs
  
  # 指定输出目录
  python batch_extract_kettle_sql.py --dir /path/to/kettle/jobs --output my_analysis
  
  # 处理特定模式的文件
  python batch_extract_kettle_sql.py --dir /path/to/kettle/jobs --pattern "*.kjb"
  
  # 从文件列表读取
  python batch_extract_kettle_sql.py --list kettle_files.txt
        """
    )
    
    parser.add_argument('--file', nargs='+', help='单个或多个Kettle文件路径')
    parser.add_argument('--dir', help='包含Kettle文件的目录路径')
    parser.add_argument('--list', help='包含文件路径列表的文本文件')
    parser.add_argument('--pattern', nargs='+', default=['*.kjb', '*.ktr'], 
                       help='文件匹配模式 (默认: *.kjb *.ktr)')
    parser.add_argument('--output', help='输出目录 (默认: batch_kettle_analysis)', 
                       default='batch_kettle_analysis')
    parser.add_argument('--consolidate', action='store_true', 
                       help='生成合并的SQL文件')
    parser.add_argument('--simple-output', action='store_true',
                       help='简化输出，只生成HTML报告和总结')
    
    args = parser.parse_args()
    
    if not any([args.file, args.dir, args.list]):
        parser.print_help()
        return 1
    
    # 创建批处理器
    extractor = BatchKettleSQLExtractor(args.output)
    
    # 收集文件路径
    file_paths = []
    
    if args.file:
        file_paths.extend(args.file)
    
    if args.dir:
        summary = extractor.process_directory(args.dir, args.pattern)
        if summary:
            print(f"✅ 已处理目录: {args.dir}")
            print(f"   成功文件: {summary['success_files']}/{summary['total_files']}")
            print(f"   SQL组件: {summary['total_sql_components']}个")
            print(f"   输出目录: {extractor.batch_output_dir}")
    
    if args.list:
        list_file = Path(args.list)
        if list_file.exists():
            with open(list_file, 'r', encoding='utf-8') as f:
                paths_from_list = [line.strip() for line in f if line.strip()]
            file_paths.extend(paths_from_list)
        else:
            logger.error(f"列表文件不存在: {args.list}")
    
    # 处理单独指定的文件
    if file_paths:
        summary = extractor.process_files(file_paths, "specified_files")
        if summary:
            print(f"✅ 已处理指定文件: {len(file_paths)}个")
            print(f"   成功文件: {summary['success_files']}/{summary['total_files']}")
            print(f"   SQL组件: {summary['total_sql_components']}个")
            print(f"   输出目录: {extractor.batch_output_dir}")
    
    # 生成合并文件（如果指定）
    if args.consolidate and extractor.batch_summary['total_sql_components'] > 0:
        consolidated_file = extractor.generate_consolidated_sql_file()
        print(f"📦 合并SQL文件: {consolidated_file}")
    
    # 打印总结
    print("\n" + "=" * 80)
    print("批量处理完成!")
    print(f"总输出目录: {extractor.batch_output_dir}")
    print("包含:")
    print("  - batch_summary.json/txt - 批处理总结")
    print("  - batch_report.html - HTML格式报告")
    if args.consolidate:
        print("  - all_extracted_sql.txt - 合并的SQL文件")
    print("  - 每个文件的独立目录 - 包含详细结果")
    print("=" * 80)
    
    return 0


if __name__ == '__main__':
    exit(main())