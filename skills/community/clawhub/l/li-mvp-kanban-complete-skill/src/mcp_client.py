#!/usr/bin/env python3
"""
MCP 客户端测试脚本
演示如何调用 MCP 工具操作看板系统
"""
import requests
import json

BASE_URL = "http://localhost:9999"

class KanbanMCPClient:
    """简化版 MCP 客户端（通过 REST API）"""
    
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
    
    def call_tool(self, tool_name: str, params: dict = None):
        """调用 MCP 工具"""
        if params is None:
            params = {}
        
        # 映射 MCP 工具到 REST API
        api_map = {
            'list_projects': ('GET', '/api/projects', None),
            'add_project': ('POST', '/api/projects', params),
            'update_project_full': ('PUT', f"/api/projects/{params.get('project_id')}", params),
            'delete_project': ('DELETE', f"/api/projects/{params.get('project_id')}", None),
            'list_lanes': ('GET', '/api/lanes', None),
            'add_lane': ('POST', '/api/lanes', params),
            'delete_lane': ('DELETE', f"/api/lanes/{params.get('lane_id')}", None),
            'analyze_board': ('GET', '/api/llm/analyze', None),
            'nlp_command': ('POST', '/api/llm/command', {'command': params.get('command')}),
            'llm_search': ('POST', '/api/llm/search', params),
        }
        
        if tool_name not in api_map:
            raise ValueError(f"未知工具：{tool_name}")
        
        method, endpoint, data = api_map[tool_name]
        url = f"{self.base_url}{endpoint}"
        
        if method == 'GET':
            response = requests.get(url, params=data, timeout=10)
        elif method == 'POST':
            response = requests.post(url, json=data, timeout=10)
        elif method == 'PUT':
            # 移除 project_id
            put_data = {k: v for k, v in params.items() if k != 'project_id'}
            response = requests.put(url, json=put_data, timeout=10)
        elif method == 'DELETE':
            response = requests.delete(url, timeout=10)
        
        response.raise_for_status()
        return response.json()


def demo():
    """演示 MCP 工具调用"""
    print("="*60)
    print("MCP 客户端演示")
    print("="*60)
    
    client = KanbanMCPClient()
    
    # 1. 列出所有项目
    print("\n1️⃣ 列出所有项目")
    projects = client.call_tool("list_projects")
    print(f"   项目数：{len(projects)}")
    for p in projects[:3]:
        print(f"   - {p['name']} ({p['status']})")
    
    # 2. 添加项目
    print("\n2️⃣ 添加项目")
    result = client.call_tool("add_project", {
        "name": "MCP 客户端测试",
        "lane": "feature",
        "priority": "high",
        "assignee": "AI"
    })
    print(f"   ✅ 创建：{result['name']} (ID: {result['id']})")
    new_project_id = result['id']
    
    # 3. 更新项目
    print("\n3️⃣ 更新项目")
    result = client.call_tool("update_project_full", {
        "project_id": new_project_id,
        "status": "in_progress",
        "priority": "high"
    })
    print(f"   ✅ 更新：{result['name']} -> {result['status']}")
    
    # 4. AI 分析
    print("\n4️⃣ AI 看板分析")
    analysis = client.call_tool("analyze_board")
    print(f"   总任务数：{analysis['summary']['total_projects']}")
    print(f"   瓶颈数：{len(analysis.get('bottlenecks', []))}")
    print(f"   风险数：{len(analysis.get('risks', []))}")
    
    # 5. 自然语言命令
    print("\n5️⃣ 自然语言命令")
    result = client.call_tool("nlp_command", {
        "command": "添加一个低优先级的 bug 修复任务"
    })
    if result.get('success'):
        print(f"   ✅ 执行成功：{result['result']['name']}")
    else:
        print(f"   ⚠️ 执行失败：{result.get('error')}")
    
    # 6. 向量搜索
    print("\n6️⃣ 向量搜索")
    result = client.call_tool("llm_search", {
        "query": "测试",
        "limit": 3
    })
    print(f"   找到 {result.get('count', 0)} 个相似任务")
    for r in result.get('results', [])[:2]:
        print(f"   - {r['name']}")
    
    # 7. 列出泳道
    print("\n7️⃣ 列出泳道")
    lanes = client.call_tool("list_lanes")
    print(f"   泳道数：{len(lanes)}")
    for lane in lanes:
        print(f"   - {lane['icon']} {lane['name']} ({lane['id']})")
    
    # 8. 添加泳道
    print("\n8️⃣ 添加泳道")
    result = client.call_tool("add_lane", {
        "lane_id": "demo",
        "name": "演示泳道",
        "color": "#ff6b6b",
        "icon": "🎯"
    })
    print(f"   ✅ 创建：{result['name']}")
    
    # 9. 删除项目
    print("\n9️⃣ 删除项目")
    result = client.call_tool("delete_project", {
        "project_id": new_project_id
    })
    print(f"   ✅ 删除：{result.get('deleted', '成功')}")
    
    print("\n" + "="*60)
    print("演示完成！")
    print("="*60)


if __name__ == "__main__":
    try:
        demo()
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        print("请确保看板系统正在运行：http://localhost:9999")
