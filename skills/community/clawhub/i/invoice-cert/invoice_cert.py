#!/usr/bin/env python3
"""发票认证技能 - 税局扫码登录、发票勾选认证、抵扣统计"""

import argparse
import io
import json
import os
import sys
import tempfile

try:
    from common import post, validate_date
except ImportError:
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    from common import post, validate_date

try:
    import qrcode
except ImportError:  # 未安装时降级为输出纯链接
    qrcode = None

QR_LOGIN_PATH = "/api/jxplus/zxtSkill/login/getLoginQrUrl"
ORG_INFO_PATH = "/api/jxplus/zxtSkill/dzsj/getLoginOrgInfo"

GUIDANCE_HEAD = "税局登录已失效，请扫码登录。"
GUIDANCE_FOOTER = (
    "\n为保护账号安全，本技能改用扫码登录：您的税局密码不会经过对话窗口，\n"
    "也不会被 AI 模型采集或存储。登录全程在您手机端完成。\n\n"
    "扫码完成后告诉我，我会继续执行刚才的操作。"
)


# ---- 扫码登录 ----

def fetch_login_qr(api_key: str):
    """获取税局登录二维码地址，失败返回 None。"""
    result = post(QR_LOGIN_PATH, {"data": {"apiKey": api_key}})
    if str(result.get("status")) != "200":
        return None
    data = result.get("data") or {}
    return data.get("qrUrl") or None


def render_qr_ascii(url: str):
    """把 URL 渲染成终端可扫的二维码图案；qrcode 不可用时返回 None。"""
    if qrcode is None:
        return None
    qr = qrcode.QRCode(border=1)
    qr.add_data(url)
    qr.make(fit=True)
    buf = io.StringIO()
    qr.print_ascii(out=buf, invert=True)
    return buf.getvalue().rstrip("\n")


QR_CAPTION = [
    "发票认证技能 invoice-cert",
    "本二维码用于登录电局，完成进项发票认证与抵扣统计",
    "请使用微信扫码完成电局登录",
]

# 中文字体候选路径，按平台优先级排列
CJK_FONT_CANDIDATES = [
    r"C:\Windows\Fonts\msyh.ttc",       # Windows 微软雅黑
    r"C:\Windows\Fonts\simhei.ttf",     # Windows 黑体
    r"C:\Windows\Fonts\simsun.ttc",     # Windows 宋体
    "/System/Library/Fonts/PingFang.ttc",              # macOS
    "/System/Library/Fonts/STHeiti Medium.ttc",        # macOS
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    "/usr/share/fonts/truetype/arphic/uming.ttc",
]


def find_cjk_font():
    """探测系统中可用的中文字体路径；找不到返回 None。"""
    for path in CJK_FONT_CANDIDATES:
        if os.path.isfile(path):
            return path
    return None


def append_caption(img):
    """在二维码图片下方绘制说明文案（来源技能 + 用途 + 安全说明）。

    找不到中文字体或绘制失败时，原样返回二维码图片——
    终端输出里仍有完整文案，不影响登录流程。
    """
    font_path = find_cjk_font()
    if font_path is None:
        return img
    try:
        from PIL import Image as PilImage, ImageDraw, ImageFont

        font = ImageFont.truetype(font_path, 18)
        pad, gap = 18, 8
        line_h = 18 + gap

        probe = ImageDraw.Draw(img)
        text_w = int(max(probe.textlength(t, font=font) for t in QR_CAPTION))
        width = max(img.width, text_w + pad * 2)
        height = img.height + pad + line_h * len(QR_CAPTION) + pad

        canvas = PilImage.new("RGB", (width, height), "white")
        canvas.paste(img, ((width - img.width) // 2, 0))

        draw = ImageDraw.Draw(canvas)
        y = img.height + pad
        for text in QR_CAPTION:
            x = (width - draw.textlength(text, font=font)) / 2
            draw.text((x, y), text, font=font, fill="#333333")
            y += line_h
        return canvas
    except Exception:
        return img


def render_qr_image(url: str):
    """把二维码渲染成 PNG 写入系统临时目录，返回文件路径；不可用时返回 None。"""
    if qrcode is None:
        return None
    try:
        img = qrcode.make(url).convert("RGB")
        img = append_caption(img)
        path = os.path.join(tempfile.gettempdir(), "zxt_login_qr.png")
        img.save(path)
        return path
    except Exception:
        return None


def login_guidance(api_key: str) -> str:
    """组装扫码登录引导文案（含二维码与防 AI 采集密码的说明）。"""
    qr_url = fetch_login_qr(api_key)
    if not qr_url:
        return (f"{GUIDANCE_HEAD}\n\n"
                "[提示] 未能获取登录二维码，请稍后重试；"
                "若持续失败请确认 apiKey 是否具备该接口权限。\n"
                f"{GUIDANCE_FOOTER}")

    hint = "\n  请用微信扫码，或在浏览器中打开下方链接\n"
    body = None

    # 首选：生成图片文件，交由上层（AI）用自身的图片展示能力呈现给用户。
    # 脚本不主动弹窗——避免与对话内展示重复，也避免打扰用户桌面。
    img_path = render_qr_image(qr_url)
    if img_path:
        body = (f"\n二维码图片已生成：\n  {img_path}\n"
                f"{hint}  链接: {qr_url}\n")

    # 降级一：在终端渲染可扫图案
    if body is None:
        art = render_qr_ascii(qr_url)
        if art is not None:
            body = f"\n{art}\n{hint}  链接: {qr_url}\n"

    # 降级二：只输出链接
    if body is None:
        body = ("\n[提示] 未能生成二维码图片，也无法在终端渲染。\n"
                "请执行 pip install qrcode pillow 后重试，"
                "或手动将以下链接转为二维码后扫描：\n"
                f"{qr_url}\n")

    return f"{GUIDANCE_HEAD}\n{body}{GUIDANCE_FOOTER}"


def cmd_login_qr(args):
    print(login_guidance(args.api_key))


# ---- 当前登录企业 ----

def fetch_org_info(api_key: str):
    """获取当前登录企业信息，失败返回 None。"""
    result = post(ORG_INFO_PATH, {"data": {"apiKey": api_key}})
    if str(result.get("status")) != "200":
        return None
    return result.get("data") or None


def describe_org(api_key: str) -> str:
    """当前登录企业的可读描述（名称 + 税号）；取不到时返回空串。

    只在业务操作**成功后**调用。该接口不反映税局会话状态——会话失效时
    它仍可能返回 200 和企业名，若在操作前调用，会把企业名打进失败输出，
    让用户误以为操作已经发生。取不到不报错：企业信息仅用于标注操作对象，
    真正未登录的情况由业务接口的 309 分支统一处理。
    """
    info = fetch_org_info(api_key)
    if not info:
        return ""
    return f"{info.get('orgName') or '-'}（税号 {info.get('nsrsbh') or '-'}）"


def cmd_org_info(args):
    result = post(ORG_INFO_PATH, {"data": {"apiKey": args.api_key}})
    err = check_error(result, args.api_key)
    if err:
        print(err)
        return
    d = result.get("data") or {}
    print(f"当前登录企业：{d.get('orgName') or '-'}")
    print(f"  纳税人识别号: {d.get('nsrsbh') or '-'}")


def check_error(result: dict, api_key: str = ""):
    status = str(result.get("status", ""))
    if status == "200":
        return None
    if status == "309":
        return login_guidance(api_key)
    return f"[错误] {result.get('message', '未知错误')} (status={status})"


# ---- 子命令实现 ----

def cmd_current_period(args):
    result = post("/api/jxplus/zxtSkill/check/getCurrSkssq", {
        "data": {"apiKey": args.api_key}
    })
    err = check_error(result, args.api_key)
    if err:
        print(err)
        return
    org = describe_org(args.api_key)
    if org:
        print(f"当前登录企业: {org}")
    print(f"当前税款所属期: {result.get('data', '')}")


def cmd_sign(args):
    result = post("/api/jxplus/zxtSkill/check/doSignature", {
        "data": {"apiKey": args.api_key}
    })
    err = check_error(result, args.api_key)
    if err:
        print(err)
        return
    org = describe_org(args.api_key)
    if org:
        print(f"操作企业: {org}")
    print("确认签名成功")
    d = result.get("data")
    if d:
        print(json.dumps(d, ensure_ascii=False, indent=2))


def cmd_statistics(args):
    result = post("/api/jxplus/zxtSkill/check/commitStatistics", {
        "data": {"commitType": args.commit_type, "bz": args.bz,
                 "apiKey": args.api_key}
    })
    msg = str(result.get("message", ""))
    if "1001" in msg or "1002" in msg:
        print(f"提示：{msg}，正在自动重试（bz=Y）...")
        result = post("/api/jxplus/zxtSkill/check/commitStatistics", {
            "data": {"commitType": args.commit_type, "bz": "Y",
                     "apiKey": args.api_key}
        })
    err = check_error(result, args.api_key)
    if err:
        print(err)
        return
    action = "申请统计" if args.commit_type == "1" else "撤销统计"
    org = describe_org(args.api_key)
    if org:
        print(f"操作企业: {org}")
    print(f"{action}成功")
    d = result.get("data")
    if d:
        print(json.dumps(d, ensure_ascii=False, indent=2))


def cmd_deduct_stats(args):
    data = {"apiKey": args.api_key}
    if args.skssq:
        data["skssq"] = args.skssq
    result = post("/api/jxplus/zxtSkill/check/getDeductStatistList", {"data": data})
    err = check_error(result, args.api_key)
    if err:
        print(err)
        return
    org = describe_org(args.api_key)
    if org:
        print(f"当前登录企业: {org}")
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_checked_invoices(args):
    data = {"apiKey": args.api_key}
    if args.skssq:
        data["skssq"] = args.skssq
    result = post("/api/jxplus/zxtSkill/check/getCheckedInvoiceList", {"data": data})
    err = check_error(result, args.api_key)
    if err:
        print(err)
        return
    org = describe_org(args.api_key)
    if org:
        print(f"当前登录企业: {org}")
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
    data = {"invoiceNumber": args.invoice_number,
            "invoiceDate": args.invoice_date,
            "apiKey": args.api_key}
    if args.invoice_code:
        data["invoiceCode"] = args.invoice_code
    result = post("/api/jxplus/zxtSkill/check/getInvoiceCheckStatus", {"data": data})
    err = check_error(result, args.api_key)
    if err:
        print(err)
        return
    org = describe_org(args.api_key)
    d = result.get("data", {})
    gxzt = d.get("gxzt", "-")
    gxzt_name = "已勾选" if gxzt == "1" else "未勾选"
    print(f"发票认证状态：{gxzt_name} (gxzt={gxzt})")
    if org:
        print(f"  查询企业: {org}")
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
    print(f"正在操作: {action}，共 {len(invoice_list)} 张发票")

    total_success = 0
    total_fail = 0
    all_success = []
    all_fail = []
    skssq = None

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
        result = post("/api/jxplus/zxtSkill/check/commitDeduction", {"data": data})
        err = check_error(result, args.api_key)
        if err:
            # 中途失败时先汇报已完成的部分，避免丢失进度。
            # 只有确实提交成功过才标注企业，避免企业信息不可靠时误导用户。
            print(f"{action}中断于第 {batch_no}/{total_batches} 批：")
            if total_success > 0:
                org = describe_org(args.api_key)
                if org:
                    print(f"  操作企业: {org}")
            if skssq:
                print(f"  税款所属期: {skssq}")
            print(f"  已完成成功: {total_success} 张")
            print(f"  已完成失败: {total_fail} 张")
            print("")
            print(err)
            return
        d = result.get("data", {})
        skssq = d.get("skssq") or skssq
        total_success += int(d.get("successCount", "0"))
        total_fail += int(d.get("failCount", "0"))
        all_success.extend(d.get("successList", []))
        all_fail.extend(d.get("failLIst", []))

    org = describe_org(args.api_key)
    if org:
        print(f"{action}完成 —— 发票已操作至企业: {org}")
    else:
        print(f"{action}完成：")
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

    sub.add_parser("login-qr", help="获取税局扫码登录二维码")

    sub.add_parser("org-info", help="查询当前登录企业信息")

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
        "login-qr": cmd_login_qr,
        "org-info": cmd_org_info,
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
