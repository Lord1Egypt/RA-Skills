import sys
import os
import io
import fitz
import logging
import zipfile
import tempfile
from uuid import uuid1
from PIL import Image

# =============================================================================
# OpenClaw Skill: PDF to OFD High-Fidelity Converter
# Version: 1.1.0
# Description: Converts PDF to OFD with character-level precision and
#              advanced vector graphics support.
# =============================================================================
# Logging Configuration
# =============================================================================
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("OpenClaw-PDF2OFD")

# =============================================================================
# Constants & Geometry
# =============================================================================
INVOICE_RED = "128 0 0"
PT_TO_MM = 25.4 / 72.0

# =============================================================================
# Font Mapping Table
# =============================================================================
FONT_MAP = {
    "SimSun": "宋体",
    "NSimSun": "新宋体",
    "STSong": "宋体",
    "Songti": "宋体",
    "KaiTi": "楷体",
    "STKaiti": "楷体",
    "Kaiti": "楷体",
    "SimHei": "黑体",
    "Heiti": "黑体",
    "STHeiti": "黑体",
    "FangSong": "仿宋",
    "STFangsong": "仿宋",
    "Arial": "Arial",
    "TimesNewRoman": "Times New Roman",
    "Courier": "Courier New",
}

def get_font_name(pdf_font_name):
    base_name = pdf_font_name.split('+')[-1].replace(" ", "").replace("-", "")
    for key, val in FONT_MAP.items():
        if key.lower() in base_name.lower():
            return val
    if "song" in base_name.lower(): return "宋体"
    if "kai" in base_name.lower(): return "楷体"
    if "hei" in base_name.lower(): return "黑体"
    if "fang" in base_name.lower(): return "仿宋"
    return base_name

# =============================================================================
# Monkey Patch Logic
# =============================================================================
def apply_skill_patches():
    from easyofd.draw.pdf_parse import DPFParser
    from easyofd.draw.draw_ofd import OFDWrite
    from easyofd.draw.ofdtemplate import ContentTemplate, DocumentResTemplate, CurId, OFDStructure, DocumentTemplate

    # 1. Improved PDF Parser (High Fidelity from rawdict)
    def patched_extract(self, doc_byte):
        res_map = {"img": {}, "font": {}, "other": {"page_size": []}}
        details = []
        with fitz.open(stream=doc_byte, filetype="pdf") as doc:
            for page in doc:
                res_map["other"]["page_size"].append(list(page.rect))
                page_data = []
                # Text
                for block in page.get_text("rawdict").get("blocks", []):
                    if block.get("type") == 0:
                        for l in block["lines"]:
                            for s in l["spans"]:
                                chars = s.get("chars", [])
                                text = "".join([c["c"] for c in chars])
                                if not text.strip(): continue
                                f_name = get_font_name(s["font"])
                                res_uid = f"F_{f_name}"
                                res_map["font"][res_uid] = f_name
                                
                                delta_x = []
                                if chars:
                                    for i in range(len(chars) - 1):
                                        d = chars[i+1]["origin"][0] - chars[i]["origin"][0]
                                        delta_x.append(f"{d * PT_TO_MM:.4f}")
                                
                                color_int = s["color"]
                                r, g, b = (color_int >> 16) & 255, (color_int >> 8) & 255, color_int & 255
                                cur_c = INVOICE_RED if (r > 100 and g < 70 and b < 70) else f"{r} {g} {b}"
                                
                                page_data.append({
                                    "type": "text", "text": text, "res_uuid": res_uid, "size": s["size"], "bbox": list(s["bbox"]), "color": cur_c,
                                    "delta_x": " ".join(delta_x) if delta_x else None,
                                    "origin": list(chars[0]["origin"]) if chars else [s["bbox"][0], s["bbox"][3]]
                                })
                # Images
                for img in page.get_images(full=True):
                    xref, smask_xref = img[0], img[1]
                    res_uid = f"IMG_{xref}"
                    try:
                        pix = fitz.Pixmap(doc, xref)
                        if smask_xref > 0: pix = fitz.Pixmap(pix, fitz.Pixmap(doc, smask_xref))
                        if pix.colorspace and pix.colorspace.n not in (3, 4): pix = fitz.Pixmap(fitz.csRGB, pix)
                        buf = io.BytesIO()
                        if pix.alpha:
                             Image.frombytes("RGBA", [pix.width, pix.height], pix.samples).save(buf, format="PNG")
                             ext = "png"
                        else:
                             Image.frombytes("RGB", [pix.width, pix.height], pix.samples).save(buf, format="JPEG")
                             ext = "jpg"
                        res_map["img"][res_uid] = (buf, ext)
                        for r in page.get_image_rects(xref):
                            if r: page_data.append({"type": "img", "bbox": list(r), "res_uuid": res_uid})
                    except: pass
                # Paths
                for d in page.get_drawings():
                    def color_to_str(c):
                        if not c: return None
                        return f"{int(c[0]*255)} {int(c[1]*255)} {int(c[2]*255)}"
                    s_color = color_to_str(d.get("color"))
                    f_color = color_to_str(d.get("fill"))
                    if s_color and " 0 0" in s_color and int(s_color.split()[0]) > 100: s_color = INVOICE_RED
                    if f_color and " 0 0" in f_color and int(f_color.split()[0]) > 100: f_color = INVOICE_RED

                    abbr = []
                    last_point = None
                    for i in d.get("items", []):
                        if i[0] == "l":
                            p1, p2 = (i[1].x, i[1].y), (i[2].x, i[2].y)
                            if last_point == p1: abbr.append(f"L {p2[0]:.4f} {p2[1]:.4f}")
                            else: abbr.append(f"M {p1[0]:.4f} {p1[1]:.4f} L {p2[0]:.4f} {p2[1]:.4f}")
                            last_point = p2
                        elif i[0] == "re":
                            r = i[1]
                            abbr.append(f"M {r.x0:.4f} {r.y0:.4f} L {r.x1:.4f} {r.y0:.4f} L {r.x1:.4f} {r.y1:.4f} L {r.x0:.4f} {r.y1:.4f} C")
                            last_point = None
                        elif i[0] == "c":
                            abbr.append(f"M {i[1].x:.4f} {i[1].y:.4f} B {i[2].x:.4f} {i[2].y:.4f} {i[3].x:.4f} {i[3].y:.4f} {i[4].x:.4f} {i[4].y:.4f}")
                            last_point = (i[4].x, i[4].y)
                    if not abbr: continue
                    path_str = " ".join(abbr).replace("M", " M ").replace("L", " L ").replace("B", " B ").replace("C", " C ")
                    page_data.append({
                        "type": "path", "abbr": path_str.split(), "bbox": list(d["rect"]),
                        "width": d.get("width", 0.1), "is_closed": "C" in path_str,
                        "draw_type": d.get("type", "fs"),
                        "stroke_color": s_color, "fill_color": f_color,
                        "opacity": d.get("opacity", 1.0), "fill_opacity": d.get("fill_opacity", 1.0)
                    })
                details.append(page_data)
        return details, res_map
    DPFParser.extract_text_with_details = patched_extract

    # 2. FIXED: Document Resources (Consistent ID naming and extensions)
    def patched_doc_res(instance, img_len=0, id_obj=None, pfd_res_uuid_map=None):
        MultiMedia = []
        if pfd_res_uuid_map and (p_img := pfd_res_uuid_map.get("img")):
            for uid, val in p_img.items():
                if isinstance(val, tuple):
                    _, ext = val
                    MultiMedia.append({"@ID": 0, "@Type": "Image", "ofd:MediaFile": f"Image_{uid}.{ext}", "res_uuid": uid})
        return DocumentResTemplate(MultiMedia=MultiMedia, id_obj=id_obj)
    OFDWrite.build_document_res = patched_doc_res

    # 3. Build Content with geometry fixes
    def patched_build_content(instance, pdf_info_list=None, **kwargs):
        id_obj, res_map = kwargs.get("id_obj"), kwargs.get("pfd_res_uuid_map")
        results = []
        for idx, content in enumerate(pdf_info_list):
            txts, imgs, paths = [], [], []
            p_rect = res_map["other"]["page_size"][idx]
            pw, ph = (p_rect[2]-p_rect[0])*PT_TO_MM, (p_rect[3]-p_rect[1])*PT_TO_MM
            for b in content:
                box = b['bbox']
                x0, y0 = box[0] * PT_TO_MM, box[1] * PT_TO_MM
                bw, bh = (box[2]-box[0])*PT_TO_MM, (box[3]-box[1])*PT_TO_MM
                if b["type"] == "text":
                    s_m = (b.get('size') or 12) * PT_TO_MM
                    ox, oy = (b["origin"][0] - box[0]) * PT_TO_MM, (b["origin"][1] - box[1]) * PT_TO_MM
                    
                    # Manual Font ID mapping
                    font_id = id_obj.uuid_map.get(b["res_uuid"])
                    
                    t_obj = {
                        "@ID": 0, "@size": f"{s_m:.4f}", "@Boundary": f"{x0:.4f} {y0:.4f} {bw:.4f} {bh:.4f}",
                        "@Font": f"{font_id or ''}",
                        "ofd:FillColor": {"@Value": b.get("color", "0 0 0")},
                        "ofd:TextCode": {"#text": b["text"], "@X": f"{ox:.4f}", "@Y": f"{oy:.4f}"}
                    }
                    if b.get("delta_x"): t_obj["ofd:TextCode"]["@DeltaX"] = b["delta_x"]
                    else: t_obj["ofd:TextCode"]["@DeltaX"] = f"g {len(b['text'])-1} {(bw/max(1, len(b['text']))):.4f}"
                    txts.append(t_obj)
                elif b["type"] == "img":
                    # Manual Image Resource mapping
                    res_id = id_obj.uuid_map.get(b["res_uuid"])
                    if res_id:
                        imgs.append({
                            "@ID": 0, "@Boundary": f"{x0:.4f} {y0:.4f} {max(0.0001,bw):.4f} {max(0.0001,bh):.4f}", 
                            "@CTM": f"{max(0.0001,bw):.4f} 0 0 {max(0.0001,bh):.4f} 0 0", 
                            "@ResourceID": f"{res_id}"
                        })
                elif b["type"] == "path":
                    conv_p, cursor = [], 'X'
                    for p in b['abbr']:
                        try:
                            v = float(p)
                            conv_p.append(f"{(v - (box[0] if cursor == 'X' else box[1])) * PT_TO_MM:.4f}")
                            cursor = 'Y' if cursor == 'X' else 'X'
                        except:
                            conv_p.append(p)
                            if p in ('M', 'L', 'Q', 'B'): cursor = 'X'
                    l_w = max(0.01, (b.get('width') or 0.1) * PT_TO_MM * 0.5)
                    p_obj = {"@ID": 0, "@Boundary": f"{x0:.4f} {y0:.4f} {max(0.0001,bw):.4f} {max(0.0001,bh):.4f}", "ofd:AbbreviatedData": " ".join(conv_p), "@LineWidth": f"{l_w:.4f}"}
                    
                    draw_type = b.get("draw_type", "fs")
                    if "f" in draw_type or b.get("is_closed"):
                        f_color = b.get("fill_color") or INVOICE_RED
                        p_obj.update({"@Fill": "true", "ofd:FillColor": {"@Value": f_color}})
                        if b.get("fill_opacity", 1.0) < 1.0: p_obj["ofd:FillColor"]["@Alpha"] = int(b["fill_opacity"] * 255)
                    if "s" in draw_type or not b.get("is_closed"):
                        s_color = b.get("stroke_color") or INVOICE_RED
                        p_obj.update({"@Stroke": "true", "ofd:StrokeColor": {"@Value": s_color}})
                        if b.get("opacity", 1.0) < 1.0: p_obj["ofd:StrokeColor"]["@Alpha"] = int(b["opacity"] * 255)
                    paths.append(p_obj)
            tpl = ContentTemplate(PhysicalBox=f"0 0 {pw:.4f} {ph:.4f}", ImageObject=imgs, PathObject=paths, TextObject=txts, id_obj=id_obj)
            if paths:
                tpl.final_json["ofd:Page"]["ofd:Content"]["ofd:Layer"]["ofd:PathObject"] = paths
                for p in paths: p["@ID"] = f"{id_obj.get_id()}"
            results.append(tpl)
        return results
    OFDWrite.build_content_res = patched_build_content

    # 3. Virtual ZIP Generation
    def patched_ofd_call(self, test=False):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_doc_0 = os.path.join(temp_dir, 'Doc_0')
            temp_dir_pages = os.path.join(temp_dir, 'Doc_0', "Pages")
            temp_dir_res = os.path.join(temp_dir, 'Doc_0', "Res")
            for i in [temp_dir_doc_0, temp_dir_pages, temp_dir_res]: os.mkdir(i)
            self.ofd.save(os.path.join(temp_dir, 'OFD.xml'))
            self.document.update_max_unit_id()
            self.document.save(os.path.join(temp_dir_doc_0, 'Document.xml'))
            self.document_res.save(os.path.join(temp_dir_doc_0, 'DocumentRes.xml'))
            self.public_res.save(os.path.join(temp_dir_doc_0, 'PublicRes.xml'))
            for idx, page in enumerate(self.content_res):
                temp_dir_pages_idx = os.path.join(temp_dir_pages, f"Page_{idx}")
                os.mkdir(temp_dir_pages_idx)
                page.save(os.path.join(temp_dir_pages_idx, 'Content.xml'))
            for k, v in self.res_static.items():
                with open(os.path.join(temp_dir_res, k), "wb") as f: f.write(v)
            buf = io.BytesIO()
            with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zip_f:
                for path, _, filenames in os.walk(temp_dir):
                    fpath = path.replace(temp_dir, '').strip('/\\')
                    for filename in filenames:
                        zip_f.write(os.path.join(path, filename), arcname=os.path.join(fpath, filename))
            return buf.getvalue()
    OFDStructure.__call__ = patched_ofd_call

    # 4. Global call override
    def patched_main_call(instance, pdf_bytes=None, optional_text=False, **kwargs):
        if not pdf_bytes: return None
        info, res_map = DPFParser().extract_text_with_details(pdf_bytes)
        id_obj = CurId()
        p_rect = res_map["other"]["page_size"][0]
        pw, ph = (p_rect[2]-p_rect[0])*PT_TO_MM, (p_rect[3]-p_rect[1])*PT_TO_MM
        ent = instance.build_ofd_entrance(id_obj=id_obj)
        doc = instance.build_document(len(info), id_obj=id_obj, PhysicalBox=f"0 0 {pw:.4f} {ph:.4f}")
        pub = instance.build_public_res(id_obj=id_obj, pfd_res_uuid_map=res_map)
        d_res = instance.build_document_res(id_obj=id_obj, pfd_res_uuid_map=res_map)
        cont = instance.build_content_res(pdf_info_list=info, id_obj=id_obj, pfd_res_uuid_map=res_map)
        st_res = {f"Image_{k}.{ext}": data.getvalue() for k, v in res_map.get("img", {}).items() if isinstance(v, tuple) for data, ext in [v]}
        return OFDStructure("doc", ofd=ent, document=doc, public_res=pub, document_res=d_res, content_res=cont, res_static=st_res)(test=False)
    OFDWrite.__call__ = patched_main_call

# =============================================================================
# Skill Implementation
# =============================================================================
class PDF2OFDConverter:
    def __init__(self):
        apply_skill_patches()

    def convert(self, pdf_bytes: bytes) -> bytes:
        from easyofd.draw.draw_ofd import OFDWrite
        writer = OFDWrite()
        return writer(pdf_bytes=pdf_bytes, optional_text=True)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pdf2ofd.py <input.pdf> [output.ofd]")
        sys.exit(1)
    
    input_pdf = sys.argv[1]
    output_ofd = sys.argv[2] if len(sys.argv) > 2 else input_pdf.rsplit(".", 1)[0] + ".ofd"
    
    with open(input_pdf, "rb") as f:
        pdf_data = f.read()
    
    converter = PDF2OFDConverter()
    ofd_data = converter.convert(pdf_data)
    
    with open(output_ofd, "wb") as f:
        f.write(ofd_data)
    print(f"Success: {output_ofd}")
