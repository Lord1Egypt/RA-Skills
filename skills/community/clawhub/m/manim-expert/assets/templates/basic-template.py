from manim import *

class BasicTemplate(Scene):
    def construct(self):
        # 示例：创建一个简单的文本动画
        text = Text("Hello Manim!", font_size=48)
        self.play(Write(text))
        self.wait(1)
        self.play(FadeOut(text))