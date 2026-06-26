#!/usr/bin/env python3
"""
根据博物馆名称检索在展文物信息。
使用 ProSearch 搜索，大模型提取并整理文物列表。

用法：python3 search_artifacts.py "<museum_name>"
输出：JSON格式的文物列表，供 plan_route.py 使用
"""

import sys
import json
import os
import requests
from pathlib import Path
from typing import Optional, List, Dict, Any

# 导入离线数据加载器
sys.path.insert(0, str(Path(__file__).parent))
from load_references import load_artifacts_from_csv, list_available_museums

SEARCH_QUERIES = [
    "{museum} 镇馆之宝",
    "{museum} 文物 名单",
    "{museum} 在展文物",
    "{museum} 精品文物",
    "{museum} 著名文物",
    "{museum} 必看文物",
    "{museum} 馆藏珍品",
    "{museum} 参观攻略 文物",
]


from extract_profile import call_llm_api


def prosearch(keyword: str, count: int = 10) -> dict:
    """调用天集 ProSearch API 进行搜索"""
    port = os.environ.get("AUTH_GATEWAY_PORT", "19000")
    url = f"http://localhost:{port}/proxy/prosearch/search"
    
    payload = {"keyword": keyword, "cnt": count}
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def extract_artifacts_with_llm(search_results: List[str], museum_name: str) -> List[Dict]:
    """使用大模型从搜索结果中提取文物信息"""
    
    combined_content = "\n\n".join([
        f"--- 搜索结果 {i+1} ---\n{result[:1500]}"
        for i, result in enumerate(search_results[:12])
    ])

    prompt = f"""
你是一位博物馆文物专家。请从以下{museum_name}的搜索结果中提取文物信息。

要求：
1. 只提取该博物馆的**常设馆藏文物**，排除借展、巡展、复制品、仿品
2. 提取文物名称、所属展馆、所属时期、文物种类、是否是镇馆之宝、简要描述
2. 时期必须从以下列表中选择：远古时期、夏商西周、春秋战国、秦汉、三国两晋南北朝、隋唐五代、辽宋夏金元、明清
3. 文物种类必须从以下列表中选择：青铜器、陶器、瓷器、漆器、玉器宝石、石器石刻、书画古籍、服饰、砖瓦、钱币、化石、金银器、其他
4. 关注的领域从以下列表中选择：农耕、狩猎、饮食、建筑、人物、武器、文房四宝、牌章证件、货币、书法、绘画、雕像、服装、饰品、仪器、佛教、乐器、纹饰、花瓶、礼制、古生物、新石器、旧石器、陈设品、科技、其他
5. 如果搜索结果中未提及展馆，请使用"待确认"
6. 尽可能多地提取文物（至少20件）

请返回JSON数组格式：
[
    {{
        "name": "文物名称",
        "hall": "展馆名称",
        "period": "时期",
        "type": "文物种类",
        "is_treasure": true/false,
        "description": "简要描述",
        "domains": ["领域1", "领域2"],
        "child_friendly": true/false
    }}
]

搜索结果：
{combined_content}
"""

    try:
        result = call_llm_api(prompt)
        if "error" in result:
            print(f"大模型提取失败: {result['error']}", file=sys.stderr)
            return []
        return result if isinstance(result, list) else []
    except Exception as e:
        print(f"大模型提取异常: {e}", file=sys.stderr)
        return []


def search_artifacts(museum_name: str) -> list:
    """使用天集 ProSearch 搜索文物，大模型提取"""
    search_results = []
    
    for query_template in SEARCH_QUERIES:
        query = query_template.format(museum=museum_name)
        try:
            result = prosearch(query, count=10)
            
            docs = result.get('data', {}).get('docs', [])
            if not docs:
                continue
                
            for item in docs:
                passage = item.get('passage', '')
                if passage:
                    search_results.append(passage)
        except Exception:
            pass
    
    if not search_results:
        return []
    
    artifacts = extract_artifacts_with_llm(search_results, museum_name)
    return artifacts


def get_artifacts(museum_name: str) -> tuple:
    """
    获取博物馆文物列表。
    返回 (artifacts, source)，source 为 "offline" 或 "online"。
    """
    # 优先查找离线数据
    offline = load_artifacts_from_csv(museum_name)
    if offline is not None:
        print(f"[离线模式] 使用 references/ 中的数据，共 {len(offline)} 件文物", file=sys.stderr)
        return offline, "offline"

    # 没有离线数据，走在线搜索
    print(f"[在线模式] 未找到 {museum_name} 的离线数据，启动联网搜索...", file=sys.stderr)
    artifacts = search_artifacts(museum_name)
    return artifacts, "online"


def main():
    museum_name = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    if not museum_name:
        print(json.dumps({"error": "请提供博物馆名称"}, ensure_ascii=False))
        sys.exit(1)

    artifacts, source = get_artifacts(museum_name)

    # 描述由 plan_route.py 的 summarize_reasons_with_llm 统一生成
    print(json.dumps({
        "museum_name": museum_name,
        "source": source,
        "artifacts_count": len(artifacts),
        "artifacts": artifacts
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
