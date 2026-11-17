# Mystilink Router Skill

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## 개요

사용자가 체계를 지정하지 않았거나, 어떤 방법이 맞는지 묻거나, 여러 전통을 한꺼번에 섞어 요청할 때 Mystilink 명리/점술 skill(팔자, 자미, 타로, 육효, 서양 점성) 중 하나를 고르는 Agent Skill입니다. 차트 계산이나 뽑기는 수행하지 않습니다.

## 배포 유형

이 저장소는 **Agent Skill** 패키지(`SKILL.md` + references + examples)입니다. 계산기 라이브러리에서 쓰는 C / C++ / C# / Java / JavaScript / Python 언어 매트릭스는 **적용되지 않습니다**.

## 요구 사항

- Agent Skills 호환 호스트(Cursor, Claude Code, OpenClaw, Hermes 등)
- 라우팅 후 이어가려면 대상 이론 skill이 설치되어 있어야 함

## 설치

이 저장소를 호스트 skills 디렉터리에 `mystilink-router`로 복제합니다(폴더 이름은 `SKILL.md`의 `name`과 일치해야 함):

| 호스트 | 경로 |
|------|------|
| Cursor | `.cursor/skills/mystilink-router/` 또는 `~/.cursor/skills/mystilink-router/` |
| Claude Code | `.claude/skills/mystilink-router/` 또는 `~/.claude/skills/mystilink-router/` |

```bash
cp -R mystilink-router-skill /path/to/.cursor/skills/mystilink-router
```

## 사용법

`SKILL.md`를 따릅니다. 라우팅 휴리스틱:

| 필요 | Skill |
|------|--------|
| 생년월일시 → 장기 구조, 십신 | `mystilink-bazi` |
| 생 → 십이궁 / 자미 성요 | `mystilink-ziwei` |
| 출생지 + 시각 → 행성/하우스/애스펙트 | `mystilink-horoscope` |
| 구체적 한 질문, 상징 카드 | `mystilink-tarot` |
| 구체적 한 질문, 괘 / 동효 | `mystilink-liuyao` |

선택적 Wiki 보조(네트워크):

```text
GET https://wiki.mystilink.com/api/v1/pages/shared.concept.choosing-a-system?locale=en
```

선택 후 해당 skill의 `SKILL.md`를 불러 계속합니다. 요청당 주 체계 하나를 우선합니다.

## 예제

샘플 의도와 기대 대상은 `examples/routing-cases.md`를 참고하세요.

## 제한

- 이 skill에는 계산 스크립트가 없음
- 여러 체계를 “혹시 몰라” 동시에 실행하지 않음
- Wiki 호출은 선택; `locale`/`lang` 생략 → `en`; 번역 없으면 `zh-Hans`로 폴백할 수 있음

## 라이선스

MIT. [LICENSE](../../LICENSE) 참고.

## 피드백

사용자 의도 문구(가상만)와 선택되었거나 놓친 skill 이름을 함께 보고하세요.
