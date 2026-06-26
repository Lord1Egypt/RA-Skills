# DESIGN.md - 微信 (WeChat) Style

> 超级应用，绿色简洁，十亿用户的极致体验

---

## 1. Visual Theme & Atmosphere

**设计哲学**: 简洁、克制、实用、连接  
**氛围**: 友好、温和、可靠、日常  
**密度**: 信息密集但清晰，功能至上  
**设计语言**: 极简主义、扁平化、图标驱动  
**目标用户**: 全年龄段用户、日常沟通、生活服务  
**品牌个性**: 可靠、温和、连接、克制

### 设计原则

1. **极简主义** - 去除一切不必要元素
2. **功能至上** - 每个设计都服务于功能
3. **克制表达** - 不过度设计，保持克制

### 视觉隐喻

- **微信绿**: 生命力、希望、连接
- **极简界面**: 清晰、专注、效率
- **圆角卡片**: 友好、温和、现代

---

## 2. Color Palette & Roles

### 主色调

| 名称 | Hex | RGB | 角色 |
|------|-----|-----|------|
| `wechat-green` | #07C160 | rgb(7, 193, 96) | 品牌主色、发送、成功 |
| `wechat-bg` | #EDEDED | rgb(237, 237, 237) | 背景色 |
| `wechat-text` | #191919 | rgb(25, 25, 25) | 主文本 |
| `wechat-secondary` | #888888 | rgb(136, 136, 136) | 次要文本 |

### 辅助色

| 名称 | Hex | 角色 |
|------|-----|------|
| `gray-100` | #F7F7F7 | 背景色 |
| `gray-200` | #E5E5E5 | 分割线 |
| `gray-300` | #CCCCCC | 禁用状态 |
| `white` | #FFFFFF | 卡片背景 |

### 语义色

| 名称 | Hex | 用途 |
|------|-----|------|
| `success` | #07C160 | 成功、发送 |
| `warning` | #FA9D3B | 警告 |
| `error` | #FA5151 | 错误、删除 |
| `info` | #10AEFF | 信息、链接 |

### 无障碍访问

- **对比度**: 4.5:1 (AA)
- **色盲友好**: 是
- **焦点指示器**: 绿色轮廓

---

## 3. Typography Rules

### 字体家族

```css
/* 中文字体 */
--font-cn: -apple-system, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;

/* 英文字体 */
--font-en: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

### 字体层级表

| 元素 | 大小 | 字重 | 行高 |
|------|------|------|------|
| `h1` | 20px | 600 | 1.4 |
| `h2` | 18px | 600 | 1.5 |
| `h3` | 16px | 500 | 1.5 |
| `body` | 16px | 400 | 1.6 |
| `caption` | 14px | 400 | 1.5 |

---

## 4. Component Stylings

### 按钮

```css
.btn-primary {
  background: #07C160;
  color: #FFFFFF;
  padding: 10px 24px;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 500;
  border: none;
  cursor: pointer;
}

.btn-primary:hover {
  background: #06AD56;
}

.btn-secondary {
  background: #F7F7F7;
  color: #191919;
  border: none;
  padding: 10px 24px;
  border-radius: 4px;
  font-size: 16px;
}
```

### 输入框

```css
.input {
  background: #FFFFFF;
  border: none;
  border-bottom: 1px solid #E5E5E5;
  padding: 12px 0;
  font-size: 16px;
  color: #191919;
}

.input:focus {
  outline: none;
  border-bottom-color: #07C160;
}
```

### 卡片

```css
.card {
  background: #FFFFFF;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}
```

---

## 5. Layout Principles

### 间距系统

| 名称 | 值 | 用途 |
|------|-----|------|
| `xs` | 4px | 图标间距 |
| `sm` | 8px | 小间距 |
| `md` | 16px | 默认间距 |
| `lg` | 24px | 大间距 |
| `xl` | 32px | 章节间距 |

### 网格系统

- **最大宽度**: 无限制（响应式）
- **边距**: 16px

---

## 6. Depth & Elevation

### 阴影系统

```css
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
--shadow-md: 0 2px 8px rgba(0, 0, 0, 0.08);
--shadow-lg: 0 4px 12px rgba(0, 0, 0, 0.1);
```

### z-index

- `base`: 0
- `dropdown`: 10
- `modal`: 20
- `toast`: 30

---

## 7. Do's and Don'ts

### ✅ 正确做法

- 保持极简设计
- 使用微信绿色作为主色
- 中文行高 1.6-1.8
- 使用圆角 4-8px
- 功能至上

### ❌ 错误做法

- 过度装饰
- 使用过多颜色
- 复杂的动画
- 忽视老年用户体验
- 信息过载

---

## 8. Responsive Behavior

### 断点

- `mobile`: 0-767px
- `desktop`: 768px+

### 触摸目标

- **最小尺寸**: 44px × 44px

---

## 9. Agent Prompt Guide

### 快速参考

```css
--color-primary: #07C160;
--color-background: #EDEDED;
--color-text: #191919;
--font-cn: 'PingFang SC', sans-serif;
--border-radius: 4px;
```

### 常用提示词

```
创建一个微信风格的聊天页面：
- 微信绿 #07C160
- 极简设计
- 圆角 4px
- 功能至上
```

### AI Agent 指令

1. 使用 PingFang SC 字体
2. 微信绿色主色
3. 极简设计
4. 功能至上
5. 实现所有状态

---

**微信设计系统 v2.0.0**  
**最后更新**: 2026-04-09
