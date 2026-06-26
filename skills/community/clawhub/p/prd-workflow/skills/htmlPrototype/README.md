# htmlPrototype Skill

OpenClaw 技能 - 高保真 HTML 原型生成器

## 🚀 快速开始

### 在 OpenClaw 中使用

```
用户：创建一个产品列表页
助手：✅ 已生成产品列表页原型
      📁 ~/Desktop/prototype_list.html
      🖼️  ~/Desktop/prototype_list.png
```

### 命令行使用

```bash
cd ~/.openclaw/skills/htmlPrototype

# 生成列表页
python3 main.py "创建一个产品列表页"

# 生成表单页
python3 main.py "创建一个用户表单页" --page form

# 生成仪表盘
python3 main.py "创建一个电商仪表盘" --page dashboard

# 自定义输出
python3 main.py "创建登录页" --output ~/Projects/login

# 不生成截图
python3 main.py "创建列表页" --no-screenshot

# 生成后自动打开
python3 main.py "创建仪表盘" --open
```

## 📋 支持的页面类型

| 类型 | 参数 | 说明 |
|------|------|------|
| 列表页 | `list` | 数据表格、筛选、分页 |
| 表单页 | `form` | 输入框、下拉选择、提交 |
| 仪表盘 | `dashboard` | 数据卡片、图表、统计 |
| 详情页 | `detail` | 详细信息展示 |
| 登录页 | `login` | 登录表单 |

## 🎨 功能特性

- ✅ **快速生成** - 几秒内完成
- ✅ **高保真** - 现代 UI 设计
- ✅ **自动截图** - 使用系统 Chrome
- ✅ **可交互** - HTML 可在浏览器操作
- ✅ **可定制** - 根据关键词调整内容

## 📁 文件结构

```
htmlPrototype/
├── SKILL.md              # 技能说明
├── main.py               # 主入口
├── generator/
│   ├── __init__.py
│   └── templates.py        # HTML 模板
├── screenshot/
│   ├── __init__.py
│   └── capture.py          # 截图工具
└── README.md             # 本文档
```

## 🔧 依赖

- Python 3.8+
- Playwright（用于截图）
- Google Chrome（系统安装）

## 🐛 故障排查

### 截图失败

```bash
# 检查 Chrome 是否安装
ls "/Applications/Google Chrome.app"

# 如果不存在，安装 Chrome
```

### HTML 文件打不开

```bash
# 手动打开
open ~/Desktop/prototype_list.html
```

## 📝 更新日志

### v1.0.0 (2026-02-24)
- ✅ 初始版本
- ✅ 支持 5 种页面类型
- ✅ 自动截图功能

## 💬 反馈

问题或建议？请联系开发者。
