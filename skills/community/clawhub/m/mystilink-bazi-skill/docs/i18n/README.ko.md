# Mystilink 팔자 Skill

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## 개요

팔자(사주) Agent Skill: 내장 스크립트로 출생 자료에서 사주·대운·유년을 계산한 뒤, 이론 페이지(일주, 십신 등)로 해석합니다. 차트 계산은 `scripts/`에 있습니다.

## 배포 유형

이 저장소는 **Agent Skill** 패키지(`SKILL.md` + `scripts/` + `references/` + `examples/`)입니다. 계산기 라이브러리의 C / C++ / C# / Java / JavaScript / Python 언어 매트릭스는 **적용되지 않습니다**. 다언어 SDK/CLI는 동계열 `mystilink-bazi-calculator`(선택; 이 skill 실행에 필수 아님).

## 요구 사항

- Python 3.9+ (`zoneinfo`)
- Agent Skills 호환 호스트
- 해석 시 Mystilink Wiki API는 선택(네트워크)

## 설치

폴더 이름은 `mystilink-bazi`(`SKILL.md`의 `name`과 일치):

| 호스트 | 경로 |
|------|------|
| Cursor | `.cursor/skills/mystilink-bazi/` |
| Claude Code | `.claude/skills/mystilink-bazi/` |

```bash
cp -R mystilink-bazi-skill /path/to/.cursor/skills/mystilink-bazi
```

## 빠른 시작(스크립트)

skill 디렉터리에서:

```bash
python3 scripts/bazi_calculate.py --date 1990-05-15 --hour 12
python3 scripts/bazi_calculate.py --birth-json examples/profile.v0.json
python3 scripts/bazi_calculate.py --profile-json examples/profile.json
python3 scripts/bazi_dayun_calculate.py --date 1990-05-15 --gender female --count 8
python3 scripts/bazi_liunian_calculate.py --year 2026 --day-stem 甲
```

성공: stdout에 JSON. 실패: 비영 종료와 JSON `{"error":…}`.

기둥 객체는 `stem_index`, `branch_index`, `text`, 그리고 구필드 `ganzhi`(`=` `text`)를 포함합니다.

## 워크플로

1. 출생 프로필 수집 — 다음 중 하나:
   - `examples/profile.v0.json` (`mystilink.birth/0.1` BirthProfile), 또는
   - `examples/profile.json` (구 skill 필드)
2. 필요 시 차트 스크립트 실행(`--birth-json` / `--profile-json` 두 형태 모두 수용)
3. 선택적 Wiki 해석:

```text
GET https://wiki.mystilink.com/api/v1/search?q=day+master&system=bazi&locale=en
GET https://wiki.mystilink.com/api/v1/pages/bazi.concept.ri-zhu?locale=en
```

4. **차트 사실**과 **해석**을 구분; Wiki 사용 시 출처 명시

전체 안내: `SKILL.md`. 짧은 id: `references/wiki-ids.md`.

## 예제

- `examples/profile.v0.json` — BirthProfile (`mystilink.birth/0.1`, 가상)
- `examples/profile.json` — 구 출생 프로필(가상); 스크립트는 계속 수용

## 제한

- 스크립트는 단독 skill 설치용 내장 복사본이며 다언어 SDK가 아님
- 대운 절기일은 양력 근사
- 진태양시는 타임존과 경도 모두 필요
- Wiki locale: 생략 → `en`; 번역 없으면 `zh-Hans`로 폴백할 수 있음

## 라이선스

MIT. [LICENSE](../../LICENSE) 참고.

## 피드백

정확한 스크립트 명령(가상 날짜만)과 stdout/stderr JSON을 함께 보고하세요.
