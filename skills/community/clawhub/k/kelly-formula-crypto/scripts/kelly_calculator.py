#!/usr/bin/env python3
"""
Kelly Formula Calculator for Crypto Trading
Price: 0.01 USDC via x402
"""

import argparse
import json
from typing import Optional, Tuple

# x402 payment endpoint
X402_ENDPOINT = "https://api.x402.dev/pay"
PAYMENT_ADDRESS = "0x24b288c98421d7b447c2d6a6442538d01c5fce22"


def kelly_position(p: float, b: float, fraction: float = 0.5) -> float:
    """
    Calculate Kelly position size.
    
    Args:
        p: Win probability (0-1)
        b: Win/Loss ratio (e.g., 2.0 means win 2x of what you lose)
        fraction: Kelly fraction (0.5 = half-Kelly, 0.25 = quarter-Kelly)
    
    Returns:
        Position size as percentage (0-1)
    """
    if p <= 0.5 or b <= 0:
        return 0.0
    
    f_star = (p * b - (1 - p)) / b
    if f_star < 0:
        return 0.0
    
    return f_star * fraction


def net_edge(p: float, win_pct: float, loss_pct: float) -> float:
    """
    Calculate net edge.
    
    Args:
        p: Win probability
        win_pct: Win percentage (e.g., 5 for 5%)
        loss_pct: Loss percentage (e.g., 3 for 3%)
    
    Returns:
        Net edge as percentage
    """
    return p * win_pct - (1 - p) * loss_pct


def suggested_position(net_edge: float, win_pct: float, fraction: float = 0.5) -> float:
    """
    Calculate suggested position from net edge.
    
    Args:
        net_edge: Net edge percentage
        win_pct: Win percentage
        fraction: Kelly fraction
    
    Returns:
        Suggested position as percentage
    """
    if net_edge <= 0 or win_pct <= 0:
        return 0.0
    
    return (net_edge / win_pct) * fraction


def leverage_safety(liquidation_pct: float, stop_loss_pct: float) -> Tuple[bool, float]:
    """
    Check if leverage is safe.
    
    Args:
        liquidation_pct: Distance to liquidation (e.g., 10 for 10%)
        stop_loss_pct: Stop loss distance (e.g., 3 for 3%)
    
    Returns:
        (is_safe, safety_factor)
    """
    safety_factor = liquidation_pct / stop_loss_pct
    is_safe = safety_factor >= 2.0
    return is_safe, safety_factor


def adjusted_multi_position(positions: list, correlation: float, discount: float = 0.7) -> float:
    """
    Adjust position for correlation.
    
    Args:
        positions: List of individual positions
        correlation: Correlation between positions (0-1)
        discount: Discount factor when correlation > 0.7
    
    Returns:
        Adjusted total position
    """
    total = sum(positions)
    if correlation > 0.7:
        return total * discount
    return total


def symmetric_lookup(p: float, fraction: float = 0.5) -> Optional[float]:
    """
    Quick lookup for symmetric wins/losses.
    
    Args:
        p: Win probability (e.g., 0.55 for 55%)
        fraction: Kelly fraction
    
    Returns:
        Position as percentage or None if no edge
    """
    # f* ≈ 2p - 1
    kelly = 2 * p - 1
    if kelly <= 0:
        return None
    
    return kelly * fraction


def calculate_trade(p: float, win_pct: float, loss_pct: float, 
                   fraction: float = 0.5, leverage: float = 1.0,
                   liquidation_pct: Optional[float] = None,
                   stop_loss_pct: Optional[float] = None) -> dict:
    """
    Full trade calculation with all factors.
    """
    b = win_pct / loss_pct
    
    # Basic Kelly
    full_kelly = kelly_position(p, b, 1.0)
    half_kelly = kelly_position(p, b, 0.5)
    quarter_kelly = kelly_position(p, b, 0.25)
    
    # Net edge method
    edge = net_edge(p, win_pct, loss_pct)
    suggested = suggested_position(edge, win_pct, fraction)
    
    result = {
        "inputs": {
            "win_probability": p,
            "win_pct": win_pct,
            "loss_pct": loss_pct,
            "fraction": fraction,
            "leverage": leverage
        },
        "kelly": {
            "full_kelly_pct": round(full_kelly * 100, 2),
            "half_kelly_pct": round(half_kelly * 100, 2),
            "quarter_kelly_pct": round(quarter_kelly * 100, 2)
        },
        "net_edge": {
            "edge_pct": round(edge, 2),
            "suggested_pct": round(suggested * 100, 2)
        },
        "recommendation": {
            "position_pct": round(half_kelly * 100, 2),
            "reason": "Half-Kelly recommended for balanced risk"
        }
    }
    
    # Leverage check
    if leverage > 1 and liquidation_pct and stop_loss_pct:
        is_safe, safety_factor = leverage_safety(liquidation_pct, stop_loss_pct)
        result["leverage_check"] = {
            "liquidation_pct": liquidation_pct,
            "stop_loss_pct": stop_loss_pct,
            "safety_factor": round(safety_factor, 2),
            "is_safe": is_safe,
            "recommendation": "Reduce leverage" if not is_safe else "OK"
        }
    
    return result


def main():
    parser = argparse.ArgumentParser(description="Kelly Formula Calculator for Crypto")
    parser.add_argument("-p", "--probability", type=float, required=True,
                        help="Win probability (0-1, e.g., 0.55)")
    parser.add_argument("-w", "--win", type=float, required=True,
                        help="Win percentage (e.g., 5 for 5%)")
    parser.add_argument("-l", "--loss", type=float, required=True,
                        help="Loss percentage (e.g., 3 for 3%)")
    parser.add_argument("-f", "--fraction", type=float, default=0.5,
                        help="Kelly fraction (default: 0.5)")
    parser.add_argument("--leverage", type=float, default=1.0,
                        help="Leverage (default: 1.0)")
    parser.add_argument("--liquidation", type=float,
                        help="Liquidation distance percentage")
    parser.add_argument("--stop-loss", type=float,
                        help="Stop loss percentage")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    
    args = parser.parse_args()
    
    result = calculate_trade(
        p=args.probability,
        win_pct=args.win,
        loss_pct=args.loss,
        fraction=args.fraction,
        leverage=args.leverage,
        liquidation_pct=args.liquidation,
        stop_loss_pct=args.stop_loss
    )
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"\n📊 Kelly Formula 计算结果")
        print(f"=" * 40)
        print(f"胜率: {args.probability*100:.0f}% | 盈亏比: {args.win/args.loss:.2f}")
        print(f"")
        print(f"🧮 仓位建议:")
        print(f"  全凯利: {result['kelly']['full_kelly_pct']}%")
        print(f"  ½凯利:  {result['kelly']['half_kelly_pct']}%")
        print(f"  ¼凯利:  {result['kelly']['quarter_kelly_pct']}%")
        print(f"")
        print(f"✅ 推荐仓位: {result['recommendation']['position_pct']}%")
        
        if "leverage_check" in result:
            lc = result["leverage_check"]
            print(f"")
            print(f"⚠️ 杠杆检查:")
            print(f"  安全系数: {lc['safety_factor']}")
            print(f"  状态: {lc['recommendation']}")


if __name__ == "__main__":
    main()
