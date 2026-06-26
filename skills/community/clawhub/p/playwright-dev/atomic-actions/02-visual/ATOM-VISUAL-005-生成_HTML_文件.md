# ATOM-VISUAL-005 - 生成 HTML 文件

> 版本：V1.0  
> 状态：✅ 已固化  
> 最后更新：2026-03-07 08:55

---

## 📋 动作定义

**名称：** 生成 HTML 文件  
**分类：** 呈现层（Visual Layer）  
**编号：** ATOM-VISUAL-005

**一句话描述：** 生成科学杂志风格的专家点评 HTML 报告

---

## 🎯 输入输出

### 输入
- **类型：** Markdown 内容 + Mermaid 图表
- **内容：** 专家评分/核心观点/深度洞察/知识架构/对比分析/行动建议
- **必填：** 是

### 输出
- **类型：** 文件
- **路径：** `expert-review-YYYY-MM-DD-主题.html`
- **格式：** HTML5（UTF-8）
- **大小：** <50KB

---

## ⚙️ 偏好设置

### 视觉风格
- **标准：** 科学杂志 + 小红书视觉
- **背景：** 白色 (#FFFFFF)
- **字体：** 微软雅黑 14px
- **主色：** 黑色 (#000000)
- **强调色：** 小红书红 (#FE2C55)

### 章节结构（6 章节）
1. ⭐ 专家评分
2. 💡 核心观点
3. 🔍 深度洞察
4. 📊 知识架构（Mermaid）
5. 📋 对比分析
6. 🎯 行动建议

### 图标使用
- ⭐ 专家评分
- 💡 核心观点
- 🔍 深度洞察
- 📊 知识架构
- 📋 对比分析
- 🎯 行动建议

### 文件命名
- **格式：** `expert-review-YYYY-MM-DD-主题.html`
- **编码：** UTF-8

---

## 📝 操作步骤

```powershell
# 1. 准备 HTML 模板
$htmlTemplate = @"
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>专家点评 - $topic</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        /* 科学杂志风格 CSS */
        :root {
            --primary-color: #000000;
            --accent-color: #FE2C55;
            --bg-color: #FFFFFF;
        }
        body { font-family: 'Microsoft YaHei'; font-size: 14px; background: #fff; }
        h2 { border-left: 4px solid #FE2C55; padding-left: 10px; }
        .section { margin: 30px 0; padding: 20px; background: #F8F9FA; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 专家点评 - $topic</h1>
            <p>生成时间：$(Get-Date -Format 'yyyy-MM-dd HH:mm')</p>
        </div>
        
        <!-- 6 个章节 -->
        <div class="section">
            <h2>⭐ 专家评分</h2>
            $ratingContent
        </div>
        
        <div class="section">
            <h2>💡 核心观点</h2>
            $corePoints
        </div>
        
        <div class="section">
            <h2>🔍 深度洞察</h2>
            $insights
        </div>
        
        <div class="section">
            <h2>📊 知识架构</h2>
            $mermaidChart
        </div>
        
        <div class="section">
            <h2>📋 对比分析</h2>
            $comparison
        </div>
        
        <div class="section">
            <h2>🎯 行动建议</h2>
            $actions
        </div>
    </div>
    
    <script>mermaid.initialize({ startOnLoad: true });</script>
</body>
</html>
"@

# 2. 保存文件
$htmlTemplate | Set-Content $outputPath -Encoding UTF8

# 3. Chrome 打开
Start-Process "chrome.exe" -ArgumentList $outputPath

# 4. 确认
Write-Host "✅ HTML 已生成：$outputPath"
```

---

## 🔄 使用场景

### 场景 1：豆包会话专家点评
```
触发：用户发送"豆包 [内容]"
  ↓
处理：分析内容 → 生成评分/洞察/建议
  ↓
调用：ATOM-VISUAL-005
  ↓
输出：expert-review-2026-03-07-xiaomi-auto.html
```

### 场景 2：手动生成点评
```
触发：用户说"生成专家点评"
  ↓
调用：ATOM-VISUAL-005
  ↓
输出：HTML 报告
```

---

## 🔗 关联动作

### 前置动作
- ATOM-VISUAL-007：生成专家评分
- ATOM-VISUAL-006：生成 Mermaid 图表
- ATOM-ANALYSIS-017：专家视角分析

### 后置动作
- ATOM-VISUAL-009：Chrome 打开文件

### 常组合使用
- ATOM-VISUAL-007 + ATOM-VISUAL-006 + ATOM-VISUAL-005 + ATOM-VISUAL-009
  （评分 → 图表 → HTML → 打开）

---

## ✅ 检查清单

执行前确认：
- [ ] 6 章节内容完整
- [ ] Mermaid 图表正确
- [ ] 科学杂志风格 CSS
- [ ] UTF-8 编码
- [ ] 文件大小<50KB
- [ ] 🆕 Mermaid 语法正确（无中文 subgraph 名称）
- [ ] 🆕 节点标签简化（无复杂 HTML）
- [ ] 🆕 stroke-dasharray 无空格

---

## ⚠️ 常见问题（2026-03-07 14:42 更新）

### 问题 1：Mermaid Syntax error

**错误信息：**
```
Syntax error in text
mermaid version 10.9.5
```

**原因：**
1. subgraph 名称包含中文 + 特殊符号 + 引号
2. 节点标签过于复杂（HTML 标签 + 长中文）
3. stroke-dasharray 语法有空格

**错误示例：**
```mermaid
❌ subgraph 原子动作层 ["⚛️ 下层：原子动作层（Atomic Actions）- 共享"]
❌ A29["ATOM-DOC-029<br/>更新飞书原子动作清单"]
❌ stroke-dasharray: 5 5
```

**正确示例：**
```mermaid
✅ subgraph Layer1["下层：原子动作"]
✅ A29["ATOM-DOC-029"]
✅ stroke-dasharray:5 5
```

**解决方案：**
1. subgraph 名称用英文（Layer1/Layer2/Layer3）
2. 节点标签简化（中文放标签内，不用 HTML）
3. stroke-dasharray 不用空格（5 5 或 5,5）
4. 使用英文引号

---

## 🚫 禁止事项

- ❌ 花哨背景（渐变色、图案）
- ❌ 过多颜色（≤5 种主色）
- ❌ 手绘风格图表（用 Mermaid）
- ❌ 无结构堆砌（必须 6 章节）
- ❌ 被动总结（要有 Critical Thinking）

---

## 📚 参考文档

- 主数据清单：`原子级动作主数据清单.md`
- 标准文档：`skills/html-expert-review/HTML-STANDARD.md`
- 使用 Skill：`skills/html-expert-review/SKILL.md`

---

_模块化定义 | 可独立调用 | 2026-03-07_
