# ATOM-CANVAS-020 - 渲染 Mermaid 为 PNG

> 版本：V1.0  
> 状态：🟡 新建  
> 最后更新：2026-03-07

---

## 📋 动作定义

**名称：** 渲染 Mermaid 为 PNG  
**分类：** 工具层（Tool Layer）  
**编号：** ATOM-CANVAS-020

**一句话描述：** 调用 Canvas 工具将 Mermaid 代码渲染成 PNG 图片

---

## 🎯 输入输出

### 输入
- **类型：** 文本
- **内容：** Mermaid 代码
- **格式：** Mermaid 语法字符串

### 输出
- **类型：** 文件路径
- **内容：** PNG 图片的绝对路径
- **格式：** PNG（高质量）

---

## ⚙️ 偏好设置

### 图片规格
- **宽度：** 800px
- **高度：** 600px
- **质量：** 90%
- **格式：** PNG

### 输出目录
- **路径：** `workspace/diagrams/`
- **命名：** `diagram-YYYYMMDD-HHMMSS.png`

### Mermaid 配置
- **主题：** base
- **字体：** Microsoft YaHei
- **曲线：** basis

---

## 📝 操作步骤

```powershell
# 1. 准备 Mermaid 代码
$mermaidCode = @"
graph TD
    A[感知与行动中心] --> B[产能监控系统]
    A --> C[风险预警机制]
    style A fill:#FE2C55,stroke:#333,stroke-width:2px,color:#fff
"@

# 2. 创建临时 HTML 文件
$tempHtml = @"
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
</head>
<body>
    <div class="mermaid">$mermaidCode</div>
    <script>mermaid.initialize({startOnLoad:true});</script>
</body>
</html>
"@

$tempPath = "$env:TEMP\mermaid-temp.html"
$tempHtml | Set-Content $tempPath -Encoding UTF8

# 3. 调用 Canvas 工具渲染
# （实际调用时通过 OpenClaw canvas 工具）
# canvas -action snapshot -url "file://$tempPath" -outputFormat png

# 4. 保存 PNG 文件
$outputDir = "C:\Users\Xiabi\.openclaw\workspace\diagrams"
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Force -Path $outputDir | Out-Null
}

$outputPath = "$outputDir\diagram-$(Get-Date -Format 'yyyyMMdd-HHmmss').png"

# 5. 返回路径
Write-Host "✅ Mermaid 已渲染为 PNG：$outputPath"
return $outputPath
```

---

## 🔄 使用场景

### 场景 1：专家点评 HTML 嵌入图片
```
触发：生成 HTML 报告
  ↓
调用：ATOM-CANVAS-020
  ↓
输出：PNG 图片
  ↓
嵌入：HTML 的<img>标签
```

### 场景 2：独立架构图输出
```
触发：需要单独分享架构图
  ↓
调用：ATOM-CANVAS-020
  ↓
输出：PNG 图片文件
  ↓
交付：飞书发送文件
```

---

## 🔗 关联动作

### 前置动作
- ATOM-VISUAL-006：生成 Mermaid 图表

### 后置动作
- ATOM-IO-021：保存 HTML 文件（嵌入图片）
- ATOM-DELIVERY-012：飞书发送文件

### 常组合使用
- ATOM-VISUAL-006 + ATOM-CANVAS-020 + ATOM-IO-021
  （生成代码 → 渲染图片 → 嵌入 HTML）

---

## ✅ 检查清单

执行前确认：
- [ ] Mermaid 代码正确
- [ ] Canvas 工具可用
- [ ] 输出目录可写
- [ ] 网络可访问（加载 Mermaid CDN）

---

## ⚠️ 常见错误

### 错误 1：Mermaid 代码错误
```
❌ 错误：语法错误导致渲染失败
✅ 正确：先用 Mermaid Live Editor 验证代码
```

### 错误 2：Canvas 工具不可用
```
❌ 错误：浏览器未启动
✅ 正确：检查浏览器状态或改用备用方案
```

---

_模块化定义 | 可独立调用 | 2026-03-07_
