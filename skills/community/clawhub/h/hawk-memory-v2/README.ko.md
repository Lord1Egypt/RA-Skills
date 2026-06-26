# 🦅 Context-Hawk

> **AI 컨텍스트 메모리 가디언** — 추적을 잃는 것을 멈추고, 중요한 것을 기억하기 시작하세요.

*어떤 AI 에이전트에게도 session을 넘어, 주제를 넘어, 시간을超越하여 실제로 작동하는 기억을 제공하세요.*

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-2026.3%2B-brightgreen)](https://github.com/openclaw/openclaw)
[![ClawHub](https://img.shields.io/badge/ClawHub-context--hawk-blue)](https://clawhub.com)

**English** | [中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Italiano](README.it.md) | [Русский](README.ru.md) | [Português (Brasil)](README.pt-BR.md)

---

## 무엇을 하나요?

대부분의 AI 에이전트는 **건망증**으로 고통받습니다 — 새로운 session이 시작될 때마다零에서 시작합니다. Context-Hawk는 생산グレード 메모리 관리 시스템으로 이것을 해결합니다. 중요한 것을 자동으로 캡처하고, 노이즈를 희석시키며, 올바른 시간에 올바른 기억을思い出します.

**Context-Hawk 없이:**
> "이미 말했잖아요 — 간결한 답장을 좋아한다고!"
> (다음 session, 에이전트가 다시 잊어버림)

**Context-Hawk 사용 시:**
> (session 1에서 자동으로 커뮤니케이션 선호도를 적용)
> ✅ 매번 간결하고 직접적인 응답을 제공

---

## ✨ 10가지 핵심 기능

| # | 기능 | 설명 |
|---|---------|-------|
| 1 | **작업 상태 지속성** | `hawk resume` — 작업 상태 보존, 재시작 후 계속 |
| 2 | **4계층 메모리** | Working → Short → Long → Archive, Weibull衰减 적용 |
| 3 | **구조화된 JSON** | 중요도 점수(0-10), 카테고리, 티어, L0/L1/L2 레이어 |
| 4 | **AI 중요도 점수화** | 기억에 자동 점수 부여, 저가치 콘텐츠 폐기 |
| 5 | **5가지 주입 전략** | A(높은 중요도) / B(작업 관련) / C(최근) / D(Top5) / E(전체) |
| 6 | **5가지 압축 전략** | summarize / extract / delete / promote / archive |
| 7 | **자기 성찰** | 작업 명확성, 누락된 정보, 루프 감지 확인 |
| 8 | **LanceDB 벡터 검색** | 선택 사항 — 하이브리드 vector + BM25 검색 |
| 9 | **순수 메모리 폴백** | LanceDB 없이 동작, JSONL 파일 지속성 |
| 10 | **자동 중복 제거** | 중복 기억을 자동으로 병합 |

---

## 🏗️ 아키텍처

```
┌──────────────────────────────────────────────────────────────┐
│                      Context-Hawk                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Working Memory  ←── 현재 session (최근 5-10턴)           │
│       ↓ Weibull衰减                                         │
│  Short-term      ←── 24시간 콘텐츠, 요약됨               │
│       ↓ access_count ≥ 10 + 중요도 ≥ 0.7                │
│  Long-term       ←── 영구 지식, 벡터 인덱싱               │
│       ↓ >90일 또는 decay_score < 0.15                     │
│  Archive          ←── 이력, 요청 시 로드                   │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│  Task State Memory  ←── 재시작 간 지속 (핵심!)            │
│  - 현재 작업 / 다음 단계 / 진행률 / 출력물                  │
├──────────────────────────────────────────────────────────────┤
│  주입 엔진       ←── 전략 A/B/C/D/E가 리콜 결정           │
│  자기 성찰        ←── 매 답변 시 컨텍스트 확인              │
│  자동 트리거      ←── 매 10턴 (설정 가능)                │
└──────────────────────────────────────────────────────────────┘
```

---

## 📦 작업 상태 메모리 (가장 가치 있는 기능)

재시작, 정전 또는 session 전환 후에도 Context-Hawk는 정확한 중단 지점에서 재개합니다.

```json
// memory/.hawk/task_state.jsonl
{
  "task_id": "task_20260329_001",
  "description": "API 문서 완료",
  "status": "in_progress",
  "progress": 65,
  "next_steps": ["아키텍처 템플릿 검토", "사용자에게 보고"],
  "outputs": ["SKILL.md", "constitution.md"],
  "constraints": ["커버율 98% 필수", "API는 버전化管理"],
  "resumed_count": 3
}
```

```bash
hawk task "문서 완료"        # 작업 생성
hawk task --step 1 done  # 단계 완료 표시
hawk resume               # 재시작 후 재개 ← 핵심!
```

---

## 🧠 구조화된 메모리

```json
{
  "id": "mem_20260329_001",
  "type": "task|knowledge|conversation|document|preference|decision",
  "content": "완전한 원본 콘텐츠",
  "summary": "한 줄 요약",
  "importance": 0.85,
  "tier": "working|short|long|archive",
  "created_at": "2026-03-29T00:00:00+08:00",
  "access_count": 3,
  "decay_score": 0.92
}
```

### 중요도 점수화

| 점수 | 유형 | 행동 |
|-------|------|------|
| 0.9-1.0 | 결정/규칙/오류 | 영구, 가장 느린衰减 |
| 0.7-0.9 | 작업/선호도/지식 | 장기 기억 |
| 0.4-0.7 | 대화/논의 | 단기, archive로衰减 |
| 0.0-0.4 | 채팅/인사 | **폐기, 절대 저장 안 함** |

---

## 🎯 5가지 컨텍스트 주입 전략

| 전략 | 트리거 | 절약 |
|------|---------|------|
| **A: 높은 중요도** | `중요도 ≥ 0.7` | 60-70% |
| **B: 작업 관련** | scope 일치 | 30-40% ← 기본값 |
| **C: 최근** | 마지막 10턴 | 50% |
| **D: Top5 리콜** | `access_count` Top 5 | 70% |
| **E: 전체** | 필터 없음 | 100% |

---

## 🗜️ 5가지 압축 전략

`summarize` · `extract` · `delete` · `promote` · `archive`

---

## 🔔 4단계 알림 시스템

| 레벨 | 임계값 | 행동 |
|-------|---------|------|
| ✅ Normal | < 60% | 자동 |
| 🟡 Watch | 60-79% | 압축 제안 |
| 🔴 Critical | 80-94% | 자동 쓰기 일시 중지, 강제 제안 |
| 🚨 Danger | ≥ 95% | 쓰기 차단, 압축 필수 |

---

## 🚀 빠른 시작

```bash
# LanceDB 플러그인 설치 (권장)
openclaw plugins install memory-lancedb-pro@beta

# 스킬 활성화
openclaw skills install ./context-hawk.skill

# 초기화
hawk init

# 핵심 명령
hawk task "내 작업"    # 작업 생성
hawk resume             # 마지막 작업 재개 ← 가장 중요
hawk status            # 컨텍스트 사용량 확인
hawk compress          # 메모리 압축
hawk strategy B        # 작업 관련 모드로 전환
hawk introspect         # 자기 성찰 보고서
```

---

## 자동 트리거: 매 N턴

매 **10턴** (기본값, 설정 가능), Context-Hawk가 자동으로:

1. 컨텍스트 수위 확인
2. 기억 중요도 평가
3. 사용자에게 상태 보고
4. 필요 시 압축 제안

```bash
# 설정 (memory/.hawk/config.json)
{
  "auto_check_rounds": 10,          # 매 N턴 확인
  "keep_recent": 5,                 # 마지막 N턴 보존
  "auto_compress_threshold": 70      # 70% 초과 시 압축
}
```

---

## 파일 구조

```
context-hawk/
├── SKILL.md
├── README.md
├── LICENSE
├── scripts/
│   └── hawk               # Python CLI 도구
└── references/
    ├── memory-system.md           # 4계층 아키텍처
    ├── structured-memory.md      # 메모리 형식 및 중요도
    ├── task-state.md           # 작업 상태 지속성
    ├── injection-strategies.md  # 5가지 주입 전략
    ├── compression-strategies.md # 5가지 압축 전략
    ├── alerting.md             # 알림 시스템
    ├── self-introspection.md   # 자기 성찰
    ├── lancedb-integration.md  # LanceDB 통합
    └── cli.md                  # CLI 참조
```

---

## 🔌 기술 사양

- **지속성**: JSONL 로컬 파일, 데이터베이스 불필요
- **벡터 검색**: LanceDB (선택), 파일로 자동 폴백
- **Cross-Agent**: 범용, 비지니스 로직 없음, 모든 AI 에이전트와 동작
- **제로 설정**: 스마트 기본값, 즉시 사용 가능
- **확장 가능**: 커스텀 주입 전략, 압축 정책, 점수화 규칙

---

## 라이선스

MIT — 무료로 사용, 수정, 배포 가능.
