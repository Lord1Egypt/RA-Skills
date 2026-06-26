"""
transition_builder.py — Slide transition injection via lxml.

python-pptx has no transition API; we inject OOXML directly.

Reference: ECMA-376 §19.3.1.50 (p:transition)
SO workaround: https://stackoverflow.com/questions/73901095/
"""

from lxml import etree
from pptx.oxml.ns import qn

TRANSITION_MAP = {
    "fade": "fade",
    "push": "push",
    "wipe": "wipe",
    "split": "split",
    "blinds": "blinds",
    "checker": "checker",
    "circle": "circle",
    "dissolve": "dissolve",
    "comb": "comb",
    "cover": "cover",
    "cut": "cut",
    "diamond": "diamond",
    "plus": "plus",
    "random": "random",
    "strips": "strips",
    "wedge": "wedge",
    "wheel": "wheel",
    "zoom": "zoom",
}


def apply_transition(slide, transition_type="fade", duration_ms=700, advance_ms=None):
    """Inject a slide transition into the slide XML.

    transition_type: one of the keys in TRANSITION_MAP
    duration_ms: transition animation duration in milliseconds
    advance_ms: auto-advance after N ms (None = click to advance)
    """
    slide_elem = slide._element

    for existing in slide_elem.findall(qn("p:transition")):
        slide_elem.remove(existing)

    ooxml_type = TRANSITION_MAP.get(transition_type, "fade")

    trans_attribs = {"spd": "med"}
    if duration_ms <= 300:
        trans_attribs["spd"] = "fast"
    elif duration_ms >= 1500:
        trans_attribs["spd"] = "slow"

    if advance_ms is not None:
        trans_attribs["advTm"] = str(advance_ms)

    transition = etree.SubElement(slide_elem, qn("p:transition"), attrib=trans_attribs)

    if ooxml_type == "fade":
        etree.SubElement(transition, qn("p:fade"))
    elif ooxml_type == "push":
        etree.SubElement(transition, qn("p:push"))
    elif ooxml_type == "wipe":
        etree.SubElement(transition, qn("p:wipe"))
    elif ooxml_type == "dissolve":
        etree.SubElement(transition, qn("p:dissolve"))
    elif ooxml_type == "split":
        etree.SubElement(transition, qn("p:split"))
    elif ooxml_type == "blinds":
        etree.SubElement(transition, qn("p:blinds"))
    elif ooxml_type == "checker":
        etree.SubElement(transition, qn("p:checker"))
    elif ooxml_type == "comb":
        etree.SubElement(transition, qn("p:comb"))
    elif ooxml_type == "cover":
        etree.SubElement(transition, qn("p:cover"))
    elif ooxml_type == "cut":
        etree.SubElement(transition, qn("p:cut"))
    elif ooxml_type == "random":
        etree.SubElement(transition, qn("p:random"))
    else:
        etree.SubElement(transition, qn("p:fade"))


def apply_transitions_to_presentation(prs, transition_spec=None):
    """Apply transitions to all slides in a presentation.

    transition_spec: dict with optional keys:
      {
        "type": "fade",
        "duration": 700,
        "advanceAfter": null,
        "perSlide": {0: {"type": "push"}, 2: {"type": "wipe"}}
      }
    """
    if transition_spec is None:
        transition_spec = {"type": "fade", "duration": 700}

    default_type = transition_spec.get("type", "fade")
    default_dur = transition_spec.get("duration", 700)
    default_adv = transition_spec.get("advanceAfter")
    per_slide = transition_spec.get("perSlide", {})

    for idx, slide in enumerate(prs.slides):
        slide_conf = per_slide.get(idx, per_slide.get(str(idx), {}))
        t_type = slide_conf.get("type", default_type)
        t_dur = slide_conf.get("duration", default_dur)
        t_adv = slide_conf.get("advanceAfter", default_adv)
        apply_transition(slide, t_type, t_dur, t_adv)
