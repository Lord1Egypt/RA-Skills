# hwp-batch-convert

Windows에서 한컴 한글(HWP/HWPX) 문서를 COM 자동화로 일괄 변환하는 OpenClaw 스킬입니다.

## 새 기능: 보안 확인 팝업 자동 허용

한글 COM 자동화 중 아래 조건을 **모두 만족하는 보안 팝업만** 자동으로 처리할 수 있습니다.

- 창 제목: `한글`
- 본문 텍스트에 `접근하려는 시도` 포함
- 버튼 텍스트: `모두 허용` 우선, 없으면 `허용`

예상치 못한 다른 팝업은 건드리지 않도록 화이트리스트 방식으로 제한했습니다.

## 사용 예시

```powershell
python skills/hwp-batch-convert/scripts/hwp_batch_convert.py "C:\docs\hwp" --format PDF --output-dir "C:\docs\pdf" --auto-allow-dialogs --json --report-json "C:\docs\pdf\report.json"
```

## 테스트

### 1) UI 자동 클릭 로컬 테스트

```powershell
python skills/hwp-batch-convert/scripts/hwp_batch_convert.py --self-test-dialog-handler
```

### 2) 모의 변환 테스트

```powershell
python skills/hwp-batch-convert/scripts/hwp_batch_convert.py "C:\docs\sample" --format PDF --output-dir "C:\docs\out" --mode mock --auto-allow-dialogs --json
```

mock 모드에서는 실제 한글 창이 없으므로 자동 허용이 동작하지 않고 경고만 남깁니다.

## 리포트 확인 포인트

JSON summary에 다음 필드가 추가됩니다.

- `auto_dialog_enabled`
- `auto_dialog_detected_count`
- `auto_dialog_clicked_count`
- `auto_dialog_events[]`
