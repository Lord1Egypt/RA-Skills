#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""自测驱动器：**只连接**一个已经开着调试端口的 Chrome，跑 selftest.py。

🔒🔒 能力边界（与本 skill 的对外承诺完全一致）
----------------------------------------------------
本脚本**不启动、不结束任何浏览器进程** —— 它只连接一个**用户已经开好**的
Chrome 调试端口，在上面**新建一个自己的标签页**跑自测，跑完**关掉自己那个
标签页**。

🚨 2026-11-02 教训：ClawHub 的安全评审判了这个 skill 一条
   *"its optional test launcher exceeds its advertised browser restrictions"*
   —— 因为早先版本会用 `subprocess.Popen` 去**启动** Chrome，
   与「不启动浏览器进程」的对外承诺直接冲突。
   ⇒ 现在**彻底移除启动逻辑**：端口不通就**打印可复制的命令**让用户自己起，
     绝不代劳。
   ⇒ 同理也**不 kill** 用户的浏览器 —— 只关自己新建的那个 target。

用法
----
    python run_selftest.py --port 9228
    # 端口不通时它会打印一条可直接复制的启动命令，然后退出。

⚠ 沙箱/受限环境下自启的 Chrome 容易被回收（表现为「Chrome 退出码 3、
  无任何 stderr」）⇒ 本脚本**不碰**这个坑，它只管连。
"""
import argparse
import json
import os
import subprocess
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))


def cdp_up(port):
    """调试端口是否可用。返回 (ok, 版本信息)。"""
    try:
        with urllib.request.urlopen(
                "http://127.0.0.1:%d/json/version" % port, timeout=4) as r:
            return True, json.loads(r.read().decode("utf-8"))
    except Exception:
        return False, None


def chrome_launch_hint(port):
    """给用户一条可直接复制的启动命令（**不代劳执行**）。"""
    import ms_cdp as M
    exe, _label = M.pick_chrome()
    exe = exe or "<Chrome 可执行文件路径>"
    prof = os.path.expanduser("~/chrome-ms-selftest")
    return (
        "  \"%s\" --remote-debugging-port=%d --remote-debugging-address=127.0.0.1 "
        "--user-data-dir=\"%s\" --no-first-run --no-default-browser-check "
        "about:blank\n\n"
        "  说明：\n"
        "    · 独立 profile 是 Chrome 136+ 的官方要求（默认 user-data-dir "
        "不允许开调试端口）。\n"
        "    · 调试端口已显式绑定 127.0.0.1，不会暴露到局域网。\n"
        "    · 窗口会一直留着，用完自己关掉即可。\n"
        "    · 本脚本**不会**替你启动或结束浏览器。"
        % (exe, port, prof))


def main():
    ap = argparse.ArgumentParser(description="连接现成 Chrome 跑自测（不启动浏览器）")
    ap.add_argument("--port", type=int,
                    default=int(os.environ.get("SELFTEST_PORT", "9334")),
                    help="已开调试端口的 Chrome（默认 9334）")
    args = ap.parse_args()

    ok, _ver = cdp_up(args.port)
    if not ok:
        print("✗ 连不上 Chrome 调试端口 127.0.0.1:%d" % args.port)
        print("请自己启动一个带调试端口的 Chrome（下面这条可直接复制）：\n")
        print(chrome_launch_hint(args.port))
        return 2

    print("[ok] 已连上 127.0.0.1:%d" % args.port)
    env = dict(os.environ)
    env["SELFTEST_PORT"] = str(args.port)
    r = subprocess.run([sys.executable, os.path.join(HERE, "selftest.py")],
                       cwd=HERE, env=env)
    print("[..] 自测退出码 = %s" % r.returncode)
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
