# HTML 专家点评技能备份 - V2.0

**备份时间：** 2026-03-10 11:12  
**备份原因：** 用户要求备份所有相关内容，防止误改后无法恢复  
**备份位置：** `backups/html-expert-review-v2.0/`

---

## 📦 备份内容

### 1️⃣ 核心技能文件

| 文件 | 大小 | 说明 |
|------|------|------|
| **SKILL.md** | 36.5 KB | HTML 专家点评技能主文件（含用户偏好 V2.0） |
| **HTML-STANDARD.md** | 11.7 KB | HTML 结构标准文档 |

### 2️⃣ 示例 HTML 文件

| 文件 | 说明 |
|------|------|
| **示例 - 知识库架构.html** | 2026-03-08 原始版本（标准模板） |
| **示例 -OpenClaw 知识库架构（最新复刻）.html** | 2026-03-10 最新复刻版本 |
| **示例 - 进展中项目全览.html** | 2026-03-10 项目全览版本 |

### 3️⃣ 用户偏好记录

| 文件 | 说明 |
|------|------|
| **用户偏好固化记录.md** | 2026-03-10 固化的 6 大核心风格 |

---

## 🎨 用户偏好 V2.0（核心风格）

### 6 大核心风格

1. **渐变背景**
   - 整体：`#f5f7fa → #c3cfe2`（浅灰蓝）
   - Header：`#667eea → #764ba2`（紫色）

2. **大圆角设计**
   - container：20px
   - 卡片/图表：15px
   - 表格：10px

3. **阴影效果**
   - container：`0 20px 60px`
   - 专家卡片：`0 10px 30px`

4. **配色方案**
   - 主色：紫色 `#667eea → #764ba2`
   - 专家卡片：橙色 `#ffecd2 → #fcb69f`
   - 存储格：青粉 `#a8edea → #fed6e3`

5. **装饰元素**
   - Header：📚🏗️
   - 章节：🔹
   - 卡片：⭐

6. **Mermaid 样式**
   - 带 emoji（📑📁📚）
   - 紫色系自定义颜色

---

## 🔄 恢复方法

### 如果不小心修改了技能文件

**步骤 1：确认需要恢复的文件**
- 如果只是修改了样式 → 恢复 `SKILL.md`
- 如果修改了标准 → 恢复 `HTML-STANDARD.md`
- 如果全部要恢复 → 恢复整个文件夹

**步骤 2：复制回原位置**

```powershell
# 恢复 SKILL.md
Copy-Item -Path "backups/html-expert-review-v2.0/SKILL.md" `
          -Destination "skills/html-expert-review/SKILL.md" `
          -Force

# 恢复 HTML-STANDARD.md
Copy-Item -Path "backups/html-expert-review-v2.0/HTML-STANDARD.md" `
          -Destination "skills/html-expert-review/HTML-STANDARD.md" `
          -Force

# 恢复整个文件夹
Copy-Item -Path "backups/html-expert-review-v2.0\*" `
          -Destination "skills/html-expert-review/" `
          -Recurse -Force
```

**步骤 3：验证恢复**
- 生成一个测试 HTML
- 检查是否符合用户偏好 V2.0
- 确认渐变背景、大圆角、阴影效果等

---

## 📋 检查清单

恢复后检查以下项目：

- [ ] **背景渐变** - body 使用 `#f5f7fa → #c3cfe2`
- [ ] **Header 渐变** - 使用 `#667eea → #764ba2`（紫色）
- [ ] **圆角尺寸** - container 20px、卡片 15px、表格 10px
- [ ] **阴影效果** - container 大阴影（0 20px 60px）
- [ ] **专家卡片** - 橙色渐变背景（`#ffecd2 → #fcb69f`）
- [ ] **存储格** - 青粉渐变背景（`#a8edea → #fed6e3`）
- [ ] **装饰 emoji** - Header 有📚🏗️、章节有🔹、卡片有⭐
- [ ] **Mermaid emoji** - 节点名称前带 emoji
- [ ] **Mermaid 颜色** - 紫色系（#667eea, #764ba2, #f093fb）
- [ ] **字体** - Microsoft YaHei（微软雅黑）

---

## 🎯 参考文件

**标准模板：**
- `示例 - 知识库架构.html`（2026-03-08 原始版本）

**最新版本：**
- `示例 -OpenClaw 知识库架构（最新复刻）.html`（2026-03-10）
- `示例 - 进展中项目全览.html`（2026-03-10）

---

## ⚠️ 重要提示

1. **不要删除备份文件夹** - 这是恢复的唯一来源
2. **定期更新备份** - 每次技能有重大更新时，更新备份
3. **备份命名规范** - `html-expert-review-v 版本号/`
4. **恢复前确认** - 恢复前先查看备份文件内容，确认是正确版本

---

## 📝 备份历史

| 版本 | 时间 | 说明 |
|------|------|------|
| **V2.0** | 2026-03-10 | 首次完整备份（含用户偏好 V2.0） |

---

_备份人：阿福 🦞_  
_备份原因：用户要求"万一以后不小心改了的话，也有地方可以恢复"_
