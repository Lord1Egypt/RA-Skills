# /// script
# requires-python = ">=3.11"
# dependencies = ["pymupdf", "google-genai", "markdown2", "weasyprint", "pillow", "tenacity"]
# ///
import fitz, os, sys, json, re, time, base64
from google import genai
from weasyprint import HTML, CSS
from PIL import Image, ImageDraw
import markdown2
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# 辅助函数：将图片转为 Data URI，防止图片丢失
def b64_img(path):
    with open(path, "rb") as f: 
        encoded = base64.b64encode(f.read()).decode('utf-8')
    mime = "image/png"
    return f"data:{mime};base64,{encoded}"

def process_page_v8(pdf_path, p_num, api_key):
    print(f"[*] V8 Processing Page {p_num}...")
    doc = fitz.open(pdf_path)
    page = doc[p_num-1]
    
    # 渲染原图并保存
    img_path = f"raw_p{p_num}.png"
    page.get_pixmap(matrix=fitz.Matrix(2,2)).save(img_path)
    
    client = genai.Client(api_key=api_key)
    uploaded = client.files.upload(file=img_path)
    
    prompt = f"""
    你是航天工程文档翻译专家。请翻译NASA图纸第{p_num}页。
    【死命令】：
    1. 严禁改动数学公式（如 k=2NcKa）。
    2. 使用XML结构输出：
    <HEADER>页眉 Markdown 表格</HEADER>
    <BODY>正文 Markdown 翻译。如果原图有图表标注，请在文末用【图例说明】列表列出。</BODY>
    <FOOTER>页脚图框 Markdown 表格</FOOTER>
    """
    
    res = client.models.generate_content(model='gemini-2.5-pro', contents=[prompt, uploaded])
    text = res.text
    
    header = re.search(r'<HEADER>(.*?)</HEADER>', text, re.S).group(1).strip()
    body = re.search(r'<BODY>(.*?)</BODY>', text, re.S).group(1).strip()
    footer = re.search(r'<FOOTER>(.*?)</FOOTER>', text, re.S).group(1).strip()
    
    # 物理嵌入原图 (作为所有文字的参考图，确保信息不丢失)
    embedded_img = b64_img(img_path)
    
    full_html = f"""
    <html><head><style>
        @page {{ size: A4; margin: 10mm; }}
        body {{ font-family: sans-serif; font-size: 10pt; line-height: 1.3; }}
        .page-container {{ border: 1px solid #ccc; padding: 10px; margin-bottom: 20px; }}
        table {{ width: 100%; border-collapse: collapse; border: 1px solid #000; }}
        th, td {{ border: 1px solid #000; padding: 3px; font-size: 8pt; }}
        .original-ref {{ margin-top: 20px; border: 1px solid #ddd; padding: 5px; text-align: center; }}
        .original-ref img {{ max-width: 95%; }}
    </style></head>
    <body>
        <div class="page-container">
            <div class="header">{markdown2.markdown(header, extras=["tables"])}</div>
            <div class="body">{markdown2.markdown(body, extras=["tables"])}</div>
            <div class="footer">{markdown2.markdown(footer, extras=["tables"])}</div>
            <div class="original-ref">
                <p><strong>[原图参考 Page {p_num}]</strong></p>
                <img src="{embedded_img}">
            </div>
        </div>
    </body></html>
    """
    
    out_pdf = f"V8_Page_{p_num}_Final.pdf"
    HTML(string=full_html).write_pdf(out_pdf)
    return out_pdf

if __name__ == "__main__":
    out_pdf = process_page_v8(sys.argv[1], 12, os.environ.get("GEMINI_API_KEY"))
    print(f"✅ V8 Final PDF: {out_pdf}")
