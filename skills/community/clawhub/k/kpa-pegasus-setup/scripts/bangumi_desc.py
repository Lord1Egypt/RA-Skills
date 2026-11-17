#!/usr/bin/env python3
"""Bangumi (bgm.tv) 中文真简介升级脚本 —— kpa 元数据第二阶段

用法（需 bgm.tv 可达的网络，本机宽带下直连即可）：
    python3 bangumi_desc.py            # 处理 out/*.txt -> final/*.txt
    python3 bangumi_desc.py --push     # 完成后自动推回设备并清缓存

功能：
1. 对每个游戏用中文名搜索 Bangumi，取匹配度最高的游戏条目；
2. 用其官方中文简介替换模板简介（保留改版说明行）；
3. 从 infobox 提取 开发商/发行商/发售日期，回填 publisher/release
   （修复 NDS/FC/SFC/PS/PSP/SATURN/DC/MSX/PICO 等 16 个平台字段缺失）；
4. 全程缓存到 cache.json，可断点续跑；失败/未命中的保留模板简介。

限速：约 4 请求/秒，请勿调高。数据源规范：https://github.com/bangumi/api
"""
import json, re, os, sys, glob, time, difflib
import urllib.request, urllib.error

UA = "kpa-game-setup/1.0 (https://skillhub.cn/user/user_43faedd6)"
DELAY = 0.25
CACHE = "cache.json"
MARKERS = re.compile(r'(完全汉化版|完全汉化|汉化版|汉化|简体中文版|简体中文|繁体中文版|繁体中文|官方中文版|官方中文|中文版|无敌版|金手指版|金手指|加强版|重制版|复刻版|高清版|合辑|合集|典藏版)')

def norm(s):
    return re.sub(r'[\s：:·～~（）()\[\]【】\-—_、,，.!！?？IVX]+', '', s.lower())

def api(path, body=None):
    req = urllib.request.Request("https://api.bgm.tv" + path,
        data=json.dumps(body).encode() if body else None,
        headers={"User-Agent": UA, "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=20))

def get_field(block, key):
    m = re.search(rf'(?m)^{key}: *(.*)$', block)
    return m.group(1).strip() if m else None

def load_cache():
    if os.path.exists(CACHE):
        return json.load(open(CACHE, encoding='utf-8'))
    return {}

def search(title, cache):
    """返回 (summary, publisher, release) 或 None。命中结果缓存。"""
    key = "kw:" + title
    if key in cache:
        return cache[key]
    out = None
    try:
        r = api("/v0/search/games", {"keyword": title})
        cands = (r.get("data") or [])[:6]
        nq, best, score = norm(title), None, 0.0
        for c in cands:
            for nm in (c.get("name_cn") or "", c.get("name") or ""):
                s = difflib.SequenceMatcher(None, nq, norm(nm)).ratio()
                if s > score:
                    score, best = s, c
        if best and score >= 0.55:
            detail = api(f"/v0/subjects/{best['id']}")
            pub, rel = None, None
            for item in detail.get("infobox", []):
                k = item.get("key", "")
                v = item.get("value")
                if isinstance(v, list):
                    v = " / ".join(str(x.get("v", x)) for x in v)
                if k in ("开发商", "developer") and not pub: pub = v
                if k in ("发行", "发行商", "publisher") and not pub: pub = v
                if k in ("发售日期", "发行日期") and not rel: rel = str(v)[:4] if v else None
            out = {"summary": (detail.get("summary") or "").strip(),
                   "publisher": pub, "release": rel, "match": round(score, 2)}
    except Exception as e:
        out = {"error": str(e)}
    cache[key] = out
    time.sleep(DELAY)
    return out

def main():
    push = "--push" in sys.argv
    cache = load_cache()
    os.makedirs("final", exist_ok=True)
    hit, miss, err = 0, 0, 0
    for path in sorted(glob.glob("out/*.txt")):
        plat = os.path.basename(path)[:-4]
        txt = open(path, encoding='utf-8').read()
        blocks = re.split(r'(?m)^(?=game: )', txt)
        for i, e in enumerate(blocks[1:], 1):
            t = get_field(e, "game")
            if not t: continue
            res = search(t, cache)
            if not res or res.get("error") or not res.get("summary"):
                if res and res.get("error"): err += 1
                else: miss += 1
                continue
            hit += 1
            note = ""
            m = re.search(r'(?m)^description: (.*)\n(  .*\n)*', e)
            if m:
                old = m.group(0)
                keep = [ln for ln in old.rstrip('\n').split('\n')[1:] if '本作为' in ln]
                new = "description: " + res["summary"].replace('\r', '')
                new = re.sub(r'\n(?!  )', '\n  ', new)  # 续行统一缩进
                if keep: new += "\n" + "\n".join(keep)
                e = e.replace(old, new + "\n")
            # 回填 publisher / release（仅当缺失时）
            if res.get("publisher") and not get_field(e, "publisher"):
                e = re.sub(r'(?m)^(game: .*\n)', rf'\1publisher: {res["publisher"]}\n', e, count=1)
            if res.get("release") and not get_field(e, "release"):
                e = re.sub(r'(?m)^(game: .*\n(?:publisher: .*\n)?)', rf'\1release: {res["release"]}\n', e, count=1)
            blocks[i] = e
        open(f"final/{plat}.txt", 'w', encoding='utf-8').write("".join(blocks))
        json.dump(cache, open(CACHE, 'w', encoding='utf-8'), ensure_ascii=False)
    print(f"命中 {hit}，未命中 {miss}，出错 {err}")
    if push and hit:
        import subprocess
        import shutil
        adb = os.environ.get("KPA_ADB") or shutil.which("adb")
        if not adb:
            cands = glob.glob(os.path.expanduser("~/WorkBuddy/*/tools/platform-tools/adb"))
            adb = cands[0] if cands else None
        if not adb or not os.path.exists(adb):
            raise SystemExit("ERROR: 未找到 adb，请设置 KPA_ADB 环境变量")
        tf = os.environ.get("KPA_TF", "/storage/6AF3-384F")
        for f in glob.glob("final/*.txt"):
            plat = os.path.basename(f)[:-4]
            subprocess.run([adb, "push", f, f"{tf}/Roms/{plat}/metadata.pegasus.txt"], check=True)
        subprocess.run([adb, "shell", "rm /sdcard/pegasus-frontend/dataCache.json"], check=True)
        print("已推送并清除天马缓存，重启前端即可生效")

if __name__ == "__main__":
    main()
