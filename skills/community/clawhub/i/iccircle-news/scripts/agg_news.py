import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

def fetch_rss(url, source_name, max_items=5, keyword_filter=None):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req, timeout=10)
        xml_data = response.read().decode('utf-8')
        root = ET.fromstring(xml_data)
        
        items = root.findall('.//item')
        if not items:
            return
            
        print(f"====== 【{source_name}】 最新资讯 ======")
        count = 0
        for item in items:
            title = item.find('title')
            link = item.find('link')
            pubDate = item.find('pubDate')
            desc = item.find('description')
            
            t = title.text.strip() if title is not None and title.text else "No Title"
            l = link.text.strip() if link is not None and link.text else "No Link"
            d = pubDate.text.strip() if pubDate is not None and pubDate.text else ""
            c = desc.text.strip() if desc is not None and desc.text else ""
            
            if keyword_filter:
                match = any(k in t or k in c for k in keyword_filter)
                if not match:
                    continue
            
            print(f"[{count+1}] {t}")
            if d:
                print(f"    🕒时间: {d}")
            print(f"    🔗链接: {l}")
            print()
            
            count += 1
            if count >= max_items:
                break
                
        if count == 0:
            print("  （无匹配的相关资讯）")
            print()
            
    except Exception as e:
        print(f"[{source_name}] 抓取失败: {e}")
        print()

def main():
    print("🦞 小龙虾特供：聚合芯片与半导体领域资讯")
    print("--------------------------------------------------")
    print()

    # iccircle
    ic_columns = [
        ("IC技术圈官方", "https://iccircle.com/feed?column=IC%E6%8A%80%E6%9C%AF%E5%9C%88%E5%AE%98%E6%96%B9"),
        ("iLoveIC", "https://iccircle.com/feed?column=iLoveIC"),
        ("ExASIC", "https://iccircle.com/feed?column=ExASIC"),
        ("web开发笔记", "https://iccircle.com/feed?column=web%E5%BC%80%E5%8F%91%E7%AC%94%E8%AE%B0"),
        ("半导体行业快讯", "https://iccircle.com/feed?column=%E5%8D%8A%E5%AF%BC%E4%BD%93%E8%A1%8C%E4%B8%9A%E5%BF%AB%E8%AE%AF"),
        ("芯想事珹", "https://iccircle.com/feed?column=%E8%8A%AF%E6%83%B3%E4%BA%8B%E7%8F%B9"),
        ("NanDigits", "https://iccircle.com/feed?column=NanDigits")
    ]
    
    for display_name, feed_url in ic_columns:
        fetch_rss(feed_url, f"IC技术圈 - {display_name}", 3)

    # vlsiblogs agg rss
    fetch_rss("https://vlsiblogs.com/aggrss", "VLSI BLOGS Agg RSS", 8)
        
    # ithome
    keywords = ['芯片', '半导体', '晶圆', '台积电', '英伟达', 'AMD', 'Intel', '光刻机', '海思', 'EDA']
    fetch_rss("https://www.ithome.com/rss/", "IT之家 (芯片精选)", 3, keyword_filter=keywords)

    # 36kr
    fetch_rss("https://www.36kr.com/feed", "36氪", 3, keyword_filter=keywords)
    

if __name__ == "__main__":
    main()
