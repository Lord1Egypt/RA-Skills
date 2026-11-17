# -*- coding: utf-8 -*-
"""manim_scene_template.py — llm-output-explainer 模块 D 场景模板

用法:
    cp 本文件 my_scene.py → 按"场景=脚本段落"改写 →
    manim -ql my_scene.py DemoScene      # 快速草稿
    manim -qh my_scene.py DemoScene      # 1080p 定稿

铁律提醒（references/module-d-video.md）：
    1. 先有旁白脚本，再写本文件  2. 一个场景一个核心视觉隐喻  3. 文字≤12字/屏
"""
from manim import *


def cn(text, **kwargs):
    """中文字体安全封装：Manim 默认字体不含中文，必须显式指定。

    可用字体取决于 env_check.py 的 cjk_font 结果；Noto Sans CJK SC 为首选。
    若 fc-list :lang=zh 显示其他字体（如文泉驿），替换 font= 即可。
    """
    return Text(text, font="Noto Sans CJK SC", **kwargs)


# 本 skill 固定配色（4-5 色，语义一致，全片统一）
BLUE = "#3B6EA5"    # 核心对象
ORANGE = "#D97742"  # 对比/变化
GRAY = "#8A8F94"    # 背景/次要
YELLOW = "#E8B84B"  # 高亮
RED = "#B3402E"     # 警示


class DemoScene(Scene):
    """示例：一句话版本 + 核心概念入场。按旁白脚本逐段改写。"""

    def construct(self):
        # 第 1 拍：钩子（≤5秒）——用问题或反直觉事实开场
        hook = cn("为什么复杂的东西总讲不清楚？", color=BLUE)
        self.play(Write(hook), run_time=2)
        self.wait(1)

        # 第 2 拍：一句话版本（高亮停留，允许观众读完）
        thesis = cn("选对机制，复杂内容就能讲懂", color=ORANGE).scale(1.2)
        self.play(ReplacementTransform(hook, thesis), run_time=1.5)
        self.wait(2.5)  # 关键句停留 ≥ 2.5 秒

        # 第 3 拍：核心视觉隐喻贯穿全场（示例：四色卡片=四模块，按需增删）
        items = VGroup(
            cn("受控语言", color=BLUE),
            cn("图表", color=ORANGE),
            cn("HTML 工件", color=YELLOW),
            cn("讲解视频", color=RED),
        ).arrange(RIGHT, buff=0.6)
        self.play(LaggedStart(*[FadeIn(it, shift=UP) for it in items], lag_ratio=0.25))
        self.wait(2)

        # 第 4 拍：结论回收（视觉回到一句话版本）
        final = cn("先选机制，再动笔", color=BLUE).scale(1.1)
        self.play(FadeOut(items), ReplacementTransform(thesis, final), run_time=1.5)
        self.wait(2)


# 多段落脚本 = 多个 Scene 类，渲染时逐个指定：
#   manim -qh my_scene.py DemoScene HookScene ConclusionScene
# 然后 ffmpeg 合成 + 拼接旁白（见 module-d-video.md 第 4-5 步）
