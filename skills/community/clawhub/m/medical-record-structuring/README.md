# Medical Record Structuring · 中文病历结构化

[English](#english) | [中文](#chinese)

---

## English

Convert unstructured Chinese clinical narratives into structured JSON aligned with HL7 FHIR R4 and Chinese national EMR standards (WS 445-2014, ICD-10, ICD-9-CM-3).

### Quick Start

```bash
# After installing the skill
echo "$RECORD_TEXT" | python3 scripts/run_pipeline.py \
  --record-type admission \
  --output /tmp/extracted.json
python3 scripts/render_preview.py /tmp/extracted.json
```

### Installation

```bash
# From ClawHub
openclaw skills install medical-record-structuring

# From SkillHub.cn
openclaw skills install medical-record-structuring
```

### Features

- 🏥 8 entity groups: patient demographics, chief complaint, history, vitals, diagnosis, medication, procedure, lab results
- 🔢 ICD-10 / ICD-9-CM-3 / LOINC code normalization
- 📋 HL7 FHIR R4 Bundle output
- 🔒 PII masking by default, no external network calls
- 📍 Full provenance: every extracted field traces back to source text span
- ⚠️ Low-confidence flagging for human review

### Privacy & Safety

This skill processes potentially sensitive medical data. By design:
- All processing is local; no network calls
- PII is masked in preview output
- Output is data extraction only, never clinical advice

See [SKILL.md](./SKILL.md) for full documentation.

### License

MIT-0 (see LICENSE)

---

## Chinese

将非结构化中文临床文本转换为符合 HL7 FHIR R4 与国家电子病历规范（WS 445-2014）的结构化 JSON。

### 快速开始

```bash
echo "$RECORD_TEXT" | python3 scripts/run_pipeline.py \
  --record-type admission \
  --output /tmp/extracted.json
python3 scripts/render_preview.py /tmp/extracted.json
```

### 安装

```bash
# ClawHub
openclaw skills install medical-record-structuring

# SkillHub
openclaw skills install medical-record-structuring
```

### 功能

- 🏥 8 大类抽取：患者信息、主诉、病史、生命体征、诊断、用药、操作、化验
- 🔢 ICD-10 / ICD-9-CM-3 / LOINC 编码归一
- 📋 HL7 FHIR R4 Bundle 输出
- 🔒 默认 PII 脱敏，零外部网络请求
- 📍 完整溯源：每个抽取字段可定位回原文片段
- ⚠️ 低置信度自动标记供人工复核

### 隐私与安全

本技能处理敏感医疗数据，设计上：
- 全部本地处理，无网络请求
- 预览中 PII 自动脱敏
- 仅数据抽取，绝不输出临床建议

详见 [SKILL.md](./SKILL.md)

### 协议

MIT-0（见 LICENSE）
