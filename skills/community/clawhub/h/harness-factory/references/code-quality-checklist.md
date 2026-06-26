# Code Quality Checklist

## Mechanical Checks (Must ALL Pass)
- [ ] `py_compile` on every changed `.py` file
- [ ] `tsc --noEmit` on frontend (if TypeScript)
- [ ] `npm run build` succeeds (if frontend deployment)
- [ ] No syntax errors in any changed file

## Clean Code
- [ ] No `console.log` / `print()` debug statements
- [ ] No `TODO` / `FIXME` / `HACK` comments
- [ ] No `as any` type assertions (TypeScript)
- [ ] No commented-out code blocks
- [ ] All imports are used (no dead imports)
- [ ] All functions have docstrings/comments

## Architecture
- [ ] Follows existing code patterns and conventions
- [ ] No duplicate code (DRY principle)
- [ ] Clean separation of concerns
- [ ] New dependencies justified and documented

## Error Handling
- [ ] Every external call (API, DB, file) wrapped in try/catch
- [ ] User-facing error messages are friendly and actionable
- [ ] Internal errors logged with context (not swallowed silently)
- [ ] Partial failures handled gracefully (one failure doesn't kill everything)

## Performance
- [ ] No N+1 queries
- [ ] Concurrent operations use proper concurrency controls (semaphores)
- [ ] Large operations have reasonable timeouts
- [ ] No blocking calls in async context

## Lessons from Our Projects
- [ ] **BeautifulSoup/requests** — don't add if project uses httpx (Brand Style Clone Round 2)
- [ ] **Image size threshold** — 10KB minimum, not 5KB (Brand Style Clone Round 4)
- [ ] **Parallel strategies** — I/O-bound operations should run in ThreadPoolExecutor (Brand Style Clone Round 4)
- [ ] **In-memory storage** — persist to DB, not just dicts that die on restart (TrendMuse Round 2)
- [ ] **Chinese text in English app** — grep for Chinese characters before shipping (TrendMuse Round 5)
