#!/usr/bin/env python3
"""
发票识别脚本 - invoice-ocr-extractor skill
支持单张识别、批量处理、税务验真、结果导出
"""

import argparse
import base64
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# ── 依赖检查 ──────────────────────────────────────────────────────────────────

def check_deps():
    missing = []
    for pkg in ["PIL", "requests", "pandas"]:
        try:
            __import__(pkg if pkg != "PIL" else "PIL.Image")
        except ImportError:
            missing.append(pkg.replace("PIL", "pillow"))
    if missing:
        print(f"[WARN] 缺少依赖: {', '.join(missing)}")
        print(f"       安装命令: pip3 install {' '.join(missing)}")

# ── OCR 调用 ──────────────────────────────────────────────────────────────────

def ocr_baidu(image_path: str) -> dict:
    """百度发票识别 API"""
    import requests
    api_key = os.environ.get("BAIDU_OCR_API_KEY", "")
    secret_key = os.environ.get("BAIDU_OCR_SECRET_KEY", "")
    if not api_key or not secret_key:
        raise ValueError("未配置 BAIDU_OCR_API_KEY / BAIDU_OCR_SECRET_KEY")

    # 获取 access_token
    token_url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={api_key}&client_secret={secret_key}"
    token = requests.post(token_url).json().get("access_token")

    # 调用发票识别
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()

    url = f"https://aip.baidubce.com/rest/2.0/ocr/v1/vat_invoice?access_token={token}"
    resp = requests.post(url, data={"image": img_b64}).json()

    if "words_result" not in resp:
        raise ValueError(f"百度 OCR 返回错误: {resp}")

    r = resp["words_result"]
    return {
        "invoice_type":   r.get("InvoiceType", {}).get("word", ""),
        "invoice_code":   r.get("InvoiceCode", {}).get("word", ""),
        "invoice_number": r.get("InvoiceNum", {}).get("word", ""),
        "invoice_date":   _normalize_date(r.get("InvoiceDate", {}).get("word", "")),
        "seller_name":    r.get("SellerName", {}).get("word", ""),
        "buyer_name":     r.get("PurchaserName", {}).get("word", ""),
        "amount":         _normalize_amount(r.get("TotalAmount", {}).get("word", "")),
        "tax_rate":       r.get("TaxRate", {}).get("word", ""),
        "tax_amount":     _normalize_amount(r.get("TotalTax", {}).get("word", "")),
        "total_amount":   _normalize_amount(r.get("AmountInFiguers", {}).get("word", "")),
        "source":         "baidu_ocr",
        "confidence":     "high",
    }


def ocr_ai_vision(image_path: str) -> dict:
    """降级方案：使用 AI 视觉能力（无需 API key）
    实际调用时，agent 会直接分析图片，此函数返回提示信息。
    """
    return {
        "invoice_type": "",
        "invoice_code": "",
        "invoice_number": "",
        "invoice_date": "",
        "seller_name": "",
        "buyer_name": "",
        "amount": "",
        "tax_rate": "",
        "tax_amount": "",
        "total_amount": "",
        "source": "ai_vision",
        "confidence": "medium",
        "_note": "请将图片发送给 AI 模型，使用视觉能力提取字段",
    }


def extract_invoice(image_path: str) -> dict:
    """识别单张发票，自动选择 OCR 引擎"""
    path = Path(image_path)
    if not path.exists():
        return {"error": f"文件不存在: {image_path}"}

    result = {"file": str(path), "extracted_at": datetime.now().isoformat()}

    # 尝试百度 OCR
    try:
        data = ocr_baidu(image_path)
        result.update(data)
    except Exception as e:
        print(f"[INFO] 百度 OCR 不可用 ({e})，使用 AI 视觉降级")
        data = ocr_ai_vision(image_path)
        result.update(data)

    # 数据校验
    result["validation"] = validate(result)

    # 费用分类
    result["expense_category"] = classify_expense(result)

    return result


# ── 数据校验 ──────────────────────────────────────────────────────────────────

def validate(data: dict) -> dict:
    issues = []

    # 金额校验
    try:
        amt = float(data.get("amount") or 0)
        tax = float(data.get("tax_amount") or 0)
        total = float(data.get("total_amount") or 0)
        if total > 0 and abs(amt + tax - total) > 0.02:
            issues.append(f"金额校验失败: {amt} + {tax} ≠ {total}")
    except (ValueError, TypeError):
        pass

    # 日期校验
    date_str = data.get("invoice_date", "")
    if date_str:
        try:
            d = datetime.strptime(date_str, "%Y-%m-%d")
            if d > datetime.now():
                issues.append("开票日期是未来日期")
        except ValueError:
            issues.append(f"日期格式异常: {date_str}")

    # 发票代码格式
    code = data.get("invoice_code", "")
    if code and not (len(code) in (10, 12, 20) and code.isdigit()):
        issues.append(f"发票代码格式异常: {code}")

    # 大额提醒
    try:
        if float(data.get("total_amount") or 0) > 1000:
            issues.append("金额 > 1000 元，建议人工复核")
    except (ValueError, TypeError):
        pass

    return {"passed": len(issues) == 0, "issues": issues}


# ── 费用分类 ──────────────────────────────────────────────────────────────────

CATEGORY_RULES = [
    ("交通费-机票",   ["机票", "航空", "航班", "行程单"]),
    ("交通费-火车",   ["铁路", "高铁", "动车", "火车"]),
    ("交通费-出租车", ["出租车", "的士", "滴滴", "曹操", "神州", "T3", "网约车"]),
    ("交通费-地铁",   ["地铁", "轨道交通", "公交"]),
    ("住宿费",        ["酒店", "宾馆", "旅馆", "民宿", "客栈", "如家", "汉庭", "希尔顿"]),
    ("餐饮费",        ["餐厅", "饭店", "酒楼", "食堂", "外卖", "咖啡", "茶饮", "KFC", "麦当劳", "星巴克"]),
    ("办公费",        ["文具", "耗材", "打印", "复印", "办公用品"]),
    ("通讯费",        ["移动", "联通", "电信", "话费", "网费", "宽带"]),
]

def classify_expense(data: dict) -> str:
    invoice_type = data.get("invoice_type", "")
    if "机票" in invoice_type or "行程单" in invoice_type:
        return "交通费-机票"
    if "火车" in invoice_type or "铁路" in invoice_type:
        return "交通费-火车"

    text = " ".join([
        data.get("seller_name", ""),
        data.get("invoice_type", ""),
    ])
    for category, keywords in CATEGORY_RULES:
        if any(kw in text for kw in keywords):
            return category
    return "其他"


# ── 工具函数 ──────────────────────────────────────────────────────────────────

def _normalize_date(s: str) -> str:
    """统一日期格式为 YYYY-MM-DD"""
    if not s:
        return ""
    s = s.replace("年", "-").replace("月", "-").replace("日", "").strip()
    for fmt in ("%Y-%m-%d", "%Y%m%d", "%y.%m.%d"):
        try:
            return datetime.strptime(s, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return s


def _normalize_amount(s: str) -> str:
    """清理金额字符串"""
    if not s:
        return ""
    return s.replace("¥", "").replace(",", "").replace("，", "").strip()


# ── 批量处理 ──────────────────────────────────────────────────────────────────

def batch_extract(directory: str, output: str = "results.xlsx", fmt: str = "excel") -> list:
    import pandas as pd

    dir_path = Path(directory)
    if not dir_path.exists():
        print(f"[ERROR] 目录不存在: {directory}")
        sys.exit(1)

    exts = {".jpg", ".jpeg", ".png", ".pdf", ".bmp"}
    files = [f for f in dir_path.iterdir() if f.suffix.lower() in exts]
    print(f"[INFO] 找到 {len(files)} 张发票")

    results = []
    seen = set()  # 去重：发票代码+号码

    for i, f in enumerate(files, 1):
        print(f"[{i}/{len(files)}] 处理: {f.name}")
        r = extract_invoice(str(f))

        # 去重检查
        key = f"{r.get('invoice_code', '')}-{r.get('invoice_number', '')}"
        if key != "-" and key in seen:
            r["_duplicate"] = True
            print(f"  [WARN] 重复发票，跳过: {key}")
        else:
            seen.add(key)

        results.append(r)
        time.sleep(0.5)  # 避免 API 频率限制

    # 导出
    if fmt == "json":
        with open(output, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"[OK] 已导出 JSON: {output}")
    else:
        df = pd.DataFrame(results)
        df.to_excel(output, index=False)
        print(f"[OK] 已导出 Excel: {output}")

    # 汇总
    valid = [r for r in results if not r.get("_duplicate")]
    total = sum(float(r.get("total_amount") or 0) for r in valid)
    print(f"\n📊 汇总：共 {len(valid)} 张（去重后），合计金额 ¥{total:.2f}")

    return results


# ── 税务验真 ──────────────────────────────────────────────────────────────────

def verify_invoice(code: str, number: str, date: str, amount: str) -> dict:
    """调用税务验真 API（需配置 TAX_VERIFY_API_KEY）"""
    import requests

    api_key = os.environ.get("TAX_VERIFY_API_KEY", "")
    if not api_key:
        return {
            "result": "未配置",
            "message": "未配置 TAX_VERIFY_API_KEY，请手动登录 https://inv.chinatax.gov.cn/ 查验",
        }

    # 日期格式转换
    date_fmt = date.replace("-", "")

    payload = {
        "fpdm": code,
        "fphm": number,
        "kprq": date_fmt,
        "je": amount,
    }

    try:
        resp = requests.post(
            "https://inv.chinatax.gov.cn/api/verify",
            json=payload,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10,
        ).json()

        code_map = {
            "0001": ("真实", True),
            "0002": ("查无此票", False),
            "0003": ("不一致（可能伪造）", False),
            "0004": ("超过查验次数", None),
            "0005": ("已作废", False),
            "0006": ("已冲红", False),
        }
        result_code = resp.get("resultCode", "")
        label, valid = code_map.get(result_code, ("未知", None))
        return {"result": label, "valid": valid, "raw": resp}

    except Exception as e:
        return {"result": "查验失败", "message": str(e)}


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="发票识别工具")
    sub = parser.add_subparsers(dest="cmd")

    # extract
    p_extract = sub.add_parser("extract", help="识别单张发票")
    p_extract.add_argument("--file", required=True, help="发票图片路径")
    p_extract.add_argument("--format", default="json", choices=["json", "text"])

    # batch
    p_batch = sub.add_parser("batch", help="批量识别")
    p_batch.add_argument("--dir", required=True, help="发票目录")
    p_batch.add_argument("--output", default="results.xlsx", help="输出文件")
    p_batch.add_argument("--format", default="excel", choices=["excel", "json"])

    # verify
    p_verify = sub.add_parser("verify", help="税务验真")
    p_verify.add_argument("--code", required=True, help="发票代码")
    p_verify.add_argument("--number", required=True, help="发票号码")
    p_verify.add_argument("--date", required=True, help="开票日期 YYYY-MM-DD")
    p_verify.add_argument("--amount", required=True, help="不含税金额")

    args = parser.parse_args()

    if args.cmd == "extract":
        check_deps()
        result = extract_invoice(args.file)
        if args.format == "json":
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            for k, v in result.items():
                print(f"{k}: {v}")

    elif args.cmd == "batch":
        check_deps()
        batch_extract(args.dir, args.output, args.format)

    elif args.cmd == "verify":
        result = verify_invoice(args.code, args.number, args.date, args.amount)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
