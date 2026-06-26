# pptxgenjs 兼容性缺陷大全

> 基于 GitHub Issue #1449 和实战经验整理  
> 最后更新：2026-04-08

## 一、触发 PowerPoint "内容有问题" 修复对话框的缺陷

### 🔴 P0 — 必定触发修复对话框

#### 1. 幻影 slideMaster 覆盖项（最严重！）

**现象**：pptxgenjs 在 `[Content_Types].xml` 中为每张 slide 都额外注册了一个不存在的 slideMaster Override。

**示例**：18页PPT → `[Content_Types].xml` 中出现 slideMaster1~18 的 Override，但实际只有 `ppt/slideMasters/slideMaster1.xml`

**PowerPoint 行为**：检测到引用的文件不存在 → 弹出修复对话框 → "删除无法读取的内容"

**修复**：用 ElementTree 解析 `[Content_Types].xml`，只保留指向实际存在文件的 Override

```python
# 修复逻辑：检查 PartName 对应的文件是否存在
if 'slideMaster' in part_name and relative_path not in existing_files:
    root.remove(override)  # 删除幻影覆盖项
```

#### 2. 无效主题字体引用

**现象**：pptxgenjs 生成 `+mn-lt`, `+mn-ea`, `+mn-cs`, `+mj-lt`, `+mj-ea`, `+mj-cs` 等无效字体引用

**原因**：这些是 Office 主题字体的内部引用语法，但 pptxgenjs 在没有主题字体定义的情况下直接使用

**修复**：替换为安全的跨平台字体名
```
+mn-lt → Microsoft YaHei  (正文拉丁字体)
+mn-ea → Microsoft YaHei  (正文东亚字体)
+mn-cs → Microsoft YaHei  (正文复杂脚本字体)
+mj-lt → Microsoft YaHei  (标题拉丁字体)
+mj-ea → Microsoft YaHei  (标题东亚字体)
+mj-cs → Microsoft YaHei  (标题复杂脚本字体)
```

### 🟡 P1 — 可能触发修复对话框

#### 3. dirty 属性

**现象**：pptxgenjs 在多个元素上添加 `dirty=""` 属性，这不是 OOXML 标准属性

**修复**：用正则移除所有 `dirty="..."` 属性

#### 4. p14:modId 元素

**现象**：pptxgenjs 在某些 slide 上生成 `<p14:modId .../>` 元素，使用了非标准命名空间前缀

**修复**：正则移除所有 `<p14:modId .../>` 和 `<p14:modId ...>...</p14:modId>`

#### 5. Notes Slides 无效占位符

**现象**：pptxgenjs 生成的 notesMaster 包含无效占位符形状，notesSlides 使用 p14: 命名空间

**修复**：删除所有 notesSlides 和 notesMasters 文件，同时清理 .rels 中的引用

#### 6. 零尺寸形状

**现象**：`<a:ext cx="0" cy="0"/>` — 零尺寸的形状在某些 PowerPoint 版本中报错

**常见于**：LINE 形状（高度为0是正常的线条，但宽度和高度同时为0则有问题）

**修复**：替换 `cx="0"` → `cx="1"`, `cy="0"` → `cy="1"` (1 EMU 不可见)

### 🟢 P2 — 不会触发修复但影响显示

#### 7. 空 `<a:ln />` 元素

**现象**：空的线条元素在某些版本中渲染异常

**修复**：`<a:ln />` → `<a:ln w="0"><a:noFill/></a:ln>`

#### 8. 空文本元素

**现象**：`<a:t></a:t>` 空文本节点

**修复**：替换为 `<a:t> </a:t>` (含空格)

#### 9. 未使用的 Default 扩展类型

**现象**：`[Content_Types].xml` 中注册了 jpeg/jpg/svg/gif/m4v/mp4/vml/xlsx 等 Default，但 PPTX 中并无对应文件

**修复**：只保留 rels, xml, png 的 Default，其余按需

---

## 二、Shadow 和 Transparency — 兼容性地雷

### Shadow（阴影效果）

**问题**：pptxgenjs 的 shadow API 生成极其复杂的 OOXML 效果链（outerShdw/innerShdw + alpha + blurRad + dist + dir），在以下场景会出问题：
- PowerPoint 2013 及更早版本不支持
- WPS Office 渲染错误
- LibreOffice 忽略阴影
- 某些 Mac 版 PowerPoint 崩溃

**替代方案**：用细边框（line）模拟视觉层次
```javascript
// ❌ 不要用
shadow: { type: "outer", blur: 3, offset: 2, color: "000000", opacity: 0.3 }

// ✅ 用边框代替
line: { color: "30363D", width: 0.75 }
```

### Transparency（透明度）

**问题**：shape/text/line/image 的 transparency 属性在跨版本时表现不一致

**替代方案**：用预混色（pre-mixed color）代替透明度
```javascript
// ❌ 不要用
fill: { color: "FFFFFF", transparency: 80 }  // 80%透明度白色

// ✅ 在深色背景上，预计算混合色
// 背景 #1A1A2E + 白色 20% → 约 #3A3A4E
fill: { color: "3A3A4E" }
```

**图标的暗化版**：需要透明度效果的图标，预渲染暗色版本
```javascript
// ❌ 不要用 image transparency
slide.addImage({ data: icon, transparency: 70 })

// ✅ 预渲染暗色图标
const iconDim = await iconToBase64Png(FaShield, "3A4450", 256)  // 暗色
slide.addImage({ data: iconDim })
```

---

## 三、形状名称陷阱

pptxgenjs 的 shapes 枚举常量映射关系：

| 枚举常量 | 生成的 prstGeom 值 | 是否合规 |
|---------|-------------------|---------|
| `pres.shapes.OVAL` | `ellipse` | ✅ |
| `"oval"` (字符串) | `oval` | ❌ 不在 OOXML 标准中 |
| `pres.shapes.ROUNDED_RECTANGLE` | `roundRect` | ✅ |
| `"roundedRectangle"` (字符串) | `roundedRectangle` | ❌ 不在 OOXML 标准中 |
| `pres.shapes.RECTANGLE` | `rect` | ✅ |
| `pres.shapes.LINE` | `line` | ✅ |

**规则**：始终使用枚举常量 `pres.shapes.XXX`，不要使用字符串

---

## 四、正确的工作流程

### 生成阶段（预防）

1. **禁止使用 shadow API** — 用边框/预混色代替
2. **禁止使用 transparency** — 用预混色/预渲染暗色图标代替
3. **使用枚举常量** — `pres.shapes.OVAL` 而非 `"oval"`
4. **使用 ZIP_DEFLATED** — 但 pptxgenjs 默认已压缩

### 后处理阶段（修复）

生成 PPTX 后，**必须**运行后处理脚本修复 pptxgenjs 无法避免的缺陷：

```bash
python fix_pptx_compatibility.py output.pptx
```

脚本修复内容：
1. ✅ 移除幻影 slideMaster 覆盖项
2. ✅ 替换无效主题字体引用
3. ✅ 移除 dirty 属性
4. ✅ 移除 p14:modId 元素
5. ✅ 移除 Notes Slides 无效内容
6. ✅ 修复零尺寸形状
7. ✅ 修复空文本/空线条元素
8. ✅ 清理未使用的 Default 扩展类型

### 验证阶段

用 PowerPoint 实际打开验证。自动化验证可检查：
- `[Content_Types].xml` 中所有 Override 的 PartName 指向的文件是否存在
- 所有 .rels 中的 Target 指向的文件是否存在
- 无 `+mn-lt` 等无效字体引用
- 无 `dirty=` 属性
- 无 `p14:` 命名空间

---

## 五、参考链接

- [pptxgenjs Issue #1449 — Needs Repair Errors](https://github.com/gitbrent/PptxGenJS/issues/1449)
- [pptxgenjs 官方修复文档](https://gitbrent.github.io/PptxGenJS/docs/needs-repair-errors/)
- [OOXML Standard — ECMA-376](https://www.ecma-international.org/publications-and-standards/standards/ecma-376/)
