"""
批量文件夹导入
扫描指定文件夹，按文件扩展名分类，对每个文件调用 collector.collect()
"""
import sys
import json
from pathlib import Path
from datetime import datetime

# 添加当前路径
sys.path.insert(0, str(Path(__file__).parent))
from collector import collect

# 文件扩展名映射
EXTENSION_MAP = {
    ".md": "markdown",
    ".txt": "text",
    ".py": "python",
    ".st": "structured_text",
    ".cpp": "cpp",
    ".c": "c",
    ".cs": "csharp",
    ".java": "java",
    ".pdf": "pdf",
    ".docx": "word",
    ".xlsx": "excel"
}


def batch_import(folder_path: str, recursive: bool = True) -> dict:
    """
    批量导入文件夹中的知识文件
    
    Args:
        folder_path: 文件夹路径
        recursive: 是否递归扫描子目录
    
    Returns:
        导入报告 {"success": int, "failed": int, "skipped": int, "details": list}
    """
    folder = Path(folder_path)
    if not folder.exists() or not folder.is_dir():
        return {"error": f"文件夹不存在: {folder_path}"}
    
    # 扫描文件
    pattern = "**/*" if recursive else "*"
    files = [f for f in folder.glob(pattern) if f.is_file()]
    
    report = {
        "folder": str(folder),
        "total_files": len(files),
        "success": 0,
        "failed": 0,
        "skipped": 0,
        "details": []
    }
    
    for file_path in files:
        ext = file_path.suffix.lower()
        file_type = EXTENSION_MAP.get(ext, "unknown")
        
        # 跳过不支持的文件类型
        if file_type == "unknown":
            report["skipped"] += 1
            report["details"].append({
                "file": str(file_path),
                "status": "skipped",
                "reason": f"不支持的文件类型: {ext}"
            })
            continue
        
        # 跳过 PDF/Word/Excel（需要额外解析库）
        if file_type in ["pdf", "word", "excel"]:
            report["skipped"] += 1
            report["details"].append({
                "file": str(file_path),
                "status": "skipped",
                "reason": f"需要额外解析库: {ext}"
            })
            continue
        
        # 读取文件内容
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            if len(content.strip()) < 50:
                report["skipped"] += 1
                report["details"].append({
                    "file": str(file_path),
                    "status": "skipped",
                    "reason": "内容过短（<50字符）"
                })
                continue
            
            # 调用 collector
            title = file_path.stem.replace("_", " ").replace("-", " ")
            result = collect(content, source_type="batch", title=title)
            
            report["success"] += 1
            report["details"].append({
                "file": str(file_path),
                "status": "success",
                "entity_id": result["entity_id"],
                "classification": result["classification"]
            })
            
        except Exception as e:
            report["failed"] += 1
            report["details"].append({
                "file": str(file_path),
                "status": "failed",
                "error": str(e)
            })
    
    # 打印报告
    print(f"\n批量导入报告")
    print(f"文件夹: {folder}")
    print(f"总文件数: {report['total_files']}")
    print(f"成功: {report['success']}")
    print(f"失败: {report['failed']}")
    print(f"跳过: {report['skipped']}")
    
    return report


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="批量导入知识文件")
    parser.add_argument("folder", help="文件夹路径")
    parser.add_argument("--no-recursive", action="store_true", help="不递归扫描子目录")
    args = parser.parse_args()
    
    report = batch_import(args.folder, recursive=not args.no_recursive)
    
    # 保存报告
    report_path = Path(args.folder) / f"import_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n报告已保存: {report_path}")
