# 演示结构模板（Presentation Structure Template）

> 复制本模板搭建一页一主张的演示大纲。分页用 `---`，每页首行是 `#` 标题。配合 [scripts/check_presentation.py](../scripts/check_presentation.py) 校验（每页 ≤120 字、标题层级统一、不重复）。

```markdown
# 开场：钩子（反直觉/痛点/故事）
一句话抓住注意力 + 一个数据点。

---

# 路线图
今天讲什么、不讲什么。

---

# 主体一：核心主张
- 要点一（≤20 字）
- 要点二（≤20 字）

---

# 主体二：证据与案例
- 数据/截图/ Demo 一句话结论

---

# 总结与行动号召
复述 3 个要点 + 具体下一步。
```

## 自检

```bash
python3 scripts/check_presentation.py outline --file deck.md
```

## 检查清单

- [ ] 第 1 页是钩子（非自我介绍）
- [ ] 每页一个标题，层级统一为 `#`
- [ ] 每页 ≤120 字，要点化
- [ ] 无重复标题
- [ ] 结尾有具体 CTA
