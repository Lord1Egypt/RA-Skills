# Profile 纠正处理 Prompt

## 任务

用户指出当前 `profile.md` 的某个结论不准确/过时。

你需要：
1) 明确指出要修正的具体句子或要点
2) 给出修正后的版本
3) 说明修正依据（用户纠正 / 新证据 / Wikipedia 更新 / 记忆库动态变化）

约束：
- 本仓库的本地修订（Adjustments）**存储在** `gurus/{slug}/meta.json` 的 `adjustments` 字段中，并在每次同步/生成 `profile.md` 时自动附加到 `## Adjustments`。
- 因此：不要直接手改 `profile.md` 的 Adjustments（会被覆盖/重建）。应当把纠正写入 `meta.json.adjustments`。
- 若无法确认：保留原结论但加“存在争议/尚未确认”的标注，并列出下一步需要的证据。

---

## 输出

1) 变更点列表（旧 → 新），说明改的是哪一层
2) 对 `gurus/{slug}/meta.json` 的补丁（只改 `adjustments` 字段）：
	- 把纠正写成可追溯的条目（建议包含日期与依据来源）
3) （可选）若需要重建文件：说明应执行 `python scripts/skill_writer.py --action guru-sync --slug {slug}` 以重新生成 `profile.md`
