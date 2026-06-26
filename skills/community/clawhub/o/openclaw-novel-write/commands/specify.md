# /novel specify - 定义故事规格

## 触发方式

```
/novel specify [故事概要]
```

或对话式：
```
定义故事规格
创建故事规格文档
```

---

## 目标

将模糊的故事想法转化为具体的故事规格文档。**AI 自动分析用户描述并加载对应知识库，用户确认后可修改。**

---

## 执行步骤

### 1. 收集故事信息（描述型）

通过对话收集信息，**鼓励用户自由描述**：

```
请描述您想写的小说：
- 什么题材？（都市、古代、玄幻、悬疑...）
- 什么类型？（甜宠、虐文、爽文、复仇...）
- 主角是谁？有什么特点？
- 核心冲突是什么？
- 有哪些特别想要的情节或元素？

您可以随意描述，我来帮您整理和分析。
```

---

### 2. 🎯 AI 自动分析 + 确认

**AI 根据用户描述自动判断类型、加载知识库，然后等待用户确认。**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 故事分析结果

根据您的描述，我初步判断：

📖 题材类型：都市言情 × 豪门
🎭 故事风格：甜宠 / 爽文
👤 主角定位：普通人逆袭
🌟 金手指类型：隐藏身份 / 能力

📚 已加载的知识库：
   ✓ genres/romance.md（言情知识）
   ✓ styles/web-novel.md（网文风格）
   ✓ requirements/romance-sweet.md（甜文规范）
   ✓ requirements/anti-ai-v4.md（反AI规范）

📋 已识别的必备元素：
   - 身份差（豪门×普通人）✓
   - 先婚后爱 ✓
   - 甜宠互动 ✓
   - 打脸绿茶 ✓

⚠️ 请确认或修改以上分析
━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### 3. 用户确认或修改

用户可以：
- **直接确认**：回复 "OK" 或 "确认"
- **修改某项**：如 "把豪门改成普通都市"
- **补充信息**：继续描述更多想法

**如果用户修改**，AI 重新分析并展示结果，直到用户确认。

---

### 4. 生成规格文档

用户确认后，输出到 `stories/<story-name>/specification.md`

```markdown
---
title: [暂定标题]
type: [题材类型]
genre: [子类型]
target-audience: [目标读者]
estimated-words: [预估字数]
chapters: [预估章节数]
writing-style: [预设风格]
writing-requirements:
  - anti-ai-v4
  - [其他规范]
knowledge-base:
  - genres/[类型].md
---

# [故事名称] - 故事规格

## 1. 类型定位

[详细说明题材和类型]

## 2. 核心冲突

[主要矛盾是什么]

## 3. 主角设定

### [主角名]
- **身份**：背景、职业、社会地位
- **性格**：核心性格特征
- **欲望**：想要什么
- **恐惧**：害怕什么
- **金手指/特殊能力**：（如有）

## 4. 配角概览

[主要配角及他们的角色定位]

## 5. 世界观设定

[故事发生的背景环境]

## 6. 情感基调

[整体情感倾向：甜/虐/爽等]

## 7. 目标读者

[读者画像]

## 8. 内容红线

[禁止出现的内容]

## 9. 必备元素

[必须包含的桥段或场景]

## 10. 章节规划方向

[大致的章节走向]
```

---

## 知识库自动加载规则

| 用户描述关键词 | 自动加载 |
|---------------|---------|
| 都市、现代 | genres/romance.md 或 genres/mystery.md |
| 古代、古风 | genres/historical.md 或 genres/wuxia.md |
| 玄幻、异世界 | genres/wuxia.md |
| 悬疑、推理 | genres/mystery.md |
| 复仇 | genres/revenge.md |
| 甜宠、甜文 | styles/web-novel.md + requirements/romance-sweet.md |
| 虐文、虐心 | requirements/romance-angst.md + requirements/strong-emotion.md |
| 爽文、打脸 | requirements/fast-paced.md + requirements/anti-ai-v4.md |
| 复仇 | requirements/no-poison.md + requirements/strong-emotion.md |

---

## 输出

文件路径：`stories/<story-name>/specification.md`

---

## 提示下一步

规格创建完成后，建议执行：
```
/novel clarify - 澄清关键决策
```
