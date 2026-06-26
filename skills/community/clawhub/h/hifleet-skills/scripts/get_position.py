#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取船舶最新位置信息。支持关键字（船名或 MMSI）或直接 MMSI 查询。
两步流程：先 position/shipSearch 搜船，再 position/position/get/token 查位。
需配置环境变量 `HIFLEET_API_KEY`。
可选 `HIFLEET_API_BASE`（默认 https://api.hifleet.com，无末尾斜杠）。

用法:
  python get_position.py <MMSI>              # 直接查位（9 位 MMSI）
  python get_position.py <船名或关键字>        # 先搜船：1 条则直接查位，多条则列出并提示指定 MMSI
  python get_position.py <关键字> <MMSI>     # 多条命中时，用第二个参数指定要查的 MMSI

Security: 仅向 HIFLEET_API_BASE 下 position 相关路径发起 GET；`api_key` 仅用于 API 鉴权；标准库 only。
"""
import os
import sys
import urllib.request
import urllib.parse
import json


def api_base():
    return (os.environ.get("HIFLEET_API_BASE") or "https://api.hifleet.com").rstrip("/")


def get_api_key():
    return os.environ.get("HIFLEET_API_KEY")


def ship_search(shipname: str, api_key: str, i18n: str = "zh", count: str = "50") -> dict:
    """按船名或 MMSI 关键字搜索船舶。"""
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


def get_position(mmsi: str, api_key: str) -> dict:
    """根据 MMSI 获取最新船位。"""
    params = {"mmsi": mmsi, "api_key": api_key}
    url = api_base() + "/position/position/get/token?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def _min_to_dms(minutes: float, is_lat: bool) -> str:
    """将「分」转为 度°分′秒″，纬度带 N/S，经度带 E/W。"""
    deg_float = abs(float(minutes or 0)) / 60
    d = int(deg_float)
    m_float = (deg_float - d) * 60
    m = int(m_float)
    s = round((m_float - m) * 60)
    if s >= 60:
        m, s = m + 1, 0
    if m >= 60:
        d, m = d + 1, 0
    if is_lat:
        ns = "N" if (minutes and float(minutes) >= 0) else "S"
        return f"{d}°{m:02d}′{s:02d}″ {ns}"
    ew = "E" if (minutes and float(minutes) >= 0) else "W"
    return f"{d}°{m:02d}′{s:02d}″ {ew}"


def print_position(data: dict) -> None:
    """按截图样式输出船位：更新于、MMSI、IMO、呼号、船首/航迹、航速、状态、纬度、经度、目的港、ETA、船旗、吃水、类型、长/宽。"""
    lst = data.get("list", {})
    if not lst:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    ti = lst.get("ti") or "-"
    m = lst.get("m") or "-"
    imo = lst.get("imonumber") or "-"
    callsign = lst.get("callsign") or "-"
    h = lst.get("h") or "-"
    co = lst.get("co") or "-"
    sp = lst.get("sp")
    sp_str = sp if sp and str(sp).strip() else "-"
    status = lst.get("status") or "-"
    la_min = lst.get("la")
    lo_min = lst.get("lo")
    lat_str = _min_to_dms(la_min, True) if la_min else "-"
    lon_str = _min_to_dms(lo_min, False) if lo_min else "-"
    destination = lst.get("destination") or "-"
    eta = lst.get("eta") or "-"
    dn = lst.get("dn") or lst.get("fn") or "-"
    draught = lst.get("draught")
    draught_str = f"{draught}米" if draught and str(draught).strip() else "-"
    ship_type = lst.get("type") or "-"
    l_val = lst.get("l")
    w_val = lst.get("w")
    if l_val and w_val:
        lw_str = f"{l_val}米/{w_val}米"
    elif l_val:
        lw_str = f"{l_val}米"
    elif w_val:
        lw_str = f"{w_val}米"
    else:
        lw_str = "-"

    n = lst.get("n") or "-"
    lines = [
        "船名: " + str(n),
        "更新于: " + ti + " UTC+8",
        "MMSI: " + str(m),
        "IMO: " + str(imo),
        "呼号: " + str(callsign),
        "船首/航迹: " + str(h) + "°/" + str(co) + "°",
        "航速: " + (f"{sp_str}节" if sp_str != "-" else "-"),
        "状态: " + str(status),
        "纬度: " + lat_str,
        "经度: " + lon_str,
        "目的港: " + str(destination),
        "ETA: " + str(eta),
        "船旗: " + str(dn),
        "吃水: " + draught_str,
        "类型: " + str(ship_type),
        "长/宽: " + str(lw_str),
    ]
    print("\n".join(lines))


def main():
    api_key = get_api_key()
    if not api_key:
        print("请先配置 HiFleet 授权 api_key（环境变量 HIFLEET_API_KEY）", file=sys.stderr)
        sys.exit(1)
    if len(sys.argv) < 2:
        print("用法: python get_position.py <MMSI> 或 python get_position.py <船名或关键字> [MMSI]", file=sys.stderr)
        sys.exit(1)

    keyword = sys.argv[1].strip()
    chosen_mmsi = sys.argv[2].strip() if len(sys.argv) > 2 else None

    # 已是 9 位数字 MMSI：直接查位
    if keyword.isdigit() and len(keyword) == 9:
        mmsi = chosen_mmsi if chosen_mmsi and chosen_mmsi.isdigit() and len(chosen_mmsi) == 9 else keyword
        try:
            data = get_position(mmsi, api_key)
        except Exception as e:
            print(f"请求失败: {e}", file=sys.stderr)
            sys.exit(1)
        if data.get("result") != "ok":
            print(json.dumps(data, ensure_ascii=False, indent=2), file=sys.stderr)
            sys.exit(1)
        print_position(data)
        return

    # 关键字模式：先搜船
    try:
        search_data = ship_search(keyword, api_key)
    except Exception as e:
        print(f"船舶搜索失败: {e}", file=sys.stderr)
        sys.exit(1)
    if search_data.get("result") != "ok":
        print(json.dumps(search_data, ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(1)

    num = search_data.get("num", 0)
    lst = search_data.get("list", [])

    if num == 0:
        print("未找到匹配船舶，请检查关键字。", file=sys.stderr)
        sys.exit(1)

    if num == 1:
        mmsi = lst[0].get("mmsi")
        if not mmsi:
            print("搜索结果无 MMSI", file=sys.stderr)
            sys.exit(1)
    else:
        # 用户已通过第二参数指定 MMSI
        if chosen_mmsi and chosen_mmsi.isdigit() and len(chosen_mmsi) == 9:
            if not any(s.get("mmsi") == chosen_mmsi for s in lst):
                print(f"指定的 MMSI {chosen_mmsi} 不在搜索结果中。", file=sys.stderr)
                sys.exit(1)
            mmsi = chosen_mmsi
        else:
            # 尝试推断：关键字是否为某条记录的完整 MMSI 或唯一船名
            keyword_upper = keyword.upper()
            by_mmsi = [s for s in lst if s.get("mmsi") == keyword]
            by_name = [s for s in lst if (s.get("name") or "").upper() == keyword_upper]
            if by_mmsi:
                mmsi = by_mmsi[0].get("mmsi")
            elif len(by_name) == 1:
                mmsi = by_name[0].get("mmsi")
            else:
                # 无法唯一确定，列出列表并提示用户指定 MMSI
                print("命中多条船舶，请指定 MMSI 后重试：", file=sys.stderr)
                for s in lst:
                    print(
                        f"  {s.get('name', '')}  MMSI: {s.get('mmsi', '')}  类型: {s.get('type', '')}  船籍: {s.get('dn', '')}",
                        file=sys.stderr,
                    )
                print("用法: python get_position.py <关键字> <MMSI>", file=sys.stderr)
                sys.exit(1)

    try:
        data = get_position(mmsi, api_key)
    except Exception as e:
        print(f"位置查询失败: {e}", file=sys.stderr)
        sys.exit(1)
    if data.get("result") != "ok":
        print(json.dumps(data, ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(1)
    print_position(data)


if __name__ == "__main__":
    main()
