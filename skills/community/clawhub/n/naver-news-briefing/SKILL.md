---
name: naver-news-briefing
description: Search, brief, and monitor 대한민국 Naver News via the Naver Search API using natural-language Korean queries. Use when the user wants 네이버 뉴스 브리핑, 최근 N일 뉴스 요약, 제외어 포함 뉴스 검색, 여러 질의를 한 번에 묶은 멀티 브리핑, 키워드 그룹 저장/관리, 특정 키워드의 지속 감시 규칙 추가/목록/삭제, 채팅형 자동화 요청을 watch/group 설정으로 바꾸기, or cron-friendly operator guidance for periodic news checks. Prefer this skill for Korean Naver-news workflows backed by local persistent state.
---

# naver-news-briefing

Use the CLI script at `scripts/naver_news_briefing.py`.

## Onboarding

- Treat Naver Search API credentials as mandatory before the first real use.
- Tell the user early that search/briefing/watch flows will fail until `client_id` and `client_secret` are stored.
- If the user has not completed setup yet, direct them to run:
  - `python scripts/naver_news_briefing.py setup --client-id ... --client-secret ...`
  - `python scripts/naver_news_briefing.py check-credentials --json`
- Present setup as the first-run path, not an optional advanced step.
- When helping with installation or first use, mention that credentials are stored in `data/config.json` and use DPAPI-backed secret storage on Windows when possible.

## Workflow

1. Store credentials once before any search/brief/watch command.
   - `python scripts/naver_news_briefing.py setup --client-id ... --client-secret ...`
   - Verify with `python scripts/naver_news_briefing.py check-credentials --json`
2. Run a one-shot briefing.
   - `python scripts/naver_news_briefing.py search "최근 3일 반도체 뉴스 브리핑 -광고"`
   - Add `--json` for machine-readable output.
3. Manage persistent watch rules with optional operator metadata.
   - Add: `python scripts/naver_news_briefing.py watch-add semiconductor "최근 7일 반도체 -광고" --label "반도체 감시" --tag watch --template watch-alert`
   - List: `python scripts/naver_news_briefing.py watch-list`
   - Remove: `python scripts/naver_news_briefing.py watch-remove semiconductor`
   - Check: `python scripts/naver_news_briefing.py watch-check semiconductor --json`
4. Manage persistent keyword groups for recurring briefings.
   - Add: `python scripts/naver_news_briefing.py group-add market-watch "최근 3일 반도체 -광고" "오늘 AI 데이터센터 -주가" --label "아침 시장" --tag 테크 --context "오전 보고용" --template morning-briefing`
   - List: `python scripts/naver_news_briefing.py group-list`
   - Inspect one group: `python scripts/naver_news_briefing.py group-list market-watch --json`
   - Update: `python scripts/naver_news_briefing.py group-update market-watch --add-query "배터리 공급망 -광고" --tag 공급망 --template analyst`
   - Remove: `python scripts/naver_news_briefing.py group-remove market-watch`
5. Run combined briefings.
   - `python scripts/naver_news_briefing.py brief-multi --group market-watch`
   - `python scripts/naver_news_briefing.py brief-multi --group market-watch --query "환율 뉴스" --template morning-briefing --json`
   - If `--template` is omitted, prefer the saved group template when present.
6. Convert chat-style automation requests into structured plans.
   - Inspect plan: `python scripts/naver_news_briefing.py plan "반도체 뉴스 1시간마다 모니터링해줘" --json`
   - Build an OpenClaw-friendly integration bundle: `python scripts/naver_news_briefing.py integration-plan "반도체 뉴스 1시간마다 모니터링해줘" --json`
   - Support practical Korean patterns such as `매일 아침 7시에 반도체랑 AI 데이터센터 뉴스 브리핑해줘` and `증권사 리포트 빼고 삼성전자 뉴스 계속 체크해줘`.
7. Materialize plans into persistent configs.
   - Watch: `python scripts/naver_news_briefing.py plan-save "반도체 뉴스 1시간마다 모니터링해줘" --as watch --name semiconductor-hourly`
   - Group: `python scripts/naver_news_briefing.py plan-save "매일 아침 7시에 반도체랑 AI 데이터센터 뉴스 브리핑해줘" --as group --name morning-tech --label "아침 브리핑"`

## Behavior

- Parse positive keywords and `-제외어` using the upstream tab-search policy.
- Interpret recent-news phrases such as `오늘`, `최근 3일`, `최근 2주`, `한달`, `이번주`, `지난주` as a date window and remove that phrase from the API search query.
- Normalize more natural Korean sentence inputs by stripping request phrases, common 조사, duplicate tokens, and Korean exclusion phrases such as `A 말고`, `B 빼고`, `C 제외` into `-제외어` tokens.
- Parse practical schedule intent from Korean chat requests into `interval`, `daily`, `weekly`, or `manual` plans.
- Preserve operator-facing metadata on saved watch/group entries: `label`, `tags`, `template`, `schedule`, `operator_hints`, and original request context.
- Use DPAPI-backed secret storage on Windows when possible.
- Deduplicate watch notifications by `(watch_id, link)` so repeated cron runs emit only newly seen items.
- `plan` returns cron-friendly operator hints, recommended commands, and a storage-target recommendation (`watch` vs `group`).
- `integration-plan` returns a more practical operator bundle: save command, run command, schedule object, cron line, OpenClaw-friendly systemEvent text, and a Korean confirmation summary.
- `plan-save` materializes a parsed plan into a saved `watch` or `group` configuration without owning cron wiring itself.
- `brief-multi` returns chat-friendly combined text by default and structured JSON with `--json`.

## Notes

- Read `references/upstream-notes.md` before major edits.
- The skill uses headline/summary metadata from the Naver Search API. It does not fetch or summarize full article bodies.
- Keep additions additive: preserve existing `search`, `watch-add`, `watch-list`, `watch-remove`, and `watch-check` flows.
- Public user-facing documentation lives in `README.md`; keep it Korean-first and concrete.
