# 🚀 TokenSaver (토큰세이버)

**95-96% Korean | 85-90% English** - Bilingual Context DB for AI Agents  
**한국어 95-96% | 영어 85-90%** - 한영겸용 AI 에이전트용 Context DB

> Save tokens, save money! / 토큰을 저장해서 돈을 절약하세요!

**Bilingual Support / 한영겸용:**
- 🇰🇷 Korean: 95-96% cost reduction (Josa/Eomi removal, stemming)
- 🇺🇸 English: 85-90% cost reduction (Stopwords removal, stemming)

## Installation / 설치

```bash
# English package name / 영어 패키지명
pip install tokensaver

# With performance optimizations / 성능 최적화 포함
pip install tokensaver[speed]  # orjson + aiofiles
pip install tokensaver[korean]  # konlpy for advanced NLP
pip install tokensaver[vector]  # sentence-transformers for vector search
```

## ⚡ Quick Start / 빠른 시작

### English Usage / 영어 사용법
```python
from openviking_korean import TokenSaver

# Initialize (No Java required!)
client = TokenSaver()

# Save with auto 4-level compression
client.save("project/memo", """
TokenSaver is a Korean Context DB for AI agents.
Features:
- 96% token cost reduction
- 4-level compression
- Async batch processing
""", level=2)

# Search with Korean NLP
results = client.find("AI cost reduction")

# Batch processing (10x faster)
items = [
    {"uri": f"memo/{i}", "content": f"Content {i}"}
    for i in range(100)
]
client.save_batch(items)

# Load with compression levels
abstract = client.load("project/memo", level=0)   # L0: 99% reduction (keywords only)
overview = client.load("project/memo", level=1)  # L1: 96% reduction (key sentences)
content = client.load("project/memo", level=2)  # L2: 91% reduction (default)
fulltext = client.load("project/memo", level=3) # L3: Original full text
```

### 한국어 사용법
```python
from openviking_korean import TokenSaver

# 클라이언트 초기화 (Java 설치 불필요!)
client = TokenSaver()

# 저장 (자동 4단계 압축)
client.save("마케팅/닥터레이디", """
닥터레이디는 여성청결제 브랜드입니다.
- 제품: 케어워시, 이너앰플
- 매출: 온라인 2위
- 타겟: 20-40대 여성
""", level=2)

# 검색 (토큰 96% 절감)
results = client.find("닥터레이디 제품")

# 배치 처리 (10x 빠름)
items = [
    {"uri": "메모/1", "content": "내용1"},
    {"uri": "메모/2", "content": "내용2"},
]
client.save_batch(items)

# 레벨별 로드
abstract = client.load("마케팅/닥터레이디", level=0)   # L0: 99% 절감 (키워드만)
overview = client.load("마케팅/닥터레이디", level=1)  # L1: 96% 절감 (핵심 문장)
content = client.load("마케팅/닥터레이디", level=2)   # L2: 91% 절감 (기본)
detail = client.load("마케팅/닥터레이디", level=3)    # L3: 원본 전체
```

## CLI 사용

```bash
# 검색
ovk find "마케팅 전략"

# 저장
ovk save "프로젝트/마케팅" --content "닥터레이디 마케팅 계획..."

# 요약
ovk abstract "memories/프로젝트/마케팅"

# 개요
ovk overview "memories/프로젝트/마케팅"

# 전체 읽기
ovk read "memories/프로젝트/마케팅"
```

## 📊 4단계 압축 시스템

| 레벨 | 이름 | 절감률 | 내용 | 사용 시나리오 |
|------|------|--------|------|--------------|
| **L0** | Abstract | **99%** | 키워드 5개 | 빠른 탐색 |
| **L1** | Overview | **96%** | 핵심 문장 3개 | 미리보기 |
| **L2** | Summary | **91%** | 요약 + 키워드 | **기본 (권장)** |
| **L3** | Full | **0%** | 원본 전체 | 상세 작업 |

**예시:**
```python
text = "인공지능과 머신러닝은 미래 기술입니다. 많은 기업들이 투자하고 있어요."

# L0 (99% 절감): "[인공지능][머신러닝][미래][기술][기업]"
# L1 (96% 절감): "인공지능과 머신러닝은 미래 기술입니다"
# L2 (91% 절감): "[인공지능/머신러닝/미래] 인공지능과 머신러닝은 미래 기술입니다 많은 기업들이 투자하고 있어요"
# L3 (원본): 그대로
```

## 🚀 성능 최적화

### JVM-Free
```python
# Java 설치 없이 바로 사용!
from 토큰세이버 import TokenSaver
client = TokenSaver()  # 즉시 동작
```

### 비동기 처리
```python
import asyncio

# 100개 동시 저장 (10x 빠름)
await client.save_batch_async(items)
```

### 캐싱
- `@lru_cache` 적용으로 동일 텍스트 1000x+ 속도 향상
- 정규식 미리 컴파일

### 고성능 JSON
- `orjson` 사용 시 3-10x 파싱 속도 향상
```bash
pip install orjson
```

## 📦 기능 목록

- ✅ **4단계 압축** (L0-L3): 99% → 91% 선택적 절감
- ✅ **JVM-Free**: Pure Python으로 Java 없이 동작
- ✅ **비동기 API**: `save_async()`, `save_batch_async()`
- ✅ **배치 처리**: 여러 개 한 번에 저장/검색
- ✅ **익스포트/임포트**: 백업/복원/이전
- ✅ **자동 압축**: 오래된 데이터 자동 정리
- ✅ **한국어 최적화**: 형태소 분석 + 조사/어미 제거

## 🔗 연동

### OpenClaw
```python
# 자동 연동
# OpenClaw heartbeat에서 자동으로 컨텍스트 로드
```

### FastAPI / Flask
```python
from fastapi import FastAPI
from 토큰세이버 import TokenSaver

app = FastAPI()
client = TokenSaver()

@app.post("/save")
async def save(uri: str, content: str):
    return client.save(uri, content)

@app.get("/find")
async def find(query: str):
    return client.find(query)
```

## 📚 문서

- [API Reference](docs/API_REFERENCE.md)
- [Benchmarks](benchmarks/benchmark_tokensaver.py)
- [Tests](tests/test_tokensaver.py)

## 📞 지원

- **GitHub**: https://github.com/dorongs/tokensaver
- **ClawHub**: https://clawhub.com/skills/tokensaver
- **이메일**: support@tokensaver.pro

## 📜 라이선스

MIT License - 자유롭게 사용하세요!

---

Made with ❤️ by Roken (김명진)

**토큰을 세이브하고, 비용을 절약하세요!**