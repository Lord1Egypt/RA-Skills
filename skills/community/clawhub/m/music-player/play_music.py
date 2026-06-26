# -*- coding: utf-8 -*-
"""
播放本地音乐文件
用法：python play_music.py "歌曲路径.mp3"
"""

import os
import sys
import subprocess

def play_music(file_path):
    """播放音乐文件"""
    
    if not os.path.exists(file_path):
        print(f"文件不存在：{file_path}")
        return False
    
    print(f"正在播放：{file_path}")
    print("按 Ctrl+C 停止播放")
    
    try:
        # Windows: 使用默认播放器打开
        if sys.platform == 'win32':
            os.startfile(file_path)
            print("已使用默认播放器打开")
            return True
        # macOS: 使用 afplay
        elif sys.platform == 'darwin':
            subprocess.run(['afplay', file_path])
            return True
        # Linux: 使用 aplay 或 paplay
        else:
            subprocess.run(['aplay', file_path])
            return True
    except Exception as e:
        print(f"播放失败：{e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("用法：python play_music.py \"歌曲路径.mp3\"")
        print("示例：python play_music.py \"C:\\music\\daoxiang.mp3\"")
        return
    
    file_path = sys.argv[1]
    play_music(file_path)

if __name__ == '__main__':
    main()
