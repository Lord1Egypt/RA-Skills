#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Image for your article

@Time    : 2023/08/09 10:00:00
@File    : generate_img.py
@Software: odd_article_skills
@Desc    : 调用 ModelScope 图片生成 API 生成图片，
            并将生成的图片保存为 result_image.jpg
"""

import requests
import time
import json
from PIL import Image
from io import BytesIO

base_url = 'https://api-inference.modelscope.cn/'
api_key = "ms-c5105352-22dd-4be1-8e2d-e057ae27df8d"
model_name = "Qwen/Qwen-Image"

common_headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

def generate_image(title: str, content: str, output_file: str = "result_image.jpg"):
    response = requests.post(
        f"{base_url}v1/images/generations",
        headers={**common_headers, "X-ModelScope-Async-Mode": "true"},
        data=json.dumps({
            "model": model_name,
            "prompt": f"{title}\n{content}"
        }, ensure_ascii=False).encode('utf-8')
    )
    
    print(f"Response status: {response.status_code}")
    print(f"Response text: {response.text[:500]}")


    response.raise_for_status()
    task_id = response.json()["task_id"]

    while True:
        result = requests.get(
            f"{base_url}v1/tasks/{task_id}",
            headers={**common_headers, "X-ModelScope-Task-Type": "image_generation"},
        )
        result.raise_for_status()
        data = result.json()

        if data["task_status"] == "SUCCEED":
            image = Image.open(BytesIO(requests.get(data["output_images"][0]).content))
            image.save(output_file)
            print(f"图片已保存到: {output_file}")
            break
        elif data["task_status"] == "FAILED":
            print("Image Generation Failed.")
            break

        time.sleep(5)

if __name__ == "__main__":
    generate_image("A golden cat", "A golden cat")