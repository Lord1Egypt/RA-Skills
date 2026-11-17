# Mystilink 육효 Skill

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## 개요

육효 Agent Skill: 내장 Node 스크립트로 여섯 번 시괘하여 괘상을 만들고, 방법 페이지와 Wiki의 주역 장으로 해석합니다. 일사일괘. 경문을 날조하지 마세요.

## 배포 유형

**Agent Skill** 패키지. 계산기 언어 매트릭스는 **적용되지 않습니다**. 시괘 로직은 `scripts/`에만 내장(별도 육효 계산기 저장소 없음).

## 요구 사항

- Node.js 18+
- Agent Skills 호환 호스트
- 방법 페이지와 고전을 위해 Wiki 접근 권장

## 설치

폴더 이름은 `mystilink-liuyao`여야 함:

```bash
cp -R mystilink-liuyao-skill /path/to/.cursor/skills/mystilink-liuyao
```

| 호스트 | 경로 |
|------|------|
| Cursor | `.cursor/skills/mystilink-liuyao/` |
| Claude Code | `.claude/skills/mystilink-liuyao/` |

## 빠른 시작

```bash
node scripts/cast.mjs --seed 42
# or fixed throws: node scripts/cast.mjs --throws "3,2,3,3,2,3"
```

stdout JSON: 육효(아래→위), 동효 플래그, 사용 가능한 괘 키. 동전 모델은 스크립트 도움말(앞=3, 뒤=2 합).

## 워크플로

1. 한 가지 일을 명확히(`examples/cast-request.json`); 다주제 남발 시괘 거부
2. 스크립트로 시괘하거나 사용자 투척 수용
3. Wiki로 읽기, 예:

```text
GET https://wiki.mystilink.com/api/v1/pages/liuyao.method.six-casts?locale=en
GET https://wiki.mystilink.com/api/v1/pages/liuyao.rule.ben-zhi-bian?locale=en
GET https://wiki.mystilink.com/api/v1/pages/shared.work.yijing.gua.01-qian?locale=zh-Hans
```

4. 주역 원문은 Wiki references / cites 우선

상세: `SKILL.md`. 안내: `references/overview.md`.

## 예제

- `examples/cast-request.json` — 시괘 요청 샘플

## 제한

- 고전은 다른 locale에 본문이 없으면 흔히 `zh-Hans`로 폴백
- 내장 시괘 도우미는 제품 동전→효 의미의 단순 구현
- Wiki locale 생략 → `en`

## 라이선스

MIT. [LICENSE](../../LICENSE) 참고.

## 피드백

seed/throws와 stdout JSON(가상 사항만)을 포함하세요.
