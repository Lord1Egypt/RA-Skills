# meta-coordinator Korean demo script

## Scenario A — billing/webhook incident

### 1. CS intake
고객이 오늘 아침부터 결제 확인이 늦고 webhook 처리도 깨진 것 같다고 합니다.

Expected behavior:
- build issue skeleton first
- classify as incident
- severity high
- state TRIAGED

### 2. Ops evidence
오전 9시 5분 이후 Stripe 카드 결제 전체에서 같은 증상이 보입니다. billing webhook worker에서 retry가 늘고 backlog도 쌓이고 있습니다.

Expected behavior:
- confidence increases
- primary module billing-webhook
- state TRIAGED -> ASSIGNED
- primary owner Billing Engineering
- backup owner Platform Backend Team

### 3. No response
1시간 동안 엔지니어링 업데이트가 없습니다.

Expected behavior:
- do not resolve
- produce Follow-up Check
- ask for ETA / mitigation / backlog / customer impact

### 4. Partial recovery
rollback은 완료됐고 신규 webhook은 처리되기 시작했습니다. 다만 기존 backlog는 아직 비우는 중입니다.

Expected behavior:
- remain ASSIGNED
- do not resolve yet

### 5. Recovery confirmed
backlog가 모두 비워졌고 최근 테스트 결제가 정상 확인됩니다. Support에서도 PRO 활성화가 다시 정상 동작하는 것 확인했습니다.

Expected behavior:
- move ASSIGNED -> RESOLVED
- summarize recovery and next follow-up items

## Scenario B — permission/access issue

### 1. CS intake
결제는 됐는데 초대한 팀원이 아직 팀 워크스페이스에 접근을 못 합니다.

Expected behavior:
- primary module workspace-membership-sync
- secondary entitlement-sync / auth-service
- category permission issue
- likely owner Account Platform Team

### 2. Additional evidence
payment verified as captured, entitlement record exists, workspace membership sync failed.

Expected behavior:
- move to ASSIGNED
- route to Account Platform Team

### 3. No response
3시간 무응답.

Expected behavior:
- escalation follow-up
- keep issue active

### 4. Resolution
membership sync replay completed and Support verified access.

Expected behavior:
- move to RESOLVED

## Short usage examples

### Example input 1
Customer says payment confirmation is delayed and webhook processing seems broken since this morning.

### Example input 2
Paid teammate still cannot access the team workspace after payment and invitation.
