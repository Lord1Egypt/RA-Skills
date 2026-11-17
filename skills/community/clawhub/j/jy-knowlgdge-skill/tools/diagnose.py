"""
问题诊断工具
当 main.py 或其他脚本报错时，运行此工具获取详细诊断信息。

用法: python tools/diagnose.py [--full]
  --full  输出完整诊断（含环境变量、网络状态等）
  默认    快速诊断
"""

import sys
import os

# 修复 Windows GBK 编码问题
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import json
import subprocess
import traceback


def diagnose_mongodb():
    """诊断 MongoDB 连接"""
    results = {"status": "unknown", "details": []}
    
    # 检查 Docker 容器
    try:
        r = subprocess.run(["docker", "ps", "--format", "{{.Names}}\t{{.Status}}"],
                          capture_output=True, text=True, timeout=5)
        mongo_line = [l for l in r.stdout.split('\n') if 'knowledge-mongo' in l or 'mongo' in l.lower()]
        if mongo_line:
            results["container"] = mongo_line[0]
            results["status"] = "running"
            results["details"].append(f"Docker 容器运行中: {mongo_line[0]}")
        else:
            results["status"] = "stopped"
            results["details"].append("未找到 MongoDB Docker 容器")
    except Exception as e:
        results["status"] = "error"
        results["details"].append(f"Docker 检查失败: {e}")

    # 尝试直接连接
    try:
        from pymongo import MongoClient
        c = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=3000)
        c.server_info()
        results["connection"] = "ok"
        results["details"].append("MongoDB 直接连接成功")
        # 列出数据库
        dbs = c.list_database_names()
        if "knowledge_skill" in dbs:
            results["database"] = "exists"
            results["details"].append("数据库 knowledge_skill 存在")
            colls = c["knowledge_skill"].list_collection_names()
            ds_colls = [c for c in colls if c.startswith("ds_")]
            results["details"].append(f"数据集集合: {len(ds_colls)} 个")
        else:
            results["database"] = "missing"
            results["details"].append("数据库 knowledge_skill 不存在（首次使用正常）")
        c.close()
    except Exception as e:
        results["connection"] = "failed"
        results["details"].append(f"MongoDB 连接失败: {e}")

    return results


def diagnose_easydataset():
    """诊断 EasyDataset 服务"""
    results = {"status": "unknown", "details": []}
    
    try:
        r = subprocess.run(["docker", "ps", "--format", "{{.Names}}\t{{.Status}}"],
                          capture_output=True, text=True, timeout=5)
        ed_line = [l for l in r.stdout.split('\n') if 'easy-dataset' in l]
        if ed_line:
            results["container"] = ed_line[0]
            results["status"] = "running"
            results["details"].append(f"Docker 容器运行中: {ed_line[0]}")
        else:
            results["status"] = "stopped"
            results["details"].append("未找到 easy-dataset Docker 容器")
    except Exception as e:
        results["status"] = "error"
        results["details"].append(f"Docker 检查失败: {e}")

    # 尝试 API 调用
    try:
        import urllib.request
        resp = urllib.request.urlopen("http://localhost:1717/api/projects", timeout=5)
        data = resp.read().decode()
        results["api"] = "ok"
        results["details"].append(f"EasyDataset API 正常 (返回 {len(data)} bytes)")
    except Exception as e:
        results["api"] = "failed"
        results["details"].append(f"EasyDataset API 不可达: {e}")

    return results


def diagnose_config():
    """检查配置文件"""
    skill_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(os.path.dirname(skill_root), "config.json")
    
    if not os.path.exists(config_path):
        return {"status": "missing", "path": config_path, 
                "detail": f"配置文件不存在: {config_path}"}

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            cfg = json.load(f)
        llm = cfg.get("llm", {})
        issues = []
        if not llm.get("base_url"): issues.append("llm.base_url 为空")
        if not llm.get("api_key"): issues.append("llm.api_key 为空")
        if not llm.get("model"): issues.append("llm.model 为空")
        
        return {
            "status": "issues" if issues else "ok",
            "path": config_path,
            "issues": issues,
            "detail": "配置正常" if not issues else f"发现 {len(issues)} 个问题: {', '.join(issues)}"
        }
    except json.JSONDecodeError as e:
        return {"status": "invalid", "path": config_path, "detail": f"JSON 格式错误: {e}"}
    except Exception as e:
        return {"status": "error", "path": config_path, "detail": f"读取失败: {e}"}


def diagnose_logs():
    """获取最近日志（从 main.py 的输出）"""
    skill_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_dir = os.path.join(os.path.dirname(skill_root), "logs")
    results = {"found": False}
    if os.path.exists(log_dir):
        log_files = sorted([f for f in os.listdir(log_dir) if f.endswith('.log')], reverse=True)
        if log_files:
            log_path = os.path.join(log_dir, log_files[0])
            try:
                with open(log_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                results["found"] = True
                results["file"] = log_files[0]
                results["lines"] = len(lines)
                results["last_20"] = lines[-20:]
            except Exception:
                pass
    return results


def run(full=False):
    print(f"{'# ' * 30}")
    print(f"JY_Knowledge_Skill 问题诊断")
    print(f"{'# ' * 30}\n")

    # 系统信息
    print(f"Python: {sys.version}")
    print(f"工作目录: {os.getcwd()}\n")

    # 配置文件
    cfg = diagnose_config()
    status = {"ok": "OK", "issues": "WARN", "missing": "MISS", "invalid": "INVALID", "error": "ERROR"}
    print(f"{status.get(cfg['status'], '❓')} 配置文件: {cfg.get('detail', '')}")
    if cfg.get("issues"):
        for issue in cfg["issues"]:
            print(f"   → {issue}")

    # MongoDB
    print(f"\n--- MongoDB ---")
    mongo = diagnose_mongodb()
    print(f"   状态: {mongo['status']}")
    for d in mongo["details"]:
        print(f"   {d}")

    # EasyDataset
    print(f"\n--- EasyDataset ---")
    ed = diagnose_easydataset()
    print(f"   状态: {ed['status']}")
    for d in ed["details"]:
        print(f"   {d}")

    # 日志
    logs = diagnose_logs()
    if logs.get("found"):
        print(f"\n--- 最近日志 ({logs['file']}, {logs['lines']}行) ---")
        for line in logs.get("last_20", []):
            print(f"   {line.rstrip()}")
    else:
        print(f"\n--- 日志 ---")
        print(f"   未找到日志文件")

    # Docker 容器总览
    if full:
        print(f"\n--- Docker 容器 ---")
        try:
            r = subprocess.run(["docker", "ps", "-a", "--format", "table {{.Names}}\t{{.Status}}\t{{.Ports}}"],
                              capture_output=True, text=True, timeout=5)
            print(r.stdout)
        except Exception as e:
            print(f"   Docker 命令失败: {e}")

    print(f"\n{'# ' * 30}")
    print("诊断完成。如问题未解决，请将以上输出提供给支持人员。")
    print(f"{'# ' * 30}")


if __name__ == "__main__":
    full = "--full" in sys.argv
    run(full=full)
