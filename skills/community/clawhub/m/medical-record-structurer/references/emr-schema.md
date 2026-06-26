# EMR Schema Reference

## Electronic Medical Record Structure

### Version 1.0 Schema

```json
{
  "emr_version": "1.0",
  "record_id": "EMR_YYYYMMDDHHMMSS",
  "record_date": "ISO8601 timestamp",
  "patient_demographics": {
    "name": "string",
    "gender": "Male|Female|Unknown",
    "age": "number|null",
    "date_of_birth": "string (optional)",
    "contact": "string (optional)"
  },
  "clinical_information": {
    "chief_complaint": "string - Primary reason for visit",
    "history_of_present_illness": "string - Detailed symptom description",
    "past_medical_history": "string - Previous conditions",
    "physical_examination": "string - Exam findings",
    "vital_signs": {
      "blood_pressure": "string (optional)",
      "heart_rate": "number (optional)",
      "temperature": "number (optional)",
      "respiratory_rate": "number (optional)"
    }
  },
  "assessment_and_plan": {
    "diagnosis": "string - Primary and secondary diagnoses",
    "treatment_plan": "string - Recommended treatments",
    "medications": "string - Prescribed medications",
    "follow_up_instructions": "string - Next steps",
    "referrals": "string (optional)"
  },
  "metadata": {
    "source_text": "string - Original input",
    "processed_at": "ISO8601 timestamp",
    "processor_version": "string"
  }
}
```

## Field Definitions

### Patient Demographics

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Patient full name |
| gender | enum | Yes | Male, Female, or Unknown |
| age | number | No | Patient age in years |
| date_of_birth | string | No | Date of birth (YYYY-MM-DD) |
| contact | string | No | Phone or email |

### Clinical Information

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| chief_complaint | string | Yes | Main symptom/reason for visit |
| history_of_present_illness | string | No | Detailed history |
| past_medical_history | string | No | Previous medical conditions |
| physical_examination | string | No | Physical exam findings |

### Assessment and Plan

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| diagnosis | string | Yes | Clinical diagnosis |
| treatment_plan | string | No | Treatment recommendations |
| medications | string | No | Prescribed drugs |
| follow_up_instructions | string | No | Follow-up care instructions |

## Supported Input Patterns

### Chinese Medical Notes

The processor recognizes common Chinese medical documentation patterns:

- 患者[姓名]，[性别]，[年龄]岁
- 主诉：[症状描述]
- 现病史：[详细描述]
- 体格检查：[检查结果]
- 诊断：[诊断结果]
- 治疗：[治疗方案]

### English Medical Notes

Standard English medical documentation:

- Patient [name], [gender], [age] years old
- Chief Complaint: [description]
- History of Present Illness: [description]
- Physical Examination: [findings]
- Diagnosis: [diagnosis]
- Treatment: [plan]

## Examples

### Example 1: Chinese Input

**Input:**
```
患者李四，男，56岁，主诉胸痛2小时。既往有高血压病史10年。
体格检查：血压160/95mmHg，心率88次/分。
诊断：急性冠脉综合征
治疗：给予阿司匹林300mg口服，建议住院进一步治疗。
```

**Output Fields:**
- name: "李四"
- gender: "男"
- age: 56
- chief_complaint: "胸痛2小时"
- history_present_illness: "胸痛2小时，既往有高血压病史10年"
- physical_examination: "血压160/95mmHg，心率88次/分"
- diagnosis: "急性冠脉综合征"
- treatment_plan: "给予阿司匹林300mg口服，建议住院进一步治疗"
- medications: "阿司匹林300mg"

### Example 2: English Input

**Input:**
```
Patient John Smith, Male, 45 years old. Chief complaint: headache for 3 days.
Physical exam: BP 130/80, HR 72, afebrile.
Diagnosis: Tension headache.
Treatment: Ibuprofen 400mg TID, rest, hydration.
```

**Output Fields:**
- name: "John Smith"
- gender: "Male"
- age: 45
- chief_complaint: "headache for 3 days"
- physical_examination: "BP 130/80, HR 72, afebrile"
- diagnosis: "Tension headache"
- treatment_plan: "Ibuprofen 400mg TID, rest, hydration"
- medications: "Ibuprofen 400mg TID"
