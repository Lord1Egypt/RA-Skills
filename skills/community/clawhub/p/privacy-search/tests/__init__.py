"""
测试包

关闭字节码写入并清理已产生的残留（死规则 13）。

为什么单靠 sys.dont_write_bytecode 不够：
    unittest discover 通过 importlib 加载测试模块，字节码在模块代码
    真正执行之前就已写盘。因此按字母序最先被加载的那个模块，其文件内的
    dont_write_bytecode 尚未生效，仍会留下一个 .pyc。
    此处在包导入时补一次清理，使得无论以何种方式运行都不污染仓库。
"""

import atexit
import os
import shutil
import sys

sys.dont_write_bytecode = True

_HERE = os.path.dirname(os.path.abspath(__file__))


def _purge_bytecode() -> None:
    """移除测试包内的字节码缓存目录"""
    for root, dirs, _ in os.walk(_HERE):
        for d in list(dirs):
            if d == "__pycache__":
                shutil.rmtree(os.path.join(root, d), ignore_errors=True)
                dirs.remove(d)


# 导入时清一次：处理本次加载之前遗留的残留。
# 退出时再清一次：处理本次加载过程中、设置生效前写入的字节码。
_purge_bytecode()
atexit.register(_purge_bytecode)
