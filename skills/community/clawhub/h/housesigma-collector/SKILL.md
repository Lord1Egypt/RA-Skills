# HouseSigma Collector Skill

HouseSigma에서 매물 데이터를 수집하여 Hauscout SQLite DB에 저장하는 skill.

## 프로젝트 경로
- **Hauscout**: `/Users/kendrick/projects/hauscout`
- **DB**: `/Users/kendrick/projects/hauscout/data/hauscout.db`
- **스크립트**: `/Users/kendrick/projects/hauscout/scripts/collect.ts`

## 사용법

### 자동 수집 (검색 프로필 기반)
```bash
cd /Users/kendrick/projects/hauscout && npx tsx scripts/collect.ts
```

### 특정 매물 수집
```bash
cd /Users/kendrick/projects/hauscout && npx tsx scripts/collect.ts --url "<housesigma_url>"
```

### 특정 프로필만 수집
```bash
cd /Users/kendrick/projects/hauscout && npx tsx scripts/collect.ts --profile <id>
```

### 브라우저 창 보면서 수집 (디버깅)
```bash
cd /Users/kendrick/projects/hauscout && npx tsx scripts/collect.ts --headed
```

## 수동 수집 (브라우저 직접 사용)

Playwright 스크립트 대신 Clawdbot 브라우저로 직접 수집할 때:

1. 브라우저로 HouseSigma 매물 상세 페이지 열기
2. DOM 스냅샷에서 데이터 추출
3. SQLite에 직접 INSERT

### DOM 데이터 매핑
HouseSigma 상세 페이지의 구조:
- **주소/상태**: `<h1>` 태그 (Unit X - Street - Municipality - Community)
- **가격**: `<em>` 태그의 `$ X,XXX` 패턴
- **Key Facts**: `<dt>`/`<dd>` 쌍 (Tax, Property Type, Maintenance, etc.)
- **Details**: 같은 `<dt>`/`<dd>` 패턴 (Bedrooms, Bathrooms, etc.)
- **방 정보**: "Metres" 섹션의 텍스트 패턴
- **Estimates**: SigmaEstimate, Estimated Rent, Rental Yield
- **학교**: Catchment Schools 섹션
- **인기도**: "Popularity : XX/100" 텍스트
- **커뮤니티 통계**: Community Statistics 섹션

## 검색 프로필 관리

프로필 추가:
```bash
cd /Users/kendrick/projects/hauscout
sqlite3 data/hauscout.db "INSERT INTO search_profiles (name, center_lat, center_lng, radius_km, property_types, price_min, price_max, beds_min, beds_max, baths_min, baths_max, is_active) VALUES ('이름', lat, lng, radius, '[\"Condo Apartment\"]', 0, 800000, 2, 3, 1, 2, 1);"
```

현재 프로필 확인:
```bash
sqlite3 data/hauscout.db "SELECT * FROM search_profiles;"
```

## 데이터 수집 후

수집 후 대시보드에 반영하려면:
```bash
cd /Users/kendrick/projects/hauscout
git add data/hauscout.db
git commit -m "data: daily collection $(date +%Y-%m-%d)"
git push
```
Vercel 배포 시 자동으로 최신 데이터가 반영됩니다.

## 크론잡

Clawdbot cron으로 매일 오전 9시에 자동 수집:
- 스크립트 실행 → DB 업데이트 → git commit & push

## 주의사항
- HouseSigma rate limiting 방지를 위해 요청 간 2-4초 간격 유지
- headless 모드에서 차단될 수 있음 → --headed 옵션으로 확인
- 검색 프로필의 결과가 많으면 시간이 오래 걸림 (매물당 ~5초)
