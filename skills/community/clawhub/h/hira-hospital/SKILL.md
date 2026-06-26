---
name: hira-hospital
description: HIRA hospital information search API
version: 3.2.0
author: chumjibot
created: 2026-02-10
updated: 2026-02-19
tags: [hospital, medical, korea, openapi, data.go.kr]
connectors: [~~hospital, ~~search, ~~notify]
---

# Hospital Info Skill

HIRA (Health Insurance Review & Assessment Service) hospital search + detail lookup.

## Overview

| Service | ID | Endpoint | Purpose |
|---------|-----|----------|---------|
| Hospital Info | 15001698 | `hospInfoServicev2` | Hospital list search |
| Detail Info | 15001699 | `MadmDtlInfoService2.7` | Departments, hours, transport |

| Key | Value |
|-----|-------|
| Auth | `~/.config/data-go-kr/api_key` |
| Base URL | `https://apis.data.go.kr/B551182/` |
| Legal basis | National Health Insurance Act §43 |

## Scripts

```
scripts/
├── hospital_search.sh  → Search hospitals (name/region/type/dept)
└── hospital_detail.sh  → Hospital detail (parallel API calls)
```

## Workflow

### Step 1: Parse search criteria
- "근처 이비인후과" → region + department search
- "서울대병원 진료시간" → specific hospital detail
- ~~search to supplement hospital name/location

### Step 2: Search hospitals
- `hospital_search.sh [criteria]`

### Step 3: Detail lookup (if needed)
- `hospital_detail.sh [institution_code]`

### Step 4: Structured response

## Output Template

```markdown
## 🏥 [Query] Hospital Results

| Hospital | Type | Address | Phone | Departments |
|----------|------|---------|-------|-------------|

### [Hospital Name] Detail (on request)
- 📍 Address: ...
- ☎️ Phone: ...
- 🕐 Hours: ...
- 🚗 Transport: ...
```

## Connectors

| Placeholder | Purpose | Current Tool |
|-------------|---------|-------------|
| `~~hospital` | Hospital API | HIRA data.go.kr |
| `~~search` | Name/location supplement | Brave Search |
| `~~notify` | Alerts | Telegram |

## Intent Router

| Intent | Trigger Examples | Strategy |
|--------|-----------------|----------|
| Quick Search | "근처 이비인후과", "강남 피부과", "소아과 찾아줘" | `hospital_search.sh` → 지역+진료과목 검색 → 목록 |
| Detail Lookup | "이 병원 정보 자세히", "진료시간 알려줘", "주차 되나?" | `hospital_detail.sh` → 진료시간, 교통, 진료과목 상세 |

**Routing logic:** 검색/찾기/추천 → Quick Search, 특정 병원 + 상세/시간/교통 → Detail Lookup

## Cross-Skill Integration

| Trigger | Target Skill | Integration |
|---------|-------------|-------------|
| 병원 검색 결과 보충 | `web_search` (Brave) | 병원 리뷰·평판·홈페이지 보충 검색 |
| 외출 시 참고 | `kma-weather` | 비/추위 예보 시 "따뜻하게 입고 가세요" 팁 |

---
*Cowork architecture v3.2 — 🦞 chumjibot (2026-02-19)*

## 🔧 Setup (공공데이터 포털 API)

1. [data.go.kr](https://www.data.go.kr) 회원가입
2. 로그인 → 마이페이지 → **일반 인증키(Decoding)** 복사
3. API 키 저장:
   ```bash
   mkdir -p ~/.config/data-go-kr
   echo "YOUR_API_KEY" > ~/.config/data-go-kr/api_key
   ```
4. 아래 서비스 **활용신청** 후 사용 (자동승인)
   - [심평원 병원 정보](https://www.data.go.kr/data/15001698/openapi.do) (15001698)
