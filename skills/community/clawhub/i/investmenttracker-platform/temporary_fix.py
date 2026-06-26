#!/usr/bin/env python3
"""
InvestmentTracker 临时修复方案
在MCP API修复期间，提供手动数据输入和模拟数据功能
"""

import json
import os
import sys
from typing import Dict, Any, List
from datetime import datetime

class TemporaryInvestmentTracker:
    """临时投资追踪器"""
    
    def __init__(self, data_file: str = "user_investment_data.json"):
        self.data_file = data_file
        self.data = self._load_data()
        
    def _load_data(self) -> Dict[str, Any]:
        """加载用户数据"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # 默认模拟数据
        return {
            "user_info": {
                "id": "user_123",
                "name": "投资用户",
                "email": "investor@example.com",
                "joined_date": "2024-01-01",
                "investment_style": "成长型",
                "note": "这是模拟数据，请使用 update_user_info 更新真实数据"
            },
            "positions": [
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
                    "status": "POSITION",
                    "note": "模拟数据 - 示例持仓"
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
                    "status": "POSITION",
                    "note": "模拟数据 - 示例持仓"
                }
            ],
            "methodology": {
                "strategy": "价值投资 + 趋势跟踪",
                "risk_tolerance": "中等",
                "time_horizon": "长期",
                "diversification": "跨资产类别分散",
                "rebalancing_frequency": "季度",
                "note": "模拟数据 - 示例投资策略"
            },
            "stats": {
                "total_portfolio_value": 125000.50,
                "total_return": 25000.50,
                "return_percentage": 25.0,
                "active_positions": 2,
                "closed_positions": 5,
                "win_rate": 75.0,
                "note": "模拟数据 - 示例统计数据"
            },
            "last_updated": datetime.now().isoformat(),
            "data_source": "simulated"
        }
    
    def _save_data(self):
        """保存数据"""
        self.data["last_updated"] = datetime.now().isoformat()
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def update_user_info(self, name: str = None, email: str = None, 
                        investment_style: str = None, **kwargs):
        """更新用户信息"""
        if name:
            self.data["user_info"]["name"] = name
        if email:
            self.data["user_info"]["email"] = email
        if investment_style:
            self.data["user_info"]["investment_style"] = investment_style
        
        for key, value in kwargs.items():
            self.data["user_info"][key] = value
        
        self.data["user_info"]["note"] = "手动更新数据"
        self.data["data_source"] = "manual"
        self._save_data()
        return {"status": "success", "updated": self.data["user_info"]}
    
    def add_position(self, symbol: str, name: str, quantity: float, 
                    current_price: float, cost_basis: float = None, **kwargs):
        """添加持仓"""
        position_id = f"pos_{len(self.data['positions']) + 1:03d}"
        
        if cost_basis is None:
            cost_basis = current_price * quantity * 0.9  # 假设成本比现价低10%
        
        current_value = quantity * current_price
        unrealized_gain = current_value - cost_basis
        
        position = {
            "id": position_id,
            "symbol": symbol,
            "name": name,
            "asset_type": kwargs.get("asset_type", "unknown"),
            "quantity": quantity,
            "current_price": current_price,
            "current_value": current_value,
            "cost_basis": cost_basis,
            "unrealized_gain": unrealized_gain,
            "status": "POSITION",
            "note": "手动添加持仓",
            "added_date": datetime.now().isoformat()
        }
        
        # 添加额外参数
        for key, value in kwargs.items():
            if key not in position:
                position[key] = value
        
        self.data["positions"].append(position)
        self.data["data_source"] = "manual"
        self._save_data()
        
        return {
            "status": "success", 
            "position_id": position_id,
            "position": position
        }
    
    def update_position(self, position_id: str, **kwargs):
        """更新持仓"""
        for position in self.data["positions"]:
            if position["id"] == position_id:
                for key, value in kwargs.items():
                    if key in ["quantity", "current_price", "cost_basis"]:
                        position[key] = value
                
                # 重新计算
                if "quantity" in kwargs or "current_price" in kwargs:
                    position["current_value"] = position["quantity"] * position["current_price"]
                
                if "cost_basis" in kwargs or "current_value" in kwargs:
                    position["unrealized_gain"] = position["current_value"] - position["cost_basis"]
                
                position["note"] = f"手动更新于 {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                self.data["data_source"] = "manual"
                self._save_data()
                
                return {"status": "success", "updated_position": position}
        
        return {"status": "error", "message": f"未找到持仓 {position_id}"}
    
    def delete_position(self, position_id: str):
        """删除持仓"""
        original_count = len(self.data["positions"])
        self.data["positions"] = [p for p in self.data["positions"] if p["id"] != position_id]
        
        if len(self.data["positions"]) < original_count:
            self.data["data_source"] = "manual"
            self._save_data()
            return {"status": "success", "message": f"已删除持仓 {position_id}"}
        else:
            return {"status": "error", "message": f"未找到持仓 {position_id}"}
    
    def update_methodology(self, **kwargs):
        """更新投资方法论"""
        for key, value in kwargs.items():
            if key in self.data["methodology"]:
                self.data["methodology"][key] = value
        
        self.data["methodology"]["note"] = "手动更新策略"
        self.data["data_source"] = "manual"
        self._save_data()
        
        return {"status": "success", "updated_methodology": self.data["methodology"]}
    
    def update_stats(self, **kwargs):
        """更新统计数据"""
        for key, value in kwargs.items():
            if key in self.data["stats"]:
                self.data["stats"][key] = value
        
        self.data["stats"]["note"] = "手动更新统计"
        self.data["data_source"] = "manual"
        self._save_data()
        
        return {"status": "success", "updated_stats": self.data["stats"]}
    
    def get_user_info(self) -> Dict[str, Any]:
        """获取用户信息"""
        return {
            "source": self.data.get("data_source", "simulated"),
            "data": self.data["user_info"],
            "last_updated": self.data.get("last_updated", "")
        }
    
    def list_positions(self, status: str = "POSITION", limit: int = 10) -> Dict[str, Any]:
        """列出持仓"""
        positions = [p for p in self.data["positions"] if p["status"] == status][:limit]
        
        total_value = sum(p["current_value"] for p in positions)
        
        return {
            "source": self.data.get("data_source", "simulated"),
            "data": {
                "positions": positions,
                "count": len(positions),
                "total_value": total_value
            },
            "last_updated": self.data.get("last_updated", "")
        }
    
    def get_methodology(self) -> Dict[str, Any]:
        """获取投资方法论"""
        return {
            "source": self.data.get("data_source", "simulated"),
            "data": self.data["methodology"],
            "last_updated": self.data.get("last_updated", "")
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计数据"""
        return {
            "source": self.data.get("data_source", "simulated"),
            "data": self.data["stats"],
            "last_updated": self.data.get("last_updated", "")
        }
    
    def get_data_summary(self) -> Dict[str, Any]:
        """获取数据摘要"""
        return {
            "data_source": self.data.get("data_source", "simulated"),
            "last_updated": self.data.get("last_updated", ""),
            "position_count": len(self.data["positions"]),
            "user_name": self.data["user_info"].get("name", "N/A"),
            "total_positions_value": sum(p["current_value"] for p in self.data["positions"]),
            "notes": {
                "user": self.data["user_info"].get("note", ""),
                "methodology": self.data["methodology"].get("note", ""),
                "stats": self.data["stats"].get("note", "")
            }
        }
    
    def format_positions(self) -> str:
        """格式化持仓输出"""
        positions_data = self.list_positions()
        data = positions_data["data"]
        source = positions_data["source"]
        
        output = []
        output.append("📊 持仓列表")
        output.append("=" * 60)
        output.append(f"数据源: {'手动数据' if source == 'manual' else '模拟数据'}")
        output.append(f"更新时间: {positions_data.get('last_updated', '未知')[:19]}")
        output.append("")
        
        positions = data.get("positions", [])
        if positions:
            output.append(f"持仓数量: {len(positions)}")
            output.append(f"总价值: ${data.get('total_value', 0):,.2f}")
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
                if pos.get("note"):
                    output.append(f"   📝 {pos['note']}")
        else:
            output.append("暂无持仓记录")
            output.append("使用 add_position 命令添加持仓")
        
        return "\n".join(output)
    
    def format_summary(self) -> str:
        """格式化数据摘要"""
        summary = self.get_data_summary()
        
        output = []
        output.append("📋 投资数据摘要")
        output.append("=" * 60)
        output.append(f"数据源: {'手动数据' if summary['data_source'] == 'manual' else '模拟数据'}")
        output.append(f"更新时间: {summary['last_updated'][:19]}")
        output.append(f"用户: {summary['user_name']}")
        output.append(f"持仓数量: {summary['position_count']}")
        output.append(f"持仓总价值: ${summary['total_positions_value']:,.2f}")
        output.append("")
        
        # 显示备注
        notes = summary['notes']
        if any(notes.values()):
            output.append("📝 备注:")
            for key, note in notes.items():
                if note:
                    output.append(f"  {key}: {note}")
        
        output.append("")
        output.append("💡 使用以下命令管理数据:")
        output.append("  update_user_info - 更新用户信息")
        output.append("  add_position - 添加持仓")
        output.append("  update_position - 更新持仓")
        output.append("  delete_position - 删除持仓")
        
        return "\n".join(output)

# 命令行接口
def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="InvestmentTracker临时数据管理")
    parser.add_argument("command", nargs="?", help="命令: view, summary, update, add, delete, help")
    
    # 子命令参数
    parser.add_argument("--name", help="用户名称")
    parser.add_argument("--email", help="用户邮箱")
    parser.add_argument("--style", help="投资风格")
    
    parser.add_argument("--symbol", help="资产代码")
    parser.add_argument("--asset-name", help="资产名称")
    parser.add_argument("--quantity", type=float, help="数量")
    parser.add_argument("--price", type=float, help="当前价格")
    parser.add_argument("--cost", type=float, help="成本基础")
    
    parser.add_argument("--position-id", help="持仓ID")
    
    parser.add_argument("--strategy", help="投资策略")
    parser.add_argument("--risk", help="风险承受能力")
    
    parser.add_argument("--file", default="user_investment_data.json", help="数据文件路径")
    
    args = parser.parse_args()
    
    tracker = TemporaryInvestmentTracker(args.file)
    
    if args.command == "view" or not args.command:
        # 查看持仓
        print(tracker.format_positions())
        
    elif args.command == "summary":
        # 查看摘要
        print(tracker.format_summary())
        
    elif args.command == "update":
        # 更新用户信息
        if args.name or args.email or args.style:
            result = tracker.update_user_info(
                name=args.name,
                email=args.email,
                investment_style=args.style
            )
            print(f"✅ 用户信息已更新: {json.dumps(result, ensure_ascii=False)}")
        else:
            print("❌ 请提供更新参数 (--name, --email, --style)")
            
    elif args.command == "add":
        # 添加持仓
        if args.symbol and args.asset_name and args.quantity and args.price:
            result = tracker.add_position(
                symbol=args.symbol,
                name=args.asset_name,
                quantity=args.quantity,
                current_price=args.price,
                cost_basis=args.cost
            )
            print(f"✅ 持仓已添加: {json.dumps(result, ensure_ascii=False)}")
        else:
            print("❌ 请提供持仓参数 (--symbol, --asset-name, --quantity, --price)")
            
    elif args.command == "delete":
        # 删除持仓
        if args.position_id:
            result = tracker.delete_position(args.position_id)
            print(f"✅ {result['message']}")
        else:
            print("❌ 请提供持仓ID (--position-id)")
            
    elif args.command == "help":
        print("📖 InvestmentTracker临时数据管理命令:")
        print("")
        print("查看数据:")
        print("  python3 temporary_fix.py view           # 查看持仓")
        print("  python3 temporary_fix.py summary        # 查看数据摘要")
        print("")
        print("管理数据:")
        print("  python3 temporary_fix.py update \\")
        print("    --name '你的名字' \\")
        print("    --email '邮箱' \\")
        print("    --style '投资风格'")
        print("")
        print("  python3 temporary_fix.py add \\")
        print("    --symbol BTC \\")
        print("    --asset-name 'Bitcoin' \\")
        print("    --quantity 0.5 \\")
        print("    --price 45000")
        print("")
        print("  python3 temporary_fix.py delete --position-id pos_001")
        print("")
        print("数据文件: user_investment_data.json")
        
    else:
        print(f"❌ 未知命令: {args.command}")
        print("使用 'help' 查看可用命令")

if __name__ == "__main__":
    main()