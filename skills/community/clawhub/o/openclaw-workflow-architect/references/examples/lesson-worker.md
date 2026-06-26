# ============================================================
# VÍ DỤ: Worker sinh học liệu bài học — Mode A hoặc C
#
# Chạy bên trong mỗi tác nhân worker (được tạo bởi OpenProse parallel block)
# Hoặc chạy độc lập trong Mode A.
#
# Lý do dùng Lobster ở đây dù đã có OpenProse bên ngoài:
# Thứ tự sinh artifacts phải tuyệt đối xác định:
#   lesson_plan → slides_outline → exercises → teacher_guide
# Lobster đảm bảo điều này bằng stdin: $step.stdout
# ============================================================

name: lesson-materials
args:
  lesson_json:
    required: true
  output_dir:
    default: "projects/curriculum/lessons"

steps:
  # ── BƯỚC 1: Sinh giáo án ──────────────────────────────────
  - id: gen_lesson_plan
    command: >
      openclaw.invoke --tool llm-task --action json --args-json '{
        "prompt": "Sinh giáo án 5E (Engage, Explore, Explain, Elaborate, Evaluate) theo đặc tả bài học đầu vào. Trả về JSON đầy đủ.",
        "model": "gemini-3-flash-preview",
        "temperature": 0.4,
        "maxTokens": 6000,
        "schema": {
          "type": "object",
          "properties": {
            "lesson_id": { "type": "string" },
            "title": { "type": "string" },
            "objectives": { "type": "array", "items": { "type": "string" } },
            "phases": {
              "type": "object",
              "properties": {
                "engage": { "type": "string" },
                "explore": { "type": "string" },
                "explain": { "type": "string" },
                "elaborate": { "type": "string" },
                "evaluate": { "type": "string" }
              }
            },
            "duration_minutes": { "type": "number" }
          },
          "required": ["lesson_id", "title", "objectives", "phases"]
        }
      }'
    stdin: $lesson_json

  - id: validate_lesson_plan
    command: python tools/validator.py validate --schema schemas/lesson_plan.schema.json
    stdin: $gen_lesson_plan.stdout

  - id: save_lesson_plan
    command: >
      python tools/file_manager.py save_artifact
      --artifact lesson_plan
      --dir "${output_dir}"
    stdin: $validate_lesson_plan.stdout

  # ── BƯỚC 2: Sinh phác thảo slide (dựa trên giáo án) ──────
  - id: gen_slides_outline
    command: >
      openclaw.invoke --tool llm-task --action json --args-json '{
        "prompt": "Dựa trên giáo án, tạo phác thảo slide cho bài giảng. Trả về JSON.",
        "model": "gemini-3-flash-preview",
        "temperature": 0.3,
        "maxTokens": 4000,
        "schema": {
          "type": "object",
          "properties": {
            "slides": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "slide_number": { "type": "number" },
                  "title": { "type": "string" },
                  "content_points": { "type": "array", "items": { "type": "string" } },
                  "visual_suggestion": { "type": "string" }
                }
              }
            }
          },
          "required": ["slides"]
        }
      }'
    stdin: $save_lesson_plan.stdout

  - id: save_slides_outline
    command: >
      python tools/file_manager.py save_artifact
      --artifact slides_outline
      --dir "${output_dir}"
    stdin: $gen_slides_outline.stdout

  # ── BƯỚC 3: Sinh bài tập (dựa trên giáo án) ──────────────
  - id: gen_exercises
    command: >
      openclaw.invoke --tool llm-task --action json --args-json '{
        "prompt": "Tạo bộ bài tập đa dạng (trắc nghiệm, tự luận, thực hành) phù hợp với mục tiêu bài học. Trả về JSON.",
        "model": "gemini-3-flash-preview",
        "temperature": 0.5,
        "maxTokens": 5000,
        "schema": {
          "type": "object",
          "properties": {
            "exercises": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "type": { "type": "string", "enum": ["multiple_choice", "essay", "practical"] },
                  "question": { "type": "string" },
                  "answer_key": { "type": "string" },
                  "difficulty": { "type": "string", "enum": ["easy", "medium", "hard"] }
                }
              }
            }
          },
          "required": ["exercises"]
        }
      }'
    stdin: $save_slides_outline.stdout

  - id: save_exercises
    command: >
      python tools/file_manager.py save_artifact
      --artifact exercises
      --dir "${output_dir}"
    stdin: $gen_exercises.stdout

  # ── BƯỚC 4: Sinh hướng dẫn giáo viên (dựa trên tất cả) ──
  - id: gen_teacher_guide
    command: >
      openclaw.invoke --tool llm-task --action json --args-json '{
        "prompt": "Tổng hợp giáo án, slides và bài tập để tạo hướng dẫn giảng dạy chi tiết cho giáo viên. Bao gồm gợi ý xử lý tình huống khó và câu hỏi phổ biến của học sinh.",
        "model": "gemini-3-flash-preview",
        "temperature": 0.3,
        "maxTokens": 5000
      }'
    stdin: $save_exercises.stdout

  - id: save_teacher_guide
    command: >
      python tools/file_manager.py save_artifact
      --artifact teacher_guide
      --dir "${output_dir}"
    stdin: $gen_teacher_guide.stdout

  # ── BƯỚC 5: Đánh giá chất lượng ──────────────────────────
  - id: critique
    command: >
      openclaw.invoke --tool llm-task --action json --args-json '{
        "prompt": "Đánh giá toàn bộ học liệu theo tiêu chí sư phạm. Chấm điểm từng tiêu chí từ 0-100. Trả về JSON.",
        "model": "gemini-3-flash-preview",
        "temperature": 0.2,
        "maxTokens": 3000,
        "schema": {
          "type": "object",
          "properties": {
            "scores": {
              "type": "object",
              "properties": {
                "alignment_with_objectives": { "type": "number" },
                "pedagogical_quality": { "type": "number" },
                "content_accuracy": { "type": "number" },
                "exercise_diversity": { "type": "number" }
              }
            },
            "overall_score": { "type": "number" },
            "suggestions": { "type": "array", "items": { "type": "string" } }
          },
          "required": ["scores", "overall_score"]
        }
      }'
    stdin: $save_teacher_guide.stdout

  - id: check_threshold
    command: python tools/validator.py check_critique_threshold --min-score 75
    stdin: $critique.stdout

  - id: save_quality_report
    command: >
      python tools/file_manager.py save_artifact
      --artifact quality_report
      --dir "${output_dir}"
    stdin: $critique.stdout
    condition: $check_threshold.passed
