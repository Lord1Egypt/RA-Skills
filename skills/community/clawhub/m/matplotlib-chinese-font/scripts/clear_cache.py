#!/usr/bin/env python3
"""清除 matplotlib 字体缓存"""

import os
import shutil
import matplotlib

cache_dir = matplotlib.get_cachedir()
print(f"字体缓存目录: {cache_dir}")

if os.path.exists(cache_dir):
    shutil.rmtree(cache_dir)
    print("✅ 字体缓存已清除")
else:
    print("字体缓存目录不存在，无需清除")
