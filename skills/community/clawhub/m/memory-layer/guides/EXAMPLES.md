# 使用示例

## 写入流程

```bash
# 1. Transcript（自动追加）
cat >> memory/transcripts/2026-04/2026-04-02.log << EOF
[TRANSCRIPT] 2026-04-02 18:52
[TYPE] monitor
[DATA] ETF1: 1.675, -4.23%
EOF

# 2. Topic（更新动态状态）
# 编辑 memory/topics/project-tool.md

# 3. Index（更新指针）
# 编辑 MEMORY.md
```

---

## 查询流程

```bash
# 1. 搜索 Index（始终加载）
grep "关键词" MEMORY.md

# 2. 加载 Topic（按需）
cat memory/topics/project-tool.md

# 3. 搜索 Transcripts（仅 grep）
grep -r "关键词" memory/transcripts/
```

---

*理解模式，自行实现。*

*最后更新：2026-04-03*
