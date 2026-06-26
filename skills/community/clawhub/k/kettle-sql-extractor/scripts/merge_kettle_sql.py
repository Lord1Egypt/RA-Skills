#!/usr/bin/env python3
"""
将单个Kettle作业中的多个SQL组件合并成一个SQL脚本
支持.kjb和.ktr文件，智能合并SQL语句，保持执行顺序
"""

import os
import sys
import re
import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class KettleSQLMerger:
    """Kettle SQL合并器 - 将单个Kettle作业中的多个SQL组件合并成一个SQL脚本"""
    
    def __init__(self):
        self.sql_components = []
        self.merged_sql = ""
        self.analysis = {
            'original_components': 0,
            'merged_statements': 0,
            'tables_created': [],
            'tables_used': [],
            'operations': {
                'create_table': 0,
                'insert_into': 0,
                'update': 0,
                'delete': 0,
                'select': 0,
                'drop_table': 0,
                'truncate': 0,
                'alter_table': 0,
            },
            'dependencies': {},  # 表依赖关系
            'execution_order_suggested': [],  # 建议的执行顺序
        }
    
    def extract_kettle_sql_complete(self, file_path: str) -> List[Dict]:
        """从Kettle文件中完全提取所有SQL组件"""
        
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
        
        # 修复XML特殊字符
        content = content.replace('&lt;', '<').replace('&gt;', '>')
        content = content.replace('&amp;', '&').replace('&quot;', '"').replace('&apos;', "'")
        
        # 提取完整<entry>标签
        entries = re.findall(r'<entry>[\s\S]*?</entry>', content)
        
        sql_components = []
        
        for i, entry in enumerate(entries, 1):
            # 提取步骤名称
            name_match = re.search(r'<name>([^<]+)</name>', entry)
            step_name = name_match.group(1).strip() if name_match else f"步骤_{i}"
            
            # 提取SQL内容
            sql_match = re.search(r'<sql>([\s\S]*?)</sql>', entry)
            if sql_match:
                sql_content = sql_match.group(1).strip()
                
                # 清理CDATA标记
                sql_content = re.sub(r'<!\[CDATA\[|\]\]>', '', sql_content)
                
                # 处理XML注释
                sql_content = re.sub(r'<!--.*?-->', '', sql_content, flags=re.DOTALL)
                
                sql_content = sql_content.strip()
                
                if sql_content:
                    # 分析SQL类型
                    sql_type = self.analyze_sql_type(sql_content)
                    
                    sql_components.append({
                        'step': step_name,
                        'sql': sql_content,
                        'length': len(sql_content),
                        'component_index': i,
                        'sql_type': sql_type,
                        'tables': self.extract_tables_from_sql(sql_content),
                        'operation': sql_type['primary_operation'],
                    })
        
        return sql_components
    
    def analyze_sql_type(self, sql_content: str) -> Dict:
        """分析SQL类型和特征"""
        sql_upper = sql_content.upper()
        
        analysis = {
            'primary_operation': 'UNKNOWN',
            'operations': [],
            'has_cte': False,
            'has_subquery': False,
            'has_join': False,
            'has_union': False,
            'is_ddl': False,
            'is_dml': False,
            'is_query': False,
        }
        
        # 检测主要操作类型
        if 'CREATE TABLE' in sql_upper:
            analysis['primary_operation'] = 'CREATE_TABLE'
            analysis['operations'].append('CREATE_TABLE')
            analysis['is_ddl'] = True
        elif 'DROP TABLE' in sql_upper:
            analysis['primary_operation'] = 'DROP_TABLE'
            analysis['operations'].append('DROP_TABLE')
            analysis['is_ddl'] = True
        elif 'ALTER TABLE' in sql_upper:
            analysis['primary_operation'] = 'ALTER_TABLE'
            analysis['operations'].append('ALTER_TABLE')
            analysis['is_ddl'] = True
        elif 'TRUNCATE TABLE' in sql_upper or 'TRUNCATE ' in sql_upper:
            analysis['primary_operation'] = 'TRUNCATE'
            analysis['operations'].append('TRUNCATE')
            analysis['is_ddl'] = True
        elif 'INSERT INTO' in sql_upper:
            analysis['primary_operation'] = 'INSERT_INTO'
            analysis['operations'].append('INSERT_INTO')
            analysis['is_dml'] = True
        elif 'UPDATE ' in sql_upper:
            analysis['primary_operation'] = 'UPDATE'
            analysis['operations'].append('UPDATE')
            analysis['is_dml'] = True
        elif 'DELETE FROM' in sql_upper:
            analysis['primary_operation'] = 'DELETE'
            analysis['operations'].append('DELETE')
            analysis['is_dml'] = True
        elif 'SELECT ' in sql_upper:
            analysis['primary_operation'] = 'SELECT'
            analysis['operations'].append('SELECT')
            analysis['is_query'] = True
        
        # 检测其他特征
        if re.search(r'WITH\s+\w+\s+AS', sql_upper):
            analysis['has_cte'] = True
        if re.search(r'SELECT\s+.+?\s+FROM\s*\(', sql_upper, re.IGNORECASE):
            analysis['has_subquery'] = True
        if 'JOIN' in sql_upper:
            analysis['has_join'] = True
        if 'UNION' in sql_upper:
            analysis['has_union'] = True
        
        return analysis
    
    def extract_tables_from_sql(self, sql_content: str) -> List[str]:
        """从SQL中提取表名"""
        sql_upper = sql_content.upper()
        tables = []
        
        # 提取CREATE TABLE的表名
        create_matches = re.findall(r'CREATE\s+(?:TEMPORARY\s+)?TABLE\s+(?:\w+\.)?(\w+)', sql_upper)
        tables.extend(create_matches)
        
        # 提取INSERT INTO的表名
        insert_matches = re.findall(r'INSERT\s+INTO\s+(?:\w+\.)?(\w+)', sql_upper)
        tables.extend(insert_matches)
        
        # 提取UPDATE的表名
        update_matches = re.findall(r'UPDATE\s+(?:\w+\.)?(\w+)', sql_upper)
        tables.extend(update_matches)
        
        # 提取DELETE FROM的表名
        delete_matches = re.findall(r'DELETE\s+FROM\s+(?:\w+\.)?(\w+)', sql_upper)
        tables.extend(delete_matches)
        
        # 提取FROM子句中的表名
        from_matches = re.findall(r'FROM\s+(?:\w+\.)?(\w+)', sql_upper)
        tables.extend(from_matches)
        
        # 提取JOIN子句中的表名
        join_matches = re.findall(r'JOIN\s+(?:\w+\.)?(\w+)', sql_upper)
        tables.extend(join_matches)
        
        # 去重并返回
        return list(set(tables))
    
    def analyze_dependencies(self):
        """分析SQL组件之间的依赖关系"""
        # 初始化依赖关系
        for i, comp in enumerate(self.sql_components):
            self.analysis['dependencies'][i] = {
                'depends_on': [],  # 依赖哪些组件
                'required_by': [],  # 被哪些组件依赖
                'tables_created': comp.get('tables', []),  # 创建的表
                'tables_used': [],  # 使用的表（非创建）
            }
        
        # 分析表使用和创建关系
        for i, comp in enumerate(self.sql_components):
            comp_tables = set(comp.get('tables', []))
            comp_creates = set(comp.get('tables', []))  # 假设所有提到的表都是创建的（简化）
            
            # 检查这个组件是否使用其他组件创建的表
            for j, other_comp in enumerate(self.sql_components):
                if i == j:
                    continue
                
                other_creates = set(other_comp.get('tables', []))
                
                # 如果当前组件使用的表在其他组件中被创建
                used_tables = comp_tables.intersection(other_creates)
                if used_tables:
                    self.analysis['dependencies'][i]['depends_on'].append(j)
                    self.analysis['dependencies'][j]['required_by'].append(i)
    
    def suggest_execution_order(self) -> List[int]:
        """根据依赖关系建议执行顺序"""
        # 简单的拓扑排序（基于依赖关系）
        visited = set()
        order = []
        
        def visit(node):
            if node in visited:
                return
            visited.add(node)
            
            # 先访问依赖的节点
            for dep in self.analysis['dependencies'][node]['depends_on']:
                visit(dep)
            
            order.append(node)
        
        # 访问所有节点
        for node in range(len(self.sql_components)):
            if node not in visited:
                visit(node)
        
        self.analysis['execution_order_suggested'] = order
        return order
    
    def merge_sql_components(self, execution_order: Optional[List[int]] = None) -> str:
        """合并SQL组件成一个SQL脚本"""
        
        if not self.sql_components:
            return ""
        
        # 使用指定的执行顺序，或使用建议的顺序
        if execution_order is None:
            execution_order = list(range(len(self.sql_components)))
        
        merged_lines = []
        
        # 添加文件头信息
        merged_lines.append("-- ============================================")
        merged_lines.append("-- 合并的Kettle作业SQL脚本")
        merged_lines.append("-- 生成时间: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        merged_lines.append("-- 原始SQL组件数: " + str(len(self.sql_components)))
        merged_lines.append("-- ============================================")
        merged_lines.append("")
        
        # 添加组件信息摘要
        merged_lines.append("-- SQL组件信息摘要:")
        for i, comp in enumerate(self.sql_components):
            merged_lines.append(f"--  组件 {i+1}: {comp['step']}")
            merged_lines.append(f"--      类型: {comp['operation']}")
            merged_lines.append(f"--      表: {', '.join(comp.get('tables', []))}")
            merged_lines.append(f"--      长度: {comp['length']} 字符")
        merged_lines.append("")
        
        # 添加建议的执行顺序
        merged_lines.append("-- 建议的执行顺序 (基于依赖分析):")
        order_str = " -> ".join([str(i+1) for i in self.analysis['execution_order_suggested']])
        merged_lines.append(f"--  {order_str}")
        merged_lines.append("")
        
        # 添加合并的SQL语句（按执行顺序）
        merged_lines.append("-- ============================================")
        merged_lines.append("-- 合并的SQL语句开始")
        merged_lines.append("-- ============================================")
        merged_lines.append("")
        
        for idx in execution_order:
            if 0 <= idx < len(self.sql_components):
                comp = self.sql_components[idx]
                
                # 添加组件分隔和注释
                merged_lines.append(f"-- {'='*50}")
                merged_lines.append(f"-- 组件 {idx+1}: {comp['step']}")
                merged_lines.append(f"-- 类型: {comp['operation']}")
                merged_lines.append(f"-- {'='*50}")
                merged_lines.append("")
                
                # 添加SQL语句
                sql_lines = comp['sql'].split('\n')
                for line in sql_lines:
                    merged_lines.append(line)
                
                # 添加语句结束分隔符（如果不是最后一条）
                if idx != execution_order[-1]:
                    merged_lines.append("")
                    merged_lines.append("-- 语句结束")
                    merged_lines.append("")
        
        merged_lines.append("")
        merged_lines.append("-- ============================================")
        merged_lines.append("-- 合并的SQL语句结束")
        merged_lines.append("-- ============================================")
        
        # 添加执行建议
        merged_lines.append("")
        merged_lines.append("-- ============================================")
        merged_lines.append("-- 执行建议")
        merged_lines.append("-- ============================================")
        merged_lines.append("")
        merged_lines.append("-- 1. 检查表依赖关系:")
        for i, comp in enumerate(self.sql_components):
            deps = self.analysis['dependencies'][i]['depends_on']
            if deps:
                dep_names = [self.sql_components[d]['step'] for d in deps]
                merged_lines.append(f"--    组件 {i+1} ({comp['step']}) 依赖于: {', '.join(dep_names)}")
        
        merged_lines.append("")
        merged_lines.append("-- 2. 执行前检查:")
        merged_lines.append("--    - 确保所有依赖的表已存在")
        merged_lines.append("--    - 检查表名冲突")
        merged_lines.append("--    - 验证数据类型兼容性")
        merged_lines.append("")
        merged_lines.append("-- 3. 事务处理建议:")
        merged_lines.append("--    -- 开始事务")
        merged_lines.append("--    BEGIN TRANSACTION;")
        merged_lines.append("--    ")
        merged_lines.append("--    -- 执行上面的SQL语句")
        merged_lines.append("--    ")
        merged_lines.append("--    -- 提交或回滚")
        merged_lines.append("--    -- COMMIT;  -- 如果所有语句成功")
        merged_lines.append("--    -- ROLLBACK; -- 如果任何语句失败")
        
        self.merged_sql = '\n'.join(merged_lines)
        return self.merged_sql
    
    def create_executable_sql(self, add_transaction: bool = True) -> str:
        """创建可执行的SQL脚本（包含事务控制）"""
        
        if not self.merged_sql:
            self.merge_sql_components()
        
        executable_lines = []
        
        # 添加事务控制
        if add_transaction:
            executable_lines.append("-- ============================================")
            executable_lines.append("-- 可执行SQL脚本（带事务控制）")
            executable_lines.append("-- ============================================")
            executable_lines.append("")
            executable_lines.append("-- 设置事务隔离级别（可选）")
            executable_lines.append("-- SET TRANSACTION ISOLATION LEVEL READ COMMITTED;")
            executable_lines.append("")
            executable_lines.append("-- 开始事务")
            executable_lines.append("BEGIN TRANSACTION;")
            executable_lines.append("")
            executable_lines.append("-- 错误处理设置（根据数据库类型调整）")
            executable_lines.append("-- SET XACT_ABORT ON;  -- SQL Server")
            executable_lines.append("-- SET autocommit=0;    -- MySQL")
            executable_lines.append("")
        
        # 添加SQL语句（从合并的SQL中提取实际语句）
        sql_statements = []
        in_comment = False
        
        for line in self.merged_sql.split('\n'):
            line_stripped = line.strip()
            
            # 跳过注释行（以--开头但不是语句的一部分）
            if line_stripped.startswith('--') and not in_comment:
                continue
            
            # 处理多行注释
            if '/*' in line:
                in_comment = True
            if '*/' in line:
                in_comment = False
                continue
            
            if not in_comment and line_stripped and not line_stripped.startswith('--'):
                sql_statements.append(line)
        
        # 添加SQL语句
        executable_lines.extend(sql_statements)
        
        # 添加事务结束
        if add_transaction:
            executable_lines.append("")
            executable_lines.append("-- 提交事务（如果所有语句成功）")
            executable_lines.append("COMMIT;")
            executable_lines.append("")
            executable_lines.append("-- 如果任何语句失败，使用ROLLBACK回滚")
            executable_lines.append("-- ROLLBACK;")
        
        return '\n'.join(executable_lines)
    
    def create_simple_merged_sql(self) -> str:
        """创建简化的合并SQL（只包含SQL语句，无注释）"""
        
        if not self.sql_components:
            return ""
        
        simple_lines = []
        
        # 按原始顺序添加SQL语句
        for i, comp in enumerate(self.sql_components):
            # 添加简单的分隔
            if i > 0:
                simple_lines.append("")
                simple_lines.append("-- " + "-" * 40)
                simple_lines.append("")
            
            # 添加SQL语句
            sql_lines = comp['sql'].split('\n')
            simple_lines.extend(sql_lines)
        
        return '\n'.join(simple_lines)
    
    def process_kettle_file(self, kettle_file: str) -> Dict:
        """处理单个Kettle文件，返回处理结果"""
        
        result = {
            'file_path': kettle_file,
            'file_name': Path(kettle_file).name,
            'status': 'pending',
            'error': None,
            'sql_components_count': 0,
            'merged_sql_length': 0,
            'output_files': [],
        }
        
        try:
            logger.info(f"📄 处理Kettle文件: {Path(kettle_file).name}")
            
            # 提取SQL组件
            self.sql_components = self.extract_kettle_sql_complete(kettle_file)
            result['sql_components_count'] = len(self.sql_components)
            
            if not self.sql_components:
                result['status'] = 'no_sql'
                result['error'] = '未找到SQL组件'
                logger.warning(f"⚠️  未找到SQL组件: {Path(kettle_file).name}")
                return result
            
            # 分析依赖关系
            self.analyze_dependencies()
            
            # 建议执行顺序
            self.suggest_execution_order()
            
            # 更新分析统计
            self.analysis['original_components'] = len(self.sql_components)
            
            for comp in self.sql_components:
                op = comp['operation']
                if op in self.analysis['operations']:
                    self.analysis['operations'][op] += 1
            
            result['status'] = 'success'
            logger.info(f"✅ 成功处理: {Path(kettle_file).name} ({len(self.sql_components)}个SQL组件)")
            
        except Exception as e:
            result['status'] = 'failed'
            result['error'] = str(e)
            logger.error(f"❌ 处理失败: {Path(kettle_file).name} - {e}")
        
        return result
    
    def save_results(self, output_dir: str, kettle_file_name: str, 
                     output_types: List[str] = None) -> List[str]:
        """保存处理结果到文件，支持选择输出类型"""
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        output_files = []
        
        # 如果没有指定输出类型，默认生成所有文件
        if output_types is None:
            output_types = ['analysis', 'detailed', 'executable', 'simple', 'components']
        
        # 根据输出类型生成文件
        for output_type in output_types:
            if output_type == 'analysis':
                report_file = output_path / f"{kettle_file_name}_analysis.json"
                report_data = {
                    'file_info': {
                        'name': kettle_file_name,
                        'processing_time': datetime.now().isoformat(),
                    },
                    'sql_components': self.sql_components,
                    'analysis': self.analysis,
                    'statistics': {
                        'total_components': len(self.sql_components),
                        'merged_statements': len(self.sql_components),
                        'total_sql_length': sum(c['length'] for c in self.sql_components),
                    }
                }
                with open(report_file, 'w', encoding='utf-8') as f:
                    json.dump(report_data, f, ensure_ascii=False, indent=2)
                output_files.append(str(report_file))
            
            elif output_type == 'detailed':
                merged_file = output_path / f"{kettle_file_name}_merged_detailed.sql"
                merged_sql = self.merge_sql_components()
                with open(merged_file, 'w', encoding='utf-8') as f:
                    f.write(merged_sql)
                output_files.append(str(merged_file))
            
            elif output_type == 'executable':
                executable_file = output_path / f"{kettle_file_name}_executable.sql"
                executable_sql = self.create_executable_sql()
                with open(executable_file, 'w', encoding='utf-8') as f:
                    f.write(executable_sql)
                output_files.append(str(executable_file))
            
            elif output_type == 'simple':
                simple_file = output_path / f"{kettle_file_name}_simple.sql"
                simple_sql = self.create_simple_merged_sql()
                with open(simple_file, 'w', encoding='utf-8') as f:
                    f.write(simple_sql)
                output_files.append(str(simple_file))
            
            elif output_type == 'components':
                components_file = output_path / f"{kettle_file_name}_components.txt"
                with open(components_file, 'w', encoding='utf-8') as f:
                    f.write(f"Kettle文件: {kettle_file_name}\n")
                    f.write(f"SQL组件数: {len(self.sql_components)}\n")
                    f.write("=" * 60 + "\n\n")
                    
                    for i, comp in enumerate(self.sql_components, 1):
                        f.write(f"组件 {i}: {comp['step']}\n")
                        f.write(f"类型: {comp['operation']}\n")
                        f.write(f"表: {', '.join(comp.get('tables', []))}\n")
                        f.write(f"长度: {comp['length']} 字符\n")
                        f.write("-" * 40 + "\n")
                        f.write(comp['sql'])
                        f.write("\n\n" + "=" * 60 + "\n\n")
                output_files.append(str(components_file))
        
        logger.info(f"💾 结果已保存到: {output_path}")
        
        return output_files


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='将单个Kettle作业中的多个SQL组件合并成一个SQL脚本',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基本用法：合并一个Kettle作业的SQL
  python merge_kettle_sql.py job.kjb
  
  # 指定输出目录
  python merge_kettle_sql.py job.kjb --output my_output
  
  # 只生成详细SQL文件（用户的常见需求）
  python merge_kettle_sql.py job.kjb --only-detailed
  
  # 只生成可执行SQL文件
  python merge_kettle_sql.py job.kjb --only-executable
  
  # 只生成简化SQL文件
  python merge_kettle_sql.py job.kjb --only-simple
  
  # 指定要生成的文件类型
  python merge_kettle_sql.py job.kjb --output-files detailed executable
  
  # 只生成简化的SQL（兼容旧参数）
  python merge_kettle_sql.py job.kjb --simple
  
  # 生成可执行的SQL（兼容旧参数）
  python merge_kettle_sql.py job.kjb --executable
  
  # 批量处理多个文件
  python merge_kettle_sql.py job1.kjb job2.ktr --batch
  
  # 简化输出：在当前目录生成SQL文件，不创建分析文件夹（最新需求）
  python merge_kettle_sql.py job1.kjb job2.kjb --simple-output
        """
    )
    
    parser.add_argument('kettle_files', nargs='+', help='Kettle文件路径 (.kjb 或 .ktr)')
    parser.add_argument('--output', '-o', help='输出目录 (默认: merged_kettle_sql)', 
                       default='merged_kettle_sql')
    parser.add_argument('--simple', action='store_true', 
                       help='只生成简化的SQL（无注释）')
    parser.add_argument('--executable', action='store_true', 
                       help='生成可执行的SQL（带事务控制）')
    parser.add_argument('--batch', action='store_true', 
                       help='批量处理多个文件')
    parser.add_argument('--no-transaction', action='store_true',
                       help='可执行SQL中不包含事务控制')
    parser.add_argument('--only-detailed', action='store_true',
                       help='只生成详细SQL文件')
    parser.add_argument('--only-executable', action='store_true',
                       help='只生成可执行SQL文件')
    parser.add_argument('--only-simple', action='store_true',
                       help='只生成简化SQL文件')
    parser.add_argument('--output-files', nargs='+', 
                       choices=['detailed', 'executable', 'simple', 'components', 'analysis'],
                       help='指定要生成的文件类型')
    parser.add_argument('--simple-output', action='store_true',
                       help='简化输出：在当前目录生成SQL文件，不创建分析文件夹')
    
    args = parser.parse_args()
    
    # 如果是简化输出模式，不创建默认的输出目录
    if args.simple_output:
        output_dir = None  # 简化模式下不使用输出目录
    else:
        # 创建输出目录
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    results = []
    
    for kettle_file in args.kettle_files:
        file_path = Path(kettle_file)
        if not file_path.exists():
            logger.error(f"文件不存在: {kettle_file}")
            continue
        
        # 创建合并器实例
        merger = KettleSQLMerger()
        
        # 处理文件
        result = merger.process_kettle_file(kettle_file)
        
        if result['status'] == 'success':
            # 确定输出文件类型
            if args.output_files:
                output_types = args.output_files
            elif args.simple_output:
                output_types = ['detailed']  # 简化输出只生成详细SQL
            elif args.only_detailed:
                output_types = ['detailed']
            elif args.only_executable:
                output_types = ['executable']
            elif args.only_simple:
                output_types = ['simple']
            elif args.simple:
                output_types = ['analysis', 'detailed', 'executable', 'simple', 'components']
            elif args.executable:
                output_types = ['analysis', 'detailed', 'executable', 'simple', 'components']
            else:
                output_types = ['analysis', 'detailed', 'executable', 'simple', 'components']
            
            # 保存结果
            file_stem = file_path.stem
            
            # 如果是简化输出模式，直接保存在当前目录
            if args.simple_output:
                # 使用当前目录，而不是创建子目录
                simple_output_dir = Path.cwd()
                output_files = merger.save_results(simple_output_dir, file_stem, output_types)
            else:
                # 正常模式：创建子目录
                output_files = merger.save_results(output_dir / file_stem, file_stem, output_types)
            
            result['output_files'] = output_files
            result['merged_sql_length'] = len(merger.merged_sql) if merger.merged_sql else 0
            
            # 打印处理结果
            print(f"\n✅ 处理完成: {file_path.name}")
            print(f"   SQL组件数: {result['sql_components_count']}")
            print(f"   合并SQL长度: {result['merged_sql_length']} 字符")
            print(f"   输出文件数: {len(output_files)}")
            if output_files:
                print(f"   输出文件:")
                for output_file in output_files:
                    print(f"     - {Path(output_file).name}")
        
        elif result['status'] == 'no_sql':
            print(f"\n⚠️  警告: {file_path.name} - 未找到SQL组件")
        
        else:
            print(f"\n❌ 失败: {file_path.name} - {result['error']}")
        
        results.append(result)
    
    # 生成批处理总结（如果处理了多个文件且不是简化输出模式）
    if len(results) > 1 and not args.simple_output:
        summary_file = output_dir / "batch_summary.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("Kettle SQL合并批处理总结\n")
            f.write("=" * 80 + "\n\n")
            
            success_count = sum(1 for r in results if r['status'] == 'success')
            total_count = len(results)
            
            f.write(f"处理时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"总文件数: {total_count}\n")
            f.write(f"成功文件: {success_count}\n")
            f.write(f"失败文件: {total_count - success_count}\n\n")
            
            f.write("文件详情:\n")
            for result in results:
                status_icon = "✅" if result['status'] == 'success' else "❌"
                f.write(f"  {status_icon} {result['file_name']}: ")
                
                if result['status'] == 'success':
                    f.write(f"{result['sql_components_count']}个SQL组件\n")
                elif result['status'] == 'no_sql':
                    f.write("未找到SQL组件\n")
                else:
                    f.write(f"失败 - {result['error']}\n")
            
            f.write("\n" + "=" * 80 + "\n")
            f.write(f"详细结果请查看: {output_dir}\n")
            f.write("=" * 80 + "\n")
        
        print(f"\n📊 批处理总结已保存到: {summary_file}")
    
    return 0


if __name__ == '__main__':
    exit(main())