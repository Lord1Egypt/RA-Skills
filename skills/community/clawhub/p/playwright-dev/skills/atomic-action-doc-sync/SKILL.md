# Atomic Action Doc Sync - 原子动作文档同步 Skill

> 版本：V1.0  
> 状态：🆕 新建  
> 最后更新：2026-03-07 14:14

---

## 📋 Skill 定义

**名称：** 原子动作文档同步  
**编号：** SKILL-DOC-SYNC-001  
**触发：** 原子动作增删改后自动触发

**一句话描述：** 自动同步原子动作变更到飞书文档（三线同步）

---

## 🎯 目标

**解决什么问题：**
- ❌ 之前：只更新本地 MD/TXT，忘记更新飞书文档
- ✅ 现在：自动同步，三线一致

**核心价值：**
- 线上线下信息一致
- 不用手动更新飞书
- 避免遗漏和不同步

---

## 🔄 工作流程

```
原子动作变更（新增/修改/删除）
  ↓
1. 更新本地 MD 文件 ✅
  ↓
2. 更新本地 TXT 文件 ✅
  ↓
3. 触发：atomic-action-doc-sync Skill
  ↓
4. 调用 ATOM-DOC-029（提取变更信息）
  ↓
5. 调用 ATOM-FEISHU-028（分块写入飞书）
  ↓
✅ 三线同步完成（飞书 + MD + TXT）
```

---

## 📝 详细步骤

### 步骤 1：原子动作变更
```powershell
# 用户/阿福更新原子动作
# 示例：修改 ATOM-DELIVERY-013（锁屏检测）

# 1. 更新 MD 文件
Edit-File "atomic-actions/03-delivery/ATOM-DELIVERY-013.md"

# 2. 更新 TXT 文件
Edit-File "原子动作说明/03-交付层/013-本地播放语音.txt"
```

### 步骤 2：触发 Skill
```powershell
# 自动触发（或手动调用）
.\atomic-action-doc-sync.ps1 -Action "ATOM-DELIVERY-013" -ChangeType "modify"
```

### 步骤 3：提取变更信息
```powershell
# 读取 MD 文件头部
$mdContent = Get-Content "atomic-actions/03-delivery/ATOM-DELIVERY-013.md" -Raw

# 提取信息
$actionNumber = "ATOM-DELIVERY-013"
$actionName = "本地播放语音"
$changeDesc = "新增锁屏检测功能"
$changeTime = Get-Date -Format "yyyy-MM-dd HH:mm"
$newVersion = "V1.2"  # 自动递增
```

### 步骤 4：更新飞书文档
```powershell
# 调用 ATOM-DOC-029
$docToken = "GeG0dywMxof8dLx1tcUckSFNndh"

# 4.1 更新版本记录表（开头添加新行）
$newVersionRow = "| $newVersion | $changeTime | $changeDesc | 阿福 |"

# 4.2 更新原子动作表格（找到对应分类，更新对应行）
# 查找"03-交付层"表格，更新 ATOM-DELIVERY-013 行

# 4.3 更新总览信息
# 总数：不变（修改）
# 最后更新时间：$changeTime

# 4.4 分块写入（调用 ATOM-FEISHU-028）
# 第 1 块：版本记录 + 部分表格（write 模式）
# 第 2 块：剩余表格（append 模式）
# 第 3 块：说明 + 日志（append 模式）
```

### 步骤 5：确认同步完成
```powershell
Write-Host "✅ 三线同步完成！" -ForegroundColor Green
Write-Host "  飞书文档：已更新（版本 $newVersion）" -ForegroundColor Cyan
Write-Host "  MD 文件：已更新" -ForegroundColor Cyan
Write-Host "  TXT 文件：已更新" -ForegroundColor Cyan
```

---

## 📊 输入输出

### 输入
- **动作编号：** 如 `ATOM-DELIVERY-013`
- **变更类型：** `add` / `modify` / `delete`
- **变更内容：** 描述文本（如"新增锁屏检测功能"）
- **飞书 Token：** `GeG0dywMxof8dLx1tcUckSFNndh`

### 输出
- **状态：** `success` / `failed`
- **版本号：** 更新后的版本号（如 `V1.2`）
- **日志：** 同步过程记录

---

## 🎯 使用示例

### 示例 1：新增原子动作
```powershell
# 创建 ATOM-FEISHU-028 后
.\atomic-action-doc-sync.ps1 -Action "ATOM-FEISHU-028" -ChangeType "add" -Desc "新增写入飞书文档原子动作"

# 输出：
# ✅ 三线同步完成！
#   飞书文档：V1.0 → V1.1
#   交付层表格：+1 行
#   MD/TXT：已创建
```

### 示例 2：修改原子动作
```powershell
# 修改 ATOM-DELIVERY-013 后
.\atomic-action-doc-sync.ps1 -Action "ATOM-DELIVERY-013" -ChangeType "modify" -Desc "新增锁屏检测功能"

# 输出：
# ✅ 三线同步完成！
#   飞书文档：V1.1 → V1.2
#   交付层表格：更新偏好
#   MD/TXT：已更新
```

### 示例 3：删除原子动作
```powershell
# 删除原子动作后
.\atomic-action-doc-sync.ps1 -Action "ATOM-XXX-000" -ChangeType "delete" -Desc "删除废弃动作"

# 输出：
# ✅ 三线同步完成！
#   飞书文档：V1.2 → V1.3
#   对应表格：-1 行（标记已删除）
#   MD/TXT：已删除
```

---

## 📁 文件结构

```
workspace/
├── atomic-actions/                      # MD 模块库
│   ├── 03-delivery/
│   │   └── ATOM-DELIVERY-013.md        # ✅ 已更新
│   └── 04-documentation/
│       └── ATOM-DOC-029.md             # 🆕 新建
├── 原子动作说明/                         # TXT 说明库
│   ├── 03-交付层/
│   │   └── 013-本地播放语音.txt        # ✅ 已更新
│   └── 04-文档层/
│       └── 029-更新飞书原子动作清单.txt # 🆕 新建
├── skills/
│   └── atomic-action-doc-sync/
│       ├── SKILL.md                    # 🆕 本文件
│       └── sync.ps1                    # 🆕 同步脚本
└── 飞书文档/
    └── 原子动作清单 - 动态更新           # 🆕 线上同步
```

---

## ✅ 检查清单

执行前确认：
- [ ] 本地 MD 文件已更新
- [ ] 本地 TXT 文件已更新
- [ ] 飞书文档 Token 正确
- [ ] 有编辑权限
- [ ] 版本号正确递增

执行后确认：
- [ ] 飞书文档版本记录已更新
- [ ] 飞书文档表格已更新
- [ ] 三线信息一致
- [ ] 日志已记录

---

## ⚠️ 常见错误

### 错误 1：忘记触发 Skill
```
❌ 错误：更新 MD/TXT 后，忘记调用同步 Skill
✅ 正确：更新后立即调用 atomic-action-doc-sync
```

### 错误 2：版本号错误
```
❌ 错误：版本号不递增或格式错误
✅ 正确：V{主版本}.{次版本}，次版本 +1
```

### 错误 3：一次性写入太多
```
❌ 错误：一次性写入全部内容 → 400 错误
✅ 正确：分块写入（≤200 blocks/块）
```

---

## 💡 核心原则

> **线上线下同步更新，不能只更新一方！**

**三线同步：**
- ✅ 飞书文档（云端协作）
- ✅ MD 文件（本地模块）
- ✅ TXT 文件（人类可读）

**触发时机：**
- 原子动作增删改后立即触发
- 自动同步，不用手动

**质量保证：**
- 版本号自动递增
- 版本记录完整
- 表格内容一致

---

## 📚 参考文档

- 原子动作清单：飞书文档 `GeG0dywMxof8dLx1tcUckSFNndh`
- 原子动作主数据：`原子级动作主数据清单.md`
- 原子动作模块：`atomic-actions/`
- 人类可读说明：`原子动作说明/`

---

_自动同步 | 三线一致 | 2026-03-07_
