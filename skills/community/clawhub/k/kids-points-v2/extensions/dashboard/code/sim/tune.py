"""排版微调助手 (M1.1 v1.3+).

用法:
  /usr/bin/python3.10 tune.py                                       # baseline (用 desktop_sim.py 当前参数)
  /usr/bin/python3.10 tune.py --title-font 48 --row-font 32         # 字号改大
  /usr/bin/python3.10 tune.py --row1-y 24 --row2-y 40 --row3-y 56  # 流水上移
  /usr/bin/python3.10 tune.py --fg 255,180,0 --dim 140,90,0         # 配色
  /usr/bin/python3.10 tune.py --out /tmp/sim_tune.png               # 自定义输出

原理: monkey-patch desktop_sim 的常量, 然后调一次 render_frame_to_surface 出图.
     调完不写回 desktop_sim.py, 老王觉得 OK 再手动改顶部常量.
"""

import argparse
import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")  # 无窗口跑图

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pygame
import desktop_sim as sim


def parse_color(s: str) -> tuple:
    """'R,G,B' 字符串 → (R, G, B) tuple. 例: '255,140,0' → (255, 140, 0)."""
    parts = [int(x.strip()) for x in s.split(",")]
    assert len(parts) == 3, f"--fg 必须是 'R,G,B' 格式, 收到 {s!r}"
    for p in parts:
        assert 0 <= p <= 255, f"颜色值必须 0-255, 收到 {p}"
    return tuple(parts)


def apply_overrides(args):
    """把命令行参数 monkey-patch 到 desktop_sim 常量.

    顺序: 先 set_orientation (切横/竖, 改 字号+4 区 y 默认值),
          再用 args.XXX 覆盖 (如果用户传了). 如果用户没传, 保留 set_orientation 设置的值.
    """
    # 1) 切横/竖 (这一步会改 sim.WIDTH/HEIGHT/字号/4 区 y)
    orient = sim.set_orientation(args.orientation)
    print(f"  切换 orientation: {orient} (WIDTH={sim.WIDTH}, HEIGHT={sim.HEIGHT})")

    # 2) 字号 / 4 区 y — 规则: 用户传了 (非 None) 就覆盖, 没传 (None) 保留 set_orientation 默认
    # argparse default 全部为 None, main() 里在 set_orientation 之后用 sim 当前值
    def maybe_set(name, value):
        if value is not None:
            setattr(sim, name, value)
            print(f"  覆盖 {name} = {value}")
        else:
            print(f"  保留 {name} = {getattr(sim, name)} (orientation {orient} 默认)")

    maybe_set("TITLE_FONT_PX", args.title_font)
    maybe_set("ROW_FONT_PX", args.row_font)
    maybe_set("FOOTER_FONT_PX", args.footer_font)
    maybe_set("TITLE_Y", args.title_y)
    maybe_set("DIVIDER_1_Y", args.divider1_y)
    maybe_set("ROW_1_Y", args.row1_y)
    maybe_set("ROW_2_Y", args.row2_y)
    maybe_set("ROW_3_Y", args.row3_y)
    maybe_set("DIVIDER_2_Y", args.divider2_y)
    maybe_set("FOOTER_Y", args.footer_y)
    maybe_set("BG_COLOR", parse_color(args.bg))
    maybe_set("FG_COLOR", parse_color(args.fg))
    maybe_set("DIM_COLOR", parse_color(args.dim))
    maybe_set("ERROR_COLOR", parse_color(args.err))
    return None


def main():
    p = argparse.ArgumentParser(
        description="M1.1 排版微调助手 (跑 1 张图, 不改 desktop_sim.py)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
示例:
  # 横向 (默认 128×96)
  tune.py --title-font 48 --row-font 32 --footer-font 28

  # 竖向 (96×128, 板旋转 90°)
  tune.py --orientation vertical

  # 竖向 + 字号改大
  tune.py --orientation vertical --title-font 48 --row-font 32

  # 流水上移 4 像素
  tune.py --row1-y 24 --row2-y 40 --row3-y 56 --divider2-y 74 --footer-y 78

  # 配色 (琥珀变浅)
  tune.py --fg 255,180,0 --dim 140,90,0

  # 错误色变纯红
  tune.py --err 255,0,0
""",
    )
    # 输出
    p.add_argument("--orientation", choices=["horizontal", "vertical"], default="horizontal",
                   help="横竖切换 (默认 horizontal 128×96, vertical 96×128). 切完字号+4 区 y 默认值跟着变")
    # 字号 / 4 区 y 默认 None, main() 内部在 set_orientation 后用 sim 当前值 (避免模块导入时锁 horizontal 默认覆盖 vertical)
    p.add_argument("--title-font", type=int, default=None, help="标题字号 (屏像素, 默认跟 orient 走: 36)")
    p.add_argument("--row-font", type=int, default=None, help="流水字号 (屏像素, 默认跟 orient 走: 24)")
    p.add_argument("--footer-font", type=int, default=None, help="底栏字号 (屏像素, 默认跟 orient 走: 横向 20, 竖向 24)")
    p.add_argument("--title-y", type=int, default=None, help="标题顶部 y (物理像素, 默认跟 orient 走)")
    p.add_argument("--divider1-y", type=int, default=None, help="上分隔线 y (物理像素, 默认跟 orient 走)")
    p.add_argument("--row1-y", type=int, default=None, help="流水 1 y (物理像素, 默认跟 orient 走)")
    p.add_argument("--row2-y", type=int, default=None, help="流水 2 y (物理像素, 默认跟 orient 走)")
    p.add_argument("--row3-y", type=int, default=None, help="流水 3 y (物理像素, 默认跟 orient 走)")
    p.add_argument("--divider2-y", type=int, default=None, help="下分隔线 y (物理像素, 默认跟 orient 走)")
    p.add_argument("--footer-y", type=int, default=None, help="底栏顶部 y (物理像素, 默认跟 orient 走)")
    # 配色
    p.add_argument("--bg", type=str, default="0,0,0", help="背景色 'R,G,B' (默认 '0,0,0' 黑底)")
    p.add_argument("--fg", type=str, default="255,140,0", help="主色 'R,G,B' (默认 '255,140,0' 琥珀)")
    p.add_argument("--dim", type=str, default="120,70,0", help="暗色 (占位) 'R,G,B' (默认 '120,70,0')")
    p.add_argument("--err", type=str, default="200,30,0", help="错误色 'R,G,B' (默认 '200,30,0' 暗红)")
    # 输出
    p.add_argument("--out", type=str, default=None, help="输出 PNG 路径 (默认 /tmp/sim_tune_<orientation>.png)")
    p.add_argument("--mock", choices=["sparse", "promoted", "error"], default="sparse",
                   help="用哪个 mock 数据 (默认 sparse = V2 production DB 当前真实数据)")

    args = p.parse_args()

    print(f"=== tune.py 调参 ===")
    apply_overrides(args)
    print()

    # 初始化 pygame + 字体 (在 monkey-patch 之后, 拿新字号)
    pygame.init()
    fonts = sim.init_fonts()

    # 拿数据
    if args.mock == "sparse":
        data = sim.fetch_data()
    elif args.mock == "promoted":
        data = {
            "title": "KID POINTS", "total_balance": 19, "today_count": 4, "today_net": 2,
            "recent": [
                {"date": "06-14", "type": "+", "amount": 6, "description": "跳绳+口算"},
                {"date": "06-14", "type": "-", "amount": 5, "description": "吃萨莉亚"},
                {"date": "06-10", "type": "+", "amount": 3, "description": "ABC Reading"},
            ],
            "last_updated": "2026-06-14T22:30:00",
        }
    else:  # error
        data = {
            "title": "KID POINTS",
            "_error": "V2 CLI 不可用, 显示占位",
            "recent": [], "total_balance": None, "today_count": 0, "today_net": 0,
        }

    # 屏画布 (跟 set_orientation 后的 WIDTH/HEIGHT 匹配)
    screen = pygame.display.set_mode((sim.WIDTH * sim.PIXEL_SIZE, sim.HEIGHT * sim.PIXEL_SIZE))
    sim.render_frame_to_surface(screen, data, fonts)

    # 默认输出路径: /tmp/sim_tune_<orientation>_<mock>.png
    out_path = args.out or f"/tmp/sim_tune_{args.orientation}_{args.mock}.png"
    pygame.image.save(screen, out_path)
    args.out = out_path  # 让后面报告用上

    # 报告
    print(f"=== 输出 ===")
    print(f"  mock: {args.mock}")
    print(f"  PNG: {args.out}")
    if not data.get("_error"):
        print(f"  data: balance={data['total_balance']}, today_count={data['today_count']}, today_net={data['today_net']}, recent={len(data['recent'])} 行")
    else:
        print(f"  data: 错误状态")

    # 物理 1:1 验证 (跟 v1.3 同款, 但用新字号)
    import numpy as np
    arr = pygame.surfarray.array3d(screen).swapaxes(0, 1)
    amber = (arr[:,:,0] > 200) & (arr[:,:,1] > 50) & (arr[:,:,1] < 200) & (arr[:,:,2] < 50)
    # 4 区 amber 像素统计
    zones = [
        ("title ", sim.TITLE_Y, sim.DIVIDER_1_Y),
        ("row1  ", sim.ROW_1_Y, sim.ROW_2_Y),
        ("row2  ", sim.ROW_2_Y, sim.ROW_3_Y),
        ("row3  ", sim.ROW_3_Y, sim.DIVIDER_2_Y),
        ("footer", sim.FOOTER_Y, sim.HEIGHT),
    ]
    print()
    print("=== 各区 amber 像素 (验证字号是否爆框) ===")
    for name, y1, y2 in zones:
        s1, s2 = y1 * sim.PIXEL_SIZE, y2 * sim.PIXEL_SIZE
        count = amber[s1:s2].sum()
        status = "✓" if count > 100 else "✗ 空!"
        print(f"  {name} 物理 y={y1}-{y2} (屏 {s1}-{s2}): {count} px {status}")


if __name__ == "__main__":
    main()
