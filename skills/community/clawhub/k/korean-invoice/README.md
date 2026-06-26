# korean-invoice

한국형 견적서/세금계산서 자동 생성 스킬

## 디렉토리 구조

```
korean-invoice/
├── SKILL.md              # 스킬 설명서
├── README.md             # 개발자 문서 (이 파일)
├── package.json          # 의존성
├── scripts/
│   ├── generate.js       # 견적서/세금계산서 생성 (메인)
│   ├── manage-clients.js # 거래처 관리
│   └── manage-items.js   # 품목 관리
├── templates/
│   ├── quote.html        # 견적서 템플릿
│   └── tax-invoice.html  # 세금계산서 템플릿
├── data/
│   ├── my-info.json      # 내 사업자 정보
│   ├── clients.json      # 거래처 DB
│   └── items.json        # 품목 DB
└── output/               # 생성된 파일 저장 (HTML, PDF)
```

## 설치

```bash
cd /Users/mupeng/.openclaw/workspace/skills/korean-invoice
npm install
```

## 사용법

### 1. 내 정보 설정

`data/my-info.json` 파일을 편집하여 내 사업자 정보 입력:

```json
{
  "businessNumber": "123-45-67890",
  "companyName": "무펭이즘",
  "ceo": "김무펭",
  "address": "서울특별시 강남구 테헤란로 123",
  "phone": "010-1234-5678",
  "email": "contact@mufism.com",
  "bankAccount": "우리은행 1002-123-456789"
}
```

### 2. 거래처 관리

```bash
# 거래처 추가
node scripts/manage-clients.js add "무펭이즘" \
  --business-number "123-45-67890" \
  --ceo "김형님" \
  --address "서울시..." \
  --phone "010-1234-5678" \
  --email "contact@mufism.com"

# 거래처 목록
node scripts/manage-clients.js list

# 거래처 조회
node scripts/manage-clients.js view "무펭이즘"

# 거래처 수정
node scripts/manage-clients.js edit "무펭이즘" --phone "010-9999-9999"

# 거래처 삭제
node scripts/manage-clients.js remove "무펭이즘"
```

### 3. 품목 관리

```bash
# 품목 추가
node scripts/manage-items.js add "포토부스 대여" \
  --price 500000 \
  --unit "일" \
  --description "이동형 포토부스 대여 (1일 기준)"

# 품목 목록
node scripts/manage-items.js list

# 품목 조회
node scripts/manage-items.js view "포토부스 대여"

# 품목 수정
node scripts/manage-items.js edit "포토부스 대여" --price 600000

# 품목 삭제
node scripts/manage-items.js remove "포토부스 대여"
```

### 4. 견적서 생성

```bash
# 품목 직접 입력 (품목명,수량,단가;...)
node scripts/generate.js quote \
  --client "무펭이즘" \
  --items "포토부스 대여,2,500000;출장비,1,100000" \
  --notes "부가세 별도"

# 저장된 품목 사용
node scripts/generate.js quote \
  --client "무펭이즘" \
  --item-ids "포토부스 대여,출장비"

# HTML만 생성 (PDF 변환 안 함)
node scripts/generate.js quote \
  --client "무펭이즘" \
  --items "포토부스 대여,1,500000" \
  --no-pdf
```

### 5. 세금계산서 생성

```bash
# 세금계산서 생성 (영수)
node scripts/generate.js tax \
  --client "무펭이즘" \
  --items "포토부스 대여,1,500000" \
  --type 영수

# 세금계산서 생성 (청구)
node scripts/generate.js tax \
  --client "무펭이즘" \
  --items "포토부스 대여,1,500000" \
  --type 청구 \
  --issue-date "2026-02-17"
```

## 출력 파일

생성된 파일은 `output/` 디렉토리에 저장됩니다:

- `YYYY-MM-DD-견적서-{거래처명}.html`
- `YYYY-MM-DD-견적서-{거래처명}.pdf`
- `YYYY-MM-DD-세금계산서-{거래처명}.html`
- `YYYY-MM-DD-세금계산서-{거래처명}.pdf`

## PDF 변환

PDF 변환은 puppeteer를 사용하여 OpenClaw 브라우저(포트 18800)에 연결합니다.

**주의:**
- OpenClaw 브라우저가 실행중이어야 함
- `browser start` 명령으로 브라우저 시작

## 템플릿 커스터마이징

`templates/` 디렉토리의 HTML 파일을 편집하여 양식을 커스터마이징할 수 있습니다.

### 변수

견적서 (`quote.html`):
- `{{myCompanyName}}`, `{{myBusinessNumber}}`, `{{myCEO}}`, `{{myAddress}}`, `{{myPhone}}`, `{{myEmail}}`
- `{{clientName}}`, `{{clientBusinessNumber}}`, `{{clientCEO}}`, `{{clientAddress}}`, `{{clientPhone}}`
- `{{issueDate}}`, `{{validUntil}}`
- `{{itemRows}}` - 품목 테이블 행
- `{{subtotal}}`, `{{vat}}`, `{{total}}`
- `{{notes}}`

세금계산서 (`tax-invoice.html`):
- `{{approvalNumber}}`, `{{type}}`, `{{issueDate}}`
- 공급자/공급받는자 정보는 견적서와 동일
- `{{itemRows}}` - 품목 테이블 행
- `{{subtotal}}`, `{{vat}}`, `{{total}}`

## OpenClaw 통합

OpenClaw에서 자연어로 호출:

```
"무펭이즘 거래처에 포토부스 대여 2일 견적서 작성해줘"
"예시거래처에 세금계산서 발행해줘 (포토부스 대여 1일)"
```

Agent가 자동으로 스크립트를 실행하고 결과를 보고합니다.

## 트러블슈팅

### PDF 생성 실패

```
Error: connect ECONNREFUSED 127.0.0.1:18800
```

→ OpenClaw 브라우저가 실행중인지 확인: `openclaw browser status`

### 거래처/품목 없음

→ `manage-clients.js` / `manage-items.js`로 먼저 등록

### 템플릿 변수 미치환

→ `data/my-info.json`에 모든 필드가 입력되었는지 확인

## 라이선스

MIT

## 작성자

무펭이 🐧 (2026-02-17)
