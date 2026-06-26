#!/usr/bin/env python3
"""
知识库抽象层 v1.0
支持多种数据源：腾讯文档、本地文件、API等
统一数据访问接口，实现知识库分离架构

优化 v1.1 (2026-06-12):
  - 添加文件缓存 + TTL检查（减少MCP调用）
  - 添加内存缓存（加速同一进程内的重复读取）
  - 添加缓存统计（命中率监控）

优化 v1.2 (2026-06-13):
  - 新增 SQLiteSource 数据源（本地数据库模式）
  - 支持零 token 超快查询（<0.1秒）
"""

import os
import sys
import json
import csv
import time
import sqlite3
from pathlib import Path
from datetime import datetime
from abc import ABC, abstractmethod


# Workspace 根目录
WORKSPACE_DIR = os.path.expanduser("~/.workbuddy/workspace/investment-assistant")


class DataSource(ABC):
    """数据源抽象基类"""
    
    @abstractmethod
    def load_data(self, sheet_name):
        """
        加载数据
        :param sheet_name: 数据表名称（如：房源销控表）
        :return: {"records": [...], "total": N, "format": "mcp"|"compact"}
        """
        pass
    
    @abstractmethod
    def save_data(self, sheet_name, data):
        """
        保存数据
        :param sheet_name: 数据表名称
        :param data: 数据内容
        """
        pass
    
    @abstractmethod
    def get_info(self):
        """
        获取数据源信息
        :return: {"type": "xxx", "description": "..."}
        """
        pass


class TencentDocSource(DataSource):
    """腾讯文档数据源（通过AI调用MCP获取）"""
    
    def __init__(self, project_dir, config):
        self.project_dir = project_dir
        self.config = config
        self.data_dir = os.path.join(project_dir, "data")
        os.makedirs(self.data_dir, exist_ok=True)
    
    def load_data(self, sheet_name):
        """
        从本地缓存加载数据（AI通过MCP获取后写入）
        """
        data_file = os.path.join(self.data_dir, f"{sheet_name}.json")
        
        if not os.path.exists(data_file):
            return None, (
                f"⚠️ 数据文件不存在：{data_file}\n"
                f"请让 AI 调用 MCP 读取腾讯文档：\n"
                f"  mcp__tencent-docs__smartsheet.list_records(\n"
                f"    file_id='{self.config.get(sheet_name, 'YOUR_DOC_ID')}',\n"
                f"    sheet_id='{self.config.get(sheet_name + '_sheet_id', 'YOUR_SHEET_ID')}',\n"
                f"    limit=100\n"
                f"  )"
            )
        
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # 检测数据格式
        raw_records = data.get("records", [])
        if raw_records and "field_values" in raw_records[0]:
            # MCP原始格式
            valid_records = [r for r in raw_records if r.get("field_values")]
            filtered_count = len(raw_records) - len(valid_records)
            data_format = "mcp"
        else:
            # 紧凑格式
            valid_records = raw_records
            filtered_count = 0
            data_format = "compact"
        
        return {
            "records": valid_records,
            "filtered_count": filtered_count,
            "total": len(valid_records),
            "format": data_format,
            "source": "tencent_doc",
            "cached_at": data.get("cached_at", "未知")
        }, None
    
    def save_data(self, sheet_name, data):
        """
        保存数据到本地缓存（AI调用MCP后写入）
        """
        data_file = os.path.join(self.data_dir, f"{sheet_name}.json")
        
        # 添加缓存时间戳
        if isinstance(data, dict):
            data["cached_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return data_file
    
    def get_info(self):
        return {
            "type": "tencent_doc",
            "description": "腾讯文档智能表格",
            "config": self.config,
            "data_dir": self.data_dir
        }
    
    def get_mcp_command(self, sheet_name):
        """生成MCP调用命令（供AI使用）"""
        doc_id = self.config.get(sheet_name, "YOUR_DOC_ID")
        sheet_id = self.config.get(f"{sheet_name}_sheet_id", "YOUR_SHEET_ID")
        
        return (
            f"mcp__tencent-docs__smartsheet.list_records(\n"
            f"  file_id='{doc_id}',\n"
            f"  sheet_id='{sheet_id}',\n"
            f"  limit=100,\n"
            f"  field_titles=['房间号', '楼层', '面积(㎡)', '状态', '业态', '租售类型', '底价(元/㎡/天)', '朝向', '备注']\n"
            f")"
        )


class LocalFileSource(DataSource):
    """本地文件数据源（JSON/CSV）"""
    
    def __init__(self, project_dir, config):
        self.project_dir = project_dir
        self.config = config
        self.data_dir = os.path.join(project_dir, "data")
        os.makedirs(self.data_dir, exist_ok=True)
    
    def load_data(self, sheet_name):
        """
        从本地文件加载数据（支持JSON和CSV）
        """
        # 查找文件
        file_path = self.config.get(sheet_name)
        if not file_path:
            # 尝试默认路径
            file_path = os.path.join(self.data_dir, f"{sheet_name}.json")
        
        if not os.path.isabs(file_path):
            file_path = os.path.join(self.project_dir, file_path)
        
        if not os.path.exists(file_path):
            return None, f"⚠️ 文件不存在：{file_path}"
        
        # 根据文件类型加载
        if file_path.endswith('.json'):
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # 检测数据格式
            raw_records = data if isinstance(data, list) else data.get("records", [])
            if raw_records and "field_values" in raw_records[0]:
                valid_records = [r for r in raw_records if r.get("field_values")]
                data_format = "mcp"
            else:
                valid_records = raw_records
                data_format = "compact"
            
            return {
                "records": valid_records,
                "total": len(valid_records),
                "format": data_format,
                "source": "local_file",
                "file_path": file_path
            }, None
        
        elif file_path.endswith('.csv'):
            records = []
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    records.append(row)
            
            return {
                "records": records,
                "total": len(records),
                "format": "compact",
                "source": "local_file",
                "file_path": file_path
            }, None
        
        else:
            return None, f"⚠️ 不支持的文件格式：{file_path}"
    
    def save_data(self, sheet_name, data):
        """
        保存数据到本地文件
        """
        file_path = self.config.get(sheet_name)
        if not file_path:
            file_path = os.path.join(self.data_dir, f"{sheet_name}.json")
        
        if not os.path.isabs(file_path):
            file_path = os.path.join(self.project_dir, file_path)
        
        # 根据文件类型保存
        if file_path.endswith('.json'):
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        
        elif file_path.endswith('.csv'):
            if isinstance(data, list) and data:
                fieldnames = data[0].keys()
                with open(file_path, "w", encoding="utf-8", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(data)
        
        return file_path
    
    def get_info(self):
        return {
            "type": "local_file",
            "description": "本地JSON/CSV文件",
            "config": self.config,
            "data_dir": self.data_dir
        }


class APISource(DataSource):
    """API数据源（未来扩展）"""
    
    def __init__(self, project_dir, config):
        self.project_dir = project_dir
        self.config = config
    
    def load_data(self, sheet_name):
        """
        从API加载数据（待实现）
        """
        return None, "⚠️ API数据源尚未实现"
    
    def save_data(self, sheet_name, data):
        """保存数据到API（待实现）"""
        raise NotImplementedError("API数据源尚未实现")
    
    def get_info(self):
        return {
            "type": "api",
            "description": "API接口（待实现）",
            "config": self.config
        }


class KnowledgeBase:
    """
    知识库统一接口
    根据项目配置自动选择合适的数据源
    
    优化 v1.1: 添加缓存机制（文件缓存 + 内存缓存）
    """
    
    # 类级别的内存缓存（跨实例共享）
    _shared_memory_cache = {}
    _cache_stats = {"hit": 0, "miss": 0}
    
    def __init__(self, project_id=None, cache_ttl=1800):
        """
        初始化知识库
        :param project_id: 项目ID，如果为None则使用默认项目
        :param cache_ttl: 缓存TTL（秒），默认1800秒（30分钟）
        """
        self.project_id = self._resolve_project_id(project_id)
        self.project_dir = os.path.join(WORKSPACE_DIR, "projects", self.project_id)
        
        # 缓存配置
        self.cache_ttl = cache_ttl
        self.cache_dir = os.path.join(self.project_dir, "cache")
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # 加载项目配置
        self.config = self._load_project_config()
        
        # 创建数据源
        self.source = self._create_data_source()
    
    def _resolve_project_id(self, project_id):
        """解析项目ID（如果为None则读取默认项目）"""
        if project_id is not None:
            return project_id
        
        # 读取全局配置
        global_config_file = os.path.join(WORKSPACE_DIR, "config.json")
        if os.path.exists(global_config_file):
            with open(global_config_file, "r", encoding="utf-8") as f:
                global_config = json.load(f)
                return global_config.get("default_project", "meilan-center")
        
        return "meilan-center"
    
    def _load_project_config(self):
        """加载项目配置"""
        config_file = os.path.join(self.project_dir, "config.json")
        
        if not os.path.exists(config_file):
            return {}
        
        with open(config_file, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def _create_data_source(self):
        """根据配置创建数据源"""
        source_type = self.config.get("knowledge_source", "tencent_doc")
        
        if source_type == "tencent_doc":
            return TencentDocSource(self.project_dir, self.config.get("tencent_doc", {}))
        
        elif source_type == "local_file":
            return LocalFileSource(self.project_dir, self.config.get("local_files", {}))
        
        elif source_type == "api":
            return APISource(self.project_dir, self.config.get("api", {}))
        
        else:
            # 默认使用腾讯文档
            return TencentDocSource(self.project_dir, self.config.get("tencent_doc", {}))
    
    def load(self, sheet_name, use_cache=True):
        """
        加载数据（统一接口，带缓存检查）
        :param sheet_name: 数据表名称
        :param use_cache: 是否使用缓存（默认True，设为False强制刷新）
        :return: (data, error)
        """
        # 第1步：检查内存缓存（最快）
        cache_key = f"{self.project_id}_{sheet_name}"
        if use_cache and cache_key in self.__class__._shared_memory_cache:
            self.__class__._cache_stats["hit"] += 1
            return self.__class__._shared_memory_cache[cache_key], None
        
        # 第2步：检查文件缓存（跨进程）
        if use_cache:
            cached_data, cache_error = self._load_from_cache(sheet_name)
            if not cache_error and cached_data:
                self.__class__._cache_stats["hit"] += 1
                # 更新内存缓存
                self.__class__._shared_memory_cache[cache_key] = cached_data
                return cached_data, None
        
        # 第3步：缓存未命中，从数据源加载
        self.__class__._cache_stats["miss"] += 1
        data, error = self.source.load_data(sheet_name)
        
        # 第4步：更新缓存
        if not error and data:
            self._update_cache(sheet_name, data)
        
        return data, error
    
    def _load_from_cache(self, sheet_name):
        """
        从文件缓存加载数据
        :return: (data, error)
        """
        cache_file = os.path.join(self.cache_dir, f"{sheet_name}.cache")
        
        if not os.path.exists(cache_file):
            return None, "缓存文件不存在"
        
        # 检查缓存是否过期
        cache_age = time.time() - os.path.getmtime(cache_file)
        if cache_age > self.cache_ttl:
            return None, f"缓存已过期（{cache_age:.0f}秒前，TTL={self.cache_ttl}秒）"
        
        # 读取缓存
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                cache_data = json.load(f)
            
            # 添加缓存元数据
            cache_data["_cache_info"] = {
                "cached_at": datetime.fromtimestamp(os.path.getmtime(cache_file)).strftime("%Y-%m-%d %H:%M:%S"),
                "cache_age_seconds": int(cache_age),
                "from_cache": True
            }
            
            return cache_data, None
        except Exception as e:
            return None, f"读取缓存失败：{str(e)}"
    
    def _update_cache(self, sheet_name, data):
        """
        更新缓存（文件缓存 + 内存缓存）
        """
        # 更新内存缓存
        cache_key = f"{self.project_id}_{sheet_name}"
        self.__class__._shared_memory_cache[cache_key] = data
        
        # 更新文件缓存
        cache_file = os.path.join(self.cache_dir, f"{sheet_name}.cache")
        try:
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"⚠️ 更新文件缓存失败：{str(e)}")
            return False
    
    def invalidate_cache(self, sheet_name=None):
        """
        使缓存失效
        :param sheet_name: 数据表名称，如果为None则清除所有缓存
        """
        if sheet_name:
            # 清除指定表的缓存
            cache_key = f"{self.project_id}_{sheet_name}"
            if cache_key in self.__class__._shared_memory_cache:
                del self.__class__._shared_memory_cache[cache_key]
            
            cache_file = os.path.join(self.cache_dir, f"{sheet_name}.cache")
            if os.path.exists(cache_file):
                os.remove(cache_file)
            
            return f"✅ 已清除 {sheet_name} 的缓存"
        else:
            # 清除所有缓存
            self.__class__._shared_memory_cache.clear()
            
            import shutil
            if os.path.exists(self.cache_dir):
                shutil.rmtree(self.cache_dir)
                os.makedirs(self.cache_dir, exist_ok=True)
            
            return f"✅ 已清除所有缓存"
    
    def get_cache_stats(self):
        """
        获取缓存统计信息
        """
        total = self.__class__._cache_stats["hit"] + self.__class__._cache_stats["miss"]
        hit_rate = self.__class__._cache_stats["hit"] / total if total > 0 else 0
        
        return {
            "hit_count": self.__class__._cache_stats["hit"],
            "miss_count": self.__class__._cache_stats["miss"],
            "total": total,
            "hit_rate": f"{hit_rate:.1%}",
            "memory_cache_keys": list(self.__class__._shared_memory_cache.keys())
        }
    
    def save(self, sheet_name, data, update_cache=True):
        """
        保存数据（统一接口）
        :param sheet_name: 数据表名称
        :param data: 数据内容
        :param update_cache: 是否同步更新缓存（默认True）
        :return: 保存路径
        """
        # 保存到数据源
        result = self.source.save_data(sheet_name, data)
        
        # 同步更新缓存
        if update_cache and result:
            self._update_cache(sheet_name, data)
        
        return result
    
    def get_info(self):
        """获取知识库信息"""
        return {
            "project_id": self.project_id,
            "project_name": self.config.get("project_name", self.project_id),
            "source": self.source.get_info(),
            "project_dir": self.project_dir
        }
    
    def switch_source(self, source_type):
        """
        切换数据源类型
        :param source_type: "tencent_doc" | "local_file" | "api"
        """
        self.config["knowledge_source"] = source_type
        
        # 保存配置
        config_file = os.path.join(self.project_dir, "config.json")
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
        
        # 重新创建数据源
        self.source = self._create_data_source()
        
        return self.get_info()


def parse_record_fields(record):
    """
    解析记录中的字段值（兼容两种格式）
    支持：MCP原始格式、紧凑格式
    """
    # 检测数据格式
    if "field_values" in record:
        # MCP原始格式
        fields = {}
        for fv in record.get("field_values", []):
            field_name = fv.get("field", "")
            # 尝试提取各种类型的值
            if "text_value" in fv:
                items = fv["text_value"].get("items", [])
                fields[field_name] = items[0]["text"] if items else ""
            elif "number_value" in fv:
                fields[field_name] = fv["number_value"]
            elif "option_value" in fv:
                items = fv["option_value"].get("items", [])
                fields[field_name] = items[0]["text"] if items else ""
            else:
                fields[field_name] = ""
        return fields
    else:
        # 紧凑格式：直接返回记录（排除 record_id）
        fields = {k: v for k, v in record.items() if k != "record_id"}
        return fields


def get_knowledge_base(project_id=None):
    """
    获取知识库实例（工厂函数）
    :param project_id: 项目ID
    :return: KnowledgeBase实例
    """
    return KnowledgeBase(project_id=project_id)


if __name__ == "__main__":
    # 测试代码
    import argparse
    
    parser = argparse.ArgumentParser(description='知识库抽象层测试')
    parser.add_argument('--project', type=str, default=None, help='项目ID')
    parser.add_argument('--action', type=str, default='info', choices=['info', 'load'], help='操作')
    parser.add_argument('--sheet', type=str, default='房源销控表', help='数据表名称')
    
    args = parser.parse_args()
    
    # 创建知识库实例
    kb = get_knowledge_base(args.project)
    
    # 执行操作
    if args.action == 'info':
        info = kb.get_info()
        print("📊 知识库信息:")
        print(json.dumps(info, ensure_ascii=False, indent=2))
    
    elif args.action == 'load':
        print(f"📥 加载数据: {args.sheet}")
        data, error = kb.load(args.sheet)
        
        if error:
            print(f"❌ 错误: {error}")
        else:
            print(f"✅ 成功加载 {data['total']} 条记录")
            print(f"   数据格式: {data['format']}")
            print(f"   数据来源: {data['source']}")
            
            if data.get('cached_at'):
                print(f"   缓存时间: {data['cached_at']}")


# ─────────────────────────────────────────────
# SQLite 数据源（v2.15.0 新增）
# ─────────────────────────────────────────────
class SQLiteSource(DataSource):
    """
    SQLite 本地数据库数据源
    提供超快查询（<0.1秒）和零 token 消耗
    
    数据库路径：~/.workbuddy/workspace/investment-assistant/local_db.sqlite
    """
    
    def __init__(self, project_dir, config):
        self.project_dir = project_dir
        self.config = config
        self.db_path = os.path.join(project_dir, "local_db.sqlite")
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # 确保数据库和表存在
        self._init_db()
    
    def _init_db(self):
        """初始化数据库表结构"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 房源销控表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS 房源销控表 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            record_id TEXT,
            房间号 TEXT,
            楼层 TEXT,
            "面积(㎡)" REAL,
            状态 TEXT,
            业态 TEXT,
            "租售类型" TEXT,
            "底价(元/㎡/天)" REAL,
            朝向 TEXT,
            备注 TEXT,
            _sync_time TEXT
        )
        """)
        
        # 客户跟进记录表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS 客户跟进记录 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            record_id TEXT,
            企业名称 TEXT,
            联系人 TEXT,
            电话 TEXT,
            行业 TEXT,
            "需求面积" TEXT,
            优先级 TEXT,
            "最后跟进日期" TEXT,
            阶段 TEXT,
            负责人 TEXT,
            _sync_time TEXT
        )
        """)
        
        # 租金报价表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS 租金报价表 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            record_id TEXT,
            区域 TEXT,
            "楼层区间" TEXT,
            "底价区间" TEXT,
            物业费 TEXT,
            _sync_time TEXT
        )
        """)
        
        # 配套资源表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS 配套资源表 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            record_id TEXT,
            配套名称 TEXT,
            配套类别 TEXT,
            详情 TEXT,
            _sync_time TEXT
        )
        """)
        
        # 产业政策库表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS 产业政策库 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            record_id TEXT,
            政策名称 TEXT,
            补贴金额 TEXT,
            申报条件 TEXT,
            _sync_time TEXT
        )
        """)

        # 渠道跟进记录表（v2.16.0 新增）
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS 渠道跟进记录 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            record_id TEXT,
            渠道名称 TEXT,
            对接人 TEXT,
            电话 TEXT,
            推荐客户数 INTEGER,
            成交数 INTEGER,
            佣金比例 TEXT,
            状态 TEXT,
            _sync_time TEXT
        )
        """)

        # 同步日志表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sync_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_name TEXT,
            sync_time TEXT,
            status TEXT,
            record_count INTEGER
        )
        """)
        
        conn.commit()
        conn.close()
    
    def load_data(self, sheet_name):
        """
        从 SQLite 加载数据
        返回格式与 TencentDocSource 兼容：{"records": [...], "total": N, "format": "sqlite"}
        """
        if not os.path.exists(self.db_path):
            return None, f"⚠️ 数据库不存在：{self.db_path}\n请先执行同步：python3 scripts/sync_to_sqlite.py"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 检查表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (sheet_name,))
        if not cursor.fetchone():
            conn.close()
            return None, f"⚠️ 数据表不存在：{sheet_name}\n请先执行同步：python3 scripts/sync_to_sqlite.py"
        
        # 读取数据
        cursor.execute(f"SELECT * FROM [{sheet_name}]")
        columns = [description[0] for description in cursor.description]
        
        records = []
        for row in cursor.fetchall():
            record = {}
            for i, col in enumerate(columns):
                if col.startswith('_'):
                    continue  # 跳过内部字段
                record[col] = row[i]
            
            # 添加 record_id（用于兼容）
            record_id_idx = columns.index('record_id') if 'record_id' in columns else -1
            if record_id_idx >= 0:
                record['record_id'] = row[record_id_idx]
            
            records.append(record)
        
        conn.close()
        
        return {
            "records": records,
            "total": len(records),
            "format": "sqlite",
            "source": "sqlite_local",
            "db_path": self.db_path
        }, None
    
    def save_data(self, sheet_name, data):
        """
        保存数据到 SQLite（全量覆盖）
        data 格式：{"records": [...], "format": "mcp"|"compact"}
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        sync_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 清空表
        cursor.execute(f"DELETE FROM [{sheet_name}]")
        
        # 插入数据
        records = data.get("records", [])
        for record in records:
            # 解析字段
            fields = parse_record_fields(record) if "field_values" in record else record
            
            # 构建 INSERT 语句
            columns = []
            values = []
            for key, val in fields.items():
                if key == 'record_id':
                    columns.append('record_id')
                    values.append(val)
                else:
                    columns.append(key)
                    values.append(val)
            
            columns.append('_sync_time')
            values.append(sync_time)
            
            placeholders = ','.join(['?'] * len(values))
            column_names = ','.join([f'[{c}]' for c in columns])
            
            cursor.execute(f"INSERT INTO [{sheet_name}] ({column_names}) VALUES ({placeholders})", values)
        
        # 更新同步日志
        cursor.execute("""
        INSERT INTO sync_log (table_name, sync_time, status, record_count)
        VALUES (?, ?, 'success', ?)
        """, (sheet_name, sync_time, len(records)))
        
        conn.commit()
        conn.close()
        
        return True
    
    def get_info(self):
        """获取数据源信息"""
        db_exists = os.path.exists(self.db_path)
        db_size = os.path.getsize(self.db_path) if db_exists else 0
        
        # 获取各表记录数
        table_counts = {}
        if db_exists:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            for table in tables:
                if table == 'sync_log':
                    continue
                cursor.execute(f"SELECT COUNT(*) FROM [{table}]")
                table_counts[table] = cursor.fetchone()[0]
            
            conn.close()
        
        return {
            "type": "sqlite",
            "description": "SQLite 本地数据库",
            "db_path": self.db_path,
            "db_exists": db_exists,
            "db_size_mb": round(db_size / 1024 / 1024, 2),
            "table_counts": table_counts
        }
    
    def is_fresh(self, max_age_hours=24):
        """
        检查数据库是否新鲜（最近N小时内同步过）
        """
        if not os.path.exists(self.db_path):
            return False
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT MAX(sync_time) FROM sync_log WHERE status = 'success'")
            result = cursor.fetchone()
            
            if not result or not result[0]:
                return False
            
            last_sync = datetime.fromisoformat(result[0])
            age_hours = (datetime.now() - last_sync).total_seconds() / 3600
            
            return age_hours < max_age_hours
        except:
            return False
        finally:
            conn.close()


# 打补丁：让 KnowledgeBase 支持 sqlite 数据源
def _patch_knowledge_base_for_sqlite():
    """给 KnowledgeBase 类打补丁，添加 SQLite 支持"""
    
    original_create_data_source = KnowledgeBase._create_data_source
    
    def new_create_data_source(self):
        source_type = self.config.get("knowledge_source", "tencent_doc")
        
        if source_type == "sqlite":
            return SQLiteSource(self.project_dir, self.config)
        else:
            return original_create_data_source(self)
    
    KnowledgeBase._create_data_source = new_create_data_source
    
    # 添加 SQLite 快捷方法
    def load_from_sqlite(self, sheet_name):
        """强制从 SQLite 加载（忽略缓存）"""
        if not isinstance(self.source, SQLiteSource):
            # 临时切换到 SQLite 数据源
            original_source = self.source
            self.source = SQLiteSource(self.project_dir, self.config)
            data, error = self.source.load_data(sheet_name)
            self.source = original_source
            return data, error
        else:
            return self.source.load_data(sheet_name)
    
    def sync_to_sqlite(self, sheet_name, data):
        """同步数据到 SQLite"""
        if not isinstance(self.source, SQLiteSource):
            sqlite_source = SQLiteSource(self.project_dir, self.config)
        else:
            sqlite_source = self.source
        
        return sqlite_source.save_data(sheet_name, data)
    
    KnowledgeBase.load_from_sqlite = load_from_sqlite
    KnowledgeBase.sync_to_sqlite = sync_to_sqlite


# 执行补丁
_patch_knowledge_base_for_sqlite()

