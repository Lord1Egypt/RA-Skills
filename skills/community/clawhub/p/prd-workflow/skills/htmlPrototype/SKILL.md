---
name: htmlPrototype
description: Generate high-fidelity HTML prototypes from natural language descriptions. Supports list pages, forms, dashboards, and more with automatic screenshot generation.
homepage: https://docs.openclaw.ai
metadata: {"clawdbot":{"emoji":"🎨","requires":{"bins":["python3"]},"primaryEnv":"PYTHONPATH"}}
---

# HTML Prototype Generator

从自然语言描述生成**高保真 HTML 原型**，支持自动截图。

## 🚀 功能

- ✅ **快速生成** - 从描述到原型只需几秒
- ✅ **高保真** - 现代 UI 设计，接近真实产品
- ✅ **自动截图** - 使用系统 Chrome，无需下载浏览器
- ✅ **可交互** - HTML 文件可在浏览器中查看和操作
- ✅ **多页面** - 支持列表页、表单页、仪表盘等

## 💬 使用示例

### 方式 1：从需求文档生成（推荐）

```
用户：[上传 PRD 文档] 根据这个需求文档生成原型

助手：📄 正在读取需求文档：requirements.md
      📋 从文档提取:
         页面类型：列表页
         关键词：产品、销售、库存
         组件：表格、筛选、分页
         风格：商务专业
      
      💡 建议:
         - 建议包含：搜索框、表格、分页器
         - 表格建议显示：名称、价格、状态
         - 筛选条件：关键词、状态下拉
      
      ✅ 已生成原型
      📁 ~/Desktop/prototype_from_prd.html
      🖼️ ~/Desktop/prototype_from_prd.png
```

### 简单模式（快速生成）

```
用户：创建一个产品列表页
助手：✅ 已生成产品列表页原型
      📁 ~/Desktop/prototype_list.html
      🖼️ ~/Desktop/prototype_list.png
```

### 交互模式（推荐，多轮问答）

```
用户：创建一个产品列表页 --interactive

助手：📋 让我问几个问题，帮您更好地定制原型：
      ════════════════════════════════════════════
      
      [1/5] 您希望使用什么风格？
      1️⃣ 现代简约（默认）
      2️⃣ 商务专业
      3️⃣ 活泼清新
      您的选择 [回车使用默认]: 2
      
      [2/5] 表格需要显示哪些列？（用逗号分隔）
      您的选择：产品名称，价格，库存，状态，操作
      
      [3/5] 需要哪些筛选条件？
      1️⃣ 搜索框
      2️⃣ 下拉选择
      3️⃣ 日期选择
      4️⃣ 都需要（默认）
      您的选择：4
      
      [4/5] 需要哪些操作按钮？
      1️⃣ 新建
      2️⃣ 导出
      3️⃣ 批量删除
      4️⃣ 都需要（默认）
      您的选择：4
      
      [5/5] 产品类型？
      1️⃣ 实物商品（默认）
      2️⃣ 虚拟商品
      3️⃣ 服务
      您的选择：1
      
      ✅ 好的，马上为您生成！
      
      📄 生成 HTML...
      🎨 应用定制选项...
      ✅ 已生成商务专业风格的产品列表页
      📁 ~/Desktop/prototype_list.html
      🖼️ ~/Desktop/prototype_list.png
```

### 高级模式（指定参数）

```
用户：创建一个电商仪表盘，包含销售数据卡片、趋势图、订单表格
助手：✅ 已生成电商仪表盘原型
      📊 包含：4 个数据卡片、2 个图表、订单表格
      🎨 风格：现代简约，蓝色主题
      📁 ~/Desktop/ecommerce_dashboard.html
```

## 📋 支持的页面类型

| 类型 | 命令 | 说明 |
|------|------|------|
| **列表页** | `list` | 数据表格、筛选、分页 |
| **表单页** | `form` | 输入框、下拉选择、提交按钮 |
| **仪表盘** | `dashboard` | 数据卡片、图表、统计 |
| **详情页** | `detail` | 详细信息展示 |
| **登录页** | `login` | 登录表单、记住密码 |

## 🔧 配置

### 环境变量（可选）

```bash
# 自定义输出目录
export HTMLPROTOTYPE_OUTPUT=~/Projects/prototypes

# 自定义截图尺寸
export HTMLPROTOTYPE_WIDTH=1920
export HTMLPROTOTYPE_HEIGHT=1080

# 是否自动截图
export HTMLPROTOTYPE_SCREENSHOT=true
```

## 📁 文件结构

```
htmlPrototype/
├── SKILL.md              # 技能说明（本文件）
├── main.py               # 主入口
├── generator/
│   ├── __init__.py
│   ├── html_generator.py   # HTML 生成
│   └── templates.py        # 页面模板
├── screenshot/
│   ├── __init__.py
│   └── capture.py          # 截图工具
├── templates/
│   ├── list_page.html
│   ├── form_page.html
│   ├── dashboard.html
│   └── detail_page.html
└── assets/
    └── styles.css          # 公共样式
```

## 💡 最佳实践

### 1. 使用交互模式（推荐）

**交互模式会自动问您 5-7 个问题**，帮您明确需求：

```bash
python3 main.py "创建一个产品列表页" --interactive
# 或简写
python3 main.py "创建一个产品列表页" -i
```

**好处**：
- ✅ 不用一次性想清楚所有细节
- ✅ 系统引导您做决定
- ✅ 避免遗漏重要功能
- ✅ 生成更精准的原型

### 2. 简单模式：描述要具体

**好**：
> "创建一个产品列表页，包含产品名称、价格、库存、状态，支持筛选和分页"

**不好**：
> "做个列表页"

### 3. 指定样式偏好

```
用户：创建一个登录页，使用紫色主题，现代简约风格
```

### 4. 说明组件需求

```
用户：创建一个仪表盘，需要：
- 4 个数据卡片（销售额、订单数、用户数、转化率）
- 销售趋势图
- 最近订单表格
- 顶部导航和左侧菜单
```

### 5. 多轮迭代

```
第一轮：创建一个列表页 → 查看效果
第二轮：把紫色改成蓝色，增加导出按钮
第三轮：调整表格列，增加状态筛选
```

## 🎨 自定义模板

### 添加新页面类型

1. 在 `templates/` 目录创建 HTML 文件
2. 在 `generator/templates.py` 添加映射
3. 测试生成

### 修改样式

编辑 `assets/styles.css`：

```css
/* 修改主题色 */
:root {
  --primary-color: #667eea;
  --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

## 🐛 故障排查

### 问题 1：截图失败

```bash
# 检查 Chrome 是否安装
ls "/Applications/Google Chrome.app"

# 如果不存在，安装 Chrome 或使用 Firefox
```

### 问题 2：HTML 文件打不开

```bash
# 检查文件路径
ls -l ~/Desktop/prototype_*.html

# 用浏览器打开
open ~/Desktop/prototype_list.html
```

### 问题 3：样式不显示

确保 HTML 文件完整生成，检查 `<style>` 标签是否存在。

## 📊 输出说明

### HTML 文件

- **格式**：完整 HTML5 文档
- **样式**：内联 CSS，无需外部文件
- **交互**：支持点击、输入等基础交互
- **大小**：通常 10-50KB

### PNG 截图

- **格式**：PNG（透明背景）
- **分辨率**：1440x900（可配置）
- **大小**：通常 100-500KB
- **质量**：高清（2x 缩放）

## 🔗 相关技能

- **drawio** - 流程图绘制
- **prd-writer** - PRD 文档编写
- **browser** - 浏览器自动化

## 📝 更新日志

### v1.0.0 (2026-02-24)
- ✅ 初始版本
- ✅ 支持 4 种页面类型
- ✅ 自动截图功能
- ✅ 使用系统 Chrome，无需下载

## 💬 社区

遇到问题？提交 Issue 或参与讨论：
- GitHub: https://github.com/openclaw/skills
- Discord: https://discord.gg/clawd

---

**Happy Prototyping! 🎨**
