---
name: hwp-batch-convert
description: Batch-convert 한컴 한글 문서(HWP/HWPX) on Windows into PDF and other export formats with a Korean-friendly automation workflow. Use when the user asks for 이 폴더 hwp 전부 pdf로 바꿔줘, hwp/hwpx/doc/pdf 일괄 변환, 한글문서 일괄 처리, 폴더 단위 변환, 여러 한글 파일을 다른 형식으로 내보내기, or wants plan-only / mock / real conversion runs with machine-readable reports. Supports HWP/HWPX to PDF, HWPX, DOCX, ODT, HTML, RTF, TXT, PNG, JPG, BMP, and GIF, plus optional automatic approval of known 한글 보안 확인 팝업. Prefer this skill for Windows environments with Hancom HWP installed; do not use it for non-HWP document families unless the task is explicitly about HWP/HWPX conversion.
---

# Hwp Batch Convert

Use this skill for **Windows 기반 한글(HWP/HWPX) 문서 일괄 변환**.

Current scope:
- 폴더 단위 일괄 변환
- 파일 여러 개 일괄 변환
- HWP/HWPX → PDF 기본 변환
- HWP/HWPX → HWPX/DOCX/ODT/HTML/RTF/TXT/PNG/JPG/BMP/GIF 변환
- 동일 형식 자동 건너뜀
- 출력 파일명 충돌 시 자동 번호 부여
- 작업 계획만 확인하는 `--plan-only`
- OpenClaw 상위 레이어 연동용 `--json`, `--report-json`
- 한글 보안 확인 팝업 자동 허용용 `--auto-allow-dialogs`
- 로컬 UI 검증용 `--self-test-dialog-handler`
- 테스트용 `--mode mock`

## Source basis

This skill reuses the design of the local/source repo:
- `tmp/HwpMate`
- upstream: `https://github.com/twbeatles/HwpMate`

Main logic origin:
- `hwpmate/services/hwp_converter.py`
- `hwpmate/services/task_planner.py`
- `hwpmate/constants.py`
- `hwpmate/path_utils.py`

If you need the mapping details or reuse rationale, read:
- `references/hwpmate-reuse-notes.md`

If you need the popup whitelist / safety details, read:
- `references/auto-allow-dialogs.md`

## Quick start

같은 폴더에 PDF 출력:

```bash
python skills/hwp-batch-convert/scripts/hwp_batch_convert.py "C:\docs\contracts" --format PDF --same-location
```

별도 출력 폴더로 변환:

```bash
python skills/hwp-batch-convert/scripts/hwp_batch_convert.py "C:\docs\hwp" --format PDF --output-dir "C:\docs\pdf" --auto-allow-dialogs
```

여러 파일 한 번에 변환:

```bash
python skills/hwp-batch-convert/scripts/hwp_batch_convert.py "C:\docs\a.hwp" "C:\docs\b.hwpx" --format DOCX --output-dir "C:\docs\docx"
```

실제 변환 없이 계획만 확인:

```bash
python skills/hwp-batch-convert/scripts/hwp_batch_convert.py "C:\docs\hwp" --format PDF --output-dir "C:\docs\pdf" --plan-only --json
```

테스트용 모의 변환:

```bash
python skills/hwp-batch-convert/scripts/hwp_batch_convert.py "C:\docs\sample" --format PDF --output-dir "C:\docs\out" --mode mock --json
```

## Main script

### `scripts/hwp_batch_convert.py`

Parameters:
- `sources...`: 입력 파일/폴더 경로 하나 이상
- `--format`: 출력 형식 (`PDF`, `HWPX`, `DOCX`, `ODT`, `HTML`, `RTF`, `TXT`, `PNG`, `JPG`, `BMP`, `GIF`, `HWP`)
- `--same-location`: 원본과 같은 폴더에 출력
- `--output-dir`: 출력 루트 폴더
- `--include-sub`: 하위 폴더 포함(기본값)
- `--no-include-sub`: 하위 폴더 제외
- `--overwrite`: 같은 이름 출력 허용
- `--plan-only`: 실제 변환 없이 작업 계획만 생성
- `--mode real|mock`: 실변환 또는 모의 변환
- `--auto-allow-dialogs`: 제목 `한글`, 본문에 `접근하려는 시도`, 버튼 `모두 허용`/`허용` 조건을 모두 만족하는 보안 팝업만 자동 클릭
- `--json`: stdout JSON 출력
- `--report-json`: 결과 JSON 파일 저장
- `--self-test-dialog-handler`: 로컬 테스트용 샘플 `한글` 창을 띄워 자동 클릭 로직만 검증

## Recommended workflow

1. 사용자 요청이 폴더/여러 파일 기반 HWP/HWPX 변환인지 확인한다.
2. 출력 형식이 명시되지 않았으면 보통 `PDF`를 기본 제안으로 사용한다.
3. 먼저 `--plan-only --json` 으로 대상/건너뜀/출력 경로를 확인한다.
4. 환경이 Windows + 한글 설치 + pywin32 가능하면 `--mode real` 로 실행한다.
5. 환경 검증이 먼저 필요하면 `--mode mock` 으로 경로/출력 구조만 검증한다.
6. 필요하면 `--report-json` 으로 결과 파일을 남긴다.

## Operational notes

- 이 스킬은 사실상 **Windows 전용**이다.
- 실변환(`--mode real`)은 **한컴 한글 설치**와 **pywin32**가 필요하다.
- `--auto-allow-dialogs` 는 화이트리스트 방식이다. 제목이 `한글` 이고, 본문에 `접근하려는 시도` 가 있으며, 버튼이 `모두 허용` 또는 `허용` 인 경우에만 클릭한다.
- 위 조건에 맞지 않는 다른 팝업은 자동으로 건드리지 않는다. 감지되더라도 클릭 없이 이벤트만 남기거나 무시한다.
- 자동 허용 기록은 stdout JSON/`--report-json` 의 `auto_dialog_*` 필드와 `auto_dialog_events` 배열에서 확인한다.
- 한글 COM 자동화가 실패하면 `--mode mock` 으로 스킬/경로 로직만 먼저 검증하고, 이후 환경 문제를 분리 진단한다.
- 여러 폴더를 동시에 입력하면서 `--output-dir` 를 쓰면, 파일명 충돌 가능성이 있으니 결과 경로를 확인한다.
- 기본 입력 확장자는 `.hwp`, `.hwpx` 만 대상으로 한다.
- 사용자 요청이 DOCX/PDF 일반 문서 처리 중심이고 HWP가 핵심이 아니면 다른 문서 스킬/도구를 우선 고려한다.
