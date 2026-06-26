# 한글 보안 팝업 자동 허용 메모

## 목적

한글(HWP) COM 자동화 중 뜨는 보안 확인 팝업 때문에 `Open`/`SaveAs` 흐름이 멈추는 경우를 줄이기 위해, 매우 제한된 조건의 팝업만 자동 클릭한다.

## 화이트리스트 조건

다음 조건을 모두 만족할 때만 클릭한다.

1. 최상위 창 제목이 정확히 `한글`
2. 자식 컨트롤 텍스트를 합친 본문에 `접근하려는 시도` 포함
3. 버튼 텍스트가 `모두 허용` 우선, 없으면 `허용`

## 안전장치

- 제목만 `한글` 인 다른 창은 본문/버튼 조건까지 함께 확인하기 전에는 클릭하지 않는다.
- 버튼 텍스트가 없거나 다른 경우 클릭하지 않는다.
- 화이트리스트와 맞지 않는 창은 `text-mismatch`, `button-mismatch` 등 이유를 이벤트에 남길 수 있다.
- 탐지된 창 핸들은 중복 처리하지 않는다.
- 외부 UI 자동화 패키지 없이 Win32 API(`EnumWindows`, `EnumChildWindows`, `SendMessageW(BM_CLICK)`)만 사용한다.

## 테스트 방법

### UI 클릭 자체 테스트

```powershell
python skills/hwp-batch-convert/scripts/hwp_batch_convert.py --self-test-dialog-handler
```

테스트는 PowerShell WinForms로 아래와 유사한 샘플 창을 띄우고, 자동 클릭 로직이 `모두 허용` 버튼을 실제로 누르는지 확인한다.

- 제목: `한글`
- 본문: `한글 문서에 접근하려는 시도를 허용하시겠습니까?`
- 버튼: `모두 허용`

### 변환 경로 테스트

```powershell
python skills/hwp-batch-convert/scripts/hwp_batch_convert.py <입력> --format PDF --output-dir <출력> --mode mock --auto-allow-dialogs --json
```

mock 모드에서는 실제 한글 창이 없으므로 `auto_dialog_detected_count = 0` 이 정상이다.
