"""
Database Scanner - 数据库结构扫描器
扫描数据库相关文件，提取表结构信息
"""

import re
from pathlib import Path
from typing import Dict, List, Optional


class DatabaseScanner:
    """数据库结构扫描器"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.sql_files = []
        self.entity_files = []
        
    def scan(self) -> Dict:
        """执行数据库扫描"""
        result = {
            'db_type': self._detect_db_type(),
            'sql_files': [],
            'tables': [],
            'entities': [],
            'migrations': []
        }
        
        # 1. 扫描 SQL 文件
        self._scan_sql_files()
        result['sql_files'] = self.sql_files
        
        # 2. 扫描实体类
        self._scan_entity_files()
        result['entities'] = self.entity_files
        
        # 3. 解析表结构
        result['tables'] = self._parse_tables()
        
        # 4. 整理迁移记录
        result['migrations'] = self._get_migrations()
        
        return result
    
    def _detect_db_type(self) -> str:
        """检测数据库类型"""
        # 1. 扫描 SQL 文件判断
        for sql_file in self._find_sql_files():
            content = sql_file.read_text(encoding='utf-8', errors='ignore')
            
            if 'AUTO_INCREMENT' in content or 'ENGINE=InnoDB' in content or 'CHARSET=' in content:
                return 'MySQL'
            if 'SERIAL' in content or 'GENERATED ALWAYS' in content or '::regclass' in content:
                return 'PostgreSQL'
            if 'NUMBER GENERATED' in content or 'CLOB' in content:
                return 'Oracle'
            if 'IDENTITY(1,1)' in content or 'nvarchar' in content:
                return 'SQL Server'
        
        # 2. 扫描配置文件判断
        config_files = [
            'application.yml', 'application.properties',
            'application-dev.yml', 'application-prod.yml',
            'application-test.yml'
        ]
        
        for config_file in config_files:
            for yaml_path in self.project_path.rglob(config_file):
                content = yaml_path.read_text(encoding='utf-8', errors='ignore')
                
                if 'mysql' in content.lower():
                    return 'MySQL'
                if 'postgresql' in content.lower() or 'postgres' in content.lower():
                    return 'PostgreSQL'
                if 'oracle' in content.lower():
                    return 'Oracle'
                if 'sqlserver' in content.lower() or 'mssql' in content.lower():
                    return 'SQL Server'
        
        return 'Unknown'
    
    def _find_sql_files(self) -> List[Path]:
        """查找所有 SQL 文件"""
        sql_files = []
        
        # 常见 SQL 文件目录
        sql_dirs = ['db-migration', 'migrations', 'database', 'sql', 'scripts', 'docs']
        
        for sql_dir in sql_dirs:
            sql_path = self.project_path / sql_dir
            if sql_path.exists():
                sql_files.extend(sql_path.glob('*.sql'))
        
        # 直接在项目根目录查找
        sql_files.extend(self.project_path.glob('*.sql'))
        
        # 递归查找
        sql_files.extend(self.project_path.rglob('*.sql'))
        
        # 去重
        return list(set(sql_files))
    
    def _scan_sql_files(self) -> None:
        """扫描 SQL 文件"""
        self.sql_files = []
        
        for sql_file in self._find_sql_files():
            try:
                content = sql_file.read_text(encoding='utf-8', errors='ignore')
                
                tables = self._extract_tables(content)
                
                self.sql_files.append({
                    'path': str(sql_file),
                    'name': sql_file.name,
                    'tables': tables,
                    'size': sql_file.stat().st_size
                })
            except Exception as e:
                print(f"   ⚠️ 读取 SQL 文件失败: {sql_file} - {e}")
    
    def _extract_tables(self, content: str) -> List[Dict]:
        """从 SQL 内容中提取表结构"""
        tables = []
        
        # 匹配 CREATE TABLE 语句
        pattern = r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?[`"\[\]]?(\w+)[`"\[\]]?\s*\(([\s\S]*?)\)(?:\s*(?:ENGINE|DEFAULT|CHARSET|COLLATE|PARTITION)[^;]*)?;'
        
        matches = re.finditer(pattern, content, re.IGNORECASE)
        
        for match in matches:
            table_name = match.group(1)
            table_def = match.group(2)
            
            # 跳过系统表
            if table_name.startswith('_'):
                continue
            
            table_info = {
                'name': table_name,
                'schema': self._extract_schema(content),
                'columns': self._extract_columns(table_def),
                'indexes': self._extract_indexes(table_def, content),
                'constraints': self._extract_constraints(table_def, content)
            }
            
            tables.append(table_info)
        
        return tables
    
    def _extract_schema(self, content: str) -> Optional[str]:
        """提取 Schema"""
        schema_pattern = r'CREATE\s+TABLE\s+([\w.]+)\.'
        match = re.search(schema_pattern, content, re.IGNORECASE)
        return match.group(1) if match else None
    
    def _extract_columns(self, table_def: str) -> List[Dict]:
        """提取字段"""
        columns = []
        
        # 分割字段定义
        lines = table_def.split(',')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 跳过约束和索引定义
            if any(kw in line.upper() for kw in ['PRIMARY KEY', 'FOREIGN KEY', 'UNIQUE', 'INDEX', 'KEY', 'CONSTRAINT', 'CHECK']):
                continue
            
            # 解析字段
            col = self._parse_column(line)
            if col:
                columns.append(col)
        
        return columns
    
    def _parse_column(self, line: str) -> Optional[Dict]:
        """解析单个字段"""
        # 匹配字段定义
        pattern = r'[`"\[\]]?(\w+)[`"\[\]]?\s+(\w+(?:\([^)]+\))?)'
        match = re.search(pattern, line, re.IGNORECASE)
        
        if not match:
            return None
        
        col_name = match.group(1)
        col_type = match.group(2)
        
        # 判断是否主键
        is_primary = 'PRIMARY KEY' in line.upper()
        
        # 判断是否可空
        is_nullable = 'NOT NULL' not in line.upper()
        
        # 提取默认值
        default = None
        default_match = re.search(r"DEFAULT\s+('[^']*'|\S+)", line, re.IGNORECASE)
        if default_match:
            default = default_match.group(1)
        
        # 提取注释
        comment = None
        comment_match = re.search(r"COMMENT\s+['\"]([^'\"]+)['\"]", line, re.IGNORECASE)
        if comment_match:
            comment = comment_match.group(1)
        
        return {
            'name': col_name,
            'type': col_type,
            'nullable': is_nullable,
            'primary_key': is_primary,
            'default': default,
            'comment': comment
        }
    
    def _extract_indexes(self, table_def: str, full_content: str) -> List[Dict]:
        """提取索引"""
        indexes = []
        
        # 提取主键索引
        pk_pattern = r'PRIMARY\s+KEY\s*\(([^)]+)\)'
        for match in re.finditer(pk_pattern, table_def, re.IGNORECASE):
            indexes.append({
                'name': 'PRIMARY',
                'type': 'PRIMARY',
                'columns': [c.strip().strip('`"[]') for c in match.group(1).split(',')]
            })
        
        # 提取唯一索引
        unique_pattern = r'UNIQUE\s*(?:KEY|INDEX)?\s*[`"\[\]]?(\w*)[`"\[\]]?\s*\(([^)]+)\)'
        for match in re.finditer(unique_pattern, table_def, re.IGNORECASE):
            indexes.append({
                'name': match.group(1) or 'UNIQUE',
                'type': 'UNIQUE',
                'columns': [c.strip().strip('`"[]') for c in match.group(2).split(',')]
            })
        
        # 提取普通索引
        index_pattern = r'(?:KEY|INDEX)\s*[`"\[\]]?(\w+)[`"\[\]]?\s*\(([^)]+)\)'
        for match in re.finditer(index_pattern, table_def, re.IGNORECASE):
            indexes.append({
                'name': match.group(1),
                'type': 'INDEX',
                'columns': [c.strip().strip('`"[]') for c in match.group(2).split(',')]
            })
        
        return indexes
    
    def _extract_constraints(self, table_def: str, full_content: str) -> List[Dict]:
        """提取约束"""
        constraints = []
        
        # 外键约束
        fk_pattern = r'FOREIGN\s+KEY\s*\(([^)]+)\)\s*REFERENCES\s+([`"\[\]]?\w+[`"\[\]]?)\s*\(([^)]+)\)'
        for match in re.finditer(fk_pattern, table_def, re.IGNORECASE):
            constraints.append({
                'type': 'FOREIGN KEY',
                'column': match.group(1).strip().strip('`"[]'),
                'references': match.group(2).strip().strip('`"[]'),
                'references_column': match.group(3).strip().strip('`"[]')
            })
        
        return constraints
    
    def _scan_entity_files(self) -> None:
        """扫描实体类"""
        self.entity_files = []
        
        # Java 实体类位置
        entity_patterns = [
            '**/*DO.java',
            '**/*Entity.java',
            '**/*PO.java',
            '**/*DO*.java',
            '**/entity/*.java',
            '**/do/*.java',
            '**/domain/*.java'
        ]
        
        for pattern in entity_patterns:
            for entity_file in self.project_path.glob(pattern):
                if 'target' in str(entity_file) or 'test' in str(entity_file):
                    continue
                
                try:
                    content = entity_file.read_text(encoding='utf-8', errors='ignore')
                    
                    # 提取表名
                    table_match = re.search(r'@TableName\(["\']([^"\']+)["\']\)', content)
                    if table_match:
                        table_name = table_match.group(1)
                        
                        # 提取字段
                        fields = []
                        field_pattern = r'@TableField\(["\']([^"\']+)["\']\)\s*private\s+(\w+)\s+(\w+)'
                        for fm in re.finditer(field_pattern, content):
                            fields.append({
                                'column': fm.group(1),
                                'type': fm.group(2),
                                'name': fm.group(3)
                            })
                        
                        self.entity_files.append({
                            'path': str(entity_file),
                            'class_name': entity_file.stem,
                            'table_name': table_name,
                            'fields': fields
                        })
                except Exception as e:
                    print(f"   ⚠️ 读取实体类失败: {entity_file} - {e}")
    
    def _parse_tables(self) -> List[Dict]:
        """解析所有表的完整结构"""
        tables = []
        
        # 从 SQL 文件解析
        for sql_file in self.sql_files:
            tables.extend(sql_file['tables'])
        
        # 与实体类对照
        for table in tables:
            for entity in self.entity_files:
                if table['name'].upper() == entity['table_name'].upper():
                    table['entity'] = entity
        
        return tables
    
    def _get_migrations(self) -> List[Dict]:
        """获取迁移记录"""
        migrations = []
        
        for sql_file in self._find_sql_files():
            # 提取迁移文件名中的日期和说明
            filename = sql_file.stem
            match = re.match(r'(\d+)_([\d.]+)_([\w-]+)', filename)
            
            if match:
                migrations.append({
                    'version': match.group(1),
                    'date': match.group(2),
                    'description': match.group(3),
                    'file': str(sql_file)
                })
        
        return sorted(migrations, key=lambda x: x['version'])


# 导出
__all__ = ['DatabaseScanner']
