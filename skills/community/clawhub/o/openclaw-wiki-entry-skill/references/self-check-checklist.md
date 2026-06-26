# 自检清单（阶段一）

## Step 9 之后必须为真

- [ ] Wiki 来源表新增了本篇来源行
- [ ] Wiki 演进记录新增了本次变更
- [ ] Wiki frontmatter `sources_count` 与来源表行数一致
- [ ] Wiki frontmatter `last_updated` 为今天
- [ ] 中转站文档写入 `graduated_to`
- [ ] 中转站文档状态更新为 `graduated` 或回到 `waiting`
- [ ] `_INDEX.md` 对应主题来源数完成同步

## Step 10 审计必须通过

- [ ] `wiki_entry_audit.sh` 返回 RESULT: PASS
- [ ] 没有 dangling wikilink
- [ ] 三件套数字一致（来源表 / sources_count / _INDEX）

## Step 12 收尾

- [ ] 更新 changelog.md
- [ ] 更新 context_today.md
- [ ] 更新今日日记
- [ ] 向 Gavin 汇报结果与剩余风险
