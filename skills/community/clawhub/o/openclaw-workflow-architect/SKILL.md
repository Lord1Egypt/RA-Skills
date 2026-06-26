---
name: openclaw-workflow-architect
description: >
  Dùng skill này bất cứ khi nào người dùng muốn thiết kế, phân tích, hoặc
  sinh code quy trình cho OpenClaw — bao gồm: hỏi nên dùng Lobster hay
  OpenProse, có workflow/pipeline hiện tại cần review, muốn chuyển kiến trúc
  cũ sang đúng tầng, hoặc cần tạo file .prose/.lobster thực sự vào workspace.
  Kích hoạt ngay cả khi người dùng chỉ mô tả yêu cầu bằng lời (chưa có code).
  Cũng dùng khi người dùng hỏi "cái này nên để Lobster hay OpenProse xử lý",
  "giúp tôi viết file .lobster", "thiết kế agentic pipeline cho OpenClaw", hay
  bất kỳ câu hỏi nào liên quan đến approval gate, llm-task, resumeToken,
  /prose, sub-agent, hoặc workflow có nhiều bước trong OpenClaw.
---

# OpenClaw Workflow Architect

## Nguyên tắc phân tầng cốt lõi

Mọi quyết định thiết kế đều bắt đầu từ hai câu hỏi này:

> **"Bước này đang *nói chuyện với AI* để lý luận, hiểu ngữ cảnh, ra quyết định?"**
> → Đó là việc của **OpenProse**
>
> **"Bước này đang xác định *điều gì xảy ra sau khi AI đã quyết định*?"**
> → Đó là việc của **Lobster**

| Lobster làm tốt | OpenProse làm tốt |
|-----------------|-------------------|
| Chạy chuỗi CLI theo thứ tự xác định | Đọc kỹ năng, lý luận về ngữ cảnh |
| Cổng phê duyệt trước side effects | Tạo và điều phối nhiều tác nhân AI |
| Truyền JSON giữa các bước | Vòng lặp qua danh sách với AI xử lý |
| Resume với token sau khi approve | Chạy song song nhiều phiên AI |
| Kiểm tra schema, lưu file | Quản lý trạng thái giữa các phiên |

Đọc `references/layering-guide.md` để có bảng phân tích chi tiết và danh sách anti-patterns.

---

## Phần 1 — Nhận diện input

Xác định loại input trước khi làm bất cứ điều gì:

- **Mô tả bằng lời** (người dùng mô tả yêu cầu chưa có code) → đến Phần 2 (Phỏng vấn)
- **File có sẵn** (người dùng cung cấp `.lobster`, `.prose`, hoặc code Python/script) → đến Phần 3 (Phân tích)
- **Hỗn hợp** → chạy Phần 3 trước, sau đó Phần 2 với thông tin đã phân tích

---

## Phần 2 — Phỏng vấn thiết kế mới

Hỏi lần lượt các câu sau (chỉ hỏi những câu chưa rõ từ ngữ cảnh):

**Q1.** Quy trình có bao nhiêu bước chính? Bước nào cần con người phê duyệt trước khi tiếp tục?

**Q2.** Có bước nào cần chạy song song không? (ví dụ: xử lý nhiều bài học cùng lúc, nhiều tác nhân nghiên cứu độc lập)

**Q3.** Có vòng lặp qua danh sách không? (ví dụ: lặp qua từng bài học, từng file, từng khách hàng)

**Q4.** Với mỗi bước: đây là bước **AI lý luận** (cần hiểu ngữ cảnh, ra quyết định) hay bước **thực thi xác định** (lưu file, gọi CLI, kiểm tra schema)?

**Q5.** Model đang dùng là gì? Có phải một trong các Prose Complete systems không?
- Prose Complete: Claude Code + Opus, OpenCode + Opus, Amp + Opus
- Nếu không (ví dụ: Gemini 3 Flash Preview) → xem cảnh báo tương thích bên dưới

**Sau phỏng vấn:** Vẽ sơ đồ tầng dạng text, xác nhận với người dùng trước khi chọn mode và sinh file.

### Cảnh báo tương thích model

Nếu model **không phải** Prose Complete system:

```
⚠️  CẢNH BÁO TƯƠNG THÍCH
Model [tên model] chưa được xác nhận là Prose Complete system.
- File .lobster: hoạt động đầy đủ ✓
- File .prose: có thể không chạy đúng — OpenProse cần model đủ
  năng lực mô phỏng VM khi đọc spec.

Các lựa chọn:
  A. Lobster only — chạy được ngay, AI reasoning qua llm-task
  B. OpenProse only — tiếp tục nhưng cần test thực tế
  C. Auto (mixed) — sinh cả hai, bạn chọn dùng cái nào sau khi test
```

Chờ người dùng xác nhận mode trước khi tiếp tục.

---

## Phần 3 — Phân tích file có sẵn

Chạy checklist này với mỗi file được cung cấp:

### Checklist anti-patterns

- [ ] Có file Python/script làm cầu nối để đưa context vào LLM?
  → *Triệu chứng:* `prepare_prompt.py`, `build_context.py`, script đọc SKILL.md rồi nhét vào prompt
  → *Vấn đề:* Lobster đang làm việc của OpenProse
  → *Fix:* Chuyển sang OpenProse session — nó đọc skill file trực tiếp

- [ ] Có workaround cho vòng lặp (script Python riêng vì "Lobster không có for-loop")?
  → *Vấn đề:* Đang ở sai tầng
  → *Fix:* OpenProse có `for item in list:` native

- [ ] Có tự build logic spawn sub-agent thủ công (inject vào AGENTS.md, tự quản lý state)?
  → *Vấn đề:* Đang tái tạo thứ OpenProse đã có sẵn
  → *Fix:* OpenProse `parallel:` block + session isolation

- [ ] `approval: required` có đặt **trước** bước có side effect không?
  → *Nếu không:* lỗi thiết kế nghiêm trọng — side effect có thể chạy mà không có kiểm soát

- [ ] Dùng `tools.allow: ["lobster"]` thay vì `tools.alsoAllow`?
  → *Cảnh báo:* `allow` là allowlist thuần — có thể vô tình block các core tools khác
  → *Fix:* Dùng `alsoAllow` trừ khi chủ ý chạy restrictive mode

- [ ] Context của phiên chính bị phình to do sub-agent không có isolation?
  → *Fix:* Mỗi OpenProse sub-session có context riêng

**Đầu ra phân tích:** Trình bày báo cáo ngắn theo cấu trúc:
```
VẤN ĐỀ: [mô tả]
NGUYÊN NHÂN: [giải thích tại sao đây là anti-pattern]
ĐỀ XUẤT: [cách sửa cụ thể]
```

Xác nhận người dùng đồng ý với đề xuất trước khi sinh file mới.

---

## Phần 4 — Chọn mode sinh file

Sau phỏng vấn hoặc phân tích, hỏi người dùng chọn một trong ba mode:

### Mode A — Lobster only
**Khi nào phù hợp:**
- Model không phải Prose Complete
- Quy trình chủ yếu là thực thi xác định, ít AI orchestration phức tạp
- Cần chạy được ngay, không muốn phụ thuộc vào OpenProse runtime

**Cách sinh:**
- Một file `.lobster` chính làm orchestrator
- Các bước AI reasoning → dùng `llm-task` với schema rõ ràng
- Vòng lặp → Python/CLI script nhỏ emit JSON list, Lobster xử lý
- Multi-step → nhiều file `.lobster` gọi nhau có cấu trúc

### Mode B — OpenProse only
**Khi nào phù hợp:**
- Model là Prose Complete system
- Quy trình nặng về AI orchestration, multi-agent, parallel execution
- Không có side effects phức tạp cần approval gate Lobster

**Cách sinh:**
- Một file `.prose` chính
- Các bước thực thi đơn giản xử lý trực tiếp trong session
- Ghi chú `# COMPATIBILITY:` ở đầu file nếu model chưa được xác nhận

### Mode C — Auto (mixed)
**Khi nào phù hợp:**
- Quy trình phức tạp có cả AI orchestration lẫn side effects cần kiểm soát
- Muốn tận dụng điểm mạnh của cả hai

**Cách sinh (thứ tự bắt buộc):**
1. Sinh `.prose` làm tầng điều phối trước
2. Xác định các điểm gọi Lobster trong `.prose`
3. Sinh từng `.lobster` tương ứng sau
4. Sinh thêm `fallback-orchestrator.lobster` nếu model không phải Prose Complete

---

## Phần 5 — Sinh file vào workspace

### Cấu trúc thư mục chuẩn

```
workflows/
├── [tên-quy-trình].prose          # Mode B hoặc C
├── [tên-quy-trình].lobster        # Mode A hoặc C
├── gates/
│   └── [tên-gate].lobster         # Các cổng phê duyệt tái sử dụng
└── workers/
    └── [tên-worker].lobster       # Các worker con
```

### Quy trình sinh file

```
1. Kiểm tra thư mục workflows/ — tạo nếu chưa có
2. [Mode A] Sinh .lobster chính → sinh workers/ nếu cần
3. [Mode B] Sinh .prose → thêm ghi chú tương thích nếu cần
4. [Mode C] Sinh .prose → sinh .lobster được gọi bởi .prose → sinh workers/
5. Báo cáo danh sách file đã tạo
6. Hướng dẫn lệnh chạy cụ thể
```

### Template ghi chú tương thích (dùng cho Mode B/C với non-Prose Complete)

```yaml
# ============================================================
# COMPATIBILITY NOTE
# Model: [tên model] — chưa xác nhận là Prose Complete system
# .lobster files: hoạt động đầy đủ ✓
# .prose files: cần test thực tế — xem fallback-orchestrator.lobster
#               nếu .prose không chạy đúng
# Prose Complete systems: Claude Code + Opus, OpenCode + Opus, Amp + Opus
# ============================================================
```

### Checklist trước khi lưu file

- [ ] `approval: required` đặt trước mọi bước có side effect
- [ ] Dùng `alsoAllow` thay vì `allow`
- [ ] Có `timeoutMs` và `maxStdoutBytes` cho mọi Lobster call
- [ ] Mọi bước Lobster có `id` duy nhất
- [ ] File `.prose` có `requires:` và `ensures:` rõ ràng (Mode B/C)
- [ ] Worker files nhận đủ context cần thiết qua `args` hoặc `stdin`

---

## Tham chiếu nhanh

| Cần tra cứu | Đọc file |
|-------------|---------|
| Cú pháp đầy đủ `.lobster`, tham số runtime, approval flow | `references/lobster-spec.md` |
| Cú pháp `.prose`, state modes, slash commands | `references/openprose-spec.md` |
| Bảng phân tầng chi tiết, danh sách anti-patterns | `references/layering-guide.md` |
| Ví dụ hoàn chỉnh curriculum pipeline | `references/examples/` |
