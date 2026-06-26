# -*- coding: utf-8 -*-
"""
嵌入音乐文件的 ID3 元数据
用法：python embed_metadata.py "歌曲.mp3" "歌名" "歌手" "专辑" "封面.jpg"
"""

import sys
import os

try:
    from mutagen.id3 import ID3, TIT2, TPE1, TALB, APIC, USLT, encoding
    from mutagen.mp3 import MP3
    HAS_MUTAGEN = True
except ImportError:
    HAS_MUTAGEN = False
    print("需要安装 mutagen: pip install mutagen")

def embed_metadata(file_path, title='', artist='', album='', cover_path='', lyrics=''):
    """嵌入 ID3 元数据"""
    
    if not HAS_MUTAGEN:
        return False
    
    if not os.path.exists(file_path):
        print(f"文件不存在：{file_path}")
        return False
    
    try:
        # 创建或加载 ID3 标签
        audio = MP3(file_path, ID3=ID3)
        
        try:
            audio.add_tags()
        except:
            pass  # 标签已存在
        
        # 设置标题
        if title:
            audio['TIT2'] = TIT2(encoding=3, text=title)
        
        # 设置艺术家
        if artist:
            audio['TPE1'] = TPE1(encoding=3, text=artist)
        
        # 设置专辑
        if album:
            audio['TALB'] = TALB(encoding=3, text=album)
        
        # 设置封面
        if cover_path and os.path.exists(cover_path):
            with open(cover_path, 'rb') as f:
                cover_data = f.read()
            audio['APIC'] = APIC(
                encoding=3,
                mime='image/jpeg',
                type=3,  # 封面
                desc='Cover',
                data=cover_data
            )
        
        # 设置歌词
        if lyrics:
            audio['USLT'] = USLT(
                encoding=3,
                lang='chi',
                desc='Lyrics',
                text=lyrics
            )
        
        audio.save()
        print("元数据已嵌入")
        return True
        
    except Exception as e:
        print(f"嵌入失败：{e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("用法：python embed_metadata.py \"歌曲.mp3\" [歌名] [歌手] [专辑] [封面.jpg]")
        return
    
    file_path = sys.argv[1]
    title = sys.argv[2] if len(sys.argv) > 2 else ''
    artist = sys.argv[3] if len(sys.argv) > 3 else ''
    album = sys.argv[4] if len(sys.argv) > 4 else ''
    cover = sys.argv[5] if len(sys.argv) > 5 else ''
    
    embed_metadata(file_path, title, artist, album, cover)

if __name__ == '__main__':
    main()
