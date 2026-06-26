# -*- coding: utf-8 -*-
"""
浏阳本地生活 Skill - MCP 后端服务
功能：找师傅（疏通/水电/开锁/搬家等）、找餐厅农庄、找酒店
端口：8002
"""

import sys
import json
from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from data import (
    search_services, search_restaurants, search_hotels,
    SERVICE_CATEGORIES, RESTAURANT_CATEGORIES,
    SERVICE_WORKERS, RESTAURANTS, HOTELS
)

sys.stdout.reconfigure(encoding="utf-8")

app = FastAPI(
    title="浏阳本地生活 Skill",
    description="浏阳本地生活服务助手：找师傅、找餐厅、找酒店",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# MCP 协议入口
# ============================================================
@app.post("/")
async def mcp_endpoint(request: Request):
    """MCP JSON-RPC 2.0 入口"""
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(content={
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32700, "message": "Parse error"}
        })

    method = body.get("method", "")
    req_id = body.get("id")
    params = body.get("params", {})

    if method == "initialize":
        return mcp_response(req_id, {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": "liuduoduo-life-skill", "version": "0.1.0"}
        })

    elif method == "tools/list":
        return mcp_response(req_id, {"tools": TOOLS_LIST})

    elif method == "tools/call":
        tool_name = params.get("name", "")
        args = params.get("arguments", {})
        result = handle_tool_call(tool_name, args)
        return mcp_response(req_id, {
            "content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False, indent=2)}]
        })

    elif method == "notifications/initialized":
        return JSONResponse(content="")

    else:
        return JSONResponse(content={
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Method not found: {method}"}
        })


def mcp_response(req_id, result):
    return JSONResponse(content={
        "jsonrpc": "2.0",
        "id": req_id,
        "result": result
    })


# ============================================================
# 工具列表
# ============================================================
TOOLS_LIST = [
    {
        "name": "find_service",
        "description": "查找浏阳本地生活服务师傅。用户说'下水道堵了'、'找个开锁的'、'要搬家'、'空调坏了'、'水管漏了'等生活服务需求时使用。返回师傅的姓名、电话、价格、评价。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "服务类别：疏通下水道、水电维修、开锁换锁、搬家、家电维修、空调清洗、防水补漏"
                },
                "keyword": {
                    "type": "string",
                    "description": "搜索关键词，如：马桶、漏水、空调等"
                }
            },
            "required": []
        }
    },
    {
        "name": "find_restaurant",
        "description": "查找浏阳本地餐厅或农庄。用户说'请客吃饭'、'浏阳特色菜'、'找个农庄'、'吃蒸菜'等时使用。可以按预算、人数、是否要风景来筛选。返回餐厅名称、地址、人均价格、特色菜、电话。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "budget_per_person": {
                    "type": "number",
                    "description": "人均预算（元）。如果用户说总预算500元6个人，请算好人均再传入（约83元）"
                },
                "people_count": {
                    "type": "number",
                    "description": "用餐人数"
                },
                "want_scenery": {
                    "type": "boolean",
                    "description": "是否要有风景/环境好的（农庄类）。用户提到'风景好'、'有特色'、'农庄'时设为true"
                },
                "keyword": {
                    "type": "string",
                    "description": "搜索关键词，如：蒸菜、农庄、河鲜、大围山、烧烤等"
                }
            },
            "required": []
        }
    },
    {
        "name": "find_hotel",
        "description": "查找浏阳本地酒店住宿。用户说'订酒店'、'住哪里'、'推荐酒店'等时使用。可以按价格、位置、是否有早餐来筛选。返回酒店名称、地址、价格、设施、电话。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "max_price": {
                    "type": "number",
                    "description": "每晚最高预算（元）"
                },
                "need_breakfast": {
                    "type": "boolean",
                    "description": "是否需要含早餐"
                },
                "near_landmark": {
                    "type": "string",
                    "description": "靠近哪个地标，如：天空剧院、步行街、大围山"
                },
                "room_type": {
                    "type": "string",
                    "description": "房间类型：大床房、双床房、家庭房、套房"
                }
            },
            "required": []
        }
    }
]


# ============================================================
# 工具调用处理
# ============================================================
def handle_tool_call(tool_name, args):
    if tool_name == "find_service":
        category = args.get("category")
        keyword = args.get("keyword")
        return search_services(category=category, keyword=keyword)

    elif tool_name == "find_restaurant":
        budget = args.get("budget_per_person")
        people = args.get("people_count")
        scenery = args.get("want_scenery", False)
        keyword = args.get("keyword")
        return search_restaurants(
            budget_per_person=budget,
            people_count=people,
            want_scenery=scenery,
            keyword=keyword
        )

    elif tool_name == "find_hotel":
        max_price = args.get("max_price")
        breakfast = args.get("need_breakfast", False)
        landmark = args.get("near_landmark")
        room_type = args.get("room_type")
        return search_hotels(
            max_price=max_price,
            need_breakfast=breakfast,
            near_landmark=landmark,
            room_type=room_type
        )

    else:
        return {"error": f"未知工具: {tool_name}"}


# ============================================================
# 健康检查
# ============================================================
@app.get("/health")
async def health():
    return {"status": "ok", "service": "liuduoduo-life-skill", "version": "0.1.0"}


# ============================================================
# 调试接口（浏览器直接访问测试）
# ============================================================
@app.get("/services")
async def api_services(category: Optional[str] = None, keyword: Optional[str] = None):
    """浏览器调试：查看服务师傅"""
    return search_services(category=category, keyword=keyword)


@app.get("/restaurants")
async def api_restaurants(
    budget: Optional[int] = None,
    people: Optional[int] = None,
    scenery: bool = False,
    keyword: Optional[str] = None
):
    """浏览器调试：查看餐厅"""
    return search_restaurants(
        budget_per_person=budget,
        people_count=people,
        want_scenery=scenery,
        keyword=keyword
    )


@app.get("/hotels")
async def api_hotels(
    max_price: Optional[int] = None,
    breakfast: bool = False,
    landmark: Optional[str] = None,
    room_type: Optional[str] = None
):
    """浏览器调试：查看酒店"""
    return search_hotels(
        max_price=max_price,
        need_breakfast=breakfast,
        near_landmark=landmark,
        room_type=room_type
    )


@app.get("/categories")
async def api_categories():
    """查看所有可用分类"""
    return {
        "service_categories": SERVICE_CATEGORIES,
        "restaurant_categories": RESTAURANT_CATEGORIES,
        "total_services": len(SERVICE_WORKERS),
        "total_restaurants": len(RESTAURANTS),
        "total_hotels": len(HOTELS)
    }


if __name__ == "__main__":
    import uvicorn
    print("=" * 50)
    print("  浏阳本地生活 Skill 启动中...")
    print("  打开浏览器访问: http://127.0.0.1:8002/docs")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=8002)
