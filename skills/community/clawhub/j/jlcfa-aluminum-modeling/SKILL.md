---
name: jlcfa-aluminum-modeling
description: "Build and review JLCFA/JiaLiChuang FA aluminum alloy enclosure modeling attributes. Use when users mention 嘉立创, JLCFA, 铝合金外壳, 外壳设计器, 开孔, 螺孔, 沉头孔, 喷砂氧化, UV打印, 激光打标, 盖板加工, 壳身加工, or need AI/CAD attributes for manufacturable aluminum enclosure modeling."
license: MIT
---

# JLCFA Aluminum Modeling

Use this skill to turn enclosure requirements into structured modeling attributes and to check them against JLCFA aluminum alloy enclosure process limits.

## Usage Preview

![BBClaw aluminum enclosure design preview](https://raw.githubusercontent.com/zhoushoujianwork/jlcfa-aluminum-modeling-skill/main/jlcfa-aluminum-modeling/assets/bbclaw-usage-preview.png)

Example output from a BBClaw enclosure request: the skill reads a 3MF shell reference, turns the request into JLCFA-oriented design notes, structured JSON attributes, and a front-panel SVG preview.

## Source Rules

Before giving manufacturability advice, detailed dimensions, tolerances, materials, finishes, marking, or machining-process choices, read [references/jlcfa-standards.md](references/jlcfa-standards.md).

Treat the reference as a design aid transcribed from JLCFA public pages. For order-critical or high-cost production decisions, tell the user to verify the current values on the linked JLCFA pages.

## Workflow

1. Parse the user's enclosure intent into: base shell/profile, cover plates, faces, openings, screw/countersink holes, text/graphics, finish, machining process, tolerances, and export needs.
2. Keep dimensions in millimeters. State the coordinate frame you assume for each face, such as `front-panel origin at lower-left, +X right, +Y up`.
3. Prefer explicit, machine-readable attributes. If the user only gives natural language, infer conservative defaults and mark every assumption.
4. For built-in connector openings, map the user phrase to the standard-opening enum in the reference, and preserve the JLCFA Chinese label when the live designer label matters.
5. Check every feature against the JLCFA constraints in the reference: minimum cut width, opening-to-edge distance, rib reservations, available threaded holes, cover thickness, process choices, finish colors, and marking rules.
6. When a feature conflicts with constraints, propose the smallest practical adjustment and explain which rule drove it.
7. End with a compact "属性清单" plus a "待确认" list for missing dimensions, shell model/profile, quantity, color, surface quality, and production-critical tolerances.

## Attribute Shape

Use this shape unless the target CAD/tool has its own schema:

```json
{
  "project": {
    "name": "string",
    "vendor": "JLCFA",
    "unit": "mm",
    "coordinateSystem": "face-local origins are declared per feature"
  },
  "body": {
    "type": "extruded_aluminum_shell",
    "profileId": "unknown-or-user-provided",
    "material": "6063-T5",
    "lengthMm": null,
    "finish": {
      "process": "sandblast_anodize",
      "color": "natural|black|sky_blue|champagne|red|lake_blue|rose_pink|emerald_green|deep_space_gray"
    },
    "machining": {
      "process": "laser_cut|cnc|laser_plus_cnc",
      "toleranceGrade": "GB/T 1804-2000 m"
    }
  },
  "covers": [
    {
      "face": "front|rear|top|bottom|left|right",
      "material": "5052",
      "thicknessMm": 1.5,
      "machiningProcess": "laser_cut|laser_plus_cnc|cnc"
    }
  ],
  "features": [
    {
      "id": "feature-1",
      "face": "front",
      "type": "standard_opening|custom_opening|round_hole|slot|threaded_hole|countersunk_hole|laser_mark|uv_print",
      "shape": "circle|rectangle|rounded_slot|custom_svg|text",
      "centerMm": [0, 0],
      "sizeMm": [0, 0],
      "diameterMm": null,
      "rotationDeg": 0,
      "process": "laser_cut|cnc|laser_mark|uv_print",
      "standardOpening": {
        "kind": "standard_round_through_hole|standard_round_tapered_countersink|ethernet_rj45|ethernet_rj45_led|usb_type_c_male|usb_type_c_female|usb_rect_usb_port|usb_micro_b_female|usb_mini_b_female|dsub_vga_hdmi_port|dsub_vga_ddmr00pm_d|dsub_vga_dvi_female|dsub_vga_hdmi_female|dsub_db9|dc_power_connector_variant_a|dc_power_connector_variant_b|custom_library_other",
        "label": null,
        "catalogGroup": "standard_round_hole|ethernet_connector|usb_connector|vga_dsub_connector|dc_power_connector|other",
        "designerClearanceMm": 0.2
      },
      "constraintsChecked": [],
      "notes": []
    }
  ],
  "quality": {
    "appearanceLevel": "general|strict|extreme",
    "toleranceGrade": "m"
  },
  "assumptions": [],
  "openQuestions": []
}
```

## Output Style

Use Chinese when the user writes Chinese. Keep the final result practical: a short explanation, a JSON-like attribute block, conflicts/fixes, and open questions. Do not claim that JLCFA will accept a model unless the current order page or an engineer has confirmed it.
