#!/usr/bin/env python3
from typing import Any, Dict, List

DETAIL_LIMIT = 10


def _safe(v):
    return '-' if v is None else v


def _num(v):
    if v is None:
        return '-'
    try:
        if isinstance(v, int):
            return f'{v:,}'
        fv = float(v)
        if abs(fv) >= 1000:
            return f'{fv:,.2f}'.rstrip('0').rstrip('.')
        return f'{fv:.2f}'.rstrip('0').rstrip('.')
    except Exception:
        return v


def format_snapshot(summary: Dict[str, Any]) -> str:
    lines = []
    symbol = summary.get('symbol') or '-'
    name = summary.get('name') or '-'
    lines.append(f'标的：{name}（{symbol}）')
    lines.append(f'最新价：{_num(summary.get("last_price"))}')
    if summary.get('change_value') is not None or summary.get('change_pct') is not None:
        lines.append(f'涨跌额/涨跌幅：{_num(summary.get("change_value"))} / {_num(summary.get("change_pct"))}%')
    lines.append(f'今开/最高/最低：{_num(summary.get("open_price"))} / {_num(summary.get("high_price"))} / {_num(summary.get("low_price"))}')
    if summary.get('volume') is not None or summary.get('turnover') is not None:
        lines.append(f'成交量/成交额：{_num(summary.get("volume"))} / {_num(summary.get("turnover"))}')
    if summary.get('last_price') is not None and summary.get('open_price') is not None:
        try:
            if float(summary['last_price']) >= float(summary['open_price']):
                lines.append('观察：当前价格不弱于今开，盘中相对偏强。')
            else:
                lines.append('观察：当前价格低于今开，盘中相对偏弱。')
        except Exception:
            pass
    return '\n'.join(lines)


def format_market_state(summary_list: List[Dict[str, Any]]) -> str:
    if not summary_list:
        return '暂无市场状态数据'
    if len(summary_list) == 1:
        x = summary_list[0]
        return f'标的：{x.get("name") or "-"}（{x.get("symbol") or "-"}）\n当前状态：{x.get("market_state_text") or x.get("market_state")}'
    lines = ['全局市场状态：']
    for x in summary_list:
        lines.append(f'- {x.get("name") or x.get("symbol") or "-"}：{x.get("market_state_text") or x.get("market_state") or "-"}')
    return '\n'.join(lines)


def format_intraday(summary: Dict[str, Any], detail: bool = False) -> str:
    latest = summary.get('latest') or {}
    if detail and summary.get('items'):
        shown = summary.get('items', [])[-DETAIL_LIMIT:]
        lines = [f'标的：{latest.get("name") or "-"}（{latest.get("code") or "-"}）', '分时明细：']
        for i, x in enumerate(shown, 1):
            lines.append(
                f'{i}）{x.get("time") or x.get("data_time") or "-"}｜现价{_num(x.get("cur_price"))} / 均价{_num(x.get("avg_price"))} / 成交量{_num(x.get("volume"))}'
            )
        if len(summary.get('items', [])) > DETAIL_LIMIT:
            lines.append(f'说明：仅展示最近 {DETAIL_LIMIT} 条分时记录。')
        return '\n'.join(lines)

    lines = [
        f'标的：{latest.get("name") or "-"}（{latest.get("code") or "-"}）',
        f'当前价：{_num(latest.get("cur_price"))}',
        f'均价：{_num(summary.get("avg_price"))}',
        f'昨收：{_num(summary.get("last_close"))}',
        f'成交量：{_num(summary.get("volume"))}',
    ]
    try:
        cur = latest.get('cur_price')
        avg = summary.get('avg_price')
        if cur is not None and avg is not None:
            lines.append('观察：现价高于均价，分时相对偏强。' if float(cur) >= float(avg) else '观察：现价低于均价，分时相对偏弱。')
    except Exception:
        pass
    return '\n'.join(lines)


def format_kline(summary: Dict[str, Any], detail: bool = False) -> str:
    latest = summary.get('latest') or {}
    title_name = latest.get('name') or summary.get('name') or '-'
    title_code = latest.get('code') or summary.get('symbol') or '-'
    if detail and summary.get('items'):
        shown = summary.get('items', [])[-DETAIL_LIMIT:]
        lines = [f'标的：{title_name}（{title_code}）', 'K线明细：']
        for i, x in enumerate(shown, 1):
            lines.append(
                f'{i}）{x.get("time_key") or "-"}｜开{_num(x.get("open"))} / 高{_num(x.get("high"))} / 低{_num(x.get("low"))} / 收{_num(x.get("close"))}'
            )
        if len(summary.get('items', [])) > DETAIL_LIMIT:
            lines.append(f'说明：仅展示最近 {DETAIL_LIMIT} 条K线记录。')
        if summary.get('highest') is not None or summary.get('lowest') is not None:
            lines.append(f'区间收盘高低：{_num(summary.get("highest"))} / {_num(summary.get("lowest"))}')
        return '\n'.join(lines)

    lines = [
        f'标的：{title_name}（{title_code}）',
        f'最新K线：开{_num(latest.get("open"))} / 高{_num(latest.get("high"))} / 低{_num(latest.get("low"))} / 收{_num(latest.get("close"))}',
        f'成交量/成交额：{_num(latest.get("volume"))} / {_num(latest.get("turnover"))}',
    ]
    try:
        o = latest.get('open')
        c = latest.get('close')
        if o is not None and c is not None:
            lines.append('观察：这根K线收涨。' if float(c) >= float(o) else '观察：这根K线收跌。')
    except Exception:
        pass
    return '\n'.join(lines)


def format_orderbook(summary: Dict[str, Any]) -> str:
    bid = summary.get('best_bid') or {}
    ask = summary.get('best_ask') or {}
    lines = [
        f'标的：{summary.get("name") or "-"}（{summary.get("symbol") or "-"}）',
        f'买一：{_num(bid.get("price"))} / {_num(bid.get("quantity"))}',
        f'卖一：{_num(ask.get("price"))} / {_num(ask.get("quantity"))}',
        f'档位：买{_safe(summary.get("bid_levels"))}档 / 卖{_safe(summary.get("ask_levels"))}档',
    ]
    try:
        bq = bid.get('quantity')
        aq = ask.get('quantity')
        if bq is not None and aq is not None:
            lines.append('观察：买一量不弱于卖一量。' if float(bq) >= float(aq) else '观察：卖一量高于买一量，上方抛压更明显。')
    except Exception:
        pass
    return '\n'.join(lines)


def format_ticker(summary: Dict[str, Any], detail: bool = False) -> str:
    items = summary.get('items') or []
    latest = summary.get('latest') or {}
    if not items:
        return '暂无逐笔成交数据'
    lines = [f'标的：{latest.get("name") or "-"}（{latest.get("code") or "-"}）', f'逐笔成交：共 {summary.get("count") or 0} 条']
    shown = items if detail else items[:10]
    for i, x in enumerate(shown, 1):
        lines.append(f'{i}）{x.get("time") or "-"}｜价格{_num(x.get("price"))}｜成交量{_num(x.get("volume"))}｜方向{x.get("ticker_direction") or "-"}')
    return '\n'.join(lines)


def format_broker_queue(summary: Dict[str, Any]) -> str:
    lines = [
        f'标的：{summary.get("name") or "-"}（{summary.get("symbol") or "-"}）',
        f'经纪队列：买盘{_safe(summary.get("bid_count"))}条 / 卖盘{_safe(summary.get("ask_count"))}条',
    ]
    bid_items = summary.get('bid_items') or []
    ask_items = summary.get('ask_items') or []
    if bid_items:
        lines.append('买盘前列：')
        for x in bid_items[:5]:
            lines.append(f'- {x.get("bid_broker_name") or x.get("bid_broker_id") or "-"}（位置{x.get("bid_broker_pos") or "-"}）')
    if ask_items:
        lines.append('卖盘前列：')
        for x in ask_items[:5]:
            lines.append(f'- {x.get("ask_broker_name") or x.get("ask_broker_id") or "-"}（位置{x.get("ask_broker_pos") or "-"}）')
    return '\n'.join(lines)


def format_trading_days(summary: Dict[str, Any]) -> str:
    first = summary.get('first') or {}
    last = summary.get('last') or {}
    return '\n'.join([
        '交易日历：',
        f'区间起止：{first.get("date") or "-"} ~ {last.get("date") or "-"}',
        f'交易日：{_safe(summary.get("trading_days"))} 天',
        f'非交易日：{_safe(summary.get("non_trading_days"))} 天',
    ])


def format_clarification(name: str, choices: list[dict]) -> str:
    lines = [f'“{name}”同时存在港股和美股，请先确认你要查哪个市场：']
    for idx, item in enumerate(choices, 1):
        lines.append(f'{idx}. {item.get("label")}（{item.get("symbol")}）')
    lines.append('你直接回复“港股”或“美股”就行。')
    return '\n'.join(lines)


def format_capital_flow(summary: Dict[str, Any], detail: bool = False) -> str:
    latest = summary.get('latest') or {}
    if detail and summary.get('items'):
        shown = summary.get('items', [])[-DETAIL_LIMIT:]
        lines = ['资金流向（逐条）：']
        for i, x in enumerate(shown, 1):
            lines.extend([
                f'{i}）净流入：{_num(x.get("in_flow"))}',
                f'  - 特大单：{_num(x.get("super_in_flow"))}',
                f'  - 大单：{_num(x.get("big_in_flow"))}',
                f'  - 中单：{_num(x.get("mid_in_flow"))}',
                f'  - 小单：{_num(x.get("sml_in_flow"))}',
            ])
        if len(summary.get('items', [])) > DETAIL_LIMIT:
            lines.append(f'说明：仅展示最近 {DETAIL_LIMIT} 条资金流向记录。')
        if summary.get('has_trimmed_zero_tail'):
            lines.append('说明：已自动忽略尾部 0 值占位记录。')
        return '\n'.join(lines)

    lines = [
        '资金流向：',
        f'整体净流入：{_num(latest.get("in_flow"))}',
        f'特大单净流入：{_num(latest.get("super_in_flow"))}',
        f'大单净流入：{_num(latest.get("big_in_flow"))}',
        f'中单净流入：{_num(latest.get("mid_in_flow"))}',
        f'小单净流入：{_num(latest.get("sml_in_flow"))}',
    ]
    try:
        total = latest.get('in_flow')
        if total is not None:
            lines.append('观察：整体呈净流入。' if float(total) >= 0 else '观察：整体呈净流出。')
    except Exception:
        pass
    if summary.get('has_trimmed_zero_tail'):
        lines.append('说明：已自动忽略尾部 0 值占位记录。')
    return '\n'.join(lines)


def format_basicinfo(summary_list: List[Dict[str, Any]]) -> str:
    if not summary_list:
        return '暂无基础信息'
    x = summary_list[0]
    return '\n'.join([
        f'标的：{x.get("name") or "-"}（{x.get("symbol") or "-"}）',
        f'上市日期：{_safe(x.get("listing_date"))}',
        f'每手股数：{_safe(x.get("lot_size"))}',
        f'是否退市：{_safe(x.get("delisting"))}',
    ])


def format_us_analysis(summary: Dict[str, Any]) -> str:
    target = summary.get('target_price') or {}
    rating = summary.get('rating') or {}
    lines = [
        '美股分析：',
        f'分析师平均评级：{_safe(rating.get("average_rating"))}',
        f'分析师数量：{_safe(rating.get("analyst_count"))}',
        f'目标价区间：低 {_num(target.get("low"))} / 均 {_num(target.get("mean"))} / 高 {_num(target.get("high"))}',
        f'最新价：{_num(target.get("last_price"))}',
    ]
    week = rating.get('one_week_ago') or {}
    if week:
        lines.append(
            '近一周评级分布：强买入 {strongBuy} / 买入 {buy} / 持有 {hold} / 卖出 {sell} / 强卖出 {strongSell}'.format(
                strongBuy=week.get('strongBuy', '-'),
                buy=week.get('buy', '-'),
                hold=week.get('hold', '-'),
                sell=week.get('sell', '-'),
                strongSell=week.get('strongSell', '-'),
            )
        )
    return '\n'.join(lines)


def format_rank(summary: Dict[str, Any]) -> str:
    items = summary.get('items') or []
    if not items:
        return '暂无排行榜数据'
    field = summary.get('rank_field_label') or summary.get('rank_field') or '指标'
    direction = '升序' if summary.get('ascend') else '降序'
    lines = [f'排行榜：按{field}{direction}，共返回 {summary.get("count") or 0} 条']
    for i, x in enumerate(items[:10], 1):
        lines.append(
            f'{i}）{x.get("name") or "-"}（{x.get("symbol") or "-"}）｜最新价{_num(x.get("last_price"))}｜涨跌幅{_num(x.get("change_pct"))}%'
        )
    return '\n'.join(lines)


def format_ipo_list(summary: Dict[str, Any]) -> str:
    items = summary.get('items') or []
    if not items:
        return '暂无 IPO 列表数据'
    lines = [f'IPO 列表：共返回 {summary.get("count") or 0} 条']
    for i, x in enumerate(items[:10], 1):
        lines.append(
            f'{i}）{x.get("name") or "-"}（{x.get("symbol") or "-"}）｜上市日期{_safe(x.get("listing_date"))}｜发行价{_num(x.get("issue_price"))}｜每手{_safe(x.get("lot_size"))}'
        )
    return '\n'.join(lines)


def format_financial(summary: Dict[str, Any]) -> str:
    market = summary.get('market')
    if market == 'HK':
        return '\n'.join([
            '港股财务数据：',
            f'报告期：{_safe(summary.get("report_end"))}',
            f'基本每股收益：{_num(summary.get("eps"))}',
            f'每股净资产：{_num(summary.get("bps"))}',
            f'ROE（加权）：{_num(summary.get("roe"))}',
            f'毛利率：{_num(summary.get("gross_margin"))}%',
            f'净利率：{_num(summary.get("net_margin"))}%',
            f'资产负债率：{_num(summary.get("debt_ratio"))}%',
            f'营业收入同比：{_num(summary.get("revenue_growth_yoy"))}%',
            f'净利润同比：{_num(summary.get("net_profit_growth_yoy"))}%',
        ])
    return '\n'.join([
        '美股财务数据：',
        f'报告期：{_safe(summary.get("report_end"))}',
        f'币种：{_safe(summary.get("currency"))}',
        f'基本每股收益：{_num(summary.get("eps"))}',
        f'每股净资产：{_num(summary.get("bps"))}',
        f'每股经营现金流：{_num(summary.get("operating_cashflow_per_share"))}',
        f'每股营业收入：{_num(summary.get("operating_income_per_share"))}',
        f'每股股息：{_num(summary.get("dividend_per_share"))}',
        f'基本每股收益同比：{_num(summary.get("yoy_growth_in_basic_eps"))}%',
    ])


def format_shareholder_inc_red_hold(summary: Dict[str, Any]) -> str:
    items = summary.get('items') or []
    if not items:
        return '暂无股东增减持数据'
    lines = [f'股东增减持：共返回 {summary.get("count") or 0} 条']
    for i, x in enumerate(items[:10], 1):
        lines.append(
            f'{i}）{x.get("holder_name") or "-"}｜{x.get("sec_name") or "-"}（{x.get("symbol") or "-"}）｜日期{x.get("event_date") or "-"}｜变动股数{_num(x.get("shares_traded"))}｜变动金额{_num(x.get("changed_amount"))}'
        )
    return '\n'.join(lines)



def format_wealth_balance_list(summary: Dict[str, Any]) -> str:
    items = summary.get('items') or []
    if not items:
        return '暂无余额列表数据'
    lines = [
        f'余额列表：共 {summary.get("count") or 0} 个币种',
        f'账户现金总额：{_num(summary.get("total_cash_balance_amount"))}',
    ]
    for i, x in enumerate(items[:10], 1):
        lines.append(f'{i}）币种{x.get("currency") or "-"}｜现金余额{_num(x.get("cash_balance_amount"))}｜总余额{_num(x.get("balance_amount"))}｜冻结{_num(x.get("cash_frozen_amount"))}')
    return '\n'.join(lines)



def format_wealth_cash_total_asset(summary: Dict[str, Any]) -> str:
    items = summary.get('items') or []
    if not items:
        return '暂无现金类资产数据'
    lines = [f'现金类资产：共 {summary.get("count") or 0} 个币种（以下为各币种资产，未做汇率换算）']
    for i, x in enumerate(items[:10], 1):
        lines.append(f'{i}）币种{x.get("currency") or "-"}｜总资产{_num(x.get("total_asset"))}｜当日收益{_num(x.get("day_profit"))}｜累计收益{_num(x.get("total_asset_profit"))}｜待确认{_num(x.get("total_confirming_amount"))}｜冻结{_num(x.get("total_freeze_amount"))}')
    return '\n'.join(lines)


def format_wealth_fixed_income(summary: Dict[str, Any]) -> str:
    lines = [
        '固收资产汇总：',
        f'目标币种：{summary.get("currency") or "-"}',
        f'总资产：{_num(summary.get("total_asset"))}',
        f'待确认金额：{_num(summary.get("total_confirming_amount"))}',
        f'持有收益：{_num(summary.get("total_holding_profit"))}',
        f'累计收益：{_num(summary.get("total_profit"))}',
        f'在途交易笔数：{_num(summary.get("total_transaction_count"))}',
        f'产品类型/币种分组数：{_num(summary.get("group_count"))}',
    ]
    return '\n'.join(lines)


def format_wealth_private_contract_asset_list(summary: Dict[str, Any]) -> str:
    items = summary.get('items') or []
    if not items:
        return '暂无私募资产数据'
    lines = [
        f'私募资产：共 {summary.get("total_contract_count") or summary.get("count") or 0} 个合同（接口汇总币种：{summary.get("currency") or "-"}）',
        f'总资产：{_num(summary.get("total_asset"))}',
        f'已确认资产：{_num(summary.get("total_confirmed_asset"))}',
        f'累计投入：{_num(summary.get("total_input_amount"))}',
        f'累计浮盈亏：{_num(summary.get("total_float_profit"))}',
    ]
    for i, x in enumerate(items[:10], 1):
        lines.append(f'{i}）{x.get("product_name") or "-"}｜类别{x.get("asset_class_desc") or "-"}｜币种{x.get("currency") or "-"}｜资产{_num(x.get("asset"))}｜确认资产{_num(x.get("confirmed_asset"))}｜浮盈亏{_num(x.get("float_profit"))}')
    return '\n'.join(lines)


def format_wealth_total_asset(summary: Dict[str, Any]) -> str:
    return '\n'.join([
        '总资产（接口汇总口径）：',
        f'汇总币种：{summary.get("currency") or "-"}',
        f'总资产：{_num(summary.get("total_asset"))}',
        f'现金资产：{_num(summary.get("cash_asset"))}',
        f'公募基金资产：{_num(summary.get("fund_asset"))}',
        f'私募资产：{_num(summary.get("private_asset"))}',
        f'银行定存资产：{_num(summary.get("bank_deposit_asset"))}',
        f'票据/结构化资产：{_num(summary.get("note_asset"))}',
        f'持仓金额：{_num(summary.get("hold_total_holding_amount"))}',
        f'持仓收益：{_num(summary.get("hold_total_holding_profit"))}',
        f'待确认金额：{_num(summary.get("hold_total_confirming_amount"))}',
        f'冻结金额：{_num(summary.get("hold_total_freeze_amount"))}',
        '说明：以上汇总值来自接口返回口径。',
    ])


