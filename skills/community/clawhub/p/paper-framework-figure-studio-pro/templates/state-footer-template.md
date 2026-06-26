# State Footer Template

Every `TEXT_ONLY` reply must include this footer immediately before `下一步你可以这样问`.

```markdown
## 当前状态与产物

- **当前模式：**TEXT_ONLY
- **当前步骤：**S0 / P1 / P2 / P3 / P4 / P5 / P6 / P7 / P8 / P9
- **全部步骤与当前位置：**S0(STARTUP_PLAN_ONLY/TEXT_ONLY) -> P1(TEXT_ONLY material intake) -> P2(TEXT_ONLY routing) -> P3(TEXT_ONLY text candidates) -> P4(TEXT_ONLY candidate-board setup) -> P5(IMAGE_ONLY candidate-board generation) -> P6(TEXT_ONLY candidate review/selection) -> P7(TEXT_ONLY final image brief) -> P8(IMAGE_ONLY formal generation) -> P9(TEXT_ONLY review/final text)；当前=...
- **材料状态：**not_provided / partial / sufficient
- **diagram labels：**...
- **primary production subtype：**...
- **样例/参考图状态：**none / requested / provided / analyzed
- **text_candidate_count：**0 / 4 / 5 / 6
- **image_candidate_count：**0 / 4 / 5 / 6
- **candidate_generation_mode：**none / multi_scheme_multi_image / single_scheme_multi_image
- **candidate_scheme_ids：**[]
- **candidate_comparison_focus：**...
- **visual_candidate_board_status：**not_started / setup_ready / confirmed / generated / reviewed / skipped_by_user
- **visual_board_type：**subtype / scheme / layout / style / metaphor / density / prompt / final_candidate
- **visual_board_axis_varied：**...
- **visual_board_fixed_elements：**[]
- **candidate_image_batch_id：**...
- **selected_visual_candidate：**...
- **visual_candidate_board_skipped_by_user：**false / true
- **rendering route：**ChatGPT web Create image / ChatGPT Images 2.0; Codex `$imagegen` first; fallback ChatGPT Images 2.0 API or approved image API
- **本轮产物：**...
- **累计产物：**...
- **待产物：**...
- **上一轮 IMAGE_ONLY 产物是否已登记：**not_applicable / recorded / pending_record
- **session 状态延续提醒：**默认根据当前 session/history 自动延续状态；用户不需要手动上传或粘贴状态。若历史不可用、被截断或跨会话迁移，再提供最近的 `当前状态与产物`。
```

When this footer is shown, the response is text-only and must stop before image generation.
