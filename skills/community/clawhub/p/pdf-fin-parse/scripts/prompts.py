"""Prompt 模板：normal / detail 两档。

约定输出 JSON schema（与 assets/output_schema.json 的 per-page 等价子集）：
{
  "page_no": int,
  "markdown": str,                                  # 该页 Markdown（标题/正文/表格/列表）
  "blocks": [                                       # 文本块（按阅读顺序）
    {"type": "heading"|"paragraph"|"figure_caption",
     "level": 1..6 | null,
     "text": str,
     "source_page": int,
     "source_bbox": [x0,y0,x1,y1] | null}
  ],
  "tables": [
    {"caption": str | null,
     "n_rows": int, "n_cols": int,
     "header_rows": int,                            # 表头占的行数（多级表头时 > 1）
     "source_page": int,
     "source_bbox": [x0,y0,x1,y1] | null,
     "cells": [
        {"row": int, "col": int,
         "rowspan": int, "colspan": int,
         "text": str,                                # 原文（去千分位前）
         "value": number | null,                     # 解析后的数值；非数字为 null
         "unit": str | null}                         # "yuan"|"wan_yuan"|"yi_yuan"|"percent"|"usd"|null
     ]}
  ],
  "confidence": 0.0..1.0                             # 模型自评（越高越确信）
}

设计：模型一次性把版面 + 表格 + 阅读顺序 + 数值规整都做完，本地不再加工。
"""
from __future__ import annotations

from typing import Dict


_BASE_SCHEMA_INSTRUCTION = """你是金融领域文档结构化助手。我会给你**一页**财务报告/年报/招股书/10-K 的渲染图。

请严格按以下 JSON schema 输出（不要任何额外文字、不要 Markdown 代码块、不要解释）：

{
  "page_no": <整数，使用我给你的页号>,
  "markdown": "<该页的 Markdown：保留阅读顺序、标题层级、表格用 GFM 表格语法、图表写为占位>",
  "blocks": [
    {"type": "heading|paragraph|figure_caption",
     "level": 1-6 或 null,
     "text": "...",
     "source_page": <页号>,
     "source_bbox": [x0,y0,x1,y1] 或 null}
  ],
  "tables": [
    {"caption": "..." 或 null,
     "n_rows": N, "n_cols": M,
     "header_rows": K,
     "source_page": <页号>,
     "source_bbox": [x0,y0,x1,y1] 或 null,
     "cells": [
        {"row": r, "col": c,
         "rowspan": 1, "colspan": 1,
         "text": "原文",
         "value": 数字 或 null,
         "unit": "yuan|wan_yuan|yi_yuan|percent|usd" 或 null}
     ]}
  ],
  "confidence": 0.0~1.0
}

通用约束：
1. **阅读顺序**：多栏排版按"先左栏从上到下，再右栏"输出 blocks；表格按 y 顺序插入
2. **标题层级**：从 1（一级标题）开始；非标题段落 level=null
3. **表格规范**：
   - 多级表头：header_rows 设为表头占的行数；cells 中前 header_rows 行为表头
   - 合并单元格：在锚位置（左上角）写 text，rowspan/colspan>1；被覆盖的位置不出现 cell
   - 跨页表格：只输出本页可见的行；caption 标注 "(续上页)" 或 "(续下页)"
4. **数值规整**：
   - 原文 "1,234,567.89" → text="1,234,567.89", value=1234567.89, unit 按上下文判断
   - 负数原文 "(1,234)" → text="(1,234)", value=-1234, unit 同上
   - 百分比 "12.5%" → value=12.5, unit="percent"
   - 货币单位识别"单位：元/万元/亿元/USD"声明（页面任意位置出现），applied 到该表所有数值列
   - **中文方向词决定正负**：含"下降/减少/降低/亏损/下滑"→ value 取负；含"增长/上升/提高/上涨/盈利"→ value 取正。如 "下降0.57个百分点" → value=-0.57, unit="percent"
   - 无法解析为数字（如 "—"、"不适用"、空白）→ value=null
5. **页眉页脚**：识别但**不**放入 blocks 输出（去除页码/公司名重复出现的边缘文本）
6. **图片/图表**：写 figure_caption block，markdown 中保留 `![描述](placeholder)`
7. **confidence**：自评 0~1；遇到模糊/扫描/手写时降低；正常清晰文档 ≥0.85

页面没有任何内容时输出：{"page_no": <页号>, "markdown": "", "blocks": [], "tables": [], "confidence": 1.0}
"""


_DETAIL_ADDENDUM = """

【DETAIL 模式追加要求】
- **逐字符确认**：表格中每个数字必须与图像逐字符对照；不允许"猜测"
- **多级表头**：必须正确识别"合并表头 / 行表头 / 数值"三维结构；header_rows 准确反映层数
- **印章/水印**：识别但忽略，不影响下方文本
- **扫描件**：尽力识别；不确定的字符在 text 中用 "?" 占位（如 "总资?" 字段）并降低该 cell 所在表的整体 confidence
- **跨页推理**：若上下文表明本页表格延续自上页，caption 加 "(续上页)"
- **币种判定**：优先看本页"单位：xxx"声明；如无，看章节名称（"以人民币计量"等）；都没有则 unit=null
"""


# ---------------------------------------------------------------------------
# 对外
# ---------------------------------------------------------------------------

_PROMPTS: Dict[str, str] = {
    "normal": _BASE_SCHEMA_INSTRUCTION,
    "detail": _BASE_SCHEMA_INSTRUCTION + _DETAIL_ADDENDUM,
}


def build_prompt(mode: str) -> str:
    if mode not in _PROMPTS:
        raise ValueError(f"未知 parse mode: {mode}; 可选: {list(_PROMPTS)}")
    return _PROMPTS[mode]


def list_modes() -> list[str]:
    return list(_PROMPTS.keys())
