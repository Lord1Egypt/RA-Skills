# Mystilink 타로 Skill

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## 개요

타로 Agent Skill: 내장 Node 스크립트로 스프레드에 정위치/역위치 카드를 뽑고, 카드 이론 페이지로 해석합니다. 실제 뽑기(스크립트 또는 사용자 제공)를 우선하며, 뽑기 결과를 조용히 날조하지 마세요.

## 배포 유형

**Agent Skill** 패키지. 계산기 언어 매트릭스는 **적용되지 않습니다**. 뽑기/검증 로직은 `scripts/`에만 내장(별도 타로 계산기 저장소 없음).

## 요구 사항

- Node.js 18+
- Agent Skills 호환 호스트
- Wiki API는 선택(네트워크)

## 설치

폴더 이름은 `mystilink-tarot`여야 함:

```bash
cp -R mystilink-tarot-skill /path/to/.cursor/skills/mystilink-tarot
```

| 호스트 | 경로 |
|------|------|
| Cursor | `.cursor/skills/mystilink-tarot/` |
| Claude Code | `.claude/skills/mystilink-tarot/` |

## 빠른 시작

```bash
node scripts/draw.mjs --spread three-card --seed 42
# or: echo '{"spread":"three-card","seed":42}' | node scripts/draw.mjs
```

stdout JSON: `id`, `name`, `orientation`(`upright`|`reversed`), 위치가 있는 카드. 카드 `id`는 Wiki `tarot.card.*`와 일치.

## 워크플로

1. 질문과 스프레드 명확화(기본: three-card); `examples/draw-request.json` 참고
2. 스크립트로 뽑거나 사용자 제공 카드 수용
3. 각 카드에 대해 선택적 Wiki:

```text
GET https://wiki.mystilink.com/api/v1/search?q=The+Fool&system=tarot&locale=en
GET https://wiki.mystilink.com/api/v1/pages/<card.id>?locale=en
```

4. 각 위치를 질문에 연결; Wiki 사용 시 출처 명시

상세: `SKILL.md`. 뽑기 방법: `references/method-draw.md`.

## 예제

- `examples/draw-request.json` — 뽑기 요청 샘플

## 제한

- 의료·법적 확정을 주장하지 않음
- 뽑기당 명확한 질문 하나 우선
- Wiki locale 생략 → `en`

## 라이선스

MIT. [LICENSE](../../LICENSE) 참고.

## 피드백

스프레드 flags/seed(또는 stdin JSON)와 stdout JSON(가상 질문만)을 포함하세요.
