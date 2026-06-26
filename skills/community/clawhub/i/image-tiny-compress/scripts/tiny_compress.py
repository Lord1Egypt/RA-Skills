#!/usr/bin/env python3
"""
TinyPNG/Tinify 图片压缩工具
通过 TinyPNG 网页端免费接口压缩图片，无需 API Key。
支持 PNG、JPEG、WebP 格式，单张最大 5MB。

用法:
    python tiny_compress.py compress <file1> [file2] ... [--output-dir <dir>] [--server cn|global]
    python tiny_compress.py compress-dir <dir> [--output-dir <dir>] [--recursive] [--server cn|global]

参数:
    compress       压缩指定的一张或多张图片
    compress-dir   压缩整个目录下的图片
    --output-dir   输出目录（默认在原文件同目录生成 _compressed 后缀文件）
    --recursive    递归处理子目录
    --server       选择服务器: cn (中国站, 更快) 或 global (国际站, 默认)
    --overwrite    直接覆盖原文件
"""

import os
import sys
import json
import time
import random
import argparse
import hashlib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import requests
except ImportError:
    print("错误: 需要安装 requests 库")
    print("请运行: pip install requests")
    sys.exit(1)


# ============================================================
# 配置
# ============================================================
SERVERS = {
    "global": "https://tinypng.com/backend/opt/shrink",
    "cn": "https://tinify.cn/backend/opt/shrink",
}

SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_CONCURRENT = 1  # 最大并发数（网页端接口需要串行以避免限流）
MAX_BATCH_SIZE = 20  # 单批次最多处理 20 张
REQUEST_DELAY = 1.5  # 请求间隔（秒），避免被限流

# User-Agent 池，随机选择以避免被限制
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
]


def get_random_headers():
    """生成随机请求头，模拟浏览器访问"""
    ip = ".".join(str(random.randint(1, 254)) for _ in range(4))
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "X-Forwarded-For": ip,
        "Cache-Control": "no-cache",
        "Content-Type": "application/x-www-form-urlencoded",
        "Postman-Token": str(int(time.time() * 1000)),
    }


def format_size(size_bytes):
    """格式化文件大小"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"


def compress_single_image(file_path, output_path=None, server="global", overwrite=False):
    """
    压缩单张图片
    
    Args:
        file_path: 输入图片路径
        output_path: 输出路径（可选）
        server: 服务器选择 ("global" 或 "cn")
        overwrite: 是否覆盖原文件
    
    Returns:
        dict: 压缩结果信息
    """
    file_path = Path(file_path).resolve()
    
    # 验证文件
    if not file_path.exists():
        return {"success": False, "file": str(file_path), "error": "文件不存在"}
    
    if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        return {"success": False, "file": str(file_path), "error": f"不支持的格式: {file_path.suffix}"}
    
    original_size = file_path.stat().st_size
    if original_size > MAX_FILE_SIZE:
        return {"success": False, "file": str(file_path), "error": f"文件过大: {format_size(original_size)} (最大 5MB)"}
    
    if original_size == 0:
        return {"success": False, "file": str(file_path), "error": "文件为空"}
    
    # 确定输出路径
    if overwrite:
        final_output = file_path
    elif output_path:
        final_output = Path(output_path).resolve()
    else:
        # 默认在同目录下生成 _compressed 后缀的文件
        final_output = file_path.parent / f"{file_path.stem}_compressed{file_path.suffix}"
    
    # 确保输出目录存在
    final_output.parent.mkdir(parents=True, exist_ok=True)
    
    url = SERVERS.get(server, SERVERS["global"])
    
    try:
        # Step 1: 上传图片进行压缩（带重试）
        with open(file_path, "rb") as f:
            image_data = f.read()
        
        max_retries = 3
        resp = None
        last_error = None
        
        for attempt in range(max_retries):
            try:
                headers = get_random_headers()  # 每次重试换一组headers
                if attempt > 0:
                    wait_time = 2 * attempt  # 指数退避
                    time.sleep(wait_time)
                resp = requests.post(url, data=image_data, headers=headers, timeout=60)
                if resp.status_code in (200, 201):
                    break
                last_error = f"HTTP {resp.status_code}"
            except requests.exceptions.ConnectionError as e:
                last_error = f"Connection error (attempt {attempt + 1})"
                if attempt < max_retries - 1:
                    continue
            except requests.exceptions.Timeout:
                last_error = f"Timeout (attempt {attempt + 1})"
                if attempt < max_retries - 1:
                    continue
        
        if resp is None or resp.status_code not in (200, 201):
            return {
                "success": False,
                "file": str(file_path),
                "error": f"Upload failed after {max_retries} attempts: {last_error}"
            }
        
        result = resp.json()
        
        if "output" not in result:
            return {
                "success": False,
                "file": str(file_path),
                "error": f"服务器返回异常: {json.dumps(result, ensure_ascii=False)[:200]}"
            }
        
        output_info = result["output"]
        compressed_url = output_info.get("url")
        compressed_size = output_info.get("size", 0)
        compression_ratio = output_info.get("ratio", 1.0)
        output_type = output_info.get("type", "unknown")
        
        if not compressed_url:
            return {
                "success": False,
                "file": str(file_path),
                "error": "未获取到压缩后的下载地址"
            }
        
        # Step 2: 下载压缩后的图片
        download_resp = requests.get(compressed_url, timeout=60)
        
        if download_resp.status_code != 200:
            return {
                "success": False,
                "file": str(file_path),
                "error": f"下载失败 (HTTP {download_resp.status_code})"
            }
        
        # Step 3: 保存文件
        with open(final_output, "wb") as f:
            f.write(download_resp.content)
        
        saved_bytes = original_size - compressed_size
        saved_percent = (1 - compression_ratio) * 100
        
        return {
            "success": True,
            "file": str(file_path),
            "output": str(final_output),
            "original_size": original_size,
            "compressed_size": compressed_size,
            "saved_bytes": saved_bytes,
            "saved_percent": round(saved_percent, 1),
            "compression_ratio": round(compression_ratio, 4),
            "type": output_type,
        }
        
    except requests.exceptions.Timeout:
        return {"success": False, "file": str(file_path), "error": "请求超时 (60s)"}
    except requests.exceptions.ConnectionError:
        return {"success": False, "file": str(file_path), "error": "网络连接失败"}
    except Exception as e:
        return {"success": False, "file": str(file_path), "error": str(e)}


def compress_batch(file_paths, output_dir=None, server="global", overwrite=False, max_workers=MAX_CONCURRENT):
    """
    批量压缩图片
    
    Args:
        file_paths: 图片路径列表
        output_dir: 输出目录（可选）
        server: 服务器选择
        overwrite: 是否覆盖原文件
        max_workers: 最大并发数
    
    Returns:
        list[dict]: 每张图片的压缩结果
    """
    results = []
    total = len(file_paths)
    
    if total == 0:
        print("没有找到需要压缩的图片")
        return results
    
    if total > MAX_BATCH_SIZE:
        print(f"[WARN] file count ({total}) exceeds batch limit ({MAX_BATCH_SIZE}), will process in batches")
    
    print(f"\n[IMG] Ready to compress {total} image(s)...")
    print(f"[SERVER] {'China (tinify.cn)' if server == 'cn' else 'Global (tinypng.com)'}")
    print(f"[WORKERS] {max_workers}")
    if output_dir:
        print(f"[OUTPUT] {output_dir}")
    elif overwrite:
        print("[MODE] Overwrite original files")
    else:
        print("[MODE] Generate _compressed suffix files")
    print("=" * 60)
    
    def process_file(file_path):
        if output_dir:
            out_path = Path(output_dir) / Path(file_path).name
        else:
            out_path = None
        return compress_single_image(file_path, out_path, server, overwrite)
    
    completed = 0
    total_saved = 0
    total_original = 0
    
    # 串行处理，每次请求之间添加间隔以避免被限流
    for idx, fp in enumerate(file_paths):
        if idx > 0:
            time.sleep(REQUEST_DELAY)
        
        completed += 1
        result = process_file(fp)
        results.append(result)
        
        if result["success"]:
            total_saved += result["saved_bytes"]
            total_original += result["original_size"]
            print(
                f"  [{completed}/{total}] [OK] {Path(result['file']).name} "
                f"| {format_size(result['original_size'])} -> {format_size(result['compressed_size'])} "
                f"| saved {result['saved_percent']}%"
            )
        else:
            print(f"  [{completed}/{total}] [FAIL] {Path(result['file']).name} | {result['error']}")
    
    # 汇总
    success_count = sum(1 for r in results if r["success"])
    fail_count = total - success_count
    
    print("=" * 60)
    print(f"\n[DONE] Compression complete!")
    print(f"   Success: {success_count} | Failed: {fail_count}")
    if total_original > 0:
        overall_ratio = (1 - (total_original - total_saved) / total_original) * 100 if total_saved > 0 else 0
        print(f"   Total saved: {format_size(total_saved)} ({overall_ratio:.1f}%)")
    
    return results


def collect_images(directory, recursive=False):
    """收集目录中的图片文件"""
    directory = Path(directory).resolve()
    if not directory.is_dir():
        print(f"错误: {directory} 不是有效目录")
        return []
    
    images = []
    if recursive:
        for ext in SUPPORTED_EXTENSIONS:
            images.extend(directory.rglob(f"*{ext}"))
            images.extend(directory.rglob(f"*{ext.upper()}"))
    else:
        for ext in SUPPORTED_EXTENSIONS:
            images.extend(directory.glob(f"*{ext}"))
            images.extend(directory.glob(f"*{ext.upper()}"))
    
    # 去重并排序
    seen = set()
    unique_images = []
    for img in sorted(images):
        img_resolved = img.resolve()
        if img_resolved not in seen:
            seen.add(img_resolved)
            unique_images.append(str(img_resolved))
    
    return unique_images


def main():
    parser = argparse.ArgumentParser(
        description="TinyPNG/Tinify 图片压缩工具 — 无需 API Key",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 压缩单张图片
  python tiny_compress.py compress photo.png

  # 压缩多张图片到指定目录
  python tiny_compress.py compress img1.png img2.jpg --output-dir ./compressed

  # 使用中国站压缩（更快）
  python tiny_compress.py compress photo.png --server cn

  # 压缩整个目录
  python tiny_compress.py compress-dir ./images --output-dir ./compressed

  # 递归压缩目录并覆盖原文件
  python tiny_compress.py compress-dir ./images --recursive --overwrite
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # compress 子命令
    compress_parser = subparsers.add_parser("compress", help="压缩指定的图片文件")
    compress_parser.add_argument("files", nargs="+", help="图片文件路径")
    compress_parser.add_argument("--output-dir", help="输出目录")
    compress_parser.add_argument("--server", choices=["cn", "global"], default="global", help="服务器 (默认: global)")
    compress_parser.add_argument("--overwrite", action="store_true", help="覆盖原文件")
    
    # compress-dir 子命令
    dir_parser = subparsers.add_parser("compress-dir", help="压缩目录下的所有图片")
    dir_parser.add_argument("directory", help="图片目录路径")
    dir_parser.add_argument("--output-dir", help="输出目录")
    dir_parser.add_argument("--recursive", action="store_true", help="递归处理子目录")
    dir_parser.add_argument("--server", choices=["cn", "global"], default="global", help="服务器 (默认: global)")
    dir_parser.add_argument("--overwrite", action="store_true", help="覆盖原文件")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    if args.command == "compress":
        # 验证文件存在
        valid_files = []
        for f in args.files:
            p = Path(f).resolve()
            if p.exists():
                valid_files.append(str(p))
            else:
                print(f"[WARN] Skip missing file: {f}")
        
        if not valid_files:
            print("错误: 没有有效的图片文件")
            sys.exit(1)
        
        results = compress_batch(
            valid_files,
            output_dir=args.output_dir,
            server=args.server,
            overwrite=args.overwrite,
        )
    
    elif args.command == "compress-dir":
        images = collect_images(args.directory, args.recursive)
        
        if not images:
            print(f"在 {args.directory} 中没有找到支持的图片文件")
            sys.exit(0)
        
        results = compress_batch(
            images,
            output_dir=args.output_dir,
            server=args.server,
            overwrite=args.overwrite,
        )
    
    # 输出 JSON 结果（供程序解析）
    if "--json" in sys.argv:
        print("\n--- JSON OUTPUT ---")
        print(json.dumps(results, ensure_ascii=False, indent=2))
    
    # 返回成功/失败的退出码
    if results and all(r["success"] for r in results):
        sys.exit(0)
    elif results and any(r["success"] for r in results):
        sys.exit(0)  # 部分成功也返回 0
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
