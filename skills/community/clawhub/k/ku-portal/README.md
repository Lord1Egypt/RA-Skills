# KU Portal — 고려대학교 KUPID 포털 스킬

고려대학교 KUPID 포털, 도서관, Canvas LMS 정보를 OpenClaw에서 조회하는 스킬.

> 원본: [SonAIengine/ku-portal-mcp](https://github.com/SonAIengine/ku-portal-mcp) 패키지를 Python 라이브러리로 사용하는 OpenClaw CLI 래퍼.

## 아키텍처 (ku-portal-mcp와의 관계)

- **ku-portal-mcp** (upstream): MCP 서버 프로젝트이자 PyPI 패키지.
- **ku-portal 스킬** (이 저장소): `ku_query.py`가 ku-portal-mcp의 내부 모듈(`auth`, `courses`, `library` 등)을 **Python 라이브러리로 직접 import**하여 사용. MCP 프로토콜은 사용하지 않음.
- upstream 패키지 업데이트(`pip install --upgrade ku-portal-mcp`)로 신기능이 반영됨.
- fork 저장소 ([garibong-labs/ku-portal-mcp](https://github.com/garibong-labs/ku-portal-mcp))는 upstream 추적/참조용.

## 기능

| 기능 | 로그인 | 설명 |
|------|--------|------|
| 도서관 좌석 | 불필요 | 6개 도서관 53개 열람실 실시간 좌석 현황 |
| 공지사항 | SSO | 목록 조회 + 상세 + 키워드 검색 |
| 학사일정 | SSO | 학사일정 목록 + 상세 |
| 장학공지 | SSO | 장학공지 목록 |
| 시간표 | SSO | 주간 시간표 + ICS 내보내기 |
| 수강과목 | SSO | 수강신청 내역, 개설과목 검색, 강의계획서 |
| LMS | KSSO | 과제, 강의자료, 성적, 퀴즈, 대시보드 |

## 설치

```bash
# 1. 스킬 설치
clawhub install garibong-labs/ku-portal

# 2. 자동 설치 (venv 생성 + 패키지 설치 + 안내)
bash scripts/setup.sh
```

또는 수동 설치:

```bash
# 스킬 디렉터리로 이동
cd <skill-dir>

# Python venv 생성 + 패키지 설치
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install ku-portal-mcp

# 자격 증명 설정 (로그인 기능 사용 시)
mkdir -p ~/.config/ku-portal
cat > ~/.config/ku-portal/credentials.json << 'EOF'
{"id": "your-kupid-id", "pw": "your-kupid-password"}
EOF
chmod 600 ~/.config/ku-portal/credentials.json
```

OpenClaw 스킬 문서 안에서는 `{baseDir}`를 사용할 수 있습니다.

```bash
. {baseDir}/.venv/bin/activate
python3 {baseDir}/ku_query.py lms courses
```

## 사용법

```bash
# 먼저 스킬 디렉터리로 이동
cd <skill-dir>
. .venv/bin/activate

# 도서관 좌석 (로그인 불필요)
python3 ku_query.py library
python3 ku_query.py library --name 중앙도서관

# 공지사항
python3 ku_query.py notices --limit 10
python3 ku_query.py notices --detail <message_id>

# 학사일정 / 장학공지
python3 ku_query.py schedules
python3 ku_query.py scholarships

# 통합 검색
python3 ku_query.py search 수강신청

# 시간표
python3 ku_query.py timetable
python3 ku_query.py timetable --day 월
python3 ku_query.py timetable --ics

# 수강과목
python3 ku_query.py mycourses
python3 ku_query.py courses --college 정보대학 --dept 컴퓨터학과
python3 ku_query.py syllabus COSE101

# LMS
python3 ku_query.py lms courses
python3 ku_query.py lms assignments <course_id>
python3 ku_query.py lms todo
python3 ku_query.py lms dashboard
python3 ku_query.py lms grades <course_id>
```

## 로컬 파일 접근 / 보안

- 자격 증명 읽기: `~/.config/ku-portal/credentials.json` (chmod 600 권장)
- 포털 세션 캐시: `~/.cache/ku-portal-mcp/session.json` (30분 TTL)
- LMS 세션 캐시: `~/.cache/ku-portal-mcp/lms_session.json` (약 25분 TTL)
- 서버 로그: `~/.cache/ku-portal-mcp/server.log`
- ICS 내보내기: `~/Downloads/ku_timetable.ics` (`timetable --ics` 사용 시 생성)
- 자격 증명은 스킬 디렉터리 밖이라 git/ClawHub 번들에 포함되지 않음

## 라이선스

MIT — 원본 [ku-portal-mcp](https://github.com/SonAIengine/ku-portal-mcp) MIT 라이선스 준수.

## 문의

contact@garibong.dev
