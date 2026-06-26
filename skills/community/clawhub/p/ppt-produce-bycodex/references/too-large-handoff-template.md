# Too-Large Handoff Template

Use this compact template after a 413/too-large hard stop. Keep it short. Do not embed images, base64, long prompts, large logs, or bulk source text.

```markdown
# PPT 生成 413 接力提示词

请继续 `{项目名称}` PPT PNG 制作任务。

项目路径：
`{项目根目录}`

当前任务：
`{当前任务一句话}`

触发接力原因：
`{413/Payload Too Large/response too large/CC Switch local proxy failed/...}`

已执行策略：
- 4K too-large 后已停止 4K 重试。
- 已尝试原生 2K high：`{是/否，次数}`
- 失败后已按规则停止，未继续压缩内容密度。

已成功产物：
- `{成功文件路径或无}`

失败/待处理页面：
- `{页名/页码/目标输出路径/失败原因}`

下一步建议：
1. 新会话先读取项目内最新接力提示词/方案 MD/PPT 大纲。
2. 不要重发大图或 base64。
3. 对失败页使用同内容密度的 2K high，必要时拆页。
4. 成功后生成接触表，确认后再阶段性询问是否生成 PPTX。
```
