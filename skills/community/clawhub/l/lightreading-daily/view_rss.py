# -*- coding: utf-8 -*-
"""查看 RSS 内容"""
import cloudscraper
import xml.etree.ElementTree as ET

def view_rss(url, limit=10):
    """查看 RSS 最新文章"""
    scraper = cloudscraper.create_scraper()
    resp = scraper.get(url, timeout=60)
    
    root = ET.fromstring(resp.content)
    namespaces = {'dc': 'http://purl.org/dc/elements/1.1/'}
    
    print("=" * 70)
    print("RSS: {}".format(url))
    print("=" * 70)
    
    items = root.findall('.//item')[:limit]
    
    for i, item in enumerate(items, 1):
        title = item.find('title')
        link = item.find('link')
        pub_date = item.find('pubDate')
        desc = item.find('description')
        creator = item.find('dc:creator', namespaces)
        
        print("\n[{}] {}".format(i, title.text if title is not None else 'N/A'))
        print("    链接：{}".format(link.text if link is not None else 'N/A'))
        print("    日期：{}".format(pub_date.text if pub_date is not None else 'N/A'))
        print("    作者：{}".format(creator.text if creator is not None and creator.text else '(无)'))
        if desc is not None and desc.text:
            preview = desc.text[:100].replace('\n', ' ')
            print("    摘要：{}...".format(preview))

# 查看 LightReading RSS
view_rss('https://www.lightreading.com/rss.xml', limit=10)

# 查看 TechCrunch RSS
print("\n\n")
view_rss('https://techcrunch.com/feed/', limit=10)
