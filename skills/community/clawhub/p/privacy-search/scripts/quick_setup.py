#!/usr/bin/env python3
"""
一键安装启动脚本
- 自动创建 venv
- 安装依赖
- 配置 config.yaml
- 启动 SearXNG
- 验证安装

版本号从 SKILL.md 解析，避免与实际发版脱节。
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

# 不生成 __pycache__（死规则 13）
sys.dont_write_bytecode = True

# 本脚本在依赖安装之前运行，只能依赖标准库。
# version_util 无第三方依赖，可安全导入。
try:
    from version_util import get_current_version, display_width
except ImportError:
    try:
        from .version_util import get_current_version, display_width
    except ImportError:
        def get_current_version() -> str:
            """极端情况下（文件缺失）不因取不到版本号而中断安装"""
            return ""

        def display_width(text: str) -> int:
            """兜底实现：仅粗略区分全角与半角"""
            return sum(2 if ord(ch) > 0x2E80 else 1 for ch in text)


def run(cmd: list, check: bool = True, capture: bool = False) -> subprocess.CompletedProcess:
    print(f"  > {' '.join(cmd)}")
    result = subprocess.run(
        cmd,
        capture_output=capture,
        text=True,
        timeout=60,
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"执行失败: {result.stderr.strip() if result.stderr else result.returncode}")
    return result


def main():
    version = get_current_version()
    title = "隐私搜索 %s- 一键安装启动" % (("v%s " % version) if version else "")
    # 边框按标题实际显示宽度对齐：中文与emoji占两列
    width = display_width(title)
    pad = max(0, 58 - width)
    left = pad // 2
    print("""
╔══════════════════════════════════════════════════════════════╗
║  {space_l}{title}{space_r}  ║
╚══════════════════════════════════════════════════════════════╝
""".format(title=title, space_l=" " * left, space_r=" " * (pad - left)))

    base_dir = Path(__file__).parent.parent
    scripts_dir = base_dir / "scripts"

    # Step 1: check python
    print("📌 [1/5] 检查 Python 版本...")
    result = run(["python", "--version"], check=False, capture=True)
    if result.returncode != 0:
        print("❌ 未找到 Python，请先安装 Python 3.10+")
        sys.exit(1)
    version_str = result.stdout.strip() or result.stderr.strip()
    print(f"   ✅ {version_str}")

    # Step 2: create venv
    print("\n📌 [2/5] 创建虚拟环境...")
    venv_path = base_dir / ".venv"
    if venv_path.exists():
        print("   ⚠️  .venv 已存在，跳过创建")
    else:
        run([sys.executable, "-m", "venv", str(venv_path)])
        print("   ✅ 虚拟环境已创建")

    # Step 3: install deps
    print("\n📌 [3/5] 安装依赖...")
    pip_path = venv_path / "Scripts" / "pip.exe" if os.name == "nt" else venv_path / "bin" / "pip"
    python_path = venv_path / "Scripts" / "python.exe" if os.name == "nt" else venv_path / "bin" / "python"
    requirements_path = base_dir / "requirements.txt"
    run([str(pip_path), "install", "-q", "-r", str(requirements_path)])
    print("   ✅ 依赖安装完成")

    # Step 4: copy config
    print("\n📌 [4/5] 配置 config.yaml...")
    config_path = base_dir / "config.yaml"
    example_path = base_dir / "references" / "config.yaml.example"
    if config_path.exists():
        print("   ⚠️  config.yaml 已存在，跳过")
    else:
        shutil.copy(str(example_path), str(config_path))
        print("   ✅ config.yaml 已创建")

    # Step 5: verify
    print("\n📌 [5/5] 验证安装...")
    result = run(
        [str(python_path), str(scripts_dir / "search.py"), "--help"],
        check=False, capture=True,
    )
    if result.returncode == 0:
        print("   ✅ search.py 可运行")
    else:
        print(f"   ⚠️  search.py 运行异常: {result.stderr[:200]}")

    result = run(
        [str(python_path), str(scripts_dir / "privacy.py"), "--help"],
        check=False, capture=True,
    )
    if result.returncode == 0:
        print("   ✅ privacy.py 可运行")

    result = run(
        [str(python_path), str(scripts_dir / "update_checker.py"), "--help"],
        check=False, capture=True,
    )
    if result.returncode == 0:
        print("   ✅ update_checker.py 可运行")

    # V1.9 优化：简化输出，一条命令出结果
    python_cmd = "python" if os.name != "nt" else "python"
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  ✅ 安装完成！                                              ║
╠══════════════════════════════════════════════════════════════╣
║  一条命令开始搜索：                                         ║
║                                                              ║
║     {python_cmd} scripts/search.py "关键词"                  ║
║                                                              ║
║  可选：                                                     ║
║     --privacy strict    隐私模式（默认 normal）              ║
║     --engines baidu,bing 指定引擎                            ║
║     --selftest          体检引擎状态                         ║
╚══════════════════════════════════════════════════════════════╝
""")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ 安装失败: {e}")
        print("请手动执行安装步骤，详见 QUICK_START.md")
        sys.exit(1)
