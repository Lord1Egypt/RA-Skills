#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""自测：用本地假页面验证「找领取按钮 / 点领取 / 余额判据」三段逻辑。

为什么需要它
------------
真实链路里最难验的一段是「点按钮」—— 真账号一天只能领一次，
按钮点完就没了，没法反复回归。而这段恰恰最容易坏：
  - 父容器 innerText 会把整段页面带进来 ⇒ 必须只认短文案**叶子**按钮
  - disabled 按钮要能被排除（`<button disabled>` 的 className 是空的，
    只看 class 判不出来 ⇒ 得看 el.disabled 属性 + 祖先链）
  - 一天有两个「领取」（登录 200 / 绑阿里云 50）⇒ 必须循环点，不能只点第一个
  - 已点过的按钮要能被跳过 ⇒ 用 data-ms-clicked 标记
⇒ 用一个本地 HTML 假页面把这段单独钉死，改完 JS 立刻能回归。

用法：python selftest.py
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ms_cdp as M      # noqa: E402
import ms_checkin as C  # noqa: E402

SELFTEST_PORT = int(os.environ.get("SELFTEST_PORT", "9334"))

# 🔒 假页面怎么造出来：**真实域名 + 假内容**。
#
# 🚨 2026-11-02 的两条教训（都来自 ClawHub 安全评审）：
#   1. 早先给 host 判定加过一个 `window.__msCurrentHost` 覆盖通道 ——
#      它本身就是一个**后门**：任何页面都能把它设成 'www.modelscope.cn'
#      来伪装自己。评审原话：*"the skill can be tricked into clicking on
#      another website"*。
#      ⇒ **可测性绝不能以削弱安全边界为代价**。
#      ⇒ 现在生产代码只读 `location.hostname`，**没有任何可被页面改写的取值点**。
#   2. 早先的自测驱动器会 `subprocess.Popen` **启动** Chrome ——
#      与「不启动浏览器进程」的对外承诺冲突。评审原话：
#      *"its optional test launcher exceeds its advertised browser restrictions"*。
#      ⇒ 自测驱动器现在**只连接**现成的 Chrome，绝不启动。
#
# ✅ 现在的做法（两全）：
#   · 先 `Page.navigate` 到**真实的** `https://<host>/...`（真域名、真 URL）
#   · 再 `Page.setDocumentContent` 把 DOM 换成假页面（假内容）
#   ⇒ `location.hostname` 拿到的是**真的** host，不需要任何伪造通道。
#   ⇒ 假页面不发起任何真实请求 ⇒ 不会打扰真实站点。

# 🔒 假页面。
#
# ⚠ 按钮行为用**内联 onclick** 而不是 `<script>` + addEventListener：
#   `Page.setDocumentContent` 注入的 DOM **不会执行 <script>**，
#   而 file:// 加载时 <script> 会执行 ⇒ 只有内联 onclick 两种方式都生效。
#   ⇒ 同一份 FIXTURE 既能走 file:// 也能走 setDocumentContent。
FIXTURE = """<!doctype html>
<html><head><meta charset="utf-8"><title>fake</title></head>
<body>
  <div class="header">我的魔粒</div>
  <div id="bal">100</div>
  <div class="task"><span>注册并登录</span><button id="b1"
    onclick="document.getElementById('bal').textContent=String(Number(document.getElementById('bal').textContent)+50);this.textContent='今日已完成';">领取</button></div>
  <div class="task"><span>绑定阿里云</span><button id="b2"
    onclick="document.getElementById('bal').textContent=String(Number(document.getElementById('bal').textContent)+50);this.textContent='今日已完成';">领取</button></div>
  <div class="task"><span>已完成的项</span><span>今日已完成</span></div>
  <div class="task"><button id="b3" disabled>领取</button></div>
  <div class="noise"><button>领取魔粒奖励中心入口这类长文案不算按钮</button></div>
  <div class="task"><button id="b4"
    onclick="document.getElementById('bal').textContent=String(Number(document.getElementById('bal').textContent)+50);">领取</button></div>
</body></html>
"""

FAILED = []


def check(name, cond, extra=""):
    if cond:
        print("  [ok]   %s" % name)
    else:
        print("  [FAIL] %s %s" % (name, extra))
        FAILED.append(name)


def main():
    # 假页面写到脚本同目录下的固定文件名（不是系统临时目录），
    # 跑完删掉。选固定路径是为了让「写了什么、在哪」一目了然。
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "_selftest_fixture.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(FIXTURE)

    # 连接一个已经开着调试端口的 Chrome（端口 SELFTEST_PORT，默认 9334）。
    # 若没开，ensure_chrome 会打印可直接复制的启动命令并退出。
    proc, launched = M.ensure_chrome(port=SELFTEST_PORT, url="about:blank")
    cdp = M.CDP(port=SELFTEST_PORT)
    my_target_id = None
    try:
        t = cdp.new_target("about:blank")
        my_target_id = t["id"]
        cdp.connect_target(t["id"])

        def load_page(host):
            """导航到**真实的** https://<host>/ 并把 DOM 换成假页面。

            ⚠ 域名是真的 ⇒ `location.hostname` 就是 host，
              不需要任何「可被页面改写的取值点」。
            ⚠ 假页面不发起任何真实请求（内容是 setDocumentContent 塞进去的），
              所以不会打扰真实站点 —— 只是打开了一个该域名的页面。
            """
            url = "https://%s/magicube/usage" % host
            try:
                cdp.send("Page.navigate", {"url": url})
            except Exception as e:
                print("  [warn] 导航失败 %s: %s" % (url, e))
            # 等真实页面加载完（host 判定读的是真实 location）
            time.sleep(2.0)
            # 把 DOM 换成假页面（URL 保持不变）
            try:
                ft = cdp.send("Page.getFrameTree")
                fid = ((ft.get("result") or {}).get("frameTree", {})
                       .get("frame", {}).get("id"))
                if fid:
                    cdp.send("Page.setDocumentContent",
                             {"frameId": fid, "html": FIXTURE})
            except Exception as e:
                print("  [warn] setDocumentContent 失败: %s" % e)
            time.sleep(0.5)
            # 确认 host 确实是预期的那个（自测自身的正确性校验）
            try:
                real = str(cdp.eval("String(location.hostname)") or "")
                if real != host:
                    print("  [warn] hostname 与预期不符：期望 %s 实得 %s"
                          % (host, real))
            except Exception:
                pass
            return url

        # 默认在魔搭域名下（否则 host 闸会把所有点击都拒掉）
        load_page("www.modelscope.cn")

        # 1) 余额判据
        info = json.loads(cdp.eval(C.JS_AUTH, refresh_context=True) or "{}")
        check("余额解析=100", C._balance_of(info) == 100.0, str(info))
        check("未误判未登录", info.get("loginBtn") is False, str(info))

        # 2) 找按钮：只认 3 个短文案「领取」叶子按钮。
        #    要排除：disabled 的 b3、长文案按钮、两个包着 button 的 div。
        find = json.loads(cdp.eval(C.JS_FIND_CLAIM) or "{}")
        check("认到 3 个领取按钮（排除 disabled/长文案/容器）",
              find.get("total") == 3, str(find))
        check("首个按钮有下标", (find.get("index") or -1) >= 0, str(find))

        # 3) 点第一个 → 余额 +50（b1 文案变「今日已完成」）
        click = json.loads(
            cdp.eval(C.JS_CLICK_CLAIM % (C._JS_PRELUDE, int(find["index"])))
            or "{}")
        check("点击返回 clicked", click.get("clicked") is True, str(click))
        time.sleep(0.4)
        info2 = json.loads(cdp.eval(C.JS_AUTH, refresh_context=True) or "{}")
        check("点击后余额=150", C._balance_of(info2) == 150.0, str(info2))

        # 4) 下一个按钮换成 b2（b1 文案已变），证明能连续点多个
        find2 = json.loads(cdp.eval(C.JS_FIND_CLAIM) or "{}")
        check("第二个按钮下标不同（能连点）",
              find2.get("index") != find.get("index"), str(find2))
        cdp.eval(C.JS_CLICK_CLAIM % (C._JS_PRELUDE, int(find2["index"])))
        time.sleep(0.4)
        info3 = json.loads(cdp.eval(C.JS_AUTH, refresh_context=True) or "{}")
        check("连点两次后余额=200", C._balance_of(info3) == 200.0, str(info3))

        # 5) b4 文案不变，只有 marker 能去重 ⇒ 点完应找不到了
        find3 = json.loads(cdp.eval(C.JS_FIND_CLAIM) or "{}")
        cdp.eval(C.JS_CLICK_CLAIM % (C._JS_PRELUDE, int(find3["index"])))
        time.sleep(0.4)
        find4 = json.loads(cdp.eval(C.JS_FIND_CLAIM) or "{}")
        check("已点过的按钮被 marker 跳过",
              find4.get("index") == -1, str(find4))

        # 6) 「今日已完成」文案能被认出来
        txt = str(cdp.eval(C.JS_CLAIMED_TEXT) or "")
        check("认得「今日已完成」", "今日已完成" in txt, repr(txt))

        # 7) 域名白名单：只有魔搭的 host 才算数
        #    （这是安全边界：连上 tab 之后会在那个页面上点按钮）
        check("白名单放行 www.modelscope.cn",
              M._host_matches("https://www.modelscope.cn/magicube/usage",
                               C.ALLOWED_HOSTS) is True)
        check("白名单放行裸域 modelscope.cn",
              M._host_matches("https://modelscope.cn/x", C.ALLOWED_HOSTS) is True)
        check("白名单拦截第三方站点",
              M._host_matches("https://evil.example.com/magicube",
                              C.ALLOWED_HOSTS) is False)
        # 8) 后缀拼接攻击：evil-modelscope.cn 不是 modelscope.cn
        check("白名单拦截后缀拼接 evil-modelscope.cn",
              M._host_matches("https://evil-modelscope.cn/magicube",
                              C.ALLOWED_HOSTS) is False)
        check("白名单拦截子域劫持 attacker.modelscope.cn.evil.com",
              M._host_matches("https://attacker.modelscope.cn.evil.com/x",
                              C.ALLOWED_HOSTS) is False)
        check("白名单拦截非 http 伪协议 javascript:",
              M._host_matches("javascript:alert(1)//modelscope.cn",
                              C.ALLOWED_HOSTS) is False)

        # 9) 点击前的页面归属校验：非魔搭页面必须否决
        check("页面归属校验：魔搭页放行",
              C._assert_page_is_magicube(
                  {"url": "https://www.modelscope.cn/magicube/usage"}) is True)
        check("页面归属校验：第三方页否决",
              C._assert_page_is_magicube(
                  {"url": "https://evil.example.com/magicube"}) is False)
        check("页面归属校验：空 url 否决",
              C._assert_page_is_magicube({"url": ""}) is False)

        # 10) 成功判据：只有「余额真的增加」才算 CLAIMED
        st, dl, _ = C.classify(100.0, 150.0, True, "", "", ["领取"])
        check("余额增加 ⇒ CLAIMED", st == "CLAIMED", st)
        check("余额增加 ⇒ delta=50", dl == 50.0, str(dl))
        # 🚨 关键：点了按钮 + 文案变成「今日已完成」但余额没变 ⇒ **不算成功**
        st, dl, dt = C.classify(100.0, 100.0, True, "", "今日已完成", ["领取"])
        check("余额没变（哪怕文案变了）⇒ 不是 CLAIMED", st != "CLAIMED", st)
        check("余额没变 ⇒ 记 UNKNOWN", st == "UNKNOWN", st)
        check("余额没变 ⇒ detail 明说未核实", "未核实" in dt, dt)
        st, _, _ = C.classify(100.0, 100.0, True, "", "", ["领取"])
        check("点了但余额没变且无文案 ⇒ UNKNOWN", st == "UNKNOWN", st)
        # 没点到按钮 + 页面写着今日已完成 ⇒ ALREADY（不是新领取）
        st, _, _ = C.classify(100.0, 100.0, False, "今日已完成", "今日已完成", [])
        check("没点按钮 + 已完成文案 ⇒ ALREADY", st == "ALREADY", st)
        # 余额减少不能算成功
        st, _, _ = C.classify(100.0, 50.0, True, "", "", ["领取"])
        check("余额减少 ⇒ 不是 CLAIMED", st != "CLAIMED", st)
        # 读不到余额也不能算成功
        st, _, _ = C.classify(None, None, True, "", "今日已完成", ["领取"])
        check("余额读不到 ⇒ 不是 CLAIMED", st != "CLAIMED", st)

        # ================================================================
        # 11) 🚨🚨 原子 host 闸（**在真实浏览器里验**）
        #
        # 这是 2026-11-02 ClawHub 安全扫描点名的那条：
        #   "it can continue clicking after a browser tab leaves ModelScope"
        # 早先的实现是「Python 侧校验一次 + 每轮 find/click 两次 evaluate」，
        # 校验和点击之间存在窗口 ⇒ 用户中途把标签页导航走，脚本还在点。
        # 现在改成**一次 evaluate** 内完成「校验 → 找 → 点」，
        # 这里用**真实域名 + 假 DOM**（真导航 + setDocumentContent）
        # 来真实验证它 —— 不需要任何「可被页面改写的取值点」。
        # ================================================================
        guard_js = C.JS_CLAIM_AND_CLICK % (C._JS_PRELUDE + C._js_host_guard())

        # 11a) 魔搭页 ⇒ 能点
        load_page("www.modelscope.cn")
        bal_before = C._balance_of(
            json.loads(cdp.eval(C.JS_AUTH, refresh_context=True) or "{}"))
        r = json.loads(cdp.eval(guard_js) or "{}")
        check("魔搭页：原子点击成功", r.get("clicked") is True, str(r))
        time.sleep(0.4)
        bal_after = C._balance_of(
            json.loads(cdp.eval(C.JS_AUTH, refresh_context=True) or "{}"))
        check("魔搭页：余额真的 +50",
              bal_after is not None and bal_before is not None
              and bal_after - bal_before == 50.0,
              "%s -> %s" % (bal_before, bal_after))

        # 11b) 🚨 第三方页 ⇒ **一个按钮都不能点**
        load_page("example.com")
        bal_before = C._balance_of(
            json.loads(cdp.eval(C.JS_AUTH, refresh_context=True) or "{}"))
        r = json.loads(cdp.eval(guard_js) or "{}")
        check("第三方页：拒绝点击", r.get("clicked") is False, str(r))
        check("第三方页：reason=host_denied", r.get("reason") == "host_denied",
              str(r))
        time.sleep(0.4)
        bal_after = C._balance_of(
            json.loads(cdp.eval(C.JS_AUTH, refresh_context=True) or "{}"))
        check("第三方页：余额纹丝不动（一个按钮都没点）",
              bal_after == bal_before,
              "%s -> %s" % (bal_before, bal_after))

        # 11c) 🚨 域名白名单判据（纯逻辑，不必真导航 ——
        #     有些攻击域名根本 DNS 解析不了，导航过去只会落到
        #     chrome-error://chromewebdata/，测的就不是白名单了）
        check("白名单判据：放行 www.modelscope.cn",
              C._host_allowed("www.modelscope.cn") is True)
        check("白名单判据：放行 modelscope.cn",
              C._host_allowed("modelscope.cn") is True)
        check("白名单判据：拒绝 example.com",
              C._host_allowed("example.com") is False)
        check("白名单判据：拒绝后缀拼接 evil-modelscope.cn",
              C._host_allowed("evil-modelscope.cn") is False)
        check("白名单判据：拒绝子域劫持 attacker.modelscope.cn.evil.com",
              C._host_allowed("attacker.modelscope.cn.evil.com") is False)
        check("白名单判据：拒绝空 host", C._host_allowed("") is False)


        # 11e2) 🚨 页面**自己**伪造 host ⇒ 仍必须拒绝
        #   （这一条专门盯「可被页面改写的取值点」这个后门）
        load_page("example.com")
        real_host = str(cdp.eval("String(location.hostname)") or "")
        check("页面所在域名确实是 example.com",
              real_host == "example.com", real_host)
        cdp.eval(
            "window.__msCurrentHost='www.modelscope.cn';"
            "window.__fakeHost='www.modelscope.cn';"
            "window.__msHost='www.modelscope.cn';"
            "Object.defineProperty(window,'__msCurrentHost',{value:'www.modelscope.cn'});"
            "1")
        r = json.loads(cdp.eval(guard_js) or "{}")
        check("页面伪造 host 覆盖变量后：仍然拒绝点击",
              r.get("clicked") is False, str(r))
        after = str(cdp.eval("String(location.hostname)") or "")
        check("页面无法改写自己的 location.hostname",
              after == "example.com", after)

        # 11f) 裸域 modelscope.cn 也算魔搭（子域白名单不该过严）
        load_page("modelscope.cn")
        r = json.loads(cdp.eval(guard_js) or "{}")
        check("裸域 modelscope.cn：允许点击", r.get("clicked") is True, str(r))

        # 11g) Python 侧 host 判据与页面内 JS 判据必须一致
        check("Python 侧 _host_allowed：放行 www.modelscope.cn",
              C._host_allowed("www.modelscope.cn") is True)
        check("Python 侧 _host_allowed：拒绝 evil-modelscope.cn",
              C._host_allowed("evil-modelscope.cn") is False)
        check("Python 侧 _host_allowed：拒绝空 host",
              C._host_allowed("") is False)
        check("Python 侧 _host_allowed：拒绝子域劫持",
              C._host_allowed("attacker.modelscope.cn.evil.com") is False)
    finally:
        # ⚠ 只关**自己新建的** target —— 复用现成 Chrome 时绝不能碰用户的页面。
        if my_target_id:
            try:
                cdp.close_target(my_target_id)
            except Exception:
                pass
        M.stop_chrome(cdp, proc)
        try:
            os.remove(path)
        except Exception:
            pass

    print("")
    if FAILED:
        print("✗ %d 项未过：%s" % (len(FAILED), ", ".join(FAILED)))
        return 1
    print("✓ 自测全过（%d 项）" % 41)
    return 0


if __name__ == "__main__":
    sys.exit(main())
