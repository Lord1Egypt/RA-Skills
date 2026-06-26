# The Three-Sentence Contract

Every `*.prompt.md` build bundle this skill produces **must** contain three explicitly labeled sentences. The verify-lite scanner rejects bundles missing any of them.

## The three sentences

### S1 — WHO + WHAT

> "**Who** uses it, **what** they do, **what data** flows in and out."

Examples:

- "财务同事，每天把一堆 PDF 发票整理成 Excel 台账。"
- "Frontline support engineers, who triage incoming Slack alerts by extracting the failing service from each message and routing it to an on-call rotation."
- "妈妈，每晚记录宝宝睡眠时段，一周生成一张分享图。"

S1 must name a **concrete person** and a **concrete action** with **concrete data**. Reject vague S1 like "users do stuff" or "an AI app that helps everyone".

### S2 — WHERE

> "**Platform target(s)**, **runtime constraints**, **distribution channel**."

Examples:

- "macOS + Windows 桌面，本地运行，不联网；通过公司 MDM 私有分发。"
- "iOS 17+ only, App Store distribution, syncs via iCloud private DB."
- "Internal Docker Compose on a 4-core company server, LDAP auth."

S2 must name at least one platform from the 12-mode table. It must also state network posture (offline / online / hybrid).

### S3 — HOW SUCCESS LOOKS

> "**Binary acceptance**, **packaging artifact**, **non-goals**."

Examples:

- "拖入文件夹自动出 .xlsx；不确定字段标黄；产物为 .dmg + .exe；不做 OCR、不做云同步。"
- "Cold start <1.2s on iPhone 12; primary flow works with the sample CSV; ships as TestFlight build; explicitly NOT a chat app."

S3 must be **observable** (yes/no items, not vibes) and must name the **non-goals** so the calling agent doesn't pad scope.

## What if the user gives only one sentence?

**Infer the other two and label them `(assumed)`.** Do **not** block with clarifying questions on the first turn. Pattern:

```markdown
## S1 — WHO + WHAT
财务同事，每天把一堆 PDF 发票整理成 Excel 台账。

## S2 — WHERE
*(assumed)* macOS 13+ and Windows 10/11, 100% local, no network at first launch.
Distribution: private download link. — flag if wrong.

## S3 — HOW SUCCESS LOOKS
*(assumed)* Drop a folder, get an .xlsx in <30s; uncertain rows highlighted yellow;
ship .dmg + .exe; explicitly NOT doing OCR for handwriting. — flag if wrong.
```

The bundle still verifies. The user can correct in turn 2.

## What if S1 names multiple personas?

Pick the **primary** persona for S1; mention secondary personas under `## Acceptance` as edge cases. Bundles are about one workflow at a time.

## What if S2 names multiple platforms?

Emit **one bundle per platform** plus a shared `shared-core.md`. See [modes.md → Multi-platform requests](modes.md#multi-platform-requests).

## Anti-patterns (verify-lite rejects these)

| Anti-pattern | Reject reason |
|---|---|
| S1 missing | "build bundle has no who/what" |
| S1 = "users do things" | Vague — no concrete persona or action |
| S2 missing platform | "no platform target named" |
| S3 has no binary acceptance | "no observable success criterion" |
| S3 with "and many more features" | Scope creep marker — fail |
| Any `TODO:` or `lorem ipsum` literal in body | Template leak |
| Hardcoded `sk_live_...` / `ghp_...` / `AKIA...` etc. | Secret leak — fail hard |

## Why exactly three?

- **Three** is enough to disambiguate routing, acceptance, and packaging.
- **Three** is short enough for a user to write in one breath.
- **Three** maps cleanly to the three S-sections every template carries — no off-by-one between the human side and the agent side of the contract.
