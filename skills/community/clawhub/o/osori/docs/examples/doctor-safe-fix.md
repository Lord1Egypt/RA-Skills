# Doctor: Safe Fix Guide

`/doctor`는 레지스트리 건강검진 + 안전한 자동 수정 도구입니다.

## 기본 동작 (Preview-First)

```bash
/doctor
```

**변경을 적용하지 않고** 분석 결과와 수정 계획만 보여줍니다:

```
🩺 Osori Doctor
Registry: ~/.openclaw/osori.json
Counts: ERROR=0 WARN=2 INFO=0

[WARN] registry.legacy_array: Legacy array registry detected.
  ↳ fix: Run with --fix to migrate to versioned schema.
[WARN] project.duplicate_name: duplicate project name 'my-app' at indices [0, 3]
  ↳ fix: Keep one canonical entry and remove duplicates.

📋 Fix Plan:
  1. 🟢 [LOW] Migrate legacy array format → versioned schema v2
     → 5 project(s)
  2. 🟡 [MEDIUM] Remove 1 duplicate(s) of 'my-app'
     → indices: [0, 3]

Risk summary: 🟢 low=1  🟡 medium=1  🔴 high=0

ℹ️  Preview only — no changes applied.
   Run with --fix to apply, or --dry-run to confirm preview.
```

## Risk 등급

| 등급 | 아이콘 | 설명 | 예시 |
|---|---|---|---|
| **low** | 🟢 | 스키마/버전 정규화 | 마이그레이션, 필드 추가 |
| **medium** | 🟡 | 데이터 변경 (복구 가능) | 중복 제거, root 참조 수정 |
| **high** | 🔴 | 파괴적 변경 | 깨진 레지스트리 초기화 |

## 수정 적용

```bash
/doctor --fix
```

- low/medium 수정을 적용합니다
- **high risk는 차단**됩니다 (별도 승인 필요)
- 적용 전 자동으로 `.bak-<timestamp>` 백업 생성

## High Risk 승인

```bash
/doctor --fix --yes
```

`--yes`를 추가하면 high risk 작업도 자동 승인합니다.

## Dry-Run (절대 미적용)

```bash
/doctor --dry-run
```

`--fix`와 함께 사용해도 **절대로 변경을 적용하지 않습니다**. CI/스크립트에서 안전하게 점검할 때 사용합니다.

## JSON 출력

```bash
/doctor --json
/doctor --dry-run --json
```

```json
{
  "status": "issues",
  "counts": { "error": 0, "warn": 2, "info": 0 },
  "plan": [
    { "risk": "low", "action": "migrate_legacy", "description": "..." },
    { "risk": "medium", "action": "dedupe_name", "description": "..." }
  ],
  "riskSummary": { "low": 1, "medium": 1, "high": 0 },
  "fix": { "requested": false, "dryRun": true, "applied": false }
}
```

## 안전 보장

1. **Preview-first** — 기본 실행은 항상 읽기 전용
2. **Backup** — 모든 변경 전 `.bak-<timestamp>` 자동 생성
3. **Corrupted 보존** — 깨진 파일은 `.broken-<timestamp>`로 보존
4. **Risk gate** — high risk는 명시적 승인 없이 실행 불가
5. **Dry-run** — `--dry-run` 플래그는 다른 모든 플래그를 override
