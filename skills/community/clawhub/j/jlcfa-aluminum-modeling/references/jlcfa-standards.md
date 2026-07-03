# JLCFA Aluminum Alloy Enclosure Reference

Sources, reviewed 2026-06-30:

- JLCFA help manual: https://www.jlcfa.com/help/44006
- JLCFA process parameters: https://ke.jlcfa.com/housing/11

## Online Designer Concepts

- Left toolbar: standard openings, custom openings, text/graphic tools, and local upload.
- Top menu: model information, 3D view controls, version history, and design export.
- Right parameter panel: precise parameter adjustment for selected modeling elements.
- Modeling area: drag and adjust openings in the 3D view.
- Standard openings support position and relative-angle adjustment.
- Custom openings support relative position, relative angle, and detailed opening parameters.
- The designer also supports text/graphics, local uploads, object snapping, right-side panel editing, view switching, orientation ball, version history, and export.

## Materials

- Shell body: 6063-T5 aluminum alloy. Unspecified dimensional tolerance for material follows GB/T 5237.1-2017 high precision.
- Cover plate: 5052 aluminum alloy.
- Cover thickness options: 1.5 mm, 2 mm, 3 mm.

## Cutouts And Holes

- Laser minimum opening: 0.5 mm.
- Supported threaded holes: M2, M2.5, M3, M4.
- If opening height is under 30 mm, reserve at least 2 mm rib.
- If opening height is over 30 mm and under 70 mm, reserve at least 3 mm rib.
- Keep hole-to-edge distance over 3 mm.
- Avoid laser cutting/drilling at stiffening ribs, threaded-hole areas, or wall thickness over 4 mm.
- System-library openings are already expanded by 0.2 mm clearance over the physical measured size.

## Standard Opening Library

Known standard opening labels transcribed from the JLCFA online designer help screenshots, reviewed 2026-06-30. Treat this as a stable modeling vocabulary, not a promise that the current live designer has no additional entries. If a live designer entry is not listed here, keep `feature.type: "standard_opening"`, set `standardOpening.kind: "custom_library_other"`, and preserve the exact displayed label.

Standard/library openings only support position and relative-angle adjustment. Do not resize their cutout geometry unless the designer exposes a parameter for that specific entry.

| Enum kind | JLCFA displayed label | Catalog group | Notes |
| --- | --- | --- | --- |
| `standard_round_through_hole` | 标准圆孔 / 通孔 | 标准圆孔 | Parameter panel shows `孔类型: 通孔`; choose the designer's displayed hole spec. |
| `standard_round_tapered_countersink` | 标准圆孔 / 锥形沉头孔 | 标准圆孔 | Parameter panel shows `孔类型: 锥形沉头孔`; confirm screw/head standard before ordering. |
| `ethernet_rj45` | 以太网连接器（网线接口） | 以太网连接器 | Use for normal RJ45/network-cable opening language. |
| `ethernet_rj45_led` | 以太网连接器（带LED） | 以太网连接器 | Use when the connector has LED windows/light pipes in the jack opening. |
| `usb_type_c_male` | USB连接（Type-C公端） | USB连接口 | Screenshot label says 公端; preserve label if the live designer distinguishes male/female/mechanical style. |
| `usb_type_c_female` | USB连接（Type-C母） | USB连接口 | Visible in the standard-opening screenshot lower area. |
| `usb_rect_usb_port` | USB连接（USB口） | USB连接口 | Rectangular USB opening shown by the designer; often maps to USB-A style requests, but keep the displayed label. |
| `usb_micro_b_female` | USB连接（Micro-B母） | USB连接口 | Use for Micro-B female receptacle openings. |
| `usb_mini_b_female` | USB连接（Mini-B母） | USB连接口 | Use for Mini-B female receptacle openings. |
| `dsub_vga_hdmi_port` | D-Sub_VGA连接器（HDMI口） | VGA连接器 | Screenshot truncates the prefix as `D-Sub_VGA连...`; keep the complete readable suffix. |
| `dsub_vga_ddmr00pm_d` | D-Sub_VGA连接器（D-DMR00PM-D...） | VGA连接器 | Specific displayed model is truncated in the screenshot; verify the current designer label for production. |
| `dsub_vga_dvi_female` | D-Sub_VGA连接器（DVI母） | VGA连接器 | Use for DVI female style openings. |
| `dsub_vga_hdmi_female` | D-Sub_VGA连接器（HDMI母） | VGA连接器 | Use for HDMI female style openings. |
| `dsub_db9` | DB9 | VGA连接器 | DB9/D-sub 9-pin style opening. |
| `dc_power_connector_variant_a` | DC电源连接器 | DC电源连接器 | One of two visible DC power connector variants; the screenshot does not expose the full variant name. |
| `dc_power_connector_variant_b` | DC电源连接器 | DC电源连接器 | Second visible DC power connector variant; verify exact current label before production. |
| `custom_library_other` | exact live-designer label | More common openings | Use for current built-in/library entries not captured above. Preserve label, category, and screenshot/source if available. |

## Countersunk Screw Holes

Countersunk-hole execution standards listed by JLCFA: GB/T 819-1985, ISO 7046-1-1994, JIS B 1111-1996.

| Thread | Through hole D | Countersink W | Recommended FA screw | Screw length |
| --- | ---: | ---: | --- | ---: |
| M2 | 2.4 | 4.5 | EDLW-CE1-M2-L8 | 8 |
| M2.5 | 2.9 | 5.4 | EDLW-CE1-M2.5-L8 | 8 |
| M3 | 3.4 | 6.5 | EDLW-CE1-M3-L8 | 8 |
| Small-head M4 | 4.5 | 6.8 | ELLD-CE1-M4-L8 | 8 |
| Large-head M4 | 4.5 | 8.6 | EDLW-CE1-M4-L8 | 8 |

## Tolerance Defaults

- Blanking/cutting precision: +/-0.2 mm.
- General machining follows GB/T 1804-2000, tolerance grade m unless the user requests another grade.

Linear dimensions, grade m:

| Range mm | 0.5-3 | >3-6 | >6-30 | >30-120 | >120-400 | >400-1000 | >1000-2000 | >2000-4000 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Tolerance | +/-0.10 | +/-0.10 | +/-0.20 | +/-0.30 | +/-0.50 | +/-0.80 | +/-1.20 | +/-2.00 |

Radius/chamfer height dimensions, grade m:

| Range mm | 0.5-3 | >3-6 | >6-30 | >30 |
| --- | ---: | ---: | ---: | ---: |
| Tolerance | +/-0.20 | +/-0.50 | +/-1.00 | +/-2.00 |

Angle dimensions, grade m:

| Shorter side range mm | <=10 | >10-50 | >50-120 | >120-400 | >400 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Tolerance | +/-1 deg | +/-30 min | +/-20 min | +/-10 min | +/-5 min |

## Appearance Levels

- General: slight color difference is allowed; profile texture is allowed up to 5 places; slight scratches within 10 mm are allowed up to 5 places; no more than five spots up to 2 mm are allowed.
- Strict, priced +10%: no visible color difference, except possible batch color difference; spots up to 1 mm are allowed up to 2 places; slight scratches up to 5 mm are allowed up to 2 places.
- Extreme, priced +30%: no visible color difference, except possible slight batch color difference; no visible spots or scratches.

## Sandblast Anodizing

- Standard products only provide natural and black; other colors should be selected in the designer.
- Optional colors shown by JLCFA: natural, black, sky blue, champagne, red, lake blue, rose pink, emerald green, deep space gray.
- Sandblast medium: corundum, 100 mesh.
- Process note: sandblast first, then anodize, to maintain insulation.

Anodized film thickness:

| Color | Thickness |
| --- | ---: |
| Natural | 3.8-5.7 um |
| Black | 1.6-2.4 um |
| Sky blue | 1.4-2.0 um |
| Champagne | 1.2-1.8 um |
| Red | 0.9-1.5 um |
| Lake blue | 4.5-8.0 um |
| Rose pink | 1.0-2.0 um |
| Emerald green | 1.3-2.6 um |
| Deep space gray | 0.8-1.9 um |

## Marking And Printing

Laser marking:

- Depth: 3-5 um.
- Minimum character: 0.2 mm.
- Minimum line width: 0.012 mm.
- Laser marking supports single color.
- For black lettering, shown body colors include natural, deep space gray, and champagne.
- For white lettering, shown body colors include black, lake blue, rose pink, red, emerald green, and sky blue.
- SVG vector upload is recommended.
- Keep disconnected/negative-space gaps over 3 px to avoid sticking together.
- For high-quality graphics, recommend UV printing.
- Font preview recommends No. 4 font. Supported displayed font sizes: 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0.
- Do not upload unverified certification/standard marks or claims, including national standard numbers, environmental/certification logos such as RoHS, CE, 3C, UL, certification-related graphics, or text implying compliance such as ISO9001/RoHS certification. JLCFA may reject production or delete violating marks.

UV printing:

- JLCFA presents UV printing as replacing silkscreen for better vividness, durability, fade resistance, and appearance.
- Font color can be arbitrary; graphic shape can be arbitrary.
- Print height must be under 100 mm.
- Prefer printing on flat surfaces.
- UV supports multicolor output; laser marking is single-color.

## Machining Process Selection

Cover machining:

- Full laser cutting: relatively rough surface, laser-cut texture, no micro-tabs on internal holes, micro-tabs on outer contour.
- Laser cutting plus CNC: internal structures use laser cutting; outer contour and countersinks use CNC; smoother outer contour, no laser cutting texture, no micro-tabs.
- Full CNC: smooth surface, no laser cutting texture, no micro-tabs.
- If the design has steps, counterbore/countersink holes, or blind holes, choose CNC.
- If a hole is a sharp right angle, default machining uses R0.5.
- If cover thickness is over 2 mm, JLCFA recommends laser cutting plus CNC. Cover thickness choices remain 1.5, 2, and 3 mm.

Body machining:

- Full laser cutting: relatively rough surface, laser-cut texture, micro-tabs.
- Full CNC: smooth surface, no laser cutting texture, no micro-tabs.
- If the design has steps, counterbore/countersink holes, or blind holes, choose CNC.
- If a hole is a sharp right angle, default machining uses R0.5.

## Attribute Construction Tips

- Use `process: "laser_cut"` only for simple through cutouts that satisfy minimum width, rib, edge, and thickness constraints.
- Use `process: "cnc"` for blind holes, counterbores/countersinks, steps, sharp internal-corner expectations, wall thickness over 4 mm, or features near ribs/threaded regions.
- Use `feature.type: "standard_opening"` for library cutouts and keep the 0.2 mm default clearance in mind.
- For built-in openings, fill `standardOpening.kind` from the Standard Opening Library table and preserve the Chinese `label` when the entry name matters.
- Use `feature.type: "custom_opening"` for user dimensions, and explicitly record checked constraints in `constraintsChecked`.
- For marking, separate `laser_mark` and `uv_print`; record whether the artwork is `svg`, `image`, or `text`, and whether the selected color/process is single- or multi-color.
- When the profile/model number is unknown, do not invent it. Set `profileId: "unknown"` and ask the user to pick a JLCFA shell model.
