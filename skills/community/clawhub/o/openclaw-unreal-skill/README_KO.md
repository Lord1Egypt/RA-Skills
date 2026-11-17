# 🦞 OpenClaw Unreal Skill

Unreal Engine 통합을 위한 OpenClaw 스킬. [OpenClaw Unreal Plugin](https://github.com/openclaw/openclaw-unreal-plugin)과 함께 작동합니다.

## 설치

```bash
# OpenClaw workspace에 복제 또는 복사
cp -r openclaw-unreal-skill ~/.openclaw/workspace/skills/unreal-plugin
```

## 구조

```
openclaw-unreal-skill/
├── extension/
│   ├── index.ts       # 도구 정의, 핸들러, 안전 게이트
│   ├── dist/index.js  # 컴파일된 번들
│   ├── openclaw.plugin.json
│   └── package.json   # Extension 메타데이터
├── tests/
│   └── gate.test.mjs  # 안전 게이트 테스트 (Unreal 불필요)
├── SKILL.md           # 스킬 문서 (영문)
├── SKILL_KO.md        # 스킬 문서 (한국어)
├── README.md          # 영문 README
├── README_KO.md       # 한국어 README (이 파일)
└── LICENSE.md         # Apache-2.0
```

## 안전

조회 전용 도구(`level.getCurrent`, `actor.find`, `transform.get*`,
`debug.hierarchy`, `debug.screenshot`, `console.getLogs` 등)는 이전과 동일하게
동작합니다. 프로젝트를 바꾸는 도구는 기본이 거부이며, 두 가지 옵트인이 모두
필요합니다:

```bash
# 1. 운영자가 게이트웨이 프로세스에서 프로젝트 변경을 허용
OPENCLAW_EDITOR_ALLOW_DESTRUCTIVE=1 openclaw gateway restart
```

```
# 2. 사용자에게 확인한 뒤, 호출마다 그 변경을 승인
unreal_execute: actor.delete {name: "Cube_01"}, confirm: true
```

`dryRun: true` 로 전송 없이 미리 볼 수 있고, `openclaw unreal status` 로 현재
허용 여부를 확인할 수 있습니다. 자세한 내용은
[SKILL_KO.md 의 안전 및 권한](SKILL_KO.md#안전-및-권한) 참고.

## 개발

```bash
# 안전 게이트 테스트 실행 (Node 22.18+ / 24, Unreal Editor 불필요)
node --test --test-force-exit tests/*.test.mjs

# extension/index.ts 수정 후 번들 재빌드
npx --yes esbuild@0.21.5 extension/index.ts --bundle --format=esm \
  --platform=node --target=esnext --external:openclaw \
  --outfile=extension/dist/index.js
```

## 사용법

설치 후 스킬은 OpenClaw에 의해 자동으로 로드됩니다. 자연어로 Unreal Editor와 상호작용:

- "레벨 계층 구조를 보여줘"
- "위치 100, 200, 50에 큐브 만들어"
- "플레이 모드 시작해"
- "스크린샷 찍어"
- "플레이어 스타트를 원점으로 옮겨"

## 요구 사항

1. OpenClaw Gateway 실행 중
2. OpenClaw Plugin이 설치된 Unreal Engine 프로젝트
3. Gateway에 연결된 플러그인

## 도구

전체 도구 문서는 [SKILL_KO.md](SKILL_KO.md) 참조.

## 라이선스

MIT 라이선스
