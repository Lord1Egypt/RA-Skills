#!/usr/bin/env python3
"""
Milvus 向量数据库记忆管理脚本
用于长期记忆的存储、检索和状态管理

功能：
- 初始化集合
- 存储记忆信息
- 查询记忆
- 更新记忆状态
- 删除记忆
"""

import os
import sys
import json
import argparse
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

# 加载 .env 文件
def load_env_file():
    """加载 .env 文件到环境变量"""
    # 优先加载脚本所在目录的 .env
    script_dir = Path(__file__).parent
    env_file = script_dir / ".env"
    
    # 如果脚本目录没有，尝试加载当前工作目录的 .env
    if not env_file.exists():
        env_file = Path.cwd() / ".env"
    
    # 如果还没有，尝试加载 Skill 根目录的 .env
    if not env_file.exists():
        skill_root = script_dir.parent
        env_file = skill_root / ".env"
    
    if env_file.exists():
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # 跳过空行和注释
                    if not line or line.startswith('#'):
                        continue
                    # 解析 KEY=VALUE
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        # 移除引号
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        elif value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]
                        # 设置环境变量（不覆盖已存在的）
                        if key and not os.getenv(key):
                            os.environ[key] = value
            print(f"✓ 已加载环境配置文件：{env_file}")
        except Exception as e:
            print(f"⚠ 加载 .env 文件失败：{e}")

# 在导入依赖前加载环境变量
load_env_file()

try:
    from pymilvus import MilvusClient, DataType
except ImportError:
    print("错误：缺少 pymilvus 库，请安装：pip install pymilvus==2.3.0")
    sys.exit(1)


# 默认集合名称
DEFAULT_COLLECTION_NAME = "memory_store"


class MilvusMemoryManager:
    """Milvus 记忆管理器"""
    
    def __init__(self, collection_name: str = DEFAULT_COLLECTION_NAME):
        """
        初始化记忆管理器
        
        Args:
            collection_name: 集合名称
        """
        self.collection_name = collection_name
        self.client: Optional[MilvusClient] = None
        self._connected = False
        
    def connect(self) -> bool:
        """
        连接到 Milvus 数据库
        
        Returns:
            连接是否成功
        """
        try:
            # 从环境变量获取 URI 和 Token
            uri = os.getenv("MILVUS_URI")
            token = os.getenv("MILVUS_TOKEN")
            
            # 检查配置完整性
            missing_configs = []
            if not uri:
                missing_configs.append("MILVUS_URI（实例访问地址，格式：http://your-instance.milvus.ivolces.com:19530）")
            if not token:
                missing_configs.append("MILVUS_TOKEN（认证令牌，格式：Username:Password，如 root:yourpassword）")
            
            if missing_configs:
                error_msg = "❌ 缺少必要的配置项，请在 .env 文件中设置以下值：\n"
                for config in missing_configs:
                    error_msg += f"  - {config}\n"
                error_msg += "\n.env 文件位置：scripts/.env 或当前工作目录下的 .env"
                raise ValueError(error_msg)
            
            # 使用 MilvusClient 连接
            self.client = MilvusClient(uri=uri, token=token)
            self._connected = True
            
            print(f"✓ 成功连接到 Milvus 实例：{uri}")
            return True
            
        except Exception as e:
            print(f"✗ 连接失败：{str(e)}")
            return False
    
    def disconnect(self):
        """断开连接"""
        if self.client:
            self.client.close()
            self._connected = False
    
    def init_collection(self, recreate: bool = False) -> bool:
        """
        初始化记忆集合
        
        Args:
            recreate: 是否重新创建（删除现有集合）
        
        Returns:
            是否成功
        """
        if not self._connected:
            if not self.connect():
                return False
        
        try:
            # 如果集合已存在且要求重建
            if self.client.has_collection(self.collection_name):
                if recreate:
                    print(f"删除现有集合：{self.collection_name}")
                    self.client.drop_collection(self.collection_name)
                else:
                    print(f"集合已存在：{self.collection_name}")
                    return True
            
            # 创建 Schema
            schema = self.client.create_schema()
            schema.add_field("id", DataType.INT64, is_primary=True, auto_id=True, description="主键ID")
            schema.add_field("memory_id", DataType.VARCHAR, max_length=64, description="记忆唯一标识")
            schema.add_field("content", DataType.VARCHAR, max_length=2000, description="记忆内容")
            schema.add_field("category", DataType.VARCHAR, max_length=50, description="分类")
            schema.add_field("role", DataType.VARCHAR, max_length=50, description="角色")
            schema.add_field("project", DataType.VARCHAR, max_length=100, description="项目")
            schema.add_field("event", DataType.VARCHAR, max_length=100, description="事件")
            schema.add_field("status", DataType.VARCHAR, max_length=30, description="状态")
            schema.add_field("priority", DataType.VARCHAR, max_length=20, description="优先级")
            schema.add_field("tags", DataType.VARCHAR, max_length=500, description="标签")
            schema.add_field("context", DataType.VARCHAR, max_length=5000, description="上下文")
            schema.add_field("metadata", DataType.VARCHAR, max_length=3000, description="元数据")
            schema.add_field("created_at", DataType.VARCHAR, max_length=32, description="创建时间")
            schema.add_field("updated_at", DataType.VARCHAR, max_length=32, description="更新时间")
            
            # 创建集合
            self.client.create_collection(self.collection_name, schema=schema)
            
            # 创建索引（为常用查询字段）
            index_params = self.client.prepare_index_params()
            index_params.add_index(field_name="category", index_type="Trie", index_name="category_index")
            index_params.add_index(field_name="role", index_type="Trie", index_name="role_index")
            index_params.add_index(field_name="project", index_type="Trie", index_name="project_index")
            index_params.add_index(field_name="event", index_type="Trie", index_name="event_index")
            index_params.add_index(field_name="status", index_type="Trie", index_name="status_index")
            index_params.add_index(field_name="priority", index_type="Trie", index_name="priority_index")
            
            self.client.create_index(self.collection_name, index_params)
            
            print(f"✓ 成功创建集合：{self.collection_name}")
            return True
            
        except Exception as e:
            print(f"✗ 初始化集合失败：{str(e)}")
            return False
    
    def save_memory(self, memory_info: Dict[str, Any]) -> Optional[str]:
        """
        保存记忆到集合
        
        Args:
            memory_info: 记忆信息字典
        
        Returns:
            记忆 ID 或 None（失败时）
        """
        if not self._connected:
            if not self.connect():
                return None
        
        try:
            # 确保集合存在
            if not self.client.has_collection(self.collection_name):
                if not self.init_collection():
                    return None
            
            # 生成记忆 ID
            memory_id = memory_info.get("memory_id") or str(uuid.uuid4())
            current_time = datetime.now().isoformat()
            
            # 准备数据
            data_row = {
                "memory_id": memory_id,
                "content": memory_info.get("content", ""),
                "category": memory_info.get("category", "general"),
                "role": memory_info.get("role", ""),
                "project": memory_info.get("project", ""),
                "event": memory_info.get("event", ""),
                "status": memory_info.get("status", "pending"),
                "priority": memory_info.get("priority", "medium"),
                "tags": json.dumps(memory_info.get("tags", []), ensure_ascii=False),
                "context": json.dumps(memory_info.get("context", {}), ensure_ascii=False),
                "metadata": json.dumps(memory_info.get("metadata", {}), ensure_ascii=False),
                "created_at": current_time,
                "updated_at": current_time
            }
            
            # 插入数据
            result = self.client.insert(self.collection_name, [data_row])
            
            print(f"✓ 记忆已保存，ID：{memory_id}")
            return memory_id
            
        except Exception as e:
            print(f"✗ 保存记忆失败：{str(e)}")
            return None
    
    def query_memories(
        self,
        category: Optional[str] = None,
        role: Optional[str] = None,
        project: Optional[str] = None,
        event: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        查询记忆
        
        Args:
            category: 分类过滤
            role: 角色过滤
            project: 项目过滤
            event: 事件过滤
            status: 状态过滤
            priority: 优先级过滤
            limit: 返回数量限制
        
        Returns:
            记忆列表
        """
        if not self._connected:
            if not self.connect():
                return []
        
        try:
            if not self.client.has_collection(self.collection_name):
                print("✗ 集合不存在")
                return []
            
            # 构建过滤表达式
            filters = []
            if category:
                filters.append(f'category == "{category}"')
            if role:
                filters.append(f'role == "{role}"')
            if project:
                filters.append(f'project == "{project}"')
            if event:
                filters.append(f'event == "{event}"')
            if status:
                filters.append(f'status == "{status}"')
            if priority:
                filters.append(f'priority == "{priority}"')
            
            filter_expr = " and ".join(filters) if filters else None
            
            # 执行查询
            results = self.client.query(
                collection_name=self.collection_name,
                filter=filter_expr,
                output_fields=["memory_id", "content", "category", "role", "project", 
                              "event", "status", "priority", "tags", "created_at", "updated_at"],
                limit=limit
            )
            
            # 格式化结果
            memories = []
            for result in results:
                memory = {
                    "memory_id": result.get("memory_id"),
                    "content": result.get("content"),
                    "category": result.get("category"),
                    "role": result.get("role"),
                    "project": result.get("project"),
                    "event": result.get("event"),
                    "status": result.get("status"),
                    "priority": result.get("priority"),
                    "tags": json.loads(result.get("tags", "[]")),
                    "created_at": result.get("created_at"),
                    "updated_at": result.get("updated_at")
                }
                memories.append(memory)
            
            print(f"✓ 查询到 {len(memories)} 条记忆")
            return memories
            
        except Exception as e:
            print(f"✗ 查询失败：{str(e)}")
            return []
    
    def get_memory(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """
        获取特定记忆详情
        
        Args:
            memory_id: 记忆 ID
        
        Returns:
            记忆详情或 None
        """
        if not self._connected:
            if not self.connect():
                return None
        
        try:
            if not self.client.has_collection(self.collection_name):
                print("✗ 集合不存在")
                return None
            
            # 查询特定记忆
            results = self.client.query(
                collection_name=self.collection_name,
                filter=f'memory_id == "{memory_id}"',
                output_fields=["*"]
            )
            
            if not results:
                print(f"✗ 未找到记忆：{memory_id}")
                return None
            
            # 格式化结果
            result = results[0]
            memory = {
                "memory_id": result.get("memory_id"),
                "content": result.get("content"),
                "category": result.get("category"),
                "role": result.get("role"),
                "project": result.get("project"),
                "event": result.get("event"),
                "status": result.get("status"),
                "priority": result.get("priority"),
                "tags": json.loads(result.get("tags", "[]")),
                "context": json.loads(result.get("context", "{}")),
                "metadata": json.loads(result.get("metadata", "{}")),
                "created_at": result.get("created_at"),
                "updated_at": result.get("updated_at")
            }
            
            print(f"✓ 找到记忆：{memory_id}")
            return memory
            
        except Exception as e:
            print(f"✗ 获取记忆失败：{str(e)}")
            return None
    
    def update_memory_status(
        self,
        memory_id: str,
        status: str
    ) -> bool:
        """
        更新记忆状态
        
        Args:
            memory_id: 记忆 ID
            status: 新状态
        
        Returns:
            是否成功
        """
        if not self._connected:
            if not self.connect():
                return False
        
        try:
            if not self.client.has_collection(self.collection_name):
                print("✗ 集合不存在")
                return False
            
            # 先查询记忆是否存在
            existing = self.get_memory(memory_id)
            if not existing:
                return False
            
            # Milvus 不支持直接更新，需要删除后重新插入
            self.client.delete(
                collection_name=self.collection_name,
                filter=f'memory_id == "{memory_id}"'
            )
            
            # 插入更新后的记录
            memory_info = {
                "memory_id": memory_id,
                "content": existing["content"],
                "category": existing.get("category", "general"),
                "role": existing.get("role", ""),
                "project": existing.get("project", ""),
                "event": existing.get("event", ""),
                "status": status,
                "priority": existing.get("priority", "medium"),
                "tags": existing.get("tags", []),
                "context": existing.get("context", {}),
                "metadata": existing.get("metadata", {})
            }
            
            # 重新保存
            new_id = self.save_memory(memory_info)
            
            if new_id:
                print(f"✓ 记忆状态已更新：{memory_id} -> {status}")
                return True
            else:
                return False
                
        except Exception as e:
            print(f"✗ 更新记忆失败：{str(e)}")
            return False
    
    def delete_memory(self, memory_id: str) -> bool:
        """
        删除记忆
        
        Args:
            memory_id: 记忆 ID
        
        Returns:
            是否成功
        """
        if not self._connected:
            if not self.connect():
                return False
        
        try:
            if not self.client.has_collection(self.collection_name):
                print("✗ 集合不存在")
                return False
            
            # 删除记忆
            self.client.delete(
                collection_name=self.collection_name,
                filter=f'memory_id == "{memory_id}"'
            )
            
            print(f"✓ 记忆已删除：{memory_id}")
            return True
            
        except Exception as e:
            print(f"✗ 删除记忆失败：{str(e)}")
            return False


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="Milvus 长期记忆管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  # 初始化集合
  python milvus_manager.py --action init

  # 存储记忆
  python milvus_manager.py --action save --memory-file ./memory.json

  # 查询记忆
  python milvus_manager.py --action query --project website-redesign --limit 10

  # 获取详情
  python milvus_manager.py --action get --memory-id xxx

  # 更新状态
  python milvus_manager.py --action update --memory-id xxx --status completed

  # 删除记忆
  python milvus_manager.py --action delete --memory-id xxx
        """
    )
    
    parser.add_argument(
        "--action",
        required=True,
        choices=["init", "save", "query", "get", "update", "delete"],
        help="操作类型"
    )
    
    parser.add_argument(
        "--memory-file",
        help="记忆信息文件路径（JSON 格式，用于 save 操作）"
    )
    
    parser.add_argument(
        "--memory-id",
        help="记忆 ID（用于 get、update、delete 操作）"
    )
    
    parser.add_argument(
        "--category",
        help="分类过滤（用于 query）"
    )
    
    parser.add_argument(
        "--role",
        help="角色过滤（用于 query）"
    )
    
    parser.add_argument(
        "--project",
        help="项目过滤（用于 query）"
    )
    
    parser.add_argument(
        "--event",
        help="事件过滤（用于 query）"
    )
    
    parser.add_argument(
        "--status",
        help="状态过滤（用于 query）或新状态（用于 update）"
    )
    
    parser.add_argument(
        "--priority",
        help="优先级过滤（用于 query）"
    )
    
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="查询结果数量限制（默认：10）"
    )
    
    parser.add_argument(
        "--recreate",
        action="store_true",
        help="重新创建集合（用于 init 操作）"
    )
    
    parser.add_argument(
        "--collection",
        default=DEFAULT_COLLECTION_NAME,
        help=f"集合名称（默认：{DEFAULT_COLLECTION_NAME}）"
    )
    
    args = parser.parse_args()
    
    # 创建管理器
    manager = MilvusMemoryManager(collection_name=args.collection)
    
    try:
        # 执行操作
        if args.action == "init":
            success = manager.init_collection(recreate=args.recreate)
            sys.exit(0 if success else 1)
        
        elif args.action == "save":
            if not args.memory_file:
                print("错误：save 操作需要 --memory-file 参数")
                sys.exit(1)
            
            # 读取记忆文件
            try:
                with open(args.memory_file, 'r', encoding='utf-8') as f:
                    memory_info = json.load(f)
            except FileNotFoundError:
                print(f"错误：文件不存在：{args.memory_file}")
                sys.exit(1)
            except json.JSONDecodeError as e:
                print(f"错误：JSON 格式错误：{e}")
                sys.exit(1)
            
            memory_id = manager.save_memory(memory_info)
            sys.exit(0 if memory_id else 1)
        
        elif args.action == "query":
            memories = manager.query_memories(
                category=args.category,
                role=args.role,
                project=args.project,
                event=args.event,
                status=args.status,
                priority=args.priority,
                limit=args.limit
            )
            
            if memories:
                print("\n查询结果：")
                print(json.dumps(memories, indent=2, ensure_ascii=False))
            sys.exit(0)
        
        elif args.action == "get":
            if not args.memory_id:
                print("错误：get 操作需要 --memory-id 参数")
                sys.exit(1)
            
            memory = manager.get_memory(args.memory_id)
            if memory:
                print("\n记忆详情：")
                print(json.dumps(memory, indent=2, ensure_ascii=False))
                sys.exit(0)
            else:
                sys.exit(1)
        
        elif args.action == "update":
            if not args.memory_id or not args.status:
                print("错误：update 操作需要 --memory-id 和 --status 参数")
                sys.exit(1)
            
            success = manager.update_memory_status(args.memory_id, args.status)
            sys.exit(0 if success else 1)
        
        elif args.action == "delete":
            if not args.memory_id:
                print("错误：delete 操作需要 --memory-id 参数")
                sys.exit(1)
            
            success = manager.delete_memory(args.memory_id)
            sys.exit(0 if success else 1)
    
    finally:
        manager.disconnect()


if __name__ == "__main__":
    main()
