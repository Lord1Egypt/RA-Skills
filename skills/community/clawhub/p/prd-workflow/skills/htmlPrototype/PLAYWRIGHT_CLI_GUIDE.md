# Playwright CLI 使用指南

## ✅ 安装状态

- **Playwright 版本**：v1.58.0
- **CLI 路径**：`~/.nvm/versions/node/v22.22.0/bin/playwright`
- **使用方式**：需要完整路径或添加到 PATH

---

## 🚀 快速使用

### 方式 1：使用完整路径

```bash
~/.nvm/versions/node/v22.22.0/bin/playwright --version
```

### 方式 2：添加到 PATH（推荐）

```bash
# 添加到 ~/.zshrc
echo 'export PATH="$HOME/.nvm/versions/node/v22.22.0/bin:$PATH"' >> ~/.zshrc

# 重新加载
source ~/.zshrc

# 现在可以直接使用
playwright --version
```

### 方式 3：使用 Python 模块

```bash
python3 -m playwright --version
```

---

## 📋 常用命令

### 1. 安装浏览器

```bash
# 安装所有浏览器
playwright install

# 只安装 Chromium
playwright install chromium

# 只安装 Firefox
playwright install firefox

# 只安装 WebKit
playwright install webkit
```

### 2. 截图

```bash
# 截图网页
playwright screenshot https://example.com screenshot.png

# 全屏截图
playwright screenshot --full-page https://example.com full.png

# 指定设备
playwright screenshot --device "iPhone 14" https://example.com mobile.png

# 等待元素后截图
playwright screenshot --wait-for-selector ".content" https://example.com waited.png
```

### 3. 生成 PDF

```bash
# 保存为 PDF
playwright pdf https://example.com page.pdf

# A4 纸张
playwright pdf --paper-size A4 https://example.com a4.pdf
```

### 4. 代码生成器

```bash
# 打开代码生成器
playwright codegen https://example.com

# 生成特定操作的代码
playwright codegen https://example.com --target python
```

### 5. 打开浏览器

```bash
# 打开 Chromium
playwright cr https://example.com

# 打开 Firefox
playwright ff https://example.com

# 打开 WebKit
playwright wk https://example.com
```

### 6. 安装依赖

```bash
# 安装系统依赖（需要 sudo）
playwright install-deps

# 只安装 Chromium 依赖
playwright install-deps chromium
```

### 7. 查看 Trace

```bash
# 查看追踪文件
playwright show-trace trace.zip
```

---

## 💡 实际应用示例

### 批量截图多个页面

```bash
#!/bin/bash

urls=(
    "https://example1.com"
    "https://example2.com"
    "https://example3.com"
)

for url in "${urls[@]}"; do
    filename=$(echo $url | sed 's/https:\/\///' | sed 's/\//_/g')
    playwright screenshot "$url" "${filename}.png"
    echo "✅ 已截图：${filename}.png"
done
```

### 监控网页变化

```bash
#!/bin/bash

URL="https://example.com"
OUTPUT="screenshot.png"

# 第一次截图
playwright screenshot "$URL" "$OUTPUT"

# 等待 1 小时
sleep 3600

# 第二次截图
playwright screenshot "$URL" "screenshot_new.png"

# 比较差异
diff "$OUTPUT" "screenshot_new.png" && echo "无变化" || echo "有变化！"
```

### 生成网页 PDF 存档

```bash
#!/bin/bash

urls=(
    "https://example.com/page1"
    "https://example.com/page2"
    "https://example.com/page3"
)

for url in "${urls[@]}"; do
    filename=$(echo $url | sed 's/https:\/\///' | sed 's/\//_/g')
    playwright pdf --paper-size A4 "$url" "${filename}.pdf"
    echo "✅ 已保存：${filename}.pdf"
done
```

---

## 🎯 在 htmlPrototype 中使用

### 方式 1：CLI 截图

```bash
cd ~/.openclaw/skills/htmlPrototype

# 生成 HTML
python3 main.py "创建一个产品列表页"

# 使用 CLI 截图
playwright screenshot \
    --full-page \
    --viewport-size 1440,900 \
    file://$HOME/Desktop/prototype_list.html \
    $HOME/Desktop/prototype_list.png
```

### 方式 2：Python API（当前使用）

```python
# ~/.openclaw/skills/htmlPrototype/screenshot/capture.py

from playwright.sync_api import sync_playwright

def screenshot(html_path, output_path):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto(f'file://{html_path}')
        page.screenshot(path=output_path, full_page=True)
        browser.close()
```

---

## 🔧 配置选项

### 截图选项

| 选项 | 说明 | 示例 |
|------|------|------|
| `--full-page` | 全屏截图 | `playwright screenshot --full-page url out.png` |
| `--clip` | 裁剪区域 | `playwright screenshot --clip 0,0,800,600 url out.png` |
| `--omit-background` | 透明背景 | `playwright screenshot --omit-background url out.png` |
| `--device` | 模拟设备 | `playwright screenshot --device "iPhone 14" url out.png` |
| `--wait-for-selector` | 等待元素 | `playwright screenshot --wait-for-selector ".content" url out.png` |
| `--wait-for-timeout` | 等待时间 | `playwright screenshot --wait-for-timeout 2000 url out.png` |

### PDF 选项

| 选项 | 说明 | 示例 |
|------|------|------|
| `--paper-size` | 纸张大小 | `playwright pdf --paper-size A4 url out.pdf` |
| `--landscape` | 横向 | `playwright pdf --landscape url out.pdf` |

---

## 🐛 故障排查

### 问题 1：命令未找到

```bash
# 检查 PATH
echo $PATH | grep nvm

# 添加 PATH
export PATH="$HOME/.nvm/versions/node/v22.22.0/bin:$PATH"

# 或使用完整路径
~/.nvm/versions/node/v22.22.0/bin/playwright
```

### 问题 2：浏览器未找到

```bash
# 安装浏览器
playwright install chromium

# 或使用系统 Chrome
playwright screenshot --browser chromium https://example.com out.png
```

### 问题 3：权限问题

```bash
# 添加执行权限
chmod +x ~/.nvm/versions/node/v22.22.0/bin/playwright
```

---

## 📊 CLI vs Python API

| 特性 | CLI | Python API |
|------|-----|-----------|
| **易用性** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **灵活性** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **脚本化** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **调试** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **推荐场景** | 快速截图 | 复杂自动化 |

---

## 💡 最佳实践

### 1. 使用完整路径（避免 PATH 问题）

```bash
PLAYWRIGHT="$HOME/.nvm/versions/node/v22.22.0/bin/playwright"
$PLAYWRIGHT screenshot url out.png
```

### 2. 添加错误处理

```bash
#!/bin/bash

if ! playwright screenshot "$1" "$2"; then
    echo "❌ 截图失败"
    exit 1
fi
echo "✅ 截图成功"
```

### 3. 使用无头模式（更快）

```bash
# CLI 默认就是无头模式
playwright screenshot https://example.com out.png
```

### 4. 等待页面加载

```bash
# 等待网络空闲
playwright screenshot --wait-for-timeout 2000 https://example.com out.png
```

---

## 📚 学习资源

- **官方文档**：https://playwright.dev/python/docs/cli
- **命令参考**：`playwright --help`
- **示例**：`playwright codegen https://example.com`

---

## 🎓 快速参考

```bash
# 版本
playwright --version

# 安装浏览器
playwright install chromium

# 截图
playwright screenshot https://example.com out.png

# 全屏截图
playwright screenshot --full-page https://example.com out.png

# PDF
playwright pdf https://example.com out.pdf

# 代码生成
playwright codegen https://example.com

# 打开浏览器
playwright cr https://example.com
```

---

**Playwright CLI 已就绪！** 🚀
