#!/usr/bin/env python3
"""
绘本打包工具 - 完整版：包含封面，支持图片下载和重试
"""

import argparse
import json
import os
import sys
import base64
import time
import requests
from urllib.parse import urlparse


def load_metadata(book_dir):
    """加载绘本元数据 - 支持相对路径和绝对路径"""
    # 标准化路径（去除 ./ 前缀）
    book_dir = book_dir.lstrip('./')
    if not os.path.isabs(book_dir):
        book_dir = os.path.abspath(book_dir)
    
    metadata_file = os.path.join(book_dir, "metadata.json")
    if not os.path.exists(metadata_file):
        print(f"错误：找不到元数据文件 {metadata_file}")
        print(f"当前工作目录: {os.getcwd()}")
        print(f"查找的路径: {book_dir}")
        if os.path.exists(book_dir):
            print(f"目录存在，列出内容: {os.listdir(book_dir)}")
        sys.exit(1)
    with open(metadata_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_pages(book_dir):
    """加载所有页面信息 - 支持相对路径和绝对路径"""
    # 标准化路径（去除 ./ 前缀）
    book_dir = book_dir.lstrip('./')
    if not os.path.isabs(book_dir):
        book_dir = os.path.abspath(book_dir)
    
    pages_dir = os.path.join(book_dir, "pages")
    
    # 检查 pages 目录是否存在
    if not os.path.exists(pages_dir):
        print(f"警告：找不到页面目录 {pages_dir}，将尝试从 metadata.json 读取图片URL")
        return [], pages_dir
    
    page_files = sorted([f for f in os.listdir(pages_dir) 
                        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))])
    
    if not page_files:
        print("警告：pages 目录中没有找到图片文件，将尝试从 metadata.json 读取图片URL")
    
    return page_files, pages_dir


def download_image(url, max_retries=3):
    """下载图片，支持重试"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response.content
        except Exception as e:
            print(f"图片下载失败 (尝试 {attempt + 1}/{max_retries}): {url}")
            print(f"错误信息: {str(e)}")
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 2  # 递增等待时间：2s, 4s, 6s
                print(f"等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
            else:
                return None
    return None


def image_to_base64(image_path_or_url, max_retries=3):
    """将图片转换为base64，支持本地文件和URL"""
    # 检查是否是URL
    if image_path_or_url.startswith('http://') or image_path_or_url.startswith('https://'):
        # 下载URL图片
        image_data = download_image(image_path_or_url, max_retries)
        if image_data is None:
            raise Exception(f"无法下载图片: {image_path_or_url}")
        
        # 从URL推断文件格式
        parsed = urlparse(image_path_or_url)
        path = parsed.path
        img_format = path.split('.')[-1].lower()
        
        # 验证是否是真正的图片（检查文件头）
        if not is_valid_image(image_data):
            raise Exception(f"下载的文件不是有效的图片（可能是HTML错误页面），大小: {len(image_data)} 字节")
    else:
        # 读取本地文件
        if not os.path.exists(image_path_or_url):
            raise Exception(f"图片文件不存在: {image_path_or_url}")
        
        with open(image_path_or_url, 'rb') as f:
            image_data = f.read()
        
        img_format = image_path_or_url.split('.')[-1].lower()
    
    # 验证图片数据大小
    if len(image_data) < 1000:
        raise Exception(f"图片数据异常（大小只有 {len(image_data)} 字节，可能下载失败）: {image_path_or_url}")
    
    # 转换为base64
    image_base64 = base64.b64encode(image_data).decode('utf-8')
    
    # 确定MIME类型
    mime_type = {
        'png': 'image/png', 
        'jpg': 'image/jpeg', 
        'jpeg': 'image/jpeg',
        'gif': 'image/gif', 
        'webp': 'image/webp'
    }.get(img_format, 'image/png')
    
    return f"data:{mime_type};base64,{image_base64}"


def is_valid_image(image_data):
    """验证是否是有效的图片数据"""
    # 检查文件大小（小于1KB的通常是错误页面）
    if len(image_data) < 1000:
        return False
    
    # 检查文件头（Magic Numbers）
    # PNG: 89 50 4E 47
    if image_data[:4] == b'\x89PNG':
        return True
    # JPEG: FF D8 FF
    if image_data[:3] == b'\xff\xd8\xff':
        return True
    # GIF: 47 49 46 38
    if image_data[:4] == b'GIF8':
        return True
    # WebP: 52 49 46 46 ... 57 45 42 50
    if image_data[:4] == b'RIFF' and len(image_data) > 12 and image_data[8:12] == b'WEBP':
        return True
    
    # 检查是否包含HTML标签（错误页面的特征）
    text = image_data[:500].decode('utf-8', errors='ignore').lower()
    if '<html' in text or '<!doctype' in text or '<error' in text:
        return False
    
    return True


def generate_html(metadata, page_files, pages_dir, max_retries=3):
    """生成HTML绘本 - 包含封面，支持图片下载重试"""
    
    # 加载页面数据
    pages_data = []
    pages_metadata = metadata.get('pages', [])
    failed_images = []
    
    # 如果本地 pages 目录有文件，使用本地文件；否则使用 metadata.json 中的图片URL
    if page_files:
        # 使用本地文件
        source_type = "本地文件"
        image_sources = page_files
    elif pages_metadata:
        # 从 metadata.json 读取图片URL
        source_type = "URL"
        image_sources = []
        for page_data in pages_metadata:
            # 支持多种字段名：image、url、file
            image_url = page_data.get('image') or page_data.get('url') or page_data.get('file')
            if image_url:
                image_sources.append(image_url)
            else:
                # 如果没有图片URL，使用占位图
                image_sources.append(None)
    else:
        print("错误：既没有本地图片文件，也没有在 metadata.json 中找到图片URL")
        sys.exit(1)
    
    print(f"图片来源: {source_type}")
    print(f"图片数量: {len(image_sources)}")
    
    for idx, image_source in enumerate(image_sources):
        page_number = idx + 1
        
        # 如果没有图片源，使用占位图
        if image_source is None:
            print(f"处理第 {page_number} 页: 无图片URL")
            print(f"  ✗ 图片加载失败: 未找到图片URL")
            failed_images.append({
                'page': page_number,
                'file': '无',
                'error': '未找到图片URL'
            })
            image_url = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300' viewBox='0 0 400 300'%3E%3Crect width='400' height='300' fill='%23ddd'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' font-family='Arial' font-size='20' fill='%23999'%3E无图片URL%3C/text%3E%3C/svg%3E"
        else:
            print(f"处理第 {page_number} 页: {image_source}")
            
            try:
                # 如果是URL，直接使用URL；如果是本地文件名，拼接完整路径
                if image_source.startswith('http://') or image_source.startswith('https://'):
                    # URL图片
                    full_path = image_source
                else:
                    # 本地文件
                    full_path = os.path.join(pages_dir, image_source)
                
                # 转换为base64（支持重试）
                image_url = image_to_base64(full_path, max_retries)
                print(f"  ✓ 图片加载成功")
            except Exception as e:
                print(f"  ✗ 图片加载失败: {str(e)}")
                failed_images.append({
                    'page': page_number,
                    'file': image_source,
                    'error': str(e)
                })
                # 使用占位图
                image_url = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300' viewBox='0 0 400 300'%3E%3Crect width='400' height='300' fill='%23ddd'/%3E%3Ctext x='50%25' y='45%25' dominant-baseline='middle' text-anchor='middle' font-family='Arial' font-size='18' fill='%23999'%3E图片加载失败%3C/text%3E%3Ctext x='50%25' y='60%25' dominant-baseline='middle' text-anchor='middle' font-family='Arial' font-size='12' fill='%23666'%3E%3C/text%3E%3C/svg%3E"
        
        # 获取文字
        page_text = ""
        if pages_metadata and idx < len(pages_metadata):
            page_data = pages_metadata[idx]
            if 'text' in page_data:
                page_text = page_data['text']
            elif 'text_cn' in page_data or 'text_en' in page_data:
                text_cn = page_data.get('text_cn', '')
                text_en = page_data.get('text_en', '')
                if text_cn and text_en:
                    # 使用div分开中英文，便于CSS控制样式
                    page_text = f'<div class="text-cn">{text_cn}</div><div class="text-en">{text_en}</div>'
                elif text_cn:
                    page_text = f'<div class="text-cn">{text_cn}</div>'
                elif text_en:
                    page_text = f'<div class="text-en">{text_en}</div>'
        
        pages_data.append({
            'number': page_number,
            'image': image_url,
            'text': page_text
        })
    
    # 如果有失败的图片，询问用户是否继续
    if failed_images:
        print(f"\n⚠️  警告: {len(failed_images)} 张图片加载失败！")
        for img in failed_images:
            print(f"  - 第 {img['page']} 页: {img['file']}")
            print(f"    错误: {img['error']}")
        
        # 这里选择继续生成，但使用占位图
        print("\n继续生成绘本（失败的图片将显示占位符）...")
    
    # 生成封面HTML
    cover_html = f'''
    <div class="sheet sheet-cover" id="sheet-cover">
        <div class="cover-content">
            <h1 class="cover-title">{metadata.get('title', '绘本')}</h1>
            <div class="cover-author">作者：{metadata.get('author', '未知')}</div>
            {f'<div class="cover-description">{metadata.get("description", "")}</div>' if metadata.get('description') else ''}
            <button class="cover-btn" id="startBtn">开始阅读</button>
        </div>
    </div>'''
    
    # 生成内容页HTML - 每个sheet包含一页的完整内容（左图右文）
    sheets_html = ""
    for i, page in enumerate(pages_data):
        sheets_html += f'''
    <div class="sheet sheet-content" id="sheet-{i}">
        <div class="sheet-page sheet-page-left">
            <img class="page-image" src="{page['image']}" alt="Page {page['number']}">
        </div>
        <div class="sheet-page sheet-page-right">
            <div class="page-text-container">
                <div class="page-text">{page['text']}</div>
                <div class="page-number">{page['number']}/{len(pages_data)}</div>
            </div>
        </div>
    </div>'''
    
    # 生成完整HTML
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>{metadata.get('title', '绘本')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            background: radial-gradient(circle at center, #3c322a 0%, #12100e 100%);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
            font-family: "Microsoft YaHei", sans-serif;
        }}
        
        :root {{
            --book-max-width: 90vw;
            --book-max-height: 90vh;
            --page-bg: #fffbf0;
            --text-color: #2c3e50;
        }}
        
        .book-container {{
            width: min(var(--book-max-width), calc(var(--book-max-height) * 2 * 5 / 7));
            height: min(var(--book-max-height), calc(var(--book-max-width) * 7 / 10));
            position: relative;
            perspective: 2000px;
        }}
        
        /* 每个sheet是一页，包含左图右文 */
        .sheet {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            transform-style: preserve-3d;
            transition: transform 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        /* 封面样式 */
        .sheet-cover {{
            background: linear-gradient(135deg, #8B7355 0%, #A0896C 100%);
            border-radius: 24px;
        }}
        
        .cover-content {{
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: #fff;
            text-align: center;
            padding: 60px;
        }}
        
        .cover-title {{
            font-size: 3rem;
            font-weight: bold;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }}
        
        .cover-author {{
            font-size: 1.5rem;
            margin-bottom: 30px;
            opacity: 0.9;
        }}
        
        .cover-description {{
            font-size: 1.2rem;
            line-height: 1.6;
            opacity: 0.85;
            max-width: 600px;
            margin-bottom: 40px;
        }}
        
        .cover-btn {{
            padding: 15px 50px;
            font-size: 1.2rem;
            background: #fff;
            color: #8B7355;
            border: none;
            border-radius: 30px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }}
        
        .cover-btn:hover {{
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
        }}
        
        .sheet.hidden {{
            opacity: 0;
            pointer-events: none;
        }}
        
        .sheet.visible {{
            opacity: 1;
            pointer-events: auto;
        }}
        
        .sheet.flipped {{
            transform: rotateY(90deg);
            opacity: 0;
        }}
        
        .sheet-page {{
            flex: 1;
            background: var(--page-bg);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 15px;
            min-height: 0;
        }}
        
        .sheet-page-left {{
            border-radius: 20px 0 0 20px;
            position: relative;
            overflow: hidden;
        }}
        
        .sheet-page-left::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: #fffbf0;
            z-index: -1;
        }}
        
        .sheet-page-right {{
            border-radius: 0 20px 20px 0;
        }}
        
        .page-image {{
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            position: relative;
            z-index: 1;
        }}
        
        .page-text-container {{
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            width: 100%;
            height: 100%;
        }}
        
        .page-text {{
            font-size: 1.4rem;
            line-height: 1.8;
            color: var(--text-color);
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 20px;
            text-align: center;
        }}
        
        .text-cn {{
            font-size: 1.4rem;
            font-weight: 500;
            margin-bottom: 15px;
            line-height: 1.8;
        }}
        
        .text-en {{
            font-size: 1.2rem;
            color: #555;
            line-height: 1.6;
        }}
        
        .page-number {{
            font-size: 0.9rem;
            color: #999;
            margin-top: 10px;
        }}
        
        .controls {{
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 20px;
            z-index: 1000;
        }}
        
        .btn {{
            width: 60px;
            height: 60px;
            border-radius: 50%;
            border: none;
            background: rgba(255, 255, 255, 0.9);
            color: #333;
            font-size: 24px;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }}
        
        .btn:hover {{
            background: #fff;
            transform: scale(1.1);
        }}
        
        .btn:disabled {{
            opacity: 0.3;
            cursor: not-allowed;
            transform: none;
        }}
        
        @media (max-width: 768px) {{
            .book-container {{
                width: 90vw;
                height: 85vh;
                max-height: 85vh;
            }}
            
            .sheet {{
                flex-direction: column;
            }}
            
            .sheet-page {{
                width: 100%;
                flex: 1;
                border-radius: 0;
                min-height: 0;
            }}
            
            .sheet-page-left {{
                flex: 1;
                border-radius: 20px 20px 0 0;
                padding: 10px;
                overflow: hidden;
            }}
            
            .sheet-page-right {{
                flex: 1;
                border-radius: 0 0 20px 20px;
                padding: 15px;
                min-height: 0;
            }}
            
            .page-image {{
                width: 100%;
                height: 100%;
                object-fit: contain;
            }}
            
            .page-text-container {{
                padding: 10px 15px;
                height: 100%;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                overflow: hidden;
            }}
            
            .page-text {{
                font-size: 1.1rem;
                line-height: 1.6;
                padding: 5px;
                flex: 1;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center;
                overflow-y: auto;
                min-height: 0;
            }}
            
            .text-cn {{
                font-size: 1.2rem;
                font-weight: 500;
                margin-bottom: 10px;
                line-height: 1.6;
            }}
            
            .text-en {{
                font-size: 1.0rem;
                color: #555;
                line-height: 1.5;
            }}
            
            .page-number {{
                font-size: 0.8rem;
                color: #999;
                margin-top: 5px;
                flex-shrink: 0;
            }}
        }}
    </style>
</head>
<body>
    <div class="book-container" id="book">
        {cover_html}
        {sheets_html}
    </div>
    
    <div class="controls">
        <button class="btn" id="prevBtn">←</button>
        <button class="btn" id="nextBtn">→</button>
    </div>
    
    <script>
        const coverSheet = document.getElementById('sheet-cover');
        const contentSheets = document.querySelectorAll('.sheet-content');
        const totalPages = contentSheets.length;
        let currentPage = 0; // 当前页码，-1表示封面
        let isCoverMode = true; // 是否在封面模式
        
        function updateBook() {{
            if (isCoverMode) {{
                // 封面模式
                coverSheet.classList.add('visible');
                coverSheet.classList.remove('hidden', 'flipped');
                
                contentSheets.forEach(sheet => {{
                    sheet.classList.add('hidden');
                    sheet.classList.remove('visible', 'flipped');
                }});
            }} else {{
                // 内容页模式
                coverSheet.classList.add('hidden');
                coverSheet.classList.remove('visible', 'flipped');
                
                contentSheets.forEach((sheet, index) => {{
                    if (index === currentPage) {{
                        sheet.classList.add('visible');
                        sheet.classList.remove('hidden', 'flipped');
                    }} else if (index < currentPage) {{
                        sheet.classList.add('flipped');
                        sheet.classList.remove('visible', 'hidden');
                    }} else {{
                        sheet.classList.add('hidden');
                        sheet.classList.remove('visible', 'flipped');
                    }}
                }});
            }}
            
            // 更新按钮状态
            document.getElementById('prevBtn').disabled = isCoverMode;
            document.getElementById('nextBtn').disabled = !isCoverMode && currentPage >= totalPages - 1;
        }}
        
        function nextPage() {{
            if (isCoverMode) {{
                // 从封面进入第一页
                isCoverMode = false;
                currentPage = 0;
            }} else if (currentPage < totalPages - 1) {{
                currentPage++;
            }}
            updateBook();
        }}
        
        function prevPage() {{
            if (!isCoverMode) {{
                if (currentPage === 0) {{
                    // 从第一页返回封面
                    isCoverMode = true;
                    currentPage = -1;
                }} else if (currentPage > 0) {{
                    currentPage--;
                }}
            }}
            updateBook();
        }}
        
        // 开始按钮 - 从封面进入
        document.getElementById('startBtn').addEventListener('click', function() {{
            isCoverMode = false;
            currentPage = 0;
            updateBook();
        }});
        
        // 导航按钮
        document.getElementById('nextBtn').addEventListener('click', nextPage);
        document.getElementById('prevBtn').addEventListener('click', prevPage);
        
        // 键盘控制
        document.addEventListener('keydown', function(e) {{
            if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'Enter') {{
                e.preventDefault();
                if (isCoverMode) {{
                    isCoverMode = false;
                    currentPage = 0;
                    updateBook();
                }} else {{
                    nextPage();
                }}
            }} else if (e.key === 'ArrowLeft' || e.key === 'Escape') {{
                e.preventDefault();
                if (currentPage === 0 && !isCoverMode) {{
                    isCoverMode = true;
                    currentPage = -1;
                    updateBook();
                }} else {{
                    prevPage();
                }}
            }}
        }});
        
        // 触摸滑动支持
        let touchStartX = 0;
        let touchEndX = 0;
        
        document.addEventListener('touchstart', function(e) {{
            touchStartX = e.changedTouches[0].screenX;
        }});
        
        document.addEventListener('touchend', function(e) {{
            touchEndX = e.changedTouches[0].screenX;
            handleSwipe();
        }});
        
        function handleSwipe() {{
            const swipeDistance = touchEndX - touchStartX;
            
            if (Math.abs(swipeDistance) > 50) {{
                if (swipeDistance < 0) {{
                    // 向左滑动 - 下一页
                    if (isCoverMode) {{
                        isCoverMode = false;
                        currentPage = 0;
                    }} else {{
                        nextPage();
                    }}
                }} else {{
                    // 向右滑动 - 上一页
                    if (currentPage === 0 && !isCoverMode) {{
                        isCoverMode = true;
                        currentPage = -1;
                    }} else {{
                        prevPage();
                    }}
                }}
                updateBook();
            }}
        }}
        
        // 初始化显示封面
        updateBook();
    </script>
</body>
</html>'''
    
    return html


def save_html(html, output_file):
    """保存HTML文件"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✓ 绘本已生成: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='绘本打包工具')
    parser.add_argument('--input', required=True, help='绘本目录（支持相对路径和绝对路径）')
    parser.add_argument('--output', default='book.html', help='输出HTML文件（支持相对路径）')
    parser.add_argument('--max-retries', type=int, default=3, help='图片下载失败时的最大重试次数（默认3次）')
    
    args = parser.parse_args()
    
    # 显示当前工作目录，方便调试
    print(f"当前工作目录: {os.getcwd()}")
    print(f"输入目录: {args.input}")
    print(f"最大重试次数: {args.max_retries}")
    
    # 加载数据
    metadata = load_metadata(args.input)
    page_files, pages_dir = load_pages(args.input)
    
    print(f"\n标题: {metadata.get('title', '未知')}")
    print(f"页数: {len(page_files)}")
    print(f"开始处理图片...\n")
    
    # 生成HTML
    html = generate_html(metadata, page_files, pages_dir, args.max_retries)
    
    # 标准化输出路径
    output_file = args.output.lstrip('./')
    if not os.path.isabs(output_file):
        output_file = os.path.abspath(output_file)
    
    # 保存
    save_html(html, output_file)
    
    print("\n✓ 绘本打包完成！")
    print(f"输出文件: {output_file}")


if __name__ == '__main__':
    main()
