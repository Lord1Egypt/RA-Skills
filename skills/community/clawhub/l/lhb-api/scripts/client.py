"""
龙虎榜数据 + 资金流向 API — Python 客户端

使用方式：
    from client import LHBClient
    client = LHBClient()
    
    # 当日龙虎榜
    data = client.daily()
    
    # 个股历史龙虎榜
    history = client.history("002031")
    
    # 资金流向
    flow = client.moneyflow("600519")
"""

import json
import urllib.request
import urllib.parse


class LHBClient:
    """数据API客户端"""

    def __init__(self, base_url: str = "http://fffy520.gicp.net:8003"):
        self.base_url = base_url.rstrip("/")

    def _request(self, path: str, params: dict = None) -> dict:
        url = f"{self.base_url}{path}"
        if params:
            url += "?" + urllib.parse.urlencode(
                {k: v for k, v in params.items() if v is not None}
            )
        try:
            with urllib.request.urlopen(urllib.request.Request(url), timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="ignore")
            try:
                return json.loads(body)
            except json.JSONDecodeError:
                return {"code": e.code, "error": body}
        except Exception as e:
            return {"code": 500, "error": str(e)}

    def daily(self, date: str = None) -> dict:
        """当日龙虎榜（含买5卖5营业部明细）"""
        return self._request("/api/lhb/daily", {"date": date} if date else None)

    def history(self, code: str) -> dict:
        """个股历史龙虎榜"""
        return self._request("/api/lhb/history", {"code": code})

    def moneyflow(self, code: str, trade_date: str = "") -> dict:
        """个股资金流向（主力/超大单/大单/中单/小单）"""
        params = {"code": code}
        if trade_date:
            params["trade_date"] = trade_date
        return self._request("/api/moneyflow", params)


if __name__ == "__main__":
    import sys
    client = LHBClient()

    if len(sys.argv) < 2:
        print("用法: python client.py <命令> [参数]")
        print("  命令:")
        print("    daily             最新一日龙虎榜")
        print("    daily 2026-05-08  指定日期龙虎榜")
        print("    history 002031    个股历史龙虎榜")
        print("    moneyflow 600519  资金流向")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "daily":
        date = sys.argv[2] if len(sys.argv) > 2 else None
        r = client.daily(date)
        if r.get("code") == 200:
            print(f"共 {len(r['data'])} 条 | 剩余: {r['remaining']}")
            for e in r["data"][:3]:
                print(f"  {e['date']} {e['code']} {e['name']} {e['change']}% 净买{e['net_buy']}万")
        else:
            print(f"❌ {r.get('error', r.get('detail', '?'))}")

    elif cmd == "history":
        if len(sys.argv) < 3:
            print("请指定股票代码"); sys.exit(1)
        r = client.history(sys.argv[2])
        if r.get("code") == 200:
            print(f"{len(r['data'])}条 | 剩余: {r['remaining']}")
            for e in r["data"][:5]:
                print(f"  {e['date']} {e['name']} {e['change']}% 净买{e['net_buy']}万")
        else:
            print(f"❌ {r.get('error', r.get('detail', '?'))}")

    elif cmd == "moneyflow":
        if len(sys.argv) < 3:
            print("请指定股票代码"); sys.exit(1)
        date = sys.argv[3] if len(sys.argv) > 3 else ""
        r = client.moneyflow(sys.argv[2], date)
        if r.get("code") == 200:
            d = r["data"]
            print(f"{d['stock_code']} {d['stock_name']}")
            print(f"  主力净流入: {d['main_net_inflow']:.0f}元 ({d['main_net_pct']}%)")
            print(f"  超大单: {d['super_large_inflow']:.0f}元 | 大单: {d['large_inflow']:.0f}元")
            print(f"  中单: {d['medium_inflow']:.0f}元 | 小单: {d['small_inflow']:.0f}元")
        else:
            print(f"❌ {r.get('error', r.get('detail', '?'))}")
