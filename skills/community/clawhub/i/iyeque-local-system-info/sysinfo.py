import psutil
import argparse
import json
import sys

def get_cpu():
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "cpu_count": psutil.cpu_count(),
        "load_avg": ([x / max(1, psutil.cpu_count() or 1) for x in psutil.getloadavg()] if hasattr(psutil, "getloadavg") else [])
    }

def get_memory():
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    return {
        "total": mem.total,
        "available": mem.available,
        "percent": mem.percent,
        "swap_percent": swap.percent
    }

def get_disk():
    usage = psutil.disk_usage('/')
    return {
        "total": usage.total,
        "used": usage.used,
        "free": usage.free,
        "percent": usage.percent
    }

def get_processes(limit=20, include_owners=False):
    if not isinstance(limit, int) or limit < 1 or limit > 100:
        raise ValueError("limit must be an integer from 1 to 100")
    procs = []
    fields = ['pid', 'name', 'cpu_percent', 'memory_percent'] + (['username'] if include_owners else [])
    for p in psutil.process_iter(fields):
        try:
            p_info = p.info
            procs.append(p_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    # Sort by CPU usage descending
    procs.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
    return procs[:limit]

def get_summary():
    return {
        "cpu": get_cpu(),
        "memory": get_memory(),
        "disk": get_disk()
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Local System Info Skill")
    parser.add_argument("action", choices=["summary", "cpu", "memory", "disk", "processes"], help="Action to perform")
    parser.add_argument("--limit", type=int, default=20, help="Limit for process list (1-100)")
    parser.add_argument("--include-owners", action="store_true", help="Include process usernames; use only when explicitly needed")
    
    args = parser.parse_args()
    
    result = {}
    try:
        if args.action == "summary":
            result = get_summary()
        elif args.action == "cpu":
            result = get_cpu()
        elif args.action == "memory":
            result = get_memory()
        elif args.action == "disk":
            result = get_disk()
        elif args.action == "processes":
            result = get_processes(args.limit, args.include_owners)
            
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
