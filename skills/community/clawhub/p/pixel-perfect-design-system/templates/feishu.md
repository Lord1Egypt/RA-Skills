# DESIGN.md - 飞书 (Feishu/Lark) Style

> 蓝色企业协作平台，专业高效的企业级应用

---

## 1. Visual Theme & Atmosphere

**设计哲学**: 专业、高效、协作、智能  
**氛围**: 商务、清晰、可靠、现代  
**密度**: 信息密集但井井有条，企业级应用  
**设计语言**: 扁平化设计、清晰的层级、图标驱动  
**目标用户**: 企业用户、团队协作、办公场景  
**品牌个性**: 专业、高效、智能、可靠

### 设计原则

1. **效率优先** - 减少点击，快速完成任务
2. **信息清晰** - 层级分明，一目了然
3. **协作无缝** - 实时协作，流畅沟通

### 视觉隐喻

- **飞书蓝**: 专业、可靠、科技
- **卡片式设计**: 信息组织、清晰分类
- **图标系统**: 快速识别、视觉统一

---

## 2. Color Palette & Roles

### 主色调

| 名称 | Hex | RGB | 角色 |
|------|-----|-----|------|
| `feishu-blue` | #3370FF | rgb(51, 112, 255) | 品牌主色、按钮、链接 |
| `feishu-dark` | #1F2329 | rgb(31, 35, 41) | 主文本 |
| `feishu-bg` | #FFFFFF | rgb(255, 255, 255) | 背景色 |
| `feishu-light` | #F5F6F7 | rgb(245, 246, 247) | 次背景 |

### 辅助色

| 名称 | Hex | 角色 |
|------|-----|------|
| `gray-50` | #F5F6F7 | 背景色 |
| `gray-100` | #EBEDF0 | 边框、分割线 |
| `gray-200` | #D4D6D9 | 禁用状态 |
| `gray-300` | #8F9399 | 占位符 |
| `gray-400` | #646A73 | 次要文本 |
| `gray-500` | #1F2329 | 主文本 |

### 语义色

| 名称 | Hex | 用途 |
|------|-----|------|
| `success` | #00B578 | 成功、在线、已完成 |
| `warning` | #FF7D00 | 警告、待处理 |
| `error` | #F54A45 | 错误、删除、离线 |
| `info` | #3370FF | 信息、提示 |

### 蓝色系

```css
/* 蓝色梯度 */
--blue-50: #EBF1FF;
--blue-100: #C5D8FF;
--blue-200: #9FBFFF;
--blue-300: #79A6FF;
--blue-400: #538DFF;
--blue-500: #3370FF; /* 主色 */
--blue-600: #295ACC;
--blue-700: #1F4399;
--blue-800: #142C66;
--blue-900: #0A1533;
```

### 无障碍访问

- **对比度**: 4.5:1 (AA) 文本对比度
- **色盲友好**: 是
- **焦点指示器**: 蓝色轮廓

---

## 3. Typography Rules

### 字体家族

```css
/* 中文字体系统 */
--font-cn: 'Source Han Sans CN', 'Noto Sans CJK SC', 'PingFang SC', sans-serif;

/* 英文字体系统 */
--font-en: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;

/* 代码字体 */
--font-code: 'Source Code Pro', 'Consolas', monospace;

/* 数字字体 */
--font-number: 'DIN Pro', 'Roboto Mono', monospace;
```

### 字体层级表

| 元素 | 字体 | 大小 | 字重 | 行高 | 字间距 |
|------|------|------|------|------|--------|
| `h1` | 思源黑体 | 24px | 600 | 1.4 | 0 |
| `h2` | 思源黑体 | 20px | 600 | 1.5 | 0 |
| `h3` | 思源黑体 | 18px | 500 | 1.5 | 0 |
| `h4` | 思源黑体 | 16px | 500 | 1.6 | 0 |
| `body-large` | 思源黑体 | 16px | 400 | 1.8 | 0 |
| `body` | 思源黑体 | 14px | 400 | 1.8 | 0 |
| `body-small` | 思源黑体 | 13px | 400 | 1.7 | 0 |
| `caption` | 思源黑体 | 12px | 400 | 1.6 | 0 |

### 中文排版规范

#### 标题

- **H1**: 页面标题、对话框标题
- **H2**: 章节标题、卡片标题
- **H3**: 小节标题、列表标题
- **H4**: 列表项标题、标签

#### 正文

- **Large**: 重要内容、首段
- **Regular**: 正文内容、列表
- **Small**: 辅助说明、元数据
- **Caption**: 时间戳、状态标签

### 中英文混排

```css
/* 中英文混排 */
.mixed-text {
  font-family: 'Source Han Sans CN', 'Inter', sans-serif;
  line-height: 1.8;
  letter-spacing: 0;
}

/* 纯英文 */
.english-text {
  font-family: 'Inter', sans-serif;
  line-height: 1.6;
  letter-spacing: -0.01em;
}

/* 数字强调 */
.number-highlight {
  font-family: 'DIN Pro', monospace;
  font-weight: 500;
}
```

### 特殊排版

```css
/* 文档标题 */
.doc-title {
  font-size: 18px;
  font-weight: 500;
  line-height: 1.5;
  color: #1F2329;
}

/* 用户名 */
.username {
  font-size: 14px;
  font-weight: 500;
  color: #1F2329;
}

/* 时间戳 */
.timestamp {
  font-size: 12px;
  color: #8F9399;
}

/* 在线状态 */
.status-text {
  font-size: 12px;
  font-weight: 500;
}

.status-online {
  color: #00B578;
}

.status-offline {
  color: #8F9399;
}
```

---

## 4. Component Stylings

### 按钮

#### 主按钮

```css
.btn-primary {
  /* 基础样式 */
  background: #3370FF;
  color: #FFFFFF;
  padding: 8px 16px;
  border-radius: 4px;
  font-weight: 500;
  font-size: 14px;
  font-family: 'Source Han Sans CN', sans-serif;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

/* 悬停状态 */
.btn-primary:hover {
  background: #538DFF;
}

/* 激活状态 */
.btn-primary:active {
  background: #295ACC;
}

/* 聚焦状态 */
.btn-primary:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(51, 112, 255, 0.2);
}

/* 禁用状态 */
.btn-primary:disabled {
  background: #C5D8FF;
  cursor: not-allowed;
}
```

#### 次要按钮

```css
.btn-secondary {
  background: #FFFFFF;
  color: #1F2329;
  border: 1px solid #D4D6D9;
  padding: 7px 15px;
  border-radius: 4px;
  font-weight: 500;
  font-size: 14px;
  font-family: 'Source Han Sans CN', sans-serif;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  border-color: #3370FF;
  color: #3370FF;
}
```

#### 文字按钮

```css
.btn-text {
  background: transparent;
  color: #3370FF;
  padding: 8px 12px;
  border-radius: 4px;
  font-weight: 500;
  font-size: 14px;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-text:hover {
  background: #EBF1FF;
}
```

### 输入框

#### 文本输入

```css
.input {
  /* 基础样式 */
  background: #FFFFFF;
  border: 1px solid #D4D6D9;
  border-radius: 4px;
  padding: 8px 12px;
  font-size: 14px;
  font-family: 'Source Han Sans CN', sans-serif;
  color: #1F2329;
  width: 100%;
  transition: all 0.2s ease;
}

/* 占位符 */
.input::placeholder {
  color: #8F9399;
}

/* 聚焦状态 */
.input:focus {
  outline: none;
  border-color: #3370FF;
  box-shadow: 0 0 0 2px rgba(51, 112, 255, 0.1);
}

/* 错误状态 */
.input.error {
  border-color: #F54A45;
}

/* 禁用状态 */
.input:disabled {
  background: #F5F6F7;
  color: #C0C4CC;
  cursor: not-allowed;
}
```

### 卡片

#### 文档卡片

```css
.doc-card {
  background: #FFFFFF;
  border: 1px solid #EBEDF0;
  border-radius: 8px;
  padding: 16px;
  transition: all 0.2s ease;
  cursor: pointer;
}

.doc-card:hover {
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  border-color: #3370FF;
}

.doc-icon {
  width: 32px;
  height: 32px;
  margin-bottom: 12px;
}

.doc-title {
  font-size: 14px;
  font-weight: 500;
  color: #1F2329;
  margin-bottom: 8px;
}

.doc-meta {
  font-size: 12px;
  color: #8F9399;
}
```

#### 消息卡片

```css
.message-card {
  background: #FFFFFF;
  border-radius: 8px;
  padding: 12px 16px;
  display: flex;
  gap: 12px;
}

.message-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  flex-shrink: 0;
}

.message-content {
  flex: 1;
  min-width: 0;
}

.message-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.message-author {
  font-size: 14px;
  font-weight: 500;
  color: #1F2329;
}

.message-time {
  font-size: 12px;
  color: #8F9399;
}

.message-text {
  font-size: 14px;
  line-height: 1.6;
  color: #646A73;
}
```

### 导航

#### 侧边导航

```css
.sidebar {
  background: #FFFFFF;
  border-right: 1px solid #EBEDF0;
  width: 240px;
  height: 100vh;
  overflow-y: auto;
}

.sidebar-header {
  padding: 16px;
  border-bottom: 1px solid #EBEDF0;
}

.nav-section {
  padding: 8px;
}

.nav-section-title {
  font-size: 12px;
  font-weight: 500;
  color: #8F9399;
  padding: 8px 12px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 4px;
  color: #646A73;
  cursor: pointer;
  transition: all 0.2s ease;
}

.nav-item:hover {
  background: #F5F6F7;
}

.nav-item.active {
  background: #EBF1FF;
  color: #3370FF;
}

.nav-icon {
  width: 16px;
  height: 16px;
}

.nav-label {
  font-size: 14px;
  flex: 1;
}
```

#### 顶部导航

```css
.header {
  background: #FFFFFF;
  border-bottom: 1px solid #EBEDF0;
  padding: 0 16px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-title {
  font-size: 16px;
  font-weight: 500;
  color: #1F2329;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}
```

---

## 5. Layout Principles

### 间距系统

| 名称 | 值 | 用途 |
|------|-----|------|
| `xs` | 4px | 图标间距、紧密间距 |
| `sm` | 8px | 小间距、列表项 |
| `md` | 12px | 默认间距 |
| `lg` | 16px | 卡片内边距 |
| `xl` | 24px | 章节间距 |
| `2xl` | 32px | 页面章节 |

### 网格系统

- **列数**: 12
- **间距**: 16px
- **最大宽度**: 1200px
- **侧边栏**: 240px

### 断点定义

```css
--breakpoint-sm: 576px;
--breakpoint-md: 768px;
--breakpoint-lg: 992px;
--breakpoint-xl: 1200px;
--breakpoint-xxl: 1600px;
```

### 布局模式

- **侧边栏 + 内容**: 240px 侧边栏 + 主内容区
- **三栏布局**: 侧边栏 + 内容 + 详情面板
- **卡片网格**: 响应式卡片网格
- **列表视图**: 清晰的列表展示

### 留白哲学

- **适度留白**: 企业应用，不过度留白
- **信息密集**: 最大化信息展示
- **层级清晰**: 通过留白区分层级
- **专业感**: 保持专业商务感

---

## 6. Depth & Elevation

### 阴影系统

```css
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.04);
--shadow-md: 0 2px 8px rgba(0, 0, 0, 0.08);
--shadow-lg: 0 4px 16px rgba(0, 0, 0, 0.12);
--shadow-xl: 0 8px 24px rgba(0, 0, 0, 0.16);
```

### 层级系统

| 名称 | 值 | 用途 |
|------|-----|------|
| `base` | 0 | 默认层级 |
| `dropdown` | 100 | 下拉菜单 |
| `modal` | 200 | 弹窗 |
| `toast` | 300 | 提示消息 |
| `tooltip` | 400 | 工具提示 |

---

## 7. Do's and Don'ts

### ✅ 正确做法

- 使用思源黑体中文字体
- 中文行高保持 1.8
- 使用飞书蓝作为主色
- 保持专业商务风格
- 实现清晰的层级结构
- 使用图标系统
- 保持信息密集但有序
- 实现高效的交互流程
- 使用 4px 圆角按钮
- 保持一致的间距系统

### ❌ 错误做法

- 使用过大的圆角（保持 4px）
- 过度使用动画
- 信息过于稀疏
- 使用过多颜色
- 忽视企业级需求
- 字体层级不清晰
- 图标风格不统一
- 交互流程复杂
- 缺少状态反馈
- 移动端体验差

### 中文排版注意事项

1. **行高**: 企业应用行高可稍低（1.7-1.8）
2. **字重**: 标题使用 500-600，正文 400
3. **颜色**: 深色文字 #1F2329，浅色文字 #646A73
4. **间距**: 段落间距 16px
5. **对齐**: 左对齐为主，标题居中可选

---

## 8. Responsive Behavior

### 断点系统

| 名称 | 最小宽度 | 最大宽度 | 目标设备 |
|------|----------|----------|----------|
| `xs` | 0px | 575px | 手机 |
| `sm` | 576px | 767px | 大屏手机 |
| `md` | 768px | 991px | 平板 |
| `lg` | 992px | 1199px | 小桌面 |
| `xl` | 1200px | ∞ | 大桌面 |

### 响应式策略

```css
/* 移动端: 隐藏侧边栏 */
@media (max-width: 767px) {
  .sidebar { display: none; }
  .mobile-nav { display: block; }
}

/* 平板: 可折叠侧边栏 */
@media (min-width: 768px) and (max-width: 991px) {
  .sidebar { width: 64px; }
}

/* 桌面: 完整侧边栏 */
@media (min-width: 992px) {
  .sidebar { width: 240px; }
}
```

### 折叠策略

- **移动端**: 隐藏侧边栏，使用底部导航
- **平板**: 可折叠侧边栏（64px）
- **桌面**: 完整侧边栏（240px）
- **响应式**: 内容区域自适应

---

## 9. Agent Prompt Guide

### 快速参考

```css
/* 颜色 */
--color-primary: #3370FF;
--color-background: #FFFFFF;
--color-text: #1F2329;
--color-secondary: #646A73;

/* 字体 */
--font-cn: 'Source Han Sans CN', sans-serif;
--font-number: 'DIN Pro', monospace;

/* 间距 */
--spacing-base: 8px;
--border-radius: 4px;

/* 阴影 */
--shadow-md: 0 2px 8px rgba(0, 0, 0, 0.08);
```

### 常用提示词

**创建中文企业应用**:
```
创建一个[页面名称]页面，使用飞书设计风格：
- 飞书蓝主色 #3370FF
- 思源黑体字体，行高 1.8
- 4px 圆角按钮
- 侧边栏 240px
- 专业商务风格
```

**创建组件**:
```
创建一个[组件名称]组件，遵循飞书设计规范：
- 背景色: #FFFFFF
- 边框: 1px solid #EBEDF0
- 圆角: 8px
- 悬停: box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08)
- 中文字体: 思源黑体
```

### 代码模板

#### React 组件（企业应用）

```tsx
import React from 'react';
import styles from './DocCard.module.css';

interface DocCardProps {
  icon: string;
  title: string;
  meta: string;
  onClick?: () => void;
}

export function DocCard({ icon, title, meta, onClick }: DocCardProps) {
  return (
    <div className={styles.card} onClick={onClick}>
      <div className={styles.icon}>{icon}</div>
      <h3 className={styles.title}>{title}</h3>
      <p className={styles.meta}>{meta}</p>
    </div>
  );
}
```

#### CSS Module（企业应用）

```css
.card {
  background: white;
  border: 1px solid #EBEDF0;
  border-radius: 8px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.card:hover {
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  border-color: #3370FF;
}

.icon {
  width: 32px;
  height: 32px;
  margin-bottom: 12px;
}

.title {
  font-size: 14px;
  font-weight: 500;
  color: #1F2329;
  margin-bottom: 8px;
}

.meta {
  font-size: 12px;
  color: #8F9399;
}
```

### AI Agent 指令

生成基于此 DESIGN.md 的 UI 代码时：

1. **使用思源黑体** - 中文字体系统
2. **中文行高 1.8** - 企业应用标准
3. **飞书蓝主色** - #3370FF
4. **专业商务风格** - 不使用过度装饰
5. **清晰的层级** - 信息组织清晰
6. **实现所有状态** - hover、active、disabled
7. **响应式设计** - 移动端适配
8. **高效交互** - 减少点击次数
9. **图标驱动** - 使用图标系统
10. **企业级体验** - 专业可靠

### 组件生成清单

生成组件前，检查：

- [ ] 使用思源黑体
- [ ] 中文行高 1.8
- [ ] 飞书蓝主色
- [ ] 专业商务风格
- [ ] 实现所有交互状态
- [ ] 响应式设计
- [ ] 无障碍访问
- [ ] 清晰的层级结构
- [ ] 高效交互流程
- [ ] 图标系统

---

**飞书设计系统 v2.0.0**  
**最后更新**: 2026-04-09  
**支持语言**: 中文  
**应用类型**: 企业级应用  
**许可证**: MIT
