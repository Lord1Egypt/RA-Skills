# ============================================================
# VÍ DỤ: Cổng phê duyệt tái sử dụng
# Dùng trong Mode A, B, hoặc C — gọi từ Lobster hoặc OpenProse
#
# Cách gọi từ OpenProse:
#   invoke lobster:
#     pipeline: workflows/gates/gate-approval.lobster
#     args: { gate: 1, file: constraints, label: "Ràng buộc" }
#     wait_for_approval: true
#
# Cách gọi từ Lobster khác:
#   openclaw.invoke --tool lobster --action run \
#     --pipeline workflows/gates/gate-approval.lobster \
#     --args-json '{"gate": 1, "file": "constraints.md", "label": "Ràng buộc"}'
# ============================================================

name: gate-approval
args:
  gate:
    required: true
  file:
    required: true
  label:
    default: "Nội dung"

steps:
  # Hiển thị checklist cho người dùng xem
  - id: show_label
    command: echo "=== CỔng PHÊ DUYỆT ${gate}: ${label} ==="

  # Hiển thị nội dung file cần review
  - id: show_content
    command: cat "${file}"

  # Hiển thị checklist tiêu chuẩn
  - id: show_checklist
    command: >
      echo "Checklist trước khi phê duyệt:
      [ ] Nội dung đầy đủ và chính xác?
      [ ] Không có thông tin thiếu hoặc mâu thuẫn?
      [ ] Sẵn sàng để tiếp tục giai đoạn tiếp theo?"

  # Cổng phê duyệt — dừng và chờ quyết định
  - id: human_gate
    command: echo "Cổng ${gate} (${label}) — Đang chờ phê duyệt từ người dùng..."
    stdin: $show_content.stdout
    approval: required

  # Đánh dấu đã được phê duyệt (chỉ chạy nếu approve)
  - id: mark_approved
    command: >
      python tools/progress_tracker.py mark_gate
      --gate "${gate}"
      --label "${label}"
      --status approved
    condition: $human_gate.approved

  # Ghi nhật ký
  - id: log_result
    command: >
      echo "Cổng ${gate} (${label}): $([ '$human_gate.approved' = 'true' ] && echo 'APPROVED' || echo 'REJECTED')"
    condition: $human_gate.approved
