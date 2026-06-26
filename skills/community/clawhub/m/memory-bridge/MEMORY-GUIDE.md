# 🤍 memory-bridge 使用指南

> **新会话重启后，AI 还知道上次在聊什么。**
> 
> 装一次，记忆永远在。不会因为重启窗口就全忘了。

---

## 核心设计

**不是"启动时读一堆文件"，而是"一个索引就够了"。**

```
新会话 → 只读 MEMORY.md（5-10 行）→ AI 知道你是谁、在做什么
                                    → 需要时才读详细文件
```

这样：
- 初始 token 极小（5-10 行）
- 日记、任务卡、教训都不影响启动速度
- AI 还是能记住一切，只是"按需读取"

---

## 装好就不用管了

```
clawhub install memory-bridge
```

装完后，AI 下次唤醒会自动帮你初始化。

## 文件在哪？

```
~/.openclaw/workspace/
├── MEMORY.md                ← 索引（新会话唯一自动加载的，5-10 行）
├── USER.md                  ← 用户档案（按需读取）
├── memory/
│   ├── current-handoff.md   ← 任务卡（按需读取）
│   ├── entities.md          ← 人物/项目（按需读取）
│   ├── SESSION-STATE.md     ← 临时日志
│   └── working-buffer.md    ← 上下文缓冲
└── .learnings/
    ├── LEARNINGS.md         ← 教训（按需读取）
    ├── ERRORS.md            ← 错误（按需读取）
    └── FEATURE_REQUESTS.md  ← 功能需求
```

你可以手动编辑这些文件，AI 下次醒来会读取你改过的内容。

---

## 常见问题

**Q：新会话会读很多文件吗？**
A：不会。只读 MEMORY.md（5-10 行索引），其他文件需要时才读。

**Q：reset 后真的还记得吗？**
A：真的！试一下：装好后开新窗口，问"我们上次在聊什么？"

**Q：记忆会越来越长吗？**
A：MEMORY.md 保持在 10 行以内。详细内容在其他文件，不影响初始 token。

**Q：我可以清空记忆吗？**
A：可以。删除 `MEMORY.md`、`memory/`、`.learnings/` 这些目录即可。

**Q：会覆盖我已有的 SOUL.md 吗？**
A：绝对不会。这个 skill 只建记忆文件，你已有的人设和规则完全不动。
