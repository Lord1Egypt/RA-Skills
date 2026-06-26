---
name: huo15-mind-map
displayName: 火一五思维导图技能
description: 规范 + 时尚的思维导图生成。输入 Markdown 大纲 / JSON / OPML / XMind，输出 XMind 2021+ (.xmind)、OPML、FreeMind (.mm)、Markdown、PNG、PDF、SVG；内置 13 种风格（modern / classic / dark / xiaohongshu / ocean / forest / sunset / minimal / pastel / github / editorial NYT 杂志 / bauhaus 三原色 / swiss 国际主义）。触发词：思维导图、脑图、mind map、mindmap、生成思维导图、导出 xmind、画思维导图、编辑杂志风、纽约客、NYT、Monocle、包豪斯、三原色、瑞士国际主义、Helvetica 网格、Müller-Brockmann。
version: 1.2.0
aliases:
  - 火一五思维导图技能
  - 火一五脑图技能
  - 火一五思维导图
  - 火一五脑图
  - 思维导图生成
  - mind-map
  - mindmap
  - 脑图
  - XMind导出
dependencies:
  python-packages:
    - matplotlib
    - Pillow
---

# 火一五思维导图技能 v1.0

> 规范 + 时尚的思维导图生成器 — 青岛火一五信息科技有限公司

---

## 一、核心能力

1. **一端多出** — 同一个输入可同时导出：
   - `.xmind`（XMind 2021+ ZIP，含 content.json / metadata.json / manifest.json）
   - `.opml`（OPML 2.0，兼容 MindNode / 幕布 / WorkFlowy / Apple Notes）
   - `.mm`（FreeMind 格式，兼容 XMind、EdrawMind、亿图图示、幕布）
   - `.md`（Markdown outline，方便回写知识库 / 复用）
   - `.png` / `.pdf` / `.svg`（渲染图，发群/导入幻灯都合适）
   - `.json`（内部统一结构，编程复用）
2. **十三种风格 ⭐v1.2** — `modern` / `classic` / `dark` / `xiaohongshu` / `ocean` / `forest` / `sunset` / `minimal` / `pastel` / `github` + **`editorial`（编辑杂志 NYT 风）/ `bauhaus`（三原色几何）/ `swiss`（国际主义 Helvetica 网格）⭐v1.2**（中文别名：现代 / 经典 / 暗色 / 小红书 / 海洋 / 森林 / 夕阳 / 极简 / 马卡龙 / 极客 / 编辑、纽约客、NYT、Monocle / 包豪斯、三原色、几何 / 瑞士、国际主义、Helvetica）。
3. **多种输入** — Markdown 大纲 / 内部 JSON / OPML / 已有的 XMind 文件都能读；Markdown 支持标题 (#) 与无序/有序列表混排。
4. **中文友好** — 自动选取系统内的 PingFang SC / Microsoft YaHei / Noto Sans CJK 等字体。

---

## 二、输入格式

### 2.1 Markdown 大纲（推荐）

```markdown
# 火一五产品矩阵              # 第 1 个标题成为根节点

## 核心平台                   # ##  → 一级分支
### 龙虾 OpenClaw             # ### → 二级分支
- 插件体系                    # 缩进列表 → 下一级叶子
- 技能市场
- 场景编排
### 辉火云管家·贾维斯
- 跨应用代理
- 记忆系统

## 行业解决方案
### 机器人企业
- 数字化管家
...
```

规则：
- 第一个出现的 `#` 标题升格为根节点；
- 后续 `##` `###` 依次作为子级；
- `- item` / `* item` / `1. item` 可接续在标题后面作为更深层级；
- 连续非标题非列表的文本行会挂到当前节点的 `note` 上，导出 XMind 时会写入 `notes.plain.content`。

### 2.2 内部 JSON

```json
{
  "title": "火一五产品矩阵",
  "children": [
    {"title": "核心平台", "children": [
      {"title": "龙虾 OpenClaw"}, {"title": "辉火云管家"}
    ]},
    {"title": "行业解决方案"}
  ]
}
```

### 2.3 OPML / XMind 导入

直接喂路径给 `--input`，用 `--input-format opml|xmind` 强制解析器。

---

## 三、命令行

### 3.1 基础用法

```bash
# 1. 从 Markdown 生成 XMind（默认 modern 风格）
python3 scripts/create-mind-map.py \
  --input outline.md \
  --output /tmp/map.xmind

# 2. 同时导出 PNG + PDF + OPML（基于 --output 的同名文件）
python3 scripts/create-mind-map.py \
  --input outline.md \
  --output /tmp/map.xmind \
  --also png,pdf,opml \
  --style xiaohongshu

# 3. 仅渲染为 PNG，指定分辨率
python3 scripts/create-mind-map.py \
  --input outline.md \
  --output /tmp/map.png \
  --style dark --dpi 300

# 4. 把现有 XMind 转换为 Markdown
python3 scripts/create-mind-map.py \
  --input existing.xmind --input-format xmind \
  --output /tmp/existing.md

# 5. 从 stdin 读 Markdown
cat outline.md | python3 scripts/create-mind-map.py \
  --output /tmp/map.png --style modern
```

### 3.2 参数速查

| 参数 | 说明 |
|------|------|
| `--input / -i` | 输入文件路径（md / json / opml / xmind） |
| `--input-text` | 直接传 Markdown / JSON / OPML 字符串 |
| `--input-format` | `auto` (默认) / `markdown` / `json` / `opml` / `xmind` |
| `--output / -o` | 主输出路径；扩展名决定格式 |
| `--also` | 逗号分隔的额外格式（基于 `--output` 同名） |
| `--style` | `modern` / `classic` / `dark` / `xiaohongshu` / `ocean` / `forest` / `sunset` / `minimal` / `pastel` / `github` / `editorial` / `bauhaus` / `swiss`（默认 modern，支持中文别名） |
| `--dpi` | PNG 分辨率（默认 200） |
| `--sheet-name` | XMind sheet 名称（默认用根节点标题） |
| `--title` | 手动覆盖根节点标题 |

---

## 四、Python API

```python
import sys
sys.path.insert(0, 'scripts')

from mindmap_tree import parse_markdown, to_xmind, to_opml, to_json
from mindmap_render import render

with open('outline.md', encoding='utf-8') as fh:
    root = parse_markdown(fh.read())

to_xmind(root, '/tmp/map.xmind')
print(to_opml(root)[:200])
render(root, '/tmp/map.png', style_name='xiaohongshu', dpi=240)
```

主要 API：

| 函数 | 说明 |
|------|------|
| `parse_markdown(text) → Node` | Markdown outline → 树 |
| `parse_json(text) → Node` | 内部 JSON → 树 |
| `parse_opml(text) → Node` | OPML 2.0 → 树 |
| `parse_xmind(path) → Node` | XMind 2021+ → 树 |
| `to_xmind(root, path)` | 写 XMind |
| `to_opml(root) → str` | OPML 字符串 |
| `to_markdown(root) → str` | Markdown 字符串 |
| `to_freemind(root) → str` | FreeMind `.mm` 字符串 |
| `to_json(root) → str` | 内部 JSON |
| `render(root, path, style_name, dpi)` | 渲染 PNG/PDF/SVG |

`Node` 数据结构（可自由增删）：

```python
@dataclass
class Node:
    title: str
    note: str = ''
    children: List[Node] = []
```

---

## 五、风格

| key | 名称 | 背景 | 主色 | 适用场景 |
|-----|------|------|------|---------|
| `modern`（默认） | 现代商务 | 白底 `#FFFFFF` | 深蓝灰 `#2C3E50` | 对外汇报、产品方案 |
| `classic` | 经典稳重 | 浅灰 `#FAFAFA` | 靛蓝 `#374785` | 正式文档、技术白皮书 |
| `dark` | 暗色霓虹 | 深蓝 `#0F172A` | 亮蓝 `#38BDF8` | 大屏演示、暗色幻灯 |
| `xiaohongshu` (`xhs`, `小红书`) | 小红书暖奶油 | 奶油 `#FFF8F3` | 小红书红 `#FF2442` | 营销帖、品牌故事 |
| `ocean` (`海洋`, `蓝`) | 海洋蓝 | 冰蓝 `#F8FBFE` | 深蓝 `#0077B6` | SaaS 产品、技术架构 |
| `forest` (`森林`, `绿`, `自然`) | 森林绿 | 米白 `#F7FAF8` | 墨绿 `#2D6A4F` | 环保、农业、健康 |
| `sunset` (`夕阳`, `暖橙`, `橙`) | 夕阳暖橙 | 奶杏 `#FFFBF5` | 赤橙 `#E76F51` | 运营活动、温暖叙事 |
| `minimal` (`极简`, `素雅`, `学术`) | 极简素雅 | 纯白 `#FFFFFF` | 近黑 `#2E2E2E` | 学术论文、出版物 |
| `pastel` (`马卡龙`, `粉`, `儿童`) | 马卡龙粉嫩 | 粉白 `#FFFBFC` | 天蓝 `#B5D8FA` | 儿童教育、女性向 |
| `github` (`极客`, `程序员`) | 极客 GitHub | 纯白 `#FFFFFF` | 深灰 `#24292E` | 开源文档、README |
| `editorial` ⭐v1.2 (`编辑`, `纽约客`, `NYT`, `Monocle`) | 编辑杂志 | 米白 `#FAF8F5` | 报纸黑 `#0F0F0F` + 报头朱红 `#D0021B` | NYT/Monocle 杂志风信息组织、长篇报告、思想型品牌 |
| `bauhaus` ⭐v1.2 (`包豪斯`, `三原色`, `几何`) | 包豪斯 | 象牙 `#FAFAFA` | 黑 `#0A0A0A` + 红黄蓝三原色循环 | 文化机构、艺术展、几何品牌、设计运动主题 |
| `swiss` ⭐v1.2 (`瑞士`, `国际主义`, `Helvetica`, `Müller`, `Brockmann`) | 瑞士国际主义 | 纯白 `#FFFFFF` | 黑 `#000000` + 报头红 `#D4181F` accent | 网格化信息组织、博物馆展览、政府公共项目、Müller-Brockmann 风学术 |

> 风格只影响配色、字号、圆角；结构层级、字体选择是自适应的。

---

## 六、与主流软件互通

| 软件 | 导入方式 |
|------|---------|
| **XMind** | 直接打开 `.xmind`（2021+ 格式）或导入 `.opml` / `.mm` |
| **MindNode / MindMeister** | 导入 `.opml` |
| **幕布 / WorkFlowy / Notion** | 粘贴 `.md`，或导入 `.opml` |
| **EdrawMind / 亿图图示** | 导入 `.xmind` / `.mm` |
| **Apple Notes / Outlook** | 粘贴 `.md` |

当甲方拿的是微软 Visio / Miro 这类工具时，直接发 PNG / PDF / SVG 即可。

---

## 七、触发词

- 思维导图 / 脑图 / 心智图 / mind map / mindmap
- 画思维导图 / 做思维导图 / 生成思维导图
- 导出 xmind / 生成 xmind / 转 xmind
- outline 转思维导图

---

## 八、版本历史

- **v1.2.0（当前 · 2026-04-28）** — 三个有性格风格扩展。新增 `editorial` 编辑杂志风（米白 `#FAF8F5` 底 + 报纸黑 `#0F0F0F` 根 + 报头朱红 `#D0021B` 分支 + 接近直角圆角 0.08，杂志感）/ `bauhaus` 包豪斯风（象牙白 `#FAFAFA` 底 + 黑根 + 红 `#D32F2F` + 黄 `#FFD600` + 蓝 `#1565C0` 三原色分支循环 + 0 圆角严格几何 + 2px 边）/ `swiss` 瑞士国际主义风（纯白底 + 黑根 + 黑 / 报头红 `#D4181F` / 灰循环分支 + 0 圆角 + 1px 细描边）。三个新风格**与软色范式 10 风格反差互补**，专攻"有性格 / 设计师作品级"思维导图场景；和 design-director v3.0 §二 视觉三元组的 §2.2 #6 NYT / §2.5 #19 Bauhaus / §2.1 #3 Swiss Design 锚点 1:1 对应；和 huo15-flow-chart v1.4 同名风格配色完全同源（同一品牌可在流程图和思维导图间无缝切换）。总风格数 10 → 13。

- **v1.1.0** — 扩展 6 种预设风格：`ocean` 海洋蓝 / `forest` 森林绿 / `sunset` 夕阳暖橙 / `minimal` 极简素雅 / `pastel` 马卡龙粉嫩 / `github` 极客 GitHub；完善中文别名。

- **v1.0.0** — 首版。支持 Markdown/JSON/OPML/XMind 输入；输出 XMind/OPML/FreeMind/Markdown/PNG/PDF/SVG/JSON；内置 modern/classic/dark/xiaohongshu 四风格。

---

**技术支持：** 青岛火一五信息科技有限公司
