status: open

# PR-001: Implement Structured Notification Formatting Logic

## 1. Objective
Create a new module or functions to generate structured, emoji-rich, numbered Slack notification messages in Chinese for the SDLC process.

## 2. Scope & Implementation Details
- Create `src/notifications.py` (or add to existing utility).
- Implement functions returning formatted strings:
  - `format_sdlc_start(prd_id: str) -> str`: Returns "🚀 1. [{prd_id}] SDLC 启动"
  - `format_slicing_start(prd_id: str) -> str`: Returns "🔪 2. [{prd_id}] 切片中..."
  - `format_slicing_done(prd_id: str, count: int) -> str`: Returns "✅ 3. [{prd_id}] 切片结束，共生成 {count} 个切片"
  - `format_coder_start(pr_id: str) -> str`: Returns "👨‍💻 4. [{pr_id}] Coder 运行中..."
  - `format_review_start(pr_id: str) -> str`: Returns "🧐 5. [{pr_id}] Coder 结束，Review 中..."
  - `format_review_result(pr_id: str, summary: str) -> str`: Returns "📝 6. [{pr_id}] Review 结果：{summary}"

## 3. TDD & Acceptance Criteria
- Create `tests/test_notifications.py`.
- Write unit tests for every formatting function, asserting the exact string output matches the required format including emojis and numbering.

---

status: open

# PR-002: Integrate Structured Notifications into Orchestrator

## 1. Objective
Replace the existing unstructured `notify_channel` calls in `orchestrator.py` with the new structured formatting functions created in PR-001.

## 2. Scope & Implementation Details
- Modify `src/orchestrator.py`.
- Import the formatting functions from `notifications.py`.
- Locate the SDLC lifecycle stages (start, slicing start, slicing end, coder start, review start, review end) and update the message passed to `notify_channel` using the new formatters.

## 3. TDD & Acceptance Criteria
- Modify or create `tests/test_orchestrator.py`.
- Use `unittest.mock.patch` to mock `notify_channel`.
- Run the orchestrator flow (or specific functions) and assert that `notify_channel` is called with the exact formatted strings at each stage.
