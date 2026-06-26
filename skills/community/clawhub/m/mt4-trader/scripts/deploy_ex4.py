"""
MT4 EA 部署指引脚本
提示用户从 Gitee 手动下载 .ex4 文件并完成部署。

用法:
  python deploy_ex4.py              # 显示下载指引
  python deploy_ex4.py deploy       # 复制已下载的文件到 MT4 目录
"""

import os
import sys
import shutil

GITEE_URL = "https://gitee.com/3603317/skill-plugin/tree/master/mt4"

FILES = [
    ("mt4_bridge.ex4", "Experts", "主程序 EA（必选）"),
    ("\u829d\u9ebb\u7f51\u683cV2.ex4", "Experts", "网格策略 EA（可选）"),
    ("tools2.3.ex4", "Libraries", "网格策略依赖库（选网格则必选）"),
]


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_dir = os.path.dirname(script_dir)
    mql4_dir = os.path.join(skill_dir, "mql4")

    print("=" * 50)
    print("MT4 EA \u90e8\u7f72\u5de5\u5177")
    print("=" * 50)

    print(f"\n[*] \u8bf7\u4ece Gitee \u4ed3\u5e93\u4e0b\u8f7d .ex4 \u6587\u4ef6\uff1a")
    print(f"    {GITEE_URL}\n")

    print(f"    \u9700\u8981\u4e0b\u8f7d\u7684\u6587\u4ef6\uff1a")
    for filename, subdir, desc in FILES:
        raw_url = f"https://gitee.com/3603317/skill-plugin/raw/master/mt4/{filename}"
        print(f"    \u250c {filename}  \u2500 {desc}")
        print(f"    \u2514 {raw_url}")

    if len(sys.argv) <= 1 or sys.argv[1] != "deploy":
        print(f"\n[*] \u4e0b\u8f7d\u5b8c\u6210\u540e\uff0c\u8fd0\u884c\u4ee5\u4e0b\u547d\u4ee4\u90e8\u7f72\uff1a")
        print(f"    python deploy_ex4.py deploy")
        print(f"\n[*] \u6216\u5c06\u6587\u4ef6\u624b\u52a8\u62f7\u8d1d\u5230 MT4 \u5b89\u88c5\u76ee\u5f55")
        print(f"    \u250c MT4\\MQL4\\Experts\\  \u2500 mt4_bridge.ex4, \u829d\u9ebb\u7f51\u683cV2.ex4")
        print(f"    \u2514 MT4\\MQL4\\Libraries\\ \u2500 tools2.3.ex4")
        return

    # deploy mode: copy files from mql4/ to MT4 directories
    os.makedirs(mql4_dir, exist_ok=True)

    experts_dir = None
    libraries_dir = None

    # Auto-detect MT4
    candidates = [
        r"C:\Program Files (x86)\EBC Financial Group Cayman MT4 Terminal\MQL4",
        r"C:\Program Files\MetaTrader 4\MQL4",
        r"C:\Program Files (x86)\MetaTrader 4\MQL4",
        r"C:\Program Files\Alpari MT4\MQL4",
        r"C:\Program Files (x86)\Alpari MT4\MQL4",
    ]
    for c in candidates:
        if os.path.isdir(os.path.join(c, "Experts")):
            experts_dir = os.path.join(c, "Experts")
            libraries_dir = os.path.join(c, "Libraries")
            print(f"\n[*] \u81ea\u52a8\u68c0\u6d4b\u5230 MT4: {c}")
            break

    if not experts_dir:
        print(f"\n[!] \u672a\u81ea\u52a8\u68c0\u6d4b\u5230 MT4 \u5b89\u88c5\u76ee\u5f55")
        return

    missing = []
    for filename, subdir, desc in FILES:
        src = os.path.join(mql4_dir, filename)
        if not os.path.isfile(src):
            missing.append(filename)
            continue
        dst_dir = experts_dir if subdir == "Experts" else libraries_dir
        dst = os.path.join(dst_dir, filename)
        os.makedirs(dst_dir, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"  [+] {filename} \u5df2\u90e8\u7f72 -> {dst}")

    if missing:
        print(f"\n[!] \u4ee5\u4e0b\u6587\u4ef6\u672a\u627e\u5230\uff0c\u8bf7\u5148\u4ece Gitee \u4e0b\u8f7d\uff1a")
        for fn in missing:
            print(f"    - {fn}")

    print(f"\n[+] \u90e8\u7f72\u5b8c\u6210\uff01\u8bf7\u5728 MT4 \u4e2d\u786e\u8ba4:")
    print(f"    - \u5bfc\u822a\u5668\u4e2d\u53ef\u89c1 mt4_bridge.ex4, \u829d\u9ebb\u7f51\u683cV2.ex4")
    print(f"    - MQL4\\\\Libraries\\\\ \u76ee\u5f55\u4e0b\u53ef\u89c1 tools2.3.ex4")


if __name__ == "__main__":
    main()
