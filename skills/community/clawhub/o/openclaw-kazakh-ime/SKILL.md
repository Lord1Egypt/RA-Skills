# OpenClaw Kazakh IME - 哈萨克语输入法

> **版本**: 1.3.0  
> **创建日期**: 2026-04-06  
> **作者**: OpenClaw Team  
> **位置**: `skills/openclaw-kazakh-ime/`

---

## 📋 技能描述

为 OpenClaw 和任何网页添加哈萨克语输入法支持，支持**阿拉伯文**和**西里尔文**两种哈萨克文字书写系统。

---

## 🎯 触发条件

当用户提到以下内容时激活此技能：
- "哈萨克语输入法"
- "Kazakh IME"
- "阿拉伯文输入"
- "西里尔文输入"
- "قا" / "қ" 输入
- "在网页中输入哈萨克语"

---

## 🚀 核心功能

### 三种输入模式
1. **英文模式** - 默认模式，正常英文输入
2. **阿拉伯文模式** - 哈萨克语阿拉伯文字符输入 (قا)
3. **西里尔文模式** - 哈萨克语西里尔文字符输入 (қ)

### 切换方式
- **快捷键**: `Ctrl+Shift+K` 循环切换三种模式
- **状态按钮**: 点击右下角状态按钮切换

### 虚拟键盘
- 可拖动的虚拟键盘
- 支持触屏设备
- 一键显示/隐藏

---

## 📦 安装方法

### 1. 复制文件到目标位置

```powershell
# 复制输入法脚本到 OpenClaw 控制 UI 目录
Copy-Item "C:\Users\Administrator\.openclaw\workspace\skills\openclaw-kazakh-ime\scripts\openclaw-kazakh-ime.js" `
  "C:\Users\Administrator\AppData\Roaming\npm\node_modules\openclaw\dist\control-ui\" -Force
```

### 2. 修改 index.html

在 `</body>` 标签之前添加：

```html
<script src="./openclaw-kazakh-ime.js"></script>
```

**完整示例:**
```html
<body>
  <openclaw-app></openclaw-app>
  <script src="./openclaw-kazakh-ime.js"></script>
</body>
```

### 3. 刷新页面

刷新浏览器，输入法自动生效。

---

## 🎹 键盘映射表

### 阿拉伯文模式 (قا)

| 英文键 | 哈萨克字符 | 英文键 | 哈萨克字符 |
|--------|-----------|--------|-----------|
| q | چ | w | ۋ |
| e | ء | r | ر |
| t | ت | y | ي |
| u | ۇ | i | ڭ |
| o | و | p | پ |
| a | ھ | s | س |
| d | د | f | ا |
| g | ە | h | ى |
| j | ق | k | ك |
| l | ل | z | ز |
| x | ش | c | ع |
| v | ۆ | b | ب |
| n | ن | m | م |

### 西里尔文模式 (қ)

| 英文键 | 哈萨克字符 | 英文键 | 哈萨克字符 |
|--------|-----------|--------|-----------|
| q | қ | w | ў |
| e | е | r | р |
| t | т | y | у |
| u | ү | i | і |
| o | о | p | п |
| a | а | s | с |
| d | д | f | ф |
| g | ғ | h | һ |
| j | ж | k | к |
| l | л | z | з |
| x | х | c | ц |
| v | в | b | б |
| n | н | m | м |

---

## 💡 使用示例

### 场景 1: 在 OpenClaw 聊天中输入哈萨克语

1. 按 `Ctrl+Shift+K` 切换到阿拉伯文模式
2. 使用英文键盘输入，自动转换为哈萨克语
3. 例如：输入 "salem" → 输出 "سەلەم"

### 场景 2: 切换西里尔文模式

1. 按 `Ctrl+Shift+K` 切换到西里尔文模式
2. 输入 "salem" → 输出 "сәлем"

### 场景 3: 使用虚拟键盘

1. 点击右下角 ⌨ 按钮显示虚拟键盘
2. 拖动 ☰ 区域调整位置
3. 点击按键直接输入

---

## 🔧 配置选项

### 字体设置

在 `openclaw-kazakh-ime.js` 文件开头修改：

```javascript
const FONT_SETTINGS = {
    arabic: 'UKK TZK1, Microsoft Uighur, sans-serif',
    cyrillic: 'UKK TZK1, sans-serif',
    english: ''
};
```

### 推荐字体
- **UKK TZK1** - 哈萨克语专用字体（推荐）
- **Microsoft Uighur** - 支持阿拉伯文

---

## 📁 文件结构

```
skills/openclaw-kazakh-ime/
├── SKILL.md              # 技能说明文件
├── scripts/
│   └── openclaw-kazakh-ime.js  # 输入法主文件
└── references/
    └── README.md         # 完整文档（可选）
```

---

## ⚠️ 注意事项

1. **文件路径** - 确保 JS 文件路径正确
2. **适用元素** - 仅对 `input[type="text"]` 和 `textarea` 生效
3. **字体支持** - 需安装哈萨克语字体（如 UKK TZK1）
4. **浏览器** - 推荐 Chrome/Edge/Firefox

---

## 🔄 更新日志

### v1.3.0 (2026-04-06)
- ✅ 新增西里尔文模式
- ✅ 循环模式切换
- ✅ 虚拟键盘支持
- ✅ 优化组合键处理

### v1.2.0
- ✅ 添加虚拟键盘

### v1.1.0
- ✅ 修复大写字母映射

### v1.0.0
- ✅ 初始版本（阿拉伯文模式）

---

## 📞 调用命令

```bash
# 安装输入法
"安装哈萨克语输入法"

# 查看使用方法
"哈萨克语输入法怎么用？"

# 切换输入模式
"切换到阿拉伯文模式"
"切换到西里尔文模式"

# 查看键盘映射
"显示哈萨克语键盘映射表"
```

---

## 🔗 相关链接

- **GitHub 仓库**: https://github.com/ayden76/openclaw-kazakh-ime
- **ClawHub**: 待发布
- **文档**: `references/README.md`

---

*OpenClaw Kazakh IME - 为哈萨克语用户提供便捷的输入体验！💚*
