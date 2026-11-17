<div align="center">

# 🤖 Omnibot

### AI 에이전트를 위한 브라우저 인프라

[![Version](https://img.shields.io/badge/version-2.4.0-blue?style=flat-square)](./SKILL.md)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=flat-square)]()

[![SkillHub](https://img.shields.io/badge/SkillHub-omnibot-00A8E0?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNOCAwTDAgNFYxMkw4IDE2TDE2IDEyVjRMOCAwWiIgZmlsbD0id2hpdGUiLz48L3N2Zz4=)](https://skillhub.cn/skills/omnibot)
[![ClawHub](https://img.shields.io/badge/ClawHub-omnibot--skills-FF6B35?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNOCAxQzQuMTMgMSAxIDQuMTMgMSA4QzEgMTEuODcgNC4xMyAxNSA4IDE1QzExLjg3IDE1IDE1IDExLjg3IDE1IDhDMTUgNC4xMyAxMS44NyAxIDggMVpNOCAzQzkuNjYgMyAxMSA0LjM0IDExIDZDMTEgNy42NiA5LjY2IDkgOCA5QzYuMzQgOSA1IDcuNjYgNSA2QzUgNC4zNCA2LjM0IDMgOCAzWiIgZmlsbD0id2hpdGUiLz48L3N2Zz4=)](https://clawhub.ai/dennisjcy/skills/omnibot-skills)

[![Chrome 웹 스토어](https://img.shields.io/badge/Chrome%20웹%20스토어-브라우저%20확장-4285F4?style=flat-square&logo=google-chrome&logoColor=white)](https://chromewebstore.google.com/detail/fojlpefamkmjbboafmjkkaejohagbdgn)

**AI 에이전트를 실제 Chromium 브라우저에 연결합니다.**<br>
페이지를 읽습니다. 버튼을 클릭합니다. 폼을 채웁니다. 탐색합니다. 콘텐츠를 추출합니다. 증거를 수집합니다.<br>
로컬 데몬과 CLI를 통해 모든 것을 수행합니다 — 헤드리스 해킹 없음, 취약한 선택자 없음.

[빠른 시작](#-빠른-시작) · [작동 방식](#-작동-방식) · [기능](#-기능) · [문서](#-문서)

🌐 **[English](./README.md)** · **[中文](./README_zh.md)** · **[日本語](./README_ja.md)** · **[Español](./README_es.md)** · **[Français](./README_fr.md)** · **[Deutsch](./README_de.md)**

</div>

---

## 🚀 Omnibot이란?

Omnibot는 AI 에이전트와 실제 웹 사이의 간격을 해소합니다. **Hermes**, **Claude Code**, **Codex**, **OpenCode** 및 기타 에이전트에게 살아있는 Chromium 브라우저를 보고 상호 작용할 수 있는 능력을 부여합니다 — 인간과 같은 방식으로.

```
┌──────────────┐         ┌──────────────┐         ┌──────────────────┐
│   AI Agent   │ ──CLI──▶│  Omnibot     │ ──WS──▶ │  Chromium        │
│  (Hermes,    │         │  데몬        │         │  확장 프로그램   │
│   Claude...) │         │  :18765      │         │  (실제 브라우저) │
└──────────────┘         └──────────────┘         └──────────────────┘
```

Puppeteer 없음. Playwright 없음. 실제처럼 가장하는 헤드리스 브라우저 없음.<br>
**실제 브라우저. 실제 쿠키. 실제 확장 프로그램. 실제 사용자 세션.**

## 🎬 데모 영상

<table>
<tr>
<td width="50%" align="center" valign="top">

### WeChat 공식 계정 분석
**Hermes가 WeChat 백엔드 데이터 및 트렌드를 자동 분석**

[![WeChat 분석](https://img.youtube.com/vi/xZ-_0TInCRE/maxresdefault.jpg)](https://youtu.be/xZ-_0TInCRE)

*Hermes 에이전트가 WeChat 공식 계정 백엔드에 자동 로그인하여 사용자 성장, 기사 조회수, 사용자 통계를 추출하고 완전한 데이터 분석 보고서를 생성합니다.*

</td>
<td width="50%" align="center" valign="top">

### X (Twitter) AI 뉴스 수집
**Hermes가 X에서 최신 AI 뉴스를 자동 수집**

[![X AI 뉴스](https://img.youtube.com/vi/PknnOhAE6bI/maxresdefault.jpg)](https://youtu.be/PknnOhAE6bI)

*Hermes 에이전트가 X (Twitter)를 자동 브라우징하여 최신 AI 뉴스를 검색하고 필터링하며, 구조화된 뉴스 브리핑으로 정리합니다.*

</td>
</tr>
<tr>
<td width="50%" align="center" valign="top">

### 법원 문서 분석
**Hermes가 살인 사건 판결문을 검색 및 분석**

[![법원 분석](https://img.youtube.com/vi/PQQNDbzgXgQ/maxresdefault.jpg)](https://youtu.be/PQQNDbzgXgQ)

*Hermes 에이전트가 법원 기록에서 살인 사건을 검색하고, 8건의 전체 사건 파일을 읽으며, 범죄자 프로필, 동기 분석, 범죄 패턴을 포함한 종합 분석 보고서를 생성합니다.*

</td>
<td width="50%" align="center" valign="top">

### Toutiao 자동 게시
**Hermes가 기사를 Toutiao에 자동 게시**

[![Toutiao 게시](https://img.youtube.com/vi/elUxHLp1C4Q/maxresdefault.jpg)](https://youtu.be/elUxHLp1C4Q)

*Hermes 에이전트가 Toutiao에 자동 로그인하여 제목, 본문 텍스트를 입력하고 이미지를 삽입하며, 커버와 광고 수익을 설정하고, 미리보기 후 원클릭으로 기사를 게시합니다.*

</td>
</tr>
</table>

<div align="center">

**더 많은 사용 사례가 여러분을 기다리고 있습니다!**

</div>

## ✨ 기능

<table>
<tr>
<td width="50%" valign="top">

### 🔍 관찰
- 렌더링된 페이지 콘텐츠를 깔끔한 텍스트/마크다운으로 읽기
- 대화형 참조가 포함된 전체 접근성 트리 스냅샷
- 전체 페이지 또는 특정 시각적 영역의 스크린샷 캡처
- 콘솔 로그, 네트워크 트래픽 및 DOM 상태 검사

</td>
<td width="50%" valign="top">

### 🎯 작업
- 의미적 역할, 플레이스홀더 또는 접근성 참조로 요소 클릭
- 폼 채우기, 옵션 선택, 체크박스 선택 — 이벤트 디스패치 포함
- 페이지 간 탐색, 탭 및 탭 그룹 관리
- 드래그, 스크롤, 입력, 키 누르기 — 인간 같은 상호 작용

</td>
</tr>
<tr>
<td width="50%" valign="top">

### ✅ 검증
- 조건 대기: URL 변경, 요소 가시성, 텍스트 출현
- 요소 상태 어설션: 활성화됨, 보임, 선택됨, 값
- 네트워크 로그 및 API 증거 캡처
- 관찰 → 작업 → 검증 루프가 포함된 다단계 검증

</td>
<td width="50%" valign="top">

### 🛡️ 신뢰성
- 세션 토큰 워크플로우 격리
- 탭 대상 명령 — 실수로 인한 크로스 탭 변경 없음
- 의미적에서 원시 CDP까지의 7단계 폴백 체인
- 내장된 안티패턴 가드 및 안전 규칙

</td>
</tr>
</table>

## ⚡ 빠른 시작

### 1. CLI 설치

npm을 통해 Omnibot CLI를 전역 설치(권장):

```bash
npm install -g @omniaibot/omnibot
```

플랫폼을 자동 감지하여 해당 바이너리를 설치합니다. 설치 후 `omnibot doctor`를 실행하여 확인하세요.

### 2. 브라우저 확장 프로그램 로드

- [Chrome 웹 스토어의 Omnibot 확장 프로그램 페이지](https://chromewebstore.google.com/detail/fojlpefamkmjbboafmjkkaejohagbdgn)를 엽니다
- "Chrome에 추가"를 클릭하고 설치를 완료합니다
- 브라우저 오른쪽 상단의 Omnibot 확장 프로그램 아이콘을 클릭합니다
- 확장 프로그램에 **연결됨**이 표시되는지 확인하거나, 팝업에서 머신 코드를 복사하여 활성화 코드를 구매합니다

기본적으로 확장 프로그램은 로컬 WebSocket 서비스 `127.0.0.1:18765`에 연결합니다.

확장 프로그램 팝업 설정:
- **WebSocket 주소**: `ws://127.0.0.1:18765`
- 연결 상태가 자동 새로고침됩니다
- 연결에 실패하면 먼저 `omnibot doctor`를 실행하여 데몬 상태를 확인하세요

### 3. 연결 확인

데몬을 수동으로 시작할 필요가 없습니다. 브라우저 명령을 실행하면 omnibot CLI가 로컬 데몬을 자동 시작하고, 브라우저 확장 프로그램이 WebSocket을 통해 `127.0.0.1:18765`에 연결합니다.

```bash
omnibot doctor
omnibot tabs
```

`doctor`는 데몬과 확장 프로그램 상태를 확인합니다. `tabs`는 사용 가능한 브라우저 탭을 나열합니다.

`doctor`가 확장 프로그램이 연결되지 않았다고 표시하면, Chrome/Edge를 열고 브라우저 확장 프로그램을 로드하거나 다시 로드한 후 최소한 하나의 HTTP/HTTPS 탭을 열어두세요.

### 4. 에이전트 스킬 설치

Omnibot v2는 MCP 프롬프트 주입 대신 스킬을 사용합니다:

```bash
omnibot skills install --agent hermes --profile nuwa
omnibot skills install --agent opencode
omnibot skills install --agent claude
omnibot skills install --agent codex
```

내장 스킬 경로 확인:

```bash
omnibot skills path
```

Omnibot은 인기 있는 AI 에이전트의 스킬 설정을 내장하고 있습니다. 빠른 시작 페이지에서 에이전트를 선택하여 설치 명령을 확인하세요.

## 🔄 작동 방식

모든 브라우저 작업은 규율 있는 루프를 따릅니다:

```
  ┌──────────┐      ┌──────────┐      ┌──────────┐
  │  관찰    │ ───▶ │  작업    │ ───▶ │  검증    │──┐
  │          │      │ (한 번)  │      │          │  │
  └──────────┘      └──────────┘      └──────────┘  │
       ▲                                              │
       └──────────── 실패 시 폴백으로 재시도 ─────────┘
```

1. **관찰** — 페이지 스냅샷, 콘텐츠 읽기, 현재 상태 확인
2. **작업** — 사용 가능한 최선의 패턴을 사용하여 한 번의 작업 수행
3. **검증** — 증거로 예상되는 상태 변경 확인

검증이 실패하면, 에이전트는 다시 관찰하고 다음 폴백 티어를 시도합니다. 맹목적인 재시도 없음. 추측 없음.

## 🧩 네이티브 명령 라우터

Omnibot는 항상 작업에 가장 좁은 네이티브 명령을 선택합니다:

| 의도 | 네이티브 명령 | 이것 말고 |
|------|-------------|----------|
| 페이지 콘텐츠 읽기 | `read`, `get text` | ~~`execute-js`~~ |
| 버튼 클릭 | `find --action click`, `click @eN` | ~~`querySelector().click()`~~ |
| 폼 채우기 | `fill`, `type` | ~~`element.value = "..."`~~ |
| 상태 대기 | `wait` | ~~`sleep 3`~~ |
| 스크롤 | `scroll`, `scrollintoview` | ~~`window.scrollTo()`~~ |

**네이티브가 우선. JavaScript는 폴백이지 지름길이 아닙니다.**

## 🏗️ 아키텍처

```
Agent Skill (SKILL.md)
    │
    ▼
omnibot CLI  ──────────────────────────────┐
    │                                       │
    ▼                                       ▼
로컬 데몬 (:18765)                  Chromium 확장 프로그램
    │                                       │
    ├── 세션 관리                           ├── DOM 접근
    ├── 명령 라우팅                         ├── 접근성 트리
    ├── 탭 추적                             ├── 네트워크 인터셉트
    └── 워크플로우 격리                     └── 시각적 영역 감지
```

**핵심 설계 원칙:**
- **신뢰성 > 편의성** — 모든 작업이 검증됨
- **명시적 상태 > 암시적 상태** — 숨겨진 가정 없음
- **패턴 > 명령** — API가 아닌 작업에서 시작
- **폴백은 허용되지만, 우선은 아님**

## 📚 문서

| 리소스 | 설명 |
|--------|------|
| [SKILL.md](./SKILL.md) | 전체 에이전트 실행 사양 |
| [명령 참조](./references/command-reference.md) | 완전한 CLI 명령 조회 |
| [작업 패턴](./references/operation-patterns.md) | 읽기, 클릭, 채우기, 스크롤, 탐색, 대기, 추출, 배치 |
| [안티패턴](./references/anti-patterns.md) | 일반적인 실수와 피하는 방법 |
| [디버깅 및 증거](./references/debugging-and-evidence.md) | 스크린샷, 네트워크 로그, 추적, 기록/재생 |
| [세션 및 탭](./references/session-and-tabs.md) | 워크플로우 격리 및 탭 대상 지정 |
| [폴백 작업](./references/fallback-operations.md) | 7단계 폴백 체인 설명 |

## 🤝 호환되는 에이전트

Omnibot는 CLI 명령을 실행할 수 있는 모든 에이전트 시스템과 작동합니다:

- 🧠 **Hermes** — 네이티브 통합
- 🟠 **Claude Code** — 스킬 파일을 통해
- 📦 **Codex** — 스킬 파일을 통해
- 🔓 **OpenCode** — 스킬 파일을 통해
- 🔧 **CLI 지원 에이전트** — `omnibot` 명령을 통해

## 📋 워크플로우 예시

```bash
# 워크플로우 컨텍스트 설정
export OMNIBOT_SESSION_TOKEN=research

# 새 탭 열기
omnibot open "https://github.com"

# 대화형 참조로 페이지 스냅샷
omnibot snapshot -i --tab-id $TAB_ID

# 검색 상자를 클릭하고 입력
omnibot find placeholder "Search GitHub" --action type \
  --action-value "omnibot" --tab-id $TAB_ID

# Enter 누르기
omnibot press Enter --tab-id $TAB_ID

# 결과 대기
omnibot wait --text "repositories" --tab-id $TAB_ID

# 결과 읽기
omnibot read --tab-id $TAB_ID
```

## 📄 라이선스

독점적. 자세한 내용은 LICENSE를 참조하십시오.

---

<div align="center">

**웹을 "봐야 하는" 에이전트를 위해 — 단순히 가져오는 것이 아니라.**

[⭐ GitHub에서 스타](https://github.com/DennisJcy/Omnibot-skills) · [📖 스킬 사양 읽기](./SKILL.md)

</div>
