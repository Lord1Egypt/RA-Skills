#!/usr/bin/env python3
"""Shared Word paragraph text surface helpers.

This module defines a single visible-text projection for paragraph anchoring and
comment injection so offset calculations and XML mutations use the same model.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import List, Optional, Tuple

from lxml import etree

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XML_SPACE = "{http://www.w3.org/XML/1998/namespace}space"


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _ancestor_run(node: etree._Element) -> Optional[etree._Element]:
    current = node
    while current is not None:
        if _local_name(current.tag) == "r":
            return current
        current = current.getparent()
    return None


def _symbol_text(node: etree._Element) -> str:
    raw = node.get(f"{{{W_NS}}}char") or node.get("char") or ""
    if not raw:
        return ""
    try:
        return chr(int(raw, 16))
    except Exception:
        return ""


def node_visible_text(node: etree._Element) -> str:
    tag = _local_name(node.tag)
    if tag == "t":
        return node.text or ""
    if tag == "tab":
        return "\t"
    if tag in {"br", "cr"}:
        return "\n"
    if tag == "noBreakHyphen":
        return "-"
    if tag == "softHyphen":
        return "\u00ad"
    if tag == "sym":
        return _symbol_text(node)
    return ""


@dataclass(frozen=True)
class SurfaceChar:
    run: etree._Element
    node: etree._Element
    char: str
    node_char_index: int


@dataclass(frozen=True)
class ParagraphTextSurface:
    text: str
    chars: List[SurfaceChar]


def build_paragraph_text_surface(paragraph: etree._Element) -> ParagraphTextSurface:
    chars: List[SurfaceChar] = []
    pieces: List[str] = []
    for node in paragraph.iter():
        text = node_visible_text(node)
        if not text:
            continue
        run = _ancestor_run(node)
        if run is None:
            continue
        pieces.append(text)
        for idx, ch in enumerate(text):
            chars.append(SurfaceChar(run=run, node=node, char=ch, node_char_index=idx))
    return ParagraphTextSurface(text="".join(pieces), chars=chars)


def get_paragraph_visible_text(paragraph: etree._Element) -> str:
    return build_paragraph_text_surface(paragraph).text


def get_run_visible_text(run: etree._Element) -> str:
    pieces: List[str] = []
    for child in run:
        if _local_name(child.tag) == "rPr":
            continue
        pieces.append(node_visible_text(child))
    return "".join(pieces)


def _clone_text_like_node(node: etree._Element, text: str) -> etree._Element:
    cloned = deepcopy(node)
    cloned.text = text
    if text.startswith(" ") or text.endswith(" "):
        cloned.set(XML_SPACE, "preserve")
    else:
        cloned.attrib.pop(XML_SPACE, None)
    return cloned


def _clone_run_with_children(run: etree._Element, children: List[etree._Element]) -> Optional[etree._Element]:
    if not children:
        return None
    cloned = etree.Element(run.tag, nsmap=run.nsmap)
    for key, value in run.attrib.items():
        cloned.set(key, value)
    for child in run:
        if _local_name(child.tag) == "rPr":
            cloned.append(deepcopy(child))
            break
    for child in children:
        cloned.append(deepcopy(child))
    return cloned


def split_run_at_surface_position(
    run: etree._Element,
    node: etree._Element,
    node_char_index: int,
    *,
    after: bool,
) -> Tuple[Optional[etree._Element], Optional[etree._Element]]:
    """Split a run at a visible-text boundary while preserving non-text children."""

    content_children = [child for child in run if _local_name(child.tag) != "rPr"]
    left_children: List[etree._Element] = []
    right_children: List[etree._Element] = []
    located = False

    for child in content_children:
        if child is not node:
            if located:
                right_children.append(child)
            else:
                left_children.append(child)
            continue

        located = True
        child_text = node_visible_text(child)
        tag = _local_name(child.tag)

        if tag in {"t", "delText", "instrText"}:
            split_offset = node_char_index + 1 if after else node_char_index
            if split_offset <= 0:
                right_children.append(child)
            elif split_offset >= len(child_text):
                left_children.append(child)
            else:
                left_children.append(_clone_text_like_node(child, child_text[:split_offset]))
                right_children.append(_clone_text_like_node(child, child_text[split_offset:]))
        else:
            if after:
                left_children.append(child)
            else:
                right_children.append(child)

    if not located:
        raise ValueError("target node not found in run when splitting visible surface")

    parent = run.getparent()
    if parent is None:
        return None, None
    insert_at = parent.index(run)
    left_run = _clone_run_with_children(run, left_children)
    right_run = _clone_run_with_children(run, right_children)
    parent.remove(run)
    offset = 0
    if left_run is not None:
        parent.insert(insert_at, left_run)
        offset = 1
    if right_run is not None:
        parent.insert(insert_at + offset, right_run)
    return left_run, right_run
