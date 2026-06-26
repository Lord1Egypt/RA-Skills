#!/usr/bin/env python3
"""
OWS - 搜索全球采购需求
自动搜索 MoltsList、Moltbook、OW 社区等平台的买家需求
"""

import json
import pathlib
import requests
import sys
from datetime import datetime

STATE_DIR = pathlib.Path(__file__).resolve().parent.parent / "state"
OPPS_DIR = STATE_DIR / "opportunities"

# 平台配置
PLATFORMS = {
    "moltslist": {
        "base_url": "https://moltslist.com/api/v1",
        "auth_required": True,
        "endpoint": "/listings?type=request"
    },
    "moltbook": {
        "base_url": "https://moltbook.com/api",
        "auth_required": False,
        "endpoint": "/posts?type=request"
    },
    "ow": {
        "base_url": "http://localhost:3000/api",
        "auth_required": False,
        "endpoint": "/posts?type=request"
    }
}

def search_moltslist(api_key=None, category=None, limit=50):
    """搜索 MoltsList 采购需求"""
    url = f"{PLATFORMS['moltslist']['base_url']}{PLATFORMS['moltslist']['endpoint']}&limit={limit}"
    if category:
        url += f"&category={category}"
    
    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                return data.get("listings", [])
    except Exception as e:
        print(f"MoltsList 搜索失败：{e}")
    
    return []

def search_moltbook(limit=50):
    """搜索 Moltbook 采购需求"""
    url = f"{PLATFORMS['moltbook']['base_url']}{PLATFORMS['moltbook']['endpoint']}&limit={limit}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                return data.get("posts", [])
    except Exception as e:
        print(f"Moltbook 搜索失败：{e}")
    
    return []

def search_ow(base_url="http://localhost:3000", limit=50):
    """搜索 OW 社区采购需求"""
    url = f"{base_url}{PLATFORMS['ow']['endpoint']}&limit={limit}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                return data.get("posts", [])
    except Exception as e:
        print(f"OW 社区搜索失败：{e}")
    
    return []

def save_opportunity(opportunity):
    """保存销售机会到本地"""
    OPPS_DIR.mkdir(parents=True, exist_ok=True)
    opp_file = OPPS_DIR / f"{opportunity['req_id']}.json"
    opp_file.write_text(json.dumps(opportunity, indent=2, ensure_ascii=False))

def search_all_platforms(api_key=None, category=None):
    """搜索所有平台"""
    print("🔍 开始搜索全球采购需求...\n")
    
    all_opportunities = []
    
    # 搜索 MoltsList
    print("📦 搜索 MoltsList...")
    moltslist_results = search_moltslist(api_key, category)
    print(f"   找到 {len(moltslist_results)} 个需求")
    all_opportunities.extend(moltslist_results)
    
    # 搜索 Moltbook
    print("📦 搜索 Moltbook...")
    moltbook_results = search_moltbook()
    print(f"   找到 {len(moltbook_results)} 个需求")
    all_opportunities.extend(moltbook_results)
    
    # 搜索 OW 社区
    print("📦 搜索 OW 社区...")
    ow_results = search_ow()
    print(f"   找到 {len(ow_results)} 个需求")
    all_opportunities.extend(ow_results)
    
    # 去重
    seen = set()
    unique_opps = []
    for opp in all_opportunities:
        key = opp.get("req_id") or opp.get("id")
        if key and key not in seen:
            seen.add(key)
            unique_opps.append(opp)
    
    print(f"\n✅ 共找到 {len(unique_opps)} 个独立采购需求")
    
    # 保存到本地
    for opp in unique_opps:
        save_opportunity(opp)
    
    return unique_opps

def format_opportunities(opportunities):
    """格式化输出"""
    if not opportunities:
        return "❌ 未找到匹配的采购需求"
    
    output = f"🛒 找到 {len(opportunities)} 个采购需求\n\n"
    
    for i, opp in enumerate(opportunities[:10], 1):
        output += f"{i}. {opp.get('item') or opp.get('title') or '未知商品'}\n"
        output += f"   预算：¥{opp.get('budget_max') or opp.get('priceCredits') or '面议'}\n"
        output += f"   买家：{opp.get('buyer') or opp.get('agent_name') or '未知'}\n"
        output += f"   截止：{opp.get('deadline') or opp.get('created_at') or '未知'}\n"
        output += f"   来源：{opp.get('source') or '平台'}\n\n"
    
    if len(opportunities) > 10:
        output += f"... 还有 {len(opportunities) - 10} 个需求\n"
    
    return output

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="搜索全球采购需求")
    parser.add_argument("--category", "-c", help="商品类别")
    parser.add_argument("--api-key", "-k", help="MoltsList API Key")
    parser.add_argument("--save", "-s", action="store_true", help="保存到本地")
    
    args = parser.parse_args()
    
    opportunities = search_all_platforms(args.api_key, args.category)
    
    if args.save:
        for opp in opportunities:
            save_opportunity(opp)
        print(f"💾 已保存到 {OPPS_DIR}")
    
    print("\n" + format_opportunities(opportunities))

if __name__ == "__main__":
    main()