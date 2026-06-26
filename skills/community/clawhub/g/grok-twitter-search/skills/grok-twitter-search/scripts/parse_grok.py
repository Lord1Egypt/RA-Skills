#!/usr/bin/env python3
"""测试 Grok 返回数据解析"""
import re
import json

# 模拟 Grok API 返回的文本
grok_text = '''Here are the most recent tweets (up to 5) from @cz_binance containing "musk", sorted by latest first:[[1]](https://x.com/i/status/1988689709045047579)[[2]](https://x.com/i/status/1957019646000865521)[[3]](https://x.com/i/status/1705212160295473459)

1. **Nov 12, 2025** (Likes: 3.8K, Views: 918K):  
   "Our intern tells me that 60% of the comments under my posts are likely AI generated or assisted. Same for Elon Musk's posts."  
   [[1]](https://x.com/i/status/1988689709045047579)

2. **Aug 17, 2025** (Likes: 96, Views: 25K):  
   "Vintage CZ"  
   [[2]](https://x.com/i/status/1957019646000865521)

3. **Sep 22, 2023** (Likes: 3.7K, Views: 580K):  
   "The new Elon Musk book by Walter Isaacson is pretty good."
   [[3]](https://x.com/i/status/1705212160295473459)'''

def parse_grok_tweets(text: str, max_results: int = 10):
    """解析 Grok 返回的格式化推文数据"""
    tweets = []
    
    # 1. 提取所有推文链接（创建编号到 URL 的映射）
    url_pattern = r'\[\[(\d+)\]\]\(https://x\.com/i/status/(\d+)\)'
    url_matches = re.findall(url_pattern, text)
    url_map = {num: url for num, url in url_matches}
    
    # 2. 提取推文基本信息：编号、日期、点赞数
    tweet_pattern = r'(\d+)\.\s+\*\*([^*]+)\*\*\s*\(Likes:\s*([\d.]+[KMB]*)'
    matches = re.findall(tweet_pattern, text)
    
    for num, date, likes in matches:
        if len(tweets) >= max_results:
            break
        
        # 解析点赞数
        like_count = 0
        if likes and likes.strip():
            like_str = likes.strip()
            try:
                if 'K' in like_str:
                    like_count = int(float(like_str.replace('K', '')) * 1000)
                elif 'M' in like_str:
                    like_count = int(float(like_str.replace('M', '')) * 1000000)
                elif 'B' in like_str:
                    like_count = int(float(like_str.replace('B', '')) * 1000000000)
                else:
                    like_count = int(float(like_str))
            except:
                pass
        
        # 提取推文内容
        start_marker = f"{num}. **"
        start_idx = text.find(start_marker)
        if start_idx != -1:
            next_num = int(num) + 1
            end_marker = f"{next_num}. **"
            end_idx = text.find(end_marker, start_idx)
            if end_idx == -1:
                end_idx = len(text)
            
            segment = text[start_idx:end_idx]
            content_match = re.search(r'"([^"]+)"', segment)
            content = content_match.group(1) if content_match else ""
        else:
            content = ""
        
        tweet_url = f"https://x.com/i/status/{url_map.get(num, '')}"
        
        tweets.append({
            "author": "@cz_binance",
            "content": content.strip()[:500],
            "timestamp": date.strip(),
            "likes": like_count,
            "retweets": 0,
            "url": tweet_url if url_map.get(num) else ""
        })
    
    return tweets

result = parse_grok_tweets(grok_text, max_results=5)
print(json.dumps(result, indent=2, ensure_ascii=False))
