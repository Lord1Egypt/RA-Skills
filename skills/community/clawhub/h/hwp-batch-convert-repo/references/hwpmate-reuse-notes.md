# HwpMate 재사용 메모

이 스킬의 최소 CLI는 `twbeatles/HwpMate`의 다음 구조를 직접 참고해 경량 재구성했다.

- `hwpmate/services/hwp_converter.py`
  - pywin32 + HWP COM 초기화
  - `Open` + `SaveAs` + `Clear` 기반 변환 흐름
  - 여러 ProgID 폴백 시도
- `hwpmate/services/task_planner.py`
  - 폴더/파일 입력을 변환 작업 목록으로 펼치기
  - 동일 형식 자동 건너뜀
  - 출력 경로 충돌 시 ` (1)`, ` (2)` 번호 부여
- `hwpmate/constants.py`
  - 지원 입력 확장자, 출력 포맷 매핑, ProgID 목록
- `hwpmate/path_utils.py`
  - 지원 파일 순회 로직
- `hwpmate/models.py`
  - 작업/요약 데이터 구조

스킬 쪽 구현은 OpenClaw에서 바로 쓰기 쉽게 GUI 의존성(PyQt6)을 제거하고 CLI 중심으로 축소했다.

## 차이점

- GUI, 백업, 트레이, 토스트, CSV/TXT 실패 리포트는 제외
- OpenClaw에서 쓰기 좋은 `--plan-only`, `--json`, `--report-json`, `--mode mock` 추가
- `sources` 인자에 파일/폴더 여러 개를 동시에 받을 수 있게 단순화
- 기본 목적은 `한글 문서 일괄 처리` 요청에서 빠르게 실행 가능한 최소 기능 제공
