# prototype-design 通用页面原型设计技能

## 简介

基于 58种设计风格（默认figma） UI 的复杂业务系统 HTML 原型开发技能，适用于管理后台页面的快速原型设计。

## 功能特性

- 📋 标准页面结构（Header + 统计卡片 + 筛选条件 + 数据表格）
- 🎨 支持 58+ 设计系统风格（Figma、Linear、Vercel、Notion 等）
- 📝 弹窗设计规范（居中遮罩、表单项样式）
- 📊 看板视图、Tab 切换
- 📱 响应式适配

## 适用场景

1. 创建新的管理页面原型
2. 对照业务文档实现功能模块
3. 设计弹窗和详情页
4. 构建带看板和列表视图的页面

## 使用方法

### 1. 选择设计系统

默认使用 Figma 风格，可根据需求切换：

| 风格 | 设计系统 | 特点 |
|------|---------|------|
| 默认 | `figma-DESIGN.md` | 多彩色、现代 |
| 管理后台 | `linear-DESIGN.md` | 紫色主题、精致 |
| 简约专业 | `vercel-DESIGN.md` | 黑白精准、极简 |
| 温暖风格 | `notion-DESIGN.md` | 暖色极简 |
| 企业级 | `stripe-DESIGN.md` | 紫色渐变、高级感 |

### 2. 参考设计规范

`references/design-systems/` 目录包含 58 种设计风格，参考其颜色、字体、间距等规范进行开发。

### 3. 按照规范开发

参考 SKILL.md 中的组件模板和样式规范进行开发。

## 文件结构

```
prototype-design/
├── SKILL.md                     # 技能核心文档
├── README.md                    # 本文件
└── references/
    ├── page-template.html       # 页面模板参考
    ├── field-norms.md          # 字段规范
    └── design-systems/          # 58种设计风格
        ├── figma-DESIGN.md
        ├── linear-DESIGN.md
        └── ...
```

## 设计系统列表

详见 `design-systems/` 目录，包含：Figma、Linear、Stripe、Vercel、Notion、Airbnb、Spotify、Nvidia、Uber 等 58 种设计系统。

## 注意事项

1. 弹窗 HTML 必须放在页面 div 内部
2. 按钮必须手动绑定 onclick
3. 修改 pages/ 后需要同步到 index.html
4. 使用 Python 脚本做精确替换，避免手动错误

## 经验沉淀

详见 SKILL.md 中的「经验沉淀」章节，包含 WMS 项目实战经验。

---

**版本**：1.0.0  
**更新**：2026-04-17
