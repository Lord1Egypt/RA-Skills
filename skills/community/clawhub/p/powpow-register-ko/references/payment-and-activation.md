# 구독 활성화와 결제 — powpow-register

## 결론(먼저 답부터)
> **무료 테스트 기간(2026-10-18 시작; 플랫폼의 실제 동작이 우선합니다)**: 이 기간에는 가입한 계정이 모든 기능을 바로 사용할 수 있고 **구독은 요구사항이 아니라 선택적 업그레이드**입니다 — 사용자가 스스로 멤버십을 원할 때만 이 파일의 플로우를 따르세요. 테스트 기간이 끝나면 구독하지 않은 계정이 콘텐츠 페이지를 방문할 때 구독 페이지로 리디렉션됩니다. 이 파일에 따라 구독을 완료하면 됩니다.


**Alipay 구독과 PayPal 구독 모두 agent가 발주와 입금 추적을 대행할 수 있습니다.**
Alipay는 일회성 구매로 자동 갱신이 없어 중국 본토/Alipay가 있는 사용자에게 맞고, PayPal은 월간 자동 갱신으로 언제든 해지 가능해
해외/Alipay가 없는 사용자에게 맞습니다. WeChat 스캔(수동 확인)과 화웨이 IAP도 남아 있지만 skill이 대행하지는 않습니다.

결제 단계의 책임 경계: agent는 **주문 생성, 계산대 열기, 입금 확인**까지만 할 수 있습니다. 사용자의 Alipay/PayPal
계정/결제 자격증명에는 **절대** 접촉하지 않고 '대신 결제'도 약속하지 않습니다. 결제 행위는 항상 사용자 본인이 공식 계산대에서 수행합니다.

## Alipay 채널(vibepay, 주력)

일회성 매수제: 한 번 결제하면 해당 기간이 개통되고 **자동 갱신 없음**. 플랜은
`src/lib/alipay-vibepay.ts`(`ALIPAY_PACKAGES`)에 고정되어 있습니다:

| key | planId | 이름 | 가격 | 기간 |
|---|---|---|---|---|
| `monthly` | alipay-monthly | 월간 멤버십 | ¥6.99 | 30일 |
| `quarterly` | alipay-quarterly | 분기 멤버십 | ¥19.99 | 90일 |
| `yearly` | alipay-yearly | 연간 멤버십 | ¥69.99 | 365일 |

### 인터페이스 계약(skill 스크립트가 이미 래핑됨. agent가 직접 요청을 조립하지 않음)

| API | 메서드 | 설명 |
|---|---|---|
| `/api/payment/alipay/create-order` | POST | `Authorization: Bearer <JWT>` 필요(pending 사용자도 가능). body `{package}` → `{paymentHtml, outTradeNo, amount, planName}` 반환. `paymentHtml`은 Alipay 게이트웨이로 자동 제출되는 폼 페이지 |
| `/api/payment/alipay/query` | GET `?outTradeNo=` | 마찬가지로 Bearer 인증. `paid` / `pending` / `closed` / `unknown` 반환 |
| `/api/payment/alipay/notify` | POST(Alipay 서버 콜백) | 5요소 서명 검증(서명, app_id, 금액 일치, TRADE_SUCCESS/TRADE_FINISHED, 가맹점 유일성) → **멱등**으로 주문 업데이트 + 구독 생성 + 계정 활성화. skill은 이 API에 절대 접촉하지 않음 |
| `/payment/alipay/return` | 브라우저 회귀 페이지 | 공개 경로. 결제 후 '결제 성공' 확인 표시, 페이지 내에서 백엔드 실제 상태를 폴링 |

- 미결제 주문은 **2시간 후 자동 종료**. 사용자가 도중에 포기하면 → 그냥 `create-order` 다시 실행. 이전 주문은 신경 쓰지 않아도 됩니다.
- 스크립트는 `paymentHtml`을 임시 HTML 파일로 작성하고, agent가 시스템 명령으로 열면 Alipay 계산대에 진입합니다
  (QR 스캔 또는 Alipay 내 로그인으로 결제).

### 활성화 경로(자동, 수동 불필요)

notify 서명 검증 통과 → `paymentOrders`를 결제 완료로 표시 → `user_subscriptions` 생성/순연
(`planId`, `currentPeriodEnd`는 durationDays로 계산, 갱신은 원래 만료일에 순연) →
`users.accountStatus: active` + `subscriptionStatus: ACTIVE` → 회귀 페이지가 paid를 폴링해 성공 표시.

### 결제 후 반드시 새 로그인 상태로 교체(중요)

JWT에는 구독 클레임이 들어 있습니다(pending 계정은 `NONE`). **결제 입금은 DB만 업데이트하고 이미 발급된
JWT는 바꾸지 않습니다** — 이전 token의 클레임은 그대로 NONE이라서, 그것으로 로그인 링크를 생성하면 '멤버십이 없는' 것처럼 보입니다.
그래서 skill은 `paid` / PayPal `ACTIVE` 확인 후 먼저 `refresh-login`을 실행하고(재로그인으로 새 JWT 교체, 클레임이 ACTIVE로), 
그다음 링크 2를 생성합니다. 설계된 동작이지 취약점 수정이 아닙니다.

## PayPal 구독 채널(skill 대행, 웹 버전이며 비(非) HarmonyOS)

플랜은 Premium Monthly 하나뿐입니다(약 $1/월, `/api/subscription/plans` 반환값 기준). **월간 자동 갱신**이며,
사용자는 언제든 PayPal에서 해지할 수 있습니다.

### 인터페이스 계약(skill 스크립트가 이미 래핑. agent가 직접 요청을 조립하지 않음)

| 인터페이스 | 메서드 | 설명 |
|---|---|---|
| `/api/subscription/plans` | GET | Bearer 인증. 사용 가능한 플랜 목록 반환(현재 1개) |
| `/api/subscription/create` | POST | body `{planId}` → `{subscriptionId, approveUrl, status}` 반환. `status`는 보통 `APPROVAL_PENDING` |
| `/api/subscription/create` | GET | Bearer 인증. `{activeSubscription, allSubscriptions}` 반환. agent는 `activeSubscription.subscription.status === 'ACTIVE'`를 폴링 |
| `/api/subscription/verify` | POST | 성공 페이지가 자동 호출(cookie 포함). webhook이 안 왔을 때 PayPal API로 직접 활성화 |
| `/subscription/success` | 브라우저 리턴 페이지 | PayPal 승인 후 착지 페이지. verify를 자동 폴링하고 활성화 후 홈/원래 페이지로 복귀 |
| `/subscription/cancel` | 브라우저 페이지 | 사용자가 취소하거나 실패했을 때 착지 페이지. 다시 시작 가능 |

### 대행 흐름

```
create-order --provider paypal  # → approveUrl 반환, 로컬 HTML 파일로 기록
HTML 파일 열기                   # → 브라우저가 PayPal 승인 페이지로 이동
query(10~15초마다)               # → ACTIVE까지 폴링
refresh-login                   # → 새 JWT로 교체(구독 클레임 ACTIVE)
login-link --target home        # → 정식 로그인 링크 생성
```

- 1시간 안에 완료되지 않은 PENDING 구독은 백엔드가 자동 정리합니다. 다시 시작하면 됩니다.
- 사용자가 `create-order`를 반복하면 백엔드가 유효한 `APPROVAL_PENDING` 구독을 재사용해 409를 피합니다.
- Alipay와 동일: 입금은 DB만 갱신하고 기존 JWT는 자동 갱신되지 않으므로, 홈 링크를 보내기 전에 **반드시** `refresh-login`을 실행하세요.

## 구독 페이지의 4가지 채널

구독 페이지 `src/app/(public)/subscription/page.tsx`는 실행 환경에 따라 표시합니다:

| 채널 | 환경 | 메커니즘 | 활성화 방식 |
|---|---|---|---|
| **Alipay(주력)** | 웹 버전 | `AlipayPaymentSection`이 vibepay API 사용(위 표) | notify 서버 자동 활성화, 초 단위 |
| PayPal 구독 | 웹 버전(HarmonyOS 제외) | `/api/subscription/create` → PayPal 인가로 이동. 월간 자동 갱신, 언제든 해지 가능(`/api/subscription/manage`) | PayPal Webhook(`BILLING.SUBSCRIPTION.*`)으로 자동 active |
| WeChat 스캔 구독 | 웹 버전(HarmonyOS 제외) | 페이지 하단 'WeChat 스캔 구독': QR 송금 | **수동 확인**, 입금 지연 가능. 결제 직후 실패로 판단하지 말 것 |
| 화웨이 인앱 결제 | HarmonyOS 앱 내 | 네이티브 `NativeBridge.purchaseSubscription()` | `/api/subscription/activate-huawei`가 화웨이 주문 검증 후 활성화 |

PayPal 플랜과 가격은 `/api/subscription/plans`에서 동적으로 읽습니다. 페이지 고정 문구: Auto-renews. Cancel anytime.

## 상태와 전환

- Alipay 결제 완료 → 회귀 페이지에 성공 표시. PayPal 성공 → `/subscription/success` → 계정 active →
  `next` 파라미터가 지정한 원래 페이지로 자동 복귀(없으면 홈).
- 이미 구독 중인 사용자가 구독 페이지 방문 → "You're All Set!" 표시, 3초 후 자동으로 홈으로.
- 결제 실패/취소(PayPal)→ `/subscription/cancel`, 다시 시도할 수 있습니다.

## 해결

| 현상 | 처리 |
|---|---|
| Alipay로 결제했는데 `query`가 계속 pending | notify 지연은 드뭅니다. 30초 기다렸다가 다시 조회. 그래도 안 되면 사용자에게 브라우저 회귀 페이지 상태를 확인하게 하고, 그래도 안 되면 플랫폼 지원(dongtao@outlook.com)에 `outTradeNo`를 첨부해 연락 |
| Alipay로 결제했는데, 링크 2로 들어가도 계속 막힘 | `refresh-login`이 빠졌음(이전 JWT 클레임 미갱신) — 먼저 `refresh-login`, 그다음 `login-link` |
| PayPal `query`가 계속 PENDING | 사용자가 PayPal에서 승인을 완료하지 않았습니다. 브라우저에서 승인 링크가 열렸는지 확인. 승인했는데도 PENDING이면 webhook 지연일 수 있으니 성공 페이지에서 몇 초 더 기다리거나 새로고침 |
| PayPal `query`가 409 반환 | 미완료 PENDING 구독이 이미 있습니다. 1시간 기다려 만료시키거나, 브라우저에서 이전 링크 승인을 완료 |
| PayPal 결제했는데 링크 2로 들어가도 계속 막힘 | Alipay와 동일: 먼저 `refresh-login`, 그다음 `login-link` |
| 결제했는데 계속 403(PayPal) | Webhook이 가끔 지연됩니다. 다시 로그인해 상태 갱신 |
| WeChat으로 결제했는데 개통 안 됨 | 수동 확인은 비동기입니다. 몇 시간 내에 개통되지 않으면 플랫폼 지원에 연락 |
| 구독 페이지에 "No subscription plans available" 표시 | `/api/subscription/plans`에 사용 가능한 PayPal 플랜이 없는 플랫폼 측 설정 문제. 중국 내 사용자는 Alipay를 쓰면 됩니다 |

## 역사적 비고

코드에는 **오래된** Alipay 웹 결제가 하나 더 있습니다(`src/lib/alipay.ts`, `/api/payment/create-order`,
¥9.90/¥99 일회성 매수, 샌드박스에서 키 미설정 시 모의 결제로 다운그레이드). 단, 구독 페이지 UI에는 한 번도 연결되지 않았고 vibepay와
무관합니다. skill은 이에 일절 접촉하지 않습니다. 현재 채널은 `alipay-vibepay.ts`입니다.
