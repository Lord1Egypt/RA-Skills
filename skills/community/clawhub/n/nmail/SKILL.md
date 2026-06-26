# nmail — Korean Email CLI Skill

> 한국 이메일(네이버, 다음) CLI. 에이전트가 이메일을 읽고 보내기 위한 도구.

## Prerequisites
- `nmail` binary in PATH (`go install github.com/harlock/nmail@latest`)
- 계정 설정 완료 (`nmail config add`)

## Setup
```bash
# 네이버 계정 추가 (앱 비밀번호 필요)
nmail config add --provider naver --email <email> --password <app-password>

# 다음 계정
nmail config add --provider daum --email <email> --password <app-password>

# 설정 확인
nmail config list
```

## Commands

### 받은편지함 확인
```bash
# 최근 20개 (JSON)
nmail inbox

# 개수 지정
nmail inbox --limit 5

# 사람이 읽기 편한 형태
nmail inbox --pretty
```

**JSON 출력 예시:**
```json
[
  {"id": 42, "from": "friend@naver.com", "subject": "안녕", "date": "2026-03-19T10:00:00+09:00", "is_read": false},
  {"id": 41, "from": "service@naver.com", "subject": "알림", "date": "2026-03-19T09:30:00+09:00", "is_read": true}
]
```

### 메일 읽기
```bash
# ID로 본문 읽기 (inbox에서 확인한 id)
nmail read 42

# 사람용
nmail read 42 --pretty
```

### 메일 보내기
```bash
# 직접 본문
nmail send --to friend@naver.com --subject "제목" --body "내용"

# 파일에서 본문
nmail send --to friend@naver.com --subject "제목" --body-file ./message.txt

# stdin으로 본문
echo "파이프로 보내기" | nmail send --to friend@naver.com --subject "제목" --body-file -
```

### 메일 검색
```bash
# 보낸사람으로 검색
nmail search --from "socra"

# 조합 검색
nmail search --subject "코딩" --since 2026-03-01 --limit 10

# 안 읽은 것만
nmail search --unseen

# 본문+제목 전체 검색
nmail search --text "키워드"
```

### 새 메일 감시
```bash
# 폴링 모드 (5초 간격) — JSON line 출력
nmail watch --poll 5

# 사람용
nmail watch --poll 5 --pretty
# 📬 New: [제목] from 보낸사람
```

> ⚠️ 네이버 IMAP은 IDLE 미지원. `--poll` 사용 필수.

### 계정 관리
```bash
nmail config list          # 계정 목록
nmail config add ...       # 계정 추가
nmail config remove --email <email>  # 계정 삭제
```

## Agent Usage Patterns

### 새 메일 확인 → 요약
```bash
nmail inbox --limit 5
# → JSON 파싱 → is_read: false인 것만 필터 → read로 본문 확인 → 요약
```

### 메일 검색
```bash
nmail search --from "socra" --since 2026-03-01
# → JSON 파싱 → 원하는 메일 찾기
```

### 실시간 감시 (OpenClaw 연동)
```bash
# watch 출력을 openclaw system event로 파이프
nmail watch --poll 10 | while IFS= read -r line; do
  subj=$(echo "$line" | jq -r '.subject')
  from=$(echo "$line" | jq -r '.from')
  openclaw system event --text "📬 새 메일: $subj (from: $from)" --mode now
done
```

### 메일 답장
```bash
# 1. 원본 읽기
nmail read 42
# 2. 답장 작성 (from 주소로 send)
nmail send --to <original-from> --subject "Re: <original-subject>" --body "답장 내용"
```

## Notes
- 출력은 기본 JSON. `--pretty`는 사람에게 보여줄 때만.
- 한글 제목/본문 자동 인코딩 (EUC-KR ↔ UTF-8)
- 앱 비밀번호는 `~/.nmail/config.yaml`에 저장됨 (로컬 전용)
- 에러도 JSON: `{"error": "message"}`
