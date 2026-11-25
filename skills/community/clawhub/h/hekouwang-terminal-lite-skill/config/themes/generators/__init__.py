"""付费包生成器的加载点。

pro.py 在 → 返回它；不在 → 返回 None，_generate.py 据此只出 iTerm2。
故意写得这么直白：这是产品分档，不是防破解。代码摆在这儿，
付费买的是「已经做好的东西 + 更新与答疑」，不是「看不到源码」。
"""


def load_pro():
    try:
        from . import pro
        return pro
    except ImportError:
        return None
