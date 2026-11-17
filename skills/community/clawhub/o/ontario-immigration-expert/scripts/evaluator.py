#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ontario-immigration-expert — 安省移民通用算分引擎 (OINP, 本地, 不联网)
- OINP Ontario Workforce Priority stream EOI 全因子 + 前置资格核验
- 输入: stdin 传 JSON profile (任意候选人), 或省略走示例
- 职业类别由 NOC 5位码首位自动推导 (官方 "broad occupational category" = NOC大类号)
- 双语官方规则: 2门官方语言(均CLB6+)=10, 1门=5
- 官方页未声明总分上限; 输出"因子参考上限"而非"官方满分130"
"""
import json, sys

# ---- 官方 EOI 规则 (依据 data/snapshots/oinp-workforce-priority-OFFICIAL.txt) ----
def teer_points(teer):
    return 9 if teer in (0,1) else (6 if teer in (2,3) else 0)

OCC_CAT = {  # NOC 大类号 (0-9) -> 分数
    3: 10, 7: 8, 2: 6, 0: 4, 1: 4, 4: 4, 8: 4, 9: 4, 5: 2, 6: 2,
}

def wage_points(w):
    return 15 if w >= 40 else 12 if w >= 35 else 10 if w >= 30 else 8 if w >= 25 else 5 if w >= 20 else 0

def exp_points(curr_m, total_on_m):
    if curr_m >= 24: return 18
    if curr_m >= 13: return 15
    if curr_m >= 6:  return 12
    # 现职<6mo 用安省累计
    if total_on_m >= 24: return 12
    if total_on_m >= 13: return 9
    if total_on_m >= 6:  return 6
    return 0

def noa_points(inc):
    return 8 if inc >= 70000 else 6 if inc >= 50000 else 4 if inc >= 30000 else 0

def permit_points(permit):
    p = (permit or "").lower()
    if any(k in p for k in ("work","pgwp","closed","open")): return 10
    if "study" in p: return 5
    return 0

def edu_points(edu):
    e = (edu or "").lower()
    if any(k in e for k in ("phd","doctor")): return 10
    if "master" in e: return 8
    if "bachelor" in e or "above a bachelor" in e: return 6
    if any(k in e for k in ("diploma","certificate","apprentic","trade","cegep")): return 5
    return 0

def lang_points(clb):
    if clb is None: return None
    return 15 if clb >= 9 else 12 if clb == 8 else 8 if clb == 7 else 4 if clb == 6 else 0

def region_points(region):
    r = (region or "").lower()
    if "north" in r: return 15
    if any(k in r for k in ("east","central","southwest","outside gta")): return 10
    if "gta" in r and "toronto" not in r: return 5
    return 0  # Toronto 或未知按 0

def normalize_noc(noc):
    """从 NOC 返回 (teer, major_category). TEER=NOC第二位, 大类=NOC首位."""
    n = str(noc).strip()
    if not n.isdigit() or len(n) < 2:
        return None, None
    teer = int(n[1])          # NOC 第2位
    major = int(n[0])         # NOC 首位 (broad occupational category)
    return teer, major

def evaluate_oinp(profile, warnings):
    """returns (breakdown, total, ref_cap). ref_cap = 因子最高分参考合计(非官方满分)."""
    bd = []
    noc = profile.get("noc")
    teer = profile.get("teer")
    major = profile.get("nocCategory")
    if noc and (teer is None or major is None):
        teer, major = normalize_noc(noc)
        if teer is not None:
            warnings.append(f"已由 NOC {noc} 推导: TEER={teer}, 职业类别={major}")

    # 1 TEER
    t_pts = teer_points(teer) if teer is not None else None
    bd.append({"item": "NOC TEER", "condition": f"TEER {teer}" if teer is not None else "缺NOC", "points": t_pts, "ref_max": 9, "source": "官方页 line 588-597"})

    # 2 职业类别
    c_pts = OCC_CAT.get(major) if major is not None else None
    bd.append({"item": "职业类别(broad occ. category)", "condition": f"Category {major}" if major is not None else "缺NOC", "points": c_pts, "ref_max": 10, "source": "官方页 line 603-607 (=NOC大类号)"})

    # 3 时薪
    w = profile.get("hourlyWage")
    bd.append({"item": "时薪", "condition": f"${w}/h" if w is not None else "缺", "points": wage_points(w) if w is not None else None, "ref_max": 15, "source": "官方页 line 612-617"})

    # 4 工龄
    cm = profile.get("currentJobMonths"); tom = profile.get("ontarioTotalMonths")
    bd.append({"item": "安省工龄", "condition": f"现职{cm}m/安省累计{tom}m" if (cm is not None or tom is not None) else "缺", "points": exp_points(cm or 0, tom or 0), "ref_max": 18, "source": "官方页 line 620-628"})

    # 5 NOA
    inc = profile.get("latestNOAEarnings")
    bd.append({"item": "CRA NOA年收入", "condition": f"${inc}" if inc is not None else "缺", "points": noa_points(inc) if inc is not None else None, "ref_max": 8, "source": "官方页 line 637-640"})

    # 6 身份
    permit = profile.get("permitType")
    bd.append({"item": "加拿大身份", "condition": (permit or "缺").upper(), "points": permit_points(permit), "ref_max": 10, "source": "官方页 line 643-645"})

    # 7 学历
    edu = profile.get("highestEducation")
    bd.append({"item": "最高学历", "condition": (edu or "缺").title(), "points": edu_points(edu), "ref_max": 10, "source": "官方页 line 649-657"})

    # 8 加拿大证书
    cc = profile.get("canadianCredentialsCount")
    cc_pts = 10 if (cc or 0) >= 2 else 5 if cc == 1 else 0
    bd.append({"item": "加拿大证书数", "condition": f"{cc} 证" if cc is not None else "缺", "points": cc_pts if cc is not None else None, "ref_max": 10, "source": "官方页 line 662-664"})

    # 9 语言
    clb = profile.get("lowestCLB")
    bd.append({"item": "语言(最低CLB)", "condition": f"CLB {clb}" if clb is not None else "缺", "points": lang_points(clb), "ref_max": 15, "source": "官方页 line 673-677"})

    # 10 双语 (官方: 2门=10, 1门=5)
    bi = profile.get("isBilingual")
    bi_pts = 10 if bi else 5
    bd.append({"item": "双语(2门官方语言均CLB6+)", "condition": "双语" if bi else "单语", "points": bi_pts, "ref_max": 10, "source": "官方页 line 679-681 (单语=5)"})

    # 11 区域
    reg = profile.get("workRegion")
    bd.append({"item": "工作地点区域", "condition": (reg or "缺").title(), "points": region_points(reg), "ref_max": 15, "source": "官方页 line 688-693"})

    total = sum(i["points"] for i in bd if isinstance(i["points"], int))
    ref_cap = 9+10+15+18+8+10+10+10+15+10+15  # 130 reference cap (非官方满分)
    return bd, total, ref_cap

def eligibility_gate(profile, warnings):
    """前置资格核验: 不满足时给出明确阻断."""
    has_offer = profile.get("hasJobOffer")
    if has_offer is not True:
        warnings.append("通道A前置门槛: 需 job offer + 雇主已在 Employer Portal 申请职位获批, 拿到 Job Offer ID 后 30 天内注册 EOI。当前未确认 offer, EOI 分数仅作参考, 不构成获邀保证。")
    return warnings

def main():
    raw = sys.stdin.read().strip()
    if raw:
        try:
            profile = json.loads(raw)
        except Exception as e:
            print(json.dumps({"error": f"JSON parse error: {e}"}, ensure_ascii=False)); sys.exit(1)
    else:
        # 示例候选人 (仅供演示)
        profile = {
            "age": 30, "hasSpouse": False,
            "noc": "21232",  # 软件工程师, TEER1, 大类2
            "hourlyWage": 41.0,
            "currentJobMonths": 14, "ontarioTotalMonths": 14,
            "latestNOAEarnings": 72000,
            "permitType": "PGWP",
            "highestEducation": "Master",
            "canadianCredentialsCount": 1,
            "lowestCLB": 9,
            "isBilingual": False,
            "workRegion": "Northern Ontario",
            "hasJobOffer": True
        }

    warnings = []
    eligibility_gate(profile, warnings)
    bd, total, ref_cap = evaluate_oinp(profile, warnings)

    print("=" * 66)
    print("ontario-immigration-expert — OINP Ontario Workforce Priority EOI 算分")
    print("=" * 66)
    print(f"{'项目':<28}{'条件':<22}{'分':>4}{'/max':>6}")
    print("-" * 66)
    for r in bd:
        pts = r["points"]
        pts_s = str(pts) if pts is not None else "(缺)"
        print(f"{r['item']:<24}{r['condition']:<26}{pts_s:>4}{('/'+str(r['ref_max'])):>6}")
    print("-" * 66)
    print(f"合计(仅计入可确认项)      {total:>30}")
    print(f"因子参考上限(非官方满分)  {ref_cap:>30}")
    print("============================================================")
    for w in warnings:
        print("⚠", w)
    print("### 以官方最终 OINP 决定为准 ###")

if __name__ == "__main__":
    main()
