"""
文件操作模块 - 提供文件读写、列表、存在性检查功能
"""
import os

from modules.security import check_file_path, log_operation


def file_read(path: str):
    allowed, reason = check_file_path(path, "read")
    if not allowed:
        return {"success": False, "data": None, "error": f"文件访问被安全策略拦截: {reason}"}

    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        return {"success": True, "data": {"path": path, "content": content}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def file_write(path: str, content: str):
    allowed, reason = check_file_path(path, "write")
    if not allowed:
        return {"success": False, "data": None, "error": f"文件写入被安全策略拦截: {reason}"}

    try:
        os.makedirs(os.path.dirname(path) if os.path.dirname(path) else '.', exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return {"success": True, "data": {"path": path}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def file_list(path: str):
    allowed, reason = check_file_path(path, "list")
    if not allowed:
        return {"success": False, "data": None, "error": f"目录访问被安全策略拦截: {reason}"}

    try:
        if not os.path.exists(path):
            return {"success": False, "data": None, "error": "路径不存在"}

        items = []
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            items.append({
                "name": item,
                "is_dir": os.path.isdir(full_path),
                "size": os.path.getsize(full_path) if os.path.isfile(full_path) else 0
            })
        return {"success": True, "data": {"path": path, "items": items}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def file_exists(path: str):
    allowed, reason = check_file_path(path, "exists")
    if not allowed:
        return {"success": False, "data": None, "error": f"文件检查被安全策略拦截: {reason}"}

    try:
        exists = os.path.exists(path)
        return {"success": True, "data": {"path": path, "exists": exists}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}
