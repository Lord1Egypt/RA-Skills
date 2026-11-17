# Mystilink 자미 Skill

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## 개요

자미두수 Agent Skill: 내장 Python 스크립트로 십이궁 차트(선택적 사화)를 만든 뒤 이론 페이지로 해석합니다. 차트 계산은 `scripts/`에 있습니다.

## 배포 유형

**Agent Skill** 패키지. 계산기 언어 매트릭스(C / C++ / C# / Java / JS / Python SDK)는 **적용되지 않습니다**. 선택적 동계열: `mystilink-ziwei-calculator`.

## 요구 사항

- Python 3.9+
- `pip install zhdate`
- Agent Skills 호환 호스트
- Wiki API는 선택(네트워크)

## 설치

폴더 이름은 `mystilink-ziwei`여야 함:

```bash
cp -R mystilink-ziwei-skill /path/to/.cursor/skills/mystilink-ziwei
```

| 호스트 | 경로 |
|------|------|
| Cursor | `.cursor/skills/mystilink-ziwei/` |
| Claude Code | `.claude/skills/mystilink-ziwei/` |

## 빠른 시작

```bash
python3 scripts/ziwei_chart_calculate.py \
  --datetime "1990-05-15 14:30" \
  --timezone Asia/Shanghai \
  --gender female \
  --output json

python3 scripts/ziwei_chart_calculate.py \
  --birth-json examples/profile.v0.json \
  --output json
```

선택 플래그: `--si-hua`, `--year YYYY`, `--longitude E`, `--midnight-zi`.

성공: stdout JSON. 실패: 비영 종료 + JSON error.

## 워크플로

1. 출생 자료 수집 — `examples/profile.v0.json`(BirthProfile) 또는 구 `examples/profile.json`
2. 차트 스크립트 실행
3. 선택적 Wiki:

```text
GET https://wiki.mystilink.com/api/v1/search?q=life+palace&system=ziwei&locale=en
GET https://wiki.mystilink.com/api/v1/pages/ziwei.concept.ming-gong?locale=en
```

4. 차트 사실과 해석을 구분

상세: `SKILL.md`. 안내: `references/overview.md`.

## 예제

- `examples/profile.v0.json` — BirthProfile (`mystilink.birth/0.1`, 가상)
- `examples/profile.json` — 구 가상 출생 입력

## 제한

- 음력 변환은 `zhdate`에 의존
- 단독 skill용 내장 스크립트이며 다언어 SDK가 아님
- Wiki locale 생략 → `en`; 폴백은 `zh-Hans`일 수 있음

## 라이선스

MIT. [LICENSE](../../LICENSE) 참고.

## 피드백

정확한 명령(가상 datetime)과 JSON 출력/오류를 포함하세요.
