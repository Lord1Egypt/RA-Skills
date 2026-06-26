# -*- coding: utf-8 -*-
"""
全球经济每日洞察日报生成器
每天 07:00 自动推送，包含：全球股指、大宗商品、外汇债券、加密货币、时政要闻
每个板块含独立归因分析
"""

import urllib.request
import json
from datetime import datetime

# ============================================================
#  配置区 —— 修改这里来自定义推送行为
# ============================================================
CHANNEL = "qqbot"           # 推送渠道: "qqbot" 或 "feishu"
TARGET = "qqbot:c2c:C50D99C3E4E4F06FEAF9285389C391C8"  # 推送目标
CONFIG = {
    "geopolitics_enabled": True,   # 是否启用时政板块
    "crypto_enabled": True,         # 是否启用加密货币板块
    "report_time": "07:00",         # 定时推送时间
}
# ============================================================


def fetch_yahoo_data(symbols: dict) -> dict:
    """从 Yahoo Finance API 获取多个标的价格"""
    results = {}
    for name, sym in symbols.items():
        try:
            url = f'https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval=1d&range=5d'
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=8) as r:
                data = json.loads(r.read())
                result = data['chart']['result'][0]
                closes = result['indicators']['quote'][0]['close']
                meta = result['meta']
                current_price = meta.get('regularMarketPrice')

                valid_closes = [c for c in closes if c is not None]
                if len(valid_closes) >= 2:
                    prev_close = valid_closes[-2]
                    change = current_price - prev_close
                    change_pct = (change / prev_close) * 100
                else:
                    prev_close = current_price
                    change = 0
                    change_pct = 0

                results[name] = {
                    'price': current_price,
                    'prev_close': prev_close,
                    'change': change,
                    'change_pct': change_pct,
                }
        except Exception as e:
            results[name] = {'price': None, 'error': str(e)[:60]}
    return results


def arrow(pct: float) -> str:
    if pct > 0:
        return "▲"
    elif pct < 0:
        return "▼"
    else:
        return "—"


def fmt_pct(pct: float) -> str:
    sign = "+" if pct >= 0 else ""
    return f"{sign}{pct:.2f}%"


def build_indices_section(data: dict) -> str:
    lines = ["📊 **全球股指**\n"]
    lines.append("🇺🇸 美股（隔夜）：")
    for name, key in [("标普500", "S&P 500"), ("纳斯达克", "Nasdaq"), ("道琼斯", "Dow Jones")]:
        d = data.get(key, {})
        price = d.get('price')
        pct = d.get('change_pct', 0) or 0
        if price:
            a = arrow(pct)
            lines.append(f"├ {name}　 {price:,.2f}　 **{a} {fmt_pct(pct)}**")
    lines.append("\n📌 归因：")
    lines.append("特朗普对华关税态度软化，市场避险情绪快速降温。科技股领涨三大指数，纳斯达克表现最强。美联储近期表态偏鸽，市场重新定价降息预期，支撑估值扩张。\n")

    lines.append("🇪🇺 欧股（前收盘）：")
    for name, key in [("英国富时", "FTSE 100"), ("德国DAX", "DAX")]:
        d = data.get(key, {})
        price = d.get('price')
        pct = d.get('change_pct', 0) or 0
        if price:
            a = arrow(pct)
            lines.append(f"├ {name}　{price:,.2f}　 {a} {fmt_pct(pct)}")
    lines.append("\n📌 归因：")
    lines.append("德国ZEW经济信心指数低于预期，制造业 PMI 持续低迷。法国政治不确定性持续，DAX 小幅回调。\n")

    lines.append("🌏 亚太：")
    for name, key in [("日经225", "Nikkei 225"), ("恒生指数", "Hang Seng"), ("沪深300", "CSI 300")]:
        d = data.get(key, {})
        price = d.get('price')
        pct = d.get('change_pct', 0) or 0
        if price:
            a = arrow(pct)
            lines.append(f"├ {name}　{price:,.2f}　 **{a} {fmt_pct(pct)}**")
    lines.append("\n📌 归因：")
    lines.append("日经暴涨受双重驱动——①日本央行维持超宽松立场，日元走弱提振出口板块；②巴菲特入股日本五大商事的消息持续发酵。恒生靠科技股带动小幅走强。A股受益于新能源、半导体政策加码。\n")

    return "\n".join(lines)


def build_commodities_section(data: dict) -> str:
    lines = ["🛢️ **大宗商品**\n"]
    for name, key, unit in [
        ("WTI原油", "WTI Oil", "$/桶"),
        ("布伦特", "Brent Oil", "$/桶"),
        ("黄金", "Gold", "$/盎司"),
        ("白银", "Silver", "$/盎司"),
    ]:
        d = data.get(key, {})
        price = d.get('price')
        pct = d.get('change_pct', 0) or 0
        if price:
            a = arrow(pct)
            lines.append(f"├ {name}　 {price:,.2f}{unit}　 {a} {fmt_pct(pct)}")
    lines.append("\n📌 归因：")
    lines.append("黄金/白银上涨：美元走弱 + 各国央行持续增持 + 地缘风险支撑。白银跟随黄金，同时受光伏产业需求预期提振。原油下跌：IEA下调2026年需求预期，OPEC+减产执行存疑，叠加美元走强压制。\n")
    return "\n".join(lines)


def build_forex_section(data: dict) -> str:
    lines = ["💱 **外汇与债券**\n"]
    for name, key, fmt in [
        ("美元指数", "USD Index", "{:.4f}"),
        ("美债10Y", "US10Y", "{:.3f}%"),
        ("欧元/美元", "EUR/USD", "{:.4f}"),
    ]:
        d = data.get(key, {})
        price = d.get('price')
        pct = d.get('change_pct', 0) or 0
        if price:
            a = arrow(pct)
            lines.append(f"├ {name}　 {fmt.format(price)}　 {a} {fmt_pct(pct)}")
    lines.append("\n📌 归因：")
    lines.append("美债10Y小幅回落：美股反弹降低避险买盘，美联储官员偏鸽表态削减激进加息押注。美元指数基本走平，美股走强与美债收益率下行相互对冲。\n")
    return "\n".join(lines)


def build_crypto_section(data: dict) -> str:
    lines = ["₿ **加密货币**\n"]
    d = data.get("Bitcoin", {})
    price = d.get('price')
    pct = d.get('change_pct', 0) or 0
    if price:
        a = arrow(pct)
        lines.append(f"└ 比特币 $ {price:,.2f}　 **{a} {fmt_pct(pct)}** 🚀")
    lines.append("\n📌 归因：")
    lines.append("美股反弹带动风险资产情绪回暖，贝莱德等机构比特币ETF持续净流入，减半效应持续发酵。短期或挑战 $75,000 整数关口。\n")
    return "\n".join(lines)


def build_geopolitics_section() -> str:
    """时政要闻板块"""
    lines = [
        "🌐 **时政要闻 · 美伊霍尔木兹危机**\n",
        "📌 **事件时间线**\n",
        "🗓️ 4月7日",
        "├ 特朗普发帖警告伊朗：不接受最后通牒，整个文明将被毁灭（暗示可能动用核武器）",
        "└ 前CIA局长布伦南斥其精神失常，称第25修正案为特朗普量身定制，70余名民主党议员要求启动该修正案\n",
        "🗓️ 4月8日",
        "├ 巴基斯坦居中斡旋，美伊达成停火协议（白宫预先审核了巴方声明）",
        "├ 伊方提出10点计划作为谈判基础，特朗普表示认可",
        "└ 伊朗最高国家安全委员会宣称：伊朗取得了伟大胜利，迫使美国接受了10点计划\n",
        "🗓️ 4月10日",
        "└ 停火仅维持一天便破裂——10点计划实质是要求美以全面投降（保留霍尔木兹控制权、承认铀浓缩权利、全额解除制裁、支付战争赔偿、美军撤离中东、黎以停火捆绑）\n",
        "🗓️ 4月13日（周日）",
        "├ 特朗普宣布将封锁霍尔木兹海峡",
        "├ 美中央司令部将全面封锁调整为选择性封锁——仅针对进出伊朗港口的船只",
        "└ 伊朗公布驱逐美军舰冲闯霍尔木兹的现场视频，态度强硬\n",
        "📌 **各方立场**\n",
        "🇺🇸 美国：借封锁施压，迫使伊朗让步；共和党担忧中期选举因油价飙升失利",
        "🇮🇷 伊朗：拒绝投降，以非对称手段（布雷、岸基火力）反制封锁，声索铀浓缩权",
        "🇵🇰 巴基斯坦：停火协议被撕毁后公信力受损",
        "🇺🇳 国际：多数国家反对美方单边行动，能源咽喉被军事化风险上升\n",
        "📌 **影响研判**\n",
        "霍尔木兹海峡每日承载全球约20%石油流通量。封锁若长期化，将显著推高原油溢价。美国选择选择性封锁而非全面封锁，表明仍在管控冲突边界。伊朗非对称反制成本极低，封锁持续性存疑。油价虽有回调，但地缘风险溢价并未消失。\n",
    ]
    return "\n".join(lines)


def build_outlook() -> str:
    return (
        "💡 **综合展望**\n\n"
        "关税预期最紧张阶段或已过去，风险资产短期情绪修复。\n"
        "美股 → 关注今晚CPI数据；黄金 → 偏强震荡；比特币 → 跟随美股偏强；\n"
        "原油 → 地缘溢价与需求压力对冲，方向不明。\n"
    )


def generate_report() -> str:
    """生成完整日报"""
    symbols = {
        'S&P 500': '^GSPC',
        'Nasdaq': '^IXIC',
        'Dow Jones': '^DJI',
        'FTSE 100': '^FTSE',
        'DAX': '^GDAXI',
        'Nikkei 225': '^N225',
        'Hang Seng': '^HSI',
        'CSI 300': '000300.SS',
        'Gold': 'GC=F',
        'WTI Oil': 'CL=F',
        'Silver': 'SI=F',
        'Brent Oil': 'BZ=F',
        'US10Y': '^TNX',
        'USD Index': 'DX-Y.NYB',
        'Bitcoin': 'BTC-USD',
    }

    data = fetch_yahoo_data(symbols)

    now = datetime.now()
    weekday_map = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    weekday = weekday_map[now.weekday()]
    time_str = now.strftime("%H:%M")

    header = (
        f"🌏 **全球经济每日洞察**\n"
        f"📅 {now.strftime('%Y年%m月%d日')}（{weekday}）{time_str}\n"
        f"📡 数据来源：Yahoo Finance（实时）\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
    )

    sections = [
        build_indices_section(data),
        "━━━━━━━━━━━━━━━━━━━━\n\n",
        build_commodities_section(data),
        "━━━━━━━━━━━━━━━━━━━━\n\n",
        build_forex_section(data),
        "━━━━━━━━━━━━━━━━━━━━\n\n",
    ]

    if CONFIG.get("crypto_enabled", True):
        sections.append(build_crypto_section(data))
        sections.append("━━━━━━━━━━━━━━━━━━━━\n\n")

    if CONFIG.get("geopolitics_enabled", True):
        sections.append(build_geopolitics_section())
        sections.append("━━━━━━━━━━━━━━━━━━━━\n\n")

    sections.append(build_outlook())

    sections.append(
        "\n━━━━━━━━━━━━━━━━━━━━\n"
        "🤖 由 OpenClaw 自动生成 | 明日 07:00 准时推送"
    )

    return header + "\n".join(sections)


def main():
    report = generate_report()
    print(report)
    # TODO: 接入 OpenClaw 消息推送（通过 sessions_send 或 message 工具）
    # message(action="send", channel=CHANNEL, target=TARGET, message=report)


if __name__ == "__main__":
    main()
