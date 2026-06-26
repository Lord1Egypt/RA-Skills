#!/usr/bin/env python3
"""美团旅行助手 v1.0 - 酒店/机票/火车票/景点门票/行程规划一站式查询
零配置即装即用，数据覆盖全国300+城市"""

import sys
import json
import urllib.request
import urllib.error

PROXY_URL = "https://1439498936-5f2xpfi4t3.ap-guangzhou.tencentscf.com"
PROXY_TOKEN = "tp_8k2mX9vQ4z"


def _post(type_name, params):
    """调用美团代理"""
    body = json.dumps({"type": type_name, "params": params}, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    req = urllib.request.Request(PROXY_URL, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("X-Proxy-Token", PROXY_TOKEN)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("code") == 0:
                return data.get("data", {})
            return data
    except urllib.error.HTTPError as e:
        err = ""
        try:
            err = e.read().decode("utf-8")[:300]
        except:
            pass
        return {"error": "HTTP " + str(e.code) + ": " + err}
    except Exception as e:
        return {"error": str(e)}


def tool_meituan_travel_query(params):
    """美团旅行综合查询：酒店/机票/火车票/景点门票/行程规划一站式服务"""
    city = params.get("city", "")
    query = params.get("query", "")
    if not city or not query:
        return {"error": "city和query均为必填参数"}
    return _post("meituan_travel_query", {"city": city, "query": query})


# ==================== 工具路由 ====================

TOOLS = {
    "meituan_travel_query": tool_meituan_travel_query,
}


def main():
    if len(sys.argv) < 3:
        print(json.dumps({"error": "用法: python3 main.py <tool> '<json_params>'", "available_tools": list(TOOLS.keys())}, ensure_ascii=False))
        sys.exit(1)

    tool_name = sys.argv[1]
    try:
        params = json.loads(sys.argv[2])
    except json.JSONDecodeError as e:
        print(json.dumps({"error": "参数JSON解析失败: " + str(e)}, ensure_ascii=False))
        sys.exit(1)

    if tool_name not in TOOLS:
        print(json.dumps({"error": "未知工具: " + tool_name, "available_tools": list(TOOLS.keys())}, ensure_ascii=False))
        sys.exit(1)

    try:
        result = TOOLS[tool_name](params)
        print(json.dumps(result, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
