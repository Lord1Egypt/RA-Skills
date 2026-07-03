#!/usr/bin/env python3
"""
power-cad-drafter / scripts/dxf_generator.py
10kV及以下供配电工程 DXF 图纸自动生成
"""

import ezdxf
import os
from typing import Dict, Any


def create_single_line_diagram(params: Dict[str, Any], output_path: str):
    """Generate 10kV / 0.4kV single-line diagram."""
    doc = ezdxf.new("R2018")
    msp = doc.modelspace()
    doc.header["$INSUNITS"] = 6

    msp.add_text("10kV 一次主接线图", height=8).set_placement(
        (420, 560), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
    msp.add_text(f"工程名称：{params.get('project_name', 'XX工程')}", height=3).set_placement((50, 545))

    y_hv = 450
    x_start = 80
    x_step = 120

    for i in range(params.get("power_source_count", 1)):
        x = x_start + i * x_step * 3
        _draw_breaker(msp, x, y_hv, label=f"10kV进线{i+1}")
        _draw_metering(msp, x + 40, y_hv)
        if params.get("hv_switch_type") == "breaker":
            _draw_breaker(msp, x + 80, y_hv, label="配变柜")
        else:
            _draw_load_switch(msp, x + 80, y_hv, label="配变柜")

    y_tx = 350
    tx_count = params.get("transformer_count", 1)
    for i in range(tx_count):
        x = x_start + i * 200
        _draw_transformer(msp, x, y_tx,
                          capacity=params.get("transformer_capacity", 800),
                          tx_type=params.get("transformer_type", "dry"))
        msp.add_line((x, y_hv - 20), (x, y_tx + 40))

    y_lv = 250
    for i in range(tx_count):
        x = x_start + i * 200
        _draw_lv_incomer(msp, x, y_lv, in_a=params.get("transformer_capacity", 800))
        msp.add_line((x, y_tx - 40), (x, y_lv + 20))

    if params.get("lv_bus_coupler", False) and tx_count >= 2:
        x_mid = x_start + (tx_count - 1) * 200 / 2
        _draw_breaker(msp, x_mid, y_lv, label="0.4kV母联", orientation="horizontal")
        msp.add_line((x_start, y_lv), (x_start + (tx_count - 1) * 200, y_lv))

    _draw_legend(msp, 650, 100)
    doc.saveas(output_path)
    print(f"[DXF] 主接线图已生成：{output_path}")


def create_layout_plan(params: Dict[str, Any], output_path: str):
    """Generate substation layout plan."""
    doc = ezdxf.new("R2018")
    msp = doc.modelspace()
    doc.header["$INSUNITS"] = 6

    msp.add_text("配电室平面布置图", height=8).set_placement(
        (420, 560), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)

    rw = params.get("room_width", 8) * 1000
    rd = params.get("room_depth", 6) * 1000
    origin = (100, 100)
    msp.add_lwpolyline([
        origin, (origin[0] + rw, origin[1]),
        (origin[0] + rw, origin[1] + rd), (origin[0], origin[1] + rd)
    ], close=True)

    _add_dim(msp, origin[0], origin[1] - 30, origin[0] + rw, origin[1] - 30, text=f"{rw/1000:.1f}m")
    _add_dim(msp, origin[0] - 30, origin[1], origin[0] - 30, origin[1] + rd, text=f"{rd/1000:.1f}m")

    for eq in params.get("equipment_list", []):
        ex = origin[0] + eq.get("x", 0) * 1000
        ey = origin[1] + eq.get("y", 0) * 1000
        ew = eq.get("width", 0.8) * 1000
        ed = eq.get("depth", 0.6) * 1000
        msp.add_lwpolyline([
            (ex, ey), (ex + ew, ey), (ex + ew, ey + ed), (ex, ey + ed)
        ], close=True)
        msp.add_text(eq.get("name", "设备"), height=2.5).set_placement(
            (ex + ew/2, ey + ed/2), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)

    for aisle in params.get("aisle_annotations", []):
        ax = origin[0] + aisle["x"] * 1000
        ay = origin[1] + aisle["y"] * 1000
        msp.add_text(f"通道≥{aisle['width']:.1f}m", height=2.5).set_placement((ax, ay))

    doc.saveas(output_path)
    print(f"[DXF] 平面布置图已生成：{output_path}")


def create_grounding_plan(params: Dict[str, Any], output_path: str):
    """Generate grounding layout plan."""
    doc = ezdxf.new("R2018")
    msp = doc.modelspace()
    doc.header["$INSUNITS"] = 6

    msp.add_text("接地装置布置图", height=8).set_placement(
        (420, 560), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)

    for i in range(4):
        x = 200 + i * 150
        y = 300
        msp.add_circle((x, y), 8)
        msp.add_text("接地极", height=2.5).set_placement((x, y - 20))

    msp.add_lwpolyline([(150, 300), (650, 300)], close=False)
    msp.add_text("水平接地体 φ16热镀锌圆钢", height=3).set_placement((400, 280))
    msp.add_line((400, 300), (400, 400))
    msp.add_text("引下线", height=2.5).set_placement((420, 350))
    msp.add_text(f"接地电阻 R≤{params.get('grounding_resistance', 4)}Ω", height=4).set_placement((400, 200))

    doc.saveas(output_path)
    print(f"[DXF] 接地布置图已生成：{output_path}")


def create_cable_plan(params: Dict[str, Any], output_path: str):
    """Generate cable routing plan."""
    doc = ezdxf.new("R2018")
    msp = doc.modelspace()
    doc.header["$INSUNITS"] = 6

    msp.add_text("电缆敷设路径图", height=8).set_placement(
        (420, 560), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)

    msp.add_lwpolyline([(100, 300), (700, 300), (700, 340), (100, 340)], close=True)
    msp.add_text("电缆沟", height=3).set_placement((400, 320))

    for i, cable in enumerate(params.get("cables", [])):
        y = 310 + i * 5
        msp.add_line((120, y), (680, y))
        msp.add_text(cable.get("id", f"DL-{i+1}"), height=2).set_placement((400, y + 2))

    doc.saveas(output_path)
    print(f"[DXF] 电缆敷设图已生成：{output_path}")


def _draw_breaker(msp, x, y, label="断路器", orientation="vertical"):
    w, h = (16, 24) if orientation == "vertical" else (24, 16)
    pts = [(x-w/2, y-h/2), (x+w/2, y-h/2), (x+w/2, y+h/2), (x-w/2, y+h/2)]
    msp.add_lwpolyline(pts, close=True)
    msp.add_line((x-w/2, y-h/2), (x+w/2, y+h/2))
    msp.add_text(label, height=2.5).set_placement((x, y - h/2 - 10))


def _draw_load_switch(msp, x, y, label="负荷开关"):
    w, h = 16, 24
    pts = [(x-w/2, y-h/2), (x+w/2, y-h/2), (x+w/2, y+h/2), (x-w/2, y+h/2)]
    msp.add_lwpolyline(pts, close=True)
    msp.add_line((x, y-h/2), (x, y+h/2))
    msp.add_text(label, height=2.5).set_placement((x, y - h/2 - 10))


def _draw_metering(msp, x, y):
    w, h = 20, 30
    pts = [(x-w/2, y-h/2), (x+w/2, y-h/2), (x+w/2, y+h/2), (x-w/2, y+h/2)]
    msp.add_lwpolyline(pts, close=True)
    msp.add_text("计量", height=2.5).set_placement((x, y), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)


def _draw_transformer(msp, x, y, capacity=800, tx_type="dry"):
    r = 30
    msp.add_circle((x, y), r)
    msp.add_text(f"{capacity}kVA", height=2.5).set_placement((x, y + 5), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
    msp.add_text("干式" if tx_type == "dry" else "油浸", height=2).set_placement((x, y - 8), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)


def _draw_lv_incomer(msp, x, y, in_a=800):
    w, h = 24, 20
    pts = [(x-w/2, y-h/2), (x+w/2, y-h/2), (x+w/2, y+h/2), (x-w/2, y+h/2)]
    msp.add_lwpolyline(pts, close=True)
    msp.add_text(f"{in_a}A", height=2).set_placement((x, y), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)


def _draw_legend(msp, x, y):
    msp.add_lwpolyline([(x, y), (x+150, y), (x+150, y+80), (x, y+80)], close=True)
    msp.add_text("图例", height=3).set_placement((x+75, y+70), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)


def _add_dim(msp, x1, y1, x2, y2, text=""):
    msp.add_line((x1, y1), (x2, y2))
    mx, my = (x1+x2)/2, (y1+y2)/2
    msp.add_text(text, height=2.5).set_placement((mx, my))


if __name__ == "__main__":
    test_params = {
        "project_name": "测试工程",
        "transformer_count": 2,
        "transformer_capacity": 800,
        "transformer_type": "dry",
        "hv_switch_type": "breaker",
        "lv_bus_coupler": True,
        "power_source_count": 1,
        "room_width": 8.5,
        "room_depth": 6.2,
        "equipment_list": [
            {"name": "高压柜", "width": 0.8, "depth": 1.5, "x": 1.0, "y": 4.0},
            {"name": "变压器", "width": 1.2, "depth": 1.0, "x": 2.5, "y": 2.5},
            {"name": "低压柜", "width": 0.8, "depth": 1.5, "x": 4.5, "y": 4.0},
        ],
        "aisle_annotations": [{"x": 2.0, "y": 1.5, "width": 1.5}],
        "cables": [{"id": "DL-01", "spec": "ZRYJV22-3x95"}, {"id": "DL-02", "spec": "ZRYJV-4x240+1x120"}],
        "grounding_resistance": 4,
    }
    out_dir = "/Users/wnep/.openclaw/workspace"
    create_single_line_diagram(test_params, os.path.join(out_dir, "test_single_line.dxf"))
    create_layout_plan(test_params, os.path.join(out_dir, "test_layout.dxf"))
    create_grounding_plan(test_params, os.path.join(out_dir, "test_grounding.dxf"))
    create_cable_plan(test_params, os.path.join(out_dir, "test_cable.dxf"))
