#!/usr/bin/env python3
"""
Merge multiple PPTX files into one — ZIP-level copy with full chart/embedding support.

Strategy:
  - Treat each .pptx as a ZIP archive (never use python-pptx slide copy API)
  - Copy slide XML, rels, chart XML, embeddings, and media files directly
  - Remap all file references to avoid name collisions (chart1→chartN, etc.)
  - Patch presentation.xml + rels + [Content_Types].xml to register new slides
  - Repack into final.pptx

Root cause this script fixes:
  pptxgenjs writes chart refs as ABSOLUTE paths (/ppt/charts/chart1.xml).
  When multiple slides each have chart1.xml, the python-pptx relate_to() API
  produces duplicate zip entries and corrupt/wrong chart data.
  This script renames every chart/embedding file to a unique index before merging.
"""

import argparse
import copy
import os
import re
import sys
import glob
import zipfile
from pathlib import Path
from lxml import etree

# ── XML namespaces ─────────────────────────────────────────────────────────────
RELS_NS  = "http://schemas.openxmlformats.org/package/2006/relationships"
CT_NS    = "http://schemas.openxmlformats.org/package/2006/content-types"
PRES_NS  = "http://schemas.openxmlformats.org/presentationml/2006/main"
R_NS     = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

SLIDE_CT       = "application/vnd.openxmlformats-officedocument.presentationml.slide+xml"
CHART_CT       = "application/vnd.openxmlformats-officedocument.drawingml.chart+xml"
SLIDE_REL_TYPE = f"{R_NS}/slide"


# ── helpers ────────────────────────────────────────────────────────────────────

def read_zip(path):
    with zipfile.ZipFile(path, "r") as z:
        return {name: z.read(name) for name in z.namelist()}


def write_zip(path, files):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in sorted(files.items()):
            z.writestr(name, data if isinstance(data, bytes) else data.encode("utf-8"))


def xparse(data):
    return etree.fromstring(data)


def xbytes(tree):
    return etree.tostring(tree, xml_declaration=True, encoding="UTF-8", standalone=True)


def count_pat(files, pattern):
    return len([n for n in files if re.match(pattern, n)])


def inspect_pptx(path):
    """Return (n_slides, n_shapes) for quick validation."""
    try:
        with zipfile.ZipFile(path) as z:
            names = z.namelist()
            slides = [n for n in names if re.match(r"ppt/slides/slide\d+\.xml$", n)]
            shapes = 0
            for sn in slides:
                root = xparse(z.read(sn))
                for sp in root.findall(".//{http://schemas.openxmlformats.org/presentationml/2006/main}spTree"):
                    shapes += len(list(sp))
            return len(slides), shapes
    except Exception as e:
        return 0, str(e)


# ── core merge logic ───────────────────────────────────────────────────────────

def add_slide(dest, src, src_slide_num=1):
    """
    Append one slide from src (zip dict) into dest (zip dict, modified in place).

    Handles:
      - Slide XML + rels
      - Chart XML files (renamed to avoid collision)
      - Chart rels (with updated embedding refs)
      - Embedding .xlsx files (renamed)
      - Media/image files (renamed)
      - presentation.xml sldIdLst + rels
      - [Content_Types].xml overrides
    """
    dest_slide_n  = count_pat(dest, r"ppt/slides/slide\d+\.xml$")
    dest_chart_n  = count_pat(dest, r"ppt/charts/chart\d+\.xml$")
    dest_embed_n  = count_pat(dest, r"ppt/embeddings/.*\.xlsx$")
    dest_media_n  = count_pat(dest, r"ppt/media/image\d+\.")

    new_slide_num = dest_slide_n + 1
    chart_offset  = dest_chart_n
    embed_offset  = dest_embed_n
    media_offset  = dest_media_n

    src_slide_xml  = src.get(f"ppt/slides/slide{src_slide_num}.xml")
    src_slide_rels = src.get(f"ppt/slides/_rels/slide{src_slide_num}.xml.rels")

    if not src_slide_xml:
        print(f"  [skip] slide{src_slide_num}.xml not found in source")
        return

    # ── build remapping tables ─────────────────────────────────────────────────
    # chart_remap[old_abs_or_rel_target] = new_abs_target  (/ppt/charts/chartN.xml)
    chart_remap = {}
    # media_remap[old_media_filename]    = new_media_filename  (image N.png)
    media_remap = {}

    if src_slide_rels:
        rels_tree = xparse(src_slide_rels)
        for rel in rels_tree.findall(f"{{{RELS_NS}}}Relationship"):
            target = rel.get("Target", "")
            rtype  = rel.get("Type",   "")

            # ── chart ──────────────────────────────────────────────────────────
            if "chart" in rtype.lower():
                # Normalize to absolute file key: ppt/charts/chartX.xml
                if target.startswith("/"):
                    old_file = target.lstrip("/")          # ppt/charts/chart1.xml
                    old_abs  = target                      # /ppt/charts/chart1.xml
                else:
                    # relative like ../charts/chart1.xml
                    old_file = "ppt/charts/" + target.split("/")[-1]
                    old_abs  = "/" + old_file

                if old_abs not in chart_remap:
                    chart_offset += 1
                    new_abs  = f"/ppt/charts/chart{chart_offset}.xml"
                    new_file = new_abs.lstrip("/")
                    chart_remap[old_abs]    = new_abs
                    chart_remap[target]     = new_abs   # also map the original target string

                    # Copy chart XML
                    chart_data = src.get(old_file)
                    if chart_data:
                        dest[new_file] = chart_data

                    # Process chart rels (embeddings)
                    old_crels_key = old_file.replace("ppt/charts/", "ppt/charts/_rels/") + ".rels"
                    crels_data = src.get(old_crels_key)
                    if crels_data:
                        crels = xparse(crels_data)
                        for crel in crels.findall(f"{{{RELS_NS}}}Relationship"):
                            ctarget = crel.get("Target", "")
                            if ".xlsx" in ctarget or "embeddings" in ctarget:
                                old_embed_file = "ppt/embeddings/" + ctarget.split("/")[-1]
                                embed_data = src.get(old_embed_file)
                                if embed_data:
                                    embed_offset += 1
                                    new_embed_name = f"Microsoft_Excel_Worksheet{embed_offset}.xlsx"
                                    new_embed_rel  = f"../embeddings/{new_embed_name}"
                                    dest[f"ppt/embeddings/{new_embed_name}"] = embed_data
                                    crel.set("Target", new_embed_rel)
                        new_crels_key = f"ppt/charts/_rels/chart{chart_offset}.xml.rels"
                        dest[new_crels_key] = xbytes(crels)

            # ── media/image ───────────────────────────────────────────────────
            elif "../media/" in target or target.startswith("../media/"):
                fname = target.split("/")[-1]
                if fname not in media_remap:
                    media_offset += 1
                    ext      = Path(fname).suffix
                    new_name = f"image{media_offset}{ext}"
                    media_remap[fname] = new_name
                    media_data = src.get("ppt/media/" + fname)
                    if media_data:
                        dest[f"ppt/media/{new_name}"] = media_data

    # ── update slide rels ──────────────────────────────────────────────────────
    if src_slide_rels:
        rels_tree = xparse(src_slide_rels)
        for rel in rels_tree.findall(f"{{{RELS_NS}}}Relationship"):
            target = rel.get("Target", "")
            rtype  = rel.get("Type", "")
            if "chart" in rtype.lower():
                new_t = chart_remap.get(target) or chart_remap.get(
                    "/" + "ppt/charts/" + target.split("/")[-1])
                if new_t:
                    rel.set("Target", new_t)
            elif "../media/" in target:
                fname = target.split("/")[-1]
                if fname in media_remap:
                    rel.set("Target", f"../media/{media_remap[fname]}")
            elif "notesSlide" in rtype:
                rels_tree.remove(rel)    # don't copy notes across

        # Ensure a slideLayout rel exists
        has_layout = any("slideLayout" in r.get("Type", "")
                         for r in rels_tree.findall(f"{{{RELS_NS}}}Relationship"))
        if not has_layout:
            s1_rels = dest.get("ppt/slides/_rels/slide1.xml.rels")
            if s1_rels:
                for r in xparse(s1_rels).findall(f"{{{RELS_NS}}}Relationship"):
                    if "slideLayout" in r.get("Type", ""):
                        rels_tree.append(copy.deepcopy(r))
                        break

        new_rels_bytes = xbytes(rels_tree)
    else:
        new_rels_bytes = (
            b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            b'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            b'<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout"'
            b' Target="../slideLayouts/slideLayout1.xml"/>'
            b"</Relationships>"
        )

    dest[f"ppt/slides/slide{new_slide_num}.xml"]          = src_slide_xml
    dest[f"ppt/slides/_rels/slide{new_slide_num}.xml.rels"] = new_rels_bytes

    # ── presentation.xml ──────────────────────────────────────────────────────
    pres  = xparse(dest["ppt/presentation.xml"])
    sldIdLst = pres.find(f".//{{{PRES_NS}}}sldIdLst")
    max_id = max(
        (int(el.get("id", 255)) for el in sldIdLst.findall(f"{{{PRES_NS}}}sldId")),
        default=255
    )

    pres_rels  = xparse(dest["ppt/_rels/presentation.xml.rels"])
    used_rids  = {r.get("Id", "") for r in pres_rels.findall(f"{{{RELS_NS}}}Relationship")}
    new_rid    = f"rId_s{new_slide_num}"
    i = 2
    while new_rid in used_rids:
        new_rid = f"rId_s{new_slide_num}_{i}"; i += 1

    new_sld = etree.SubElement(sldIdLst, f"{{{PRES_NS}}}sldId")
    new_sld.set("id", str(max_id + 1))
    new_sld.set(f"{{{R_NS}}}id", new_rid)
    dest["ppt/presentation.xml"] = xbytes(pres)

    # ── presentation.xml.rels ─────────────────────────────────────────────────
    new_rel = etree.SubElement(pres_rels, f"{{{RELS_NS}}}Relationship")
    new_rel.set("Id",     new_rid)
    new_rel.set("Type",   SLIDE_REL_TYPE)
    new_rel.set("Target", f"slides/slide{new_slide_num}.xml")
    dest["ppt/_rels/presentation.xml.rels"] = xbytes(pres_rels)

    # ── [Content_Types].xml ───────────────────────────────────────────────────
    ct = xparse(dest["[Content_Types].xml"])

    def has_override(part):
        return any(e.get("PartName") == part
                   for e in ct.findall(f"{{{CT_NS}}}Override"))

    for part, ctype in [
        (f"/ppt/slides/slide{new_slide_num}.xml", SLIDE_CT),
    ] + [
        (f"/{n}", CHART_CT)
        for n in dest
        if re.match(r"ppt/charts/chart\d+\.xml$", n) and not has_override(f"/{n}")
    ]:
        if not has_override(part):
            ov = etree.SubElement(ct, f"{{{CT_NS}}}Override")
            ov.set("PartName",    part)
            ov.set("ContentType", ctype)

    dest["[Content_Types].xml"] = xbytes(ct)

    added_charts = chart_offset  - dest_chart_n
    added_embeds = embed_offset  - dest_embed_n
    added_media  = media_offset  - dest_media_n
    print(f"  -> slide{new_slide_num}.xml  "
          f"charts+{added_charts}  embeds+{added_embeds}  media+{added_media}")


def merge(source_files, output_path):
    print(f"Base  : {source_files[0]}")
    dest = read_zip(source_files[0])

    for src_path in source_files[1:]:
        print(f"Adding: {src_path}")
        add_slide(dest, read_zip(src_path))

    write_zip(output_path, dest)
    n_slides = count_pat(dest, r"ppt/slides/slide\d+\.xml$")
    size_kb   = sum(len(v) for v in dest.values() if isinstance(v, bytes)) // 1024
    print(f"\nWritten: {output_path}  ({n_slides} slides, ~{size_kb}KB)")


# ── CLI ────────────────────────────────────────────────────────────────────────

def find_slide_files(slides_dir):
    pattern = os.path.join(slides_dir, "slide_*", "output.pptx")
    return sorted(glob.glob(pattern))


def main():
    parser = argparse.ArgumentParser(
        description="Merge PPTX slides (ZIP-level, chart-safe)")
    parser.add_argument("files", nargs="*",
                        help="Explicit .pptx list (optional)")
    parser.add_argument("--slides-dir", default="./tmp",
                        help="Directory containing slide_NN/ subdirs")
    parser.add_argument("--out", default="./final.pptx",
                        help="Output file path")
    parser.add_argument("--no-strict", action="store_true",
                        help="Skip empty-slide rejection")
    args = parser.parse_args()

    source_files = args.files if args.files else find_slide_files(args.slides_dir)
    if not source_files:
        print(f"[ERROR] No slide files found in {args.slides_dir}")
        sys.exit(1)

    print(f"Found {len(source_files)} file(s):")
    for f in source_files:
        n, s = inspect_pptx(f)
        print(f"  {f}  ({n} slide, {s} shapes, {os.path.getsize(f)//1024}KB)")

    if not args.no_strict:
        for f in source_files:
            n, s = inspect_pptx(f)
            if isinstance(s, int) and s == 0:
                print(f"[ERROR] {f} has 0 shapes — run gen.js first or use --no-strict")
                sys.exit(1)

    print()
    merge(source_files, args.out)

    n, s = inspect_pptx(args.out)
    print(f"Verified: {n} slides, {s} shapes total")


if __name__ == "__main__":
    main()
