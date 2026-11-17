#!/usr/bin/env python3
"""env_check.py — llm-output-explainer 模块D 环境检查

检查视频/图表管线的全部硬依赖，输出人类可读报告 + --json 机器可读。
任何一项缺失时，SKILL.md 要求走 references/module-d-video.md 的降级路线。

用法:
    python3 env_check.py            # 人类可读
    python3 env_check.py --json     # JSON（供 agent 解析）
"""
import json
import shutil
import subprocess
import sys


def check_cmd(name, cmd, version_args=["--version"], hint=""):
    """检查命令是否存在，返回 (ok, version_str)"""
    path = shutil.which(cmd)
    if not path:
        return False, "", f"未安装。{hint}"
    try:
        out = subprocess.run([cmd] + version_args, capture_output=True, text=True, timeout=15)
        ver = (out.stdout or out.stderr).strip().split("\n")[0][:80]
        return True, ver, ""
    except Exception as e:
        return True, f"(版本获取失败: {e})", ""


def check_import(module, pip_name, hint=""):
    try:
        mod = __import__(module)
        return True, getattr(mod, "__version__", "installed"), ""
    except ImportError:
        return False, "", f"未安装。pip install {pip_name}。{hint}"


def check_cjk_font():
    """检查系统是否有可用中文字体（Manim Text 渲染中文必需）"""
    try:
        out = subprocess.run(
            ["fc-list", ":lang=zh", "family"], capture_output=True, text=True, timeout=15
        )
        families = sorted(set(l.strip() for l in out.stdout.splitlines() if l.strip()))
        if families:
            return True, families[0], ""
        return False, "", "无中文字体。apt install fonts-noto-cjk"
    except FileNotFoundError:
        # fc-list 不存在时退化为常见路径检查
        import os
        for p in ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
                  "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"]:
            if os.path.exists(p):
                return True, p, ""
        return False, "", "fc-list 不可用且无常见中文字体路径。apt install fonts-noto-cjk"
    except Exception as e:
        return False, "", f"检测失败: {e}"


def check_edge_tts_network():
    """edge-tts 需要访问 speech.platform.bing.com；网络不通时降级为字幕"""
    import socket
    try:
        socket.create_connection(("speech.platform.bing.com", 443), timeout=8).close()
        return True, "speech.platform.bing.com:443 可达", ""
    except Exception as e:
        return False, "", f"TTS 服务不可达({e})。降级路线：仅交付无声视频+字幕轨"


def main():
    checks = {
        "python3": check_cmd("Python", "python3"),
        "ffmpeg": check_cmd("FFmpeg", "ffmpeg", hint="apt install ffmpeg"),
        "manim": check_import("manim", "manim", hint="需 Python≥3.9，参考 module-d-video.md"),
        "edge_tts": check_import("edge_tts", "edge-tts"),
        "edge_tts_network": check_edge_tts_network(),
        "cjk_font": check_cjk_font(),
        "node_npx": check_cmd("Node/npx", "npx", version_args=["--version"]),
    }

    # mermaid-cli：npx @mermaid-js/mermaid-cli 首次需下载+Chromium，仅探测不执行
    ok, ver, hint = checks["node_npx"]
    checks["mermaid_cli"] = (ok, "npx 可用，运行时按需下载 @mermaid-js/mermaid-cli（需 Chromium）" if ok else "",
                             "需 Node.js" if not ok else "")

    hard_for_video = ["ffmpeg", "manim", "cjk_font"]
    hard_for_tts = ["edge_tts", "edge_tts_network"]
    video_ready = all(checks[k][0] for k in hard_for_video)
    tts_ready = all(checks[k][0] for k in hard_for_tts)

    if "--json" in sys.argv:
        print(json.dumps({
            "video_ready": video_ready,
            "tts_ready": tts_ready,
            "checks": {k: {"ok": v[0], "detail": v[1], "fix": v[2]} for k, v in checks.items()},
        }, ensure_ascii=False, indent=2))
        return

    print("=" * 56)
    print("llm-output-explainer 环境检查报告")
    print("=" * 56)
    labels = {
        "python3": "Python", "ffmpeg": "FFmpeg", "manim": "Manim 社区版",
        "edge_tts": "edge-tts", "edge_tts_network": "TTS 网络",
        "cjk_font": "中文字体", "node_npx": "Node/npx", "mermaid_cli": "Mermaid CLI",
    }
    for k, (ok, ver, hint) in checks.items():
        mark = "✅" if ok else "❌"
        line = f"{mark} {labels[k]:<12}"
        if ver:
            line += f" {ver}"
        print(line)
        if not ok and hint:
            print(f"   └─ {hint}")
    print("-" * 56)
    print(f"视频管线（无声）: {'✅ 可用' if video_ready else '❌ 不满足 → 走降级路线'}")
    print(f"中文配音管线:     {'✅ 可用' if tts_ready else '❌ 不满足 → 字幕轨降级'}")
    if video_ready and tts_ready:
        print("全部就绪：可完整执行模块 D。")


if __name__ == "__main__":
    main()
