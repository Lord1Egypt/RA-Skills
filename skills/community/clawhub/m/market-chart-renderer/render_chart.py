#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUTDIR = ROOT / 'output' / 'generated' / 'images'
OUTDIR.mkdir(parents=True, exist_ok=True)

AKSHARE_SKILL_DIR = ROOT / 'skills' / 'akshare-futures-options-data'
if str(AKSHARE_SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(AKSHARE_SKILL_DIR))

from akshare_router_cn import build_chart_payload  # noqa: E402

MA_SPECS = [
    ('ma5', 'MA5', '#f59e0b'),
    ('ma10', 'MA10', '#a855f7'),
    ('ma20', 'MA20', '#60a5fa'),
    ('ma60', 'MA60', '#22d3ee'),
]
MACD_COLORS = {
    'dif': '#38bdf8',
    'dea': '#f97316',
    'hist_pos': '#ef4444',
    'hist_neg': '#22c55e',
}
CHROME_CANDIDATES = ['google-chrome', 'chromium', 'chromium-browser']


def _series(df: pd.DataFrame, col: str) -> pd.Series:
    return pd.to_numeric(df[col], errors='coerce')


def _resolve_chrome_binary() -> str | None:
    for name in CHROME_CANDIDATES:
        found = shutil.which(name)
        if found:
            return found
    return None


def runtime_env_check() -> dict[str, Any]:
    chrome = _resolve_chrome_binary()
    return {
        'ok': bool(chrome),
        'chrome_binary': chrome,
        'png_supported': bool(chrome),
        'warnings': [] if chrome else ['未找到 google-chrome/chromium/chromium-browser，当前环境仅支持 HTML/JSON 导出；可改用 --no-png'],
    }


def apply_indicators(bars: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(bars).copy()
    if df.empty:
        return df
    df['bar_time'] = pd.to_datetime(df['bar_time'])
    close = _series(df, 'close')
    for window in (5, 10, 20, 60):
        df[f'ma{window}'] = close.rolling(window).mean()
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    df['macd_dif'] = ema12 - ema26
    df['macd_dea'] = df['macd_dif'].ewm(span=9, adjust=False).mean()
    df['macd_hist'] = (df['macd_dif'] - df['macd_dea']) * 2
    return df


def build_payload(chart_input: dict[str, Any], limit: int = 120) -> dict[str, Any]:
    df = apply_indicators(chart_input['bars'])
    work = df.tail(limit).copy().reset_index(drop=True)
    work = work.where(pd.notnull(work), None)
    category = [pd.to_datetime(v).strftime('%m-%d %H:%M') for v in work['bar_time']]
    candle = work[['open', 'close', 'low', 'high']].values.tolist()
    volume = [0 if v is None else float(v) for v in work['volume'].tolist()]
    ma = {
        col: [None if pd.isna(v) else float(v) for v in pd.to_numeric(work[col], errors='coerce').tolist()]
        for col, _, _ in MA_SPECS
        if col in work.columns
    }
    dif = [None if pd.isna(v) else float(v) for v in pd.to_numeric(work['macd_dif'], errors='coerce').tolist()]
    dea = [None if pd.isna(v) else float(v) for v in pd.to_numeric(work['macd_dea'], errors='coerce').tolist()]
    hist_raw = pd.to_numeric(work['macd_hist'], errors='coerce').tolist()
    hist = []
    for v in hist_raw:
        if pd.isna(v):
            hist.append({'value': None})
        else:
            num = float(v)
            hist.append({
                'value': num,
                'itemStyle': {'color': MACD_COLORS['hist_pos'] if num >= 0 else MACD_COLORS['hist_neg']},
            })
    instrument = chart_input['instrument']
    last = work.iloc[-1].to_dict() if len(work) else {}
    for key, value in list(last.items()):
        if isinstance(value, pd.Timestamp):
            last[key] = value.isoformat()
    return {
        'contract': instrument['contract'],
        'product': instrument['product'],
        'freq': instrument['freq'],
        'exchange': instrument.get('exchange'),
        'source': chart_input.get('source'),
        'quality': chart_input.get('quality'),
        'meta': {'bar_count': len(work)},
        'categoryData': category,
        'candles': candle,
        'volume': volume,
        'ma': ma,
        'macd': {'dif': dif, 'dea': dea, 'hist': hist},
        'last': last,
    }


def build_option(payload: dict[str, Any]) -> dict[str, Any]:
    legend = [label for _, label, _ in MA_SPECS] + ['DIF', 'DEA', 'MACD']
    ma_series = []
    for col, label, color in MA_SPECS:
        if col not in payload['ma']:
            continue
        ma_series.append({
            'name': label,
            'type': 'line',
            'data': payload['ma'][col],
            'showSymbol': False,
            'smooth': False,
            'lineStyle': {'width': 1.6, 'color': color},
            'emphasis': {'disabled': True},
            'xAxisIndex': 0,
            'yAxisIndex': 0,
        })
    return {
        'backgroundColor': '#0b1220',
        'animation': False,
        'title': [
            {
                'text': f"{payload['product']}  {payload['contract']}  {payload['freq']}",
                'left': 20,
                'top': 12,
                'textStyle': {'color': '#e5e7eb', 'fontSize': 24, 'fontWeight': 'bold'},
            },
            {
                'text': (
                    f"最新  O:{payload['last'].get('open')}  H:{payload['last'].get('high')}  "
                    f"L:{payload['last'].get('low')}  C:{payload['last'].get('close')}  "
                    f"VOL:{payload['last'].get('volume')}"
                ),
                'left': 20,
                'top': 44,
                'textStyle': {'color': '#94a3b8', 'fontSize': 12, 'fontWeight': 'normal'},
            },
        ],
        'legend': {
            'top': 72,
            'left': 20,
            'itemWidth': 24,
            'itemHeight': 10,
            'textStyle': {'color': '#cbd5e1', 'fontSize': 12},
            'data': legend,
        },
        'tooltip': {'trigger': 'axis', 'axisPointer': {'type': 'cross'}},
        'axisPointer': {'link': [{'xAxisIndex': 'all'}], 'label': {'backgroundColor': '#334155'}},
        'grid': [
            {'left': 60, 'right': 50, 'top': 110, 'height': 470},
            {'left': 60, 'right': 50, 'top': 620, 'height': 170},
        ],
        'xAxis': [
            {
                'type': 'category',
                'data': payload['categoryData'],
                'boundaryGap': True,
                'axisLine': {'lineStyle': {'color': '#475569'}},
                'axisLabel': {'show': False},
                'axisTick': {'show': False},
                'splitLine': {'show': False},
                'min': 'dataMin',
                'max': 'dataMax',
            },
            {
                'type': 'category',
                'gridIndex': 1,
                'data': payload['categoryData'],
                'boundaryGap': True,
                'axisLine': {'lineStyle': {'color': '#475569'}},
                'axisLabel': {
                    'color': '#cbd5e1',
                    'rotate': 0,
                    'showMinLabel': True,
                    'showMaxLabel': True,
                    'margin': 12,
                },
                'axisTick': {'show': True},
                'splitLine': {'show': False},
                'min': 'dataMin',
                'max': 'dataMax',
            },
        ],
        'yAxis': [
            {
                'scale': True,
                'splitArea': {'show': False},
                'axisLine': {'lineStyle': {'color': '#475569'}},
                'splitLine': {'lineStyle': {'color': '#1f2937'}},
                'axisLabel': {'color': '#94a3b8'},
            },
            {
                'scale': True,
                'gridIndex': 1,
                'axisLine': {'lineStyle': {'color': '#475569'}},
                'splitLine': {'lineStyle': {'color': '#1f2937'}},
                'axisLabel': {'color': '#94a3b8'},
            },
        ],
        'graphic': [
            {'type': 'text', 'left': 72, 'top': 628, 'style': {'text': 'MACD', 'fill': '#94a3b8', 'font': '12px sans-serif'}},
        ],
        'dataZoom': [
            {'type': 'inside', 'xAxisIndex': [0, 1], 'start': 0, 'end': 100},
            {'show': False, 'type': 'slider', 'xAxisIndex': [0, 1], 'start': 0, 'end': 100},
        ],
        'series': [
            {
                'name': 'K线',
                'type': 'candlestick',
                'data': payload['candles'],
                'itemStyle': {
                    'color': '#ef4444',
                    'color0': '#22c55e',
                    'borderColor': '#ef4444',
                    'borderColor0': '#22c55e',
                },
                'xAxisIndex': 0,
                'yAxisIndex': 0,
            },
            {
                'name': 'MACD',
                'type': 'bar',
                'xAxisIndex': 1,
                'yAxisIndex': 1,
                'data': payload['macd']['hist'],
                'barWidth': '55%',
            },
            {
                'name': 'DIF',
                'type': 'line',
                'xAxisIndex': 1,
                'yAxisIndex': 1,
                'data': payload['macd']['dif'],
                'showSymbol': False,
                'lineStyle': {'width': 1.8, 'color': MACD_COLORS['dif']},
            },
            {
                'name': 'DEA',
                'type': 'line',
                'xAxisIndex': 1,
                'yAxisIndex': 1,
                'data': payload['macd']['dea'],
                'showSymbol': False,
                'lineStyle': {'width': 1.8, 'color': MACD_COLORS['dea']},
            },
        ] + ma_series,
    }


def build_html(payload: dict[str, Any]) -> str:
    option = build_option(payload)
    option_json = json.dumps(option, ensure_ascii=False)
    payload_json = json.dumps(payload, ensure_ascii=False)
    return f'''<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Market Chart Renderer</title>
  <style>
    html, body {{ margin: 0; width: 1400px; height: 900px; background: #0b1220; overflow: hidden; }}
    #chart {{ width: 1400px; height: 900px; }}
  </style>
  <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
</head>
<body>
  <div id="chart"></div>
  <script>
    window.__PAYLOAD__ = {payload_json};
    const chart = echarts.init(document.getElementById('chart'), null, {{ renderer: 'canvas' }});
    const option = {option_json};
    chart.setOption(option);
    window.__ECHARTS_DONE__ = true;
  </script>
</body>
</html>'''


def render_png(html_path: Path, png_path: Path, width: int = 1400, height: int = 900) -> str:
    chrome_binary = _resolve_chrome_binary()
    if not chrome_binary:
        raise RuntimeError('chrome binary not found; use --no-png or install google-chrome/chromium')
    cmd = [
        chrome_binary,
        '--headless=new',
        '--disable-gpu',
        '--hide-scrollbars',
        f'--window-size={width},{height}',
        '--run-all-compositor-stages-before-draw',
        '--virtual-time-budget=4000',
        f'--screenshot={png_path}',
        html_path.resolve().as_uri(),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return chrome_binary


def render_chart(symbol: str, period: str, limit: int = 120, output_stem: str | None = None, write_png: bool = True) -> dict[str, Any]:
    chart_input = build_chart_payload(query=symbol, period=period)
    payload = build_payload(chart_input, limit=limit)
    stem = output_stem or f"{symbol.lower()}_{period}m_market_chart_renderer"
    base = OUTDIR / stem
    json_path = base.with_suffix('.json')
    html_path = base.with_suffix('.html')
    png_path = base.with_suffix('.png')
    env = runtime_env_check()
    html_path.write_text(build_html(payload), encoding='utf-8')
    json_path.write_text(json.dumps({'chart_input': chart_input, 'payload': payload}, ensure_ascii=False, indent=2), encoding='utf-8')
    png_written = False
    if write_png:
        chrome_binary = render_png(html_path, png_path)
        env['chrome_binary'] = chrome_binary
        png_written = True
    return {
        'ok': True,
        'symbol': symbol,
        'period': f'{period}m',
        'html_path': str(html_path),
        'png_path': str(png_path) if write_png else None,
        'json_path': str(json_path),
        'source': chart_input.get('source'),
        'quality': chart_input.get('quality'),
        'bar_count': payload['meta']['bar_count'],
        'png_written': png_written,
        'env': env,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Render market chart with ECharts + MACD subpanel')
    parser.add_argument('--symbol', default='MA0')
    parser.add_argument('--period', default='60', help='minute period, e.g. 60')
    parser.add_argument('--limit', type=int, default=120)
    parser.add_argument('--output-stem', default=None)
    parser.add_argument('--no-png', action='store_true', help='only export HTML/JSON, skip headless Chrome screenshot')
    parser.add_argument('--check-env', action='store_true', help='print runtime dependency check and exit')
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.check_env:
        print(json.dumps(runtime_env_check(), ensure_ascii=False, indent=2))
        return 0
    result = render_chart(
        symbol=args.symbol,
        period=str(args.period),
        limit=args.limit,
        output_stem=args.output_stem,
        write_png=not args.no_png,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
