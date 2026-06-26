import requests
from bs4 import BeautifulSoup
import datetime
import os
import argparse
import json
import time

def get_abstract(pmid, headers):
    """根据 PMID 抓取具体的摘要内容"""
    url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
    try:
        # 稍微给一点延迟，防止 PubMed 屏蔽 T580 的 IP
        time.sleep(0.5) 
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'lxml')
        # 抓取摘要正文
        abstract_div = soup.select_one('.abstract-content')
        if abstract_div:
            # 清洗多余的空格和换行
            return " ".join(abstract_div.text.split())
        return "No abstract available."
    except:
        return "Failed to retrieve abstract."

def fetch_weekly_intel(journal_name, paper_type="Article", days=7):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    base_url = "https://pubmed.ncbi.nlm.nih.gov/"
    
    pt_filter = "journal+article" if paper_type.lower() == "article" else "review"
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=days)
    date_range = f"{start_date.strftime('%Y/%m/%d')}:{today.strftime('%Y/%m/%d')}"
    query_journal = journal_name.replace(" ", "+")
    
    try:
        # 1. 初始检索
        search_url = (
            f"{base_url}?term=%22{query_journal}%22%5BJournal%5D+"
            f"AND+%22{pt_filter}%22%5BPublication+Type%5D+"
            f"AND+{date_range}%5Bpdat%5D&sort=date&size=50" # 建议周报先抓前50篇，保证速度
        )
        
        print(f"📡 正在获取列表: {journal_name} | {paper_type}")
        res = requests.get(search_url, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, 'lxml')
        articles = soup.select('.docsum-content')
        
        if not articles:
            print(f"☕ 期间无新内容。")
            return

        articles_data_list = []
        total = len(articles)
        print(f"✅ 发现 {total} 篇文献，开始深度提取摘要（这可能需要一两分钟）...")

        # 2. 循环进入每一篇详情页抓摘要
        for i, art in enumerate(articles, 1):
            title = art.select_one('.docsum-title').text.strip()
            pmid = art.select_one('.docsum-pmid').text.strip()
            
            print(f"  [{i}/{total}] 正在提取 PMID: {pmid} 的摘要...")
            abstract_text = get_abstract(pmid, headers)
            
            articles_data_list.append({
                "pmid": pmid,
                "english_title": title,
                "abstract": abstract_text # 核心：现在有了全文摘要
            })

        # 3. 保存为 JSON
        save_dir = os.path.expanduser(f"~/Documents/Journal_Intel")
        if not os.path.exists(save_dir): os.makedirs(save_dir)
        
        file_path = os.path.join(save_dir, f"{journal_name.replace(' ', '_')}_{today}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(articles_data_list, f, ensure_ascii=False, indent=4)
        
        print(f"🚀 深度情报收集完成！原始 JSON 已存至: {file_path}")

    except Exception as e:
        print(f"💥 故障: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--journal", type=str, required=True)
    parser.add_argument("--type", type=str, default="Article")
    parser.add_argument("--days", type=int, default=7)
    args = parser.parse_args()
    fetch_weekly_intel(args.journal, args.type, args.days)
