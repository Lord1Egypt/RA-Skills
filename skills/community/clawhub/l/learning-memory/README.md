<div align="center">

# 🧠 learning-memory

### Bộ khung tự tiến hóa bộ não dài hạn & tự đóng gói kỹ năng cho OpenClaw Agent

*Autonomous Long-Term Memory Evolution & Self-Synthesizing Skill Framework for OpenClaw*

<p align="center">
  <a href="https://clawhub.io/skills/learning-memory">
    <img src="https://img.shields.io/badge/ClawHub-learning--memory-orange.svg" alt="ClawHub">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License">
  </a>
  <a href="https://github.com/openclaw/openclaw">
    <img src="https://img.shields.io/badge/OpenClaw-2026.6+-purple.svg" alt="OpenClaw">
  </a>
</p>

</div>

---

<details open>
<summary><img src="https://flagcdn.com/20x15/vn.png" alt="VN"> <b>Tiếng Việt</b></summary>

## 🎁 Giới thiệu
Mặc dù OpenClaw rất mạnh mẽ nhờ khả năng tích hợp đa kênh (Zalo, Telegram, Browser, Workboard), các Agent mặc định thường gặp tình trạng "mau quên" sau một khoảng thời gian do cơ chế nén ngữ cảnh tự động (context compaction). 

`learning-memory` giải quyết triệt để vấn đề này bằng cách thiết lập một **vòng lặp học hỏi khép kín (closed-loop self-improvement)**:
1. **Chủ động ghi nhớ dài hạn:** Ép bot tự động ghi lại các bài học, sở thích hoặc quy tắc mới trực tiếp vào [MEMORY.md](MEMORY.md) theo thời gian thực.
2. **Tự động đóng gói Kỹ năng:** Hướng dẫn bot tự động kết hợp các chuỗi thao tác phức tạp thành script riêng trong thư mục `skills/` và cập nhật lệnh gọi vào [TOOLS.md](TOOLS.md).
3. **Phản tư cuối phiên làm việc (Self-Reflection):** Bot tự rà soát và dọn dẹp bộ nhớ trước khi kết thúc phiên.

---

## 🧭 Bảng so sánh tính năng

| Tính năng | Agent Mặc định | **Agent cài đặt learning-memory** |
|---|:---:|:---:|
| **Ghi nhớ bài học** | Quên sau khi compaction | ✅ **Lưu trữ vĩnh viễn** vào `MEMORY.md` ngay lập tức |
| **Học thói quen của User** | Phải nhắc đi nhắc lại | ✅ **Nhớ ngay** sau khi User thiết lập quy tắc |
| **Tự động hóa tác vụ mới** | Phải viết code chạy lại từ đầu | ✅ **Tự viết script helper**, lưu vào `skills/` & cập nhật `TOOLS.md` |
| **Vòng lặp tự cải tiến** | Chỉ phản ứng theo lệnh | ✅ **Tự phản tư cuối mỗi phiên làm việc** |

---

## 🚀 Cách cài đặt & Sử dụng

Chạy script cài đặt để tự động quét `openclaw.json` và cập nhật quy tắc tự tiến hóa vào toàn bộ các Agent đang chạy trong hệ thống của bạn:

```bash
node install.js
```

Để khôi phục trạng thái ban đầu của các file `AGENTS.md` (gỡ bỏ patch tự học):
```bash
node install.js --restore
```

---

## 💡 Hướng dẫn Prompt để kích hoạt tính năng tự động

Để bot kích hoạt đúng cơ chế tự học và tự đóng gói kỹ năng, bạn chỉ cần giao tiếp bình thường theo các cấu trúc gợi ý dưới đây:

### 1. Kích hoạt Tự ghi nhớ dài hạn (MEMORY.md)
Khi bạn muốn dạy bot một thói quen, sở thích, hoặc cách xử lý lỗi hệ thống mà bạn muốn nó nhớ mãi mãi.
* **Gợi ý Prompt:**
  * *"Từ nay trở đi khi tôi yêu cầu tạo báo cáo Excel, hãy luôn sử dụng font chữ 'Lexend' và đặt tên theo định dạng Bao-Cao-Kent-[NgayThangNam].xlsx"*
  * *"Hãy nhớ rằng IP máy chủ sao lưu là 192.168.1.100, mỗi khi gặp lỗi kết nối hãy thử IP này."*
  * *"Hãy lưu ý quy tắc bảo mật của nhóm: không bao giờ gửi file danh sách thành viên thật lên group chat."*

### 2. Kích hoạt Tự đóng gói Kỹ năng (skills/ & TOOLS.md)
Khi bạn có một tác vụ lặp đi lặp lại hoặc phức tạp gồm nhiều bước (cào dữ liệu, xử lý Excel, tổng hợp báo cáo định kỳ) và muốn bot tự tạo công cụ cho chính nó sử dụng sau này.
* **Gợi ý Prompt:**
  * *"Tôi thường xuyên nhận được các file Excel thành viên. Hãy giúp tôi đọc file hiện tại, lọc ra danh sách thành viên có SĐT đầu 09 và xuất ra file thanh-vien-09.txt. Hãy tự động đóng gói quy trình này thành một script để các lần sau tôi chỉ cần gọi 1 lệnh là xử lý được ngay cho bất kỳ file excel nào."*
  * *"Hãy viết script cào giá vàng thế giới hàng ngày từ API, định dạng kết quả và lưu vào gold.md. Hãy lưu nó thành một skill hệ thống để sau này chạy lại dễ dàng."*

---

## 📂 Cấu trúc thư mục skill
```text
openclaw-skill-super-memory/
├── .agent/
│   └── workflows/
│       └── update.md       # Tài liệu hướng dẫn cập nhật phiên bản
├── scripts/
│   └── publish.js          # Script tự động tag Git & publish lên ClawHub
├── install.js              # Script tự động cập nhật quy tắc vào AGENTS.md các workspace
├── SKILL.md                # Hệ thống quy tắc nạp vào Agent (System Prompt)
├── README.md               # Hướng dẫn sử dụng
└── package.json            # Metadata của Skill & phiên bản
```

---

## 🦞 Hệ sinh thái OpenClaw (cùng tác giả)
Các repository hữu ích khác để bạn xây dựng một AI Agent tự vận hành hoàn chỉnh:

* **🚀 Cài đặt & Hạ tầng:**
  * [openclaw-setup](https://github.com/tuanminhhole/openclaw-setup) — Setup AI bot miễn phí bằng OpenClaw + Google Gemini (Telegram/Docker)
* **🔌 Plugin (runtime):**
  * [openclaw-zalo-mod](https://github.com/tuanminhhole/openclaw-zalo-mod) — Quản lý nhóm Zalo zero-token (slash command, anti-spam, warn, memory)
  * [openclaw-browser-automation](https://github.com/tuanminhhole/openclaw-browser-automation) — Tự động hóa trình duyệt qua giao thức CDP
  * [openclaw-facebook-crawler](https://github.com/tuanminhhole/openclaw-facebook-crawler) — Trích xuất dữ liệu bài viết Facebook
* **🧩 Skill nâng cao:**
  * [openclaw-skill-infographic](https://github.com/tuanminhhole/openclaw-skill-infographic) — Tạo ảnh infographic, poster tự động
  * [openclaw-skill-zalo-sticker-mention](https://github.com/tuanminhhole/openclaw-skill-zalo-sticker-mention) — Gửi sticker và tự động tag tên thành viên Zalo

---

<div align="center">
<sub>🧠 <b>learning-memory</b> · một phần của hệ sinh thái <a href="https://github.com/tuanminhhole">tuanminhhole (Kent)</a> · MIT License</sub>
</div>

</details>

<details>
<summary><img src="https://flagcdn.com/20x15/us.png" alt="US"> <b>English</b></summary>

## 🎁 Overview
While OpenClaw is highly versatile across channels (Zalo, Telegram, Browser, Workboard), default agents often suffer from "context amnesia" over time due to automatic context compaction limits.

`learning-memory` resolves this by introducing a **closed-loop self-improvement cycle**:
1. **Durable Memory Auto-Synthesis:** Directs the agent to proactively record new guidelines, user preferences, or bug fixes directly into [MEMORY.md](MEMORY.md) in real-time.
2. **Autonomous Skill Synthesis:** Instructs the agent to bundle complex, multi-step workflows into standalone script files under the `skills/` folder and index them in [TOOLS.md](TOOLS.md) for future execution.
3. **Self-Reflection Loop:** Prompt the agent to run a self-review loop at the end of each major session to clean up outdated memories and optimize its knowledge.

---

## 🧭 Feature Comparison

| Feature | Default Agent | **Agent with learning-memory** |
|---|:---:|:---:|
| **Memory Retention** | Forgotten after compaction | ✅ **Durable storage** in `MEMORY.md` instantly |
| **User Preference Adaptation** | Requires constant reminding | ✅ **Learned immediately** after setting rules |
| **New Task Automation** | Requires rewriting code | ✅ **Self-packages script helpers** to `skills/` & registers in `TOOLS.md` |
| **Self-Improvement Loop** | Reactive execution only | ✅ **Self-reflects at the end of every session** |

---

## 🚀 Installation & Usage

Run the installer to scan `openclaw.json` and patch the autonomous rules into all active agent workspaces:

```bash
node install.js
```

To revert agent instructions back to their original state:
```bash
node install.js --restore
```

---

## 💡 How to Prompt to Trigger Autonomous Behavior

To trigger the memory update and skill packaging routines, communicate with your bot using the following prompt structures:

### 1. Triggering Long-Term Memory (MEMORY.md)
Use this when you want the agent to remember a specific rule, layout format, or system workaround permanently.
* **Prompt Examples:**
  * *"From now on, whenever I ask you to generate Excel reports, always use the 'Lexend' font and format the filename as Bao-Cao-Kent-[DDMMYYYY].xlsx"*
  * *"Remember that the backup server IP is 192.168.1.100. Try this IP whenever connection errors occur."*
  * *"Keep in mind our security guideline: never send real member lists directly to the group chat."*

### 2. Triggering Autonomous Skill Packaging (skills/ & TOOLS.md)
Use this when you perform a manual, repetitive, or complex task (such as data scraping, batch file formatting, or automated reports) and want the agent to build an automated tool for itself to reuse later.
* **Prompt Examples:**
  * *"I regularly receive member Excel sheets. Please read the current one, filter members whose phone numbers start with '09', count them, and save the report as thanh-vien-09.txt. Automate this process into a reusable script so I can run it with a single command for future files."*
  * *"Write a script to fetch daily exchange rates from the API, format the result, and save it to rates.md. Package this as a system skill for future ease of use."*

---

## 📂 Directory Structure
```text
openclaw-skill-super-memory/
├── .agent/
│   └── workflows/
│       └── update.md       # Release workflow instructions
├── scripts/
│   └── publish.js          # Auto commit, tag, and publish to ClawHub
├── install.js              # Multi-agent workspace prompt patcher
├── SKILL.md                # System prompt instructions
├── README.md               # User guide
└── package.json            # Skill manifest & versioning
```

---

## 🦞 OpenClaw Ecosystem (by the same author)
Complementary tools to build a fully autonomous AI Agent setup:

* **🚀 Installation & Infrastructure:**
  * [openclaw-setup](https://github.com/tuanminhhole/openclaw-setup) — Run a free AI Agent with OpenClaw & Google Gemini (Telegram/Docker)
* **🔌 Plugins (runtime):**
  * [openclaw-zalo-mod](https://github.com/tuanminhhole/openclaw-zalo-mod) — Zero-token Zalo group administration (slash commands, anti-spam, warn)
  * [openclaw-browser-automation](https://github.com/tuanminhhole/openclaw-browser-automation) — Control Chrome via Chrome DevTools Protocol (CDP)
  * [openclaw-facebook-crawler](https://github.com/tuanminhhole/openclaw-facebook-crawler) — Scraping Facebook post contents
* **🧩 Advanced Skills:**
  * [openclaw-skill-infographic](https://github.com/tuanminhhole/openclaw-skill-infographic) — Create beautiful infographics and posters
  * [openclaw-skill-zalo-sticker-mention](https://github.com/tuanminhhole/openclaw-skill-zalo-sticker-mention) — Send stickers and auto-mention members on Zalo

---

<div align="center">
<sub>🧠 <b>learning-memory</b> · part of the <a href="https://github.com/tuanminhhole">tuanminhhole (Kent)</a> ecosystem · MIT License</sub>
</div>

</details>
