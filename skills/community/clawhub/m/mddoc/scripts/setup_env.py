#!/usr/bin/env python3
"""mddoc 环境自检与准备 — 固定专用虚拟环境,幂等。

说明:
    在固定位置(Linux/macOS: ~/.cache/mddocx/venv;Windows: %LOCALAPPDATA%/mddocx/venv)
    维护一个专用 Python 虚拟环境,跨会话/跨目录复用,避免在用户项目目录创建 .venv
    干扰项目依赖。仅当该环境缺失或依赖缺失时才创建/安装,就绪时零操作。

用法:
    python3 setup_env.py

返回值:
    退出码 0 = 环境就绪;非 0 = 自检或准备失败。
    stdout 最后一行输出就绪的 Python 解释器绝对路径,格式 `READY <path>`,
    供调用方(转换脚本、Agent)后续执行使用。
"""

import os
import subprocess
import sys
from pathlib import Path

REQUIRED_MODULES = ['docx', 'PIL', 'requests', 'mistune']
PIP_PACKAGES = 'python-docx Pillow requests mistune'
# 清华 PyPI 镜像源，国内安装加速
PIP_INDEX = 'https://pypi.tuna.tsinghua.edu.cn/simple'


def venv_dir() -> Path:
    """返回专用虚拟环境根目录。

    参数:
        无

    返回值:
        Path — 虚拟环境目录。Linux/macOS 为 ~/.cache/mddocx/venv,
        Windows 为 %LOCALAPPDATA%/mddocx/venv。
    """
    if sys.platform == 'win32':
        base = Path(os.environ.get('LOCALAPPDATA', str(Path.home())))
    else:
        base = Path(os.environ.get('XDG_CACHE_HOME', str(Path.home() / '.cache')))
    return base / 'mddocx' / 'venv'


def bin_dir(venv: Path) -> str:
    """返回 venv 内可执行文件所在目录名。

    参数:
        venv (Path): 虚拟环境目录。

    返回值:
        str — Windows 为 'Scripts',其余平台为 'bin'。
    """
    return 'Scripts' if sys.platform == 'win32' else 'bin'


def python_path(venv: Path) -> Path:
    """返回 venv 内 Python 解释器路径。

    参数:
        venv (Path): 虚拟环境目录。

    返回值:
        Path — 解释器绝对路径。
    """
    name = 'python.exe' if sys.platform == 'win32' else 'python'
    return venv / bin_dir(venv) / name


def deps_ok(python: Path) -> bool:
    """检查指定解释器能否 import 全部依赖。

    参数:
        python (Path): Python 解释器路径。

    返回值:
        bool — True 表示依赖可用,False 表示缺失。
    """
    code = 'import ' + ', '.join(REQUIRED_MODULES)
    return subprocess.run([str(python), '-c', code],
                          capture_output=True).returncode == 0


def main() -> int:
    """执行环境自检与准备,返回退出码。"""
    venv = venv_dir()
    py = python_path(venv)

    # 1) 专用 venv 存在且依赖可用 → 就绪,零操作
    if py.is_file() and deps_ok(py):
        print(f'READY {py}')
        return 0

    try:
        # 2) venv 不存在 → 创建
        if not py.is_file():
            print(f'[mddoc] 创建虚拟环境: {venv}', file=sys.stderr)
            subprocess.run([sys.executable, '-m', 'venv', str(venv)], check=True)

        # 3) 依赖缺失 → 仅此时安装
        pip = venv / bin_dir(venv) / ('pip.exe' if sys.platform == 'win32' else 'pip')
        print(f'[mddoc] 安装缺失依赖: {PIP_PACKAGES}（镜像: {PIP_INDEX}）', file=sys.stderr)
        subprocess.run([str(pip), 'install', '--disable-pip-version-check',
                        '-i', PIP_INDEX]
                       + PIP_PACKAGES.split(), check=True)
    except subprocess.CalledProcessError as exc:
        print(f'[mddoc] 环境准备失败: {exc}', file=sys.stderr)
        return 1

    print(f'READY {py}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
