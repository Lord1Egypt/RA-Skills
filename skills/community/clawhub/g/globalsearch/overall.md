
# Global Search
# 注意：此脚本专门用于执行全面搜索（即同时搜索所有可用来源），当用户要求进行全面搜索时必须使用此脚本。
#
# ⚠️ 隐私和安全声明：
# - 本脚本会将用户查询发送到外部服务 https://clb.ciglobal.cn/web_search
# - 请确保已获得用户同意后再发送其查询
# - 不要处理敏感、机密或个人数据
# - 请使用环境变量存储API密钥，切勿硬编码
# - 服务提供商 (clb.ciglobal.cn) 是第三方服务，使用前请验证其可信度
# - API密钥会将所有查询与您的账户关联，提供商可能会记录搜索历史
#
# 使用说明：
# 1. 设置环境变量: GLOBAL_SEARCH_API_KEY=your_api_key_here
# 2. 修改下面的 keyword 和 page 变量为实际值
# 3. 运行此脚本执行全面搜索

from aiohttp import FormData

# 定义四种请求配置
SEARCH_CONFIGS = [
    {
        "id":3,
        "name": "百度搜索",
        "mode": "network",
        "search_source": "baidu_search"
    },
    {   "id":2,
        "name": "谷歌搜索",
        "mode": "network",
        "search_source": "google_search"
    },
    {
        "id":1,
        "name": "百度AI搜索",
        "mode": "network",
        "search_source": "baidu_search_ai"
    },
    {
        "id":4,
        "name": "全库搜",
        "mode": "warehouse",
        "search_source": None  # 全库搜模式下不需要search_source
    }
]


import aiohttp
import asyncio
import json
import os

# ===== 配置区域 =====
API_URL = "https://clb.ciglobal.cn/web_search"
# 从环境变量获取API密钥（推荐方式）
API_KEY = os.environ.get("GLOBAL_SEARCH_API_KEY", "your_api_key_here")

if API_KEY == "your_api_key_here":
    raise ValueError("请设置 GLOBAL_SEARCH_API_KEY 环境变量，或在此处填入您的API密钥")

keyword = "人工智能"  # TODO: 替换为搜索关键词
page = 1  # TODO: 替换为页码
# ==================

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/x-www-form-urlencoded",
}
async def fetch_data(semaphore, i):
    async with semaphore:  # 控制并发数
        print(f"开始请求 {i}")

        async with aiohttp.ClientSession() as session:
            result_data = None
            for item in SEARCH_CONFIGS:
                if item['id'] == i:
                    result_data = item
                    break
            data = {
                "keyword": keyword,
                "page": page,
                "mode": result_data['mode'],
                "search_source": result_data['search_source']
            }
            async with session.post(API_URL, headers=headers,data=data) as response:
                # 重要：必须 await response.json()
                try:
                    result = await response.json()
                except Exception as e:
                    print(e)
                    result = {}
                references = result.get('references')
                return references

async def main():
    semaphore = asyncio.Semaphore(5)  # 最多同时5个请求
    tasks = [fetch_data(semaphore, i) for i in range(1,5)]
    results = await asyncio.gather(*tasks)
    result = []
    for item in results:
        result += item
    print(result)
    return result

asyncio.run(main())
