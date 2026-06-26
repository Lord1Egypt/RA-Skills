#!/usr/bin/env python3
"""🔥 Hot Trends - 真实热搜抓取（百度/头条/GitHub）"""

import argparse, json, sys, re, html as html_mod
import urllib.request, urllib.error

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

def jget(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=15) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"  ⚠️ {e}", file=sys.stderr)
        return None

def hget(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=15) as r:
            return r.read().decode("utf-8")
    except Exception as e:
        print(f"  ⚠️ {e}", file=sys.stderr)
        return None

def get_baidu(kw=None, limit=20):
    d = jget("https://top.baidu.com/api/board?platform=wise&tab=realtime&offset=0&limit=30")
    if not d:
        return None
    # 百度API结构不稳定，用正则暴力提取word字段
    text = json.dumps(d, ensure_ascii=False)
    words = re.findall(r'"word":\s*"([^"]{4,})"', text)
    # 去重保序
    seen = set()
    items = []
    for w in words:
        if w in seen:
            continue
        seen.add(w)
        if kw and kw.lower() not in w.lower():
            continue
        items.append({"rank": len(items)+1, "title": w, "heat": ""})
        if len(items) >= limit:
            break
    return items or None

def get_toutiao(kw=None, limit=20):
    d = jget("https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc")
    if not d:
        return None
    items = []
    for it in d.get("data", []):
        title = it.get("Title", "")
        if not title:
            continue
        heat = it.get("HotValue", "")
        if kw and kw.lower() not in title.lower():
            continue
        items.append({"rank": len(items)+1, "title": title, "heat": str(heat)})
        if len(items) >= limit:
            break
    return items or None

def get_github(kw=None, limit=20, lang=None):
    url = "https://github.com/trending" + (f"/{lang}" if lang else "") + "?since=daily"
    text = hget(url)
    if not text:
        return None
    items = []
    for m in re.finditer(r'<article class="Box-row">(.*?)</article>', text, re.DOTALL):
        b = m.group(1)
        repo = re.search(r'<h2[^>]*>.*?<a[^>]*href="/([^"]+)"', b, re.DOTALL)
        if not repo:
            continue
        repo = repo.group(1).strip()
        dm = re.search(r'<p class="col-9[^"]*">\s*(.*?)\s*</p>', b, re.DOTALL)
        desc = html_mod.unescape(re.sub(r'<[^>]+>', '', dm.group(1)).strip()) if dm else ""
        st = re.search(r'([\d,]+)\s*stars today', b)
        st = st.group(1).replace(",","") if st else "?"
        tt = re.search(r'Stargazers[^>]*>\s*([\d.]+[kKmM]?)\s*</a>', b)
        tt = tt.group(1).strip() if tt else "?"
        lg = re.search(r'itemprop="programmingLanguage">(.*?)<', b)
        lg = lg.group(1).strip() if lg else ""
        if kw and kw.lower() not in f"{repo} {desc}".lower():
            continue
        items.append({"rank": len(items)+1, "title": repo, "heat": f"⭐{tt}(+{st})", "lang": lg, "desc": desc[:80]})
        if len(items) >= limit:
            break
    return items or None

def show(items, name):
    if not items:
        print(f"\n❌ {name}: 获取失败")
        return
    print(f"\n🔥 {name} Top {len(items)}")
    print("─" * 70)
    for i in items:
        r, t, h = i["rank"], i["title"][:55], i.get("heat","")
        if "lang" in i:
            print(f"  {r:>2}. {t}")
            print(f"      {h} | {i['lang']} | {i.get('desc','')}")
        elif i.get("desc"):
            print(f"  {r:>2}. {t}")
            print(f"      🔥{h}  {i['desc']}")
        else:
            print(f"  {r:>2}. {t}  🔥{h}")
    print("─" * 70)

def main():
    p = argparse.ArgumentParser(description="🔥 热搜趋势")
    p.add_argument("platform", nargs="?", default="all", choices=["baidu","toutiao","github","all"])
    p.add_argument("-k", "--keyword", help="关键词过滤")
    p.add_argument("-n", "--limit", type=int, default=20)
    p.add_argument("-l", "--lang", help="GitHub语言")
    a = p.parse_args()

    F = {
        "baidu": ("百度热搜", lambda: get_baidu(a.keyword, a.limit)),
        "toutiao": ("头条热搜", lambda: get_toutiao(a.keyword, a.limit)),
        "github": ("GitHub Trending", lambda: get_github(a.keyword, a.limit, a.lang)),
    }
    targets = F if a.platform == "all" else {a.platform: F[a.platform]}
    for _, (name, fn) in targets.items():
        show(fn(), name)

if __name__ == "__main__":
    main()
