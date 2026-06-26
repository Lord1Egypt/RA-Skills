#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
根据 IMO 查询船舶 PSC（港口国监督检查）数据；支持直接 IMO，或通过船名/MMSI 先搜船再取 IMO。
接口：GET {base}/pscapi/get?imo=...&api_key=...
需配置环境变量 `HIFLEET_API_KEY`。
可选 `HIFLEET_API_BASE`（默认 https://api.hifleet.com，无末尾斜杠）。

用法:
  python get_psc.py <IMO>                    # 7 位 IMO（可带 IMO 前缀）
  python get_psc.py <船名或关键字>           # 先 shipSearch，1 条则取 IMO 查 PSC
  python get_psc.py <船名或关键字> <MMSI>    # 多条命中时指定 MMSI 再取 IMO 查 PSC
  python get_psc.py <9位MMSI>                # 以 MMSI 关键字搜船后取 IMO（同搜船逻辑）

Security: 仅向 HIFLEET_API_BASE 下 position/shipSearch 与 pscapi/get 发起 GET；标准库 only。
"""
import os
import sys
import urllib.request
import urllib.parse
import json
from typing import Optional


def api_base():
    return (os.environ.get("HIFLEET_API_BASE") or "https://api.hifleet.com").rstrip("/")


def get_api_key():
    return os.environ.get("HIFLEET_API_KEY")


def ship_search(shipname: str, api_key: str, i18n: str = "zh", count: str = "50") -> dict:
    params = {
        "shipname": shipname,
        "api_key": api_key,
        "i18n": i18n,
        "count": count,
    }
    url = api_base() + "/position/shipSearch?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def get_psc(api_key: str, imo: str) -> dict:
    params = {"imo": imo.strip(), "api_key": api_key}
    url = api_base() + "/pscapi/get?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def _psc_api_error(data: dict) -> bool:
    c = data.get("code")
    if c is None:
        return False
    try:
        n = int(c)
    except (TypeError, ValueError):
        return True
    return n >= 4000


def _psc_error_hint(data: dict) -> Optional[str]:
    """根据服务端 code 给出中文说明（stderr）。"""
    try:
        n = int(data.get("code"))
    except (TypeError, ValueError):
        return None
    if n == 4001:
        return (
            "该 api_key 无权访问 PSC 接口（/pscapi/get）。"
            "请在 HiFleet 开通或续约 PSC 数据 API 权限，或使用已授权该路径的 api_key。"
        )
    if n == 4004:
        return "api_key 无效或不存在，请检查 HIFLEET_API_KEY。"
    if n == 4005:
        return "未携带 api_key，请配置环境变量或项目中的 api_key。"
    return None


def _print_psc_success(data: dict) -> None:
    """
    成功体结构以服务端为准。优先识别常见形态：status=1 + data 列表、顶层 list、或 code 为 0/200。
    无法识别时回退为整份 JSON。
    """
    # HiFleet 档案类风格：status 为 1，data 为数组
    if str(data.get("status")) == "1":
        payload = data.get("data")
        if isinstance(payload, list):
            if not payload:
                print("（无 PSC 记录）")
                return
            for i, row in enumerate(payload, 1):
                print("\n--- 记录 %d ---" % i)
                if isinstance(row, dict):
                    for k, v in sorted(row.keys()):
                        print("  %s: %s" % (k, v))
                else:
                    print(json.dumps(row, ensure_ascii=False, indent=2))
            return

    # 与船位搜船类似的顶层 list
    lst = data.get("list")
    if isinstance(lst, list):
        if not lst:
            print("（无 PSC 记录）")
            return
        if isinstance(lst[0], dict):
            for i, row in enumerate(lst, 1):
                print("\n--- 记录 %d ---" % i)
                for k, v in sorted(row.keys()):
                    print("  %s: %s" % (k, v))
            return

    # 部分接口用数值 code 表示成功
    if data.get("code") in (0, 200, "0", "200"):
        inner = data.get("data")
        if isinstance(inner, list) and inner:
            for i, row in enumerate(inner, 1):
                print("\n--- 记录 %d ---" % i)
                if isinstance(row, dict):
                    for k, v in sorted(row.keys()):
                        print("  %s: %s" % (k, v))
                else:
                    print(json.dumps(row, ensure_ascii=False, indent=2))
            return

    print(json.dumps(data, ensure_ascii=False, indent=2))


def print_psc(data: dict) -> None:
    if _psc_api_error(data):
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    if data.get("status") is not None and str(data.get("status")) != "1":
        # 部分接口用 status 表示失败（且无 code）
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    _print_psc_success(data)


def _normalize_imo_arg(raw: str) -> str:
    s = raw.strip()
    if s.upper().startswith("IMO"):
        s = s.upper().replace("IMO", "", 1).strip()
    return s


def _is_imo_token(s: str) -> bool:
    """IMO 一般为 6～7 位数字；9 位走 MMSI 搜船分支。"""
    if not s.isdigit():
        return False
    return len(s) in (6, 7)


def resolve_imo_from_search(keyword: str, api_key: str, chosen_mmsi: Optional[str]) -> str:
    search_data = ship_search(keyword, api_key)
    if search_data.get("result") != "ok":
        raise ValueError(json.dumps(search_data, ensure_ascii=False))

    num = search_data.get("num", 0)
    lst = search_data.get("list", [])

    if num == 0 or not lst:
        raise ValueError("未找到匹配船舶，请检查关键字。")

    if num == 1:
        ship = lst[0]
    else:
        if chosen_mmsi and chosen_mmsi.isdigit() and len(chosen_mmsi) == 9:
            if not any(s.get("mmsi") == chosen_mmsi for s in lst):
                raise ValueError(f"指定的 MMSI {chosen_mmsi} 不在搜索结果中。")
            ship = next(s for s in lst if s.get("mmsi") == chosen_mmsi)
        else:
            keyword_upper = keyword.upper()
            by_mmsi = [s for s in lst if s.get("mmsi") == keyword]
            by_name = [s for s in lst if (s.get("name") or "").upper() == keyword_upper]
            if by_mmsi:
                ship = by_mmsi[0]
            elif len(by_name) == 1:
                ship = by_name[0]
            else:
                lines = ["命中多条船舶，请指定 MMSI 后重试："]
                for s in lst:
                    imo_disp = s.get("imonumber") or "-"
                    lines.append(
                        f"  {s.get('name', '')}  MMSI: {s.get('mmsi', '')}  IMO: {imo_disp}  类型: {s.get('type', '')}"
                    )
                lines.append("用法: python get_psc.py <关键字> <MMSI>")
                raise ValueError("\n".join(lines))

    imo = (ship.get("imonumber") or "").strip()
    if not imo:
        raise ValueError(
            "该船无 IMO（可能为内贸船），PSC 接口按 IMO 查询。请换用有 IMO 的船舶或直接向用户提供 IMO。"
        )
    return imo


def main():
    api_key = get_api_key()
    if not api_key:
        print("请先配置 HiFleet 授权 api_key（环境变量 HIFLEET_API_KEY）", file=sys.stderr)
        sys.exit(1)
    if len(sys.argv) < 2:
        print(
            "用法: python get_psc.py <IMO> | python get_psc.py <船名或MMSI关键字> [MMSI]",
            file=sys.stderr,
        )
        sys.exit(1)

    keyword = sys.argv[1].strip()
    chosen_mmsi = sys.argv[2].strip() if len(sys.argv) > 2 else None

    imo: Optional[str] = None
    norm = _normalize_imo_arg(keyword)

    if _is_imo_token(norm):
        imo = norm
    elif keyword.isdigit() and len(keyword) == 9:
        # 9 位：按 MMSI 搜船再取 IMO
        try:
            imo = resolve_imo_from_search(keyword, api_key, chosen_mmsi)
        except ValueError as e:
            print(str(e), file=sys.stderr)
            sys.exit(1)
    else:
        try:
            imo = resolve_imo_from_search(keyword, api_key, chosen_mmsi)
        except ValueError as e:
            print(str(e), file=sys.stderr)
            sys.exit(1)

    if not imo:
        print("无法确定 IMO", file=sys.stderr)
        sys.exit(1)

    print(f"查询 IMO: {imo}", file=sys.stderr)
    try:
        raw = get_psc(api_key, imo)
    except Exception as e:
        print(f"PSC 请求失败: {e}", file=sys.stderr)
        sys.exit(1)

    if _psc_api_error(raw):
        hint = _psc_error_hint(raw)
        if hint:
            print(hint, file=sys.stderr)
        print(json.dumps(raw, ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(1)
    print_psc(raw)


if __name__ == "__main__":
    main()
