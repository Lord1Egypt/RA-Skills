# Mystilink 점성 Skill

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## 개요

서양 네이탈 점성 Agent Skill: 내장 스크립트로 출생 시각과 장소에서 행성·하우스·애스펙트를 계산한 뒤 이론 페이지로 해석합니다.

## 배포 유형

**Agent Skill** 패키지. 계산기 언어 매트릭스는 **적용되지 않습니다**. 선택적 동계열: `mystilink-horoscope-calculator`.

## 요구 사항

- Python 3.9+
- `pip install pyswisseph`
- Agent Skills 호환 호스트
- Wiki API는 선택(네트워크)

## 설치

폴더 이름은 `mystilink-horoscope`여야 함:

```bash
cp -R mystilink-horoscope-skill /path/to/.cursor/skills/mystilink-horoscope
```

| 호스트 | 경로 |
|------|------|
| Cursor | `.cursor/skills/mystilink-horoscope/` |
| Claude Code | `.claude/skills/mystilink-horoscope/` |

## 빠른 시작

```bash
python3 scripts/astro_chart_calculate.py \
  --datetime "1990-05-15 14:30" \
  --timezone Asia/Shanghai \
  --lat 31.23 --lon 121.47 \
  --output json

python3 scripts/astro_chart_calculate.py \
  --birth-json examples/profile.v0.json \
  --output json
```

선택: `--zodiac tropical|sidereal`, `--true-solar-time`.

성공: stdout JSON. 실패: 비영 종료 + JSON error.

## 워크플로

1. 출생 자료 수집 — `examples/profile.v0.json`(BirthProfile) 또는 구 `examples/profile.json`
2. 네이탈 스크립트 실행
3. 선택적 Wiki:

```text
GET https://wiki.mystilink.com/api/v1/search?q=ascendant&system=horoscope&locale=en
GET https://wiki.mystilink.com/api/v1/pages/horoscope.concept.natal-chart?locale=en
```

4. 차트 데이터와 해석을 구분

상세: `SKILL.md`. 안내: `references/overview.md`.

## 예제

- `examples/profile.v0.json` — BirthProfile (`mystilink.birth/0.1`, 가상)
- `examples/profile.json` — 구 가상 네이탈 입력

## 제한

- `pyswisseph`(Swiss Ephemeris) 필요
- skill 설치용 내장 스크립트이며 다언어 SDK가 아님
- Wiki locale 생략 → `en`; 폴백은 `zh-Hans`일 수 있음

## 라이선스

MIT. [LICENSE](../../LICENSE) 참고.

## 피드백

정확한 명령(가상 좌표/datetime)과 JSON 출력/오류를 포함하세요.
