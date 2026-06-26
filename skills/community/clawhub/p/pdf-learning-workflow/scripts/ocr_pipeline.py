#!/usr/bin/env python3
"""OCR 分批处理：调用 GLM-OCR 识别页面图片"""
import os, sys, base64, glob, time
from zai import ZhipuAiClient

BATCH_SIZE = 5

def read_api_key():
    path = os.path.expanduser("~/.config/glm-ocr/api_key")
    if not os.path.exists(path):
        print("❌ GLM-OCR API Key 未配置！请先运行:")
        print("   mkdir -p ~/.config/glm-ocr")
        print('   echo "your-api-key" > ~/.config/glm-ocr/api_key')
        sys.exit(1)
    return open(path).read().strip()

def process_page(client, image_path):
    """单页 OCR"""
    with open(image_path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode()
        data_url = f"data:image/png;base64,{b64}"
    
    response = client.layout_parsing.create(model="glm-ocr", file=data_url)
    return response.md_results

def process_pages(pages_dir, output_dir):
    api_key = read_api_key()
    client = ZhipuAiClient(api_key=api_key)
    
    # 获取所有页面文件，按页码排序
    page_files = sorted(glob.glob(os.path.join(pages_dir, "page_*.png")))
    total = len(page_files)
    print(f"📄 待识别: {total} 页")
    
    os.makedirs(output_dir, exist_ok=True)
    
    for i in range(0, total, BATCH_SIZE):
        batch = page_files[i:i + BATCH_SIZE]
        chunk_num = i // BATCH_SIZE + 1
        chunk_path = os.path.join(output_dir, f"chunk_{chunk_num:03d}.md")
        
        print(f"⏳ 处理 chunk {chunk_num} (页 {i+1}-{min(i+BATCH_SIZE, total)})...")
        all_text = []
        
        for page_path in batch:
            page_num = os.path.basename(page_path).split("_")[1].split(".")[0]
            try:
                md = process_page(client, page_path)
                all_text.append(f"### Page {int(page_num)}\n\n{md}")
                print(f"  ✅ 页 {int(page_num)} OK")
            except Exception as e:
                print(f"  ⚠️ 页 {int(page_num)} 失败: {e}")
                # 重试一次
                try:
                    time.sleep(2)
                    md = process_page(client, page_path)
                    all_text.append(f"### Page {int(page_num)}\n\n{md}")
                    print(f"  ✅ 页 {int(page_num)} 重试成功")
                except:
                    print(f"  ❌ 页 {int(page_num)} 跳过")
                    all_text.append(f"### Page {int(page_num)}\n\n*[OCR failed]*")
        
        with open(chunk_path, 'w', encoding='utf-8') as f:
            f.write("\n\n---\n\n".join(all_text))
        print(f"  💾 已保存: {chunk_path}")
        
        # 避免 API 限流
        if i + BATCH_SIZE < total:
            time.sleep(1)
    
    print(f"✅ OCR 完成: {total} 页 → {output_dir}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: ocr_pipeline.py <pages_dir> <output_dir>")
        sys.exit(1)
    process_pages(sys.argv[1], sys.argv[2])
