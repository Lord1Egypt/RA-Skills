# ============================================================
# VÍ DỤ: Curriculum Pipeline — Mode C (Auto/Mixed)
# OpenProse làm tầng điều phối, Lobster làm tầng thực thi
#
# COMPATIBILITY NOTE
# Yêu cầu Prose Complete system để chạy đầy đủ.
# Prose Complete: Claude Code + Opus, OpenCode + Opus, Amp + Opus
# Nếu dùng model khác (ví dụ: gemini-3-flash-preview):
#   → Xem fallback-orchestrator.lobster
# ============================================================

---
name: curriculum-pipeline
kind: program
---

requires:
  - project: tên dự án cần tạo chương trình học

ensures:
  - full_curriculum: bộ học liệu hoàn chỉnh đã qua phê duyệt của người dùng

strategies:
  - when requirements are ambiguous: ask clarifying questions before proceeding
  - when a gate is rejected: stop and ask user what to adjust

# ──────────────────────────────────────────────────────────────
# GIAI ĐOẠN 1–3: Công việc phiên AI — OpenProse xử lý
# ──────────────────────────────────────────────────────────────

session "Thu thập yêu cầu từ người dùng qua kỹ năng phỏng vấn."
  skill: skills/phase-1/skill-interview
  output: requirements

session "Nghiên cứu bối cảnh công nghệ và xã hội liên quan."
  skill: skills/phase-1/skill-research-synthesis
  context: { requirements }
  output: research_notes

session "Ánh xạ yêu cầu thành ràng buộc SMART."
  skill: skills/phase-3-5/skill-constraint-mapping
  context: { requirements, research_notes }
  output: constraints

# Cổng 1: Phê duyệt có tác dụng phụ — Lobster xử lý
invoke lobster:
  pipeline: workflows/gates/gate-approval.lobster
  args: { gate: 1, file: constraints, label: "Ràng buộc & Yêu cầu" }
  wait_for_approval: true

# ──────────────────────────────────────────────────────────────
# GIAI ĐOẠN 4–5: Tiếp tục thiết kế
# ──────────────────────────────────────────────────────────────

session "Thiết kế sản phẩm học tập."
  skill: skills/phase-4/skill-product-design
  context: { constraints }
  output: product_map

session "Xây dựng khung đơn vị học tập."
  skill: skills/phase-3-5/skill-unit-framework
  context: { constraints, product_map }
  output: unit_framework

# Cổng 2
invoke lobster:
  pipeline: workflows/gates/gate-approval.lobster
  args: { gate: 2, file: unit_framework, label: "Khung Đơn Vị Học Tập" }
  wait_for_approval: true

# ──────────────────────────────────────────────────────────────
# GIAI ĐOẠN 6–7: Phân rã thành bài học
# ──────────────────────────────────────────────────────────────

session "Phân rã thành đặc tả bài học chi tiết."
  skill: skills/phase-7/skill-lesson-spec
  context: { unit_framework, constraints }
  output: lesson_specs

# Cổng 3
invoke lobster:
  pipeline: workflows/gates/gate-approval.lobster
  args: { gate: 3, file: lesson_specs, label: "Đặc Tả Bài Học" }
  wait_for_approval: true

# ──────────────────────────────────────────────────────────────
# GIAI ĐOẠN 8: Sinh học liệu song song — OpenProse native
# ──────────────────────────────────────────────────────────────

parallel:
  for lesson in lesson_specs:
    materials_{lesson.id} = session: lesson_worker
      prompt: "Sinh đầy đủ học liệu cho bài học: {lesson.title}."
      context: { lesson, constraints, unit_framework }
      tools_allow: ["lobster"]   # Worker được phép gọi Lobster để lưu file xác định
