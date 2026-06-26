#!/usr/bin/env python3
"""
GitLab MR Review Pipeline - 清理脚本
清理临时文件和旧的报告文件
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

REPORTS_DIR = Path("mr-reports")
FILE_REPORT = Path("file/mr-code-review-report.md")
PROMPT_FILE = Path("/tmp/code_review_prompt.txt")


def cleanup_temp_files():
    """清理临时 markdown 文件"""
    cleaned = []
    
    if FILE_REPORT.exists():
        FILE_REPORT.unlink()
        cleaned.append(str(FILE_REPORT))
        print(f"✓ 已清理：{FILE_REPORT}")
    
    if PROMPT_FILE.exists():
        PROMPT_FILE.unlink()
        cleaned.append(str(PROMPT_FILE))
        print(f"✓ 已清理：{PROMPT_FILE}")
    
    return cleaned


def cleanup_old_reports(days=7):
    """清理指定天数前的 PDF 报告"""
    if not REPORTS_DIR.exists():
        print("ℹ️  报告目录不存在")
        return []
    
    cutoff = datetime.now() - timedelta(days=days)
    cleaned = []
    
    for pdf_file in REPORTS_DIR.glob("*.pdf"):
        try:
            mtime = datetime.fromtimestamp(pdf_file.stat().st_mtime)
            if mtime < cutoff:
                file_size = pdf_file.stat().st_size
                pdf_file.unlink()
                cleaned.append({
                    "file": str(pdf_file),
                    "size": file_size,
                    "age": (datetime.now() - mtime).days
                })
                print(f"✓ 已清理：{pdf_file} ({file_size/1024:.1f}KB, {cutoff - mtime}天前)")
        except Exception as e:
            print(f"⚠️  清理失败 {pdf_file}: {e}")
    
    return cleaned


def show_stats():
    """显示统计信息"""
    print("\n📊 存储统计\n")
    
    # 临时文件
    temp_count = sum(1 for f in [FILE_REPORT, PROMPT_FILE] if f.exists())
    print(f"临时文件：{temp_count} 个")
    
    # PDF 报告
    if REPORTS_DIR.exists():
        pdf_files = list(REPORTS_DIR.glob("*.pdf"))
        total_size = sum(f.stat().st_size for f in pdf_files)
        print(f"PDF 报告：{len(pdf_files)} 个 ({total_size/1024:.1f}KB)")
        
        # 按时间分组
        now = datetime.now()
        today = sum(1 for f in pdf_files if (now - datetime.fromtimestamp(f.stat().st_mtime)).days == 0)
        week = sum(1 for f in pdf_files if (now - datetime.fromtimestamp(f.stat().st_mtime)).days <= 7)
        month = sum(1 for f in pdf_files if (now - datetime.fromtimestamp(f.stat().st_mtime)).days <= 30)
        
        print(f"  - 今天：{today} 个")
        print(f"  - 7 天内：{week} 个")
        print(f"  - 30 天内：{month} 个")
    else:
        print("PDF 报告：0 个")
    
    print()


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="清理临时文件和旧报告")
    parser.add_argument("--days", type=int, default=7, help="清理 N 天前的文件（默认 7）")
    parser.add_argument("--stats", action="store_true", help="显示存储统计")
    parser.add_argument("--all", action="store_true", help="清理所有文件（包括临时和旧报告）")
    
    args = parser.parse_args()
    
    print("🧹 GitLab MR Review Pipeline - 清理工具\n")
    
    if args.stats:
        show_stats()
    
    if args.all or args.days:
        # 清理临时文件
        temp_cleaned = cleanup_temp_files()
        
        # 清理旧报告
        old_cleaned = cleanup_old_reports(args.days)
        
        # 总结
        print(f"\n✅ 清理完成")
        print(f"   临时文件：{len(temp_cleaned)} 个")
        print(f"   旧报告：{len(old_cleaned)} 个")
        
        if old_cleaned:
            total_size = sum(f['size'] for f in old_cleaned)
            print(f"   释放空间：{total_size/1024:.1f}KB")
    else:
        parser.print_help()
    
    sys.exit(0)


if __name__ == "__main__":
    main()
