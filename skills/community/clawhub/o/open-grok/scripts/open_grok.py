#!/usr/bin/env python3
import subprocess
import platform

url = "https://grok.x.ai"
system = platform.system()

if system == "Windows":
    subprocess.Popen(["start", "brave", url], shell=True)
elif system == "Darwin":
    subprocess.Popen(["open", "-a", "Brave Browser", url])
else:
    subprocess.Popen(["brave-browser", url])

print("✅ Grok opening in Brave!")