---
name: humanize-zh-pro
version: 1.0.0
description: "中文去AI味 — 将AI生成的机械化文本转换为自然、有人情味的人类写作风格。支持5种平台风格（知乎/小红书/公众号/朋友圈/通用），内置AI味检测器和深度风格指南。比现有版本多了自动化脚本、多风格支持、批量处理和AI味评分。"
author: renyetu
homepage: https://github.com/renyetu/humanize-zh-pro
license: MIT
metadata:
  clawhub:
    emoji: "✍️"
    categories: ["Prompts", "Workflows"]
    tags: ["chinese", "writing", "humanize", "ai-detector"]
---

# 中文去AI味 Pro ✍️

将AI生成的机械化文本转换为自然、有人情味的人类写作风格。

**比 `humanize-zh` 强在哪？**
- ✅ 自动化脚本（不只是提示词）
- ✅ 5 种平台风格（不是单一通用）
- ✅ AI味检测评分（客观量化）
- ✅ 批量处理 + 深度风格指南

---

## 目录

- [快速开始](#快速开始)
- [5 种风格](#5-种风格)
- [AI味检测](#ai味检测)
- [批量处理](#批量处理)
- [深度指南](#深度指南)

---

## 快速开始

```bash
# 1. 先检测文本的AI味
./scripts/detect-ai-taste.sh my_article.txt

# 2. 对AI味重的文本去味
./scripts/humanize.sh -i my_article.txt -s zhihu -o ready.txt

# 3. AI 读取 ready.txt 中的提示词，执行去味

# 4. 再检测一次确认效果
./scripts/detect-ai-taste.sh ready.txt
```

---

## 5 种风格

| 风格 | 命令 | 适用平台 |
|------|------|----------|
| `zhihu` | `-s zhihu` | 知乎回答、专栏文章 |
| `xiaohongshu` | `-s xiaohongshu` | 小红书笔记 |
| `gongzhonghao` | `-s gongzhonghao` | 微信公众号 |
| `pengyouquan` | `-s pengyouquan` | 朋友圈、短文案 |
| `casual` | `-s casual` | 博客、私信、通用 |

每种风格都有完整的模板（语气、结构、用词、禁忌、开头/结尾模板），见 `scripts/templates/`。

---

## AI味检测

`detect-ai-taste.sh` 从 4 个维度评估：

**维度1: 结构模式 (0-50)**
- 序列化结构（首先/其次、第一/第二）
- AI总结语（综上所述、总而言之）
- AI万能开头（在当今、随着发展、众所周知）

**维度2: 语句多样性 (0-35)**
- 句子长度均匀性
- 标点多样性

**维度3: 人性化指标 (0-55)**
- 语气词使用
- 个人观点表达
- 情感强化词
- 个人经历引用
- emoji 使用

**维度4: 连接词模式 (0-30)**
- AI偏好连接词
- AI客套结尾

**评分:**
- 🔴 ≥60% — 重度AI味
- 🟡 30-59% — 中度AI味
- 🟢 <30% — 接近人类写作

---

## 批量处理

```bash
# 批量检测文件夹中所有txt文件
for f in drafts/*.txt; do
  echo "=== $f ==="
  ./scripts/detect-ai-taste.sh "$f"
done

# 批量去味（知乎风格）
for f in drafts/*.txt; do
  base=$(basename "$f" .txt)
  ./scripts/humanize.sh -i "$f" -s zhihu -o "ready/${base}_zhihu.txt"
done
```

---

## 深度指南

完整风格指南和去味方法论见 `references/style-guide.md`，包含：

- **去味金字塔** — 换词→破结构→注灵魂
- **7 个去味公式** — 拆序列、加冗余、插故事、露情绪...
- **平台差异速查** — 字数/emoji/语气/段落对照
- **AI词替换表** — 50+ 组对照

---

## 进阶用法

### 管道模式
```bash
cat ai_draft.txt | ./scripts/humanize.sh -s casual
```

### 仅评分（不生成去味提示词）
```bash
./scripts/humanize.sh -i article.txt --score
```

### 组合使用——先检测再选择风格
```bash
SCORE=$(./scripts/humanize.sh -i text.txt --score 2>/dev/null | grep 'AI味评分' | grep -o '[0-9]*')

if [ "$SCORE" -ge 70 ]; then
  ./scripts/humanize.sh -i text.txt -s casual -o humanized.txt
  echo "深度去味完成"
else
  ./scripts/humanize.sh -i text.txt -s zhihu -o humanized.txt
  echo "轻度润色完成"
fi
```

---

## 与现有 `humanize-zh` 对比

| 功能 | humanize-zh | humanize-zh-pro |
|------|:-----------:|:---------------:|
| 写作指导 | ✅ | ✅ |
| 自动化脚本 | ❌ | ✅ |
| AI味检测 | ❌ | ✅ 4维评分 |
| 多平台风格 | ❌ | ✅ 5种 |
| 批量处理 | ❌ | ✅ |
| 深度风格指南 | ❌ | ✅ |
| 管道模式 | ❌ | ✅ |
| 风格模板库 | ❌ | ✅ 5个完整模板 |

---

## 文件结构

```
humanize-zh-pro/
├── SKILL.md                          # 本文件
├── scripts/
│   ├── humanize.sh                   # 主脚本（去味）
│   ├── detect-ai-taste.sh            # AI味检测器
│   └── templates/
│       ├── zhihu.md                  # 知乎风格模板
│       ├── xiaohongshu.md            # 小红书风格模板
│       ├── gongzhonghao.md           # 公众号风格模板
│       ├── pengyouquan.md            # 朋友圈风格模板
│       └── casual.md                 # 通用口语模板
└── references/
    └── style-guide.md                # 深度风格指南
```

---

## 许可证

MIT — 随便用，署名就好。
