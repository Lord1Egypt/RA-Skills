---
name: openviking-pro
description: AI 비용 96% 절약하는 클라우드 API. 설치 없이 바로 사용. 1개월 무료 체험. Trigger: "AI 비용", "토큰 절약", "API", "클라우드", "OpenViking".
compatibility: All platforms
---

# OpenViking Pro - AI 비용 96% 절약하는 클라우드 API

**설치 없이. API만 호출하면 끝.**

---

## 💰 비교하세요

| Before | After |
|--------|-------|
| 월 10만 원 | 월 4천 원 |
| 100,000 토큰 | 4,000 토큰 |
| **비용 폭증** | **96% 절약** |

---

## 🎯 뭐하는 거냐구요?

AI가 대화할 때마다 모든 걸 다시 읽어요. 비용이 계속 늘어나죠.

**OpenViking Pro**는 AI의 기억을 **클라우드에 압축**해서 저장해요.

- 설치 필요 없음
- API만 호출하면 끝
- 어디서든 접속 가능

**결과:** 토큰 96% 절약 → 돈 96% 절약

---

## 🚀 사용법

```python
import requests

# 저장
requests.post("https://api.openviking.pro/v1/memory/save", json={
    "uri": "memories/project",
    "content": "프로젝트 정보..."
})

# 검색 (토큰 96% 절약)
response = requests.post("https://api.openviking.pro/v1/memory/search", json={
    "query": "프로젝트",
    "level": 0  # 요약만
})
```

---

## 🎁 요금제

| Plan | 비용 | API Calls | 기능 |
|------|------|-----------|------|
| **무료 체험** | ₩0 | 무제한 | 1개월 |
| **Pro** | ₩9,000/월 | 1,000/일 | 팀 공유 |
| **Team** | ₩29,000/월 | 무제한 | 협업 기능 |

---

## ✅ 왜 쓰냐구요?

1. **설치 없음**: API만 호출
2. **비용 절약**: 월 10만 원 → 4천 원
3. **어디서든**: 클라우드라 어디서든
4. **팀 공유**: 여러 AI가 같은 DB 공유

---

## 🔧 어떻게 돌아가냐구요?

```
당신의 AI → API 호출 → OpenViking Pro → 압축된 기억 반환
                                    ↓
                              토큰 96% 절약
```

---

## 📦 API 엔드포인트

| Endpoint | 설명 |
|----------|------|
| `POST /v1/memory/save` | 기억 저장 |
| `POST /v1/memory/search` | 기억 검색 |
| `GET /v1/memory/list` | 기억 목록 |
| `GET /v1/usage` | 사용량 확인 |

---

## 📞 문의

- ClawHub: https://clawhub.com/skills/openviking-pro
- API: https://api.openviking.pro
- 이메일: support@openviking.pro

---

**지금 시작하세요. 1개월 무료.**

```python
import requests
# API Key 발급 후 바로 사용 가능
```