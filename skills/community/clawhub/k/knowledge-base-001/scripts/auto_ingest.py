#!/usr/bin/env python3
"""
Knowledge Base 自动导入监控脚本
扫描 /tmp/openclaw/ 目录，自动将新文件导入知识库
"""
import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

# 添加 scripts 目录到路径
scripts_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, scripts_dir)

# 依赖检测
from _check_deps import check_dependencies, check_kb_ready
if not check_dependencies():
    sys.exit(1)
if not check_kb_ready():
    sys.exit(1)

from kb_manager import ingest_file, ensure_kb_exists, KB_ROOT

WATCH_DIR = Path("/tmp/openclaw")
STATE_FILE = KB_ROOT / ".auto_ingest_state.json"
SUPPORTED_EXTS = {
    '.pdf', '.docx', '.pptx', '.xlsx', '.xls', '.html', '.htm',
    '.epub', '.txt', '.csv', '.json', '.xml', '.zip', '.png',
    '.jpg', '.jpeg', '.gif', '.webp', '.mp3', '.wav', '.mp4'
}


def load_state():
    """加载已处理的文件记录"""
    if STATE_FILE.exists():
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"processed": {}, "last_run": None}


def save_state(state):
    """保存已处理的文件记录"""
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def scan_files():
    """扫描目录，返回所有支持的文件"""
    if not WATCH_DIR.exists():
        return []
    
    files = []
    for path in WATCH_DIR.iterdir():
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTS:
            # 跳过明显是系统/临时文件的
            if path.name.startswith('.') or path.name.startswith('openclaw_'):
                continue
            files.append(path)
    
    return files


def get_file_hash(filepath):
    """计算文件简单哈希（大小+修改时间）"""
    stat = os.stat(filepath)
    return f"{stat.st_size}:{stat.st_mtime}"


def auto_ingest_once(dry_run=False):
    """执行一次自动导入扫描"""
    ensure_kb_exists()
    state = load_state()
    files = scan_files()
    
    imported = []
    skipped = []
    errors = []
    
    for filepath in files:
        file_hash = get_file_hash(str(filepath))
        file_id = str(filepath)
        
        # 检查是否已处理
        if file_id in state["processed"] and state["processed"][file_id] == file_hash:
            skipped.append(str(filepath.name))
            continue
        
        # 导入文件
        try:
            if not dry_run:
                result = ingest_file(str(filepath))
                state["processed"][file_id] = file_hash
                imported.append({
                    "file": str(filepath.name),
                    "title": result["title"],
                    "category": result["category"],
                    "doc_id": result["id"]
                })
                print(f"✅ 已导入: {filepath.name} → [{result['category']}] {result['title']}")
            else:
                imported.append({"file": str(filepath.name), "dry_run": True})
                print(f"[预览] 将导入: {filepath.name}")
        except Exception as e:
            errors.append({"file": str(filepath.name), "error": str(e)})
            print(f"❌ 导入失败: {filepath.name} - {e}")
    
    state["last_run"] = datetime.now().isoformat()
    if not dry_run:
        save_state(state)
    
    return {
        "imported": imported,
        "skipped": skipped,
        "errors": errors,
        "total_files": len(files)
    }


def watch_loop(interval=30):
    """持续监控模式"""
    print(f"开始监控目录: {WATCH_DIR}")
    print(f"扫描间隔: {interval}秒")
    print("按 Ctrl+C 停止\n")
    
    try:
        while True:
            result = auto_ingest_once()
            if result["imported"]:
                print(f"\n本次导入 {len(result['imported'])} 个文件")
            if result["errors"]:
                print(f"失败 {len(result['errors'])} 个文件")
            
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n已停止监控")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="自动导入监控")
    parser.add_argument("--watch", "-w", action="store_true", help="持续监控模式")
    parser.add_argument("--interval", "-i", type=int, default=30, help="监控间隔（秒）")
    parser.add_argument("--dry-run", "-d", action="store_true", help="预览模式（不实际导入）")
    parser.add_argument("--once", "-o", action="store_true", help="只运行一次")
    
    args = parser.parse_args()
    
    if args.watch:
        watch_loop(args.interval)
    elif args.once or not args.watch:
        result = auto_ingest_once(args.dry_run)
        print(f"\n扫描完成: 共 {result['total_files']} 个文件")
        print(f"导入: {len(result['imported'])}")
        print(f"跳过: {len(result['skipped'])}")
        print(f"失败: {len(result['errors'])}")
