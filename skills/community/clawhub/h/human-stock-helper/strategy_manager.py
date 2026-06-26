#!/usr/bin/env python3
"""
Stock Strategy Manager - 策略管理与执行分析系统
核心功能：
1. 保存/更新股票交易策略
2. 记录交易执行动作
3. 对比实际执行与策略建议的差异
4. 计算交易纪律评分
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any

# 配置文件路径
MEMORY_DIR = Path("/Users/maxhou/Desktop/openclawmax/memory")
STRATEGIES_FILE = MEMORY_DIR / "stock-strategies.json"
EXECUTIONS_FILE = MEMORY_DIR / "stock-executions.json"
POSITIONS_FILE = MEMORY_DIR / "stock-positions.json"


def load_json(filepath: Path) -> dict:
    """加载 JSON 文件"""
    if not filepath.exists():
        return {"version": "1.0", "strategies": []} if "strategies" in filepath.name else {"version": "1.0", "executions": []}
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(filepath: Path, data: dict):
    """保存 JSON 文件"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_strategy(code: str) -> Optional[dict]:
    """获取指定股票的策略"""
    data = load_json(STRATEGIES_FILE)
    return next((s for s in data.get("strategies", []) if s["code"] == code and s["status"] == "active"), None)


def get_position(code: str) -> Optional[dict]:
    """获取指定股票的持仓"""
    data = load_json(POSITIONS_FILE)
    return next((p for p in data.get("positions", []) if p["code"] == code and p["status"] == "holding"), None)


def calculate_discipline_score() -> dict:
    """计算交易纪律评分"""
    exec_data = load_json(EXECUTIONS_FILE)
    executions = exec_data.get("executions", [])
    
    if not executions:
        return {"score": 0, "total": 0, "aligned": 0, "deviated": 0}
    
    aligned = sum(1 for e in executions if e.get("strategy_alignment", {}).get("aligned", False))
    total = len(executions)
    
    return {
        "score": round((aligned / total) * 100, 1),
        "total": total,
        "aligned": aligned,
        "deviated": total - aligned
    }


def record_execution(
    code: str,
    action: str,  # 买入/卖出/加仓/减仓/止损/止盈
    price: float,
    shares: int,
    notes: str = ""
) -> dict:
    """
    记录交易执行，并自动对比策略建议
    
    示例:
        python3 strategy_manager.py execute 600089 减仓 31.50 100 "到达第一止盈位"
    """
    strategy = get_strategy(code)
    position = get_position(code)
    
    if not strategy:
        print(f"⚠️  未找到 {code} 的交易策略，执行将记录但无法对比")
    
    if not position:
        print(f"⚠️  未找到 {code} 的持仓，执行将记录但无法对比")
    
    # 构建执行记录
    execution = {
        "id": f"exec_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "strategy_id": strategy["id"] if strategy else None,
        "code": code,
        "name": strategy["name"] if strategy else position["name"] if position else code,
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "type": classify_action_type(action),
        "execution_details": {
            "price": price,
            "shares": shares,
            "amount": round(price * shares, 2)
        },
        "strategy_alignment": analyze_alignment(strategy, position, action, price, shares) if strategy else None,
        "context": {
            "market_condition": notes,
            "setup_quality": None
        }
    }
    
    # 保存执行记录
    exec_data = load_json(EXECUTIONS_FILE)
    if "executions" not in exec_data:
        exec_data["executions"] = []
    exec_data["executions"].append(execution)
    exec_data["alignment_summary"] = calculate_discipline_score()
    save_json(EXECUTIONS_FILE, exec_data)
    
    # 输出分析结果
    print(f"\n{'='*60}")
    print(f"📝 执行记录已保存: {code} {action} {shares}股 @ {price}元")
    print(f"{'='*60}")
    
    if strategy:
        print_alignment_analysis(execution["strategy_alignment"])
    
    return execution


def classify_action_type(action: str) -> str:
    """分类操作类型"""
    action_map = {
        "买入": "entry",
        "建仓": "entry",
        "卖出": "exit",
        "清仓": "exit",
        "加仓": "add",
        "减仓": "reduce",
        "止盈": "take_profit",
        "止损": "stop_loss"
    }
    return action_map.get(action, "unknown")


def analyze_alignment(strategy: dict, position: dict, action: str, price: float, shares: int) -> dict:
    """分析执行与策略的一致性"""
    strategy_plan = strategy.get("strategy", {})
    expected_price_levels = strategy_plan.get("take_profit_levels", [])
    stop_loss = strategy_plan.get("stop_loss", {})
    
    alignment = {
        "aligned": False,
        "deviation": None,
        "reason": "",
        "expected_action": None,
        "actual_action": f"{action} {shares}股 @ {price}元",
        "suggestions": []
    }
    
    # 分析不同类型操作的策略一致性
    action_type = classify_action_type(action)
    
    if action_type == "take_profit" or action_type == "reduce":
        # 检查是否到达止盈位
        for level in expected_price_levels:
            if abs(price - level["price"]) / level["price"] < 0.02:  # 2%误差范围
                if shares == level["shares"]:
                    alignment["aligned"] = True
                    alignment["reason"] = f"完美执行第{level['level']}档止盈策略"
                else:
                    alignment["aligned"] = True
                    alignment["deviation"] = f"股数偏差: 策略建议{level['shares']}股, 实际{shares}股"
                    alignment["reason"] = f"基本符合第{level['level']}档止盈，股数略有偏差"
                alignment["expected_action"] = f"第{level['level']}档止盈: {level['price']}元减仓{level['shares']}股"
                break
        else:
            # 未到达止盈位就减仓
            if expected_price_levels:
                next_level = expected_price_levels[0]
                if price < next_level["price"]:
                    alignment["aligned"] = False
                    alignment["deviation"] = "提前减仓"
                    alignment["reason"] = f"未到达第一止盈位({next_level['price']}元)就减仓，可能错失后续涨幅"
                    alignment["expected_action"] = f"等待 {next_level['price']}元 再减仓"
                    alignment["suggestions"].append("如果担心回调，可考虑减仓更少（如50股而非100股）")
                    alignment["suggestions"].append("或设置移动止损，而非提前止盈")
    
    elif action_type == "stop_loss":
        expected_stop = stop_loss.get("current_setting", stop_loss.get("breakeven", 0))
        if abs(price - expected_stop) / expected_stop < 0.01:  # 1%误差
            alignment["aligned"] = True
            alignment["reason"] = "严格执行止损策略，冰冷执行"
        elif price > expected_stop:
            alignment["aligned"] = False
            alignment["deviation"] = "止损偏高"
            alignment["reason"] = f"止损执行价({price})高于设定止损位({expected_stop})，多亏损了"
        else:
            alignment["aligned"] = True
            alignment["deviation"] = "止损滑点"
            alignment["reason"] = f"止损价略有滑点({price} vs {expected_stop})，属正常市场现象"
        alignment["expected_action"] = f"止损 @ {expected_stop}元"
    
    elif action_type == "entry":
        alignment["aligned"] = True
        alignment["reason"] = "建仓操作，符合策略初始规划"
    
    return alignment


def print_alignment_analysis(alignment: dict):
    """打印策略一致性分析"""
    if not alignment:
        return
    
    print("\n📊 策略一致性分析")
    print("-" * 60)
    
    if alignment["aligned"]:
        print("✅ 执行与策略一致")
    else:
        print("⚠️  执行与策略有偏差")
    
    if alignment["expected_action"]:
        print(f"\n策略建议: {alignment['expected_action']}")
    print(f"实际操作: {alignment['actual_action']}")
    
    if alignment["deviation"]:
        print(f"\n偏差类型: {alignment['deviation']}")
    
    print(f"\n分析: {alignment['reason']}")
    
    if alignment.get("suggestions"):
        print("\n💡 改进建议:")
        for i, sug in enumerate(alignment["suggestions"], 1):
            print(f"   {i}. {sug}")
    
    print("-" * 60)


def view_strategy(code: str):
    """查看策略详情"""
    strategy = get_strategy(code)
    if not strategy:
        print(f"❌ 未找到 {code} 的策略")
        return
    
    print("\n" + "=" * 70)
    print(f"📋 {strategy['name']} ({code}) 交易策略")
    print("=" * 70)
    print(f"创建时间: {strategy['created_at']}")
    print(f"策略状态: {'✅ 活跃' if strategy['status'] == 'active' else '⏸️ 已关闭'}")
    
    # 持仓背景
    ctx = strategy.get("position_context", {})
    print(f"\n【策略制定时的持仓背景】")
    print(f"  成本价: {ctx.get('entry_price')}元")
    print(f"  持股数: {ctx.get('shares')}股")
    print(f"  当时股价: {ctx.get('current_price_at_analysis')}元")
    print(f"  当时盈亏: {ctx.get('unrealized_pnl_pct_at_analysis')}%")
    
    # 止盈策略
    print(f"\n【止盈策略】")
    for level in strategy["strategy"]["take_profit_levels"]:
        print(f"  第{level['level']}档: {level['price']}元 ({level['pct']:+.1f}%)")
        print(f"          操作: {level['action']} {level['shares']}股")
        print(f"          理由: {level['reason']}")
    
    # 止损策略
    sl = strategy["strategy"]["stop_loss"]
    print(f"\n【止损策略】")
    print(f"  止损位: {sl['current_setting']}元")
    print(f"  逻辑: {sl['reason']}")
    
    # 执行计划
    print(f"\n【执行计划】")
    for action in strategy["execution_plan"]["conditional_actions"]:
        status_emoji = "⏳" if action['status'] == 'pending' else "✅"
        print(f"  {status_emoji} 当 {action['trigger']} → {action['action']}")
    
    print("=" * 70 + "\n")


def view_execution_analysis(code: Optional[str] = None):
    """查看执行分析"""
    exec_data = load_json(EXECUTIONS_FILE)
    executions = exec_data.get("executions", [])
    
    if code:
        executions = [e for e in executions if e["code"] == code]
    
    if not executions:
        print("📭 暂无执行记录")
        return
    
    print("\n" + "=" * 70)
    print("📈 交易执行分析")
    print("=" * 70)
    
    # 纪律评分
    score_data = calculate_discipline_score()
    print(f"\n【交易纪律评分】")
    print(f"  总分: {score_data['score']}/100")
    print(f"  总执行次数: {score_data['total']}")
    print(f"  符合策略: {score_data['aligned']}次")
    print(f"  偏离策略: {score_data['deviated']}次")
    
    # 执行列表
    print(f"\n【执行记录】")
    for exec_record in executions[-10:]:  # 最近10条
        alignment = exec_record.get("strategy_alignment", {})
        emoji = "✅" if alignment.get("aligned") else "⚠️" if alignment else "📝"
        print(f"\n{emoji} {exec_record['timestamp'][:10]} {exec_record['name']}({exec_record['code']})")
        print(f"   操作: {exec_record['action']} {exec_record['execution_details']['shares']}股 "
              f"@ {exec_record['execution_details']['price']}元")
        if alignment:
            print(f"   一致性: {'符合' if alignment['aligned'] else '偏离'}")
            if alignment.get("deviation"):
                print(f"   偏差: {alignment['deviation']}")
    
    print("=" * 70 + "\n")


def update_strategy_status(code: str, status: str):
    """更新策略状态（如策略到期、目标达成等）"""
    data = load_json(STRATEGIES_FILE)
    strategy = next((s for s in data.get("strategies", []) if s["code"] == code), None)
    
    if not strategy:
        print(f"❌ 未找到 {code} 的策略")
        return
    
    strategy["status"] = status
    strategy["updated_at"] = datetime.now().isoformat()
    save_json(STRATEGIES_FILE, data)
    print(f"✅ 已更新 {code} 策略状态为: {status}")


def main():
    if len(sys.argv) < 2:
        print("""
Stock Strategy Manager - 策略管理与执行分析

用法:
  python3 strategy_manager.py strategy <code>              # 查看策略详情
  python3 strategy_manager.py execute <code> <action> <price> <shares> [notes]
                                                           # 记录执行并分析
  python3 strategy_manager.py analysis [code]              # 查看执行分析
  python3 strategy_manager.py close <code>                 # 关闭策略（目标达成/止损）

示例:
  python3 strategy_manager.py strategy 600089              # 查看特变电工策略
  python3 strategy_manager.py execute 600089 减仓 31.50 100 "到达第一止盈位"
  python3 strategy_manager.py analysis                     # 查看所有执行分析
  python3 strategy_manager.py close 600089                 # 标记策略完成
        """)
        return
    
    command = sys.argv[1]
    
    if command == "strategy" and len(sys.argv) >= 3:
        view_strategy(sys.argv[2])
    
    elif command == "execute" and len(sys.argv) >= 6:
        code = sys.argv[2]
        action = sys.argv[3]
        price = float(sys.argv[4])
        shares = int(sys.argv[5])
        notes = sys.argv[6] if len(sys.argv) > 6 else ""
        record_execution(code, action, price, shares, notes)
    
    elif command == "analysis":
        code = sys.argv[2] if len(sys.argv) > 2 else None
        view_execution_analysis(code)
    
    elif command == "close" and len(sys.argv) >= 3:
        update_strategy_status(sys.argv[2], "completed")
    
    else:
        print("❌ 未知命令或参数不足")


if __name__ == "__main__":
    main()
