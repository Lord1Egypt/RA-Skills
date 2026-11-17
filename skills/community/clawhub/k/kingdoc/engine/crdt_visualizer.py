"""KingDoc CRDT 冲突可视化引擎（v4.4.0 T6）

能力：
- 从 crdt_table 会话导出单元格级操作日志（含向量时钟）
- 冲突标记在 Web 面板以时间线呈现（ECharts 单文件 HTML）
- 冲突可审查、可追溯：按单元格分组、标注并发操作与最终值
- 验收：还原一次真实并发编辑（两个 client 并发写同一单元格）
- 本地降级：无 ECharts CDN 时用内联 SVG 时间线兜底，离线可读

设计原则：
- 只读 crdt_table 的会话内存态，不改动 CRDT 算法
- 可视化数据为纯 JSON；HTML 自包含（ECharts CDN + SVG fallback）
- 零第三方 Python 依赖
"""
from __future__ import annotations

import html
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# 冲突/操作类型配色（中文语义）
COLOR_MAP = {
    "conflict": "#dc2626",   # 冲突-红
    "set": "#2563eb",        # 写入-蓝
    "delete": "#6b7280",     # 删除-灰
    "resolved": "#16a34a",   # 已解决-绿
}


class CRDTVisualizer:
    """CRDT 冲突时间线可视化"""

    def __init__(self, crdt_engine: Any = None):
        self.crdt_engine = crdt_engine

    @staticmethod
    def _ts_key(op: Dict[str, Any]) -> float:
        """统一 timestamp 排序键，容忍 int/float/数字字符串/ISO 字符串混排。"""
        ts = op.get("timestamp", 0)
        if isinstance(ts, (int, float)):
            return float(ts)
        try:
            return float(ts)
        except (ValueError, TypeError):
            # ISO 时间字符串退化为 0，保证不抛异常（内部日志时间戳一致，仅外部注入需容错）
            return 0.0

    # ------------------------------------------------------------------
    # 日志导出
    # ------------------------------------------------------------------
    def export_operations(self, session_id: str) -> Dict[str, Any]:
        """导出会话的单元格级操作日志（含向量时钟与冲突标记）"""
        engine = self.crdt_engine
        if engine is None:
            return {"success": False, "error": "未提供 crdt_table 引擎实例"}

        session = None
        if hasattr(engine, "get_session"):
            session = engine.get_session(session_id)
        if session is None and hasattr(engine, "_sessions"):
            session = engine._sessions.get(session_id)
        if session is None:
            return {"success": False, "error": f"会话不存在：{session_id}"}

        operations: List[Dict[str, Any]] = []
        cell_summaries: List[Dict[str, Any]] = []

        cells = getattr(session, "cells", {})
        for cell_id, cell in cells.items():
            row = getattr(cell, "row", 0); col = getattr(cell, "col", 0)
            for op in getattr(cell, "history", []):
                d = op.to_dict() if hasattr(op, "to_dict") else dict(op)
                d["cell_label"] = f"R{row}C{col}"
                d["is_conflict"] = False
                operations.append(d)
            # 冲突值也进入时间线
            if getattr(cell, "conflict", False):
                for cv in getattr(cell, "conflict_values", []):
                    operations.append({
                        "op_id": f"cf_{cell_id}_{cv.get('client_id', '')}",
                        "cell_id": cell_id,
                        "cell_label": f"R{row}C{col}",
                        "client_id": cv.get("client_id", ""),
                        "value": cv.get("value"),
                        "vector_clock": cv.get("vector_clock", {}),
                        "timestamp": cv.get("timestamp", 0),
                        "op_type": "set",
                        "is_conflict": True,
                    })
            cell_summaries.append({
                "cell_id": cell_id,
                "cell_label": f"R{row}C{col}",
                "final_value": getattr(cell, "value", None),
                "version": getattr(cell, "version", 0),
                "conflict": getattr(cell, "conflict", False),
                "conflict_count": len(getattr(cell, "conflict_values", [])),
                "op_count": len(getattr(cell, "history", [])),
            })

        operations.sort(key=lambda x: CRDTVisualizer._ts_key(x))
        conflict_count = sum(1 for c in cell_summaries if c["conflict"])
        return {
            "success": True,
            "session_id": session_id,
            "total_operations": len(operations),
            "total_cells": len(cell_summaries),
            "conflict_cells": conflict_count,
            "operations": operations,
            "cells": cell_summaries,
        }

    @staticmethod
    def from_operations(operations: List[Dict[str, Any]],
                        session_id: str = "replay") -> Dict[str, Any]:
        """从外部注入操作日志直接构造可视化数据（用于还原并发编辑测试）"""
        cells_map: Dict[str, Dict[str, Any]] = defaultdict(
            lambda: {"cell_id": "", "cell_label": "", "final_value": None,
                     "version": 0, "conflict": False, "conflict_count": 0, "op_count": 0}
        )
        ops = sorted(operations, key=lambda x: CRDTVisualizer._ts_key(x))
        for op in ops:
            cid = op.get("cell_id", "")
            c = cells_map[cid]
            c["cell_id"] = cid
            c["cell_label"] = op.get("cell_label", cid)
            if "value" in op and op["value"] is not None:
                c["final_value"] = op["value"]
            c["op_count"] += 1
            if op.get("is_conflict"):
                c["conflict"] = True
                c["conflict_count"] += 1
        return {
            "success": True,
            "session_id": session_id,
            "total_operations": len(ops),
            "total_cells": len(cells_map),
            "conflict_cells": sum(1 for c in cells_map.values() if c["conflict"]),
            "operations": ops,
            "cells": list(cells_map.values()),
        }

    # ------------------------------------------------------------------
    # 可视化渲染
    # ------------------------------------------------------------------
    def render_timeline(self, data: Dict[str, Any], output_path: str = "",
                        title: str = "CRDT 冲突时间线") -> Dict[str, Any]:
        """生成 ECharts 单文件 HTML 时间线（含 SVG 降级）"""
        path = output_path or str(
            Path(__file__).resolve().parent.parent / "crdt_timeline.html"
        )
        # 转义 HTML 敏感字符，防止 CRDT value（不可信客户端输入）闭合 <script> 造成注入
        payload = (json.dumps(data, ensure_ascii=False)
                   .replace("<", "\\u003c")
                   .replace(">", "\\u003e")
                   .replace("&", "\\u0026"))
        html_text = self._build_html(title, payload, data)
        try:
            Path(path).write_text(html_text, encoding="utf-8")
            return {
                "success": True, "path": path, "size": len(html_text),
                "total_operations": data.get("total_operations", 0),
                "conflict_cells": data.get("conflict_cells", 0),
                "offline_fallback": True,
            }
        except Exception as e:
            return {"success": False, "error": f"写入时间线失败：{e}"}

    def visualize_session(self, session_id: str, output_path: str = "",
                          title: str = "CRDT 冲突时间线") -> Dict[str, Any]:
        """一站式：导出会话日志 -> 渲染时间线"""
        data = self.export_operations(session_id)
        if not data.get("success"):
            return data
        return self.render_timeline(data, output_path, title)

    @staticmethod
    def _build_html(title: str, payload: str, data: Dict[str, Any]) -> str:
        esc = html.escape
        # 内联 SVG 降级时间线（按操作顺序画点 + 连线）
        ops = data.get("operations", [])
        svg_parts = []
        n = len(ops)
        width = max(760, n * 110)
        y_mid = 90
        for i, op in enumerate(ops):
            x = 60 + i * 110
            color = COLOR_MAP.get(
                "conflict" if op.get("is_conflict") else op.get("op_type", "set"),
                "#2563eb",
            )
            client = esc(str(op.get("client_id", "?")))
            val = esc(str(op.get("value", ""))[:16])
            label = esc(str(op.get("cell_label", op.get("cell_id", ""))))
            marker = "⚠" if op.get("is_conflict") else "●"
            svg_parts.append(
                f'<g><line x1="{x-55}" y1="{y_mid}" x2="{x}" y2="{y_mid}" stroke="#cbd5e1" stroke-width="2"/>'
                f'<circle cx="{x}" cy="{y_mid}" r="9" fill="{color}"/>'
                f'<text x="{x}" y="{y_mid-18}" text-anchor="middle" font-size="12" fill="#1f2937">{marker} {label}</text>'
                f'<text x="{x}" y="{y_mid+28}" text-anchor="middle" font-size="11" fill="#6b7280">{client}</text>'
                f'<text x="{x}" y="{y_mid+44}" text-anchor="middle" font-size="11" fill="#374151">{val}</text></g>'
            )
        svg = (
            f'<svg id="fallback" width="{width}" height="180" xmlns="http://www.w3.org/2000/svg" '
            f'style="display:none;background:#fff"><text x="20" y="30" font-size="15" font-weight="bold" '
            f'fill="#1f2937">离线时间线（ECharts 未加载时显示）</text>'
            + "".join(svg_parts) + "</svg>"
        )

        return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>{esc(title)}</title>
<script src="https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js"></script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,"Microsoft YaHei",sans-serif;background:#f5f7fa;color:#1f2937;padding:28px}}
h1{{font-size:22px;margin-bottom:6px}}
.meta{{color:#6b7280;font-size:13px;margin-bottom:18px}}
#chart{{width:100%;height:520px;background:#fff;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,.06)}}
.scroll{{overflow-x:auto;background:#fff;border-radius:12px;padding:12px;box-shadow:0 2px 8px rgba(0,0,0,.06)}}
</style></head><body>
<h1>{esc(title)}</h1>
<div class="meta">共 {data.get('total_operations',0)} 次操作 · {data.get('total_cells',0)} 个单元格 · {data.get('conflict_cells',0)} 个冲突单元格 · 单元格级向量时钟可追溯</div>
<div id="chart"></div>
<div class="scroll">{svg}</div>
<script>
var DATA = {payload};
function scaleTime(ts){{
  var nums = DATA.operations.map(function(o){{return Number(o.timestamp)||0;}});
  var min = Math.min.apply(null,nums), max = Math.max.apply(null,nums);
  if(!isFinite(min)||!isFinite(max)||min===max) return 0;
  return Math.round((Number(ts)-min)/(max-min)*1000);
}}
function render(){{
  if (typeof echarts === 'undefined') {{
    document.getElementById('chart').style.display='none';
    document.getElementById('fallback').style.display='block';
    return;
  }}
  var chart = echarts.init(document.getElementById('chart'));
  // tooltip 以 HTML 渲染，动态值必须先转义，防止 CRDT value 二次 DOM XSS
  function escHtml(v){{
    return String(v==null?'':v).replace(/&/g,'&amp;').replace(/</g,'&lt;')
      .replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');
  }}
  var groups = {{}};
  DATA.operations.forEach(function(o){{
    var k = o.cell_label || o.cell_id;
    (groups[k] = groups[k] || []).push(o);
  }});
  var series = [], y = 0, yLabels = [];
  Object.keys(groups).forEach(function(k){{
    yLabels.push(k);
    groups[k].forEach(function(o){{
      var color = o.is_conflict ? '{COLOR_MAP["conflict"]}' :
        (o.op_type==='delete' ? '{COLOR_MAP["delete"]}' : '{COLOR_MAP["set"]}');
      series.push({{
        name: k, type:'scatter',
        symbolSize: o.is_conflict ? 20 : 12,
        itemStyle:{{color:color}},
        data:[[scaleTime(o.timestamp), y]],
        label:{{show:true, position:'top', fontSize:10,
          formatter:escHtml(o.client_id||'')+'\\n'+escHtml(o.value==null?'':o.value).slice(0,10)}},
        tooltip:{{formatter:function(){{
          return '<b>'+escHtml(k)+'</b><br/>客户端: '+escHtml(o.client_id)+
            '<br/>值: '+escHtml(JSON.stringify(o.value))+
            '<br/>向量时钟: '+escHtml(JSON.stringify(o.vector_clock))+
            (o.is_conflict?'<br/><span style="color:red">⚠ 并发冲突</span>':'');
        }}}}
      }});
    }});
    y += 1;
  }});
  chart.setOption({{
    title:{{text:'单元格操作时间线（含并发冲突标记）',left:'center',textStyle:{{fontSize:15}}}},
    tooltip:{{trigger:'item'}},
    grid:{{left:70,right:30,top:50,bottom:60}},
    xAxis:{{type:'value',name:'相对时间 →',min:0,max:1000,
      axisLabel:{{formatter:function(v){{return v===0?'开始':(v===1000?'结束':'');}}}}}},
    yAxis:{{type:'category',data:yLabels,inverse:true,axisLabel:{{fontSize:11}}}},
    series:series
  }});
  window.addEventListener('resize',function(){{chart.resize();}});
}}
if (typeof echarts !== 'undefined') {{ render(); }}
else {{ window.addEventListener('load', function(){{
  var s=document.createElement('script');
  s.src='https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js';
  s.onload=render; s.onerror=render; document.head.appendChild(s);
}}); }}
</script>
</body></html>"""


# ---------------------------------------------------------------------------
# 模块级便捷函数
# ---------------------------------------------------------------------------
def get_visualizer(crdt_engine: Any = None) -> CRDTVisualizer:
    return CRDTVisualizer(crdt_engine)


def export_crdt_log(session_id: str, crdt_engine: Any = None) -> Dict[str, Any]:
    return CRDTVisualizer(crdt_engine).export_operations(session_id)


def visualize_session(session_id: str, crdt_engine: Any = None,
                      output_path: str = "") -> Dict[str, Any]:
    return CRDTVisualizer(crdt_engine).visualize_session(session_id, output_path)


def render_conflict_timeline(operations: List[Dict[str, Any]],
                             output_path: str = "",
                             session_id: str = "replay") -> Dict[str, Any]:
    """从操作日志直接渲染时间线（便于还原并发编辑测试）"""
    vis = CRDTVisualizer()
    data = CRDTVisualizer.from_operations(operations, session_id)
    return vis.render_timeline(data, output_path)
