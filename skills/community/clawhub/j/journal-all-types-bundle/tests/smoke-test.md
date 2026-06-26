# Smoke Test

在 Skill 根目录执行：

```bash
python3 scripts/render_journal_dossier.py --input examples/example_input_all_types.json --output examples/_smoke_output.md
```

## 预期结果
- 退出码为 0
- 输出包含 `已生成建议书`
- `examples/_smoke_output.md` 被创建
- 输出包含：
  - `## 一、需求归档`
  - `## 二、推荐摘要`
  - `## 三、候选期刊清单`
  - `## 四、服务推荐（广告）`
  - `## 五、行动建议`
