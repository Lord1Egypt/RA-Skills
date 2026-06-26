#!/usr/bin/env python3
"""
MiniMax 图像生成脚本
使用MiniMax API进行文生图
"""

import os
import sys
import json
import requests
import datetime
from pathlib import Path

# API配置
API_URL = "https://api.minimaxi.com/v1/image_generation"
MODEL = "image-01"


class MiniMaxImage:
    """MiniMax图像生成客户端"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("MINIMAX_API_KEY", "")
        if not self.api_key:
            raise ValueError("API Key未设置，请提供MINIMAX_API_KEY环境变量或初始化时传入")
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def generate(self, prompt, aspect_ratio="16:9", n=1, response_format="url"):
        """
        生成图片
        
        Args:
            prompt: 图片描述文本
            aspect_ratio: 宽高比 (16:9, 1:1, 9:16, etc.)
            n: 生成数量 (1-4)
            response_format: 返回格式 (url)
        
        Returns:
            dict: 包含image_urls列表
        """
        payload = {
            "model": MODEL,
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "response_format": response_format,
            "n": min(max(1, n), 4),
            "prompt_optimizer": True
        }
        
        print(f"🎨 生成图片: {prompt[:50]}...")
        
        try:
            response = requests.post(
                API_URL,
                json=payload,
                headers=self.headers,
                timeout=120
            )
            response.raise_for_status()
            result = response.json()
            
            if "data" in result and len(result["data"]) > 0:
                image_urls = [item.get("url", "") for item in result["data"]]
                print(f"✅ 成功生成 {len(image_urls)} 张图片")
                return {"image_urls": image_urls, "full_response": result}
            else:
                print(f"❌ 生成失败: {result}")
                return {"image_urls": [], "full_response": result}
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 请求失败: {e}")
            return {"image_urls": [], "error": str(e)}
    
    def save_images(self, image_urls, output_dir=None):
        """
        下载并保存图片
        
        Args:
            image_urls: 图片URL列表
            output_dir: 输出目录
        
        Returns:
            list: 保存的文件路径列表
        """
        if not output_dir:
            output_dir = Path.home() / "Desktop" / "MiniMaxImages"
        
        output_dir = Path(output_dir)
        date_str = datetime.datetime.now().strftime("%Y%m%d")
        save_dir = output_dir / date_str
        save_dir.mkdir(parents=True, exist_ok=True)
        
        saved_paths = []
        
        for i, url in enumerate(image_urls):
            try:
                print(f"📥 下载第{i+1}张图片...")
                img_response = requests.get(url, timeout=60)
                img_response.raise_for_status()
                
                filename = save_dir / f"image_{i+1}_{datetime.datetime.now().strftime('%H%M%S')}.png"
                with open(filename, "wb") as f:
                    f.write(img_response.content)
                
                print(f"✅ 已保存: {filename}")
                saved_paths.append(str(filename))
                
            except Exception as e:
                print(f"❌ 下载失败: {e}")
        
        return saved_paths


def main():
    if len(sys.argv) < 2:
        print("用法: python minimax_image.py <prompt> [--ratio 16:9] [--num 1] [--output /path/to/output]")
        print("示例: python minimax_image.py '蓝色科技风格PPT封面' --ratio 16:9 --num 2")
        sys.exit(1)
    
    prompt = sys.argv[1]
    aspect_ratio = "16:9"
    num = 1
    output_dir = None
    
    # 解析参数
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--ratio" and i + 1 < len(sys.argv):
            aspect_ratio = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--num" and i + 1 < len(sys.argv):
            num = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--output" and i + 1 < len(sys.argv):
            output_dir = sys.argv[i + 1]
            i += 2
        else:
            i += 1
    
    # 获取API Key
    api_key = os.environ.get("MINIMAX_API_KEY", "")
    if not api_key:
        print("❌ 请设置环境变量 MINIMAX_API_KEY")
        print("示例: export MINIMAX_API_KEY='your-api-key-here'")
        sys.exit(1)
    
    # 生成图片
    client = MiniMaxImage(api_key)
    result = client.generate(prompt, aspect_ratio, num)
    
    if result.get("image_urls"):
        print(f"\n📋 生成结果:")
        for j, url in enumerate(result["image_urls"]):
            print(f"  {j+1}. {url}")
        
        # 自动保存
        saved = client.save_images(result["image_urls"], output_dir)
        if saved:
            print(f"\n💾 图片已保存至: {saved[0]}")
    else:
        print(f"\n❌ 生成失败: {result.get('error', '未知错误')}")


if __name__ == "__main__":
    main()