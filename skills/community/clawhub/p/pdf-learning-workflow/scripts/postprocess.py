#!/usr/bin/env python3
"""OCR 后处理：公式清洗 + 代码块识别 + 图片裁剪"""
import re, sys, os, glob
from PIL import Image

# === 代码行检测 ===

CODE_KEYWORDS = r'\b(int|double|float|void|char|bool|long|short|unsigned|struct|class|if|else|for|while|do|switch|case|break|continue|return|include|define|using|namespace|printf|scanf|cout|cin|endl|std::|const|static|virtual|public|private|protected|template|typedef|sizeof|new|delete|try|catch|throw|true|false|nullptr|NULL|implicit|real|integer|parameter|common|call|subroutine|function|end\s*(do|if|subroutine|function|program|module)|program|module|save|data|format|write|read|open|close|stop|pause|allocate|deallocate|pointer|target|extern|friend|operator|enum|union)\b'

def is_code_line(line):
    stripped = line.strip()
    if not stripped or stripped.startswith('#'):
        return False
    keywords = re.findall(CODE_KEYWORDS, stripped, re.IGNORECASE)
    score = len(keywords)
    score += 1 if ';' in stripped else 0
    score += 1 if '//' in stripped else 0
    score += 1 if '=' in stripped and not stripped.startswith('=') and '===' not in stripped else 0
    score += 1 if '{' in stripped or '}' in stripped else 0
    score += 1 if re.search(r'[<>+\-*/%]=?|!=|&&|\|\|', stripped) else 0
    return score >= 2

def wrap_code_blocks(text):
    lines = text.split('\n')
    result = []
    in_code = False
    buffer = []
    for line in lines:
        if line.strip().startswith('```'):
            if in_code: in_code = False
            else: in_code = True
            result.append(line)
            continue
        if in_code:
            result.append(line)
            continue
        if is_code_line(line):
            buffer.append(line)
        else:
            if len(buffer) > 1:
                result.append('```cpp')
                result.extend(buffer)
                result.append('```')
            elif len(buffer) == 1:
                result.append(buffer[0])
            buffer.clear()
            result.append(line)
    if len(buffer) > 1:
        result.append('```cpp')
        result.extend(buffer)
        result.append('```')
    elif len(buffer) == 1:
        result.append(buffer[0])
    return '\n'.join(result)

# === 公式清洗 ===

def clean_formula_spacing(text):
    text = re.sub(r'\$\$\s+(.*?)\s+\$\$', r'$$\1$$', text, flags=re.DOTALL)
    text = re.sub(r'(?<!\$)\$\s+(.*?)\s+\$(?!\$)', r'$\1$', text)
    return text

# === 图片裁剪 ===

IMAGE_RE = re.compile(r'!\[\]\(page=(\d+),bbox=\[(\d+),\s*(\d+),\s*(\d+),\s*(\d+)\]\)')

PAGE_HEADER_RE = re.compile(r'^#+\s+Page\s+(\d+)', re.IGNORECASE)

def extract_images(text, pages_dir, assets_dir):
    """从页 PNG 裁剪图片区域，替换标记为本地引用"""
    os.makedirs(assets_dir, exist_ok=True)
    fig_count = 0
    page_cache = {}
    current_page = 0  # 通过 ## Page X 跟踪当前页码
    
    def get_page_img(page_num):
        if page_num not in page_cache:
            path = os.path.join(pages_dir, f"page_{page_num:04d}.png")
            if os.path.exists(path):
                page_cache[page_num] = Image.open(path)
            else:
                page_cache[page_num] = None
        return page_cache[page_num]
    
    lines = text.split('\n')
    result = []
    
    for line in lines:
        # 跟踪当前页码
        m = PAGE_HEADER_RE.search(line)
        if m:
            current_page = int(m.group(1))
        
        # 图片标记替换
        im = IMAGE_RE.search(line)
        if im:
            # 忽略 marker 里的 page 值（永远是 0），使用 current_page
            _, x1, y1, x2, y2 = int(im.group(1)), int(im.group(2)), int(im.group(3)), int(im.group(4)), int(im.group(5))
            x1, y1, x2, y2 = int(im.group(2)), int(im.group(3)), int(im.group(4)), int(im.group(5))
            img = get_page_img(current_page)
            if img is not None:
                w, h = img.size
                x1, y1, x2, y2 = max(0,x1), max(0,y1), min(w,x2), min(h,y2)
                if x2 - x1 >= 10 and y2 - y1 >= 10:
                    try:
                        crop = img.crop((x1, y1, x2, y2))
                        fig_count += 1
                        fname = f"fig_{fig_count:03d}.png"
                        crop.save(os.path.join(assets_dir, fname))
                        line = IMAGE_RE.sub(f"![插图](assets/{fname})", line)
                    except:
                        pass
        
        result.append(line)
    
    return '\n'.join(result), fig_count

# === 主流程 ===

def process_file(input_path, output_path=None, pages_dir=None):
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = clean_formula_spacing(content)
    content = wrap_code_blocks(content)
    
    fig_count = 0
    if pages_dir and os.path.isdir(pages_dir):
        out_dir = os.path.dirname(output_path or input_path)
        assets_dir = os.path.join(out_dir, "assets")
        content, fig_count = extract_images(content, pages_dir, assets_dir)
    
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 已处理: {output_path}")
        if fig_count:
            print(f"   🖼️ 裁剪 {fig_count} 张图片 → {os.path.join(os.path.dirname(output_path), 'assets')}")
    else:
        print(content)
    
    return content

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: postprocess.py <input.md> [output.md] [--pages <pages_dir>]")
        sys.exit(1)
    
    pages_dir = None
    output = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else sys.argv[1]
    
    for i, arg in enumerate(sys.argv):
        if arg == '--pages' and i + 1 < len(sys.argv):
            pages_dir = sys.argv[i + 1]
    
    process_file(sys.argv[1], output, pages_dir)
