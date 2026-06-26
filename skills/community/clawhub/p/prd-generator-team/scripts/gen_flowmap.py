#!/usr/bin/env python3
"""
页面流程图生成器 — PRD Generator Skill 标准脚本

自动读取截图目录，根据 flowmap-config.json 配置生成整体页面流程图 PNG。

用法:
  python gen_flowmap.py <项目目录>

参数:
  项目目录    PRD项目根目录（包含 prototype/screenshots/ 和 flowmap-config.json）

配置文件: flowmap-config.json（位于项目目录下）
  AI 在 Step 5 生成截图后，自动创建该配置文件，描述页面布局和连线关系。

配置文件格式:
{
  "title": "整体页面流程图 — 产品名称",
  "layers": [
    {"name": "入口层", "y_range": [90, 620]},
    {"name": "弹窗/中间层", "y_range": [640, 960]},
    ...
  ],
  "nodes": [
    {"id": "home", "label": "首页", "type": "page", "screenshot": "home.png", "col": 0, "layer": 0},
    {"id": "popup1", "label": "确认弹窗", "type": "popup", "col": 1, "layer": 1},
    {"id": "check1", "label": "判断", "type": "decision", "col": 2, "layer": 1},
    {"id": "boundary1", "label": "网络异常", "type": "boundary", "col": 0, "layer": 4},
    ...
  ],
  "connections": [
    {"from": "home", "to": "detail", "label": "点击卡片", "color": "normal"},
    {"from": "detail", "to": "popup1", "color": "popup", "label": "触发弹窗"},
    {"from": "check1", "to": "success", "color": "success", "label": "通过"},
    {"from": "check1", "to": "fail", "color": "convert", "label": "未通过"},
    {"from": "success", "to": "home", "color": "back", "label": "返回"},
    {"from": "boundary1", "to": "home", "color": "boundary", "label": "重试"},
    ...
  ]
}

节点类型(type):
  - page:     页面截图节点（需 screenshot 字段指向截图文件名）
  - popup:    弹窗节点（圆角矩形，浅蓝底色）
  - decision: 判断节点（菱形）
  - boundary: 边界条件节点（圆角矩形，浅橙底色）

连线颜色(color):
  - normal:   普通路径（绿色）
  - success:  成功路径（蓝色）
  - convert:  转化/付费路径（红色）
  - back:     回退路径（紫色）
  - popup:    弹窗触发（天蓝色）
  - boundary: 边界/异常（橙色）

输出: prototype/screenshots/page-flow-map.png
"""

import os
import sys
import json
from PIL import Image, ImageDraw, ImageFont

# ============== 常量 ==============

# 颜色定义
COLORS = {
    "normal":   (34, 139, 34),
    "success":  (0, 120, 215),
    "convert":  (220, 50, 50),
    "back":     (128, 0, 255),
    "popup":    (0, 162, 232),
    "boundary": (255, 140, 0),
}
C_TEXT      = (40, 40, 40)
C_LABEL     = (90, 100, 110)
C_LAYER_BG  = (248, 250, 252)
C_LAYER_BD  = (218, 223, 228)
BG_COLOR    = (255, 255, 255)

# 缩略图宽度
THUMB_W = 240

# 字体路径（NotoSansCJK — 禁止使用其他字体，否则中文乱码）
FONT_PATH = "/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc"
FONT_BOLD = "/usr/share/fonts/google-noto-cjk/NotoSansCJK-Bold.ttc"

# 列间距和行高等布局参数
COL_SPACING = 600        # 列间距
LAYER_PADDING_TOP = 60   # 层内顶部留白
LAYER_GAP = 20           # 层间间距
NODE_MARGIN = 60         # 画布边距


def get_font(size, bold=False):
    p = FONT_BOLD if bold and os.path.exists(FONT_BOLD) else FONT_PATH
    if not os.path.exists(p):
        print(f"WARNING: Font not found: {p}, falling back to default")
        return ImageFont.load_default()
    return ImageFont.truetype(p, size)


class FlowmapGenerator:
    def __init__(self, project_dir):
        self.project_dir = project_dir
        self.screenshots_dir = os.path.join(project_dir, "prototype", "screenshots")
        self.config_path = os.path.join(project_dir, "flowmap-config.json")
        self.output_path = os.path.join(self.screenshots_dir, "page-flow-map.png")

        # 字体
        self.ft_title  = get_font(36, bold=True)
        self.ft_layer  = get_font(24)
        self.ft_name   = get_font(20, bold=True)
        self.ft_node   = get_font(18)
        self.ft_arrow  = get_font(16)
        self.ft_legend = get_font(16)

        # 运行时数据
        self.config = None
        self.nodes = {}       # id -> node_info (with computed cx, cy, hw, hh)
        self.thumbs = {}      # id -> PIL Image
        self.img = None
        self.draw = None

    def load_config(self):
        if not os.path.exists(self.config_path):
            print(f"ERROR: Config file not found: {self.config_path}")
            print("AI should create flowmap-config.json before calling this script.")
            sys.exit(1)

        with open(self.config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)

        print(f"Loaded config: {len(self.config.get('nodes', []))} nodes, "
              f"{len(self.config.get('connections', []))} connections, "
              f"{len(self.config.get('layers', []))} layers")

    def load_thumbnails(self):
        """加载页面截图并生成缩略图（等比缩放）"""
        for node in self.config["nodes"]:
            if node["type"] == "page" and "screenshot" in node:
                fname = node["screenshot"]
                path = os.path.join(self.screenshots_dir, fname)
                if os.path.exists(path):
                    orig = Image.open(path).convert("RGB")
                    ow, oh = orig.size
                    th = int(oh * THUMB_W / ow)  # 等比缩放高度
                    self.thumbs[node["id"]] = orig.resize((THUMB_W, th), Image.LANCZOS)
                else:
                    print(f"WARNING: Screenshot not found: {path}, using placeholder")
                    self.thumbs[node["id"]] = Image.new("RGB", (THUMB_W, 424), (200, 200, 200))

    def compute_layout(self):
        """计算画布尺寸和节点坐标"""
        nodes_cfg = self.config["nodes"]
        layers_cfg = self.config.get("layers", [])

        # 计算列数
        max_col = max((n.get("col", 0) for n in nodes_cfg), default=0)
        num_cols = max_col + 1

        # 画布宽度
        self.canvas_w = max(3500, num_cols * COL_SPACING + 2 * NODE_MARGIN + 400)

        # 列X坐标（均匀分布）
        usable_w = self.canvas_w - 2 * NODE_MARGIN - 300  # 右侧留图例空间
        col_start = NODE_MARGIN + 150
        col_step = usable_w // max(num_cols, 1)
        self.col_x = [col_start + i * col_step for i in range(num_cols)]

        # 按层分组节点，计算每层所需高度
        layer_nodes = {}
        for n in nodes_cfg:
            layer_idx = n.get("layer", 0)
            if layer_idx not in layer_nodes:
                layer_nodes[layer_idx] = []
            layer_nodes[layer_idx].append(n)

        num_layers = len(layers_cfg) if layers_cfg else (max(layer_nodes.keys(), default=0) + 1)

        # 计算每层高度（根据该层最高节点）
        layer_heights = []
        for li in range(num_layers):
            max_h = 200  # 最小层高
            for n in layer_nodes.get(li, []):
                if n["type"] == "page" and n["id"] in self.thumbs:
                    th = self.thumbs[n["id"]].size[1]
                    max_h = max(max_h, th + 80)  # 截图高 + 标签 + 留白
                else:
                    max_h = max(max_h, 100)
            layer_heights.append(max_h)

        # 画布高度
        title_h = 80
        self.canvas_h = title_h + sum(layer_heights) + LAYER_GAP * (num_layers + 1) + 100

        # 计算层Y区间
        self.layer_rects = []
        y_cursor = title_h + LAYER_GAP
        for li in range(num_layers):
            y0 = y_cursor
            y1 = y_cursor + layer_heights[li]
            self.layer_rects.append((y0, y1))
            y_cursor = y1 + LAYER_GAP

        # 计算每个节点的中心坐标
        for n in nodes_cfg:
            nid = n["id"]
            col = n.get("col", 0)
            layer = n.get("layer", 0)

            cx = self.col_x[col] if col < len(self.col_x) else self.col_x[-1]

            # 层中心Y
            if layer < len(self.layer_rects):
                ly0, ly1 = self.layer_rects[layer]
                cy = (ly0 + ly1) // 2
            else:
                cy = self.canvas_h // 2

            # 节点半宽半高
            if n["type"] == "page" and nid in self.thumbs:
                tw, th = self.thumbs[nid].size
                hw = tw // 2 + 5
                hh = th // 2 + 5
            elif n["type"] == "decision":
                hw, hh = 48, 38
            else:
                label = n.get("label", "")
                hw = max(int(len(label) * 14 / 2) + 15, 55)
                hh = 18

            self.nodes[nid] = {
                "cx": cx, "cy": cy, "hw": hw, "hh": hh,
                "type": n["type"], "label": n.get("label", ""),
                "id": nid,
                "t": cy - hh, "b": cy + hh + (24 if n["type"] == "page" else 0),
                "l": cx - hw, "r": cx + hw,
            }

    def create_canvas(self):
        self.img = Image.new("RGB", (self.canvas_w, self.canvas_h), BG_COLOR)
        self.draw = ImageDraw.Draw(self.img)

    def draw_title(self):
        title = self.config.get("title", "整体页面流程图")
        tw = self.draw.textlength(title, font=self.ft_title)
        self.draw.text(((self.canvas_w - tw) / 2, 18), title, fill=C_TEXT, font=self.ft_title)

    def draw_layers(self):
        layers_cfg = self.config.get("layers", [])
        for i, (y0, y1) in enumerate(self.layer_rects):
            label = layers_cfg[i]["name"] if i < len(layers_cfg) else f"Layer {i}"
            self.draw.rounded_rectangle(
                [NODE_MARGIN, y0, self.canvas_w - NODE_MARGIN, y1],
                radius=10, fill=C_LAYER_BG, outline=C_LAYER_BD, width=1
            )
            self.draw.text((NODE_MARGIN + 12, y0 + 8), label, fill=C_LABEL, font=self.ft_layer)

    def draw_nodes(self):
        for nid, n in self.nodes.items():
            if n["type"] == "page":
                self._draw_page_node(nid, n)
            elif n["type"] == "popup":
                self._draw_popup_node(n)
            elif n["type"] == "decision":
                self._draw_decision_node(n)
            elif n["type"] == "boundary":
                self._draw_boundary_node(n)

    def _draw_page_node(self, nid, n):
        if nid not in self.thumbs:
            return
        thumb = self.thumbs[nid]
        tw, th = thumb.size
        x0 = n["cx"] - tw // 2
        y0 = n["cy"] - th // 2

        # 页面名称标签（上方）
        label = n["label"]
        lw = self.draw.textlength(label, font=self.ft_name)
        self.draw.text((n["cx"] - lw / 2, y0 - 28), label, fill=C_TEXT, font=self.ft_name)

        # 阴影 + 边框 + 缩略图
        self.draw.rectangle([x0 + 4, y0 + 4, x0 + tw + 4, y0 + th + 4], fill=(225, 225, 225))
        self.draw.rectangle([x0 - 2, y0 - 2, x0 + tw + 2, y0 + th + 2], outline=(170, 170, 170), width=2)
        self.img.paste(thumb, (x0, y0))

    def _draw_popup_node(self, n):
        label = n["label"]
        tw = self.draw.textlength(label, font=self.ft_node) + 24
        x0 = n["cx"] - tw / 2
        y0 = n["cy"] - 16
        self.draw.rounded_rectangle(
            [x0, y0, x0 + tw, y0 + 32], radius=8,
            fill=(230, 245, 255), outline=(0, 162, 232), width=2
        )
        self.draw.text((x0 + 12, y0 + 6), label, fill=(0, 120, 200), font=self.ft_node)

    def _draw_decision_node(self, n):
        sz = 30
        pts = [(n["cx"], n["cy"] - sz), (n["cx"] + sz + 10, n["cy"]),
               (n["cx"], n["cy"] + sz), (n["cx"] - sz - 10, n["cy"])]
        self.draw.polygon(pts, fill=(255, 248, 230), outline=(200, 150, 0), width=2)
        label = n["label"]
        tw = self.draw.textlength(label, font=self.ft_node)
        self.draw.text((n["cx"] - tw / 2, n["cy"] - 8), label, fill=C_TEXT, font=self.ft_node)

    def _draw_boundary_node(self, n):
        label = n["label"]
        tw = self.draw.textlength(label, font=self.ft_node) + 24
        x0 = n["cx"] - tw / 2
        y0 = n["cy"] - 16
        self.draw.rounded_rectangle(
            [x0, y0, x0 + tw, y0 + 32], radius=6,
            fill=(255, 243, 224), outline=(255, 140, 0), width=2
        )
        self.draw.text((x0 + 12, y0 + 6), label, fill=(200, 100, 0), font=self.ft_node)

    def draw_connections(self):
        for conn in self.config.get("connections", []):
            src_id = conn["from"]
            dst_id = conn["to"]
            if src_id not in self.nodes or dst_id not in self.nodes:
                print(f"WARNING: Connection {src_id} -> {dst_id}: node not found, skipping")
                continue

            src = self.nodes[src_id]
            dst = self.nodes[dst_id]
            color = COLORS.get(conn.get("color", "normal"), COLORS["normal"])
            label = conn.get("label", "")

            self._draw_auto_route(src, dst, color, label)

    def _draw_auto_route(self, src, dst, color, label):
        """自动路由：使用曼哈顿路由（正交折线），避免穿过节点"""
        sx, sy = src["cx"], src["cy"]
        dx, dy = dst["cx"], dst["cy"]

        # 简单路由策略
        if abs(sx - dx) < 10:
            # 同列，直线
            if dy > sy:
                pts = [(sx, src["b"]), (dx, dst["t"] - 24)]
            else:
                pts = [(sx, src["t"]), (dx, dst["b"])]
        elif abs(sy - dy) < 10:
            # 同行，直线
            if dx > sx:
                pts = [(src["r"], sy), (dst["l"], dy)]
            else:
                pts = [(src["l"], sy), (dst["r"], dy)]
        else:
            # 不同行不同列：L形或Z形路由
            mid_y = (src["b"] + dst["t"]) // 2 if dy > sy else (src["t"] + dst["b"]) // 2

            if dy > sy:
                # 向下走
                if dx > sx:
                    pts = [(src["r"], sy), (src["r"] + 30, sy), (src["r"] + 30, mid_y),
                           (dx, mid_y), (dx, dst["t"] - 24)]
                else:
                    pts = [(src["l"], sy), (src["l"] - 30, sy), (src["l"] - 30, mid_y),
                           (dx, mid_y), (dx, dst["t"] - 24)]
            else:
                # 向上走
                if dx > sx:
                    pts = [(src["r"], sy), (src["r"] + 30, sy), (src["r"] + 30, mid_y),
                           (dx, mid_y), (dx, dst["b"])]
                else:
                    pts = [(src["l"], sy), (src["l"] - 30, sy), (src["l"] - 30, mid_y),
                           (dx, mid_y), (dx, dst["b"])]

        self._draw_arrow_path(pts, color, label)

    def _draw_arrow_path(self, pts, color, label=None, lw=2):
        """绘制折线箭头"""
        for i in range(len(pts) - 1):
            self.draw.line([pts[i], pts[i + 1]], fill=color, width=lw)

        # 箭头
        x0, y0 = pts[-2]
        x1, y1 = pts[-1]
        sz = 10
        if x1 > x0:
            ah = [(x1, y1), (x1 - sz, y1 - sz // 2), (x1 - sz, y1 + sz // 2)]
        elif x1 < x0:
            ah = [(x1, y1), (x1 + sz, y1 - sz // 2), (x1 + sz, y1 + sz // 2)]
        elif y1 > y0:
            ah = [(x1, y1), (x1 - sz // 2, y1 - sz), (x1 + sz // 2, y1 - sz)]
        else:
            ah = [(x1, y1), (x1 - sz // 2, y1 + sz), (x1 + sz // 2, y1 + sz)]
        self.draw.polygon(ah, fill=color)

        # 标签
        if label:
            mid_idx = len(pts) // 2
            lx, ly = pts[mid_idx]
            tw = self.draw.textlength(label, font=self.ft_arrow)
            self.draw.rectangle([lx - 2, ly - 17, lx + tw + 2, ly - 1], fill=BG_COLOR)
            self.draw.text((lx, ly - 16), label, fill=color, font=self.ft_arrow)

    def draw_legend(self):
        lx = self.canvas_w - 320
        ly = 95
        items = [
            ("普通路径", COLORS["normal"]),
            ("成功路径", COLORS["success"]),
            ("转化/付费", COLORS["convert"]),
            ("回退路径", COLORS["back"]),
            ("弹窗触发", COLORS["popup"]),
            ("边界/异常", COLORS["boundary"]),
        ]
        self.draw.rounded_rectangle(
            [lx - 15, ly - 10, lx + 210, ly + len(items) * 28 + 8],
            radius=8, fill=BG_COLOR, outline=(200, 200, 200), width=1
        )
        for i, (text, color) in enumerate(items):
            y = ly + i * 28
            self.draw.line([(lx, y + 9), (lx + 40, y + 9)], fill=color, width=3)
            sz = 8
            ah = [(lx + 40, y + 9), (lx + 40 - sz, y + 9 - sz // 2), (lx + 40 - sz, y + 9 + sz // 2)]
            self.draw.polygon(ah, fill=color)
            self.draw.text((lx + 55, y), text, fill=color, font=self.ft_legend)

    def save(self):
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        self.img.save(self.output_path, optimize=True)
        sz = os.path.getsize(self.output_path)
        print(f"OK: {self.output_path} ({self.canvas_w}x{self.canvas_h}, {sz // 1024}KB)")

    def generate(self):
        """完整生成流程"""
        print(f"=== Page Flow Map Generator ===")
        print(f"Project: {self.project_dir}")

        self.load_config()
        self.load_thumbnails()
        self.compute_layout()
        self.create_canvas()
        self.draw_title()
        self.draw_layers()
        self.draw_nodes()
        self.draw_connections()
        self.draw_legend()
        self.save()

        print("Done!")


def main():
    if len(sys.argv) < 2:
        print("Usage: python gen_flowmap.py <项目目录>")
        print("Example: python gen_flowmap.py /data/workspace/.codebuddy/docs/prd/my-project")
        sys.exit(1)

    project_dir = sys.argv[1]
    if not os.path.isdir(project_dir):
        print(f"ERROR: Directory not found: {project_dir}")
        sys.exit(1)

    gen = FlowmapGenerator(project_dir)
    gen.generate()


if __name__ == "__main__":
    main()
