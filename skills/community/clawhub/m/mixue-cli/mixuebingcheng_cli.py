#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
蜜雪冰城 CLI（供 AI 调用）—— 全链路已对 mxsa.mxbc.net 实测跑通。

签名算法：
    sign = base64url_nopad( RSA_PKCS1_v1_5_SHA256( canonical ) )
    canonical = 把「query 业务参数 + JSON body 全部字段 + appId + t」按 key 排序拼 k=v&...
                嵌套对象/数组按其紧凑 JSON 字符串参与排序
    appId = d82be6bbc1da11eb9dd000163e122ecb ,  t = 13 位毫秒时间戳

链路：
    shops → menu → add(需要商品 modifiedTime) → calc(orderType/takeType/orderChannel)
    → order(生成 orderCode) → paylink(跳小程序收银台，微信里确认付款) / cancel
"""
import argparse
import base64
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

APPID_DEFAULT = 'd82be6bbc1da11eb9dd000163e122ecb'
BASE_DEFAULT = 'https://mxsa.mxbc.net'
VERSION = '1.11.1'
ROOT = os.path.dirname(os.path.abspath(__file__))

ENV_TEMPLATE = """# 蜜雪冰城 CLI 配置 —— chmod 600，含登录态，切勿外传/提交
# 取值方式见 README：抓一次小程序 HAR，然后 `mixue har 抓包.har`
MIXUE_TOKEN=
MIXUE_OPENID=
MIXUE_CUSTOMER_ID=
MIXUE_SHOP=
MIXUE_BASE=https://mxsa.mxbc.net
MIXUE_APPID=d82be6bbc1da11eb9dd000163e122ecb
MIXUE_MP_APPID=wx7696c66d2245d107
MIXUE_KEY_PATH=./tools/mxbc_key.pem
"""


def _load_env():
    """按优先级读 .env：$MIXUE_ENV → $ROOT/.env → ~/.config/mixue/.env

    已存在的真实环境变量优先（setdefault），所以 export 的值总能盖住文件。
    """
    cands = [os.environ.get('MIXUE_ENV'), os.path.join(ROOT, '.env'),
             os.path.expanduser('~/.config/mixue/.env')]
    for path in cands:
        if not path or not os.path.exists(path):
            continue
        try:
            with open(path, encoding='utf-8') as f:
                for raw in f:
                    line = raw.strip()
                    if not line or line.startswith('#') or '=' not in line:
                        continue
                    k, v = line.split('=', 1)
                    v = v.strip()
                    if len(v) >= 2 and v[0] == v[-1] and v[0] in '"\'':
                        v = v[1:-1]
                    os.environ.setdefault(k.strip(), v)
        except OSError:
            continue
        return path
    return None


ENV_FILE = _load_env()


def _env(name, default=''):
    return (os.environ.get(name) or default).strip()


APPID = _env('MIXUE_APPID', APPID_DEFAULT)
BASE = _env('MIXUE_BASE', BASE_DEFAULT)
KEY_PATH = _env('MIXUE_KEY_PATH', os.path.join(ROOT, 'tools', 'mxbc_key.pem'))
if KEY_PATH and not os.path.isabs(KEY_PATH):
    KEY_PATH = os.path.join(ROOT, KEY_PATH)
TOKEN_PATH = _env('MIXUE_TOKEN_PATH', os.path.join(ROOT, 'tools', 'token.txt'))
OPENID_PATH = _env('MIXUE_OPENID_PATH', os.path.join(ROOT, 'tools', 'openid.txt'))
CUSTOMER_PATH = _env('MIXUE_CUSTOMER_PATH', os.path.join(ROOT, 'tools', 'customer_id.txt'))
DEFAULT_SHOP = _env('MIXUE_SHOP', '')
# ── 支付策略：默认只允许礼品卡，其他通道标记为暂不可用且不主动调用 ──
PAYMENT_POLICY = 'giftcard-only'
ALLOW_NON_GIFTCARD_PAY = False   # 已彻底移除解锁通道；如需放行必须改代码并评审

TOKEN_OVERRIDE = None      # 由命令行 --token 临时覆盖
OPENID_OVERRIDE = None     # 由命令行 --openid 临时覆盖

# 实测有效枚举（order/save、calcprice、prepay 校验通过）
DEFAULT_ORDER = dict(orderType=1, takeType=1, orderChannel=3)

# 蜜雪冰城小程序（H5 redirect 页里写死）与小程序收银台页（APK 字符串）
MP_APPID = 'wx7696c66d2245d107'
MP_PAY_PATH = 'pages/order_detail/pay/index'

_priv = None


def priv():
    global _priv
    if _priv is None:
        from cryptography.hazmat.primitives import serialization
        inline = _env('MIXUE_PRIVATE_KEY')
        if inline:
            pem = inline.replace('\\n', '\n').encode()
        else:
            if not os.path.exists(KEY_PATH):
                die({'error': '缺少签名私钥',
                     'looked_at': KEY_PATH,
                     'fix': ['把你的私钥文件路径写进 MIXUE_KEY_PATH',
                             '或把 PEM 内容写进 MIXUE_PRIVATE_KEY（\\n 转义）',
                             '跑 `mixuebingcheng-cli key` 看当前状态']})
            with open(KEY_PATH, 'rb') as f:
                pem = f.read()
        try:
            _priv = serialization.load_pem_private_key(pem, password=None)
        except Exception as e:
            die({'error': '私钥无法解析（需 RSA PEM，未加密）', 'reason': str(e)[:120]})
    return _priv


def sign_content(content):
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    sig = priv().sign(content.encode(), padding.PKCS1v15(), hashes.SHA256())
    return base64.urlsafe_b64encode(sig).decode().rstrip('=')


def _flat(v):
    if isinstance(v, (dict, list)):
        return json.dumps(v, ensure_ascii=False, separators=(',', ':'))
    return v


def canonical(params, ts, appid=APPID):
    merged = dict(params or {})
    merged['appId'] = appid
    merged['t'] = ts
    return '&'.join('%s=%s' % (k, _flat(merged[k])) for k in sorted(merged))


def signed_query(params, appid=APPID):
    ts = int(time.time() * 1000)
    q = dict(params or {})
    q.update({'t': ts, 'appId': appid, 'sign': sign_content(canonical(params, ts, appid))})
    return q


def load_token(explicit=None):
    if explicit:
        return explicit
    if TOKEN_OVERRIDE:
        return TOKEN_OVERRIDE
    env = os.environ.get('MIXUE_TOKEN')
    if env:
        return env
    if os.path.exists(TOKEN_PATH):
        return open(TOKEN_PATH).read().strip()
    return None


ALLOWED_HOSTS = {'mxsa.mxbc.net'}   # 无任何运行时开关可以扩展这道白名单


def _assert_target(url):
    """只允许 https + 白名单域名，防止配置错误把 token 发到别的服务器。"""
    u = urllib.parse.urlparse(url)
    if u.scheme != 'https':
        die({'ok': False, 'error': '拒绝非 HTTPS 请求',
             'scheme': u.scheme, 'path': u.path, 'note': '未发起任何网络请求'})
    port = u.port if u.port is not None else (443 if u.scheme == 'https' else 80)
    if port != 443:
        die({'ok': False, 'error': '拒绝非标准端口（只允许 443）',
             'host': u.hostname, 'port': port,
             'note': '未发起任何网络请求'})
    if u.hostname not in ALLOWED_HOSTS:
        die({'ok': False, 'error': '目标域名不在白名单，已拒绝（防止 token 外发）',
             'host': u.hostname, 'allowed': sorted(ALLOWED_HOSTS),
             'hint': '本版本不提供任何指向其他主机的开关',
             'note': '未发起任何网络请求'})


class _SameHostRedirect(urllib.request.HTTPRedirectHandler):
    """只允许同域 + 同 scheme(https) 的重定向。

    任何降级到 http、或换域名的跳转都直接中断 —— 否则认证头可能被带走。
    """

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        old = urllib.parse.urlparse(req.full_url)
        new = urllib.parse.urlparse(newurl)
        if new.scheme.lower() != 'https':
            raise urllib.error.HTTPError(newurl, code,
                                          'blocked non-https redirect', headers, fp)
        if new.scheme != old.scheme or new.netloc != old.netloc:
            raise urllib.error.HTTPError(newurl, code,
                                          'blocked cross-host redirect', headers, fp)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


_OPENER = urllib.request.build_opener(_SameHostRedirect)


def _build_url(path, params, sign_params, ts):
    """URL 只放 query 参数 + appId/t/sign；body 字段不写进 URL（防日志泄露）。

    签名仍按「query + body」合并计算，与服务端一致。
    """
    q = dict(params)
    q.update({'t': ts, 'appId': APPID,
              'sign': sign_content(canonical(sign_params, ts, APPID))})
    return BASE + path + '?' + urllib.parse.urlencode(q)


def request(method, path, params=None, token=None, body=None, raw_body=None):
    """params 进 URL 并参与签名；body 只放请求体，但同样参与签名。

    ⚠️ 不要把 body 字段再拼进 URL：手机号/验证码/卡号会落到服务端与代理的访问日志里。
    不做任何形式的“失败后把 body 塞回 URL”的回退。
    """
    params = dict(params or {})
    sign_params = dict(params)
    if isinstance(body, dict):
        sign_params.update(body)
    ts = int(time.time() * 1000)
    url = _build_url(path, params, sign_params, ts)
    headers = {
        'Host': 'mxsa.mxbc.net',
        'Accept': 'application/json',
        'User-Agent': 'okhttp/4.9.0',
        'Content-Type': 'application/json;charset=utf-8',
    }
    tok = load_token(token)
    if tok:
        headers['Access-Token'] = tok
    data = raw_body
    if data is None and body is not None:
        data = json.dumps(body, ensure_ascii=False).encode()
    if data is None and method == 'POST':
        data = b''
    req = urllib.request.Request(url, data=data, method=method)
    for k, v in headers.items():
        req.add_header(k, v)
    _assert_target(url)
    status = None
    try:
        with _OPENER.open(req, timeout=25) as r:
            status = r.status
            txt = r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        status = e.code
        try:
            txt = e.read().decode('utf-8', 'replace')
        except Exception:
            txt = ''
        # HTTP 层错误必须原样上报，不能因为 body 为空就说成功
        if not txt.strip():
            return {'ok': False, 'http_status': status,
                    'error': 'HTTP %s：响应体为空' % status,
                    'path': path}
        try:
            parsed = json.loads(txt)
        except Exception:
            return {'ok': False, 'http_status': status, 'error': 'HTTP %s' % status, 'raw': txt[:500]}
        if isinstance(parsed, dict):
            parsed.setdefault('http_status', status)
        return parsed
    except Exception as e:                       # 网络/重定向拦截等
        return {'ok': False, 'http_status': status, 'error': '%s: %s' % (type(e).__name__, str(e)[:200])}

    if not txt.strip():
        return {'ok': True, 'http_status': status, 'note': 'empty response (HTTP %s)' % status}
    try:
        return json.loads(txt)
    except Exception:
        return {'ok': False, 'http_status': status, 'error': '响应不是 JSON', 'raw': txt[:500]}


# ------------------------- 输出脱敏 -------------------------
# 默认对所有输出做脱敏（token / openId / customerId / 手机号 / 礼品卡号），
# 需要看原值时加全局参数 --no-redact（仅限自查，别贴到聊天或日志里）。

REDACT_EXACT = {
    # 值整体隐藏，只留前 3 位
    'token': 2, 'accesstoken': 2, 'refreshtoken': 2, 'authorization': 2,
    'sign': 2, 'password': 2, 'secret': 2, 'paysign': 2,
    'packagestr': 2, 'orderstr': 2, 'prepayid': 2, 'idcard': 2,
    # 保留前后各 4 位
    'openid': 1, 'customerid': 1, 'mobile': 1, 'mobilephone': 1, 'phone': 1,
    'cardno': 1, 'cardnumber': 1, 'email': 1,
}

# 字段名只要是这些后缀就脱敏（覆盖 receiverPhone / contactMobile / userToken 等未登记字段）
REDACT_SUFFIX = [
    ('mobilephone', 1), ('receiverphone', 1), ('contactphone', 1), ('phone', 1),
    ('mobile', 1), ('telephone', 1), ('openid', 1), ('cardno', 1), ('cardnumber', 1),
    ('idcard', 2), ('email', 1), ('token', 2), ('secret', 2), ('paysign', 2),
    ('packagestr', 2), ('orderstr', 2), ('prepayid', 2), ('password', 2),
]

PHONE_RE = re.compile(r'(?<!\d)(1[3-9]\d{9})(?!\d)')   # 中国大陆手机号
RAW_OUTPUT = False


def _mask(v, keep=0):
    s = str(v)
    if len(s) <= 4:
        return '***'
    if keep == 2:
        return s[:3] + '***'
    return s[:4] + '*' * max(4, len(s) - 8) + s[-4:]


def _rule_for(key):
    kl = str(key).lower().replace('-', '').replace('_', '')
    if kl in REDACT_EXACT:
        return REDACT_EXACT[kl]
    for suf, rule in REDACT_SUFFIX:
        if kl.endswith(suf):
            return rule
    return None


def _scrub_str(v):
    """字符串里的手机号也要遮（订单号/商品 ID 不动，避免影响使用）。"""
    return PHONE_RE.sub(lambda m: m.group(1)[:3] + '****' + m.group(1)[-4:], v)


def redact(obj):
    if isinstance(obj, dict):
        res = {}
        for k, v in obj.items():
            rule = _rule_for(k)
            if rule and isinstance(v, (str, int)) and not isinstance(v, bool):
                res[k] = _mask(v, rule)
            else:
                res[k] = redact(v)
        return res
    if isinstance(obj, list):
        return [redact(v) for v in obj]
    if isinstance(obj, str):
        if obj.startswith('eyJ') and obj.count('.') == 2 and len(obj) > 60:
            return _mask(obj, 2)
        return _scrub_str(obj)
    return obj


def out(x):
    if not RAW_OUTPUT:
        x = redact(x)
    print(json.dumps(x, ensure_ascii=False, indent=2))


def die(msg):
    payload = {'ok': False, 'error': msg}
    if not RAW_OUTPUT:
        payload = redact(payload)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    sys.exit(1)


# ------------------------- helpers -------------------------

def fetch_menu(shop):
    r = request('POST', '/api/v3/shop/menu/info', body={'shopId': shop})
    if not isinstance(r, dict) or r.get('code') != 0:
        die(r)
    return r['data']


def find_product(menu, ident):
    for cat in menu:
        for p in (cat.get('products') or []):
            if ident in (p.get('productId'), p.get('productName')):
                return p
            if isinstance(ident, str) and ident and ident in (p.get('productName') or ''):
                return p
    return None


def scene_params(a):
    return {'orderType': a.order_type, 'takeType': a.take_type, 'orderChannel': a.order_channel}


def load_openid():
    """小程序 openId（prepay 必填）。--openid > env MIXUE_OPENID > tools/openid.txt。"""
    if OPENID_OVERRIDE:
        return OPENID_OVERRIDE
    oid = _env('MIXUE_OPENID')
    if oid:
        return oid
    try:
        with open(OPENID_PATH) as f:
            return f.read().strip()
    except Exception:
        return ''


def fetch_giftcards(shop, order_type=1):
    """可用礼品卡列表：[{cardNo, cardBalance, templateName, expDate}]。"""
    r = request('POST', '/api/v1/giftcard/available/list',
                body={'shopId': shop, 'orderType': order_type})
    if isinstance(r, dict) and r.get('code') == 0:
        return r.get('data') or []
    return []


def pay_with_giftcard(order_code, shop=None, order_type=1, cards=None):
    """用礼品卡结账：prepay → isZeroPay=1 即已付清。

    cards 为 [{'cardNo':...}]；不传则自动取可用卡里余额最高的那张。
    返回 (ok, info_dict)
    """
    openid = load_openid()
    if not openid:
        return False, {'error': '缺少 openId：把小程序抓包里的 openId 写到 tools/openid.txt，或传 --openid'}
    if cards is None:
        cards = fetch_giftcards(shop, order_type) if shop else []
        cards = [max(cards, key=lambda c: c.get('cardBalance') or 0)] if cards else []
    if not cards:
        return False, {'error': '没有可用礼品卡'}
    r = request('POST', '/api/v2/order/prepay',
                body={'miniAppId': MP_APPID, 'orderCode': order_code,
                      'payType': 1, 'openId': openid})
    if not (isinstance(r, dict) and r.get('code') == 0):
        return False, {'prepay': r}
    d = r.get('data') or {}
    return bool(d.get('isZeroPay')), {'prepay': d, 'isZeroPay': d.get('isZeroPay'),
                                      'cards': [c.get('cardNo') if isinstance(c, dict) else c for c in cards]}


def _pick_giftcards(spec, shop, order_type=1):
    """--giftcard auto | <cardNo> [,cardNo2] → [{'cardNo':...}]"""
    if not spec:
        return None
    avail = fetch_giftcards(shop, order_type)
    if not avail:
        die('没有可用礼品卡（或接口失败）')
    if spec.strip().lower() == 'auto':
        best = max(avail, key=lambda c: c.get('cardBalance') or 0)
        return [{'cardNo': best['cardNo']}]
    wanted = [s.strip() for s in spec.split(',') if s.strip()]
    have = {c['cardNo'] for c in avail}
    miss = [w for w in wanted if w not in have]
    if miss:
        die({'error': '礼品卡不可用', 'not_available': miss,
             'available': [{'cardNo': c['cardNo'], 'balance': c.get('cardBalance')} for c in avail]})
    return [{'cardNo': w} for w in wanted]


def _save_payload(shop, calc_data, order_type, take_type, gift_cards=None):
    """从 settlement 结果拼出 order/save 的 body（含自动选中的优惠券字段）。

    真实账号结算时会自动套券（如 88 折券），若 save 不带这些券字段，
    服务端按「下单价 != 算价」拒绝，返回 8003「优惠价格变更」。

    gift_cards: [{'cardNo': '...'}] —— 蜜雪礼品卡在建单时就带上，
    金额足够时 prepay 返回 isZeroPay=1，订单直接变已支付（不需要微信）。
    """
    d = calc_data or {}
    body = dict(shopId=shop, orderType=order_type, takeType=take_type,
                orderChannel=2, miniProgType=1, useWalletPay=0)
    if gift_cards:
        body['selectedGiftCardList'] = [{'cardNo': c['cardNo']} if isinstance(c, dict) else {'cardNo': str(c)}
                                        for c in gift_cards]
    if d.get('cartId'):
        body['cartId'] = d['cartId']
    for k in ('couponId', 'couponCode', 'couponRuleId', 'couponType',
              'couponChannelSource', 'selectedCouponCategory', 'couponTag'):
        if d.get(k) is not None:
            body[k] = d[k]
    return body


# ------------------------- commands -------------------------

def cmd_ping(a):
    out(request('GET', '/api/v1/app/getTimestamp'))


def cmd_config(a):
    out(request('GET', '/api/v1/app/config'))


def _save_env_var(key, value):
    """把 key=value 写进 .env（存在则替换该行，不存在则追加），0600。"""
    target = ENV_FILE or os.path.join(ROOT, '.env')
    lines, found = [], False
    if os.path.exists(target):
        with open(target, encoding='utf-8') as f:
            for line in f:
                if line.strip().startswith(key + '='):
                    lines.append('%s=%s\n' % (key, value))
                    found = True
                else:
                    lines.append(line)
    if not found:
        if lines and not lines[-1].endswith('\n'):
            lines.append('\n')
        lines.append('%s=%s\n' % (key, value))
    with open(target, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    os.chmod(target, 0o600)
    os.environ[key] = value
    return target


def save_token(tok):
    """写 token：有 .env 就更新其中的 MIXUE_TOKEN 行，否则写 tools/token.txt。"""
    if ENV_FILE and os.path.exists(ENV_FILE):
        return _save_env_var('MIXUE_TOKEN', tok)
    d = os.path.dirname(TOKEN_PATH)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(TOKEN_PATH, 'w') as f:
        f.write(tok)
    os.chmod(TOKEN_PATH, 0o600)
    os.environ['MIXUE_TOKEN'] = tok
    return TOKEN_PATH


CAPTURE_HOST = 'mxsa.mxbc.net'

CAPTURE_GUIDE = {
    'hosts': {
        'mxsa.mxbc.net': '蜜雪小程序业务接口（唯一必须抓的域名，凭据全在这里）',
        'mxsa-oss.mxbc.net': '图片 CDN，不需要抓（体积大、无凭据）',
    },
    'proxy_filter': 'mxsa.mxbc.net',
    'mini_program_appid': 'wx7696c66d2245d107',
    'how_to_trigger': [
        '1. 手机微信打开小程序「蜜雪冰城」，确认已登录',
        '2. 允许定位 → 进入任意一家门店（触发 shopinfo/findNear 或 findRecommend）',
        '3. 把一个商品加进购物车（触发 shoppingCart/addProduct、calcprice）',
        '4. 点「去结算」（触发 shoppingCart/settlement/update，这里会带 customerId）',
        '5. 走到收银台但不付款（触发 order/prepay，这里会带 openId）',
        '6. 回抓包工具导出 .har',
    ],
    'fields': [
        {'env': 'MIXUE_TOKEN', 'where': '请求头 Access-Token',
         'seen_on': '几乎所有 /api/* 请求（GET 也有）', 'required': True,
         'note': 'JWT，形如 eyJ...，长度约 195'},
        {'env': 'MIXUE_OPENID', 'where': 'POST /api/v2/order/prepay 的请求体 openId',
         'seen_on': '只有走到收银台/支付才会出现', 'required': '支付与礼品卡必填',
         'note': 'wx 开头 28 位；不付款也能拿到，prepay 请求发出即可'},
        {'env': 'MIXUE_CUSTOMER_ID', 'where': '请求体 customerId（或响应里的 customerId）',
         'seen_on': '/api/v1/customer/info、settlement/update', 'required': '建议',
         'note': '纯数字'},
        {'env': 'MIXUE_SHOP', 'where': '响应里的 shopId',
         'seen_on': '/api/v2/shopinfo/findNear', 'required': '可选',
         'note': '填了就不用每次 --shop'},
    ],
    'endpoints': {
        'GET  /api/v1/customer/info': '账号信息，可验证 token 是否有效',
        'POST /api/v2/shopinfo/findNear': '附近门店，拿 shopId',
        'POST /api/v3/shop/menu/info': '门店菜单，拿 productId',
        'POST /api/v3/shoppingCart/addProduct': '加购（productId + modifiedTime）',
        'POST /api/v3/shoppingCart/calcprice': '算价',
        'POST /api/v3/shoppingCart/settlement/update': '结算（带 customerId；礼品卡在此抵扣）',
        'POST /api/v2/order/save': '建单，返回 orderCode',
        'POST /api/v2/order/prepay': '聚合支付（带 openId；isZeroPay=1 表示礼品卡已付清）',
        'GET  /api/v2/order/cust/info/{orderCode}': '订单详情，取餐号 takeNo',
    },
    'har_alternatives': '拿不到 HAR 时：Reqable/Charles 的「复制 cURL」也行，'
                        'Access-Token 在 -H 参数里，openId 在 --data 的 JSON 里',
}


def cmd_key(a):
    """查看/设置签名私钥。"""
    if getattr(a, 'set', None):
        path = os.path.expanduser(a.set)
        if not os.path.exists(path):
            die('文件不存在: %s' % path)
        pem = open(path, 'rb').read()
        try:
            from cryptography.hazmat.primitives import serialization
            serialization.load_pem_private_key(pem, password=None)
        except Exception as e:
            die({'error': '不是有效的 RSA PEM 私钥', 'reason': str(e)[:120]})
        written = _save_env_var('MIXUE_KEY_PATH', os.path.abspath(path))
        out({'ok': True, 'key_path': os.path.abspath(path), 'written_to': written})
        return
    inline = _env('MIXUE_PRIVATE_KEY')
    exists = os.path.exists(KEY_PATH)
    status = 'inline' if inline else ('file' if exists else 'missing')
    res = {'key_status': status, 'key_path': KEY_PATH, 'inline_set': bool(inline),
           'note': '签名私钥状态见上；可用 key --set <pem> 指定或替换'}
    if status == 'missing':
        res['how_to'] = ['mixuebingcheng-cli key --set /path/to/mxbc_key.pem',
                         '或把 PEM 内容写进 .env：MIXUE_PRIVATE_KEY="-----B...\\n..."']
    out(res)


def cmd_needs(a):
    """打印「要抓什么」的完整说明：域名、过滤表达式、要触发的操作、字段在哪。"""
    out({'version': VERSION, 'capture_host': CAPTURE_HOST,
         'proxy_filter': CAPTURE_GUIDE['proxy_filter'],
         'mini_program_appid': CAPTURE_GUIDE['mini_program_appid'],
         'hosts': CAPTURE_GUIDE['hosts'],
         'steps': CAPTURE_GUIDE['how_to_trigger'],
         'fields': CAPTURE_GUIDE['fields'],
         'endpoints': CAPTURE_GUIDE['endpoints'],
         'alternatives': CAPTURE_GUIDE['har_alternatives'],
         'then': 'mixue har 你的文件.har   →   mixue whoami'})


def cmd_har(a):
    """从浏览器/Reqable 导出的 .har 里提取登录凭据，写入 .env。

    只认 mxsa.mxbc.net 的请求：Access-Token 头、请求体里的 openId / customerId。
    不保存 HAR 原文，也不打印完整凭据。
    """
    path = os.path.expanduser(a.path)
    if not os.path.exists(path):
        die('文件不存在: %s' % path)
    try:
        with open(path, encoding='utf-8', errors='replace') as f:
            data = json.load(f)
        entries = data['log']['entries']
    except Exception as e:
        die('解析 HAR 失败（不是合法 HAR？）: %s' % e)

    tokens, openids, cids = {}, {}, {}      # 值 → 首次出现的接口路径
    hosts, matched = {}, 0
    for e in entries:
        req = e.get('request') or {}
        url = req.get('url') or ''
        try:
            u = urllib.parse.urlparse(url)
        except Exception:
            continue
        host = (u.hostname or '').lower()
        hosts[host] = hosts.get(host, 0) + 1
        # 严格相等，避免 mxsa.mxbc.net.attacker.example 之类混入；且必须 https
        if host != CAPTURE_HOST or u.scheme != 'https':
            continue
        matched += 1
        endpoint = '%s %s' % (req.get('method') or 'GET', u.path)
        for h in (req.get('headers') or []):
            if (h.get('name') or '').lower().replace('-', '') == 'accesstoken':
                v = (h.get('value') or '').strip()
                if v:
                    tokens.setdefault(v, endpoint)
        text = ((req.get('postData') or {}).get('text') or '')
        if text:
            try:
                b = json.loads(text)
            except Exception:
                continue
            if isinstance(b, dict):
                if b.get('openId'):
                    openids.setdefault(str(b['openId']), endpoint)
                if b.get('customerId'):
                    cids.setdefault(str(b['customerId']), endpoint)

    if matched == 0:
        die({'error': 'HAR 里没有 %s 的请求' % CAPTURE_HOST,
             'hosts_seen': dict(sorted(hosts.items(), key=lambda kv: -kv[1])[:8]),
             'fix': ['抓包时把过滤条件设成 %s' % CAPTURE_GUIDE['proxy_filter'],
                     '确认抓的是微信小程序「蜜雪冰城」，不是 App/网页版',
                     '跑 `mixue needs` 看完整采集要求']})
    if not tokens:
        die({'error': 'HAR 里有 %s 的请求，但没有 Access-Token 头' % CAPTURE_HOST,
             'matched_entries': matched,
             'fix': ['多半是没登录：小程序里重新登录后再抓',
                     '或抓的时间太短，只抓到了 app/config 这类免登录接口']})

    tok = sorted(tokens, key=len, reverse=True)[0]
    written = {'MIXUE_TOKEN': save_token(tok)}
    oid = sorted(openids)[0] if openids else ''
    cid = sorted(cids)[0] if cids else ''
    if oid:
        written['MIXUE_OPENID'] = _save_env_var('MIXUE_OPENID', oid)
    if cid:
        written['MIXUE_CUSTOMER_ID'] = _save_env_var('MIXUE_CUSTOMER_ID', cid)

    openid_from = openids.get(oid, '')
    result = {
        'ok': True, 'har': path, 'entries': len(entries),
        'capture': {'host': CAPTURE_HOST, 'matched_entries': matched,
                    'top_hosts': dict(sorted(hosts.items(), key=lambda kv: -kv[1])[:5])},
        'found': {'tokens': len(tokens), 'openid': bool(oid), 'customer_id': bool(cid)},
        'sources': {'MIXUE_TOKEN': tokens.get(tok, ''),
                    'MIXUE_OPENID': openid_from or '(未找到)',
                    'MIXUE_CUSTOMER_ID': cids.get(cid, '') or '(未找到)'},
        'written_to': written,
        'token_preview': tok[:12] + '…' + tok[-6:],
    }
    if not oid:
        result['warn_openid'] = ('没抓到 openId：支付和礼品卡会失败。'
                                 '要走到收银台（prepay 请求）才会出现，见 `mixue needs`')
    result['next'] = 'mixue whoami'
    out(result)


def cmd_init(a):
    """首次配置：没有 .env 就按模板生成，并打印需要填的项。"""
    target = ENV_FILE or os.path.join(ROOT, '.env')
    created = False
    if not os.path.exists(target):
        with open(target, 'w', encoding='utf-8') as f:
            f.write(ENV_TEMPLATE)
        os.chmod(target, 0o600)
        created = True
    missing = [k for k, need in (('MIXUE_TOKEN', True), ('MIXUE_OPENID', True))
               if need and not _env(k)]
    out({'ok': True, 'env_file': target, 'created': created,
         'missing': missing,
         'how_to_get_credentials': [
             '1. 手机登录微信小程序「蜜雪冰城」',
             '2. 用 Reqable / Charles / mitmproxy 抓包（只抓自己的流量）',
             '3. 导出 .har，跑 `mixue har <文件.har>`（自动提取 token/openId/customerId）',
             '或手工把 Access-Token 头填进 MIXUE_TOKEN 行',
         ],
         'next': 'mixue whoami  →  mixue shops --lat <纬度> --lng <经度>' if not missing
                 else '先补齐 %s' % ', '.join(missing)})


def cmd_env(a):
    """显示当前配置来源（不打印任何密钥明文）。"""
    def mask(v, keep=6):
        return (v[:keep] + '…' + v[-4:]) if v and len(v) > keep + 6 else ('(已设置)' if v else '')
    tok = load_token()
    out({'env_file': ENV_FILE or '(未找到 .env，走 os.environ + 旧文件)',
         'base': BASE, 'appid': APPID, 'mp_appid': MP_APPID,
         'shop': DEFAULT_SHOP or '(未设置)',
         'token_source': ('--token' if TOKEN_OVERRIDE else
                          'env MIXUE_TOKEN' if os.environ.get('MIXUE_TOKEN') else
                          ('file ' + TOKEN_PATH) if os.path.exists(TOKEN_PATH) else '缺失'),
         'token': mask(tok or ''),
         'openid_source': ('--openid' if OPENID_OVERRIDE else
                           'env MIXUE_OPENID' if os.environ.get('MIXUE_OPENID') else
                           ('file ' + OPENID_PATH) if os.path.exists(OPENID_PATH) else '缺失'),
         'customer_id': load_customer_id() or '(未设置)',
         'key': ('env MIXUE_PRIVATE_KEY（内联）' if os.environ.get('MIXUE_PRIVATE_KEY')
                 else ('file ' + KEY_PATH) if os.path.exists(KEY_PATH) else '缺失')})


def cmd_login(a):
    # 手机号/验证码必须走 body：放进 params 会被写进 URL，落到访问日志
    r = request('POST', '/api/v1/app/login', body={'mobilePhone': a.phone, 'captcha': a.code})
    data = (r or {}).get('data') or {}
    tok = data.get('accessToken')
    if tok:
        print('token saved to', save_token(tok))
    out(r)


def cmd_sms(a):
    out(request('POST', '/api/v1/app/captchaSms', body={'mobilePhone': a.phone}))


def cmd_whoami(a):
    out(request('GET', '/api/v1/customer/info'))


def cmd_token(a):
    if a.set_token:
        print('token saved to', save_token(a.set_token.strip()))
        out(request('GET', '/api/v1/customer/info'))
        return
    if getattr(a, 'stdin', False):
        tok_new = sys.stdin.read().strip()
        if not tok_new:
            die('stdin 里没有内容')
        print('token saved to', save_token(tok_new))
        out(request('GET', '/api/v1/customer/info'))
        return
    tok = load_token()
    if not tok:
        die('未设置 token：`mixuebingcheng-cli token --stdin`（粘贴后 Ctrl-D）或写进 .env 的 MIXUE_TOKEN')
    try:
        payload = tok.split('.')[1]
        payload += '=' * (-len(payload) % 4)
        claims = json.loads(base64.urlsafe_b64decode(payload).decode())
    except Exception:
        claims = {}
    # claims 内嵌的 customerId（如 sub=wxmini_123...）也要遮掉
    def _scrub(v):
        if isinstance(v, str):
            return re.sub(r'\d{10,}', lambda m: m.group(0)[:4] + '*' * max(4, len(m.group(0)) - 8) + m.group(0)[-4:], v)
        if isinstance(v, dict):
            return {k: _scrub(x) for k, x in v.items()}
        if isinstance(v, list):
            return [_scrub(x) for x in v]
        return v
    out({'token_set': True, 'token_len': len(tok), 'claims': _scrub(claims),
         'source': ('env MIXUE_TOKEN' if os.environ.get('MIXUE_TOKEN')
                    else TOKEN_PATH),
         'hint': '要看完整 token 加 --no-redact（仅限自查，别外传）'})


def cmd_shops(a):
    r = request('POST', '/api/v2/shopinfo/findNear', body={'latitude': a.lat, 'longitude': a.lng})
    if getattr(a, 'table', False) and isinstance(r, dict) and r.get('code') == 0:
        for s in (r.get('data') or []):
            print('%-22s %-24s %s' % (s.get('shopId'), s.get('shopName'), s.get('shopAddress')))
        return
    out(r)


def cmd_menu(a):
    menu = fetch_menu(a.shop)
    if getattr(a, 'table', False):
        for cat in menu:
            print('## ' + str(cat.get('categoryNameSale')))
            for p in (cat.get('products') or []):
                print('  %-22s %-28s %5.2f元' % (
                    p.get('productId'), p.get('productName'), (p.get('productPrice') or 0) / 100.0))
        return
    out(menu)


def cmd_cart_add(a):
    menu = fetch_menu(a.shop)
    p = find_product(menu, a.product)
    if not p:
        die('商品不存在: %s' % a.product)
    body = {'shopId': a.shop, 'productId': p['productId'],
            'productAmount': int(a.num), 'modifiedTime': p.get('modifiedTime')}
    out(request('POST', '/api/v3/shoppingCart/addProduct', body=body))


def cmd_calc(a):
    body = {'shopId': a.shop}
    body.update(scene_params(a))
    r = request('POST', '/api/v3/shoppingCart/calcprice', body=body)
    if isinstance(r, dict) and r.get('code') == 0:
        d = r['data']
        d['_summary'] = {'总价(元)': (d.get('total') or 0) / 100.0,
                         '数量': d.get('productAmount'),
                         '原价(元)': (d.get('originPrice') or 0) / 100.0}
    out(r)


def cmd_clear(a):
    body = {'shopId': a.shop}
    body.update(scene_params(a))
    out(request('POST', '/api/v3/shoppingCart/clearCart', body=body))


def cmd_giftcards(a):
    """列可用礼品卡。"""
    cards = fetch_giftcards(a.shop)
    out({'shop': a.shop, 'count': len(cards),
         'cards': [{'cardNo': c.get('cardNo'), 'balance_yuan': (c.get('cardBalance') or 0) / 100.0,
                    'face_yuan': (c.get('faceAmount') or 0) / 100.0,
                    'template': c.get('templateName'), 'expDate': c.get('expDate')} for c in cards],
         'openid_present': bool(load_openid())})


CUSTOMER_PATH_LEGACY = CUSTOMER_PATH


def load_customer_id():
    """customerId（settlement/update 里要带）。env → 缓存文件 → 接口。"""
    cid = _env('MIXUE_CUSTOMER_ID')
    if cid:
        return cid
    try:
        with open(CUSTOMER_PATH) as f:
            cid = f.read().strip()
            if cid:
                return cid
    except Exception:
        pass
    try:
        r = request('GET', '/api/v1/customer/info')
        d = (r or {}).get('data') or {}
        cid = str(d.get('customerId') or d.get('id') or '')
        if cid:
            with open(CUSTOMER_PATH, 'w') as f:
                f.write(cid)
            os.chmod(CUSTOMER_PATH, 0o600)
            return cid
    except Exception:
        pass
    return ''


def settlement(shop, prods, order_type=1, take_type=1, cards=None, trans_token=None):
    """POST /api/v3/shoppingCart/settlement/update

    这是礼品卡抵扣真正生效的地方：带上 selectedGiftCardList 后，
    返回的 price 才是「卡抵完还要付多少」（total 仍是原价）。
    """
    body = {'shopId': shop, 'orderType': str(order_type), 'takeType': take_type,
            'products': prods, 'plusDiscountProductList': [], 'useWalletPay': 0}
    cid = load_customer_id()
    if cid:
        body['customerId'] = cid
    if trans_token:
        body['transToken'] = trans_token
    if cards:
        body['selectedGiftCardList'] = [{'cardNo': c} for c in cards]
    return request('POST', '/api/v3/shoppingCart/settlement/update', body=body)


def place_with_giftcard(shop, prods, cards, order_type=1, take_type=1):
    """完整小程序礼品卡链路：settlement(无卡) → settlement(带卡) → order/save。

    cards: ['cardNo', ...]
    返回 {'settlement': {...}, 'save': {...}, 'payable': 分, 'orderCode': ...}
    """
    s1 = settlement(shop, prods, order_type, take_type)
    if not (isinstance(s1, dict) and s1.get('code') == 0):
        return {'step': 'settlement(no-card)', 'resp': s1}
    tt = (s1.get('data') or {}).get('transToken')

    s2 = settlement(shop, prods, order_type, take_type, cards=cards, trans_token=tt)
    if not (isinstance(s2, dict) and s2.get('code') == 0):
        return {'step': 'settlement(with-card)', 'resp': s2}
    d2 = s2.get('data') or {}
    tt = d2.get('transToken') or tt

    # 支付策略：只允许礼品卡。卡不够全额 → 不建单（避免留下无法支付的孤儿订单）
    if not ALLOW_NON_GIFTCARD_PAY and (d2.get('price') or 0) > 0:
        return {'step': 'insufficient-card', 'aborted': True,
                'settlement': d2, 'total': d2.get('total'), 'payable': d2.get('price'),
                'card_discount': (d2.get('total') or 0) - (d2.get('price') or 0)}

    payload = {
        'shopId': shop, 'products': prods, 'transToken': tt, 'discountsType': 1,
        'selectedProductVoucherList': [], 'plusDiscountProductList': [],
        'orderType': str(order_type), 'miniProgType': 1, 'orderChannel': 2,
        'selectedGiftCardList': [{'cardNo': c} for c in cards],
        'useWalletPay': 0, 'takeType': take_type,
    }
    # ⚠️ 不要带 orderExtVo / remark / tableware：实测 4003 invalid sign（签名口径不一致），
    #    带 orderExtVo 则 8003「优惠信息变更」。省略这三个字段建单正常。
    for k in ('couponCode', 'couponId'):
        if d2.get(k):
            payload[k] = d2[k]
    save = request('POST', '/api/v2/order/save', body=payload)
    code = (save.get('data') or {}).get('orderCode') if isinstance(save, dict) else None
    return {'step': 'done', 'settlement': d2, 'save': save, 'orderCode': code,
            'total': d2.get('total'), 'payable': d2.get('price'),
            'card_discount': (d2.get('total') or 0) - (d2.get('price') or 0)}


def block_non_giftcard(what):
    """非礼品卡支付通道：已停用，直接拒绝，不发起任何调用（无环境变量开关）。"""
    die({'ok': False,
         'error': '非礼品卡支付暂不可用',
         'blocked_action': what,
         'policy': PAYMENT_POLICY,
         'hint': ['只用礼品卡结账：order --shop <id> --product <id> --yes',
                  '本版本不提供任何放行开关'],
         'note': '未发起任何网络请求'})


def _num(v, default=0.0):
    """把 200 / '200' / '200.0' 统一成 float；失败返回 default。"""
    try:
        return float(str(v).strip())
    except (TypeError, ValueError):
        return default


def _reject_specs(specs_arg):
    """--specs 目前后端不兼容：在任何网络请求之前就拒绝。"""
    if specs_arg and str(specs_arg).strip():
        die({'ok': False, 'error': '加料/规格（--specs）暂不支持',
             'reason': '结算接口只接受属性（温度/糖度）；specIds 非空会返回 4000 参数错误',
             'hint': '选口味请用 --attrs；加料待确认服务端字段后再开放',
             'note': '未发起任何网络请求'})


def _option_table(p):
    """列出商品的属性（温度/糖度…）与加料（spec），供 --attrs / --specs 解析。"""
    attrs, specs = [], []
    for g in p.get('productAttrs') or []:
        for a in g.get('productAttrs') or []:
            attrs.append({'id': str(a.get('attributeId')), 'name': a.get('attributeName'),
                          'group': g.get('attributeName'),
                          # attrStatus 可能是 int 1 也可能是字符串 '1'
                          'disabled': str(a.get('attrStatus')).strip() not in ('1', 'True', 'true'),
                          'rec': bool(a.get('cornerTag'))})
    for g in p.get('productSpecs') or []:
        for x in g.get('specs') or []:
            if x.get('specStatus') != 1:
                continue
            specs.append({'id': str(x.get('specId')), 'name': x.get('specName'),
                          'group': g.get('specName'),
                          'price': _num(x.get('specPrice'), 0) / 100.0})
    return attrs, specs


def _resolve_options(p, attrs_arg=None, specs_arg=None):
    """把 --attrs '正常冰,七分糖' 解析成 attributeId 列表。

    --specs 目前不具备后端兼容性（结算接口对非空 specIds 一律回 4000），
    因此在**发任何网络请求之前**就直接拒绝，避免走到下单阶段才失败。
    """
    if specs_arg and str(specs_arg).strip():
        die({'ok': False, 'error': '加料/规格（--specs）暂不支持',
             'reason': '结算接口只接受属性（温度/糖度）；specIds 非空会返回 4000 参数错误',
             'hint': '选口味请用 --attrs；加料待确认服务端字段后再开放',
             'note': '未发起任何网络请求'})

    attrs, _specs = _option_table(p)
    ids_a, picked = [], {}
    for want in [w.strip() for w in str(attrs_arg or '').split(',') if w.strip()]:
        hit = [x for x in attrs if x['id'] == want or x['name'] == want]
        if not hit:
            die({'ok': False, 'error': '商品没有这个属性: %s' % want,
                 'available': ['%s=%s' % (x['group'], x['name']) for x in attrs]})
        x = hit[0]
        if x['disabled']:
            die({'ok': False, 'error': '属性在本店不可选: %s' % x['name']})
        if picked.get(x['group']) == x['id']:
            continue                                  # 同一口味重复输入 → 去重，不产生重复 id
        if picked.get(x['group']):
            die({'ok': False, 'error': '同一组只能选一个: %s' % x['group']})
        picked[x['group']] = x['id']
        ids_a.append(x['id'])
    return ids_a, []


def _prods_for(p, num, attrs_arg=None, specs_arg=None):
    ids_a, ids_s = _resolve_options(p, attrs_arg, specs_arg)
    return [{'productId': p['productId'], 'cupId': '', 'productAmount': int(num),
             'modifiedTime': p.get('modifiedTime'), 'specIds': ids_s,
             'attributeIds': ids_a, 'comboProductDetail': []}]


def cmd_order(a):
    """报价（不写购物车）→ `--yes` 才建单。"""
    _reject_specs(getattr(a, 'specs', None))
    menu = fetch_menu(a.shop)
    p = find_product(menu, a.product)
    if not p:
        die('商品不存在: %s' % a.product)

    prods = _prods_for(p, a.num, getattr(a, 'attrs', None), getattr(a, 'specs', None))

    # 报价：直接走 settlement，不 addProduct、不 clearCart —— 不写购物车
    card_spec = getattr(a, 'giftcard', None) or 'auto'
    cards = _pick_giftcards(card_spec, a.shop, a.order_type)
    q = settlement(a.shop, prods, a.order_type, a.take_type)
    if not (isinstance(q, dict) and q.get('code') == 0):
        die({'step': 'settlement(quote)', 'resp': q})
    total = ((q.get('data') or {}).get('total') or 0) / 100.0
    print('[quote] 门店=%s 商品=%s x%s 合计=%.2f元' % (a.shop, p['productName'], a.num, total))

    if not a.yes:
        qc = settlement(a.shop, prods, a.order_type, a.take_type,
                        cards=[c['cardNo'] for c in cards],
                        trans_token=(q.get('data') or {}).get('transToken'))
        qd = qc.get('data') or {}
        payable = (qd.get('price') or 0) / 100.0
        out({'ok': False, 'quote_only': True,
             'msg': '只报价，未建单、未写购物车（加 --yes 才会真正下单）',
             'total_yuan': total, 'card_covers_yuan': (qd.get('total', 0) - qd.get('price', 0)) / 100.0,
             'payable_yuan': payable,
             'card_enough': payable <= 0})
        return

    # 实测关键点（否则 8003「优惠价格变更」）：
    #  1) 必须走小程序渠道 orderChannel=2 + miniProgType=1（orderChannel=3 建单失败）
    #  2) calcprice 里自动选中的优惠券字段必须原样带给 order/save ——
    #     真实账号会默认套「88折券」等券，不带券字段会导致下单价与算价不一致被拒。
    #  3) 礼品卡抵扣发生在 settlement/update（带 selectedGiftCardList → 返回 price=抵扣后应付），
    #     建单时要带同一个 transToken + selectedGiftCardList；付清 → prepay 返回 isZeroPay=1。
    # 默认必须走礼品卡（其他支付通道暂不可用）
    if cards:
        res = place_with_giftcard(a.shop, prods, [c['cardNo'] for c in cards],
                                  a.order_type, a.take_type)
        if res.get('aborted'):
            die({'ok': False,
                 'error': '礼品卡余额不足，未建单',
                 'total_yuan': (res.get('total') or 0) / 100.0,
                 'card_covers_yuan': (res.get('card_discount') or 0) / 100.0,
                 'short_yuan': (res.get('payable') or 0) / 100.0,
                 'policy': PAYMENT_POLICY,
                 'hint': '其他支付方式暂不可用；充值礼品卡后重试，或减少数量/换更便宜的商品'})
        code = res.get('orderCode')
        if not code:
            out({'ok': False, 'giftcard': [c['cardNo'] for c in cards], 'detail': res})
            return
        payable = (res.get('payable') or 0) / 100.0
        saved = (res.get('card_discount') or 0) / 100.0
        print('   礼品卡抵扣 %.2f 元 → 还需支付 %.2f 元' % (saved, payable))
        result = {'ok': True, 'orderCode': code,
                  'total_yuan': (res.get('total') or 0) / 100.0,
                  'giftcard_discount_yuan': saved, 'payable_yuan': payable}
        if payable <= 0:
            paid, info = pay_with_giftcard(code, a.shop, a.order_type, cards)
            result['paid'] = paid
            result['giftcard_pay'] = info
            result['next'] = ('已用礼品卡付清（零元支付，微信不参与）；取餐号：watch --order %s'
                              % code) if paid else '零元支付失败，看 giftcard_pay'
        else:
            result['paid'] = False
            result['next'] = ('礼品卡只抵了 %.2f 元，还差 %.2f 元需要微信付：paylink --order %s'
                              % (saved, payable, code))
        out(result)
        return

    save = request('POST', '/api/v2/order/save',
                   body=_save_payload(a.shop, calc.get('data'), a.order_type, a.take_type))
    code = (save.get('data') or {}).get('orderCode') if isinstance(save, dict) else None
    out({'order': save, 'total_yuan': total,
         'next': '订单已创建但未支付：跑 `paylink --order %s` 生成跳转收银台的链接/二维码' % code})


def cmd_cancel(a):
    """取消订单。会改变服务端状态，必须显式 --yes。"""
    if not getattr(a, 'yes', False):
        die({'ok': False,
             'error': 'cancel 会取消服务端订单，必须显式确认',
             'would_do': '取消订单 %s（已支付的单可能进入退款流程）' % a.order,
             'hint': ['确认取消就加 --yes'],
             'note': '未发起任何网络请求'})
    out(request('POST', '/api/v2/order/cancel', body={'orderCode': a.order}))


STATUS_TEXT = {10: '待支付', 20: '已支付/待取餐', 30: '制作中', 40: '待取餐',
               50: '已完成', 70: '已完成', 80: '已取消/已关闭'}


def find_order(code):
    r = request('POST', '/api/v2/order/cust/list', body={'type': 4, 'pageNum': 1, 'pageSize': 20})
    for o in ((r.get('data') or {}).get('list') or []):
        if str(o.get('orderCode')) == str(code):
            return o
    return None


def fetch_take_no(order_code):
    """支付后取餐号（HAR 里见到的 /api/v2/order/getTakeNo）"""
    for method in ('GET', 'POST'):
        try:
            r = request(method, '/api/v2/order/getTakeNo', {'orderCode': order_code},
                        body={} if method == 'POST' else None)
            if isinstance(r, dict) and r.get('code') == 0:
                return r.get('data')
        except Exception:
            pass
    return None


def cmd_watch(a):
    """轮询订单状态，直到支付/取消（给 AI 做闭环用）"""
    last = None
    for i in range(int(a.times)):
        o = find_order(a.order)
        if not o:
            print('[%02d] 查询不到该订单（可能已过期）' % i)
        else:
            st = o.get('orderStatus')
            line = 'status=%s(%s) payType=%s payTime=%s' % (
                st, STATUS_TEXT.get(st, '?'), o.get('payType'), o.get('payTime'))
            if line != last:
                print('[%02d] %s' % (i, line))
                last = line
            if st in (20, 30, 40, 50, 70):
                print('已支付 ✅')
                take = o.get('takeNo')
                if not take:
                    got = fetch_take_no(a.order) or {}
                    take = got.get('takeNo') if isinstance(got, dict) else None
                print('取餐号:', take if take else '（还没出号，稍后再查 orders）')
                return
            if st in (80,):
                print('订单已关闭 ❌')
                return
        time.sleep(a.interval)
    print('超时，未观察到状态变化')


def cmd_wechatqr(a):
    """PC 微信自动化支付：已停用（依赖 Windows 脚本，且属非礼品卡支付）。"""
    block_non_giftcard('wechatqr（PC 微信自动化支付）')
    die({'error': 'wechatqr 依赖 Windows + PowerShell 与 tools/wechat_pay_qr.ps1，本包未包含该脚本',
         'alternative': '用礼品卡结账：order --shop <id> --product <id> --yes',
         'note': '未发起任何网络请求'})


def cmd_place(a):
    """一条命令：报价 → 礼品卡建单 → 支付 →（可选）等取餐号。

    支付策略：默认只用礼品卡；其他支付通道暂不可用。卡不够全额时**不建单**。
    """
    _reject_specs(getattr(a, 'specs', None))
    if not getattr(a, 'yes', False):
        die({'ok': False,
             'error': 'place 会直接建单并扣减礼品卡余额，必须显式确认',
             'would_do': '算价 → 礼品卡建单 → 支付（卡不足则不建单）',
             'hint': ['确认要买就加 --yes',
                      '只想看价格用：order --shop <id> --product <id>（不带 --yes，只算价）'],
             'note': '未发起任何网络请求'})

    menu = fetch_menu(a.shop)
    p = find_product(menu, a.product)
    if not p:
        die('商品不存在: %s' % a.product)

    cards = _pick_giftcards(getattr(a, 'giftcard', None) or 'auto', a.shop, a.order_type)
    prods = _prods_for(p, a.num, getattr(a, 'attrs', None), getattr(a, 'specs', None))
    res = place_with_giftcard(a.shop, prods, [c['cardNo'] for c in cards],
                              a.order_type, a.take_type)

    if res.get('aborted'):
        die({'ok': False, 'error': '礼品卡余额不足，未建单',
             'total_yuan': (res.get('total') or 0) / 100.0,
             'card_covers_yuan': (res.get('card_discount') or 0) / 100.0,
             'short_yuan': (res.get('payable') or 0) / 100.0,
             'policy': PAYMENT_POLICY,
             'hint': '其他支付方式暂不可用；充值礼品卡后重试'})

    code = res.get('orderCode')
    if not code:
        die({'step': 'order/save', 'detail': res})

    total = (res.get('total') or 0) / 100.0
    print('✅ 已下单：%s  %s x%s  合计 %.2f 元' % (code, p['productName'], a.num, total))
    print('   门店：%s  |  礼品卡 %s' % (a.shop, cards[0]['cardNo'][:4] + '****' + cards[0]['cardNo'][-4:]))

    paid, info = pay_with_giftcard(code, a.shop, a.order_type, cards)
    if paid:
        print('   💳 礼品卡已付清（零元支付），不用微信')
    else:
        print('   ⚠️ 礼品卡支付未完成：%s' % json.dumps(redact(info), ensure_ascii=False)[:200])

    if a.wait and paid:
        print('   等待取餐号……')
        a2 = type('X', (), dict(order=code, interval=a.interval, times=a.times))()
        cmd_watch(a2)
    elif a.wait:
        print('   未付清，不等待取餐号')


def cmd_orders(a):
    r = request('POST', '/api/v2/order/cust/list',
                body={'type': int(a.type), 'pageNum': int(a.page), 'pageSize': int(a.size)})
    if isinstance(r, dict) and r.get('code') == 0:
        lst = (r.get('data') or {}).get('list') or []
        print('共 %s 单' % (r['data'].get('totalCount')))
        for o in lst:
            print('  %-20s status=%-3s payType=%-4s %5.2f元  %s' % (
                o.get('orderCode'), o.get('orderStatus'), o.get('payType'),
                (o.get('price') or 0) / 100.0, o.get('shopName')))
        return
    out(r)


def cmd_pay(a):
    """聚合支付（微信/支付宝）—— 已停用，默认不发起任何调用。"""
    block_non_giftcard('pay（微信/支付宝聚合支付）')
    return _cmd_pay_unused(a)


def _cmd_pay_unused(a):
    """聚合支付下单：POST /api/v2/order/prepay {orderCode, payType, openId}

    实测：payType=1/3/4/5/6 走微信(JSAPI)，返回 prepay_id+paySign；payType=2 走支付宝(需支付宝身份)。
    """
    body = {'orderCode': a.order, 'payType': int(a.pay_type)}
    if a.open_id:
        body['openId'] = a.open_id
    r = request('POST', '/api/v2/order/prepay', body=body)
    if isinstance(r, dict) and r.get('code') == 0:
        d = r.get('data') or {}
        if d.get('packageStr') or d.get('paySign'):
            snippet = {
                'channel': 'wechat-jsapi（微信支付，signType=%s）' % d.get('signType'),
                'wx.requestPayment': {
                    'timeStamp': str(d.get('timestamp')),
                    'nonceStr': d.get('nonceStr'),
                    'package': d.get('packageStr'),
                    'signType': d.get('signType'),
                    'paySign': d.get('paySign'),
                },
                'note': '在微信小程序里调用 wx.requestPayment(上面的参数) 才会真正扣款',
            }
        else:
            snippet = {'channel': 'unknown', 'raw': d,
                       'note': '支付宝通道 orderStr 为空表示该渠道未开通/需要支付宝身份'}
        out({'prepay': d, 'how_to_invoke': snippet})
    else:
        out({'prepay': r,
             'hint': 'payType=1/3/4/5/6 走微信(需微信 openId)；payType=2 走支付宝(需支付宝身份，易报 7002)'})


def build_mini_program_links(order_code, path=MP_PAY_PATH, env='release', query=None):
    """按蜜雪 H5 /#/redirect 页的同一套拼法生成跳转链接（已从 H5 源码确认）。"""
    import urllib.parse as up
    q = query if query else 'orderCode=%s' % order_code
    scheme = ('weixin://dl/business/?appid=%s&path=%s&query=%s&env_version=%s'
              % (MP_APPID, path, up.quote(q, safe=''), env))
    if '?' in path:
        p, sub = path.split('?', 1)
        q = sub
    else:
        p = path
    h5 = ('https://mxsa-h5.mxbc.net/#/redirect?path=%s%%3F%s&env=%s'
          % (p, up.quote(q, safe=''), env))
    return scheme, h5


def cmd_paylink(a):
    """跳小程序收银台（微信支付）—— 已停用，默认不发起任何调用。"""
    block_non_giftcard('paylink（微信收银台链接/二维码）')
    return _cmd_paylink_unused(a)


def _cmd_paylink_unused(a):
    """生成「跳到小程序收银台」的链接 + 二维码（微信里打开即可唤起付款界面）"""
    scheme, h5 = build_mini_program_links(a.order, path=a.path, env=a.env, query=a.query)
    info = {
        'orderCode': a.order,
        'miniProgram': {'appid': MP_APPID, 'path': a.path, 'env_version': a.env},
        'weixin_scheme': scheme,
        'h5_redirect': h5,
        'how_to_use': [
            '① 手机微信里直接打开 weixin_scheme（发到「文件传输助手」点开）',
            '② 或把 h5_redirect 发到微信里点开，它会自动跳到小程序',
            '③ 或用微信「扫一扫」扫下面的二维码',
        ],
        'if_page_empty': '若小程序没进收银台，试 --query "orderId=%s"' % a.order,
    }
    if a.qr:
        import qrcode
        img = qrcode.make(scheme)
        img.save(a.qr)
        info['qr_file'] = os.path.abspath(a.qr)
    out(info)


ALLOWED_RAW_PATHS = {
    # 只读：不改购物车、不建单、不支付
    '/api/v1/app/getTimestamp', '/api/v1/app/config', '/api/v1/app/version', '/api/v1/app/nav',
    '/api/v1/customer/info', '/api/v1/wallet/balance',
    '/api/v1/giftcard/summary', '/api/v1/giftcard/available/list',
    '/api/v2/shopinfo/findNear', '/api/v3/shopinfo/findRecommend', '/api/v4/shopinfo/findRecommend',
    '/api/v3/shop/menu/info', '/api/v2/shop/v2/menu/extInfo', '/api/v1/marketingMenu/query',
    '/api/v1/hotProduct/list', '/api/v2/shop/listMarketing',
    '/api/v2/order/cust/list', '/ordact/api/v1/luck-pack/info',
}


def _guard_raw_path(path):
    """通用 get/post 只能访问只读白名单，杜绝绕过 order/place 的确认。"""
    clean = urllib.parse.urlparse(path).path
    if clean not in ALLOWED_RAW_PATHS:
        die({'ok': False,
             'error': '通用接口只允许只读白名单，已拒绝',
             'path': clean,
             'hint': ['建单/支付/取消请用 order / place / cancel 等带确认的命令',
                      '白名单见源码 ALLOWED_RAW_PATHS'],
             'note': '未发起任何网络请求'})


def cmd_get(a):
    _guard_raw_path(a.path)
    params = dict(kv.split('=', 1) for kv in a.param) if a.param else {}
    out(request('GET', a.path, params))


def cmd_post(a):
    _guard_raw_path(a.path)
    params = dict(kv.split('=', 1) for kv in a.param) if a.param else {}
    body = json.loads(a.data) if a.data else None
    out(request('POST', a.path, params, body=body))


def main():
    global TOKEN_OVERRIDE, RAW_OUTPUT
    p = argparse.ArgumentParser(prog='mixuebingcheng-cli', description='蜜雪冰城点单 CLI（协议逆向版）')
    p.add_argument('--version', action='version', version='mixuebingcheng-cli %s' % VERSION)
    p.add_argument('--no-redact', action='store_true',
                   help='关闭输出脱敏（仅在自查时用，别把结果贴到聊天/日志）')
    p.add_argument('--token', default=None, help='临时覆盖 Access-Token（不写入文件）')
    sub = p.add_subparsers(dest='cmd', required=True)

    sub.add_parser('ping', help='服务器时间').set_defaults(func=cmd_ping)
    sub.add_parser('config', help='全局配置').set_defaults(func=cmd_config)

    s = sub.add_parser('login', help='手机号+验证码登录')
    s.add_argument('--phone', required=True)
    s.add_argument('--code', required=True)
    s.set_defaults(func=cmd_login)

    s = sub.add_parser('sms', help='发送短信验证码（需人机验证）')
    s.add_argument('--phone', required=True)
    s.set_defaults(func=cmd_sms)

    sub.add_parser('whoami', help='当前 token 用户信息').set_defaults(func=cmd_whoami)

    s = sub.add_parser('token', help='查看/设置 Access-Token（--stdin 避免进 shell 历史）')
    s.add_argument('--set', dest='set_token', help='写入新的 Access-Token')
    s.add_argument('--stdin', action='store_true', help='从标准输入读 token（推荐，不进历史）')
    s.add_argument('--show', action='store_true', help='已废弃：完整值请用全局 --no-redact')
    s.set_defaults(func=cmd_token)

    s = sub.add_parser('shops', help='附近门店')
    s.add_argument('--lat', required=True)
    s.add_argument('--lng', required=True)
    s.add_argument('--table', action='store_true')
    s.set_defaults(func=cmd_shops)

    s = sub.add_parser('menu', help='门店菜单')
    s.add_argument('--shop', required=True)
    s.add_argument('--table', action='store_true')
    s.set_defaults(func=cmd_menu)

    s = sub.add_parser('orders', help='订单列表')
    s.add_argument('--type', default='4', help='4=全部（默认，1 会返回空）')
    s.add_argument('--page', default='1')
    s.add_argument('--size', default='10')
    s.set_defaults(func=cmd_orders)

    s = sub.add_parser('pay', help='【暂不可用】聚合支付（微信/支付宝），默认拒绝调用')
    s.add_argument('--order', required=True, help='orderCode')
    s.add_argument('--pay-type', default='1')
    s.add_argument('--open-id', default=None)
    s.set_defaults(func=cmd_pay)

    s = sub.add_parser('paylink', help='【暂不可用】小程序收银台链接/二维码（微信支付）')
    s.add_argument('--order', required=True, help='orderCode')
    s.add_argument('--path', default=MP_PAY_PATH, help='小程序页面路径')
    s.add_argument('--env', default='release', help='release / trial / develop')
    s.add_argument('--query', default=None, help='自定义查询串，如 orderCode=xxx / orderId=xxx')
    s.add_argument('--qr', default=None, help='生成二维码 PNG 的路径，如 pay.png')
    s.set_defaults(func=cmd_paylink)

    def scene_opts(sp):
        sp.add_argument('--order-type', type=int, default=DEFAULT_ORDER['orderType'])
        sp.add_argument('--take-type', type=int, default=DEFAULT_ORDER['takeType'])
        sp.add_argument('--order-channel', type=int, default=DEFAULT_ORDER['orderChannel'])

    s = sub.add_parser('cart-add', help='加入购物车')
    s.add_argument('--shop', required=True)
    s.add_argument('--product', required=True)
    s.add_argument('--num', default='1')
    scene_opts(s)
    s.set_defaults(func=cmd_cart_add)

    s = sub.add_parser('calc', help='购物车算价')
    s.add_argument('--shop', required=True)
    scene_opts(s)
    s.set_defaults(func=cmd_calc)

    s = sub.add_parser('clear', help='清空购物车')
    s.add_argument('--shop', required=True)
    scene_opts(s)
    s.set_defaults(func=cmd_clear)

    s = sub.add_parser('order', help='报价（默认只读）/ --yes 建单并用礼品卡支付')
    s.add_argument('--shop', required=True)
    s.add_argument('--product', required=True)
    s.add_argument('--num', default='1')
    s.add_argument('--yes', action='store_true', help='确认建单并用礼品卡支付（必填才下单）')
    s.add_argument('--giftcard', default='auto',
                   help='礼品卡结账（默认 auto=自动选余额最高的一张）；也可填 cardNo。其他支付方式暂不可用')
    s.add_argument('--openid', default=None, help='临时覆盖小程序 openId（默认读 tools/openid.txt）')
    s.add_argument('--attrs', default=None, help="口味属性，逗号分隔，如 '正常冰,七分糖'（也可给 attributeId）")
    s.add_argument('--specs', default=None, help="加料/规格，逗号分隔，如 '脆啵啵'（加料后端暂不支持）")
    scene_opts(s)
    s.set_defaults(func=cmd_order)

    s = sub.add_parser('giftcards', help='列可用蜜雪礼品卡（cardNo / 余额 / 有效期）')
    s.add_argument('--shop', default=DEFAULT_SHOP, required=not DEFAULT_SHOP)
    s.set_defaults(func=cmd_giftcards)

    s = sub.add_parser('env', help='显示配置来源（.env / 环境变量 / 旧文件），不打印密钥明文')
    s.set_defaults(func=cmd_env)

    s = sub.add_parser('init', help='首次配置：生成 .env 模板并提示怎么获取凭据')
    s.set_defaults(func=cmd_init)

    s = sub.add_parser('har', help='从抓包 .har 自动提取 Access-Token / openId / customerId')
    s.add_argument('path', help='.har 文件路径')
    s.set_defaults(func=cmd_har)

    s = sub.add_parser('needs', aliases=['guide'], help='要抓哪些域名/接口、每个字段出现在哪')
    s.set_defaults(func=cmd_needs)

    s = sub.add_parser('key', help='查看/设置签名私钥（状态与路径）')
    s.add_argument('--set', default=None, help='指定 PEM 私钥文件路径并写入 .env')
    s.set_defaults(func=cmd_key)

    s = sub.add_parser('cancel', help='取消订单（需 --yes）')
    s.add_argument('--order', required=True, help='orderCode')
    s.add_argument('--yes', action='store_true', help='确认取消（必填）')
    s.set_defaults(func=cmd_cancel)

    s = sub.add_parser('watch', help='轮询订单状态（付完自动确认并输出取餐号）')
    s.add_argument('--order', required=True, help='orderCode')
    s.add_argument('--interval', type=int, default=3, help='轮询间隔秒')
    s.add_argument('--times', type=int, default=40, help='最多轮询次数')
    s.set_defaults(func=cmd_watch)

    s = sub.add_parser('place', help='一键下单+礼品卡支付（需 --yes；--wait 等取餐号）')
    s.add_argument('--shop', required=True)
    s.add_argument('--product', required=True)
    s.add_argument('--num', default='1')
    s.add_argument('--wait', action='store_true', help='下单后一直等到支付成功并打印取餐号')
    s.add_argument('--interval', type=int, default=3)
    s.add_argument('--times', type=int, default=200)
    s.add_argument('--giftcard', default='auto',
                   help='礼品卡结账（默认 auto）；其他支付方式暂不可用')
    s.add_argument('--yes', action='store_true', help='确认下单并扣减礼品卡（place 必填）')
    s.add_argument('--openid', default=None, help='临时覆盖小程序 openId')
    s.add_argument('--attrs', default=None, help="口味属性，逗号分隔，如 '正常冰,七分糖'（也可给 attributeId）")
    s.add_argument('--specs', default=None, help="加料/规格，逗号分隔，如 '脆啵啵'（加料后端暂不支持）")
    scene_opts(s)
    s.set_defaults(func=cmd_place)

    s = sub.add_parser('wechatqr', help='【暂不可用】PC 微信自动化支付')
    s.add_argument('--shop', default=DEFAULT_SHOP, required=not DEFAULT_SHOP)
    s.add_argument('--product', required=True)
    s.add_argument('--num', default='1')
    s.add_argument('--order', default=None, help='复用已存在的 orderCode（跳过建单）')
    s.add_argument('--out', default=os.path.join(ROOT, 'pay_wechat_qr.png'))
    scene_opts(s)
    s.set_defaults(func=cmd_wechatqr)

    s = sub.add_parser('get', help='任意 GET')
    s.add_argument('--path', required=True)
    s.add_argument('--param', action='append')
    s.set_defaults(func=cmd_get)

    s = sub.add_parser('post', help='任意 POST')
    s.add_argument('--path', required=True)
    s.add_argument('--param', action='append')
    s.add_argument('--data')
    s.set_defaults(func=cmd_post)

    a = p.parse_args()
    RAW_OUTPUT = bool(getattr(a, 'no_redact', False))
    TOKEN_OVERRIDE = a.token
    global OPENID_OVERRIDE
    OPENID_OVERRIDE = getattr(a, 'openid', None)
    a.func(a)


if __name__ == '__main__':
    main()
