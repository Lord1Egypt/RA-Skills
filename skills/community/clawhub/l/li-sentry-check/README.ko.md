# 🔍 li_sentry_check - 서버 점검 스킬

> 멀티 플랫폼 서버 점검 및 헬스체크 스킬. SSH 키 인증을 통해 원격 Linux 서버에 로그인하여 읽기 전용 점검 명령을 실행하고 구조화된 Markdown 보고서를 생성합니다.

[![버전](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://clawhub.ai/skills/li_sentry_check)
[![플랫폼](https://img.shields.io/badge/플랫폼-nanobot%20%7C%20OpenClaw%20%7C%20Hermes-green.svg)]()
[![라이선스](https://img.shields.io/badge/라이선스-MIT-green.svg)](LICENSE)

## 📋 개요

`li_sentry_check`는 **nanobot**, **OpenClaw**, **Hermes agent**를 지원하는 크로스 플랫폼 서버 점검 스킬입니다. SSH 키 인증을 통해 원격 Linux 서버에 로그인하여 읽기 전용 점검 명령(CPU, 메모리, 디스크, 네트워크, 서비스, 보안)을 실행하고 이상 정보를 자동으로 강조 표시하는 구조화된 Markdown 보고서를 생성합니다.

## ✨ 핵심 기능

| 기능 | 설명 |
|------|------|
| 🔐 SSH 키 인증 | 키 전용 인증, 비밀번호 로그인 비활성화, 보안 강화 |
| 📊 하드웨어 점검 | CPU, 메모리, 디스크, 네트워크 사용량 |
| 🖥️ 서비스 점검 | 주요 서비스 상태, 오류 로그 |
| 🛡️ 보안 점검 | SSH 비정상 로그인, 방화벽 경고, 커널 오류 |
| 📝 구조화된 보고서 | Markdown/JSON 형식, 이상 정보 우선 표시 |
| 🌐 크로스 플랫폼 | nanobot, OpenClaw, Hermes 지원 |

## 🚀 빠른 시작

### 1. 스킬 설치

```bash
# nanobot
./manage.sh skill install li_sentry_check

# OpenClaw
npx clawhub@latest install li_sentry_check

# Hermes
hermes skill install li_sentry_check
```

### 2. SSH 키 구성

```bash
# 키 쌍 생성
ssh-keygen -t rsa -b 4096 -f ~/.ssh/li_sentry_check -N ""

# 공개 키를 원격 서버에 복사
ssh-copy-id -i ~/.ssh/li_sentry_check.pub inspector@<서버_IP>

# 연결 테스트
ssh -i ~/.ssh/li_sentry_check inspector@<서버_IP>
```

### 3. 대상 서버 구성

`references/targets.yaml` 수정:

```yaml
targets:
  운영-웹:
    host: YOUR_SERVER_IP
    port: 22
    user: inspector
    keyPath: ~/.ssh/li_sentry_check
    services:
      - nginx
      - docker
      - sshd
```

### 4. 점검 실행

```bash
# 기본 점검 (하드웨어 리소스)
python3 scripts/inspect.py --target 운영-웹 --checks basic

# 서비스 점검
python3 scripts/inspect.py --target 운영-웹 --checks services

# 전체 점검 (기본 + 서비스 + 보안 + 로그)
python3 scripts/inspect.py --target 운영-웹 --checks daily

# JSON 형식 출력
python3 scripts/inspect.py --target 운영-웹 --checks daily --format json

# 파일로 출력
python3 scripts/inspect.py --target 운영-웹 --checks daily --output report.md
```

## 📖 점검 체크 그룹

| 그룹 | 내용 | 명령 수 |
|------|------|---------|
| `basic` | CPU, 메모리, 디스크, 네트워크 | 8 |
| `services` | 서비스 상태 + 오류 로그 (동적) | 3×N |
| `daily` | 전체 점검 (기본 + 서비스 + 보안 + 로그) | 26 |

## 📊 보고서 예시

```markdown
# 🔍 서버 점검 보고서

- 대상: 운영-웹
- 호스트: YOUR_SERVER_IP
- 사용자: inspector
- 체크: daily
- 시작: 2026-04-26T09:00:00+00:00
- 전체 체크: 26
- ⚠️ 이상: 3

## 전체 상태: ⚠️ 경고

## ⚠️ 이상 (우선)

### ⚠️ systemd_failed_units
명령: `systemctl --failed --no-pager`
상태: OK (이상 포함)

출력:
```
UNIT          LOAD   ACTIVE SUB    DESCRIPTION
mcelog.service loaded failed failed Machine Check Exception Logging Daemon
```
```

## 🔧 명령줄 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--target` | 대상 서버 이름 (targets.yaml에 정의) | (필수) |
| `--checks` | 체크 그룹: `basic`, `services`, `daily` | `basic` |
| `--format` | 출력 형식: `markdown`, `json` | `markdown` |
| `--output` | 파일로 출력 (기본: stdout) | stdout |

## 🌐 크로스 플랫폼 지원

| 플랫폼 | 런타임 | 스크립트 | 명령 |
|--------|--------|----------|------|
| **OpenClaw** | Node.js 24+ | `scripts/inspect.mjs` | `node scripts/inspect.mjs --target bogon --checks daily` |
| **NanoBot** | Python 3.10+ | `scripts/inspect.py` | `python3 scripts/inspect.py --target bogon --checks daily` |
| **Hermes** | Python 3.10+ | `scripts/inspect.py` | `python3 scripts/inspect.py --target bogon --checks daily` |

## 📁 파일 구조

```
li_sentry_check/
├── SKILL.md                  # 스킬 문서
├── _meta.json                # 스킬 메타데이터
├── design.md                 # 설계 문서
├── references/
│   ├── targets.yaml          # 대상 서버 구성
│   └── checks.yaml           # 점검 명령 허용 목록
└── scripts/
    ├── inspect.mjs           # Node.js 구현 (OpenClaw)
    └── inspect.py            # Python 구현 (NanoBot/Hermes)
```

## 🔒 보안 모범 사례

- **키 권한**: `chmod 600 ~/.ssh/li_sentry_check`
- **호스트 검증**: 프로덕션에서는 `accept-new` 대신 `known_hosts`를 사전에 채우세요
- **서비스 이름**: 영숫자, 하이픈, 밑줄만 허용 (사용 전 검증)
- **명령 허용 목록**: `checks.yaml`을 상태 변경 명령으로 절대 수정하지 마세요
- **보고서 처리**: 보고서에 시스템 데이터가 포함될 수 있음 — 공개적으로 공유하지 마세요

## 🔧 확장 가이드

### 새 대상 서버 추가

`references/targets.yaml` 수정:

```yaml
targets:
  데이터베이스-서버:
    host: YOUR_SERVER_IP
    port: 22
    user: inspector
    keyPath: ~/.ssh/li_sentry_check
    services:
      - mysql
      - redis
```

### 새 체크 그룹 추가

`references/checks.yaml` 수정:

```yaml
checks:
  데이터베이스:
    description: 데이터베이스 점검
    commands:
      - id: mysql_status
        cmd: "systemctl status mysql --no-pager | sed -n '1,20p'"
        timeoutSec: 10
      - id: mysql_connections
        cmd: "mysql -e 'SHOW STATUS LIKE \"Threads_connected\"' || true"
        timeoutSec: 15
```

## 📝 버전 기록

| 버전 | 날짜 | 변경 사항 |
|------|------|-----------|
| 0.1.0 | 2026-04-26 | 초기 릴리스: 기본, 서비스, 전체 점검 |

## 📄 라이선스

MIT 라이선스
