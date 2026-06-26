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

# --- QA & Helper Functions ---
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

# --- Agent Definitions ---

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=4, max=20), retry=retry_if_exception_type((QualityCheckFailed, APIRateLimitExceeded)))
def agent_1_5_annotate(client, fig_path):
    print(f"    -> [Agent 1.5] Annotating figure: {os.path.basename(fig_path)}")
    uploaded = client.files.upload(file=fig_path)
    prompt = """
    Analyze this engineering diagram. Extract all text labels and their corresponding descriptions from the image.
    Format the output as a clean, simple Markdown list. Example:
    * **Symbol**: Description
    * **m**: mass
    If no labels are found, return an empty string.
    """
    res = client.models.generate_content(model='gemini-2.5-pro', contents=[prompt, uploaded])
    return res.text.strip()

@retry(stop=stop_after_attempt(4), wait=wait_exponential(min=4, max=30), retry=retry_if_exception_type((QualityCheckFailed, APIRateLimitExceeded)))
def agent_2_translate(client, img_path, p_num, ctx_prompt):
    uploaded = client.files.upload(file=img_path)
    prompt = f"""
    {ctx_prompt}
    你是航天翻译专家。处理第{p_num}页。
    【V9军规】：
    1. 绝对不要改动数学公式和字母变量大小写。数学公式必须用 `$` 或 `$$` 包裹。
    2. 全文翻译为【纯正中文】。严禁出现中英夹杂。
    3. 对于公式中符号的说明，必须使用格式：`**$变量$**: 变量的中文说明`
    4. 严格使用 XML 标签：<HEADER>...</HEADER><BODY>...</BODY><FOOTER>...</FOOTER>
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
    print(f"\n[*] V9 Final Engine Processing Page {p_num}...")
    main_img = os.path.join(work_dir, f"p{p_num}.png")
    doc[p_num-1].get_pixmap(matrix=fitz.Matrix(2.5, 2.5)).save(main_img)
    
    annotations = ""
    # Heuristic for image-heavy pages
    if p_num in [13, 14, 27]:
        annotations = agent_1_5_annotate(client, main_img)
        
    ctx_prompt = ""
    if p_num > 1:
        prev = doc[p_num-2].get_text()[-300:]
        if prev: ctx_prompt += f"【上一页参考】：{prev}\n"

    xml = agent_2_translate(client, main_img, p_num, ctx_prompt)
    h_md = re.search(r'<HEADER>(.*?)</HEADER>', xml, re.S).group(1).strip()
    b_md = re.search(r'<BODY>(.*?)</BODY>', xml, re.S).group(1).strip()
    f_md = re.search(r'<FOOTER>(.*?)</FOOTER>', xml, re.S).group(1).strip()

    b_md = re.sub(r'\$\$([\s\S]+?)\$\$', lambda m: math_svg(m, True), b_md)
    b_md = re.sub(r'(?<!\$)\$([^\$]+)\$(?!\$)', lambda m: math_svg(m, False), b_md)

    h_html = markdown2.markdown(h_md, extras=["tables"])
    b_html = markdown2.markdown(b_md, extras=["tables"])
    f_html = markdown2.markdown(f_md, extras=["tables"])
    
    app_html = ""
    if annotations:
        app_html = f"<div class='app'><h3>[ 图例符号说明 ]</h3>{markdown2.markdown(annotations)}</div>"
        
    return f"""
    <div class="page-container">
        <div class="page-divider">--- Page {p_num} ---</div>
        <div class="header">{h_html}</div>
        <div class="body">{b_html}{app_html}</div>
        <div class="footer">{f_html}</div>
    </div>
    """

def build_pdf(html_segments, out_pdf):
    css = """@page { size: A4; margin: 15mm; } body { font-family: "Noto Sans SC", sans-serif; font-size: 9.5pt; line-height: 1.5; color: #333; } .page-container { margin-bottom: 20px; padding-bottom: 10px; border-bottom: 3px solid #f0f0f0; page-break-inside: avoid; } .page-divider { text-align: center; font-size: 8pt; color: #aaa; letter-spacing: 1px; padding: 4px; margin-bottom: 15px; background-color: #f9f9f9; border-radius: 4px; } table { width: 100%; border-collapse: collapse; margin-bottom: 12px; border: 1px solid #ccc; font-size: 8.5pt; } th, td { border: 1px solid #ccc; padding: 5px; text-align: left; } th { background-color: #f2f2f2; font-weight: bold; } .header { border-bottom: 2px solid #000; margin-bottom: 15px; padding-bottom: 5px; } .footer { border-top: 2px solid #000; margin-top: 15px; padding-top: 5px; } .app { margin-top: 20px; padding: 10px; background: #fdfdfd; border: 1px solid #eaeaea; border-radius: 5px; } .app h3 { font-size: 10pt; color: #444; text-align: center; border-bottom: 1px solid #eee; padding-bottom: 5px; } .math-inline { height: 1.3em; vertical-align: middle; margin: 0 3px; } .math-block { text-align: center; margin: 15px 0; padding: 10px; background: #f8fcfd; border-left: 3px solid #0056b3; overflow-x: auto; } .math-block img { max-width: 100%; height: auto; max-height: 60px; }"""
    html = f"<html><head><style>{css}</style></head><body>{''.join(html_segments)}</body></html>"
    html = final_sanitizer(html)
    HTML(string=html, base_url=os.getcwd()).write_pdf(out_pdf)

def main():
    parser = argparse.ArgumentParser(description="V9 Final PDF Translation Engine")
    parser.add_argument("pdf_path", help="Path to the source PDF file.")
    parser.add_argument("--start", type=int, required=True, help="Starting page number.")
    parser.add_argument("--end", type=int, required=True, help="Ending page number.")
    args = parser.parse_args()
    
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    doc = fitz.open(args.pdf_path)
    
    work_dir = "v9_final_run"
    os.makedirs(work_dir, exist_ok=True)
    all_html = []
    
    for p in range(args.start, args.end + 1):
        try:
            all_html.append(process_page(client, doc, p, work_dir))
            time.sleep(3) # Rate limiting
        except Exception as e:
            error_message = f"❌ FATAL ERROR on Page {p}: {e}"
            print(error_message)
            all_html.append(f"<div class='page-container'><h2>Page {p} Failed</h2><p>{error_message}</p></div>")

    output_filename = f"NASA_Chapter2_V9_FINAL_P{args.start}-{args.end}.pdf"
    build_pdf(all_html, output_filename)
    shutil.rmtree(work_dir, ignore_errors=True)
    print(f"✅ V9 Final Processing Complete! Output: {output_filename}")

if __name__ == "__main__":
    main()
