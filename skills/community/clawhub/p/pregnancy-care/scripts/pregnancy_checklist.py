# pregnancy_checklist.py

# A static checklist of pregnancy milestones and weekly advice.
# This data structure maps week ranges to specific tasks and advice.

CHECKLIST_DATA = {
    # First Trimester (Week 1-12)
    "first_trimester": {
        "milestones": [
            {
                "week_start": 6,
                "week_end": 8,
                "id": "early_ultrasound",
                "title": "早期B超检查 (Early Ultrasound)",
                "description": "确认宫内孕及胎心搏动。",
                "reminder_weeks_before": 1
            },
            {
                "week_start": 11,
                "week_end": 13,
                "id": "nt_scan",
                "title": "NT检查 (Nuchal Translucency Scan)",
                "description": "早期唐氏筛查的重要指标，需提前预约。",
                "reminder_weeks_before": 2
            },
            {
                "week_start": 12,
                "week_end": 12,
                "id": "registration",
                "title": "建档 (Hospital Registration)",
                "description": "在预定分娩的医院建立母子健康档案。",
                "reminder_weeks_before": 2
            }
        ],
        "advice": {
            "diet": "补充叶酸（每日0.4mg-0.8mg）；清淡饮食，少食多餐以缓解孕吐。",
            "lifestyle": "避免剧烈运动；远离烟酒及有害化学物质；注意休息。",
            "symptoms": "可能出现恶心、呕吐、嗜睡、乳房胀痛，属于正常早孕反应。"
        }
    },
    # Second Trimester (Week 13-27)
    "second_trimester": {
        "milestones": [
            {
                "week_start": 15,
                "week_end": 20,
                "id": "down_screening",
                "title": "唐氏筛查/无创DNA (Down's Screening / NIPT)",
                "description": "评估胎儿染色体异常风险。",
                "reminder_weeks_before": 1
            },
            {
                "week_start": 20,
                "week_end": 24,
                "id": "anomaly_scan",
                "title": "大排畸B超 (Anomaly Scan)",
                "description": "详细检查胎儿各器官发育情况，需提前一个月预约。",
                "reminder_weeks_before": 3
            },
            {
                "week_start": 24,
                "week_end": 28,
                "id": "ogtt",
                "title": "糖耐量试验 (OGTT)",
                "description": "筛查妊娠期糖尿病，需空腹抽血。",
                "reminder_weeks_before": 1
            }
        ],
        "advice": {
            "diet": "增加优质蛋白（鱼、肉、蛋、奶）；适量补钙和铁；控制糖分摄入。",
            "lifestyle": "可进行孕妇瑜伽、散步等适度运动；注意口腔卫生。",
            "symptoms": "早孕反应消失，胃口变好；可能出现便秘、腰酸、轻微水肿。"
        }
    },
    # Third Trimester (Week 28-40)
    "third_trimester": {
        "milestones": [
            {
                "week_start": 28,
                "week_end": 32,
                "id": "growth_scan",
                "title": "小排畸B超 (Growth Scan)",
                "description": "评估胎儿生长发育及羊水情况。",
                "reminder_weeks_before": 1
            },
            {
                "week_start": 36,
                "week_end": 37,
                "id": "gbs_check",
                "title": "B族链球菌检查 (GBS)",
                "description": "预防新生儿感染。",
                "reminder_weeks_before": 1
            },
            {
                "week_start": 36,
                "week_end": 40,
                "id": "weekly_checkup",
                "title": "每周产检 (Weekly Checkup)",
                "description": "胎心监护，评估宫颈成熟度。",
                "reminder_weeks_before": 0
            }
        ],
        "advice": {
            "diet": "控制体重增长；少吃盐以预防水肿；多吃富含膳食纤维食物防便秘。",
            "lifestyle": "数胎动（早中晚各1小时）；准备待产包；练习拉玛泽呼吸法。",
            "symptoms": "尿频加重；耻骨痛；假性宫缩频繁（注意区分真假宫缩）。"
        }
    }
}

def get_trimester_data(weeks):
    if weeks < 13:
        return CHECKLIST_DATA["first_trimester"]
    elif weeks < 28:
        return CHECKLIST_DATA["second_trimester"]
    else:
        return CHECKLIST_DATA["third_trimester"]

def get_upcoming_milestones(current_weeks):
    """
    Returns a list of milestones that are coming up within the reminder window.
    """
    upcoming = []
    # Iterate through all trimesters to find relevant milestones
    for trimester in CHECKLIST_DATA.values():
        for milestone in trimester["milestones"]:
            start = milestone["week_start"]
            reminder_weeks = milestone.get("reminder_weeks_before", 1)
            
            # Logic: If current week is within [start - reminder, start]
            if (start - reminder_weeks) <= current_weeks <= start:
                upcoming.append(milestone)
    return upcoming
