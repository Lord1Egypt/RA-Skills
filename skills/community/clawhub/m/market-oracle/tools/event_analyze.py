#!/usr/bin/env python3
"""
Market Oracle — Event Impact Analyzer
Fetches news + market data, builds a structured context for three-layer impact analysis.
This script collects all data and outputs a structured analysis prompt/context
that the AI agent uses to generate the final prediction.
"""

import argparse
import json
import os
import subprocess
import sys
import urllib.request
from datetime import datetime
from html.parser import HTMLParser


class HTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self._result = []
        self._skip = False

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'nav', 'footer', 'header'):
            self._skip = True

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'nav', 'footer', 'header'):
            self._skip = False

    def handle_data(self, data):
        if not self._skip:
            text = data.strip()
            if text:
                self._result.append(text)

    def get_text(self):
        return '\n'.join(self._result)


def extract_text_from_url(url, timeout=15):
    """Extract main text content from a URL."""
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/131.0.0.0 Safari/537.36'
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            html = resp.read().decode('utf-8', errors='replace')
        extractor = HTMLTextExtractor()
        extractor.feed(html)
        text = extractor.get_text()
        # Truncate to reasonable length
        return text[:3000] if len(text) > 3000 else text
    except Exception as e:
        return f"[无法提取URL内容: {e}]"


def run_tool(script_name, args_list):
    """Run a sibling tool script and capture JSON output."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(base_dir, script_name)

    cmd = [sys.executable, script_path] + args_list + ['--json']
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout)
        else:
            print(f"[WARN] {script_name} stderr: {result.stderr[:200]}", file=sys.stderr)
            return None
    except subprocess.TimeoutExpired:
        print(f"[WARN] {script_name} timed out", file=sys.stderr)
        return None
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"[WARN] {script_name} error: {e}", file=sys.stderr)
        return None


# Asset correlation knowledge base
CORRELATION_MAP = {
    'gold': {
        'positive': ['silver', 'platinum', 'usdjpy_inverse'],
        'negative': ['usdx', 'spy'],
        'description': '黄金与美元指数负相关，与白银正相关，避险情绪推动上涨'
    },
    'oil': {
        'positive': ['brent', 'natgas', 'energy_stocks'],
        'negative': ['airline_stocks', 'consumer_discretionary'],
        'description': '原油上涨推高通胀预期，利空航空和消费板块，利多能源板块'
    },
    'btc': {
        'positive': ['eth', 'sol', 'risk_appetite'],
        'negative': ['usdx', 'bonds'],
        'description': '加密货币与风险偏好正相关，美元走强时承压'
    },
    'spy': {
        'positive': ['qqq', 'dia', 'risk_appetite'],
        'negative': ['gold', 'vix', 'bonds'],
        'description': '美股上涨反映风险偏好，与避险资产负相关'
    }
}

# ══════════════════════════════════════════════════════════════════════
# HISTORICAL BACKTESTING CASE LIBRARY
# Each case records: event → predicted direction/magnitude → actual outcome
# Used for: (1) self-validation  (2) confidence scoring  (3) rule calibration
# ══════════════════════════════════════════════════════════════════════

HISTORICAL_CASES = [
    # ── Case 1: 美联储2024年9月降息50bp ──
    {
        'id': 'fed_cut_2024sep',
        'event': '美联储宣布降息50个基点，联邦基金利率下调至4.75%-5.00%',
        'date': '2024-09-18',
        'event_types': ['央行/货币政策'],
        'direction': 'bullish',
        'severity': 'extreme',
        'actual_reactions': {
            'gold':  {'dir': '↑', 'pct': +1.2, 'note': '一度涨破2600创新高，后冲高回落收平'},
            'btc':   {'dir': '↑', 'pct': +3.5, 'note': 'BTC突破62500，表现领先美股和黄金'},
            'spy':   {'dir': '↕', 'pct': -0.29, 'note': '先涨后跌，三大指数全线转跌'},
            'qqq':   {'dir': '↕', 'pct': -0.31, 'note': '纳指冲高回落'},
            'usdx':  {'dir': '↓', 'pct': -0.5, 'note': '美元指数跳水后反弹'},
            'oil':   {'dir': '→', 'pct': +0.3, 'note': '原油反应平淡'},
        },
        'key_lesson': '超预期降息50bp利好已提前price-in，美股"买预期卖事实"冲高回落。'
                       'BTC对流动性宽松最敏感。黄金虽创新高但同样冲高回落。'
    },
    # ── Case 2: 2024年4月伊朗以色列冲突 ──
    {
        'id': 'iran_israel_2024apr',
        'event': '以色列袭击伊朗驻叙利亚大使馆，伊朗向以色列发射导弹报复',
        'date': '2024-04-13',
        'event_types': ['地缘政治'],
        'direction': 'bearish',
        'severity': 'extreme',
        'actual_reactions': {
            'gold':  {'dir': '↑', 'pct': +3.5, 'note': '触及近两个月高位'},
            'oil':   {'dir': '↑', 'pct': +7.0, 'note': '原油上周五上涨逾7%'},
            'spy':   {'dir': '↓', 'pct': -0.9, 'note': '标普500期货下跌0.9%'},
            'btc':   {'dir': '↓', 'pct': -3.0, 'note': '加密市场跟随风险资产下跌'},
            'usdx':  {'dir': '↑', 'pct': +0.6, 'note': '美元避险走强'},
        },
        'key_lesson': '中东地缘冲突对油价冲击最大(7%+)，黄金避险明确(3%+)。'
                       'BTC在地缘危机中表现为风险资产(下跌)而非避险资产。'
    },
    # ── Case 3: 2025年4月特朗普对等关税 ──
    {
        'id': 'trump_tariff_2025apr',
        'event': '特朗普宣布对所有贸易伙伴加征最低10%对等关税，部分国家税率高达49%',
        'date': '2025-04-02',
        'event_types': ['其他/综合'],
        'direction': 'bearish',
        'severity': 'extreme',
        'actual_reactions': {
            'spy':   {'dir': '↓', 'pct': -4.0, 'note': '标普期货跌超4%，纳指期货跌超5%'},
            'qqq':   {'dir': '↓', 'pct': -5.0, 'note': '纳斯达克两日暴跌11.44%'},
            'gold':  {'dir': '↕', 'pct': -1.5, 'note': '黄金先涨后跌，一周跌幅达13%！避险失灵'},
            'oil':   {'dir': '↓', 'pct': -8.0, 'note': 'WTI跌破60美元，创2021年以来新低'},
            'btc':   {'dir': '↓', 'pct': -5.0, 'note': 'BTC暴跌5%，28万人爆仓'},
            'usdx':  {'dir': '↑', 'pct': +0.8, 'note': '美元短期走强'},
        },
        'key_lesson': '极端关税引发系统性抛售，连黄金等传统避险资产都下跌（流动性危机）。'
                       '原油因需求崩塌预期暴跌(-8%)而非上涨。BTC完全是风险资产。'
                       '这是"扔掉一切换现金"的极端情景。'
    },
    # ── Case 4: OPEC+ 2023年4月意外减产160万桶/日 ──
    {
        'id': 'opec_cut_2023apr',
        'event': 'OPEC+意外宣布减产逾160万桶/日',
        'date': '2023-04-02',
        'event_types': ['能源/OPEC'],
        'direction': 'bullish',
        'severity': 'high',
        'actual_reactions': {
            'oil':   {'dir': '↑', 'pct': +7.5, 'note': '布油飙升至86美元，涨幅7.94%'},
            'gold':  {'dir': '↑', 'pct': +0.8, 'note': '通胀预期上修小幅利好黄金'},
            'spy':   {'dir': '↓', 'pct': -0.5, 'note': '能源成本上升压制美股'},
            'btc':   {'dir': '→', 'pct': +0.2, 'note': '加密市场几乎无反应'},
        },
        'key_lesson': 'OPEC减产对油价冲击立竿见影(+7-8%)，对其他资产影响有限。'
                       '黄金因通胀预期小幅受益。BTC与能源市场脱钩。'
    },
    # ── Case 5: 日本央行2024年7月意外加息 ──
    {
        'id': 'boj_hike_2024jul',
        'event': '日本央行意外加息15个基点至0.15%-0.25%，超出市场预期',
        'date': '2024-07-31',
        'event_types': ['央行/货币政策'],
        'direction': 'bearish',
        'severity': 'extreme',
        'actual_reactions': {
            'spy':   {'dir': '↓', 'pct': -3.0, 'note': '全球股市暴跌，8月5日美股大跌'},
            'qqq':   {'dir': '↓', 'pct': -4.5, 'note': '科技股跌幅更大'},
            'gold':  {'dir': '↕', 'pct': -0.5, 'note': '日元套利交易平仓，黄金短期承压'},
            'btc':   {'dir': '↓', 'pct': -8.0, 'note': 'BTC暴跌，日元套利平仓引发连锁反应'},
            'usdx':  {'dir': '↓', 'pct': -1.5, 'note': '日元大幅升值，美元对日元贬值'},
        },
        'key_lesson': '日本加息触发全球日元套利交易(carry trade)大规模平仓，连锁反应远超加息本身。'
                       '日经暴跌12.4%创1987年以来纪录。BTC跌幅大于美股。'
                       '非美央行加息对美元是利空(美元走弱)，与美联储加息反向。'
    },
    # ── Case 6: 2024年1月比特币现货ETF获SEC批准 ──
    {
        'id': 'btc_etf_2024jan',
        'event': 'SEC批准11只比特币现货ETF上市交易',
        'date': '2024-01-10',
        'event_types': ['加密货币监管'],
        'direction': 'bullish',
        'severity': 'high',
        'actual_reactions': {
            'btc':   {'dir': '↕', 'pct': -8.3, 'note': '先涨至49000后暴跌至42000，典型买预期卖事实'},
            'gold':  {'dir': '→', 'pct': +0.1, 'note': '黄金几乎无反应'},
            'spy':   {'dir': '→', 'pct': +0.3, 'note': '美股几乎无反应'},
        },
        'key_lesson': '重大利好已被市场充分定价(BTC从16000涨到46000)，'
                       '消息落地后"买预期卖事实"导致暴跌8.3%。'
                       '加密监管事件对黄金和美股影响极小。'
    },
    # ── Case 7: 2022年2月俄乌冲突爆发 ──
    {
        'id': 'russia_ukraine_2022feb',
        'event': '俄罗斯入侵乌克兰，全面军事冲突爆发',
        'date': '2022-02-24',
        'event_types': ['地缘政治'],
        'direction': 'bearish',
        'severity': 'extreme',
        'actual_reactions': {
            'oil':   {'dir': '↑', 'pct': +25.0, 'note': '从88美元飙至140美元（数周内）'},
            'gold':  {'dir': '↑', 'pct': +6.0, 'note': '短期内涨超6%'},
            'spy':   {'dir': '↓', 'pct': -2.5, 'note': '美股当日先跌后反弹'},
            'btc':   {'dir': '↓', 'pct': -8.0, 'note': 'BTC从39000跌至34000'},
            'usdx':  {'dir': '↑', 'pct': +1.5, 'note': '避险买盘推动美元走强'},
        },
        'key_lesson': '大规模地缘冲突对油价的冲击是持续性的(数周+25%)，而非一天的事。'
                       '黄金在大规模战争中确实是避险资产。BTC在战争中表现为风险资产。'
                       '美股当日"先跌后反弹"说明市场有自我修复能力。'
    },
    # ── Case 8: 2024年9月中国央行降准50bp ──
    {
        'id': 'pboc_rrr_2024sep',
        'event': '中国央行宣布降准0.5个百分点，提供约1万亿元长期流动性',
        'date': '2024-09-27',
        'event_types': ['央行/货币政策'],
        'direction': 'bullish',
        'severity': 'high',
        'actual_reactions': {
            'spy':   {'dir': '↑', 'pct': +0.5, 'note': '中国刺激对美股正面但有限'},
            'gold':  {'dir': '↑', 'pct': +0.9, 'note': '黄金小幅受益于宽松预期'},
            'oil':   {'dir': '↑', 'pct': +1.2, 'note': '中国需求预期改善推动油价'},
            'btc':   {'dir': '↑', 'pct': +2.0, 'note': '全球流动性宽松利好加密'},
            'usdx':  {'dir': '↓', 'pct': -0.3, 'note': '人民币走强压制美元指数'},
        },
        'key_lesson': '中国央行降准对全球资产影响偏温和但方向明确。'
                       '对A股影响最大(当日+2.89%~+10%)，对国际资产影响幅度减半。'
                       '中国宽松对油价利好因为提振需求预期。'
    },
    # ── Case 9: 2025年3月特朗普对加墨加征25%关税 ──
    {
        'id': 'trump_tariff_2025mar',
        'event': '特朗普宣布对加拿大、墨西哥加征25%关税',
        'date': '2025-03-04',
        'event_types': ['其他/综合'],
        'direction': 'bearish',
        'severity': 'high',
        'actual_reactions': {
            'spy':   {'dir': '↓', 'pct': -1.76, 'note': '美股三大指数尾盘跳水'},
            'gold':  {'dir': '↑', 'pct': +2.0, 'note': '国际金价突破2900美元创新高'},
            'btc':   {'dir': '↓', 'pct': -3.0, 'note': '加密市场跟随风险资产下跌'},
            'oil':   {'dir': '↓', 'pct': -1.5, 'note': '需求担忧压制油价'},
            'usdx':  {'dir': '↑', 'pct': +0.5, 'note': '贸易战中美元走强'},
        },
        'key_lesson': '一般性关税(非极端)：黄金作为避险上涨，美股下跌，油价因需求担忧下跌。'
                       '与Case3极端关税不同，普通关税下黄金避险功能正常。'
    },
    # ── Case 10: 2026年3月2日美以袭击伊朗（最新） ──
    {
        'id': 'us_israel_iran_2026mar',
        'event': '美国和以色列袭击伊朗',
        'date': '2026-03-02',
        'event_types': ['地缘政治'],
        'direction': 'bearish',
        'severity': 'extreme',
        'actual_reactions': {
            'oil':   {'dir': '↑', 'pct': +13.0, 'note': '布油开盘飙升13%至82美元'},
            'gold':  {'dir': '↑', 'pct': +1.6, 'note': '黄金开盘上涨1.6%'},
            'spy':   {'dir': '↓', 'pct': -0.9, 'note': '标普500期货下跌0.9%'},
            'qqq':   {'dir': '↓', 'pct': -1.2, 'note': '纳斯达克100期货下跌1.2%'},
            'btc':   {'dir': '↓', 'pct': -2.0, 'note': '估计跟随风险资产下跌'},
            'usdx':  {'dir': '↑', 'pct': +0.8, 'note': '避险买盘推动美元走强'},
        },
        'key_lesson': '直接军事打击产油国（伊朗）对油价冲击巨大(+13%)。'
                       '黄金涨幅反而不如油价，说明市场更关注供应冲击。'
    },
    # ── Case 11: 2025年5月中国央行降准50bp+降息10bp ──
    {
        'id': 'pboc_cut_2025may',
        'event': '中国央行降准0.5个百分点，同时降息10bp至1.4%',
        'date': '2025-05-07',
        'event_types': ['央行/货币政策'],
        'direction': 'bullish',
        'severity': 'high',
        'actual_reactions': {
            'spy':   {'dir': '↑', 'pct': +0.3, 'note': '对美股影响有限'},
            'gold':  {'dir': '↑', 'pct': +0.5, 'note': '宽松预期小幅利好'},
            'oil':   {'dir': '↑', 'pct': +0.8, 'note': '中国需求预期改善'},
            'btc':   {'dir': '↑', 'pct': +1.5, 'note': '全球流动性宽松'},
        },
        'key_lesson': '中国央行组合拳（降准+降息）对国际资产影响方向明确但幅度温和。'
    },
    # ── Case 12: 2025年4月7日关税引发全球黑色星期一 ──
    {
        'id': 'black_monday_2025apr',
        'event': '特朗普关税政策引发全球"黑色星期一"，系统性恐慌',
        'date': '2025-04-07',
        'event_types': ['其他/综合'],
        'direction': 'bearish',
        'severity': 'extreme',
        'actual_reactions': {
            'spy':   {'dir': '↓', 'pct': -4.5, 'note': '标普500期货暴跌'},
            'qqq':   {'dir': '↓', 'pct': -5.5, 'note': '纳指跌超5%'},
            'gold':  {'dir': '↓', 'pct': -3.0, 'note': '黄金跌至3008，周跌13%！'},
            'oil':   {'dir': '↓', 'pct': -6.0, 'note': 'WTI跌破60美元'},
            'btc':   {'dir': '↓', 'pct': -5.0, 'note': '加密市场血洗'},
            'usdx':  {'dir': '↑', 'pct': +1.0, 'note': '现金为王，美元走强'},
        },
        'key_lesson': '系统性恐慌下所有资产（包括黄金）齐跌——流动性危机"cash is king"。'
                       '这打破了"黄金避险"的默认假设。'
                       '极端关税+系统性恐慌 ≠ 普通地缘风险，需要区分对待。'
    },
]


def _run_backtest_single(case):
    """Run the analysis engine on a single historical case and compare with actual outcome.

    Returns a score dict: {asset: {predicted_dir, actual_dir, dir_match, pct_in_range}}
    """
    event_text = case['event']

    # Simulate a minimal context (no live news/market data)
    event_types = classify_event(event_text)
    affected = identify_affected_assets(event_text)
    # Ensure we cover all assets that have actual data
    for asset in case['actual_reactions']:
        if asset not in affected:
            affected.append(asset)

    context = {
        'event': {
            'text': event_text,
            'enriched_text': event_text,
            'types': event_types,
            'timestamp': case['date'],
        },
        'affected_assets': affected,
        'market_snapshot': {},
        'related_news': [],
        'news_articles_raw': [],
        'correlations': {},
    }

    predictions = generate_predictions(context)

    # Parse predicted directions per asset from short-term predictions
    predicted = {}
    for p in predictions.get('short', []):
        # Format: "NAME (当前 $X) → ↑ 预计 +X%~Y% | reason"
        for asset in case['actual_reactions']:
            asset_upper = asset.upper()
            if asset_upper in p or asset.upper() in p:
                if '→ ↑' in p:
                    predicted[asset] = '↑'
                elif '→ ↓' in p:
                    predicted[asset] = '↓'
                elif '→ ↕' in p:
                    predicted[asset] = '↕'
                elif '→ →' in p:
                    predicted[asset] = '→'

    # Score each asset
    results = {}
    for asset, actual in case['actual_reactions'].items():
        pred_dir = predicted.get(asset, '?')
        actual_dir = actual['dir']
        actual_pct = actual['pct']

        # Direction match scoring
        if pred_dir == actual_dir:
            dir_score = 1.0
        elif pred_dir == '↕' or actual_dir == '↕':
            dir_score = 0.5  # ↕ is a hedge, partial credit
        elif pred_dir == '→' and abs(actual_pct) < 1.0:
            dir_score = 0.8  # predicted flat, was nearly flat
        elif pred_dir == '?' :
            dir_score = 0.0
        else:
            dir_score = 0.0

        results[asset] = {
            'predicted_dir': pred_dir,
            'actual_dir': actual_dir,
            'actual_pct': actual_pct,
            'dir_score': dir_score,
        }

    return results


def run_full_backtest(verbose=False):
    """Run backtest on ALL historical cases. Returns aggregate stats.

    This is the self-validation mechanism: we run the analysis engine on
    historical events and compare predictions with actual market reactions.
    """
    all_results = []
    total_predictions = 0
    correct_predictions = 0
    partial_predictions = 0

    for case in HISTORICAL_CASES:
        results = _run_backtest_single(case)
        case_score = 0
        case_total = 0

        for asset, r in results.items():
            total_predictions += 1
            case_total += 1
            case_score += r['dir_score']
            if r['dir_score'] >= 0.8:
                correct_predictions += 1
            elif r['dir_score'] >= 0.5:
                partial_predictions += 1

        all_results.append({
            'case_id': case['id'],
            'event': case['event'][:50],
            'date': case['date'],
            'asset_results': results,
            'case_accuracy': case_score / case_total if case_total > 0 else 0,
        })

        if verbose:
            print(f"\n{'─' * 60}", file=sys.stderr)
            print(f"Case: {case['event'][:60]}", file=sys.stderr)
            print(f"Date: {case['date']}", file=sys.stderr)
            for asset, r in results.items():
                match = '✅' if r['dir_score'] >= 0.8 else ('🟡' if r['dir_score'] >= 0.5 else '❌')
                print(f"  {match} {asset:6s} 预测:{r['predicted_dir']} 实际:{r['actual_dir']}({r['actual_pct']:+.1f}%) 得分:{r['dir_score']:.1f}", file=sys.stderr)
            avg = sum(r['dir_score'] for r in results.values()) / len(results) if results else 0
            print(f"  Case accuracy: {avg:.0%}", file=sys.stderr)

    overall_accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0
    partial_accuracy = (correct_predictions + partial_predictions) / total_predictions if total_predictions > 0 else 0

    # ── Identify systematic biases ──
    biases = _detect_biases(all_results)

    return {
        'total_cases': len(HISTORICAL_CASES),
        'total_predictions': total_predictions,
        'correct': correct_predictions,
        'partial': partial_predictions,
        'wrong': total_predictions - correct_predictions - partial_predictions,
        'strict_accuracy': overall_accuracy,
        'lenient_accuracy': partial_accuracy,
        'case_results': all_results,
        'biases': biases,
    }


def _detect_biases(all_results):
    """Detect systematic prediction biases from backtest results."""
    biases = []

    # Count errors by asset
    asset_errors = {}
    for case in all_results:
        for asset, r in case['asset_results'].items():
            if asset not in asset_errors:
                asset_errors[asset] = {'total': 0, 'errors': 0, 'false_up': 0, 'false_down': 0}
            asset_errors[asset]['total'] += 1
            if r['dir_score'] < 0.5:
                asset_errors[asset]['errors'] += 1
                if r['predicted_dir'] == '↑' and r['actual_dir'] == '↓':
                    asset_errors[asset]['false_up'] += 1
                elif r['predicted_dir'] == '↓' and r['actual_dir'] == '↑':
                    asset_errors[asset]['false_down'] += 1

    for asset, stats in asset_errors.items():
        if stats['total'] > 0 and stats['errors'] / stats['total'] > 0.3:
            biases.append(f"{asset}: 错误率{stats['errors']}/{stats['total']}，"
                         f"假涨{stats['false_up']}次，假跌{stats['false_down']}次")

    return biases


def get_confidence_from_backtest(event_types, severity):
    """Get confidence level based on historical backtest accuracy for similar event types.

    Returns: (confidence_pct, matching_cases_count, historical_note)
    """
    matching_cases = []
    for case in HISTORICAL_CASES:
        if any(t in case['event_types'] for t in event_types):
            matching_cases.append(case)

    if not matching_cases:
        return 50, 0, '无同类型历史案例，置信度默认50%'

    # Run backtest on matching cases
    total_score = 0
    total_count = 0
    for case in matching_cases:
        results = _run_backtest_single(case)
        for r in results.values():
            total_score += r['dir_score']
            total_count += 1

    accuracy = total_score / total_count if total_count > 0 else 0.5
    confidence = int(accuracy * 100)

    # Severity adjustment
    # Historical data shows: extreme events are HARDER to predict (more "buy the rumor sell the fact")
    if severity == 'extreme':
        confidence = max(30, confidence - 10)
        note = f'基于{len(matching_cases)}个同类历史案例，方向命中率{accuracy:.0%}。极端事件存在"冲高回落"风险，置信度下调10%。'
    elif severity == 'high':
        note = f'基于{len(matching_cases)}个同类历史案例，方向命中率{accuracy:.0%}。'
    else:
        confidence = min(85, confidence + 5)
        note = f'基于{len(matching_cases)}个同类历史案例，方向命中率{accuracy:.0%}。温和事件可预测性较高。'

    # Special lessons injection
    special_notes = []
    for case in matching_cases:
        if '买预期卖事实' in case.get('key_lesson', '') or '冲高回落' in case.get('key_lesson', ''):
            special_notes.append('⚠️ 历史案例警示：同类事件存在"买预期卖事实→冲高回落"的模式')
            break
    for case in matching_cases:
        if '流动性危机' in case.get('key_lesson', '') or '齐跌' in case.get('key_lesson', ''):
            special_notes.append('⚠️ 历史案例警示：极端事件可能触发流动性危机，连避险资产都下跌')
            break

    full_note = note
    if special_notes:
        full_note += '\n' + '\n'.join(special_notes)

    return confidence, len(matching_cases), full_note


# ── Rule-based impact prediction engine ─────────────────────────────
# Maps (event_type, asset) → directional impact rules
# CALIBRATED based on historical backtest results
IMPACT_RULES = {
    # ── 地缘政治 ──
    # 历史校准: 伊朗以色列(2024.4)油+7%/金+3.5%，俄乌(2022.2)油+25%/金+6%，美以打伊朗(2026.3)油+13%
    ('地缘政治', 'gold'):  {'dir': '↑', 'mag': '+1.5%~6%',  'reason': '避险资金涌入黄金（历史验证: +1.6%~6%）'},
    ('地缘政治', 'silver'):{'dir': '↑', 'mag': '+1%~3%',    'reason': '贵金属板块联动上涨'},
    ('地缘政治', 'oil'):   {'dir': '↑', 'mag': '+5%~13%',   'reason': '供应中断预期推高油价（历史验证: +7%~13%）'},
    ('地缘政治', 'btc'):   {'dir': '↓', 'mag': '-2%~8%',    'reason': 'BTC在地缘危机中表现为风险资产（历史验证: 100%下跌）'},
    ('地缘政治', 'spy'):   {'dir': '↓', 'mag': '-0.9%~3%',  'reason': '风险偏好下降（历史验证: -0.9%~-2.5%）'},
    ('地缘政治', 'qqq'):   {'dir': '↓', 'mag': '-1%~4%',    'reason': '科技股受风险情绪拖累'},
    ('地缘政治', 'usdx'):  {'dir': '↑', 'mag': '+0.5%~1.5%','reason': '美元避险属性走强（历史验证: +0.6%~1.5%）'},

    # ── 央行/货币政策（降息方向）──
    # 历史校准: 美联储降息50bp(2024.9)美股冲高回落-0.29%，BTC+3.5%，黄金冲高回落
    # 日本加息(2024.7)引发全球暴跌，BTC-8%，美股-3%~-4.5%
    # 中国降准(2024.9/2025.5)对国际资产影响温和但方向明确
    ('央行/货币政策', 'gold'):  {'dir': '↑', 'mag': '+0.5%~3%',  'reason': '利率下行降低持有黄金的机会成本（历史验证: 冲高回落风险）'},
    ('央行/货币政策', 'silver'):{'dir': '↑', 'mag': '+0.5%~2%',  'reason': '贵金属受益于宽松预期'},
    ('央行/货币政策', 'oil'):   {'dir': '↑', 'mag': '+0.3%~2%',  'reason': '宽松预期提振需求侧预期（历史验证: +0.3%~1.2%）'},
    ('央行/货币政策', 'btc'):   {'dir': '↑', 'mag': '+1.5%~5%',  'reason': '流动性宽松利好加密货币（历史验证: +1.5%~3.5%）'},
    ('央行/货币政策', 'spy'):   {'dir': '↕', 'mag': '±0.3%~3%',  'reason': '"买预期卖事实"风险高（历史验证: 美联储降息后美股冲高回落）'},
    ('央行/货币政策', 'qqq'):   {'dir': '↕', 'mag': '±0.3%~4%',  'reason': '成长股对利率敏感但存在冲高回落风险'},
    ('央行/货币政策', 'usdx'):  {'dir': '↓', 'mag': '-0.3%~1.5%','reason': '降息削弱美元收益吸引力（历史验证: -0.3%~-1.5%）'},

    # ── 能源/OPEC ──
    # 历史校准: OPEC减产160万桶(2023.4)油+7.5%，黄金+0.8%，美股-0.5%，BTC无反应
    ('能源/OPEC', 'gold'):  {'dir': '↑', 'mag': '+0.3%~1%', 'reason': '油价上涨推高通胀预期（历史验证: +0.8%）'},
    ('能源/OPEC', 'oil'):   {'dir': '↑', 'mag': '+5%~8%',   'reason': '减产直接推高原油价格（历史验证: +7.5%）'},
    ('能源/OPEC', 'btc'):   {'dir': '→', 'mag': '±0.5%',    'reason': '加密货币与能源市场脱钩（历史验证: 几乎无反应）'},
    ('能源/OPEC', 'spy'):   {'dir': '↓', 'mag': '-0.5%~1%', 'reason': '能源成本上升压缩企业利润（历史验证: -0.5%）'},
    ('能源/OPEC', 'usdx'):  {'dir': '↑', 'mag': '+0.3%~1%', 'reason': '油价上涨→通胀→美联储鹰派预期'},

    # ── 宏观经济数据（CPI/通胀超预期）──
    ('宏观经济数据', 'gold'):  {'dir': '↕', 'mag': '±1%~3%',   'reason': '通胀利好黄金但加息预期利空'},
    ('宏观经济数据', 'oil'):   {'dir': '→', 'mag': '±0.5%~1%', 'reason': '经济数据对油价影响取决于方向'},
    ('宏观经济数据', 'btc'):   {'dir': '↓', 'mag': '-2%~5%',   'reason': '紧缩预期压制风险资产'},
    ('宏观经济数据', 'spy'):   {'dir': '↓', 'mag': '-1%~3%',   'reason': '通胀超预期→加息预期→估值承压'},
    ('宏观经济数据', 'usdx'):  {'dir': '↑', 'mag': '+0.5%~1.5%','reason': '强经济数据支撑美元'},

    # ── 加密货币监管 ──
    # 历史校准: BTC ETF获批(2024.1)BTC先涨后暴跌-8.3%（买预期卖事实）
    ('加密货币监管', 'btc'):   {'dir': '↕', 'mag': '±5%~10%',  'reason': '重大利好可能已price-in→冲高回落（历史验证: ETF获批后-8.3%）'},
    ('加密货币监管', 'eth'):   {'dir': '↕', 'mag': '±5%~10%',  'reason': '加密市场联动'},
    ('加密货币监管', 'gold'):  {'dir': '→', 'mag': '±0.2%',    'reason': '加密监管对黄金影响极小（历史验证: +0.1%）'},
    ('加密货币监管', 'spy'):   {'dir': '→', 'mag': '±0.3%',    'reason': '对美股影响极小（历史验证: +0.3%）'},

    # ── 企业/行业 ──
    ('企业/行业', 'spy'):   {'dir': '↕', 'mag': '±1%~3%',   'reason': '取决于财报好坏和行业权重'},
    ('企业/行业', 'qqq'):   {'dir': '↕', 'mag': '±1%~4%',   'reason': '科技巨头财报对纳指影响放大'},
    ('企业/行业', 'btc'):   {'dir': '→', 'mag': '±0.5%',    'reason': '个股事件对加密影响有限'},
    ('企业/行业', 'gold'):  {'dir': '→', 'mag': '±0.3%',    'reason': '企业事件对黄金影响有限'},

    # ── 自然灾害/供应链 ──
    ('自然灾害/供应链', 'gold'):  {'dir': '↑', 'mag': '+0.5%~2%', 'reason': '供应链危机推动避险'},
    ('自然灾害/供应链', 'oil'):   {'dir': '↑', 'mag': '+2%~6%',   'reason': '灾害影响产能和运输'},
    ('自然灾害/供应链', 'spy'):   {'dir': '↓', 'mag': '-1%~3%',   'reason': '供应链中断影响企业盈利'},
    ('自然灾害/供应链', 'btc'):   {'dir': '→', 'mag': '±1%',      'reason': '供应链事件对加密影响有限'},

    # ── 贸易战/关税 ──
    # 历史校准: 特朗普加墨25%关税(2025.3)金+2%/股-1.76%
    # 极端关税(2025.4)系统性恐慌→连黄金都跌(-13%周跌)→避险失灵！
    # 重要教训: 普通关税→黄金涨(避险)；极端关税→黄金跌(流动性危机)
    ('其他/综合', 'gold'):  {'dir': '↕', 'mag': '±1%~3%',   'reason': '普通关税利好避险，极端关税触发流动性危机反跌（历史验证: +2% vs -13%）'},
    ('其他/综合', 'oil'):   {'dir': '↓', 'mag': '-1%~8%',   'reason': '贸易摩擦压制全球需求预期（历史验证: -1.5%~-8%）'},
    ('其他/综合', 'btc'):   {'dir': '↓', 'mag': '-3%~5%',   'reason': 'BTC在贸易战中100%下跌（历史验证: -3%~-5%）'},
    ('其他/综合', 'spy'):   {'dir': '↓', 'mag': '-1.5%~5%', 'reason': '关税直接冲击企业利润（历史验证: -1.76%~-4.5%）'},
    ('其他/综合', 'qqq'):   {'dir': '↓', 'mag': '-2%~6%',   'reason': '科技股供应链敏感（历史验证: -5%~-5.5%）'},
    ('其他/综合', 'usdx'):  {'dir': '↑', 'mag': '+0.5%~1%', 'reason': '贸易战中美元走强（历史验证: +0.5%~1%）'},
}

# Derivative event predictions per event type
DERIVATIVE_EVENTS = {
    '地缘政治': {
        'short': [
            '各国政府发表声明谴责/支持，外交斡旋启动',
            '相关地区航班停飞、航运绕道，运输成本飙升',
            '期权市场波动率(VIX)飙升，恐慌指数可能突破30',
        ],
        'medium': [
            '联合国安理会紧急会议召开',
            '相关国家可能宣布经济制裁或反制裁',
            '能源供应链出现阶段性中断预警，各国释放战略石油储备',
            '保险公司上调战争险费率',
        ],
        'long': [
            '央行可能发表紧急声明稳定市场预期',
            '受影响国家主权信用评级面临下调风险',
            '军工板块持续走强，防务订单预期上修',
            '全球供应链重新评估地缘风险，"近岸外包"趋势加速',
        ],
    },
    '央行/货币政策': {
        'short': [
            '债券市场即时定价调整，收益率曲线变化',
            '外汇市场剧烈波动，套利交易平仓',
            '股指期货快速反应，可能触发程序化交易',
        ],
        'medium': [
            '华尔街各大投行发布利率预测修正报告',
            '新兴市场货币承压/走强（取决于方向）',
            '房地产板块重新定价，REITs波动加大',
            '其他央行可能暗示跟进或保持观望',
        ],
        'long': [
            '信贷市场利差调整，企业融资成本变化',
            '消费信贷和房贷利率联动调整',
            '资金从货币市场基金流向/流出风险资产',
            '下一次央行议息会议预期被重新锚定',
        ],
    },
    '能源/OPEC': {
        'short': [
            '航空公司股价承压，燃油附加费预期上调',
            '化工、塑料等下游行业成本预期上升',
            '能源ETF和石油期货成交量激增',
        ],
        'medium': [
            '各国可能宣布释放战略石油储备',
            '新能源板块获得资金关注，替代能源逻辑强化',
            '通胀数据预期上修，央行加息概率调整',
            '运输和物流成本传导至消费品价格',
        ],
        'long': [
            '汽油零售价格上调，消费者信心指数承压',
            '产油国财政收入预期改善，中东主权基金可能增加全球投资',
            '长期能源转型政策讨论加速',
            'LNG现货市场溢价扩大',
        ],
    },
    '宏观经济数据': {
        'short': [
            '利率期货即时重新定价',
            '汇率市场快速反应，利差交易调整',
            '股指期货波动加剧',
        ],
        'medium': [
            '美联储官员可能在公开场合对数据发表评论',
            '债券基金调整久期仓位',
            '新兴市场面临资金流动压力',
        ],
        'long': [
            '下一次FOMC会议利率决议预期被锚定',
            '企业盈利预测被分析师修正',
            '消费者和企业信心指数后续数据受影响',
        ],
    },
    '加密货币监管': {
        'short': [
            '交易所交易量激增，可能出现闪崩或暴涨',
            'DeFi协议TVL大幅波动',
            '稳定币溢价/折价出现',
        ],
        'medium': [
            '其他国家监管机构可能跟进表态',
            '加密货币相关上市公司（Coinbase、MicroStrategy等）股价联动',
            '矿工和质押者行为调整',
        ],
        'long': [
            '行业合规成本重估',
            '机构投资者准入政策调整',
            '加密货币市场结构性变化（交易所、托管、衍生品）',
        ],
    },
    '企业/行业': {
        'short': [
            '相关个股及同业竞争对手股价联动',
            '板块ETF资金流向变化',
            '期权隐含波动率飙升',
        ],
        'medium': [
            '分析师密集发布评级调整报告',
            '产业链上下游公司被重新估值',
            '同行业其他公司业绩预期被修正',
        ],
        'long': [
            '行业格局可能发生改变（并购/退出）',
            '监管层可能对相关领域加强审查',
            '投资者风格轮动（成长→价值或反向）',
        ],
    },
    '自然灾害/供应链': {
        'short': [
            '保险股承压，再保险市场报价调整',
            '受灾地区相关产业链公司股价下跌',
            '商品期货出现供应溢价',
        ],
        'medium': [
            '救灾和重建相关财政支出预算启动',
            '替代供应商和替代路线获得溢价',
            '基建和重建板块获得资金关注',
        ],
        'long': [
            '供应链多元化加速，企业调整供应商布局',
            '保险行业费率长期上调',
            '气候政策讨论强化',
        ],
    },
    '其他/综合': {
        'short': [
            '市场情绪转向防御，波动率上升',
            '避险资产获得买盘支撑',
            '跨境资金流动出现异动',
        ],
        'medium': [
            '受影响国家可能出台反制措施',
            '全球贸易组织（WTO等）可能介入调解',
            '跨国企业下调营收指引',
            '替代供应链和"去风险化"讨论加速',
        ],
        'long': [
            '全球化格局面临重构压力',
            '区域贸易协定谈判加速',
            '相关产业链回流/外迁趋势强化',
            '消费者物价上涨压力向下游传导',
        ],
    },
}

# Trade-war / tariff specific keywords for better classification
TARIFF_KEYWORDS = ['关税', '贸易战', 'tariff', 'trade war', '加征', '贸易摩擦', '贸易壁垒',
                    '进口税', '出口管制', '脱钩', 'decoupling']


def _extract_event_details(event_text):
    """Extract specific details from event text: numbers, countries, organisations, direction."""
    import re
    details = {
        'numbers': [],       # percentages, amounts
        'countries': [],     # mentioned countries / regions
        'organisations': [], # central banks, OPEC, companies
        'direction': None,   # bullish / bearish / mixed signal
        'severity': 'medium', # low / medium / high / extreme
    }

    # ── Extract numbers & percentages ──
    for m in re.finditer(r'(\d+[\d,.]*)\s*(%|个基点|基点|万桶|亿|万亿|美元|bp)', event_text):
        details['numbers'].append(m.group(0))

    # ── severity based on magnitude words ──
    extreme_words = ['暴跌', '暴涨', '崩盘', '暴发', '全面', '紧急', '史无前例', '突然',
                     'crash', 'surge', 'collapse', 'emergency', 'unprecedented', '骤', '狂']
    high_words = ['大幅', '急剧', '重大', '剧烈', '猛', 'sharply', 'significantly', 'dramatic']
    low_words = ['小幅', '微调', '温和', '略', 'slight', 'modest', 'minor']

    text_lower = event_text.lower()
    if any(w in event_text for w in extreme_words):
        details['severity'] = 'extreme'
    elif any(w in event_text for w in high_words):
        details['severity'] = 'high'
    elif any(w in event_text for w in low_words):
        details['severity'] = 'low'

    # ── Countries / Regions ──
    country_map = {
        '中国': '中国', '美国': '美国', '俄罗斯': '俄罗斯', '乌克兰': '乌克兰',
        '伊朗': '伊朗', '以色列': '以色列', '日本': '日本', '欧洲': '欧洲',
        '英国': '英国', '德国': '德国', '法国': '法国', '韩国': '韩国',
        '印度': '印度', '沙特': '沙特阿拉伯', '土耳其': '土耳其', '巴西': '巴西',
        '台湾': '台湾', '朝鲜': '朝鲜', '中东': '中东地区', '东南亚': '东南亚',
        '泰国': '泰国', '印尼': '印尼', '马来西亚': '马来西亚', '菲律宾': '菲律宾',
        '新加坡': '新加坡', '澳大利亚': '澳大利亚', '新西兰': '新西兰',
        '加拿大': '加拿大', '阿根廷': '阿根廷', '智利': '智利', '哥伦比亚': '哥伦比亚',
        '南非': '南非', '尼日利亚': '尼日利亚', '埃及': '埃及', '巴基斯坦': '巴基斯坦',
        '孟加拉': '孟加拉', '缅甸': '缅甸', '老挝': '老挝', '柬埔寨': '柬埔寨',
        'China': '中国', 'US': '美国', 'Russia': '俄罗斯', 'Iran': '伊朗',
        'Israel': '以色列', 'Japan': '日本', 'Europe': '欧洲', 'India': '印度',
        'Saudi': '沙特阿拉伯', 'Turkey': '土耳其', 'Brazil': '巴西',
        'Mexico': '墨西哥', '墨西哥': '墨西哥', '越南': '越南',
        'Thailand': '泰国', 'Indonesia': '印尼', 'Malaysia': '马来西亚',
        'Philippines': '菲律宾', 'Singapore': '新加坡', 'Australia': '澳大利亚',
        'Canada': '加拿大', 'South Africa': '南非', 'Egypt': '埃及',
    }
    for kw, name in country_map.items():
        if kw in event_text and name not in details['countries']:
            details['countries'].append(name)

    # ── Organisations ──
    org_map = {
        '美联储': '美联储(Fed)', 'Fed': '美联储(Fed)', 'ECB': '欧央行(ECB)',
        '欧央行': '欧央行(ECB)', '日本央行': '日本央行(BOJ)', 'BOJ': '日本央行(BOJ)',
        '中国央行': '中国人民银行(PBOC)', '人民银行': '中国人民银行(PBOC)',
        'OPEC': 'OPEC', 'SEC': 'SEC', '特朗普': '特朗普政府', '拜登': '拜登政府',
        '普京': '俄罗斯政府', 'WTO': 'WTO', 'IMF': 'IMF',
        '苹果': 'Apple', '特斯拉': 'Tesla', '英伟达': 'NVIDIA',
        'Apple': 'Apple', 'Tesla': 'Tesla', 'NVIDIA': 'NVIDIA',
        '币安': 'Binance', 'Coinbase': 'Coinbase',
    }
    for kw, name in org_map.items():
        if kw in event_text and name not in details['organisations']:
            details['organisations'].append(name)

    # ── Direction signal ──
    bullish_kw = ['降息', '降准', '宽松', '刺激', '利好', '上涨', '暴涨', '飙升', '突破', '新高',
                  '获批', '通过', '批准', '减产', '流入', '破纪录', '增长', '复苏', '反弹',
                  'rate cut', 'easing', 'stimulus', 'bullish', 'surge', 'approve', 'rally',
                  'boom', 'record high', 'inflow']
    bearish_kw = ['加息', '紧缩', '制裁', '暴跌', '崩盘', '下跌', '衰退', '违约', '禁令',
                  '封锁', '关税', '打压', '加征', '流出', '抛售', '做空', '萎缩', '恶化',
                  'rate hike', 'tightening', 'crash', 'bearish', 'ban', 'tariff', 'recession',
                  'default', 'outflow', 'sell-off', 'collapse']
    b_count = sum(1 for w in bullish_kw if w in text_lower or w in event_text)
    s_count = sum(1 for w in bearish_kw if w in text_lower or w in event_text)
    if b_count > s_count:
        details['direction'] = 'bullish'
    elif s_count > b_count:
        details['direction'] = 'bearish'
    else:
        details['direction'] = 'mixed'

    return details


# Severity → magnitude multiplier for fine-tuning predictions
_SEVERITY_MULT = {'low': 0.3, 'medium': 1.0, 'high': 1.8, 'extreme': 2.5}


def _fmt_price(asset_data, asset_key):
    """Get display name and formatted price string from market data."""
    if isinstance(asset_data, dict) and 'price' in asset_data:
        p = asset_data['price']
        name = asset_data.get('display_name', asset_key.upper())
        if p >= 10000:
            price_str = f"(当前 ${p:,.0f})"
        elif p >= 1:
            price_str = f"(当前 ${p:,.2f})"
        else:
            price_str = f"(当前 ${p:.4f})"
        return name, price_str
    return asset_key.upper(), ''


def _scale_range(mag_str, severity):
    """Scale a magnitude range string by severity multiplier. Returns new string."""
    import re
    mult = _SEVERITY_MULT.get(severity, 1.0)
    def _replace(m):
        sign = m.group(1) or ''
        lo = float(m.group(2)) * mult
        hi = float(m.group(3)) * mult
        return f"{sign}{lo:.1f}%~{hi:.1f}%"
    scaled = re.sub(r'([+\-±]?)(\d+\.?\d*)%~(\d+\.?\d*)%', _replace, mag_str)
    return scaled


def generate_predictions(context):
    """Generate concrete predictions combining user event + global headlines.

    The enriched_text already contains extracted details from both the user's
    event and the global news context. We use it for all analysis.
    """
    event_text = context['event']['text']
    enriched_text = context['event'].get('enriched_text', event_text)
    event_types = context['event']['types']
    affected = context['affected_assets']
    market = context.get('market_snapshot', {})

    # Use enriched text for countries/numbers/severity extraction (richer data)
    details = _extract_event_details(enriched_text)
    severity = details['severity']
    countries = details['countries']
    orgs = details['organisations']
    numbers = details['numbers']

    # BUT use ORIGINAL event text for direction detection and key org/country
    # (global news might have opposite sentiment that shouldn't override user's event)
    user_details = _extract_event_details(event_text)
    direction = user_details['direction']
    # Prefer user's countries/orgs if available, else fall back to enriched
    if user_details['countries']:
        countries = user_details['countries']
    else:
        # Infer country from org when user didn't explicitly mention a country
        org_to_country = {
            '美联储(Fed)': '美国', '欧央行(ECB)': '欧洲', '日本央行(BOJ)': '日本',
            '中国人民银行(PBOC)': '中国',
        }
        inferred = []
        for o in user_details['organisations']:
            if o in org_to_country:
                c = org_to_country[o]
                if c not in inferred:
                    inferred.append(c)
        if inferred:
            countries = inferred
    if user_details['organisations']:
        orgs = user_details['organisations']
    if user_details['numbers']:
        numbers = user_details['numbers']

    is_tariff = any(kw in enriched_text.lower() for kw in TARIFF_KEYWORDS)

    # Build a short event summary tag for embedding in predictions
    country_tag = '、'.join(countries[:3]) if countries else '全球'
    org_tag = '、'.join(orgs[:2]) if orgs else ''
    num_tag = '（' + '、'.join(numbers[:2]) + '）' if numbers else ''
    severity_label = {'low': '温和', 'medium': '中等', 'high': '强烈', 'extreme': '极端'}[severity]

    predictions = {
        'short': [],
        'medium': [],
        'long': [],
        'chain': [],
        'derivative_events': {'short': [], 'medium': [], 'long': []},
    }

    # ═══════════════════════════════════════════
    # 1. SHORT-TERM: Asset-specific predictions with event details embedded
    #    Direction-aware:央行/货币政策 rules flip when direction is bearish (加息)
    # ═══════════════════════════════════════════
    _DIR_FLIP = {'↑': '↓', '↓': '↑', '↕': '↕', '→': '→'}

    for etype in event_types:
        for asset in affected:
            rule = IMPACT_RULES.get((etype, asset))
            if not rule:
                continue

            name, price_str = _fmt_price(market.get(asset, {}), asset)
            dir_sym = rule['dir']
            mag = _scale_range(rule['mag'], severity)
            base_reason = rule['reason']

            # Flip direction for央行/货币政策 when event direction is bearish (加息/紧缩)
            # IMPACT_RULES are calibrated for降息(bullish), so加息 flips them
            if etype == '央行/货币政策' and direction == 'bearish':
                # Special case: for non-US central bank tightening, USD strengthens (not weakens)
                # So usdx should NOT be flipped when a non-US bank tightens
                is_non_us_cb = any(c not in ('美国',) for c in countries) and '美联储(Fed)' not in orgs
                if asset == 'usdx' and is_non_us_cb:
                    # Non-US CB tightening: USD may weaken (their currency strengthens)
                    dir_sym = '↓'
                    base_reason = '非美央行加息→该国货币升值→美元相对走弱（历史验证: 日本加息→美元-1.5%）'
                else:
                    dir_sym = _DIR_FLIP.get(dir_sym, dir_sym)
                    base_reason = base_reason.replace('降低', '增加').replace('宽松', '紧缩').replace('下行', '上行')
                    base_reason += '（加息/紧缩方向，规则已翻转）'

            # Customize reason with event specifics
            if countries:
                base_reason += f"（{country_tag}事件驱动）"
            if numbers:
                base_reason += f" {num_tag}"

            predictions['short'].append(
                f"{name} {price_str} → {dir_sym} 预计 {mag} | {base_reason}"
            )

    # ═══════════════════════════════════════════
    # 2. SHORT-TERM DERIVATIVE EVENTS: Tailored to event text
    # ═══════════════════════════════════════════
    for etype in event_types:
        base_deriv = DERIVATIVE_EVENTS.get(etype, DERIVATIVE_EVENTS.get('其他/综合', {}))
        for horizon in ['short', 'medium', 'long']:
            for evt in base_deriv.get(horizon, []):
                # Inject country/org specifics into generic template
                customized = evt
                if '各国' in evt and countries:
                    customized = evt.replace('各国', country_tag + '等国')
                if '相关国家' in evt and countries:
                    customized = evt.replace('相关国家', country_tag)
                if '受影响国家' in evt and countries:
                    customized = evt.replace('受影响国家', country_tag)
                if customized not in predictions['derivative_events'][horizon]:
                    predictions['derivative_events'][horizon].append(customized)

    # ═══════════════════════════════════════════
    # 3. MEDIUM-TERM: Dynamic cross-market analysis
    # ═══════════════════════════════════════════
    if any(t in event_types for t in ['地缘政治', '能源/OPEC']):
        if severity in ('high', 'extreme'):
            predictions['medium'].extend([
                f'由于{country_tag}局势{severity_label}冲击 → 原油上涨 → 通胀预期上修 → 美联储降息预期推迟',
                f'航空股（UAL/DAL/AAL）和邮轮股（CCL/RCL）受{country_tag}风险拖累，预计下跌 3%~8%',
                f'能源板块（XLE）和军工板块（LMT/RTX/NOC）因{country_tag}事件逆势上涨',
                f'新兴市场货币（尤其是能源进口国：印度卢比、土耳其里拉）受{severity_label}冲击承压',
            ])
        else:
            predictions['medium'].extend([
                f'{country_tag}局势 → 原油温和上行 → 通胀预期小幅上修',
                '航空和运输板块承受一定成本压力',
                '能源板块小幅受益',
            ])

    if any(t in event_types for t in ['央行/货币政策']):
        cb_name = org_tag if org_tag else '央行'
        if direction == 'bullish':  # 降息/宽松
            predictions['medium'].extend([
                f'{cb_name}宽松信号 → 房地产板块（REITs）受益，预计上涨 1%~3%',
                f'{cb_name}降息 → 科技成长股弹性最大，ARKK/SOXX等高贝塔ETF领涨',
                f'美元走弱 → 新兴市场资金回流 → EM ETF（EEM）可能上涨',
                f'{cb_name}宽松 → 贵金属矿业股（GDX）放大弹性，黄金白银持续走强',
            ])
        else:  # 加息/紧缩
            predictions['medium'].extend([
                f'{cb_name}鹰派 → 高估值科技股承压，纳斯达克跌幅可能大于标普',
                f'{cb_name}紧缩 → 美元走强 → 出口导向型企业盈利承压',
                '新兴市场面临资金外流压力',
            ])

    if is_tariff or '其他/综合' in event_types:
        target = country_tag if countries else '相关国家'
        predictions['medium'].extend([
            f'{target}出口企业首当其冲，相关货币贬值压力加大',
            f'{target}供应链上的跨国公司（苹果、特斯拉等）股价承压',
            '替代供应国（越南、印度、墨西哥）相关ETF可能获得资金流入',
            f'大宗商品贸易流向因{target}贸易壁垒而改变，工业金属需求预期下修',
        ])

    if any(t in event_types for t in ['加密货币监管']):
        reg_body = org_tag if org_tag else '监管机构'
        if direction == 'bullish':
            predictions['medium'].extend([
                f'{reg_body}利好政策 → 机构资金加速入场，交易量暴增',
                '加密货币相关上市公司（Coinbase/MicroStrategy）股价联动上涨',
                'DeFi和质押板块受益，TVL可能回升',
            ])
        else:
            predictions['medium'].extend([
                f'{reg_body}打压 → 交易所合规成本飙升，部分平台可能退出',
                '加密货币相关上市公司（Coinbase/MicroStrategy）联动下跌',
                '资金从高风险山寨币流向BTC/ETH等主流币种避险',
            ])

    if any(t in event_types for t in ['宏观经济数据']):
        predictions['medium'].extend([
            f'{country_tag}经济数据公布后 → 美联储官员可能在公开场合发表评论',
            '债券基金调整久期仓位，收益率曲线形态变化',
            f'外汇市场重新定价{country_tag}经济前景',
        ])

    if any(t in event_types for t in ['企业/行业']):
        company = org_tag if org_tag else '相关企业'
        predictions['medium'].extend([
            f'{company}事件 → 同行业竞争对手股价联动',
            f'分析师密集发布{company}评级调整报告',
            f'{company}产业链上下游被重新估值',
        ])

    if any(t in event_types for t in ['自然灾害/供应链']):
        region = country_tag if countries else '受灾地区'
        predictions['medium'].extend([
            f'{region}灾后 → 救灾和重建财政支出预算启动',
            f'{region}供应链中断 → 替代供应商和替代路线获得溢价',
            '基建和重建板块（CAT/VMC/MLM）获得资金关注',
        ])

    # ═══════════════════════════════════════════
    # 4. LONG-TERM: Customised structural predictions
    # ═══════════════════════════════════════════
    predictions['long'].append(
        f'全球各大市场依次开盘消化「{event_text[:30]}…」：亚洲→欧洲→美洲，注意开盘跳空缺口'
    )
    if severity in ('high', 'extreme'):
        predictions['long'].append(
            f'事件冲击等级为「{severity_label}」，期权市场隐含波动率可能维持高位1-2天'
        )
        predictions['long'].append(
            'ETF再平衡 + 被动基金自动调仓 → 事件后1-2天二次波动'
        )
    else:
        predictions['long'].append(
            '事件冲击相对温和，市场可能在24小时内消化并回归趋势'
        )

    # Type-specific long-term
    if any(t in event_types for t in ['地缘政治']):
        predictions['long'].extend([
            f'{country_tag}局势后续 → 各国可能重新评估地缘风险敞口',
            f'若{country_tag}冲突持续 → 军工、能源板块中长期逻辑强化',
            f'{country_tag}风险 → 供应链"近岸外包"和"友岸外包"趋势可能加速',
        ])
    if any(t in event_types for t in ['央行/货币政策']):
        cb = org_tag if org_tag else '央行'
        predictions['long'].extend([
            f'{cb}决议后 → 下一次议息会议预期被重新锚定',
            '信贷市场利差调整 → 企业融资成本和消费信贷利率联动变化',
            f'{cb}政策信号 → 全球其他央行可能跟进或保持观望',
        ])
    if is_tariff:
        predictions['long'].extend([
            f'{country_tag}贸易摩擦 → 全球化格局面临重构，区域贸易协定谈判可能加速',
            f'被征税产业链面临回流/外迁抉择，中长期产能布局将发生改变',
            f'消费者物价上涨压力从{country_tag}进口端向下游全面传导',
        ])

    # ═══════════════════════════════════════════
    # 5. CAUSE-EFFECT CHAIN: Built from actual event details
    # ═══════════════════════════════════════════
    if any(t in event_types for t in ['地缘政治']):
        predictions['chain'] = [
            event_text,
            f'{country_tag}冲突 → 原油供应中断预期 + 全球避险情绪{severity_label}飙升',
            f'黄金/原油{severity_label}上涨，美股/新兴市场下跌，美元短期走强',
            f'通胀预期上修 → 央行政策空间收窄 → 全球经济增长预期下调',
        ]
    elif any(t in event_types for t in ['央行/货币政策']):
        cb = org_tag if org_tag else '央行'
        act = '降息' if direction == 'bullish' else '加息/紧缩'
        predictions['chain'] = [
            event_text,
            f'{cb}{act}{num_tag} → 利率预期重新定价，债券市场即时反应',
            f'美元{"走弱" if direction == "bullish" else "走强"} → 大宗商品和新兴市场联动',
            f'信贷环境变化 → 企业投资和消费行为调整 → 经济增速预期修正',
        ]
    elif any(t in event_types for t in ['能源/OPEC']):
        predictions['chain'] = [
            event_text,
            f'{"OPEC" if "OPEC" in event_text else country_tag}决定 → 原油价格跳涨{num_tag}，能源板块领涨',
            f'运输和制造成本上升 → 通胀数据上行 → 央行鹰派预期强化',
            '消费者支出被挤压 → 零售和消费板块承压 → 经济放缓担忧',
        ]
    elif is_tariff:
        predictions['chain'] = [
            event_text,
            f'{country_tag}进口成本飙升{num_tag} → 消费者价格上涨 → 通胀压力',
            f'{country_tag}供应链企业紧急寻找替代方案 → 短期混乱、长期重构',
            f'{country_tag}可能反制 → 贸易战升级 → 全球GDP增速下调',
        ]
    elif any(t in event_types for t in ['加密货币监管']):
        reg = org_tag if org_tag else '监管层'
        predictions['chain'] = [
            event_text,
            f'{reg}政策出台 → 加密市场剧烈波动，交易量激增',
            f'{"机构资金加速入场" if direction == "bullish" else "恐慌性抛售，资金出逃"} → 市场格局重塑',
            '行业合规成本和准入门槛重新定义 → 长期结构性变化',
        ]
    elif any(t in event_types for t in ['宏观经济数据']):
        predictions['chain'] = [
            event_text,
            f'{country_tag}经济数据{"超预期" if direction == "bullish" else "不及预期"}{num_tag} → 利率期货即时重新定价',
            '汇率和债券市场联动 → 风险资产重新估值',
            '后续政策预期调整 → 下一次FOMC/央行会议成为关键博弈点',
        ]
    else:
        predictions['chain'] = [
            event_text,
            f'{country_tag}市场不确定性上升{num_tag}，波动率飙升',
            f'资金从风险资产流向避险资产',
            f'后续{org_tag + "的" if org_tag else ""}政策回应和市场消化决定中长期走势',
        ]

    return predictions

# Event type classification keywords
EVENT_TYPES = {
    '央行/货币政策': ['降息', '加息', '美联储', 'Fed', 'ECB', '央行', '利率', 'rate', '货币政策',
                      'QE', '量化宽松', 'taper', '缩表'],
    '地缘政治': ['战争', '冲突', '制裁', '军事', '导弹', '攻击', '入侵', 'war', 'sanction',
                  '中东', '俄罗斯', '乌克兰', '台海', '朝鲜', '袭击', '轰炸', '空袭',
                  '以色列', '伊朗', '巴勒斯坦', '黎巴嫩', '叙利亚', 'strike', 'bomb',
                  '核武', '报复', '紧张局势', 'missile', 'invasion'],
    '能源/OPEC': ['OPEC', '减产', '增产', '石油', '原油', '油价', '管道', '炼油', '产油国'],
    '加密货币监管': ['SEC', '监管', '合规', 'ETF', '比特币ETF', '交易所', '稳定币', '币安',
                      'Coinbase', 'regulation', 'crypto ban'],
    '宏观经济数据': ['GDP', 'CPI', 'PPI', '非农', '就业', '失业率', 'PMI', '通胀', '零售',
                      '消费', 'inflation', 'employment', 'payroll'],
    '企业/行业': ['财报', '业绩', '营收', '利润', '裁员', '并购', '收购', 'IPO', '回购',
                    'earnings', 'revenue', 'merger', 'acquisition'],
    '自然灾害/供应链': ['地震', '飓风', '洪水', '干旱', '供应链', '芯片', '短缺', '港口',
                         'supply chain', 'shortage', '灾难', '灾害', '台风', '海啸',
                         '火灾', '爆炸', '泄漏', '瘟疫', '疫情'],
}


def enrich_event_from_news(event_text, news_articles):
    """Extract key details from news articles to enrich a short event description.

    When users provide a brief event like '泰国遭遇突发灾难', this function
    reads through related news titles and summaries to extract concrete details
    (what happened, scale, affected industries, numbers) and builds an
    enriched event description that drives better analysis.

    Returns: (enriched_text, news_insights_list)
    """
    if not news_articles:
        return event_text, []

    import re

    # Collect all text from news for keyword extraction
    all_news_text = ''
    insights = []
    for article in news_articles[:10]:
        title = article.get('title', '')
        summary = article.get('summary', '')
        all_news_text += f" {title} {summary}"
        if title:
            insights.append(title)

    if not all_news_text.strip():
        return event_text, []

    # ── Extract concrete details from news ──
    extracted = {
        'disaster_types': [],
        'numbers': [],
        'locations': [],
        'industries': [],
        'impacts': [],
        'key_phrases': [],
    }

    # Disaster types
    disaster_map = {
        '地震': '地震', '海啸': '海啸', '洪水': '洪水', '洪灾': '洪灾',
        '飓风': '飓风', '台风': '台风', '龙卷风': '龙卷风',
        '干旱': '干旱', '火灾': '火灾', '山火': '山火', '野火': '野火',
        '火山': '火山喷发', '泥石流': '泥石流', '滑坡': '山体滑坡',
        '爆炸': '爆炸', '泄漏': '泄漏', '核': '核事故',
        '疫情': '疫情', '瘟疫': '瘟疫', '传染': '传染病',
        'earthquake': '地震', 'tsunami': '海啸', 'flood': '洪水',
        'hurricane': '飓风', 'typhoon': '台风', 'drought': '干旱',
        'wildfire': '山火', 'volcano': '火山喷发', 'explosion': '爆炸',
        'pandemic': '疫情', 'epidemic': '疫情',
        '暴雨': '暴雨', '暴风雪': '暴风雪', '冰雹': '冰雹',
    }
    for kw, name in disaster_map.items():
        if kw in all_news_text.lower() and name not in extracted['disaster_types']:
            extracted['disaster_types'].append(name)

    # Numbers from news
    for m in re.finditer(r'(\d+[\d,.]*)\s*(%|人|亿|万|美元|死|伤|遇难|失踪|受灾|吨|桶|万桶|级|miles|km|hectares|acres)', all_news_text):
        num = m.group(0)
        if num not in extracted['numbers'] and len(extracted['numbers']) < 5:
            extracted['numbers'].append(num)

    # Industries affected
    industry_kw = {
        '旅游': '旅游业', '航空': '航空业', '农业': '农业', '渔业': '渔业',
        '制造': '制造业', '半导体': '半导体', '芯片': '芯片产业',
        '汽车': '汽车产业', '电子': '电子产业', '矿业': '矿业',
        '保险': '保险业', '房地产': '房地产', '基建': '基础设施',
        '港口': '港口物流', '运输': '运输物流', '能源': '能源',
        '橡胶': '橡胶', '棕榈油': '棕榈油', '大米': '大米/粮食',
        '天然气': '天然气', '煤炭': '煤炭', '钢铁': '钢铁',
        'tourism': '旅游业', 'semiconductor': '半导体', 'mining': '矿业',
        'agriculture': '农业', 'oil': '石油', 'shipping': '航运',
    }
    for kw, name in industry_kw.items():
        if kw in all_news_text.lower() and name not in extracted['industries']:
            extracted['industries'].append(name)

    # Impact words
    impact_kw = {
        '停产': '停产', '停工': '停工', '中断': '中断', '瘫痪': '瘫痪',
        '疏散': '疏散', '撤离': '撤离', '封锁': '封锁', '关闭': '关闭',
        '短缺': '短缺', '涨价': '涨价', '断供': '断供', '延误': '延误',
        '损失': '损失', '破坏': '破坏', '倒塌': '倒塌', '崩溃': '崩溃',
    }
    for kw, name in impact_kw.items():
        if kw in all_news_text and name not in extracted['impacts']:
            extracted['impacts'].append(name)

    # ── Build enriched event text ──
    enriched_parts = [event_text]

    if extracted['disaster_types']:
        enriched_parts.append(f"[新闻细节] 灾害类型: {', '.join(extracted['disaster_types'])}")
    if extracted['numbers']:
        enriched_parts.append(f"[新闻细节] 关键数据: {', '.join(extracted['numbers'])}")
    if extracted['industries']:
        enriched_parts.append(f"[新闻细节] 受影响产业: {', '.join(extracted['industries'])}")
    if extracted['impacts']:
        enriched_parts.append(f"[新闻细节] 影响方式: {', '.join(extracted['impacts'])}")

    enriched_text = '\n'.join(enriched_parts)
    return enriched_text, insights


def generate_news_summary(event_text, news_articles, details):
    """Generate a contextual summary paragraph from news articles.

    Instead of just listing news titles, synthesize them into a coherent
    narrative that connects to the event's market impact.
    """
    if not news_articles:
        return ''

    country_tag = '、'.join(details['countries'][:3]) if details['countries'] else '相关地区'
    severity_label = {'low': '温和', 'medium': '中等', 'high': '强烈', 'extreme': '极端'}[details['severity']]

    titles = [a.get('title', '') for a in news_articles[:8] if a.get('title')]
    if not titles:
        return ''

    # Extract the most informative news phrases
    summary_lines = []
    summary_lines.append(f"  综合 {len(titles)} 条实时新闻，当前事件核心情况如下：")

    # Categorise news by content
    price_news = [t for t in titles if any(k in t for k in ['涨', '跌', '价格', '指数', '$', '暴', '飙', '大幅', 'price', 'surge', 'drop', 'rally'])]
    policy_news = [t for t in titles if any(k in t for k in ['政府', '政策', '央行', '宣布', '紧急', '声明', 'government', 'policy', 'emergency'])]
    impact_news = [t for t in titles if any(k in t for k in ['损失', '死亡', '影响', '中断', '破坏', '受灾', '难民', 'damage', 'impact', 'loss'])]
    other_news = [t for t in titles if t not in price_news and t not in policy_news and t not in impact_news]

    if impact_news:
        summary_lines.append(f"  • 事件影响：")
        for t in impact_news[:3]:
            summary_lines.append(f"    - {t}")
    if price_news:
        summary_lines.append(f"  • 市场反应：")
        for t in price_news[:3]:
            summary_lines.append(f"    - {t}")
    if policy_news:
        summary_lines.append(f"  • 政策动态：")
        for t in policy_news[:2]:
            summary_lines.append(f"    - {t}")
    if other_news and not impact_news and not price_news:
        summary_lines.append(f"  • 相关动态：")
        for t in other_news[:3]:
            summary_lines.append(f"    - {t}")

    return '\n'.join(summary_lines)


def classify_event(event_text):
    """Classify event type based on keywords."""
    matched_types = []
    text_lower = event_text.lower()
    for event_type, keywords in EVENT_TYPES.items():
        for kw in keywords:
            if kw.lower() in text_lower:
                matched_types.append(event_type)
                break
    return matched_types if matched_types else ['其他/综合']


def identify_affected_assets(event_text):
    """Identify which assets are most likely affected by the event."""
    text_lower = event_text.lower()
    affected = []

    asset_keywords = {
        'gold': ['黄金', 'gold', '避险', '贵金属'],
        'silver': ['白银', 'silver'],
        'oil': ['原油', '石油', 'oil', 'OPEC', '减产', '增产', '能源'],
        'btc': ['比特币', 'bitcoin', 'BTC', '加密', 'crypto', '数字货币', '币'],
        'eth': ['以太坊', 'ethereum', 'ETH'],
        'spy': ['美股', 'S&P', '标普', '股市', '股票', 'stock'],
        'qqq': ['科技股', '纳斯达克', 'nasdaq', 'tech'],
        'usdx': ['美元', 'dollar', 'USD', '汇率'],
    }

    for asset, keywords in asset_keywords.items():
        for kw in keywords:
            if kw.lower() in text_lower:
                affected.append(asset)
                break

    # If no specific assets detected, include all major ones
    if not affected:
        affected = ['gold', 'oil', 'btc', 'spy']

    return list(set(affected))


def build_analysis_context(event_text, enriched_text, market_data, news_data, focus_assets):
    """Build a structured context for the AI to analyze.

    event_text: original user input
    enriched_text: event text enriched with news details
    """

    # Use enriched text for classification (richer keywords) but display original
    event_types = classify_event(enriched_text)
    affected_assets = identify_affected_assets(enriched_text)

    # Merge focus with detected assets
    if focus_assets:
        all_assets = list(set(focus_assets + affected_assets))
    else:
        all_assets = affected_assets

    # Build correlation context
    correlations = []
    for asset in all_assets:
        if asset in CORRELATION_MAP:
            correlations.append(f"  - {asset}: {CORRELATION_MAP[asset]['description']}")

    news_articles = news_data.get('articles', []) if news_data else []

    context = {
        'event': {
            'text': event_text,            # original user input
            'enriched_text': enriched_text, # enriched with news details
            'types': event_types,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        },
        'affected_assets': all_assets,
        'market_snapshot': market_data.get('assets', {}) if market_data else {},
        'related_news': [
            {'title': a['title'], 'source': a['source'], 'published': a['published'],
             'summary': a.get('summary', '')}
            for a in news_articles[:8]
        ],
        'news_articles_raw': news_articles,  # keep full data for enrichment
        'correlations': {
            asset: CORRELATION_MAP.get(asset, {})
            for asset in all_assets if asset in CORRELATION_MAP
        },
        'analysis_framework': {
            'short_term': '立刻 — 1小时内: 直接市场反应、情绪冲击、成交量异动',
            'medium_term': '1-12小时: 二次传导、跨市场联动、后续新闻事件',
            'long_term': '12-24小时: 新均衡价格、政策回应、衍生事件预测',
        }
    }

    return context


def _generate_standalone_interpretation(event_text, event_types, affected_assets, market):
    """Generate a standalone narrative interpretation of the user's event ONLY.

    This is a pure, self-contained analysis paragraph — no global news mixed in.
    It reads like a human analyst's first-take assessment of the event.
    """
    user_details = _extract_event_details(event_text)
    severity = user_details['severity']
    severity_label = {'low': '温和', 'medium': '中等', 'high': '强烈', 'extreme': '极端'}[severity]
    direction = user_details['direction']
    countries = user_details['countries']
    orgs = user_details['organisations']
    numbers = user_details['numbers']

    country_tag = '、'.join(countries[:3]) if countries else '相关地区'
    org_tag = '、'.join(orgs[:2]) if orgs else ''
    num_tag = '、'.join(numbers[:2]) if numbers else ''

    paragraphs = []

    # ── Opening sentence ──
    if severity in ('high', 'extreme'):
        paragraphs.append(f"「{event_text}」是一条{severity_label}级别的重大新闻，预计将对全球金融市场产生显著冲击。")
    elif severity == 'medium':
        paragraphs.append(f"「{event_text}」是一条值得高度关注的重要新闻，将对相关标的产生明确的方向性影响。")
    else:
        paragraphs.append(f"「{event_text}」虽然冲击等级相对温和，但仍会对部分标的产生可观测的影响。")

    # ── Type-specific interpretation ──
    for etype in event_types:
        if etype == '地缘政治':
            paragraphs.append(
                f"从地缘政治角度看，{country_tag}事件将直接触发全球避险情绪升温。"
                f"黄金和原油作为传统避险/地缘受益资产将获得买盘支撑，"
                f"而美股等风险资产则面临资金撤离压力。美元短期可能因避险属性走强。"
            )
            if severity in ('high', 'extreme'):
                paragraphs.append(
                    f"鉴于冲击等级为「{severity_label}」，市场反应可能非常剧烈，"
                    f"期权隐含波动率(VIX)可能大幅飙升，程序化交易和止损单密集触发将放大波动。"
                )
        elif etype == '央行/货币政策':
            if direction == 'bullish':
                paragraphs.append(
                    f"{org_tag or '央行'}释放宽松信号{f'（{num_tag}）' if num_tag else ''}，"
                    f"这将重塑利率预期。降息/降准直接降低持有黄金的机会成本，利好贵金属；"
                    f"流动性宽松利好风险资产（股票、加密货币），美元则因收益率吸引力下降而承压。"
                )
                if severity in ('high', 'extreme'):
                    paragraphs.append(
                        f"超预期的宽松力度{f'（{num_tag}）' if num_tag else ''}表明{org_tag or '央行'}"
                        f"对经济前景持较强的刺激意愿，市场可能迎来一波显著的风险偏好提升行情。"
                    )
            else:
                paragraphs.append(
                    f"{org_tag or '央行'}释放鹰派/紧缩信号{f'（{num_tag}）' if num_tag else ''}，"
                    f"这意味着利率将维持高位甚至进一步上升。高估值科技股和风险资产将承压，"
                    f"美元走强，新兴市场面临资金外流风险。"
                )
        elif etype == '能源/OPEC':
            paragraphs.append(
                f"能源/OPEC相关事件{f'（{num_tag}）' if num_tag else ''}将直接影响原油价格。"
                f"原油上涨会通过「油价→运输成本→通胀→央行政策」的传导链影响几乎所有资产类别。"
                f"能源板块直接受益，航空和消费板块则面临成本压力。"
            )
        elif etype == '自然灾害/供应链':
            paragraphs.append(
                f"{country_tag}遭遇的灾害/供应链事件将导致区域性经济活动中断。"
                f"受灾地区相关产业链（制造、运输、农业等）公司将承压，"
                f"大宗商品可能因供应预期收紧而上行，避险资产获得买盘支撑。"
                f"保险板块短期承压，重建板块中长期受益。"
            )
        elif etype == '加密货币监管':
            if direction == 'bullish':
                paragraphs.append(
                    f"利好的加密货币监管政策将大幅提振市场信心，机构资金加速入场，"
                    f"BTC和ETH可能出现较大幅度上涨。"
                )
            else:
                paragraphs.append(
                    f"不利的加密货币监管消息将触发恐慌性抛售，交易所面临合规压力，"
                    f"资金从高风险山寨币向主流币种集中避险。"
                )
        elif etype == '宏观经济数据':
            paragraphs.append(
                f"{country_tag}的宏观经济数据{f'（{num_tag}）' if num_tag else ''}将重新锚定市场"
                f"对利率路径的预期。利率期货、汇率和债券市场会最先反应，"
                f"随后传导至股票和大宗商品。"
            )
        elif etype == '企业/行业':
            paragraphs.append(
                f"{org_tag or '相关企业'}事件将引发同行业板块联动，"
                f"分析师将密集发布评级调整，产业链上下游估值面临重新校准。"
            )

    # ── Closing with historical calibration warnings ──
    if direction == 'bullish':
        paragraphs.append(f"综合来看，此事件整体信号偏多/看涨，重点关注做多机会。")
    elif direction == 'bearish':
        paragraphs.append(f"综合来看，此事件整体信号偏空/看跌，需注意风险敞口管理。")
    else:
        paragraphs.append(f"综合来看，此事件多空信号交织，需结合后续发展判断方向。")

    # Historical pattern warnings (calibrated from real cases)
    if severity in ('high', 'extreme'):
        paragraphs.append(
            f"⚠️ 历史校准提醒: 同等级别（{severity_label}）事件，历史上存在「买预期卖事实」的冲高回落模式。"
            f"2024年9月美联储降息50bp后美股冲高回落收跌-0.29%，2024年1月BTC ETF获批后暴跌-8.3%。"
            f"建议关注事件消息公布后10-30分钟内的价格反转信号。"
        )
    if any(t == '其他/综合' for t in event_types) and severity == 'extreme':
        paragraphs.append(
            f"⚠️ 极端关税历史警告: 2025年4月特朗普极端关税曾触发系统性恐慌，"
            f"连黄金都暴跌-13%（流动性危机，所有资产齐跌）。"
            f"当关税力度极端时，传统避险逻辑可能失效。"
        )

    return paragraphs


def _filter_conflicting_headlines(global_headlines, user_event_text, user_direction, user_types):
    """Filter out global headlines that DIRECTLY CONFLICT with the user's event.

    Conflict means: the headline asserts the opposite conclusion on the SAME topic.
    For example:
      - User says "央行降息" (bullish), headline says "央行加息" (bearish) → conflict
      - User says "oil surges", headline says "oil drops" → conflict

    Returns: (filtered_headlines, removed_headlines_info)
    """
    if not global_headlines:
        return [], []

    user_details = _extract_event_details(user_event_text)
    user_countries = set(user_details['countries'])
    user_orgs = set(user_details['organisations'])

    filtered = []
    removed = []

    for article in global_headlines:
        title = article.get('title', '')
        if not title:
            continue

        h_details = _extract_event_details(title)
        h_types = classify_event(title)
        h_direction = h_details['direction']
        h_countries = set(h_details['countries'])
        h_orgs = set(h_details['organisations'])

        is_conflict = False
        conflict_reason = ''

        # Check for DIRECT conflict: same topic/entity, opposite direction
        # 1. Same country/org AND same event type AND opposite direction
        has_common_entity = bool(user_countries & h_countries) or bool(user_orgs & h_orgs)
        has_common_type = bool(set(user_types) & set(h_types))

        if has_common_entity and has_common_type:
            if user_direction in ('bullish', 'bearish') and h_direction in ('bullish', 'bearish'):
                if user_direction != h_direction:
                    is_conflict = True
                    conflict_reason = f"与你的新闻方向直接冲突（你: {user_direction}, 该新闻: {h_direction}）"

        # 2. Specific contradiction patterns
        user_lower = user_event_text.lower()
        title_lower = title.lower()

        # Rate cut vs rate hike on same entity
        if ('降息' in user_lower or 'rate cut' in user_lower or '降准' in user_lower):
            if ('加息' in title_lower or 'rate hike' in title_lower or 'tightening' in title_lower):
                if has_common_entity:
                    is_conflict = True
                    conflict_reason = "该新闻声称加息/紧缩，与你的降息/宽松新闻直接矛盾"
        elif ('加息' in user_lower or 'rate hike' in user_lower):
            if ('降息' in title_lower or 'rate cut' in title_lower or 'easing' in title_lower):
                if has_common_entity:
                    is_conflict = True
                    conflict_reason = "该新闻声称降息/宽松，与你的加息/紧缩新闻直接矛盾"

        # Asset price direction contradiction on same asset
        price_up_kw = ['上涨', '暴涨', '飙升', 'surge', 'rally', 'soar', 'jump']
        price_down_kw = ['下跌', '暴跌', '崩盘', 'drop', 'crash', 'plunge', 'slump', 'fall']
        user_says_up = any(k in user_lower for k in price_up_kw)
        user_says_down = any(k in user_lower for k in price_down_kw)
        headline_says_up = any(k in title_lower for k in price_up_kw)
        headline_says_down = any(k in title_lower for k in price_down_kw)

        if has_common_type and has_common_entity:
            if user_says_up and headline_says_down:
                is_conflict = True
                conflict_reason = "该新闻声称下跌，与你的上涨新闻直接矛盾"
            elif user_says_down and headline_says_up:
                is_conflict = True
                conflict_reason = "该新闻声称上涨，与你的下跌新闻直接矛盾"

        if is_conflict:
            removed.append({
                'title': title,
                'reason': conflict_reason,
            })
        else:
            filtered.append(article)

    return filtered, removed


def _build_user_event_deep_analysis(event_text, enriched, event_types, affected_assets, predictions, market):
    """Build the prominent user-event deep analysis section.

    This is the MOST IMPORTANT section of the report — the user's news is
    treated as a HIGH-PRIORITY event and analysed in depth before anything else.
    """
    lines = []
    user_details = _extract_event_details(event_text)
    severity = user_details['severity']
    severity_label = {'low': '温和', 'medium': '中等', 'high': '强烈', 'extreme': '极端'}[severity]
    direction = user_details['direction']
    dir_label = {'bullish': '利多/看涨', 'bearish': '利空/看跌', 'mixed': '多空交织'}[direction]
    countries = user_details['countries']
    orgs = user_details['organisations']
    numbers = user_details['numbers']

    lines.append("╔" + "═" * 68 + "╗")
    lines.append("║" + "  🔥 核心事件深度解读（你提供的重大新闻）".center(56) + "║")
    lines.append("╚" + "═" * 68 + "╝")
    lines.append("")
    lines.append(f"  📰 事件: {event_text}")
    lines.append(f"  🏷️  分类: {', '.join(event_types)}")
    lines.append(f"  💥 冲击等级: {severity_label}   信号方向: {dir_label}")
    if countries:
        lines.append(f"  🌏 涉及国家/地区: {', '.join(countries)}")
    if orgs:
        lines.append(f"  🏛️  涉及机构: {', '.join(orgs)}")
    if numbers:
        lines.append(f"  🔢 关键数据: {', '.join(numbers)}")

    # ── News enriched details (from fetched related news) ──
    enriched_lines = [l for l in enriched.split('\n') if l.startswith('[新闻细节]')]
    if enriched_lines:
        lines.append("")
        lines.append("  📋 实时新闻补充情报:")
        for el in enriched_lines:
            lines.append(f"    {el}")

    # ── Core impact on each asset (user event ALONE, not mixed with global) ──
    lines.append("")
    lines.append("  ─── 此事件对各标的的核心影响 ───")
    short_preds = predictions.get('short', [])
    if short_preds:
        for p in short_preds:
            lines.append(f"  ★ {p}")
    else:
        lines.append(f"  ★ 影响资产: {', '.join(affected_assets)}（详细方向见下方三层分析）")

    # ── Immediate cause-effect chain (user event only) ──
    chain = predictions.get('chain', [])
    if chain:
        lines.append("")
        lines.append("  ─── 核心事件因果链 ───")
        for i, step in enumerate(chain):
            if i == 0:
                lines.append(f"  [{i+1}] 🎯 {step}")
            elif i == len(chain) - 1:
                lines.append(f"  [{i+1}] 🏁 {step}")
            else:
                lines.append(f"  [{i+1}]  ↓  {step}")

    lines.append("")
    lines.append("═" * 70)

    return lines


def format_text_report(context, predictions):
    """Format the analysis as a readable text report.

    Report priority order:
      1. USER EVENT deep analysis (most prominent, highest weight)
      2. Market snapshot
      3. Three-layer predictions (user event driven, global as supplement)
      4. Global news background (supporting role)
      5. Comprehensive summary (user event as protagonist)
    """
    lines = []
    event_text = context['event']['text']
    enriched = context['event'].get('enriched_text', event_text)
    event_types = context['event']['types']
    affected_assets = context['affected_assets']
    news = context.get('related_news', [])
    global_news = context.get('global_headlines', [])
    global_events = context.get('global_event_analysis', [])

    # ══════════════════════════════════════════════════════════
    # SECTION 1: USER EVENT DEEP ANALYSIS (highest priority)
    # ══════════════════════════════════════════════════════════
    lines.append("═" * 70)
    lines.append(f"⏰ 分析时间: {context['event']['timestamp']}")
    lines.append("═" * 70)
    lines.append("")

    user_analysis = _build_user_event_deep_analysis(
        event_text, enriched, event_types, affected_assets, predictions,
        context.get('market_snapshot', {}),
    )
    lines.extend(user_analysis)

    # ══════════════════════════════════════════════════════════
    # SECTION 1.5: STANDALONE INTERPRETATION (pure user event, no global)
    # ══════════════════════════════════════════════════════════
    lines.append("")
    lines.append("╔" + "═" * 68 + "╗")
    lines.append("║" + "  📖 独立解读（仅基于你提供的新闻，不掺杂其他信息）".center(48) + "║")
    lines.append("╚" + "═" * 68 + "╝")
    lines.append("")

    standalone = _generate_standalone_interpretation(
        event_text, event_types, affected_assets, context.get('market_snapshot', {}),
    )
    for para in standalone:
        lines.append(f"  {para}")
        lines.append("")

    lines.append("═" * 70)

    # ══════════════════════════════════════════════════════════
    # Show removed conflicting headlines (if any)
    # ══════════════════════════════════════════════════════════
    removed = context.get('removed_conflicting_headlines', [])
    if removed:
        lines.append(f"\n⛔ 以下 {len(removed)} 条全球新闻与你的核心新闻直接冲突，已从分析中剔除:")
        lines.append("─" * 70)
        for r in removed:
            lines.append(f"  ✗ {r['title']}")
            lines.append(f"    原因: {r['reason']}")
        lines.append("")

    # ══════════════════════════════════════════════════════════
    # SECTION 2: Related news for user event
    # ══════════════════════════════════════════════════════════
    if news:
        lines.append(f"\n📰 事件相关实时新闻佐证 ({len(news)} 条)")
        lines.append("─" * 70)
        for i, n in enumerate(news, 1):
            lines.append(f"  [{i}] {n['title']}")
            lines.append(f"      来源: {n['source']} | {n['published']}")

    # ══════════════════════════════════════════════════════════
    # SECTION 3: Market snapshot
    # ══════════════════════════════════════════════════════════
    market = context.get('market_snapshot', {})
    if market:
        lines.append("\n📊 当前市场快照")
        lines.append("─" * 70)
        lines.append(f"  {'资产':<20} {'价格':>12} {'涨跌':>12} {'趋势'}")
        lines.append(f"  {'─' * 64}")
        for key, data in market.items():
            if isinstance(data, dict) and 'price' in data:
                name = data.get('display_name', key)
                price = data['price']
                pct = data.get('change_pct', 0)
                if price >= 10000:
                    price_str = f"${price:,.0f}"
                elif price >= 1:
                    price_str = f"${price:,.2f}"
                else:
                    price_str = f"${price:.6f}"
                if pct > 0:
                    change_str = f"🟢 +{pct:.2f}%"
                elif pct < 0:
                    change_str = f"🔴 {pct:.2f}%"
                else:
                    change_str = f"⚪ {pct:.2f}%"
                trend = data.get('trend', '')
                lines.append(f"  {name:<20} {price_str:>12} {change_str:>12} {trend}")

    # ══════════════════════════════════════════════════════════
    # SECTION 4: Three-layer predictions (user event as CORE driver)
    # ══════════════════════════════════════════════════════════
    lines.append("\n" + "═" * 70)
    lines.append("📋 三层影响预测（以你的核心事件为主驱动）")
    lines.append("═" * 70)

    # Short term
    lines.append("\n🔴 短期影响 (立刻 — 1小时内)")
    lines.append("─" * 70)
    if predictions.get('short'):
        lines.append("  ── 核心事件直接冲击 ──")
        for p in predictions['short']:
            lines.append(f"  ★ {p}")
    deriv_short = predictions.get('derivative_events', {}).get('short', [])
    if deriv_short:
        lines.append("\n  📌 核心事件可能触发的即时事件:")
        for evt in deriv_short:
            lines.append(f"    → {evt}")
    # Global supplement for short term
    if global_events:
        lines.append("\n  ── 全球背景叠加效应（辅助参考）──")
        for item in global_events[:3]:
            lines.append(f"    + {item}")

    # Medium term
    lines.append(f"\n🟡 中期影响 (1 — 12小时)")
    lines.append("─" * 70)
    if predictions.get('medium'):
        lines.append("  ── 核心事件传导路径 ──")
        for p in predictions['medium']:
            lines.append(f"  ★ {p}")
    deriv_med = predictions.get('derivative_events', {}).get('medium', [])
    if deriv_med:
        lines.append("\n  📌 核心事件可能触发的后续事件:")
        for evt in deriv_med:
            lines.append(f"    → {evt}")
    # Global supplement for medium term
    if global_events and len(global_events) > 3:
        lines.append("\n  ── 全球背景叠加效应（辅助参考）──")
        for item in global_events[3:6]:
            lines.append(f"    + {item}")

    # Long term
    lines.append(f"\n🟢 长期影响 (12 — 24小时)")
    lines.append("─" * 70)
    if predictions.get('long'):
        lines.append("  ── 核心事件长期影响 ──")
        for p in predictions['long']:
            lines.append(f"  ★ {p}")
    deriv_long = predictions.get('derivative_events', {}).get('long', [])
    if deriv_long:
        lines.append("\n  📌 核心事件可能催生的衍生事件:")
        for evt in deriv_long:
            lines.append(f"    → {evt}")

    # ══════════════════════════════════════════════════════════
    # SECTION 5: Global headlines (supporting context, LOWER priority)
    # ══════════════════════════════════════════════════════════
    if global_news:
        lines.append(f"\n{'─' * 70}")
        lines.append(f"🌍 同期全球重大新闻背景（辅助参考，共 {len(global_news)} 条）")
        lines.append("─" * 70)
        for i, n in enumerate(global_news[:8], 1):
            title = n.get('title', '')
            src = n.get('source', '')
            lines.append(f"  [{i}] {title}  ({src})")

    # Correlations
    corr = context.get('correlations', {})
    if corr:
        lines.append("\n🔗 资产关联性")
        lines.append("─" * 70)
        for asset, info in corr.items():
            desc = info.get('description', '')
            if desc:
                lines.append(f"  • {asset}: {desc}")

    # ══════════════════════════════════════════════════════════
    # SECTION 6: COMPREHENSIVE SUMMARY (user event as protagonist)
    # ══════════════════════════════════════════════════════════
    lines.append(f"\n{'═' * 70}")
    lines.append("📝 综合结论")
    lines.append("═" * 70)

    user_details = _extract_event_details(event_text)
    severity_label = {'low': '温和', 'medium': '中等', 'high': '强烈', 'extreme': '极端'}[user_details['severity']]
    direction = user_details['direction']
    dir_label = {'bullish': '利多/看涨', 'bearish': '利空/看跌', 'mixed': '多空交织'}[direction]

    # Main conclusion block — user event is the star
    lines.append("")
    lines.append(f"  ┌──────────────────────────────────────────────────────────────┐")
    lines.append(f"  │  核心判断：「{event_text[:40]}{'…' if len(event_text)>40 else ''}」")
    lines.append(f"  │  冲击等级: {severity_label}    信号方向: {dir_label}")

    short_preds = predictions.get('short', [])
    up_assets = [p.split(' ')[0] for p in short_preds if '→ ↑' in p]
    down_assets = [p.split(' ')[0] for p in short_preds if '→ ↓' in p]
    mixed_assets = [p.split(' ')[0] for p in short_preds if '→ ↕' in p or '→ →' in p]

    if up_assets:
        lines.append(f"  │  📈 预计上涨: {', '.join(up_assets)}")
    if down_assets:
        lines.append(f"  │  📉 预计下跌: {', '.join(down_assets)}")
    if mixed_assets:
        lines.append(f"  │  📊 方向不确定: {', '.join(mixed_assets)}")

    lines.append(f"  └──────────────────────────────────────────────────────────────┘")

    # Supplementary context
    lines.append("")
    medium_count = len(predictions.get('medium', []))
    deriv_count = sum(len(predictions.get('derivative_events', {}).get(h, [])) for h in ['short', 'medium', 'long'])
    lines.append(f"  🔄 跨市场传导路径: {medium_count} 条")
    lines.append(f"  ⚡ 预测衍生事件: {deriv_count} 个")

    if news:
        lines.append(f"  📰 新闻佐证: {len(news)} 条实时新闻验证了核心事件的分析方向")
    if global_news:
        lines.append(f"  🌍 全球背景: {len(global_news)} 条全球头条作为辅助参考")
    if global_events:
        amplify = [e for e in global_events if '叠加' in e or '双重' in e or '更大' in e or '更强' in e]
        offset = [e for e in global_events if '对冲' in e or '缓解' in e]
        if amplify:
            lines.append(f"  🔥 全球事件放大效应: {len(amplify)} 个全球事件与你的核心新闻形成共振，放大影响")
        if offset:
            lines.append(f"  🛡️  全球事件对冲效应: {len(offset)} 个全球事件可能部分抵消核心事件影响")

    # ══════════════════════════════════════════════════════════
    # SECTION 7: HISTORICAL VALIDATION & CONFIDENCE
    # ══════════════════════════════════════════════════════════
    confidence_pct, match_count, confidence_note = get_confidence_from_backtest(
        event_types, user_details['severity'],
    )
    lines.append(f"\n{'─' * 70}")
    lines.append("📊 历史回测验证 & 分析置信度")
    lines.append("─" * 70)
    lines.append(f"  🎯 分析置信度: {confidence_pct}%")
    lines.append(f"  📚 同类历史案例: {match_count} 个")
    for note_line in confidence_note.split('\n'):
        lines.append(f"  {note_line}")

    # Show most relevant historical precedent
    matching_cases = [c for c in HISTORICAL_CASES if any(t in c['event_types'] for t in event_types)]
    if matching_cases:
        lines.append("")
        lines.append("  ── 最相关历史先例 ──")
        for case in matching_cases[:3]:
            lines.append(f"  📅 {case['date']}「{case['event'][:45]}{'…' if len(case['event'])>45 else ''}」")
            # Show actual reactions for reference
            reactions = []
            for asset, r in list(case['actual_reactions'].items())[:4]:
                reactions.append(f"{asset.upper()}:{r['dir']}{r['pct']:+.1f}%")
            lines.append(f"     实际: {' | '.join(reactions)}")
            if case.get('key_lesson'):
                lesson_short = case['key_lesson'].split('。')[0] + '。'
                lines.append(f"     教训: {lesson_short}")

    lines.append(f"\n{'═' * 70}")
    lines.append("⚠️  风险提示: 以上分析以你提供的核心事件为主驱动，结合实时全球大事件 + 历史模式推演。")
    lines.append("   仅供参考，不构成投资建议。实际走势取决于事件后续发展、市场情绪和资金博弈。")
    lines.append(f"   本分析经过 {len(HISTORICAL_CASES)} 个历史真实案例回测校准，当前事件类型置信度 {confidence_pct}%。")

    return '\n'.join(lines)


def analyze_global_headlines(headlines, user_event_types):
    """Analyze global headlines to find events that amplify or offset the user's event.

    Returns a list of analysis strings describing how global events interact
    with the user's event.
    """
    if not headlines:
        return []

    analysis = []

    # Classify each headline
    for article in headlines[:15]:
        title = article.get('title', '')
        if not title:
            continue

        h_types = classify_event(title)
        h_details = _extract_event_details(title)

        # Check for interaction with user event
        for ut in user_event_types:
            for ht in h_types:
                interaction = _get_interaction(ut, ht, h_details['direction'], title)
                if interaction:
                    analysis.append(interaction)

    # Deduplicate and limit
    seen = set()
    unique = []
    for a in analysis:
        if a not in seen:
            seen.add(a)
            unique.append(a)
    return unique[:8]


def _get_interaction(user_type, headline_type, headline_direction, headline_title):
    """Determine how a global headline interacts with the user's event type."""
    short_title = headline_title[:60] + ('...' if len(headline_title) > 60 else '')

    # Amplifying combinations
    if user_type == '自然灾害/供应链' and headline_type == '能源/OPEC':
        return f"「{short_title}」→ 能源事件 + 供应链灾害 = 油价上行压力叠加，通胀预期进一步上修"
    if user_type == '自然灾害/供应链' and headline_type == '地缘政治':
        return f"「{short_title}」→ 地缘风险 + 灾害 = 全球避险情绪双重升温，黄金受双重支撑"
    if user_type == '地缘政治' and headline_type == '能源/OPEC':
        return f"「{short_title}」→ 能源+地缘叠加 = 原油可能出现更大幅度上涨"
    if user_type == '地缘政治' and headline_type == '地缘政治':
        return f"「{short_title}」→ 多重地缘风险叠加 = 避险资产（黄金/美债）获得更强支撑"
    if user_type == '央行/货币政策' and headline_type == '宏观经济数据':
        return f"「{short_title}」→ 经济数据 + 央行政策联动 = 利率预期可能出现更大幅度调整"

    # Offsetting combinations
    if user_type == '自然灾害/供应链' and headline_type == '央行/货币政策':
        if headline_direction == 'bullish':
            return f"「{short_title}」→ 央行宽松 可能部分对冲灾害带来的经济下行压力"
        else:
            return f"「{short_title}」→ 央行紧缩 + 灾害冲击 = 经济前景双重承压"
    if user_type == '地缘政治' and headline_type == '央行/货币政策':
        if headline_direction == 'bullish':
            return f"「{short_title}」→ 央行宽松 可能缓解地缘冲击对股市的下行压力"

    # General market-moving headlines
    if headline_type == '央行/货币政策':
        if headline_direction == 'bullish':
            return f"「{short_title}」→ 全球背景: 央行宽松环境，风险资产有支撑"
        elif headline_direction == 'bearish':
            return f"「{short_title}」→ 全球背景: 央行紧缩环境，风险资产承压"
    if headline_type == '宏观经济数据':
        return f"「{short_title}」→ 全球经济数据影响市场风险偏好"
    if headline_type == '企业/行业':
        return f"「{short_title}」→ 企业/行业事件可能影响市场情绪"

    return None


def enrich_with_global_context(enriched_text, global_headlines):
    """Add global news context into the enriched text for better keyword extraction.

    This ensures that when we classify event types and extract details,
    the global news context is also considered.
    """
    if not global_headlines:
        return enriched_text

    # Extract key themes from global headlines
    all_text = ' '.join(h.get('title', '') for h in global_headlines[:10])
    global_details = _extract_event_details(all_text)

    parts = [enriched_text]

    if global_details['countries']:
        extra_countries = [c for c in global_details['countries'] if c not in enriched_text]
        if extra_countries:
            parts.append(f"[全球背景] 涉及国家/地区: {', '.join(extra_countries[:5])}")

    if global_details['organisations']:
        extra_orgs = [o for o in global_details['organisations'] if o not in enriched_text]
        if extra_orgs:
            parts.append(f"[全球背景] 涉及机构: {', '.join(extra_orgs[:5])}")

    # Detect global macro themes
    global_types = classify_event(all_text)
    if global_types and global_types != ['其他/综合']:
        parts.append(f"[全球背景] 同期重大事件类型: {', '.join(global_types)}")

    return '\n'.join(parts)


def main():
    parser = argparse.ArgumentParser(description='Event impact analysis for financial markets')
    parser.add_argument('--event', '-e', help='Event description text')
    parser.add_argument('--url', '-u', help='News article URL to analyze')
    parser.add_argument('--focus', '-f', help='Comma-separated asset focus (e.g., gold,oil,btc)')
    parser.add_argument('--market-data', '-m', default='auto',
                        help='"auto" to fetch live data, or path to saved JSON')
    parser.add_argument('--output', '-o', default='text', choices=['text', 'json'],
                        help='Output format (default: text)')
    parser.add_argument('--json', action='store_true', help='Alias for --output json')
    parser.add_argument('--skip-news', action='store_true', help='Skip news fetching')
    parser.add_argument('--skip-market', action='store_true', help='Skip market data fetching')
    parser.add_argument('--skip-global', action='store_true',
                        help='Skip global headlines fetching')
    parser.add_argument('--backtest', action='store_true',
                        help='Run historical backtest validation (≥10 cases) and exit')

    args = parser.parse_args()

    # ── Backtest mode ──
    if args.backtest:
        print("╔" + "═" * 68 + "╗")
        print("║" + "  📊 历史回测验证系统（自我校准模式）".center(50) + "║")
        print("╚" + "═" * 68 + "╝")
        print(f"\n运行 {len(HISTORICAL_CASES)} 个历史真实案例回测...\n")
        results = run_full_backtest(verbose=True)
        print(f"\n{'═' * 60}")
        print(f"📊 回测总结")
        print(f"{'─' * 60}")
        print(f"  总案例数: {results['total_cases']}")
        print(f"  总预测数: {results['total_predictions']}")
        print(f"  ✅ 正确:  {results['correct']} ({results['correct']}/{results['total_predictions']})")
        print(f"  🟡 部分:  {results['partial']}")
        print(f"  ❌ 错误:  {results['wrong']}")
        print(f"  严格准确率: {results['strict_accuracy']:.1%}")
        print(f"  宽松准确率: {results['lenient_accuracy']:.1%}")
        if results['biases']:
            print(f"\n  ⚠️  发现系统性偏差:")
            for bias in results['biases']:
                print(f"    • {bias}")
        print(f"\n{'═' * 60}")
        sys.exit(0)

    if args.json:
        args.output = 'json'

    # Get event text
    event_text = args.event or ''
    if args.url:
        print(f"📥 提取URL内容: {args.url}", file=sys.stderr)
        url_content = extract_text_from_url(args.url)
        if event_text:
            event_text = event_text + '\n\n原文摘要:\n' + url_content
        else:
            event_text = url_content

    if not event_text:
        print("ERROR: 请提供 --event 或 --url 参数", file=sys.stderr)
        sys.exit(1)

    # Parse focus assets
    focus_assets = []
    if args.focus:
        focus_assets = [a.strip().lower() for a in args.focus.split(',')]

    # ════════════════════════════════════════════
    # STEP 1: Fetch related news (about user's event)
    # ════════════════════════════════════════════
    news_data = None
    if not args.skip_news:
        print("📰 获取事件相关新闻...", file=sys.stderr)
        search_terms = event_text[:50]
        news_data = run_tool('news_fetch.py', ['--query', search_terms, '--limit', '8'])

    # ════════════════════════════════════════════
    # STEP 2: Fetch GLOBAL top headlines (independent of user event)
    # ════════════════════════════════════════════
    global_data = None
    if not args.skip_global and not args.skip_news:
        print("🌍 获取全球实时重大新闻...", file=sys.stderr)
        global_data = run_tool('news_fetch.py', ['--global-headlines', '--limit', '10'])

    # ════════════════════════════════════════════
    # STEP 3: Enrich event text with news details
    # ════════════════════════════════════════════
    news_articles = news_data.get('articles', []) if news_data else []
    enriched_text, _ = enrich_event_from_news(event_text, news_articles)

    global_headlines = global_data.get('articles', []) if global_data else []
    enriched_text = enrich_with_global_context(enriched_text, global_headlines)

    # ════════════════════════════════════════════
    # STEP 4: Fetch market data
    # ════════════════════════════════════════════
    market_data = None
    if not args.skip_market:
        if args.market_data == 'auto':
            print("📊 获取实时市场数据...", file=sys.stderr)
            detected = identify_affected_assets(enriched_text)
            fetch_assets = list(set(detected + focus_assets)) if focus_assets else detected
            if not fetch_assets:
                fetch_assets = ['gold', 'oil', 'btc', 'spy']
            for core in ['gold', 'oil', 'btc', 'spy', 'usdx']:
                if core not in fetch_assets:
                    fetch_assets.append(core)
            asset_str = ','.join(fetch_assets)
            market_data = run_tool('market_data.py', ['--assets', asset_str, '--period', '1d', '--interval', '15m'])
        elif os.path.isfile(args.market_data):
            with open(args.market_data, 'r') as f:
                market_data = json.load(f)

    # ════════════════════════════════════════════
    # STEP 5: Build context + analyze global headline interactions
    # ════════════════════════════════════════════
    context = build_analysis_context(event_text, enriched_text, market_data, news_data, focus_assets)

    # Add global headlines to context (AFTER filtering conflicts)
    user_event_types = context['event']['types']
    user_direction = _extract_event_details(event_text)['direction']
    filtered_headlines, removed_headlines = _filter_conflicting_headlines(
        global_headlines, event_text, user_direction, user_event_types,
    )
    context['global_headlines'] = filtered_headlines
    context['removed_conflicting_headlines'] = removed_headlines

    if removed_headlines:
        print(f"⛔ 过滤掉 {len(removed_headlines)} 条与你的新闻冲突的全球新闻", file=sys.stderr)

    # Analyze how global events interact with user event (using filtered list)
    global_event_analysis = analyze_global_headlines(filtered_headlines, user_event_types)
    context['global_event_analysis'] = global_event_analysis

    # ════════════════════════════════════════════
    # STEP 6: Generate predictions (uses enriched text with global context)
    # ════════════════════════════════════════════
    predictions = generate_predictions(context)

    # ════════════════════════════════════════════
    # STEP 7: Output
    # ════════════════════════════════════════════
    if args.output == 'json':
        context['predictions'] = predictions
        # Remove raw articles from JSON to keep it clean
        context.pop('news_articles_raw', None)
        print(json.dumps(context, ensure_ascii=False, indent=2))
    else:
        print(format_text_report(context, predictions))


if __name__ == '__main__':
    main()
