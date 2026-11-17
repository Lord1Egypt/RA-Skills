"""
环境检测工具
逐一检查 JY_Knowledge_Skill 所需的所有依赖，输出详细的状态报告。
Model 可执行此脚本来快速了解环境状态。

用法: python tools/check_env.py [--json]
  --json  输出 JSON 格式（供程序解析）
  默认    输出人类可读格式
"""

import sys
import os
import json

# 修复 Windows GBK 编码问题
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


REQUIRED_LIBS = {
    "requests": {"用途": "HTTP API 调用", "pip": "requests>=2.31.0"},
    "pymongo": {"用途": "MongoDB 驱动", "pip": "pymongo>=4.6.0"},
    "mammoth": {"用途": "DOCX 转 Markdown", "pip": "mammoth>=1.6.0"},
    "openpyxl": {"用途": "Excel 读写", "pip": "openpyxl>=3.1.0"},
    "PIL": {"用途": "图片处理（Pillow）", "pip": "Pillow"},
    "matplotlib": {"用途": "表格渲染截图", "pip": "matplotlib>=3.7.0"},
    "pdfplumber": {"用途": "PDF 文本提取", "pip": "pdfplumber>=0.10.0"},
    "fitz": {"用途": "PDF 转图片（PyMuPDF）", "pip": "pymupdf>=1.24.0"},
    "pandas": {"用途": "CSV 表格处理", "pip": "pandas>=2.0.0"},
}


def check_python():
    v = sys.version_info
    ok = v >= (3, 10)
    return {
        "ok": ok,
        "version": f"{v.major}.{v.minor}.{v.micro}",
        "executable": sys.executable,
        "detail": "Python >= 3.10 满足" if ok else "需要 Python 3.10+"
    }


def check_lib(name, info):
    try:
        __import__(name)
        return {"ok": True, "name": name, "用途": info["用途"], "detail": "已安装"}
    except ImportError:
        return {"ok": False, "name": name, "用途": info["用途"], 
                "pip_cmd": f"pip install {info['pip']}", "detail": f"未安装，请执行: pip install {info['pip']}"}


def check_file(path, desc):
    exists = os.path.exists(path)
    return {"ok": exists, "path": path, "desc": desc,
            "detail": "存在" if exists else f"不存在: {path}"}


def check_command(cmd, desc):
    """执行诊断命令。cmd 必须是本脚本内定义的硬编码字符串，不接受外部输入。"""
    import subprocess
    # 对于支持数组形式的命令使用 shell=False，带管道的命令仍需 shell=True
    use_shell = "|" in cmd or ">" in cmd
    try:
        result = subprocess.run(cmd, shell=use_shell, capture_output=True, text=True, timeout=10)
        output = (result.stdout + result.stderr).strip()
        return {"ok": result.returncode == 0, "cmd": cmd, "desc": desc,
                "detail": output[:200] if output else "命令执行成功但无输出"}
    except FileNotFoundError:
        return {"ok": False, "cmd": cmd, "desc": desc,
                "detail": f"命令不存在: {cmd.split()[0]} 未安装"}
    except Exception as e:
        return {"ok": False, "cmd": cmd, "desc": desc,
                "detail": f"执行异常: {e}"}


def run(json_mode=False):
    results = {"python": check_python(), "libraries": [], "files": [], "services": []}

    # 检查 Python 库
    for name, info in REQUIRED_LIBS.items():
        results["libraries"].append(check_lib(name, info))

    # 检查关键文件（相对于 skill 根目录）
    skill_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(os.path.dirname(skill_root), "config.json")
    results["files"].append(check_file(config_path, "配置文件"))
    results["files"].append(check_file(skill_root, "Skill 代码目录"))

    # 检查服务
    results["services"].append(check_command("docker --version", "Docker 运行时"))
    results["services"].append(check_command("curl -s http://localhost:1717/api/projects", "EasyDataset API"))
    results["services"].append(check_command("docker ps --format '{{.Names}}' | grep knowledge-mongo", "MongoDB 容器"))

    if json_mode:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        _print_human(results)


def _print_human(r):
    py = r["python"]
    print(f"{'= ' * 30}")
    print(f"JY_Knowledge_Skill 环境检测报告")
    print(f"{'= ' * 30}\n")

    # Python
    status = "✅" if py["ok"] else "❌"
    print(f"{status} Python {py['version']} ({py['executable']})")
    if not py["ok"]:
        print(f"   → {py['detail']}")

    # 依赖库
    print(f"\n--- Python 依赖 ---")
    all_libs_ok = True
    for lib in r["libraries"]:
        status = "✅" if lib["ok"] else "❌"
        print(f"{status} {lib['name']:20s} {lib['用途']}")
        if not lib["ok"]:
            print(f"   → {lib['pip_cmd']}")
            all_libs_ok = False
    if all_libs_ok:
        print("   全部依赖已安装 ✅")

    # 文件
    print(f"\n--- 关键文件 ---")
    for f in r["files"]:
        status = "✅" if f["ok"] else "❌"
        print(f"{status} {f['desc']}: {f['path']}")

    # 服务
    print(f"\n--- 外部服务 ---")
    for s in r["services"]:
        status = "✅" if s["ok"] else "❌"
        print(f"{status} {s['desc']}")
        if not s["ok"]:
            detail = s['detail'][:150]
            print(f"   → {detail}")

    # 总结
    all_ok = (py["ok"] and all_libs_ok and
              all(f["ok"] for f in r["files"]) and
              all(s["ok"] for s in r["services"]))
    print(f"\n{'= ' * 30}")
    if all_ok:
        print("所有检测通过 ✅  可以执行: python main.py -t")
    else:
        missing = []
        if not py["ok"]: missing.append("Python")
        missing.extend(lib["name"] for lib in r["libraries"] if not lib["ok"])
        missing.extend(f["desc"] for f in r["files"] if not f["ok"])
        missing.extend(s["desc"] for s in r["services"] if not s["ok"])
        print(f"发现问题 ({len(missing)}项): {', '.join(missing)}")
        print("请根据上述提示逐一修复后重新检测")
    print(f"{'= ' * 30}")


if __name__ == "__main__":
    json_mode = "--json" in sys.argv
    run(json_mode=json_mode)
