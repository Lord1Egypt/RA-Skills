import fitz
import json
import sys
import os
from openai import OpenAI

def extract_text_from_pdf(filepath: str) -> str:
    try:
        doc = fitz.open(filepath)
        full_text = "\n".join(page.get_text() for page in doc)
        doc.close()
        return full_text
    except Exception:
        return ""

def extract_metadata_with_ai(text: str) -> dict:
    api_key = os.getenv("MOONSHOT_API_KEY")
    if not api_key:
        return {
            "title_apa": "无API_KEY",
            "keywords": [],
            "abstract": "请配置 MOONSHOT_API_KEY 环境变量"
        }

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.moonshot.cn/v1"
    )

    prompt = f"""
你是学术论文信息提取助手，只返回JSON，不要其他任何内容。

提取三项：
1. title_apa：论文标题
2. keywords：关键词数组
3. abstract：摘要

论文文本：
{text[:5000]}
"""

    try:
        response = client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        content = response.choices[0].message.content.strip()
        return json.loads(content)
    except Exception:
        return {
            "title_apa": "提取失败",
            "keywords": [],
            "abstract": "AI调用出错"
        }

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "缺少PDF路径"}, ensure_ascii=False))
        return

    pdf_path = sys.argv[1]
    full_text = extract_text_from_pdf(pdf_path)

    if not full_text:
        print(json.dumps({
            "title_apa": "无法读取PDF",
            "keywords": [],
            "abstract": "文件无法打开或不是有效PDF"
        }, ensure_ascii=False))
        return

    result = extract_metadata_with_ai(full_text)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()