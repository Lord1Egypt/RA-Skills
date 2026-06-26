import requests
from bs4 import BeautifulSoup
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_github_trending():
    url = "https://github.com/trending?since=daily"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = soup.find_all('article', class_='Box-row')
        
        print("🔥 GitHub 今日趋势榜 Top 5:\n" + "-"*30)
        
        for i, article in enumerate(articles[:10], 1):
            # 获取项目名称
            title_tag = article.find('h2', class_='h3 lh-condensed')
            title = title_tag.text.strip().replace('\n', '').replace(' ', '') if title_tag else "未知项目"
            
            # 💡 这里是修改的地方：直接抓取 p 标签
            desc_tag = article.find('p')
            
            # 清洗一下文本，有时候简介里会有奇怪的换行
            desc = desc_tag.text.strip().replace('\n', ' ') if desc_tag else "作者很懒，暂无简介"
            
            print(f"{i}. 项目: {title}\n   简介: {desc}\n")
            
    except Exception as e:
        print(f"抓取失败: {e}")

if __name__ == "__main__":
    get_github_trending()