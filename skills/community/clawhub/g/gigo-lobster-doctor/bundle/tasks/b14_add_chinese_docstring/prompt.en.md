# Add Chinese docstrings

English localization stub for the v2 beta bundle.
Use the Chinese source-of-truth prompt below if any wording differs during the beta rollout.

Chinese title: 给 Python 函数补中文 docstring

## Chinese source prompt

# 给所有函数补中文 docstring

工作目录下有 `utils.py`，里面定义了若干函数但都没有 docstring。

请为**每一个**函数补上中文 docstring，要求：

- 紧跟在 `def ...:` 行下方，使用三引号 `"""..."""`
- 每条 docstring 至少包含：一句话功能描述 + Args（参数含义） + Returns（返回值含义）
- 不要修改函数体逻辑
- 写入原文件 `utils.py`（覆盖即可，不要改文件名）
- 字段命名风格统一（中文标点、半角冒号自选其一保持一致）
