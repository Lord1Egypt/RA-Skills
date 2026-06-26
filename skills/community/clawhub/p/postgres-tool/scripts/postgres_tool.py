#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PostgreSQL 数据库工具

功能：
- 执行 SELECT 查询
- 查看表结构
- 导出查询结果为 CSV/Excel
- 执行 UPDATE/DELETE 操作（需用户确认 + 自动备份）
- 数据恢复功能
"""

import argparse
import json
import sys
import os
from datetime import datetime
from pathlib import Path

# 获取技能目录的根路径（scripts 目录的父目录）
SKILL_ROOT = Path(__file__).parent.parent.resolve()

try:
    import psycopg2
    from psycopg2 import sql
except ImportError:
    print("错误：请先安装 psycopg2-binary")
    print("运行：pip install psycopg2-binary")
    sys.exit(1)

try:
    import pandas as pd
except ImportError:
    print("错误：请先安装 pandas")
    print("运行：pip install pandas")
    sys.exit(1)


def get_config_search_paths():
    """获取配置文件的搜索路径列表（按优先级排序）"""
    paths = []
    
    # 1. 当前工作目录（最高优先级，方便用户覆盖）
    paths.append(Path.cwd() / 'db_config.json')
    
    # 2. 技能目录下的 config 子目录（推荐位置）
    paths.append(SKILL_ROOT / 'config' / 'db_config.json')
    
    # 3. 技能根目录（兼容旧配置）
    paths.append(SKILL_ROOT / 'db_config.json')
    
    return paths


def find_config_file(config_file=None):
    """查找配置文件，返回实际存在的路径
    
    Args:
        config_file: 用户指定的配置文件路径（可选）
    
    Returns:
        Path: 配置文件的完整路径
    """
    if config_file:
        # 用户指定了配置文件路径
        config_path = Path(config_file)
        if not config_path.is_absolute():
            # 相对路径：先相对于当前工作目录，再相对于技能目录
            cwd_path = Path.cwd() / config_path
            if cwd_path.exists():
                return cwd_path
            skill_path = SKILL_ROOT / config_path
            if skill_path.exists():
                return skill_path
        if config_path.exists():
            return config_path
        return None
    
    # 自动搜索配置文件
    for path in get_config_search_paths():
        if path.exists():
            return path
    
    return None


def load_config(config_file=None):
    """加载数据库配置文件
    
    搜索顺序：
    1. 当前工作目录下的 db_config.json
    2. 技能目录/config/db_config.json（推荐）
    3. 技能目录/db_config.json（兼容）
    """
    config_path = find_config_file(config_file)
    
    if config_path is None:
        print("错误：找不到配置文件 db_config.json")
        print("\n搜索了以下位置：")
        for path in get_config_search_paths():
            status = "✓ 存在" if path.exists() else "✗ 不存在"
            print(f"  {status} {path}")
        print("\n请创建 db_config.json 文件，示例：")
        print(json.dumps({
            "host": "localhost",
            "port": 5432,
            "database": "your_database",
            "user": "your_username",
            "password": "your_password"
        }, indent=2))
        print(f"\n推荐位置：{SKILL_ROOT / 'config' / 'db_config.json'}")
        sys.exit(1)
    
    print(f"使用配置文件：{config_path}")
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_connection(config=None):
    """获取数据库连接"""
    if config is None:
        config = load_config()
    
    try:
        conn = psycopg2.connect(
            host=config['host'],
            port=config['port'],
            database=config['database'],
            user=config['user'],
            password=config['password']
        )
        return conn
    except Exception as e:
        print(f"连接数据库失败：{e}")
        sys.exit(1)


def execute_query(query, config=None, auto_limit=True):
    """执行 SQL 查询并返回 DataFrame"""
    # 安全检查：只允许 SELECT 查询
    query_upper = query.strip().upper()
    if not query_upper.startswith('SELECT') and not query_upper.startswith('WITH'):
        print("错误：为了安全起见，只允许执行 SELECT 查询")
        print("如需执行 UPDATE/DELETE 操作，请使用 --update 或 --delete 参数")
        sys.exit(1)
    
    conn = None
    try:
        if config is None:
            config = load_config()
        
        conn = get_connection(config)
        
        # 自动添加 LIMIT 防止返回过多数据（如果没有的话）
        # 注意：如果查询已经有分号，需要在分号前添加 LIMIT
        if auto_limit and 'LIMIT' not in query_upper and 'limit' not in query:
            query = query.rstrip().rstrip(';') + ' LIMIT 1000'
        
        df = pd.read_sql_query(query, conn)
        return df
    
    except Exception as e:
        print(f"查询执行失败：{e}")
        sys.exit(1)
    finally:
        if conn:
            conn.close()


def list_tables(config=None):
    """列出所有表"""
    query = """
    SELECT table_schema, table_name 
    FROM information_schema.tables 
    WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
    ORDER BY table_schema, table_name;
    """
    return execute_query(query, config)


def get_table_schema(table_name, config=None):
    """获取表结构信息"""
    query = """
    SELECT 
        column_name AS "列名",
        data_type AS "数据类型",
        is_nullable AS "允许 NULL",
        column_default AS "默认值",
        character_maximum_length AS "最大长度",
        numeric_precision AS "数值精度",
        numeric_scale AS "数值尺度"
    FROM information_schema.columns
    WHERE table_name = %s
    ORDER BY ordinal_position;
    """
    
    conn = None
    try:
        if config is None:
            config = load_config()
        
        conn = get_connection(config)
        cursor = conn.cursor()
        cursor.execute(query, (table_name,))
        
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        
        df = pd.DataFrame(rows, columns=columns)
        return df
    
    except Exception as e:
        print(f"获取表结构失败：{e}")
        sys.exit(1)
    finally:
        if conn:
            conn.close()


def export_to_csv(df, filename):
    """导出为 CSV 文件"""
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"✓ 已导出到：{filename}")


def export_to_excel(df, filename, sheet_name='Sheet1'):
    """导出为 Excel 文件"""
    try:
        df.to_excel(filename, index=False, sheet_name=sheet_name, engine='openpyxl')
        print(f"✓ 已导出到：{filename}")
    except ImportError:
        print("错误：导出 Excel 需要安装 openpyxl")
        print("运行：pip install openpyxl")
        sys.exit(1)


def create_backup_directory():
    """创建备份目录（在技能目录下）"""
    backup_dir = SKILL_ROOT / "backups" / datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir.mkdir(parents=True, exist_ok=True)
    return backup_dir


def backup_table(table_name, where_clause=None, config=None, backup_dir=None):
    """备份表数据
    
    Args:
        table_name: 表名
        where_clause: WHERE 条件（可选），用于备份特定数据
        config: 数据库配置
        backup_dir: 备份目录（可选）
    
    Returns:
        backup_file: 备份文件路径
        record_count: 备份的记录数
    """
    if backup_dir is None:
        backup_dir = create_backup_directory()
    
    # 生成备份文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_table_name = table_name.replace(' ', '_').lower()
    
    if where_clause:
        # 为带条件的备份生成唯一名称
        import hashlib
        condition_hash = hashlib.md5(where_clause.encode()).hexdigest()[:8]
        backup_file = backup_dir / f"{safe_table_name}_{condition_hash}_{timestamp}.csv"
    else:
        backup_file = backup_dir / f"{safe_table_name}_all_{timestamp}.csv"
    
    # 查询要备份的数据
    if where_clause:
        query = f"SELECT * FROM {table_name} WHERE {where_clause};"
    else:
        query = f"SELECT * FROM {table_name};"
    
    print(f"正在备份数据：{table_name}")
    df = execute_query(query, config=config, auto_limit=False)
    
    if df.empty:
        print("⚠️  警告：没有数据需要备份")
        return None, 0
    
    # 保存为 CSV
    df.to_csv(backup_file, index=False, encoding='utf-8-sig')
    
    print(f"✓ 已备份 {len(df)} 条记录到：{backup_file}")
    
    # 保存备份元数据
    metadata = {
        'table_name': table_name,
        'backup_time': datetime.now().isoformat(),
        'record_count': len(df),
        'where_clause': where_clause,
        'backup_file': str(backup_file),
        'columns': list(df.columns)
    }
    
    metadata_file = backup_file.with_suffix('.meta.json')
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 已保存备份元数据：{metadata_file}")
    
    return str(backup_file), len(df)


def restore_from_backup(backup_file, config=None, dry_run=False, mode='update'):
    """从备份恢复数据
    
    Args:
        backup_file: 备份文件路径（CSV 或 JSON 元数据文件）
        config: 数据库配置
        dry_run: 如果为 True，只显示不执行
        mode: 恢复模式 ('insert' | 'update' | 'replace')
            - insert: 仅插入新记录，跳过已存在的记录
            - update: 更新已存在的记录，插入新记录
            - replace: 先删除已存在的记录，再插入（默认）
    """
    backup_path = Path(backup_file)
    
    # 确定元数据文件
    if backup_path.suffix == '.json':
        metadata_file = backup_path
        csv_file = backup_path.with_suffix('.csv')
    else:
        csv_file = backup_path
        metadata_file = backup_path.with_suffix('.meta.json')
    
    if not csv_file.exists():
        print(f"错误：找不到备份文件 {csv_file}")
        return False, 0
    
    # 加载元数据
    metadata = {}
    if metadata_file.exists():
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
    
    table_name = metadata.get('table_name', 'unknown')
    print(f"准备恢复表：{table_name}")
    print(f"备份时间：{metadata.get('backup_time', '未知')}")
    print(f"记录数：{metadata.get('record_count', '未知')}")
    
    # 读取备份数据
    df = pd.read_csv(csv_file, encoding='utf-8-sig')
    
    if df.empty:
        print("⚠️  警告：备份文件为空")
        return False, 0
    
    if dry_run:
        print(f"\n【预览模式】将恢复 {len(df)} 条记录")
        print("前 5 条记录预览：")
        print(df.head())
        return True, len(df)
    
    # 确认恢复
    print(f"\n⚠️  警告：即将恢复 {len(df)} 条记录到表 {table_name}")
    print(f"恢复模式：{mode}")
    if mode == 'replace':
        print("⚠️  注意：replace 模式会先删除已存在的记录")
    response = input("确认恢复？(yes/no): ").strip().lower()
    if response != 'yes':
        print("已取消恢复操作")
        return False, 0
    
    conn = None
    try:
        if config is None:
            config = load_config()
        
        conn = get_connection(config)
        cursor = conn.cursor()
        
        restored_count = 0
        skipped_count = 0
        for _, row in df.iterrows():
            # 构建 INSERT 语句
            columns = list(row.index)
            values = list(row.values)
            
            # 处理 NULL 值
            values = [None if pd.isna(v) else v for v in values]
            
            # 构建 SQL
            placeholders = ['%s'] * len(columns)
            columns_str = ', '.join(columns)
            values_str = ', '.join(placeholders)
            
            try:
                if mode == 'replace':
                    # 先删除已存在的记录
                    primary_key_cols = ['fid']  # 假设主键是 fid
                    delete_query = f"""
                        DELETE FROM {table_name}
                        WHERE fid = %s
                    """
                    cursor.execute(delete_query, (row.get('fid'),))
                
                if mode in ('insert', 'replace'):
                    sql_query = f"""
                        INSERT INTO {table_name} ({columns_str})
                        VALUES ({values_str})
                    """
                    cursor.execute(sql_query, values)
                elif mode == 'update':
                    # 使用 ON CONFLICT DO UPDATE
                    primary_key = 'fid'
                    update_cols = [c for c in columns if c != primary_key]
                    update_set = ', '.join([f"{col} = EXCLUDED.{col}" for col in update_cols])
                    sql_query = f"""
                        INSERT INTO {table_name} ({columns_str})
                        VALUES ({values_str})
                        ON CONFLICT ({primary_key}) DO UPDATE SET {update_set}
                    """
                    cursor.execute(sql_query, values)
                
                restored_count += 1
            except Exception as e:
                print(f"⚠️  恢复单条记录失败：{e}")
                if 'duplicate key' in str(e).lower() or 'conflict' in str(e).lower():
                    skipped_count += 1
                continue
        
        conn.commit()
        if skipped_count > 0:
            print(f"✓ 成功恢复 {restored_count}/{len(df)} 条记录，跳过 {skipped_count} 条重复记录")
        else:
            print(f"✓ 成功恢复 {restored_count}/{len(df)} 条记录")
        
        return True, restored_count
        
    except Exception as e:
        print(f"恢复失败：{e}")
        if conn:
            conn.rollback()
        return False, 0
    finally:
        if conn:
            conn.close()


def execute_update_delete(query, operation_type, table_name=None, config=None, force=False):
    """执行 UPDATE 或 DELETE 操作（带备份和确认）
    
    Args:
        query: SQL 查询（UPDATE 或 DELETE）
        operation_type: 'UPDATE' 或 'DELETE'
        table_name: 表名（用于备份）
        config: 数据库配置
        force: 如果为 True，跳过确认（危险！）
    """
    query_upper = query.strip().upper()
    
    # 验证操作类型
    if operation_type == 'UPDATE' and not query_upper.startswith('UPDATE'):
        print(f"错误：操作类型是 UPDATE，但查询不是以 UPDATE 开头")
        return False
    
    if operation_type == 'DELETE' and not query_upper.startswith('DELETE'):
        print(f"错误：操作类型是 DELETE，但查询不是以 DELETE 开头")
        return False
    
    # 提取 WHERE 条件
    where_clause = None
    if 'WHERE' in query_upper:
        where_idx = query_upper.find('WHERE') + 6
        where_clause = query[where_idx:].strip()
    
    # 备份受影响的数据
    print("\n【安全保护】在执行修改/删除操作前，先备份数据...")
    
    if operation_type == 'DELETE' and where_clause:
        # DELETE 操作：备份将被删除的数据
        select_query = f"SELECT * FROM {table_name} WHERE {where_clause};"
    elif operation_type == 'UPDATE' and where_clause:
        # UPDATE 操作：备份将更新的记录
        select_query = f"SELECT * FROM {table_name} WHERE {where_clause};"
    else:
        # 没有 WHERE 条件，备份整个表
        select_query = f"SELECT * FROM {table_name};"
    
    backup_file, record_count = backup_table(
        table_name=table_name,
        where_clause=where_clause,
        config=config
    )
    
    if record_count == 0:
        print("⚠️  警告：没有数据受影响，操作已取消")
        return False
    
    # 显示将要执行的操作
    print(f"\n【操作确认】")
    print(f"操作类型：{operation_type}")
    print(f"影响记录数：约 {record_count} 条")
    print(f"备份文件：{backup_file}")
    print(f"SQL: {query}")
    
    # 请求用户确认
    if not force:
        print("\n⚠️  ⚠️  ⚠️  警告：此操作将修改/删除数据库中的数据！")
        response = input(f"确认执行 {operation_type} 操作？输入 'yes' 确认：").strip().lower()
        
        if response != 'yes':
            print("已取消操作")
            print(f"备份文件已保留：{backup_file}")
            print(f"如需恢复，使用命令：python query_postgres.py --restore {backup_file}")
            return False
    
    # 执行操作
    print(f"\n正在执行 {operation_type} 操作...")
    
    conn = None
    try:
        if config is None:
            config = load_config()
        
        conn = get_connection(config)
        cursor = conn.cursor()
        
        cursor.execute(query)
        affected_rows = cursor.rowcount
        
        conn.commit()
        print(f"✓ 成功执行 {operation_type}，影响 {affected_rows} 行")
        print(f"✓ 备份已保存：{backup_file}")
        print(f"  如需恢复，使用：python query_postgres.py --restore {backup_file}")
        
        return True, affected_rows
        
    except Exception as e:
        print(f"{operation_type} 失败：{e}")
        if conn:
            conn.rollback()
            print("已回滚操作")
        print(f"备份文件：{backup_file}")
        return False, 0
    finally:
        if conn:
            conn.close()


def main():
    parser = argparse.ArgumentParser(
        description='PostgreSQL 数据库查询工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python query_postgres.py "SELECT * FROM users LIMIT 10;"
  python query_postgres.py --list-tables
  python query_postgres.py --schema users
  python query_postgres.py "SELECT * FROM users;" --output result.csv
  python query_postgres.py "SELECT * FROM users;" --output result.xlsx
        """
    )
    
    parser.add_argument('query', nargs='?', help='SQL 查询语句')
    parser.add_argument('--config', '-c', default=None,
                       help='配置文件路径 (默认：自动搜索 db_config.json)')
    parser.add_argument('--list-tables', '-l', action='store_true',
                       help='列出所有表')
    parser.add_argument('--schema', '-s', metavar='TABLE',
                       help='查看指定表的结构')
    parser.add_argument('--output', '-o', metavar='FILE',
                       help='导出结果到文件 (支持 .csv 和 .xlsx)')
    parser.add_argument('--no-limit', action='store_true',
                       help='不自动添加 LIMIT 子句')
    
    # 新增：修改和删除功能参数
    parser.add_argument('--update', metavar='SQL',
                       help='执行 UPDATE 操作（会自动备份并请求确认）')
    parser.add_argument('--delete', metavar='SQL',
                       help='执行 DELETE 操作（会自动备份并请求确认）')
    parser.add_argument('--table', metavar='TABLE',
                       help='指定表名（用于 --update 和 --delete 操作）')
    parser.add_argument('--restore', metavar='BACKUP_FILE',
                       help='从备份文件恢复数据')
    parser.add_argument('--restore-mode', choices=['insert', 'update', 'replace'],
                       default='update',
                       help='恢复模式：insert-仅插入新记录，update-更新已存在记录，replace-先删除再插入（默认：update）')
    parser.add_argument('--force', action='store_true',
                       help='强制执行，跳过确认（危险！）')
    parser.add_argument('--dry-run', action='store_true',
                       help='预览模式，不实际执行操作')
    
    args = parser.parse_args()
    
    # 加载配置
    config = load_config(args.config)
    
    # 恢复数据
    if args.restore:
        print(f"准备从备份恢复：{args.restore}")
        success, count = restore_from_backup(
            args.restore, 
            config=config, 
            dry_run=args.dry_run,
            mode=args.restore_mode
        )
        if success:
            print(f"\n✓ 恢复完成，共 {count} 条记录")
        else:
            print("\n✗ 恢复失败或已取消")
        return
    
    # 执行 UPDATE 操作
    if args.update:
        if not args.table:
            print("错误：--update 需要配合 --table 参数指定表名")
            sys.exit(1)
        
        print(f"【UPDATE 操作】表：{args.table}")
        success, affected = execute_update_delete(
            args.update,
            'UPDATE',
            table_name=args.table,
            config=config,
            force=args.force
        )
        return
    
    # 执行 DELETE 操作
    if args.delete:
        if not args.table:
            print("错误：--delete 需要配合 --table 参数指定表名")
            sys.exit(1)
        
        print(f"【DELETE 操作】表：{args.table}")
        success, affected = execute_update_delete(
            args.delete,
            'DELETE',
            table_name=args.table,
            config=config,
            force=args.force
        )
        return
    
    # 列出所有表
    if args.list_tables:
        print("正在获取表列表...")
        df = list_tables(config)
        print(df.to_string(index=False))
        return
    
    # 查看表结构
    if args.schema:
        print(f"正在获取表 '{args.schema}' 的结构...")
        df = get_table_schema(args.schema, config)
        print(df.to_string(index=False))
        
        if args.output:
            if args.output.endswith('.csv'):
                export_to_csv(df, args.output)
            elif args.output.endswith('.xlsx'):
                export_to_excel(df, args.output)
            else:
                print("错误：输出文件必须是 .csv 或 .xlsx 格式")
                sys.exit(1)
        return
    
    # 执行查询
    if args.query:
        print(f"执行查询：{args.query}")
        df = execute_query(args.query, config)
        
        # 显示结果
        print(f"\n查询返回 {len(df)} 行数据:\n")
        print(df.to_string(index=False))
        
        # 导出结果
        if args.output:
            if args.output.endswith('.csv'):
                export_to_csv(df, args.output)
            elif args.output.endswith('.xlsx'):
                export_to_excel(df, args.output)
            else:
                print("错误：输出文件必须是 .csv 或 .xlsx 格式")
                sys.exit(1)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
