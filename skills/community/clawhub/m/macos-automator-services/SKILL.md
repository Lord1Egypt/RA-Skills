---
name: macos-automator-services
description: 部署和使用军舰的 macOS Automator 自动化服务集合。包含 5 个实用工作流：PDF转JPG、PNG重命名并转JPG、图像拼接、解压RAR、顺序命名图像文件。一键安装所有服务到 ~/Library/Services/ 目录。使用场景：(1) "安装我的自动化服务"，(2) "部署所有 Automator 工作流"，(3) "设置快捷操作"，(4) "批量处理图像"，(5) "解压 RAR 文件"。
---

# macOS Automator 自动化服务集合

一键部署军舰的 5 个实用 macOS Automator 工作流，大幅提升日常文件处理效率。

## 服务概览

| 服务名称 | 功能描述 | 依赖 |
|---------|---------|------|
| PDF转JPG | 将 PDF 每页转换为高质量 JPG 图片 | ImageMagick |
| PNG重命名并转JPG | 重命名 PNG 文件并转换为 JPG 格式 | ImageMagick |
| 拼接图像 | 多张图像垂直或水平拼接 | ImageMagick |
| 解压RAR | 一键解压 RAR 压缩文件 | unrar |
| 顺序命名图像文件 | 按选择顺序批量重命名图像 | 无 |

---

## 快速开始

### 1. 安装依赖

```bash
# 安装 ImageMagick（图像处理）
brew install imagemagick

# 安装 unrar（RAR 解压）
brew install unrar
```

### 2. 部署服务

```bash
# 将所有工作流复制到系统服务目录
cp -r assets/*.workflow ~/Library/Services/
```

### 3. 使用服务

1. 在 Finder 中选择文件
2. 右键菜单 → 服务 → 选择对应的服务
3. 按照提示操作即可

---

## 详细使用说明

### 1. PDF转JPG

**功能：** 将 PDF 文件的每一页转换为高质量 JPG 图片，每页单独保存。

**使用场景：**
- 需要从 PDF 中提取图片
- 将 PDF 文档转换为可编辑的图片格式
- 为网页或演示文稿准备 PDF 内容

**使用方法：**
1. 在 Finder 中选择一个或多个 PDF 文件
2. 右键 → 服务 → PDF转JPG
3. 程序会自动：
   - 在 PDF 同级目录创建同名文件夹
   - 将每一页转换为 300 DPI 的高质量 JPG
   - 文件名格式：`{PDF名}-{页码}.jpg`
   - 完成后显示通知

**技术细节：**
- 分辨率：300 DPI
- 图片质量：90%
- 色彩空间：RGB
- 自动跳过非 PDF 文件

---

### 2. PNG重命名并转JPG

**功能：** 将 PNG 文件重命名并转换为 JPG 格式，减小文件体积。

**使用场景：**
- 批量处理屏幕截图
- 为网页优化图片格式
- 统一图片格式和命名

**使用方法：**
1. 在 Finder 中选择一个或多个 PNG 文件
2. 右键 → 服务 → PNG重命名并转JPG
3. 程序会自动处理

---

### 3. 拼接图像

**功能：** 将多张图像垂直或水平拼接成一张大图。

**使用场景：**
- 拼接长截图
- 合并多张设计稿
- 创建对比图
- 制作全景图

**使用方法：**
1. 在 Finder 中选择 2 张或更多图像
2. 右键 → 服务 → 拼接图像
3. 在弹出的对话框中选择拼接方式：
   - **垂直拼接**：从上到下排列
   - **水平拼接**：从左到右排列
4. 拼接后的图像会保存在同一目录

**文件命名：**
- 垂直拼接：`垂直拼接_YYYY-MM-DD HH.MM.SS.{扩展名}`
- 水平拼接：`水平拼接_YYYY-MM-DD HH.MM.SS.{扩展名}`

**支持格式：**
- JPG、PNG、GIF、BMP 等常见图像格式
- 自动保留原始格式
- 自动处理大小写扩展名

---

### 4. 解压RAR

**功能：** 一键解压 RAR 压缩文件。

**使用场景：**
- 快速解压下载的 RAR 文件
- 批量处理多个 RAR 压缩包

**使用方法：**
1. 在 Finder 中选择一个或多个 RAR 文件
2. 右键 → 服务 → 解压RAR
3. 程序会自动解压到同级目录

---

### 5. 顺序命名图像文件

**功能：** 按选择顺序批量重命名图像文件。

**使用场景：**
- 整理照片序列
- 为文档插图统一命名
- 准备网页图片素材

**使用方法：**
1. 在 Finder 中按顺序选择多个图像文件（按住 Command 点击选择）
2. 右键 → 服务 → 顺序命名图像文件
3. 按照提示设置命名规则

---

## 部署指南

### 标准部署

```bash
# 复制所有工作流到系统服务目录
cp -r assets/*.workflow ~/Library/Services/

# 验证安装
ls -la ~/Library/Services/
```

### 自定义部署

如果你只想部署部分服务：

```bash
# 只部署图像拼接
cp -r assets/拼接图像.workflow ~/Library/Services/

# 只部署 PDF 工具
cp -r assets/PDF转JPG.workflow ~/Library/Services/
cp -r assets/PNG重命名并转JPG.workflow ~/Library/Services/
```

### 卸载服务

```bash
# 删除所有服务
rm -rf ~/Library/Services/PDF转JPG.workflow
rm -rf ~/Library/Services/PNG重命名并转JPG.workflow
rm -rf ~/Library/Services/拼接图像.workflow
rm -rf ~/Library/Services/解压RAR.workflow
rm -rf ~/Library/Services/顺序命名图像文件.workflow
```

---

## 故障排除

### ImageMagick 未安装

**错误提示：** "ImageMagick 未安装！"

**解决方案：**
```bash
brew install imagemagick
```

**验证安装：**
```bash
magick --version
```

### unrar 未安装

**错误提示：** 解压 RAR 文件时出错

**解决方案：**
```bash
brew install unrar
```

**验证安装：**
```bash
unrar --version
```

### 服务没有出现在右键菜单中

**解决方案：**
1. 重新启动 Finder
   ```bash
   killall Finder
   ```
2. 或者注销并重新登录
3. 确认工作流已正确复制到 `~/Library/Services/`

### 权限问题

如果遇到权限错误：

```bash
# 修复服务目录权限
chmod -R 755 ~/Library/Services/*.workflow
```

---

## 技术架构

### 工作流结构

每个 `.workflow` 都是一个 macOS Automator 工作流包，包含：

```
服务名.workflow/
├── Contents/
│   ├── Info.plist          # 工作流配置
│   ├── document.wflow      # 工作流定义（XML）
│   └── QuickLook/
│       ├── Preview.png     # 预览图
│       └── Thumbnail.png   # 缩略图
```

### 核心技术栈

- **Automator：** macOS 原生自动化框架
- **Shell Script：** zsh/bash 脚本处理逻辑
- **ImageMagick：** 强大的图像处理工具
- **unrar：** RAR 格式解压工具
- **osascript：** macOS AppleScript 桥接（显示对话框和通知）

### Homebrew 环境加载

所有脚本都自动支持 Apple Silicon 和 Intel 芯片：

```bash
# Apple Silicon (M1/M2/M3)
if [ -f "/opt/homebrew/bin/brew" ]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
fi

# Intel
if [ -f "/usr/local/bin/brew" ]; then
    eval "$(/usr/local/bin/brew shellenv)"
fi
```

---

## 自定义和扩展

### 修改现有工作流

1. 在 Automator 中打开工作流：
   ```bash
   open ~/Library/Services/拼接图像.workflow
   ```

2. 在 Automator 编辑器中修改
3. 保存后立即生效

### 创建新工作流

1. 打开 Automator.app
2. 选择"快速操作"（Quick Action）
3. 添加"运行 Shell 脚本"动作
4. 编写脚本逻辑
5. 保存到 `~/Library/Services/`

### 脚本模板

参考现有工作流的脚本结构：

```bash
#!/bin/bash

# 加载 Homebrew 环境
if [ -f "/opt/homebrew/bin/brew" ]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
fi

# 从 stdin 读取文件
files=()
while IFS= read -r file; do
    files+=("$file")
done

# 处理文件
for file in "${files[@]}"; do
    # 你的逻辑 here
done
```

---

## 使用技巧

### 1. 键盘快捷键

为常用服务设置快捷键：

1. 打开 系统设置 → 键盘 → 键盘快捷键
2. 选择"服务"
3. 找到你的服务，双击右侧添加快捷键

**推荐快捷键：**
- PDF转JPG：`Cmd + Shift + P`
- 拼接图像：`Cmd + Shift + I`
- 解压RAR：`Cmd + Shift + R`

### 2. 批量处理

所有服务都支持批量处理多个文件，选择时按住：
- `Command`：逐个选择
- `Shift`：连续选择

### 3. 智能文件过滤

服务会自动过滤不符合的文件类型：
- PDF转JPG 只处理 .pdf/.PDF 文件
- 其他服务会跳过无法处理的文件

---

## 性能优化

### 大文件处理

对于大文件或大量文件的处理：

1. **PDF转JPG：** 可以降低 DPI 提高速度
   - 修改脚本中的 `-density 300` 为 `-density 150`

2. **图像拼接：** 建议一次不超过 10 张大图
   - 超过 10 张时分批处理

3. **批量操作：** 一次选择 50 个以内文件为宜

---

## 备份和同步

### 备份工作流

```bash
# 备份到其他位置
cp -r ~/Library/Services/ ~/Backup/Automator-Services-$(date +%Y%m%d)/
```

### 跨设备同步

使用 iCloud Drive 或 Dropbox 同步：

```bash
# 链接到 iCloud
ln -s ~/Library/Services/ ~/Library/Mobile\ Documents/com~apple~Automator/Documents/Services
```

---

## 更新日志

### v1.0.0 (2026-03-13)
- ✨ 初始版本
- 📦 包含 5 个核心服务
- 🍎 支持 Apple Silicon 和 Intel 芯片
- 🛡️ 完善的错误处理和用户提示

---

## 参考资源

### Apple 官方文档
- [Automator 用户指南](https://support.apple.com/zh-cn/guide/automator/welcome/mac)
- [macOS 终端命令](https://support.apple.com/zh-cn/guide/terminal/welcome/mac)

### ImageMagick
- [官方文档](https://imagemagick.org/script/)
- [命令行参考](https://imagemagick.org/script/command-line-tools.php)

---

*本技能由军舰精心打造，致力于提升 macOS 用户的文件处理效率！*
