#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""launch_workbench.py — 把「96原则实时选股工作台」一键部署到当前工作目录并启动。

用法（在你的任意工作目录里执行）：
    python launch_workbench.py            # 默认端口 8765
    python launch_workbench.py 9000       # 指定端口

做了什么：
  1. 把技能里的 workbench_server.py / workbench_realtime.html 同步（复制）到当前目录；
  2. 在当前目录启动本地服务（127.0.0.1:<port>），数据文件（candidates/kline/intraday 等）也落在当前目录；
  3. 浏览器打开 http://127.0.0.1:<port>/ 即可。

之后怎么刷新数据：
  · 点页面上的「🔄 实时重新筛查」——工作台自己拉 东财初筛 + 新浪K线 + 东财分时强度，
    无需再找 Agent。约 60~120 秒完成（盘中跑即盘中快照，收盘后跑即全天分时）。
  · 公告核查（九不买 #3/#5/#6）仍需 Wind/Agent：对 Agent 说「跑 Wind 核查」，Agent 写盘后
    刷新页面即可看到客观结论；未跑则自动回落 👁 人工项，不影响其他逻辑。

⚠️ 仅方法论演示，不构成投资建议。
"""
import os, sys, shutil, subprocess, socket

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
FILES = ["workbench_server.py", "workbench_realtime.html"]
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765


def port_in_use(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        return s.connect_ex(("127.0.0.1", port)) == 0
    finally:
        s.close()


def main():
    cwd = os.getcwd()
    print(f"工作目录：{cwd}")
    # 1) 同步文件
    for f in FILES:
        src = os.path.join(SKILL_DIR, f)
        if not os.path.exists(src):
            print(f"  ⚠️ 技能内未找到 {f}（路径 {src}），跳过同步")
            continue
        dst = os.path.join(cwd, f)
        shutil.copy2(src, dst)
        print(f"  已同步 {f} → {dst}")
    # 2) 启动（若端口已被占用，提示而非重复启动）
    if port_in_use(PORT):
        print(f"\n⚠️ 端口 {PORT} 已被占用（工作台可能已在运行）。")
        print(f"   直接打开 http://127.0.0.1:{PORT}/ 即可；如需重启请先结束旧进程。")
        return
    server = os.path.join(cwd, "workbench_server.py")
    if not os.path.exists(server):
        print(f"  ❌ 未找到 {server}，无法启动。")
        return
    print(f"\n🚀 启动工作台：http://127.0.0.1:{PORT}/")
    print(f"   按 Ctrl+C 停止。\n")
    try:
        subprocess.run([sys.executable, server, str(PORT)], cwd=cwd)
    except KeyboardInterrupt:
        print("\n已停止工作台。")


if __name__ == "__main__":
    main()
