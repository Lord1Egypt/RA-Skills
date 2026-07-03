"""
儿童积分看板 — 桌面 dashboard 仿真 (M1.1 v1, 2026-06-14)

物理: 128×96 像素 (¥190 P2 128×96, 11" 4:3, 256×192mm)
数据: kids-points V2 CLI 3 接口 (balance / today / history)
配色: 黑底 + 琥珀 (R=255, G=140, B=0), 关蓝 (B=0)

业务代码 (render_frame) 跟硬件版 ESP32 C++ 共享, 上硬件时只换输出端.
仿真版 (pygame): 1 像素 = PIXEL_SIZE 屏像素, 整屏 768×576 桌面可见.

按 R 重拉 V2 数据, 按 S 截图 (M1.1 v1 视觉验证用), 按 ESC/Q 退出.
"""
import json
import os
import subprocess
import sys
import time
from typing import Optional

import pygame

# ==================== 物理参数 (跟 plan.md § 5 完全一致) ====================

# 仿真基础参数 (横竖共用)
PIXEL_SIZE = 6    # 仿真 1 物理像素 = 6 屏像素
FPS = 10          # 仿真帧率 (看板不需要更高)
SIM_SCALE = PIXEL_SIZE  # 6

# 仿真 SysFont 字号注释 (跟 plan.md § 5 物理像素近似 1:1, M1.3 上真 bdf)
# 字号 N 屏, 字符框 ~1.4N 屏; 选字号让字符框 < 区高屏 (留 padding)
# 真物理 bdf 字符: title 12 物理 / row 8 物理 / footer 10 物理

# 横/竖 2 套物理布局 + 字号配置 (M1.1 排版微调)
# 切换方法: tune.py --orientation {horizontal,vertical} (临时) 或 set_orientation() (代码)
# 选定后写回方式 B 持久: 改下面 2 个字典后, 把 DEFAULT_ORIENTATION 改一改
ORIENTATION_CONFIGS = {
    "horizontal": {
        # 物理 128×96 (11 寸 4:3 横版, ¥190 P2 板默认朝向)
        "WIDTH": 128, "HEIGHT": 96,
        "TITLE_FONT_PX": 36,    # 6 物理字符
        "ROW_FONT_PX": 24,      # 4 物理字符
        "FOOTER_FONT_PX": 20,   # 3.3 物理字符
        "TITLE_Y": 4, "DIVIDER_1_Y": 22,
        "ROW_1_Y": 28, "ROW_2_Y": 44, "ROW_3_Y": 60,   # 16 物理 / 行
        "DIVIDER_2_Y": 78, "FOOTER_Y": 82,            # 底栏 12 物理高
    },
    "vertical": {
        # 物理 96×128 (11 寸 3:4 竖版, 板旋转 90° 安装)
        "WIDTH": 96, "HEIGHT": 128,
        "TITLE_FONT_PX": 36,    # 6 物理字符 (跟横向一致, 标题醒目)
        "ROW_FONT_PX": 24,      # 4 物理字符 (advance 4 物理, 流水 20 字符完整装 96 屏宽)
        "FOOTER_FONT_PX": 24,   # 4 物理字符 (跟 row 一致)
        "TITLE_Y": 4, "DIVIDER_1_Y": 26,
        "ROW_1_Y": 32, "ROW_2_Y": 56, "ROW_3_Y": 80,   # 24 物理 / 行 (比横 16 大 50%)
        "DIVIDER_2_Y": 108, "FOOTER_Y": 112,           # 底栏 16 物理高
    },
}

# 顶部常量 (默认横向 v1.3, 兼容老代码直接 import sim.WIDTH / sim.TITLE_Y)
DEFAULT_ORIENTATION = "horizontal"
WIDTH = ORIENTATION_CONFIGS[DEFAULT_ORIENTATION]["WIDTH"]
HEIGHT = ORIENTATION_CONFIGS[DEFAULT_ORIENTATION]["HEIGHT"]
TITLE_FONT_PX = ORIENTATION_CONFIGS[DEFAULT_ORIENTATION]["TITLE_FONT_PX"]
ROW_FONT_PX = ORIENTATION_CONFIGS[DEFAULT_ORIENTATION]["ROW_FONT_PX"]
FOOTER_FONT_PX = ORIENTATION_CONFIGS[DEFAULT_ORIENTATION]["FOOTER_FONT_PX"]
TITLE_Y = ORIENTATION_CONFIGS[DEFAULT_ORIENTATION]["TITLE_Y"]
DIVIDER_1_Y = ORIENTATION_CONFIGS[DEFAULT_ORIENTATION]["DIVIDER_1_Y"]
ROW_1_Y = ORIENTATION_CONFIGS[DEFAULT_ORIENTATION]["ROW_1_Y"]
ROW_2_Y = ORIENTATION_CONFIGS[DEFAULT_ORIENTATION]["ROW_2_Y"]
ROW_3_Y = ORIENTATION_CONFIGS[DEFAULT_ORIENTATION]["ROW_3_Y"]
DIVIDER_2_Y = ORIENTATION_CONFIGS[DEFAULT_ORIENTATION]["DIVIDER_2_Y"]
FOOTER_Y = ORIENTATION_CONFIGS[DEFAULT_ORIENTATION]["FOOTER_Y"]


def set_orientation(orient: str = "horizontal") -> str:
    """切换横/竖物理布局. 改模块全局常量 (WIDTH / HEIGHT / 4 区 y / 字号).

    切换后必须重新调 init_fonts() (新字号) + pygame.display.set_mode() (新 W×H×PIXEL_SIZE).

    Args:
        orient: "horizontal" (128×96) 或 "vertical" (96×128)

    Returns:
        实际设置的 orient (兜底返 DEFAULT_ORIENTATION).
    """
    assert orient in ORIENTATION_CONFIGS, f"orientation 必须是 {list(ORIENTATION_CONFIGS.keys())} 之一, 收到 {orient!r}"
    cfg = ORIENTATION_CONFIGS[orient]
    for k, v in cfg.items():
        globals()[k] = v
    return orient


# 护眼配色 (黑底 + 琥珀 + 关蓝 B=0, 横竖共用)
BG_COLOR = (0, 0, 0)
FG_COLOR = (255, 140, 0)         # 琥珀
DIM_COLOR = (120, 70, 0)         # 暗琥珀 (占位/等待)
ERROR_COLOR = (200, 30, 0)       # 红色 (错误提示, 调试用)

# ==================== V2 CLI 路径配置 ====================

V2_CLI = "/home/wang/projects/kids-points-v2/runtime/cli.py"
CACHE_FILE = "/tmp/dashboard_cache.json"
CLI_TIMEOUT = 5  # 5s, V2 CLI 纯读, 正常 < 0.1s

# ==================== 字体 (仿真用 pygame 像素字体, M1.3 上真 bdf) ====================

# 中英文字体回退链: 优先 noto sans cjk (老王桌面 Linux 多数有装), 回退 wqy / dejavu
FONT_FAMILY = "notosanscjksc,notosansmonocjksc,notosansmono,wqy-microhei,wqy-zenhei,dejavusansmonospace,monospace"


# ==================== V2 CLI 包装 (跟 § 3 / § 8 data_source.py 同款, M1.2 抽出) ====================

def cli_call(subcmd: list, timeout: int = CLI_TIMEOUT) -> Optional[dict]:
    """调 V2 CLI 子命令, 返 dict. 失败返 None."""
    try:
        result = subprocess.run(
            ["python3", V2_CLI] + subcmd,
            capture_output=True, text=True, timeout=timeout,
        )
        if result.returncode != 0:
            print(f"[cli_call] {subcmd} exit {result.returncode}: {result.stderr[:200]}", file=sys.stderr)
            return None
        return json.loads(result.stdout)
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError) as e:
        print(f"[cli_call] {subcmd} 失败: {e}", file=sys.stderr)
        return None


def fetch_data() -> dict:
    """拉 V2 数据组装成 § 4 dashboard JSON Schema.

    V2 production DB 数据稀疏 (V2 promotion 前) → today/history 可能返 0, 板显示"等待" 占位.
    失败兜底: 读 /tmp/dashboard_cache.json (上次成功拉的), 都没有 → 返全占位.
    """
    balance_data = cli_call(["balance"])
    today_data = cli_call(["today"])
    history_data = cli_call(["history", "--days", "1", "--limit", "3"])

    # 失败兜底: 读 cache
    if not balance_data or not today_data:
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE) as f:
                    cached = json.load(f)
                if cached.get("balance") is not None and cached.get("today") is not None:
                    print(f"[fetch_data] V2 CLI 失败, 用 cache {CACHE_FILE}")
                    balance_data = cached["balance"]
                    today_data = cached["today"]
                    history_data = history_data or cached.get("history") or {"history": []}
            except Exception as e:
                print(f"[fetch_data] cache 读失败: {e}")

    # 全部失败 → 返全占位
    if not balance_data or not today_data:
        return {
            "title": "KID POINTS",
            "total_balance": None,
            "today_count": 0,
            "today_net": 0,
            "recent": [],
            "last_updated": None,
            "_error": "V2 CLI 不可用, 显示占位",
        }

    # 类型符号映射 (V2 type → dashboard +/-)
    recent = []
    for tx in (history_data or {}).get("history", []):
        recent.append({
            "date": tx["date"][5:] if tx.get("date", "").startswith("20") else tx.get("date", ""),  # YYYY-MM-DD → MM-DD
            "type": "+" if tx.get("type") == "income" else "-",
            "amount": abs(tx.get("amount", 0)),
            "description": tx.get("description", ""),
        })

    out = {
        "title": "KID POINTS",
        "total_balance": balance_data.get("balance"),
        "today_count": today_data.get("tx_count", 0),
        "today_net": today_data.get("net", 0),
        "recent": recent,
        "last_updated": balance_data.get("as_of"),
    }

    # 写 cache (下次失败兜底)
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump({"balance": balance_data, "today": today_data, "history": history_data}, f)
    except Exception as e:
        print(f"[fetch_data] cache 写失败: {e}")

    return out


# ==================== 渲染 (业务代码, ESP32 C++ 端同款结构) ====================

def render_frame_to_surface(surface: pygame.Surface, data: dict, fonts: dict) -> None:
    """仿真渲染入口. surface 是屏画布 768×576 (WIDTH*PIXEL_SIZE × HEIGHT*PIXEL_SIZE).

    渲染策略: 抛弃 pygame 在物理画布 (128×96) blit 时奇怪的 TTF 错位 (实测 SysFont 60 blit 物理
    y=4 字符 ink 实际 y=30, 差 26 物理), 改**直接 blit 到屏画布**, 字号按屏像素选, blit 屏 y
    = 物理 y × 6. 这样能精确控制字符 ink 位置, blit 行为可预测.

    业务逻辑跟 ESP32 端 render_frame 共用 (数据流一致, 只换输出端).
    ESP32 端伪代码 (M1.3 实施):
        void render_frame(MatrixPanel_DMA *dma, const DashboardData &data) {
            draw_text(dma, data.title, 4, TITLE_Y, AMBER, 12px);
            draw_hline(dma, 0, DIVIDER_1_Y, WIDTH, AMBER);
            for (int i = 0; i < 3; i++) {
                draw_row(dma, data.recent[i], ROW_1_Y + i*16, 8px);
            }
            draw_hline(dma, 0, DIVIDER_2_Y, WIDTH, AMBER);
            draw_text(dma, footer, 4, FOOTER_Y, AMBER, 10px);
        }
    """
    surface.fill(BG_COLOR)
    fg = FG_COLOR
    dim = DIM_COLOR
    PAD = 4 * PIXEL_SIZE  # 物理 4 像素 padding → 屏 24 像素

    def y(physical_y):
        """物理 y 坐标 → 屏 y 坐标."""
        return physical_y * PIXEL_SIZE

    def w(physical_w):
        """物理宽度 → 屏宽度 (用于分隔线)."""
        return physical_w * PIXEL_SIZE

    def text(text_str, font, color, y_phy):
        """在物理 y_phy (字符框顶) blit 文字到 surface (屏画布)."""
        return surface.blit(font.render(text_str, True, color), (PAD, y(y_phy)))

    # 错误状态
    if data.get("_error"):
        text(data["title"], fonts["title"], fg, TITLE_Y)
        text(data["_error"], fonts["row"], ERROR_COLOR, ROW_2_Y)
        # 错误状态底栏也画 (v1.1 修复, 避免板显示"标题 + 错误 + 空底栏" 误导)
        text("今日 --     总 --", fonts["footer"], fg, FOOTER_Y)
        return

    # === 1. 标题 ===
    text(data["title"], fonts["title"], fg, TITLE_Y)

    # === 2. 分隔线 ===
    pygame.draw.line(surface, fg, (0, y(DIVIDER_1_Y)), (w(WIDTH), y(DIVIDER_1_Y)), PIXEL_SIZE)
    pygame.draw.line(surface, fg, (0, y(DIVIDER_2_Y)), (w(WIDTH), y(DIVIDER_2_Y)), PIXEL_SIZE)

    # === 3. 3 行流水 ===
    for i in range(3):
        row_y = [ROW_1_Y, ROW_2_Y, ROW_3_Y][i]
        if i < len(data["recent"]):
            tx = data["recent"][i]
            sign = tx["type"]
            amount = f"{sign}{tx['amount']}"
            date = tx["date"]  # MM-DD
            desc = tx["description"][:12]  # 128px 宽, SysFont 24 advance 24/6=4 物理, 12 字符 = 48 物理 OK
            row_text = f"{amount:>3} {date} {desc}"
            text(row_text, fonts["row"], fg, row_y)
        else:
            placeholder = f"  -    --  [等待 V2 飞书消息]" if i == 0 else f"  -    --  "
            text(placeholder, fonts["row"], dim, row_y)

    # === 4. 底栏 ===
    if data["today_count"] > 0:
        footer_text = f"今日 +{data['today_net']}      总 {data['total_balance']}"
    else:
        footer_text = f"今日 --     总 {data['total_balance'] if data['total_balance'] is not None else '--'}"
    text(footer_text, fonts["footer"], fg, FOOTER_Y)


# ==================== 仿真主循环 ====================

def init_fonts() -> dict:
    """初始化 3 套 SysFont 字体 (按屏像素选字号, 跟 4 区物理高度匹配).

    M1.3 替换为 ESP32 bdf 字库 (跟 home-dashboard-display/skill 模板一致).
    中英文字体回退链: notosans* → wqy* → dejavu → monospace.
    """
    return {
        "title": pygame.font.SysFont(FONT_FAMILY, TITLE_FONT_PX, bold=True),    # 屏 36 = 物理 6 字符
        "row": pygame.font.SysFont(FONT_FAMILY, ROW_FONT_PX),                    # 屏 24 = 物理 4 字符
        "footer": pygame.font.SysFont(FONT_FAMILY, FOOTER_FONT_PX, bold=True),   # 屏 20 = 物理 3.3 字符
    }


def main() -> int:
    pygame.init()
    pygame.display.set_caption(f"Kids Points Dashboard 仿真 {WIDTH}×{HEIGHT} (pygame)")
    screen = pygame.display.set_mode((WIDTH * PIXEL_SIZE, HEIGHT * PIXEL_SIZE))
    clock = pygame.time.Clock()
    fonts = init_fonts()

    # 启动时拉 1 次数据
    data = fetch_data()
    last_reload = time.time()
    RELOAD_INTERVAL = 30  # 30s 跟 ESP32 端拉频率一致 (仿真预览够用)

    running = True
    while running:
        # === 事件 ===
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif event.key == pygame.K_r:
                    print("[main] R: 重新拉 V2 数据")
                    data = fetch_data()
                    last_reload = time.time()
                elif event.key == pygame.K_s:
                    # 截图: 给老王看视觉 (M1.1 验证用)
                    screenshot_path = f"/tmp/dashboard_sim_{int(time.time())}.png"
                    pygame.image.save(screen, screenshot_path)
                    print(f"[main] S: 截图已存 {screenshot_path}")

        # === 定时重拉 (跟 ESP32 端 30s 拉一致) ===
        if time.time() - last_reload > RELOAD_INTERVAL:
            data = fetch_data()
            last_reload = time.time()

        # === 渲染: 直接画到屏画布 (无 transform.scale, 避免 pygame SysFont blit 物理画布的 TTF 错位) ===
        render_frame_to_surface(screen, data, fonts)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())
