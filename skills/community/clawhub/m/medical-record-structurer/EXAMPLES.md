# Examples

This document provides detailed examples of using the Medical Record Structurer skill.

## Table of Contents

1. [Basic Examples](#basic-examples)
2. [Chinese Medical Records](#chinese-medical-records)
3. [English Medical Records](#english-medical-records)
4. [Complex Cases](#complex-cases)
5. [Batch Processing](#batch-processing)
6. [Integration Examples](#integration-examples)

## Basic Examples

### Example 1: Simple Chief Complaint

**Input:**
```python
from scripts.process_record import process_medical_record

result = process_medical_record(
    input_text="患者张三，男，45岁，主诉头痛3天。",
    user_id="demo_user_001"
)

print(json.dumps(result, ensure_ascii=False, indent=2))
```

**Output:**
```json
{
  "success": true,
  "trial_mode": true,
  "trial_remaining": 9,
  "balance": null,
  "structured_record": {
    "emr_version": "1.0",
    "record_id": "EMR_20240306123045",
    "record_date": "2024-03-06T12:30:45",
    "patient_demographics": {
      "name": "张三",
      "gender": "男",
      "age": 45
    },
    "clinical_information": {
      "chief_complaint": "头痛3天",
      "history_of_present_illness": "",
      "past_medical_history": "",
      "physical_examination": ""
    },
    "assessment_and_plan": {
      "diagnosis": "",
      "treatment_plan": "",
      "medications": "",
      "follow_up_instructions": ""
    }
  }
}
```

### Example 2: Complete Outpatient Record

**Input:**
```python
record = """
患者李四，女，32岁，主诉腹痛2天，伴有恶心呕吐。
患者2天前进食油腻食物后出现上腹部疼痛，呈持续性隐痛，
伴有恶心呕吐，呕吐物为胃内容物。
既往体健，无慢性疾病史。
体格检查：体温37.8℃，血压120/80mmHg，
上腹部压痛，无反跳痛及肌紧张。
初步诊断：急性胃肠炎。
治疗方案：
1. 奥美拉唑20mg口服每日一次
2. 蒙脱石散3g口服每日三次
3. 清淡饮食，多饮水
建议休息3天，如症状加重及时就诊。
"""

result = process_medical_record(
    input_text=record,
    user_id="demo_user_002"
)
```

**Output:**
```json
{
  "success": true,
  "trial_mode": true,
  "trial_remaining": 8,
  "structured_record": {
    "emr_version": "1.0",
    "record_id": "EMR_20240306123115",
    "record_date": "2024-03-06T12:31:15",
    "patient_demographics": {
      "name": "李四",
      "gender": "女",
      "age": 32
    },
    "clinical_information": {
      "chief_complaint": "腹痛2天，伴有恶心呕吐",
      "history_of_present_illness": "患者2天前进食油腻食物后出现上腹部疼痛...",
      "past_medical_history": "既往体健，无慢性疾病史",
      "physical_examination": "体温37.8℃，血压120/80mmHg，上腹部压痛..."
    },
    "assessment_and_plan": {
      "diagnosis": "急性胃肠炎",
      "treatment_plan": "1. 奥美拉唑20mg口服每日一次 2. 蒙脱石散3g口服每日三次...",
      "medications": "奥美拉唑20mg，蒙脱石散3g",
      "follow_up_instructions": "建议休息3天，如症状加重及时就诊"
    }
  }
}
```

## Chinese Medical Records

### Example 3: Emergency Department Record

**Input:**
```python
record = """
急诊病历
患者王五，男，58岁，主诉胸痛2小时，伴有呼吸困难。
患者2小时前无明显诱因出现胸骨后压榨性疼痛，
向左肩及左上肢放射，伴有出汗、恶心。
既往有高血压病史10年，糖尿病史5年，吸烟史30年。
体格检查：
- 血压：160/95mmHg
- 心率：110次/分
- 呼吸：24次/分
- 体温：36.8℃
- 神志清楚，痛苦面容
初步诊断：
1. 急性冠脉综合征
2. 高血压病3级（极高危）
治疗方案：
1. 立即给予阿司匹林300mg嚼服
2. 硝酸甘油0.5mg舌下含服
3. 建立静脉通路，心电监护
4. 联系心内科会诊，准备介入治疗
"""

result = process_medical_record(input_text=record, user_id="demo_user_003")
```

### Example 4: Pediatric Record

**Input:**
```python
record = """
儿科门诊病历
患儿赵六，男，3岁，主诉发热咳嗽3天。
患儿3天前出现发热，体温最高39.5℃，伴有咳嗽，
呈阵发性连声咳，有痰不易咳出，无喘息。
精神食欲欠佳，大小便正常。
既往体健，按时接种疫苗。
体格检查：
- 体温：38.8℃
- 呼吸：32次/分
- 心率：120次/分
- 咽部充血，双肺呼吸音粗，可闻及散在湿啰音
初步诊断：急性支气管炎
治疗方案：
1. 布洛芬混悬液5ml口服，体温>38.5℃时使用
2. 氨溴索口服液2.5ml每日三次
3. 雾化吸入治疗（布地奈德+沙丁胺醇）
4. 多饮水，保持室内空气流通
5. 3天后复诊，如高热不退或呼吸困难及时就诊
"""

result = process_medical_record(input_text=record, user_id="demo_user_004")
```

## English Medical Records

### Example 5: SOAP Note

**Input:**
```python
record = """
Patient: John Smith
Age: 45, Male
Date: March 6, 2024

SUBJECTIVE:
Chief Complaint: Chest pain for 2 hours
History of Present Illness: Patient reports sudden onset of 
crushing chest pain radiating to left arm, associated with 
sweating and shortness of breath.
Past Medical History: Hypertension, Hyperlipidemia
Medications: Lisinopril 10mg daily, Atorvastatin 20mg daily
Allergies: NKDA

OBJECTIVE:
Vital Signs: BP 160/95, HR 110, RR 22, Temp 98.6F, O2Sat 96%
Physical Exam: Alert, diaphoretic, chest tenderness

ASSESSMENT:
1. Acute Coronary Syndrome
2. Hypertension, uncontrolled

PLAN:
1. Aspirin 325mg chewable
2. Nitroglycerin 0.4mg SL
3. Cardiology consult
4. Serial troponins
"""

result = process_medical_record(input_text=record, user_id="demo_user_005")
```

### Example 6: Progress Note

**Input:**
```python
record = """
Hospital Day 3
Patient: Mary Johnson, 67F

Subjective: Patient reports improved breathing today. 
Chest pain resolved. Able to walk to bathroom without 
shortness of breath.

Objective:
Vitals: T 98.2, BP 128/78, HR 82, RR 18, O2 97% RA
Exam: Lungs clear bilaterally, no edema

Assessment:
1. Community Acquired Pneumonia - improving
2. Type 2 Diabetes Mellitus - stable

Plan:
1. Continue ceftriaxone and azithromycin
2. Discharge planning - anticipate discharge tomorrow
3. Diabetes education referral
4. Follow up with PCP in 1 week
"""

result = process_medical_record(input_text=record, user_id="demo_user_006")
```

## Complex Cases

### Example 7: Multi-problem Visit

**Input:**
```python
record = """
患者孙七，女，72岁，主诉多系统不适。

主诉：
1. 头晕1周，伴乏力
2. 双下肢水肿3天
3. 血糖控制不佳

现病史：
患者1周来反复出现头晕，活动后加重，休息可缓解。
3天来发现双下肢水肿，按压有凹陷。
有2型糖尿病史15年，近期血糖监测空腹10-12mmol/L。

既往史：
- 2型糖尿病15年
- 高血压病10年
- 冠心病5年
- 慢性肾功能不全3年

体格检查：
血压：150/90mmHg
心率：88次/分
双下肢凹陷性水肿

诊断：
1. 高血压病3级（极高危）
2. 2型糖尿病
3. 冠心病
4. 慢性心力衰竭
5. 慢性肾功能不全

处理：
1. 调整降压方案：氨氯地平5mg每日一次
2. 调整降糖方案：二甲双胍0.5g每日三次
3. 呋塞米20mg每日一次利尿
4. 低盐糖尿病饮食
5. 心内科、内分泌科联合门诊随访
"""

result = process_medical_record(input_text=record, user_id="demo_user_007")
```

## Batch Processing

### Example 8: Processing Multiple Records

```python
from scripts.process_record import process_medical_record
import json

# List of records to process
records = [
    {
        "id": "REC001",
        "text": "患者张三，男，45岁，主诉头痛3天..."
    },
    {
        "id": "REC002",
        "text": "患者李四，女，32岁，主诉腹痛2天..."
    },
    {
        "id": "REC003",
        "text": "患者王五，男，58岁，主诉胸痛2小时..."
    }
]

# Process all records
results = []
for record in records:
    result = process_medical_record(
        input_text=record["text"],
        user_id="batch_user_001"
    )
    results.append({
        "id": record["id"],
        "result": result
    })
    
    # Check trial status
    if result.get("trial_remaining", 0) == 0:
        print("Warning: Free trial exhausted!")
        break

# Save results
with open("batch_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
```

## Integration Examples

### Example 9: Flask Web API

```python
from flask import Flask, request, jsonify
from scripts.process_record import process_medical_record

app = Flask(__name__)

@app.route('/api/structure', methods=['POST'])
def structure_record():
    data = request.json
    
    result = process_medical_record(
        input_text=data.get('text'),
        user_id=data.get('user_id')
    )
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
```

### Example 10: Command Line with File Input

```bash
# Create input file
cat > input.txt << 'EOF'
患者张三，男，45岁，主诉头痛3天。
既往有高血压病史。
体格检查：血压140/90mmHg。
诊断：高血压性头痛。
处理：给予布洛芬0.3g口服。
EOF

# Process file
python scripts/process_record.py \
  --input "$(cat input.txt)" \
  --user-id "cli_user_001" \
  --output result.json

# View result
cat result.json
```

## Sample Data Files

The `sample_data/` directory contains example medical records you can use for testing:

```bash
# List sample files
ls sample_data/

# Process a sample file
python demo.py --file sample_data/outpatient_record_01.txt
```

---

**See Also:**
- [Getting Started Guide](GETTING_STARTED.md)
- [FAQ](FAQ.md)
- [Security Policy](SECURITY.md)
