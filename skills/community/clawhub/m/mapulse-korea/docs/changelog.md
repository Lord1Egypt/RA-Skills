# Changelog

All notable changes to Mapulse are documented here.

---

## [1.1.0] — 2026-03-24

### 🔥 Bug Fixes (Critical)
- **상승 TOP에 마이너스 종목 표시** — `gainers` 필터에 `change_pct > 0` 조건 누락으로 전종목 하락일에 -1.0% 종목이 상승 TOP3에 포함되는 버그 수정
- **종목명 미표시** — ticker 직접 입력 시 `277810 (277810)` 처럼 코드만 표시되던 버그 수정. KRX API fallback `_resolve_stock_name()` 추가
- **resolve_ticker 최장매칭** — `삼성바이오로직스` 입력 시 `삼성`이 먼저 매칭되어 삼성전자(005930)로 잘못 조회되는 버그 수정. 별명 길이 내림차순 정렬로 최장매칭 우선
- **레인보우로보틱스 ticker 오류** — 454910(두산로보틱스)으로 잘못 매핑 → 277810으로 수정
- **Telegram Markdown 파싱 오류** — `_이탤릭_` 사용으로 면책 문구·CTA 깨지는 문제 수정

### 🚀 New Features

#### Billing v2 — 사용량 과금 시스템
- `scripts/billing.py` — Pay-per-call 과금 엔진
  - 일반 조회 $0.08/회, 심층 분석 $0.16/회
  - 7일/50회 무료 대화 + 7일 무료 추송 trial
  - 잔액 체크, 사용 기록, trial 만료 안내
- `scripts/infini_pay.py` — Infini Money 결제 게이트웨이 (HMAC-SHA256 인증)
  - 주문 생성 → 호스티드 체크아웃 → 웹훅 수신 → 잔액 자동 충전
  - 최소 충전 $10 USDT
- `scripts/payment_monitor.py` — 결제 상태 모니터링 (cron 1분 간격)
- Bot commands: `/topup`, `/balance`

#### Referral System — 추천 리워드
- `scripts/referral.py` — A→B 추천 시 B 결제금의 15% 를 A에게 USDT 크레딧 지급
  - 추천 코드 자동 생성 (ref_XXXXXX)
  - 누적 커미션 추적
- Bot commands: `/invite`, `/referrals`

#### Platform Push — 4-타임 정기 추송
- `scripts/cron_platform_push.py` — LLM 기반 시황 추송 (OpenRouter)
  - 🌅 08:30 모닝 브리프 (개장 전)
  - 📊 12:20 장중 리포트 (오전장 정리)
  - ⚡ 14:00 오후 핵심 변수 (질문 유도)
  - 🌙 20:50 나이트 브리프 (해외 시장)
- 모든 추송에 🚨 *한 줄 요약* + 📌 *행동 지침* 포함 (v1.1 신규)
- 공개 채널 + 개인 사용자 동시 발송

#### News Intelligence — 뉴스 수집 & 분석
- `scripts/cron_news_aggregate.py` — 뉴스 수집 + 점수화 (news_digest 테이블)
  - Investing.com, Yahoo RSS, 6551.io 소스 통합
  - impact_direction / score 자동 분류
- `scripts/cron_news_scan.py` — 실시간 뉴스 스캔 + 고영향 즉시 push

#### Push Performance Tracker
- `scripts/push_tracker.py` — 추송 성과 추적
  - 추천 종목 추후 가격 변동 기록 (D+1, D+3, D+5)
  - 방향 적중률 / 수익률 통계
  - `/track` command + `backfill` cron

#### User Engagement
- `scripts/cron_day2_survey.py` — Day-2 사용자 프로필 설문 (투자 성향, 관심 섹터)
- `scripts/cron_daily_metrics.py` — 일일 운영 지표 리포트 (DAU, 메시지, 전환율)
- `scripts/trust_badge.py` — 신뢰 배지 시스템 (intent별 데이터 출처 명시)

#### Extended Coverage
- `scripts/extended_aliases.py` — 종목 별명 172개, 종목 59개, 테마 키워드 117개
  - 반도체, AI, 2차전지, 방산, 바이오, K-POP 등 테마 검색 지원
  - 한국어/중국어/영어 트리링걸 별명
- `resolve_multiple_tickers()` — 겹침 방지 + 최장매칭 다중 종목 추출

### Enhanced
- **Stock queries** — 종목 조회 시 KRX에 없는 ticker도 자동 이름 조회 (fallback)
- **Push quality** — SYSTEM_PROMPT에 한 줄 요약 필수, 행동 지침 필수, Markdown 안전 규칙 추가
- **Bot commands** — 15개 명령어 체계: `/start`, `/help`, `/pulse`, `/stock`, `/sector`, `/hot`, `/dart`, `/alert`, `/notify`, `/track`, `/stats`, `/topup`, `/balance`, `/invite`, `/referrals`

### Technical
- systemd service: `mapulse-bot.service` (auto-restart)
- cron: 12개 정기 작업 (push 4회, news 2회, metrics, survey, payment monitor 등)
- LLM: OpenRouter (Haiku fast + Opus deep), temperature 0.4
- DB: SQLite with billing, referral, push_log, news_digest, push_tracking tables

---

## [1.0.0] — 2026-03-17

### Added
- **Daum Finance + Naver Extended Integration**
  - `scripts/daum_finance.py` — 7 endpoints (stock, batch, chart, indices, investors, sectors, hot ranks)
  - `scripts/naver_extended.py` — Estimated PER/EPS, foreign exhaustion, dividend yield
  - Intent: `SECTOR_RANKING`, `HOT_RANK`
  - Bot commands: `/sector`, `/hot`
  - Documentation: `docs/` directory

### [Pre-1.0] — 2026-03-13 ~ 2026-03-16

#### 2026-03-16 — Data Source Expansion
- Exchange rates (exchangerate-api.com), VIX, Fear & Greed Index
- Stock disclosures (Naver), Financial summary, Price history
- Intents: `DISCLOSURE`, `FINANCIAL`, `EXCHANGE_RATE`, `FEAR_GREED`

#### 2026-03-16 — 6551.io Integration
- `scripts/news_6551.py` — OpenNews (72+ sources)
- `scripts/twitter_6551.py` — OpenTwitter (KOL tracking)

#### 2026-03-15 — Community & Sentiment
- `scripts/forum_scraper.py` — Naver community (OpenTalk, 종토방, broker research)
- `scripts/news_intelligence.py` — Self-hosted news (Investing.com, Yahoo RSS)
- Intents: `COMMUNITY`, `RESEARCH`, `SUPPLY_DEMAND`

#### 2026-03-14 — Claude AI Analysis Layer
- `scripts/claude_ai.py` — Auto language detection, pro/con analysis, user profiling
- `scripts/llm.py` — Haiku (fast) + Opus (deep) two-phase response

#### 2026-03-13 — Core MVP
- `scripts/fetch_briefing.py` — pykrx daily briefing
- `scripts/chat_query.py` — 12 intents, natural language query
- `scripts/crash_alert.py` — Crash detection
- `scripts/butterswap_pay.py` — ButterSwap billing
- `bot/mapulse_bot.py` — Telegram bot
- Trilingual: Korean, Chinese, English

---

## Roadmap

- [ ] KRX direct data — Short selling, market-wide ranking (OTP auth)
- [ ] Industry alert — Auto-push on significant sector movements
- [ ] Portfolio tracking — User portfolio P/L calculation
- [ ] Daum investor API — Per-stock investor flow
- [ ] Subscription billing — Monthly plan via Infini subscription API
- [ ] Push A/B testing — Test different message formats for engagement
