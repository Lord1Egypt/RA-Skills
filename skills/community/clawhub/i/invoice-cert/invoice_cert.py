#!/usr/bin/env python3
"""发票认证技能 - 税局登录、发票勾选认证、抵扣统计"""

import argparse
import json
import os
import sys

try:
    from common import is_error, post, validate_date
except ImportError:
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    from common import is_error, post, validate_date

SESSION_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".session")


def save_session(api_key: str, credit_code: str, account: str, password: str,
                 area_code: str = ""):
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump({"apiKey": api_key, "creditCode": credit_code,
                   "account": account, "password": password,
                   "areaCode": area_code}, f, ensure_ascii=False)


def load_session():
    if not os.path.isfile(SESSION_FILE):
        return None
    try:
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def clear_session():
    if os.path.isfile(SESSION_FILE):
        os.remove(SESSION_FILE)


def try_auto_login(api_key: str) -> bool:
    session = load_session()
    if not session:
        return False
    data = {"apiKey": api_key, "creditCode": session["creditCode"]}
    if session.get("account"):
        data["account"] = session["account"]
    if session.get("password"):
        data["password"] = session["password"]
    if session.get("areaCode"):
        data["areaCode"] = session["areaCode"]
    result = post("/api/jxplus/zxtSkill/dzsj/dzsjLogin", {"data": data})
    d = result.get("data", {})
    if str(result.get("status")) == "200" and str(d.get("returnType")) == "4000":
        return True
    clear_session()
    return False


def post_with_auto_login(path: str, data: dict, api_key: str) -> dict:
    result = post(path, data)
    if str(result.get("status", "")) != "309":
        return result
    if try_auto_login(api_key):
        return post(path, data)
    return result


def check_error(result: dict):
    status = str(result.get("status", ""))
    if status == "200":
        return None
    if status == "309":
        return ("税局未登录且无可用会话缓存，请先调用 login 命令进行税局登录。"
                "需要提供税号、账号、密码等信息。")
    return f"[错误] {result.get('message', '未知错误')} (status={status})"


# ---- 子命令实现 ----

def cmd_login(args):
    data = {"apiKey": args.api_key, "creditCode": args.credit_code}
    if args.account:
        data["account"] = args.account
    if args.password:
        data["password"] = args.password
    if args.area_code:
        data["areaCode"] = args.area_code
    result = post("/api/jxplus/zxtSkill/dzsj/dzsjLogin", {"data": data})
    err = check_error(result)
    if err:
        print(err)
        return
    d = result.get("data", {})
    rt = d.get("returnType", "")
    if rt == "4000":
        save_session(args.api_key, args.credit_code,
                     args.account or "", args.password or "", args.area_code or "")
        print("登录成功")
    elif rt == "4001":
        save_session(args.api_key, args.credit_code,
                     args.account or "", args.password or "", args.area_code or "")
        mobile = d.get("loginMobile", "")
        print(f"需要验证码登录，验证码将发送至手机号：{mobile}")
        print("请先调用 send-sms 发送验证码，再调用 login-sms 完成登录。")
    elif rt == "4002":
        save_session(args.api_key, args.credit_code,
                     args.account or "", args.password or "", args.area_code or "")
        areas = d.get("areaList", [])
        print("需要设置地区，可选地区如下：")
        for a in areas:
            print(f"  {a.get('areaCode', '')} - {a.get('areaName', '')}")
        print("请使用 --area-code 参数指定地区码后重新登录。")
    else:
        print(f"登录返回：returnType={rt}")
        print(json.dumps(d, ensure_ascii=False, indent=2))


def cmd_login_sms(args):
    result = post("/api/jxplus/zxtSkill/dzsj/dzsjLoginBySmsCode", {
        "data": {"smsCode": args.sms_code, "creditCode": args.credit_code,
                 "account": args.account, "apiKey": args.api_key}
    })
    err = check_error(result)
    if err:
        print(err)
        return
    d = result.get("data", {})
    rt = d.get("returnType", "")
    if rt == "4000":
        save_session(args.api_key, args.credit_code, args.account, "")
        print("验证码登录成功")
    elif rt == "4001":
        print("身份认证已失效，请重新登录")
    else:
        print(f"返回：returnType={rt}")


def cmd_send_sms(args):
    result = post("/api/jxplus/zxtSkill/dzsj/dzsjSendSmsCode", {
        "data": {"creditCode": args.credit_code, "account": args.account,
                 "apiKey": args.api_key}
    })
    err = check_error(result)
    if err:
        print(err)
        return
    d = result.get("data", {})
    rt = d.get("returnType", "")
    if rt == "4000":
        print("验证码发送成功")
    elif rt == "4001":
        print("身份认证已失效，请重新登录")
    else:
        print(f"返回：returnType={rt}")


def cmd_current_period(args):
    result = post_with_auto_login("/api/jxplus/zxtSkill/check/getCurrSkssq", {
        "data": {"apiKey": args.api_key}
    }, args.api_key)
    err = check_error(result)
    if err:
        print(err)
        return
    d = result.get("data", "")
    print(f"当前税款所属期: {d}")


def cmd_sign(args):
    result = post_with_auto_login("/api/jxplus/zxtSkill/check/doSignature", {
        "data": {"apiKey": args.api_key}
    }, args.api_key)
    err = check_error(result)
    if err:
        print(err)
        return
    print("确认签名成功")
    d = result.get("data")
    if d:
        print(json.dumps(d, ensure_ascii=False, indent=2))


def cmd_statistics(args):
    result = post_with_auto_login("/api/jxplus/zxtSkill/check/commitStatistics", {
        "data": {"commitType": args.commit_type, "bz": args.bz,
                 "apiKey": args.api_key}
    }, args.api_key)
    msg = str(result.get("message", ""))
    if "1001" in msg or "1002" in msg:
        print(f"提示：{msg}，正在自动重试（bz=Y）...")
        result = post_with_auto_login("/api/jxplus/zxtSkill/check/commitStatistics", {
            "data": {"commitType": args.commit_type, "bz": "Y",
                     "apiKey": args.api_key}
        }, args.api_key)
    err = check_error(result)
    if err:
        print(err)
        return
    action = "申请统计" if args.commit_type == "1" else "撤销统计"
    print(f"{action}成功")
    d = result.get("data")
    if d:
        print(json.dumps(d, ensure_ascii=False, indent=2))


def cmd_deduct_stats(args):
    data = {"apiKey": args.api_key}
    if args.skssq:
        data["skssq"] = args.skssq
    result = post_with_auto_login(
        "/api/jxplus/zxtSkill/check/getDeductStatistList", {"data": data},
        args.api_key)
    err = check_error(result)
    if err:
        print(err)
        return
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_checked_invoices(args):
    data = {"apiKey": args.api_key}
    if args.skssq:
        data["skssq"] = args.skssq
    result = post_with_auto_login("/api/jxplus/zxtSkill/check/getCheckedInvoiceList", {
        "data": data
    }, args.api_key)
    err = check_error(result)
    if err:
        print(err)
        return
    invoices = result.get("data", [])
    if isinstance(invoices, list):
        print(f"当前属期认证发票共 {len(invoices)} 张：")
        for i, inv in enumerate(invoices, 1):
            print(f"  [{i}] {inv.get('fplxName', '-')} {inv.get('invoiceNumber', '-')}")
            print(f"      发票代码: {inv.get('invoiceCode') or '-'}  "
                  f"全电发票号码: {inv.get('qdfphm') or '-'}")
            print(f"      开票日期: {inv.get('kprq', '-')}  "
                  f"发票类型: {inv.get('fplx', '-')}")
            print(f"      合计金额: {inv.get('hjje', '-')}  "
                  f"合计税额: {inv.get('hjse', '-')}  "
                  f"价税合计: {inv.get('jshj', '-')}")
            print(f"      销方: {inv.get('xsfMc', '-')}  "
                  f"销方税号: {inv.get('xsfNsrsbh', '-')}")
    else:
        print(json.dumps(invoices, ensure_ascii=False, indent=2))


def cmd_check_status(args):
    result = post_with_auto_login("/api/jxplus/zxtSkill/check/getInvoiceCheckStatus", {
        "data": {"invoiceNumber": args.invoice_number,
                 "invoiceDate": args.invoice_date,
                 "apiKey": args.api_key,
                 **({"invoiceCode": args.invoice_code} if args.invoice_code else {})}
    }, args.api_key)
    err = check_error(result)
    if err:
        print(err)
        return
    d = result.get("data", {})
    gxzt = d.get("gxzt", "-")
    gxzt_name = "已勾选" if gxzt == "1" else "未勾选"
    print(f"发票认证状态：{gxzt_name} (gxzt={gxzt})")
    print(f"  发票代码: {d.get('invoiceCode') or '-'}")
    print(f"  发票号码: {d.get('invoiceNumber', '-')}")
    print(f"  开票日期: {d.get('kprq', '-')}")
    print(f"  合计金额: {d.get('hjje', '-')}  合计税额: {d.get('hjse', '-')}")
    print(f"  认证属期: {d.get('skssq') or '-'}")


BATCH_SIZE = 50


def cmd_commit_deduction(args):
    invoice_list = []
    for item_str in args.invoices:
        parts = item_str.split(",")
        if len(parts) < 3:
            print(f"[错误] 发票信息格式不正确: {item_str}，需要 invoiceCode,kprq,invoiceNumber")
            return
        invoice_list.append({
            "invoiceCode": parts[0],
            "kprq": parts[1],
            "invoiceNumber": parts[2]
        })

    # 按开票日期排序
    invoice_list.sort(key=lambda x: x["kprq"])

    action = "勾选认证" if args.commit_type == "1" else "取消勾选认证"
    total_success = 0
    total_fail = 0
    all_success = []
    all_fail = []

    # 分批提交，每批最多 BATCH_SIZE 张
    for i in range(0, len(invoice_list), BATCH_SIZE):
        batch = invoice_list[i:i + BATCH_SIZE]
        batch_no = i // BATCH_SIZE + 1
        total_batches = (len(invoice_list) + BATCH_SIZE - 1) // BATCH_SIZE

        if total_batches > 1:
            print(f"[批次 {batch_no}/{total_batches}] 提交 {len(batch)} 张发票...")

        data = {"commitType": args.commit_type, "list": batch,
                "apiKey": args.api_key}
        if args.skssq:
            data["skssq"] = args.skssq
        result = post_with_auto_login(
            "/api/jxplus/zxtSkill/check/commitDeduction", {"data": data},
            args.api_key)
        err = check_error(result)
        if err:
            print(err)
            return
        d = result.get("data", {})
        total_success += int(d.get("successCount", "0"))
        total_fail += int(d.get("failCount", "0"))
        all_success.extend(d.get("successList", []))
        all_fail.extend(d.get("failLIst", []))

    print(f"{action}完成：")
    skssq = d.get("skssq")
    if skssq:
        print(f"  税款所属期: {skssq}")
    print(f"  成功: {total_success} 张")
    print(f"  失败: {total_fail} 张")
    for inv in all_success:
        print(f"  [成功] {inv.get('invoiceCode', '')} {inv.get('invoiceNumber', '')} {inv.get('kprq', '')}")
    for inv in all_fail:
        print(f"  [失败] {inv.get('invoiceCode', '')} {inv.get('invoiceNumber', '')} "
              f"{inv.get('kprq', '')} - {inv.get('errorMsg', '')}")


def main():
    parser = argparse.ArgumentParser(description="发票认证技能")
    parser.add_argument("--api-key", default=os.environ.get("ZXT_API_KEY", ""),
                        help="apiKey，未传则读取环境变量 ZXT_API_KEY")
    sub = parser.add_subparsers(dest="action", required=True)

    p_login = sub.add_parser("login", help="税局登录")
    p_login.add_argument("--credit-code", required=True, help="纳税人识别号（税号）")
    p_login.add_argument("--account", default="", help="税局账号")
    p_login.add_argument("--password", default="", help="税局密码")
    p_login.add_argument("--area-code", default="", help="地区码（如 BJ、TJ）")

    p_sms_login = sub.add_parser("login-sms", help="验证码登录")
    p_sms_login.add_argument("--sms-code", required=True, help="短信验证码")
    p_sms_login.add_argument("--credit-code", required=True, help="纳税人识别号")
    p_sms_login.add_argument("--account", required=True, help="税局账号")

    p_send_sms = sub.add_parser("send-sms", help="发送验证码")
    p_send_sms.add_argument("--credit-code", required=True, help="纳税人识别号")
    p_send_sms.add_argument("--account", required=True, help="税局账号")

    sub.add_parser("sign", help="确认签名")

    sub.add_parser("current-period", help="获取当前税款所属期")

    p_stats = sub.add_parser("statistics", help="申请或撤销统计")
    p_stats.add_argument("--commit-type", required=True, choices=["1", "2"],
                         help="1 申请统计，2 撤销统计")
    p_stats.add_argument("--bz", required=True,
                         help="N 忽略未勾选发票直接统计，Y 取消未完成的统计状态")

    p_deduct = sub.add_parser("deduct-stats", help="查询抵扣统计数据")
    p_deduct.add_argument("--skssq", default="", help="税款所属期（选填）")

    p_checked = sub.add_parser("checked-invoices", help="查询当前属期认证发票集合")
    p_checked.add_argument("--skssq", default="", help="税款所属期（选填，支持查询历史认证记录）")

    p_check = sub.add_parser("check-status", help="查询发票认证状态")
    p_check.add_argument("--invoice-number", required=True, help="发票号码")
    p_check.add_argument("--invoice-date", required=True, help="开票日期 (YYYY-MM-DD)")
    p_check.add_argument("--invoice-code", default="", help="发票代码")

    p_commit = sub.add_parser("commit-deduction", help="提交或取消认证")
    p_commit.add_argument("--commit-type", required=True, choices=["1", "2"],
                          help="1 勾选认证，2 取消勾选认证")
    p_commit.add_argument("--invoices", required=True, nargs="+",
                          help="发票列表，格式：invoiceCode,kprq,invoiceNumber")
    p_commit.add_argument("--skssq", default="", help="税款所属期（选填）")

    args = parser.parse_args()
    if not args.api_key:
        print("[错误] 缺少 apiKey。您需要完成以下三步，即可自动配置并执行技能：")
        print("")
        print("1. 注册账号")
        print("   访问中兴通简税Skill平台：https://skill.quandianfapiao.com/ 完成注册。")
        print("")
        print("2. 申请 apiKey")
        print("   登录后进入'技能中心'，复制您的 apiKey。")
        print("")
        print("3. 提供 apiKey")
        print("   将复制的 apiKey 发送给我，我将为您完成配置并立即执行技能。")
        sys.exit(1)

    # 日期参数校验
    if args.action == "check-status":
        err = validate_date(args.invoice_date, "开票日期")
        if err:
            print(err)
            sys.exit(1)

    handlers = {
        "login": cmd_login,
        "login-sms": cmd_login_sms,
        "send-sms": cmd_send_sms,
        "current-period": cmd_current_period,
        "sign": cmd_sign,
        "statistics": cmd_statistics,
        "deduct-stats": cmd_deduct_stats,
        "checked-invoices": cmd_checked_invoices,
        "check-status": cmd_check_status,
        "commit-deduction": cmd_commit_deduction,
    }
    handlers[args.action](args)


if __name__ == "__main__":
    main()
