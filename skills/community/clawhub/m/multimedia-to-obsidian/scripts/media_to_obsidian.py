#!/usr/bin/env python3
"""
多媒体导入 Obsidian - 支持 PPT、PDF、DOCX、图片
"""
import os
import sys
import json
import base64
import subprocess
import time
import re
import argparse
from pathlib import Path

# 默认环境变量
API_KEY = os.environ.get("MINIMAX_API_KEY", os.environ.get("OPENAI_API_KEY", os.environ.get("ANTHROPIC_API_KEY", "")))
API_HOST = os.environ.get("MINIMAX_API_HOST", "https://api.minimaxi.com")
DEFAULT_MODEL = "minimax"

def understand_image(image_path, model=DEFAULT_MODEL, prompt="直接描述这张图片的业务含义和数据内容，不要罗列元素位置关系"):
    """调用多模态模型理解图片"""
    try:
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")
        
        ext = os.path.splitext(image_path)[1].lower()
        media_type = f"image/{ext[1:]}"
        if media_type == "image/jpg":
            media_type = "image/jpeg"
        
        if model == "openai":
            return understand_openai(image_data, media_type, prompt)
        elif model == "anthropic":
            return understand_anthropic(image_data, media_type, prompt)
        else:
            return understand_minimax(image_data, media_type, prompt)
            
    except Exception as e:
        return f"[失败: {str(e)}]"

def understand_minimax(image_data, media_type, prompt):
    """MiniMax VLM"""
    API_KEY = os.environ.get("MINIMAX_API_KEY", "")
    API_HOST = os.environ.get("MINIMAX_API_HOST", "https://api.minimaxi.com")
    
    if not API_KEY:
        return "[错误] 请设置 MINIMAX_API_KEY"
    
    image_url = f"data:{media_type};base64,{image_data}"
    payload = {"prompt": prompt, "image_url": image_url}
    
    cmd = [
        "curl", "-s", "--max-time", "30",
        f"{API_HOST}/v1/coding_plan/vlm",
        "-H", f"Authorization: Bearer {API_KEY}",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(payload)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=35)
    data = json.loads(result.stdout)
    
    if data.get("base_resp", {}).get("status_code") == 0:
        return data.get("content", "")
    return f"[失败: {data.get('base_resp', {}).get('status_msg', '未知错误')}]"

def understand_openai(image_data, media_type, prompt):
    """OpenAI GPT-4V"""
    API_KEY = os.environ.get("OPENAI_API_KEY", "")
    
    if not API_KEY:
        return "[错误] 请设置 OPENAI_API_KEY"
    
    import requests
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    
    payload = {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:{media_type};base64,{image_data}"}}
        ]}],
        "max_tokens": 1000
    }
    
    resp = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=60)
    data = resp.json()
    
    if "choices" in data and data["choices"]:
        return data["choices"][0]["message"]["content"]
    return f"[失败: {data.get('error', {}).get('message', '未知错误')}]"

def understand_anthropic(image_data, media_type, prompt):
    """Anthropic Claude Vision"""
    API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
    
    if not API_KEY:
        return "[错误] 请设置 ANTHROPIC_API_KEY"
    
    import requests
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01"
    }
    
    payload = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": image_data}}
        ]}]
    }
    
    resp = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=payload, timeout=60)
    data = resp.json()
    
    if "content" in data:
        for block in data["content"]:
            if block.get("type") == "text":
                return block["text"]
    return f"[失败: {data.get('error', {}).get('message', '未知错误')}]"

def extract_images_from_docx(docx_path, output_dir):
    """从 DOCX 提取图片"""
    os.makedirs(output_dir, exist_ok=True)
    subprocess.run([
        "pandoc", docx_path, "-t", "markdown",
        "--extract-media", output_dir, "-o", "/dev/null"
    ], capture_output=True)
    
    media_dir = os.path.join(output_dir, "media")
    if os.path.exists(media_dir):
        return [os.path.join(media_dir, f) for f in os.listdir(media_dir) 
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))]
    return []

def extract_images_from_pdf(pdf_path, output_dir):
    """从 PDF 提取每一页为图片"""
    os.makedirs(output_dir, exist_ok=True)
    pdf_images = []
    
    # 使用 pdftoppm 转换
    base_name = os.path.join(output_dir, "page")
    subprocess.run([
        "pdftoppm", "-png", "-r", "150", pdf_path, base_name
    ], capture_output=True)
    
    for f in os.listdir(output_dir):
        if f.startswith("page-") and f.endswith(".png"):
            pdf_images.append(os.path.join(output_dir, f))
    
    return sorted(pdf_images)

def extract_images_from_ppt(ppt_path, output_dir):
    """从 PPT 提取每一页为图片"""
    os.makedirs(output_dir, exist_ok=True)
    
    # 使用 pandoc 转换为图片
    subprocess.run([
        "pandoc", ppt_path, "-t", "slide.html", "-o", "/dev/null"
    ], capture_output=True)
    
    # 使用 python-pptx
    try:
        from pptx import Presentation
        prs = Presentation(ppt_path)
        
        ppt_images = []
        for i, slide in enumerate(prs.slides):
            # 保存 slide 为图片需要额外处理，这里简单处理只返回提示
            pass
    except:
        pass
    
    # 简单方案：转换为 PDF 再提取
    pdf_path = os.path.join(output_dir, "temp.pdf")
    subprocess.run([
        "soffice", "--headless", "--convert-to", "pdf", ppt_path,
        "--outdir", output_dir
    ], capture_output=True)
    
    if os.path.exists(pdf_path):
        return extract_images_from_pdf(pdf_path, output_dir + "_pdf")
    return []

def process_single_file(file_path, output_dir, category, model):
    """处理单个文件"""
    filename = os.path.basename(file_path)
    name_without_ext = os.path.splitext(filename)[0]
    
    # 创建输出目录
    if category:
        target_dir = os.path.join(output_dir, category)
    else:
        target_dir = os.path.join(output_dir, "导入")
    os.makedirs(target_dir, exist_ok=True)
    
    output_md = os.path.join(target_dir, f"{name_without_ext}.md")
    temp_dir = os.path.join(target_dir, f"{name_without_ext}_temp")
    
    print(f"\n处理: {filename}")
    
    # 提取图片
    images = []
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext in ['.docx', '.doc']:
        images = extract_images_from_docx(file_path, temp_dir)
    elif ext == '.pdf':
        images = extract_images_from_pdf(file_path, temp_dir)
    elif ext in ['.pptx', '.ppt']:
        images = extract_images_from_ppt(file_path, temp_dir)
    elif ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp']:
        images = [file_path]
    
    print(f"  提取到 {len(images)} 张图片")
    
    # 生成 Markdown
    with open(output_md, 'w', encoding='utf-8') as f:
        f.write(f"# {name_without_ext}\n\n")
        f.write(f"*来源: {filename}*\n\n")
        f.write("---\n\n")
        
        if images:
            f.write("## 图片理解\n\n")
            
            for idx, img_path in enumerate(images):
                if not os.path.exists(img_path):
                    continue
                
                print(f"  [{idx+1}/{len(images)}] 理解中...", end=" ", flush=True)
                
                desc = understand_image(img_path, model)
                f.write(f"### {os.path.basename(img_path)}\n\n{desc}\n\n")
                
                print("✓")
                time.sleep(0.3)
        else:
            f.write("*未提取到图片*\n")
    
    # 清理临时目录
    if os.path.exists(temp_dir):
        subprocess.run(["rm", "-rf", temp_dir], capture_output=True)
    
    print(f"  -> 已保存: {output_md}")
    return len(images)

def main():
    parser = argparse.ArgumentParser(description="多媒体导入 Obsidian")
    parser.add_argument("source", help="源文件或目录")
    parser.add_argument("output", help="Obsidian 仓库路径")
    parser.add_argument("--format", choices=["ppt", "pdf", "docx", "image", "all"], default="all", help="文件格式")
    parser.add_argument("--model", choices=["minimax", "openai", "anthropic"], default="minimax", help="模型")
    parser.add_argument("--category", default="", help="分类目录名")
    
    args = parser.parse_args()
    
    source = args.source
    output = args.output
    file_format = args.format
    model = args.model
    category = args.category
    
    # 检查输出目录
    if not os.path.exists(output):
        print(f"错误: 输出目录不存在: {output}")
        sys.exit(1)
    
    total_images = 0
    
    if os.path.isfile(source):
        total_images += process_single_file(source, output, category, model)
    elif os.path.isdir(source):
        for root, dirs, files in os.walk(source):
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                
                if file_format == "all":
                    valid = ext in ['.pptx', '.ppt', '.pdf', '.docx', '.doc', '.png', '.jpg', '.jpeg']
                else:
                    format_map = {"ppt": ['.pptx', '.ppt'], "pdf": ['.pdf'], "docx": ['.docx', '.doc'], "image": ['.png', '.jpg', '.jpeg', '.gif', '.webp']}
                    valid = ext in format_map.get(file_format, [])
                
                if valid:
                    file_path = os.path.join(root, f)
                    total_images += process_single_file(file_path, output, category, model)
    
    print(f"\n完成! 共处理 {total_images} 张图片")

if __name__ == "__main__":
    main()
