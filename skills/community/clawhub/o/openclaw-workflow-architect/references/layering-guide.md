# Hướng dẫn phân tầng — OpenProse vs Lobster

---

## Sơ đồ tầng

```
┌─────────────────────────────────────────────────────────────┐
│  OPENPROSE — Tầng Điều Phối                                 │
│                                                             │
│  • Định nghĩa quy trình, luồng kiểm soát, đa tác nhân      │
│  • Đọc kỹ năng, lý luận về ngữ cảnh, xây dựng phiên AI     │
│  • Thực thi song song, cô lập ngữ cảnh                     │
│  • Quản lý trạng thái qua các phiên                        │
│  • Gọi Lobster như một công cụ bên dưới                     │
└──────────────────────┬──────────────────────────────────────┘
                       │ gọi khi cần
┌──────────────────────▼──────────────────────────────────────┐
│  LOBSTER — Tầng Thực Thi                                    │
│                                                             │
│  • Chạy chuỗi lệnh shell/CLI theo thứ tự xác định          │
│  • Cổng phê duyệt trước các tác dụng phụ                   │
│  • Truyền JSON giữa các bước                               │
│  • Tiếp tục với token sau khi được phê duyệt               │
│  • Kiểm tra schema, lưu file, so sánh sự khác biệt         │
└─────────────────────────────────────────────────────────────┘
```

---

## Bảng phân chia theo loại công việc

| Loại công việc | Công cụ đúng | Lý do |
|----------------|-------------|-------|
| Định nghĩa quy trình nhiều bước, điều phối AI | **OpenProse** | Hiểu ngữ cảnh và mục đích |
| Đọc file kỹ năng, lý luận về yêu cầu | **OpenProse** | Đây là công việc của phiên AI |
| Tạo và điều phối nhiều tác nhân AI | **OpenProse** | Đa tác nhân và chạy song song tích hợp sẵn |
| Vòng lặp qua danh sách (bài học, file, mục) | **OpenProse** | Luồng kiểm soát tích hợp sẵn |
| Quản lý trạng thái giữa các phiên | **OpenProse** | Hệ thống lưu trữ trạng thái tích hợp sẵn |
| Cổng phê duyệt trước tác dụng phụ | **Lobster** | Tất định, minh bạch, có thể kiểm tra |
| Kiểm tra schema + lưu kết quả | **Lobster** | Công cụ thuần túy, không cần lý luận AI |
| So sánh file, sao lưu phiên bản | **Lobster** | Thao tác ở tầng vỏ |
| Chạy lệnh CLI có tác dụng phụ | **Lobster** | Cần cổng phê duyệt và token tiếp tục |
| AI reasoning step trong chuỗi xác định | **Lobster + llm-task** | Nhúng AI vào pipeline tất định |

---

## Anti-patterns phổ biến

### Anti-pattern 1: Cầu nối thủ công để đưa context vào LLM

**Triệu chứng:**
```
Lobster step
  → prepare_prompt.py  ← file này không nên tồn tại
  → llm-task
  → file_manager.py
```

Có file Python làm một việc duy nhất: đọc `SKILL.md`, gộp file tham chiếu, điền biến, rồi tạo chuỗi text làm đầu vào cho `llm-task`.

**Nguyên nhân:** Lobster không biết cách nói chuyện với ngữ cảnh AI. Nó là vỏ thực thi — chỉ biết stdin/stdout.

**Fix:**
```
Phiên OpenProse  ← tác nhân là AI session
  → đọc skill file trực tiếp
  → lý luận về ngữ cảnh
  → [gọi Lobster khi cần thực thi xác định + phê duyệt]
```

---

### Anti-pattern 2: Tự xây kiến trúc tác nhân con từ đầu

**Triệu chứng:**
```
# Tài liệu thiết kế viết:
# "Phải tự inject task packet vào AGENTS.md trước khi spawn worker"
# "Tự handle announce pattern"
# "Tự quản lý state giữa 3 tầng"
```

Hoặc trong code:
```python
# Tự build 3 tầng
main_agent → sessions_spawn → orchestrator_agent
                                → sessions_spawn → worker_1
                                → sessions_spawn → worker_2
# + inject context thủ công vào AGENTS.md
```

**Nguyên nhân:** Đang tái tạo thứ OpenProse đã có sẵn.

**Fix:**
```yaml
# OpenProse thay thế toàn bộ:
parallel:
  for lesson in lessons:
    result_{lesson.id} = session: lesson_worker
      prompt: "Xử lý {lesson.title}."
      context: { lesson, constraints }
```

---

### Anti-pattern 3: Workaround cho vòng lặp

**Triệu chứng:**
```
# Comment trong code:
# "Giai đoạn 6-7 xử lý bằng Python script riêng vì Lobster không có for-loop"
```

Hoặc có file `process_items.py` được gọi từ Lobster chỉ để lặp qua một danh sách.

**Nguyên nhân:** Đang ở sai tầng. Lobster là vỏ thực thi, không phải ngôn ngữ điều phối.

**Fix:** OpenProse có `for item in list:` native. Nếu model không phải Prose Complete, dùng CLI script emit JSON list + Lobster `--each`.

---

### Anti-pattern 4: Approval gate đặt sai vị trí

**Triệu chứng:**
```yaml
steps:
  - id: execute          # ← side effect chạy TRƯỚC
    command: send-email --execute
    stdin: $data.stdout

  - id: approve          # ← approval đặt SAU, vô nghĩa
    command: confirm
    approval: required
```

**Nguyên nhân:** Hiểu nhầm thứ tự — `approval: required` phải dừng workflow TRƯỚC khi side effect xảy ra.

**Fix:**
```yaml
steps:
  - id: approve          # ← dừng và chờ phê duyệt
    command: preview-changes
    stdin: $data.stdout
    approval: required

  - id: execute          # ← chỉ chạy SAU khi được approve
    command: send-email --execute
    stdin: $data.stdout
    condition: $approve.approved
```

---

### Anti-pattern 5: Dùng `allow` thay vì `alsoAllow`

**Triệu chứng:**
```json
{
  "tools": {
    "allow": ["lobster"]
  }
}
```

**Nguyên nhân:** `allow` là allowlist thuần — chỉ cho phép đúng các tool được liệt kê, có thể vô tình block tất cả core tools.

**Fix:**
```json
{
  "tools": {
    "alsoAllow": ["lobster"]
  }
}
```

`alsoAllow` là bổ sung — thêm Lobster vào danh sách hiện có, không thay thế.

---

### Anti-pattern 6: Context phiên chính bị phình to

**Triệu chứng:**
```
# Phase 8 với 20 lesson workers đều dump context vào phiên chính
# → Context window bị lấp đầy
# → Agent bắt đầu "quên" thông tin từ đầu conversation
```

**Nguyên nhân:** Không có cô lập ngữ cảnh — tất cả sub-agents đều chia sẻ context với phiên chính.

**Fix:** OpenProse sub-sessions có context riêng. Chỉ kết quả cuối cùng (đầu ra đã tóm tắt) được trả về phiên chính.

---

## So sánh kiến trúc: Chỉ Lobster vs OpenProse + Lobster

| Khía cạnh | Chỉ dùng Lobster | OpenProse + Lobster |
|-----------|-----------------|---------------------|
| Đọc kỹ năng, xây dựng ngữ cảnh | `prepare_prompt.py` (cầu nối thủ công) | OpenProse tự xử lý (không cần mã thêm) |
| Vòng lặp qua danh sách | Script Python riêng (giải pháp vá víu) | `for item in list:` (tích hợp sẵn) |
| Thực thi song song | Không có | Khối `parallel:` (tích hợp sẵn) |
| Điều phối tác nhân con | Tự xây 3 tầng + inject AGENTS.md | Đa tác nhân OpenProse (tích hợp sẵn) |
| Cô lập ngữ cảnh | Tự quản lý | Mỗi phiên con có ngữ cảnh riêng |
| Cổng phê duyệt | `approval: required` ✓ | `approval: required` ✓ |
| Thực thi xác định | Các bước Lobster ✓ | Các bước Lobster ✓ |
| Tiếp tục sau sự cố | resumeToken ✓ | resumeToken ✓ |
| Số dòng mã hạ tầng | ~500 (công cụ Python) | ~150 (cầu nối tối giản) |

---

## Tại sao Lobster vẫn cần thiết ngay cả khi dùng OpenProse

Một số bước **phải** tuyệt đối xác định về thứ tự:

```
lesson_plan → slides_outline → exercises → teacher_guide
     ↑               ↑              ↑             ↑
  Phải xong      Dựa trên      Phải xong      Reference
  trước         lesson_plan     trước         exercises
```

Lobster đảm bảo điều này bằng `stdin: $step.stdout` — không bước nào bắt đầu trước bước trước hoàn thành và xuất kết quả.

**OpenProse mang lại:** orchestration thông minh, cô lập ngữ cảnh, multi-agent
**Lobster mang lại:** thứ tự xác định tuyệt đối, approval gates, resume tokens

Cả hai cần nhau trong quy trình phức tạp.
