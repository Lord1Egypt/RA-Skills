# PPT Master SVG 最佳实践

**版本**: v1.0  
**创建时间**: 2026-04-16  
**目的**: 规范 pptx-master 技能中 SVG 生成的最佳实践，避免常见问题

---

## ⭐ 核心原则

### 1. 使用图标库代替 emoji

**问题**: 直接在 SVG 中使用 emoji 字符（💰🔬📎）会导致 XML 解析失败

**解决**: 使用图标库中的 SVG icon

```svg
<!-- ❌ 错误：直接使用 emoji -->
<text x="0" y="0">💰 投融资</text>
<text x="0" y="0">🔬 技术突破</text>
<text x="0" y="0">📎 附录</text>

<!-- ✅ 正确：使用图标库 -->
<image x="0" y="0" width="24" height="24" href="templates/icons/tabler-filled/money.svg"/>
<text x="30" y="17">投融资</text>
```

### 2. 特殊字符转义

**问题**: XML 特殊字符需要转义

```svg
<!-- ❌ 错误 -->
<text>A & B > C</text>

<!-- ✅ 正确 -->
<text>A &amp; B &gt; C</text>
```

### 3. 中文字体声明

**问题**: 中文字体需要明确声明

```svg
<!-- ✅ 推荐 -->
<text font-family="Microsoft YaHei, sans-serif">中文内容</text>
```

---

## 📚 图标库使用指南

### 图标库位置

```
/home/Vincent/.openclaw/workspace/skills/pptx-master/templates/icons/
├── chunk/          # Chunk 图标库（填充风格）
├── tabler-filled/  # Tabler 填充风格
└── tabler-outline/ # Tabler 轮廓风格
```

### 常用图标映射表

| 场景 | 推荐图标 | 文件名 | 库 |
|------|----------|--------|-----|
| **投融资** | 💰 | `money.svg`, `dollar.svg` | tabler-filled |
| **技术/科研** | 🔬 | `microscope.svg`, `flask.svg` | tabler-filled |
| **附录/附件** | 📎 | `paperclip.svg`, `attachment.svg` | tabler-filled |
| **趋势/增长** | 📈 | `trending-up.svg`, `chart.svg` | tabler-filled |
| **警告/注意** | ⚠️ | `alert-triangle.svg` | tabler-filled |
| **成功/完成** | ✅ | `check-circle.svg` | tabler-filled |
| **错误/失败** | ❌ | `x-circle.svg` | tabler-filled |
| **信息/提示** | ℹ️ | `info-circle.svg` | tabler-filled |
| **时间/日历** | 📅 | `calendar.svg` | tabler-filled |
| **用户/人员** | 👤 | `user.svg` | tabler-filled |
| **设置/配置** | ⚙️ | `settings.svg` | tabler-filled |
| **搜索/查找** | 🔍 | `search.svg` | tabler-filled |
| **下载** | 📥 | `download.svg` | tabler-filled |
| **上传** | 📤 | `upload.svg` | tabler-filled |
| **链接** | 🔗 | `link.svg` | tabler-filled |

### 图标使用示例

```svg
<?xml version="1.0" encoding="UTF-8"?>
<svg width="1280" height="720" viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg">
  <!-- 背景 -->
  <rect width="1280" height="720" fill="#f5f5f5"/>
  
  <!-- 标题 + 图标 -->
  <g transform="translate(100, 60)">
    <!-- 图标 -->
    <image x="0" y="0" width="32" height="32" href="../templates/icons/tabler-filled/money.svg"/>
    <!-- 标题文字 -->
    <text x="40" y="24" font-family="Microsoft YaHei, sans-serif" font-size="24" font-weight="bold" fill="#333333">
      投融资和行业事件
    </text>
  </g>
</svg>
```

---

## 🔧 常见问题排查

### 问题 1: SVG 转换失败，报错"not well-formed"

**原因**: 
- 使用了 emoji 字符
- XML 特殊字符未转义
- 编码问题

**解决**:
1. 移除所有 emoji，改用图标库
2. 转义特殊字符：`&` → `&amp;`, `<` → `&lt;`, `>` → `&gt;`
3. 确保文件编码为 UTF-8

### 问题 2: 中文显示为方框

**原因**: 字体未正确声明

**解决**:
```svg
<text font-family="Microsoft YaHei, sans-serif">中文内容</text>
```

### 问题 3: 图标不显示

**原因**: 
- 图标路径错误
- 图标文件不存在

**解决**:
1. 检查图标路径是否正确
2. 使用 `ls templates/icons/<library>/` 确认图标存在
3. 使用相对路径或绝对路径

---

## 📋 检查清单

在导出 PPTX 前，检查以下项目：

- [ ] 所有 emoji 已替换为图标库 SVG
- [ ] XML 特殊字符已转义
- [ ] 中文字体已声明
- [ ] 图标路径正确
- [ ] SVG 文件格式正确（UTF-8 编码）
- [ ] 所有页面页码正确

---

## 🎯 快速参考

### emoji → 图标映射速查

```
💰 → money.svg
🔬 → microscope.svg
📎 → paperclip.svg
📈 → trending-up.svg
⚠️ → alert-triangle.svg
✅ → check-circle.svg
❌ → x-circle.svg
ℹ️ → info-circle.svg
📅 → calendar.svg
👤 → user.svg
⚙️ → settings.svg
🔍 → search.svg
```

### 图标库快速搜索

```bash
# 搜索特定图标
ls templates/icons/tabler-filled/ | grep money
ls templates/icons/tabler-filled/ | grep chart
ls templates/icons/tabler-filled/ | grep user
```

---

**创建者**: 零壹  
**创建时间**: 2026-04-16  
**状态**: 正式版本 v1.0
