#!/usr/bin/env python3
"""
recognize.py
翔云护照 OCR Skill — 识别执行脚本

用法:
  # 本地图片文件（推荐）
  python recognize.py --file /path/to/passport.jpg

  # Base64 字符串
  python recognize.py --base64 "/9j/4AAQSkZJRgAB..."

  # 指定输出格式（json/table，默认 json）
  python recognize.py --file /path/to/passport.jpg --output-format table

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
from datetime import datetime

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

TYPE_ID = "13"  # 护照识别固定值，禁止修改


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
    "-1": "识别失败：图片质量不佳或未检测到护照",
    "-2": "识别失败：参数错误",
    "-3": "服务次数不足：请登录翔云平台充值后重试",
    "-4": "认证失败：key 或 secret 不正确",
    "-5": "余额不足",
}

# 护照识别返回字段映射（desc -> 标准化字段名）
# 翔云护照 API (typeId=13) 实际返回的 desc 字段名
FIELD_MAP = {
    # 核心字段
    "护照号码":         "passport_number",
    "护照号码MRZ":       "passport_number_mrz",
    "护照类型":         "document_type",
    "本国姓名":         "name",
    "本国姓名(VIZ)":    "name_visual",
    "英文姓名":         "name_english",
    "英文姓":           "surname_english",
    "英文名":           "given_name_english",
    "英文姓名(VIZ)":    "name_english_visual",
    "英文姓(VIZ)":      "surname_english_visual",
    "英文名(VIZ)":      "given_name_english_visual",
    "本国姓名拼音OCR":  "name_pinyin",
    "性别":             "sex",
    # 日期/地点
    "出生日期":         "birth_date",
    "出生地点":         "birth_place",
    "出生地点拼音":     "birth_place_pinyin",
    "签发日期":         "issue_date",
    "签发地点":         "issue_place",
    "签发地点拼音":     "issue_place_pinyin",
    "有效期限":         "expiry_date",
    "有效期至":         "expiry_date",
    "签发机关":         "issuing_authority",
    "签发机关OCR":      "issuing_authority_ocr",
    # 国籍/签发国
    "国籍":             "nationality",
    "签发国":           "issuing_country",
    "签发国代码":       "issuing_country_code",
    "持证人国籍代码":   "holder_country_code",
    # MRZ
    "MRZ1":             "mrz_line1",
    "MRZ2":             "mrz_line2",
    "RFID MRZ":         "rfid_mrz",
    "OCR MRZ":          "ocr_mrz",
    # 其他
    "身份证号码":       "id_number",
    "身份证号码OCR":    "id_number_ocr",
    "身高":             "height",
    "监护人姓名":       "guardian_name",
    "校对英文姓":       "verified_surname_english",
    "校对英文名":       "verified_given_name_english",
    "出生日期OCR":      "birth_date_ocr",
    "有效期至OCR":      "expiry_date_ocr",
    "性别OCR":          "sex_ocr",
    "持证人国籍代码OCR": "holder_country_code_ocr",
}


def parse_result(raw: dict) -> dict:
    """
    将翔云原始响应解析为标准结构。

    翔云证件识别 API 返回格式（含护照，typeId=13）：
    {
      "message": {"status": 0, "value": "识别完成"},
      "cardsinfo": [{
        "type": "13",
        "items": [
          {"desc": "护照号码", "content": "E12345678"},
          {"desc": "姓名", "content": "张三"},
          {"desc": "拼音", "content": "ZHANG SAN"},
          ...
        ]
      }]
    }

    注意：Base64 接口（recogliu.do）和文件上传接口（recog.do）可能返回不同格式。
    """
    msg = raw.get("message", {})
    status = msg.get("status")
    status_str = str(status) if status is not None else ""

    # 处理错误状态
    # 注意：翔云 API 对于证件识别返回的 status 可能是 typeId（如 13）而非 0
    # 只要有 cardsinfo 数据即为成功，不依赖 status 判断
    cardsinfo = raw.get("cardsinfo", [])
    if not cardsinfo and status not in (0, int(TYPE_ID)):
        err_msg = ERROR_MAP.get(status_str, msg.get("value", f"API 返回错误 status={status}"))
        return {"success": False, "error_code": status_str, "error_message": err_msg, "raw": raw}

    # 解析 cardsinfo 格式
    cardsinfo = raw.get("cardsinfo", [])
    if cardsinfo:
        card = cardsinfo[0]
        items = card.get("items", [])

        result = {"success": True}

        for item in items:
            desc = item.get("desc", "")
            content = item.get("content", "")
            if desc in FIELD_MAP:
                result[FIELD_MAP[desc]] = content
            else:
                # 未知字段也保留，方便调试
                safe_key = desc.replace(" ", "_").lower()
                if safe_key:
                    result[safe_key] = content

        result["raw"] = raw
        return result

    # 兼容旧格式：responseCode / inferredValue
    code = str(raw.get("responseCode", ""))
    if code == "1":
        inferred = raw.get("inferredValue", raw)
        result = {"success": True}
        for desc, field in FIELD_MAP.items():
            val = inferred.get(field, "")
            if val:
                result[field] = val
        result["raw"] = raw
        return result

    # 无法解析
    err_msg = msg.get("value", "未知错误")
    return {"success": False, "error_code": status_str, "error_message": f"API 返回错误：{err_msg}", "raw": raw}


# ---------- 格式化输出 ----------

# 表格显示字段定义（按顺序）
DISPLAY_FIELDS = [
    ("document_type",       "护照类型"),
    ("passport_number",     "护照号码"),
    ("passport_number_mrz", "护照号码(MRZ)"),
    ("name",                "姓名"),
    ("name_english",        "英文姓名"),
    ("name_pinyin",         "拼音"),
    ("sex",                 "性别"),
    ("birth_date",          "出生日期"),
    ("birth_place",         "出生地点"),
    ("birth_place_pinyin",  "出生地点(拼音)"),
    ("issue_date",          "签发日期"),
    ("expiry_date",         "有效期限"),
    ("issue_place",         "签发地点"),
    ("issuing_authority",   "签发机关"),
    ("issuing_authority_ocr","签发机关(OCR)"),
    ("issuing_country_code","签发国代码"),
    ("holder_country_code", "持证人国籍代码"),
    ("id_number",           "身份证号码"),
]


def _mask_passport_number(pp_no: str) -> str:
    """对护照号码进行部分脱敏处理。"""
    if len(pp_no) <= 4:
        return pp_no
    return pp_no[:2] + "****" + pp_no[-2:]


def print_table(result: dict) -> None:
    if not result["success"]:
        print(f"\n❌ 护照识别失败\n\n错误信息：{result['error_message']}\n")
        return

    print("\n✅ 护照识别成功\n")
    print(f"{'字段':<12} {'识别结果'}")
    print("-" * 42)

    for key, label in DISPLAY_FIELDS:
        val = result.get(key, "")
        if val:
            if key == "passport_number":
                val = _mask_passport_number(val)
            print(f"{label:<12} {val}")

    # 打印未知字段（如有）
    known_keys = {k for k, _ in DISPLAY_FIELDS} | {"success", "raw", "error_code", "error_message", "recognized_at", "source_image"}
    extra = {k: v for k, v in result.items() if k not in known_keys and isinstance(v, str) and v}
    if extra:
        print()
        for k, v in extra.items():
            print(f"{k:<12} {v}")

    print()


# ---------- 主程序 ----------

def main():
    parser = argparse.ArgumentParser(description="翔云护照 OCR 识别")
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
                print(json.dumps({"success": False, "error_message": f"文件不存在: {args.file}"}, ensure_ascii=False, indent=2))
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
    result["recognized_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
