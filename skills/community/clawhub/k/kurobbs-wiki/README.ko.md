# 🌊 kurobbs-wiki — 쿠로블록스 명조 WIKI 조회 + 파티 편성 도우미

> 🌍 **이 문서 읽기** · [English](README.en.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [中文](README.md)

**Agent Skill 공개 표준**(SKILL.md)을 따르는 범용 스킬로, 쿠로블록스(kurobbs) 공개 API를 통해 명조(Wuthering Waves)의 도감·공략·캐릭터 정보를 바로 조회하고, **메커니즘 분석 + 파티 편성 엔진**을 내장하며, 본인 쿠로블록스 계정으로 로그인해 실제 캐릭터 풀로 팀을 짤 수도 있습니다. Agent Skill을 불러올 수 있는 모든 AI(Claude, Cursor, Copilot, Gemini, OpenClaw 등)를 지원합니다.

> 이 프로젝트는 명조를 하면서 "캐릭터 공략·파티 편성을 보려면 웹페이지를 하나씩 뒤져야 한다"는 불편함에서 출발했으며, 스킬 하나로 대화 중에 바로 물어볼 수 있게 만들었습니다.

---

## ✨ 기능 한눈에 보기

| 모듈 | 명령 | 설명 |
|------|------|------|
| 🔍 목차/목록 | `tree` / `list` | 분류 목차 트리(170+ 노드) + 분류별 항목 |
| 📖 항목 상세 | `detail` | 캐릭터/무기/아이템/공략 상세, `--render` Markdown 정렬·`--section` 정밀 구간 추출 지원 |
| 🔎 이름 검색 | `search` | 분류를 넘나드는 검색, 3단 하위 분류 자동 탐색 |
| 🖼️ 커뮤니티 게시물 미디어 | `post` | WAF 우회로 한 장 요약/영상 게시물의 이미지·커버·m3u8 영상 가져오기 |
| 🧠 메커니즘 분석 | `probe` | 6개 차원 메커니즘 프로필(효과/버프/계열/스킬/에코/무기) |
| 🤝 페어링 엔진 | `pair` / `team` | 두 캐릭터 5차원 호환성 점수, 풀 선택 팀 구성, 전체 60명 열거, 공략 교차 검증 풀 보충 |
| 🎯 LLM 정밀 정렬 | `candidates` + `--profile` | 규칙 기반 1차 후보 필터 + LLM 팀별 정밀 정렬(가장 정확한 편성) |
| 👤 내 계정 | `my` | 쿠로블록스 로그인, 실제 캐릭터 조회, 내 캐릭터로 팀 구성, token 갱신 |

---

## 📦 설치

### 방법 1: 로컬 디렉터리에서 설치(가장 간단)

본 저장소의 `kurobbs-wiki/` 디렉터리를 AI의 skills 디렉터리(Claude Code, Cursor, Copilot 등 모두 지원)에 넣거나, 해당 디렉터리를 지원하는 agent에서:

```bash
# SKILL_DIR을 본 저장소 루트의 절대 경로로 지정
# Windows 예시
set SKILL_DIR=D:\tools\kurobbs-wiki

# macOS / Linux 예시
export SKILL_DIR=~/tools/kurobbs-wiki
```

### 방법 2: npx skills 사용(마켓에 등록된 후)

```bash
npx skills add Alphamancer/kurobbs-wiki
```

> 출시 후 마켓에서 원클릭 설치가 가능합니다. 자세한 내용은 아래 「출시 및 등록」을 참고하세요.

### 의존성

- **Python 3.8+**(순수 표준 라이브러리, `wikiquery.py`는 제3자 의존성 없음)
- **Playwright**(`post`로 커뮤니티 게시물 미디어를 가져올 때만 필요)
  ```bash
  pip install playwright && playwright install chromium
  ```
- **ffmpeg**(선택, `--download-video`로 m3u8 영상을 mp4로 다운로드할 때 사용)

---

## 🚀 빠른 시작

```bash
cd $SKILL_DIR

# 1. 디렉터리 트리 초기화(~/.kurobbs-wiki-cache/에 캐시)
python -X utf8 -u scripts/wikiquery.py tree

# 2. 캐릭터 검색
python -X utf8 -u scripts/wikiquery.py search 穗穗 --preview --limit 3

# 3. 공략 본문의 특정 소절 가져오기
python -X utf8 -u scripts/wikiquery.py detail <previewEntryId> --section "编队&队伍轴推荐"

# 4. 메커니즘 분석 + 파티 편성
python -X utf8 -u scripts/wikiquery.py probe 穗穗
python -X utf8 -u scripts/wikiquery.py team 穗穗 --pool 洛瑟菈,今汐,秧秧 --top 3

# 5. 계정 로그인 후 실제 캐릭터로 팀 구성
python -X utf8 -u scripts/wikiquery.py my login    # 브라우저에서 휴대폰 번호 입력 → 슬라이더 → 인증번호 입력
python -X utf8 -u scripts/wikiquery.py my roles
python -X utf8 -u scripts/wikiquery.py my team 穗穗 --guide-pool --top 5
```

> 💡 **팁**: 모든 명령은 skill 디렉터리에서 실행하고, `-X utf8 -u`를 함께 사용해야 합니다(Windows에서 한중일/emoji 출력에 필요).

---

## 🧠 파티 편성 엔진 사용법

### 두 캐릭터 평가

```bash
python -X utf8 -u scripts/wikiquery.py pair 穗穗 洛瑟菈
```

5개 차원 각 20점: 효과 시너지 / 아웃트로 스킬 매칭 / 포지션 보완 / 에코 연계 / 트리거 사이클. 80점 이상이면 높은 적합도.

### 캐릭터 풀로 팀 구성

```bash
python -X utf8 -u scripts/wikiquery.py team 穗穗 --pool 洛瑟菈,今汐,秧秧 --top 3   # 지정 풀
python -X utf8 -u scripts/wikiquery.py team 穗穗 --all --top 5                    # 전체 60명 열거
python -X utf8 -u scripts/wikiquery.py team 穗穗 --guide-pool --top 5             # 공략 교차 검증으로 풀 자동 보충
```

각 팀에는 출처가 표시됩니다: 🟢 공략 실증 / 🟡 혼합 / 🔵 엔진 추론, 그리고 검증을 위해 클릭할 수 있는 📚 공략 URL이 함께 제공됩니다.

### LLM 정밀 정렬(가장 정확한 편성)

```bash
# 1단계: 규칙 기반 1차 후보 필터(초 단위)
python -X utf8 -u scripts/wikiquery.py candidates 绯雪 --guide-pool

# 2단계: 후보 팀 + 세 캐릭터 6차원 전체 프로필 가져오기(출력이 크므로 파일로 리다이렉트)
python -X utf8 -u scripts/wikiquery.py team 绯雪 --pool 千咲,维里奈,穗穗 --profile --top 10 > %TEMP%\team_profile.txt
```

Claude가 실제 프로필 데이터를 바탕으로 팀별 6차원 정밀 정렬을 수행하여, "메커니즘 버프", "협주 서브딜러" 등 규칙으로 판별하기 어려운 포지션을 식별합니다.

---

## 🔐 개인정보 및 데이터 안내

> ⚠️ **꼭 읽어 주세요** — 이 스킬에는 계정 데이터를 읽는 로그인 기능이 포함되어 있습니다.

- **WIKI 조회(`tree`/`list`/`detail`/`search`/`probe`/`pair`/`team`)**: 전부 **공개·인증 없는** API를 사용하며, **로그인이 필요 없고** 개인 데이터와 관련이 없습니다.
- **「내 계정」기능(`my login`/`my roles`/`my team`/`my sync`)**: 브라우저에서 직접 쿠로블록스에 로그인해야 합니다. 로그인 후 다음 데이터는 **로컬** `~/.kurobbs-wiki-cache/`에 저장됩니다:
  - `account.json` — 로그인 token + 내 캐릭터 목록
  - `role_details/` — 각 캐릭터의 공명 체인 해금, 실제 무기/에코, 스킬 레벨, 패널
- **이 데이터는 로컬에만 저장되며 어떤 서버에도 업로드되지 않습니다.** token은 약 45분 후 만료되며, `my renew`로 갱신할 수 있습니다.
- 이 스킬은 **로그인하지 않은 상태에서** 내 계정 캐릭터를 추측하거나 위조하지 않으며, 제3자에게 계정 데이터를 보내지 않습니다.

**완전히 오프라인/비로그인으로 사용하려면**: `tree`/`search`/`detail`/`probe`/`pair`/`team`만 쓰면 되며, `my` 계열 명령은 전혀 필요 없습니다.

---

## 📚 디렉터리 구조

```
kurobbs-wiki/
├── SKILL.md               # Skill 지침(트리거 조건, 명령 빠른 참조, 워크플로, 핵심 함정)
├── README.md              # 이 파일(사용자용)
├── PUBLISHING.md          # 출시 작업 체크리스트(작성자 전용, 사용자는 볼 필요 없음)
├── _meta.json             # skill 메타데이터
├── references/
│   └── catalogue-map.md   # 분류 ID 매핑 빠른 참조표(170+ 노드)
└── scripts/
    ├── wikiquery.py       # 메인 CLI(tree/list/detail/search/probe/pair/team/candidates/my) 순수 표준 라이브러리
    ├── post_fetch.py      # 커뮤니티 게시물 미디어 가져오기(Playwright로 WAF 우회)
    └── kuro_login.py      # 쿠로블록스 로그인(브라우저 상호작용)
```

---

## ⚠️ 알려진 제한 사항

- **비공개 API, 공식 문서 없음**: 필드 구조가 쿠로블록스 개편에 따라 바뀔 수 있습니다. 오류 발생 시 먼저 `tree --refresh`로 디렉터리 트리를 다시 가져오세요.
- **저빈도 사용**: 공개·인증 없는 인터페이스이므로 잦은 요청은 리스크 관리를 유발할 수 있으며, 스크립트에 0.05초 속도 제한이 내장되어 있습니다.
- **분류 동적 변화**: 게임 업데이트로 신규 버전 활동 분류가 추가되며, 새 콘텐츠가 검색되지 않으면 `list <분류> --refresh` 또는 `tree --refresh`를 사용하세요.
- **공략 항목은 "플레이스홀더 카드"**: `detail <5자리 id>`가 2031을 반환할 수 있으며, 내장된 실제 entryId를 얻으려면 `search --preview`를 사용해야 합니다(이는 구조이지 버그가 아닙니다).
- **Windows에서는 반드시 `-X utf8 -u` 필요**: 그렇지 않으면 한중일/emoji 출력이 GBK 인코딩에서 크래시합니다.

---

## 🧾 라이선스

[MIT](LICENSE)

---

## 🙏 마음에 드신다면, 더 많은 사람에게 알려 주세요

이 스킬이 유용하다고 느껴지신다면 명조를 하는 친구에게 공유하거나, 여러분의 skill 마켓에 등록해 주세요.

설치 명령:

```bash
npx skills add Alphamancer/kurobbs-wiki
```

---

## 🤝 기여

issue와 PR을 환영합니다. 개발 시 주의사항:

- 수정 후 `python -X utf8 -c "import py_compile; py_compile.compile('scripts/wikiquery.py', doraise=True)"`를 실행해 문법을 검증하세요
- `wikiquery.py`를 순수 표준 라이브러리로 유지하세요(`post` 하위 명령 제외), 조회 메인 흐름에 제3자 의존성을 추가하지 마세요
- SKILL.md의 「핵심 함정」과 「알려진 카드 포인트 빠른 참조」 규약을 준수하세요
