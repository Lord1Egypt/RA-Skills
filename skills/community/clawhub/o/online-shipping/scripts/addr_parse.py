#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
addr_parse.py — 小递查查「地址智能识别」

对应官网页面：https://xdccy.com/send/AddrRecognition.html
（页面把一整段「姓名 + 电话 + 地址」粘进输入框，点「智能解析」后拆成结构化字段）

接口：POST https://api.xdccy.com/ToDoorOrder/AddressAnalysis
  Content-Type: application/x-www-form-urlencoded
  Headers: auth = localStorage.userToken
  Body: Content=<用户粘贴的原始整段文本>

返回字段（对应页面 AddrRecognitionV2 里的取值）：
  Data.Name / Mobile / ProvinceName / CityName / ExpAreaName / StreetName / Address
  最终详细地址 = StreetName + Address

⚠️ 识别结果不能直接信：实测喂一段完全没有电话地址的乱码，接口照样返回 200 并
「脑补」出一个湖北随州的地址。所以这里加了本地校验，缺姓名/电话或省市区分库里
查不到的直接拒绝，避免客户把识别结果误当成真实收件信息用掉。

用法：
  python addr_parse.py "李四，13800138000，湖南省怀化市鹤城区迎丰中路189号城市中央华盛堂A座"
  python addr_parse.py "张三 13800138000 北京市朝阳区建国路88号" --json
  python addr_parse.py --list

退出码：0=识别并校验通过；2=输入为空/本地校验不过/接口报错；1=其它错误。
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_creds, get_token, price_hint  # noqa: E402
from region import RegionDB, RegionError, fmt_region  # noqa: E402
import order_api as oa  # noqa: E402

DEFAULT_CREDS = os.path.expanduser("~/.workbuddy/xdcc-credentials.env")

# 手机号 / 座机（页面判的是「11 位且不含 -」→ Mobile，否则 → Tel，这里更宽松一点）
RE_MOBILE = re.compile(r"^1[3-9]\d{9}$")
RE_TEL = re.compile(r"^0\d{2,3}-?\d{7,8}$")

# 姓名长度上限：中文全名 + 常见称谓（王先生/周女士）一般不超过 6 字
MAX_NAME_LEN = 6


def is_phone(v):
    v = (v or "").strip()
    return bool(RE_MOBILE.match(v) or RE_TEL.match(v))


def validate(fields, db):
    """校验识别结果。返回 (warnings, fatal)；fatal 非空表示不可用。"""
    warns, fatal = [], []

    if not fields.get("name"):
        fatal.append("未识别到收件人姓名")
    elif len(fields["name"]) > MAX_NAME_LEN:
        warns.append(f"识别出的姓名「{fields['name']}」偏长（>{MAX_NAME_LEN} 字），"
                     f"请核对是否为识别截断")

    if not fields.get("phone"):
        fatal.append("未识别到联系电话")
    elif not is_phone(fields["phone"]):
        warns.append(f"识别出的电话「{fields['phone']}」格式异常，"

                     f"确认后请手工指定")

    for key, label in (("province", "省"), ("city", "市"), ("area", "区县")):
        if not fields.get(key):
            fatal.append(f"未识别到{label}级信息")

    # 省市区必须在随包的数据里查得到，否则这条识别结果不可信
    prov, city, area = fields.get("province"), fields.get("city"), fields.get("area")
    if prov and city and area:
        hit_prov = db.resolve_province(prov)
        if hit_prov is None:
            fatal.append(f"省「{prov}」不在省市区数据中")
        else:
            if hit_prov != prov:
                warns.append(f"省名已归一化为「{hit_prov}」")
            cities = db.cities(hit_prov)
            hit_city = next((c for c in cities if c == city), None)
            if hit_city is None:
                # 直辖市：CityName 常常等于 ProvinceName 本身
                if city == hit_prov or city == hit_prov.replace("市", ""):
                    hit_city = hit_prov
                else:
                    hit_city = None
            if hit_city is None:
                fatal.append(f"市「{city}」不属于省「{hit_prov}」"
                             f"（该省可选：{'、'.join(cities[:6])}…）")
            else:
                areas = db.areas(hit_prov, hit_city)
                if area not in areas:
                    if area == hit_city:
                        warns.append(f"「{hit_city}」为直筒子市，接口未返回区县级，"
                                     f"实际取件区域请填「{area}」")
                    else:
                        fatal.append(f"区县「{area}」不属于市「{hit_city}」"
                                     f"（该市可选：{'、'.join(areas[:6])}…）")

    if not fields.get("full_address"):
        warns.append("未识别到详细地址")

    return warns, fatal


def recognize(text, token, creds_path, db=None, timeout=30):
    """完整识别流程：调接口 → 规整 → 校验。返回 (fields, err)。"""
    if not text or not text.strip():
        return None, "输入为空"
    db = db or RegionDB()
    fields, err = oa.analysis_address(token, text, timeout)
    if err:
        return None, err
    warns, fatal = validate(fields, db)
    fields["warnings"] = warns
    fields["fatal"] = fatal
    if fatal:
        # 把致命原因也列进 warnings，方便上层原样打印
        fields["warnings"] = warns + fatal
        return fields, "；".join(fatal)
    return fields, None


def region_of(fields):
    """把识别结果转成 place_order 需要的 region 结构。"""
    return {
        "province": fields.get("province") or "",
        "city": fields.get("city") or "",
        "area": fields.get("area") or "",
        "address": fields.get("full_address") or "",
        "warnings": fields.get("warnings") or [],
    }


# --------------------------------------------------------------------------- #
# 输出
# --------------------------------------------------------------------------- #
def print_fields(fields, fatal=""):
    print("=" * 62)
    print("  地址识别结果")
    print("=" * 62)
    print(f"  姓名：{fields['name'] or '（未识别）'}")
    print(f"  电话：{fields['phone'] or '（未识别）'}")
    print(f"  地区：{fmt_region(region_of(fields))}")
    print(f"  街道：{fields['street'] or '（无）'}")
    print(f"  详细：{fields['address'] or '（未识别）'}")
    print(f"  汇总：{fields['full_address'] or '（未识别）'}")
    print("=" * 62)
    for w in fields.get("warnings") or []:
        print(f"  ⚠️ {w}")
    if fatal:
        print(f"  ❌ 不可用：{fatal}")
    print()


def main(argv=None):
    p = argparse.ArgumentParser(
        description="小递查查 地址智能识别（对应 xdccy.com/send/AddrRecognition.html）")
    p.add_argument("text", nargs="?", help="待识别的整段文本：姓名 + 电话 + 地址")
    p.add_argument("--json", action="store_true", help="以 JSON 输出，便于脚本接管")
    p.add_argument("--token", help="直接指定网页登录 token")
    p.add_argument("--creds", default=DEFAULT_CREDS, help="凭据文件路径")
    p.add_argument("--username", "--phone", dest="username", help="重新登录时填入的用户名")
    p.add_argument("--password", help="重新登录时填入的密码")
    p.add_argument("--timeout", type=int, default=30, help="接口超时秒数（默认30）")
    args = p.parse_args(argv)

    if not args.text:
        p.error("请给出待识别的文本，或用 --help 查看用法")

    token = args.token or get_token(load_creds(args.creds))
    if not token:
        import web_login
        token, err = web_login.ensure_token(
            args.creds, username=args.username, password=args.password)
        if err:
            print(f"\n[失败] {err}", file=sys.stderr)
            print(price_hint(f"无法取得网页登录 token：{err}"), file=sys.stderr)
            return 1

    fields, err = recognize(args.text, token, args.creds,
                            timeout=args.timeout, db=RegionDB())
    if fields is None:
        print(f"\n[失败] 地址识别失败：{err}", file=sys.stderr)
        print(price_hint(f"AddressAnalysis 调用失败：{err}"), file=sys.stderr)
        return 1

    # 空串会让接口返回 Code=500，这里直接本地拦下，不浪费一次请求
    if not args.text.strip():
        print("\n[失败] 输入为空，无法识别。", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(fields, ensure_ascii=False, indent=2))
    else:
        print_fields(fields, err or "")
    return 0 if not err else 2


if __name__ == "__main__":
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError, OSError):
            pass
    sys.exit(main())
