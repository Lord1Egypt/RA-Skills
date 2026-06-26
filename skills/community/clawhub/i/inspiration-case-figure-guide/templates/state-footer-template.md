# State Footer Template

Use this in every `TEXT_ONLY` reply under `当前状态与产物`.

```markdown
当前状态与产物

- active_skill: inspiration-case-figure-guide v3.0.0
- response_mode: TEXT_ONLY
- current_step: <S0/P1/P2/P3/P4/P6/P7/P9>
- target_paper_material_status: <missing/partial/ready>
- target_slot: <intro/method_lead_in/analysis/limitation/rebuttal/slides>
- paper_thesis: <known/unknown>
- figure_thesis: <known/unknown>
- inspiration_source: <case/observation/failure/contrast/scenario/taxonomy/mechanism/unknown>
- subtype_labels: []
- primary_production_subtype: <not_locked/problem_teaser/...>
- reader_effect_contract: <one sentence>
- evidence_anchors: []
- exact_labels_allowed: []
- invented_content_forbidden: true
- sample_reference_image_status: <none/offered/provided/attribute_map_recorded>
- text_candidate_count: <0/4/5/6>
- candidate_scheme_ids: []
- visual_candidate_board_status: not_started | setup_ready | confirmed | generated | reviewed | skipped_by_user
- visual_board_type: <subtype/scheme/layout/style/metaphor/density/prompt/final_candidate>
- visual_board_axis_varied: ""
- visual_board_fixed_elements: []
- visual_board_candidate_count: 6
- candidate_image_batch_id: ""
- selected_visual_candidate: null
- final_image_brief_status: <not_started/drafted/approved>
- rendering_route: "ChatGPT web Create image / Codex $imagegen first"
- previous_IMAGE_ONLY_batch_recorded: <yes/no/not_applicable>
- current_turn_outputs: []
- cumulative_outputs: []
- pending_outputs: []

全部步骤与当前位置

| Step | Mode | Status |
|---|---|---|
| S0 | STARTUP_PLAN_ONLY (TEXT_ONLY) | <done/current/pending> |
| P1 | TEXT_ONLY | <done/current/pending> |
| P2 | TEXT_ONLY | <done/current/pending> |
| P3 | TEXT_ONLY | <done/current/pending> |
| P4 | TEXT_ONLY | <done/current/pending> |
| P5 | IMAGE_ONLY | <done/current/pending> |
| P6 | TEXT_ONLY | <done/current/pending> |
| P7 | TEXT_ONLY | <done/current/pending> |
| P8 | IMAGE_ONLY | <done/current/pending> |
| P9 | TEXT_ONLY | <done/current/pending> |
```
