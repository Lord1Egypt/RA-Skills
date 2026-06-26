"""
进程管理模块 - 提供进程列表、进程终止、进程信息获取功能
"""
import psutil
import os

from modules.security import check_process_operation, log_operation


def process_list():
    log_operation("process_list", {}, True)
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'cpu': proc.info['cpu_percent'],
                    'memory': proc.info['memory_percent']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return {
            "success": True,
            "data": {"processes": processes[:100]},
            "error": None
        }
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def process_kill(name: str):
    allowed, reason = check_process_operation(name, "kill")
    if not allowed:
        return {"success": False, "data": None, "error": f"进程操作被安全策略拦截: {reason}"}

    try:
        killed = []
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'].lower() == name.lower():
                proc.kill()
                killed.append(proc.info['pid'])
        return {
            "success": True,
            "data": {"killed_pids": killed},
            "error": None
        }
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def process_get(name: str):
    allowed, reason = check_process_operation(name, "get")
    if not allowed:
        return {"success": False, "data": None, "error": f"进程查询被安全策略拦截: {reason}"}

    try:
        matches = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'create_time']):
            if name.lower() in proc.info['name'].lower():
                matches.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'cpu': proc.info['cpu_percent'],
                    'memory': proc.info['memory_percent'],
                    'create_time': proc.info['create_time']
                })
        return {
            "success": True,
            "data": {"processes": matches},
            "error": None
        }
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}
