# ATOM-DATA-001 - 保存豆包会话

> 版本：V1.0  
> 状态：✅ 已固化  
> 最后更新：2026-03-06

---

## 📋 动作定义

**名称：** 保存豆包会话  
**分类：** 数据层（Data Layer）  
**编号：** ATOM-DATA-001

**一句话描述：** 将豆包聊天记录保存到本地 Markdown 文件

---

## 🎯 输入输出

### 输入
- **类型：** 文本
- **内容：** 豆包聊天记录（原始内容）
- **必填：** 是

### 输出
- **类型：** 文件
- **路径：** `knowledge-base/doubao-sessions/YYYY-MM-DD-序号.md`
- **格式：** Markdown（UTF-8）

---

## ⚙️ 偏好设置

### 文件命名
- **格式：** `YYYY-MM-DD (周 X) -N worklog.md`
- **序号规则：** 同一天自动递增（-1, -2, -3...）
- **编码：** UTF-8

### 内容结构
```markdown
# 豆包会话归档

**日期：** 2026-03-07 (周六)
**序号：** -1
**原始时间：** 2026-03-07 10:30
**会话主题：** [自动提取或用户指定]

---

## 会话内容

[原始聊天内容]

---

_自动归档于 [时间]_
```

### 存储位置
- **根目录：** `knowledge-base/doubao-sessions/`
- **自动创建：** 目录不存在时自动创建

---

## 📝 操作步骤

```powershell
# 1. 生成文件名
$today = Get-Date -Format "yyyy-MM-dd"
$weekday = Get-Date -Format "(ddd)"
$pattern = "$today $weekday -*.md"
$existingFiles = Get-ChildItem "knowledge-base/doubao-sessions" -Filter $pattern
$nextNum = $existingFiles.Count + 1
$filename = "$today $weekday -$nextNum worklog.md"

# 2. 生成内容
$markdown = @"
# 豆包会话归档

**日期：** $today $weekday
**序号：** -$nextNum
**原始时间：** $(Get-Date -Format 'yyyy-MM-dd HH:mm')
**会话主题：** $topic

---

## 会话内容

$content

---

_自动归档于 $(Get-Date -Format 'yyyy-MM-dd HH:mm')_
"@

# 3. 保存文件
$markdown | Set-Content "knowledge-base/doubao-sessions/$filename" -Encoding UTF8

# 4. 确认
Write-Host "✅ 会话已归档：$filename"
```

---

## 🔄 使用场景

### 场景 1：豆包聊天后自动保存
```
触发：用户发送"豆包 [聊天内容]"
  ↓
调用：ATOM-DATA-001
  ↓
输出：doubao-sessions/2026-03-07 (周六) -1 worklog.md
```

### 场景 2：手动归档
```
触发：用户说"保存刚才的豆包会话"
  ↓
调用：ATOM-DATA-001
  ↓
输出：doubao-sessions/2026-03-07 (周六) -2 worklog.md
```

---

## 🔗 关联动作

### 前置动作
- 无（可独立执行）

### 后置动作
- ATOM-DATA-002：更新 worklog（提取工作内容）
- ATOM-ANALYSIS-015：识别项目关键词
- ATOM-ANALYSIS-016：提取工作内容

### 常组合使用
- ATOM-DATA-001 + ATOM-DATA-002 + ATOM-VISUAL-005
  （保存会话 → 更新 worklog → 生成 HTML）

---

## ✅ 检查清单

执行前确认：
- [ ] 目录存在（knowledge-base/doubao-sessions/）
- [ ] 内容非空
- [ ] 编码 UTF-8
- [ ] 文件名含日期和序号

---

## 📚 参考文档

- 主数据清单：`原子级动作主数据清单.md`
- 使用 Skill：`skills/doubao-session-archiver/SKILL.md`
- 存储目录：`knowledge-base/doubao-sessions/`

---

_模块化定义 | 可独立调用 | 2026-03-07_
