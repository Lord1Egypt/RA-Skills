#!/usr/bin/env python3
"""
亚马逊评论抓取工具 - 使用 Bright Data API
分批获取评论，每次30条，支持1-3星筛选
"""

import requests
import json
import time
import sys
import urllib.parse

def get_reviews(product_url, api_key, batch_size=30, max_total=500):
    """
    获取亚马逊商品评论
    
    Args:
        product_url: 亚马逊商品URL
        api_key: Bright Data API Key
        batch_size: 每批获取数量
        max_total: 最大获取总数
    
    Returns:
        所有评论列表
    """
    encoded_url = urllib.parse.quote(product_url, safe='')
    
    # 使用 Bright Data 的结构化数据 API 获取 Amazon 评论
    base_url = "https://api.brightdata.com/datasets/v3/amazon_product_reviews"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    all_reviews = []
    offset = 0
    
    print(f"开始抓取评论: {product_url}")
    print(f"每批数量: {batch_size}, 最大总数: {max_total}")
    
    while offset < max_total:
        # 构建请求参数 - 筛选1-3星评论
        params = {
            "url": encoded_url,
            "reviews_star": "1,2,3",  # 筛选1-3星
            "limit": batch_size,
            "offset": offset
        }
        
        try:
            # 使用 Amazon Reviews Scraper API
            response = requests.get(
                base_url,
                headers=headers,
                params=params,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                reviews = data.get("reviews", [])
                
                if not reviews:
                    print(f"第 {(offset // batch_size) + 1} 批: 获取到 0 条评论，已完成所有数据抓取")
                    break
                
                all_reviews.extend(reviews)
                print(f"第 {(offset // batch_size) + 1} 批: 获取到 {len(reviews)} 条评论，累计 {len(all_reviews)} 条")
                
                if len(reviews) < batch_size:
                    print("已获取所有剩余评论")
                    break
                    
                offset += batch_size
                time.sleep(1)  # 避免请求过快
                
            elif response.status_code == 429:
                print("请求频率限制，等待10秒后重试...")
                time.sleep(10)
            else:
                print(f"请求失败: {response.status_code} - {response.text}")
                break
                
        except Exception as e:
            print(f"请求异常: {str(e)}")
            break
    
    print(f"\n总计获取 {len(all_reviews)} 条评论")
    return all_reviews

def extract_review_texts(reviews):
    """
    提取评论文本用于标注
    """
    extracted = []
    for i, review in enumerate(reviews, 1):
        # 提取评论内容
        text = review.get("body", review.get("text", ""))
        star = review.get("star", review.get("rating", ""))
        
        if text and star:
            extracted.append({
                "index": i,
                "star": star,
                "text": text[:500]  # 限制长度
            })
    
    return extracted

def main():
    if len(sys.argv) < 3:
        print("用法: python review_scraper.py <商品URL> <API_KEY>")
        sys.exit(1)
    
    product_url = sys.argv[1]
    api_key = sys.argv[2]
    
    reviews = get_reviews(product_url, api_key)
    extracted = extract_review_texts(reviews)
    
    # 输出JSON格式供后续处理
    output_file = "extracted_reviews.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(extracted, f, ensure_ascii=False, indent=2)
    
    print(f"评论已保存到 {output_file}")
    return extracted

if __name__ == "__main__":
    main()