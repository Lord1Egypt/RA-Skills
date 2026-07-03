# Changelog

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this skill adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.3] - 2026-07-02

### Added
- **Multi-language template support** - Added English, Chinese, and MVTM simplified templates
  - `playbook/07-templates.md` - Standard English templates (complete, ~200 fields)
  - `playbook/07-templates-zh-CN.md` - Chinese templates with regulatory extensions (等保、数据出境、生成式AI备案)
  - `playbook/07-templates-mvtm.md` - MVTM simplified templates (~60 fields with auto-inheritance)
  - `playbook/07-template-guide.md` - Template selection guide with decision trees
  - `README-TEMPLATES.md` - Comprehensive template system documentation

- **Template language selection** - Users can now choose English or Chinese templates during setup
  - Added `template_language` field to state.json
  - Added `template_file` field to state.json
  - Added template selection step in Pre-Engagement (Step 2)

- **Chinese regulatory extensions** - 6 new fields in Business Context template
  - 等保级别 (Classification level per 《网络安全法》Art.21)
  - 数据出境要求 (Data export requirements per 《数据安全法》Art.31)
  - 重要数据/核心数据 (Important/Core data classification)
  - 生成式AI服务备案 (Generative AI service filing requirement)
  - AI安全风险分类 (AI security risk classification per 《人工智能安全治理框架》2.0)
  - 合规负责人 (Compliance officer for accountability)

- **Auto field inheritance** - MVTM templates support automatic field inheritance to reduce duplication
  - Business Context → Threat Identification (Criticality → Severity baseline)
  - Threat Actors → Threat Identification (Attack Vector → Attack Vector)
  - Trust Boundaries → Threat Identification (Boundary Strength → Attack Complexity)
  - Asset Flows → Threat Identification (Asset Classification → Affected Components)
  - Threat Identification → Mitigation Planning (Threat Level → Mitigation Priority)
  - Mitigation Planning → Residual Risk (Implementation Status → Residual Risk Calculation)

### Changed
- Updated state.json schema to version 1.2.0 with template fields
- Improved documentation with bilingual support (English/Chinese)
- Enhanced MVTM checklist with automated field population

### Fixed
- N/A (Initial release of template system)

## [1.0.2] - 2026-07-01

### Added
- Initial release to ClawHub
- Interactive Q&A threat modeling workflow
- MVTM Checklist mode (10-item minimum viable threat model)
- Full Assessment mode (10-phase comprehensive assessment)
- Multi-format output support (.md, .docx, .xlsx)
- AI risk classification mapping to 《人工智能安全治理框架》2.0

### Features
- Two analysis modes: MVTM Checklist and Full Assessment
- Dual decision tree: MAESTRO 5 questions + China-specific 5 criteria
- Supports agentic AI systems and OpenCode Skills
- Phases 6-10 can be auto-completed by AI
- Chinese regulatory compliance mapping

---

## Template System Overview

### Template Files Structure

```
playbook/
├── 07-templates.md              # Standard English templates (~200 fields)
├── 07-templates-zh-CN.md        # Chinese templates with regulatory extensions
├── 07-templates-mvtm.md         # MVTM simplified templates (~60 fields)
├── 07-template-guide.md         # Template selection guide
└── README-TEMPLATES.md          # Comprehensive documentation
```

### Template Comparison

| Template | Fields | Layers | Languages | Use Case |
|----------|--------|--------|-----------|----------|
| Standard English | ~200 | L1-L7+Cross | English | International teams, standard compliance |
| Standard Chinese | ~200 | L1-L7+Cross | Chinese + Regulatory | Chinese users, China compliance |
| MVTM Simplified | ~60 | L1-L4,L6 | English | Quick assessments, agile teams |

### Analysis Mode Decision Tree

```
Start
  ├─ Business critical? → Full Assessment
  ├─ Confidential/Restricted data? → Full Assessment
  ├─ Externally facing? → Standard Assessment
  ├─ Full autonomy? → Standard Assessment
  ├─ Multi-agent? → Standard Assessment
  └─ None of above → MVTM Checklist
```

### Version Schema

- **Playbook Version**: MAESTRO framework version (1.2.0)
- **Schema Version**: state.json structure version (1.2.0)
- **Template Version**: Template system version (1.0.0)
- **Skill Version**: This skill's version (1.0.3)

---

*For more details, see README-TEMPLATES.md*
