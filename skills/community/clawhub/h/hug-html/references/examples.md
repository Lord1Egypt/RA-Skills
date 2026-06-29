# examples.md — hug-html 使用示例

## 示例 1：生成宣传面板 HTML

```bash
python "scripts/template_generator.py" ^
  --output "data/output/promo.html" ^
  --type promo
```

输出：`data/output/promo.html`（粉紫渐变风格宣传面板）

---

## 示例 2：生成可视化编辑界面

```bash
python "scripts/visual_editor.py" ^
  --template "data/output/promo.html" ^
  --output "data/output/editor.html"
```

在浏览器中打开 `editor.html`：
1. 按 `Ctrl+E` 进入编辑模式
2. 点击任意文字区域直接更新
3. 点击图片可更换 URL
4. 使用顶部工具栏调整颜色/字号/透明度
5. 点击「✅ 生成最终HTML」下载成品

---

## 示例 3：用模块库组装 HTML

```bash
# 查看所有可用模块
python "scripts/module_assembler.py" --list

# 组装：渐变背景 + 大标题 + 封面图 + 分隔线
python "scripts/module_assembler.py" ^
  --modules "color:gradient-purple,font:title-large,image:img-cover,effect:divider" ^
  --output "data/output/assembled.html"
```

---

## 示例 4：自动填充模板内容

```bash
# 自动生成示例内容
python "scripts/content_filler.py" ^
  --template "data/output/promo.html" ^
  --auto ^
  --output "data/output/promo-filled.html"
```

---

## 示例 5：用 JSON 文件填充内容

`data/config/content.json`：
```json
{
  "title": "🎉 2026 新春庆典",
  "subtitle": "时间：2026年5月28日 14:00",
  "highlight": "精彩演出 · 美食盛宴 · 幸运抽奖",
  "time": "2026年5月28日 14:00-18:00",
  "location": "深圳市南山区创业路 XX 大厦",
  "detail": "本次活动免费参加，请提前报名。现场提供茶歇和纪念品。",
  "footer": "© 2026 新春庆典组委会 | 咨询电话：138-XXXX-XXXX"
}
```

```bash
python "scripts/content_filler.py" ^
  --template "data/output/promo.html" ^
  --content "data/config/content.json" ^
  --output "data/output/final.html"
```

---

## 示例 6：应用样式预设

```bash
# 生成科技风格模板
python "scripts/template_generator.py" ^
  --output "data/output/tech.html" ^
  --type tech

# 应用「商务」预设
python "scripts/content_filler.py" ^
  --template "data/output/tech.html" ^
  --preset business ^
  --output "data/output/tech-business.html"
```

---

## 示例 7：提取编辑后的内容

用户在可视化编辑器中更新后导出 HTML，提取内容为 JSON：

```bash
python "scripts/content_filler.py" ^
  --extract "data/output/editor-output.html" ^
  --output "data/config/extracted.json"
```
