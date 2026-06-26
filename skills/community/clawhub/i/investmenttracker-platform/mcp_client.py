#!/usr/bin/env python3
"""
InvestmentTracker MCP 标准客户端
遵循 MCP (Model Context Protocol) 标准规范
"""

import json
import time
import asyncio
import aiohttp
from typing import Dict, Any, List, Optional
import sys

class InvestmentTrackerMCPClient:
    """MCP 标准客户端"""
    
    def __init__(self, server_url: str, api_key: str):
        self.server_url = server_url
        self.api_key = api_key
        self.session = None
        self.request_id = 1
        
    async def __aenter__(self):
        """异步上下文管理器入口"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self.session:
            await self.session.close()
    
    async def send_request(self, method: str, params: Dict = None) -> Optional[Dict[str, Any]]:
        """发送 MCP JSON-RPC 2.0 请求"""
        if not self.session:
            raise RuntimeError("Client not initialized. Use async context manager.")
        
        request = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
            "id": self.request_id
        }
        self.request_id += 1
        
        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        try:
            async with self.session.post(
                self.server_url,
                headers=headers,
                json=request,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    print(f"HTTP Error: {response.status}")
                    text = await response.text()
                    print(f"Response: {text}")
                    return None
                    
        except asyncio.TimeoutError:
            print("Request timeout")
            return None
        except Exception as e:
            print(f"Request error: {e}")
            return None
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """列出所有可用工具"""
        result = await self.send_request("tools/list")
        if result and "result" in result:
            return result["result"].get("tools", [])
        return []
    
    async def call_tool(self, tool_name: str, arguments: Dict = None) -> Optional[Dict[str, Any]]:
        """调用工具"""
        result = await self.send_request("tools/call", {
            "name": tool_name,
            "arguments": arguments or {}
        })
        if result and "result" in result:
            return result["result"]
        return None
    
    async def list_resources(self) -> List[Dict[str, Any]]:
        """列出所有可用资源"""
        result = await self.send_request("resources/list")
        if result and "result" in result:
            return result["result"].get("resources", [])
        return []
    
    async def read_resource(self, uri: str) -> Optional[Dict[str, Any]]:
        """读取资源"""
        result = await self.send_request("resources/read", {"uri": uri})
        if result and "result" in result:
            return result["result"]
        return None

class InvestmentTrackerSkill:
    """InvestmentTracker 技能（MCP标准版）"""
    
    def __init__(self, config_path: str = "mcp_config.json"):
        self.config_path = config_path
        self.config = self._load_config()
        self.client = None
        
    def _load_config(self) -> Dict[str, Any]:
        """加载配置"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # 默认配置
            return {
                "mcpServers": {
                    "investmenttracker": {
                        "url": "https://investmenttracker-ingest-production.up.railway.app/mcp",
                        "headers": {
                            "X-API-Key": "it_live_E8MnP28kdPmgpxdjfRG1wzUB9Nr7mCiBU34NjFkAPes"
                        }
                    }
                }
            }
    
    async def initialize(self):
        """初始化客户端"""
        server_config = self.config["mcpServers"]["investmenttracker"]
        self.client = InvestmentTrackerMCPClient(
            server_url=server_config["url"],
            api_key=server_config["headers"]["X-API-Key"]
        )
        return await self.client.__aenter__()
    
    async def close(self):
        """关闭客户端"""
        if self.client:
            await self.client.__aexit__(None, None, None)
    
    async def get_user_info(self) -> Dict[str, Any]:
        """获取用户信息"""
        if not self.client:
            await self.initialize()
        
        result = await self.client.call_tool("whoami_v1")
        if result:
            return {"source": "api", "data": result}
        else:
            # 模拟数据
            return {
                "source": "simulated",
                "data": {
                    "id": "user_123",
                    "name": "投资用户",
                    "email": "investor@example.com",
                    "joined_date": "2024-01-01",
                    "investment_style": "成长型"
                }
            }
    
    async def list_positions(self, status: str = "POSITION", limit: int = 10) -> Dict[str, Any]:
        """列出持仓"""
        if not self.client:
            await self.initialize()
        
        result = await self.client.call_tool("positions_list_v1", {
            "status": status,
            "limit": limit
        })
        if result:
            return {"source": "api", "data": result}
        else:
            # 模拟数据
            positions = [
                {
                    "id": "pos_001",
                    "symbol": "BTC",
                    "name": "Bitcoin",
                    "asset_type": "crypto",
                    "quantity": 0.5,
                    "current_price": 45000.00,
                    "current_value": 22500.00,
                    "cost_basis": 20000.00,
                    "unrealized_gain": 2500.00,
                    "status": "POSITION"
                },
                {
                    "id": "pos_002",
                    "symbol": "ETH",
                    "name": "Ethereum",
                    "asset_type": "crypto",
                    "quantity": 2.5,
                    "current_price": 2500.00,
                    "current_value": 6250.00,
                    "cost_basis": 5000.00,
                    "unrealized_gain": 1250.00,
                    "status": "POSITION"
                }
            ]
            return {
                "source": "simulated",
                "data": {
                    "positions": positions,
                    "count": len(positions),
                    "total_value": sum(p["current_value"] for p in positions)
                }
            }
    
    async def get_methodology(self) -> Dict[str, Any]:
        """获取投资方法论"""
        if not self.client:
            await self.initialize()
        
        result = await self.client.call_tool("methodology_get_v1")
        if result:
            return {"source": "api", "data": result}
        else:
            # 模拟数据
            return {
                "source": "simulated",
                "data": {
                    "strategy": "价值投资 + 趋势跟踪",
                    "risk_tolerance": "中等",
                    "time_horizon": "长期",
                    "diversification": "跨资产类别分散",
                    "rebalancing_frequency": "季度"
                }
            }
    
    async def get_stats(self) -> Dict[str, Any]:
        """获取统计数据"""
        if not self.client:
            await self.initialize()
        
        result = await self.client.call_tool("stats_quick_v1")
        if result:
            return {"source": "api", "data": result}
        else:
            # 模拟数据
            return {
                "source": "simulated",
                "data": {
                    "total_portfolio_value": 125000.50,
                    "total_return": 25000.50,
                    "return_percentage": 25.0,
                    "active_positions": 3,
                    "closed_positions": 12,
                    "win_rate": 75.0
                }
            }
    
    async def list_available_tools(self) -> Dict[str, Any]:
        """列出可用工具"""
        if not self.client:
            await self.initialize()
        
        tools = await self.client.list_tools()
        if tools:
            return {"source": "api", "data": {"tools": tools}}
        else:
            # 模拟数据
            return {
                "source": "simulated",
                "data": {
                    "tools": [
                        {
                            "name": "whoami_v1",
                            "description": "获取用户身份信息",
                            "inputSchema": {"type": "object", "properties": {}}
                        },
                        {
                            "name": "methodology_get_v1",
                            "description": "获取投资方法论",
                            "inputSchema": {"type": "object", "properties": {}}
                        },
                        {
                            "name": "stats_quick_v1",
                            "description": "快速统计数据",
                            "inputSchema": {"type": "object", "properties": {}}
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
                                }
                            }
                        }
                    ]
                }
            }

# 命令行接口
async def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="InvestmentTracker MCP Skill")
    parser.add_argument("command", nargs="?", help="命令: user, positions, methodology, stats, tools, all")
    parser.add_argument("--status", default="POSITION", help="持仓状态 (POSITION/CLOSE)")
    parser.add_argument("--limit", type=int, default=10, help="限制数量")
    parser.add_argument("--config", default="mcp_config.json", help="配置文件路径")
    
    args = parser.parse_args()
    
    # 创建技能实例
    skill = InvestmentTrackerSkill(args.config)
    
    try:
        await skill.initialize()
        
        # 格式化函数
        def format_user_info(data):
            output = []
            output.append("👤 用户信息")
            output.append("=" * 60)
            output.append(f"ID: {data['data'].get('id', 'N/A')}")
            output.append(f"名称: {data['data'].get('name', 'N/A')}")
            output.append(f"邮箱: {data['data'].get('email', 'N/A')}")
            output.append(f"加入日期: {data['data'].get('joined_date', 'N/A')}")
            output.append(f"投资风格: {data['data'].get('investment_style', 'N/A')}")
            output.append(f"📡 数据源: {'API' if data['source'] == 'api' else '模拟数据'}")
            return "\n".join(output)
        
        def format_positions(data):
            output = []
            output.append("📊 持仓列表")
            output.append("=" * 60)
            
            positions = data['data'].get('positions', [])
            if positions:
                output.append(f"持仓数量: {len(positions)}")
                output.append(f"总价值: ${data['data'].get('total_value', 0):,.2f}")
                output.append("")
                output.append("详细持仓:")
                output.append("-" * 60)
                
                for pos in positions:
                    gain_percentage = (pos["unrealized_gain"] / pos["cost_basis"] * 100) if pos["cost_basis"] else 0
                    output.append(
                        f"{pos['symbol']:<6} {pos['name'][:15]:<15} "
                        f"数量: {pos['quantity']:>8.4f} "
                        f"现价: ${pos['current_price']:>8.2f} "
                        f"价值: ${pos['current_value']:>8.2f} "
                        f"收益: {gain_percentage:>5.1f}%"
                    )
            else:
                output.append("暂无持仓")
            
            output.append(f"📡 数据源: {'API' if data['source'] == 'api' else '模拟数据'}")
            return "\n".join(output)
        
        # 执行命令
        if args.command == "user":
            user_info = await skill.get_user_info()
            print(format_user_info(user_info))
        
        elif args.command == "positions":
            positions = await skill.list_positions(status=args.status, limit=args.limit)
            print(format_positions(positions))
        
        elif args.command == "methodology":
            methodology = await skill.get_methodology()
            print(format_user_info(methodology))
        
        elif args.command == "stats":
            stats = await skill.get_stats()
            print(format_user_info(stats))
        
        elif args.command == "tools":
            tools = await skill.list_available_tools()
            data = tools['data']
            output = []
            output.append("🔧 可用工具")
            output.append("=" * 60)
            
            for tool in data.get('tools', []):
                output.append(f"\n{tool.get('name', 'N/A')}:")
                output.append(f"  描述: {tool.get('description', '无描述')}")
            
            output.append(f"\n📡 数据源: {'API' if tools['source'] == 'api' else '模拟数据'}")
            print("\n".join(output))
        
        elif args.command == "all" or not args.command:
            # 显示所有信息
            print("=" * 60)
            print("InvestmentTracker MCP Skill")
            print("=" * 60)
            
            user_info = await skill.get_user_info()
            print(format_user_info(user_info))
            
            print("\n" + "=" * 60)
            positions = await skill.list_positions()
            print(format_positions(positions))
            
            print("\n" + "=" * 60)
            methodology = await skill.get_methodology()
            print(format_user_info(methodology))
            
            print("\n" + "=" * 60)
            stats = await skill.get_stats()
            print(format_user_info(stats))
            
            print("\n" + "=" * 60)
            tools = await skill.list_available_tools()
            data = tools['data']
            output = []
            output.append("🔧 可用工具")
            output.append("=" * 60)
            
            for tool in data.get('tools', []):
                output.append(f"\n{tool.get('name', 'N/A')}:")
                output.append(f"  描述: {tool.get('description', '无描述')}")
            
            output.append(f"\n📡 数据源: {'API' if tools['source'] == 'api' else '模拟数据'}")
            print("\n".join(output))
        
        else:
            print(f"错误: 未知命令 '{args.command}'")
            print("可用命令: user, positions, methodology, stats, tools, all")
    
    finally:
        await skill.close()

if __name__ == "__main__":
    # 运行异步主函数
    asyncio.run(main())