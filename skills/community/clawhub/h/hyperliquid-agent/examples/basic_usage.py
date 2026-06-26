from dataclasses import dataclass

@dataclass
class Signal:
    should_trade: bool
    side: str
    entry_price: float
    stop_loss: float
    take_profit: float | None = None

class MockAuthenticatedHyperliquidClient:
    def submit_order(self, order_request: dict) -> dict:
        return {
            "status": "filled",
            "order_id": "demo-order-001",
            "average_fill_price": order_request["entry_price"],
            "filled_size": order_request["size"],
        }

def calculate_position_size(balance: float, risk_per_trade: float, entry_price: float, stop_loss: float) -> float:
    stop_distance = abs(entry_price - stop_loss)
    if stop_distance <= 0:
        raise ValueError("stop distance must be greater than zero")
    risk_amount = balance * risk_per_trade
    return risk_amount / stop_distance

def validate_trade(account_state: dict, signal: Signal, risk_per_trade: float, leverage: float) -> tuple[bool, str]:
    if not signal.should_trade:
        return False, "no valid signal"
    if risk_per_trade <= 0 or risk_per_trade > 0.02:
        return False, "risk_per_trade outside allowed range"
    if leverage < 1 or leverage > 5:
        return False, "leverage outside allowed range"
    if account_state["daily_pnl_pct"] <= -0.05:
        return False, "daily loss limit reached"
    if signal.entry_price == signal.stop_loss:
        return False, "entry equals stop"
    return True, "ok"

def build_order_request(market: str, signal: Signal, size: float, leverage: float) -> dict:
    return {
        "market": market,
        "side": signal.side,
        "order_type": "market",
        "size": round(size, 6),
        "leverage": leverage,
        "entry_price": signal.entry_price,
        "stop_loss": signal.stop_loss,
        "take_profit": signal.take_profit,
    }

def run():
    client = MockAuthenticatedHyperliquidClient()
    account_state = {
        "balance": 1000.0,
        "daily_pnl_pct": -0.01,
        "open_positions": 0,
    }

    signal = Signal(
        should_trade=True,
        side="long",
        entry_price=50000.0,
        stop_loss=49400.0,
        take_profit=51200.0,
    )

    allowed, reason = validate_trade(
        account_state=account_state,
        signal=signal,
        risk_per_trade=0.01,
        leverage=3,
    )

    if not allowed:
        return {"trade_status": "skip", "reason": reason}

    size = calculate_position_size(
        balance=account_state["balance"],
        risk_per_trade=0.01,
        entry_price=signal.entry_price,
        stop_loss=signal.stop_loss,
    )

    order_request = build_order_request(
        market="BTC",
        signal=signal,
        size=size,
        leverage=3,
    )

    execution_result = client.submit_order(order_request)

    return {
        "trade_status": execution_result["status"],
        "reason": "validated and submitted through host-provided client",
        "order_request": order_request,
        "execution_result": execution_result,
    }

if __name__ == "__main__":
    print(run())
