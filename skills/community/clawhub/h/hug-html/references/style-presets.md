# style-presets.md — 样式预设系统

`hug-html` 支持 5 种常见风格的样式预设，通过 `content_filler.py --preset` 应用。

---

## 预设列表

### business — 商务风格

| 属性 | 值 |
|-------|-----|
| 主色 | `#1a2a4a` |
| 辅色 | `#4a5568` |
| 背景 | `#f0f4f8` |
| 字体 | Microsoft YaHei, sans-serif |
| 圆角 | `8px` |
| 适用 | 商务报告、正式文档、企业介绍 |

### academic — 科研风格

| 属性 | 值 |
|-------|-----|
| 主色 | `#333333` |
| 辅色 | `#666666` |
| 背景 | `#ffffff` |
| 字体 | SimSun, serif |
| 圆角 | `4px` |
| 适用 | 科研论文、技术报告、学术海报 |

### festive — 喜庆风格

| 属性 | 值 |
|-------|-----|
| 主色 | `#c0392b` |
| 辅色 | `#e74c3c` |
| 背景 | 渐变 `#c0392b → #e74c3c` |
| 字体 | SimSun, serif |
| 圆角 | `12px` |
| 适用 | 婚庆、节日、庆典、喜报 |

### mourning — 丧事风格

| 属性 | 值 |
|-------|-----|
| 主色 | `#333333` |
| 辅色 | `#666666` |
| 背景 | `#f5f5f5` |
| 字体 | SimSun, serif |
| 圆角 | `8px` |
| 适用 | 讣告、悼念、正式讣悼场合 |

### tech — 技术风格

| 属性 | 值 |
|-------|-----|
| 主色 | `#2D3436` |
| 辅色 | `#636E72` |
| 背景 | `#f8f9fa` |
| 字体 | Consolas, 'Courier New', monospace |
| 圆角 | `4px` |
| 适用 | 技术文档、代码说明、API 文档 |

---

## 应用方法

### 通过命令行应用

```bash
python "scripts/content_filler.py" ^
  --template "data/output/template.html" ^
  --preset business ^
  --output "data/output/styled.html"
```

### 在可视化编辑器中应用

打开生成的 `editor.html` → 点击任意区域 → 使用顶部工具栏：
- 🎨字色 — 更新文字颜色
- 🖌️背景 — 更新背景色
- 🔤字号 — 更新字号（12/14/16/18/24/32px）
- 👁️透明 — 更新透明度（100%/90%/70%/50%/30%）

### 在 HTML 中直接写死

```html
<div style="background: #1a2a4a; color: white;">
  商务风格面板
</div>
```

---

## 扩展自定义预设

编辑 `scripts/content_filler.py` 中的 `STYLE_PRESETS` 字典：

```python
STYLE_PRESETS = {
    "my-style": {
        "primary": "#ff6600",
        "secondary": "#ffcc00",
        "bg": "linear-gradient(135deg, #ff6600 0%, #ffcc00 100%)",
        "font": "'Comic Sans MS', cursive",
        "border_radius": "16px",
    },
}
```

或通过 JSON 配置文件 `data/config/style-presets.json` 管理（计划中）。

---

## 与模块库的关系

- **样式预设** = 全局风格（颜色/字体/圆角）
- **模块库** = 可复用 HTML 片段（独立组件）

建议流程：
1. 用 `--preset` 配置全局风格
2. 用 `module_assembler.py` 组装具体模块
3. 用可视化编辑器微调
