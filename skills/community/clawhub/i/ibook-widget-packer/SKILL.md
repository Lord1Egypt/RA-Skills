---
name: ibook-widget-packer
description: 将 H5 游戏项目打包成 Apple iBook 支持的 .wdgt（Widget）格式。适用于：已有 H5 游戏项目（包含 index.html、CSS、JS 等文件），需要打包成 iBook Author 可用的 Widget 压缩包（.wdgt.zip）时使用。自动完成目录结构规范化、资源路径修正、Info.plist 生成、缩略图生成、最终 zip 打包全流程。
metadata:
  author: knot-user
  version: "1.0"
compatibility: Linux/macOS 环境，需要 Python3（用于生成缩略图）、zip 命令行工具。
---

# iBook Widget Packer Skill

## 概述

本 Skill 将任意 H5 游戏项目打包成符合 Apple iBook Author Widget 规范的 `.wdgt` 格式压缩包，可直接导入 iBook Author 使用。

## Widget 包体规范

Apple iBook Widget（`.wdgt`）本质是一个特定结构的文件夹，在 macOS 上显示为 bundle 包。标准结构如下：

```
your-game.wdgt/
├── index.html          ← 主入口文件（必须）
├── Info.plist          ← Widget 配置文件（必须）
├── Default.png         ← 缩略图 1024×768（必须）
├── Default@2x.png      ← 高清缩略图 2048×1536（必须）
└── peresources/        ← 资源文件夹（推荐命名，存放 CSS/JS/图片等）
    ├── style.css
    ├── game.js
    └── ...（其他资源）
```

**关键约束：**
- `index.html` 必须在根目录
- `Info.plist` 必须在根目录，且包含 `MainHTML` 字段指向 `index.html`
- 所有资源路径使用**相对路径**（如 `peresources/style.css`）
- 压缩时文件夹本身要在 zip 顶层（即 zip 内容为 `your-game.wdgt/...`）

---

## 执行步骤

收到用户的打包请求后，按以下步骤执行：

### Step 1：确认源项目路径和输出名称

- 询问或从上下文确认：
  - **源项目目录**（包含 index.html 的目录）
  - **Widget 名称**（将作为 .wdgt 文件夹名，建议英文+连字符，如 `my-game`）
  - **游戏显示名称**（中文可以，用于 Info.plist 的 CFBundleDisplayName）
  - **版本号**（默认 `1.0`）
  - **默认尺寸**（默认 1024×768，适合 iPad 横屏）

### Step 2：分析源项目结构

读取源项目的 `index.html`，确认：
- 引用了哪些 CSS/JS 文件及其路径
- 是否已经有 `peresources` 子目录，还是所有文件平铺在根目录
- 特殊资源（图片、音频、字体等）的位置

### Step 3：创建 Widget 目录结构

```bash
# 创建 wdgt 文件夹
WDGT_DIR="/path/to/output/your-game.wdgt"
mkdir -p "$WDGT_DIR/peresources"

# 将 CSS、JS 等资源文件复制到 peresources/
cp source/style.css source/game.js source/*.js "$WDGT_DIR/peresources/"
```

**路径修正规则：**
- 若源 `index.html` 中引用路径为 `style.css`（平铺），则复制到 `peresources/` 后，`index.html` 中需改为 `peresources/style.css`
- 若源 `index.html` 中已经是 `peresources/style.css`，则路径无需修改，直接复制资源文件到对应位置

### Step 4：生成 index.html（根目录版本）

将修正了资源引用路径的 `index.html` 写入 `your-game.wdgt/index.html`。

**必须包含的 meta 标签（用于全屏适配）：**
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
<meta name="apple-mobile-web-app-capable" content="yes" />
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
```

### Step 5：生成 Info.plist

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleDisplayName</key>
  <string>【游戏中文名】</string>
  <key>CFBundleIdentifier</key>
  <string>com.【英文名小写】.widget</string>
  <key>CFBundleName</key>
  <string>【英文名驼峰】</string>
  <key>CFBundleShortVersionString</key>
  <string>【版本号，如 1.0】</string>
  <key>CFBundleVersion</key>
  <string>【版本号，如 1.0】</string>
  <key>MainHTML</key>
  <string>index.html</string>
  <key>AllowNetworkAccess</key>
  <false/>
  <key>Width</key>
  <integer>1024</integer>
  <key>Height</key>
  <integer>768</integer>
</dict>
</plist>
```

### Step 6：生成缩略图

使用 Python3 + Pillow 生成渐变缩略图（若 Pillow 未安装，先执行 `pip3 install Pillow`）：

```python
from PIL import Image, ImageDraw

def make_thumb(size, path, game_name):
    w, h = size
    img = Image.new('RGB', (w, h))
    draw = ImageDraw.Draw(img)
    # 渐变背景（紫色系）
    for i in range(h):
        r = int(102 + (150-102)*i/h)
        g = int(51 + (75-51)*i/h)
        b = int(153 + (210-153)*i/h)
        draw.line([(0,i),(w,i)], fill=(r,g,b))
    # 中心文字
    cx, cy = w//2, h//2
    draw.text((cx - len(game_name)*7, cy - 10), game_name, fill='white')
    img.save(path)

make_thumb((1024, 768),  'your-game.wdgt/Default.png', '游戏名称')
make_thumb((2048, 1536), 'your-game.wdgt/Default@2x.png', '游戏名称')
```

> 如果需要更好的缩略图效果，可以请用户提供截图，或用 PIL 绘制更精美的预览图。

### Step 7：打包成 zip

```bash
cd /path/to/output/parent
zip -r your-game.wdgt.zip your-game.wdgt/
```

**注意：** 必须先 `cd` 到 wdgt 文件夹的**父目录**，再执行 zip，确保压缩包内顶层是 `your-game.wdgt/` 文件夹。

### Step 8：验证包体结构

```bash
# 查看压缩包内容，确认结构正确
unzip -l your-game.wdgt.zip | head -20
```

期望看到：
```
Archive:  your-game.wdgt.zip
  your-game.wdgt/
  your-game.wdgt/index.html
  your-game.wdgt/Info.plist
  your-game.wdgt/Default.png
  your-game.wdgt/Default@2x.png
  your-game.wdgt/peresources/style.css
  your-game.wdgt/peresources/game.js
  ...
```

### Step 9：提供下载链接

使用 `display_download_links` 工具为用户提供 zip 文件的下载链接。

---

## iBook 使用方式（告知用户）

打包完成后，请告知用户以下使用步骤：

1. **下载** `your-game.wdgt.zip` 到本地 Mac
2. **解压**得到 `your-game.wdgt` 文件夹
3. **重命名确认**：确保文件夹后缀为 `.wdgt`（macOS 会将其识别为 Widget bundle）
4. **导入 iBook Author**：打开 iBook Author → 插入菜单 → Widget → HTML → 拖入 `.wdgt` 文件
5. **预览**：在 iBook Author 中点击预览，或导出到 iPad 的 iBooks App 查看

> ⚠️ **注意**：iBook Author 已于 2020 年停止更新，仅支持旧版 macOS。若用户使用新版系统，建议使用 Apple Pages 或第三方工具替代。

---

## 屏幕适配最佳实践

在 `style.css` 中加入响应式断点，确保游戏在不同设备上自适应：

```css
/* iPad Pro 横屏 (≥1000pt) */
@media screen and (min-width: 1000px) { ... }

/* iPad Pro 竖屏 (768-999pt) */
@media screen and (min-width: 768px) and (max-width: 999px) { ... }

/* iPhone 竖屏 (≤480pt) */
@media screen and (max-width: 480px) { ... }

/* 横屏低高度兼容 */
@media screen and (max-height: 500px) { ... }
```

同时在 `html, body` 加入：
```css
html, body {
  padding-top: env(safe-area-inset-top);
  padding-bottom: env(safe-area-inset-bottom);
}
```

---

## 常见问题排查

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| Widget 在 iBook 中显示空白 | `index.html` 路径错误或资源404 | 检查 `index.html` 在 wdgt 根目录，资源路径使用相对路径 |
| 缩略图不显示 | `Default.png` 尺寸不对 | 确保 320×240 和 640×480 |
| 游戏布局错乱 | 缺少 viewport meta | 添加 `viewport-fit=cover` meta 标签 |
| 音频无法播放 | 浏览器自动播放限制 | 监听用户首次交互事件后再播放音频 |
| zip 结构错误 | 打包路径问题 | 确保从 wdgt 父目录执行 zip 命令 |

---

## 输出清单

每次打包完成，向用户说明：
- ✅ Widget 名称和版本
- ✅ 包体文件列表（`find your-game.wdgt -type f | sort`）
- ✅ zip 文件大小
- ✅ 下载链接
- ✅ iBook 导入使用步骤
