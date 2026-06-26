# 人格蒸馏方法论

## 什么是蒸馏

蒸馏 = 从原始聊天记录中提取模式，生成结构化人格模型。
- **输入**：聊天记录文本（任意格式）
- **输出**：`.persona.json` 文件
- **激活**：把 JSON 中的 `system_prompt_snippet` 注入 AI 对话上下文

---

## 支持的聊天记录格式

distil.py 自动识别以下格式，优先级依次降低：

| 格式 | 示例 |
|------|------|
| 带时间戳 | `[10:23] 张三: 吃了吗` |
| 冒号分隔 | `张三: 在干嘛` 或 `张三：在干嘛` |
| 尖括号 | `<张三> 哈喽` |
| 纯文本 | 每行视为一条消息，用户名自动提取 |

> **建议**：导出聊天记录时优先选「文本格式」，避免 HTML/JSON 等复杂结构。

---

## 蒸馏质量指南

### 最低要求
- 至少 **20 条消息**（越多越准）
- 涵盖多种场景：日常闲聊、提问、讨论、告别

### 推荐数量
| 对话轮数 | 质量 |
|---------|------|
| < 20 | 基础，模板推断为主 |
| 20–50 | 较好，可提取口癖和常用词 |
| 50–200 | 优秀，行为模式清晰 |
| 200+ | 精准，价值观和决策风格可推断 |

---

## 各维度提取说明

### tone（语气）
| 维度 | 含义 | 推断依据 |
|------|------|---------|
| formality | 正式程度 1–5 | 词汇复杂度、中英混杂比例、emoji 频率 |
| emotion | 情绪强度 1–5 | 感叹号比例、emoji 数量、slang 使用 |
| humor | 幽默感 1–5 | slang 数量、emoji 频率、情绪分 |
| confidence | 自信程度 1–5 | 反驳/质疑次数 vs 同意次数 |

### linguistic（语言风格）
| 字段 | 含义 |
|------|------|
| sentence_style | 句子风格描述 |
| punctuation_habit | 标点习惯 |
| emoji_frequency | emoji 频率等级 |
| mixed_language_ratio | 中英混杂比例 |

### vocabulary（词汇）
- **slang**：内置 50+ 常用网络用语词库，自动匹配
- **particles**：语气词统计（啊/吧/呢/嘛/哦/嗯/哈/呀）
- **foreign_words**：英文字词（自动提取）

### patterns（行为模式）
| 字段 | 含义 |
|------|------|
| openers | 第一条消息的高频开头 |
| response_templates | 高频应答词 |
| agreement | 肯定信号 |
| disagreement | 质疑/否定信号 |

---

## system_prompt_snippet 注入方式

### 方式一：直接复制（推荐）
运行 `python activate.py activate <name>`，复制输出内容粘贴给 AI。

### 方式二：文件注入
```
# 在对话开头加一行：
/persona activate 张三
```

### 方式三：作为系统提示词
将 `system_prompt_snippet` 内容加入 AI 的系统提示词（System Prompt）。

---

## 手动微调

蒸馏结果不是 100% 准确的，需要人工微调：

1. **打开 persona 文件**：
   ```
   ~/.qclaw/personas/<name>.persona.json
   ```

2. **重点调整字段**：
   - `vocabulary.taboo_words` — 对方不愿意聊的话题
   - `vocabulary.custom_expressions` — 特殊口头禅
   - `tone.description` — 整体感觉描述
   - `system_prompt_snippet` — 核心激活指令

3. **保存后重新 activate**

---

## 多个人格管理

不同聊天记录可以蒸馏成不同人格，例如：
- `张三.persona.json` — 工作群里的张三
- `李四_私人.persona.json` — 私聊的李四

使用时按需激活即可：
```
python activate.py activate 张三
python activate.py activate 李四_私人
```
