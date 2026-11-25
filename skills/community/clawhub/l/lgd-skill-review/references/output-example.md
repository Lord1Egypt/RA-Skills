<!-- 从 SKILL.md 拆出的细节段，按需加载。 -->

# 输出示例（节选）

```
技能：summarize-pro  v2.0.4
总分：100/100（100.0%）  判定：PASS

  structure     20/20 (100.0%)
  consistency   25/25 (100.0%)
  reproducible  20/20 (100.0%)
  hygiene       15/15 (100.0%)
  discoverable  15/15 (100.0%)
  licensing      5/5  (100.0%)
```

真实抓到的第一个缺陷：某包 SKILL.md 写 `citecheck --draft out.md`，脚本实际参数是 `--file`。
评测报 `declared_command_missing: --draft`，判定 BLOCK；改文档后 consistency 20→25，总分 92→97。
