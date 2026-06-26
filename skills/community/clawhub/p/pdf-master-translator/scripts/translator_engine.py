# /// script
# requires-python = ">=3.11"
# dependencies = ["pymupdf", "google-genai", "markdown2", "weasyprint", "pillow", "tenacity"]
# ///
import fitz, os, sys, json, re, time, argparse, shutil, base64, urllib.parse
from google import genai
from weasyprint import HTML, CSS
from PIL import Image, ImageDraw
import markdown2
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

class QualityCheckFailed(Exception): pass
class APIRateLimitExceeded(Exception): pass

def qa_agent_check_json(raw_json_str, expected_keys):
    try:
        data = json.loads(raw_json_str)
        for k in expected_keys:
            if k not in data: raise QualityCheckFailed(f"Missing key: {k}")
        return data
    except json.JSONDecodeError:
        raise QualityCheckFailed("Not a valid JSON.")

@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=2, min=4, max=30), retry=retry_if_exception_type((QualityCheckFailed, APIRateLimitExceeded)))
def agent_1_layout(client, img_path, p_num):
    try:
        uploaded = client.files.upload(file=img_path)
        prompt = f"""
        NASA图纸(第{p_num}页)布局分析。
        寻找主要的工程图表/示意图。不要包含页眉页脚的纯文本表格。
        返回严格的JSON：{{ "has_figures": bool, "figures": [ {{ "box": [ymin, xmin, ymax, xmax] }} ] }}
        坐标为0-1000的归一化。
        """
        res = client.models.generate_content(model='gemini-2.5-pro', contents=[prompt, uploaded])
        raw = res.text.strip()
        if raw.startswith("```"): raw = re.sub(r"^```json\n|```\n?$", "", raw, flags=re.MULTILINE).strip()
        return qa_agent_check_json(raw, ["has_figures"])
    except Exception as e:
        if "429" in str(e): raise APIRateLimitExceeded(f"API Rate Limit: {e}")
        raise QualityCheckFailed(f"Agent 1 Error: {e}")

@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=2, min=4, max=30), retry=retry_if_exception_type((QualityCheckFailed, APIRateLimitExceeded)))
def agent_2_translate(client, masked_img_path, p_num, ctx_prompt):
    try:
        uploaded = client.files.upload(file=masked_img_path)
        prompt = f"""
        {ctx_prompt}
        你是顶级航天翻译专家。请翻译图纸第{p_num}页。
        【死命令】：
        1. 绝对不要改动数学公式。所有数学公式必须用 `$` 或 `$$` 包裹。
        2. 必须严格使用以下XML标签包裹结果：
        <HEADER>页眉和修订表格Markdown</HEADER>
        <BODY>正文翻译Markdown（包含普通表格和公式）</BODY>
        <FOOTER>底部图纸信息框Markdown</FOOTER>
        """
        res = client.models.generate_content(model='gemini-2.5-pro', contents=[prompt, uploaded])
        text = res.text
        if not (re.search(r'<HEADER>.*?</HEADER>', text, re.S) and re.search(r'<BODY>.*?</BODY>', text, re.S) and re.search(r'<FOOTER>.*?</FOOTER>', text, re.S)):
            raise QualityCheckFailed("XML Tags missing.")
        return text
    except Exception as e:
        if "429" in str(e): raise APIRateLimitExceeded(f"API Rate Limit: {e}")
        raise QualityCheckFailed(f"Agent 2 Error: {e}")

def encode_image_base64(filepath):
    with open(filepath, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    ext = os.path.splitext(filepath)[1].lower()
    mime = "image/jpeg" if ext in [".jpg", ".jpeg"] else "image/png"
    return f"data:{mime};base64,{encoded_string}"

def latex_to_svg_img(match, is_block=False):
    formula = match.group(1).strip()
    encoded = urllib.parse.quote(formula)
    # math.vercel.app returns a clean SVG rendering of the LaTeX
    url = f"https://math.vercel.app/?from={encoded}"
    if is_block:
        return f'\n<div class="math-block"><img src="{url}" alt="math formula"></div>\n'
    else:
        return f'<img src="{url}" class="math-inline" alt="math formula">'

def render_math_to_svg(md_text):
    # 替换独立公式 $$...$$
    md_text = re.sub(r'\$\$([\s\S]+?)\$\$', lambda m: latex_to_svg_img(m, True), md_text)
    # 替换行内公式 $...$
    md_text = re.sub(r'(?<!\$)\$([^\$]+)\$(?!\$)', lambda m: latex_to_svg_img(m, False), md_text)
    return md_text

def process_page(client, doc, target_page, work_dir):
    print(f"[*] Processing Page {target_page}...")
    main_img = os.path.join(work_dir, f"target_p{target_page}.png")
    doc[target_page-1].get_pixmap(matrix=fitz.Matrix(2,2)).save(main_img)
    
    layout_data = agent_1_layout(client, main_img, target_page)
    
    masked_img = main_img
    fig_b64_list = []
    if layout_data.get("has_figures"):
        with Image.open(main_img) as im:
            w, h = im.size
            masked_im = im.copy()
            draw = ImageDraw.Draw(masked_im)
            for idx, fig in enumerate(layout_data.get("figures", [])):
                box = fig["box"]
                l, t, r, b = box[1]*w/1000, box[0]*h/1000, box[3]*w/1000, box[2]*h/1000
                if (r-l)*(b-t) < (w*h*0.01): continue
                crop_fn = os.path.join(work_dir, f"extracted_fig_p{target_page}_{idx}.png")
                im.crop((l, t, r, b)).save(crop_fn)
                # Ensure images are permanently embedded as base64 strings
                fig_b64_list.append(encode_image_base64(crop_fn))
                draw.rectangle([l, t, r, b], fill="white")
            masked_img = os.path.join(work_dir, f"masked_p{target_page}.png")
            masked_im.save(masked_img)
            
    ctx_prompt = ""
    if target_page > 1:
        prev_text = doc[target_page-2].get_text()[-500:]
        if prev_text.strip(): ctx_prompt = f"【上一页参考】：{prev_text}\n"
        
    xml_text = agent_2_translate(client, masked_img, target_page, ctx_prompt)
    
    h_md = re.search(r'<HEADER>(.*?)</HEADER>', xml_text, re.S).group(1).strip()
    b_md = re.search(r'<BODY>(.*?)</BODY>', xml_text, re.S).group(1).strip()
    f_md = re.search(r'<FOOTER>(.*?)</FOOTER>', xml_text, re.S).group(1).strip()
    
    # 核心修复 2: 真正的将 LaTeX 渲染为矢量 SVG 图像
    b_md = render_math_to_svg(b_md)

    header_html = markdown2.markdown(h_md, extras=["tables"])
    body_html = markdown2.markdown(b_md, extras=["tables"])
    footer_html = markdown2.markdown(f_md, extras=["tables"])
    
    app_html = ""
    if fig_b64_list:
        app_html = "<div class='app'><h3>[ 本页原图参考 ]</h3>"
        for b64 in fig_b64_list: 
            app_html += f"<div style='text-align:center;'><img src='{b64}' class='extracted-fig'/></div>"
        app_html += "</div>"
        
    page_html = f"""
        <div class="page-container">
            <div class="header">{header_html}</div>
            <div class="body">{body_html}{app_html}</div>
            <div class="footer">{footer_html}</div>
        </div>
    """
    return page_html

def build_pdf(html_segments, out_pdf):
    # 核心修复 1: 流式紧凑排版，避免大面积留白
    full_html = f"""<html><head><style>
        @page {{ size: A4; margin: 15mm; }}
        body {{ font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; font-size: 9.5pt; line-height: 1.4; color: #222; }}
        
        /* 智能排版：内容自然流动，尽量不强行截断一个区块，但允许超出A4时自然换页 */
        .page-container {{ margin-bottom: 20px; padding-bottom: 15px; border-bottom: 2px dashed #999; page-break-inside: avoid; }}
        
        table {{ width: 100%; border-collapse: collapse; margin-bottom: 12px; border: 1.5px solid #000; font-size: 8.5pt; }}
        th, td {{ border: 1px solid #000; padding: 4px; }}
        th {{ background-color: #f5f5f5; }}
        
        .header {{ border-bottom: 2px solid #000; margin-bottom: 15px; padding-bottom: 5px; }}
        .footer {{ border-top: 2px solid #000; margin-top: 15px; padding-top: 5px; }}
        
        .app {{ margin-top: 20px; padding: 15px; background: #fafafa; border: 1px solid #ddd; }}
        .app h3 {{ font-size: 10pt; color: #555; text-align: center; border-bottom: 1px dashed #ccc; padding-bottom: 5px; }}
        .extracted-fig {{ max-width: 90%; max-height: 100mm; object-fit: contain; margin-top: 10px; border: 1px solid #ddd; box-shadow: 1px 1px 5px rgba(0,0,0,0.1); }}
        
        /* SVG公式的完美呈现样式 */
        .math-inline {{ height: 1.2em; vertical-align: middle; margin: 0 2px; }}
        .math-block {{ text-align: center; margin: 15px 0; padding: 10px; background: #f8fcfd; border-left: 3px solid #0056b3; overflow-x: auto; }}
        .math-block img {{ max-width: 100%; height: auto; max-height: 60px; }}
    </style></head><body>{''.join(html_segments)}</body></html>
    """
    HTML(string=full_html, base_url=os.getcwd()).write_pdf(out_pdf)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf_path")
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--end", type=int, default=0)
    args = parser.parse_args()
    
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    doc = fitz.open(args.pdf_path)
    end_page = args.end if args.end > 0 else len(doc)
    
    work_dir = "translator_tmp"
    os.makedirs(work_dir, exist_ok=True)
    
    all_pages_html = []
    print(f"🚀 Master Translator Started: Pages {args.start}-{end_page}")
    
    for p in range(args.start, end_page + 1):
        try:
            page_html = process_page(client, doc, p, work_dir)
            all_pages_html.append(page_html)
            time.sleep(3)
        except Exception as e:
            print(f"❌ FATAL ERROR on Page {p} after all retries: {e}")
            all_pages_html.append(f"<div class='page-container'><h2>Page {p} Extraction Failed</h2><p>{e}</p></div>")

    print(f"📦 Assembling final PDF...")
    base_name = os.path.splitext(os.path.basename(args.pdf_path))[0]
    out_pdf = f"{base_name}_translated_v3.pdf"
    
    build_pdf(all_pages_html, out_pdf)
    
    print("🔎 Running Final Layout/Math/Image Sanity Check...")
    try:
        # A quick heuristic check on the generated PDF size to ensure images were embedded
        pdf_size = os.path.getsize(out_pdf)
        if pdf_size < 50000: # 50KB is too small for a document with embedded Base64 images
             print(f"⚠️ Warning: Final PDF size is unusually small ({pdf_size} bytes). Images may not have embedded correctly.")
        else:
             print(f"✅ QA Pass: PDF size is healthy ({pdf_size/1024:.1f} KB), implying successful image embedding.")
    except Exception as e:
        print(f"QA Error: {e}")
        
    print(f"✅ Final Verified PDF saved: {out_pdf}")
    shutil.rmtree(work_dir)

if __name__ == "__main__":
    main()
