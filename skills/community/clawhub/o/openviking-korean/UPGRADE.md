# OpenViking Korean v2.0 업그레이드 계획

## 목표
1. **자동 동기화** - heartbeat 시 자동 검색
2. **벡터 검색** - 의미 기반 검색
3. **형태소 분석 개선** - 검색 정확도 향상

## 작업 목록

### Phase 1: 벡터 검색 추가
- [ ] sentence-transformers 설치
- [ ] 임베딩 캐시 시스템
- [ ] 코사인 유사도 검색 구현

### Phase 2: 형태소 분석 강화
- [ ] konlpy 최적화
- [ ] 불용어 처리
- [ ] 동의어 매핑

### Phase 3: 자동 동기화
- [ ] memory_recall 훅 연동
- [ ] HEARTBEAT.md 자동 검색
- [ ] 스마트 컨텍스트 로딩

## 파일 구조
```
openviking_korean/
├── client.py          # 메인 클라이언트
├── vector_store.py    # 벡터 검색 (NEW)
├── tokenizer.py       # 형태소 분리 (NEW)
├── auto_sync.py       # 자동 동기화 (NEW)
└── __init__.py
```

## 의존성
```
sentence-transformers
konlpy
numpy
```

---

*생성일: 2026-03-22*