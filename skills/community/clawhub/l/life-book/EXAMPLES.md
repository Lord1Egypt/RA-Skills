# 生命之书 - 对话式使用示例

## 场景 1：自然对话中沉淀

**用户：** "我出生在1990年的北京，在胡同里长大。"

**AI 操作：**
```bash
~/.openclaw/workspace/skills/life-book/append.sh append default "出生与童年" \
  "我出生在1990年的北京，在胡同里长大。"
```

**AI 回复：** "在胡同里长大一定有很多有趣的回忆吧？你最难忘的一个童年玩伴是谁？"

---

**用户：** "有个叫小明的，我们经常一起爬树、捉迷藏。"

**AI 操作：**
```bash
~/.openclaw/workspace/skills/life-book/append.sh append default "出生与童年" \
  "有个叫小明的童年玩伴，我们经常一起爬树、捉迷藏。"
```

**AI 回复：** "听起来很快乐的童年时光 😊 后来你们还有联系吗？"

---

## 场景 2：主题切换

**用户：** "说到工作，我2015年开始创业，做AI方向。"

**AI 操作：**
```bash
~/.openclaw/workspace/skills/life-book/append.sh append default "职业生涯" \
  "2015年开始创业，做的是AI方向。"
```

**AI 回复：** "AI创业很有挑战性！是什么契机让你决定创业的？"

---

## 场景 3：用户主动查看进度

**用户：** "我写了多少字了？"

**AI 操作：**
```bash
~/.openclaw/workspace/skills/life-book/append.sh stats default
```

**AI 回复：** "你已经记录了 156 字！继续加油 📖"

---

## 场景 4：生成成书

**用户：** "生成生命之书"

**AI 操作：**
```bash
~/.openclaw/workspace/skills/life-book/life-book.sh generate default
```

**AI 回复：** 
"你的生命之书已生成完成！📖

包含章节：
- 出生与童年（45字）
- 职业生涯（32字）

文件位置：`~/.openclaw/workspace/life-books/default/book.md`

你可以继续补充内容，随时重新生成。"

---

## 场景 5：补充背景资料

**用户：** "我在清华大学读的计算机系。"

**AI 操作：**
1. 追加内容：
```bash
~/.openclaw/workspace/skills/life-book/append.sh append default "求学经历" \
  "在清华大学读的计算机系。"
```

2. 搜索背景资料（可选）：
```bash
# 使用 web_search 搜索清华大学计算机系历史
```

3. 追加背景资料：
```bash
~/.openclaw/workspace/skills/life-book/append.sh append default "求学经历" \
  "#### 背景资料\n\n清华大学计算机系成立于1958年..."
```

**AI 回复：** "清华计算机系很厉害！你在那里最大的收获是什么？"

---

## 章节映射规则

| 用户提到的内容 | 自动归类到 |
|--------------|-----------|
| 出生、童年、小时候、父母、家乡 | 出生与童年.md |
| 上学、小学、中学、大学、老师、同学 | 求学经历.md |
| 工作、职业、公司、创业、项目 | 职业生涯.md |
| 朋友、恋爱、婚姻、家人、孩子 | 重要关系.md |
| 转折、改变、决定、危机、机遇 | 人生转折.md |
| 现在、未来、梦想、计划 | 当下与展望.md |

---

## AI 引导原则

1. **随时沉淀**：用户说的每句话都可能是素材，立即记录
2. **自然追问**：每次记录后，追问一个细节，让对话继续
3. **不打断**：不要频繁提醒"已记录"，保持对话流畅
4. **智能分类**：根据内容自动判断章节，无需用户指定
5. **定期总结**：每积累一定内容后，生成叙事性小结

---

## 文件结构

```
~/.openclaw/workspace/life-books/
└── default/
    ├── chapters/
    │   ├── 出生与童年.md
    │   ├── 求学经历.md
    │   ├── 职业生涯.md
    │   ├── 重要关系.md
    │   ├── 人生转折.md
    │   └── 当下与展望.md
    ├── materials/          # 照片、文档等
    ├── raw/               # 原始对话记录
    ├── metadata.json      # 元数据
    └── book.md            # 最终成书
```

---

## 隐私保护

- 所有数据存储在本地
- 用户可标记 `[私密]` 内容
- 生成成书时可选择过滤敏感信息
