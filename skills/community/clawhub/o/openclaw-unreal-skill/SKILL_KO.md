# OpenClaw Unreal Skill

OpenClaw AI 어시스턴트를 통해 Unreal Editor를 제어합니다.

## 안전 및 권한

**이 스킬이 바꿀 수 있는 것:** Unreal Editor가 할 수 있는 모든 것 — 액터와 컴포넌트,
트랜스폼, 열려 있는 레벨, 임포트한 에셋, PIE(Play In Editor), 그리고 콘솔 명령
(`console.execute`)이 닿는 범위 전부입니다.

**확인 없이 실행되는 것:** 조회 전용 도구뿐입니다 — `level.getCurrent`, `level.list`,
`actor.find`, `actor.getAll`, `actor.getData`, `transform.get*`, `component.get`,
`editor.getState`, `asset.list`, `blueprint.list`, `debug.hierarchy`,
`debug.screenshot`, `console.getLogs`, `debug.log`. 동작은 이전과 같습니다.

**런타임에서 차단되는 것:** 프로젝트를 바꾸는 모든 도구 — `actor.create`,
`actor.delete`, `actor.setProperty`, `transform.set*`, `component.add`/`remove`,
`level.open`, `level.save`, `asset.import`, `console.execute`, `input.simulate*`,
`editor.play`/`stop`/`pause`/`resume`, `blueprint.open` — 그리고 이들을 담은 배치
호출입니다. 게이트웨이 익스텐션이 기본적으로 거부합니다. 알지 못하는 이름은 동사가
명백히 조회형이 아닌 한 프로젝트 변경으로 간주합니다. 즉 모르면 막습니다.

**허용하는 방법** — 두 단계가 모두 필요합니다:

1. 운영자가 게이트웨이를 옵트인 환경 변수와 함께 시작합니다. 게이트웨이 프로세스에서
   읽는 값이므로 모델이 스스로 설정할 수 없습니다:

   ```bash
   OPENCLAW_EDITOR_ALLOW_DESTRUCTIVE=1 openclaw gateway restart
   # 이 스킬에만 적용하려면:
   OPENCLAW_UNREAL_ALLOW_DESTRUCTIVE=1 openclaw gateway restart
   ```

2. 사용자가 그 변경을 승인한 뒤, 호출마다 `confirm: true`를 함께 보냅니다:

   ```
   unreal_execute: actor.delete {name: "Cube_01"}, confirm: true
   ```

둘 중 하나라도 빠지면 거부되며, 무엇이 막혔고 어떻게 허용하는지 함께 응답합니다.
그동안 에디터에는 아무것도 전달되지 않습니다.

**먼저 미리보기:** `dryRun: true`는 호출이 어떻게 분류되는지와 무엇이 전송될지만
알려주고, 아무것도 보내지 않습니다:

```
unreal_execute: level.save, dryRun: true
→ {risk: "project-changing", requiresConfirmation: true, wouldRun: false, executed: false}
```

**현재 상태 확인:** `openclaw unreal status`는 프로젝트 변경이 허용되어 있는지
출력하고, `GET /unreal/status`도 `destructiveOperations: "enabled" | "blocked"`로
같은 값을 보고합니다.

**게이트의 적용 범위:** 이 게이트는 스킬에 함께 들어 있는 게이트웨이 익스텐션
(`extension/index.ts`)에 있습니다. 따라서 OpenClaw 게이트웨이를 거치는 모든 호출
(텔레그램, 디스코드 등)에 적용됩니다. Unreal Editor 플러그인이 직접 여는 HTTP
서버(포트 27184, 아래 Mode B)는 플러그인 저장소에서 따로 설치하는 것이라 이
패키지의 게이트가 적용되지 않습니다. 해당 포트는 로컬에만 두고, 자체 제어 수단은
플러그인 저장소를 확인하세요.

영문 `SKILL.md`의 Safety and permissions 와 동일한 기준입니다. 두 문서가 어긋나면
영문 `SKILL.md`가 우선합니다.

## 개요

이 스킬은 OpenClaw Unreal Plugin을 통해 AI 지원 Unreal Engine 개발을 가능하게 합니다. 플러그인은 HTTP 폴링 (`/unreal/*` 엔드포인트)을 통해 OpenClaw Gateway와 통신합니다.

## 아키텍처

```
┌──────────────────┐     HTTP      ┌─────────────────────┐
│  OpenClaw        │ ←──────────→  │  Unreal Editor      │
│  Gateway:18789   │  /unreal/*    │  (C++ Plugin)       │
└──────────────────┘               └─────────────────────┘
         ↑
         │ Extension
┌──────────────────┐
│  extension/      │
│  index.ts        │
└──────────────────┘
```

## 사전 요구 사항

1. Unreal Engine 5.x 프로젝트
2. 프로젝트에 OpenClaw Unreal Plugin 설치
3. OpenClaw Gateway 실행 중 (기본 포트: 18789)

## 설치

### 플러그인 설치

1. `openclaw-unreal-plugin` 폴더를 프로젝트의 `Plugins` 디렉토리에 복사
2. Unreal Editor 재시작
3. Edit → Plugins → OpenClaw에서 플러그인 활성화
4. Window → OpenClaw에서 연결 상태 확인

### 스킬 설치

```bash
# 스킬을 OpenClaw workspace에 복사
cp -r openclaw-unreal-skill ~/.openclaw/workspace/skills/unreal-plugin
```

## 사용 가능한 도구

### Level 관리
- `level.getCurrent` - 현재 레벨 정보 가져오기
- `level.list` - 모든 레벨 나열
- `level.open` - 경로로 레벨 열기
- `level.save` - 현재 레벨 저장

### Actor 조작
- `actor.find` - 이름으로 Actor 찾기
- `actor.getAll` - 모든 Actor 가져오기
- `actor.create` - 새 Actor 스폰 (Cube, PointLight, Camera 등)
- `actor.delete` / `actor.destroy` - Actor 제거
- `actor.getData` - Actor 상세 정보 가져오기
- `actor.setProperty` - Actor 속성 수정

### Transform
- `transform.getPosition` / `setPosition`
- `transform.getRotation` / `setRotation`
- `transform.getScale` / `setScale`

### Component
- `component.get` - Actor 컴포넌트 가져오기
- `component.add` - 컴포넌트 추가
- `component.remove` - 컴포넌트 제거

### Editor 제어
- `editor.play` - PIE (Play In Editor) 시작
- `editor.stop` - PIE 중지
- `editor.pause` / `resume` - 게임플레이 일시정지/재개
- `editor.getState` - 플레이 중인지 에디팅 중인지 확인

### Debug
- `debug.hierarchy` - World Outliner 트리
- `debug.screenshot` - 뷰포트 캡처
- `debug.log` - Output에 메시지 로그

### Input 시뮬레이션
- `input.simulateKey` - 키보드 입력 (W, A, S, D, Space 등)
- `input.simulateMouse` - 마우스 클릭/이동/스크롤
- `input.simulateAxis` - 게임패드/축 입력

### 에셋
- `asset.list` - 콘텐츠 브라우저 탐색
- `asset.import` - 외부 에셋 임포트

### 콘솔
- `console.execute` - 콘솔 명령 실행
- `console.getLogs` - Output 로그 메시지 가져오기

### Blueprint
- `blueprint.list` - 프로젝트의 블루프린트 나열
- `blueprint.open` - 에디터에서 블루프린트 열기

## 사용 예제

```
사용자: 위치 (100, 200, 50)에 큐브 만들어
AI: [unreal_execute tool="actor.create" parameters={type:"Cube", x:100, y:200, z:50} 사용]

사용자: 플레이어 스타트를 센터로 옮겨
AI: [unreal_execute tool="actor.find" parameters={name:"PlayerStart"} 사용]
    [unreal_execute tool="transform.setPosition" parameters={name:"PlayerStart", x:0, y:0, z:0} 사용]

사용자: 스크린샷 찍어
AI: [unreal_execute tool="debug.screenshot" 사용]

사용자: 게임 시작해
AI: [unreal_execute tool="editor.play" 사용]
```

## 설정

프로젝트 루트에 `openclaw.json` 생성 (선택사항):

```json
{
  "host": "127.0.0.1",
  "port": 18789,
  "autoConnect": true
}
```

또는 `~/.openclaw/unreal-plugin.json`에 전역 설정.

## HTTP 엔드포인트

Extension이 OpenClaw Gateway에 등록하는 엔드포인트:

| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| `/unreal/register` | POST | 새 세션 등록 |
| `/unreal/poll` | GET | 대기 중인 명령 폴링 |
| `/unreal/heartbeat` | POST | 세션 유지 |
| `/unreal/result` | POST | 도구 실행 결과 전송 |
| `/unreal/status` | GET | 모든 세션 상태 조회 |

## 문제 해결

### 플러그인 연결 안됨
- `[OpenClaw]` 메시지에 대해 Output Log 확인
- Gateway 실행 확인: `openclaw gateway status`
- 포트 18789 접근 가능 확인
- Window → OpenClaw에서 연결 상태 확인 시도

### 세션 만료
- 플러그인이 세션 만료 시 자동 재연결
- Gateway 재시작 여부 확인

### 도구 작동 안함
- 플러그인 활성화 확인 (Edit → Plugins)
- 레벨 Actor 수정 시 PIE 상태가 아닌지 확인
- Actor 이름이 정확히 일치하는지 확인 (대소문자 구분)

## 🔐 보안: 모델 호출 설정

ClawHub에 퍼블리시할 때 `disableModelInvocation`을 설정할 수 있습니다:

| 설정 | AI 자동 호출 | 사용자 명시적 요청 |
|------|-------------|------------------|
| `false` (기본값) | ✅ 허용 | ✅ 허용 |
| `true` | ❌ 차단 | ✅ 허용 |

### 권장: **`true`**

**이유:** 이 스킬은 Actor 삭제·레벨 저장·콘솔 명령 실행·입력 시뮬레이션처럼
프로젝트 상태를 바꾸는 동작을 노출합니다. 조회만 하는 도구가 아니므로 모델이
스스로 시작해서는 안 됩니다.

v1.1.0 기준 이 스킬은 `disableModelInvocation: true` 로 배포되며, **사용자가
명시적으로 요청할 때만 실행됩니다.** 그 위에 프로젝트를 바꾸는 호출은 런타임에서
따로 차단됩니다 — [안전 및 권한](#안전-및-권한) 참고. 영문 `SKILL.md` 의
Security & Privacy Disclosure 와 동일한 기준입니다.

## 보안 및 개인정보 공시

이 스킬은 실행 중인 Unreal Editor 를 제어합니다. 기능과 한계를 그대로 공개합니다.

- **로컬 HTTP 서버 강화 (플러그인 v1.3.1+)**: 내장 서버(포트 27184)는 브라우저에서
  온 요청(`Origin` 헤더가 있으면 403)을 거부하고, 공유 비밀키 인증을 선택적으로
  지원합니다 — Unreal Editor 프로세스와 MCP 클라이언트 양쪽에 `OPENCLAW_BRIDGE_TOKEN`
  을 설정하면 모든 요청에 `X-OpenClaw-Token` 이 필요합니다. 토큰을 설정하지 않으면
  신뢰할 수 있는 기기에서만 포트를 여세요 — 로컬의 어떤 프로세스든 에디터 명령을
  보낼 수 있습니다.
- **파괴적 동작은 런타임에서 차단됩니다 (v1.1.0+)**: Actor 삭제, 레벨 저장, 에셋
  임포트, 콘솔 명령 실행(`console.execute`), 키보드/마우스 입력 시뮬레이션은
  게이트웨이를 `OPENCLAW_EDITOR_ALLOW_DESTRUCTIVE=1` 로 시작하고 **동시에** 호출이
  `confirm: true` 를 담고 있을 때만 실행됩니다. 설정하기 전에 사용자에게 확인하세요
  — [안전 및 권한](#안전-및-권한) 참고. 모호한 요청에서 암묵적으로 실행되어서는
  안 됩니다.
- **데이터 노출**: `debug.screenshot` 과 `console.getLogs` 는 화면에 있거나 로그에
  남은 것을 그대로 담습니다 — 자격증명·토큰·로컬 경로가 포함될 수 있습니다. 기기
  밖으로 공유하기 전에 확인하세요.
- **트리거 범위**: "정리해줘", "다 저장해" 같은 평범한 요청도 상태를 바꾸는 에디터
  작업으로 이어집니다 — 세션에서 **상태를 바꾸는 첫 호출 전에 한 번 확인**하세요.
- **안전 기본값**: `disableModelInvocation: true`. 프로젝트를 바꾸는 도구는 기본이
  거부이고, `dryRun: true` 로 전송 없이 미리 볼 수 있습니다. 자동화 세션 전에
  프로젝트를 버전 관리에 올려두세요.

## CLI 명령

```bash
# Unreal 연결 상태 확인
openclaw unreal status
```

## 라이선스

MIT 라이선스 - LICENSE 파일 참조
