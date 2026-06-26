"""
MiMo TTS 环境检查 / Environment Check (中文/English)

检查 mijiaAPI 依赖是否安装、认证文件是否存在。
Check if mijiaAPI dependencies are installed and auth file exists.
"""

import sys
import os
import json

# Windows GBK 兼容 / Windows GBK compat
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

AUTH_PATH = os.path.expanduser(r"~\.config\mijia-api\auth.json")
REQUIRED = ["mijiaAPI"]

print("=== 环境检查 / Environment Check ===", flush=True)

# 1. 检查 Python
print(f"Python: {sys.version.split()[0]}", flush=True)

# 2. 检查依赖
all_ok = True
for pkg in REQUIRED:
    try:
        __import__(pkg)
        print(f"  ✅ {pkg} — 已安装 / installed", flush=True)
    except ImportError:
        print(f"  ❌ {pkg} — 未安装 / not installed", flush=True)
        all_ok = False

# 3. 检查认证
if os.path.exists(AUTH_PATH):
    try:
        with open(AUTH_PATH) as f:
            auth = json.load(f)
        if auth.get("userId") or auth.get("user_id"):
            print(f"  ✅ 米家已登录 / Mijia authenticated (userId: {auth.get('userId')})", flush=True)
        else:
            print(f"  ⚠️ 认证文件存在但缺少用户信息 / Auth file exists but missing userId", flush=True)
            all_ok = False
    except:
        print(f"  ❌ 认证文件损坏 / Auth file corrupted", flush=True)
        all_ok = False
else:
    print(f"  ❌ 认证文件不存在 / Auth file not found: {AUTH_PATH}", flush=True)
    print(f"    请运行 / Run: python -m mijiaAPI -l", flush=True)
    all_ok = False

# 4. 检查 mijiaAPI CLI 可用性
try:
    import subprocess
    r = subprocess.run([sys.executable, "-m", "mijiaAPI", "--version"],
                       capture_output=True, text=True, timeout=10)
    if r.returncode == 0:
        print(f"  ✅ mijiaAPI CLI 可用 / CLI available", flush=True)
    else:
        print(f"  ⚠️ mijiaAPI CLI 异常 / CLI error: {r.stderr[:100]}", flush=True)
except:
    print(f"  ⚠️ mijiaAPI CLI 检查失败 / CLI check failed", flush=True)

print("", flush=True)
if all_ok:
    print("🎉 环境就绪 / Environment ready!", flush=True)
else:
    print("⚠️ 部分检查未通过 / Some checks failed", flush=True)
    sys.exit(1)
