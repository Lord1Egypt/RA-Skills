#!/usr/bin/env python3
"""
一键运行完整流程脚本

执行完整的爬取 -> 提取 -> 整理 -> 总结流程
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from datetime import datetime


# 脚本路径
SCRIPTS_DIR = Path(__file__).parent
CRAWL_SCRIPT = SCRIPTS_DIR / "crawl.py"
EXTRACT_SCRIPT = SCRIPTS_DIR / "extract.py"
ORGANIZE_SCRIPT = SCRIPTS_DIR / "organize.py"
SUMMARIZE_SCRIPT = SCRIPTS_DIR / "summarize.py"


def run_script(script_path: Path, args: list = None) -> tuple:
    """
    运行单个脚本
    
    Args:
        script_path: 脚本路径
        args: 额外参数
        
    Returns:
        (returncode, output_file)
    """
    cmd = [sys.executable, str(script_path)]
    if args:
        cmd.extend(args)
    
    print(f"\n{'='*60}")
    print(f"运行: {script_path.name}")
    print(f"{'='*60}\n")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        # 打印输出
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        
        # 解析输出文件路径
        output_file = None
        for line in result.stdout.split('\n'):
            if line.startswith('OUTPUT_FILE:'):
                output_file = line.replace('OUTPUT_FILE:', '').strip()
                break
        
        return result.returncode, output_file
        
    except Exception as e:
        print(f"运行脚本时出错: {e}", file=sys.stderr)
        return 1, None


def run_pipeline(
    url: str = None,
    min_score: int = 0,
    skip_crawl: bool = False,
    skip_extract: bool = False,
    skip_organize: bool = False,
    skip_summarize: bool = False,
    input_file: str = None,
) -> int:
    """
    运行完整流程
    
    Args:
        url: 目标 URL
        min_score: 最小分数阈值
        skip_crawl: 跳过爬取步骤
        skip_extract: 跳过提取步骤
        skip_organize: 跳过整理步骤
        skip_summarize: 跳过总结步骤
        input_file: 输入文件（用于跳过某些步骤时）
        
    Returns:
        退出码
    """
    start_time = datetime.now()
    
    print("\n" + "="*60)
    print("HN Crawler Skill - 完整流程")
    print("="*60)
    print(f"开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"目标网站: {url or 'https://hn.aimaker.dev/'}")
    print("="*60)
    
    current_file = input_file
    
    # Step 1: Crawl
    if not skip_crawl:
        crawl_args = []
        if url:
            crawl_args.extend(["--url", url])
        
        returncode, output_file = run_script(CRAWL_SCRIPT, crawl_args)
        if returncode != 0:
            print("\n[Pipeline] ❌ 爬取步骤失败", file=sys.stderr)
            return 1
        current_file = output_file
        print("\n[Pipeline] ✅ 爬取完成")
    else:
        print("\n[Pipeline] ⏭️ 跳过爬取步骤")
    
    # Step 2: Extract
    if not skip_extract:
        extract_args = []
        if current_file:
            extract_args.append(current_file)
        
        returncode, output_file = run_script(EXTRACT_SCRIPT, extract_args)
        if returncode != 0:
            print("\n[Pipeline] ❌ 提取步骤失败", file=sys.stderr)
            return 1
        current_file = output_file
        print("\n[Pipeline] ✅ 提取完成")
    else:
        print("\n[Pipeline] ⏭️ 跳过提取步骤")
    
    # Step 3: Organize
    if not skip_organize:
        organize_args = []
        if current_file:
            organize_args.append(current_file)
        if min_score > 0:
            organize_args.extend(["--min-score", str(min_score)])
        
        returncode, output_file = run_script(ORGANIZE_SCRIPT, organize_args)
        if returncode != 0:
            print("\n[Pipeline] ❌ 整理步骤失败", file=sys.stderr)
            return 1
        current_file = output_file
        print("\n[Pipeline] ✅ 整理完成")
    else:
        print("\n[Pipeline] ⏭️ 跳过整理步骤")
    
    # Step 4: Summarize
    if not skip_summarize:
        summarize_args = []
        if current_file:
            summarize_args.append(current_file)
        
        returncode, output_file = run_script(SUMMARIZE_SCRIPT, summarize_args)
        if returncode != 0:
            print("\n[Pipeline] ❌ 总结步骤失败", file=sys.stderr)
            return 1
        current_file = output_file
        print("\n[Pipeline] ✅ 总结完成")
    else:
        print("\n[Pipeline] ⏭️ 跳过总结步骤")
    
    # 完成
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("\n" + "="*60)
    print("流程完成！")
    print("="*60)
    print(f"结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"总耗时: {duration:.2f} 秒")
    if current_file:
        print(f"最终输出: {current_file}")
    print("="*60)
    
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="一键运行 HN Crawler 完整流程",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 运行完整流程
  python run_pipeline.py
  
  # 指定目标 URL
  python run_pipeline.py --url https://hn.aimaker.dev/
  
  # 只运行提取后的步骤（跳过爬取）
  python run_pipeline.py --skip-crawl --input-file data/raw/hn_aimaker_xxx.html
  
  # 只运行总结步骤
  python run_pipeline.py --skip-crawl --skip-extract --skip-organize --input-file data/organized/articles_organized_xxx.json
  
  # 过滤低分文章
  python run_pipeline.py --min-score 50
        """
    )
    
    parser.add_argument(
        "--url",
        default=os.getenv("TARGET_URL", "https://hn.aimaker.dev/"),
        help="目标 URL (默认: https://hn.aimaker.dev/)"
    )
    parser.add_argument(
        "--min-score",
        type=int,
        default=0,
        help="最小分数阈值 (默认: 0)"
    )
    parser.add_argument(
        "--skip-crawl",
        action="store_true",
        help="跳过爬取步骤"
    )
    parser.add_argument(
        "--skip-extract",
        action="store_true",
        help="跳过提取步骤"
    )
    parser.add_argument(
        "--skip-organize",
        action="store_true",
        help="跳过整理步骤"
    )
    parser.add_argument(
        "--skip-summarize",
        action="store_true",
        help="跳过总结步骤"
    )
    parser.add_argument(
        "--input-file",
        help="输入文件路径（用于跳过某些步骤时）"
    )
    
    args = parser.parse_args()
    
    # 检查是否所有步骤都被跳过
    if all([args.skip_crawl, args.skip_extract, args.skip_organize, args.skip_summarize]):
        print("错误: 所有步骤都被跳过，没有什么可做的", file=sys.stderr)
        return 1
    
    # 如果跳过了前面的步骤但没有提供输入文件，报错
    if args.skip_crawl and not args.input_file:
        print("错误: 跳过爬取步骤时需要提供 --input-file", file=sys.stderr)
        return 1
    
    return run_pipeline(
        url=args.url,
        min_score=args.min_score,
        skip_crawl=args.skip_crawl,
        skip_extract=args.skip_extract,
        skip_organize=args.skip_organize,
        skip_summarize=args.skip_summarize,
        input_file=args.input_file,
    )


if __name__ == "__main__":
    sys.exit(main())
