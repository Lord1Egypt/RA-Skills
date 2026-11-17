---
name: pdf-to-word
description: "Convert PDF to Word (.docx) via Foxit PhantomPDF/PDF Editor keyboard automation."
---

# PDF 转 Word

通过福昕 PDF 编辑器（Foxit PhantomPDF / Foxit PDF Editor）快捷键操作，将 PDF 转换为同名 Word 文件。

## 前置条件

- 已安装 **福昕 PDF 编辑器**（Foxit PhantomPDF / Foxit PDF Editor）
- 系统语言为中文（菜单快捷键映射基于中文版）
- Windows 系统
- 脚本文件需以 **UTF-8 BOM** 编码保存（已处理）

## 安装路径检测（按优先级）

脚本按以下顺序查找福昕：

1. **硬编码路径** — 6 种常见安装位置
2. **注册表 App Paths** — `HKLM\...\App Paths\Foxit*.exe`，安装程序自动写入，最可靠
3. **注册表 Uninstall** — 卸载信息表，`DisplayName` 匹配 `Foxit + (Phantom|PDF|福昕)`
4. **抛错** — 均未找到则提示用户安装

注册表检测确保即使福昕装在不常见路径也能自动找到。

## 用法

```powershell
# 基本用法 — 转换 PDF 到桌面
skills/pdf-to-word/scripts/convert-pdf-to-word.ps1 -PdfPath "C:\报告.pdf"

# 指定输出目录 + 自动关闭福昕
skills/pdf-to-word/scripts/convert-pdf-to-word.ps1 -PdfPath "C:\报告.pdf" -OutputDir "D:\文档" -CloseAfter

# 强制模式 + 重试（处理大文件或网络盘慢速）
skills/pdf-to-word/scripts/convert-pdf-to-word.ps1 -PdfPath "C:\报告.pdf" -OutputName "12312"

# 强制模式 + 重试（处理大文件或网络盘慢速）
skills/pdf-to-word/scripts/convert-pdf-to-word.ps1 -PdfPath "C:\报告.pdf" -Force -RetryCount 2

# 详细模式（调试用）
skills/pdf-to-word/scripts/convert-pdf-to-word.ps1 -PdfPath "C:\报告.pdf" -Verbose

# 批量转换
Get-ChildItem "C:\docs\*.pdf" | ForEach-Object {
    skills/pdf-to-word/scripts/convert-pdf-to-word.ps1 -PdfPath $_.FullName -CloseAfter
}
```

## 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `-PdfPath` | string | 必填 | PDF 文件路径（支持相对路径） |
| `-OutputDir` | string | 桌面 | 输出目录 |
| `-OutputName` | string | PDF同名 | 自定义输出文件名（不含扩展名） |
| `-CloseAfter` | switch | false | 转换后关闭福昕 |
| `-WaitSeconds` | int | 120 | 最大等待秒数 |
| `-RetryCount` | int | 1 | 超时后重试按键序列次数 |
| `-Force` | switch | false | 强制关闭已有福昕进程 |
| `-Verbose` | switch | — | 显示详细日志 |

## 快捷键映射（中文版福昕）

| 按键 | 操作 |
|------|------|
| `Alt` | 激活菜单/快捷键提示（Key Tips） |
| `B` | 打开"转换"选项卡（Convert） |
| `D` | PDF 转 Word |
| `1` | 选择页面范围（全部页面） |
| `A` | 确认/应用（焦点移到文件名框） |
| `Ctrl+A → Ctrl+V` | 全选 → 粘贴完整输出路径（避免文件已存在弹窗） |
| `Enter` | 执行转换 |

## 完整按键序列

```
Alt → B → D → 1 → A → Ctrl+A → Ctrl+V(输出路径) → Enter
                          ^^^^^^^^^^^^^^^^^^^^^
                          焦点在文件名框，通过剪贴板填入完整输出路径
                          避免中文文件名乱码，同时解决"文件已存在"提示
```

## 工作流程

1. **检测路径** — 查找福昕安装位置（6 种候选路径 → 注册表 App Paths → 注册表 Uninstall）
2. **进程管理** — `-Force` 关闭已有进程，否则复用窗口
3. **启动打开** — 启动福昕并加载 PDF，等待主窗口出现
4. **窗口置前** — 还原窗口（若最小化）并设为前台
5. **构造输出路径** — 根据 `-OutputDir` 或 PDF 目录生成完整输出路径
6. **按键模拟** — 发送 `Alt → B → D → 1 → A` 打开转换对话框
7. **填入文件名** — 焦点在文件名框，`Ctrl+A` 全选 → 剪贴板粘贴输出路径（支持中文）
8. **确认转换** — `Enter`，避免文件已存在弹窗
9. **监听文件** — 轮询桌面/源目录/输出目录，检测 `.docx` 出现
7. **完整性验证** — 确认文件大小稳定不再增长后返回
8. **重试机制** — 超时未检测到时自动重试快捷键序列
9. **清理** — `-CloseAfter` 时自动关闭福昕

## 故障排查

| 问题 | 原因 | 解决方法 |
|------|------|----------|
| 福昕已启动但脚本找不到窗口 | 进程名不匹配 | 使用 `-Verbose` 查看调试日志 |
| 按键按了但没反应 | 窗口焦点丢失 | 转换期间勿移动鼠标/切换窗口 |
| 超时未检测到文件 | 快捷键映射版本差异 | 尝试 `-RetryCount 2` 或手动确认 |
| 文件输出在桌面但脚本未捕获 | 文件名不同 | 检查福昕是否重命名了文件 |
| `Add-Type` 报错 | 类型重复加载 | 已做幂等处理，重跑即可 |
| 控制台中文显示乱码 | 编码问题 | 确保终端支持 UTF-8（`chcp 65001`） |

## 性能提示

- **小文件** (< 10 页): 通常 10-20 秒完成
- **中等文件** (10-50 页): 30-60 秒
- **大文件** (> 50 页): 建议设置 `-WaitSeconds 180`
- 批处理多个文件时，建议串行执行（逐文件处理），避免资源冲突
