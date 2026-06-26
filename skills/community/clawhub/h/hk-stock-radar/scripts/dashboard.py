"""
港股雷达仪表盘：一键汇总恒生指数 + 科技股 + 板块
用法: python dashboard.py
"""
import subprocess
import sys
import os

base = os.path.dirname(os.path.abspath(__file__))

print("=" * 50)
print("  🦞 港股雷达仪表盘")
print("=" * 50)

print("\n>>> 恒生指数")
subprocess.run([sys.executable, os.path.join(base, "hk_index.py")])

print("\n>>> 港股科技四巨头 (腾讯/阿里/美团/小米)")
subprocess.run([sys.executable, os.path.join(base, "hk_quote.py"),
                "hk00700", "hk09988", "hk03690", "hk01810"])

print("\n>>> 港股板块涨跌TOP10")
subprocess.run([sys.executable, os.path.join(base, "hk_sector.py"), "30"])
