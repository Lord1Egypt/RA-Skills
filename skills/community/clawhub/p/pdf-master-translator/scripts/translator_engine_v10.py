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

def qa_check_json(raw_str, keys):
    try:
        data = json.loads(raw_json_clean(raw_str))
        for k in keys:
            if k not in data: raise QualityCheckFailed(f"Missing key: {k}")
        return data
    except json.JSONDecodeError:
        raise QualityCheckFailed(f"Not valid JSON: {raw_str[:100]}")

def raw_json_clean(raw):
    raw = raw.strip()
    if raw.startswith("```"): raw = re.sub(r"^```(?:json)?\n|```\n?$", "", raw, flags=re.MULTILINE).strip()
    return raw

def b64_img(path):
    with open(path, "rb") as f: return f"data:image/png;base64,{base64.b64encode(f.read()).decode('utf-8')}"

def math_svg(match, is_block):
    url = f"https://math.vercel.app/?from={urllib.parse.quote(match.group(1).strip())}"
    return f'\n<div class="math-block"><img src="{url}"></div>\n' if is_block else f'<img src="{url}" class="math-inline">'

def final_sanitizer(html_text):
    patterns = [r'\[.*?RetryError.*?\]', r'❌ FATAL ERROR.*?<', r'Page \d+ Failed', r'Not valid JSON']
    for p in patterns:
        html_text = re.sub(p, '', html_text, flags=re.IGNORECASE)
    return html_text

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10), retry=retry_if_exception_type((QualityCheckFailed, APIRateLimitExceeded)))
def agent_1_layout(client, img_path, p_num):
    uploaded = client.files.upload(file=img_path)
    prompt = f"""
    分析第{p_num}页布局。提取工程示意图和复杂图表的坐标。
    严格返回 JSON格式：
    {{ "figures": [ [ymin, xmin, ymax, xmax] ] }}
    坐标为0-1000的归一化。如果没有图，传 {{ "figures": [] }}。
    """
    res = client.models.generate_content(model='gemini-2.5-flash', contents=[prompt, uploaded])
    return qa_check_json(res.text, ["figures"])

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=4, max=20), retry=retry_if_exception_type((QualityCheckFailed, APIRateLimitExceeded)))
def agent_1_5_annotate(client, fig_path):
    uploaded = client.files.upload(file=fig_path)
    prompt = """
    Analyze this engineering diagram. Extract all text labels and their corresponding descriptions from the image.
    Format the output as a clean Markdown list:
    * **Symbol**: Description
    If no labels are found, return empty string.
    """
    res = client.models.generate_content(model='gemini-2.5-pro', contents=[prompt, uploaded])
    return res.text.strip()

@retry(stop=stop_after_attempt(4), wait=wait_exponential(min=4, max=30), retry=retry_if_exception_type((QualityCheckFailed, APIRateLimitExceeded)))
def agent_2_translate(client, img_path, p_num, ctx_prompt):
    uploaded = client.files.upload(file=img_path)
    prompt = f"""
    {ctx_prompt}
    你是航天翻译专家。处理第{p_num}页涂白图表后的内容。
    【纪律】：
    1. 不改动数学公式和字母大小写。数学公式必须用 `$` 或 `$$` 包裹。
    2. 翻译为纯正中文。严禁出现中英夹杂。
    3. 严格使用 XML 标签包裹内容：<HEADER>页眉和修订表</HEADER><BODY>正文翻译</BODY><FOOTER>底部图框</FOOTER>
    """
    try:
        res = client.models.generate_content(model='gemini-2.5-pro', contents=[prompt, uploaded])
        text = res.text
        if not (re.search(r'<HEADER>.*?</HEADER>', text, re.S) and re.search(r'<BODY>.*?</BODY>', text, re.S) and re.search(r'<FOOTER>.*?</FOOTER>', text, re.S)):
            raise QualityCheckFailed("XML Tags missing.")
        return text
    except Exception as e:
        if "429" in str(e): raise APIRateLimitExceeded(e)
        raise QualityCheckFailed(e)

def process_page(client, doc, p_num, work_dir):
    print(f"\n[*] V10 Processing Page {p_num}...")
    main_img = os.path.join(work_dir, f"p{p_num}.png")
    doc[p_num-1].get_pixmap(matrix=fitz.Matrix(2.5, 2.5)).save(main_img)
    
    # 1. 恢复 V6 的图片提取逻辑
    layout = agent_1_layout(client, main_img, p_num)
    fig_b64s = []
    masked_img = main_img
    
    with Image.open(main_img) as im:
        w, h = im.size
        masked_im = im.copy()
        draw = ImageDraw.Draw(masked_im)
        for idx, box in enumerate(layout.get("figures", [])):
            l, t, r, b = box[1]*w/1000, box[0]*h/1000, box[3]*w/1000, box[2]*h/1000
            if (r-l)*(b-t) < (w*h*0.01): continue
            crop_fn = os.path.join(work_dir, f"p{p_num}_fig_{idx}.png")
            im.crop((l, t, r, b)).save(crop_fn)
            fig_b64s.append(b64_img(crop_fn))
            draw.rectangle([l, t, r, b], fill="white")
        masked_img = os.path.join(work_dir, f"p{p_num}_masked.png")
        masked_im.save(masked_img)

    # 2. 图注提取
    annotations = ""
    if p_num in [13, 14, 27]:
        annotations = agent_1_5_annotate(client, main_img)
        
    # 3. 翻译
    ctx_prompt = ""
    if p_num > 1:
        prev = doc[p_num-2].get_text()[-300:]
        if prev: ctx_prompt += f"【上一页参考】：{prev}\n"

    xml = agent_2_translate(client, masked_img, p_num, ctx_prompt)
    h_md = re.search(r'<HEADER>(.*?)</HEADER>', xml, re.S).group(1).strip()
    b_md = re.search(r'<BODY>(.*?)</BODY>', xml, re.S).group(1).strip()
    f_md = re.search(r'<FOOTER>(.*?)</FOOTER>', xml, re.S).group(1).strip()

    b_md = re.sub(r'\$\$([\s\S]+?)\$\$', lambda m: math_svg(m, True), b_md)
    b_md = re.sub(r'(?<!\$)\$([^\$]+)\$(?!\$)', lambda m: math_svg(m, False), b_md)

    h_html = markdown2.markdown(h_md, extras=["tables"])
    b_html = markdown2.markdown(b_md, extras=["tables"])
    f_html = markdown2.markdown(f_md, extras=["tables"])
    
    # 4. 组装图片 HTML
    fig_html = ""
    if fig_b64s:
        fig_html = "<div class='app'><h3>[ 原文图表/示意图 ]</h3>"
        for b64 in fig_b64s:
            fig_html += f"<div style='text-align:center;'><img src='{b64}' class='extracted-fig'/></div>"
        fig_html += "</div>"
        
    app_html = ""
    if annotations:
        app_html = f"<div class='app'><h3>[ 图例符号说明 ]</h3>{markdown2.markdown(annotations)}</div>"
        
    return f"""
    <div class="page-container">
        <div class="page-divider">--- Page {p_num} ---</div>
        <div class="header">{h_html}</div>
        <div class="body">{b_html}{fig_html}{app_html}</div>
        <div class="footer">{f_html}</div>
    </div>
    """

def build_pdf(html_segments, out_pdf):
    css = """@page { size: A4; margin: 15mm; } body { font-family: "Noto Sans SC", sans-serif; font-size: 9.5pt; line-height: 1.5; color: #333; } .page-container { margin-bottom: 20px; padding-bottom: 10px; border-bottom: 3px solid #f0f0f0; page-break-inside: avoid; } .page-divider { text-align: center; font-size: 8pt; color: #aaa; letter-spacing: 1px; padding: 4px; margin-bottom: 15px; background-color: #f9f9f9; border-radius: 4px; } table { width: 100%; border-collapse: collapse; margin-bottom: 12px; border: 1px solid #ccc; font-size: 8.5pt; } th, td { border: 1px solid #ccc; padding: 5px; text-align: left; } th { background-color: #f2f2f2; font-weight: bold; } .header { border-bottom: 2px solid #000; margin-bottom: 15px; padding-bottom: 5px; } .footer { border-top: 2px solid #000; margin-top: 15px; padding-top: 5px; } .app { margin-top: 20px; padding: 10px; background: #fdfdfd; border: 1px solid #eaeaea; border-radius: 5px; } .app h3 { font-size: 10pt; color: #444; text-align: center; border-bottom: 1px solid #eee; padding-bottom: 5px; } .math-inline { height: 1.3em; vertical-align: middle; margin: 0 3px; } .math-block { text-align: center; margin: 15px 0; padding: 10px; background: #f8fcfd; border-left: 3px solid #0056b3; overflow-x: auto; } .math-block img { max-width: 100%; height: auto; max-height: 60px; } .extracted-fig { max-width: 95%; max-height: 120mm; object-fit: contain; margin-top: 10px; border: 1px solid #ddd; box-shadow: 1px 1px 5px rgba(0,0,0,0.1); }"""
    html = f"<html><head><style>{css}</style></head><body>{''.join(html_segments)}</body></html>"
    html = final_sanitizer(html)
    HTML(string=html, base_url=os.getcwd()).write_pdf(out_pdf)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf_path")
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)
    args = parser.parse_args()
    
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    doc = fitz.open(args.pdf_path)
    work_dir = "v10_run"
    os.makedirs(work_dir, exist_ok=True)
    all_html = []
    
    for p in range(args.start, args.end + 1):
        try:
            all_html.append(process_page(client, doc, p, work_dir))
        except Exception as e:
            all_html.append(f"<div class='page-container'><h2>Page {p} Failed</h2><p>{e}</p></div>")

    output_filename = f"NASA_Chapter2_V10_FINAL_P{args.start}-{args.end}.pdf"
    build_pdf(all_html, output_filename)
    shutil.rmtree(work_dir, ignore_errors=True)
    print(f"✅ V10 Processing Complete: {output_filename}")

if __name__ == "__main__":
    main()
