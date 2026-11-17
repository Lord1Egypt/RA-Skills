#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DRG 3.0 分组查询工具 — CHS-DRG 3.0 版
=====================================
数据来源：医保发〔2026〕22号 附件1《DRG 3.0 分组方案》

支持的查询：
1. ICD-10 诊断 → MDC
2. ICD-9-CM-3 手术 / ICD-10 诊断 → ADRG 列表
3. ADRG 编码 → ADRG 名称 + 所属 MDC
4. DRG 编码 → DRG 名称 + 严重程度 + 内外科
5. ICD → 是否 MCC / CC
6. ICD → 是否高危妊娠 / 不作为分组
7. ICD → 31 个基层病组之一
8. ADRG 2.0 ↔ 3.0 对比
9. 列出某 MDC 下所有 ADRG/DRG
10. 关键字模糊搜索（疾病名 → ICD/ADRG/DRG）

使用示例：
    python3 drg3.0_lookup_tool.py mdc I63.4
    python3 drg3.0_lookup_tool.py adrg 33.5000
    python3 drg3.0_lookup_tool.py drg BB21
    python3 drg3.0_lookup_tool.py mcc I50.0
    python3 drg3.0_lookup_tool.py basal 高血压
    python3 drg3.0_lookup_tool.py compare AE1
    python3 drg3.0_lookup_tool.py list mdc B
    python3 drg3.0_lookup_tool.py search 肺炎
"""

import json
import os
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any

# 数据文件路径（与 SKILL.md 平级 data/ 目录）
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# 缓存
_CACHE: Dict[str, Any] = {}


def _load(name: str) -> Any:
    """惰性加载 JSON 数据文件"""
    if name in _CACHE:
        return _CACHE[name]
    path = DATA_DIR / f"drg3.0_{name}.json"
    if not path.exists():
        raise FileNotFoundError(f"数据文件不存在: {path}")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    _CACHE[name] = data
    return data


# =================== 查询函数 ===================

def mdc_by_dx(dx_code: str) -> List[Dict]:
    """诊断编码 → MDC"""
    mdc_dx = _load("mdc_dx")["数据"]
    dx_code = dx_code.strip().upper()
    # 处理星剑号组合 A01.000x005+J17.0* - 取主码
    main_code = dx_code.split("+")[0].split("/")[0]
    results = [d for d in mdc_dx if d["诊断编码"].upper() == main_code]
    if results:
        return results
    # 模糊匹配（前缀）
    prefix_matches = [d for d in mdc_dx if d["诊断编码"].upper().startswith(main_code[:5])]
    return prefix_matches[:5]


def adrg_by_icd(icd_code: str) -> List[Dict]:
    """ICD 编码 → ADRG 列表"""
    icd_to_adrg = _load("icd_to_adrg")["数据"]
    adrg_data = {a["ADRG编码"]: a for a in _load("adrg")["数据"]}
    icd_code = icd_code.strip()
    # 兼容星剑号
    main_code = icd_code.split("+")[0].split("/")[0].rstrip("*")
    adrg_codes = icd_to_adrg.get(main_code, [])
    results = []
    for code in adrg_codes:
        if code in adrg_data:
            results.append(adrg_data[code])
    if not adrg_codes:
        # 前缀匹配
        for k, v in icd_to_adrg.items():
            if k.startswith(main_code[:6]):
                for code in v:
                    if code in adrg_data and adrg_data[code] not in results:
                        results.append(adrg_data[code])
                if len(results) >= 5:
                    break
    return results[:10]


def drg_info(drg_code: str) -> List[Dict]:
    """DRG 编码 → DRG 详情"""
    drg_data = _load("drg")["数据"]
    drg_code = drg_code.strip().upper()
    results = [d for d in drg_data if d["DRG编码"].upper() == drg_code]
    if not results:
        # 前缀匹配
        prefix = drg_code[:3]
        results = [d for d in drg_data if d["DRG编码"].upper().startswith(prefix)]
    return results


def adrg_info(adrg_code: str) -> List[Dict]:
    """ADRG 编码 → ADRG 详情"""
    adrg_data = _load("adrg")["数据"]
    adrg_code = adrg_code.strip().upper()
    results = [a for a in adrg_data if a["ADRG编码"].upper() == adrg_code]
    return results


def mcc_check(dx_code: str) -> bool:
    """诊断编码是否为 MCC"""
    mcc = _load("mcc")["数据"]
    dx_code = dx_code.strip().upper()
    main_code = dx_code.split("+")[0].split("/")[0]
    return any(d["诊断编码"].upper() == main_code for d in mcc)


def cc_check(dx_code: str) -> bool:
    """诊断编码是否为 CC"""
    cc = _load("cc")["数据"]
    dx_code = dx_code.strip().upper()
    main_code = dx_code.split("+")[0].split("/")[0]
    return any(d["诊断编码"].upper() == main_code for d in cc)


def high_risk_preg(dx_code: str) -> bool:
    """诊断编码是否为高危妊娠"""
    hrp = _load("high_risk_preg")["数据"]
    dx_code = dx_code.strip().upper()
    main_code = dx_code.split("+")[0].split("/")[0]
    return any(d["诊断编码"].upper() == main_code for d in hrp)


def basal_check(query: str) -> List[Dict]:
    """查询 31 个基层病组（按 DRG 编码或疾病名）"""
    basal = _load("basal")["数据"]
    query = query.strip()
    results = []
    # 编码匹配
    for b in basal:
        if query.upper() in b["DRG编码"].upper():
            results.append(b)
    # 名称模糊匹配
    if not results:
        for b in basal:
            if query in b["DRG名称"]:
                results.append(b)
    return results


def compare_20_30(adrg_code: str, reverse: bool = False) -> List[Dict]:
    """ADRG 2.0 ↔ 3.0 对比"""
    comp = _load("adrg_compare")["数据"]
    adrg_code = adrg_code.strip().upper()
    results = []
    for c in comp:
        if not reverse:
            if c["2.0_ADRG"] and c["2.0_ADRG"].upper() == adrg_code:
                results.append(c)
        else:
            if c["3.0_ADRG"] and c["3.0_ADRG"].upper() == adrg_code:
                results.append(c)
    return results


def list_by_mdc(mdc_letter: str) -> Dict:
    """列出某 MDC 下所有 ADRG/DRG"""
    mdc_letter = mdc_letter.strip().upper()
    if len(mdc_letter) == 4 and mdc_letter.startswith("MDC"):
        mdc_letter = mdc_letter[3:]
    mdc_letter = mdc_letter[0] if mdc_letter else "?"

    adrg = [a for a in _load("adrg")["数据"] if a["ADRG编码"].startswith(mdc_letter)]
    drg = [d for d in _load("drg")["数据"] if d["DRG编码"].startswith(mdc_letter)]
    return {"ADRG": adrg, "DRG": drg}


# 常用诊断词 → ICD 编码前缀（用于中文名模糊搜索）
# 来源：高频临床术语，配合临床术语映射（31,106条）使用更佳
COMMON_TERMS: Dict[str, str] = {
    "脑梗死": "I63", "脑梗塞": "I63", "脑卒中": "I63", "中风": "I63",
    "脑出血": "I61", "蛛网膜下腔出血": "I60",
    "心梗": "I21", "心绞痛": "I20", "心衰": "I50", "心房颤动": "I48", "房颤": "I48",
    "高血压": "I10", "高血压病": "I10",
    "糖尿病": "E11", "糖尿病酮症": "E11.1", "糖尿病足": "E11.5",
    "肺炎": "J18", "支气管炎": "J20", "慢阻肺": "J44", "哮喘": "J45",
    "阑尾炎": "K35", "阑尾切除": "47.0", "胆囊炎": "K81", "胆囊切除": "51.2",
    "胃癌": "C16", "肝癌": "C22", "肺癌": "C34", "乳腺癌": "C50", "宫颈癌": "C53", "结直肠癌": "C18-C20",
    "白血病": "C91", "淋巴瘤": "C85",
    "肾衰竭": "N18", "尿毒症": "N18", "肾结石": "N20", "尿路感染": "N39",
    "骨折": "Sxx", "脑外伤": "S06", "烧伤": "T20",
    "剖宫产": "74.0", "剖腹产": "74.0", "顺产": "80.0", "分娩": "80",
    "白内障": "H25", "青光眼": "H40", "视网膜": "H35",
    "中耳炎": "H66",
    "疝气": "K40", "腹股沟疝": "K40",
    "痔疮": "I84", "肛瘘": "K60",
    "腰椎间盘突出": "M51",
}


def search_by_keyword(keyword: str, limit: int = 20) -> List[Dict]:
    """按疾病名/手术名/ICD 编码模糊搜索"""
    keyword = keyword.strip()
    results = []

    # 1. 中文常用词 → ICD 前缀
    if keyword in COMMON_TERMS:
        prefix = COMMON_TERMS[keyword]
        results.append({
            "类型": "提示",
            "编码": prefix,
            "名称": f"常用术语 '{keyword}' 对应 ICD 范围",
            "MDC": "再用 mdc 子命令查具体 MDC"
        })

    # 2. ICD 前缀搜索（如 I63, J18, 33.5）
    # 诊断：1字母+数字 (I63) 或 1字母+1字母 (AA)
    # 手术：数字.数字 (33.5)
    is_icd_prefix = False
    if len(keyword) >= 2:
        if keyword[0].isalpha() and (keyword[1].isalnum() or keyword[1] == "."):
            # 检查余下字符也是字母/数字/点
            rest = keyword[1:].replace(".", "").replace("x", "").replace("X", "")
            if rest.isalnum() or rest == "":
                is_icd_prefix = True
        if keyword.replace(".", "").isdigit():
            is_icd_prefix = True
    if is_icd_prefix:
        kw = keyword.upper()
        mdc_dx = _load("mdc_dx")["数据"]
        icd_to_adrg = _load("icd_to_adrg")["数据"]
        seen = set()
        for d in mdc_dx:
            code = d.get("诊断编码", "").upper()
            if code.startswith(kw) and code not in seen:
                seen.add(code)
                results.append({
                    "类型": "诊断",
                    "编码": d["诊断编码"],
                    "名称": f"→ {d.get('MDC名称', '')}",
                    "MDC": d.get("MDC编码", "")
                })
                if len([r for r in results if r["类型"] == "诊断"]) >= 5:
                    break
        # 手术前缀
        if "." in kw or keyword[0].isdigit():
            ops = _load("ops")["数据"]
            for o in ops:
                if o["手术编码"].startswith(kw):
                    results.append({
                        "类型": "手术",
                        "编码": o["手术编码"],
                        "名称": o["手术名称"],
                        "MDC": ""
                    })
                    if len([r for r in results if r["类型"] == "手术"]) >= 5:
                        break

    # 3. ADRG 名称
    for a in _load("adrg")["数据"]:
        if keyword in a.get("ADRG名称", ""):
            results.append({"类型": "ADRG", "编码": a["ADRG编码"], "名称": a["ADRG名称"], "MDC": a.get("所属MDC名称", "")})

    # 4. DRG 名称
    for d in _load("drg")["数据"]:
        if keyword in d.get("DRG名称", ""):
            results.append({"类型": "DRG", "编码": d["DRG编码"], "名称": d["DRG名称"], "组别": d.get("组别", "")})

    # 5. 手术名称
    if not is_icd_prefix:
        for o in _load("ops")["数据"][:5000]:
            if keyword in o.get("手术名称", ""):
                results.append({"类型": "手术", "编码": o["手术编码"], "名称": o["手术名称"], "MDC": ""})
                if len([r for r in results if r["类型"] == "手术"]) >= 3:
                    break

    return results[:limit]


# =================== CLI ===================

def print_table(rows: List[Dict], columns: List[str], title: str = ""):
    if title:
        print(f"\n=== {title} ===")
    if not rows:
        print("(无结果)")
        return
    # 计算列宽
    widths = {c: len(c) for c in columns}
    for r in rows:
        for c in columns:
            v = str(r.get(c, ""))
            widths[c] = max(widths[c], min(len(v), 40))
    # 打印表头
    header = " | ".join(c.ljust(widths[c]) for c in columns)
    print(header)
    print("-+-".join("-" * widths[c] for c in columns))
    # 打印行
    for r in rows:
        line = " | ".join(str(r.get(c, ""))[:40].ljust(widths[c]) for c in columns)
        print(line)


def main():
    parser = argparse.ArgumentParser(
        description="CHS-DRG 3.0 分组查询工具（医保发〔2026〕22号）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s mdc I63.4                    # 诊断 → MDC
  %(prog)s adrg 33.5000                 # 手术 → ADRG
  %(prog)s drg BB21                     # DRG 编码 → 详情
  %(prog)s mcc I50.0                    # 是否 MCC
  %(prog)s cc J18.9                     # 是否 CC
  %(prog)s basal 高血压                 # 31 基层病组查询
  %(prog)s compare AE1                  # 2.0 → 3.0 对比
  %(prog)s compare AC2 --reverse        # 3.0 → 2.0 反查
  %(prog)s list MDCB                    # 列出 MDCB 下所有 ADRG/DRG
  %(prog)s search 肺炎                  # 模糊搜索
        """,
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_mdc = sub.add_parser("mdc", help="诊断编码 → MDC")
    p_mdc.add_argument("code")

    p_adrg = sub.add_parser("adrg", help="ICD 编码 → ADRG 列表")
    p_adrg.add_argument("code")

    p_drg = sub.add_parser("drg", help="DRG 编码 → 详情")
    p_drg.add_argument("code")

    p_adrg_info = sub.add_parser("adrg-info", help="ADRG 编码 → ADRG 详情")
    p_adrg_info.add_argument("code")

    p_mcc = sub.add_parser("mcc", help="是否严重合并症")
    p_mcc.add_argument("code")

    p_cc = sub.add_parser("cc", help="是否一般合并症")
    p_cc.add_argument("code")

    p_hrp = sub.add_parser("hrp", help="是否高危妊娠")
    p_hrp.add_argument("code")

    p_basal = sub.add_parser("basal", help="31 基层病组查询")
    p_basal.add_argument("query")

    p_compare = sub.add_parser("compare", help="2.0 ↔ 3.0 ADRG 对比")
    p_compare.add_argument("code")
    p_compare.add_argument("--reverse", action="store_true", help="反查（3.0 → 2.0）")

    p_list = sub.add_parser("list", help="列出 MDC 下所有 ADRG/DRG")
    p_list.add_argument("mdc", help="MDC 字母或 MDC 编码（例：B 或 MDCB）")

    p_search = sub.add_parser("search", help="关键字模糊搜索")
    p_search.add_argument("keyword")
    p_search.add_argument("--limit", type=int, default=20)

    args = parser.parse_args()

    try:
        if args.cmd == "mdc":
            rows = mdc_by_dx(args.code)
            print_table(rows, ["诊断编码", "诊断名称", "MDC编码"], f"诊断 {args.code} → MDC")
        elif args.cmd == "adrg":
            rows = adrg_by_icd(args.code)
            print_table(rows, ["ADRG编码", "ADRG名称", "所属MDC编码", "所属MDC名称"], f"ICD {args.code} → ADRG")
        elif args.cmd == "drg":
            rows = drg_info(args.code)
            print_table(rows, ["DRG编码", "DRG名称", "MCC/CC", "内外科", "组别"], f"DRG {args.code}")
        elif args.cmd == "adrg-info":
            rows = adrg_info(args.code)
            print_table(rows, ["ADRG编码", "ADRG名称", "所属MDC编码", "所属MDC名称"], f"ADRG {args.code}")
        elif args.cmd == "mcc":
            print(f"诊断 {args.code} → MCC: {mcc_check(args.code)}")
        elif args.cmd == "cc":
            print(f"诊断 {args.code} → CC: {cc_check(args.code)}")
        elif args.cmd == "hrp":
            print(f"诊断 {args.code} → 高危妊娠: {high_risk_preg(args.code)}")
        elif args.cmd == "basal":
            rows = basal_check(args.query)
            print_table(rows, ["序号", "DRG编码", "DRG名称", "分类"], f"基层病组: {args.query}")
        elif args.cmd == "compare":
            rows = compare_20_30(args.code, reverse=args.reverse)
            direction = "3.0 → 2.0" if args.reverse else "2.0 → 3.0"
            print_table(rows, ["2.0_ADRG", "2.0_名称", "3.0_ADRG", "3.0_名称", "对比"], f"ADRG {direction}: {args.code}")
        elif args.cmd == "list":
            data = list_by_mdc(args.mdc)
            print_table(data["ADRG"], ["ADRG编码", "ADRG名称", "所属MDC编码"], f"{args.mdc} ADRG")
            print_table(data["DRG"], ["DRG编码", "DRG名称", "MCC/CC", "内外科", "组别"], f"{args.mdc} DRG")
        elif args.cmd == "search":
            rows = search_by_keyword(args.keyword, limit=args.limit)
            print_table(rows, ["类型", "编码", "名称", "MDC"], f"搜索: {args.keyword}")
    except FileNotFoundError as e:
        print(f"错误: {e}", file=sys.stderr)
        print(f"提示: 请确保 {DATA_DIR} 下有所有 drg3.0_*.json 文件", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
