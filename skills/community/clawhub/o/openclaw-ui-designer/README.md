# UI Designer - UI 设计助手

专业的 UI 设计助手，帮助你创建美观、易用的用户界面。

[English Version](README_EN.md)


## 🎯 推荐安装场景

✅ **你应该安装这个技能，如果：**
- [ ] 你需要 UI 设计建议
- [ ] 你想创建设计系统
- [ ] 你需要配色方案
- [ ] 你关注可访问性

❌ **不需要安装，如果：**
- [ ] 你是专业设计师
- [ ] 你不需要设计建议

---

## ⭐ 觉得好用？

如果喜欢这个技能，请：
1. 在 ClawHub 给个 **⭐⭐⭐⭐⭐ 5 星好评**
2. 分享给其他 OpenClaw 用户
3. 提交 Issue 或 PR 改进

**你的评分对我们很重要！** 帮助更多人发现这个技能。

---

## 🔗 相关技能推荐

安装了这个技能的用户也安装了：

| 技能 | 作用 | 推荐度 |
|------|------|--------|
| [webnovel-writer](../webnovel-writer) | 网文写作 | ⭐⭐⭐⭐ |
| [memory-enhancer](../memory-enhancer) | 增强记忆 | ⭐⭐⭐ |
| [search-pro](../search-pro) | 联网搜索 | ⭐⭐⭐ |

**推荐组合安装：**
```bash
npx clawhub install openclaw-webnovel-writer
npx clawhub install openclaw-memory-enhancer
npx clawhub install openclaw-search-pro
```

---


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

---

## 📖 使用

### 设计咨询

```bash
# 登录页面设计
python3 ui-designer/scripts/design-consult.py "帮我设计一个登录页面"

# 后台管理系统
python3 ui-designer/scripts/design-consult.py "后台管理系统界面设计"
```

### 配色方案

```bash
# 现代风格
python3 ui-designer/scripts/color-palette.py --style modern

# 极简风格 + 蓝色主色
python3 ui-designer/scripts/color-palette.py --style minimal --primary blue

# 奢华风格
python3 ui-designer/scripts/color-palette.py --style luxury
```

### 组件生成

```bash
# 主按钮
python3 ui-designer/scripts/component-gen.py --type button --variant primary

# 卡片组件
python3 ui-designer/scripts/component-gen.py --type card --variant with-image

# 登录表单
python3 ui-designer/scripts/component-gen.py --type form --variant login
```

---

## 🎯 使用场景

| 场景 | 推荐使用 |
|------|----------|
| 新建 Web 应用 | ✅ 界面设计、组件选择 |
| 重新设计现有产品 | ✅ 视觉升级、体验优化 |
| 创建设计系统 | ✅ 规范制定、组件库 |
| 移动端适配 | ✅ 响应式设计、触摸优化 |
| 可访问性改进 | ✅ WCAG 合规、无障碍设计 |
| 品牌视觉设计 | ✅ 配色、字体、图标 |

---

## 🎨 设计风格

| 风格 | 说明 | 适用场景 |
|------|------|----------|
| Modern | 现代简洁 | SaaS、科技产品 |
| Minimal | 极简主义 | 博客、作品集 |
| Bold | 大胆鲜明 | 创意、营销活动 |
| Corporate | 企业风格 | 企业网站、后台 |
| Playful | 活泼有趣 | 儿童产品、游戏 |
| Luxury | 奢华高端 | 奢侈品、高端品牌 |

---

## 🛠️ 脚本说明

| 脚本 | 功能 |
|------|------|
| `design-consult.py` | 设计咨询 |
| `color-palette.py` | 配色方案生成 |
| `component-gen.py` | 组件代码生成 |

---

## 📋 配置

配置文件：
`~/.openclaw/workspace/skills/ui-designer/config/design-config.json`

可配置项：
- 默认设计风格
- 常用配色方案
- 组件库偏好
- 设计工具集成

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
**所有脚本已包含：** design-consult.py, color-palette.py, component-gen.py
- ❌ 不克隆外部仓库
- ❌ 不下载外部代码

### 网络访问
- **不联网：** 所有设计建议在本地生成

### 文件访问
- **读取：** config/design-config.json
- **写入：** 仅当使用 --output 参数时

### 数据安全
- **本地处理：** 不发送数据到外部
- **不存储：** 不保留用户输入

### 使用建议
1. 检查 scripts/ 目录脚本
2. 先测试简单命令
3. 不要提供敏感信息

---

**作者：** @williamwg2025  
**版本：** 1.0.1  
**许可证：** MIT-0
