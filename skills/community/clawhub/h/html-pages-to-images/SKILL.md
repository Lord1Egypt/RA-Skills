# HTML 页面转图片 Agent Skill

一个 Agent Skill，用于将 HTML 文件中的多个页面元素转换为独立的图片文件。

## 📋 功能

- ✅ 自动识别 HTML 中的页面元素（默认 `.page` 选择器）
- ✅ 为每个页面生成高清截图（2x 分辨率）
- ✅ 根据页面编号自动命名输出文件
- ✅ 支持自定义参数配置
- ✅ 可作为 Agent Skill 被调用

## 📦 安装

```bash
npm install
```

## 🚀 使用方法

### 作为 Agent Skill 使用

```javascript
import { execute } from './index.js';

const result = await execute({
  htmlFile: 'xiaohongshu-articles.html',
  outputDir: 'output',
  pageWidth: 375,
  pageHeight: 667,
  selector: '.page'
});

console.log(result);
```

### 直接运行

```bash
npm run convert
```

或者：

```bash
node index.js
```

## 📁 项目结构

```
.
├── index.js              # Skill 主入口文件
├── skill.json           # Skill 配置文件
├── lib/
│   └── convert-pages.js # 核心转换逻辑
├── convert-pages.js     # 旧版脚本（保留兼容）
├── package.json
└── README.md
```

## ⚙️ 参数配置

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `htmlFile` | string | `xiaohongshu-articles.html` | HTML 文件路径（相对或绝对） |
| `outputDir` | string | `output` | 输出图片的目录 |
| `pageWidth` | number | `375` | 页面宽度（像素） |
| `pageHeight` | number | `667` | 页面高度（像素） |
| `selector` | string | `.page` | 要截图的页面元素选择器 |

## 📤 输出

所有图片将保存在 `output` 目录下，文件命名格式为：
- `page-01.png` (封面页)
- `page-02.png` (第一个内页)
- `page-03.png` (第二个内页)
- ...

## 📊 返回值

```javascript
{
  success: true,
  message: "成功转换 7 个页面为图片",
  data: {
    images: ["output/page-01.png", "output/page-02.png", ...],
    count: 7,
    outputDir: "/path/to/output"
  }
}
```

## 🔧 作为 Agent Skill 集成

1. 将整个目录复制到 Agent 的 skills 目录
2. 在 Agent 配置中引用此 skill
3. 通过 `execute()` 函数调用，传入所需参数

## 📝 示例

```javascript
// 使用默认配置
const result1 = await execute();

// 自定义 HTML 文件
const result2 = await execute({
  htmlFile: './my-article.html'
});

// 完全自定义
const result3 = await execute({
  htmlFile: '/absolute/path/to/article.html',
  outputDir: './screenshots',
  pageWidth: 800,
  pageHeight: 1200,
  selector: '.article-page'
});
```
