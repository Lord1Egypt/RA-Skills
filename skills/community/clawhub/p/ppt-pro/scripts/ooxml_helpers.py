"""
ooxml_helpers.py — Low-level OOXML/lxml helpers for PPTX assembly.

Provides functions for direct XML manipulation of text run properties,
gradient fills, shadows, outlines, and theme injection. Isolated from
the main assembly logic for maintainability.

References:
  ECMA-376 Part 1 (Office Open XML): §20.1 DrawingML, §21.1 PresentationML
  python-pptx docs: https://python-pptx.readthedocs.io/
"""

import math

from lxml import etree
from pptx.oxml.ns import qn

RPR_CHILD_ORDER = [
    "ln",
    "noFill", "solidFill", "gradFill", "blipFill", "pattFill", "grpFill",
    "effectLst", "effectDag",
    "highlight",
    "uLnTx", "uLn",
    "uFillTx", "uFill",
    "latin", "ea", "cs", "sym",
    "hlinkClick", "hlinkMouseOver",
    "rtl",
    "extLst",
]


def insert_rPr_child(rPr, new_elem):
    """Insert child element into a:rPr at the correct schema position.
    Reference: ECMA-376 §21.1.2.3.9 (a:rPr child sequence)."""
    new_local = etree.QName(new_elem).localname
    try:
        new_idx = RPR_CHILD_ORDER.index(new_local)
    except ValueError:
        rPr.append(new_elem)
        return
    for i, existing in enumerate(rPr):
        existing_local = etree.QName(existing).localname
        try:
            existing_idx = RPR_CHILD_ORDER.index(existing_local)
        except ValueError:
            continue
        if existing_idx > new_idx:
            rPr.insert(i, new_elem)
            return
    rPr.append(new_elem)


def _clear_fill_children(rPr):
    """Remove all fill-related children from a:rPr."""
    for child in list(rPr):
        local = etree.QName(child).localname
        if local in ("solidFill", "gradFill", "noFill", "blipFill", "pattFill", "grpFill"):
            rPr.remove(child)


def set_run_color(run_element, hex_color, alpha=None):
    """Set solidFill color on a:rPr via lxml.

    alpha: float 0.0-1.0 opacity, or None for fully opaque.
    OOXML uses val 0-100000. Reference: ECMA-376 §20.1.2.3.1 (a:alpha).
    """
    rPr = run_element.get_or_add_rPr()
    _clear_fill_children(rPr)

    if not hex_color or len(hex_color) < 6:
        hex_color = "333333"

    sf = etree.Element(qn("a:solidFill"))
    clr_el = etree.SubElement(sf, qn("a:srgbClr"), attrib={"val": hex_color[:6].upper()})
    if alpha is not None and alpha < 0.999:
        alpha_val = max(0, min(100000, int(round(alpha * 100000))))
        etree.SubElement(clr_el, qn("a:alpha"), attrib={"val": str(alpha_val)})
    insert_rPr_child(rPr, sf)


def set_font_typefaces(run_element, font_family):
    """Set a:latin, a:ea, a:cs typeface for cross-platform font fallback.
    Reference: ECMA-376 §21.1.2.3.7 (a:latin), §21.1.2.3.3 (a:ea)."""
    rPr = run_element.get_or_add_rPr()
    for tag in ("latin", "ea", "cs"):
        existing = rPr.find(qn(f"a:{tag}"))
        if existing is not None:
            rPr.remove(existing)
    for tag in ("latin", "ea", "cs"):
        el = etree.Element(qn(f"a:{tag}"))
        el.set("typeface", font_family)
        insert_rPr_child(rPr, el)


def set_letter_spacing(run_element, spacing_em, font_size_pt):
    """Set spc attribute on a:rPr for letter-spacing.
    Unit: hundredths of a point. Reference: ECMA-376 §21.1.2.3.9."""
    if abs(spacing_em) < 0.001:
        return
    spc_val = int(round(spacing_em * font_size_pt * 100))
    if spc_val == 0:
        return
    rPr = run_element.get_or_add_rPr()
    rPr.set("spc", str(spc_val))


def apply_gradient_fill(run_element, gradient_info):
    """Inject OOXML a:gradFill for native gradient text.
    Reference: ECMA-376 §20.1.8.33 (gradFill)."""
    stops = gradient_info.get("stops", [])
    if len(stops) < 2:
        return

    rPr = run_element.get_or_add_rPr()
    _clear_fill_children(rPr)

    grad_fill = etree.Element(qn("a:gradFill"))
    gs_lst = etree.SubElement(grad_fill, qn("a:gsLst"))
    for stop in stops:
        pos = str(stop.get("pos", 0))
        color = stop.get("color", "000000")
        gs = etree.SubElement(gs_lst, qn("a:gs"), attrib={"pos": pos})
        etree.SubElement(gs, qn("a:srgbClr"), attrib={"val": color})

    angle_deg = gradient_info.get("angleDeg", 180)
    angle_ooxml = int(angle_deg * 60000)
    etree.SubElement(grad_fill, qn("a:lin"), attrib={"ang": str(angle_ooxml), "scaled": "1"})
    insert_rPr_child(rPr, grad_fill)


def apply_text_shadow(run_element, shadow_info, px_to_emu_factor):
    """Inject a:outerShdw for text shadow. Reference: ECMA-376 §20.1.8.45."""
    rPr = run_element.get_or_add_rPr()
    for child in list(rPr):
        if etree.QName(child).localname in ("effectLst", "effectDag"):
            rPr.remove(child)

    ox, oy = shadow_info["offsetX"], shadow_info["offsetY"]
    dist_px = math.sqrt(ox * ox + oy * oy)
    dist_emu = int(round(dist_px * px_to_emu_factor))
    angle_deg = math.degrees(math.atan2(oy, ox)) if dist_px > 0 else 0
    if angle_deg < 0:
        angle_deg += 360

    blur_emu = int(round(shadow_info["blurPx"] * px_to_emu_factor))
    eff_lst = etree.Element(qn("a:effectLst"))
    outer = etree.SubElement(eff_lst, qn("a:outerShdw"), attrib={
        "blurRad": str(blur_emu), "dist": str(dist_emu),
        "dir": str(int(round(angle_deg * 60000))),
        "algn": "ctr", "rotWithShape": "0",
    })
    clr = etree.SubElement(outer, qn("a:srgbClr"), attrib={"val": shadow_info["color"]})
    alpha_val = shadow_info.get("alpha", 100000)
    if alpha_val < 100000:
        etree.SubElement(clr, qn("a:alpha"), attrib={"val": str(alpha_val)})
    insert_rPr_child(rPr, eff_lst)


def apply_text_outline(run_element, outline_info):
    """Inject a:ln for text outline/stroke."""
    rPr = run_element.get_or_add_rPr()
    for child in list(rPr):
        if etree.QName(child).localname == "ln":
            rPr.remove(child)
    width_emu = int(round(outline_info["widthPx"] * 9525))
    ln = etree.Element(qn("a:ln"))
    ln.set("w", str(width_emu))
    sf = etree.SubElement(ln, qn("a:solidFill"))
    etree.SubElement(sf, qn("a:srgbClr"), attrib={"val": outline_info["color"]})
    insert_rPr_child(rPr, ln)


EFFECT_LST_ORDER = [
    "blur", "fillOverlay", "glow", "innerShdw",
    "outerShdw", "prstShdw", "reflection", "softEdge",
]


def _insert_effect_child(eff_lst, new_elem):
    """Insert child into effectLst at correct schema position.

    Reference: ECMA-376 §20.1.8.26 — effectLst child sequence.
    """
    new_local = etree.QName(new_elem).localname
    try:
        new_idx = EFFECT_LST_ORDER.index(new_local)
    except ValueError:
        eff_lst.append(new_elem)
        return
    for i, existing in enumerate(eff_lst):
        existing_local = etree.QName(existing).localname
        try:
            existing_idx = EFFECT_LST_ORDER.index(existing_local)
        except ValueError:
            continue
        if existing_idx > new_idx:
            eff_lst.insert(i, new_elem)
            return
    eff_lst.append(new_elem)


def apply_text_glow(run_element, glow_info, px_to_emu_factor):
    """Inject a:glow into effectLst. Reference: ECMA-376 §20.1.8.32."""
    rPr = run_element.get_or_add_rPr()
    eff_lst = rPr.find(qn("a:effectLst"))
    if eff_lst is None:
        eff_lst = etree.Element(qn("a:effectLst"))
        insert_rPr_child(rPr, eff_lst)
    for child in list(eff_lst):
        if etree.QName(child).localname == "glow":
            eff_lst.remove(child)
    rad_emu = int(round(glow_info.get("radiusPx", 4) * px_to_emu_factor))
    glow = etree.Element(qn("a:glow"), attrib={"rad": str(rad_emu)})
    clr = etree.SubElement(glow, qn("a:srgbClr"), attrib={"val": glow_info["color"]})
    alpha_val = glow_info.get("alpha", 60000)
    if alpha_val < 100000:
        etree.SubElement(clr, qn("a:alpha"), attrib={"val": str(alpha_val)})
    _insert_effect_child(eff_lst, glow)
