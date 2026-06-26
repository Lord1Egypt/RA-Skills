"""__init__ 模块单元测试：校验版本号存在且为合法 semver 形态。"""

import re

import __init__ as pkg


def test_version_is_semver_string():
    assert isinstance(pkg.__version__, str)
    assert re.fullmatch(r"\d+\.\d+\.\d+", pkg.__version__)
