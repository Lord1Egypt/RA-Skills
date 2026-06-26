# ATOM-DATA-027 - 删除项目卡片

> 版本：V1.0  
> 状态：🟡 新建  
> 最后更新：2026-03-07

---

## 📋 动作定义

**名称：** 删除项目卡片  
**分类：** 数据层（Data Layer）  
**编号：** ATOM-DATA-027

**一句话描述：** 从项目目录中删除项目卡片文件（可移动到回收站）

---

## 🎯 输入输出

### 输入
- **类型：** 文本
- **内容：** 项目名称
- **必填：** 是

### 输出
- **类型：** 布尔值
- **内容：** 删除成功/失败
- **附加：** 删除的文件路径

---

## ⚙️ 偏好设置

### 删除模式
- **模式 1：** 移动到回收站（推荐，可恢复）
- **模式 2：** 永久删除（谨慎使用）

### 备份策略
- **删除前：** 自动备份到 `archive/` 目录
- **备份命名：** `项目名_删除日期.md`

### 确认机制
- **重要项目：** 需要用户确认
- **测试项目：** 直接删除

---

## 📝 操作步骤

```powershell
# 1. 准备路径
$projectName = "测试项目"
$projectPath = "C:\Users\Xiabi\.openclaw\workspace\knowledge-base\projects\$projectName\项目卡片.md"

# 2. 检查文件存在
if (-not (Test-Path $projectPath)) {
    Write-Host "❌ 项目卡片不存在：$projectPath"
    return $false
}

# 3. 备份到 archive 目录
$archiveDir = "C:\Users\Xiabi\.openclaw\workspace\knowledge-base\projects\archive"
if (-not (Test-Path $archiveDir)) {
    New-Item -ItemType Directory -Force -Path $archiveDir | Out-Null
}
$backupName = "$projectName-$(Get-Date -Format 'yyyyMMdd').md"
Copy-Item $projectPath "$archiveDir\$backupName"

# 4. 删除文件（移动到回收站）
# 使用 PowerShell 的 Remove-Item（永久删除）
# 或使用 trash 命令（移动到回收站）
Remove-Item $projectPath -Force

# 5. 确认
Write-Host "✅ 项目卡片已删除：$projectName"
Write-Host "  备份：$archiveDir\$backupName"

return $true
```

---

## 🔄 使用场景

### 场景 1：删除测试项目
```
触发：测试项目完成
  ↓
调用：ATOM-DATA-027
  ↓
输出：项目卡片删除成功
```

### 场景 2：清理旧项目
```
触发：项目结项归档
  ↓
调用：ATOM-DATA-027
  ↓
输出：项目卡片移动到 archive
```

---

## 🔗 关联动作

### 前置动作
- ATOM-DATA-003：读取项目卡片（确认内容）

### 后置动作
- 无

### 常组合使用
- ATOM-DATA-003 + ATOM-DATA-027
  （读取确认 → 删除）

---

## ✅ 检查清单

执行前确认：
- [ ] 项目名称正确
- [ ] 文件存在
- [ ] 备份目录可写
- [ ] 用户确认（重要项目）

---

## ⚠️ 常见错误

### 错误 1：误删重要项目
```
❌ 错误：直接删除未备份
✅ 正确：先备份到 archive 目录
```

### 错误 2：删除不存在的项目
```
❌ 错误：文件不存在仍尝试删除
✅ 正确：先用 Test-Path 检查
```

---

_模块化定义 | 可独立调用 | 2026-03-07_
