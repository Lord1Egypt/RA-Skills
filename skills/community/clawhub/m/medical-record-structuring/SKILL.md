---
name: medical-record-structuring
description: |
  EN: Convert unstructured Chinese clinical narratives (admission notes, progress notes, discharge summaries, outpatient records) into structured JSON aligned with HL7 FHIR R4 and Chinese national EMR standards (WS 445-2014, ICD-10, ICD-9-CM-3). Use when the user provides medical text and asks to "结构化 / 抽取 / 解析病历 / 转 FHIR / extract diagnoses / parse EMR".
  中文：将非结构化中文临床文本（入院记录、病程记录、出院小结、门诊病历）转换为符合 HL7 FHIR R4 与国家电子病历共享文档规范（WS 445-2014、ICD-10、ICD-9-CM-3）的结构化 JSON。当用户提供病历文本并要求"结构化/抽取实体/解析病历/转FHIR"时触发。
version: 1.0.0
metadata:
  openclaw:
    emoji: "🏥"
    homepage: https://github.com/openclaw-skills/medical-record-structuring
    requires:
      bins:
        - python3
    envVars:
      - name: MEDICAL_NER_MODEL
        required: false
        description: Optional override for the local NER model path. Defaults to bundled rule-based extractor.
      - name: ICD10_DB_PATH
        required: false
        description: Optional path to a custom ICD-10 code database (CSV/SQLite). Defaults to bundled WHO 2019 Chinese mapping.
---

# Medical Record Structuring · 中文病历结构化

> Production-grade extraction of clinical entities from Chinese free-text medical records into FHIR R4 + WS 445-2014 compliant JSON.
>
> 将中文自由文本病历精准抽取为符合 FHIR R4 与国标 WS 445-2014 的结构化 JSON。

---

## 🎯 When to Use · 何时使用

**Trigger keywords (中文):** 结构化病历、病历抽取、电子病历解析、入院记录抽取、出院小结结构化、ICD 编码、症状抽取、用药抽取、FHIR 转换、临床实体识别、病历归一化

**Trigger keywords (EN):** structure EMR, parse clinical notes, extract diagnosis, FHIR conversion, ICD coding, clinical NER, normalize medical record

**Typical inputs:**
- 入院记录 / Admission notes
- 病程记录 / Progress notes
- 出院小结 / Discharge summaries
- 门诊病历 / Outpatient records
- 化验单文本 / Lab report text

**Do NOT use when:**
- User wants medical diagnosis or treatment advice (this skill structures data only, no clinical decisions)
- Input is an image/PDF without OCR text (use `smart-ocr` skill first)
- Input is not clinical content

---

## 📋 Extraction Schema · 抽取字段

The skill extracts 8 core entity groups per record:

| 字段组 / Group | 字段示例 / Fields | FHIR Resource | 国标依据 |
|---|---|---|---|
| 患者基本信息 Patient | 姓名、性别、年龄、住院号 | Patient | WS 445.1 |
| 主诉与现病史 Chief Complaint & HPI | 主诉、起病时间、伴随症状 | Condition + Observation | WS 445.4 |
| 既往史 Past History | 慢性病、手术史、过敏史 | AllergyIntolerance, Condition | WS 445.5 |
| 生命体征 Vitals | T/P/R/BP/SpO2 | Observation (vital-signs) | LOINC |
| 诊断 Diagnosis | 主要诊断、次要诊断 + ICD-10 | Condition | ICD-10 (GB/T 14396) |
| 药物医嘱 Medication | 药品名、剂量、频次、用法 | MedicationRequest | RxNorm + NMPA |
| 手术操作 Procedure | 术式 + ICD-9-CM-3 | Procedure | ICD-9-CM-3 |
| 化验结果 Lab Results | 检验项、结果值、参考范围、异常标志 | Observation (laboratory) | LOINC |

---

## 🔄 Extraction Protocol · 抽取流程

### Step 1: Input validation · 输入校验

```bash
python3 scripts/validate_input.py --input <path-or-stdin>
```

- Reject if input < 20 Chinese chars or contains no clinical keywords
- Auto-detect record type (admission / progress / discharge / outpatient / lab)
- Sanitize PII display per user privacy preference (`--mask-pii` flag)

### Step 2: Section segmentation · 章节切分

Use `scripts/segment_sections.py` to split the record into standard sections:
- 主诉 (Chief Complaint)
- 现病史 (History of Present Illness)
- 既往史 (Past History)
- 个人史/家族史 (Personal/Family History)
- 体格检查 (Physical Exam)
- 辅助检查 (Auxiliary Exam)
- 初步诊断 / 出院诊断 (Diagnosis)
- 诊疗经过 (Treatment Course)
- 出院医嘱 (Discharge Instructions)

### Step 3: Entity extraction · 实体抽取

Two-stage hybrid extraction:
1. **Rule-based pass** — high-precision regex + dictionary lookup for vitals, drugs, ICD codes, units, dates (`scripts/rule_extract.py`)
2. **LLM pass** — semantic extraction for symptoms, severity, temporal relations using the assistant's own LLM with the prompt template in `templates/extraction_prompt.md`

### Step 4: Code normalization · 编码归一化

- Map free-text diagnoses → ICD-10 codes via `knowledge/icd10_zh.csv` (10,000+ Chinese terms)
- Map drug names → NMPA generic names via `knowledge/drug_aliases.csv`
- Map lab tests → LOINC codes via `knowledge/lab_loinc.csv`

### Step 5: FHIR bundle assembly · FHIR 资源组装

```bash
python3 scripts/assemble_fhir.py --extracted entities.json --output bundle.json
```

Output: a FHIR R4 `Bundle` (`type: collection`) containing all derived resources, plus a sidecar `provenance.json` recording extraction source spans for auditability.

### Step 6: Validation · 校验

```bash
python3 scripts/validate_fhir.py bundle.json
```

Checks:
- FHIR R4 schema conformance (via embedded JSON Schema)
- Required WS 445 fields present
- ICD codes exist in code system
- Drug doses within plausible ranges (flag outliers, do not silently drop)

---

## 📤 Output Format · 输出格式

Default output is a JSON object with three top-level keys:

```json
{
  "fhir_bundle": { /* FHIR R4 Bundle */ },
  "ws445_summary": { /* 国标关键字段速览 */ },
  "extraction_report": {
    "record_type": "discharge_summary",
    "sections_found": ["主诉","现病史","既往史","体格检查","辅助检查","诊断","诊疗经过"],
    "entities_count": { "diagnosis": 3, "medication": 7, "lab": 12, "procedure": 1 },
    "low_confidence_spans": [ /* fields needing human review */ ],
    "warnings": [ /* e.g. inconsistent dates */ ]
  }
}
```

For human-readable preview, append `--format=markdown` to get a side-by-side table.

---

## ⚠️ Safety & Compliance · 安全合规

This skill is **data extraction only**, not a clinical decision tool. The following constraints are enforced:

1. **No diagnostic suggestion** — never infer diagnoses beyond what is literally stated in the source text.
2. **PII protection** — by default, patient name and ID are extracted but masked in any preview output (`王*三`, `***1234`). Full values stay only in the JSON output the caller controls.
3. **Audit trail** — every extracted field has a `source.span` pointer back to the original text offset for traceability.
4. **Low-confidence flagging** — entities with confidence < 0.7 are flagged in `low_confidence_spans` for human review rather than silently accepted.
5. **No external network calls** — all dictionaries are bundled locally. The skill never uploads patient data anywhere.

> 本技能仅做数据结构化，不提供任何临床诊断或治疗建议。患者隐私字段默认在预览中脱敏；所有抽取均可溯源；置信度低字段强制人工复核；技能本身不产生任何外部网络请求。

---

## 🚀 Usage Examples · 使用示例

### Example 1: Extract from admission note

User: "帮我把这段入院记录结构化：患者王某某，男，58岁，因'反复胸痛3月，加重1周'入院。既往有高血压病史10年，最高180/100mmHg，规律服用氨氯地平5mg qd..."

Agent:
```bash
echo "$RECORD_TEXT" | python3 scripts/run_pipeline.py --record-type admission --output /tmp/extracted.json
python3 scripts/render_preview.py /tmp/extracted.json
```

Returns a structured table preview + the full JSON path.

### Example 2: Batch process discharge summaries

```bash
python3 scripts/batch_process.py \
  --input-dir ./discharge_notes/ \
  --output-dir ./structured/ \
  --record-type discharge \
  --workers 4
```

### Example 3: FHIR-only output for downstream EMR

```bash
python3 scripts/run_pipeline.py \
  --input record.txt \
  --record-type outpatient \
  --fhir-only \
  --output bundle.fhir.json
```

See `examples/` for full input → output samples on real (anonymized) records.

---

## 🧪 Testing · 测试

Run the test suite to verify the installation:

```bash
cd tests && python3 -m unittest discover -v
```

Tests cover:
- Section segmentation accuracy on 12 canonical record formats
- ICD-10 mapping precision on 200 common diagnoses
- FHIR bundle schema validity
- PII masking correctness
- Edge cases: empty fields, conflicting dates, malformed lab values

---

## 📚 References · 参考资料

- HL7 FHIR R4: https://hl7.org/fhir/R4/
- WS 445-2014 电子病历基本数据集: NHFPC
- ICD-10 国家临床版 2.0
- ICD-9-CM-3 手术与操作分类
- LOINC: https://loinc.org

## 🏷️ Tags · 标签

`medical` `healthcare` `EMR` `FHIR` `ICD-10` `clinical-NER` `中文` `病历` `结构化`
