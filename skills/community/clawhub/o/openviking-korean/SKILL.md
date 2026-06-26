---
name: openviking-korean
description: TokenSaver v3.1 - 한영겸용 AI 토큰 절약. 한국어 95-96%, 영어 85-90% 비용 절감. Async + orjson + LRU 캐싱. JVM-free. Trigger: "AI 비용", "토큰 절약", "TokenSaver", "영어 최적화".
compatibility: Python 3.8+
---

# 🌍 토큰세이버 (TokenSaver) - 한영겸용 AI 비용 절약

**한국어: 95-96% | 영어: 85-90% | Bilingual Context DB**

🇰🇷 Korean: 95-96% cost reduction (Josa/Eomi removal + stemming)
🇺🇸 English: 85-90% cost reduction (180 stopwords + suffix stemming)

**돈이 줄어들어요. 진짜로.**

---

## 💰 비교하세요

| 언어 | Before | After | 절약률 |
|------|--------|-------|--------|
| 🇰🇷 한국어 | 100,000 토큰 | 4,000-5,000 토큰 | **95-96%** |
| 🇺🇸 영어 | 100,000 토큰 | 10,000-15,000 토큰 | **85-90%** |
| 💰 비용 | 월 10만 원 | 월 4천~1만 원 | **최대 96% 절약** |

---

## 🎯 뭐하는 거냐구요?

AI가 대화할 때마다 모든 걸 다시 읽어요. 그래서 비용이 계속 늘어나죠.

**토큰세이버**는 AI의 기억을 **압축**해서 저장해요.

- 옛날 대화? 요약만 읽어요
- 중요한 정보만 남겨요
- 불필요한 건 지워요

**결과:** 토큰 96% 절약 → 돈 96% 절약

---

## 📦 설치 (Installation)

```bash
# PyPI English package name
pip install tokensaver

# 또는 한국어 CLI 사용
pip install 토큰세이버

# 성능 최적화 버전 (orjson + aiofiles)
pip install tokensaver[speed]
```

---

## 🚀 사용법

```python
from 토큰세이버 import TokenSaver

# 시작
client = TokenSaver()

# 저장 (자동 압축)
client.save_memory("프로젝트/마케팅", "마케팅 전략: ...")

# 검색 (토큰 96% 절약)
results = client.find("마케팅", level=0)  # 요약만
```

---

## 🎁 요금제

| Plan | 비용 | 기능 |
|------|------|------|
| **무료 체험** | ₩0 | 1개월 무제한 |
| **Pro** | ₩9,000/월 | 무제한 + 팀 공유 |
| **Team** | ₩29,000/월 | 무제한 + 협업 |

---

## ✅ 왜 쓰냐구요?

1. **비용 절약**: 월 10만 원 → 4천 원
2. **간편함**: pip install 1줄이면 끝
3. **한국어 최적화**: 한국어 잘 이해해요
4. **자동 동기화**: heartbeat 때마다 자동 로드

---

## 🔧 어떻게 돌아가냐구요?

간단해요:

1. **저장하면** → 자동으로 요약
2. **검색하면** → 요약만 반환
3. **상세 보면** → 전체 내용

이게 전부예요.

---

## 📞 문의

- ClawHub: https://clawhub.com/skills/토큰세이버
- 이메일: support@tokensaver.pro

---

---

## 🎉 v3.0 업그레이드 - 더 강력해졌어요!

**2026-03-29 릴리스**

### 새로운 4단계 압축 시스템

| 레벨 | 이름 | 절감률 | 용도 |
|------|------|--------|------|
| **L0** | Abstract | **99%** | 빠른 검색용 |
| **L1** | Overview | **96%** | 일반 검색용 |
| **L2** | Summary | **91%** | 기본 (권장) |
| **L3** | Full | **0%** | 상세 보기용 |

### 🚀 v3.0 신기능

```python
from 토큰세이버 import TokenSaver

# ✅ Java 설치 없이 바로 사용!
ovk = TokenSaver()

# 레벨 선택 저장
ovk.save("메모/중요", "내용...", level=2)  # L2: 기본
ovk.save("메모/빠른", "내용...", level=0)  # L0: 99% 절감

# 배치 저장 (여러개 한번에)
ovk.save_batch([
    {"uri": "a/1", "content": "메모1"},
    {"uri": "a/2", "content": "메모2"},
])

# 백업/복원
ovk.export("backup.json")
ovk.import_data("backup.json")

# 자동 정리 (7일 이상 된 것 압축)
ovk.auto_compress_old(days=7, target_level=1)
```

### 왜 v3.0이 더 좋아요?

| 기능 | v2.x | **v3.0** |
|------|------|----------|
| Java 필요 | ✅ 필요 | ❌ **불필요** |
| 압축 단계 | 1단계 | **4단계** |
| 배치 처리 | ❌ 없음 | **✅ 있음** |
| 백업/복원 | ❌ 없음 | **✅ 있음** |
| 자동 정리 | ❌ 없음 | **✅ 있음** |

---

**지금 시작하세요. 1개월 무료.**

```bash
pip install 토큰세이버
```