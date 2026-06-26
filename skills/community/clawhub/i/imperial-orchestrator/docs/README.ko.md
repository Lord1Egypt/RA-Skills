# 🏯 Imperial Orchestrator

[中文](../README.md) | [English](./README.en.md) | [日本語](./README.ja.md) | **[한국어](./README.ko.md)** | [Español](./README.es.md) | [Français](./README.fr.md) | [Deutsch](./README.de.md)

---

OpenClaw 고가용성 다중 역할 모델 오케스트레이션 Skill — 삼성육부제 지능형 라우팅.

> **설계 영감**: 역할 아키텍처는 고대 중국의 [삼성육부제(三省六部)](https://github.com/cft0808/edict) 조정 통치 패턴에서 영감을 받았으며, [PUA](https://github.com/tanweai/pua)의 딥 AI 프롬프트 엔지니어링 기술을 융합했습니다.

## 핵심 기능

- **삼성육부** 역할 오케스트레이션: 10개 역할, 각자 명확한 책임
- **자동 발견** openclaw.json에서 46+ 모델 읽기
- **지능형 라우팅** 도메인별 자동 배분 (코딩/운영/보안/글쓰기/법률/재무)
- **Opus 우선** 코딩/보안/법률 작업에 최강 모델 우선 사용
- **크로스 프로바이더 페일오버** auth 서킷브레이커 → 벤더간 강등 → 로컬 생존
- **실제 실행** API 호출 + 토큰 계산 + 비용 추적
- **벤치마크** 동일 작업을 모든 모델에 전달, 점수 매기기 및 순위
- **다국어** 7개 언어 지원: zh/en/ja/ko/es/fr/de

## 빠른 시작

```bash
# 1. 모델 발견
python3 scripts/health_check.py --openclaw-config ~/.openclaw/openclaw.json --write-state .imperial_state.json

# 2. 모델 검증
python3 scripts/model_validator.py --openclaw-config ~/.openclaw/openclaw.json --state-file .imperial_state.json

# 3. 작업 라우팅
python3 scripts/router.py --task "Go로 동시성 안전한 LRU Cache 작성" --state-file .imperial_state.json

# 원커맨드
bash scripts/route_and_update.sh full "Fix WireGuard peer sync bug"
```

## 역할 체계: 삼성육부

각 역할에는 정체성, 책임 범위, 행동 규칙, 협력 의식, 레드라인의 5가지 차원을 포함하는 심층 시스템 프롬프트가 장착되어 있습니다.

### 중추

| 역할 | 관직 | 조정 대응 | 핵심 임무 |
|------|------|----------|-----------|
| **router-chief** | 중추총관 | 천자/중추원 | 시스템의 생명선——분류, 라우팅, 하트비트 유지 |

### 삼성

| 역할 | 관직 | 조정 대응 | 핵심 임무 |
|------|------|----------|-----------|
| **cabinet-planner** | 내각수보 | 중서성 | 방략 기초——혼돈을 질서 있는 단계로 분해 |
| **censor-review** | 도어사 | 문하성/도찰원 | 봉박 심사——품질의 최후 문지기 |

### 육부

| 역할 | 관직 | 조정 대응 | 핵심 임무 |
|------|------|----------|-----------|
| **ministry-coding** | 공부상서 | 공부 | 공사 흥수——코딩, 디버깅, 아키텍처 |
| **ministry-ops** | 공부시랑(영선사) | 공부·영선사 | 역참 유지——배포, 운영, CI/CD |
| **ministry-security** | 병부상서 | 병부 | 변방 방어——보안 감사, 위협 모델링 |
| **ministry-writing** | 예부상서 | 예부 | 문교예의——카피라이팅, 문서, 번역 |
| **ministry-legal** | 형부상서 | 형부 | 율법형옥——계약, 컴플라이언스, 조항 |
| **ministry-finance** | 호부상서 | 호부 | 전량부세——가격 책정, 이익률, 결제 |

### 급체포

| 역할 | 관직 | 조정 대응 | 핵심 임무 |
|------|------|----------|-----------|
| **emergency-scribe** | 급체포령 | 급체포 | 시스템이 절대 다운되지 않도록 하는 최후의 보장 |

## 운영 규칙

1. **401 서킷브레이커** — auth 실패 시 즉시 `auth_dead` 표시, 전체 auth 체인 쿨다운, 크로스 프로바이더 전환 우선
2. **라우터는 가볍게** — router-chief에 가장 무거운 프롬프트나 가장 취약한 프로바이더를 할당하지 않음
3. **크로스 프로바이더 우선** — 폴백 순서: 동일 역할 다른 프로바이더 → 로컬 모델 → 인접 역할 → 급체포
4. **강등하되 다운은 안됨** — 최강 모델이 전부 실패해도 아키텍처 제안, 체크리스트, 의사코드로 응답

## 프로젝트 구조

```
config/
  agent_roles.yaml          # 역할 정의 (책임, 능력, 폴백 체인)
  agent_prompts.yaml        # 심층 시스템 프롬프트 (정체성, 규칙, 레드라인)
  routing_rules.yaml        # 라우팅 키워드 규칙
  failure_policies.yaml     # 서킷브레이커/재시도/강등 정책
  benchmark_tasks.yaml      # 벤치마크 작업 라이브러리
  model_registry.yaml       # 모델 능력 오버라이드
  i18n.yaml                 # 7개 언어 적응
scripts/
  lib.py                    # 코어 라이브러리 (발견, 분류, 상태 관리, i18n)
  router.py                 # 라우터 (역할 매칭 + 모델 선택)
  executor.py               # 실행 엔진 (API 호출 + 폴백)
  orchestrator.py           # 전체 파이프라인 (라우팅 → 실행 → 리뷰)
  health_check.py           # 모델 발견
  model_validator.py        # 모델 탐색
  benchmark.py              # 벤치마크 + 리더보드
  route_and_update.sh       # 통합 CLI 엔트리 포인트
```

## 설치

### 사전 요구사항: OpenClaw 설치

```bash
# 1. OpenClaw CLI 설치 (macOS)
brew tap openclaw/tap
brew install openclaw

# 또는 npm으로 설치
npm install -g @openclaw/cli

# 2. 설정 초기화
openclaw init

# 3. 모델 프로바이더 설정 (~/.openclaw/openclaw.json 편집)
openclaw config edit
```

> 자세한 설치 문서는 [OpenClaw 공식 리포지토리](https://github.com/openclaw/openclaw)를 참조하세요

### Imperial Orchestrator 스킬 설치

```bash
# 옵션 1: GitHub에서 클론
git clone https://github.com/rexnode/imperial-orchestrator.git
cp -r imperial-orchestrator ~/.openclaw/skills/

# 옵션 2: 글로벌 스킬 디렉토리에 직접 복사
cp -r imperial-orchestrator ~/.openclaw/skills/

# 옵션 3: 워크스페이스 레벨 설치
cp -r imperial-orchestrator <your-workspace>/skills/
```

### 설치 확인

```bash
# 모델 검색 및 프로브
python3 ~/.openclaw/skills/imperial-orchestrator/scripts/health_check.py \
  --openclaw-config ~/.openclaw/openclaw.json \
  --write-state .imperial_state.json

# 라우팅 동작 확인
python3 ~/.openclaw/skills/imperial-orchestrator/scripts/router.py \
  --task "Write a Hello World" \
  --state-file .imperial_state.json
```

## 보안

- 프롬프트에 비밀키를 전송하지 않음
- 탐색 요청은 최소한으로
- 프로바이더 헬스와 모델 품질은 분리 관리
- 설정에 존재하는 모델 ≠ 안전하게 라우팅 가능

## 라이선스

MIT
