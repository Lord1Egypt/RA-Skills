# 主题开发指南

为 md2pdf 创建自定义主题时，请遵循以下规则。

## 基础结构

```css
/* 必须：防止 Chromium PDF 打印时降级颜色 */
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }

body {
    font-family: ...;
    font-size: ...;        /* 建议 11-14px（96dpi）或 10-12pt */
    line-height: ...;      /* 建议 1.6-2.0 */
    color: ...;            /* ⚠️ 会覆盖浏览器默认蓝色链接，需要单独设 a { color: ... } */
}

/* 必须显式定义链接颜色 */
a { color: ...; }
```

## 表格注意事项

| 规则 | 说明 |
|------|------|
| 字号 ≤ 13px / 10pt | 过大字号会加剧宽表截断 |
| 不做全局缩放 | zoom 由 md2pdf 自动处理（≥5 列触发） |
| 边框/间距适中 | padding 过大同样会撑宽表格 |
| `table-layout: auto` | 默认值，不建议改 fixed（会导致窄列内容截断） |

## 表头

```css
th { background: ...; color: ...; font-weight: 600; }
```

建议浅灰底 + 深色粗字（如 `#e8e8ed` + `#1d1d1f`），视觉区分度好。

⚠️ 如果用深色背景（如黑底白字），必须保留 `html { print-color-adjust: exact }`，否则 Chromium 会将白字降级为灰色。

## 测试清单

- [ ] 用 `--validate` 确认环境就绪
- [ ] 生成带有 6 列宽表的文档，确认缩放正常、不截断
- [ ] 确认链接为蓝色 + 下划线
- [ ] 确认表头有可见背景色
- [ ] 确认中文/CJK 正常渲染

测试命令：
```bash
python3 scripts/md2pdf.py --input README.md --theme 你的主题名 -o output/test.pdf
```
