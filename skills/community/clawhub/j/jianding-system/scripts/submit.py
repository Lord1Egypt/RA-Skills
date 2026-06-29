#!/usr/bin/env python3
"""
收藏雅集网 · 鉴定提交脚本（多环境版）

═══════════════════════════════════════════════════════════════
                          环境与认证方式
───────────────────────────────────────────────────────────────
  微信小程序环境          非微信环境（终端 / H5 / CLI）
  ─────────────           ──────────────────────────
  登录: user/wxLogin      登录: user/h5Login
  参数: --code (wx.login) 参数: --phone + --sms-code
                          发验证码: sms/sendCode
───────────────────────────────────────────────────────────────
  Token 保存到 ~/.jianding_token，后续命令自动读取
═══════════════════════════════════════════════════════════════

用法:
  # ===== 登录 =====
  # 微信环境
  python3 submit.py login --code "wx.login()的code"

  # 非微信环境
  python3 submit.py login --phone 13800138000 --sms-code 123456

  # 非微信环境 — 先发验证码
  python3 submit.py send-sms --phone 13800138000

  # ===== 查看信息 =====
  python3 submit.py info

  # ===== 完整提交 =====
  python3 submit.py full \
    --images /tmp/a.jpg /tmp/b.jpg ... \
    --desc "清乾隆青花瓷盘，直径25cm，祖传，品相完好" \
    --phone "13800138000" \
    --category "瓷器"

  支持 --token / --code / --phone 三种认证方式。

  # ===== 查结果 =====
  python3 submit.py result --order-no ORD20260615xxx

依赖: pip install requests qrcode pillow
"""

import os, sys, json, argparse, time, tempfile
import requests as req

BASE  = "https://jiand.shoucangyaji.com/jianbao/api/index.php?action="
TOKEN_FILE = os.path.expanduser("~/.jianding_token")

# ══════════════════════════════════════════════════════════
# helpers
# ══════════════════════════════════════════════════════════

def api(method, action, token=None, max_retries=3, **kw):
    """调用 API，返回 data 字段。网络错误自动重试（最多 3 次，指数退避 1s→2s→4s）。
    
    重试条件：网络超时、连接失败、DNS 解析失败、响应不完整（JSON 解析失败）。
    不重试：HTTP 业务错误（API 返回 code != 0/200）—— 业务错误重试无意义。
    """
    url = BASE + action
    h = {"Authorization": f"Bearer {token}"} if token else {}

    last_error = None
    for attempt in range(max_retries):
        try:
            if method == "GET":
                params = kw.get("params") or kw.get("json") or {}
                r = req.get(url, headers=h, params=params, timeout=30)
            elif "files" in kw:
                r = req.post(url, headers=h, files=kw["files"], timeout=60)
            else:
                h["Content-Type"] = "application/json"
                r = req.post(url, headers=h, json=kw.get("json", {}), timeout=30)

            body = r.json()
            if body.get("code") != 0 and body.get("code") != 200:
                msg = body.get("msg") or body.get("message") or json.dumps(body, ensure_ascii=False)
                die(f"API 错误 [{action}]: {msg}\n  请求: {method} {url}")
            return body.get("data", body)

        except req.exceptions.Timeout:
            last_error = f"请求超时 (第{attempt+1}/{max_retries}次): {method} {url}"
        except req.exceptions.ConnectionError:
            last_error = f"连接失败 (第{attempt+1}/{max_retries}次): {method} {url}"
        except req.exceptions.RequestException as e:
            last_error = f"网络异常[{type(e).__name__}] (第{attempt+1}/{max_retries}次): {method} {url}"
        except (json.JSONDecodeError, ValueError):
            last_error = f"响应解析失败 (第{attempt+1}/{max_retries}次): {method} {url}"

        if attempt < max_retries - 1:
            wait = 2 ** attempt  # 1s, 2s, 4s
            warn(f"{last_error}，{wait}秒后自动重试…")
            time.sleep(wait)

    die(f"{last_error}\n  已重试 {max_retries} 次均失败，请检查网络后重试。")

def die(msg):
    """打印错误并退出，附排查建议"""
    print(f"\033[31m✘ {msg}\033[0m", file=sys.stderr)
    print(f"\033[90m💡 遇到问题？查看 SKILL.md 末尾「故障排查」表格，或尝试微信打开 https://jiand.shoucangyaji.com/ 自助操作。\033[0m", file=sys.stderr)
    sys.exit(1)

def ok(msg):
    print(f"\033[32m✔ {msg}\033[0m")

def warn(msg):
    print(f"\033[33m⚠ {msg}\033[0m")

def info(msg):
    print(f"\033[36mℹ {msg}\033[0m")

def load_token():
    """从文件加载已保存的 token"""
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE) as f:
                return f.read().strip()
        except:
            pass
    return None

def save_token(token):
    """保存 token 到文件"""
    try:
        with open(TOKEN_FILE, "w") as f:
            f.write(token)
        ok(f"Token 已保存到 {TOKEN_FILE}")
    except Exception as e:
        warn(f"Token 保存失败: {e}")

# 小程序码路径（兜底用）
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_QR_FALLBACK = os.path.join(_SCRIPT_DIR, "..", "小程序码-扫码提交.png")

def _show_fallback():
    """所有认证方式都失效时，打印兜底方案"""
    qr_path = os.path.normpath(_QR_FALLBACK)
    print(f"\n{'='*50}")
    print(f"  ⚠ 当前环境无法完成自动登录/提交")
    print(f"")
    print(f"  💡 推荐方案：微信打开 H5 自助鉴定")
    print(f"     https://jiand.shoucangyaji.com/")
    print(f"     上传照片 → 填写描述 → 微信支付 ¥100 → 24h 出报告")
    print(f"")
    print(f"  📱 备选方案：微信扫小程序码提交")
    print(f"     图片路径: {qr_path}")
    print(f"{'='*50}")
    return qr_path

def get_token(args, allow_fallback=True):
    """获取 token，所有方式失效时返回 None（不 die）"""
    # 1. 直接传入的 token
    if hasattr(args, 'token') and args.token:
        return args.token

    # 2. 小程序 code → 微信登录
    if hasattr(args, 'code') and args.code:
        info("【微信环境】登录中...")
        try:
            data = api("POST", "user/wxLogin", json={"code": args.code})
            token = data.get("token") or data.get("access_token")
            if token:
                save_token(token)
                return token
            warn("微信登录返回无 token")
        except SystemExit:
            raise
        except Exception as e:
            warn(f"微信登录失败: {e}")

    # 3. 手机号+验证码 → H5 登录
    if hasattr(args, 'phone') and args.phone and hasattr(args, 'sms_code') and args.sms_code:
        info("【非微信环境】手机号登录中...")
        try:
            data = api("POST", "user/h5Login", json={"phone": args.phone, "smsCode": args.sms_code})
            token = data.get("token") or data.get("access_token")
            if token:
                save_token(token)
                return token
            warn("手机号登录返回无 token")
        except SystemExit:
            raise
        except Exception as e:
            warn(f"手机号登录失败: {e}")

    # 4. 从文件加载
    token = load_token()
    if token:
        info("使用已保存的 token")
        return token

    # 全部失效 — 兜底
    if allow_fallback:
        _show_fallback()
    return None

# ══════════════════════════════════════════════════════════
# 命令实现
# ══════════════════════════════════════════════════════════

def cmd_login(args):
    """登录并保存 token（根据参数自动选择微信或手机号登录）"""
    token = None

    if args.code:
        # ── 微信环境 ──
        info("【微信环境】通过 wx.login() code 登录...")
        data = api("POST", "user/wxLogin", json={"code": args.code})
        token = data.get("token") or data.get("access_token")
        if not token:
            die("微信登录失败：未获取到 token")

    elif args.phone and args.sms_code:
        # ── 非微信环境 ──
        info("【非微信环境】通过手机号+验证码登录...")
        data = api("POST", "user/h5Login", json={"phone": args.phone, "smsCode": args.sms_code})
        token = data.get("token") or data.get("access_token")
        if not token:
            die("手机号登录失败：未获取到 token")

    elif args.token:
        token = args.token

    else:
        die("请提供认证方式:\n"
            "  微信环境:  submit.py login --code <wx.login()code>\n"
            "  非微信环境:  submit.py login --phone 13800138000 --sms-code 123456\n"
            "  已有token: submit.py login --token <token>")

    save_token(token)
    print(f"\nToken: {token[:20]}...{token[-10:] if len(token)>30 else ''}")
    ok("登录成功！")


def cmd_send_sms(args):
    """发送短信验证码（非微信环境专用）"""
    if not args.phone:
        die("请提供手机号: submit.py send-sms --phone 13800138000")

    info(f"【非微信环境】发送验证码到 {args.phone}...")
    api("POST", "sms/sendCode", json={"phone": args.phone})
    ok(f"验证码已发送到 {args.phone}，请查收短信")


def cmd_info(_args):
    """查看鉴定费用和专家"""
    cfg = api("GET", "user/config")
    exp = api("GET", "user/experts", json={"page": 1, "pageSize": 20})

    cost = cfg.get("jianbao_cost_yuan", 100)
    total = cfg.get("total_orders", "?")
    experts = exp.get("list", [])

    print(f"收藏雅集网 · 累计鉴定 {total} 人次")
    print(f"鉴定费用: ¥{cost}/次\n")
    print("可选专家:")
    for e in experts:
        name = e.get("title") or e.get("name") or e.get("expert_name", "未知")
        exp_years = e.get("experience", "?")
        rating = e.get("rating", "?")
        cnt = e.get("order_count", "?")
        eid = e.get("expert_id") or e.get("id", "?")
        print(f"  [{eid}] {name}  ·  {exp_years}年经验  ·  好评率 {rating}%  ·  已服务 {cnt} 次")


def cmd_full(args):
    """完整流程：登录 → 上传 → 创建订单 → 支付 → 生成二维码"""
    # ── 1. 登录 ──
    token = get_token(args)
    if not token:
        return  # 已打印兜底方案

    # ── 2. 上传图片 ──
    urls = []
    for f in args.images:
        fname = os.path.basename(f)
        print(f"上传: {fname}")
        with open(f, "rb") as fh:
            data = api("POST", "upload/image", token=token, files={"file": (fname, fh)})
        url = data.get("url", "")
        if not url:
            die(f"上传失败: {fname}")
        urls.append(url)
        ok(f"  {url}")
    print(f"共上传 {len(urls)} 张图片")

    # ── 3. 创建订单 ──
    desc = args.desc or "用户上传藏品，待专家鉴定"
    if not args.desc:
        warn("未提供藏品描述，将使用默认描述。建议使用多模态模型自动生成描述。")
    body = {
        "expert_id": args.expert,
        "description": desc,
        "images": urls,
        "category": args.category or "其他",
        "source": "skills",  # 标记来源：skills/CLI 代理提交
    }
    if args.phone:
        body["phone"] = args.phone

    print("创建订单...")
    order = api("POST", "user/createOrder", token=token, json=body)
    order_id = order.get("id")
    order_no = order.get("order_no", "")
    ok(f"订单创建成功: {order_no}")

    # ── 4. 支付 ──
    print("获取支付信息...")
    pay = api("POST", "user/pay", token=token, json={"orderId": order_id, "method": "wechat"})

    # 优先二维码（code_url），其次 H5 支付链接
    pay_url = pay.get("code_url", "") or pay.get("h5_url", "") or pay.get("mweb_url", "")
    if not pay_url:
        die("未获取到支付链接，请稍后在「我的订单」中支付")

    # ── 5. 生成二维码 ──
    out = args.output or os.path.join(tempfile.gettempdir(), f"jianding_{order_no}.png")
    _gen_qr(pay_url, out)
    ok(f"二维码已生成: {out}")

    # ── 6. 汇总 ──
    amount = pay.get("amount", 0)
    amount_yuan = f"¥{amount / 100:.2f}" if isinstance(amount, (int, float)) and amount > 100 else f"¥{amount}"

    print(f"\n{'='*50}")
    print(f"  订单号: {order_no}")
    print(f"  费用: {amount_yuan}")
    print(f"  藏品: {args.desc[:40]}{'...' if len(args.desc)>40 else ''}")
    print(f"  图片: {len(urls)} 张")
    print(f"  二维码: {out}")
    print(f"{'='*50}")
    print(f"\n请微信扫码支付。支付完成后会收到短信提醒。")

    return out, order_no


def cmd_result(args):
    """查询鉴定结果"""
    token = get_token(args)
    if not token:
        return  # 已打印兜底方案

    if args.order_no:
        # order_no 格式为 "ORD..."，需通过列表匹配获取数字 id
        orders_data = api("GET", "user/orders", token=token, params={"page": 1, "pageSize": 50})
        order_list = orders_data.get("list", []) if orders_data else []
        order_id = None
        for o in order_list:
            if o.get("order_no") == args.order_no:
                order_id = o.get("id")
                break
        if not order_id:
            die(f"未找到订单: {args.order_no}\n"
                f"  请核对订单号格式（如 ORD20260615001）\n"
                f"  或微信打开 https://jiand.shoucangyaji.com/ →【个人中心】→【我的订单】查看")
        data = api("GET", "user/orderDetail", token=token, params={"id": order_id})
    else:
        orders_data = api("GET", "user/orders", token=token, params={"page": 1, "pageSize": 1})
        if orders_data and orders_data.get("list"):
            first_order = orders_data["list"][0]
            data = api("GET", "user/orderDetail", token=token, params={"id": first_order["id"]})
        else:
            die("未找到订单")

    status = data.get("status", "unknown")
    order_no = data.get("order_no", "-")

    print(f"\n订单号: {order_no}")
    print(f"状态: {_status_text(status)}")

    if status == "completed":
        report = data.get("report") or {}
        expert = data.get("expert") or {}
        expert_name = data.get("expert_title") or expert.get("title") or expert.get("name", "")
        rating = data.get("expert_rating") or expert.get("rating", "")

        result = report.get("result") or report.get("conclusion") or data.get("result", "")
        period = report.get("period") or data.get("period", "")
        value = report.get("value_estimate") or report.get("price") or data.get("value", "")
        opinion = report.get("opinion") or report.get("suggestion") or data.get("suggestion", "")

        print(f"\n{'='*50}")
        if expert_name:
            rating_str = f"（好评率 {rating}%）" if rating else ""
            print(f"  鉴定专家: {expert_name} {rating_str}")
        if result:
            print(f"  鉴定结论: {result}")
        if period:
            print(f"  年代: {period}")
        if value:
            print(f"  市场参考价: ¥{value}")
        if opinion:
            print(f"  专家意见: {opinion}")
        print(f"{'='*50}")
    elif status == "paid":
        print("订单已支付，等待专家鉴定中...")
    elif status == "processing":
        print("专家正在鉴定中，预计 24 小时内完成。")
    elif status == "pending":
        print("订单待支付，请先完成支付。")


def cmd_qr(args):
    """对已有订单生成支付二维码"""
    token = get_token(args)
    if not token:
        return  # 已打印兜底方案

    print("获取支付二维码...")
    pay = api("POST", "user/pay", token=token, json={"orderId": args.order_id, "method": "wechat"})
    pay_url = pay.get("code_url", "") or pay.get("h5_url", "") or pay.get("mweb_url", "")
    if not pay_url:
        die("未获取到支付链接")

    out = args.output or os.path.join(tempfile.gettempdir(), f"jianding_order{args.order_id}.png")
    _gen_qr(pay_url, out)
    ok(f"二维码已生成: {out}")
    print(f"请微信扫描二维码完成支付")


def _status_text(s):
    return {"pending": "待支付", "paid": "已支付待鉴定", "processing": "鉴定中", "completed": "已完成", "cancelled": "已取消"}.get(s, s)


def _gen_qr(url, path):
    try:
        import qrcode
        img = qrcode.make(url)
        img.save(path)
    except ImportError:
        die("缺少 qrcode 库: pip install qrcode pillow")

# ══════════════════════════════════════════════════════════
# 入口
# ══════════════════════════════════════════════════════════

def main():
    p = argparse.ArgumentParser(description="收藏雅集网鉴定提交脚本（微信/非微信双环境支持）")

    # 通用认证参数（所有命令共享）
    def add_auth(sp):
        sp.add_argument("--token", help="已有的登录 token")
        sp.add_argument("--code", help="[微信环境] wx.login() 返回的 code")
        sp.add_argument("--phone", help="[非微信环境] 手机号")
        sp.add_argument("--sms-code", dest="sms_code", help="[非微信环境] 短信验证码")

    sp = p.add_subparsers(dest="cmd")

    # login
    lp = sp.add_parser("login", help="登录并保存 token")
    add_auth(lp)

    # send-sms
    sp_sms = sp.add_parser("send-sms", help="[非微信环境] 发送短信验证码")
    sp_sms.add_argument("--phone", required=True, help="手机号")

    # info
    sp.add_parser("info", help="查看费用和专家")

    # full
    f = sp.add_parser("full", help="完整提交流程")
    f.add_argument("--images", nargs="+", required=True, help="图片文件路径（至少6张）")
    f.add_argument("--desc", default="", help="藏品描述（多模态模型可自动生成，否则需用户提供）")
    f.add_argument("--category", default="其他", help="分类")
    f.add_argument("--expert", type=int, default=17, help="专家ID，默认17")
    f.add_argument("-o", "--output", help="二维码输出路径")
    add_auth(f)

    # result
    rp = sp.add_parser("result", help="查询鉴定结果")
    rp.add_argument("--order-no", dest="order_no", help="订单号（不传则查最近一个）")
    add_auth(rp)

    # qr
    q = sp.add_parser("qr", help="对已有订单生成支付二维码")
    q.add_argument("--order-id", type=int, required=True, help="订单ID")
    q.add_argument("-o", "--output", help="二维码输出路径")
    add_auth(q)

    args = p.parse_args()
    if not args.cmd:
        p.print_help()
        sys.exit(0)

    try:
        if args.cmd == "login":
            cmd_login(args)
        elif args.cmd == "send-sms":
            cmd_send_sms(args)
        elif args.cmd == "info":
            cmd_info(args)
        elif args.cmd == "full":
            cmd_full(args)
        elif args.cmd == "result":
            cmd_result(args)
        elif args.cmd == "qr":
            cmd_qr(args)
    except req.exceptions.RequestException as e:
        die(f"网络错误: {e}")
    except Exception as e:
        die(f"错误: {e}")


if __name__ == "__main__":
    main()
