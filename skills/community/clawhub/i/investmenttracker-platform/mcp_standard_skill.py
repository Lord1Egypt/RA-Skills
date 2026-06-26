#!/usr/bin/env python3
"""
InvestmentTracker MCP 标准技能（无外部依赖版）
使用标准MCP配置格式，无需安装额外依赖
"""

import json
import sys
import subprocess
import time
from typing import Dict, Any, List, Optional

class InvestmentTrackerMCPSkill:
    """InvestmentTracker MCP标准技能"""
    
    def __init__(self, config_path: str = "mcp_config.json"):
        self.config_path = config_path
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """加载MCP配置"""
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
    
    def _send_mcp_request(self, method: str, params: Dict = None) -> Optional[Dict[str, Any]]:
        """发送MCP请求（使用curl）"""
        server_config = self.config["mcpServers"]["investmenttracker"]
        url = server_config["url"]
        headers = server_config["headers"]
        
        request_id = int(time.time() * 1000)
        request = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
            "id": request_id
        }
        
        # 构建curl命令
        cmd = ['curl', '-s', '-X', 'POST', url]
        
        # 添加headers
        for key, value in headers.items():
            cmd.extend(['-H', f'{key}: {value}'])
        
        cmd.extend(['-H', 'Content-Type: application/json'])
        cmd.extend(['-H', 'Accept: application/json'])
        
        # 添加请求数据
        request_json = json.dumps(request)
        cmd.extend(['-d', request_json])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0 and result.stdout:
                try:
                    response = json.loads(result.stdout)
                    if response.get('id') == request_id:
                        return response
                except json.JSONDecodeError:
                    print(f"JSON解析错误: {result.stdout[:100]}")
                    return None
            else:
                print(f"请求失败: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            print("请求超时")
            return None
        except Exception as e:
            print(f"请求异常: {e}")
            return None
        
        return None
    
    def get_user_info(self) -> Dict[str, Any]:
        """获取用户信息"""
        result = self._send_mcp_request("tools/call", {
            "name": "whoami_v1",
            "arguments": {}
        })
        
        if result and "result" in result:
            return {"source": "api", "data": result["result"]}
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
    
    def list_positions(self, status: str = "POSITION", limit: int = 10) -> Dict[str, Any]:
        """列出持仓"""
        result = self._send_mcp_request("tools/call", {
            "name": "positions_list_v1",
            "arguments": {
                "status": status,
                "limit": limit
            }
        })
        
        if result and "result" in result:
            return {"source": "api", "data": result["result"]}
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
                },
                {
                    "id": "pos_003",
                    "symbol": "AAPL",
                    "name": "Apple Inc.",
                    "asset_type": "stock",
                    "quantity": 10,
                    "current_price": 175.50,
                    "current_value": 1755.00,
                    "cost_basis": 1500.00,
                    "unrealized_gain": 255.00,
                    "status": "POSITION"
                }
            ]
            
            filtered_positions = [p for p in positions if p["status"] == status][:limit]
            
            return {
                "source": "simulated",
                "data": {
                    "positions": filtered_positions,
                    "count": len(filtered_positions),
                    "total_value": sum(p["current_value"] for p in filtered_positions)
                }
            }
    
    def get_methodology(self) -> Dict[str, Any]:
        """获取投资方法论"""
        result = self._send_mcp_request("tools/call", {
            "name": "methodology_get_v1",
            "arguments": {}
        })
        
        if result and "result" in result:
            return {"source": "api", "data": result["result"]}
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
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计数据"""
        result = self._send_mcp_request("tools/call", {
            "name": "stats_quick_v1",
            "arguments": {}
        })
        
        if result and "result" in result:
            return {"source": "api", "data": result["result"]}
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
    
    def list_tools(self) -> Dict[str, Any]:
        """列出可用工具"""
        result = self._send_mcp_request("tools/list", {})
        
        if result and "result" in result:
            return {"source": "api", "data": result["result"]}
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
    
    # 格式化方法
    def format_user_info(self, data: Dict[str, Any]) -> str:
        """格式化用户信息"""
        user_data = data["data"]
        source = data["source"]
        
        output = []
        output.append("👤 用户信息")
        output.append("=" * 60)
        output.append(f"ID: {user_data.get('id', 'N/A')}")
        output.append(f"名称: {user_data.get('name', 'N/A')}")
        output.append(f"邮箱: {user_data.get('email', 'N/A')}")
        output.append(f"加入日期: {user_data.get('joined_date', 'N/A')}")
        output.append(f"投资风格: {user_data.get('investment_style', 'N/A')}")
        output.append("")
        output.append(f"📡 数据源: {'API' if source == 'api' else '模拟数据'}")
        
        return "\n".join(output)
    
    def format_positions(self, data: Dict[str, Any]) -> str:
        """格式化持仓信息"""
        positions_data = data["data"]
        source = data["source"]
        
        output = []
        output.append("📊 持仓列表")
        output.append("=" * 60)
        
        positions = positions_data.get("positions", [])
        if positions:
            output.append(f"持仓数量: {len(positions)}")
            output.append(f"总价值: ${positions_data.get('total_value', 0):,.2f}")
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
        
        output.append("")
        output.append(f"📡 数据源: {'API' if source == 'api' else '模拟数据'}")
        
        return "\n".join(output)
    
    def format_methodology(self, data: Dict[str, Any]) -> str:
        """格式化投资方法论"""
        methodology_data = data["data"]
        source = data["source"]
        
        output = []
        output.append("📈 投资方法论")
        output.append("=" * 60)
        output.append(f"策略: {methodology_data.get('strategy', 'N/A')}")
        output.append(f"风险承受能力: {methodology_data.get('risk_tolerance', 'N/A')}")
        output.append(f"投资期限: {methodology_data.get('time_horizon', 'N/A')}")
        output.append(f"分散化: {methodology_data.get('diversification', 'N/A')}")
        output.append(f"再平衡频率: {methodology_data.get('rebalancing_frequency', 'N/A')}")
        output.append("")
        output.append(f"📡 数据源: {'API' if source == 'api' else '模拟数据'}")
        
        return "\n".join(output)
    
    def format_stats(self, data: Dict[str, Any]) -> str:
        """格式化统计数据"""
        stats_data = data["data"]
        source = data["source"]
        
        output = []
        output.append("📊 投资统计数据")
        output.append("=" * 60)
        output.append(f"投资组合总价值: ${stats_data.get('total_portfolio_value', 0):,.2f}")
        output.append(f"总收益: ${stats_data.get('total_return', 0):,.2f}")
        output.append(f"收益率: {stats_data.get('return_percentage', 0):.1f}%")
        output.append(f"活跃持仓: {stats_data.get('active_positions', 0)}")
        output.append(f"已平仓持仓: {stats_data.get('closed_positions', 0)}")
        output.append(f"胜率: {stats_data.get('win_rate', 0):.1f}%")
        output.append("")
        output.append(f"📡 数据源: {'API' if source == 'api' else '模拟数据'}")
        
        return "\n".join(output)
    
    def format_tools(self, data: Dict[str, Any]) -> str:
        """格式化工具列表"""
        tools_data = data["data"]
        source = data["source"]
        
        output = []
        output.append("🔧 可用工具")
        output.append("=" * 60)
        
        tools = tools_data.get("tools", [])
        if tools:
            for tool in tools:
                output.append(f"\n{tool.get('name', 'N/A')}:")
                output.append(f"  描述: {tool.get('description', '无描述')}")
        else:
            output.append("暂无可用工具")
        
        output.append("")
        output.append(f"📡 数据源: {'API' if source == 'api' else '模拟数据'}")
        
        return "\n".join(output)

# 命令行接口
def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="InvestmentTracker MCP标准技能")
    parser.add_argument("command", nargs="?", help="命令: user, positions, methodology, stats, tools, all")
    parser.add_argument("--status", default="POSITION", help="持仓状态 (POSITION/CLOSE)")
    parser.add_argument("--limit", type=int, default=10, help="限制数量")
    parser.add_argument("--config", default="mcp_config.json", help="配置文件路径")
    
    args = parser.parse_args()
    
    # 创建技能实例
    skill = InvestmentTrackerMCPSkill(args.config)
    
    # 执行命令
    if args.command == "user":
        user_info = skill.get_user_info()
        print(skill.format_user_info(user_info))
    
    elif args.command == "positions":
        positions = skill.list_positions(status=args.status, limit=args.limit)
        print(skill.format_positions(positions))
    
    elif args.command == "methodology":
        methodology = skill.get_methodology()
        print(skill.format_methodology(methodology))
    
    elif args.command == "stats":
        stats = skill.get_stats()
        print(skill.format_stats(stats))
    
    elif args.command == "tools":
        tools = skill.list_tools()
        print(skill.format_tools(tools))
    
    elif args.command == "all" or not args.command:
        # 显示所有信息
        print("=" * 60)
        print("InvestmentTracker MCP标准技能")
        print("=" * 60)
        
        user_info = skill.get_user_info()
        print(skill.format_user_info(user_info))
        
        print("\n" + "=" * 60)
        positions = skill.list_positions()
        print(skill.format_positions(positions))
        
        print("\n" + "=" * 60)
        methodology = skill.get_methodology()
        print(skill.format_methodology(methodology))
        
        print("\n" + "=" * 60)
        stats = skill.get_stats()
        print(skill.format_stats(stats))
        
        print("\n" + "=" * 60)
        tools = skill.list_tools()
        print(skill.format_tools(tools))
    
    else:
        print(f"错误: 未知命令 '{args.command}'")
        print("可用命令: user, positions, methodology, stats, tools, all")

if __name__ == "__main__":
    main()