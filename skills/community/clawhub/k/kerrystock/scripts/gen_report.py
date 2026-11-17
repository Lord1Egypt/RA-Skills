#!/usr/bin/env python3
"""Kerrystock 步骤4：生成「日历效应 + 买卖点」可视化 HTML 研报。

从 seasonal_stats.json 读季节性统计；从日线 CSV 自行计算当前技术截面
(MACD/KDJ/RSI/BOLL)，无需再解析 westock 的 markdown 输出。配色遵守中国习惯：
涨=红(#d4380d)、跌=绿(#18940f)；"买入窗口"=绿、"回避窗口"=红。

用法:
  python3 gen_report.py --stats seasonal_stats.json --daycsv 601138_day.csv \\
        --name 工业富联 --code sh601138 --out 研报.html
"""
import argparse
import json
import os

import pandas as pd


# ---------- 技术指标（自算，标准公式） ----------
def _rsi(close: pd.Series, n: int) -> float:
    d = close.diff()
    g = d.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    l = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    rs = g / l
    return float((100 - 100 / (1 + rs)).iloc[-1])


def calc_tech(df: pd.DataFrame) -> dict:
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)
    # 纯净值序列兼容：缺失 high/low 用 close 填充，KDJ 仍可计算
    if "high" not in df.columns or df["high"].isna().all():
        df["high"] = df["close"]
    if "low" not in df.columns or df["low"].isna().all():
        df["low"] = df["close"]
    close = df["close"]

    # BOLL(20) — 用总体标准差(ddof=0)与主流行情软件口径一致
    ma20 = close.rolling(20).mean()
    sd = close.rolling(20).std(ddof=0)
    boll_m = float(ma20.iloc[-1])
    boll_u = float((ma20 + 2 * sd).iloc[-1])
    boll_l = float((ma20 - 2 * sd).iloc[-1])

    # MACD(12,26,9)
    e12 = close.ewm(span=12, adjust=False).mean()
    e26 = close.ewm(span=26, adjust=False).mean()
    dif = e12 - e26
    dea = dif.ewm(span=9, adjust=False).mean()
    macd = float((2 * (dif - dea)).iloc[-1])

    # KDJ(9)
    low9 = df["low"].rolling(9).min()
    high9 = df["high"].rolling(9).max()
    rsv = (close - low9) / (high9 - low9) * 100
    rsv = rsv.fillna(50)
    K = rsv.ewm(alpha=1 / 3, adjust=False).mean().fillna(50)
    D = K.ewm(alpha=1 / 3, adjust=False).mean().fillna(50)
    J = 3 * K - 2 * D

    return {
        "close": round(float(close.iloc[-1]), 3),
        "boll_u": round(boll_u, 3), "boll_m": round(boll_m, 3), "boll_l": round(boll_l, 3),
        "dif": round(float(dif.iloc[-1]), 4), "dea": round(float(dea.iloc[-1]), 4), "macd": round(macd, 4),
        "k": round(float(K.iloc[-1]), 2), "d": round(float(D.iloc[-1]), 2), "j": round(float(J.iloc[-1]), 2),
        "rsi2": round(_rsi(close, 2), 2), "rsi6": round(_rsi(close, 6), 2),
        "rsi12": round(_rsi(close, 12), 2), "rsi24": round(_rsi(close, 24), 2),
    }


def build_html(stats: dict, tech: dict, name: str, code: str, price_label: str = "收盘") -> str:
    months = list(range(1, 13))
    mean = [round(stats["monthly"][str(m)]["mean"] * 100, 2) for m in months]
    win = [round(stats["monthly"][str(m)]["win_rate"] * 100, 1) for m in months]
    n = [stats["monthly"][str(m)]["n"] for m in months]
    bull = stats["bull"]
    bear = stats["bear"]
    years = sorted(int(y) for y in stats["yearly"].keys())
    yret = [round(stats["yearly"][str(y)] * 100, 2) for y in years]

    last = tech["close"]
    peak = stats["peak"]
    peak_date = stats["peak_date"]
    from_peak = round((last / peak - 1) * 100, 1)
    trough = stats["trough"]
    trough_date = stats["trough_date"]

    cal = [1 if m in bull else (-1 if m in bear else 0) for m in months]

    bull_tag = " ".join(f'<span class="tag t-buy">{m}月</span>' for m in bull) or "—"
    bear_tag = " ".join(f'<span class="tag t-sell">{m}月</span>' for m in bear) or "—"

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name}({code}) 日历效应与买卖点策略</title>
<script src="https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js"></script>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif;
    background: #f5f6f8; color: #1f2329; line-height: 1.6; }}
  .wrap {{ max-width: 1080px; margin: 0 auto; padding: 24px 16px 60px; }}
  h1 {{ font-size: 26px; font-weight: 700; margin-bottom: 4px; }}
  .sub {{ color: #646a73; font-size: 13px; margin-bottom: 20px; }}
  .card {{ background: #fff; border-radius: 12px; padding: 20px; margin-bottom: 18px;
    box-shadow: 0 1px 4px rgba(0,0,0,.06); }}
  .card h2 {{ font-size: 17px; margin-bottom: 14px; display:flex; align-items:center; gap:8px; }}
  .card h2::before {{ content:''; width:4px; height:16px; background:#d4380d; border-radius:2px; }}
  .kpis {{ display:grid; grid-template-columns:repeat(4,1fr); gap:12px; }}
  .kpi {{ background:#fafbfc; border:1px solid #eef0f2; border-radius:10px; padding:14px; }}
  .kpi .v {{ font-size:21px; font-weight:700; }}
  .kpi .l {{ font-size:12px; color:#646a73; margin-top:2px; }}
  .red {{ color:#d4380d; }} .green {{ color:#18940f; }} .gray {{ color:#646a73; }}
  .chart {{ width:100%; height:340px; }}
  .legend {{ font-size:12px; color:#646a73; margin-top:8px; }}
  table {{ width:100%; border-collapse:collapse; font-size:13px; }}
  th,td {{ padding:9px 10px; text-align:left; border-bottom:1px solid #eef0f2; }}
  th {{ background:#fafbfc; color:#646a73; font-weight:600; }}
  .tag {{ display:inline-block; padding:2px 8px; border-radius:6px; font-size:12px; font-weight:600; }}
  .t-buy {{ background:#e8f7e8; color:#18940f; }}
  .t-sell {{ background:#fdecea; color:#d4380d; }}
  .t-wait {{ background:#f0f1f2; color:#646a73; }}
  .note {{ font-size:13px; color:#3a3f47; }}
  .note li {{ margin:6px 0 6px 18px; }}
  .warn {{ background:#fff8e6; border:1px solid #ffe09a; border-radius:10px; padding:14px; font-size:12.5px; color:#7a5a00; }}
  .foot {{ font-size:11.5px; color:#969aa3; margin-top:24px; text-align:center; }}
</style>
</head>
<body>
<div class="wrap">
  <h1>{name} ({code}) 日历效应与买卖点策略</h1>
  <div class="sub">数据区间 {stats['date_range'][0]} 至 {stats['date_range'][1]}（前复权）｜ 工具链：westock-data + neodata + wb-finance-skill·seasonality ｜ Kerrystock 技能生成</div>

  <div class="card">
    <div class="kpis">
      <div class="kpi"><div class="v">{last}</div><div class="l">最新{price_label}</div></div>
      <div class="kpi"><div class="v red">{from_peak}%</div><div class="l">距历史高点 {peak} ({peak_date})</div></div>
      <div class="kpi"><div class="v green">{tech['rsi2']}</div><div class="l">RSI(2) 超卖阈值&lt;10</div></div>
      <div class="kpi"><div class="v gray">▲{','.join(map(str,bull))} ▼{','.join(map(str,bear))}</div><div class="l">统计显著做多/回避月</div></div>
    </div>
  </div>

  <div class="card">
    <h2>一、月度日历效应（季节性，基于本标的自身历史）</h2>
    <div id="monthChart" class="chart"></div>
    <div class="legend">柱=该月平均涨跌幅（红涨绿跌）；折线=历史胜率（%）。▲多=统计显著做多月（胜率≥{int(stats['win_thresh']*100)}%且均值&gt;0）；▼空=统计显著回避月（胜率≤{int(stats['lose_thresh']*100)}%且均值&lt;0）。样本数 n 见下表，n 过小则置信度低。</div>
  </div>

  <div class="card">
    <h2>二、年度收益规律</h2>
    <div id="yearChart" class="chart"></div>
    <div class="legend">年度收益反映标的的强周期/强趋势属性，是判断「日历效应权重」的关键——强趋势标的须以趋势/业绩为主、日历为辅。</div>
  </div>

  <div class="card">
    <h2>三、买卖时间点日历</h2>
    <div id="calChart" class="chart" style="height:160px;"></div>
    <div class="legend">绿色=建议买入/持有窗口（{bull_tag}）｜ 红色=建议减仓/回避窗口（{bear_tag}）｜ 灰色=中性观望。</div>
  </div>

  <div class="card">
    <h2>四、当前技术面截面</h2>
    <div class="kpis" style="grid-template-columns:repeat(3,1fr);">
      <div class="kpi"><div class="v red">{tech['macd']}</div><div class="l">MACD 柱</div></div>
      <div class="kpi"><div class="v red">{tech['j']}</div><div class="l">KDJ·J（&lt;10 超卖）</div></div>
      <div class="kpi"><div class="v gray">{tech['rsi6']} / {tech['rsi12']}</div><div class="l">RSI(6) / RSI(12)</div></div>
      <div class="kpi"><div class="v gray">{tech['boll_l']}</div><div class="l">BOLL 下轨</div></div>
      <div class="kpi"><div class="v gray">{tech['boll_m']}</div><div class="l">BOLL 中轨</div></div>
      <div class="kpi"><div class="v gray">{tech['boll_u']}</div><div class="l">BOLL 上轨</div></div>
    </div>
    <div class="note" style="margin-top:10px;">结论：最新{price_label} {tech['close']}，距高点 {peak} 回撤 {from_peak}%；
      RSI(2)={tech['rsi2']}{'（极度超卖）' if tech['rsi2']<10 else ''}、
      KDJ·J={tech['j']}{'（超卖）' if tech['j']<10 else ''}、
      收盘价{'已触及' if abs(tech['close']-tech['boll_l'])/tech['boll_l']<0.02 else '接近'} BOLL 下轨 {tech['boll_l']}。
      短期存在{'超跌反弹动能' if (tech['rsi2']<20 or tech['j']<20) else '震荡动能'}；但 MACD 柱 {('空头' if tech['macd']<0 else '多头')}排列，趋势{'未扭转' if tech['macd']<0 else '已转强'}。</div>
  </div>

  <div class="card">
    <h2>五、买卖策略框架（trade-plan 方法论）</h2>
    <table>
      <tr><th>要素</th><th>建议</th></tr>
      <tr><td>当前位置判断</td><td>依据技术截面自行判断（超卖区/趋势中/高位区），禁止套用模板</td></tr>
      <tr><td>试错仓（左侧）</td><td>若处超卖区先建 10–15% 观察仓，分批不梭哈</td></tr>
      <tr><td>确认加仓信号</td><td>放量站上 BOLL 中轨 {tech['boll_m']} 且 MACD 金叉（DIF 上穿 DEA）→ 加至 30–50%</td></tr>
      <tr><td>最佳做多窗口</td><td>{bull_tag or '（无统计显著做多月）'}</td></tr>
      <tr><td>减仓/回避窗口</td><td>{bear_tag or '（无统计显著回避月）'}</td></tr>
      <tr><td>止损位</td><td>有效跌破 BOLL 下轨 {tech['boll_l']} 且放量 → 判断反弹失效，试错仓离场</td></tr>
      <tr><td>止盈位</td><td>第一目标 BOLL 中轨 {tech['boll_m']}；强趋势可看前高 {peak} 区域分批兑现</td></tr>
      <tr><td>失效条件</td><td>跌破 {tech['boll_l']} 且 MACD 未金叉 / 业绩或行业逻辑证伪 → 放弃做多，转观望</td></tr>
    </table>
  </div>

  <div class="card">
    <h2>六、月度统计明细（含样本 n）</h2>
    <table>
      <tr><th>月份</th><th>样本数 n</th><th>胜率</th><th>平均涨跌幅</th><th>中位涨跌幅</th><th>判定</th></tr>
      {''.join(f"<tr><td>{m}月</td><td>{n[m-1]}</td><td>{win[m-1]}%</td><td class='{'red' if mean[m-1]>=0 else 'green'}'>{mean[m-1]}%</td><td class='{'red' if stats['monthly'][str(m)]['median']>=0 else 'green'}'>{round(stats['monthly'][str(m)]['median']*100,2)}%</td><td>{'<span class=\"tag t-buy\">做多</span>' if m in bull else ('<span class=\"tag t-sell\">回避</span>' if m in bear else '<span class=\"tag t-wait\">中性</span>')}</td></tr>" for m in months)}
    </table>
  </div>

  <div class="warn">
    ⚠️ 风险提示：本研报基于标的自身历史数据量化「日历效应」，但季节性是辅助规律、非主信号。
    强趋势/强基本面标的（如 AI、周期龙头）须以「业绩+趋势+事件」为主、日历规律为辅。
    历史季节性不代表未来必然重复。本研报为分析框架，<b>不构成投资建议</b>；具体操作需结合个人风险偏好、仓位与持有期限。
  </div>

  <div class="foot">数据来源：腾讯自选股（westock-data）｜ NeoData 历史走势与研报 ｜ 季节性信号引擎 wb-finance-skill·seasonality.py ｜ Kerrystock 技能生成</div>
</div>

<script>
const months = {months};
const mean = {mean};
const win = {win};
const bull = {bull}, bear = {bear};
const years = {years};
const yret = {yret};
const cal = {cal};

function col(v){{ return v>=0 ? '#d4380d' : '#18940f'; }}

const mc = echarts.init(document.getElementById('monthChart'));
mc.setOption({{
  tooltip:{{trigger:'axis', formatter:p=>{{const i=p[0].dataIndex; return months[i]+'月<br>均值: '+mean[i]+'%<br>胜率: '+win[i]+'%';}}}},
  legend:{{data:['平均涨跌幅','历史胜率'], top:0}},
  grid:{{left:50,right:50,top:40,bottom:30}},
  xAxis:{{type:'category', data:months.map(m=>m+'月')}},
  yAxis:[{{type:'value', name:'%', axisLabel:{{formatter:'{{value}}%'}}}},
         {{type:'value', name:'胜率%', min:0, max:100, axisLabel:{{formatter:'{{value}}%'}}}}],
  series:[
    {{name:'平均涨跌幅', type:'bar', data:mean.map(v=>({{value:v, itemStyle:{{color:col(v)}}}})),
      label:{{show:true, position:'top', formatter:'{{c}}%', fontSize:11}}}},
    {{name:'历史胜率', type:'line', yAxisIndex:1, data:win, smooth:true,
      lineStyle:{{color:'#2f54eb'}}, itemStyle:{{color:'#2f54eb'}}}}
  ]
}});

const yc = echarts.init(document.getElementById('yearChart'));
yc.setOption({{
  tooltip:{{trigger:'axis', formatter:p=>years[p[0].dataIndex]+'年: '+yret[p[0].dataIndex]+'%'}},
  grid:{{left:50,right:20,top:20,bottom:30}},
  xAxis:{{type:'category', data:years}},
  yAxis:{{type:'value', axisLabel:{{formatter:'{{value}}%'}}}},
  series:[{{type:'bar', data:yret.map(v=>({{value:v, itemStyle:{{color:col(v)}}}})),
    label:{{show:true, position:'top', formatter:'{{c}}%', fontSize:11}}}}]
}});

const cc = echarts.init(document.getElementById('calChart'));
const calData = cal.map((v,i)=>[i, 0, v]);
cc.setOption({{
  tooltip:{{formatter:p=>{{const m=p.data[0]+1; const s=p.data[2]===1?'买入/持有窗口':p.data[2]===-1?'减仓/回避窗口':'中性观望'; return m+'月: '+s;}}}},
  grid:{{left:20,right:20,top:10,bottom:30}},
  xAxis:{{type:'category', data:months.map(m=>m+'月'), splitArea:{{show:true}}}},
  yAxis:{{show:false}},
  series:[{{type:'heatmap', data:calData,
    itemStyle:{{borderColor:'#fff', borderWidth:3}},
    label:{{show:true, formatter:p=>{{const m=p.data[0]+1; return (p.data[2]===1?'▲'):(p.data[2]===-1?'▼'):'·')+'\\n'+m+'月';}}, color:'#fff', fontSize:12}},
    visualMap:{{show:false, min:-1, max:1,
      inRange:{{color:['#d4380d','#f0f1f2','#18940f']}}}}}}]
}});
window.addEventListener('resize',()=>{{mc.resize();yc.resize();cc.resize();}});
</script>
</body>
</html>"""
    return html


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stats", required=True, help="seasonal_analysis.py 的 json 输出")
    ap.add_argument("--daycsv", required=True, help="步骤1导出的日线 CSV（用于算当前技术截面）")
    ap.add_argument("--name", required=True, help="标的名称")
    ap.add_argument("--code", required=True, help="标的代码")
    ap.add_argument("--out", required=True, help="输出 HTML 路径")
    ap.add_argument("--tech", default=None, help="可选：外部技术截面 JSON 覆盖自算")
    ap.add_argument("--label", default="收盘", help="价格标签：股票用'收盘'，ETF/LOF用'价'，场外基金用'净值'")
    args = ap.parse_args()

    stats = json.load(open(args.stats))
    df = pd.read_csv(args.daycsv)
    tech = json.load(open(args.tech)) if args.tech else calc_tech(df)
    html = build_html(stats, tech, args.name, args.code, args.label)
    with open(args.out, "w") as f:
        f.write(html)
    print(f"HTML 生成: {args.out} ({len(html)} bytes)")


if __name__ == "__main__":
    main()
