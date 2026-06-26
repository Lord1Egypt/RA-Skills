#!/usr/bin/env python3
"""
翔云发票识别与查验脚本
功能：识别发票图片/PDF → 联网查验真伪 → 导出标准 Excel 模版

使用方法：
  # 仅识别
  python invoice.py --image <路径>

  # 识别 + 查验
  python invoice.py --image <路径> --verify

  # 识别 + 查验 + 导出 Excel（自动匹配模版）
  python invoice.py --image <路径> --verify --export

  # 批量目录
  python invoice.py --dir <目录> --verify --export

  # 指定模版：deduction / transport / goods / ledger / booking
  python invoice.py --dir <目录> --verify --export --template ledger

凭据加载顺序：config.json > 环境变量 NETOCR_KEY/NETOCR_SECRET > 命令行 --key/--secret
"""

import argparse
import base64
import json
import os
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("缺少依赖，请先执行：pip install requests openpyxl")
    sys.exit(1)

# ──────────────────────────────────────────────
# 常量
# ──────────────────────────────────────────────
API_RECOGNIZE = "https://netocr.com/api/v2/recogInvoiveBase64.do"
API_VERIFY    = "https://netocr.com/verapi/v2/verInvoice.do"

SUPPORTED_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff",
                  ".pdf", ".ofd", ".webp"}

# 需要 Pillow 预转换的格式
CONVERT_TO_JPG_EXTS = {".tif", ".tiff", ".webp"}

# 发票类型代码 → 可读名称（全部 46 种）
INVOICE_TYPE_MAP = {
    # ── 可查验 ──────────────────────────────────────────────
    "01": "增值税专用发票",
    "1":  "增值税专用发票",
    "03": "机动车销售统一发票",
    "3":  "机动车销售统一发票",
    "04": "增值税普通发票",
    "4":  "增值税普通发票",
    "08": "增值税专用发票(电子)",
    "8":  "增值税专用发票(电子)",
    "09": "数电发票(增值税专用发票)",
    "9":  "数电发票(增值税专用发票)",
    "10": "增值税电子普通发票",
    "11": "增值税普通发票(卷票)",
    "14": "通行费增值税电子普通发票",
    "15": "二手车销售统一发票",
    "61": "数电发票(航空运输电子客票行程单)",
    "62": "数电发票(铁路电子客票)",
    "63": "电子发票(机动车销售统一发票)",
    "64": "数电发票(二手车销售统一发票)",
    "72": "电子发票（普通发票）通行费",
    "83": "数电发票(普通发票)",
    "91": "数电纸质发票(增值税专用发票)",
    "92": "数电纸票发票(普通发票)",
    "93": "数电纸质发票(机动车销售统一发票)",
    "94": "数电纸票发票(二手车销售统一发票)",
    # ── 可识别（不支持查验）────────────────────────────────
    "20": "火车票",
    "21": "区块链发票",
    "22": "船票",
    "23": "定额发票",
    "24": "机打发票",
    "25": "出租车发票",
    "26": "客运汽车",
    "27": "航空运输电子客票行程单",
    "28": "过路费",
    "31": "打车行程单",
    "33": "货物清单",
    "34": "财政电子票据",
    "35": "海关缴款书",
    "36": "通用电子发票",
    "37": "完税证明",
    "38": "医疗票据",
    "39": "退票费报销凭证",
    "40": "非税收入一般缴款书(电子)",
    "41": "车辆通行费通用(电子)发票",
    "42": "银行回单",
}

# ── 可查验发票类型全集 ──────────────────────────────────────────────
# 可查验：01/03/04/08/09/10/11/14/15/61/62/63/64/72/83/91/92/93/94
VERIFY_ALL_TYPES = {
    "1", "3", "4", "8", "9", "10", "11", "14", "15",
    "61", "62", "63", "64", "72", "83",
    "91", "92", "93", "94",
}

# 查验入参 totalAmount 取 amountTax（价税合计）
VERIFY_AMOUNT_TAX_TYPES   = {"9", "61", "62", "63", "64", "72", "83"}

# 查验入参 totalAmount 取 totalAmount（不含税金额）
VERIFY_AMOUNT_TOTAL_TYPES = {"1", "3", "4", "8", "10", "11", "14", "15", "91", "92", "93", "94"}

# 查验入参 checkCode 取 fullInvoiceNumber（数电纸质普票/机动车）
VERIFY_CHECKCODE_FULLINV_TYPES = {"92", "93"}

# 各模版适用的发票类型集合（去除前导零后匹配）
TEMPLATE_INVOICE_TYPES = {
    # 勾选抵扣表：可抵扣进项的专票/机动车/通行费/航空铁路
    "deduction": {"1","3","8","9","14","91","93","61","62","72"},
    # 旅客运输抵扣表：航空/铁路/普票通行费
    "transport": {"10","20","22","26","27","61","62","83","92"},
    # 货物明细表：专票/普票/通行费/数电全类型
    "goods":     {"1","4","8","9","10","14","11","21","83","91","92","72","63","64","3","15"},
    # 台账表：覆盖最广
    "ledger":    {"1","4","8","9","10","14","11","3","15","21","83","91","92","72","61","62","63","64"},
    # 入账表
    "booking":   {"1","3","4","8","9","10","15","61","62","83","91","92","14","72","63","64","11"},
}

# ──────────────────────────────────────────────
# 模板元数据（名称 + 描述，用于交互选择）
# ──────────────────────────────────────────────
TEMPLATE_META = {
    "deduction": "增值税发票勾选抵扣表（抵扣进项税额）",
    "transport": "国内旅客运输服务抵扣表（航空/铁路/客车）",
    "goods":     "增值税发票货物明细表（商品明细记录）",
    "ledger":    "增值税发票台账表（最全字段，覆盖广）",
    "booking":   "发票入账表（财务记账用）",
}

# ──────────────────────────────────────────────
# 交互式模板选择（纯 CLI 版本，无 agent 依赖）
# 当由 Agent 调用时，建议先通过 ask_followup_question 让用户点选，
# 再将结果通过 --template 参数传入，脚本本身不弹 UI。
# ──────────────────────────────────────────────
def prompt_template_selection(pre_selected=None):
    """
    CLI 交互选择（数字/范围输入），纯脚本兜底用。
    在 WorkBuddy 环境下推荐由 Agent 调用 ask_followup_question 后传入 --template。
    """
    pre_set = set(pre_selected) if pre_selected else set()
    items = list(TEMPLATE_META.items())

    print("\n" + "=" * 60)
    print("  请选择要导出的 Excel 模版（可多选，用逗号分隔，如：1,3,5）")
    print("  或输入 all 导出全部，q 退出")
    print("=" * 60)
    for i, (key, desc) in enumerate(items, start=1):
        marker = " ★" if key in pre_set else ""
        print(f"  [{i}] {key:10s}  —  {desc}{marker}")
    print()

    while True:
        try:
            raw = input("  请输入编号: ").strip().lower()
            if raw == "q":
                print("  已取消导出。")
                return []
            if raw == "all":
                return [k for k, _ in items]

            selected = []
            parts = raw.replace(" ", "").split(",")
            for part in parts:
                part = part.strip()
                if not part:
                    continue
                if "-" in part:
                    start_end = part.split("-")
                    if len(start_end) == 2:
                        try:
                            s, e = int(start_end[0]), int(start_end[1])
                            selected.extend(range(s, e + 1))
                        except ValueError:
                            pass
                else:
                    try:
                        selected.append(int(part))
                    except ValueError:
                        pass

            seen = set()
            result = []
            for idx in selected:
                if 1 <= idx <= len(items) and idx not in seen:
                    seen.add(idx)
                    result.append(items[idx - 1][0])

            if result:
                print(f"  已选择: {', '.join(result)}")
                return result
            else:
                print("  无效输入，请重新输入。")
        except (EOFError, KeyboardInterrupt):
            print("\n  已取消。")
            return []


# ──────────────────────────────────────────────
# 凭据管理
# ──────────────────────────────────────────────
def get_config_path():
    return Path(__file__).parent.parent / "config.json"

def load_credentials(cli_key="", cli_secret=""):
    """加载凭据：config.json > 环境变量 > 命令行参数"""
    config_path = get_config_path()

    # 1. 配置文件
    if config_path.exists():
        try:
            with open(config_path, encoding="utf-8") as f:
                cfg = json.load(f)
            key    = cfg.get("key", "").strip()
            secret = cfg.get("secret", "").strip()
            if key and secret:
                return key, secret
        except Exception:
            pass

    # 2. 环境变量
    key    = os.environ.get("NETOCR_KEY", "").strip()
    secret = os.environ.get("NETOCR_SECRET", "").strip()
    if key and secret:
        return key, secret

    # 3. 命令行参数
    if cli_key and cli_secret:
        return cli_key.strip(), cli_secret.strip()

    return "", ""

def save_credentials(key, secret):
    config_path = get_config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump({"key": key, "secret": secret}, f, ensure_ascii=False, indent=2)
    print(f"  [CONFIG] 凭据已保存至：{config_path}")

def prompt_credentials():
    """引导用户输入凭据并持久化"""
    print("\n" + "="*60)
    print("  首次使用，需要配置翔云 OCR 凭据")
    print("  获取地址：https://netocr.com → 个人中心 → 查看 key/secret")
    print("="*60)
    key    = input("  请输入 ocrKey  : ").strip()
    secret = input("  请输入 ocrSecret: ").strip()
    if not key or not secret:
        print("[ERROR] key 和 secret 不能为空")
        sys.exit(1)
    save_credentials(key, secret)
    return key, secret

def check_credentials(key, secret):
    """
    批量处理前先用一个轻量请求验证 key/secret 是否有效。
    返回 True 表示可用，False 表示无效（已打印提示）。
    """
    print("\n  [CHECK] 正在验证 key/secret 可用性...")
    try:
        payload = {
            "key":    key,
            "secret": secret,
            "typeId": "20090",
            "img":    "",  # 空图片，接口会返回错误但能验证认证
            "format": "json",
        }
        resp = requests.post(API_RECOGNIZE, data=payload, timeout=30)
        result = resp.json()

        # 检测认证错误
        is_auth_err, hint = _is_auth_error(result, "识别接口")
        if is_auth_err:
            print(hint)
            return False

        # status=4 表示缺少图片内容，但认证通过
        status = str(result.get("status", ""))
        if status == "4":
            print("  [OK] key/secret 验证通过")
            return True

        # 其他 status 暂且放过，让后续实际识别报错更详细
        print(f"  [OK] key/secret 验证通过（接口返回 status={status}）")
        return True
    except Exception as e:
        # 网络错误暂且放过，避免误拦
        print(f"  [WARN] 验证请求异常: {e}，继续尝试识别...")
        return True

# ──────────────────────────────────────────────
# 格式转换：TIF/WEBP → JPG
# ──────────────────────────────────────────────
def convert_to_jpg(image_path):
    path = Path(image_path)
    if path.suffix.lower() not in CONVERT_TO_JPG_EXTS:
        return str(path), False
    try:
        from PIL import Image as _PILImage
    except ImportError:
        print("  [WARN] Pillow 未安装，无法转换格式，请执行：pip install Pillow")
        return None, False

    tmp_path = path.with_suffix(".___tmp_inv.jpg")
    try:
        img = _PILImage.open(str(path))
        if hasattr(img, "n_frames") and img.n_frames > 1:
            img.seek(0)
        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")
        img.save(str(tmp_path), "JPEG", quality=95)
        print(f"  [CONV] {path.suffix.upper()} -> JPG")
        return str(tmp_path), True
    except Exception as e:
        print(f"  [WARN] 格式转换失败: {e}")
        return None, False

# ──────────────────────────────────────────────
# 图片转 Base64
# ──────────────────────────────────────────────
def image_to_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# ──────────────────────────────────────────────
# 发票识别
# ──────────────────────────────────────────────
def _is_auth_error(result, context="接口"):
    """
    检测 API 返回是否表示 key 或 secret 错误（认证失败）。
    返回 (是认证错误, 友好提示文本)。
    """
    if not result:
        return False, ""

    # 取状态码和消息
    status = str(result.get("status", "") if isinstance(result, dict) else "")
    code   = str(result.get("code", "")   if isinstance(result, dict) else "")
    # 递归搜索 message/msg 字段
    msg = ""
    def _find_msg(d):
        if isinstance(d, dict):
            for k in ("message", "msg", "error", "error_msg"):
                if k in d:
                    return str(d[k])
            for v in d.values():
                r = _find_msg(v)
                if r:
                    return r
        elif isinstance(d, list):
            for item in d:
                r = _find_msg(item)
                if r:
                    return r
        return ""

    msg = _find_msg(result)
    msg_lower = msg.lower()

    # 认证失败的典型关键词
    auth_keywords = [
        "key", "secret", "密钥", "key错误", "secret错误",
        "密钥错误", "认证", "auth", "unauthorized", "401",
        "apikey", "api key", "api_secret", "api secret",
        "incorrect", "invalid", "权限", "签名",
    ]
    is_auth = any(kw in msg_lower for kw in auth_keywords) or \
              code in ("-1", "-2", "-3", "-4", "-5", "-6", "-99")

    if is_auth and msg:
        hint = (
            f"\n"
            f"  ╔══════════════════════════════════════════════════════╗\n"
            f"  ║  ⚠️  认证失败：{context}返回 key 或 secret 错误               ║\n"
            f"  ║                                                      ║\n"
            f"  ║  请检查以下内容：                                      ║\n"
            f"  ║    1. key/secret 是否填写正确（注意无多余空格）        ║\n"
            f"  ║    2. key/secret 是否已过期或被禁用                   ║\n"
            f"  ║    3. 套餐额度是否用尽                                 ║\n"
            f"  ║                                                      ║\n"
            f"  ║  获取地址：https://netocr.com → 个人中心 → 查看 key   ║\n"
            f"  ╚══════════════════════════════════════════════════════╝\n"
        )
        return True, hint
    elif is_auth and not msg:
        hint = (
            f"\n"
            f"  ⚠️  {context}认证失败（key 或 secret 错误），请检查凭据是否正确。\n"
            f"  获取地址：https://netocr.com → 个人中心 → 查看 key/secret\n"
        )
        return True, hint

    return False, ""


def recognize_invoice(image_path, key, secret):
    """
    调用翔云发票识别接口（typeId=20090）。
    返回完整 JSON 响应 dict，失败时返回 None。
    """
    actual_path, is_temp = convert_to_jpg(image_path)
    if actual_path is None:
        return None

    try:
        img_b64 = image_to_base64(actual_path)
        payload = {
            "img":    img_b64,
            "key":    key,
            "secret": secret,
            "typeId": "20090",
            "format": "json",
        }
        resp = requests.post(API_RECOGNIZE, data=payload, timeout=60)
        resp.raise_for_status()
        result = resp.json()

        # 检测 key/secret 错误
        is_auth_err, hint = _is_auth_error(result, "识别接口")
        if is_auth_err:
            print(hint)
            return None

        return result
    except Exception as e:
        print(f"  [ERROR] 识别请求失败: {e}")
        return None
    finally:
        if is_temp:
            try:
                Path(actual_path).unlink()
            except Exception:
                pass

# ──────────────────────────────────────────────
# 解析识别结果，提取核心字段
# ──────────────────────────────────────────────
def parse_recognize_result(result):
    """
    解析识别接口返回，提取查验所需字段和基础信息。
    返回 dict（字段缺失时为空字符串）。
    """
    if not result:
        return {}

    # 顶层可能是 list（一图多票），取第一张
    data = result
    if isinstance(data, list):
        data = data[0] if data else {}

    # 各票种字段层级不同，尽量兼容
    fields = {}
    for key in ("invoiceCode", "invoiceNumber", "billingDate", "totalAmount",
                "checkCode", "salesTaxNo", "invoiceType", "orderNo",
                "purchaserName", "purchaserTaxNo", "salesName",
                "totalTax", "amountTax", "amountTaxCN",
                "purchaserAddressPhone", "purchaserBank",
                "salesAddressPhone", "salesBankAndNo",
                "invoiceLists", "remarks",
                # 机动车/二手车专属
                "idCardNo", "vehicleType", "brandModel", "engineNo",
                "vehicleNo", "paymentVoucherNo", "carNumber",
                "auctionName", "auctionTaxNo",
                "usedCarName", "usedCarTaxNo",
                # 92/93/94 数电纸质票专属：fullInvoiceNumber = 发票代码+号码（20位）
                "fullInvoiceNumber",
                # 航空/铁路/船票
                "NAME", "name", "billingDate"):
        fields[key] = _get_field(data, key)

    # 将 invoiceType 数字转为中文名，保留原始数字到 invoiceTypeCode
    raw_type = fields.get("invoiceType", "")
    fields["invoiceTypeCode"] = raw_type
    fields["invoiceType"] = INVOICE_TYPE_MAP.get(
        str(raw_type).lstrip("0"), raw_type
    )

    return fields

def _get_field(data, key, default=""):
    """递归在 dict 中查找字段（兼容翔云多层嵌套返回）"""
    if isinstance(data, dict):
        if key in data:
            return data[key] or default
        for v in data.values():
            result = _get_field(v, key, default)
            if result != default:
                return result
    elif isinstance(data, list):
        for item in data:
            result = _get_field(item, key, default)
            if result != default:
                return result
    return default

# ──────────────────────────────────────────────
# 发票查验
# ──────────────────────────────────────────────
def verify_invoice(fields, key, secret):
    """
    根据识别结果字段调用查验接口（typeId=3007）。
    返回查验 JSON 响应 dict，失败时返回 None。

    入参规则（按发票类型代码）：
      totalAmount 取 amountTax（价税合计）：9, 61, 62, 63, 64, 72, 83
      totalAmount 取 totalAmount（不含税）：1, 3, 4, 8, 10, 11, 14, 15, 91, 92, 93, 94
      checkCode 取 fullInvoiceNumber：92, 93（数电纸质普票/机动车）
    """
    # 取原始类型代码（invoiceTypeCode），无则从 invoiceType 中推断
    type_code = str(fields.get("invoiceTypeCode", "")).strip().lstrip("0") or \
                str(fields.get("invoiceType", "")).strip().lstrip("0")

    if type_code in VERIFY_AMOUNT_TAX_TYPES:
        total_amount_val = fields.get("amountTax", "")
        _verify_amount_field = "amountTax（价税合计）"
    else:
        total_amount_val = fields.get("totalAmount", "")
        _verify_amount_field = "totalAmount（不含税金额）"

    print(f"  [VERIFY] 查验入参 totalAmount 取 {_verify_amount_field} = {total_amount_val}")

    payload = {
        "key":           key,
        "secret":        secret,
        "typeId":        "3007",
        "invoiceNumber": fields.get("invoiceNumber", ""),
        "totalAmount":   total_amount_val,
    }
    # checkCode 取值：92/93 类型用 fullInvoiceNumber，其余用 checkCode 字段
    if type_code in VERIFY_CHECKCODE_FULLINV_TYPES:
        check_code_val = fields.get("fullInvoiceNumber", "")
        if check_code_val:
            payload["checkCode"] = check_code_val
            print(f"  [VERIFY] 查验入参 checkCode 取 fullInvoiceNumber = {check_code_val}")
    # 按需填充其他可选字段
    for opt in ("invoiceCode", "billingDate", "checkCode", "salesTaxNo", "orderNo"):
        if opt == "checkCode" and type_code in VERIFY_CHECKCODE_FULLINV_TYPES:
            continue  # 已由上面处理
        val = fields.get(opt, "")
        if val:
            payload[opt] = val

    try:
        resp = requests.post(API_VERIFY, data=payload, timeout=60)
        resp.raise_for_status()
        result = resp.json()

        # 检测 key/secret 错误
        is_auth_err, hint = _is_auth_error(result, "查验接口")
        if is_auth_err:
            print(hint)
            return None

        return result
    except Exception as e:
        print(f"  [ERROR] 查验请求失败: {e}")
        return None

# ──────────────────────────────────────────────
# 解析查验结果（合并识别字段）
# ──────────────────────────────────────────────
def parse_verify_result(verify_result, recog_fields):
    """
    查验成功时用查验结果覆盖/补全识别字段（查验结果更权威）。
    返回合并后的 dict。
    """
    merged = dict(recog_fields)
    if not verify_result:
        return merged

    data = verify_result
    if isinstance(data, list):
        data = data[0] if data else {}

    # 取查验接口常见顶层字段
    for k in ("invoiceType", "invoiceCode", "invoiceNumber", "billingDate",
              "totalAmount", "totalTax", "amountTax", "amountTaxCN",
              "checkCode", "state", "checkNum",
              "purchaserName", "purchaserTaxNo", "purchaserBank", "purchaserAddressPhone",
              "salesName", "salesTaxNo", "salesAddressPhone", "salesBank", "salesBankAndNo",
              "drawerName", "receiverName", "recheckName", "remarks",
              "invoiceLists",
              "manageState", "dataSource", "varianceDeductionFlag", "uses",
              "isCheck", "proportion", "deductionTax",
              "NAME", "name", "amountTax", "proportion", "deductionTax",
              "SERIAL", "voucherType", "fullInvoiceNumber", "ccpNumber",
              "wtcNumber", "salesTaxNo", "purpose", "postingDate",
              "idCardNo", "vehicleType", "brandModel", "engineNo",
              "vehicleNo", "paymentVoucherNo", "carNumber",
              "auctionName", "auctionTaxNo", "usedCarName", "usedCarTaxNo"):
        val = _get_field(data, k)
        if val:
            merged[k] = val

    # 查验结果的 invoiceType 同样转中文
    raw_type = merged.get("invoiceType", "")
    # 若已是中文（从识别结果继承过来），不重复转换
    if raw_type and raw_type not in INVOICE_TYPE_MAP.values():
        merged["invoiceTypeCode"] = raw_type
        merged["invoiceType"] = INVOICE_TYPE_MAP.get(
            str(raw_type).lstrip("0"), raw_type
        )

    return merged

# ──────────────────────────────────────────────
# 自动匹配模版
# ──────────────────────────────────────────────
def auto_select_template(invoice_type):
    """根据 invoiceType 自动选取最合适的模版（优先级：deduction > transport > goods > ledger > booking）"""
    # 去除前导零
    t = str(invoice_type).lstrip("0") or "0"
    priority = ["deduction", "transport", "goods", "ledger", "booking"]
    for tmpl in priority:
        if t in TEMPLATE_INVOICE_TYPES[tmpl]:
            return tmpl
    return "ledger"  # 兜底

# ──────────────────────────────────────────────
# 打印识别/查验结果摘要
# ──────────────────────────────────────────────
def print_summary(fields, verified=False):
    itype_name = fields.get("invoiceType", "")     # 已是中文
    itype_code = fields.get("invoiceTypeCode", "") # 原始数字
    state_map = {"1": "正常", "2": "作废", "3": "红冲", "7": "部分红冲", "8": "全额红冲"}
    state = state_map.get(str(fields.get("state", "")), fields.get("state", ""))

    code_hint = f"（{itype_code}）" if itype_code else ""
    print(f"   发票类型  : {itype_name}{code_hint}")
    print(f"   发票代码  : {fields.get('invoiceCode','')}")
    print(f"   发票号码  : {fields.get('invoiceNumber','')}")
    print(f"   开票日期  : {fields.get('billingDate','')}")
    print(f"   合计金额  : {fields.get('totalAmount','')}")
    print(f"   合计税额  : {fields.get('totalTax','')}")
    print(f"   价税合计  : {fields.get('amountTax','')}")
    print(f"   销方名称  : {fields.get('salesName','')}")
    print(f"   销方税号  : {fields.get('salesTaxNo','')}")
    print(f"   购方名称  : {fields.get('purchaserName','')}")
    if verified:
        print(f"   查验状态  : {state}（查验次数：{fields.get('checkNum','')}）")

# ──────────────────────────────────────────────
# 处理单张发票
# ──────────────────────────────────────────────
def process_single(image_path, key, secret, do_verify=False,
                   do_export=False, template=None, output_dir=None):
    image_path = Path(image_path)
    print(f"\n[FILE] {image_path.name}")

    # 1. 识别
    recog_result = recognize_invoice(str(image_path), key, secret)
    if recog_result is None:
        print("  [FAIL] 识别失败")
        return False

    # 保存原始 JSON
    json_path = image_path.with_suffix(".invoice_result.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(recog_result, f, ensure_ascii=False, indent=2)
    print(f"  [SAVE] JSON 已保存：{json_path.name}")

    recog_fields = parse_recognize_result(recog_result)

    # 检查识别状态
    status = _get_field(recog_result, "status")
    if str(status) != "0" and str(status) != "":
        msg = _get_field(recog_result, "message") or _get_field(recog_result, "msg")
        print(f"  [FAIL] 识别返回异常 status={status} message={msg}")
        return False

    print(f"\n[OK] 识别成功")
    print_summary(recog_fields, verified=False)

    fields = recog_fields

    # 2. 查验
    if do_verify:
        inv_type_code = str(recog_fields.get("invoiceTypeCode", "")).strip().lstrip("0") or \
                        str(recog_fields.get("invoiceType", "")).strip().lstrip("0")
        if inv_type_code not in VERIFY_ALL_TYPES:
            print(f"\n  [SKIP] 票种 {inv_type_code}（{recog_fields.get('invoiceType', '')}）不支持查验，跳过")
        else:
            print(f"\n  [VERIFY] 正在查验...")
            verify_result = verify_invoice(recog_fields, key, secret)
            if verify_result is None:
                print("  [WARN] 查验请求失败，跳过查验")
            else:
                # 翔云查验接口返回 {"code":0,"msg":"成功","data":{...}}
                # 兼容旧版 status==0 格式
                v_code   = verify_result.get("code")
                v_status = _get_field(verify_result, "status")
                v_msg    = verify_result.get("msg") or _get_field(verify_result, "message") or _get_field(verify_result, "msg")
                is_success = (v_code == 0) or (str(v_status) == "0")

                # 无论成功与否，都保存查验原始 JSON
                verify_json_path = image_path.with_suffix(".verify_result.json")
                with open(verify_json_path, "w", encoding="utf-8") as f_vj:
                    json.dump(verify_result, f_vj, ensure_ascii=False, indent=2)
                print(f"  [SAVE] 查验 JSON 已保存：{verify_json_path.name}")

                if is_success:
                    # 将 data 子层展开，方便 parse_verify_result 读取
                    verify_data = verify_result.get("data") or verify_result
                    fields = parse_verify_result(verify_data, recog_fields)
                    print(f"  [OK] 查验成功（{v_msg}）")
                    print_summary(fields, verified=True)
                else:
                    print(f"  [WARN] 查验返回异常 code={v_code!r} msg={v_msg!r}")

    # 3. 导出（严格按适用票种过滤）
    if do_export:
        from export_invoice import export_to_excel
        invoice_type = fields.get("invoiceType", "")
        type_code = str(fields.get("invoiceTypeCode", "")).lstrip("0") or invoice_type.lstrip("0")

        if isinstance(template, list):
            selected = template
        elif template:
            selected = [template]
        else:
            selected = [auto_select_template(invoice_type)]

        out_dir = Path(output_dir) if output_dir else image_path.parent
        for tmpl in selected:
            # 严格过滤：只有该票种在模板适用范围内才导出
            if type_code not in TEMPLATE_INVOICE_TYPES.get(tmpl, set()):
                print(f"  [SKIP] {tmpl.upper()} 不适用于票种 {type_code}，跳过")
                continue
            out_path = out_dir / f"{image_path.stem}_{tmpl}.xlsx"
            ok, msg = export_to_excel([fields], tmpl, str(out_path))
            if ok:
                print(f"  [EXPORT] {tmpl.upper()} -> {out_path.name}")
            else:
                print(f"  [FAIL] 导出失败({tmpl}): {msg}")

    return True

# ──────────────────────────────────────────────
# 批量处理目录
# ──────────────────────────────────────────────
def process_directory(dir_path, key, secret, do_verify=False,
                      do_export=False, template=None, output_dir=None,
                      reuse=False):
    dir_path = Path(dir_path)

    if reuse:
        # ── 复用模式：只扫描已有的 JSON 文件 ─────────────────────────
        image_files = sorted([
            f for f in dir_path.iterdir()
            if f.is_file() and f.suffix.lower() in SUPPORTED_EXTS
            and "___tmp_inv" not in f.name
        ])
        if not image_files:
            print(f"[WARN] 目录中没有找到支持的图片文件：{dir_path}")
            return

        print(f"\n[REUSE] 复用模式：{dir_path}")
        all_fields = []
        for img in image_files:
            verify_json = img.with_suffix(".verify_result.json")
            json_path   = img.with_suffix(".invoice_result.json")
            if verify_json.exists():
                with open(verify_json, encoding="utf-8") as jf:
                    vjr = json.load(jf)
                recog_jr = {}
                if json_path.exists():
                    with open(json_path, encoding="utf-8") as jf2:
                        recog_jr = json.load(jf2)
                recog_f = parse_recognize_result(recog_jr)
                f = parse_verify_result(vjr, recog_f)
                print(f"  [JSON] {img.stem} → 使用查验结果")
            elif json_path.exists():
                with open(json_path, encoding="utf-8") as jf:
                    jr = json.load(jf)
                f = parse_recognize_result(jr)
                print(f"  [JSON] {img.stem} → 使用识别结果")
            else:
                print(f"  [SKIP] {img.stem} → 无 JSON 结果，跳过")
                continue
            all_fields.append((img.stem, f))

        if not all_fields:
            print("[WARN] 没有找到任何有效的 JSON 结果文件")
            return

        print(f"   共加载 {len(all_fields)} 个结果\n")

    else:
        # ── 正常模式：调用 API 识别/查验 ───────────────────────────
        files = sorted([
            f for f in dir_path.iterdir()
            if f.is_file() and f.suffix.lower() in SUPPORTED_EXTS
            and "___tmp_inv" not in f.name
            and ".invoice_result" not in f.name
        ])
        if not files:
            print(f"[WARN] 目录中没有找到支持的文件：{dir_path}")
            return

        # 批量处理前先验证 key/secret 是否可用
        if not check_credentials(key, secret):
            print("[FAIL] key/secret 无效，请检查后重试。")
            return

        print(f"\n[DIR] {dir_path}")
        print(f"   共找到 {len(files)} 个文件\n")

        success, failed = 0, 0
        all_fields = []  # 用于批量导出

        for img in files:
            try:
                ok = process_single(str(img), key, secret,
                                    do_verify=do_verify,
                                    do_export=False,   # 批量时统一导出
                                    template=template,
                                    output_dir=output_dir)
                if ok:
                    success += 1
                    # 优先读 verify_result.json（查验成功），否则用 invoice_result.json
                    verify_json = img.with_suffix(".verify_result.json")
                    json_path   = img.with_suffix(".invoice_result.json")
                    if verify_json.exists():
                        with open(verify_json, encoding="utf-8") as jf:
                            vjr = json.load(jf)
                        recog_jr = {}
                        if json_path.exists():
                            with open(json_path, encoding="utf-8") as jf2:
                                recog_jr = json.load(jf2)
                        recog_f = parse_recognize_result(recog_jr)
                        f = parse_verify_result(vjr, recog_f)
                    elif json_path.exists():
                        with open(json_path, encoding="utf-8") as jf:
                            jr = json.load(jf)
                        f = parse_recognize_result(jr)
                    else:
                        f = {}
                    all_fields.append((img.stem, f))
                else:
                    failed += 1
            except Exception as e:
                print(f"  [ERROR] 处理异常: {e}")
                failed += 1

        print(f"\n[DONE] Success: {success}, Failed: {failed}")

    # 批量导出：按模版分组写入同一个 Excel
    if do_export and all_fields:
        from export_invoice import export_to_excel
        from collections import defaultdict

        # 统一为列表形式
        if isinstance(template, list):
            selected_templates = template
        elif template:
            selected_templates = [template]
        else:
            selected_templates = None  # 待交互选择

        # 若未指定模板，进入交互选择（批量模式也需要知道导哪些）
        if selected_templates is None:
            selected_templates = prompt_template_selection()
            if not selected_templates:
                return  # 用户取消

        groups = defaultdict(list)
        for stem, f in all_fields:
            itype = f.get("invoiceType", "")
            # 取原始票种数字代码（如 "92"），用于查 TEMPLATE_INVOICE_TYPES
            type_code = str(f.get("invoiceTypeCode", "")).lstrip("0") or itype.lstrip("0")
            auto_tmpl = auto_select_template(itype)

            if selected_templates:
                # 用户已指定模板 → 严格过滤：只保留该票种适用的
                for tmpl in selected_templates:
                    if type_code in TEMPLATE_INVOICE_TYPES.get(tmpl, set()):
                        groups[tmpl].append(f)
            else:
                # 用户未指定 → 只用自动匹配的
                groups[auto_tmpl].append(f)

        out_dir = Path(output_dir) if output_dir else dir_path
        # 遍历所有选中的模板，无数据也生成空文件（仅标题+表头）
        all_templates = set(selected_templates) if selected_templates else set(groups.keys())
        for tmpl in sorted(all_templates):
            rows = groups.get(tmpl, [])
            out_path = out_dir / f"批量导出_{tmpl}.xlsx"
            ok, msg = export_to_excel(rows, tmpl, str(out_path))
            if ok:
                print(f"  [EXPORT] {tmpl.upper()} ({len(rows)}张) -> {out_path.name}")
            else:
                print(f"  [FAIL] {tmpl} 导出失败: {msg}")

# ──────────────────────────────────────────────
# 主入口
# ──────────────────────────────────────────────
def _parse_templates(raw):
    """将逗号分隔的模板名解析为列表，无效项自动过滤"""
    if not raw:
        return None
    valid = set(TEMPLATE_META.keys())
    result = []
    for t in raw.replace(" ", "").split(","):
        if t in valid:
            result.append(t)
    return result if result else None


def main():
    parser = argparse.ArgumentParser(
        description="翔云发票识别与查验工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--image",    help="单张发票路径")
    parser.add_argument("--dir",      help="批量处理的目录路径")
    parser.add_argument("--key",      default="", help="ocrKey（可省略，从 config.json 读取）")
    parser.add_argument("--secret",   default="", help="ocrSecret（可省略，从 config.json 读取）")
    parser.add_argument("--verify",   action="store_true", help="识别后自动进行查验")
    parser.add_argument("--export",   action="store_true", help="识别（查验）后导出 Excel")
    parser.add_argument("--template", default=None,
                        help="指定导出模版，支持单选或逗号多选（如：ledger,goods,transport）")
    parser.add_argument("--select-template", dest="select_template",
                        action="store_true",
                        help="交互选择导出模版（支持多选）")
    parser.add_argument("--output",   default=None, help="导出目录（默认与源文件同目录）")
    parser.add_argument("--reuse",    action="store_true",
                        help="复用已有 JSON 结果，跳过识别查验直接导出")
    args = parser.parse_args()

    if not args.image and not args.dir:
        parser.print_help()
        sys.exit(1)

    # 解析模板参数
    templates = _parse_templates(args.template)

    # 加载凭据
    key, secret = load_credentials(args.key, args.secret)
    if not key or not secret:
        key, secret = prompt_credentials()

    # 执行
    if args.image:
        if not Path(args.image).exists():
            print(f"[FAIL] 文件不存在：{args.image}")
            sys.exit(1)
        selected = templates
        # --select-template：由 Agent 调用 ask_followup_question 点选，
        # 脚本输出结构化标记后退出，Agent 再以 --template 重调用
        if args.export and args.select_template:
            print("\n__TEMPLATE_SELECTION__")
            print(json.dumps({
                "mode": "select-template",
                "image": str(Path(args.image).resolve()),
                "verify": args.verify,
                "output": args.output,
                "pre_selected": templates or [],
                "options": [f"[{k}] {v}" for k, v in TEMPLATE_META.items()],
            }, ensure_ascii=False))
            print("__END__")
            return
        process_single(args.image, key, secret,
                       do_verify=args.verify,
                       do_export=args.export,
                       template=selected,
                       output_dir=args.output)
    elif args.dir:
        if not Path(args.dir).exists():
            print(f"[FAIL] 目录不存在：{args.dir}")
            sys.exit(1)
        if args.export and args.select_template:
            print("\n__TEMPLATE_SELECTION__")
            print(json.dumps({
                "mode": "select-template",
                "dir": str(Path(args.dir).resolve()),
                "verify": args.verify,
                "output": args.output,
                "pre_selected": templates or [],
                "options": [f"[{k}] {v}" for k, v in TEMPLATE_META.items()],
            }, ensure_ascii=False))
            print("__END__")
            return
        process_directory(args.dir, key, secret,
                          do_verify=args.verify,
                          do_export=args.export,
                          template=templates,
                          output_dir=args.output,
                          reuse=args.reuse)


if __name__ == "__main__":
    main()
