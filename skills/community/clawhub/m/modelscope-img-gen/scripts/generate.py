#!/usr/bin/env python3
"""
ModelScope 图片生成脚本
调用 ModelScope API 生成图片，支持 LoRA 配置

用法:
    py generate.py --prompt "描述文字" [选项]

示例:
    py generate.py --prompt "A golden cat"
    py generate.py --prompt "一只可爱的猫咪" --output cat.jpg
    py generate.py --prompt "动漫少女" --lora your-lora-repo-id --lora-weight 0.8
    py generate.py --prompt "风景画" --model Tongyi-MAI/Z-Image-Turbo

环境变量:
    MODELSCOPE_API_KEY: API Key (必需)
"""

import argparse
import json
import os
import sys
import time
from io import BytesIO
from pathlib import Path

try:
    import requests
    from PIL import Image
except ImportError:
    print("缺少依赖，请先安装: pip install requests pillow")
    sys.exit(1)

BASE_URL = "https://api-inference.modelscope.cn/"
DEFAULT_MODEL = "Tongyi-MAI/Z-Image-Turbo"

# 配置文件路径
CONFIG_DIR = Path.home() / ".modelscope"
CONFIG_FILE = CONFIG_DIR / "api_key"


def get_api_key(cli_key: str | None = None) -> str:
    """获取 API Key，优先级: CLI参数 > 环境变量 > 配置文件"""
    if cli_key:
        return cli_key
    
    api_key = os.environ.get("MODELSCOPE_API_KEY")
    if api_key:
        return api_key
    
    if CONFIG_FILE.exists():
        return CONFIG_FILE.read_text().strip()
    
    raise ValueError(
        "未设置 API Key。请通过以下方式之一设置:\n"
        "  1. 命令行: --api-key YOUR_KEY\n"
        "  2. 环境变量: set MODELSCOPE_API_KEY=YOUR_KEY\n"
        "  3. 配置文件: 创建 ~/.modelscope/api_key 文件"
    )


def save_api_key(api_key: str):
    """保存 API Key 到配置文件"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(api_key)
    # Windows 下设置文件权限为仅当前用户可读
    if sys.platform == "win32":
        import stat
        os.chmod(CONFIG_FILE, stat.S_IREAD | stat.S_IWRITE)
    print(f"API Key 已保存到: {CONFIG_FILE}")


def generate_image(
    prompt: str,
    model: str = DEFAULT_MODEL,
    loras: str | dict | None = None,
    output: str = "result_image.jpg",
    api_key: str | None = None,
):
    """生成图片"""
    key = get_api_key(api_key)
    
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": model,
        "prompt": prompt,
    }
    
    if loras:
        payload["loras"] = loras
    
    # 发起异步请求
    resp = requests.post(
        f"{BASE_URL}v1/images/generations",
        headers={**headers, "X-ModelScope-Async-Mode": "true"},
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
    )
    resp.raise_for_status()
    task_id = resp.json()["task_id"]
    print(f"任务已提交: {task_id}")
    
    # 轮询状态
    max_attempts = 60
    for i in range(max_attempts):
        result = requests.get(
            f"{BASE_URL}v1/tasks/{task_id}",
            headers={**headers, "X-ModelScope-Task-Type": "image_generation"},
        )
        result.raise_for_status()
        data = result.json()
        
        status = data.get("task_status", "UNKNOWN")
        print(f"[{i + 1}/{max_attempts}] 状态: {status}")
        
        if status == "SUCCEED":
            image_url = data["output_images"][0]
            print(f"下载图片: {image_url}")
            
            img_resp = requests.get(image_url)
            img_resp.raise_for_status()
            
            image = Image.open(BytesIO(img_resp.content))
            image.save(output)
            print(f"图片已保存: {output}")
            return output
        
        if status == "FAILED":
            raise RuntimeError("图片生成失败")
        
        time.sleep(5)
    
    raise TimeoutError("生成超时，请稍后重试")


def main():
    parser = argparse.ArgumentParser(
        description="ModelScope 图片生成",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --prompt "A golden cat"
  %(prog)s -p "一只可爱的猫咪" -o cat.jpg
  %(prog)s -p "动漫少女" --lora your-lora-id --lora-weight 0.8
  %(prog)s -p "风景" --lora-json '{"lora-1": 0.6, "lora-2": 0.4}'
"""
    )
    
    parser.add_argument("-p", "--prompt", required=True, help="图片描述")
    parser.add_argument("-m", "--model", default=DEFAULT_MODEL, help=f"模型 ID (默认: {DEFAULT_MODEL})")
    parser.add_argument("-o", "--output", default="result_image.jpg", help="输出文件路径")
    parser.add_argument("-l", "--lora", help="单个 LoRA repo-id")
    parser.add_argument("--lora-weight", type=float, default=1.0, help="单个 LoRA 权重")
    parser.add_argument("--lora-json", help="多 LoRA JSON 配置")
    parser.add_argument("--api-key", help="API Key")
    parser.add_argument("--save-key", metavar="KEY", help="保存 API Key 到配置文件")
    
    args = parser.parse_args()
    
    # 仅保存 API Key
    if args.save_key:
        save_api_key(args.save_key)
        return
    
    # 处理 LoRA 配置
    loras = None
    if args.lora_json:
        loras = json.loads(args.lora_json)
    elif args.lora:
        loras = args.lora
    
    try:
        generate_image(
            prompt=args.prompt,
            model=args.model,
            loras=loras,
            output=args.output,
            api_key=args.api_key,
        )
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
