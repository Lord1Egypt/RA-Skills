\
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import math
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

SPECIALTY_RULES = {
    "呼吸内科": ["发热", "咳嗽", "咳痰", "气短", "胸闷", "哮喘", "呼吸"],
    "感染科": ["发热", "感染", "病毒", "咽痛"],
    "心内科": ["胸痛", "胸闷", "心悸", "心前区"],
    "骨科": ["膝痛", "膝关节疼痛", "关节", "扭伤", "骨折", "腰痛"],
    "运动医学科": ["运动损伤", "膝痛", "半月板", "扭伤"],
    "神经内科": ["头痛", "眩晕", "麻木", "无力"],
    "皮肤科": ["皮疹", "瘙痒", "过敏", "脱屑"],
    "消化内科": ["腹痛", "腹泻", "反酸", "恶心"],
    "儿科": ["儿童发热", "儿童咳嗽", "小儿", "宝宝", "孩子", "儿童"],
    "全科医学科": ["初诊", "不确定", "发热", "咳嗽", "腹痛", "皮疹"]
}

EMERGENCY_KEYWORDS = ["呼吸困难", "持续胸痛", "意识障碍", "大出血", "抽搐", "单侧无力", "口角歪斜", "言语不清"]

def load_json(name):
    with open(DATA_DIR / name, "r", encoding="utf-8") as f:
        return json.load(f)

def normalize_text(parts):
    return " ".join([str(p) for p in parts if p]).strip()

def detect_risk(text):
    for kw in EMERGENCY_KEYWORDS:
        if kw in text:
            return "高", f"命中急危重症关键词：{kw}，建议优先急诊或拨打 120。"
    if any(kw in text for kw in ["高热", "持续高热", "症状加重"]):
        return "中", "存在需要尽快线下就诊的信号，建议优先近期号源。"
    return "低", "暂未命中急危重症关键词，可做普通门诊匹配。"

def infer_specialties(text, age=None):
    scores = {}
    is_child = age is not None and age < 14
    for dept, kws in SPECIALTY_RULES.items():
        score = sum(1 for kw in kws if kw in text)
        if score > 0:
            scores[dept] = score
    if is_child:
        scores["儿科"] = scores.get("儿科", 0) + 3
    if not scores:
        scores["全科医学科"] = 1
    ordered = sorted(scores.items(), key=lambda x: (-x[1], x[0]))
    return [d for d, _ in ordered[:3]]

def title_score(title):
    if "主任" in title:
        return 1.0
    if "副主任" in title:
        return 0.9
    if "主治" in title:
        return 0.75
    return 0.6

def level_score(level):
    if "三甲" in level:
        return 1.0
    if "二甲" in level:
        return 0.8
    return 0.6

def region_score(user_region, hospital_region):
    if not user_region:
        return 0.5
    return 1.0 if user_region == hospital_region else 0.6

def find_next_slot(doctor_id, slots):
    candidates = [s for s in slots if s["doctor_id"] == doctor_id and s.get("available")]
    if not candidates:
        return None
    candidates = sorted(candidates, key=lambda x: (x["date"], x["time"]))
    return candidates[0]

def specialty_match_score(target_specialties, doctor_specialties, doctor_dept, text):
    score = 0.0
    if doctor_dept in target_specialties:
        score += 0.6
    for kw in doctor_specialties:
        if kw in text:
            score += 0.08
    return min(score, 1.0)

def fee_preference_score(user_budget, doctor_fee):
    if not user_budget:
        return 0.7
    mapping = {"低": 1, "中": 2, "高": 3}
    u = mapping.get(user_budget, 2)
    d = mapping.get(doctor_fee, 2)
    diff = abs(u - d)
    return {0: 1.0, 1: 0.75, 2: 0.5}.get(diff, 0.5)

def build_recommendations(req):
    hospitals = load_json("mock_hospitals.json")
    doctors = load_json("mock_doctors.json")
    slots = load_json("mock_slots.json")

    user = req.get("user_profile", {})
    text = normalize_text([
        req.get("chief_complaint"),
        req.get("history"),
        " ".join(req.get("symptoms", [])),
    ])
    region = req.get("current_region")
    risk_level, risk_note = detect_risk(text)
    target_specialties = infer_specialties(text, user.get("age"))

    hospital_map = {h["hospital_id"]: h for h in hospitals}
    recs = []

    for doctor in doctors:
        hospital = hospital_map[doctor["hospital_id"]]
        if doctor["department"] not in hospital["departments"]:
            continue

        dept_hit = doctor["department"] in target_specialties
        specialty_score = specialty_match_score(target_specialties, doctor["specialties"], doctor["department"], text)
        if specialty_score <= 0 and not dept_hit:
            continue

        next_slot = find_next_slot(doctor["doctor_id"], slots)
        availability_score = 1.0 if next_slot else 0.3

        score = (
            specialty_score * 40
            + (1.0 if dept_hit else 0.6) * 20
            + title_score(doctor["title"]) * 10
            + region_score(region, hospital["region"]) * 10
            + (doctor["rating"] / 5.0) * 10
            + availability_score * 5
            + fee_preference_score(user.get("budget_level"), doctor["fee_level"]) * 5
        )
        score += level_score(hospital["level"]) * 5
        score += (1.0 if hospital.get("supports_insurance") and user.get("insurance") else 0.5) * 5

        reasons = []
        if dept_hit:
            reasons.append(f"科室与推断目标科室“{doctor['department']}”一致")
        matched_kw = [kw for kw in doctor["specialties"] if kw in text]
        if matched_kw:
            reasons.append(f"医生擅长方向覆盖：{', '.join(matched_kw[:3])}")
        if region == hospital["region"]:
            reasons.append("医院与用户所在区域一致")
        if next_slot:
            reasons.append(f"近期可约：{next_slot['date']} {next_slot['time']}")
        reasons.append(f"医院等级：{hospital['level']}，医生评分：{doctor['rating']}")

        recs.append({
            "hospital_id": hospital["hospital_id"],
            "hospital_name": hospital["name"],
            "hospital_region": hospital["region"],
            "doctor_id": doctor["doctor_id"],
            "doctor_name": doctor["name"],
            "department": doctor["department"],
            "doctor_title": doctor["title"],
            "match_score": round(score, 2),
            "next_available_slot": f"{next_slot['date']} {next_slot['time']}" if next_slot else "暂无可用号源",
            "reason": "；".join(reasons)
        })

    recs = sorted(recs, key=lambda x: (-x["match_score"], x["hospital_name"], x["doctor_name"]))
    return risk_level, risk_note, target_specialties, recs[:3]

def simulate_registration(req, recommendations):
    if not req.get("need_registration") or not recommendations:
        return {"enabled": False, "message": "未请求模拟挂号或无可推荐结果。"}
    top = recommendations[0]
    if "暂无可用号源" in top["next_available_slot"]:
        return {"enabled": False, "message": "目标医生暂无可用号源。"}
    return {
        "enabled": True,
        "booking_id": f"REG-{uuid.uuid4().hex[:8].upper()}",
        "hospital_name": top["hospital_name"],
        "doctor_name": top["doctor_name"],
        "department": top["department"],
        "appointment_time": top["next_available_slot"],
        "note": "这是模拟挂号结果，未连接真实医院挂号系统。"
    }

def simulate_escort(req, registration):
    companions = load_json("mock_companions.json")
    if not req.get("need_escort"):
        return {"enabled": False, "message": "未请求陪诊。"}
    region = req.get("current_region", "")
    matches = [c for c in companions if region in c["regions"]]
    if not matches:
        return {"enabled": False, "message": "当前区域暂无模拟陪诊员。"}
    matches = sorted(matches, key=lambda x: -x["rating"])
    chosen = matches[0]
    appt_time = registration.get("appointment_time", "待确认")
    return {
        "enabled": True,
        "escort_order_id": f"ESC-{uuid.uuid4().hex[:8].upper()}",
        "companion_name": chosen["name"],
        "service_area": region,
        "service_time": appt_time,
        "service_tags": chosen["service_tags"],
        "note": "这是模拟陪诊安排，未连接真实陪诊平台。"
    }

def main():
    parser = argparse.ArgumentParser(description="基于模拟数据的医院医生推荐脚本")
    parser.add_argument("--input", required=True, help="输入 JSON 文件")
    parser.add_argument("--output", required=False, help="输出 JSON 文件")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        req = json.load(f)

    risk_level, risk_note, target_specialties, recommendations = build_recommendations(req)
    registration = simulate_registration(req, recommendations)
    escort = simulate_escort(req, registration)

    case_summary = f"主诉：{req.get('chief_complaint', '')}；病史：{req.get('history', '')}；地区：{req.get('current_region', '')}"
    notes = [
        "本结果用于就医分流与预约建议，不替代医生面诊。",
        "若出现呼吸困难、持续胸痛、意识障碍等情况，应优先急诊。",
        "挂号与陪诊为模拟流程。"
    ]

    result = {
        "case_summary": case_summary,
        "risk_level": risk_level,
        "risk_note": risk_note,
        "recommended_specialties": target_specialties,
        "top_recommendations": recommendations,
        "registration": registration,
        "escort": escort,
        "notes": notes
    }

    output_text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_text)
    else:
        print(output_text)

if __name__ == "__main__":
    main()
