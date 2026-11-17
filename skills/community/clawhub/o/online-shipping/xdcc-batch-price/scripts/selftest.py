#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
xdcc-price-query 自检脚本（纯静态，零网络）。

覆盖：省市区数据完整性、地址解析、报价接口参数构造、结果排序、
批量路线解析、凭据读写、缺 Playwright 时不硬退、包内零外部联系渠道、
「批量物流查询代码已彻底移除」回归，以及在线下单链路的参数构造、
渠道匹配、取件时间段挑选与安全闸门（预览模式绝不提交）。

下单相关用例用 mock 替换网络调用，全程零网络、不产生真实订单。
每个用例在独立临时目录中运行，零污染真实数据。
用法：python selftest.py
退出码：0 全过 / 1 有失败
"""

import contextlib
import io
import os
import re
import shutil
import sys
import tempfile

# 将脚本目录加入路径，便于 import 主模块
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

PASS = 0
FAIL = 0


def check(name: str, cond: bool, detail: str = "") -> None:
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  ✓ {name}")
    else:
        FAIL += 1
        print(f"  ✗ {name}  {detail}")


# --------------------------------------------------------------------------- #
# 1. 省市区基础数据
# --------------------------------------------------------------------------- #
def test_regions_data():
    print("[1] 省市区基础数据完整性")
    import region as rg
    data = rg.load_regions()
    provs = data["provinces"]
    check("provinces 非空", len(provs) >= 30, f"仅 {len(provs)} 个省")
    names = [p["name"] for p in provs]
    check("省份名唯一", len(names) == len(set(names)))
    for must in ("北京市", "上海市", "广东省", "浙江省", "新疆维吾尔自治区"):
        check(f"含 {must}", must in names)
    gd = next(p for p in provs if p["name"] == "广东省")
    gcities = [c["name"] for c in gd["cities"]]
    check("广东省含深圳市/东莞市", "深圳市" in gcities and "东莞市" in gcities)
    sz = next(c for c in gd["cities"] if c["name"] == "深圳市")
    check("深圳市含南山区", "南山区" in sz["areas"])
    bj = next(p for p in provs if p["name"] == "北京市")
    check("直辖市省份下只有同名城市", [c["name"] for c in bj["cities"]] == ["北京市"],
          str([c["name"] for c in bj["cities"]]))
    # 行政后缀剥离必须按最长优先，否则「新疆维吾尔自治区」会被剥成「新疆维吾尔」
    check("_core 剥离自治区后缀", rg._core("新疆维吾尔自治区") == "新疆",
          rg._core("新疆维吾尔自治区"))
    check("_core 剥离市级后缀", rg._core("深圳市") == "深圳", rg._core("深圳市"))
    # 「新区」须整体剥离，不能只剥单字「区」把「浦东新区」拆成「浦东新」
    check("_core 整体剥离新区", rg._core("浦东新区") == "浦东", rg._core("浦东新区"))
    check("_core 整体剥离滨海新区", rg._core("滨海新区") == "滨海", rg._core("滨海新区"))


# --------------------------------------------------------------------------- #
# 2. 地址解析
# --------------------------------------------------------------------------- #
def test_region_resolve():
    print("[2] 地址解析：连写 / 分隔 / 直辖市 / 直筒子市 / 省略省")
    import region as rg
    db = rg.RegionDB()

    def eq(text, prov, city, area):
        try:
            r = rg.resolve(text, db)
        except rg.RegionError as e:
            check(f"解析 {text}", False, f"抛异常 {e}")
            return
        ok = (r["province"], r["city"], r["area"]) == (prov, city, area)
        check(f"解析 {text} → {prov}/{city}/{area}", ok,
              f"实际 {r['province']}/{r['city']}/{r['area']}")

    eq("广东省深圳市南山区", "广东省", "深圳市", "南山区")
    eq("广东,深圳,南山", "广东省", "深圳市", "南山区")
    eq("广东 深圳 南山", "广东省", "深圳市", "南山区")
    eq("深圳南山", "广东省", "深圳市", "南山区")            # 省略省份，反查
    eq("北京朝阳", "北京市", "北京市", "朝阳区")            # 直辖市
    eq("上海 浦东", "上海市", "上海市", "浦东新区")
    eq("东莞南城", "广东省", "东莞市", "南城街道")          # 直筒子市（街道级）
    eq("重庆渝中", "重庆市", "重庆市", "渝中区")
    eq("新疆乌鲁木齐天山", "新疆维吾尔自治区", "乌鲁木齐市", "天山区")

    # --- 回归：这两条曾解析错误，改动 _core/省份匹配时务必保持 ---
    # 「浦东新区」一度被剥成「浦东新」，导致「上海浦东」匹配不上、错落到黄浦区
    eq("上海浦东陆家嘴", "上海市", "上海市", "浦东新区")
    # 「内蒙」是「内蒙古」的口语简称，只比全称/核心名会漏掉
    eq("内蒙呼和浩特", "内蒙古自治区", "呼和浩特市", "市辖区")

    # 尾部详细地址应被剥离出来
    r = rg.resolve("浙江省杭州市西湖区文三路100号", db)
    check("详细地址被拆出", r["address"] == "文三路100号", f"实际 {r['address']!r}")
    r2 = rg.resolve("广东 深圳 南山 科技园路1号", db)
    check("分隔式详细地址被拆出", r2["address"] == "科技园路1号", f"实际 {r2['address']!r}")

    # 缺区县 → 兜底且必须告警，不能静默猜错
    r3 = rg.resolve("广东 深圳", db)
    check("缺区县时兜底出区", bool(r3["area"]), "未兜底")
    check("缺区县时有告警", bool(r3["warnings"]), "静默兜底未告警")

    # 完全无法识别 → 抛错并给候选
    try:
        rg.resolve("火星基地阿尔法", db)
        check("无法识别时抛 RegionError", False, "没有抛异常")
    except rg.RegionError as e:
        check("无法识别时抛 RegionError", True)
        check("无法识别时给出候选", bool(e.suggestions), "无候选")

    try:
        rg.resolve("", db)
        check("空地址抛错", False, "没有抛异常")
    except rg.RegionError:
        check("空地址抛错", True)


# --------------------------------------------------------------------------- #
# 3. 报价接口参数构造
# --------------------------------------------------------------------------- #
def test_price_payload():
    print("[3] 报价接口参数构造与重量归一化")
    import price_query as pq
    s = {"province": "广东省", "city": "深圳市", "area": "南山区", "address": "科技园"}
    r = {"province": "浙江省", "city": "杭州市", "area": "西湖区", "address": ""}
    p = pq.build_payload(s, r, 1.5)
    check("Weight 字段", p["Weight"] == "1.5", p["Weight"])
    check("Receiver 嵌套键", p["Receiver[ExpAreaName]"] == "西湖区")
    check("Sender 嵌套键", p["Sender[ProvinceName]"] == "广东省")
    check("IsRequestKdn=true", p["IsRequestKdn"] == "true")
    check("参数个数与页面一致", len(p) == 10, f"实际 {len(p)} 个")

    check("重量 1 → '1'", pq._fmt_weight(1) == "1")
    check("重量 1.0 → '1'", pq._fmt_weight(1.0) == "1")
    check("重量 2.50 → '2.5'", pq._fmt_weight(2.50) == "2.5")
    check("重量 0.1 → '0.1'", pq._fmt_weight(0.1) == "0.1")


# --------------------------------------------------------------------------- #
# 4. 结果解析与排序
# --------------------------------------------------------------------------- #
def test_price_parse_sort():
    print("[4] 报价结果解析与排序")
    import price_query as pq
    data = [
        {"ShipperCode": "SF", "ShipperName": "顺丰速运", "IsAvailable": 1, "cost": 18.0, "MarketCost": 23},
        {"ShipperCode": "JD", "ShipperName": "京东快递", "IsAvailable": 0, "cost": "", "MarketCost": ""},
        {"ShipperCode": "YTO", "ShipperName": "圆通速递", "IsAvailable": 1, "cost": 7.2, "MarketCost": 10},
        {"ShipperCode": "STO", "ShipperName": "申通快递", "IsAvailable": 1, "cost": 8.5},
    ]
    rows = pq.parse_items(data)
    check("条数一致", len(rows) == 4, str(len(rows)))
    check("按价格升序", [r["shipper_code"] for r in rows[:3]] == ["YTO", "STO", "SF"],
          str([r["shipper_code"] for r in rows]))
    check("不可达排最后", rows[-1]["shipper_code"] == "JD")
    check("不可达标记", rows[-1]["available"] is False)
    check("空价不炸且为 None", rows[-1]["cost"] is None)
    sto = next(r for r in rows if r["shipper_code"] == "STO")   # 该条没有 MarketCost
    check("缺 MarketCost 为 None", sto["market_cost"] is None, str(sto["market_cost"]))
    check("空数据不炸", pq.parse_items([]) == [])
    check("脏数据不炸", isinstance(pq.parse_items([None, "x", {}]), list))

    # 渲染不抛异常，且不可达渠道不重复拼接「不可达」字样
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        pq.print_result(
            {"province": "广东省", "city": "深圳市", "area": "南山区", "address": "", "warnings": []},
            {"province": "浙江省", "city": "杭州市", "area": "西湖区", "address": "", "warnings": []},
            1, rows)
    out = buf.getvalue()
    check("渲染含最低价", "圆通速递" in out)
    check("不可达不重复拼接", out.count("该地区不可达") == 1,
          f"出现 {out.count('该地区不可达')} 次")


# --------------------------------------------------------------------------- #
# 5. 批量路线解析
# --------------------------------------------------------------------------- #
def test_price_batch_read():
    print("[5] 批量路线文件解析")
    import price_query as pq
    d = tempfile.mkdtemp(prefix="xdcc_selftest_")
    # 中文表头
    p1 = os.path.join(d, "cn.csv")
    open(p1, "w", encoding="utf-8").write(
        "寄件,收件,重量\n广东 深圳 南山,浙江 杭州 西湖,1\n上海 浦东,北京 朝阳,2.5\n")
    rows = pq.read_batch(p1)
    check("中文表头解析出 2 条", len(rows) == 2, str(len(rows)))
    check("中文表头字段正确", rows[0][:3] == ("广东 深圳 南山", "浙江 杭州 西湖", "1"), str(rows[0]))

    # 英文表头
    p2 = os.path.join(d, "en.csv")
    open(p2, "w", encoding="utf-8").write("from,to,weight\n广东 深圳 南山,北京 朝阳,3\n")
    check("英文表头解析出 1 条", len(pq.read_batch(p2)) == 1)

    # 无表头
    p3 = os.path.join(d, "raw.csv")
    open(p3, "w", encoding="utf-8").write("广东 深圳 南山,北京 朝阳,1\n")
    check("无表头解析出 1 条", len(pq.read_batch(p3)) == 1)

    # 空文件
    p4 = os.path.join(d, "empty.csv")
    open(p4, "w", encoding="utf-8").write("")
    check("空文件返回空", pq.read_batch(p4) == [])

    shutil.rmtree(d, ignore_errors=True)


# --------------------------------------------------------------------------- #
# 6. 凭据读写
# --------------------------------------------------------------------------- #
def test_common_creds_io():
    print("[6] 凭据读写与兜底提示")
    import common as cm
    d = tempfile.mkdtemp(prefix="xdcc_selftest_")
    path = os.path.join(d, "creds.env")
    open(path, "w", encoding="utf-8").write("# 注释\nOTHER_KEY=keep\nXDCC_USER_TOKEN=old\n")
    cm.update_creds(path, {"XDCC_USER_TOKEN": "new"})
    creds = cm.load_creds(path)
    check("token 被更新", creds.get("XDCC_USER_TOKEN") == "new", str(creds))
    text = open(path, encoding="utf-8").read()
    check("注释被保留", "# 注释" in text)
    check("其他键的行未被清空", "OTHER_KEY=keep" in text)
    check("get_token 读 dict", cm.get_token(creds) == "new")
    check("get_token 读路径", cm.get_token(path) == "new")

    hint = cm.price_hint("测试原因")
    check("兜底提示含原因", "测试原因" in hint)
    check("兜底提示含第 1 步", "web_login.py --check" in hint)
    check("兜底提示不含第三方账号", "xdccvip" not in hint.lower())
    check("兜底提示不含电子邮箱", not re.search(r"[\w.\-]+@[\w.\-]+\.\w+", hint))
    check("兜底提示不含外部站点链接", "http" not in hint)
    shutil.rmtree(d, ignore_errors=True)


# --------------------------------------------------------------------------- #
# 7. 缺 Playwright 时不硬退
# --------------------------------------------------------------------------- #
def test_no_hard_exit():
    print("[7] 缺 Playwright 时导入与调用都不硬退")
    import subprocess
    import web_login
    code = (
        "import sys; sys.path.insert(0, r'%s');"
        "import price_query, place_order, order_api, addr_parse, web_login, region, common;"
        "print('IMPORT_OK')" % SCRIPT_DIR.replace("\\", "\\\\")
    )
    r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=60)
    check("全部模块可独立导入", "IMPORT_OK" in r.stdout,
          f"stdout={r.stdout[:120]} stderr={r.stderr[:200]}")
    check("导入无 traceback", "Traceback" not in r.stderr, r.stderr[:200])

    # 登录页字段 id 是 usernameOrEmail / password，placeholder 是「请输入用户名或邮箱」。
    # 早期版本按「手机号」匹配 placeholder，实测匹配数为 0，用户名填不进去——这里守住定位策略。
    src = open(os.path.join(SCRIPT_DIR, "web_login.py"), encoding="utf-8").read()
    check("autofill 按 ID 优先定位", "#usernameOrEmail" in src)
    check("autofill 保留 placeholder 兜底", "用户名或邮箱" in src)
    check("autofill 返回填入结果", "u_ok" in src and "p_ok" in src)
    check("登录页地址正确", web_login.LOGIN_URL.startswith("https://xdccy.com/"))

    # 缺 Playwright 时 interactive_login 必须返回错误，而不是 sys.exit / 抛 SystemExit
    if web_login.sync_playwright is None:
        tok, err = web_login.interactive_login()
        check("缺依赖时返回 (None, err)", tok is None and bool(err), f"tok={tok} err={err}")
        check("错误信息提示安装方式", "playwright" in (err or "").lower(), str(err))
    else:
        check("本机已装 Playwright，跳过缺依赖分支", True)


# --------------------------------------------------------------------------- #
# 8. 技能包零外部联系渠道
# --------------------------------------------------------------------------- #
BANNED_PATTERNS = [
    (r"xdccv[i]p|xdcc5205[0-9]{2}", "第三方即时通讯账号"),
    (r"[\w.\-]+@[\w.\-]+\.\w+", "电子邮箱地址"),
    (r"https?://(www\.)?xdccy\.com", "外部站点首页地址"),
    (r"微\u4fe1号|公\u4f17号|加\s?微|扫[\u7801]", "外部推广话术"),
    (r"二\u7ef4\u7801", "二" + "维码"),
    (r"水\u5370|通[栏栏]|品牌色渐变", "页面满幅置顶条样式"),
]
# 白名单主机（属功能调用，非推广）：API 基址与下单页由代码必需
_ALLOWED_HOSTS = ("api.xdccy.com", "xdccy.com")

PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
IMG_EXT = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp", ".ico")
_SKIP_DIRS = {".git", ".workbuddy", "__pycache__", "node_modules", ".venv", "dist"}
_SELF = os.path.basename(__file__)  # 扫描规则自身除外，避免规则命中自己


def _walk_project():
    for dirpath, dirnames, filenames in os.walk(PROJECT_DIR):
        dirnames[:] = [d for d in dirnames if d not in _SKIP_DIRS]
        for fn in filenames:
            if fn == _SELF or fn.endswith(".pyc"):
                continue
            yield os.path.join(dirpath, fn)


def test_no_offsite_promotion():
    print("[8] 技能包零外部联系渠道扫描")
    hits, scanned = [], 0
    for fp in _walk_project():
        ext = os.path.splitext(fp)[1].lower()
        try:
            text = open(fp, encoding="utf-8").read()
        except (UnicodeDecodeError, OSError):
            if ext in IMG_EXT:
                hits.append(f"{os.path.basename(fp)}（图片资源）")
            continue
        scanned += 1
        for pat, label in BANNED_PATTERNS:
            for m in re.finditer(pat, text, re.I):
                if pat == r"https?://(www\.)?xdccy\.com" and \
                        any(m.group(0).split("://", 1)[-1].startswith(a)
                            for a in _ALLOWED_HOSTS):
                    continue  # API 基址/下单页白名单：属功能调用，非推广
                ctx = text[max(0, m.start() - 32):m.end() + 32].replace("\n", " ")
                hits.append(f"{label}｜{os.path.basename(fp)}｜{m.group(0)}｜…{ctx}…")

    check("包内无图片资源与外部联系渠道内容写入", not hits,
          "\n      · " + "\n      · ".join(hits))
    check(f"已完成 {scanned} 个文本文件扫描", scanned >= 5, f"仅扫描 {scanned} 个文件")


# --------------------------------------------------------------------------- #
# 8b. 上架发布合规（准备投放到 open.workbuddy.cn 技能市场）
#
# 发布审核卡的是四类东西：外部联系渠道、营销广告话术、非白名单外链、真实个人数据。
# 这一节把「人工 review」换成自动断言，改动文档时不会悄悄写回违规内容。
# --------------------------------------------------------------------------- #
# 本服务自身的域名，属功能调用必需（API 基址 + 官网功能页面），不是外部推广
PUBLISH_HOST_WHITELIST = ("api.xdccy.com", "xdccy.com")
# 文档示例中通用的占位手机号（等价于 example.com），非任何真人的真实号码
PUBLISH_SAMPLE_PHONES = {"13800138000", "13900139000"}
# (正则, 违规类型)
PUBLISH_BANNED = [
    (r"[\w.\-]+@[\w.\-]+\.\w{2,}", "电子邮箱地址"),
    (r"1[3-9]\d{9}", "完整手机号（示例应脱敏）"),
    (r"二维码|扫码|扫描关注", "二维码"),
    (r"加\s?微|微信号[:：]?\s*\w|公众号|QQ群|\bQQ\b", "第三方即时通讯/社群"),
    (r"淘宝|天猫|京东商城|拼多多|抖音小店|闲鱼", "第三方电商"),
    (r"全网|全行业|业界|行业第一|排名第一|销量第一|唯一.{0,4}(指定|推荐)|"
     r"天花板|史上最|全国最|顶级|王牌", "极限词（广告法风险）"),
    (r"限时|秒杀|包邮|首单立减|领券|爆款|热卖|火遍|圈粉", "促销营销话术"),
]


def test_publish_compliance():
    print("[16] 上架发布合规：外链 / 联系方式 / 广告话术 / 真实号码")
    hits, files_scanned, hosts = [], 0, set()
    img_files = []

    for fp in _walk_project():
        if os.path.splitext(fp)[1].lower() in IMG_EXT:
            img_files.append(os.path.basename(fp))
            continue
        base = os.path.basename(fp)
        try:
            text = open(fp, encoding="utf-8").read()
        except (UnicodeDecodeError, OSError):
            continue
        files_scanned += 1

        # 1) 外链域名必须落在白名单里
        for m in re.finditer(r"https?://([A-Za-z0-9.\-]+)", text):
            h = m.group(1).lower()
            hosts.add(h)
            if not any(h == w or h.endswith("." + w) for w in PUBLISH_HOST_WHITELIST):
                hits.append(f"非白名单外链｜{base}｜{m.group(0)}")

        # 2) 违规内容扫描（白名单手机号单独放行）
        for pat, label in PUBLISH_BANNED:
            for m in re.finditer(pat, text):
                if label.startswith("完整手机号"):
                    if m.group(0) in PUBLISH_SAMPLE_PHONES:
                        continue      # 文档通用占位号
                ctx = text[max(0, m.start() - 24):m.end() + 24].replace("\n", " ")
                hits.append(f"{label}｜{base}｜{m.group(0)}｜…{ctx}…")

    check("包内无图片资源（二维码/推广图）",
          not img_files, "\n      · " + "\n      · ".join(img_files[:5]))
    check("包内无电子邮箱、即时通讯账号与第三方电商", not hits, "\n      · " + "\n      · ".join(hits[:6]))
    check("外链仅限本服务域名", not [h for h in hits if h.startswith("非白名单外链")],
          "\n      · " + "\n      · ".join([h for h in hits if h.startswith("非白名单外链")][:5]))
    check("无极限词与促销话术", not [h for h in hits if "极限词" in h or "促销" in h],
          "\n      · " + "\n      · ".join([h for h in hits if "极限词" in h or "促销" in h][:5]))
    check("文档示例手机号已脱敏",
          not [h for h in hits if h.startswith("完整手机号")],
          "\n      · " + "\n      · ".join([h for h in hits if h.startswith("完整手机号")][:5]))
    check(f"已扫描 {files_scanned} 个文本、{len(hosts)} 个外链域名",
          files_scanned >= 5, f"仅扫描 {files_scanned} 个文件")


# --------------------------------------------------------------------------- #
# 9. 不应再残留批量物流查询代码
# --------------------------------------------------------------------------- #
def test_no_legacy_tracking_code():
    print("[9] 确认批量物流查询代码已彻底移除")
    import subprocess
    gone = ["batch_query.py", "onboard.py", "guided_register.py", "get_user_apikey.py"]
    for fn in gone:
        check(f"{fn} 已删除", not os.path.isfile(os.path.join(SCRIPT_DIR, fn)))
    for fn in ("api_reference.md", "onboarding_guide.md"):
        check(f"references/{fn} 已删除",
              not os.path.isfile(os.path.join(PROJECT_DIR, "references", fn)))

    # 源码里不应再 import 已删除的模块
    leftover = []
    for fp in _walk_project():
        if not fp.endswith(".py"):
            continue
        try:
            text = open(fp, encoding="utf-8").read()
        except (UnicodeDecodeError, OSError):
            continue
        for mod in ("batch_query", "guided_register", "get_user_apikey"):
            if re.search(r"^\s*import\s+%s\b|^\s*from\s+%s\b" % (mod, mod), text, re.M):
                leftover.append(f"{os.path.basename(fp)} → {mod}")
    check("无残留 import 已删除模块", not leftover, "；".join(leftover))

    # CLI 装配没被拆坏
    r = subprocess.run([sys.executable, os.path.join(SCRIPT_DIR, "price_query.py"), "--help"],
                       capture_output=True, text=True, timeout=60)
    check("price_query.py --help 正常", r.returncode == 0 and "--weight" in r.stdout,
          r.stderr[:200])


# --------------------------------------------------------------------------- #
# 10. 下单接口参数构造
# --------------------------------------------------------------------------- #
def test_order_api_payload():
    print("[10] 下单接口参数构造（flatten / 订单号 / 收寄件人）")
    import order_api as oa

    flat = oa.flatten({"Weight": 1, "Sender": {"Name": "张三", "Mobile": "13800138000"},
                       "SaveSender": True, "Drop": None})
    check("嵌套键扁平化为 Sender[Name]", flat.get("Sender[Name]") == "张三", str(flat))
    check("嵌套键扁平化为 Sender[Mobile]", flat.get("Sender[Mobile]") == "13800138000")
    check("bool 序列化为 true", flat.get("SaveSender") == "true")
    check("None 字段被跳过", "Drop" not in flat)
    check("数值转字符串", flat.get("Weight") == "1")

    code = oa.gen_platform_order_code()
    check("订单号以 KDN 开头", code.startswith("KDN"), code)
    check("订单号 KDN+毫秒时间戳+6位随机", 21 <= len(code) <= 24 and code[3:].isdigit(), code)

    region = {"province": "广东省", "city": "深圳市", "area": "南山区", "address": "科技园"}
    pm = oa.build_party(region, "张三", "13800138000")
    check("11位手机号走 Mobile", pm.get("Mobile") == "13800138000" and "Tel" not in pm, str(pm))
    pt = oa.build_party(region, "张三", "0755-12345678")
    check("带横杠号码走 Tel", pt.get("Tel") == "0755-12345678" and "Mobile" not in pt, str(pt))
    check("省市区分字段正确",
          (pm["ProvinceName"], pm["CityName"], pm["ExpAreaName"]) ==
          ("广东省", "深圳市", "南山区"))

    payload = oa.build_order_payload(
        region, region, "张三", "13800138000", "张三", "13800138000",
        "STO", "1", 6.19, "服装", "2026-10-05 09:00:00", "2026-10-05 20:00:00",
        quantity=2, remark="轻拿轻放")
    for k in ("PlatFormOrderCode", "ShipperCode", "Quantity", "PayType", "PayAmount",
              "Weight", "Sender", "Receiver", "StartDate", "EndDate", "GoodsName",
              "Remark", "SaveSender", "SaveReceiver"):
        check(f"payload 含字段 {k}", k in payload)
    check("默认现付 PayType=1", payload["PayType"] == 1)
    check("数量与重量透传", payload["Quantity"] == 2 and payload["Weight"] == "1")
    check("取件时间透传", payload["StartDate"] == "2026-10-05 09:00:00")


# --------------------------------------------------------------------------- #
# 11. 渠道匹配与取件时间段
# --------------------------------------------------------------------------- #
def test_shipper_match_and_slots():
    print("[11] 快递渠道匹配与取件时间段挑选")
    import order_api as oa
    rows = [
        {"shipper_code": "shunfeng", "shipper_name": "顺丰速递", "available": True, "cost": 18.9},
        {"shipper_code": "jtexpress", "shipper_name": "极兔快递", "available": True, "cost": 4.69},
        {"shipper_code": "shentong", "shipper_name": "申通快递", "available": False, "cost": None},
    ]
    # 接口编码不按通用缩写来（顺丰=shunfeng、申通=shentong），客户只会说中文名或 SF/STO
    check("按接口编码匹配", oa.match_shipper(rows, "shunfeng")[0]["shipper_code"] == "shunfeng")
    check("按通用缩写 SF 匹配", oa.match_shipper(rows, "SF")[0]["shipper_code"] == "shunfeng")
    check("按中文名「顺丰」匹配",
          oa.match_shipper(rows, "顺丰")[0]["shipper_code"] == "shunfeng")
    check("STO → shentong", oa.match_shipper(rows, "STO")[0]["shipper_code"] == "shentong")
    check("大小写不敏感", oa.match_shipper(rows, "shentong")[0]["shipper_code"] == "shentong")
    check("匹配不到返回 None", oa.match_shipper(rows, "火星快递")[0] is None)
    check("空输入返回 None", oa.match_shipper(rows, None)[0] is None)
    check("空列表不炸", oa.match_shipper([], "SF")[0] is None)

    slots = [
        {"start": "2020-01-01 09:00:00", "end": "2020-01-01 20:00:00", "end_fetch": ""},
        {"start": "2099-01-01 09:00:00", "end": "2099-01-01 20:00:00", "end_fetch": ""},
    ]
    s, e = oa.pick_slot(slots)
    check("自动跳过已开始的时段", e is None and s["start"].startswith("2099"), str(s))
    s2, _ = oa.pick_slot(slots, 1)
    check("显式序号优先于时间判断", s2["start"].startswith("2020"))
    check("序号越界报错", bool(oa.pick_slot(slots, 9)[1]))
    check("空时间段报错", bool(oa.pick_slot([])[1]))
    check("全过期时回退第一段", oa.pick_slot([slots[0]])[0]["start"].startswith("2020"))
    check("fmt_slot 输出可读文案", isinstance(oa.fmt_slot(slots[1]), str))
    check("fmt_slot 空值不炸", oa.fmt_slot(None) == "-")


# --------------------------------------------------------------------------- #
# 12. 下单安全闸门（mock 网络，绝不产生真实订单）
# --------------------------------------------------------------------------- #
def test_order_safety_gate():
    print("[12] 下单安全闸门：预览不提交 + 余额不足拦截")
    import order_api as oa
    import place_order as po

    saved = {
        "query_once": po.query_once,
        "get_balance": oa.get_balance,
        "get_default_addr": oa.get_default_addr,
        "get_accessible_list": oa.get_accessible_list,
        "submit_order": po.submit_order,
        "order_log": po.ORDER_LOG,
    }
    d = tempfile.mkdtemp(prefix="xdcc_selftest_")
    po.ORDER_LOG = os.path.join(d, "orders.jsonl")

    fake_rows = [{"shipper_code": "STO", "shipper_name": "申通快递", "available": True,
                  "cost": 6.19, "market_cost": 12.0, "comment": "", "raw": {}}]
    po.query_once = lambda *a, **k: (fake_rows, None)
    oa.get_default_addr = lambda t, timeout=30: (
        {"FullName": "张三", "MobilePhone": "13800138000"}, None)
    oa.get_accessible_list = lambda t, s, r, c, timeout=30: (
        [{"start": "2099-01-01 09:00:00", "end": "2099-01-01 20:00:00", "end_fetch": ""}], None)

    s_region = {"province": "广东省", "city": "深圳市", "area": "南山区",
                "address": "科技园", "warnings": []}
    r_region = {"province": "浙江省", "city": "杭州市", "area": "西湖区",
                "address": "文三路", "warnings": []}

    # --- 余额不足必须拦下，不能带着会失败的单子走到提交 ---
    oa.get_balance = lambda t, timeout=30: ({"AvailableAmount": 1.0}, None)
    ctx, err = po.prepare_order(s_region, r_region, "张三", "13800138000",
                                "张三", "13800138000", 1, "服装", "tok",
                                os.path.join(d, "creds.env"))
    check("余额不足被拦截", err is not None and "余额" in err, f"err={err}")

    # --- 余额充足时正常组装 ---
    oa.get_balance = lambda t, timeout=30: ({"AvailableAmount": 100.0}, None)
    ctx, err = po.prepare_order(s_region, r_region, "张三", "13800138000",
                                "张三", "13800138000", 1, "服装", "tok",
                                os.path.join(d, "creds.env"))
    check("正常场景组装成功", err is None, f"err={err}")
    if err is None:
        check("payload 带寄件人姓名", ctx["payload"]["Sender"]["Name"] == "张三")
        check("payload 带收件人手机", ctx["payload"]["Receiver"]["Mobile"] == "13800138000")
        check("选中渠道与报价一致", ctx["shipper_code"] == "STO" and ctx["pay_amount"] == 6.19)
        check("预览标记 confirm=False", ctx["confirm"] is False)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            po.print_preview(ctx)
        check("预览含渠道与费用", "申通快递" in buf.getvalue() and "6.19" in buf.getvalue())
        check("预览提示未提交", "未提交" in buf.getvalue())
        check("预览不产生订单日志", not os.path.exists(po.ORDER_LOG))

    # --- 最关键：预览模式下 submit_order 一次都不能被调用 ---
    def boom(*a, **k):
        raise AssertionError("预览模式下不应提交订单")

    po.submit_order = boom
    oa.get_balance = lambda t, timeout=30: ({"AvailableAmount": 100.0}, None)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            rc = po.main(["-f", "广东 深圳 南山", "-t", "浙江 杭州 西湖", "-w", "1",
                          "--to-name", "张三", "--to-phone", "13800138000",
                          "--token", "fake-token", "--no-log"])
        check("预览模式未提交订单", True)
        check("预览模式返回码为 0", rc == 0, f"rc={rc}")
    except AssertionError as e:
        check("预览模式未提交订单", False, str(e))

    # --- --dry-run 与 --confirm 互斥 ---
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            po.main(["-f", "广东 深圳 南山", "-t", "浙江 杭州 西湖",
                     "--to-name", "张三", "--to-phone", "13800138000",
                     "--token", "fake", "--dry-run", "--confirm"])
        check("--dry-run 与 --confirm 互斥", False, "未报错")
    except SystemExit:
        check("--dry-run 与 --confirm 互斥", True)

    for k, v in saved.items():
        if k == "query_once":
            po.query_once = v
        elif k == "submit_order":
            po.submit_order = v
        elif k == "order_log":
            po.ORDER_LOG = v
        else:
            setattr(oa, k, v)
    shutil.rmtree(d, ignore_errors=True)


# --------------------------------------------------------------------------- #
# 13. 地址智能识别（AddrRecognition）
# --------------------------------------------------------------------------- #
def test_addr_analysis():
    print("[13] 地址智能识别：字段规整与结果校验")
    import region as rg
    import order_api as oa
    import addr_parse as ap

    # --- 字段规整（纯函数，零网络）---
    n = oa.normalize_analysis(
        {"Name": "李四", "Mobile": "13800138000", "ProvinceName": "北京",
         "CityName": "北京市", "ExpAreaName": "朝阳区",
         "StreetName": "建国路", "Address": "88号"})
    check("直辖市裸名补‘市’", n["province"] == "北京市", n["province"])
    check("详细地址拼接 street+address", n["full_address"] == "建国路88号", n["full_address"])
    check("字段齐全", (n["name"], n["phone"], n["area"]) == ("李四", "13800138000", "朝阳区"))
    n2 = oa.normalize_analysis({"Address": "市中心", "ProvinceName": "上海市"})
    check("缺街道时 full_address 只取 address", n2["full_address"] == "市中心", n2["full_address"])
    check("缺字段不炸", oa.normalize_analysis({})["name"] == "")

    # --- 接口调用：mock post_form，同时验证空文本不发起请求 ---
    def fake_post(token, path, payload, timeout=30):
        fake_post.called.append((path, payload))
        return {"Name": "李四", "Mobile": "13800138000", "ProvinceName": "湖南省",
                "CityName": "怀化市", "ExpAreaName": "鹤城区",
                "StreetName": "迎丰街道", "Address": "中路189号"}, None
    fake_post.called = []
    orig = oa.post_form
    oa.post_form = fake_post
    try:
        fields, err = oa.analysis_address("tok", "李四13800138000湖南怀化鹤城迎丰中路189号")
        check("识别接口调用成功", err is None, str(err))
        check("走的是 AddressAnalysis 路径",
              any(p[0] == oa.EP_ADDRESS_ANALYSIS for p in fake_post.called),
              str(fake_post.called))
        check("接口只传 Content 一个参数",
              all(list(p[1].keys()) == ["Content"] for p in fake_post.called),
              str(fake_post.called[:1]))
        check("识别出姓名", fields["name"] == "李四", str(fields))
        check("电话归到 Mobile", fields["phone"] == "13800138000")
        check("街道与详细地址分开", (fields["street"], fields["address"]) ==
              ("迎丰街道", "中路189号"))
        check("汇总地址", fields["full_address"] == "迎丰街道中路189号", fields["full_address"])

        # 空文本：接口对空串返回 Code=500，必须先本地拦住
        fake_post.called = []
        fields, err = oa.analysis_address("tok", "")
        check("空文本直接本地拦截", fields is None and bool(err), f"{fields} {err}")
        check("空文本未发起请求", fake_post.called == [], str(fake_post.called))
    finally:
        oa.post_form = orig

    # --- 结果校验 ---
    db = rg.RegionDB()

    def v(prov, city, area, name="李四", phone="13800138000", street="", address="中路1号"):
        f = oa.normalize_analysis({"Name": name, "Mobile": phone, "ProvinceName": prov,
                                   "CityName": city, "ExpAreaName": area,
                                   "StreetName": street, "Address": address})
        w, fatal = ap.validate(f, db)
        return f, w, fatal

    _, w, fatal = v("湖南省", "怀化市", "鹤城区")
    check("正常识别无致命错误", not fatal, str(fatal))

    # 实测：喂一段完全乱码，接口照样返回 200 并「脑补」出湖北随州——必须能被拦下
    _, w, fatal = v("湖北省", "随州市", "随县", name="", phone="")
    check("乱码无姓名被拦下", any("姓名" in x for x in fatal), str(fatal))
    check("乱码无电话被拦下", any("电话" in x for x in fatal), str(fatal))

    _, _, fatal = v("火星省", "火星市", "火星区")
    check("省不在库里被拦下", any("省「火星省」" in x for x in fatal), str(fatal))
    _, _, fatal = v("广东省", "长沙市", "岳麓区")
    check("市不属于省被拦下", any("市「长沙市」" in x for x in fatal), str(fatal))
    _, _, fatal = v("广东省", "深圳市", "岳麓区")
    check("区县不属于市被拦下", any("区县「岳麓区」" in x for x in fatal), str(fatal))

    # 直筒子市（东莞）接口不返回区县，ExpAreaName 会回落成 CityName：只告警不拦
    _, w, fatal = v("广东省", "东莞市", "东莞市")
    check("直筒子市不致命", not fatal, str(fatal))
    check("直筒子市给出告警", any("直筒子市" in x for x in w), str(w))

    # 直辖市 CityName 等于 ProvinceName
    _, w, fatal = v("上海市", "上海市", "浦东新区")
    check("直辖市正常通过", not fatal, str(fatal))

    # 座机与手机号
    check("识别手机号", ap.is_phone("13800138000"))
    check("识别带横杠座机", ap.is_phone("020-88886666"))
    check("识别带区号无横杠座机", ap.is_phone("02088886666"))
    check("拒非法号码", not ap.is_phone("12345") and not ap.is_phone(""))

    _, _, fatal = v("湖南省", "怀化市", "鹤城区", name="李四", phone="")
    check("缺电话被拦下", any("电话" in x for x in fatal), str(fatal))
    _, w, fatal = v("湖南省", "怀化市", "鹤城区", name="欧阳平安乐逍遥", phone="13800138000")
    check("异常长姓名只告警不拦", not fatal and any("姓名" in x for x in w), str(w))

    # region_of 产出可直接喂给下单链路的结构
    f, _, _ = v("湖南省", "怀化市", "鹤城区")
    r = ap.region_of(f)
    check("region_of 输出省市与详细地址",
          (r["province"], r["city"], r["area"]) == ("湖南省", "怀化市", "鹤城区"), str(r))
    check("region_of 汇总进 address", r["address"] == "中路1号", r["address"])
    check("region_of 带 warnings 键", "warnings" in r)


# --------------------------------------------------------------------------- #
# 14. 寄件管理：列表 / 详情 / 取消（mock 网络）
# --------------------------------------------------------------------------- #
def test_manage_order():
    print("[14] 寄件列表 / 详情 / 取消：状态字典与取消闸门")
    import order_api as oa
    import manage_order as mo

    # --- 状态字典 ---
    check("订单状态 6=已取消", oa.fmt_order_status(6) == "已取消")
    check("订单状态 8=已签收", oa.fmt_order_status("8") == "已签收")
    check("未知订单状态回落 '-'", oa.fmt_order_status(99) == "-")
    check("物流状态按页面口径只在 >=4 时映射",
          oa.fmt_logistics_status(1, 1) == "-" and oa.fmt_logistics_status(5, 5) == "已签收")
    check("支付状态 2=已解冻", oa.fmt_pay_status(2) == "已解冻")
    check("工单状态 0=待处理", oa.fmt_work_order_status("0") == "待处理")
    check("可取消仅 1/2/3",
          oa.can_cancel({"OrderStatus": 1}) and oa.can_cancel({"OrderStatus": 3})
          and not oa.can_cancel({"OrderStatus": 4}) and not oa.can_cancel({}))

    # --- 行规整 ---
    row = oa.fmt_order_row({
        "OrderCode": "260926000005", "ShipperName": "极兔快递", "OrderStatus": 8,
        "LogisticsStatus": 5, "PayStatus": 3, "PredictCost": 4.69,
        "Receiver": {"FullName": "张三", "Mobile": "131****8888", "Address": "某某路1号"},
        "Sender": {"FullName": "张三"}, "CreateTime": "2026-09-26 10:17:21",
        "LogisticsCode": "JT0025925955599",
    })
    check("列表行带订单号与快递公司",
          (row["order_code"], row["shipper"]) == ("260926000005", "极兔快递"))
    check("列表行运费转 float", row["predict_cost"] == 4.69 and isinstance(row["predict_cost"], float))
    check("列表行标出可取消性", row["cancelable"] is False)
    check("列表行带脱敏手机号", row["receiver_mobile"] == "131****8888")
    check("cost 为脏数据不炸", oa.fmt_order_row({"PredictCost": "abc"})["predict_cost"] == 0.0)

    # --- 列表接口：走对路径、把筛选条件透传 ---
    calls = []

    def fake_post(token, path, payload, timeout=30):
        calls.append((path, payload))
        return {"ResultList": [{"OrderCode": "A1", "OrderStatus": 2}],
                "TotalCount": 65}, None

    orig = oa.post_form
    oa.post_form = fake_post
    try:
        rows, total, err = oa.search_order_list("tok", keyword="A1", order_status=2,
                                                page_size=50, timeout=5)
        check("列表请求成功", err is None and total == 65, f"{err} {total}")
        check("列表走 SearchOrderList 路径", calls[0][0] == oa.EP_SEARCH_ORDER_LIST, calls[0][0])
        check("关键字同时喂 OrderCode 与 LogisticsCode",
              calls[0][1]["OrderCode"] == "A1" and calls[0][1]["LogisticsCode"] == "A1",
              str(calls[0][1]))
        # post_form 里才做 flatten（int → str），这里断言的是提交前的原始值
        check("订单状态透传", str(calls[0][1]["OrderStatus"]) == "2", str(calls[0][1]))

        # 取消：空单号本地拦住，不该发请求
        calls.clear()
        data, cerr = oa.cancel_order("tok", "")
        check("空单号本地拦截", data is None and cerr == "订单号为空" and calls == [], str(calls))

        calls.clear()
        data, cerr = oa.cancel_order("tok", " 260926000005 ")
        check("取消成功", err is None and cerr is None and data is not None, str(cerr))
        check("取消走 CancelOrder 路径", calls[0][0] == oa.EP_CANCEL_ORDER, calls[0][0])
        check("取消只传 OrderCode 且已去空格",
              list(calls[0][1].items()) == [("OrderCode", "260926000005")], str(calls[0][1]))
    finally:
        oa.post_form = orig

    # --- CLI 闸门：cancel 默认预演，绝不调用 CancelOrder ---
    detail_row = {"OrderCode": "X1", "OrderStatus": 2, "LogisticsStatus": 1, "PayStatus": 2,
                  "PredictCost": 6.0, "Receiver": {"FullName": "张三", "Mobile": "138****0000",
                                                   "Address": "某某路"}, "Sender": {},
                  "CreateTime": "2026-09-26 10:17:21", "ShipperName": "极兔快递",
                  "LogisticsCode": "JT1"}
    oa.get_order_detail = lambda t, code, timeout=30: (detail_row, None)
    oa.cancel_order = lambda *a, **k: (None, AssertionError("预演模式不应真的取消"))
    try:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = mo.main(["cancel", "X1", "--token", "fake"])
        out = buf.getvalue()
        check("cancel 预演返回 0", rc == 0, f"rc={rc}")
        check("cancel 预演提示未取消", "没有真的取消" in out, out[:200])
        check("cancel 预演给出确认命令", "--confirm" in out)
    finally:
        pass
    # 不可取消的订单直接跳过
    oa.get_order_detail = lambda t, code, timeout=30: ({**detail_row, "OrderStatus": 8}, None)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = mo.main(["cancel", "X1", "--token", "fake"])
    check("已签收订单跳过取消", rc == 0 and "不属于可取消范围" in buf.getvalue(), buf.getvalue()[:200])
    oa.get_order_detail = orig_get_order_detail = oa.get_order_detail


# --------------------------------------------------------------------------- #
# 15. 工单：分类 / 列表 / 详情 / 提交（mock 网络）
# --------------------------------------------------------------------------- #
def test_work_order():
    print("[15] 工单：分类匹配 / 列表 / 详情 / 提交闸门")
    import order_api as oa
    import ticket as tk

    groups = [{"code": 993, "group": "投诉", "items": [
        {"code": 2, "name": "快递员服务态度差"}, {"code": 13, "name": "快递员私下收费"}]},
        {"code": 992, "group": "问题件", "items": [
            {"code": 8, "name": "丢件"}, {"code": 6, "name": "包裹破损"}]}]
    flat = oa.flatten_work_order_categories(groups)
    check("分类树拍平", len(flat) == 4 and flat[0] == {"code": 2, "name": "快递员服务态度差",
                                                       "group": "投诉"}, str(flat))
    check("按编码匹配", oa.match_work_order_category(groups, "13")[0]["name"] == "快递员私下收费")
    check("按中文名匹配", oa.match_work_order_category(groups, "丢件")[0]["code"] == 8)
    check("按分组/类型匹配",
          oa.match_work_order_category(groups, "投诉/包裹破损")[0]["code"] == 6)
    check("接口不返回的 18 也能兜底",
          oa.match_work_order_category(groups, "更改收件信息")[0] ==
          {"code": 18, "name": "更改收件信息", "group": "其他"})
    e = oa.match_work_order_category(groups, "火星件")[1]
    check("找不到类型时列出候选", e and "丢件" in e and "快递员服务态度差" in e, e)

    # 附加必填项规则（接口分类树不返回，只能本地内置）
    check("重量异常要反馈重量", oa.work_order_rule(3).get("need_weight") is True)
    check("丢件要商品价值", oa.work_order_rule(8).get("need_value") is True)
    check("更改收件信息要新收件地址", oa.work_order_rule(18).get("need_new_address") is True)

    # --- 提交体验证（复刻页面 verifyData） ---
    p = oa.build_work_order_payload("A1", 2, "态度差", "张三", "13800138000")
    check("工单类型转 int", p["WorkOrderType"] == 2)
    check("自动拼 Reason 附言", p["Reason"] == "我是张三,电话：13800138000,如有疑问请联系我。")
    check("Role/PayMode/SourcePage 与页面一致",
          (p["Role"], p["PayMode"], p["SourcePage"]) == ("1", 4, 1))
    check("ImageNameList 是空数组 JSON", p["ImageNameList"] == "[]")
    check("无附加项时不塞 TelWeight", "TelWeight" not in p)
    check("校验通过", oa.validate_work_order(p) == ([], []))
    check("缺问题描述被拦", any("问题描述" in x for x in oa.validate_work_order(
        oa.build_work_order_payload("A1", 2, "", "张三", "13800138000"))[1]))
    check("缺姓名被拦", any("姓名" in x for x in oa.validate_work_order(
        oa.build_work_order_payload("A1", 2, "x", "", "13800138000"))[1]))
    check("缺电话被拦", any("手机" in x for x in oa.validate_work_order(
        oa.build_work_order_payload("A1", 2, "x", "张三", ""))[1]))
    check("非手机号只告警", any("手机号" in x for x in oa.validate_work_order(
        oa.build_work_order_payload("A1", 2, "x", "张三", "010-88886666"))[0]))
    w, fatal = oa.validate_work_order(oa.build_work_order_payload("A1", 3, "重了", "刘", "1343"))
    check("重量异常缺反馈重量被拦", any("反馈重量" in x for x in fatal), str(fatal))
    check("丢件缺商品价值被拦", any("商品价值" in x for x in oa.validate_work_order(
        oa.build_work_order_payload("A1", 8, "没了", "刘", "13800138000"))[1]))
    p18 = oa.build_work_order_payload("A1", 18, "换地址", "张三", "13800138000",
                                      new_receiver_name="张三", new_receiver_phone="13900000000",
                                      new_receiver_address="湖南长沙")
    check("更改收件信息并入问题描述", "【更改后收件信息】" in p18["WorkOrderContent"]
          and "湖南长沙" in p18["WorkOrderContent"], p18["WorkOrderContent"])
    check("更改收件信息三段齐全",
          (p18["NewReceiverName"], p18["NewReceiverPhone"], p18["NewReceiverAddress"]) ==
          ("张三", "13900000000", "湖南长沙"))
    check("新收件段缺地址被拦", any("新收件地址" in x for x in oa.validate_work_order(
        oa.build_work_order_payload("A1", 18, "换地址", "张三", "13800138000",
                                    new_receiver_name="张三",
                                    new_receiver_phone="13900000000"))[1]))

    # --- 拦截（type 1/2） ---
    i2 = oa.build_intercept_payload("A1", 2, "7890123", "张三", "13800138000")
    check("拦截退回带月结号", i2["MonthCode"] == "7890123")
    check("拦截退回不带新地址", "NewAddress" not in i2)
    i1 = oa.build_intercept_payload("A1", 1, "7890123", "张三", "13800138000",
                                    province="广东省", city="深圳市", area="南山区",
                                    address="科技园")
    check("拦截转寄带新地址",
          i1["NewAddress"] == {"ProvinceName": "广东省", "CityName": "深圳市",
                               "ExpAreaName": "南山区", "Address": "科技园"}, str(i1["NewAddress"]))
    check("拦截缺月结号被拦", any("月结号" in x for x in oa.validate_work_order(
        oa.build_intercept_payload("A1", 1, "", "刘", "13800138000"))[1]))

    # --- 列表接口 & 那个「工单详情只认内部 ID」的坑 ---
    calls = []

    def fake_post(token, path, payload, timeout=30):
        calls.append((path, payload))
        if path == oa.EP_WORK_ORDER_LIST:
            return {"ResultList": [{"WorkOrderCode": "260918000015", "ID": 819,
                                    "WorkOrderType": 16, "WorkOrderName": "其他",
                                    "WorkOrderStatus": 1, "WorkOrderContent": "测试一下工单",
                                    "OrderCode": "260916000004", "ShipperName": "圆通快递",
                                    "LogisticsCode": "YT2547990581476",
                                    "ReplyContent": "已与客户达成一致"}],
                    "TotalCount": 7}, None
        if path == oa.EP_WORK_ORDER_DETAIL:
            return {"WorkOrderCode": "260918000015", "WorkOrderType": 16,
                    "WorkOrderStatus": 1, "WorkOrderContent": "测试一下工单",
                    "WorkOrderReplyList": [{"ReplyContent": "已与客户达成一致"}]}, None
        return {}, None
    oa.post_form = fake_post
    try:
        rows, total, err = oa.search_work_orders("tok", status="1", page_size=10)
        check("工单列表成功", err is None and total == 7, f"{err}")
        check("工单列表带状态筛选", calls[0][1]["WorkOrderStatus"] == "1", str(calls[0][1]))
        fr = oa.fmt_work_order_row(rows[0])
        check("工单行带中文类型与状态",
              (fr["type_name"], fr["status"]) == ("其他", "已处理"), str(fr))
        check("工单行带回复内容", fr["reply"] == "已与客户达成一致", fr["reply"])
        fr2 = oa.fmt_work_order_row({"WorkOrderCode": "W2", "WorkOrderType": 8,
                                     "WorkOrderName": "丢件", "WorkOrderStatus": 0})
        check("工单无回复时回落 '-'", fr2["reply"] == "-", fr2["reply"])
        check("工单无回复时间回落 '-'", fr2["create_time"] == "-")

        calls.clear()
        oa.get_work_order_detail("tok", 819)
        check("工单详情传的是内部 ID 键",
              calls[0][0] == oa.EP_WORK_ORDER_DETAIL and calls[0][1] == {"ID": 819},
              str(calls[0]))
    finally:
        oa.post_form = orig_post_form = oa.post_form

    # --- CLI 闸门：new 默认预演，绝不调用 AddWorkOrder ---
    oa.get_work_order_categories = lambda t, timeout=30: (groups, None)
    oa.get_default_addr = lambda t, timeout=30: (
        {"FullName": "张三", "MobilePhone": "13800138000"}, None)

    def boom(*a, **k):
        raise AssertionError("预览模式下不应提交工单")

    oa.add_work_order = boom
    oa.intercept_waybill = boom
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = tk.main(["new", "--order-code", "A1", "--type", "丢件",
                      "--content", "包裹三天没更新", "--goods-value", "199.00",
                      "--token", "fake"])
    out = buf.getvalue()
    check("工单new 预演返回 0", rc == 0, f"rc={rc}")
    check("工单new 预演提示未提交", "未提交" in out and "预览" in out, out[:200])
    check("工单new 预演带商品价值", "199.00" in out)
    check("工单new 预演给出确认命令", "--confirm" in out)

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = tk.main(["intercept", "--order-code", "A1", "--type", "2",
                      "--month-code", "7890123", "--token", "fake"])
    check("拦截预演返回 0", rc == 0, f"rc={rc}")
    check("拦截预演提示未提交", "确认无误后加" in buf.getvalue(), buf.getvalue()[:200])

    # 缺必填（丢件没给商品价值）→ 直接拒绝，连预览都不走
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = tk.main(["new", "--order-code", "A1", "--type", "丢件", "--content", "没到",
                      "--token", "fake"])
    check("缺商品价值直接拒绝", rc != 0 and "商品价值" in buf.getvalue(), buf.getvalue()[:200])

    oa.get_work_order_detail = orig_detail = oa.get_work_order_detail


# --------------------------------------------------------------------------- #
# 运行
# --------------------------------------------------------------------------- #
def main() -> int:
    print("=" * 52)
    print("xdcc-price-query selftest")
    print("=" * 52)
    test_regions_data()
    test_region_resolve()
    test_price_payload()
    test_price_parse_sort()
    test_price_batch_read()
    test_common_creds_io()
    test_no_hard_exit()
    test_no_offsite_promotion()
    test_no_legacy_tracking_code()
    test_order_api_payload()
    test_shipper_match_and_slots()
    test_order_safety_gate()
    test_addr_analysis()
    test_manage_order()
    test_work_order()
    test_publish_compliance()
    print("=" * 52)
    print(f"通过 {PASS} / 失败 {FAIL}")
    print("=" * 52)
    _cleanup_tmpdirs()
    return 0 if FAIL == 0 else 1


def _cleanup_tmpdirs() -> None:
    """清理各用例留下的临时目录，避免长期堆积。"""
    base = tempfile.gettempdir()
    try:
        names = os.listdir(base)
    except OSError:
        return
    for name in names:
        if name.startswith("xdcc_selftest_"):
            shutil.rmtree(os.path.join(base, name), ignore_errors=True)


if __name__ == "__main__":
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError, OSError):
            pass
    sys.exit(main())
