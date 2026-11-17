#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""魔搭（ModelScope）魔粒（Magicube）每日自动领取。

这个脚本做什么
--------------
连接**你自己已经打开的** Chrome（带调试端口），在魔粒页面上点一下「领取」
按钮，并记录余额前后差值。就这一件事。

这个脚本不做什么（能力边界）
--------------------------
- 不启动、不结束任何浏览器进程 —— 浏览器窗口归你，脚本只连接
- 不读写、不删除你浏览器里的任何文件 —— profile 目录完全由 Chrome 自己管
- 不读取、不导出、不解密任何 cookie 或登录凭据
- 不调用任何非公开接口 —— 只在真实页面上按真实按钮
- 不修改系统代理、环境变量或任何全局配置
- 不安装任何依赖包（只用 Python 标准库）

对浏览器唯一的写入就是那一次点击。

背景与三个被纠正过的前提
------------------------
1. **魔粒是魔搭 API-Inference 的算力额度**，官方中文名「魔粒」/ 英文 Magicube
   （文档 modelscope.cn/docs/magicube/intro）。轻量 0.5 / 主流 1 / 旗舰 2 粒每次。
   满额 500 粒 = 旗舰 250 次 / 主流 500 次 / 轻量 1000 次每天。
2. **没有官方签到 API**。任何"自动签到"脚本都是模拟网页操作 ⇒ 站点改版就失效。
   所以本脚本走 **CDP 真点页面**，只按真实按钮，不走非公开接口。
3. 🚨 **不是"登录即到账"，要在魔粒页点「领取」**。
   如果判据只写"页面读得到余额就算成功"，那等于**只登录不领取也报成功** ——
   典型的假绿：日志天天 OK，魔粒一分没多。
   ⇒ 判据必须是 **点了「领取」且余额真的增加**，或页面明确显示「今日已完成」。

用法
----
    python ms_checkin.py              # 每天：连浏览器 → 点「领取」→ 记余额
    python ms_checkin.py --login      # 首次/掉登录：等你登录完并自动验证
    python ms_checkin.py --status     # 只查余额，不点领取
    python ms_checkin.py --probe      # 打印页面判据，排查用
    python ms_checkin.py --json       # 额外输出一行 JSON（便于程序消费）

前置条件
--------
先自己启动一个带调试端口的 Chrome（脚本不会代劳，端口不通时会打印
可直接复制的命令）：

    chrome.exe --remote-debugging-port=9333 \
      --user-data-dir=<独立 profile 目录> https://www.modelscope.cn/magicube/usage

⚠ 独立 profile 是 Chrome 136+ 的官方要求（默认 user-data-dir 不允许开调试
  端口），也因此登录态与日常 Chrome 自然分开。日常 Chrome 里的会话数据
  本脚本既不读也不需要。

状态机（别把 UNKNOWN 当失败，也别把 ALREADY 当新领取）
--------------------------------------------------
    CLAIMED  点了「领取」且**余额确实增加**（记 before → after）  退出码 0
    ALREADY  没点到按钮，但页面写着「今日已完成 / 今日已领」   退出码 0
    NO_LOGIN 浏览器里没有魔搭会话 → 需要重新登录一次          退出码 2
    UNKNOWN  读不到判据 / 点了但余额没变（含「文案变了但余额没变」
            这种延迟到账情形）—— **未经核实就不算成功**        退出码 3

⚠ 只有「余额增加」是 CLAIMED 的充分条件。页面文案变了但余额没变时，
  一律记 UNKNOWN —— 那只是延迟到账的**可能**，不是领取成功的证据。
"""
import argparse
import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ms_cdp as M  # noqa: E402

USAGE_URL = "https://www.modelscope.cn/magicube/usage"
HOME_URL = "https://www.modelscope.cn/"

# 允许操作的站点白名单（安全边界，不是可选优化）。
# 本脚本连上某个 tab 之后会**在那个页面上点按钮**，所以必须先确认
# 它确实是魔搭的页面 —— 只按路径子串找 tab 会连上第三方站点。
ALLOWED_HOSTS = ["modelscope.cn"]

PORT = int(os.environ.get("MS_CDP_PORT", "9333"))
PROFILE = os.path.expanduser(
    os.environ.get("MS_CDP_PROFILE")
    or os.path.join("~", "chrome-ms-profile"))
LOG_PATH = os.path.expanduser(
    os.environ.get("MS_CHECKIN_LOG")
    or os.path.join("~", ".workbuddy", "data", "modelscope-magicube",
                    "checkin_log.json"))


def log(msg):
    print(msg, flush=True)


# ==========================================================================
# 页面判据（JS）
# ==========================================================================
# ⚠ 登录判据必须是「还有没有登录入口」，**不能**用「有没有『我的魔粒』字样」——
#   未登录时页面标题就叫「我的魔粒」，按字样判会把未登录误报成已登录。
# ⚠ 站点有中英两版文案（locale 可能落到英文），两边都要认，
#   否则英文页会被判成 UNKNOWN。
JS_AUTH = """
(function () {
  var t = document.body ? document.body.innerText : '';
  var loginBtn = /登录\\s*\\/\\s*注册|登录注册|login\\s*\\/\\s*register/i.test(t);
  var m = t.match(/(?:我的魔粒|My Magicubes?)\\s*\\n?\\s*([0-9][0-9,]*)/i);
  if (!m) {
    m = t.match(/(?:魔粒|Magicubes?)\\s*\\n?\\s*([0-9][0-9,]*)/i);
  }
  if (!m) {
    m = t.match(/(?:魔粒|Magicubes?)[^\\n]{0,12}?([0-9][0-9,]*)/i);
  }
  var nick = document.querySelector('[class*="userInfo"],[class*="user-info"],'
    + '[class*="avatar"],[class*="userName"],[class*="nickname"]');
  return JSON.stringify({
    url: location.href,
    loginBtn: loginBtn,
    magicube: m ? m[1] : null,
    hasNickEl: !!nick,
    len: t.length,
    head: t.slice(0, 200)
  });
})()
"""

# 魔粒相关文案（给 --probe 看）
JS_BALANCE = """
(function () {
  var t = document.body ? document.body.innerText : '';
  var out = [];
  var re = /([^\\n]{0,30}魔粒[^\\n]{0,40})/g, m;
  while ((m = re.exec(t)) !== null) { out.push(m[1].trim()); }
  return out.slice(0, 25).join(' || ');
})()
"""

JS_TEXT = "document.body ? document.body.innerText.slice(0, 4000) : ''"

JS_RESOURCES = (
    "performance.getEntriesByType('resource')"
    ".map(e => e.name)"
    ".filter(n => /magicube|point|credit|user|login|session/i.test(n))"
    ".slice(-40).join('\\n')"
)

# 「今天已领过」的文案（2026-10-29 实测页面）：每日发放两项会标「今日已完成」
# （注册并登录 200 / 绑定阿里云 50）。英文站与旧文案一并兜住，
# 少认一种就会把「已领」判成 UNKNOWN。
JS_CLAIMED_TEXT = """
(function () {
  var txt = document.body ? document.body.innerText : '';
  var m = txt.match(/今日已完成|今日已领|已领取|明天再来|already claimed|claimed today|completed today/i);
  return m ? m[0] : '';
})()
"""

# 找「领取」按钮：只认短文案的独立按钮（父容器 innerText 会把整段页面带进来）
_JS_PRELUDE = """
  function visible(el) {
    var r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  }
  function nodes() {
    return Array.prototype.slice.call(
      document.querySelectorAll('button, a, span, div'));
  }
  function disabledLike(el) {
    if (el.disabled === true) return true;
    var cls = String(el.className || '');
    if (/disabled|is-disabled/i.test(cls)) return true;
    if (el.getAttribute && el.getAttribute('aria-disabled') === 'true') return true;
    var p = el.parentElement;
    while (p) {
      if (p.disabled === true) return true;
      var pc = String(p.className || '');
      if (/disabled|is-disabled/i.test(pc)) return true;
      if (p.getAttribute && p.getAttribute('aria-disabled') === 'true') return true;
      p = p.parentElement;
    }
    return false;
  }
  function isClaim(el) {
    var s = (el.innerText || '').trim();
    if (!s || s.length > 8) return false;
    if (!/^(领取|立即领取|领取奖励|签到)$/.test(s)) return false;
    if (!visible(el)) return false;
    if (disabledLike(el)) return false;
    // ⚠ 只认「叶子」元素：<div class="task"><button>领取</button></div> 里
    //   那个 div 的 innerText 也正好是「领取」，会被误当成按钮点掉。
    //   BUTTON/A 自身是交互控件，豁免子元素检查。
    var tag = (el.tagName || '').toUpperCase();
    if (tag !== 'BUTTON' && tag !== 'A' && el.children.length > 0) return false;
    return true;
  }
"""

JS_FIND_CLAIM = """
(function () {
%s
  var ns = nodes(), idx = -1, label = null, total = 0;
  for (var i = 0; i < ns.length; i++) {
    if (!isClaim(ns[i])) continue;
    total++;
    if (ns[i].getAttribute('data-ms-clicked')) continue;
    if (idx < 0) { idx = i; label = (ns[i].innerText || '').trim(); }
  }
  return JSON.stringify({index: idx, label: label, total: total});
})()
""" % _JS_PRELUDE

# ⚠ 这里有两个占位符：%s = 公共 prelude，%d = 目标按钮在 nodes() 里的下标。
JS_CLICK_CLAIM = """
(function () {
%s
  var ns = nodes();
  var idx = %d;
  if (idx < 0 || idx >= ns.length) return JSON.stringify({clicked: false});
  var el = ns[idx];
  if (!isClaim(el)) return JSON.stringify({clicked: false, reason: 'changed'});
  el.setAttribute('data-ms-clicked', '1');
  el.click();
  return JSON.stringify({clicked: true, label: (el.innerText || '').trim()});
})()
"""

# 🔒🔒 页面归属闸（**必须在页面上下文里做，不能只在 Python 侧做**）。
#
# 🚨 为什么要放进 JS：
#   Python 侧那次校验发生在「读页面」那一刻，而真正的点击发生在**另一次**
#   CDP evaluate 里。这两次调用之间页面可能已经被导航走了（用户切了标签、
#   页面自己跳了路由、或者 SPA 把 location 换掉）。
#   ⇒ 「校验时的页面」和「点击时的页面」可能根本不是同一个，
#     于是会出现「浏览器标签已经离开魔搭，脚本却还在继续点」。
#
#   所以把校验**和点击合并到同一个 JS 执行里**：
#   同一段 JS 内部没有 await、不会让出事件循环 ⇒ 中间不可能被导航打断。
#   这才是「点下去之前确认自己还在魔搭」的**原子**写法。
#
# ⚠ 校验判据 = location.hostname 精确等于白名单域名，或以「.」+ 域名结尾。
#   用后缀匹配是为了兼容 www.modelscope.cn；但必须防住
#   「evil-modelscope.cn」「attacker.modelscope.cn.evil.com」这类拼接。
_JS_HOST_GUARD = """
  // 当前页面的 host。
  //
  // 🔒🔒 **只读 location.hostname，没有任何可被页面改写的取值点**。
  //
  // 🚨 2026-11-02 教训：曾经为了「可测性」加过一个 `window.__msCurrentHost`
  //   覆盖通道 —— 结果它本身就是一个**后门**：任何页面（包括恶意页面）都能
  //   把它设成 'www.modelscope.cn' 来伪装自己。ClawHub 的安全评审直接点名：
  //   *"the skill can be tricked into clicking on another website"*。
  //   ⇒ **可测性绝不能以削弱安全边界为代价**。
  //   ⇒ 测试改用「真实域名的假页面」来构造场景（见 selftest.py）。
  //
  // ⚠ 读不到 host（空串）一律拒绝 —— 宁可误伤也不能在不确定的页面上乱点。
  function currentHost() {
    try { return String(location.hostname || ''); } catch (e) { return ''; }
  }
  function hostAllowed() {
    var h = currentHost().toLowerCase();
    if (!h) return false;
    var allowed = %s;
    for (var i = 0; i < allowed.length; i++) {
      var suf = String(allowed[i]).toLowerCase();
      if (h === suf) return true;
      if (h.length > suf.length + 1 &&
          h.slice(-(suf.length + 1)) === '.' + suf) return true;
    }
    return false;
  }
"""


def _js_host_guard():
    """生成 host 白名单校验片段（ALLOWED_HOSTS 注入进 JS）。"""
    return _JS_HOST_GUARD % json.dumps(ALLOWED_HOSTS)


# 🔒 原子「校验 → 找 → 点」。**只发这一个 evaluate**。
#   返回 {clicked, label, reason, host}
#   reason 取值：
#     host_denied —— 当前页面不是魔搭，**没有点任何东西**
#     no_button   —— 页面上没有可点的「领取」按钮
#     changed     —— 找到的按钮已经不是按钮了（页面在我们看的那一瞬变了）
JS_CLAIM_AND_CLICK = """
(function () {
%s
  // ---- 第 1 道：页面归属 ----
  if (!hostAllowed()) {
    return JSON.stringify({clicked: false, reason: 'host_denied',
                           host: String(location.hostname || '')});
  }
  // ---- 第 2 道：找按钮 ----
  var ns = nodes(), idx = -1, label = null, total = 0;
  for (var i = 0; i < ns.length; i++) {
    if (!isClaim(ns[i])) continue;
    total++;
    if (ns[i].getAttribute('data-ms-clicked')) continue;
    if (idx < 0) { idx = i; label = (ns[i].innerText || '').trim(); }
  }
  if (idx < 0) {
    return JSON.stringify({clicked: false, reason: 'no_button', total: total,
                           host: String(location.hostname || '')});
  }
  // ---- 第 3 道：点之前再确认一次它还是那个按钮 ----
  var el = ns[idx];
  if (!isClaim(el)) {
    return JSON.stringify({clicked: false, reason: 'changed', total: total,
                           host: String(location.hostname || '')});
  }
  el.setAttribute('data-ms-clicked', '1');
  el.click();
  return JSON.stringify({clicked: true, label: label, total: total,
                         host: String(location.hostname || '')});
})()
"""


# ==========================================================================
# 页面读取
# ==========================================================================
def _balance_of(info):
    """从登录判据里取余额数字；取不到返回 None（不猜）。"""
    try:
        return float(str(info.get("magicube")).replace(",", ""))
    except (TypeError, ValueError):
        return None


def _read_page(cdp):
    """读一次页面判据 + 魔粒文案。返回 (info, lines)，读不到就抛。"""
    info = json.loads(cdp.eval(JS_AUTH, refresh_context=True) or "{}")
    try:
        lines = [x.strip() for x in str(cdp.eval(JS_BALANCE) or "").split("||")
                 if x.strip()]
    except Exception:
        lines = []
    return info, lines[:10]


def _assert_page_is_magicube(info):
    """确认当前页面确实是魔搭的页面。返回 True/False。

    🔒 这是**点击前的最后一道闸**：find_target 限定了 host 白名单，
      但页面可能在我们连上之后被导航走了（或者 tab 被复用）。
      ⇒ 点击任何按钮之前，必须重新确认 location.host 在白名单里。

    ⚠ 这是**第二道**防线，不是唯一一道 —— 真正的原子保证在页面里：
      `JS_CLAIM_AND_CLICK` 在**同一次 JS 执行**里先查 location.hostname
      再点按钮，中间不让出事件循环 ⇒ 不存在「校验后页面才被导航走」的窗口。
      这里这层 Python 侧复核是冗余的额外保险。
    """
    url = str(info.get("url") or "")
    if not url:
        return False
    return M._host_matches(url, ALLOWED_HOSTS)


def _page_host(cdp):
    """读当前页面的 hostname（页面里读，比从 URL 解析更贴近真实状态）。

    返回小写 host 字符串；读不到返回 ""。
    """
    try:
        v = cdp.eval("String(location.hostname || '')")
    except Exception:
        return ""
    return str(v or "").strip().lower()


def _host_allowed(host):
    """host 是否落在白名单里（精确相等，或以「.」+ 域名结尾）。

    ⚠ 复用 ms_cdp 的后缀匹配逻辑，保证 Python 侧与页面内 JS 的判据**一致**
      —— 两边规则不一样的话，就会出现「Python 说在白名单、页面说不在」
      这种自相矛盾的行为，审计起来很难查。
    """
    if not host:
        return False
    h = str(host).strip().lower()
    for suf in ALLOWED_HOSTS:
        s = str(suf).lower().lstrip(".")
        if h == s:
            return True
        if h.endswith("." + s):
            return True
    return False


def _open_usage(cdp, wait=7):
    """开魔粒页并连上。返回 True。"""
    t = cdp.find_target("magicube", host_suffixes=ALLOWED_HOSTS)
    if t:
        try:
            if cdp.connect_target(t["id"]):
                return True
        except Exception:
            pass
    t = cdp.new_target(USAGE_URL)
    tid = t.get("id") or t.get("targetId")
    if not cdp.connect_target(tid):
        return False
    time.sleep(wait)
    return True


def _claimed_text(cdp):
    try:
        return str(cdp.eval(JS_CLAIMED_TEXT) or "").strip()
    except Exception:
        return ""


# ==========================================================================
# 主流程
# ==========================================================================
def classify(before, after, clicked, claimed_before, claimed_after,
             labels=None):
    """定性：给定前后余额与文案，返回 (state, delta, detail)。

    🚨 **只有「余额真的增加」才是 CLAIMED**。
      点了按钮、页面文案从无变成「今日已完成」但余额没变 ⇒ **不算成功**：
      那只是延迟到账的*可能*，不是领取成功的证据。未经核实的成功结论
      会让调用方（尤其是定时任务）把「没领到」误当成「领到了」。

    抽成纯函数是为了能脱离浏览器直接测这条判据。
    """
    labels = labels or []

    def _n(v):
        """余额格式化：读不到时显示「?」而不是崩掉。

        ⚠ 余额取不到是**常态**（页面没渲染完 / 网络慢），不是异常路径。
          用 %g 直接格式化 None 会抛 TypeError，把一次「读不到判据」
          变成一次脚本崩溃 —— 所以这里统一走 _n。
        """
        return "?" if v is None else ("%g" % v)

    if before is not None and after is not None and after > before:
        return ("CLAIMED", after - before,
                "领取成功：%g → %g（+%g）" % (before, after, after - before))
    if clicked:
        if claimed_after and claimed_after != claimed_before:
            return ("UNKNOWN", None,
                    "点了「%s」，页面文案已变为「%s」，但余额没变"
                    "（%s → %s）—— 可能延迟到账，未核实，不算领取成功"
                    % ("、".join(labels), claimed_after, _n(before), _n(after)))
        return ("UNKNOWN", None,
                "点了「%s」但余额没变（%s → %s），可能延迟到账，去页面确认一下"
                % ("、".join(labels), _n(before), _n(after)))
    if claimed_before:
        return ("ALREADY", None,
                "页面显示「%s」（余额 %s）" % (claimed_before, _n(before)))
    return ("UNKNOWN", None,
            "没找到「领取」按钮，也没有「今日已领」文案（余额 %s）"
            "—— 可能改版，先 --probe 看页面" % _n(before))


def do_checkin(cdp):
    """打开首页 + 魔粒页 → 点「领取」→ 比对余额。返回结果 dict。

    🚨 判据为什么必须是「点了 + 余额变了」：
        额度要在魔粒页**手动点「领取」**才到账。只判「页面读得到余额」的话，
        那只证明登录成功，不证明领到了 ⇒ 日志天天 OK、魔粒一分不涨。
        只有三种算成功：余额真的增加了 / 页面明确「今日已领」/ 点了按钮但
        余额没变 → 记 UNKNOWN（可能延迟到账），**绝不当成功**。
    """
    result = {"state": "UNKNOWN", "balance": None, "before": None,
              "delta": None, "lines": [], "detail": "", "clicked": 0,
              "labels": []}

    # 1) 先开首页：带登录态访问站点（有些活动的判定挂在首页访问上）
    try:
        t = cdp.new_target(HOME_URL)
        tid = t.get("id") or t.get("targetId")
        if cdp.connect_target(tid):
            time.sleep(4)
        else:
            log("[warn] 首页 connect 失败，继续开魔粒页")
    except Exception as e:
        log("[warn] 开首页失败（不致命）：%s" % e)

    # 2) 开魔粒页
    if not _open_usage(cdp):
        result["detail"] = "connect_target 失败（魔粒页打不开）"
        return result

    try:
        info, lines = _read_page(cdp)
    except Exception as e:
        result["detail"] = "登录判据 eval 失败: %s" % e
        return result

    result["lines"] = lines
    result["before"] = _balance_of(info)

    # 🔒 点击前的页面归属校验：不是魔搭页面就绝不下手点按钮。
    if not _assert_page_is_magicube(info):
        result["state"] = "UNKNOWN"
        result["detail"] = ("当前页面不是魔搭（url=%s），已中止、没点任何按钮"
                            % str(info.get("url"))[:120])
        return result

    # ⚠ 顺序要紧：先判「有登录入口」= 未登录，再判其余。
    #   反过来（先判 URL 含 magicube / 有「我的魔粒」字样）会 100% 误报成功。
    if info.get("loginBtn"):
        result["state"] = "NO_LOGIN"
        result["detail"] = "页面仍有「登录 / 注册」入口，profile 里没有魔搭会话"
        return result
    if result["before"] is None:
        result["detail"] = ("没拿到余额判据 magicube=%s（页面可能没渲染完）"
                            % info.get("magicube"))
        return result

    # 记录点击前的「今日已完成」文案 —— 点击后若文案从无到有，同样算领到了。
    claimed_before = _claimed_text(cdp)

    # 3) 点「领取」。⚠ 一天可能有两个「领取」按钮（登录 200 / 绑阿里云 50），
    #    只点第一个会漏领 ⇒ 循环点，最多 5 轮。
    #
    # 🔒🔒 每轮只发**一次** evaluate（JS_CLAIM_AND_CLICK）：host 校验、找按钮、
    #    点击全在同一个 JS 执行里完成 ⇒ 中间不可能被导航打断。
    #    早先的写法是「Python 侧校验一次 + 每轮先 find 再 click 两次 evaluate」，
    #    校验和点击之间存在窗口，用户中途把标签页导航走就会「离开魔搭还在点」。
    for _ in range(5):
        try:
            click = json.loads(
                cdp.eval(JS_CLAIM_AND_CLICK % (_JS_PRELUDE + _js_host_guard()))
                or "{}")
        except Exception as e:
            log("[warn] 点领取按钮失败: %s" % e)
            break
        if not click.get("clicked"):
            reason = click.get("reason") or ""
            if reason == "host_denied":
                log("[!!] 页面已不是魔搭（host=%s），**停止点击**"
                    % click.get("host"))
                result["detail"] = (
                    "页面在点击前已离开魔搭（host=%s），已停止点击"
                    % (click.get("host") or "?"))
            elif reason == "changed":
                log("[warn] 按钮状态已变（页面变了），停止本轮")
            else:
                log("[..] 没有可点的「领取」按钮了（total=%s）"
                    % click.get("total"))
            break
        result["clicked"] += 1
        result["labels"].append(click.get("label"))
        log("[..] 已点「%s」，等 3 秒看页面变化" % click.get("label"))
        time.sleep(3)

    # 4) 重读余额
    if result["clicked"]:
        time.sleep(3)
        # 🔒 点击期间页面可能已经被导航走（用户切了标签/页面自己跳了路由）。
        #    这时读到的「余额」可能来自非魔搭页面 ⇒ 数字不可信，不许拿它定成功。
        host_now = _page_host(cdp)
        if host_now and not _host_allowed(host_now):
            log("[!!] 点击期间页面已离开魔搭（host=%s），余额判据作废" % host_now)
            result["detail"] = ("点击期间页面已离开魔搭（host=%s），"
                                "余额读数不可信，未核实" % host_now)
            result["balance"] = None
            result["state"] = "UNKNOWN"
            return result
        try:
            after_info, after_lines = _read_page(cdp)
            result["balance"] = _balance_of(after_info)
            if after_lines:
                result["lines"] = after_lines
        except Exception as e:
            log("[warn] 点完重读余额失败: %s" % e)
    if result["balance"] is None:
        result["balance"] = result["before"]

    # 5) 定性
    before, after = result["before"], result["balance"]
    claimed_after = _claimed_text(cdp)
    state, delta, detail = classify(before, after, result["clicked"],
                                     claimed_before, claimed_after,
                                     result["labels"])
    result["state"] = state
    result["delta"] = delta
    result["detail"] = detail
    return result


def do_status(cdp):
    """只读余额 + 登录态，不点任何按钮。"""
    if not _open_usage(cdp):
        return {"state": "UNKNOWN", "balance": None, "before": None,
                "delta": None, "lines": [],
                "detail": "魔粒页打不开"}
    try:
        info, lines = _read_page(cdp)
    except Exception as e:
        return {"state": "UNKNOWN", "balance": None, "before": None,
                "delta": None, "lines": [], "detail": str(e)}
    bal = _balance_of(info)
    if info.get("loginBtn"):
        state = "NO_LOGIN"
    elif bal is not None:
        state = "LOGGED_IN"
    else:
        state = "UNKNOWN"
    return {"state": state, "balance": bal, "before": bal, "delta": None,
            "lines": lines[:10],
            "detail": "登录态：%s；余额 %s" % (
                "未登录" if info.get("loginBtn") else "已登录",
                bal if bal is not None else "读不到")}


def do_probe(cdp):
    """调试：打印页面判据、资源列表、魔粒相关文案。"""
    if not _open_usage(cdp, wait=8):
        log("[probe] 魔粒页打不开")
        return 1
    log("\n=== 登录判据 ===")
    try:
        log(str(cdp.eval(JS_AUTH, refresh_context=True)))
    except Exception as e:
        log("  eval 失败: %s" % e)
    log("\n=== 魔粒相关文案 ===")
    try:
        log(str(cdp.eval(JS_BALANCE))[:1500])
    except Exception as e:
        log("  eval 失败: %s" % e)
    log("\n=== 领取按钮 ===")
    try:
        log(str(cdp.eval(JS_FIND_CLAIM)))
    except Exception as e:
        log("  eval 失败: %s" % e)
    log("\n=== 正文前 800 字 ===")
    try:
        log(str(cdp.eval(JS_TEXT))[:800])
    except Exception as e:
        log("  eval 失败: %s" % e)
    log("\n=== 候选资源 URL ===")
    try:
        log(str(cdp.eval(JS_RESOURCES))[:2000])
    except Exception as e:
        log("  eval 失败: %s" % e)
    return 0


def do_login(cdp, wait_seconds=300):
    """人工登录 + 自动验证。

    ⚠ 交互说明：Chrome 以**有头**模式打开魔粒页，用户在弹出的窗口里登录
      （验证码/短信都在那个窗口里）。本函数定期探一次登录态，
      登录成功（能读到魔粒数字且页面无「登录 / 注册」入口）即退出。

    ⚠ 别在用户正在登录的页面上做导航 —— 那会把人家填到一半的表单冲掉。
      所以只有当 tab 的 URL 不含 passport/login（=不在登录流程里）时才刷新，
      而且刷新有 8 秒间隔，不做高频轮询。
    """
    deadline = time.time() + wait_seconds
    log("[login] 在 Chrome 里登录 modelscope.cn，最多等 %d 秒…" % wait_seconds)
    log("[login] 登录成功后本命令会自动检测并退出，无需手动关窗口。")

    last_url = ""
    last_nav = 0.0
    while time.time() < deadline:
        try:
            t = cdp.find_target("modelscope", host_suffixes=ALLOWED_HOSTS)
            if t and cdp.tid != t["id"]:
                cdp.connect_target(t["id"])
            url = ""
            try:
                url = str(cdp.eval("location.href") or "")
            except Exception:
                pass
            if url and url != last_url:
                last_url = url
                log("  · 当前页面：%s" % url[:120])

            busy = bool(re.search(r"passport|/login|/sign", url or "", re.I))
            if not busy and (time.time() - last_nav) > 8:
                last_nav = time.time()
                try:
                    cdp.send("Page.navigate", {"url": USAGE_URL})
                except Exception:
                    pass
                time.sleep(3)

            info = json.loads(cdp.eval(JS_AUTH, refresh_context=True) or "{}")
            if info.get("loginBtn"):
                time.sleep(3)
                continue
            bal = _balance_of(info)
            if bal is not None:
                log("[✓] 登录成功，当前魔粒余额 %g" % bal)
                return {"state": "LOGGED_IN", "balance": bal,
                        "detail": "登录成功"}
            time.sleep(3)
        except Exception as e:
            log("  [warn] 探测异常：%s" % e)
            time.sleep(3)

    log("[✗] 超时：没检测到登录成功（%d 秒内）。" % wait_seconds)
    log("    请确认浏览器窗口里确实登录成功，或手动跑一次 --probe 看判据。")
    return {"state": "NO_LOGIN", "balance": None, "detail": "等待登录超时"}


# ==========================================================================
# 日志
# ==========================================================================
def append_log(entry):
    """当日只记一条，重复跑覆盖当天记录。"""
    data = {}
    if os.path.exists(LOG_PATH):
        try:
            with open(LOG_PATH, encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {}
    today = time.strftime("%Y-%m-%d")
    data.setdefault("days", {})
    data["days"][today] = entry
    data["updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    tmp = LOG_PATH + ".tmp"
    # 显式 newline=""：Windows 上默认会把 \n 翻成 \r\n，同一份 JSON 换台机器
    # 生成就是另一套行尾，diff 全是噪音。
    with open(tmp, "w", encoding="utf-8", newline="") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, LOG_PATH)


# ==========================================================================
# CLI
# ==========================================================================
def main():
    ap = argparse.ArgumentParser(
        description="魔搭魔粒每日自动领取（CDP 真点页面）")
    ap.add_argument("--login", action="store_true",
                    help="人工登录并自动验证（登录态失效时用）")
    ap.add_argument("--status", action="store_true",
                    help="只查余额与登录态，不点领取")
    ap.add_argument("--probe", action="store_true",
                    help="打印页面判据，不写日志")
    ap.add_argument("--wait", type=int, default=300,
                    help="--login 时等待登录的秒数（默认 300）")
    ap.add_argument("--port", type=int, default=PORT,
                    help="CDP 端口（默认 %d）" % PORT)
    ap.add_argument("--profile", default=PROFILE,
                    help="Chrome profile 目录（默认 %s）" % PROFILE)
    ap.add_argument("--json", action="store_true",
                    help="额外输出一行 JSON 结果")
    args = ap.parse_args()

    # ⚠ Git Bash 起的 python 缺这两个变量 → Chrome 找不到自己的 DLL/目录
    for _k, _v in (("LOCALAPPDATA", r"C:\Users\DELL\AppData\Local"),
                   ("ProgramFiles", r"C:\Program Files")):
        os.environ.setdefault(_k, _v)

    # ✅ 只连接用户自己开着的 Chrome；端口不通时由 ensure_chrome 打印
    #    可直接复制的启动命令，脚本不代为 spawn / 结束浏览器进程。
    proc, launched = M.ensure_chrome(port=args.port,
                                     url=USAGE_URL, profile=args.profile)
    cdp = M.CDP(port=args.port)
    try:
        if args.login:
            res = do_login(cdp, wait_seconds=args.wait)
            append_log({"state": res["state"], "balance": res["balance"],
                        "before": res["balance"], "delta": None,
                        "detail": res["detail"],
                        "at": time.strftime("%H:%M:%S")})
            if args.json:
                log("[json] %s" % json.dumps(res, ensure_ascii=False))
            return 0 if res["state"] == "LOGGED_IN" else 2

        if args.probe:
            return do_probe(cdp)

        res = do_status(cdp) if args.status else do_checkin(cdp)
        state = res["state"]
        entry = {
            "state": state,
            "balance": res.get("balance"),
            "before": res.get("before"),
            "delta": res.get("delta"),
            "detail": res.get("detail", ""),
            "at": time.strftime("%H:%M:%S"),
        }
        for ln in (res.get("lines") or [])[:6]:
            log("    · %s" % ln)

        if state == "CLAIMED":
            log("[✓] 领取成功  %s" % res["detail"])
            append_log(entry)
            log("    已写入 %s" % LOG_PATH)
            rc = 0
        elif state == "ALREADY":
            log("[=] 今天已经领过了：%s" % res["detail"])
            log("    （这不是失败，但也别当成刚领到）")
            append_log(entry)
            rc = 0
        elif state == "LOGGED_IN":
            log("[i] %s" % res["detail"])
            append_log(entry)
            rc = 0
        elif state == "NO_LOGIN":
            log("[✗] NO_LOGIN：该 profile 里没有魔搭登录态。")
            log("    跑一次：python ms_checkin.py --login")
            append_log(entry)
            rc = 2
        else:
            log("[?] UNKNOWN：没拿到判据（没找到领取入口 / 余额没变 / 页面没渲染完）。")
            log("    判据原话：%s" % res.get("detail"))
            log("    用 --probe 看页面到底返回了什么，别直接当失败。")
            append_log(entry)
            rc = 3

        if args.json:
            log("[json] %s" % json.dumps(entry, ensure_ascii=False))
        return rc
    finally:
        # ✅ 只断开 CDP 连接，**不结束任何浏览器进程**。
        #    浏览器窗口归用户所有 —— 脚本无权替他关掉。
        M.stop_chrome(cdp, proc)


if __name__ == "__main__":
    sys.exit(main())
