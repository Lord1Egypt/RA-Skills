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

def agent_1_layout(client, img_path, p_num):
    uploaded = client.files.upload(file=img_path)
    prompt = f"""
    分析第{p_num}页布局。区分工程示意图(figures)和数据表格(tables)。
    不要包含页眉页脚的纯文本表格。
    严格返回 JSON：
    {{ "figures": [ [ymin, xmin, ymax, xmax] ], "tables": [ [ymin, xmin, ymax, xmax] ] }}
    坐标为0-1000的归一化。空则传 []。
    """
    res = client.models.generate_content(model='gemini-2.5-pro', contents=[prompt, uploaded])
    return qa_check_json(res.text, ["figures", "tables"])

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=15), retry=retry_if_exception_type(QualityCheckFailed))
def agent_table_worker(client, img_path):
    uploaded = client.files.upload(file=img_path)
    res1 = client.models.generate_content(model='gemini-2.5-pro', contents=["将此表格翻译为中文，输出严格的 Markdown 表格格式，严禁改动公式/变量大小写。不要包含任何 Markdown 代码块包装符号（如 ```markdown）。", uploaded])
    md_table = res1.text.strip()
    if md_table.startswith("```"): md_table = re.sub(r"^```(?:markdown)?\n|```\n?$", "", md_table, flags=re.MULTILINE).strip()
    
    qa_prompt = f"""
    图1是原始表格。图2(文本)是提取的 Markdown:
    {md_table}
    请严格判断：Markdown是否准确无损地还原了原图表格的所有数据和结构（翻译除外）？
    如果存在行列错位、数据丢失、公式错误，返回 {{"is_accurate": false}}。
    如果完美还原，返回 {{"is_accurate": true}}。
    """
    res2 = client.models.generate_content(model='gemini-2.5-flash', contents=[qa_prompt, uploaded])
    qa_data = qa_check_json(res2.text, ["is_accurate"])
    
    if not qa_data["is_accurate"]: raise QualityCheckFailed("Table accuracy check failed.")
    return md_table

@retry(stop=stop_after_attempt(4), wait=wait_exponential(min=4, max=30), retry=retry_if_exception_type((QualityCheckFailed, APIRateLimitExceeded)))
def agent_2_translate(client, masked_img_path, p_num, ctx_prompt):
    uploaded = client.files.upload(file=masked_img_path)
    prompt = f"""
    {ctx_prompt}
    你是航天翻译专家。处理涂白图表后的第{p_num}页。
    【死命令】：
    1. 绝对不要改动数学公式和字母变量大小写。数学公式必须用 `$` 或 `$$` 包裹。
    2. 全文翻译为【纯正中文】（除保留原本的公式变量和必须保留的英文缩写外，严禁出现中英夹杂的半调子翻译）。
    3. 【绝对禁止】：不要在你的输出中包含任何 "```markdown" 或 "```" 这种代码块包装符号。直接输出纯文本内容！
    4. 严格使用 XML 标签包裹内容：
    <HEADER>页眉/修订表</HEADER>
    <BODY>正文翻译</BODY>
    <FOOTER>底部图框</FOOTER>
    
    重要：【强制页眉页脚格式一致性】
    页眉（HEADER）通常包含：MSFC 表格 422-8，续页，修订记录。请统一翻译或保留固定标识。
    页脚（FOOTER）通常包含：代码标识号，图幅 A，DWG NO 20M02540，以及页码。
    请确保每一页的页眉和页脚结构极其统一，即使原图上有轻微缺损也必须以 Markdown 表格的形式统一输出！
    """
    try:
        res = client.models.generate_content(model='gemini-2.5-pro', contents=[prompt, uploaded])
        text = res.text
        
        text = re.sub(r'```markdown\n?', '', text)
        text = re.sub(r'```\n?', '', text)
        
        if not (re.search(r'<HEADER>.*?</HEADER>', text, re.S) and re.search(r'<BODY>.*?</BODY>', text, re.S) and re.search(r'<FOOTER>.*?</FOOTER>', text, re.S)):
            raise QualityCheckFailed("XML Tags missing.")
            
        return text
    except Exception as e:
        if "429" in str(e): raise APIRateLimitExceeded(e)
        raise QualityCheckFailed(e)

def b64_img(path):
    with open(path, "rb") as f: return f"data:image/png;base64,{base64.b64encode(f.read()).decode('utf-8')}"

def math_svg(match, is_block):
    url = f"https://math.vercel.app/?from={urllib.parse.quote(match.group(1).strip())}"
    return f'\n<div class="math-block"><img src="{url}"></div>\n' if is_block else f'<img src="{url}" class="math-inline">'

def process_page(client, doc, p_num, work_dir):
    print(f"\n[*] Processing Page {p_num}...")
    main_img = os.path.join(work_dir, f"p{p_num}.png")
    doc[p_num-1].get_pixmap(matrix=fitz.Matrix(2,2)).save(main_img)
    
    layout = agent_1_layout(client, main_img, p_num)
    
    fig_b64s = []
    table_mds = []
    full_text_ctx = doc[p_num-1].get_text()
    
    masked_img = main_img
    with Image.open(main_img) as im:
        w, h = im.size
        masked_im = im.copy()
        draw = ImageDraw.Draw(masked_im)
        
        for idx, box in enumerate(layout.get("tables", [])):
            l, t, r, b = box[1]*w/1000, box[0]*h/1000, box[3]*w/1000, box[2]*h/1000
            if (r-l)*(b-t) < (w*h*0.01): continue
            crop_fn = os.path.join(work_dir, f"p{p_num}_tbl_{idx}.png")
            im.crop((l, t, r, b)).save(crop_fn)
            try:
                md_tbl = agent_table_worker(client, crop_fn)
                table_mds.append(md_tbl)
                draw.rectangle([l, t, r, b], fill="white")
            except QualityCheckFailed:
                fig_b64s.append(b64_img(crop_fn))
                draw.rectangle([l, t, r, b], fill="white")
                
        for idx, box in enumerate(layout.get("figures", [])):
            l, t, r, b = box[1]*w/1000, box[0]*h/1000, box[3]*w/1000, box[2]*h/1000
            if (r-l)*(b-t) < (w*h*0.01): continue
            crop_fn = os.path.join(work_dir, f"p{p_num}_fig_{idx}.png")
            im.crop((l, t, r, b)).save(crop_fn)
            fig_b64s.append(b64_img(crop_fn))
            draw.rectangle([l, t, r, b], fill="white")
            
        masked_img = os.path.join(work_dir, f"p{p_num}_masked.png")
        masked_im.save(masked_img)

    ctx_prompt = f"【本页完整原文参考】:\n{full_text_ctx}\n"
    if p_num > 1:
        prev = doc[p_num-2].get_text()[-300:]
        if prev: ctx_prompt += f"【上一页参考】：{prev}\n"

    xml = agent_2_translate(client, masked_img, p_num, ctx_prompt)
    h_md = re.search(r'<HEADER>(.*?)</HEADER>', xml, re.S).group(1).strip()
    b_md = re.search(r'<BODY>(.*?)</BODY>', xml, re.S).group(1).strip()
    f_md = re.search(r'<FOOTER>(.*?)</FOOTER>', xml, re.S).group(1).strip()

    if table_mds:
        b_md += "\n\n" + "\n\n".join(table_mds)

    b_md = re.sub(r'\$\$([\s\S]+?)\$\$', lambda m: math_svg(m, True), b_md)
    b_md = re.sub(r'(?<!\$)\$([^\$]+)\$(?!\$)', lambda m: math_svg(m, False), b_md)

    h_html = markdown2.markdown(h_md, extras=["tables"])
    b_html = markdown2.markdown(b_md, extras=["tables"])
    f_html = markdown2.markdown(f_md, extras=["tables"])

    app_html = ""
    if fig_b64s:
        app_html = "<div class='app'><h3>[ 本页原图参考 ]</h3>"
        for b64 in fig_b64s: app_html += f"<div style='text-align:center;'><img src='{b64}' class='extracted-fig'/></div>"
        app_html += "</div>"

    # 新增：更醒目的分页视觉效果，使用一个灰色的页码分隔条和强烈的虚线分割
    return f"""
    <div class="page-container">
        <div class="page-divider">
            <span>--- Page {p_num} ---</span>
        </div>
        <div class="header">{h_html}</div>
        <div class="body">{b_html}{app_html}</div>
        <div class="footer">{f_html}</div>
    </div>
    """

def build_pdf(html_segments, out_pdf):
    # CSS 深度优化：页眉页脚标准化，分页条更醒目
    css = """
    @page { size: A4; margin: 15mm; } 
    body { font-family: sans-serif; font-size: 9.5pt; line-height: 1.4; color: #222; } 
    .page-container { 
        margin-bottom: 25px; 
        padding-bottom: 15px; 
        page-break-inside: avoid; 
        position: relative;
    } 
    /* 醒目的分页分割条 */
    .page-divider {
        background-color: #e0e0e0;
        color: #555;
        text-align: center;
        font-size: 8pt;
        font-weight: bold;
        letter-spacing: 2px;
        padding: 4px 0;
        margin-bottom: 15px;
        border-radius: 3px;
        border: 1px solid #ccc;
    }
    
    table { width: 100%; border-collapse: collapse; margin-bottom: 10px; border: 1px solid #000; font-size: 8.5pt; } 
    th, td { border: 1px solid #000; padding: 4px; } 
    th { background-color: #f5f5f5; text-align: center; } /* 统一表头居中 */
    
    /* 页眉页脚强制规范样式，去除多余空白，统一底色 */
    .header { border-bottom: 2px solid #000; margin-bottom: 15px; padding-bottom: 5px; } 
    .header table { margin-bottom: 0; background-color: #fafafa; }
    
    .footer { border-top: 2px solid #000; margin-top: 15px; padding-top: 5px; } 
    .footer table { margin-bottom: 0; background-color: #fafafa; text-align: center; } /* 底部图框居中 */
    
    .app { margin-top: 20px; padding: 10px; background: #fafafa; border: 1px solid #ddd; } 
    .app h3 { font-size: 10pt; color: #555; text-align: center; border-bottom: 1px dashed #ccc; padding-bottom: 5px; } 
    .extracted-fig { max-width: 90%; max-height: 120mm; object-fit: contain; margin-top: 10px; border: 1px solid #ddd; box-shadow: 1px 1px 5px rgba(0,0,0,0.1); } 
    .math-inline { height: 1.2em; vertical-align: middle; margin: 0 2px; } 
    .math-block { text-align: center; margin: 15px 0; padding: 10px; background: #f8fcfd; border-left: 3px solid #0056b3; overflow-x: auto; } 
    .math-block img { max-width: 100%; height: auto; max-height: 60px; }
    """
    html = f"<html><head><style>{css}</style></head><body>{''.join(html_segments)}</body></html>"
    HTML(string=html, base_url=os.getcwd()).write_pdf(out_pdf)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf_path")
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--end", type=int, default=0)
    args = parser.parse_args()
    
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    doc = fitz.open(args.pdf_path)
    
    os.makedirs("translator_tmp_v6", exist_ok=True)
    all_html = []
    
    for p in range(args.start, args.end + 1):
        try:
            all_html.append(process_page(client, doc, p, "translator_tmp_v6"))
        except Exception as e:
            all_html.append(f"<div class='page-container'><h2>Page {p} Failed</h2><p>{e}</p></div>")

    build_pdf(all_html, f"NASA_Chapter2_V6_P{args.start}-{args.end}.pdf")
    shutil.rmtree("translator_tmp_v6", ignore_errors=True)
    print("✅ V6 Processing Complete!")
