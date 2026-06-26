#!/usr/bin/env python3
"""
记忆系统 - 向量搜索模块 (LanceDB + Ollama)
支持：多用户/共享模式、去重、删除功能
"""
import lancedb
import requests
import json
import os
import threading
from pathlib import Path
from datetime import datetime
from typing import Optional

# ============ 配置 ============
MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
LANCEDB_PATH = MEMORY_DIR / "lance"
CONFIG_FILE = MEMORY_DIR / "config.yaml"
OLLAMA_URL = "http://localhost:11434/api/embeddings"
OLLAMA_MODEL = "nomic-embed-text"

LANCEDB_PATH.mkdir(parents=True, exist_ok=True)

# 全局配置
_config = {
    "mode": "private",  # private | shared
    "deduplicate_after": 20,  # 每N条触发去重
    "_memory_count": 0  # 内存计数器，用于触发去重
}

# ============ 配置管理 ============

def load_config():
    """加载配置"""
    global _config
    
    # 从环境变量加载
    if os.environ.get("MEMORY_MODE"):
        _config["mode"] = os.environ.get("MEMORY_MODE")
    
    if os.environ.get("MEMORY_DEDUP_AFTER"):
        try:
            _config["deduplicate_after"] = int(os.environ.get("MEMORY_DEDUP_AFTER"))
        except:
            pass
    
    # 从配置文件加载
    if CONFIG_FILE.exists():
        try:
            import yaml
            with open(CONFIG_FILE) as f:
                yaml_config = yaml.safe_load(f)
                if yaml_config and "memory" in yaml_config:
                    mem_cfg = yaml_config["memory"]
                    if "mode" in mem_cfg:
                        _config["mode"] = mem_cfg["mode"]
                    if "deduplicate_after" in mem_cfg:
                        _config["deduplicate_after"] = mem_cfg["deduplicate_after"]
        except ImportError:
            pass  # 没有 yaml 模块，使用默认值
    
    return _config

def get_mode() -> str:
    """获取当前模式"""
    load_config()
    return _config["mode"]

def set_mode(mode: str) -> dict:
    """设置模式"""
    if mode not in ["private", "shared"]:
        return {"success": False, "error": "模式必须是 private 或 shared"}
    
    _config["mode"] = mode
    
    # 保存到配置文件
    try:
        import yaml
        config_data = {}
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE) as f:
                config_data = yaml.safe_load(f) or {}
        
        if "memory" not in config_data:
            config_data["memory"] = {}
        config_data["memory"]["mode"] = mode
        
        with open(CONFIG_FILE, "w") as f:
            yaml.dump(config_data, f)
    except ImportError:
        pass  # 没有 yaml 模块
    
    return {"success": True, "message": f"模式已切换为: {mode}"}

# ============ 向量生成 ============

def get_embedding(text: str) -> Optional[list]:
    """调用 Ollama 本地 API 获取向量"""
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": OLLAMA_MODEL, "prompt": text},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()["embedding"]
    except Exception as e:
        print(f"⚠️ Ollama API 错误: {e}")
    return None

def is_ollama_ready() -> bool:
    """检查 Ollama 是否可用"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

# ============ LanceDB 操作 ============

def get_table():
    """获取或创建 LanceDB 表"""
    db = lancedb.connect(str(LANCEDB_PATH))
    
    table_names = db.table_names()
    
    if "memories" in table_names:
        table = db.open_table("memories")
    else:
        import pyarrow as pa
        
        schema = pa.schema([
            pa.field("id", pa.string()),  # 新增：唯一ID
            pa.field("vector", pa.list_(pa.float32(), 768)),
            pa.field("user_id", pa.string()),       # 创建者
            pa.field("access", pa.string()),         # private | shared
            pa.field("visible_to", pa.string()),     # 授权用户列表，JSON
            pa.field("content", pa.string()),
            pa.field("summary", pa.string()),
            pa.field("source", pa.string()),
            pa.field("importance", pa.int32()),
            pa.field("tags", pa.string()),
            pa.field("created_at", pa.string())
        ])
        
        table = db.create_table("memories", schema=schema)
    
    return db, table

def add_memory_vector(
    content: str,
    summary: str = None,
    importance: int = 3,
    source: str = "manual",
    tags: list = None,
    user_id: str = "default",
    access: str = None  # 新增：私有/共享
) -> dict:
    """添加记忆 - 支持多用户/共享模式"""
    
    if not is_ollama_ready():
        return {"success": False, "error": "Ollama 未启动"}
    
    # 如果没有指定 access，使用当前模式
    if access is None:
        access = get_mode()
    
    vector = get_embedding(content)
    if not vector:
        return {"success": False, "error": "生成向量失败"}
    
    try:
        import uuid
        memory_id = str(uuid.uuid4())
        
        db, table = get_table()
        
        # 构建可见用户列表
        visible_to = "[]"
        if access == "shared":
            visible_to = json.dumps([])  # 空数组 = 所有人可见
        
        data = [{
            "id": memory_id,
            "vector": vector,
            "user_id": user_id,
            "access": access,
            "visible_to": visible_to,
            "content": content,
            "summary": summary or "",
            "source": source,
            "importance": importance,
            "tags": json.dumps(tags) if tags else "[]",
            "created_at": datetime.now().isoformat()
        }]
        
        table.add(data)
        
        # 更新计数器并检查是否触发去重
        _config["_memory_count"] += 1
        if _config["_memory_count"] >= _config["deduplicate_after"]:
            _config["_memory_count"] = 0
            # 异步触发去重
            threading.Thread(target=deduplicate_memories, args=(user_id, get_mode()), daemon=True).start()
        
        return {
            "success": True,
            "message": f"记住啦: {content[:30]}...",
            "memory_id": memory_id,
            "access": access
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_accessible_memories(user_id: str, mode: str = None) -> list:
    """获取用户有权限访问的记忆"""
    if mode is None:
        mode = get_mode()
    
    db, table = get_table()
    
    if mode == "private":
        # 私有模式：仅自己的私有记忆 + 授权的共享记忆
        # visible_to 包含当前用户 或 user_id 是自己
        all_memories = table.to_arrow().to_pydict()
    else:
        # 共享模式：所有标记为 shared 的记忆
        all_memories = table.to_arrow().to_pydict()
    
    accessible = []
    for i in range(len(all_memories.get("content", []))):
        m = {
            "id": all_memories["id"][i],
            "user_id": all_memories["user_id"][i],
            "access": all_memories["access"][i],
            "visible_to": all_memories["visible_to"][i],
            "content": all_memories["content"][i],
            "summary": all_memories["summary"][i],
            "importance": all_memories["importance"][i],
            "created_at": all_memories["created_at"][i]
        }
        
        # 判断权限
        if mode == "private":
            # 自己的，或者授权的
            if m["user_id"] == user_id:
                accessible.append(m)
            elif m["access"] == "shared":
                try:
                    visible_list = json.loads(m["visible_to"])
                    if not visible_list or user_id in visible_list:
                        accessible.append(m)
                except:
                    accessible.append(m)  # 空 = 所有人可见
        else:
            # 共享模式：所有 shared 记忆
            if m["access"] == "shared":
                accessible.append(m)
    
    return accessible

def search_memories_vector(
    query: str, 
    limit: int = 5, 
    user_id: str = "default",
    mode: str = None
) -> dict:
    """语义向量搜索 - 支持多用户/共享模式"""
    
    if not is_ollama_ready():
        return {"success": False, "error": "Ollama 未启动"}
    
    if mode is None:
        mode = get_mode()
    
    # 空查询返回该用户所有有权限访问的记忆
    if not query:
        try:
            memories = get_accessible_memories(user_id, mode)
            # 按重要性排序
            memories.sort(key=lambda x: x.get("importance", 0), reverse=True)
            return {
                "success": True,
                "query": query,
                "count": len(memories),
                "results": memories[:limit]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    query_vector = get_embedding(query)
    if not query_vector:
        return {"success": False, "error": "生成查询向量失败"}
    
    try:
        db, table = get_table()
        
        # 先做向量搜索
        search_result = table.search(query_vector, vector_column_name="vector")
        results = search_result.limit(limit * 3).to_list()
        
        # 过滤无权限的
        accessible_ids = {m["id"] for m in get_accessible_memories(user_id, mode)}
        
        formatted = []
        for r in results:
            if r.get("id") in accessible_ids:
                formatted.append({
                    "id": r.get("id"),
                    "user_id": r.get("user_id"),
                    "access": r.get("access"),
                    "content": r.get("content", ""),
                    "summary": r.get("summary", ""),
                    "importance": r.get("importance", 3),
                    "created_at": r.get("created_at", "")
                })
        
        return {
            "success": True,
            "query": query,
            "count": len(formatted),
            "results": formatted[:limit]
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_context_vector(query: str = None, limit: int = 5, user_id: str = "default") -> str:
    """获取格式化上下文给 AI 用"""
    
    result = search_memories_vector(query, limit, user_id)
    
    if not result.get("success") or not result.get("results"):
        return ""
    
    context = "\n## 记住的信息 (语义搜索)\n"
    for m in result["results"]:
        context += f"- {m['content']}"
        if m.get('summary'):
            context += f" ({m['summary']})"
        context += "\n"
    
    return context

# ============ 删除功能 ============

def delete_memory(memory_id: str, requester_id: str = None) -> dict:
    """删除记忆 - 权限校验"""
    # 强制从环境变量获取真实用户ID，防止伪造
    import os
    real_user_id = os.environ.get("OPENCLAW_USER_ID")
    if not real_user_id:
        return {"success": False, "error": "安全错误：无法验证用户身份，请通过正确的渠道操作"}
    requester_id = real_user_id
    
    try:
        db, table = get_table()
        
        # 获取记忆详情
        all_memories = table.to_arrow().to_pydict()
        
        memory_to_delete = None
        for i in range(len(all_memories.get("id", []))):
            if all_memories["id"][i] == memory_id:
                memory_to_delete = {
                    "id": all_memories["id"][i],
                    "user_id": all_memories["user_id"][i],
                    "content": all_memories["content"][i],
                    "access": all_memories["access"][i]
                }
                break
        
        if not memory_to_delete:
            return {"success": False, "error": "记忆不存在"}
        
        # 权限检查：只有创建人可以删除
        if memory_to_delete["user_id"] != requester_id:
            return {
                "success": False,
                "error": "权限不足：只有创建人才能删除此记忆"
            }
        
        # 执行删除
        table.delete(f"id = '{memory_id}'")
        
        return {
            "success": True,
            "message": "记忆已删除",
            "deleted_id": memory_id
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_memory_info(memory_id: str) -> dict:
    """获取记忆详情（用于删除前确认）"""
    
    try:
        db, table = get_table()
        all_memories = table.to_arrow().to_pydict()
        
        for i in range(len(all_memories.get("id", []))):
            if all_memories["id"][i] == memory_id:
                return {
                    "success": True,
                    "memory": {
                        "id": all_memories["id"][i],
                        "user_id": all_memories["user_id"][i],
                        "access": all_memories["access"][i],
                        "content": all_memories["content"][i],
                        "importance": all_memories["importance"][i],
                        "created_at": all_memories["created_at"][i]
                    }
                }
        
        return {"success": False, "error": "记忆不存在"}
        
    except Exception as e:
        return {"success": False, "error": str(e)}

def share_memory(memory_id: str, visible_to: list, requester_id: str = None) -> dict:
    """共享记忆给指定用户 - 只有创建人可以共享"""
    # 强制从环境变量获取真实用户ID，防止伪造
    import os
    real_user_id = os.environ.get("OPENCLAW_USER_ID")
    if not real_user_id:
        return {"success": False, "error": "安全错误：无法验证用户身份，请通过正确的渠道操作"}
    requester_id = real_user_id
    
    try:
        db, table = get_table()
        
        # 获取记忆详情
        all_memories = table.to_arrow().to_pydict()
        
        memory_to_share = None
        memory_index = -1
        for i in range(len(all_memories.get("id", []))):
            if all_memories["id"][i] == memory_id:
                memory_to_share = {
                    "id": all_memories["id"][i],
                    "user_id": all_memories["user_id"][i],
                    "access": all_memories["access"][i],
                    "content": all_memories["content"][i]
                }
                memory_index = i
                break
        
        if not memory_to_share:
            return {"success": False, "error": "记忆不存在"}
        
        # 权限检查：只有创建人可以共享
        if memory_to_share["user_id"] != requester_id:
            return {
                "success": False,
                "error": "权限不足：只有创建人才能共享此记忆"
            }
        
        # 更新记忆的 access 和 visible_to
        new_access = "shared" if visible_to else "private"
        new_visible_to = json.dumps(visible_to) if visible_to else "[]"
        
        # 使用 LanceDB 的 update
        table.update(
            where=f"id = '{memory_id}'",
            values={
                "access": new_access,
                "visible_to": new_visible_to
            }
        )
        
        return {
            "success": True,
            "message": "记忆共享成功",
            "memory_id": memory_id,
            "access": new_access,
            "visible_to": visible_to
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

# ============ 去重功能 ============

def deduplicate_memories(user_id: str = None, mode: str = None):
    """去重记忆 - 异步执行"""
    
    if mode is None:
        mode = get_mode()
    
    try:
        print(f"🔄 开始去重 (mode: {mode})...")
        
        db, table = get_table()
        all_memories = table.to_arrow().to_pydict()
        
        # 按内容分组
        content_groups = {}
        for i in range(len(all_memories.get("content", []))):
            m = {
                "id": all_memories["id"][i],
                "user_id": all_memories["user_id"][i],
                "access": all_memories["access"][i],
                "content": all_memories["content"][i],
                "importance": all_memories["importance"][i]
            }
            
            # 多用户模式下，只处理有权限的记忆
            if mode == "private":
                # 检查是否有权限
                if m["user_id"] != user_id and m["access"] != "shared":
                    continue
            
            key = m["content"]
            if key not in content_groups:
                content_groups[key] = []
            content_groups[key].append(m)
        
        # 删除重复的（保留重要度最高的）
        deleted_count = 0
        for content, items in content_groups.items():
            if len(items) > 1:
                items.sort(key=lambda x: x.get("importance", 0), reverse=True)
                to_delete = items[1:]
                
                for d in to_delete:
                    # 多用户模式：只能删除自己的
                    if mode == "private" and d["user_id"] != user_id:
                        continue
                    
                    table.delete(f"id = '{d['id']}'")
                    deleted_count += 1
        
        print(f"✅ 去重完成，删除了 {deleted_count} 条重复记忆")
        
    except Exception as e:
        print(f"⚠️ 去重失败: {e}")

# ============ 列表功能 ============

def list_memories(user_id: str = "default", mode: str = None, include_shared: bool = True) -> dict:
    """列出记忆（带权限过滤）"""
    
    if mode is None:
        mode = get_mode()
    
    try:
        memories = get_accessible_memories(user_id, mode)
        
        return {
            "success": True,
            "count": len(memories),
            "mode": mode,
            "results": memories
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

# ============ 测试 ============

if __name__ == "__main__":
    print("🧪 测试记忆系统 (多用户/共享模式)...")
    print(f"📋 当前模式: {get_mode()}")
    
    if is_ollama_ready():
        print("✅ Ollama 已启动")
        
        # 测试设置模式
        print("\n📝 测试设置模式...")
        result = set_mode("private")
        print(result)
        
        # 测试添加记忆
        print("\n📝 测试添加记忆...")
        result = add_memory_vector(
            content="测试记忆 - 私有模式",
            importance=3,
            user_id="test_user",
            source="test"
        )
        print(result)
        
        # 测试搜索
        print("\n🔍 测试搜索...")
        result = search_memories_vector("测试", limit=5, user_id="test_user")
        print(result)
        
        # 测试获取列表
        print("\n📋 测试列表...")
        result = list_memories(user_id="test_user")
        print(result)
        
    else:
        print("⚠️ Ollama 未启动")
