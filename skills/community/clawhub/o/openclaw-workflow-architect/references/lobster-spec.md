# Lobster — Đặc tả kỹ thuật

Nguồn: https://docs.openclaw.ai/tools/lobster

---

## Tổng quan

Lobster là workflow shell cho phép OpenClaw chạy chuỗi lệnh CLI nhiều bước như một thao tác duy nhất, tất định, với các cổng phê duyệt tường minh.

**Ba điểm cốt lõi:**
- **Một lần gọi thay vì nhiều lần:** OpenClaw gọi một Lobster tool call, nhận kết quả có cấu trúc
- **Cổng phê duyệt tích hợp sẵn:** Side effects dừng workflow cho đến khi được phê duyệt tường minh
- **Có thể tiếp tục:** Workflow dừng trả về token; approve và tiếp tục mà không chạy lại từ đầu

---

## Cú pháp file `.lobster`

```yaml
name: tên-workflow
args:
  tên-tham-số:
    default: "giá trị mặc định"
    required: true   # hoặc bỏ qua nếu có default

steps:
  - id: tên-bước-duy-nhất
    command: lệnh-cli --json

  - id: bước-tiếp
    command: lệnh-cli --json
    stdin: $tên-bước-duy-nhất.stdout   # nhận output của bước trước

  - id: bước-approval
    command: lệnh-cli --approve
    stdin: $bước-tiếp.stdout
    approval: required                  # dừng và chờ phê duyệt

  - id: bước-thực-thi
    command: lệnh-cli --execute
    stdin: $bước-tiếp.stdout
    condition: $bước-approval.approved  # chỉ chạy nếu được approve
```

**Các trường trong step:**

| Trường | Bắt buộc | Mô tả |
|--------|----------|-------|
| `id` | ✓ | Tên duy nhất, dùng để tham chiếu qua `$id.stdout` |
| `command` | ✓ | Lệnh CLI chạy trong bước này |
| `stdin` | — | Đầu vào từ bước khác: `$id.stdout` hoặc `$id.json` |
| `approval` | — | `required` → dừng và chờ phê duyệt |
| `condition` | — | `$id.approved` → chỉ chạy nếu điều kiện đúng |

---

## Cách OpenClaw gọi Lobster

### Hành động `run`

```json
{
  "action": "run",
  "pipeline": "/đường/dẫn/workflow.lobster",
  "argsJson": "{\"tham-so\":\"giá-trị\"}",
  "cwd": "workspace",
  "timeoutMs": 30000,
  "maxStdoutBytes": 512000
}
```

Chạy pipeline nội tuyến (không cần file):

```json
{
  "action": "run",
  "pipeline": "lệnh-1 --json | lệnh-2 --json",
  "timeoutMs": 30000
}
```

### Hành động `resume`

```json
{
  "action": "resume",
  "token": "<resumeToken>",
  "approve": true
}
```

### Tham số tùy chọn

| Tham số | Mặc định | Ý nghĩa |
|---------|---------|---------|
| `cwd` | workspace | Thư mục làm việc (phải nằm trong process cwd) |
| `timeoutMs` | 20000 | Kết thúc tiến trình con nếu vượt thời gian |
| `maxStdoutBytes` | 512000 | Kết thúc nếu stdout vượt kích thước |
| `argsJson` | — | JSON string truyền vào `lobster run --args-json` |
| `lobsterPath` | `lobster` trên PATH | Đường dẫn tuyệt đối nếu cần chỉ định rõ |

---

## Phong bì đầu ra (Output envelope)

Lobster trả về JSON với một trong ba trạng thái:

### Thành công
```json
{
  "ok": true,
  "status": "ok",
  "output": [{ "kết quả": "dữ liệu" }]
}
```

### Chờ phê duyệt
```json
{
  "ok": true,
  "status": "needs_approval",
  "output": [{ "summary": "5 need replies, 2 need action" }],
  "requiresApproval": {
    "type": "approval_request",
    "prompt": "Gửi 2 bản nháp?",
    "items": [],
    "resumeToken": "eyJ..."
  }
}
```

### Bị hủy
```json
{
  "ok": false,
  "status": "cancelled"
}
```

---

## Nhúng bước AI: plugin `llm-task`

Bật trong `openclaw.json`:

```json
{
  "plugins": {
    "entries": {
      "llm-task": { "enabled": true }
    }
  },
  "agents": {
    "list": [
      {
        "id": "main",
        "tools": { "allow": ["llm-task"] }
      }
    ]
  }
}
```

Dùng trong Lobster step:

```yaml
- id: classify
  command: >
    openclaw.invoke --tool llm-task --action json --args-json '{
      "prompt": "Phân loại email đầu vào, trả về JSON với intent và draft.",
      "input": { "subject": "...", "body": "..." },
      "schema": {
        "type": "object",
        "properties": {
          "intent": { "type": "string" },
          "draft": { "type": "string" }
        },
        "required": ["intent", "draft"],
        "additionalProperties": false
      },
      "model": "gemini-3-flash-preview",
      "temperature": 0.4,
      "maxTokens": 2000
    }'
  stdin: $bước-trước.stdout
```

`llm-task` yêu cầu model chỉ xuất JSON (không có giải thích hay markdown fence), kiểm tra schema trước khi trả về.

---

## Cài đặt và bật plugin

```bash
# Cài Lobster CLI
npm install -g @clawdbot/lobster

# Kiểm tra
lobster --version
```

Lobster phải nằm trên `PATH` trên cùng máy chủ chạy OpenClaw Gateway.

Bật trong `openclaw.json` (cách an toàn):

```json
{
  "tools": {
    "alsoAllow": ["lobster"]
  }
}
```

> **Quan trọng:** Dùng `alsoAllow` (bổ sung) thay vì `allow` (allowlist thuần) để không vô tình block các core tools.

---

## Xử lý lỗi thường gặp

| Lỗi | Nguyên nhân | Cách xử lý |
|-----|------------|-----------|
| `lobster subprocess timed out` | Pipeline chạy quá lâu | Tăng `timeoutMs` hoặc chia nhỏ pipeline |
| `lobster output exceeded maxStdoutBytes` | Output quá lớn | Tăng `maxStdoutBytes` hoặc giảm output mỗi bước |
| `lobster returned invalid JSON` | Pipeline không ở tool mode | Đảm bảo chỉ in JSON ra stdout |
| `lobster failed (code N)` | Lỗi trong pipeline | Chạy cùng pipeline trong terminal để xem stderr |

---

## Lưu ý bảo mật

- **Chỉ tiến trình cục bộ** — plugin không tự gọi mạng
- **Không quản lý secrets** — Lobster gọi OpenClaw tools (chúng quản lý OAuth)
- **Nhận biết sandbox** — bị tắt khi tool context là sandboxed
- **Tên thực thi cố định** — `lobster` trên PATH; timeout và output caps được enforced
