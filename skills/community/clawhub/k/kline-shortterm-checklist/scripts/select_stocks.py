#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全A 下午2:30 第1-4层客观初筛 (东方财富 push2delay 延迟行情 = 最近交易日)。

日期策略（入口自动解析）:
  - 不加 --date: 默认按「当天」；若当天为周末/休市，则自动回退到最近交易日。
  - 加 --date YYYY-MM-DD: 指定意图日期（延迟行情仅含最近交易日，若与指定不符会提示）。

pz 上限100/页, 故按 pn 翻页至 涨幅<3 为止。筛选: 涨幅3-5% & 量比>=1 & 换手5~10% & 流通50~200亿。
产出: candidates.json（候选）+ screen_meta.json（日期解析结果）。"""
import json, urllib.request, urllib.parse, time, datetime, argparse

FS = "m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23"
FIELDS = "f12,f14,f2,f3,f9,f10,f8,f20"   # +f9 市盈率TTM(用于自动核查亏损/基本面)
HOST = "https://push2delay.eastmoney.com/api/qt/clist/get"

def fetch_page(pn, pz=100):
    url = f"{HOST}?pn={pn}&pz={pz}&po=1&np=1&fltt=2&invt=2&fid=f3&fs={FS}&fields={FIELDS}"
    req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0","Referer":"https://quote.eastmoney.com/"})
    for _ in range(6):
        try:
            return json.loads(urllib.request.urlopen(req, timeout=25).read().decode("utf-8"))
        except Exception:
            time.sleep(2)
    return None

def _norm(c):
    c = c.strip()
    if c[0] == "6": return "sh"+c
    if c[0] in ("0","3"): return "sz"+c
    if c[0] in ("4","8"): return "bj"+c
    return c

def tencent_float_mv(codes):
    """批量取腾讯权威流通市值(字段44, 单位亿)，修正东方财富 f20 实为总市值的偏差。"""
    out = {}
    for i in range(0, len(codes), 40):
        q = ",".join(_norm(c) for c in codes[i:i+40])
        url = "https://qt.gtimg.cn/q=" + urllib.parse.quote(q)
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0","Referer":"https://finance.qq.com/"})
        raw = None
        for _ in range(5):
            try:
                raw = urllib.request.urlopen(req, timeout=25).read().decode("gbk","ignore")
                break
            except Exception:
                time.sleep(1.5)
        if not raw: continue
        for blk in raw.split(";"):
            blk = blk.strip()
            if not blk.startswith("v_"): continue
            inner = blk.split('"',1)[1].rsplit('"',1)[0]
            fld = inner.split("~")
            try:
                code = fld[2]; fm = float(fld[44])
            except (IndexError, ValueError):
                continue
            out[code] = fm
    return out

def f(x):
    try: return float(x)
    except: return None

def _latest_trading_day_sina(sym="sh000001"):
    """取新浪日K最后一个交易日(YYYY-MM-DD)，作为「最近交易日」的真实锚点。
    东方财富 push2delay 不含日期字段，故用上证指数日K的最近一根校准。"""
    try:
        url = (f"https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/"
               f"CN_MarketData.getKLineData?symbol={sym}&scale=240&ma=20&datalen=5")
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0","Referer":"https://finance.sina.com.cn/"})
        arr = json.loads(urllib.request.urlopen(req, timeout=15).read().decode("gbk","ignore"))
        if arr:
            return sorted(r["day"] for r in arr)[-1]
    except Exception:
        pass
    return None

def resolve_target_date(date_str):
    """返回 (intended: date, pinned: bool)。--date 解析失败则回退到今天。"""
    today = datetime.date.today()
    if date_str:
        try:
            return datetime.datetime.strptime(date_str, "%Y-%m-%d").date(), True
        except ValueError:
            print(f"[日期] 无法解析 '{date_str}'，改用今天")
    return today, False

def to_weekday(d):
    """周末回退到最近周五（休市日无法靠日历判断，最终以数据源锚点为准）。"""
    cur = d
    while cur.weekday() >= 5:   # Sat=5, Sun=6
        cur -= datetime.timedelta(days=1)
    return cur

def main():
    ap = argparse.ArgumentParser(description="全A 下午2:30 第1-4层客观初筛")
    ap.add_argument("--date", help="指定意图日期 YYYY-MM-DD（默认: 当天，非交易日自动回退最近交易日）")
    args = ap.parse_args()

    # ---- 日期解析（入口自动 fallback）----
    today = datetime.date.today()
    requested, pinned = resolve_target_date(args.date)
    intended = to_weekday(requested)
    actual = _latest_trading_day_sina()            # 真实「最近交易日」锚点
    data_date = actual or intended.isoformat()
    if pinned:
        used_fallback = (data_date != requested.isoformat())
        if used_fallback:
            print(f"[日期] 指定 {requested} → 实际行情日期 {data_date}（延迟行情仅含最近交易日，已按最新可用数据生成）")
        else:
            print(f"[日期] 指定 {requested} → 使用当天数据 {data_date}")
    elif today.weekday() >= 5:
        print(f"[日期] 今日 {today} 为周末，自动回退至最近交易日 {data_date}")
        used_fallback = True
    elif data_date != today.isoformat():
        print(f"[日期] 今日 {today} 非交易日（休市），自动回退至最近交易日 {data_date}")
        used_fallback = True
    else:
        print(f"[日期] 今日 {today} 为交易日，使用当天数据 {data_date}")
        used_fallback = False

    cands=[]; pn=1; MAXP=60
    while pn<=MAXP:
        d=fetch_page(pn)
        if not d: break
        items=d.get("data",{}).get("diff",[])
        if not items: break
        stop=False
        for it in items:
            chg=f(it.get("f3"))
            if chg is None: continue
            if chg < 3.0:   # 涨幅降序, 之后均<3
                stop=True; break
            if not (3.0 <= chg <= 5.0): continue
            vr=f(it.get("f10")); to=f(it.get("f8")); fmraw=f(it.get("f20"))
            fm=(fmraw/1e8) if (fmraw and fmraw>1000) else fmraw
            pe=f(it.get("f9"))
            nm=it.get("f14") or ""
            st = ("ST" in nm) or ("退" in nm)
            if vr is None or vr < 1: continue
            if to is None or not (5.0 <= to <= 10.0): continue
            if fm is None or not (50 <= fm <= 200): continue
            cands.append({"code":it.get("f12"),"name":nm,
                          "price":f(it.get("f2")),"chg":chg,"vr":vr,"to":to,"fm":fm,"pe":pe,"st":st})
        if stop: break
        if len(items) < 100: break
        pn+=1
    # 流通市值口径修正：东方财富 f20 个别股票返回的是总市值，统一用腾讯权威流通市值(字段44)重筛
    if cands:
        fm_map = tencent_float_mv([c["code"] for c in cands])
        kept = []
        for c in cands:
            fm = fm_map.get(c["code"])
            if fm is None or not (50 <= fm <= 200):
                continue
            c["fm"] = fm
            kept.append(c)
        dropped = len(cands) - len(kept)
        if dropped:
            print(f"[口径修正] 腾讯流通市值重筛剔除 {dropped} 只(流通<50或>200亿)")
        cands = kept
    cands.sort(key=lambda x:(-x["vr"], -x["to"]))
    with open("candidates.json","w",encoding="utf-8") as fh:
        json.dump(cands, fh, ensure_ascii=False, indent=1)
    meta = {"requested": requested.isoformat(), "intended": intended.isoformat(),
            "data_date": data_date, "today": today.isoformat(),
            "pinned": pinned, "used_fallback": bool(used_fallback)}
    with open("screen_meta.json","w",encoding="utf-8") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=1)
    print(f"翻页数={pn}  通过四层(含流通市值修正)数量={len(cands)}")
    print(f"{'代码':<8}{'名称':<10}{'现价':>8}{'涨幅%':>8}{'量比':>8}{'换手%':>8}{'流通亿':>10}")
    for c in cands[:30]:
        print(f"{c['code']:<8}{c['name']:<10}{c['price']:>8.2f}{c['chg']:>8.2f}{c['vr']:>8.2f}{c['to']:>8.2f}{c['fm']:>10.1f}")

if __name__=="__main__":
    main()
