import pysubs2
from typing import List, Dict


def parse_subtitle(file_path: str) -> List[str]:
    """解析字幕文件，返回台词列表"""
    subs = pysubs2.load(file_path)
    lines = [line.text for line in subs if line.text.strip()]
    return lines


def parse_subtitle_with_time(file_path: str) -> List[Dict]:
    """解析字幕文件，返回带时间的台词"""
    subs = pysubs2.load(file_path)
    lines = []
    for line in subs:
        if line.text.strip():
            minutes = line.start // 60000
            seconds = (line.start // 1000) % 60
            lines.append({
                'time': f"{minutes}:{seconds:02d}",
                'text': line.text
            })
    return lines


def get_first_n_lines(file_path: str, n: int = 20) -> List[str]:
    """获取前 n 条台词"""
    subs = pysubs2.load(file_path)
    lines = []
    for line in subs[:n]:
        if line.text.strip():
            lines.append(line.text)
    return lines


def get_key_scenes(file_path: str, keywords: List[str]) -> List[Dict]:
    """根据关键词提取关键场景"""
    subs = pysubs2.load(file_path)
    scenes = []
    
    for line in subs:
        text = line.text.lower()
        for keyword in keywords:
            if keyword.lower() in text:
                minutes = line.start // 60000
                seconds = (line.start // 1000) % 60
                scenes.append({
                    'time': f"{minutes}:{seconds:02d}",
                    'keyword': keyword,
                    'text': line.text
                })
                break
                
    return scenes


def get_movie_duration(file_path: str) -> str:
    """获取电影时长"""
    subs = pysubs2.load(file_path)
    total_ms = subs[-1].start
    hours = total_ms // 3600000
    minutes = (total_ms % 3600000) // 60000
    return f"{hours}:{minutes:02d}"


if __name__ == "__main__":
    # 测试
    import sys
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        
        print(f"=== {file_path} ===")
        print(f"Duration: {get_movie_duration(file_path)}")
        print(f"\nFirst 10 lines:")
        for i, line in enumerate(get_first_n_lines(file_path, 10), 1):
            print(f"{i}. {line}")
    else:
        print("Usage: python subtitle_parser.py <subtitle_file>")
