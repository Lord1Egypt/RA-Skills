<p align="center">
  <img src="assets/logo.png" alt="New Youth La Jeunesse" width="400"/>
</p>

<h1 align="center">신 청년.skill</h1>

<p align="center">

> *"사회에 있어서 청년은 마치 인간의 몸에서 신선하고 활력 있는 세포와 같다. 신진대사 — 낡고 썩은 요소들은 끊임없이 자연적으로 도태되며, 신선하고 활력 있는 자에게 공간적 위치와 시간적 생명을 제공한다."*
> — 천둥시우, 『청년에게 고함』(1915)

</p>

<p align="center">🌟 *"청년은 초봄과 같고, 아침 해와 같으며, 만물이 움트는 것과 같고, 숫돌에 닦인 칼날과 같다. 인생에서 가장 보배로운 시기이다."*</p>

<p align="center">
<a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"/></a>
<a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.9%2B-blue.svg" alt="Python 3.9+"/></a>
<a href="https://claude.com/claude-code"><img src="https://img.shields.io/badge/Claude%20Code-Skill-purple.svg" alt="Claude Code"/></a>
<a href="https://github.com/anthropics/agent-skill-standard"><img src="https://img.shields.io/badge/AgentSkills-Standard-green.svg" alt="AgentSkills"/></a>
</p>

<p align="center"><i>청춘의 나를 가지라, 청춘의 가정을 창조하라, 청춘의 국가를 건설하라.</i></p>

---

<div align="center">

[왜 이것이 존재하는가?](#왜-이것이-존재하는가) · [여섯 가지 기준](#여섯-가지-기준) · [핵심 기능](#핵심-기능) · [설치](#설치) · [사용 방법](#사용-방법) · [데모](#데모) · [신 청년 지수](#신-청년-지수) · [프로젝트 구조](#프로젝트-구조)

</div>

---

<p align="center">1915년 천둥시우가 상하이에 창간한 『La Jeunesse』(신 청년)지에 기반 —— 중국 신문화운동의 기수이며, 한 세대에 민주와 과학을 전파했다.</p>

<p align="center">
<a href="README.md">English</a> · <a href="README_ZH.md">中文</a> · <a href="README_RU.md">Русский</a> · <a href="README_JA.md">日本語</a> · <a href="README_KO.md">한국어</a> · <a href="README_FR.md">Français</a> · <a href="README_DE.md">Deutsch</a> · <a href="README_ES.md">Español</a>
</p>

---

## 왜 이것이 존재하는가?

**시대의 폐단：**
- 🤖 알고리즘이 네 욕구를 충족시켜준다 → 정보 방울
- 🎭 AI는 자신감 있게 말한다 → 그러나 허상에 가득
- 😔 사람들은 사고를 기계에 맡긴다 → 정신적으로 움츠린 존재

**우리의 답：**
사상을 주입하는 확성기가 아니라, 독립적 사고의 안내자이다. 네가 이 시대에 부끄럽지 않은 사람이 되도록 돕는다.

---

## 여섯 가지 기준

| # | 기준 | 요점 | 버려야 할 것 |
|:---|:---|:---|:---|
| 1 | **자율적** | 스스로 생각하고,他人的 코에 의존하지 않는다 | 무조건적인 복종 |
| 2 | **진보적** | 옛 것을 버리고 새 것을 받아들인다 | 보수적이고 경직된 |
| 3 | **진취적** |率先하여 事를 갈고 닦는다 | 물러나고 도망치는 |
| 4 | **세계적** |全局를 보고天下를 가슴에 안는다 | 감상에埋头 |
| 5 | **실리적** | 실천이 말보다 낫다, 실건으로 나라를 일으킨다 | 허황된 말 |
| 6 | **과학적** | 사실에 근거하여事物를探究한다 | 주관이臆断 |

---

## 핵심 기능

| 기능 | 영혼의 물음 | 수행 |
|:---|:---|:---|
| **인격 평가** | "나는 이 시대에 부끄럽지 않은가?" | 六차원 투시 |
| **결의 지도** | "어디로 가야 하나?" | 六단계 사고 |
| **관점审视** | "이 주장이 사실인가?" | 논리 감사 |
| **일상 실천** | "오늘 무엇을 해야 하나?" | 知行合一 |
| **시각 확장** | "다른 시각은?" | 나를 깨뜨린다 |
| **행동 실행** | "어떻게 실천할까?" | 空想到実践으로 |

---

## 설치

### 시스템 요구사항

- **Python**: 3.9+ (선택적 헬퍼 스크립트용)
- **플랫폼**: Windows / macOS / Linux
- **호환**: Claude Code, OpenClaw, Cursor, Coze 및 기타 Agent Skills 플랫폼

> 참고: 이 스킬은 텍스트/대화형, 외부 API 불필요.

### Claude Code

```bash
mkdir -p .claude/skills
git clone https://github.com/Moroiser/new-youth-skill.git .claude/skills/new-youth-skill
```

### OpenClaw

```bash
git clone https://github.com/Moroiser/new-youth-skill ~/.openclaw/workspace/skills/new-youth-skill
```

---

## 사용 방법

### 명령

```
/新青年
```

### 발동 조건

다음 상황에서 자동 발동：
- "나는 이 시대에 부끄럽지 않은가?"
- "선택에 부딪혔을 때, 어떻게 해야 하나?"
- "어떻게才能不负此生하지?"
- "이 주장이 사실인가? 이 말이 믿을 만한가?"
- "나는 더有为한 사람이 되고 싶다"

---

## 데모

**인격 평가：**

```
사용자    ❯ 나는 이 시대에 부끄럽지 않은가? 안정과 창업 사이에서迷っている.

신 청년  ❯ 친구よ, 이 문제를 提出할 수 있다는 것 자체가覚醒의 시작이다.
             六条標準을 거울로 삼아 진정한 나를 보자.
             六차원으로 자기 평가를 진행주세요 (1-5점)：
             ① 자율——남의 말을 자신의 것으로 삼는 일이 잦은가?
             ② 진보——변화를 받아들이는가, 옛 것을 지키는가?
             ③ 진취——기다리는가,率先하는가?
             …
```

**결의 지도：**

```
사용자    ❯ 시대의 홍류에直面하여, 어디로 가야 하나?

신 청년  ❯ 친구よ, 시대의 홍류 속에서 개인은 如何에 있을べきか?
             六단계方法来霧를散去하자：
             第一단계——자율：네 마음이 정말로 원하는 것은?
             봉급도, 지위도 아니다——네가 되고 싶은 것은 무엇인가?
```

---

## 신 청년 지수

**六차원 자기 평가** (각 1-5점)：

| 차원 | 1점 | 3점 | 5점 |
|:---|:---|:---|:---|
| 자율 | 人云亦云 | 偶有主見 | 独立判断 |
| 진보 | 抱残守缺 | 被动应变 | 主动求新 |
| 진취 | 消极待機 | 适度作为 | 永远向前 |
| 세계 | 坐井观天 | 偶尔破圈 | 纵览全局 |
| 실리 | 空谈误事 | 偶有成果 | 行穏致远 |
| 과학 | 主观臆断 | 偶尔実証 | 格物致知 |

**등급：**

| 총점 | 등급 |
|:---|:---|
| 27-30 | 🌱 신 청년 모범 |
| 24-26 | 🌿 신 청년에 접근 |
| 18-23 | 🌾 尚需精進 |
| 6-17 | 🌰 亟需覚醒 |

---

## 프로젝트 구조

| 폴더 | 용도 | 사용 방법 |
|:---|:---|:---|
| **SKILL.md** | 핵심 명령집 | AI 가 자동 로드 |
| **research/** | 원시 연구 자료（원문, 역사 문헌） | 인간이 심화 학습용 |
| **references/** | 구조화된 참고 자료 | AI 가 필요시 참조 |
| **commands/** | 수동 명령 진입점 | 사용자가 호출 |
| **scripts/** | 헬퍼 스크립트（선택） | 도구 |
| **assets/** | 이미지 리소스 | 자동 |

**research/ vs references/**：
- `research/` 는 "원석" —— 원시 문헌, PDF, 역사 자료（입력）
- `references/` 는 "황금" —— 정제된 구조화된 콘텐츠（AI 가 실행시 참조）

```
new-youth-skill/
├── SKILL.md                      # 핵심 명령집
├── research/                    # 원시 자료（인간深造用）
├── references/                   # 구조화된 참고자료（AI 가 참조）
├── commands/                    # 명령 진입점
├── scripts/                     # 헬퍼 스크립트
├── assets/                      # 이미지
└── README.md (8개 언어)
```

---

## 기원

1915년, 천둥시우는 상하이에 『신 청년(New Youth)』을 창간하여 민주와 과학의 양기치를 들어올리며 신문화운동의 기수가 되었다.

이 스킬은 그 정신을 AI 시대의 사상 무기로 응축：설교하지 않고, 각성시킨다.
