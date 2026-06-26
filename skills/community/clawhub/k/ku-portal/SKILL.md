---
name: ku-portal
description: 고려대학교 KUPID 포털 조회. 공지사항, 학사일정, 장학공지, 도서관 좌석, 시간표, 수강과목, LMS 연동. (SonAIengine/ku-portal-mcp 기반)
metadata:
  openclaw:
    min: "2026.2.0"
    requires:
      bins: ["python3"]
      config:
        - "~/.config/ku-portal/credentials.json"
        - "~/.cache/ku-portal-mcp/session.json"
        - "~/.cache/ku-portal-mcp/lms_session.json"
        - "~/.cache/ku-portal-mcp/server.log"
        - "~/Downloads/ku_timetable.ics"
---

# KU Portal - 고려대학교 KUPID 포털 스킬

고려대학교 KUPID 포털, 도서관, LMS 정보를 조회하는 OpenClaw 스킬.

## 로컬 파일 접근

이 스킬은 로그인/캐시/내보내기 기능 때문에 아래 경로를 사용합니다.

- 읽기: `~/.config/ku-portal/credentials.json` — KUPID 자격 증명
- 쓰기/읽기: `~/.cache/ku-portal-mcp/session.json` — 포털 세션 캐시
- 쓰기/읽기: `~/.cache/ku-portal-mcp/lms_session.json` — LMS 세션 캐시
- 쓰기: `~/.cache/ku-portal-mcp/server.log` — MCP 서버 로그
- 쓰기: `~/Downloads/ku_timetable.ics` — 시간표 ICS 내보내기 (`timetable --ics` 사용 시)

자격 증명 파일은 스킬 디렉터리 밖(`~/.config`)에 두며, git/ClawHub 배포 대상에 포함되지 않습니다.

## 사용법

모든 명령은 스킬 디렉터리 기준으로 실행하거나, OpenClaw가 제공하는 `{baseDir}`를 사용하세요.

```bash
source {baseDir}/.venv/bin/activate
python3 {baseDir}/ku_query.py <command> [options]
```

또는:

```bash
cd <skill-dir>
source .venv/bin/activate
python3 ku_query.py <command> [options]
```

## 명령어

### 로그인 불필요
- `library` — 전체 도서관 좌석 현황
- `library --name 중앙도서관` — 특정 도서관 좌석
- `menu` — 오늘 전체 학식 메뉴 (koreapas.com 기반)
- `menu --restaurant 교직원식당` — 특정 식당만 필터
- `menu --date 2026-03-10` — 특정 날짜 메뉴

### 로그인 필요 (KUPID SSO)
자격 증명: `~/.config/ku-portal/credentials.json`
```json
{"id": "your-kupid-id", "pw": "your-kupid-password"}
```

- `notices [--limit 10]` — 공지사항 목록
- `notices --detail <message_id>` — 공지사항 상세
- `schedules [--limit 10]` — 학사일정
- `scholarships [--limit 10]` — 장학공지
- `search <keyword>` — 공지/일정/장학 통합 검색
- `timetable [--day 월]` — 시간표 (요일 지정 가능)
- `timetable --ics` — ICS 파일 생성
- `courses --college 정보대학 --dept 컴퓨터학과` — 개설과목 검색
- `syllabus <course_id>` — 강의계획서
- `mycourses` — 내 수강신청 내역

### LMS (Canvas)
- `lms courses` — LMS 수강과목
- `lms assignments <course_id>` — 과제 목록
- `lms modules <course_id>` — 강의자료
- `lms todo` — 할 일 목록
- `lms dashboard` — 대시보드
- `lms grades <course_id>` — 성적
- `lms submissions <course_id>` — 과제 제출 현황
- `lms quizzes <course_id>` — 퀴즈 목록

## 출처
- 원본: https://github.com/SonAIengine/ku-portal-mcp
- 포크: https://github.com/garibong-labs/ku-portal-mcp
