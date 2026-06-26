"""clean 命令：按文件时间清理 30 天前产物"""

import time
from music_studio import library as lib_mod


def main(_=None):
    print("=== 清理过期音乐文件 ===")

    output_dir = lib_mod.OUTPUT_DIR()
    now = time.time()
    count = 0

    for file in output_dir.iterdir():
        if not file.is_file():
            continue
        if file.name in ("library.json", ".gitkeep"):
            continue
        mtime = file.stat().st_mtime
        age_days = (now - mtime) / 86400
        if age_days > 30:
            print(f"🗑️  删除: {file.name}")
            file.unlink()
            count += 1

    print(f"共清理 {count} 个文件")
