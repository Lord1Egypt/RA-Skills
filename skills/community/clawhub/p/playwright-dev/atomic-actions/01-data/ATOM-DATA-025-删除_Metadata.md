# ATOM-DATA-025 - 删除 Metadata

> 版本：V1.0  
> 状态：🟡 新建  
> 最后更新：2026-03-07

---

## 📋 动作定义

**名称：** 删除 Metadata  
**分类：** 数据层（Data Layer）  
**编号：** ATOM-DATA-025

**一句话描述：** 从 Metadata 文件中删除指定的键值对

---

## 🎯 输入输出

### 输入
- **类型：** 文本或数组
- **内容：** 键名（单个或列表）
- **必填：** 是

### 输出
- **类型：** 布尔值
- **内容：** 删除成功/失败
- **附加：** 删除的键数量

---

## ⚙️ 偏好设置

### Metadata 文件
- **路径：** `knowledge-base/metadata.md`
- **格式：** YAML Front Matter + Markdown
- **编码：** UTF-8

### 删除模式
- **单键删除：** 删除一个键
- **批量删除：** 删除多个键
- **条件删除：** 满足条件才删除

### 备份策略
- **删除前：** 自动备份整个 Metadata 文件
- **备份命名：** `metadata_备份日期.md`
- **保留策略：** 保留最近 7 个备份

---

## 📝 操作步骤

```powershell
# 1. 准备 Metadata 文件路径
$metadataPath = "C:\Users\Xiabi\.openclaw\workspace\knowledge-base\metadata.md"

# 2. 备份文件
$backupDir = "C:\Users\Xiabi\.openclaw\workspace\knowledge-base\backup"
if (-not (Test-Path $backupDir)) {
    New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
}
$backupName = "metadata_$(Get-Date -Format 'yyyyMMdd_HHmmss').md"
Copy-Item $metadataPath "$backupDir\$backupName"

# 3. 准备要删除的键
$keysToDelete = @("old_key", "deprecated_field")

# 4. 读取文件内容
$content = Get-Content $metadataPath -Raw

# 5. 删除键值对
$deletedCount = 0
foreach ($key in $keysToDelete) {
    if ($content -match "^$key:\s*(.*)$") {
        $content = $content -replace "^$key:\s*.*$`n?", ""
        Write-Host "✅ 已删除：$key"
        $deletedCount++
    } else {
        Write-Host "⚠️ 键不存在：$key"
    }
}

# 6. 保存文件
$content | Set-Content $metadataPath -Encoding UTF8

# 7. 返回成功
Write-Host "✅ Metadata 已删除：$deletedCount 个条目"
Write-Host "  备份：$backupDir\$backupName"
return $true
```

---

## 🔄 使用场景

### 场景 1：清理废弃字段
```
触发：系统升级，废弃旧字段
  ↓
调用：ATOM-DATA-025
  ↓
输入：@("old_field", "deprecated_key")
  ↓
输出：废弃字段已删除
```

### 场景 2：项目结项清理
```
触发：项目结项
  ↓
调用：ATOM-DATA-025
  ↓
输入：project_status
  ↓
输出：项目状态字段已删除
```

---

## 🔗 关联动作

### 前置动作
- ATOM-DATA-023：读取 Metadata（确认键存在）

### 后置动作
- 无

### 常组合使用
- ATOM-DATA-023 + ATOM-DATA-025
  （读取确认 → 删除）

---

## ✅ 检查清单

执行前确认：
- [ ] Metadata 文件存在
- [ ] 键名正确
- [ ] 备份目录可写
- [ ] 用户确认（重要字段）

---

## ⚠️ 常见错误

### 错误 1：误删重要字段
```
❌ 错误：直接删除未备份
✅ 正确：先备份整个 Metadata 文件
```

### 错误 2：删除不存在的键
```
❌ 错误：尝试删除不存在的键
✅ 正确：先用 ATOM-DATA-023 检查
```

---

_模块化定义 | 可独立调用 | 2026-03-07_
