#!/usr/bin/env python3
"""
测试MCP SSE API响应
"""

import json
import subprocess
import time

def test_mcp_api():
    """测试MCP API"""
    print("测试 InvestmentTracker MCP API (SSE版本)")
    print("=" * 70)
    
    # 测试请求
    test_requests = [
        {
            "name": "tools/list - 获取工具列表",
            "data": {
                "jsonrpc": "2.0",
                "method": "tools/list",
                "params": {},
                "id": 1
            }
        },
        {
            "name": "resources/list - 获取资源列表",
            "data": {
                "jsonrpc": "2.0",
                "method": "resources/list",
                "params": {},
                "id": 2
            }
        },
        {
            "name": "tools/call - 调用whoami_v1工具",
            "data": {
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": "whoami_v1",
                    "arguments": {}
                },
                "id": 3
            }
        },
        {
            "name": "tools/call - 调用positions_list_v1工具",
            "data": {
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": "positions_list_v1",
                    "arguments": {
                        "status": "POSITION",
                        "limit": 10
                    }
                },
                "id": 4
            }
        }
    ]
    
    for test in test_requests:
        print(f"\n🔧 测试: {test['name']}")
        print("-" * 70)
        
        # 保存请求数据
        request_file = f"/tmp/mcp_request_{test['data']['id']}.json"
        with open(request_file, 'w') as f:
            json.dump(test['data'], f)
        
        # 构建curl命令
        cmd = [
            'curl', '-s', '-N',
            '-H', 'Authorization: Bearer it_live_E8MnP28kdPmgpxdjfRG1wzUB9Nr7mCiBU34NjFkAPes',
            '-H', 'Accept: application/json, text/event-stream',
            '-H', 'Content-Type: application/json',
            '-X', 'POST',
            '--data-binary', f'@{request_file}',
            'https://investmenttracker-ingest-production.up.railway.app/mcp'
        ]
        
        try:
            # 运行命令并捕获输出
            print("发送请求...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            
            if result.stdout:
                print("响应内容:")
                print(result.stdout)
                
                # 尝试解析SSE事件
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if line.startswith('data: '):
                        try:
                            data = json.loads(line[6:])
                            print(f"解析的JSON数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
                        except json.JSONDecodeError as e:
                            print(f"JSON解析错误: {e}")
                            print(f"原始数据: {line[:100]}...")
            else:
                print("无响应内容")
                
            if result.stderr:
                print(f"错误输出: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print("请求超时")
        except Exception as e:
            print(f"执行错误: {e}")

def analyze_tools():
    """分析可用的工具"""
    print("\n" + "=" * 70)
    print("📋 可用工具分析")
    print("=" * 70)
    
    # 从之前的响应中提取工具信息
    tools = [
        {
            "name": "whoami_v1",
            "description": "获取用户身份信息",
            "inputSchema": {"type": "object", "properties": {}},
            "execution": {"taskSupport": "forbidden"}
        },
        {
            "name": "methodology_get_v1",
            "description": "获取投资方法论",
            "inputSchema": {"type": "object", "properties": {}},
            "execution": {"taskSupport": "forbidden"}
        },
        {
            "name": "stats_quick_v1",
            "description": "快速统计数据",
            "inputSchema": {"type": "object", "properties": {}},
            "execution": {"taskSupport": "forbidden"}
        },
        {
            "name": "positions_list_v1",
            "description": "列出持仓位置",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "status": {"type": "string", "enum": ["POSITION", "CLOSE"]},
                    "limit": {"type": "integer", "minimum": 1, "maximum": 200},
                    "offset": {"type": "integer", "minimum": 0}
                },
                "additionalProperties": False,
                "$schema": "http://json-schema.org/draft-07/schema#"
            },
            "execution": {"taskSupport": "forbidden"}
        }
    ]
    
    print("发现以下工具:")
    for tool in tools:
        print(f"\n🔧 {tool['name']}:")
        print(f"   描述: {tool['description']}")
        print(f"   输入参数: {json.dumps(tool['inputSchema'], ensure_ascii=False)}")
        print(f"   执行支持: {tool['execution']['taskSupport']}")

def create_skill_implementation():
    """创建skill实现"""
    print("\n" + "=" * 70)
    print("🚀 InvestmentTracker Skill 实现方案")
    print("=" * 70)
    
    implementation = '''
class InvestmentTrackerMCPClient:
    """MCP客户端实现"""
    
    def __init__(self, auth_token):
        self.base_url = "https://investmenttracker-ingest-production.up.railway.app/mcp"
        self.auth_token = auth_token
        self.headers = {
            "Authorization": f"Bearer {auth_token}",
            "Accept": "application/json, text/event-stream",
            "Content-Type": "application/json"
        }
    
    def send_request(self, method, params=None):
        """发送MCP请求"""
        import requests
        import json
        
        request = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
            "id": int(time.time() * 1000)
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=request,
                timeout=30,
                stream=True  # 重要：SSE需要流式响应
            )
            
            if response.status_code == 200:
                # 处理SSE响应
                events = []
                for line in response.iter_lines(decode_unicode=True):
                    if line.startswith('data: '):
                        try:
                            event_data = json.loads(line[6:])
                            events.append(event_data)
                        except json.JSONDecodeError:
                            continue
                return events
            else:
                return {"error": f"HTTP {response.status_code}", "details": response.text}
                
        except Exception as e:
            return {"error": str(e)}

class InvestmentTrackerSkill:
    """InvestmentTracker技能"""
    
    def __init__(self):
        self.client = InvestmentTrackerMCPClient(
            auth_token="it_live_E8MnP28kdPmgpxdjfRG1wzUB9Nr7mCiBU34NjFkAPes"
        )
    
    def get_user_info(self):
        """获取用户信息"""
        result = self.client.send_request("tools/call", {
            "name": "whoami_v1",
            "arguments": {}
        })
        return result
    
    def list_positions(self, status="POSITION", limit=10):
        """列出持仓"""
        result = self.client.send_request("tools/call", {
            "name": "positions_list_v1",
            "arguments": {
                "status": status,
                "limit": limit
            }
        })
        return result
    
    def get_methodology(self):
        """获取投资方法论"""
        result = self.client.send_request("tools/call", {
            "name": "methodology_get_v1",
            "arguments": {}
        })
        return result
    
    def get_quick_stats(self):
        """获取快速统计"""
        result = self.client.send_request("tools/call", {
            "name": "stats_quick_v1",
            "arguments": {}
        })
        return result
'''
    
    print(implementation)

def update_skill_files():
    """更新skill文件建议"""
    print("\n" + "=" * 70)
    print("📁 需要更新的文件:")
    print("=" * 70)
    
    updates = {
        "SKILL.md": """
## 更新内容：
1. 添加MCP API工具列表
2. 更新使用示例
3. 添加SSE响应处理说明

## 可用工具：
- `whoami_v1` - 获取用户身份信息
- `methodology_get_v1` - 获取投资方法论  
- `stats_quick_v1` - 快速统计数据
- `positions_list_v1` - 列出持仓位置
""",
        
        "config.json": """
{
  "mcp_server": {
    "url": "https://investmenttracker-ingest-production.up.railway.app/mcp",
    "auth_token": "it_live_E8MnP28kdPmgpxdjfRG1wzUB9Nr7mCiBU34NjFkAPes",
    "protocol": "sse",
    "headers": {
      "Accept": "application/json, text/event-stream",
      "Content-Type": "application/json"
    },
    "timeout": 30
  },
  "tools": {
    "whoami_v1": {
      "description": "获取用户身份信息",
      "parameters": {}
    },
    "positions_list_v1": {
      "description": "列出持仓位置",
      "parameters": {
        "status": ["POSITION", "CLOSE"],
        "limit": "1-200",
        "offset": ">=0"
      }
    }
  }
}
""",
        
        "scripts/fetch_data.py": """
需要重写为：
1. 使用requests库处理SSE流
2. 实现JSON-RPC 2.0请求
3. 添加工具调用方法
4. 完善错误处理
"""
    }
    
    for filename, content in updates.items():
        print(f"\n📄 {filename}:")
        print(content)

def main():
    """主函数"""
    print("InvestmentTracker MCP API 测试报告")
    print("生成时间:", time.strftime("%Y-%m-%d %H:%M:%S"))
    
    # 测试API
    test_mcp_api()
    
    # 分析工具
    analyze_tools()
    
    # 创建实现方案
    create_skill_implementation()
    
    # 更新建议
    update_skill_files()
    
    print("\n" + "=" * 70)
    print("✅ 测试完成")
    print("=" * 70)
    print("\n🎯 下一步行动:")
    print("1. 实现SSE客户端处理")
    print("2. 更新skill文件")
    print("3. 测试工具调用")
    print("4. 集成到OpenClaw技能系统")

if __name__ == "__main__":
    main()