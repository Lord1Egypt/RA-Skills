#!/usr/bin/env python3
"""
Agent接口脚本 - 为hermes、openclaw、qwen-code提供统一的API
作者: 北京老李 (beijingLL)
"""

import sys
import os
import json
import subprocess
from pathlib import Path

# Skill根目录
SKILL_DIR = Path(__file__).parent
SCRIPT_PATH = SKILL_DIR / "scripts" / "compress_videos.py"


def check_environment():
    """检查环境并返回状态"""
    result = {
        "ffmpeg": {"available": False, "version": "", "av1_nvenc": False},
        "gpu": {"available": False, "info": ""},
        "python_deps": {"tqdm": False},
        "can_proceed": False
    }
    
    # 检查FFmpeg
    try:
        proc = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True, text=True, timeout=10
        )
        if proc.returncode == 0:
            result["ffmpeg"]["available"] = True
            result["ffmpeg"]["version"] = proc.stdout.split('\n')[0]
            
            # 检查av1_nvenc
            enc_proc = subprocess.run(
                ["ffmpeg", "-encoders"],
                capture_output=True, text=True, timeout=10
            )
            if "av1_nvenc" in enc_proc.stdout:
                result["ffmpeg"]["av1_nvenc"] = True
    except:
        pass
    
    # 检查GPU
    try:
        proc = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"],
            capture_output=True, text=True, timeout=10
        )
        if proc.returncode == 0:
            result["gpu"]["available"] = True
            result["gpu"]["info"] = proc.stdout.strip()
    except:
        pass
    
    # 检查Python依赖
    try:
        import tqdm
        result["python_deps"]["tqdm"] = True
    except:
        pass
    
    # 判断是否可以继续
    result["can_proceed"] = (
        result["ffmpeg"]["available"] and 
        result["ffmpeg"]["av1_nvenc"] and 
        result["gpu"]["available"]
    )
    
    return result


def analyze_videos(input_dir):
    """分析目录下的视频文件"""
    video_extensions = ['.mp4', '.MP4', '.mkv', '.avi', '.mov']
    videos = []
    total_size = 0
    
    for file in sorted(os.listdir(input_dir)):
        file_path = os.path.join(input_dir, file)
        if os.path.isfile(file_path) and any(file.endswith(ext) for ext in video_extensions):
            size = os.path.getsize(file_path)
            videos.append({
                "filename": file,
                "path": file_path,
                "size_bytes": size,
                "size_mb": size / (1024 * 1024)
            })
            total_size += size
    
    return {
        "count": len(videos),
        "videos": videos,
        "total_size_bytes": total_size,
        "total_size_gb": total_size / (1024 * 1024 * 1024)
    }


def run_compression(input_dir, profile="B", test_mode=False, test_count=1, output_dir=None):
    """运行压缩任务"""
    cmd = [
        sys.executable, str(SCRIPT_PATH),
        "-i", input_dir,
        "-p", profile,
        "--test-count", str(test_count)
    ]
    
    if test_mode:
        cmd.append("--test")
    
    if output_dir:
        cmd.extend(["-o", output_dir])
    
    # 非交互模式
    cmd.append("--no-confirm")
    
    print(f"执行命令: {' '.join(cmd)}")
    
    # 执行压缩
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=3600  # 1小时超时
    )
    
    return {
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "command": ' '.join(cmd)
    }


def main():
    """主函数 - Agent调用入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="li_nvvideocodec Agent接口")
    parser.add_argument("--action", choices=["check", "analyze", "compress"], required=True,
                       help="操作类型: check=检查环境, analyze=分析视频, compress=压缩")
    parser.add_argument("--input-dir", "-i", help="输入视频目录")
    parser.add_argument("--output-dir", "-o", help="输出目录")
    parser.add_argument("--profile", "-p", default="B", choices=["A", "B", "C"],
                       help="压缩方案")
    parser.add_argument("--test", action="store_true", help="测试模式")
    parser.add_argument("--test-count", type=int, default=1, help="测试文件数")
    
    args = parser.parse_args()
    
    if args.action == "check":
        # 检查环境
        env = check_environment()
        print(json.dumps(env, indent=2, ensure_ascii=False))
        sys.exit(0 if env["can_proceed"] else 1)
    
    elif args.action == "analyze":
        # 分析视频
        if not args.input_dir:
            print("错误: 需要 --input-dir 参数")
            sys.exit(1)
        
        analysis = analyze_videos(args.input_dir)
        print(json.dumps(analysis, indent=2, ensure_ascii=False))
        sys.exit(0)
    
    elif args.action == "compress":
        # 压缩视频
        if not args.input_dir:
            print("错误: 需要 --input-dir 参数")
            sys.exit(1)
        
        result = run_compression(
            input_dir=args.input_dir,
            profile=args.profile,
            test_mode=args.test,
            test_count=args.test_count,
            output_dir=args.output_dir
        )
        
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(result["returncode"])


if __name__ == "__main__":
    main()
