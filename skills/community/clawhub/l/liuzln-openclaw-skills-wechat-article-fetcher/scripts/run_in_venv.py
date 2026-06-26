#!/usr/bin/env python3
"""
在虚拟环境中运行微信公众号文章爬取工具
"""

import argparse
import os
import sys
import subprocess
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="在虚拟环境中运行微信公众号文章爬取工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 爬取单篇文章
  python run_in_venv.py https://mp.weixin.qq.com/s/xxx --venv /path/to/playwright-env
  
  # 批量爬取
  python run_in_venv.py --urls-file urls.txt --venv /path/to/playwright-env --batch
        """
    )
    
    parser.add_argument("url_or_args", nargs="*", help="文章 URL 或批量参数")
    parser.add_argument("--venv", "-v", required=True, help="虚拟环境路径")
    parser.add_argument("--batch", action="store_true", help="使用批量爬取模式")
    parser.add_argument("--script", "-s", help="要运行的脚本路径（可选）")
    parser.add_argument("--script-args", nargs=argparse.REMAINDER, help="传递给脚本的参数")
    
    args = parser.parse_args()
    
    # 检查虚拟环境
    venv_path = Path(args.venv)
    if not venv_path.exists():
        print(f"❌ 虚拟环境不存在: {venv_path}")
        sys.exit(1)
    
    # 找到虚拟环境的 Python
    python_path = venv_path / "bin" / "python"
    if not python_path.exists():
        python_path = venv_path / "Scripts" / "python.exe"
    
    if not python_path.exists():
        print(f"❌ 找不到虚拟环境的 Python: {python_path}")
        sys.exit(1)
    
    # 确定要运行的脚本
    script_dir = Path(__file__).parent
    
    if args.script:
        script_path = Path(args.script)
    elif args.batch:
        script_path = script_dir / "batch_fetch.py"
    else:
        script_path = script_dir / "fetch.py"
    
    if not script_path.exists():
        print(f"❌ 脚本不存在: {script_path}")
        sys.exit(1)
    
    # 构建参数
    cmd = [str(python_path), str(script_path)]
    
    if args.url_or_args:
        cmd.extend(args.url_or_args)
    
    if args.script_args:
        cmd.extend(args.script_args)
    
    print("="*80)
    print("微信公众号文章爬取工具（虚拟环境模式）")
    print("="*80)
    print(f"🐍 虚拟环境: {venv_path}")
    print(f"📜 运行脚本: {script_path.name}")
    print(f"🚀 执行命令: {' '.join(cmd)}")
    print("="*80)
    print()
    
    # 运行脚本
    try:
        result = subprocess.run(cmd, cwd=os.getcwd())
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\n⚠️  被用户中断")
        sys.exit(130)


if __name__ == "__main__":
    main()
