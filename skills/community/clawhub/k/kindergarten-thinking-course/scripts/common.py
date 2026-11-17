# -*- coding: utf-8 -*-
"""
幼儿园思维课程体系 - 共享素材库（素材、版式、国际化文案）

本文件被主脚本与 generators/ 下所有题型插件共同依赖。
新增题型插件只需 `from common import *` 即可访问全部素材与 I18N。
"""
import random

# ---------------- 素材库 ----------------
EMOJI_ANIMALS = ["🐶", "🐱", "🐰", "🐻", "🐼", "🐨", "🐯", "🦁", "🐸", "🐵", "🐷", "🐮", "🐔", "🐧"]
EMOJI_FRUITS = ["🍎", "🍌", "🍇", "🍓", "🍊", "🍉", "🍑", "🍒", "🥝", "🍐", "🍍", "🍈"]
EMOJI_VEHICLES = ["🚗", "🚌", "🚲", "🚂", "✈️", "🚀", "🚜", "🚕", "🚁", "⛵", "🛳️", "🚜"]
EMOJI_COLORS = {"红": "🔴", "蓝": "🔵", "黄": "🟡", "绿": "🟢", "橙": "🟠", "紫": "🟣"}
SIZE_ORDER = ["🐜", "🐭", "🐰", "🐱", "🐶", "🐻", "🐮", "🐷", "🐯", "🐘", "🐳", "🦕"]  # 从小到大
SHAPES = ["圆形", "正方形", "三角形", "长方形", "星形", "心形"]

CSS = """<style>
@page { size: A4; margin: 12mm; }
* { box-sizing: border-box; -webkit-print-color-adjust:exact; print-color-adjust:exact; }
body { font-family: "Microsoft YaHei","PingFang SC",sans-serif; color:#222; margin:0; }
.sheet { width: 186mm; margin: 0 auto; }
.head { display:flex; justify-content:space-between; align-items:baseline;
        border-bottom:3px solid #4a90d9; padding-bottom:4px; margin-bottom:10px;
        flex-wrap:wrap; gap:4px 12px; }
.head h1 { font-size:18px; margin:0; color:#2c5f8a; }
.head .meta { font-size:12px; color:#666; }
.grid2 { display:grid; grid-template-columns:1fr 1fr; gap:10px 14px; }
.grid3 { display:grid; grid-template-columns:1fr 1fr 1fr; gap:10px 14px; }
.card { border:1.5px solid #cdd9e5; border-radius:8px; padding:8px 10px;
        break-inside:avoid; background:#fff; }
.card .t { font-size:13px; font-weight:bold; color:#2c5f8a; margin-bottom:2px; }
.card .i { font-size:12px; color:#555; margin-bottom:6px; }
.row { display:flex; flex-wrap:wrap; gap:6px; align-items:center; }
.cell { width:34px; height:34px; line-height:34px; text-align:center;
        font-size:22px; border:1px solid #e2e8f0; border-radius:6px; background:#fafcff; }
.cell.lg { width:44px; height:44px; line-height:44px; font-size:28px; }
.pair { display:flex; gap:18px; }
.paircol { display:flex; flex-direction:column; gap:6px; }
.seq { display:flex; gap:6px; align-items:center; flex-wrap:wrap; }
.seq .gap { width:34px; height:34px; border:2px dashed #e07b39; border-radius:6px;
            display:inline-flex; align-items:center; justify-content:center; color:#e07b39; font-weight:bold; }
.maze { border-collapse:collapse; margin:4px 0; }
.maze td { width:26px; height:26px; padding:0; position:relative; }
.ans { margin-top:14px; border-top:2px dashed #4a90d9; padding-top:8px; }
.ans h2 { font-size:14px; color:#2c5f8a; margin:0 0 6px; }
.ans ol { font-size:12px; color:#444; margin:0; padding-left:20px; }
.ans li { margin-bottom:3px; }
/* 等级主题色：L1 暖橙 / L2 浅绿 / L3 浅蓝 / L4 浅紫 */
.sheet.l1 .head { border-bottom-color:#ff8a65; }
.sheet.l1 .card .t, .sheet.l1 .score .t2, .sheet.l1 .ans h2 { color:#ff7043; }
.sheet.l1 .ans { border-top-color:#ff8a65; }
.sheet.l2 .head { border-bottom-color:#66bb6a; }
.sheet.l2 .card .t, .sheet.l2 .score .t2, .sheet.l2 .ans h2 { color:#43a047; }
.sheet.l2 .ans { border-top-color:#66bb6a; }
.sheet.l3 .head { border-bottom-color:#42a5f5; }
.sheet.l3 .card .t, .sheet.l3 .score .t2, .sheet.l3 .ans h2 { color:#1e88e5; }
.sheet.l3 .ans { border-top-color:#42a5f5; }
.sheet.l4 .head { border-bottom-color:#ab47bc; }
.sheet.l4 .card .t, .sheet.l4 .score .t2, .sheet.l4 .ans h2 { color:#8e24aa; }
.sheet.l4 .ans { border-top-color:#ab47bc; }
.brand { font-size:10px; color:#aaa; margin-top:2px; text-align:right; letter-spacing:1px; }
.shapebox { display:inline-flex; flex-direction:column; align-items:center; gap:2px; margin:4px; }
.shapebox .lab { font-size:11px; color:#555; }
.note { font-size:11px; color:#999; font-style:italic; }
.qcheck { font-size:11px; color:#888; margin-top:5px; user-select:none; }
/* 姓名可填 / 评分栏 */
.fill { border-bottom:1px solid #333; display:inline-block; min-width:90px; padding:0 4px; }
.fill.sm { min-width:46px; }
.score { margin-top:14px; border-top:2px dashed #e67e22; padding-top:8px; font-size:13px; color:#444; }
.score .t2 { font-size:13px; font-weight:bold; color:#2c5f8a; margin-bottom:4px; }
.score .row2 { display:flex; gap:24px; align-items:center; flex-wrap:wrap; margin-bottom:6px; }
.grid1 { display:grid; grid-template-columns:1fr; gap:10px 14px; }
/* 打印：答案另起一页，避免孩子做题时直接看到答案 */
@media print {
  .ans { page-break-before: always; }
  .card, .shapebox { page-break-inside: avoid; }
}
</style>"""

SVG_SHAPES = {
    "圆形": '<svg width="40" height="40" viewBox="0 0 40 40"><circle cx="20" cy="20" r="17" fill="{c}"/></svg>',
    "正方形": '<svg width="40" height="40" viewBox="0 0 40 40"><rect x="4" y="4" width="32" height="32" rx="2" fill="{c}"/></svg>',
    "三角形": '<svg width="40" height="40" viewBox="0 0 40 40"><polygon points="20,4 37,36 3,36" fill="{c}"/></svg>',
    "长方形": '<svg width="40" height="40" viewBox="0 0 40 40"><rect x="3" y="9" width="34" height="22" rx="2" fill="{c}"/></svg>',
    "星形": '<svg width="40" height="40" viewBox="0 0 40 40"><polygon points="20,3 25,15 38,15 27,23 31,36 20,28 9,36 13,23 2,15 15,15" fill="{c}"/></svg>',
    "心形": '<svg width="40" height="40" viewBox="0 0 40 40"><path d="M20 35 C2 22 6 6 20 14 C34 6 38 22 20 35 Z" fill="{c}"/></svg>',
}
SHAPE_COLORS = ["#e74c3c", "#3498db", "#f1c40f", "#2ecc71", "#9b59b6", "#e67e22"]

# 颜色 / 主题 / 形状 的中→英映射（作用于英文界面）
COLOR_EN = {"红": "red", "蓝": "blue", "黄": "yellow", "绿": "green", "橙": "orange", "紫": "purple"}
THEME_EN = {"水果": "fruits", "动物": "animals", "交通工具": "vehicles"}
SHAPE_NAMES_EN = {"圆形": "circle", "正方形": "square", "三角形": "triangle", "长方形": "rectangle", "星形": "star", "心形": "heart"}
# 方位内部 key → 中/英方向词
DIR_ZH = {"up": "上", "down": "下", "left": "左", "right": "右"}
DIR_EN = {"up": "above", "down": "below", "left": "to the left of", "right": "to the right of"}


def rid():
    return random.randint(1000, 9999)


# ---------------- 等级与默认配置 ----------------
LEVEL_TOPICS = {
    # L1 = 基础分类与「一一对应」，match（配对/连线）是本级核心，不可遗漏
    1: ["classify", "match", "same", "diff", "compare", "position", "maze"],
    2: ["classify", "match", "order", "pattern", "shape", "position", "compare", "diff", "maze"],
    3: ["pattern", "shape", "position", "compare", "diff", "maze", "order", "swap"],
    4: ["pattern", "shape", "position", "compare", "maze", "order", "swap"],
}
DEFAULT_COUNTS = {1: 6, 2: 8, 3: 8, 4: 10}
# 观察 / 专注类题型：单张练习不超过 MAX_OBSERVE 题（SKILL.md 硬规则）
OBSERVE_TOPICS = {"maze", "diff", "same"}
MAX_OBSERVE = 4
# 单张练习题目数量上限（硬规则：一次只生成一份，避免堆 30+ 题）
MAX_COUNT = 30

# ---------------- 国际化文案 ----------------
# 题型指令/答案中的变量统一用 {name}=format 注入；分隔符在生成器内按 lang 选择。
I18N = {
    "zh": {
        "head_title": "幼儿思维训练 · L{level}",
        "page_title": "幼儿思维训练 L{level}",
        "name_label": "姓名：{name}　|　共 {n} 题",
        "answer_title": "答案",
        "qcheck": "☐ 对　☐ 错",
        # 题型标题
        "title_classify": "分类", "title_match": "配对", "title_same": "找相同",
        "title_diff": "找不同", "title_order": "排序", "title_pattern": "规律",
        "title_shape": "图形", "title_position": "方位", "title_compare": "比较",
        "title_maze": "迷宫", "title_swap": "等量代换",
        # 指令
        "instr_classify_color": "圈出所有{color}色的物品。",
        "instr_classify_cat": "圈出所有{name}。",
        "instr_match": "把左边和右边相同的图连起来（在左边写出右边对应的序号）。",
        "instr_same": "有两个图是一样的，把它们圈出来。",
        "instr_diff": "有一个和其他不一样，把它圈出来。",
        "instr_order": "按从小到大（越变越大）的顺序，在图下写出编号 1-5。",
        "instr_pattern": "观察规律，在问号处画出（写出）接下来的图。",
        "instr_shape": "圈出所有「{shape}」。",
        "instr_position": "{a} 在 {b} 的（上 / 下 / 左 / 右）？圈出正确的方向。",
        "instr_compare_count": "哪边多？在多的那边数一数，写出数字。",
        "instr_compare_height": "按从高到矮，写出编号 1-3。",
        "instr_maze": "从 🚪 入口走到 🎁 出口，画出一条路线。",
        "instr_swap": "看上面的等式，算出问号等于几个 ⭐，把数字写在问号处。",
        # 答案片段
        "ans_shape_prefix": "第 ", "ans_suffix": " 个",
        "ans_same_two": "第 {x} 个 和 第 {y} 个",
        "ans_order_prefix": "顺序编号：",
        "ans_pattern_prefix": "问号依次是：",
        "ans_position": "{a} 在 {b} 的「{d}」",
        "ans_maze": "自由路径，家长判断是否能连通即算对。",
        "ans_count_more": "{side}边多（{n}个）",
        "ans_swap_suffix": " 个 ⭐",
        "name_label_prefix": "姓名：",
        "name_label_suffix": "　|　共 {n} 题",
        "score_title": "评分",
        "score_points": "得分：",
        "score_correct": "正确：",
        "score_comment": "评语：",
        "score_date": "日期：",
        "score_total_suffix": " / {n} 题",
        "brand": "用 kindergarten-thinking-course v1.1 自动生成",
    },
    "en": {
        "head_title": "Thinking Training · L{level}",
        "page_title": "Thinking Training L{level}",
        "name_label": "Name: {name}　|　{n} tasks",
        "answer_title": "Answers",
        "title_classify": "Classify", "title_match": "Matching", "title_same": "Same",
        "title_diff": "Odd One Out", "title_order": "Ordering", "title_pattern": "Patterns",
        "title_shape": "Shapes", "title_position": "Position", "title_compare": "Compare",
        "title_maze": "Maze", "title_swap": "Equal Swap",
        "instr_classify_color": "Circle all the {color} items.",
        "instr_classify_cat": "Circle all the {name}.",
        "instr_match": "Draw lines to match the same pictures (write the right-side number under each left picture).",
        "instr_same": "Two pictures are the same. Circle both of them.",
        "instr_diff": "One picture is different. Circle it.",
        "instr_order": "Put them in order from smallest to biggest. Write 1-5 under each picture.",
        "instr_pattern": "Look at the pattern. Draw or write the next picture(s) in the ? box(es).",
        "instr_shape": "Circle all the 「{shape}」.",
        "instr_position": "{a} is ( above / below / left / right ) of {b}? Circle the correct direction.",
        "instr_compare_count": "Which side has more? Count and write the number.",
        "instr_compare_height": "Put them from tallest to shortest. Write 1-3.",
        "instr_maze": "Find a path from the 🚪 entrance to the 🎁 exit.",
        "instr_swap": "Use the equation above to find how many ⭐ the ? equals. Write the number.",
        "ans_shape_prefix": "No. ", "ans_suffix": "",
        "ans_same_two": "No. {x} and No. {y}",
        "ans_order_prefix": "Order: ",
        "ans_pattern_prefix": "The ? are: ",
        "ans_position": "{a} is 「{d}」 of {b}",
        "ans_maze": "Free path — parent checks if it connects.",
        "ans_count_more": "{side} side has more ({n}).",
        "ans_swap_suffix": " ⭐",
        "name_label_prefix": "Name: ",
        "name_label_suffix": "　|　{n} tasks",
        "score_title": "Score",
        "score_points": "Score: ",
        "score_correct": "Correct: ",
        "score_comment": "Comments: ",
        "score_date": "Date: ",
        "score_total_suffix": " / {n}",
        "qcheck": "☐ right　☐ wrong",
        "brand": "Made with kindergarten-thinking-course v1.1",
    },
}

# 中文分隔符 / 英文分隔符，供生成器构造答案列表时使用
SEP = {"zh": "、", "en": ", "}
# 方位"左/右"在 compare 计数题里的中英表达
SIDE = {"zh": {"left": "左", "right": "右"}, "en": {"left": "left", "right": "right"}}
