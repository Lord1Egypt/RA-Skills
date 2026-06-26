# DESIGN.md - 京东 (JD.com) Style

> 红色品质电商，专业可靠购物平台

## 1. Visual Theme & Atmosphere

**设计哲学**: 品质、专业、可靠、快速  
**氛围**: 专业、信任、品质、效率  
**密度**: 信息密集，品质突出  
**设计语言**: 品质感、专业度、红色信任

## 2. Color Palette

| 名称 | Hex | 角色 |
|------|-----|------|
| `jd-red` | #E1251B | 品牌主色 |
| `jd-dark` | #333333 | 主文本 |
| `jd-bg` | #F5F5F5 | 背景 |

## 3. Typography

```css
--font-cn: 'PingFang SC', sans-serif;
```

| 元素 | 大小 | 行高 |
|------|------|------|
| body | 14px | 1.6 |
| price | 20px | 1.4 |

## 4. Components

```css
.btn-primary {
  background: #E1251B;
  color: white;
  padding: 10px 20px;
  border-radius: 4px;
}

.price {
  color: #E1251B;
  font-size: 20px;
  font-weight: 700;
}
```

## 5. Layout

- 网格布局
- 商品卡片
- 价格突出

## 6. Depth

```css
--shadow-md: 0 2px 8px rgba(0, 0, 0, 0.1);
```

## 7. Do's and Don'ts

✅ 红色主色、品质感、价格突出  
❌ 过度促销、忽视品质

## 8. Responsive

- 移动优先
- 网格自适应

## 9. Agent Guide

```css
--color-primary: #E1251B;
```

**提示**: 红色#E1251B、品质电商、价格突出

---
**京东设计系统 v2.0.0**
