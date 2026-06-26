# ATOM-VISUAL-030 - 过滤 Emoji 和特殊符号

> 版本：V1.0  
> 状态：🆕 新建  
> 最后更新：2026-03-07 21:07  
> 创建原因：TTS 语音会把 emoji 也念出来（如"空心对勾"），需要过滤

---

## 📋 原子动作定义

**名称：** 过滤 Emoji 和特殊符号  
**编号：** ATOM-VISUAL-030  
**层级：** 02-呈现层

**一句话描述：** 从文本中移除所有 emoji、Markdown 符号，只保留纯文字，适合 TTS 朗读

---

## 🎯 目标

**解决什么问题：**
- ✅ TTS 语音会把 emoji 也念出来（如"✅"念成"空心对勾"）
- ✅ Markdown 符号影响朗读体验
- ✅ 特殊符号导致语音不自然

**核心价值：**
- 纯文本 TTS，无 emoji 干扰
- 自然流畅的语音体验
- 避免"空心对勾"、"红心"等废话

---

## 🔄 工作流程

```
输入文本（带 emoji）
  ↓
过滤 emoji（Unicode 范围）
  ↓
过滤特殊符号（✅❌📊等）
  ↓
过滤 Markdown 符号（**#-` 等）
  ↓
过滤多余空格
  ↓
输出纯文本（适合 TTS 朗读）
```

---

## 📝 详细步骤

### 步骤 1：过滤 Emoji（Unicode 范围）

```powershell
# 过滤常用 emoji（Unicode 范围）
$cleanText = $text -replace '[\x{1F600}-\x{1F64F}]', ''  # 表情符号
$cleanText = $cleanText -replace '[\x{1F300}-\x{1F5FF}]', ''  # 符号和象形文字
$cleanText = $cleanText -replace '[\x{1F680}-\x{1F6FF}]', ''  # 交通和地图符号
$cleanText = $cleanText -replace '[\x{1F1E0}-\x{1F1FF}]', ''  # 旗帜
```

### 步骤 2：过滤特殊符号

```powershell
# 过滤特殊符号（补充）
$cleanText = $cleanText -replace '[\x{2600}-\x{26FF}]', ''  # 杂项符号
$cleanText = $cleanText -replace '[\x{2700}-\x{27BF}]', ''  # 装饰符号
$cleanText = $cleanText -replace '[\x{2300}-\x{23FF}]', ''  # 技术符号
```

### 步骤 3：过滤 Markdown 符号

```powershell
# 过滤 Markdown 符号
$cleanText = $cleanText -replace '\*\*', ''  # 粗体
$cleanText = $cleanText -replace '\*', ''    # 斜体
$cleanText = $cleanText -replace '#+', ''    # 标题
$cleanText = $cleanText -replace '\-', ' '   # 列表
$cleanText = $cleanText -replace '\`', ''    # 代码
$cleanText = $cleanText -replace '\[', ''    # 链接
$cleanText = $cleanText -replace '\]', ''
$cleanText = $cleanText -replace '\(', ''
$cleanText = $cleanText -replace '\)', ''
```

### 步骤 4：过滤多余空格

```powershell
# 过滤多余空格
$cleanText = $cleanText -replace '\s+', ' '
$cleanText = $cleanText.Trim()
```

### 步骤 5：返回纯文本

```powershell
return $cleanText
```

---

## 📊 示例对比

### 示例 1：优先级提醒

**过滤前：**
```
🔴 优先：飞书 OAuth 配置
📊 统计：13 项完成
✅ 完成：TTS 精简
```

**过滤后：**
```
优先：飞书 OAuth 配置
统计：13 项完成
完成：TTS 精简
```

---

### 示例 2：豆包点评

**过滤前：**
```
## 📊 专家点评

**评分：** 完整性 85% ✅

### 核心观点
- ✅ 观点 1
- ❌ 问题 2
- 💡 建议 3
```

**过滤后：**
```
专家点评

评分：完整性 85%

核心观点
观点 1
问题 2
建议 3
```

---

### 示例 3：用户反馈的问题

**过滤前：**
```
❤️ 红心直播是一个项目号
✅ 空心对勾不要念出来
📊 图表也不用念
```

**过滤后：**
```
红心直播是一个项目号
空心对勾不要念出来
图表也不用念
```

---

## 🔗 关联动作

### 前置动作
- 无（可独立执行）

### 后置动作
- ATOM-VISUAL-008：生成 TTS 语音（使用过滤后的纯文本）

### 复用场景
- SKILL-TTS-001：TTS 自动化（步骤 2）
- 任何需要 TTS 语音的场景

---

## ✅ 检查清单

执行前确认：
- [ ] 输入文本不为空
- [ ] 文本编码为 UTF-8

执行后确认：
- [ ] 所有 emoji 已移除
- [ ] 所有 Markdown 符号已移除
- [ ] 无多余空格
- [ ] 保留中文标点（，。？！）

---

## ⚠️ 常见错误

### 错误 1：保留部分 emoji

```
❌ 错误：只过滤了部分 emoji 范围
✅ 正确：覆盖所有常用 emoji Unicode 范围
```

### 错误 2：过滤了中文标点

```
❌ 错误：把，。？！也过滤了
✅ 正确：保留中文标点，只过滤 emoji 和特殊符号
```

### 错误 3：留下多余空格

```
❌ 错误：过滤后留下多个连续空格
✅ 正确：用 \s+ 替换为单个空格
```

---

## 💡 核心原则

> **纯文本，无 emoji，自然朗读！**

**关键点：**
1. ✅ 覆盖所有 emoji Unicode 范围
2. ✅ 过滤 Markdown 符号
3. ✅ 保留中文标点
4. ✅ 清理多余空格

---

## 📁 文件位置

**MD 模块：** `atomic-actions/02-visual/ATOM-VISUAL-030-过滤 Emoji.md`

**TXT 说明：** `原子动作说明/02-呈现层/030-过滤 Emoji.txt`

---

## 🎯 使用示例

### 在 SKILL-TTS-001 中调用

```powershell
# 原始文本（带 emoji）
$text = "✅ 完成：TTS 精简\n📊 统计：13 项完成"

# 调用 ATOM-VISUAL-030 过滤
$cleanText = ATOM-VISUAL-030 -text $text

# 调用 TTS（使用纯文本）
tts -text $cleanText
```

---

_过滤 emoji | 纯文本 TTS | 自然朗读 | 2026-03-07 21:07_
