#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import sys

from config import load_trade_config
from errors import TradeCliError
from trade_client import NoahTradeClient
from portfolio_client import (
    NoahPortfolioClient,
    summarize_account_info,
    summarize_positions,
    summarize_sec_asset,
    summarize_capital_flow,
    portfolio_text,
)
from formatters import (
    success_response,
    error_response,
    summarize_today_orders,
    summarize_today_deals,
    summarize_history_deals,
    summarize_today_unfinished_orders,
    summarize_finished_orders,
    summarize_order_detail,
    summarize_fee_estimate,
    summarize_stock_amount,
    summarize_order_fee_detail,
    summarize_max_enable_buy_amt,
)
from symbol_utils import normalize_trade_symbol


def build_parser():
    parser = argparse.ArgumentParser(
        description="Noah Trade CLI - query and pre-trade evaluation for internal stock trade APIs"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("account-info", help="Get account info")

    p_positions = subparsers.add_parser("positions", help="Get positions")
    p_positions.add_argument("--market", required=True, choices=["HK", "US", "SH", "SZ"], help="Market code")

    subparsers.add_parser("sec-asset", help="Get securities asset")

    p_flow = subparsers.add_parser("sec-capital-flow", help="Get securities capital flow")
    p_flow.add_argument("--start-date", help="Start date, yyyyMMdd")
    p_flow.add_argument("--end-date", help="End date, yyyyMMdd")
    p_flow.add_argument("--business-type")
    p_flow.add_argument("--fund-direction")
    p_flow.add_argument("--page", type=int)
    p_flow.add_argument("--page-size", type=int)
    p_flow.add_argument("--last-id")
    p_flow.add_argument("--record-last-id")
    p_flow.add_argument("--trade-code")
    p_flow.add_argument("--unique-code")

    p_orders = subparsers.add_parser("today-orders", help="Get today's order list")
    p_orders.add_argument("--market", required=True, choices=["HK", "US", "SH", "SZ"], help="Market code")
    p_orders.add_argument("--symbol", help="Optional trade symbol, e.g. HK.00700 / HK-00700 / 00700")
    p_orders.add_argument("--page", type=int, default=1, help="Page number")
    p_orders.add_argument("--page-size", type=int, default=50, help="Page size")

    p_deals = subparsers.add_parser("today-deals", help="Get today's deal list")
    p_deals.add_argument("--symbol", help="Optional trade symbol, e.g. HK.00700 / HK-00700 / 00700")

    p_hist_orders = subparsers.add_parser("history-orders", help="Get history order list")
    p_hist_orders.add_argument("--symbol", help="Optional trade symbol")
    p_hist_orders.add_argument("--start-date", required=True, help="Start date, yyyyMMdd")
    p_hist_orders.add_argument("--end-date", required=True, help="End date, yyyyMMdd")
    p_hist_orders.add_argument("--order-id")
    p_hist_orders.add_argument("--order-no")
    p_hist_orders.add_argument("--order-status")

    p_hist_deals = subparsers.add_parser("history-deals", help="Get history deal list")
    p_hist_deals.add_argument("--symbol", help="Optional trade symbol")
    p_hist_deals.add_argument("--start-date", required=True, help="Start date, yyyyMMdd")
    p_hist_deals.add_argument("--end-date", required=True, help="End date, yyyyMMdd")

    p_unfinished = subparsers.add_parser("unfinished-orders", help="Get unfinished today orders")
    p_unfinished.add_argument("--symbol", help="Optional trade symbol")
    p_unfinished.add_argument("--order-id")
    p_unfinished.add_argument("--order-no")
    p_unfinished.add_argument("--order-status")

    p_finished = subparsers.add_parser("finished-orders", help="Get finished order list")
    p_finished.add_argument("--symbol", help="Optional trade symbol")
    p_finished.add_argument("--start-date", help="Start date, yyyyMMdd")
    p_finished.add_argument("--end-date", help="End date, yyyyMMdd")
    p_finished.add_argument("--page", type=int)
    p_finished.add_argument("--page-size", type=int)
    p_finished.add_argument("--order-id")
    p_finished.add_argument("--order-no")
    p_finished.add_argument("--order-status")
    p_finished.add_argument("--order-side", choices=["BUY", "SELL"])
    p_finished.add_argument("--order-type", choices=["LIMIT", "MARKET"])

    p_detail = subparsers.add_parser("order-detail", help="Get order detail by order id")
    p_detail.add_argument("--order-id", required=True, help="Order ID")
    p_detail.add_argument("--order-no", help="Broker order no")
    p_detail.add_argument("--is-history", action="store_true", help="Query from history set")

    p_fee = subparsers.add_parser("fee-estimate", help="Estimate order fee")
    p_fee.add_argument("--symbol", required=True, help="Trade symbol, e.g. HK.00700 / HK-00700 / 00700")
    p_fee.add_argument("--side", required=True, choices=["BUY", "SELL"], help="Order side")
    p_fee.add_argument("--order-type", required=True, choices=["LIMIT", "MARKET"], help="Order type")
    p_fee.add_argument("--price", type=float, help="Order price; usually required for LIMIT")
    p_fee.add_argument("--qty", required=True, type=float, help="Order quantity")

    p_push = subparsers.add_parser("query-push-data", help="Query push data")
    p_push.add_argument("--init-date", required=True, help="Init date, yyyyMMdd")
    p_push.add_argument("--begin-serial-no", required=True)
    p_push.add_argument("--end-serial-no", required=True)

    p_fee_detail = subparsers.add_parser("order-fee-detail", help="Get order fee detail")
    p_fee_detail.add_argument("--order-id", required=True)
    p_fee_detail.add_argument("--order-no")
    p_fee_detail.add_argument("--is-history", action="store_true")

    p_amt = subparsers.add_parser("stock-amount", help="Get available buy/sell stock amount")
    p_amt.add_argument("--symbol", required=True, help="Trade symbol, e.g. HK.00700 / HK-00700 / 00700")
    p_amt.add_argument("--order-type", required=True, choices=["LO", "ELO", "SLO", "AO", "ALO", "TLO", "MO", "ODD"], help="Entrust property")
    p_amt.add_argument("--session-type", type=int, choices=[0, 1, 2, 3], help="Session type")

    p_max = subparsers.add_parser("max-enable-buy-amt", help="Get max enable buy amount")
    p_max.add_argument("--symbol", required=True, help="Trade symbol")
    p_max.add_argument("--order-type", required=True, choices=["LO", "ELO", "SLO", "AO", "ALO", "TLO", "MO", "ODD"], help="Entrust property")
    p_max.add_argument("--entrust-price", required=True, type=float, help="Entrust price")
    p_max.add_argument("--session-type", type=int, choices=[0, 1, 2, 3], help="Session type")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    command = getattr(args, "command", "unknown")

    try:
        config = load_trade_config()
        client = NoahTradeClient(config)
        portfolio = NoahPortfolioClient(config)

        if command == "account-info":
            raw = portfolio.get_account_info()
            data = raw.get('response', {}).get('data') or {}
            summary = summarize_account_info(data)
            result = {'human_summary': portfolio_text(command, summary), 'data': summary}
            print(json.dumps(success_response(command, config, result, raw), ensure_ascii=False))
            return 0

        if command == "positions":
            raw = portfolio.get_positions(market=args.market)
            data = raw.get('response', {}).get('data') or []
            summary = summarize_positions(data)
            result = {'human_summary': portfolio_text(command, summary), 'data': summary}
            print(json.dumps(success_response(command, config, result, raw), ensure_ascii=False))
            return 0

        if command == "sec-asset":
            raw = portfolio.get_sec_asset()
            data = raw.get('response', {}).get('data') or []
            summary = summarize_sec_asset(data)
            result = {'human_summary': portfolio_text(command, summary), 'data': summary}
            print(json.dumps(success_response(command, config, result, raw), ensure_ascii=False))
            return 0

        if command == "sec-capital-flow":
            raw = portfolio.get_sec_capital_flow(
                start_date=args.start_date,
                end_date=args.end_date,
                business_type=args.business_type,
                fund_direction=args.fund_direction,
                page=args.page,
                page_size=args.page_size,
                last_id=args.last_id,
                record_last_id=args.record_last_id,
                trade_code=args.trade_code,
                unique_code=args.unique_code,
            )
            data = raw.get('response', {}).get('data') or {}
            summary = summarize_capital_flow(data)
            result = {'human_summary': portfolio_text(command, summary), 'data': summary}
            print(json.dumps(success_response(command, config, result, raw), ensure_ascii=False))
            return 0

        if command == "today-orders":
            symbol = normalize_trade_symbol(args.symbol) if args.symbol else None
            raw = client.get_today_orders(market=args.market, code=symbol, page=args.page, page_size=args.page_size)
            result = summarize_today_orders(raw)
            print(json.dumps(success_response(command, config, result, raw), ensure_ascii=False))
            return 0

        if command == "today-deals":
            symbol = normalize_trade_symbol(args.symbol) if args.symbol else None
            raw = client.get_today_deals(code=symbol)
            result = summarize_today_deals(raw)
            print(json.dumps(success_response(command, config, result, raw), ensure_ascii=False))
            return 0

        if command == "history-orders":
            symbol = normalize_trade_symbol(args.symbol) if getattr(args, "symbol", None) else None
            raw = client.get_history_orders(code=symbol, start_date=args.start_date, end_date=args.end_date, order_id=args.order_id, order_no=args.order_no, order_status=args.order_status)
            result = summarize_today_orders(raw)
            print(json.dumps(success_response(command, config, result, raw), ensure_ascii=False))
            return 0

        if command == "history-deals":
            symbol = normalize_trade_symbol(args.symbol) if args.symbol else None
            raw = client.get_history_deals(code=symbol, start_date=args.start_date, end_date=args.end_date)
            result = summarize_history_deals(raw)
            print(json.dumps(success_response(command, config, result, raw), ensure_ascii=False))
            return 0

        if command == "unfinished-orders":
            symbol = normalize_trade_symbol(args.symbol) if args.symbol else None
            raw = client.get_today_unfinished_orders(code=symbol, order_id=args.order_id, order_no=args.order_no, order_status=args.order_status)
            result = summarize_today_unfinished_orders(raw)
            print(json.dumps(success_response(command, config, result, raw), ensure_ascii=False))
            return 0

        if command == "finished-orders":
            symbol = normalize_trade_symbol(args.symbol) if args.symbol else None
            raw = client.get_finished_orders(
                code=symbol,
                start_date=args.start_date,
                end_date=args.end_date,
                page=args.page,
                page_size=args.page_size,
                order_id=args.order_id,
                order_no=args.order_no,
                order_status=args.order_status,
                order_side=args.order_side,
                order_type=args.order_type,
            )
            result = summarize_finished_orders(raw)
            print(json.dumps(success_response(command, config, result, raw), ensure_ascii=False))
            return 0

        if command == "order-detail":
            raw = client.get_order_detail(order_id=args.order_id, order_no=args.order_no, is_history=args.is_history)
            result = summarize_order_detail(raw)
            print(json.dumps(success_response(command, config, result, raw), ensure_ascii=False))
            return 0

        if command == "fee-estimate":
            symbol = normalize_trade_symbol(args.symbol)
            raw = client.order_fee_query(
                symbol=symbol,
                side=args.side,
                order_type=args.order_type,
                price=args.price,
                qty=args.qty,
            )
            result = summarize_fee_estimate(raw, symbol=symbol, side=args.side, price=args.price, qty=args.qty)
            print(json.dumps(success_response(command, config, result, raw), ensure_ascii=False))
            return 0

        if command == "query-push-data":
            raw = client.query_push_data(init_date=args.init_date, begin_serial_no=args.begin_serial_no, end_serial_no=args.end_serial_no)
            print(json.dumps(success_response(command, config, {"raw": raw.get("response", {}).get("data")}, raw), ensure_ascii=False))
            return 0

        if command == "order-fee-detail":
            raw = client.get_order_fee_detail(order_id=args.order_id, order_no=args.order_no, is_history=args.is_history)
            result = summarize_order_fee_detail(raw)
            print(json.dumps(success_response(command, config, result, raw), ensure_ascii=False))
            return 0

        if command == "stock-amount":
            symbol = normalize_trade_symbol(args.symbol)
            raw = client.get_stock_amount(symbol=symbol, order_type=args.order_type, session_type=args.session_type)
            result = summarize_stock_amount(raw, symbol=symbol)
            print(json.dumps(success_response(command, config, result, raw), ensure_ascii=False))
            return 0

        if command == "max-enable-buy-amt":
            symbol = normalize_trade_symbol(args.symbol)
            raw = client.max_enable_buy_amt(
                symbol=symbol,
                order_type=args.order_type,
                entrust_price=args.entrust_price,
                session_type=args.session_type,
            )
            result = summarize_max_enable_buy_amt(raw, symbol=symbol, order_type=args.order_type)
            print(json.dumps(success_response(command, config, result, raw), ensure_ascii=False))
            return 0

        raise TradeCliError(f"Unsupported command: {command}")

    except Exception as e:
        print(json.dumps(error_response(command, e), ensure_ascii=False))
        return 1


if __name__ == "__main__":
    sys.exit(main())
