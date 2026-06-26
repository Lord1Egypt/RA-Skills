# OpenProse — Đặc tả kỹ thuật

Nguồn: https://docs.openclaw.ai/prose | https://www.prose.md

---

## Tổng quan

OpenProse là định dạng quy trình đa nền tảng, ưu tiên markdown, dùng để điều phối các phiên AI có cấu trúc, nhiều tác nhân, với luồng kiểm soát tường minh.

Trong OpenClaw, nó được tích hợp dưới dạng plugin cài đặt bộ kỹ năng OpenProse và lệnh gạch chéo `/prose`.

### Triết lý cốt lõi

> "Mô hình ngôn ngữ là bộ mô phỏng. Khi được cung cấp mô tả hệ thống đủ chi tiết, chúng mô phỏng nó. Bản đặc tả OpenProse mô tả một máy ảo với đủ độ chính xác để bất kỳ hệ thống tương thích Prose nào trở thành máy ảo đó."

OpenProse không cần trình thông dịch riêng. Khi tác nhân đọc file spec, nó *trở thành* máy ảo đó.

### Yêu cầu: Prose Complete system

OpenProse yêu cầu model và môi trường đủ mạnh để mô phỏng VM:
- **Được hỗ trợ chính thức:** Claude Code + Opus, OpenCode + Opus, Amp + Opus
- **Chưa xác nhận:** Gemini 3 Flash Preview, các model khác — cần test thực tế

---

## Cú pháp file `.prose`

### Frontmatter

```yaml
---
name: tên-chương-trình
kind: program
services: [tên-tác-nhân-1, tên-tác-nhân-2]
---
```

### Khai báo hợp đồng

```yaml
requires:
  - tên-đầu-vào: mô tả đầu vào cần có

ensures:
  - tên-đầu-ra: mô tả đầu ra được đảm bảo

strategies:
  - when [điều kiện]: [hành động xử lý]
```

### Định nghĩa tác nhân

```yaml
agent tên-tác-nhân:
  model: sonnet          # hoặc opus, haiku, gemini-3-flash-preview, v.v.
  prompt: "Mô tả vai trò và phong cách của tác nhân này."
```

### Phiên làm việc (session)

```yaml
# Phiên đơn
session "Mô tả nhiệm vụ cần thực hiện."
  context: { biến-1, biến-2 }
  output: tên-đầu-ra
  skill: đường/dẫn/skill.md     # tùy chọn

# Phiên với tác nhân cụ thể
kết-quả = session: tên-tác-nhân
  prompt: "Nhiệm vụ cụ thể cho tác nhân này."
  context: { biến-liên-quan }
```

### Chạy song song

```yaml
parallel:
  kết-quả-1 = session: tác-nhân-a
    prompt: "Nhiệm vụ A."
    context: { dữ-liệu-đầu-vào }

  kết-quả-2 = session: tác-nhân-b
    prompt: "Nhiệm vụ B."
    context: { dữ-liệu-đầu-vào }
```

### Vòng lặp

```yaml
parallel:
  for mục in danh-sách:
    kết-quả_{mục.id} = session: tên-worker
      prompt: "Xử lý {mục.tên}."
      context: { mục, ngữ-cảnh-chung }
      tools_allow: ["lobster"]   # cho phép worker gọi Lobster
```

### Gọi Lobster từ OpenProse

```yaml
invoke lobster:
  pipeline: workflows/tên-pipeline.lobster
  args: { tham-so-1: giá-trị, tham-so-2: biến }
  wait_for_approval: true   # nếu pipeline có approval gate
```

### Nhập chương trình từ nơi khác

```yaml
use "handle/slug" as tên-cục-bộ
use "@handle/slug" as tên-cục-bộ   # @ được loại bỏ tự động
use "https://url/trực-tiếp.prose" as tên-cục-bộ
```

---

## Ví dụ đầy đủ

```yaml
---
name: research-synthesis
kind: program
services: [researcher, writer]
---

requires:
  - topic: câu hỏi nghiên cứu cần tìm hiểu

ensures:
  - report: tóm tắt sẵn sàng trình bày cho lãnh đạo

input topic: "Chủ đề cần nghiên cứu là gì?"

agent researcher:
  model: sonnet
  prompt: "Bạn nghiên cứu kỹ lưỡng và trích dẫn nguồn."

agent writer:
  model: opus
  prompt: "Bạn viết tóm tắt súc tích."

parallel:
  findings = session: researcher
    prompt: "Nghiên cứu về {topic}."
  draft = session: writer
    prompt: "Tóm tắt những điểm chính về {topic}."

session "Gộp findings và draft thành báo cáo cuối cùng."
  context: { findings, draft }
  output: report
```

---

## Lệnh gạch chéo `/prose`

| Lệnh | Tác dụng |
|------|---------|
| `/prose help` | Hướng dẫn sử dụng |
| `/prose run <file.prose>` | Chạy chương trình cục bộ |
| `/prose run handle/slug` | Tải từ kho trực tuyến và chạy |
| `/prose run https://...` | Tải từ URL và chạy |
| `/prose compile <file.prose>` | Kiểm tra cú pháp (không chạy) |
| `/prose examples` | Xem các ví dụ có sẵn |
| `/prose update` | Chuyển đổi file cũ sang format mới |

---

## Ánh xạ sang OpenClaw primitives

| Khái niệm OpenProse | Công cụ OpenClaw |
|--------------------|-----------------|
| Tạo phiên / Task tool | `sessions_spawn` |
| Đọc/ghi file | `read` / `write` |
| Tải từ web | `web_fetch` |

Nếu tool allowlist block các công cụ này, chương trình OpenProse sẽ thất bại.

---

## Quản lý trạng thái

Trạng thái được lưu trong `.prose/` trong workspace:

```
.prose/
├── .env
├── runs/
│   └── {YYYYMMDD}-{HHMMSS}-{random}/
│       ├── program.prose
│       ├── state.md
│       ├── bindings/
│       └── agents/
└── agents/
```

### Ba chế độ lưu trạng thái

| Chế độ | Khi nào dùng | Cấu hình |
|--------|-------------|---------|
| `filesystem` (mặc định) | Hầu hết các trường hợp | Không cần cấu hình thêm |
| `in-context` | Chương trình nhỏ, tạm thời | Khai báo trong frontmatter |
| `sqlite` / `postgres` | Quy trình sản xuất phức tạp | `OPENPROSE_STATE=sqlite` hoặc `OPENPROSE_POSTGRES_URL=...` |

> **Bảo mật PostgreSQL:** Thông tin xác thực hiển thị trong nhật ký tác nhân. Dùng cơ sở dữ liệu riêng với quyền hạn tối thiểu.

---

## Cài đặt và bật plugin

```bash
# Bật plugin
openclaw plugins enable open-prose

# Phiên bản thử nghiệm cục bộ
openclaw plugins install ./extensions/open-prose
```

Khởi động lại Gateway sau khi bật.

> **Lưu ý:** Chỉ có **một kỹ năng duy nhất** là `open-prose`. Không có `prose-run`, `prose-compile` tách biệt.
> ```
> Sai: npx playbooks add skill openclaw/skills --skill prose-run
> Đúng: npx playbooks add skill openclaw/skills --skill prose
> ```

---

## Bảo mật

Coi file `.prose` như mã lệnh. Xem xét kỹ trước khi chạy, đặc biệt với chương trình từ kho trực tuyến hoặc URL bên ngoài. Dùng tool allowlist để kiểm soát những gì tác nhân con có thể làm.
