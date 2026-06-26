---
name: xi-markdown
description: Local Markdown Editor with Live Preview - A web-based markdown editor that opens a Flask server and provides real-time editing with live preview, sync scrolling, and toolbars for all markdown tags.
security: local-only
permissions: file-read, file-write, local-network
risk-level: low
---

# XI Markdown Editor 本地Markdown编辑器

**English** | **中文**

## ⚠️ Security Notice / 安全声明

**English:**  
This skill runs a **local-only** Flask server for markdown editing. It does NOT:
- Connect to external servers (except CDN for libraries)
- Send data outside your local machine
- Require internet access for core functionality
- Execute arbitrary code

**Security Features:**
- Localhost-only server (127.0.0.1)
- No external network connections
- File operations limited to user-specified paths
- All code is open and inspectable

**中文:**  
此技能运行**仅限本地**的Flask服务器进行Markdown编辑。它**不会**：
- 连接到外部服务器（CDN库除外）
- 将数据发送到本地机器之外
- 需要互联网访问核心功能
- 执行任意代码

**安全特性:**
- 仅限本地主机服务器 (127.0.0.1)
- 无外部网络连接
- 文件操作仅限于用户指定的路径
- 所有代码都是开放且可检查的

---

## Overview / 概述

**English:**  
A web-based markdown editor that runs locally with a Flask server and provides real-time editing with live preview. Features include sync scrolling between editor and preview, comprehensive markdown toolbar, and direct file saving.

**中文:**  
基于Web的Markdown编辑器，本地运行Flask服务器，提供实时编辑和预览功能。包括编辑器与预览同步滚动、完整的Markdown工具栏、直接文件保存。无需安装，就可以在本地直接编辑markdown。

---

## Features / 功能特性

**English:**  
- **Real-time Preview**: Edit on left, see live preview on right
- **Sync Scrolling**: Scroll one side, the other follows automatically
- **Toolbar**: Icons for all markdown tags (H1, H2, bold, italic, lists, etc.)
- **File Operations**: Open any markdown file, edit, save back to original file
- **Local Server**: Flask-based backend with RESTful API
- **Responsive Design**: Works on desktop and mobile
- **Dark Theme**: Modern dark UI with white text
- **URL Parameter Support**: Open files via URL parameter `?file=path`
- **Auto Server Shutdown**: Server automatically closes when page is closed
- **Theme Toggle**: Switch between dark and light themes
- **Relative Path Support**: Support for relative paths from workspace

**中文:**  
- **实时预览**: 左侧编辑，右侧实时预览
- **同步滚动**: 滚动一侧，另一侧自动跟随
- **工具栏**: 所有Markdown标签图标（H1、H2、粗体、斜体、列表等）
- **文件操作**: 打开任何markdown文件，编辑后保存回原文件
- **本地服务器**: 基于Flask的后端，提供RESTful API
- **响应式设计**: 支持桌面和移动设备
- **深色主题**: 现代深色UI配白色文字
- **URL参数支持**: 通过URL参数 `?file=路径` 打开文件
- **自动服务器关闭**: 页面关闭时服务器自动关闭
- **主题切换**: 在深色和浅色主题间切换
- **相对路径支持**: 支持相对于工作空间的相对路径

---

## Installation & Setup / 安装与设置

### Requirements / 依赖要求

```bash
pip install flask flask-cors markdown
```

### Quick Start / 快速开始

**English:**  
```bash


# Method 1: Direct Python command with file parameter
python app.py "path\to\your\file.md" --port 996 --force

# Method 2: Open current skill's documentation
python app.py SKILL.md --port 996 --force

# Method 3: Open empty editor
python app.py --port 996 --force

# Method 4: Open via URL parameter in browser
# After starting server, open in browser:
# http://localhost:996/?file=path/to/your/file.md

# Method 5: Using relative path (from workspace)
python app.py "skills\ace-banana2\SKILL.md" --port 996 --force
```

**中文:**  
```bash

# 方法1: 直接Python命令带文件参数
python app.py "文件路径\文件名.md" --port 996 --force

# 方法2: 打开本技能的文档
python app.py SKILL.md --port 996 --force

# 方法3: 打开空编辑器
python app.py --port 996 --force

# 方法4: 通过浏览器URL参数打开
# 启动服务器后，在浏览器中打开：
# http://localhost:996/?file=路径/文件.md

# 方法5: 使用相对路径（相对于工作空间）
python app.py "skills\ace-banana2\SKILL.md" --port 996 --force
```

---

## Usage / 使用方法

### Opening Files / 打开文件

**English:**  
1. **Start editor with a file**:
   ```bash
   python app.py "C:\path\to\file.md"
   ```

2. **Browser automatically opens** with URL parameter:
   - `http://localhost:996/?file=C:\path\to\file.md`
   - URL parameter automatically loads the file

3. **Alternative method**: Direct URL access
   ```
   http://localhost:996/?file=path/to/file.md
   ```
   - Relative paths are supported (from workspace)

4. **Edit file** with toolbar and see live preview

5. **Click "Save"** button to save changes back to original file

**中文:**  
1. **使用文件启动编辑器**：
   ```bash
   python app.py "C:\路径\文件.md"
   ```

2. **浏览器自动打开**并带URL参数：
   - `http://localhost:996/?file=C:\路径\文件.md`
   - URL参数自动加载文件

3. **替代方法**：直接URL访问
   ```
   http://localhost:996/?file=路径/文件.md
   ```
   - 支持相对路径（相对于工作空间）

4. **使用工具栏编辑文件**并查看实时预览

5. **点击"保存"按钮**将更改保存回原文件

### Toolbar Features / 工具栏功能

**Icons available:**
- **H1-H6**: Headers 标题 (with number badges in light theme)
- **B**: Bold 粗体
- **I**: Italic 斜体
- **S**: Strikethrough 删除线
- **Q**: Blockquote 引用
- **Code**: Inline code 行内代码
- **</>**: Code block 代码块
- **List**: Unordered list 无序列表
- **1.**: Ordered list 有序列表
- **Link**: Hyperlink 链接
- **Image**: Insert image 插入图片
- **Table**: Insert table 插入表格
- **HR**: Horizontal rule 水平线
- **🌙/☀️**: Theme toggle 主题切换
- **💾**: Save 保存
- **📁**: Open file 打开文件
- **🔌**: Shutdown server 关闭服务器
- **Undo/Redo**: Undo and redo 撤销/重做

---

## File Structure / 文件结构

```
xi-markdown/
├── SKILL.md                  # This documentation
├── scripts/
│   ├── app.py                # Flask server with API (enhanced)
│   ├── index.html            # Frontend HTML with JavaScript (redesigned)
│   ├── test.md              # Test markdown file
│   └── styles.css            # CSS styles (optional)
└── references/
    └── api_docs.md          # API documentation
```

---

## API Endpoints / API接口

### GET `/`
- Returns the main HTML page
- Supports URL parameter: `?file=path` (opens file via AJAX)

### GET `/api/health`
- Health check endpoint
- Returns: `{"status": "ok", "timestamp": "..."}`

### GET `/api/file`
- Returns current file content
- Query parameter: `path` (file path, supports relative paths)

### POST `/api/file`
- Saves content to file
- JSON body: `{"path": "file_path", "content": "file_content"}`
- Supports relative paths (resolved to workspace)

### GET `/api/preview`
- Converts markdown to HTML for preview
- Query parameter: `markdown` (markdown text)

### GET `/api/open`
- Opens a file in the editor
- Query parameter: `path` (file path, supports relative paths)

### GET `/api/shutdown`
- Shuts down the server
- Called automatically when page closes

---

## Keyboard Shortcuts / 键盘快捷键

- **Ctrl+S**: Save file 保存文件
- **Ctrl+O**: Open file dialog 打开文件对话框
- **Ctrl+Z**: Undo 撤销
- **Ctrl+Y**: Redo 重做
- **Ctrl+B**: Bold 粗体
- **Ctrl+I**: Italic 斜体
- **Ctrl+K**: Insert link 插入链接

---

## New Features / 新功能

### URL Parameter Support / URL参数支持
**English:**  
Open files directly via URL parameter:
```
http://localhost:996/?file=skills/xi-markdown/SKILL.md
```
- URL is automatically encoded
- Supports relative paths from workspace
- AJAX loads file content dynamically

**中文:**  
通过URL参数直接打开文件：
```
http://localhost:996/?file=skills/xi-markdown/SKILL.md
```
- URL自动编码
- 支持相对于工作空间的相对路径
- AJAX动态加载文件内容

### Auto Server Shutdown / 自动服务器关闭
**English:**  
- Server automatically shuts down when page is closed
- Uses `navigator.sendBeacon()` for reliable delivery
- Also supports manual shutdown via 🔌 icon

**中文:**  
- 页面关闭时服务器自动关闭
- 使用 `navigator.sendBeacon()` 确保请求送达
- 也支持通过🔌图标手动关闭

### Theme Support / 主题支持
**English:**  
- Switch between dark and light themes
- H1-H6 icons show number badges in light theme
- Responsive CSS for both themes

**中文:**  
- 在深色和浅色主题间切换
- 浅色主题下H1-H6图标显示数字标记
- 两个主题都有响应式CSS

## Examples / 示例

### Edit a skill's documentation:
```bash
python app.py "skills\a-stock-get\SKILL.md"
# or via URL: http://localhost:996/?file=skills/a-stock-get/SKILL.md
```

### Edit Ace Banana2 skill:
```bash
python app.py "skills\ace-banana2\SKILL.md" --port 996 --force
```

### Edit your own notes:
```bash
python app.py "C:\Users\YourName\notes.md"
```

### Start empty and create new file:
```bash
python app.py
# Then use "Save As" in the editor
```

### Open via URL parameter only:
```bash
# Start server without file
python app.py --port 996 --force
# Then open in browser:
# http://localhost:996/?file=skills/xi-markdown/SKILL.md
```

---

## Notes / 注意事项

**English:**  
- The server runs on `localhost:996` by default
- Only one file can be edited at a time
- Changes are auto-saved locally (in browser) every 30 seconds
- Click "Save" to write to original file
- Server automatically closes when page is closed
- Use `Ctrl+C` to manually stop the server if needed
- URL parameters require URL encoding for special characters

**中文:**  
- 服务器默认运行在 `localhost:996`
- 一次只能编辑一个文件
- 每30秒自动保存到本地（浏览器存储）
- 点击"保存"将写入原文件
- 页面关闭时服务器自动关闭
- 需要时使用 `Ctrl+C` 手动停止服务器
- URL参数中的特殊字符需要URL编码

---

## Development / 开发

### Adding new features:
1. Edit `app.py` for backend changes
2. Edit `index.html` for frontend changes
3. Add new CSS in `<style>` tags or separate file
4. Test with different markdown files

### Debug mode:
```bash
python app.py --debug
```

---

## Todo / 待办事项

- [x] Basic editor with live preview
- [x] Sync scrolling between editor and preview
- [x] Complete markdown toolbar
- [x] File open/save functionality
- [x] URL parameter support for file loading
- [x] Auto server shutdown on page close
- [x] Theme toggle (dark/light)
- [x] Relative path support
- [ ] Auto-save with configurable interval
- [ ] Multiple file tabs
- [ ] Search and replace
- [ ] Export to PDF/HTML
- [ ] Custom themes
- [ ] Plugin system
- [ ] Image upload and management
- [ ] Keyboard shortcut customization

---

## References / 参考资料

- [Markdown Guide](https://www.markdownguide.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Showdown.js](https://github.com/showdownjs/showdown) - Markdown parser
- [CodeMirror](https://codemirror.net/) - Text editor component

---

**Version**: 1.2.0  
**Last Updated**: 2026-03-14  
**Author**: XI Markdown Editor Team
**Email**: zhuxi0906@gmail.com
**Wechat**: jakeycis

### Changelog / 更新日志

#### v1.2.0 (2026-03-14)
- ✅ Added URL parameter support (`?file=path`)
- ✅ Added auto server shutdown on page close
- ✅ Added theme toggle (dark/light)
- ✅ Added relative path support
- ✅ Fixed H1-H6 icon badges in light theme
- ✅ Enhanced API endpoints
- ✅ Improved user experience

#### v1.1.0 (2026-03-14)
- ✅ Redesigned UI with modern toolbar
- ✅ Added sync scrolling
- ✅ Added comprehensive markdown toolbar
- ✅ Added file operations (open/save)

#### v1.0.0 (2026-03-14)
- ✅ Initial release
- ✅ Basic markdown editor with live preview
- ✅ Flask-based local server