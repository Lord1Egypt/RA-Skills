"""
Bitquery Polymarket Prediction Trades — Real-time streaming on Polygon
======================================================================
Subscribe to the Bitquery WebSocket API for a live Polymarket prediction trade feed on Polygon (matic).

Every event is a successful prediction trade with:
  - OutcomeTrade: Buyer, Seller, Amount, CollateralAmount, CollateralAmountInUSD, Price, PriceInUSD, IsOutcomeBuy
  - Prediction: Question (Title, MarketId, ResolutionSource), Outcome (Label), Marketplace (ProtocolName)
  - Block.Time, Transaction.Hash, Call.Signature.Name (e.g. matchOrders), Log.Signature.Name (e.g. OrderFilled)

Filter: EVM network matic, TransactionStatus.Success = true.

Trader use cases:
  1. Order flow / market activity
  2. Whale / large-trade detection (CollateralAmountInUSD)
  3. Market-specific monitoring (Question.MarketId, Title)
  4. Outcome imbalance (Outcome.Label, IsOutcomeBuy)
  5. Resolution source / data markets
  6. Entry / exit timing (PriceInUSD, CollateralAmountInUSD)
  7. Protocol verification (Marketplace.ProtocolName)
  8. Audit trail (Transaction.Hash, Block.Time, Call/Log signatures)

Usage:
    python scripts/stream_polymarket.py
    python scripts/stream_polymarket.py --timeout 60

Environment:
    BITQUERY_API_KEY — Your Bitquery token (required). Passed as ?token= in WebSocket URL.

Docs:
    https://docs.bitquery.io/docs/examples/polymarket-api/
"""

import asyncio
import os
import sys
from urllib.parse import urlencode

from gql import Client, gql
from gql.transport.websockets import WebsocketsTransport


BITQUERY_WS_BASE = "wss://streaming.bitquery.io/graphql"

POLYMARKET_PREDICTION_TRADES_SUBSCRIPTION = gql("""
subscription MyQuery {
  EVM(network: matic) {
    PredictionTrades(where: { TransactionStatus: { Success: true } }) {
      Block {
        Time
      }
      Call {
        Signature {
          Name
        }
      }
      Log {
        Signature {
          Name
        }
        SmartContract
      }
      Trade {
        OutcomeTrade {
          Buyer
          Seller
          Amount
          CollateralAmount
          CollateralAmountInUSD
          OrderId
          Price
          PriceInUSD
          IsOutcomeBuy
        }
        Prediction {
          CollateralToken {
            Name
            Symbol
            SmartContract
            AssetId
          }
          ConditionId
          OutcomeToken {
            Name
            Symbol
            SmartContract
            AssetId
          }
          Marketplace {
            SmartContract
            ProtocolVersion
            ProtocolName
            ProtocolFamily
          }
          Question {
            Title
            ResolutionSource
            Image
            MarketId
            Id
            CreatedAt
          }
          Outcome {
            Id
            Index
            Label
          }
        }
      }
      Transaction {
        From
        Hash
      }
    }
  }
}
""")


def get_api_key() -> str:
    """Read the Bitquery API key from the environment. Raises if not set."""
    key = os.getenv("BITQUERY_API_KEY")
    if not key:
        raise EnvironmentError(
            "BITQUERY_API_KEY is not set. "
            "Please export your Bitquery token:\n"
            "  export BITQUERY_API_KEY=your_token_here"
        )
    return key


def _addr_short(addr: str | None, length: int = 8) -> str:
    if not addr or len(addr) <= length * 2 + 2:
        return addr or "N/A"
    return f"{addr[:length]}...{addr[-length:]}"


def _fmt_usd(value) -> str:
    if value is None:
        return "N/A"
    try:
        return f"${float(value):,.4f}"
    except (ValueError, TypeError):
        return str(value)


def format_trade(data: dict) -> str:
    """Format one PredictionTrades event for display."""
    evm = (data or {}).get("EVM") or {}
    trades = evm.get("PredictionTrades") or []
    if not trades:
        return ""

    lines = []
    sep = "━" * 52

    for item in trades:
        block = item.get("Block") or {}
        call = item.get("Call") or {}
        log = item.get("Log") or {}
        trade = item.get("Trade") or {}
        tx = item.get("Transaction") or {}

        outcome_trade = trade.get("OutcomeTrade") or {}
        prediction = trade.get("Prediction") or {}
        question = prediction.get("Question") or {}
        outcome = prediction.get("Outcome") or {}
        marketplace = prediction.get("Marketplace") or {}
        collateral_token = prediction.get("CollateralToken") or {}
        collateral_symbol = collateral_token.get("Symbol") or ""

        call_name = (call.get("Signature") or {}).get("Name") or "?"
        log_name = (log.get("Signature") or {}).get("Name") or "?"
        log_contract = log.get("SmartContract") or "?"
        tx_hash = tx.get("Hash") or "?"
        tx_hash_short = _addr_short(tx_hash, 6) if tx_hash != "?" else "?"

        title = question.get("Title") or "?"
        market_id = question.get("MarketId") or "?"
        resolution = question.get("ResolutionSource") or ""
        outcome_label = outcome.get("Label") or "?"
        outcome_index = outcome.get("Index", "?")

        protocol = marketplace.get("ProtocolName") or "?"
        protocol_family = marketplace.get("ProtocolFamily") or ""

        buyer = outcome_trade.get("Buyer") or "?"
        seller = outcome_trade.get("Seller") or "?"
        collateral_amt = outcome_trade.get("CollateralAmount")
        collateral_usd = outcome_trade.get("CollateralAmountInUSD")
        price = outcome_trade.get("Price")
        price_usd = outcome_trade.get("PriceInUSD")
        amount = outcome_trade.get("Amount") or "?"
        is_buy = outcome_trade.get("IsOutcomeBuy", False)
        side = "BUY outcome" if is_buy else "SELL outcome"

        time_str = block.get("Time") or "?"

        lines.append(sep)
        lines.append(f"Polymarket  [matic]  Protocol: {protocol} ({protocol_family})")
        lines.append(f"Time: {time_str}  Tx: {tx_hash_short}")
        lines.append(sep)
        lines.append(f"Question: {title}")
        lines.append(f"MarketId: {market_id}  |  Outcome: {outcome_label}  (Index {outcome_index})")
        if resolution:
            lines.append(f"Resolution: {resolution}")
        lines.append(sep)
        lines.append("OutcomeTrade")
        lines.append(f"  Side:       {side} (IsOutcomeBuy: {is_buy})")
        lines.append(f"  Buyer:      {_addr_short(buyer)}  →  Seller: {_addr_short(seller)}")
        collateral_str = f"{collateral_amt} {collateral_symbol}".strip() if collateral_amt else _fmt_usd(collateral_usd)
        lines.append(f"  Collateral: {collateral_str}  (USD: {_fmt_usd(collateral_usd)})")
        lines.append(f"  Price:      {price}  (USD: {_fmt_usd(price_usd)})")
        lines.append(f"  Amount:     {amount} (outcome tokens)")
        order_id = outcome_trade.get("OrderId") or ""
        if order_id and len(order_id) > 24:
            order_id = order_id[:24] + "..."
        lines.append(f"  OrderId:    {order_id}")
        lines.append(f"Call: {call_name}  |  Log: {log_name} @ {_addr_short(log_contract)}")
        lines.append(sep)
        lines.append("")

    return "\n".join(lines)


async def run_stream(timeout_seconds: int | None = None) -> None:
    api_key = get_api_key()
    url = f"{BITQUERY_WS_BASE}?{urlencode({'token': api_key})}"
    transport = WebsocketsTransport(
        url=url,
        headers={"Sec-WebSocket-Protocol": "graphql-ws"},
    )

    event_count = 0

    async with Client(transport=transport) as session:
        print("Connected. Streaming Polymarket prediction trades (matic). Ctrl+C to stop.\n")

        async def consume():
            nonlocal event_count
            try:
                async for result in session.subscribe(POLYMARKET_PREDICTION_TRADES_SUBSCRIPTION):
                    event_count += 1
                    out = format_trade(result)
                    if out:
                        print(out)
            except asyncio.CancelledError:
                pass

        if timeout_seconds is not None:
            try:
                await asyncio.wait_for(consume(), timeout=float(timeout_seconds))
            except asyncio.TimeoutError:
                print(f"\nStopped after {timeout_seconds}s ({event_count} events).")
        else:
            await consume()


def main() -> None:
    timeout: int | None = None
    if len(sys.argv) > 1 and sys.argv[1] == "--timeout" and len(sys.argv) > 2:
        try:
            timeout = int(sys.argv[2])
        except ValueError:
            print("Usage: python stream_polymarket.py [--timeout SECONDS]", file=sys.stderr)
            sys.exit(2)

    try:
        asyncio.run(run_stream(timeout_seconds=timeout))
    except EnvironmentError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nStream stopped by user.")


if __name__ == "__main__":
    main()
