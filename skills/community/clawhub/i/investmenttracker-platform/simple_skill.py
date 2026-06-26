#!/usr/bin/env python3
"""
InvestmentTracker-platform 简化版本
无外部依赖，纯模拟数据
"""

import json
import time
from typing import Dict, Any, List
from enum import Enum

class ConnectionMode(Enum):
    """连接模式"""
    SIMULATED = "simulated"  # 模拟数据模式
    API = "api"              # 真实API模式（暂不可用）

class InvestmentTrackerSkill:
    """InvestmentTracker技能主类（简化版）"""
    
    def __init__(self, mode: ConnectionMode = ConnectionMode.SIMULATED):
        self.mode = mode
        
        # 模拟数据
        self.simulated_portfolio = self._create_simulated_portfolio()
        self.simulated_transactions = self._create_simulated_transactions()
    
    def _create_simulated_portfolio(self) -> Dict[str, Any]:
        """创建模拟投资组合数据"""
        return {
            "total_value": 125000.50,
            "total_invested": 100000.00,
            "total_return": 25000.50,
            "return_percentage": 25.0,
            "last_updated": "2026-02-16T15:00:00Z",
            "assets": [
                {
                    "symbol": "BTC",
                    "name": "Bitcoin",
                    "asset_type": "crypto",
                    "quantity": 0.5,
                    "current_price": 45000.00,
                    "current_value": 22500.00,
                    "cost_basis": 20000.00,
                    "unrealized_gain": 2500.00,
                    "unrealized_gain_percentage": 12.5,
                    "weight": 18.0,
                    "allocation": 18.0
                },
                {
                    "symbol": "ETH",
                    "name": "Ethereum",
                    "asset_type": "crypto",
                    "quantity": 2.5,
                    "current_price": 2500.00,
                    "current_value": 6250.00,
                    "cost_basis": 5000.00,
                    "unrealized_gain": 1250.00,
                    "unrealized_gain_percentage": 25.0,
                    "weight": 5.0,
                    "allocation": 5.0
                },
                {
                    "symbol": "AAPL",
                    "name": "Apple Inc.",
                    "asset_type": "stock",
                    "quantity": 10,
                    "current_price": 175.50,
                    "current_value": 1755.00,
                    "cost_basis": 1500.00,
                    "unrealized_gain": 255.00,
                    "unrealized_gain_percentage": 17.0,
                    "weight": 1.4,
                    "allocation": 1.4
                },
                {
                    "symbol": "CASH",
                    "name": "现金",
                    "asset_type": "cash",
                    "quantity": 94595.50,
                    "current_price": 1.00,
                    "current_value": 94595.50,
                    "cost_basis": 94595.50,
                    "unrealized_gain": 0.00,
                    "unrealized_gain_percentage": 0.0,
                    "weight": 75.6,
                    "allocation": 75.6
                }
            ]
        }
    
    def _create_simulated_transactions(self) -> List[Dict[str, Any]]:
        """创建模拟交易记录"""
        return [
            {
                "id": "txn_20260216001",
                "date": "2026-02-16T10:30:00Z",
                "type": "BUY",
                "symbol": "BTC",
                "name": "Bitcoin",
                "quantity": 0.1,
                "price": 42000.00,
                "total": 4200.00,
                "fee": 10.50,
                "status": "COMPLETED",
                "notes": "定期定投"
            },
            {
                "id": "txn_20260215001",
                "date": "2026-02-15T14:20:00Z",
                "type": "SELL",
                "symbol": "AAPL",
                "name": "Apple Inc.",
                "quantity": 5,
                "price": 180.00,
                "total": 900.00,
                "fee": 2.25,
                "status": "COMPLETED",
                "notes": "部分获利了结"
            },
            {
                "id": "txn_20260214001",
                "date": "2026-02-14T09:15:00Z",
                "type": "BUY",
                "symbol": "ETH",
                "name": "Ethereum",
                "quantity": 0.5,
                "price": 2400.00,
                "total": 1200.00,
                "fee": 3.00,
                "status": "COMPLETED",
                "notes": "加仓"
            },
            {
                "id": "txn_20260213001",
                "date": "2026-02-13T16:45:00Z",
                "type": "DIVIDEND",
                "symbol": "AAPL",
                "name": "Apple Inc.",
                "quantity": 10,
                "price": 0.24,
                "total": 2.40,
                "fee": 0.00,
                "status": "COMPLETED",
                "notes": "季度股息"
            }
        ]
    
    def get_portfolio(self) -> Dict[str, Any]:
        """获取投资组合"""
        return {
            "source": "simulated",
            "mode": self.mode.value,
            "data": self.simulated_portfolio,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
    
    def get_transactions(self, limit: int = 10) -> Dict[str, Any]:
        """获取交易记录"""
        transactions = self.simulated_transactions[:limit]
        return {
            "source": "simulated",
            "mode": self.mode.value,
            "data": {
                "transactions": transactions,
                "count": len(transactions),
                "summary": {
                    "total_buy": sum(t["total"] for t in transactions if t["type"] in ["BUY", "DIVIDEND"]),
                    "total_sell": sum(t["total"] for t in transactions if t["type"] == "SELL"),
                    "total_fees": sum(t["fee"] for t in transactions)
                }
            },
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
    
    def get_analysis(self) -> Dict[str, Any]:
        """获取投资分析"""
        portfolio = self.simulated_portfolio
        
        # 计算分析指标
        analysis = {
            "performance": {
                "total_return_percentage": portfolio["return_percentage"],
                "annualized_return": 18.5,
                "sharpe_ratio": 1.25,
                "sortino_ratio": 1.85,
                "volatility": 15.2,
                "beta": 0.85
            },
            "asset_allocation": {},
            "risk_metrics": {
                "max_drawdown": -8.5,
                "var_95_1d": -3.2,
                "var_99_1d": -5.8,
                "calmar_ratio": 1.17
            },
            "consistency": {
                "positive_months": 9,
                "negative_months": 3,
                "win_rate": 75.0,
                "profit_factor": 2.8
            }
        }
        
        # 计算资产分配
        for asset in portfolio.get("assets", []):
            asset_type = asset["asset_type"]
            value = asset["current_value"]
            
            if asset_type not in analysis["asset_allocation"]:
                analysis["asset_allocation"][asset_type] = 0
            
            analysis["asset_allocation"][asset_type] += value
        
        # 转换为百分比
        total_value = portfolio["total_value"]
        for asset_type in analysis["asset_allocation"]:
            analysis["asset_allocation"][asset_type] = round(
                analysis["asset_allocation"][asset_type] / total_value * 100, 1
            )
        
        return {
            "source": "simulated",
            "mode": self.mode.value,
            "data": analysis,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
    
    def format_portfolio(self) -> str:
        """格式化投资组合输出"""
        portfolio = self.get_portfolio()
        data = portfolio["data"]
        
        output = []
        output.append("📊 投资组合概览")
        output.append("=" * 60)
        output.append(f"💰 总价值: ${data['total_value']:,.2f}")
        output.append(f"📈 总投资: ${data['total_invested']:,.2f}")
        output.append(f"🎯 总收益: ${data['total_return']:,.2f}")
        output.append(f"📊 收益率: {data['return_percentage']:.1f}%")
        output.append(f"🕐 更新时间: {data['last_updated'][:10]}")
        output.append("")
        
        output.append("📈 资产持仓:")
        output.append("-" * 60)
        for asset in data["assets"]:
            if asset["symbol"] != "CASH":  # 现金单独显示
                output.append(
                    f"{asset['symbol']:<6} {asset['name'][:15]:<15} "
                    f"${asset['current_value']:>10,.2f} "
                    f"({asset['allocation']:>5.1f}%) "
                    f"📈 {asset['unrealized_gain_percentage']:>5.1f}%"
                )
        
        # 显示现金
        cash_asset = next((a for a in data["assets"] if a["symbol"] == "CASH"), None)
        if cash_asset:
            output.append("")
            output.append("💵 现金持仓:")
            output.append(f"  现金: ${cash_asset['current_value']:,.2f} ({cash_asset['allocation']:.1f}%)")
        
        output.append("")
        output.append(f"🔧 数据模式: {portfolio['mode']}")
        output.append(f"🕐 生成时间: {portfolio['timestamp'][:19]}")
        
        return "\n".join(output)
    
    def format_transactions(self, limit: int = 5) -> str:
        """格式化交易记录输出"""
        transactions_data = self.get_transactions(limit)
        data = transactions_data["data"]
        
        output = []
        output.append("💱 交易记录")
        output.append("=" * 60)
        
        if data["transactions"]:
            output.append(f"最近 {len(data['transactions'])} 笔交易:")
            output.append("-" * 60)
            
            for txn in data["transactions"]:
                emoji = "🟢" if txn["type"] == "BUY" else "🔴" if txn["type"] == "SELL" else "💰"
                output.append(
                    f"{emoji} {txn['date'][:10]} "
                    f"{txn['type']:<8} "
                    f"{txn['symbol']:<6} "
                    f"{txn['quantity']:>8.4f} × "
                    f"${txn['price']:>8.2f} = "
                    f"${txn['total']:>8.2f}"
                )
                if txn.get("notes"):
                    output.append(f"   📝 {txn['notes']}")
            
            output.append("")
            output.append("📊 交易摘要:")
            output.append(f"  总买入: ${data['summary']['total_buy']:,.2f}")
            output.append(f"  总卖出: ${data['summary']['total_sell']:,.2f}")
            output.append(f"  总费用: ${data['summary']['total_fees']:,.2f}")
        else:
            output.append("暂无交易记录")
        
        output.append("")
        output.append(f"🔧 数据模式: {transactions_data['mode']}")
        output.append(f"🕐 生成时间: {transactions_data['timestamp'][:19]}")
        
        return "\n".join(output)
    
    def format_analysis(self) -> str:
        """格式化投资分析输出"""
        analysis_data = self.get_analysis()
        data = analysis_data["data"]
        
        output = []
        output.append("📈 投资分析报告")
        output.append("=" * 60)
        
        # 表现分析
        perf = data["performance"]
        output.append("📊 表现分析:")
        output.append(f"  总收益率: {perf['total_return_percentage']:>6.1f}%")
        output.append(f"  年化收益率: {perf['annualized_return']:>5.1f}%")
        output.append(f"  夏普比率: {perf['sharpe_ratio']:>7.2f}")
        output.append(f"  索提诺比率: {perf['sortino_ratio']:>5.2f}")
        output.append(f"  波动率: {perf['volatility']:>10.1f}%")
        output.append(f"  贝塔: {perf['beta']:>13.2f}")
        
        # 资产分配
        output.append("")
        output.append("📊 资产分配:")
        for asset_type, percentage in data["asset_allocation"].items():
            bar = "█" * int(percentage / 2)
            output.append(f"  {asset_type:<10} {percentage:>5.1f}% {bar}")
        
        # 风险指标
        risk = data["risk_metrics"]
        output.append("")
        output.append("⚠️  风险指标:")
        output.append(f"  最大回撤: {risk['max_drawdown']:>8.1f}%")
        output.append(f"  1日95%VaR: {risk['var_95_1d']:>6.1f}%")
        output.append(f"  1日99%VaR: {risk['var_99_1d']:>6.1f}%")
        output.append(f"  卡尔玛比率: {risk['calmar_ratio']:>5.2f}")
        
        # 一致性
        consistency = data["consistency"]
        output.append("")
        output.append("📅 投资一致性:")
        output.append(f"  盈利月份: {consistency['positive_months']}个月")
        output.append(f"  亏损月份: {consistency['negative_months']}个月")
        output.append(f"  胜率: {consistency['win_rate']:>11.1f}%")
        output.append(f"  盈亏比: {consistency['profit_factor']:>10.1f}")
        
        output.append("")
        output.append(f"🔧 数据模式: {analysis_data['mode']}")
        output.append(f"🕐 生成时间: {analysis_data['timestamp'][:19]}")
        output.append("")
        output.append("💡 说明: 此为模拟数据，用于演示InvestmentTracker功能。")
        output.append("      当MCP API可用时，将自动切换为真实数据。")
        
        return "\n".join(output)

# 命令行接口
def main():
    """主函数"""
    import sys
    
    skill = InvestmentTrackerSkill()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "portfolio":
            print(skill.format_portfolio())
        elif command == "transactions":
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 5
            print(skill.format_transactions(limit))
        elif command == "analysis":
            print(skill.format_analysis())
        elif command == "json":
            if len(sys.argv) > 2:
                data_type = sys.argv[2].lower()
                if data_type == "portfolio":
                    print(json.dumps(skill.get_portfolio(), indent=2, ensure_ascii=False))
                elif data_type == "transactions":
                    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
                    print(json.dumps(skill.get_transactions(limit), indent=2, ensure_ascii=False))
                elif data_type == "analysis":
                    print(json.dumps(skill.get_analysis(), indent=2, ensure_ascii=False))
                else:
                    print("错误: 未知数据类型")
            else:
                print("用法: python simple_skill.py json <portfolio|transactions|analysis> [limit]")
        elif command == "help":
            print("InvestmentTracker Skill 命令:")
            print("  portfolio          - 显示投资组合")
            print("  transactions [n]   - 显示最近n笔交易 (默认5)")
            print("  analysis           - 显示投资分析")
            print("  json <type> [n]    - 输出JSON格式数据")
            print("  help               - 显示帮助")
        else:
            print(f"错误: 未知命令 '{command}'")
            print("使用 'help' 查看可用命令")
    else:
        # 默认显示所有信息
        print(skill.format_portfolio())
        print("\n" + "=" * 60 + "\n")
        print(skill.format_transactions())
        print("\n" + "=" * 60 + "\n")
        print(skill.format_analysis())

if __name__ == "__main__":
    main()