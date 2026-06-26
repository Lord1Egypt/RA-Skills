"""
embed_fonts.py — Embed TrueType fonts into PPTX files for cross-platform fidelity.

Inserts font binary data directly into the PPTX package as font parts,
ensuring text renders identically on any system regardless of locally
installed fonts. Uses fonttools for subsetting to minimize file size.

Structure follows ECMA-376 Part 1 §19.2.1.9 (embeddedFont) and §15.2.13 (Font Part).
PPTX package is a ZIP with:
  - ppt/fonts/fontN.fntdata  — binary font data (TTF subset)
  - ppt/_rels/presentation.xml.rels — relationships to font parts
  - ppt/presentation.xml — <p:embeddedFontLst> declaration
  - [Content_Types].xml — content type mapping

Reference: https://ooxml.info/docs/19/19.2/19.2.1/19.2.1.9/
Reference: fonttools subset docs https://fonttools.readthedocs.io/en/latest/subset/
"""

import os
import zipfile
import shutil
import tempfile

from lxml import etree

NS_P = "http://schemas.openxmlformats.org/presentationml/2006/main"
NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_CT = "http://schemas.openxmlformats.org/package/2006/content-types"
RT_FONT = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/font"
FONT_CONTENT_TYPE = "application/x-fontdata"


def _get_max_rid(rels_xml):
    """Find the highest rId number in a relationships XML."""
    max_id = 0
    for rel in rels_xml:
        rid = rel.get("Id", "rId0")
        try:
            num = int(rid.replace("rId", ""))
            if num > max_id:
                max_id = num
        except ValueError:
            continue
    return max_id


def _collect_used_chars(pptx_path):
    """Extract all unique characters used in the PPTX text content."""
    chars = set()
    with zipfile.ZipFile(pptx_path, "r") as zf:
        for name in zf.namelist():
            if name.startswith("ppt/slides/slide") and name.endswith(".xml"):
                data = zf.read(name)
                tree = etree.fromstring(data)
                ns_a = "http://schemas.openxmlformats.org/drawingml/2006/main"
                for t_el in tree.iter(f"{{{ns_a}}}t"):
                    if t_el.text:
                        chars.update(t_el.text)
    chars.add(" ")
    chars.add(".")
    return chars


def _subset_font(src_path, chars, output_path, font_number=0):
    """Create a font subset containing only the specified characters.

    Uses fonttools Subsetter for minimal file size. For TTC files,
    extracts a single font by index first.

    Returns output_path on success, None on failure.
    """
    try:
        from fontTools.ttLib import TTFont
        from fontTools import subset as ft_subset
    except ImportError:
        shutil.copy2(src_path, output_path)
        return output_path

    try:
        font = TTFont(src_path, fontNumber=font_number)
    except Exception:
        try:
            font = TTFont(src_path)
        except Exception:
            shutil.copy2(src_path, output_path)
            return output_path

    try:
        options = ft_subset.Options()
        options.layout_features = ["*"]
        options.name_IDs = ["*"]
        options.notdef_outline = True
        options.recalc_bounds = True
        options.recalc_timestamp = True
        options.drop_tables = []

        subsetter = ft_subset.Subsetter(options=options)
        text = "".join(sorted(chars))
        subsetter.populate(text=text)
        subsetter.subset(font)
        font.save(output_path)
        font.close()
        return output_path
    except Exception:
        font.close()
        shutil.copy2(src_path, output_path)
        return output_path


def embed_fonts_in_pptx(pptx_path, font_specs, output_path=None):
    """Embed fonts into an existing PPTX file.

    Args:
        pptx_path: Path to existing PPTX file.
        font_specs: List of dicts, each with:
            - typeface: str — font name (e.g. "Noto Sans CJK SC")
            - regular: str — path to regular TTF/TTC file (optional)
            - bold: str — path to bold TTF/TTC file (optional)
            - pitchFamily: str — OOXML pitch+family value (default "34")
            - charset: str — OOXML charset (default "0", "128" for CJK)
        output_path: Output path (defaults to overwriting pptx_path).

    Returns:
        Path to the output PPTX.
    """
    if output_path is None:
        output_path = pptx_path

    tmpdir = tempfile.mkdtemp(prefix="pptx-font-embed-")
    try:
        with zipfile.ZipFile(pptx_path, "r") as zin:
            zin.extractall(tmpdir)

        prs_xml_path = os.path.join(tmpdir, "ppt", "presentation.xml")
        rels_path = os.path.join(tmpdir, "ppt", "_rels", "presentation.xml.rels")
        ct_path = os.path.join(tmpdir, "[Content_Types].xml")
        fonts_dir = os.path.join(tmpdir, "ppt", "fonts")
        os.makedirs(fonts_dir, exist_ok=True)

        prs_tree = etree.parse(prs_xml_path)
        prs_root = prs_tree.getroot()

        rels_tree = etree.parse(rels_path)
        rels_root = rels_tree.getroot()

        ct_tree = etree.parse(ct_path)
        ct_root = ct_tree.getroot()

        max_rid = _get_max_rid(rels_root)
        font_idx = 1

        efl = prs_root.find(f"{{{NS_P}}}embeddedFontLst")
        if efl is None:
            efl = etree.SubElement(prs_root, f"{{{NS_P}}}embeddedFontLst")
            notes_sz = prs_root.find(f"{{{NS_P}}}notesSz")
            if notes_sz is not None:
                notes_sz.addnext(efl)
            else:
                sld_sz = prs_root.find(f"{{{NS_P}}}sldSz")
                if sld_sz is not None:
                    sld_sz.addnext(efl)

        for spec in font_specs:
            typeface = spec["typeface"]
            ef = etree.SubElement(efl, f"{{{NS_P}}}embeddedFont")
            font_el = etree.SubElement(ef, f"{{{NS_P}}}font")
            font_el.set("typeface", typeface)
            font_el.set("pitchFamily", spec.get("pitchFamily", "34"))
            font_el.set("charset", spec.get("charset", "0"))

            for variant in ("regular", "bold", "italic", "boldItalic"):
                src_path = spec.get(variant)
                if not src_path or not os.path.exists(src_path):
                    continue

                max_rid += 1
                rid = f"rId{max_rid}"
                fname = f"font{font_idx}.fntdata"
                font_idx += 1

                dest = os.path.join(fonts_dir, fname)
                used_chars = _collect_used_chars(pptx_path)
                _subset_font(src_path, used_chars, dest)

                variant_el = etree.SubElement(ef, f"{{{NS_P}}}{variant}")
                variant_el.set(f"{{{NS_R}}}id", rid)

                rel_el = etree.SubElement(rels_root, "Relationship")
                rel_el.set("Id", rid)
                rel_el.set("Type", RT_FONT)
                rel_el.set("Target", f"fonts/{fname}")

                existing_ct = ct_root.find(
                    f".//{{{NS_CT}}}Override[@PartName='/ppt/fonts/{fname}']"
                )
                if existing_ct is None:
                    ov = etree.SubElement(ct_root, "Override")
                    ov.set("PartName", f"/ppt/fonts/{fname}")
                    ov.set("ContentType", FONT_CONTENT_TYPE)

        prs_xml_bytes = etree.tostring(
            prs_root, xml_declaration=True, encoding="UTF-8", standalone=True
        )
        rels_xml_bytes = etree.tostring(
            rels_root, xml_declaration=True, encoding="UTF-8", standalone=True
        )
        ct_xml_bytes = etree.tostring(
            ct_root, xml_declaration=True, encoding="UTF-8", standalone=True
        )

        modified = {
            "ppt/presentation.xml": prs_xml_bytes,
            "ppt/_rels/presentation.xml.rels": rels_xml_bytes,
            "[Content_Types].xml": ct_xml_bytes,
        }
        for idx in range(1, font_idx):
            fname = f"font{idx}.fntdata"
            fpath = os.path.join(fonts_dir, fname)
            if os.path.exists(fpath):
                with open(fpath, "rb") as ff:
                    modified[f"ppt/fonts/{fname}"] = ff.read()

        with zipfile.ZipFile(pptx_path, "r") as zin:
            with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zout:
                for item in zin.infolist():
                    if item.filename in modified:
                        zout.writestr(item, modified.pop(item.filename))
                    else:
                        zout.writestr(item, zin.read(item.filename))
                for name, data in modified.items():
                    zout.writestr(name, data)

        return output_path
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def get_default_font_specs():
    """Return font specs for commonly used fonts in our PPT generation.

    Only embeds TTF-format fonts. CFF/OTF fonts (like Noto Sans CJK TTC)
    are excluded because MS PowerPoint rejects them as embedded font data,
    triggering the 'needs repair' prompt. CJK text falls back to the
    system's Microsoft YaHei on Windows, which is acceptable.
    Reference: MS-OE376 §15.2.12 specifies TrueType format for font parts.
    """
    specs = []

    arial_regular = "/usr/share/fonts/truetype/msttcorefonts/Arial.ttf"
    arial_bold = "/usr/share/fonts/truetype/msttcorefonts/Arial_Bold.ttf"

    if os.path.exists(arial_regular):
        specs.append({
            "typeface": "Arial",
            "regular": arial_regular,
            "bold": arial_bold if os.path.exists(arial_bold) else None,
            "pitchFamily": "34",
            "charset": "0",
        })

    return specs


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 embed_fonts.py <input.pptx> [output.pptx]")
        sys.exit(1)

    in_path = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else in_path

    specs = get_default_font_specs()
    if not specs:
        print("No fonts found to embed.")
        sys.exit(1)

    print(f"Embedding {len(specs)} font(s)...")
    for s in specs:
        variants = [v for v in ("regular", "bold", "italic", "boldItalic") if s.get(v)]
        print(f"  {s['typeface']}: {', '.join(variants)}")

    result = embed_fonts_in_pptx(in_path, specs, out_path)
    print(f"Done: {result}")
