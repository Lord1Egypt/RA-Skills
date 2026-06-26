#!/usr/bin/env python3
"""
图像生成器 - 调用第三方图像生成 API
支持 OpenAI 兼容格式的图像生成 API

使用方法：
    python image_generator.py --prompt "描述图像"
    python image_generator.py --prompt "描述" --model "model-name" --size "1024x1024" --n 1
"""

import os
import sys
import argparse
import base64
from datetime import datetime
from coze_workload_identity import requests


def get_env_var(name, required=True):
    """
    获取环境变量
    
    参数:
        name: 环境变量名称
        required: 是否必需（默认 True）
    
    返回:
        环境变量的值
    
    抛出:
        ValueError: 当必需的环境变量未设置时
    """
    # 优先尝试从凭证环境变量读取（如果通过 skill_credentials 配置）
    # 凭证 Key 格式: COZE_{CREDENTIAL_NAME}_{SKILL_ID}
    # 将变量名转换为凭证 Key
    skill_id = "7615920750117191730"
    credential_var_map = {
        "IMAGE_API_URL": f"COZE_IMAGE_API_URL_{skill_id}",
        "IMAGE_API_KEY": f"COZE_IMAGE_API_KEY_{skill_id}",
        "IMAGE_MODEL_ID": f"COZE_IMAGE_MODEL_ID_{skill_id}"
    }
    
    # 优先使用凭证环境变量，然后使用普通环境变量
    credential_key = credential_var_map.get(name)
    value = os.getenv(credential_key) if credential_key else None
    
    if not value:
        value = os.getenv(name)
    
    if required and not value:
        raise ValueError(
            f"缺少必需的消费者变量: {name}\n"
            f"请使用以下命令设置消费者变量：\n"
            f"  export {name}='your-value-here'"
        )
    return value


def save_image(image_data: bytes, filename: str):
    """
    保存图像到文件
    
    参数:
        image_data: 图像二进制数据
        filename: 保存的文件名
    
    返回:
        保存的文件路径
    
    抛出:
        Exception: 保存失败时
    """
    try:
        with open(filename, 'wb') as f:
            f.write(image_data)
        print(f"图片已保存: {filename}")
        return filename
    except Exception as e:
        raise Exception(f"保存图片失败: {str(e)}")


def generate_image(
    api_url: str,
    api_key: str,
    prompt: str,
    model: str = None,
    size: str = "1024x1024",
    n: int = 1,
    quality: str = "standard",
    output_prefix: str = None
):
    """
    调用图像生成 API 生成图像
    
    参数:
        api_url: API 完整 URL
        api_key: API 密钥
        prompt: 提示词
        model: 模型名称（可选）
        size: 图片尺寸
        n: 生成数量
        quality: 图像质量
        output_prefix: 输出文件名前缀（可选）
    
    返回:
        保存的文件路径列表
    """
    # 构建请求头
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    # 构建请求体
    data = {
        "prompt": prompt,
        "n": n,
        "size": size
    }
    
    if model:
        data["model"] = model
    
    if quality:
        data["quality"] = quality
    
    # 发起请求
    try:
        print(f"正在调用图像生成 API...")
        print(f"API URL: {api_url}")
        print(f"提示词: {prompt}")
        if model:
            print(f"模型: {model}")
        print(f"尺寸: {size}, 数量: {n}, 质量: {quality}")
        
        response = requests.post(
            api_url,
            headers=headers,
            json=data,
            timeout=120
        )
        
        # 检查 HTTP 状态码
        if response.status_code >= 400:
            raise Exception(
                f"HTTP请求失败: 状态码 {response.status_code}\n"
                f"响应内容: {response.text}"
            )
        
        result = response.json()
        
        # 检查错误响应
        if "error" in result:
            error_msg = result["error"].get("message", str(result["error"]))
            raise Exception(f"API 返回错误: {error_msg}")
        
        # 检查数据格式
        if "data" not in result:
            raise Exception(f"API 响应格式不符合预期: 缺少 'data' 字段")
        
        images = result["data"]
        if not images:
            raise Exception(f"API 返回的图像列表为空")
        
        # 处理返回的图像
        saved_files = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for i, img_data in enumerate(images):
            # 生成文件名
            if output_prefix:
                filename = f"{output_prefix}_{timestamp}_{i+1}.png"
            else:
                filename = f"generated_image_{timestamp}_{i+1}.png"
            
            # 处理 base64 格式
            if "b64_json" in img_data:
                try:
                    image_bytes = base64.b64decode(img_data["b64_json"])
                    saved = save_image(image_bytes, filename)
                    saved_files.append(saved)
                except Exception as e:
                    print(f"处理图像 {i+1} 失败 (base64): {str(e)}")
            
            # 处理 URL 格式
            elif "url" in img_data:
                try:
                    img_url = img_data["url"]
                    print(f"正在下载图像 {i+1}: {img_url}")
                    
                    img_response = requests.get(img_url, timeout=60)
                    if img_response.status_code == 200:
                        saved = save_image(img_response.content, filename)
                        saved_files.append(saved)
                    else:
                        print(f"下载图像 {i+1} 失败: HTTP {img_response.status_code}")
                except Exception as e:
                    print(f"处理图像 {i+1} 失败 (URL): {str(e)}")
            
            else:
                print(f"警告: 图像 {i+1} 既没有 b64_json 也没有 url 字段")
        
        return saved_files
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"API 调用失败: {str(e)}")
    except ValueError as e:
        raise Exception(f"响应解析失败: {str(e)}")


def main():
    parser = argparse.ArgumentParser(
        description="图像生成器 - 调用第三方图像生成 API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python image_generator.py --prompt "一只可爱的猫咪"
  python image_generator.py --prompt "赛博朋克城市" --model "dall-e-3" --size "1024x1024"
  python image_generator.py --prompt "风景画" --size "1024x1024" --n 4 --quality hd
        """
    )
    
    parser.add_argument(
        "--prompt",
        type=str,
        required=True,
        help="提示词，描述要生成的图像内容（必需）"
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="模型名称（可选，默认使用消费者变量 IMAGE_MODEL_ID，如果消费者变量也未设置则由 API 服务商决定）"
    )
    parser.add_argument(
        "--size",
        type=str,
        default="1024x1024",
        help="图片尺寸（默认: 1024x1024）"
    )
    parser.add_argument(
        "--n",
        type=int,
        default=1,
        help="生成数量（默认: 1，范围: 1-10）"
    )
    parser.add_argument(
        "--quality",
        type=str,
        default="standard",
        choices=["standard", "hd"],
        help="图像质量（默认: standard，可选: standard, hd）"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="输出文件名前缀（可选，默认自动生成）"
    )
    
    args = parser.parse_args()
    
    # 验证参数
    if args.n < 1 or args.n > 10:
        print("错误: 生成数量必须在 1-10 之间", file=sys.stderr)
        sys.exit(1)
    
    try:
        # 获取消费者变量
        api_url = get_env_var("IMAGE_API_URL")
        api_key = get_env_var("IMAGE_API_KEY")
        
        # 获取模型ID（优先使用命令行参数，其次使用消费者变量）
        model = args.model if args.model else get_env_var("IMAGE_MODEL_ID", required=False)
        
        # 调用图像生成
        saved_files = generate_image(
            api_url=api_url,
            api_key=api_key,
            prompt=args.prompt,
            model=model,
            size=args.size,
            n=args.n,
            quality=args.quality,
            output_prefix=args.output
        )
        
        # 显示结果
        print(f"\n成功生成 {len(saved_files)} 张图片")
        for img in saved_files:
            print(f"  - {img}")
            
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
