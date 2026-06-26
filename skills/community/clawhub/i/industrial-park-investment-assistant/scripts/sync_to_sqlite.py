#!/usr/bin/env python3
"""
SQLite 同步脚本 v2.15.0
将腾讯文档数据同步到本地 SQLite 数据库

用法：
  python3 sync_to_sqlite.py --project <项目ID> --table <表名>
  python3 sync_to_sqlite.py --project <项目ID> --all

示例：
  python3 sync_to_sqlite.py --project meilan-center --all
  python3 sync_to_sqlite.py --project meilan-center --table 房源销控表
"""

import os
import sys
import json
import argparse
from pathlib import Path

# 添加 scripts 目录到 path，以便导入 knowledge_base
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SKILL_DIR))
sys.path.insert(0, str(SCRIPT_DIR))

from knowledge_base import get_knowledge_base, SQLiteSource


# 需要同步的表列表（按依赖顺序）
TABLES = [
    "房源销控表",
    "客户跟进记录",
    "渠道跟进记录",   # v2.16.0 新增
    "租金报价表",
    "配套资源表",
    "产业政策库",
]


def sync_table(kb, table_name, data=None):
    """
    同步单个表到 SQLite
    
    :param kb: KnowledgeBase 实例
    :param table_name: 表名
    :param data: 已获取的数据（可选，如果为 None 则从数据源加载）
    :return: (success, record_count, error)
    """
    print(f"  📥 同步 [{table_name}]...")
    
    try:
        # 如果没有传入数据，则从数据源加载
        if data is None:
            data, error = kb.load(table_name, use_cache=False)
            if error:
                return False, 0, error
        
        # 保存到 SQLite
        sqlite_source = SQLiteSource(kb.project_dir, kb.config)
        sqlite_source.save_data(table_name, data)
        
        record_count = data.get("total", 0)
        print(f"    ✅ 同步完成：{record_count} 条记录")
        return True, record_count, None
        
    except Exception as e:
        error_msg = f"同步失败：{str(e)}"
        print(f"    ❌ {error_msg}")
        return False, 0, error_msg


def sync_all(kb):
    """
    同步所有表到 SQLite
    
    :param kb: KnowledgeBase 实例
    :return: (success_count, total_count, errors)
    """
    print(f"📊 开始同步项目 [{kb.project_id}] 的所有数据表...")
    print(f"   数据库：{os.path.join(kb.project_dir, 'local_db.sqlite')}")
    print()
    
    success_count = 0
    total_count = 0
    errors = []
    
    for table_name in TABLES:
        success, count, error = sync_table(kb, table_name)
        
        if success:
            success_count += 1
            total_count += count
        else:
            errors.append((table_name, error))
    
    print()
    print(f"📊 同步完成：{success_count}/{len(TABLES)} 个表成功，共 {total_count} 条记录")
    
    if errors:
        print(f"⚠️  失败：{len(errors)} 个表")
        for table_name, error in errors:
            print(f"   - {table_name}：{error}")
    
    return success_count, total_count, errors


def check_sqlite_status(kb):
    """
    检查 SQLite 数据库状态
    
    :param kb: KnowledgeBase 实例
    :return: 状态信息字典
    """
    sqlite_source = SQLiteSource(kb.project_dir, kb.config)
    return sqlite_source.get_info()


def main():
    parser = argparse.ArgumentParser(description='SQLite 同步脚本')
    parser.add_argument('--project', type=str, default=None, help='项目 ID')
    parser.add_argument('--table', type=str, default=None, choices=TABLES + [None], help='要同步的表名（不指定则同步所有表）')
    parser.add_argument('--all', action='store_true', help='同步所有表')
    parser.add_argument('--status', action='store_true', help='查看数据库状态')
    
    args = parser.parse_args()
    
    # 创建 KnowledgeBase 实例
    kb = get_knowledge_base(args.project)
    
    print(f"📊 知识库：{kb.project_id} ({kb.config.get('project_name', kb.project_id)})")
    print()
    
    # 查看状态
    if args.status:
        status = check_sqlite_status(kb)
        print("📊 SQLite 数据库状态：")
        print(f"   路径：{status['db_path']}")
        print(f"   存在：{status['db_exists']}")
        print(f"   大小：{status['db_size_mb']} MB")
        print(f"   各表记录数：{status['table_counts']}")
        return
    
    # 同步所有表
    if args.all or args.table is None:
        sync_all(kb)
    else:
        # 同步单个表
        sync_table(kb, args.table)


if __name__ == '__main__':
    main()
