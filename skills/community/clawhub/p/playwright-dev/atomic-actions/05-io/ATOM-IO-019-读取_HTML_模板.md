# ATOM-IO-019 - 读取 HTML 模板

> 版本：V1.0  
> 状态：🟡 新建  
> 最后更新：2026-03-07

---

## 📋 动作定义

**名称：** 读取 HTML 模板  
**分类：** IO 层（Input/Output Layer）  
**编号：** ATOM-IO-019

**一句话描述：** 从文件系统中读取 HTML 模板文件内容

---

## 🎯 输入输出

### 输入
- **类型：** 文件路径
- **内容：** HTML 模板文件的绝对路径
- **必填：** 是

### 输出
- **类型：** 文本
- **内容：** HTML 模板的完整内容
- **格式：** UTF-8 编码字符串

---

## ⚙️ 偏好设置

### 文件路径
- **根目录：** `skills/html-expert-review/templates/`
- **默认模板：** `standard-template.html`
- **编码：** UTF-8

### 错误处理
- **文件不存在：** 返回错误提示
- **编码错误：** 尝试 GBK 编码回退

---

## 📝 操作步骤

```powershell
# 1. 定义模板路径
$templatePath = "C:\Users\Xiabi\.openclaw\workspace\skills\html-expert-review\templates\standard-template.html"

# 2. 检查文件存在
if (-not (Test-Path $templatePath)) {
    Write-Host "❌ 模板文件不存在：$templatePath"
    return $null
}

# 3. 读取文件内容
$templateContent = Get-Content $templatePath -Raw -Encoding UTF8

# 4. 返回内容
return $templateContent
```

---

## 🔄 使用场景

### 场景 1：生成 HTML 专家点评
```
触发：需要生成 HTML 报告
  ↓
调用：ATOM-IO-019
  ↓
输出：HTML 模板内容
  ↓
下一步：ATOM-IO-020 写入内容
```

### 场景 2：批量生成报告
```
触发：多个报告需要统一格式
  ↓
调用：ATOM-IO-019（一次）
  ↓
输出：模板内容（复用）
  ↓
循环：ATOM-IO-020 + ATOM-IO-021
```

---

## 🔗 关联动作

### 前置动作
- 无（可独立执行）

### 后置动作
- ATOM-IO-020：写入 HTML 内容

### 常组合使用
- ATOM-IO-019 + ATOM-IO-020 + ATOM-IO-021
  （读取 → 写入 → 保存）

---

## ✅ 检查清单

执行前确认：
- [ ] 模板路径正确
- [ ] 文件存在
- [ ] 编码 UTF-8
- [ ] 文件可读

---

## ⚠️ 常见错误

### 错误 1：模板文件不存在
```
❌ 错误：路径错误或文件被删除
✅ 正确：先用 Test-Path 检查
```

### 错误 2：编码错误
```
❌ 错误：中文乱码
✅ 正确：使用 -Encoding UTF8
```

---

_模块化定义 | 可独立调用 | 2026-03-07_
