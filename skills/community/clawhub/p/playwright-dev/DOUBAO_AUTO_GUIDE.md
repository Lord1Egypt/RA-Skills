# 豆包对话自动保存配置指南

**创建时间**: 2026-03-05  
**目标**: 自动保存豆包对话到个人知识库

---

## 📋 方案对比

| 方案 | 难度 | 自动化程度 | 适用场景 |
|------|------|-----------|---------|
| **剪贴板方案** | ⭐ | 半自动 | 立即可用 |
| **浏览器自动化** | ⭐⭐⭐ | 全自动 | 高级用户 |

---

## 🚀 方案 1：剪贴板方案（立即可用）

### 使用步骤

1. **打开豆包对话页面**
   ```
   https://www.doubao.com
   ```

2. **复制对话内容**
   ```
   选中侧边栏对话 → Ctrl+C
   ```

3. **运行脚本**
   ```powershell
   powershell -ExecutionPolicy Bypass -File C:\Users\Xiabi\.openclaw\workspace\save-doubao-automation.ps1
   ```

4. **输入对话主题**
   ```
   例如：网页总结技巧、代码审查建议
   ```

5. **自动保存**
   - 保存到 `knowledge-base/doubao-主题 - 时间戳.md`
   - 自动更新知识库索引

### 优点
- ✅ 立即可用
- ✅ 不需要配置
- ✅ 简单快速

### 缺点
- ❌ 需要手动复制
- ❌ 不是完全自动化

---

## 🤖 方案 2：浏览器自动化（高级）

### 前提条件

1. **OpenClaw 运行中**
2. **浏览器已配置**（CDP 端口 18800）
3. **豆包网页可访问**

### 配置步骤

#### 第 1 步：打开豆包网页

```powershell
# 在 OpenClaw 中执行
browser.open https://www.doubao.com
```

#### 第 2 步：捕获页面结构

```powershell
# 获取页面元素结构
browser.snapshot refs="aria"
```

#### 第 3 步：定位侧边栏

豆包侧边栏通常使用以下 CSS 选择器：
```css
aside.sidebar
div.conversation-panel
div[class*="sidebar"]
div[class*="conversation"]
```

#### 第 4 步：提取对话内容

```powershell
# 使用 browser.act 提取文本
browser.act
  action: evaluate
  fn: |
    () => {
      const sidebar = document.querySelector('aside.sidebar');
      return sidebar ? sidebar.innerText : '未找到侧边栏';
    }
```

#### 第 5 步：保存到文件

```powershell
# 将提取的内容保存到 Markdown
$content | Out-File -FilePath $filename -Encoding UTF8
```

### 完整自动化脚本

创建一个完全自动化的脚本 `save-doubao-full-auto.ps1`：

```powershell
# 完全自动化版本
$workspace = "C:\Users\Xiabi\.openclaw\workspace"

# 1. 打开豆包
browser.open https://www.doubao.com

# 2. 等待加载
Start-Sleep -Seconds 3

# 3. 捕获页面
browser.snapshot refs="aria"

# 4. 提取侧边栏内容
$conversation = browser.act
  action: evaluate
  fn: "() => document.querySelector('aside.sidebar')?.innerText || ''"

# 5. 生成文件名
$timestamp = Get-Date -Format "yyyy-MM-dd-HHmmss"
$filename = "$workspace\knowledge-base\doubao-$timestamp.md"

# 6. 保存
$content = @"
# 豆包对话

**时间**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
**来源**: 豆包 AI

## 对话内容

$conversation

---
#豆包 #AI 对话 #知识库
"@

$content | Out-File -FilePath $filename -Encoding UTF8

# 7. 更新索引
& "$workspace\update-knowledge-index.ps1"
```

---

## 📁 文件结构

```
C:\Users\Xiabi\.openclaw\workspace\
├── knowledge-base/                    # 知识库目录
│   ├── doubao-网页总结 -2026-03-05-185000.md
│   ├── doubao-代码审查 -2026-03-05-190000.md
│   └── doubao-学习笔记 -2026-03-05-191000.md
├── save-doubao-conversation.ps1       # 基础脚本
├── save-doubao-automation.ps1         # 剪贴板脚本
├── save-doubao-full-auto.ps1          # 完全自动化脚本（待创建）
└── DOUBAO_AUTO_GUIDE.md              # 本指南
```

---

## 🎯 推荐使用流程

### 日常使用（剪贴板方案）

```
1. 豆包对话 → Ctrl+C 复制
2. 运行 save-doubao-automation.ps1
3. 输入主题 → 自动保存
4. 完成！
```

**耗时**: 约 30 秒

### 批量处理（完全自动化）

```
1. 运行 save-doubao-full-auto.ps1
2. 自动打开豆包
3. 自动抓取对话
4. 自动保存 + 索引
5. 完成！
```

**耗时**: 约 10 秒（无需手动操作）

---

## 🛠️ 故障排查

### 问题 1：剪贴板为空

**原因**: 没有先复制内容

**解决**: 
```
1. 打开豆包对话
2. 选中内容
3. Ctrl+C 复制
4. 再运行脚本
```

### 问题 2：知识库目录不存在

**解决**:
```powershell
New-Item -ItemType Directory -Path "C:\Users\Xiabi\.openclaw\workspace\knowledge-base" -Force
```

### 问题 3：浏览器自动化失败

**原因**: 浏览器未配置或豆包页面结构变化

**解决**:
```
1. 检查浏览器是否运行（端口 18800）
2. 手动检查豆包侧边栏 CSS 选择器
3. 更新脚本中的选择器
```

---

## 📝 文件命名规范

**格式**: `doubao-主题 - 时间戳.md`

**示例**:
```
doubao-网页总结 -2026-03-05-185000.md
doubao-代码审查 -2026-03-05-190000.md
doubao-Python 学习 -2026-03-05-191000.md
```

**优点**:
- ✅ 按时间排序
- ✅ 主题清晰
- ✅ 易于检索

---

## 🔍 检索技巧

保存后可以用这些命令检索：

### PowerShell 搜索
```powershell
# 搜索特定主题
Select-String -Path "knowledge-base\doubao-*.md" -Pattern "网页总结"

# 搜索最近的文件
Get-ChildItem "knowledge-base\doubao-*.md" | Sort-Object LastWriteTime -Descending | Select-Object -First 5
```

### 使用知识库索引
```powershell
# 查看 knowledge-index.md
Get-Content "knowledge-index.md" | Select-String "豆包"
```

---

## 🎉 快速开始

### 现在就试试！

1. **打开豆包**
   ```
   https://www.doubao.com
   ```

2. **随便找个对话，复制内容**

3. **运行脚本**
   ```powershell
   powershell -ExecutionPolicy Bypass -File C:\Users\Xiabi\.openclaw\workspace\save-doubao-automation.ps1
   ```

4. **输入主题**
   ```
   例如：测试对话
   ```

5. **完成！** 文件已保存到知识库

---

## 💡 进阶用法

### 1. 添加标签
在脚本中添加自动标签功能：
```powershell
$tags = Read-Host "输入标签（用空格分隔）"
# 添加到 Markdown 文件
```

### 2. 自动分类
根据对话内容自动分类：
```powershell
if ($conversation -match "代码") {
    $category = "编程"
} elseif ($conversation -match "总结") {
    $category = "学习"
}
```

### 3. 定时同步
配置 cron 任务，每天自动整理：
```
每天 23:00 → 整理当天豆包对话 → 生成摘要
```

---

## 📞 需要帮助？

**遇到问题随时告诉我**，我可以：
- 帮您调试脚本
- 更新 CSS 选择器
- 配置完全自动化版本

---

**Thomas 先生，现在就可以试试剪贴板方案！** 🚀

**打开豆包，复制个对话，运行脚本试试！** 🐾
