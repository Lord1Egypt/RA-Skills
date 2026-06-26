---
name: hospital
description: Help patients find suitable hospitals based on medical needs, location, hospital level, and specialties. Use when the user wants to find a hospital, compare hospitals, or get healthcare facility recommendations.
---

# Hospital (医院)

Help patients find suitable hospitals based on medical needs, location, hospital level, and specialties.

## Triggers

Activate on hospital search requests: "find hospital", "recommend hospital", "which hospital is good", "Grade A Tertiary hospital", "specialty hospital", "emergency", "inpatient", or hospital search queries.

**Before acting:** Clarify:
- Medical condition or symptoms
- Location preference (city/district)
- Urgency level (emergency vs routine)
- Hospital level preference (primary, secondary, tertiary)
- Public vs private preference

## Core Flow

1. **Assess Condition** — Emergency or routine? What specialty needed?
2. **Determine Hospital Level** — Match condition severity to hospital capability
3. **Filter by Location** — Consider patient's location and travel time
4. **Evaluate Hospitals** — Check level, specialties, reputation, facilities
5. **Recommend** — Provide 2-3 hospital options with reasoning

## Hospital Levels (China)

| Level | Name | Capabilities | Best For |
|-------|------|--------------|----------|
| Primary | 一级 (YiJi) | Basic care, common diseases | Minor illnesses, chronic disease management |
| Secondary | 二级 (ErJi) | General care, some specialties | Moderate conditions, surgery |
| Tertiary | 三级 (SanJi) | Comprehensive, advanced care | Complex conditions, rare diseases |
| Grade A Tertiary | 三甲 (SanJia) | Top-tier, research hospitals | Serious/complex cases, specialized treatment |

## Hospital Types

**General Hospitals (综合医院)**
- Multiple departments
- Handle various conditions
- Good for undiagnosed symptoms

**Specialized Hospitals (专科医院)**
- Focus on specific areas
- Often higher expertise in specialty
- Examples: Children's hospital, Cancer hospital, Eye hospital

**Community Health Centers (社区卫生服务中心)**
- Primary care, prevention
- Chronic disease management
- Close to residential areas

## Emergency vs Non-Emergency

**🚨 Go to ER Immediately (任何医院急诊):**
- Chest pain
- Difficulty breathing
- Severe bleeding
- Loss of consciousness
- Severe allergic reaction
- Major trauma

**🏥 Choose Hospital Based on Specialty:**
- Chronic conditions
- Planned procedures
- Specialist consultations
- Second opinions

## Specialty Hospital Guide

| Condition | Recommended Hospital Type |
|-----------|--------------------------|
| Pediatric issues | Children's Hospital |
| Cancer | Cancer Hospital / Oncology Center |
| Heart disease | Cardiovascular Hospital |
| Mental health | Psychiatric Hospital |
| Maternity | Maternity Hospital / Women's Hospital |
| Dental | Dental Hospital / Stomatology |
| Traditional Chinese Medicine | TCM Hospital |
| Infectious diseases | Infectious Disease Hospital |

## Evaluation Criteria

**Essential factors:**
- Hospital level (三级甲等 preferred for serious conditions)
- Specialty match
- Location and accessibility
- Emergency capabilities (if needed)

**Additional considerations:**
- Insurance acceptance
- Bed availability
- Doctor qualifications
- Equipment and facilities
- Patient reviews

## Output Format

For each recommended hospital:

**Hospital Name** - [Level] [Type]
- **Address:** Location
- **Level:** 三级甲等 / 三级乙等 / 二级等
- **Specialties:** Key departments
- **Strengths:** Notable capabilities
- **How to go:** Transportation options

## Important Notes

⚠️ **Medical Disclaimer:**
- This skill helps find hospitals but does NOT provide medical advice
- For life-threatening emergencies, call 120 immediately
- Hospital information may change; verify before visiting
- Always follow doctor's advice for treatment decisions

## Example Interactions

**User:** "北京看心脏病哪家医院好？"
**Response:** [推荐北京的心血管专科医院或三甲综合医院心内科]

**User:** "我肚子痛应该去什么医院？"
**Response:** 建议先去二级或以上综合医院消化内科。如果剧烈疼痛或伴有发热、呕吐，建议直接去三甲医院急诊。

**User:** "找附近的社区医院"
**Response:** [推荐附近的社区卫生服务中心，适合常见病、慢性病管理]
munity hospital nearby"
**Response:** [Recommended nearby community health service centers, suitable for common illnesses and chronic disease management]
