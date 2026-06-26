---
name: hauscout
description: Hauscout 부동산 데이터 수집/분석 파이프라인. HouseSigma에서 매물을 자동 수집하고 AI 분석 후 Neon PostgreSQL에 저장. '매물 수집', '부동산 데이터 수집', 'hauscout', '수집 실행', '부동산 크롤링' 요청 시 사용.
---

# Hauscout 데이터 수집

## 프로젝트 위치
`/Users/kendrick/projects/hauscout`

## 수집 실행

```bash
cd /Users/kendrick/projects/hauscout
npx tsx scripts/collect.ts
```

### CLI 옵션
- `--url <url>` — 특정 매물 1개만 수집
- `--profile <id>` — 특정 검색 프로필만
- `--headed` — 브라우저 표시 (디버깅용)
- `--dry-run` — AI 분석만, DB 저장 안 함

## 수집 파이프라인 요약
1. Playwright로 HouseSigma 맵 검색 → 매물 목록
2. 가격/침실/타입 코드 필터링
3. 상세 페이지 방문 → DOM 텍스트 추출 (Comparables 섹션 제외)
4. GPT-4o-mini AI 분석 → 구조화 데이터 + 가성비 분석
5. Neon PostgreSQL 저장 (신규/업데이트/가격변동 추적)

## 수집 후 체크리스트
1. 에러 없이 완료됐는지 확인 (exit code, 에러 카운트)
2. 신규 매물이 있으면 주소/가격/AI 요약 기록
3. 가격 변동이 있으면 기록
4. `memory/YYYY-MM-DD.md`에 수집 결과 요약 작성
5. git commit & push (변경사항 있을 때만)

## DB 확인 (필요시)

```bash
cd /Users/kendrick/projects/hauscout
npx tsx -e "
import { neon } from '@neondatabase/serverless';
import { drizzle } from 'drizzle-orm/neon-http';
import * as schema from './src/db/schema';
// .env.local 로드 필요
const sql = neon(process.env.DATABASE_URL!);
const db = drizzle(sql, { schema });
const all = await db.select().from(schema.listings);
console.log(JSON.stringify(all, null, 2));
"
```

## 검색 프로필 (현재 2개)
1. Queensway 근처 콘도 (2-3bed, $800K 이하)
2. 미시사가 단독주택 ($800K 이하)

## 주의사항
- HouseSigma는 SPA → `domcontentloaded` + waitForTimeout 사용
- 가격 추출은 `"Listed for: $XXX"` 패턴만 사용 (Comparables 가격 혼입 방지)
- 요청 간 2-4초 랜덤 딜레이 (rate limit 방지)
