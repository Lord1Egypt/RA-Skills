# nmail

한국 이메일 서비스(네이버, 다음)를 위한 CLI. OpenClaw 에이전트가 쓰기 편하게 설계됨.

> Korean email CLI for agents and humans. JSON output by default.

## Features

- 🇰🇷 **Korean email first** — Naver, Daum presets, EUC-KR auto-decode
- 🤖 **Agent-first** — JSON output by default, `--pretty` for humans
- 📦 **Single binary** — Go, zero dependencies at runtime
- 🔌 **OpenClaw skill** — Install via [ClewHub](https://clawhub.ai)

## Installation

```bash
# Homebrew (macOS / Linux)
brew tap Harlockius/nmail
brew install nmail

# Go install
go install github.com/Harlockius/nmail@latest

# OpenClaw agents
clawhub install nmail
```

## Setup

```bash
# Add Naver account (uses app password)
nmail config add --provider naver --email you@naver.com --password <app-password>
```

> **App password 발급:** 네이버 → [내정보](https://nid.naver.com/user2/help/myInfoV2) → 보안설정 → 2단계 인증 설정 → 애플리케이션 비밀번호 생성
>
> **IMAP 활성화:** 네이버 메일 → 환경설정 → POP3/IMAP 설정 → IMAP/SMTP 사용함

## Usage

```bash
# List inbox (JSON)
nmail inbox --limit 20

# Human-readable
nmail inbox --pretty

# Read a message
nmail read 42

# Send
nmail send --to friend@naver.com --subject "안녕" --body "잘 지내?"

# Send from file
nmail send --to friend@naver.com --subject "긴 메일" --body-file ./message.txt

# Manage accounts
nmail config list
nmail config remove --email old@naver.com

# Search
nmail search --from "socra"
nmail search --subject "코딩" --since 2026-03-01
nmail search --unseen --limit 10

# Watch for new mail (polling, 5s interval)
nmail watch --poll 5
nmail watch --poll 5 --pretty
```

## Agent Usage

```bash
# Check new mail → summarize unread
nmail inbox --limit 10
# Parse JSON → filter is_read: false → nmail read <id> → summarize

# Reply to a message
nmail read 42                           # read original
nmail send --to <from> --subject "Re: <subject>" --body "reply"
```

## Status

| Phase | Status |
|-------|--------|
| Phase 1: Scaffolding | ✅ |
| Phase 2: Config | ✅ |
| Phase 3: Inbox & Read | ✅ |
| Phase 4: Send | ✅ |
| Phase 5: ClewHub + Homebrew | ✅ |
| Phase 5.5: Search & Watch | ✅ |
| Phase 6: Daum, Attachments | 🔜 |

## Contributing

Issues and PRs welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT © 2026 Harlock Choi
