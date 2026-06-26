#!/usr/bin/env python3
"""
Kettle XML解析器 - 纯提取版本
用于解析Kettle作业(.kjb)和转换(.ktr)文件，提取SQL组件
"""

import xml.etree.ElementTree as ET
import re
import json
from pathlib import Path
from typing import Dict, List, Optional
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class KettleXMLParser:
    """Kettle XML文件解析器 - 纯提取版本"""
    
    def __init__(self, kettle_file: str):
        self.kettle_file = Path(kettle_file)
        self.root = None
        self.sql_components = []
        self.steps = []
        
    def parse(self) -> bool:
        """解析Kettle XML文件"""
        try:
            tree = ET.parse(self.kettle_file)
            self.root = tree.getroot()
            logger.info(f"成功解析文件: {self.kettle_file}")
            return True
        except ET.ParseError as e:
            logger.error(f"XML解析错误: {e}")
            return False
        except FileNotFoundError:
            logger.error(f"文件不存在: {self.kettle_file}")
            return False
    
    def extract_sql_components(self) -> List[Dict]:
        """提取SQL组件 - 保持原样，不做修改"""
        if not self.root:
            logger.error("请先调用parse()方法解析文件")
            return []
        
        self.sql_components = []
        
        # 处理XML特殊字符
        def fix_xml_special_chars(text: str) -> str:
            """修复XML特殊字符"""
            replacements = {
                '&lt;': '<',
                '&gt;': '>',
                '&amp;': '&',
                '&quot;': '"',
                '&apos;': "'",
            }
            for xml_char, real_char in replacements.items():
                text = text.replace(xml_char, real_char)
            return text
        
        # 查找所有SQL相关组件
        sql_patterns = [
            ('SQL', 'sql'),
            ('Table input', 'sql'),
            ('Table output', 'sql'),
            ('Execute SQL script', 'script'),
            ('MySQL', 'sql'),
            ('PostgreSQL', 'sql'),
            ('Oracle', 'sql'),
        ]
        
        # 方法1：查找entry元素
        for entry in self.root.findall('.//entry'):
            entry_type = entry.get('type', '')
            entry_text = entry.text.strip() if entry.text else ''
            
            # 修复XML特殊字符
            entry_text = fix_xml_special_chars(entry_text)
            
            # 检查是否为SQL相关
            for pattern, sql_type in sql_patterns:
                if pattern.lower() in entry_type.lower() and entry_text:
                    sql_component = {
                        'type': entry_type,
                        'sql_type': sql_type,
                        'content': entry_text,
                        'location': 'entry',
                        'length': len(entry_text),
                    }
                    self.sql_components.append(sql_component)
                    logger.debug(f"从entry找到SQL组件: {entry_type}")
        
        # 方法2：查找field元素中的SQL
        for field in self.root.findall('.//field'):
            field_name = field.get('name', '')
            field_text = field.text.strip() if field.text else ''
            
            # 修复XML特殊字符
            field_text = fix_xml_special_chars(field_text)
            
            # 检查是否为SQL字段
            if field_text and any(keyword in field_name.lower() for keyword in ['sql', 'query', 'script']):
                sql_component = {
                    'type': f"field:{field_name}",
                    'sql_type': 'field_sql',
                    'content': field_text,
                    'location': f"field/{field_name}",
                    'length': len(field_text),
                }
                self.sql_components.append(sql_component)
                logger.debug(f"从field找到SQL组件: {field_name}")
        
        # 方法3：查找steps中的SQL
        for step in self.root.findall('.//step'):
            step_type = step.get('type', '')
            step_name = step.get('name', '')
            
            # 查找step中的SQL字段
            for field in step.findall('.//field'):
                field_name = field.get('name', '')
                field_text = field.text.strip() if field.text else ''
                
                # 修复XML特殊字符
                field_text = fix_xml_special_chars(field_text)
                
                if field_text and any(keyword in field_name.lower() for keyword in ['sql', 'query', 'script']):
                    sql_component = {
                        'type': f"{step_type}:{step_name}",
                        'sql_type': 'step_sql',
                        'content': field_text,
                        'location': f"step/{step_name}/{field_name}",
                        'length': len(field_text),
                    }
                    self.sql_components.append(sql_component)
                    logger.debug(f"从step找到SQL组件: {step_type}/{step_name}")
        
        logger.info(f"共找到 {len(self.sql_components)} 个SQL组件")
        return self.sql_components
    
    def get_steps_info(self) -> List[Dict]:
        """获取作业步骤信息"""
        if not self.root:
            return []
        
        self.steps = []
        
        for step in self.root.findall('.//step'):
            step_info = {
                'name': step.get('name', ''),
                'type': step.get('type', ''),
                'description': step.get('description', ''),
            }
            self.steps.append(step_info)
        
        return self.steps
    
    def get_job_info(self) -> Dict:
        """获取作业基本信息"""
        if not self.root:
            return {}
        
        job_info = {
            'filename': self.kettle_file.name,
            'filepath': str(self.kettle_file),
            'filesize': self.kettle_file.stat().st_size,
            'modified_time': self.kettle_file.stat().st_mtime,
            'step_count': len(self.root.findall('.//step')),
            'entry_count': len(self.root.findall('.//entry')),
            'sql_component_count': len(self.sql_components),
        }
        
        # 尝试获取作业名称
        for step in self.root.findall('.//step'):
            if step.get('type', '').lower() == 'jobentryjob':
                job_name = step.get('name', '')
                if job_name:
                    job_info['job_name'] = job_name
                    break
        
        return job_info
    
    def save_extracted_sql(self, output_file: str, format: str = 'text') -> bool:
        """保存提取的SQL"""
        try:
            output_path = Path(output_file)
            
            if format == 'json':
                data = {
                    'job_info': self.get_job_info(),
                    'sql_components': self.sql_components,
                    'steps': self.get_steps_info(),
                }
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            
            else:  # text格式
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(f"Kettle文件: {self.kettle_file.name}\n")
                    f.write(f"SQL组件数量: {len(self.sql_components)}\n")
                    f.write("=" * 80 + "\n\n")
                    
                    for i, comp in enumerate(self.sql_components, 1):
                        f.write(f"SQL组件 {i}: {comp['type']}\n")
                        f.write(f"位置: {comp['location']}\n")
                        f.write(f"长度: {comp['length']} 字符\n")
                        f.write("-" * 40 + "\n")
                        f.write(comp['content'])
                        f.write("\n\n" + "=" * 80 + "\n\n")
            
            logger.info(f"SQL已保存到: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"保存SQL失败: {e}")
            return False
    
    def analyze_sql_components(self) -> Dict:
        """分析SQL组件"""
        if not self.sql_components:
            return {}
        
        analysis = {
            'total_components': len(self.sql_components),
            'component_types': {},
            'total_length': 0,
            'avg_length': 0,
            'tables_mentioned': [],
            'keywords_found': [],
        }
        
        # 统计组件类型
        for comp in self.sql_components:
            comp_type = comp['type']
            analysis['component_types'][comp_type] = analysis['component_types'].get(comp_type, 0) + 1
            analysis['total_length'] += comp['length']
            
            # 提取表名（简单正则匹配）
            sql_content = comp['content'].upper()
            table_matches = re.findall(r'\b(FROM|JOIN|INTO|UPDATE)\s+([A-Za-z0-9_.]+)', sql_content)
            for _, table in table_matches:
                if '.' in table:
                    table = table.split('.')[-1]  # 去掉schema前缀
                if table not in analysis['tables_mentioned']:
                    analysis['tables_mentioned'].append(table)
            
            # 提取关键字
            keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'DROP', 'ALTER', 'TRUNCATE']
            for keyword in keywords:
                if keyword in sql_content and keyword not in analysis['keywords_found']:
                    analysis['keywords_found'].append(keyword)
        
        # 计算平均长度
        if analysis['total_components'] > 0:
            analysis['avg_length'] = analysis['total_length'] // analysis['total_components']
        
        return analysis


def main():
    """命令行入口点"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Kettle XML解析器 - 纯SQL提取工具')
    parser.add_argument('kettle_file', help='Kettle文件路径 (.kjb 或 .ktr)')
    parser.add_argument('-o', '--output', help='输出文件路径')
    parser.add_argument('-f', '--format', choices=['text', 'json'], default='text', help='输出格式')
    parser.add_argument('-v', '--verbose', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    # 设置日志级别
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # 解析文件
    parser = KettleXMLParser(args.kettle_file)
    if not parser.parse():
        print(f"❌ 无法解析文件: {args.kettle_file}")
        return 1
    
    # 提取SQL
    sql_components = parser.extract_sql_components()
    if not sql_components:
        print(f"⚠️ 文件中未找到SQL组件")
        return 0
    
    # 输出信息
    job_info = parser.get_job_info()
    print(f"✅ 成功解析: {job_info['filename']}")
    print(f"📊 SQL组件数: {len(sql_components)}")
    
    # 分析SQL
    analysis = parser.analyze_sql_components()
    print(f"📝 总字符数: {analysis['total_length']}")
    print(f"📈 平均长度: {analysis['avg_length']}")
    
    if analysis['tables_mentioned']:
        print(f"📋 涉及表名: {', '.join(analysis['tables_mentioned'][:5])}")
        if len(analysis['tables_mentioned']) > 5:
            print(f"   ... 还有 {len(analysis['tables_mentioned']) - 5} 个表")
    
    # 保存输出
    if args.output:
        output_file = args.output
    else:
        output_file = Path(args.kettle_file).stem + f"_extracted_sql.{args.format}"
    
    if parser.save_extracted_sql(output_file, args.format):
        print(f"💾 结果已保存到: {output_file}")
    else:
        print(f"❌ 保存失败")
        return 1
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())