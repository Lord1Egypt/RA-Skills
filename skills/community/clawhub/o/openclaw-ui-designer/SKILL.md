---
name: openclaw-ui-designer
displayName: OpenClaw UI Designer - UI 设计助手
version: 1.0.1
description: |
  OpenClaw UI 设计助手 - 创建美观、易用的用户界面。
  提供设计系统、组件库、配色方案、视觉设计等专业建议。
  支持响应式布局、可访问性（WCAG）、多端适配。所有脚本已包含。
  关键词：openclaw, ui, design, frontend, components, design-system, accessibility
license: MIT-0
acceptLicenseTerms: true
tags:
  - openclaw
  - ui
  - design
  - frontend
  - components
  - design-system
  - accessibility
  - wcag
  - responsive
  - color-palette
---

# UI Designer - UI 设计助手

专业的 UI 设计助手，帮助你创建美观、易用的用户界面。

---

## ✨ 功能特性

- 🎨 **视觉设计** - 配色方案、字体选择、图标设计
- 📐 **布局建议** - 响应式布局、栅格系统、间距规范
- 🧩 **组件设计** - 按钮、表单、卡片、导航等组件设计
- 📚 **设计系统** - 创建设计规范、组件库、样式指南
- ♿ **可访问性** - WCAG 合规、色盲友好、键盘导航
- 📱 **多端适配** - 桌面、平板、移动端设计建议

---

## 🚀 安装

```bash
cd ~/.openclaw/workspace/skills
# 技能已安装在：~/.openclaw/workspace/skills/ui-designer
chmod +x ui-designer/scripts/*.py
```

**就这么简单！所有脚本已包含，无需外部克隆。**

---

## 📖 使用

### 设计咨询

```bash
python3 ui-designer/scripts/design-consult.py "帮我设计一个登录页面"
```

### 配色方案

```bash
python3 ui-designer/scripts/color-palette.py --style modern --primary blue
```

### 组件生成

```bash
python3 ui-designer/scripts/component-gen.py --type button --variant primary
```

---

## 🎯 使用场景

### 何时使用 UI Designer

| 场景 | 推荐使用 |
|------|----------|
| 新建 Web 应用 | ✅ 界面设计、组件选择 |
|  redesign 现有产品 | ✅ 视觉升级、体验优化 |
| 创建设计系统 | ✅ 规范制定、组件库 |
| 移动端适配 | ✅ 响应式设计、触摸优化 |
| 可访问性改进 | ✅ WCAG 合规、无障碍设计 |
| 品牌视觉设计 | ✅ 配色、字体、图标 |

---

## 🛠️ 脚本说明

| 脚本 | 功能 | 网络访问 | 文件写入 |
|------|------|---------|---------|
| `design-consult.py` | 设计咨询 | ❌ 否 | ❌ 否 |
| `color-palette.py` | 配色方案生成 | ❌ 否 | ❌ 否 |
| `component-gen.py` | 组件代码生成 | ❌ 否 | ✅ 可选 |

**注意：** 不存在的脚本已从文档中移除（design-review.py, accessibility-check.py）

---

## 📋 配置

配置文件：
`~/.openclaw/workspace/skills/ui-designer/config/design-config.json`

可配置项：
- 默认设计风格
- 常用配色方案
- 组件库偏好
- 设计工具集成

**文件访问：**
- **读取：** config/design-config.json
- **写入：** 可选，生成组件代码到指定目录

---

## 🎨 设计风格支持

| 风格 | 说明 | 适用场景 |
|------|------|----------|
| Modern | 现代简洁 | SaaS、科技产品 |
| Minimal | 极简主义 | 博客、作品集 |
| Bold | 大胆鲜明 | 创意、营销活动 |
| Corporate | 企业风格 | 企业网站、后台 |
| Playful | 活泼有趣 | 儿童产品、游戏 |
| Luxury | 奢华高端 | 奢侈品、高端品牌 |

---

## 📄 许可证

MIT-0

---

**作者：** @williamwg2025  
**版本：** 1.0.0  
**灵感来源：** [agency-agents/design-ui-designer](https://github.com/msitarzewski/agency-agents/blob/main/design/design-ui-designer.md)

---

## 🔒 安全说明

### 代码来源 ✅
**所有脚本已包含在包内：**
- `design-consult.py` - 设计咨询
- `color-palette.py` - 配色方案
- `component-gen.py` - 组件生成

**无外部依赖：**
- ❌ 不克隆外部仓库
- ❌ 不下载外部代码
- ❌ 不执行远程脚本

### 网络访问
**当前脚本不需要联网：**
- 所有设计建议在本地生成
- 不访问外部 API
- 不加载远程资源

### 文件访问
**读取：**
- `config/design-config.json` - 配置文件
- 用户提供的設計需求（命令行参数）

**写入：**
- `component-gen.py` 可选生成组件代码到指定目录
- 默认不写入文件，除非明确指定输出路径

### 权限要求
- **读取：** `~/.openclaw/workspace/skills/ui-designer/`
- **写入：** 仅当使用 `--output` 参数时
- **无需 root：** 以普通用户身份运行

### 数据安全
- **本地处理：** 所有设计建议在本地生成
- **不上传：** 不发送数据到外部服务器
- **不存储：** 不保留用户输入的设计需求

### 使用建议
1. **检查脚本：** 所有脚本都在 `scripts/` 目录，可自行审查
2. **测试运行：** 先运行简单命令测试行为
3. **指定输出：** 使用 component-gen.py 时明确指定输出目录
4. **不要提供敏感信息：** 设计需求中不要包含 API Key 等敏感数据

---

**作者：** @williamwg2025  
**版本：** 1.0.1  
**许可证：** MIT-0
