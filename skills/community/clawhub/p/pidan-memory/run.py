#!/usr/bin/env python3
"""
Memory Skill for OpenClaw
支持：多用户/共享模式、去重、删除功能
"""
import json
import sys
import os
from pathlib import Path

def get_real_user_id(params_user_id: str = None) -> str:
    """
    获取真实用户ID
    优先级：环境变量 > 参数 > default
    """
    # 优先从环境变量获取
    env_user_id = os.environ.get("OPENCLAW_USER_ID")
    if env_user_id:
        return env_user_id
    
    # 其次用参数
    if params_user_id:
        return params_user_id
    
    # 默认
    return "default"

MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
sys.path.insert(0, str(MEMORY_DIR))

# ============ 命令处理 ============

def handle_remember(params: dict) -> dict:
    """添加记忆"""
    from memory_lance import add_memory_vector, get_mode
    
    mode = get_mode()
    result = add_memory_vector(
        content=params.get("content", ""),
        summary=params.get("summary"),
        importance=params.get("importance", 3),
        source="skill",
        user_id=os.environ.get("OPENCLAW_USER_ID", params.get("user_id", "default")),
        access=mode  # 使用当前模式
    )
    return result


def handle_recall(params: dict) -> dict:
    """搜索记忆"""
    from memory_lance import search_memories_vector, get_mode
    
    mode = get_mode()
    result = search_memories_vector(
        query=params.get("query", ""),
        limit=params.get("limit", 5),
        user_id=os.environ.get("OPENCLAW_USER_ID", params.get("user_id", "default")),
        mode=mode
    )
    return result


def handle_recent_memories(params: dict) -> dict:
    """获取最近记忆"""
    from memory_lance import search_memories_vector, get_mode
    
    mode = get_mode()
    result = search_memories_vector(
        query="",  # 空查询返回所有
        limit=params.get("limit", 5),
        user_id=os.environ.get("OPENCLAW_USER_ID", params.get("user_id", "default")),
        mode=mode
    )
    return result


def handle_set_mode(params: dict) -> dict:
    """设置模式"""
    from memory_lance import set_mode
    
    mode = params.get("mode", "private")
    if mode not in ["private", "shared"]:
        return {"success": False, "error": "模式必须是 private 或 shared"}
    
    return set_mode(mode)


def handle_get_mode(params: dict) -> dict:
    """获取当前模式"""
    from memory_lance import get_mode
    
    return {
        "success": True,
        "mode": get_mode()
    }


def handle_delete_memory(params: dict) -> dict:
    """删除记忆"""
    from memory_lance import delete_memory, get_memory_info
    
    memory_id = params.get("memory_id")
    if not memory_id:
        return {"success": False, "error": "memory_id 不能为空"}
    
    # 强制从环境变量获取真实用户ID
    requester_id = os.environ.get("OPENCLAW_USER_ID")
    if not requester_id:
        return {"success": False, "error": "安全错误：无法验证用户身份"}
    confirm = params.get("confirm", False)
    
    # 先获取记忆详情
    info_result = get_memory_info(memory_id)
    if not info_result.get("success"):
        return info_result
    
    memory = info_result.get("memory", {})
    
    # 检查是否是创建人
    if memory.get("user_id") != requester_id:
        return {
            "success": False,
            "error": "权限不足：只有创建人才能删除此记忆"
        }
    
    # 如果没有确认，返回确认提示
    if not confirm:
        return {
            "success": True,
            "need_confirm": True,
            "message": f"确定要删除这条记忆吗？此操作不可恢复。",
            "memory": {
                "id": memory.get("id"),
                "content": memory.get("content"),
                "user_id": memory.get("user_id"),
                "created_at": memory.get("created_at")
            },
            "warning": "只有创建人才能删除此记忆"
        }
    
    # 执行删除
    return delete_memory(memory_id)  # user_id 从环境变量获取


def handle_list_memories(params: dict) -> dict:
    """列出记忆"""
    from memory_lance import list_memories, get_mode
    
    mode = get_mode()
    result = list_memories(
        user_id=os.environ.get("OPENCLAW_USER_ID", params.get("user_id", "default")),
        mode=mode,
        include_shared=params.get("include_shared", True)
    )
    return result


def handle_deduplicate(params: dict) -> dict:
    """手动触发去重"""
    from memory_lance import deduplicate_memories, get_mode
    
    mode = get_mode()
    user_id = params.get("user_id") or os.environ.get("OPENCLAW_USER_ID", "default")
    
    # 异步执行
    import threading
    threading.Thread(target=deduplicate_memories, args=(user_id, mode), daemon=True).start()
    
    return {
        "success": True,
        "message": "去重任务已启动（异步执行）"
    }


def handle_share_memory(params: dict) -> dict:
    """共享记忆给指定用户"""
    from memory_lance import share_memory
    
    memory_id = params.get("memory_id")
    if not memory_id:
        return {"success": False, "error": "memory_id 不能为空"}
    
    visible_to = params.get("visible_to", [])  # 可见用户列表
    # 强制从环境变量获取真实用户ID
    requester_id = os.environ.get("OPENCLAW_USER_ID")
    if not requester_id:
        return {"success": False, "error": "安全错误：无法验证用户身份"}
    
    return share_memory(memory_id, visible_to)  # user_id 从环境变量获取


def handle_stats(params: dict) -> dict:
    """获取统计信息"""
    from memory_lance import get_table, get_mode
    
    mode = get_mode()
    db, table = get_table()
    total = table.count_rows()
    
    # 按用户统计
    all_memories = table.to_arrow().to_pydict()
    
    user_counts = {}
    access_counts = {"private": 0, "shared": 0}
    
    for i in range(len(all_memories.get("content", []))):
        user = all_memories["user_id"][i]
        access = all_memories["access"][i]
        
        user_counts[user] = user_counts.get(user, 0) + 1
        if access in access_counts:
            access_counts[access] += 1
    
    return {
        "success": True,
        "mode": mode,
        "total_memories": total,
        "by_user": user_counts,
        "by_access": access_counts
    }


# ============ 主入口 ============

if __name__ == "__main__":
    try:
        input_data = json.load(sys.stdin)
        
        command = input_data.get("command")
        params = input_data.get("parameters", {})
        
        # 获取 user_id (从参数或环境变量)
        user_id = params.get("user_id") or os.environ.get("OPENCLAW_USER_ID", "default")
        params["user_id"] = user_id
        
        handlers = {
            "remember": handle_remember,
            "recall": handle_recall,
            "recent_memories": handle_recent_memories,
            "set_mode": handle_set_mode,
            "get_mode": handle_get_mode,
            "delete_memory": handle_delete_memory,
            "share_memory": handle_share_memory,
            "list_memories": handle_list_memories,
            "deduplicate": handle_deduplicate,
            "stats": handle_stats,
        }
        
        handler = handlers.get(command)
        if handler:
            result = handler(params)
        else:
            result = {"success": False, "error": f"未知命令: {command}"}
        
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False))
