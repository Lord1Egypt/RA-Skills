"""
系统信息模块 - 提供系统信息、显示器信息获取功能
"""
import platform
import psutil
import os


def get_system_info():
    try:
        cpu_count = psutil.cpu_count()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        info = {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "cpu_count": cpu_count,
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "memory_total": memory.total,
            "memory_available": memory.available,
            "memory_percent": memory.percent,
            "disk_total": disk.total,
            "disk_used": disk.used,
            "disk_percent": disk.percent,
        }
        return {"success": True, "data": info, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def get_displays():
    try:
        import mss
        with mss.mss() as sct:
            monitors = sct.monitors
        displays = []
        for i, m in enumerate(monitors[1:], 1):
            displays.append({
                "id": i,
                "x": m["left"],
                "y": m["top"],
                "width": m["width"],
                "height": m["height"]
            })
        return {"success": True, "data": {"displays": displays}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}
