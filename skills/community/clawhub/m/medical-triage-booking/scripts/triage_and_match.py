#!/usr/bin/env python3
import argparse
import csv
import json
import math
import os
import re
from collections import defaultdict
from typing import Dict, List, Tuple


DEPARTMENT_RULES = [
    {
        "department": "呼吸与危重症医学科",
        "aliases": ["呼吸科", "呼吸内科", "肺病科"],
        "keywords": ["咳嗽", "咳痰", "发热", "发烧", "胸闷", "气短", "气喘", "呼吸困难", "哮喘", "肺炎", "肺结节", "鼻塞", "流感", "新冠", "支气管", "胸痛"],
    },
    {
        "department": "心血管科",
        "aliases": ["心内科", "心血管内科", "心脏科", "心脏中心"],
        "keywords": ["胸痛", "胸闷", "心慌", "心悸", "高血压", "血压高", "冠心病", "心绞痛", "气短", "头晕", "水肿"],
    },
    {
        "department": "神经科",
        "aliases": ["神经内科", "神经外科", "神经外一科"],
        "keywords": ["头痛", "眩晕", "头晕", "肢体麻木", "偏瘫", "抽搐", "癫痫", "面瘫", "失眠", "记忆力", "意识", "中风", "脑梗", "脑出血"],
    },
    {
        "department": "消化科",
        "aliases": ["消化内科", "内镜中心"],
        "keywords": ["腹痛", "胃痛", "反酸", "烧心", "呕吐", "恶心", "腹泻", "便秘", "黑便", "便血", "胃胀", "肝", "胆", "胰", "消化不良"],
    },
    {
        "department": "内分泌科",
        "aliases": ["糖尿病科"],
        "keywords": ["血糖", "糖尿病", "甲状腺", "肥胖", "消瘦", "多饮", "多尿", "内分泌", "痛风", "尿酸"],
    },
    {
        "department": "妇产科",
        "aliases": ["妇科", "中医妇科", "妇产科(含国际部妇产科病区"],
        "keywords": ["月经", "经期", "阴道", "白带", "宫颈", "子宫", "卵巢", "乳房", "怀孕", "妊娠", "备孕", "产检", "妇科"],
    },
    {
        "department": "泌尿外科",
        "aliases": ["泌尿科"],
        "keywords": ["尿频", "尿急", "尿痛", "血尿", "前列腺", "肾结石", "排尿", "泌尿", "腰痛"],
    },
    {
        "department": "皮肤科",
        "aliases": [],
        "keywords": ["皮疹", "瘙痒", "湿疹", "荨麻疹", "痘", "痤疮", "脱发", "皮肤", "红斑", "过敏"],
    },
    {
        "department": "眼科",
        "aliases": ["眼科特需门诊"],
        "keywords": ["眼痛", "视力", "视物模糊", "红眼", "流泪", "眼干", "飞蚊", "白内障", "青光眼"],
    },
    {
        "department": "口腔医学中心",
        "aliases": ["口腔科", "牙科"],
        "keywords": ["牙痛", "牙龈", "口腔", "智齿", "牙周", "口臭", "龋齿"],
    },
    {
        "department": "骨科",
        "aliases": ["骨科·关节外科", "骨科·脊柱外科", "脊柱二科"],
        "keywords": ["膝盖", "关节", "骨折", "扭伤", "腰椎", "脊柱", "颈椎", "肩痛", "骨痛", "运动损伤"],
    },
    {
        "department": "风湿免疫科",
        "aliases": ["风湿病科", "中医风湿病科"],
        "keywords": ["关节痛", "晨僵", "红斑狼疮", "风湿", "类风湿", "免疫", "干燥综合征"],
    },
    {
        "department": "心理科",
        "aliases": ["心身医学科"],
        "keywords": ["焦虑", "抑郁", "失眠", "情绪", "惊恐", "心理", "压力", "睡不着"],
    },
    {
        "department": "感染疾病科",
        "aliases": [],
        "keywords": ["乙肝", "丙肝", "感染", "发热", "传染", "艾滋", "结核"],
    },
    {
        "department": "肿瘤科",
        "aliases": ["中西医结合肿瘤内科", "放射肿瘤科"],
        "keywords": ["肿瘤", "癌", "结节", "化疗", "放疗", "靶向", "肿块"],
    },
    {
        "department": "康复医学科",
        "aliases": [],
        "keywords": ["康复", "术后恢复", "偏瘫康复", "理疗", "功能训练"],
    },
    {
        "department": "老年病科",
        "aliases": [],
        "keywords": ["老年", "多病共存", "高龄", "慢病管理"],
    },
    {
        "department": "综合科",
        "aliases": ["普通内科", "全科"],
        "keywords": ["不确定挂什么科", "多种症状", "体检异常", "慢病复诊"],
    },
]

EMERGENCY_KEYWORDS = [
    "持续胸痛", "胸痛大汗", "呼吸困难", "意识不清", "昏迷", "抽搐不止", "大出血", "便血很多", "黑便明显",
    "呕血", "偏瘫", "口角歪斜", "说话不清", "突发剧烈头痛", "高热惊厥", "严重过敏", "休克",
]

NON_CLINICAL_KEYWORDS = [
    "实验室", "药理", "病理", "放射", "职能", "共同制定", "自成立之日", "积极推行", "设有门诊", "临床药理室", "检验科", "输血科",
]


def normalize_text(value: str) -> str:
    if value is None:
        return ""
    value = str(value).strip()
    if value.lower() == "nan":
        return ""
    return value


def tokenize(text: str) -> List[str]:
    text = normalize_text(text)
    cjk = re.findall(r"[\u4e00-\u9fff]{2,}", text)
    latin = re.findall(r"[A-Za-z]{2,}", text)
    return cjk + latin


def keyword_hits(text: str, keywords: List[str]) -> Tuple[int, List[str]]:
    hits = []
    for kw in keywords:
        if kw and kw in text:
            hits.append(kw)
    return len(hits), hits


def infer_departments(symptom_text: str) -> Tuple[List[Dict], bool, List[str]]:
    emergency_count, emergency_hits = keyword_hits(symptom_text, EMERGENCY_KEYWORDS)
    emergency = emergency_count > 0

    scores = []
    for rule in DEPARTMENT_RULES:
        count, hits = keyword_hits(symptom_text, rule["keywords"])
        if count > 0:
            scores.append(
                {
                    "department": rule["department"],
                    "aliases": rule["aliases"],
                    "score": count,
                    "hits": hits,
                }
            )
    if not scores:
        scores = [{"department": "综合科", "aliases": ["普通内科", "全科"], "score": 1, "hits": ["症状描述不足，建议先做综合分诊"]}]
    scores.sort(key=lambda x: (-x["score"], x["department"]))
    return scores, emergency, emergency_hits


def load_rows(csv_path: str) -> List[Dict[str, str]]:
    rows = []
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({k: normalize_text(v) for k, v in row.items()})
    return rows


def row_is_clinical(row: Dict[str, str]) -> bool:
    dept = row.get("department_name", "")
    doctor = row.get("doctor_name", "")
    hospital = row.get("hospital_name", "")
    if not dept or not doctor:
        return False
    if doctor == dept or doctor == hospital:
        return False
    if ("科" in doctor or "中心" in doctor) and len(doctor) >= 2 and len(doctor) <= 12:
        return False
    for kw in NON_CLINICAL_KEYWORDS:
        if kw in dept:
            return False
    return True


def department_match_score(row: Dict[str, str], inferred: List[Dict]) -> Tuple[float, str]:
    dept_name = row.get("department_name", "")
    doctor_dept = row.get("doctor_department", "")
    best = 0.0
    reason = ""
    for cand in inferred:
        targets = [cand["department"]] + cand.get("aliases", [])
        for t in targets:
            if t and (t in dept_name or t in doctor_dept or dept_name in t or doctor_dept in t):
                score = 6.0 + cand["score"] * 1.5
                if score > best:
                    best = score
                    reason = f"科室匹配：{cand['department']}"
        # fuzzy fallback via shared chars
        overlap = len(set(dept_name) & set(cand["department"]))
        if overlap >= 2:
            score = 2.0 + overlap * 0.5 + cand["score"]
            if score > best:
                best = score
                reason = f"科室近似匹配：{cand['department']}"
    return best, reason


def content_match_score(row: Dict[str, str], symptom_text: str, inferred: List[Dict]) -> Tuple[float, List[str]]:
    bag = " ".join([
        row.get("hospital_name", ""),
        row.get("hospital_intro", ""),
        row.get("department_name", ""),
        row.get("department_intro", ""),
        row.get("doctor_name", ""),
        row.get("doctor_department", ""),
        row.get("doctor_intro", ""),
    ])
    score = 0.0
    reasons: List[str] = []
    symptom_tokens = set(tokenize(symptom_text))
    bag_tokens = set(tokenize(bag))
    overlap = symptom_tokens & bag_tokens
    if overlap:
        score += min(4.0, len(overlap) * 1.2)
        reasons.append("症状关键词重合：" + "、".join(sorted(list(overlap))[:4]))

    for cand in inferred[:3]:
        hits = [kw for kw in cand["hits"] if kw in bag]
        if hits:
            add = min(3.5, len(hits) * 1.0)
            score += add
            reasons.append(f"擅长/简介命中：{'、'.join(hits[:4])}")
            break

    schedule = row.get("doctor_schedule", "")
    if schedule:
        score += 0.5
        reasons.append("有坐诊时间信息")
    return score, reasons


def aggregate_rows(rows: List[Dict[str, str]], inferred: List[Dict], symptom_text: str, top_k: int) -> List[Dict]:
    scored = []
    for row in rows:
        if not row_is_clinical(row):
            continue
        d_score, d_reason = department_match_score(row, inferred)
        c_score, c_reasons = content_match_score(row, symptom_text, inferred)
        total = d_score + c_score
        if total <= 0:
            continue
        reasons = []
        if d_reason:
            reasons.append(d_reason)
        reasons.extend(c_reasons)
        scored.append(
            {
                "hospital_name": row.get("hospital_name", ""),
                "hospital_intro": row.get("hospital_intro", ""),
                "department_name": row.get("department_name", ""),
                "department_intro": row.get("department_intro", ""),
                "doctor_name": row.get("doctor_name", ""),
                "doctor_department": row.get("doctor_department", ""),
                "doctor_intro": row.get("doctor_intro", ""),
                "doctor_schedule": row.get("doctor_schedule", ""),
                "score": round(total, 2),
                "reasons": reasons[:4],
            }
        )

    # unique by hospital+department+doctor, keep best score
    best_by_key: Dict[Tuple[str, str, str], Dict] = {}
    for item in scored:
        key = (item["hospital_name"], item["department_name"], item["doctor_name"])
        old = best_by_key.get(key)
        if old is None or item["score"] > old["score"]:
            best_by_key[key] = item

    deduped = list(best_by_key.values())
    deduped.sort(key=lambda x: (-x["score"], x["hospital_name"], x["department_name"], x["doctor_name"]))
    return deduped[:top_k]


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Infer likely departments from symptoms and match top hospitals/doctors from a CSV dataset.")
    p.add_argument("--csv", required=True, help="Path to hospital_extracted_final.csv")
    p.add_argument("--symptoms", required=True, help="User symptom narrative")
    p.add_argument("--history", default="", help="Past history / chronic conditions / meds")
    p.add_argument("--age", default="", help="Age, optional")
    p.add_argument("--gender", default="", help="Gender, optional")
    p.add_argument("--top-k", type=int, default=3, help="How many matches to return")
    return p


def main() -> int:
    args = build_parser().parse_args()
    if not os.path.exists(args.csv):
        print(json.dumps({"error": f"CSV not found: {args.csv}"}, ensure_ascii=False))
        return 2

    symptom_text = "；".join([x for x in [args.symptoms, args.history, args.age, args.gender] if x])
    inferred, emergency, emergency_hits = infer_departments(symptom_text)
    rows = load_rows(args.csv)
    matches = aggregate_rows(rows, inferred, symptom_text, args.top_k)

    output = {
        "input": {
            "symptoms": args.symptoms,
            "history": args.history,
            "age": args.age,
            "gender": args.gender,
        },
        "emergency_flag": emergency,
        "emergency_hits": emergency_hits,
        "department_candidates": inferred[:5],
        "top_matches": matches,
        "notes": [
            "结果仅用于挂号分诊辅助，不替代医生诊断。",
            "若出现持续胸痛、明显呼吸困难、意识改变、偏瘫、抽搐不止、大出血等情况，应优先急诊。",
            "当前CSV中存在部分科研/实验室类行，脚本已尽量过滤，但仍建议人工复核。",
        ],
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
