#!/usr/bin/env python3
"""
GHX Generator — Generate Rhino 7 Grasshopper (.ghx) XML files.

Creates valid .ghx files with native components, GhPython scripts, sliders,
and wiring. All component GUIDs are authentic, extracted from real Grasshopper
installations.

Usage:
    from ghx_generator import GHXGenerator

    gen = GHXGenerator("My Definition", "Optional description")

    # Add sliders for user-adjustable parameters
    radius = gen.add_slider("Radius", 20, 1, 100, x=50, y=50)

    # Add native components (resolved from GUID database)
    circle = gen.add_component("Circle", inputs=["Base Plane", "Radius"],
                               outputs=["Circle"], x=300, y=50)

    # Wire them together
    gen.connect(radius, "output", circle, "Radius")

    # Save
    gen.save("output.ghx")

CLI:
    python ghx_generator.py                    # Generate demo cylinder
    python ghx_generator.py -o my_file.ghx     # Custom output path
    python ghx_generator.py --list             # List known components
    python ghx_generator.py --validate file.ghx  # Validate a .ghx file
"""

from __future__ import annotations

import json
import os
import sys
import uuid
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import Optional

# ---------------------------------------------------------------------------
# GHX XML type codes
# ---------------------------------------------------------------------------
TC_BOOL = 1
TC_INT32 = 3
TC_SINGLE = 5
TC_DOUBLE = 6
TC_DATE = 8
TC_GUID = 9
TC_STRING = 10
TC_POINT = 30
TC_POINTF = 31
TC_RECTF = 35
TC_COLOR = 36
TC_VERSION = 80

# ---------------------------------------------------------------------------
# XML helpers
# ---------------------------------------------------------------------------

def _new_guid() -> str:
    """Generate a new random GUID string."""
    return str(uuid.uuid4())


def _item(name: str, value, type_name: str = "gh_string",
          type_code: int = TC_STRING, index: Optional[int] = None) -> ET.Element:
    """Create an XML <item> element."""
    attrs = {"name": name, "type_name": type_name, "type_code": str(type_code)}
    if index is not None:
        attrs["index"] = str(index)
    el = ET.Element("item", attrs)
    if value is not None:
        el.text = str(value)
    return el


def _rect(x, y, w, h) -> ET.Element:
    """Create a Bounds rectangle <item>."""
    el = _item("Bounds", None, "gh_drawing_rectanglef", TC_RECTF)
    for tag, val in [("X", x), ("Y", y), ("W", w), ("H", h)]:
        sub = ET.SubElement(el, tag)
        sub.text = str(val)
    return el


def _pivot(x, y) -> ET.Element:
    """Create a Pivot point <item>."""
    el = _item("Pivot", None, "gh_drawing_pointf", TC_POINTF)
    for tag, val in [("X", x), ("Y", y)]:
        sub = ET.SubElement(el, tag)
        sub.text = str(round(val, 2))
    return el


def _chunk(name: str, index: Optional[int] = None) -> ET.Element:
    """Create a <chunk> element."""
    attrs = {"name": name}
    if index is not None:
        attrs["index"] = str(index)
    return ET.Element("chunk", attrs)


def _wrap_items(items: list[ET.Element]) -> ET.Element:
    """Wrap items in <items count=N>."""
    el = ET.Element("items", {"count": str(len(items))})
    for item in items:
        el.append(item)
    return el


def _wrap_chunks(chunks: list[ET.Element]) -> ET.Element:
    """Wrap chunks in <chunks count=N>."""
    el = ET.Element("chunks", {"count": str(len(chunks))})
    for chunk in chunks:
        el.append(chunk)
    return el


# ---------------------------------------------------------------------------
# Component reference (returned by add_* methods for wiring)
# ---------------------------------------------------------------------------

class ComponentRef:
    """Reference to a placed component, used for wiring via connect()."""

    def __init__(self, instance_guid: str, name: str,
                 input_guids: Optional[dict[str, str]] = None,
                 output_guids: Optional[dict[str, str]] = None):
        self.instance_guid = instance_guid
        self.name = name
        self.input_guids = input_guids or {}    # param_name → InstanceGuid
        self.output_guids = output_guids or {}   # param_name → InstanceGuid

    def __repr__(self):
        return f"ComponentRef({self.name!r}, guid={self.instance_guid[:8]}…)"


# ---------------------------------------------------------------------------
# Main generator class
# ---------------------------------------------------------------------------

class GHXGenerator:
    """Generate Grasshopper .ghx (XML) files.

    Loads component GUIDs from references/component_guids.json automatically.
    """

    _guid_db: dict[str, str] = {}
    _guids_loaded: bool = False

    @classmethod
    def _load_guids(cls):
        if cls._guids_loaded:
            return
        guids_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "references", "component_guids.json"
        )
        if os.path.exists(guids_path):
            with open(guids_path, encoding="utf-8") as f:
                data = json.load(f)
            for _cat, comps in data.get("components", {}).items():
                for name, guid in comps.items():
                    cls._guid_db[name] = guid
        cls._guids_loaded = True

    def __init__(self, name: str = "Untitled", description: str = ""):
        self._load_guids()
        self.name = name
        self.description = description
        self.objects: list[tuple[ET.Element, ComponentRef]] = []
        self._doc_id = _new_guid()
        self._auto_x = 100

    def _resolve_guid(self, component_name: str) -> Optional[str]:
        """Look up authentic ComponentGuid from database."""
        if component_name in self._guid_db:
            return self._guid_db[component_name]
        lower = component_name.lower()
        for k, v in self._guid_db.items():
            if k.lower() == lower:
                return v
        return None

    # -----------------------------------------------------------------------
    # Public API: add components
    # -----------------------------------------------------------------------

    def add_slider(self, nickname: str, value: float, min_val: float = 0,
                   max_val: float = 100, digits: int = 3,
                   x: Optional[float] = None, y: Optional[float] = None) -> ComponentRef:
        """Add a Number Slider component."""
        if x is None:
            x = self._auto_x
            self._auto_x += 250
        if y is None:
            y = 50

        instance_guid = _new_guid()
        comp_guid = self._resolve_guid("Number Slider") or _new_guid()

        obj = _chunk("Object")
        obj.append(_wrap_items([
            _item("GUID", comp_guid, "gh_guid", TC_GUID),
            _item("Name", "Number Slider", "gh_string", TC_STRING),
        ]))

        container = _chunk("Container")
        container.append(_wrap_items([
            _item("Description", "Numeric slider for single values", "gh_string", TC_STRING),
            _item("InstanceGuid", instance_guid, "gh_guid", TC_GUID),
            _item("Name", "Number Slider", "gh_string", TC_STRING),
            _item("NickName", nickname, "gh_string", TC_STRING),
            _item("Optional", "false", "gh_bool", TC_BOOL),
            _item("SourceCount", "0", "gh_int32", TC_INT32),
        ]))

        attrs = _chunk("Attributes")
        attrs.append(_wrap_items([_rect(x, y, 200, 20), _pivot(x, y + 10)]))

        slider = _chunk("Slider")
        slider.append(_wrap_items([
            _item("Digits", digits, "gh_int32", TC_INT32),
            _item("GripDisplay", "1", "gh_int32", TC_INT32),
            _item("Interval", "1", "gh_int32", TC_INT32),
            _item("Max", max_val, "gh_double", TC_DOUBLE),
            _item("Min", min_val, "gh_double", TC_DOUBLE),
            _item("SnapCount", "0", "gh_int32", TC_INT32),
            _item("Value", value, "gh_double", TC_DOUBLE),
        ]))

        container.append(_wrap_chunks([attrs, slider]))
        obj.append(_wrap_chunks([container]))

        ref = ComponentRef(instance_guid, nickname,
                           output_guids={"output": instance_guid})
        self.objects.append((obj, ref))
        return ref

    def add_component(self, name: str, nickname: Optional[str] = None,
                      x: Optional[float] = None, y: Optional[float] = None,
                      inputs: Optional[list[str]] = None,
                      outputs: Optional[list[str]] = None) -> ComponentRef:
        """Add a standard Grasshopper component by name.

        Name is resolved to an authentic GUID from the database.
        Falls back to a random GUID if not found (will cause a warning in Rhino).
        """
        nickname = nickname or name
        if x is None:
            x = self._auto_x
            self._auto_x += 200
        if y is None:
            y = 50

        instance_guid = _new_guid()
        comp_guid = self._resolve_guid(name) or _new_guid()

        obj = _chunk("Object")
        obj.append(_wrap_items([
            _item("GUID", comp_guid, "gh_guid", TC_GUID),
            _item("Name", name, "gh_string", TC_STRING),
        ]))

        container = _chunk("Container")
        container.append(_wrap_items([
            _item("Description", "", "gh_string", TC_STRING),
            _item("InstanceGuid", instance_guid, "gh_guid", TC_GUID),
            _item("Name", name, "gh_string", TC_STRING),
            _item("NickName", nickname, "gh_string", TC_STRING),
        ]))

        sub_chunks: list[ET.Element] = []

        # Attributes
        n_in = len(inputs) if inputs else 0
        n_out = len(outputs) if outputs else 0
        comp_h = max(44, 20 * (n_in + n_out) + 4)
        attrs = _chunk("Attributes")
        attrs.append(_wrap_items([
            _rect(x, y, 100, comp_h),
            _pivot(x + 50, y + comp_h / 2),
        ]))
        sub_chunks.append(attrs)

        # Input params
        input_guids: dict[str, str] = {}
        if inputs:
            for i, inp_name in enumerate(inputs):
                inp_guid = _new_guid()
                input_guids[inp_name] = inp_guid
                inp_chunk = _chunk("param_input", index=i)
                inp_chunk.append(_wrap_items([
                    _item("Description", "", "gh_string", TC_STRING),
                    _item("InstanceGuid", inp_guid, "gh_guid", TC_GUID),
                    _item("Name", inp_name, "gh_string", TC_STRING),
                    _item("NickName", inp_name, "gh_string", TC_STRING),
                    _item("Optional", "false", "gh_bool", TC_BOOL),
                    _item("SourceCount", "0", "gh_int32", TC_INT32),
                ]))
                inp_attrs = _chunk("Attributes")
                inp_attrs.append(_wrap_items([
                    _rect(x + 2, y + 2 + i * 20, 18, 20),
                    _pivot(x + 11, y + 12 + i * 20),
                ]))
                inp_chunk.append(_wrap_chunks([inp_attrs]))
                sub_chunks.append(inp_chunk)

        # Output params
        output_guids: dict[str, str] = {}
        if outputs:
            for i, out_name in enumerate(outputs):
                out_guid = _new_guid()
                output_guids[out_name] = out_guid
                out_chunk = _chunk("param_output", index=i)
                out_chunk.append(_wrap_items([
                    _item("Description", "", "gh_string", TC_STRING),
                    _item("InstanceGuid", out_guid, "gh_guid", TC_GUID),
                    _item("Name", out_name, "gh_string", TC_STRING),
                    _item("NickName", out_name, "gh_string", TC_STRING),
                    _item("Optional", "false", "gh_bool", TC_BOOL),
                    _item("SourceCount", "0", "gh_int32", TC_INT32),
                ]))
                out_attrs = _chunk("Attributes")
                out_attrs.append(_wrap_items([
                    _rect(x + 80, y + 2 + i * 20, 18, 20),
                    _pivot(x + 89, y + 12 + i * 20),
                ]))
                out_chunk.append(_wrap_chunks([out_attrs]))
                sub_chunks.append(out_chunk)

        container.append(_wrap_chunks(sub_chunks))
        obj.append(_wrap_chunks([container]))

        ref = ComponentRef(instance_guid, nickname, input_guids, output_guids)
        self.objects.append((obj, ref))
        return ref

    def add_python(self, nickname: str, code: str,
                   inputs: Optional[list[str]] = None,
                   outputs: Optional[list[str]] = None,
                   x: Optional[float] = None,
                   y: Optional[float] = None) -> ComponentRef:
        """Add a GhPython Script component with custom Python code.

        Code has access to input variables by name. Assign `a = result` for output.
        Full Rhino.Geometry API is available.
        """
        inputs = inputs or []
        outputs = outputs or []
        if x is None:
            x = self._auto_x
            self._auto_x += 200
        if y is None:
            y = 50

        instance_guid = _new_guid()
        comp_guid = self._resolve_guid("GhPython Script") or _new_guid()

        obj = _chunk("Object")
        obj.append(_wrap_items([
            _item("GUID", comp_guid, "gh_guid", TC_GUID),
            _item("Name", "GhPython Script", "gh_string", TC_STRING),
        ]))

        container = _chunk("Container")
        container.append(_wrap_items([
            _item("CodeInput", code, "gh_string", TC_STRING),
            _item("Description", "A Python script component", "gh_string", TC_STRING),
            _item("InstanceGuid", instance_guid, "gh_guid", TC_GUID),
            _item("Name", "GhPython Script", "gh_string", TC_STRING),
            _item("NickName", nickname, "gh_string", TC_STRING),
        ]))

        sub_chunks: list[ET.Element] = []

        # Attributes
        attrs = _chunk("Attributes")
        attrs.append(_wrap_items([_rect(x, y, 150, 80), _pivot(x + 75, y + 40)]))
        sub_chunks.append(attrs)

        # ParameterData (input/output IDs)
        param_data = _chunk("ParameterData")
        param_items = [_item("InputCount", len(inputs), "gh_int32", TC_INT32)]
        for _ in inputs:
            param_items.append(_item("InputId", _new_guid(), "gh_guid", TC_GUID))
        param_items.append(_item("OutputCount", len(outputs), "gh_int32", TC_INT32))
        for _ in outputs:
            param_items.append(_item("OutputId", _new_guid(), "gh_guid", TC_GUID))
        param_data.append(_wrap_items(param_items))
        sub_chunks.append(param_data)

        # Input params
        input_guids: dict[str, str] = {}
        for i, inp_name in enumerate(inputs):
            inp_guid = _new_guid()
            input_guids[inp_name] = inp_guid
            inp_chunk = _chunk("InputParam", index=i)
            inp_chunk.append(_wrap_items([
                _item("AllowTreeAccess", "true", "gh_bool", TC_BOOL),
                _item("Description", f"The {inp_name} script variable", "gh_string", TC_STRING),
                _item("InstanceGuid", inp_guid, "gh_guid", TC_GUID),
                _item("Name", inp_name, "gh_string", TC_STRING),
                _item("NickName", inp_name, "gh_string", TC_STRING),
                _item("Optional", "false", "gh_bool", TC_BOOL),
                _item("ScriptParamAccess", "0", "gh_int32", TC_INT32),
                _item("ShowTypeHints", "true", "gh_bool", TC_BOOL),
                _item("SourceCount", "0", "gh_int32", TC_INT32),
                _item("TypeHintID", "8d29ae0a-5e7d-4bdf-9e90-e2a3f5c8ced8", "gh_guid", TC_GUID),
            ]))
            inp_attrs = _chunk("Attributes")
            inp_attrs.append(_wrap_items([
                _rect(x + 2, y + 2 + i * 20, 18, 20),
                _pivot(x + 11, y + 12 + i * 20),
            ]))
            inp_chunk.append(_wrap_chunks([inp_attrs]))
            sub_chunks.append(inp_chunk)

        # Output params
        output_guids: dict[str, str] = {}
        for i, out_name in enumerate(outputs):
            out_guid = _new_guid()
            output_guids[out_name] = out_guid
            out_chunk = _chunk("OutputParam", index=i)
            out_chunk.append(_wrap_items([
                _item("Description", f"The {out_name} output variable", "gh_string", TC_STRING),
                _item("InstanceGuid", out_guid, "gh_guid", TC_GUID),
                _item("Name", out_name, "gh_string", TC_STRING),
                _item("NickName", out_name, "gh_string", TC_STRING),
                _item("Optional", "false", "gh_bool", TC_BOOL),
                _item("SourceCount", "0", "gh_int32", TC_INT32),
            ]))
            out_attrs = _chunk("Attributes")
            out_attrs.append(_wrap_items([
                _rect(x + 130, y + 2 + i * 20, 18, 20),
                _pivot(x + 139, y + 12 + i * 20),
            ]))
            out_chunk.append(_wrap_chunks([out_attrs]))
            sub_chunks.append(out_chunk)

        container.append(_wrap_chunks(sub_chunks))
        obj.append(_wrap_chunks([container]))

        ref = ComponentRef(instance_guid, nickname, input_guids, output_guids)
        self.objects.append((obj, ref))
        return ref

    # -----------------------------------------------------------------------
    # Public API: wiring
    # -----------------------------------------------------------------------

    def connect(self, source: ComponentRef, source_param: str,
                target: ComponentRef, target_param: str) -> None:
        """Wire source output to target input.

        For sliders, source_param is always "output".
        For components, use the output param name (e.g. "Circle", "Extrusion").
        """
        target_input_guid = target.input_guids.get(target_param)
        if not target_input_guid:
            available = list(target.input_guids.keys())
            raise ValueError(
                f"Input '{target_param}' not found on {target.name}. "
                f"Available inputs: {available}"
            )

        # Find the output GUID to use as source reference
        source_guid = source.output_guids.get(source_param)
        if not source_guid:
            raise ValueError(
                f"Output '{source_param}' not found on {source.name}. "
                f"Available outputs: {list(source.output_guids.keys())}"
            )

        # Find target object and update its param_input Source/SourceCount
        for obj_el, ref in self.objects:
            if ref.instance_guid == target.instance_guid:
                self._add_source(obj_el, target_input_guid, source_guid)
                return

        raise ValueError(f"Target component not found: {target.name}")

    def _add_source(self, obj_el: ET.Element, param_guid: str, source_guid: str):
        """Add a source reference to a parameter within an object XML tree."""
        parent_map = {child: parent for parent in obj_el.iter() for child in parent}

        for elem in obj_el.iter():
            if (elem.tag == "item" and elem.get("name") == "InstanceGuid"
                    and elem.text == param_guid):
                items_el = parent_map.get(elem)
                if items_el is None or items_el.tag != "items":
                    return

                source_count = 0
                source_items: list[ET.Element] = []
                for item in items_el.findall("item"):
                    if item.get("name") == "SourceCount":
                        source_count = int(item.text) + 1
                        item.text = str(source_count)
                    elif item.get("name") == "Source":
                        source_items.append(item)

                new_source = _item("Source", source_guid, "gh_guid", TC_GUID,
                                   index=len(source_items))
                items_el.append(new_source)
                items_el.set("count", str(len(items_el.findall("item"))))
                return

    # -----------------------------------------------------------------------
    # Public API: output
    # -----------------------------------------------------------------------

    def generate(self) -> ET.Element:
        """Build the complete .ghx XML tree."""
        root = ET.Element("Archive", {"name": "Root"})
        root.append(ET.Comment("Grasshopper archive"))
        root.append(ET.Comment("Generated by grasshopper-generator skill"))

        # Archive version
        ver = _item("ArchiveVersion", None, "gh_version", TC_VERSION)
        for tag, val in [("Major", "0"), ("Minor", "2"), ("Revision", "2")]:
            ET.SubElement(ver, tag).text = val
        root.append(_wrap_items([ver]))

        # Definition chunk
        definition = _chunk("Definition")
        pv = _item("plugin_version", None, "gh_version", TC_VERSION)
        for tag, val in [("Major", "1"), ("Minor", "0"), ("Revision", "7")]:
            ET.SubElement(pv, tag).text = val
        definition.append(_wrap_items([pv]))

        # Document header
        header = _chunk("DocumentHeader")
        header.append(_wrap_items([
            _item("DocumentID", self._doc_id, "gh_guid", TC_GUID),
            _item("Preview", "Shaded", "gh_string", TC_STRING),
            _item("PreviewMeshType", "1", "gh_int32", TC_INT32),
        ]))

        # Definition properties
        props = _chunk("DefinitionProperties")
        props.append(_wrap_items([
            _item("Description", self.description, "gh_string", TC_STRING),
            _item("Name", self.name, "gh_string", TC_STRING),
        ]))

        # Layout + Libraries
        rcp = _chunk("RcpLayout")
        rcp.append(_wrap_items([_item("GroupCount", "0", "gh_int32", TC_INT32)]))

        libs = _chunk("GHALibraries")
        libs.append(_wrap_items([_item("Count", "0", "gh_int32", TC_INT32)]))

        # Definition objects
        obj_chunks = []
        for i, (obj_el, _) in enumerate(self.objects):
            obj_el.set("index", str(i))
            obj_chunks.append(obj_el)

        def_objects = _chunk("DefinitionObjects")
        def_objects.append(_wrap_items([
            _item("ObjectCount", str(len(self.objects)), "gh_int32", TC_INT32),
        ]))
        if obj_chunks:
            def_objects.append(_wrap_chunks(obj_chunks))

        definition.append(_wrap_chunks([header, props, rcp, libs, def_objects]))
        root.append(_wrap_chunks([definition]))
        return root

    def to_xml_string(self) -> str:
        """Generate pretty-printed XML string."""
        tree = self.generate()
        rough = ET.tostring(tree, encoding="unicode", xml_declaration=False)
        dom = minidom.parseString(rough)
        lines = dom.toprettyxml(indent="  ", encoding=None).split("\n")
        return "\n".join(line for line in lines if line.strip())

    def save(self, path: str) -> str:
        """Save .ghx file to disk. Returns the path."""
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.to_xml_string())
        return path


# ---------------------------------------------------------------------------
# Validation utility
# ---------------------------------------------------------------------------

def validate_ghx(path: str) -> list[str]:
    """Validate a .ghx file structure. Returns list of error messages."""
    errors: list[str] = []
    try:
        tree = ET.parse(path)
    except ET.ParseError as e:
        return [f"XML parse error: {e}"]

    root = tree.getroot()
    if root.tag != "Archive":
        errors.append("Root element is not 'Archive'")

    # Check DefinitionObjects
    def_objs = root.find(".//chunk[@name='DefinitionObjects']")
    if def_objs is None:
        errors.append("Missing DefinitionObjects chunk")
        return errors

    # Collect all InstanceGuids
    all_instance_guids: set[str] = set()
    for item in root.iter("item"):
        if item.get("name") == "InstanceGuid" and item.text:
            all_instance_guids.add(item.text)

    # Check each Object
    obj_count = 0
    for chunk in root.iter("chunk"):
        if chunk.get("name") != "Object":
            continue
        obj_count += 1
        idx = chunk.get("index", "?")
        name_el = chunk.find("items/item[@name='Name']")
        obj_name = name_el.text if name_el is not None else "?"

        container = chunk.find("chunks/chunk[@name='Container']")
        if container is None:
            errors.append(f"Object[{idx}] ({obj_name}): missing Container chunk")
            continue

        # Check Container has items with InstanceGuid
        c_items = container.find("items")
        iguid = None
        if c_items is not None:
            for item in c_items.findall("item"):
                if item.get("name") == "InstanceGuid" and item.text:
                    iguid = item.text
                    break

        if iguid is None:
            errors.append(f"Object[{idx}] ({obj_name}): Container missing InstanceGuid")

    # Check Source references
    sources_missing = 0
    for item in root.iter("item"):
        if item.get("name") == "Source" and item.text:
            if item.text not in all_instance_guids:
                sources_missing += 1
                errors.append(f"Source ref {item.text} not found in any InstanceGuid")

    if not errors:
        print(f"✅ Valid: {obj_count} objects, {len(all_instance_guids)} GUIDs, all sources resolve")
    else:
        print(f"❌ {len(errors)} issue(s) found:")
        for e in errors:
            print(f"   • {e}")

    return errors


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _demo():
    """Generate a demo parametric cylinder."""
    gen = GHXGenerator("Parametric Cylinder", "Circle + Extrude demo")

    r = gen.add_slider("Radius", 20, 1, 100, x=50, y=50)
    h = gen.add_slider("Height", 50, 1, 200, x=50, y=100)
    circle = gen.add_component("Circle", inputs=["Base Plane", "Radius"],
                               outputs=["Circle"], x=300, y=50)
    unit_z = gen.add_component("Unit Z", outputs=["Unit Vector"], x=300, y=150)
    extrude = gen.add_component("Extrude", inputs=["Base", "Direction"],
                                outputs=["Extrusion"], x=500, y=50)

    gen.connect(r, "output", circle, "Radius")
    gen.connect(circle, "Circle", extrude, "Base")
    gen.connect(unit_z, "Unit Vector", extrude, "Direction")
    return gen


def _list_components():
    """Print all known components."""
    GHXGenerator._load_guids()
    db = GHXGenerator._guid_db
    cats: dict[str, list[str]] = {}
    for name in sorted(db):
        cats.setdefault("all", []).append(name)

    print(f"Known components: {len(db)}")
    for name in sorted(db):
        print(f"  {name}: {db[name]}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Grasshopper .ghx file generator")
    parser.add_argument("-o", "--output", default="/tmp/demo_cylinder.ghx",
                        help="Output .ghx path")
    parser.add_argument("--list", action="store_true",
                        help="List all known component names and GUIDs")
    parser.add_argument("--validate", metavar="FILE",
                        help="Validate a .ghx file")
    args = parser.parse_args()

    if args.list:
        _list_components()
        return

    if args.validate:
        errors = validate_ghx(args.validate)
        sys.exit(1 if errors else 0)

    gen = _demo()
    path = gen.save(args.output)
    print(f"Saved to {path}")
    print(f"Objects: {len(gen.objects)}")

    # Auto-validate
    validate_ghx(path)


if __name__ == "__main__":
    main()
