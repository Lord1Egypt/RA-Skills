import requests
from bs4 import BeautifulSoup
import re

url = "https://hanime1.me/search?query=miuuuuu"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://hanime1.me/",
}

print("正在请求网页...")
response = requests.get(url, headers=headers, timeout=15)
response.encoding = 'utf-8'
response.raise_for_status()

print(f"网页状态码: {response.status_code}")
print("开始解析视频名称...")

# 使用 html.parser 解析
soup = BeautifulSoup(response.text, 'html.parser')

# 获取所有文本行
all_text = soup.get_text()
lines = [line.strip() for line in all_text.split('\n') if line.strip()]

# 视频标题的特征关键词
video_keywords = [
    '[中文字幕]', 'NTR', 'Sex Diary', '刻晴', 'Ayaka', 'Ganyu',
    '胡桃', '神子', '璃月', '淫欲', 'ZZZ', '差分', '調教', '日記',
    '重生', '阿晴', '診所', '基沃托斯'
]

# 过滤掉明显不是标题的内容
exclude_patterns = [
    r'\d+\.?\d*万次',  # 播放量
    r'\d+個月前',  # 发布时间
    'thumb_up', 'account_circle', 'EROLABS', '全部类型',
    'Motion Anime', 'Cosplay', 'Hanime1.me', '首頁'
]

video_titles = []
seen = set()

for line in lines:
    # 检查是否包含视频标题关键词
    has_keyword = any(kw in line for kw in video_keywords)

    # 检查是否包含排除内容
    has_exclude = any(re.search(pattern, line) for pattern in exclude_patterns)

    # 长度过滤
    is_length_ok = 5 < len(line) < 80

    if has_keyword and not has_exclude and is_length_ok and line not in seen:
        # 额外清理：去掉行首的数字（如果有）
        clean_line = re.sub(r'^\d+\s*', '', line)
        video_titles.append(clean_line)
        seen.add(line)

        # 只取前10个
        if len(video_titles) >= 10:
            break

# 如果上面的方法没找到，尝试直接找包含 [中文字幕] 的行
if len(video_titles) < 5:
    for line in lines:
        if '[中文字幕]' in line and len(line) < 80:
            if not any(re.search(pattern, line) for pattern in exclude_patterns):
                clean_line = re.sub(r'^\d+\s*', '', line)
                if clean_line not in video_titles:
                    video_titles.append(clean_line)
                if len(video_titles) >= 10:
                    break

# 输出结果
print("\n" + "=" * 50)
print(f"✅ 前 {len(video_titles)} 个视频名称：")
print("=" * 50)
for i, title in enumerate(video_titles[:10], 1):
    print(f"{i:2d}. {title}")
print("=" * 50)