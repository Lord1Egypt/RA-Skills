---
name: git-commit-formatter
description: |
  Format commit message theo Conventional Commits standard (Conventional Commits v1.0.0).
  Input là git diff hoặc mô tả thay đổi, output là commit message có type/scope/body.
  Dùng khi user nói "format commit", "commit message", "conventional commit",
  "viết message cho git", hoặc khi có Git diff cần chuyển đổi thành commit message chuẩn.
  KHÔNG dùng cho: tạo branch, merge PR, revert commit (có patterns riêng).
---

# Goal

Sinh commit message chuẩn Conventional Commits trong 5 giây, consistent 100% across team.

---

# Instructions

## Bước 1: Nhận input

Kiểm tra loại input user cung cấp:

**Nếu là Git diff output (có `diff --git`, `index`, lines với `+`/`-`):**
→ Parse diff để trích xuất thông tin thay đổi

**Nếu là mô tả bằng text:**
→ Hỏi clarifying nếu cần:
  - "Em cần biết thêm: (A) Tên files đã thay đổi, (B) Loại thay đổi chính xác, hay (C) File paths đã thay đổi?"

**Nếu không rõ:**
→ Hỏi: "Anh/chị cho em biết: (A) Dùng git diff, (B) Mô tả bằng tay, hay (C) File paths đã thay đổi?"

## Bước 2: Xác định TYPE

Dựa trên nội dung thay đổi, chọn type phù hợp:

| Type | Khi dùng |
| --- | --- |
| **feat** | Tính năng mới (new feature, new capability) |
| **fix** | Sửa bug (fix error, fix bug, fix issue) |
| **docs** | Thay đổi documentation |
| **style** | Format code, không ảnh hưởng logic (whitespace, semicolon) |
| **refactor** | Refactor code, không thay đổi hành vi (rename, extract) |
| **test** | Thêm, sửa, refactor test |
| **chore** | Việc maintenance (update deps, build config) |

**Logic quyết định:**
```
IF có "fix" + "bug" + "error" → type = fix
ELIF có "add" + "new" + "create" + "implement" → type = feat
ELIF có "doc" + "readme" + "comment" → type = docs
ELIF có "format" + "style" + "indent" → type = style
ELIF có "refactor" + "rename" + "extract" → type = refactor
ELIF có "test" + "spec" + "assert" → type = test
ELSE → type = chore
```

## Bước 3: Xác định SCOPE (tùy chọn)

Scope là phần thay đổi cụ thể, ngắn gọn:

**Nếu nhiều files khác nhau:**
→ Thường **KHÔNG** có scope (rủi ro quá dài)

**Nếu 1 file hoặc 1 module:**
→ Dùng file/module name kebab-case:
  - `auth`
  - `user-service`
  - `commit-formatter`

## Bước 4: Viết SUBJECT (bắt buộc)

Format: `<type>(<scope>): <description>`

**Quy tắc:**
- Subject **PHẢI** có type (lowercase)
- Subject **PHẢI** có description
- Subject ≤ **50 characters** (bao gồm type + scope)
- Subject **KHÔNG** có dấu chấm cuối
- Subject dùng **imperative mood**:
  - ✅ "Add user authentication"
  - ❌ "Added user authentication"
  - ✅ "Fix null pointer error"
  - ❌ "Fixed null pointer error"

**Examples:**
```
feat: add user login
fix(auth): resolve session timeout
docs: update API reference
style: format code with prettier
refactor: extract validation logic
test: add unit tests for auth
chore: upgrade to Node.js v22
```

## Bước 5: Viết BODY (tùy chọn)

**Khi nào cần body:**
- Có >1 sự thay đổi khác nhau
- Cần giải thích TẠI SAO (breaking change, edge case)
- Referencing issue/PR

**Format body:**

```
[blank line]
<explanation>

[optional details]
- Closes #123
- Refs PR #456
```

**Quy tắc body:**
- Có 1 blank line giữa subject và body
- Mỗi dòng ≤ 72 characters (để dễ đọc trên terminal)
- Dùng **imperative mood** giống subject
- Dùng bullet points cho multiple items

**Examples body:**
```
Add email verification flow

- Send verification link to user email
- Verify token on click
- Update user status to verified

Closes #45
```

## Bước 6: Xác thực OUTPUT

Kiểm tra commit message vừa tạo:

- [ ] Type trong danh sách (feat|fix|docs|style|refactor|test|chore)
- [ ] Type là lowercase
- [ ] Subject ≤ 50 characters
- [ ] Subject có description
- [ ] Subject KHÔNG có dấu chấm cuối
- [ ] Nếu có body: có 1 blank line giữa subject/body
- [ ] Body (nếu có): mỗi dòng ≤ 72 characters
- [ ] Subject + Body dùng imperative mood

Nếu FAIL bất kỳ check → Hỏi user sửa input.

---

# Examples

## Ví dụ 1: Happy Path — Git diff từ feature branch

**Context:** Dev vừa hoàn thành feature login, push code lên Git, muốn commit message chuẩn.

**Input (Git diff):**
```
diff --git a/index.js b/index.js
index abc123..def456 100644
--- a/index.js
+++ b/index.js
@@ -1,5 +1,6 @@
 const express = require('express');
-const app = express();
+const app = express().use(express.json());
```

**Thought Process:**
- Nhận diff: thêm `express.json()` middleware → Đây là **feat** (thay đổi behavior)
- Files: chỉ index.js → **Scope không cần** (quá dài nếu có)
- Description: "add express json middleware" → Imperative: "add express json middleware"
- Length: 29 chars (bao gồm "feat: ") < 50 ✅

**Output:**
```
feat: add express json middleware

Adds JSON body parsing to Express app.
```

## Ví dụ 2: Edge Case — Mô tả text thay vì Git diff

**Context:** Dev sửa bug trong auth module, chỉ mô tả bằng văn bản.

**Input:**
"Sửa lỗi session timeout trong file auth.js, user bị logout sau 10 phút"

**Thought Process:**
- Có "fix" + "error" → **type: fix**
- File: auth.js → **scope: auth**
- Description: "resolve session timeout" → Imperative ✅
- Length: 27 chars < 50 ✅

**Output:**
```
fix(auth): resolve session timeout

Set session timeout to 24 hours to prevent users
from being logged out too quickly.

Closes #789
```

## Ví dụ 3: Multiple Changes — Thay đổi nhiều files khác nhau

**Context:** Dev vừa refactor authentication + fix bug trong user service + update docs cho cả hai.

**Input (Mô tả):**
"Refactor auth module, fix user service validation, update docs for both"

**Thought Process:**
- 3 files khác nhau → **Không có scope** (quá dài)
- Dominant change: refactor → **type: refactor**
- Description: "refactor authentication system" → Imperative ✅

**Output:**
```
refactor: refactor authentication system

Extract user validation to separate service and improve
error handling across auth module.

Changes:
- auth.js: extract validation logic
- user-service.js: add validation middleware
- README.md: update auth flow docs

Refs PR #123, #456
```

## Ví dụ 4: Breaking Change — Thay đổi không tương thích

**Context:** Dev thay đổi API signature, breaking change cho clients cũ.

**Input (Mô tả):**
"Thay đổi API /user endpoint, từ email sang userId, breaking change cho clients"

**Thought Process:**
- Thay đổi behavior → **type: feat**
- File: user endpoint → **scope: user**
- Breaking change → Cần **body** giải thích
- Description: "change user endpoint to use userId" → Imperative ✅

**Output:**
```
feat(user): change user endpoint to use userId

BREAKING CHANGE: Email parameter removed, use userId instead.
Update API clients to use new endpoint format.

- Updated /user GET endpoint
- Removed email parameter
- Added userId parameter

Migration guide: See docs/api-migration.md

Closes #901
```

## Ví dụ 5: Style Change — Format không ảnh hưởng logic

**Context:** Dev chạy prettier, chỉ format code, không thay đổi logic.

**Input (Git diff hoặc mô tả):**
"Format tất cả files với prettier, thêm dấu chấm cuối dòng"

**Thought Process:**
- Chỉ format → **type: style**
- Files: nhiều → **Không có scope**
- Description: "format code with prettier" → Imperative ✅
- Body không cần (chỉ formatting)

**Output:**
```
style: format code with prettier
```

---

# Constraints

## Bắt buộc (MUST)

- 🚫 **TUYỆT ĐỐI KHÔNG** tạo commit type ngoài danh sách: `feat|fix|docs|style|refactor|test|chore`
- 🚫 **TUYỆT ĐỐI KHÔNG** viết type với UPPERCASE → Luôn lowercase
- 🚫 **TUYỆT ĐỐI KHÔNG** subject vượt 50 characters → Truncate hoặc tách commit
- 🚫 **TUYỆT ĐỐI KHÔNG** subject có dấu chấm cuối → Hỏi user sửa
- 🚫 **TUYỆT ĐỐI KHÔNG** thiếu description trong subject → Hỏi user thêm
- ✅ **LUÔN LUÔN** có type (bắt buộc)
- ✅ **LUÔN LUÔN** subject có description (bắt buộc)

## Không bắt buộc (SHOULD)

- ⚠️ **NÊN** có scope nếu 1 file/module duy nhất → Giúp review code dễ hơn
- ⚠️ **NÊN** có body nếu nhiều changes hoặc breaking change → Giải thích context
- ⚠️ **NÊN** body mỗi dòng ≤ 72 characters → Đọc dễ trên terminal
- ⚠️ **NÊN** refer issue/PR nếu có (Closes #123, Refs PR #456)

## Special Cases

### Nếu commit lớn (>1000 files)
→ Tách thành multiple commits, mỗi commit 1 logical change

### Nếu commit revert
→ Dùng type `revert`, format: `revert: <original subject>`

### Nếu commit merge
→ Không dùng skill này → Git tạo merge commit tự động

---

# Whitelist Integration

**Trạng thái:** ✅ Active

**File:** `/data/workspace/whitelist.yml`

**Mô tả:** File này điều khiển skill nào được phép tự động thêm vào Gateway hệ thống (auto-add). Khi Hina nhận trigger "tạo skill", "tạo skill mới", Hina sẽ kiểm tra danh sách whitelist này trước khi tự động thêm skill.

**Cách hoạt động:**
1. Hina đọc `/data/workspace/whitelist.yml`
2. Hina kiểm tra skill name có trong danh sách `skills_allowed_auto_add` không
3. Nếu có → Auto-add skill **KHÔNG** cần hỏi lại
4. Nếu không → Hina hỏi anh trước khi thêm

**Các skill hiện tại trong whitelist:**
- git-commit-formatter
- skill-creator-ultra

**Cập nhật whitelist:**
- Thêm skill: Thêm vào danh sách YAML ở trên
- Xóa skill: Đánh dấu `status: "disabled"` hoặc xóa khỏi danh sách
- Cập nhật: Sửa `last_updated` timestamp

**Lợi ích:**
- ✅ Tự động hóa cho skill phổ biến
- ✅ Tránh hỏi lặp lại
- ✅ Kiểm soát rủi ro (chỉ skill an toàn trong whitelist)

---

# Reference Data

## Conventional Commits Standard

Đây là danh sách types chính thức:

| Type | Description |
| --- | --- |
| **feat** | Tính năng mới (new feature, new capability) |
| **fix** | Sửa bug (fix error, fix bug, fix issue) |
| **docs** | Thay đổi documentation (README, comments, API docs) |
| **style** | Format code (whitespace, semicolon, indentation) - không ảnh hưởng logic |
| **refactor** | Refactor code (rename, extract) - không thay đổi behavior |
| **test** | Thêm/sửa/refactor test (tests, specs) |
| **chore** | Maintenance (build config, update deps, script) |

**Quy tắc important:**
- Type luôn **lowercase**
- Format: `<type>(<scope>): <subject>`
- Body tùy chọn, dùng nếu cần giải thích

### Subject Examples

| ❌ Sai | ✅ Đúng |
| --- | --- |
| Added user login | feat: add user login |
| Fixed bug | fix: resolve authentication error |
| Update docs | docs: update README |
| Format code | style: format with prettier |
| Refactored code | refactor: extract validation logic |

---

<!-- Generated by Skill Creator Ultra v1.0 -->
