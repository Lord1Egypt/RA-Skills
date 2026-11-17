#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""新建「人物说唱视频」项目骨架（四角色前置 · 四份记录）。

用法：
  python3 scripts/new_project.py --slug xiaoyu
  python3 scripts/new_project.py --slug xiaoyu --duration 40
  python3 scripts/new_project.py --slug xiaoyu --image ~/Desktop/me.jpg

产物：
  assets/output/MV01-xiaoyu/
  ├── 00-项目状态.md
  ├── 00-过程记录.md                 # 每站一块：角色/输入/产出/决策/待确认
  ├── 00-输入/素材/<原文件名>        # 用户原图归档（有图时）
  ├── 00-输入/音频/                  # 说唱音频（待放入 / 出曲后回传）
  ├── 00-输入/需求卡.md
  ├── 01-解读/                       # ① 任务解读官
  ├── 02-方案/                       # ② 创意总监 / ③ 钩子官 / ④ 词作者 / ⑦ 时间轴
  ├── 03-上传/
  ├── 04-图片/ref_人物.<ext>         # 出片用的参考图（有图时由原图复制）
  ├── 04-提示词/
  ├── 成片片段/
  └── 06-质检/
  并更新 assets/output/项目登记.md
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import OUTPUT_ROOT  # noqa: E402

IMG_EXTS = (".png", ".jpg", ".jpeg", ".webp")


def next_id() -> str:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    nums = []
    for p in OUTPUT_ROOT.iterdir():
        m = re.match(r"MV(\d+)", p.name)
        if m:
            nums.append(int(m.group(1)))
    return f"MV{(max(nums) + 1) if nums else 1:02d}"


def safe_slug(slug: str) -> str:
    text = re.sub(r"[^0-9A-Za-z_\-\u4e00-\u9fff]+", "-", slug.strip()).strip("-")
    return text or datetime.now().strftime("%Y%m%d-%H%M%S")


def write_registry(project_id: str, project_name: str, rel: str, step: str, duration: str = "—") -> None:
    path = OUTPUT_ROOT / "项目登记.md"
    header = (
        "# 人物说唱视频 · 项目登记\n\n"
        "| 项目ID | 项目名 | 时长 | 当前步骤 | 状态 | 输出目录 |\n"
        "|--------|--------|------|----------|------|----------|\n"
    )
    if not path.is_file():
        path.write_text(header, encoding="utf-8")
    else:
        old = path.read_text(encoding="utf-8")
        if old.splitlines() and not old.splitlines()[0].startswith("# 人物说唱视频"):
            lines = old.splitlines()
            lines[0] = "# 人物说唱视频 · 项目登记"
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    line = f"| {project_id} | {project_name} | {duration} | {step} | ⏸待确认 | `{rel}` |\n"
    with path.open("a", encoding="utf-8") as f:
        f.write(line)


def main() -> None:
    ap = argparse.ArgumentParser(description="新建人物说唱视频项目")
    ap.add_argument("--slug", default="", help="项目短名（英文/拼音/中文均可，默认时间戳）")
    ap.add_argument("--duration", type=int, default=30, choices=[30, 40, 60],
                    help="目标档位：30/40/60 秒（成片长度永远＝音频实际长度）")
    ap.add_argument("--ratio", default="9:16", choices=["9:16", "16:9", "1:1", "3:4", "4:3"],
                    help="画幅（默认 9:16）")
    ap.add_argument("--image", default="", help="用户人物图片路径（可选）")
    args = ap.parse_args()

    project_id = next_id()
    slug = safe_slug(args.slug)
    name = f"{project_id}-{slug}"
    project = OUTPUT_ROOT / name
    for sub in ("00-输入/素材", "00-输入/音频", "01-解读", "02-方案", "03-上传",
                "04-图片", "04-提示词", "成片片段", "06-质检"):
        (project / sub).mkdir(parents=True, exist_ok=True)

    img_note = "用户提供"
    if args.image:
        src = Path(args.image).expanduser().resolve()
        if not src.is_file():
            sys.exit(f"[FAIL] 图片不存在：{src}")
        if src.suffix.lower() not in IMG_EXTS:
            sys.exit(f"[FAIL] 只支持图片：{', '.join(IMG_EXTS)}；收到 {src.suffix}")
        shutil.copy2(src, project / "00-输入" / "素材" / src.name)
        ref_name = "ref_人物" + src.suffix.lower()
        shutil.copy2(src, project / "04-图片" / ref_name)
        img_note = f"用户提供（00-输入/素材/{src.name} → 04-图片/{ref_name}）"
    else:
        (project / "04-图片").mkdir(parents=True, exist_ok=True)
        img_note = "未提供，待生成「重彩水墨轻鎏金」参考图"

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    state = f"""# 项目状态 · {name}

【项目】{name} — 人物说唱视频（{args.ratio} · 目标 {args.duration}s 档 · 按音频拆镜）
【输入】人物/主题：待写进 00-输入/需求卡.md
【输入】人物图：{img_note}
【输入】说唱音频：无（待 ④ 定稿后出曲回传；有音频则直接进 ⑤ 切分）
【目标】让图片里的人跟着这条音频开口说唱，成片长度＝人声原速长度
【当前步骤】⓪ 项目初始化完成
【已完成】⓪ 建档 ✅
【待执行】① 解读任务（任务解读官）→ ② 出方案（创意总监）→ ③ 写钩子句（钩子官）→ ④ 写歌词（词作者）
          → ⑤ 素材/出曲 → ⑥ 上传外网（硬门）→ ⑦ 时间轴+提示词 → ⑧ 出片合成 → ⑨ 质检交付
【最近更新】{now}
【用户最近意见】-
"""
    (project / "00-项目状态.md").write_text(state, encoding="utf-8")

    brief = f"""# 需求卡 · {name}

## 用户描述（原话，逐字）
- 待补充

## 一句话任务
- 待 ① 任务解读官填写

## 硬约束（随任务书更新）
- 目标档位：{args.duration}s（成片长度＝音频实际长度）
- 画幅：{args.ratio}
- 镜头：单镜一镜到底；超过 30 秒自动拆镜
- 声音：用参考音频驱动口型（generate_audio: false）
- 开头：2 秒内开口说唱

## 素材状态
- 人物图：{img_note}
- 音频：无（待出曲）／有（待切分）

## 待确认
- [ ] 人物/主题具体指哪一个（同名/版本差异）
- [ ] 想让人记住哪一句话
- [ ] 时长档位 30s / 40s
- [ ] 人物授权（本人 / 已授权 / AI 生成 / 神话人物）
- [ ] 是否要字幕

## 记录纪律
- ①–④ 每站一份文件，写进 01-解读/ 与 02-方案/
- 每站结束用 `python3 scripts/log_step.py <项目> ...` 追加 00-过程记录.md
"""
    (project / "00-输入" / "需求卡.md").write_text(brief, encoding="utf-8")

    log = f"""# 过程记录 · {name}

> 每站一块，由 `scripts/log_step.py` 追加。换会话继续时，先读最后一块。

## ⓪ 建档 · {now}
- 角色：项目管家
- 输入：slug={slug} · 目标档位={args.duration}s · 画幅={args.ratio}
- 产出：00-项目状态.md / 00-输入/需求卡.md / 目录骨架
- 关键决策：项目初始化，未做任何创作判断
- 待确认：人物/主题、时长档位、素材状态
- 下一步：① 解读任务（任务解读官）
"""
    (project / "00-过程记录.md").write_text(log, encoding="utf-8")

    (project / "01-解读" / "01-任务书.md").write_text(
        f"""# 任务书 · {name}

> 由 ① 任务解读官填写。模板见 `references/01-任务解读与方案.md` 1.3。

## 1. 用户原话
> 待补充

## 2. 一句话任务
待填写。

## 3. 已知项
| 项 | 取值 | 来源 |
|---|---|---|
| 人物/主题 | 待补充 | 用户原话 |
| 用途 | 待确认 | — |
| 时长 | {args.duration}s 档 | 默认 |
| 画幅 | {args.ratio} | 默认 |
| 视觉风格 | 待确认 | — |
| 人物图 | 有 / 无 | — |
| 音频 | 有 / 无 | — |

## 4. 缺口与默认值
| # | 缺口 | 默认值 | 状态 |
|---|---|---|---|
| 1 | 人物/主题具体指哪一个 | 待用户确认 | 未问 |
| 2 | 想让人记住哪一句话 | 由方案官提 | 未问 |
| 3 | 时长档位 | {args.duration}s | 默认 |
| 4 | 素材状态 | 无图则生成 / 无音频则先写词 | 待确认 |

## 5. 硬约束
- 时长 / 画幅 / 单镜 ≤30s
- 声音：音频驱动口型
- 人物：用户图 / 生成图
- 合规：无真人/IP/品牌影射

## 6. 不做什么
- 待填写

## 7. 成功标准
- [ ] 待填写
- [ ] 待填写
- [ ] 待填写

## 8. 下一步
① 完成后停下等确认，再进 ② 出方案。
""",
        encoding="utf-8",
    )

    write_registry(project_id, name, f"assets/output/{name}", "⓪ 初始化", f"{args.duration}s")
    print(f"[OK] 项目已建：{project}")
    print(f"     目标档位 {args.duration}s · 画幅 {args.ratio} · 人物图：{img_note}")
    print("     下一步：① 解读任务 → 写 01-解读/01-任务书.md → log_step.py 记过程")


if __name__ == "__main__":
    main()
