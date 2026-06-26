# hoseo-lms

호서대학교 LMS 데이터를 수집하고, 미수강 강의를 자동 재생하는 [OpenClaw](https://clawhub.ai) 스킬.

> 이 스킬은 개인 용도로 제작되었으며, 사용으로 인해 발생하는 모든 결과에 대해 제작자는 책임을 지지 않습니다.

---

### 1. ClawHub CLI 설치

```bash
npm i -g clawhub
```

### 2. 스킬 검색 및 설치

```bash
cd ~/.openclaw/workspace

clawhub install hoseo-lms
```

### 3. 인증 파일 생성

```bash
mkdir -p ~/.config/hoseo_lms

cat << 'EOF' > ~/.config/hoseo_lms/credentials.json
{
  "id": "HOSEO_STUDENT_ID",
  "pw": "HOSEO_PASSWORD"
}
EOF

chmod 600 ~/.config/hoseo_lms/credentials.json
```

---

<details>
<summary>Windows 환경에서 인증 파일 생성</summary>

PowerShell:

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.config\hoseo_lms"

@"
{
  "id": "학번",
  "pw": "비밀번호"
}
"@ | Out-File -Encoding UTF8 "$env:USERPROFILE\.config\hoseo_lms\credentials.json"
```

</details>

<details>
<summary>수집 항목 및 OpenClaw 연동</summary>

### 데이터 크롤링

`src/scraper.py`가 LMS에서 아래 데이터를 수집하면, OpenClaw 에이전트가 `data.json`을 읽어 질의에 응답합니다.

| 수집 항목 | 내용 |
|-----------|------|
| 수강 과목 | 과목명, ID, URL, 담당 교수 |
| 온라인 출석 | 주차별 강의 제목, 인정 시간, 수강 상태 |
| 과제 | 주차, 과제명, 마감일, 제출 여부 |
| 퀴즈 | 주차, 퀴즈명, 마감일 |
| 활동 분류 | VOD / 과제 / 퀴즈 / 게시판 / 기타 |

### 자동 수강

`src/auto_attend.py`는 Playwright 기반으로 미수강 강의를 자동 재생합니다.

```bash
python3 src/auto_attend.py --limit-lectures 3
python3 src/auto_attend.py --course "과목명" --limit-lectures 2
python3 src/auto_attend.py --headed --verbose --limit-lectures 1
```

</details>

<details>
<summary>데이터 스키마</summary>

`~/.config/hoseo_lms/data.json`:

```json
{
  "metadata": {
    "last_updated": 1709900000,
    "last_updated_str": "2026-03-08 14:00:00",
    "source": "https://learn.hoseo.ac.kr",
    "course_count": 5
  },
  "courses": [
    {
      "title": "...",
      "professor": "...",
      "url": "https://learn.hoseo.ac.kr/course/view.php?id=...",
      "id": "12345",
      "activities": [
        { "type": "vod", "name": "...", "url": "..." }
      ],
      "attendance": [
        { "week": "1", "title": "...", "required_time": "25:00", "status": "O" }
      ],
      "assignments": [
        { "week": "3", "title": "...", "deadline": "2026-03-15 23:59", "submitted": "..." }
      ],
      "quizzes": [
        { "week": "4", "title": "...", "deadline": "2026-03-22 23:59" }
      ]
    }
  ]
}
```

</details>

<details>
<summary>제한 사항</summary>

- LMS HTML 구조가 학기/테마 업데이트로 변경되면 파서 수정이 필요합니다.
- 과목 권한 정책에 따라 일부 데이터 접근이 제한될 수 있습니다.
- 제출 상태 텍스트는 LMS 언어 설정에 따라 달라질 수 있습니다.
- auto_attend는 Playwright Chromium이 설치된 환경에서만 동작합니다.

</details>
