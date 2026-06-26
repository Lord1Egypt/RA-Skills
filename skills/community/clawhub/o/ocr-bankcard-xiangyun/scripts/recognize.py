#!/usr/bin/env python3
"""
recognize.py
翔云银行卡 OCR Skill — 识别执行脚本

用法:
  # 本地图片文件（推荐）
  python recognize.py --file /path/to/bankcard.jpg

  # Base64 字符串
  python recognize.py --base64 "/9j/4AAQSkZJRgAB..."

  # 指定输出格式（json/table，默认 json）
  python recognize.py --file /path/to/bankcard.jpg --output-format table

依赖:
  pip install requests

识别结果以 JSON 格式打印到 stdout，供后续 export.py 使用。
同时在 stderr 打印人类可读的表格（--output-format table 时在 stdout）。
"""

import argparse
import base64
import json
import os
import sys

try:
    import requests
except ImportError:
    print("[ERROR] 缺少依赖，请先执行: pip install requests", file=sys.stderr)
    sys.exit(3)

# 配置文件路径（skill 根目录）
SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(SKILL_ROOT, "config.json")

# 翔云 API 端点
API_BASE64 = "https://netocr.com/api/recogliu.do"   # Base64 图片流
API_FILE   = "https://netocr.com/api/recog.do"       # multipart 文件上传

TYPE_ID = "17"  # 银行卡识别固定值，禁止修改


# ---------- 配置加载 ----------

def load_config(config_path: str = CONFIG_PATH) -> dict:
    if not os.path.exists(config_path):
        return {}
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


# ---------- 图片处理 ----------

def file_to_base64(file_path: str) -> str:
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


# ---------- API 调用 ----------

def recognize_base64(b64_str: str, key: str, secret: str) -> dict:
    """使用 Base64 图片流调用识别接口。"""
    payload = {
        "img": b64_str,
        "key": key,
        "secret": secret,
        "typeId": TYPE_ID,
        "format": "json",
    }
    resp = requests.post(API_BASE64, data=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()


def recognize_file(file_path: str, key: str, secret: str) -> dict:
    """使用 multipart 文件上传调用识别接口。"""
    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f)}
        data = {
            "key": key,
            "secret": secret,
            "typeId": TYPE_ID,
            "format": "json",
        }
        resp = requests.post(API_FILE, files=files, data=data, timeout=30)
    resp.raise_for_status()
    return resp.json()


# ---------- 结果解析 ----------

ERROR_MAP = {
    "-1": "识别失败：图片质量不佳或未检测到银行卡",
    "-2": "识别失败：参数错误",
    "-3": "服务次数不足：请登录翔云平台充值后重试",
    "-4": "认证失败：key 或 secret 不正确",
    "-5": "余额不足",
}


def parse_result(raw: dict) -> dict:
    """
    将翔云原始响应解析为标准结构。

    翔云银行卡 API 实际返回格式（文件上传接口）：
    {
      "message": {"status": 0, "value": "识别完成"},
      "cardsinfo": [{
        "type": "17",
        "items": [
          {"desc": "卡号", "content": "4270200014046685"},
          {"desc": "银行卡类型", "content": "贷记卡"},
          {"desc": "银行卡名称", "content": "牡丹VISA信用卡"},
          {"desc": "银行名称", "content": "中国工商银行"},
          {"desc": "银行编号", "content": "01020000"},
          {"desc": "有效日期", "content": "11/19"},
          {"desc": "银行卡持有人", "content": "张三"}
        ]
      }]
    }

    注意：Base64 接口（recogliu.do）和文件上传接口（recog.do）可能返回不同格式。
    """
    msg = raw.get("message", {})
    status = msg.get("status")
    status_str = str(status) if status is not None else ""

    # 处理错误状态
    if status != 0:
        err_msg = ERROR_MAP.get(status_str, msg.get("value", f"API 返回错误 status={status}"))
        return {"success": False, "error_code": status_str, "error_message": err_msg, "raw": raw}

    # 解析 cardsinfo 格式
    cardsinfo = raw.get("cardsinfo", [])
    if cardsinfo:
        card = cardsinfo[0]
        items = card.get("items", [])

        # 从 desc/content 对提取字段
        def find_item(desc_key: str) -> str:
            for item in items:
                if item.get("desc") == desc_key:
                    return item.get("content", "")
            return ""

        result = {
            "success": True,
            "card_number":    find_item("卡号"),
            "card_type":      find_item("银行卡类型"),
            "card_name":      find_item("银行卡名称"),
            "bank_name":      find_item("银行名称"),
            "bank_code":      find_item("银行编号"),
            "valid_date":     find_item("有效日期"),
            "holder_name":    find_item("银行卡持有人"),
            "raw": raw,
        }
        return result

    # 兼容旧格式 responseCode / inferredValue
    code = str(raw.get("responseCode", ""))
    if code == "1":
        inferred = raw.get("inferredValue", raw)
        return {
            "success": True,
            "card_number": inferred.get("cardNumber", ""),
            "card_type":   inferred.get("cardType", ""),
            "card_name":   inferred.get("cardName", ""),
            "bank_name":   inferred.get("bankName", ""),
            "bank_code":   inferred.get("bankCode", ""),
            "valid_date":  inferred.get("validDate", ""),
            "holder_name": inferred.get("holderName", ""),
            "raw": raw,
        }

    # 无法解析
    err_msg = msg.get("value", "未知错误")
    return {"success": False, "error_code": status_str, "error_message": f"API 返回错误：{err_msg}", "raw": raw}


# ---------- 格式化输出 ----------

def mask_card_number(card_no: str) -> str:
    """对卡号进行脱敏处理（保留前 4 位和后 4 位）。"""
    if len(card_no) <= 8:
        return card_no
    return card_no[:4] + " **** " * ((len(card_no) - 8) // 4) + card_no[-4:]


def print_table(result: dict) -> None:
    if not result["success"]:
        print(f"\n❌ 识别失败\n\n错误信息：{result['error_message']}\n")
        return
    masked = mask_card_number(result["card_number"])
    print("\n✅ 银行卡识别成功\n")
    print(f"{'字段':<12} {'识别结果'}")
    print("-" * 45)
    print(f"{'卡号':<12} {masked}")
    print(f"{'卡类型':<11} {result['card_type']}")
    print(f"{'卡名称':<11} {result['card_name']}")
    print(f"{'银行名称':<11} {result['bank_name']}")
    print(f"{'银行编号':<11} {result['bank_code']}")
    if result.get("valid_date"):
        print(f"{'有效日期':<11} {result['valid_date']}")
    if result.get("holder_name"):
        print(f"{'持有人':<12} {result['holder_name']}")
    print()


# ---------- 主程序 ----------

def main():
    parser = argparse.ArgumentParser(description="翔云银行卡 OCR 识别")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file",   help="本地图片文件路径（JPG/PNG/BMP）")
    group.add_argument("--base64", help="图片的 Base64 编码字符串")
    parser.add_argument("--config", default=CONFIG_PATH, help="config.json 路径（默认 skill 根目录）")
    parser.add_argument(
        "--output-format",
        choices=["json", "table"],
        default="json",
        help="输出格式：json（默认，供脚本解析）或 table（人类可读表格）",
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="禁止自动保存识别结果到图片同级目录（默认自动保存）",
    )

    args = parser.parse_args()

    # 加载配置
    cfg = load_config(args.config)
    key    = cfg.get("key", "").strip()
    secret = cfg.get("secret", "").strip()

    if not key or not secret:
        msg = {
            "success": False,
            "error_code": "CONFIG_MISSING",
            "error_message": (
                "未找到有效的 API 配置。\n"
                "请先运行以下命令保存您的翔云凭证：\n"
                "  python scripts/config_manager.py save --key <YOUR_KEY> --secret <YOUR_SECRET>\n"
                "翔云平台注册地址：https://www.netocr.com"
            ),
        }
        if args.output_format == "table":
            print(f"\n❌ 配置缺失\n\n{msg['error_message']}\n")
        else:
            print(json.dumps(msg, ensure_ascii=False, indent=2))
        sys.exit(1)

    # 执行识别
    try:
        if args.file:
            if not os.path.exists(args.file):
                print(json.dumps({"success": False, "error_message": f"文件不存在: {args.file}"}, ensure_ascii=False))
                sys.exit(1)
            raw = recognize_file(args.file, key, secret)
        else:
            raw = recognize_base64(args.base64, key, secret)
    except requests.exceptions.ConnectionError:
        msg = {"success": False, "error_message": "网络连接失败，请检查网络后重试"}
        print(json.dumps(msg, ensure_ascii=False, indent=2))
        sys.exit(1)
    except requests.exceptions.Timeout:
        msg = {"success": False, "error_message": "API 请求超时（30s），请稍后重试"}
        print(json.dumps(msg, ensure_ascii=False, indent=2))
        sys.exit(1)
    except Exception as e:
        msg = {"success": False, "error_message": f"请求异常: {e}"}
        print(json.dumps(msg, ensure_ascii=False, indent=2))
        sys.exit(1)

    result = parse_result(raw)

    # --- 自动保存结果到图片同级目录 ---
    if args.file and not args.no_save and result["success"]:
        image_path = os.path.abspath(args.file)
        base, _ = os.path.splitext(image_path)
        result_path = base + ".json"
        # 写入精简结果（不含 raw，减少文件体积）
        save_obj = {k: v for k, v in result.items() if k != "raw"}
        save_obj["source_image"] = os.path.basename(image_path)
        try:
            with open(result_path, "w", encoding="utf-8") as f:
                json.dump(save_obj, f, ensure_ascii=False, indent=2)
        except Exception:
            pass  # 保存失败不影响主流程

    if args.output_format == "table":
        print_table(result)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
