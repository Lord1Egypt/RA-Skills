# locales · 多语言

本目录存放 `SKILL.md` 的各语言全文。**`skills/powpop-two-stories/SKILL.md`（中文）是 canonical**，这里只放它的等价译本。

| 语言 | 文件 | 状态 |
|---|---|---|
| `zh-CN` | `../SKILL.md`（canonical，不在本目录） | 源语言 |
| `en` | `en/SKILL.md` | 完整译本，与 canonical 同步 |

## 为什么中文放在上一层而不是 `locales/zh-CN/`

ClawHub 与各类 skill 加载器读的都是**包根目录的 `SKILL.md`**。如果把中文也塞进 `locales/zh-CN/`，根目录就得再放一份内容相同的副本，两份必然漂移。所以根目录那份就是中文原文，`locales/` 只放其他语言。

## 新增一门语言

1. 建 `locales/<lang>/SKILL.md`（`<lang>` 用 BCP 47，如 `ja`、`zh-TW`、`es`）。
2. frontmatter 必须带：`name`（与 canonical **完全一致**，不要翻译）、`version`（与 canonical 一致）、`language: <lang>`、`canonical: ../../SKILL.md`、`display_name`、`description_zh`、`description_en`。
3. 在 `skills/powpop-two-stories/SKILL.md` 的 frontmatter `locales:` 列表里加上这门语言。
4. 跑校验：

```bash
node scripts/check-locales.mjs
```

## 翻译时不许动的东西

这些是行为契约，不是文案，**任何语言都必须一致**：

| 项 | 值 |
|---|---|
| 同一地点半径 | `500` 米；不足 3 条才允许补一次 `1000` 米，且单列"稍远一点" |
| 单次会话 `find_nearby` 上限 | `3` 次（与 `geocode_place` 合计 12 次/分钟） |
| 呈现条数 | 最多 `5` 条（4 条按距离+字数，补 1 条最早） |
| 硬规则条数 | **21 条**，编号和内容一一对应 |
| 「合拍」的五个维度 | 写的是什么 / 情绪落点 / 人在不在场 / 时间朝向 / 说法——顺序和判据（至少三样对上）不能改 |
| 工具名 | `whoami` `geocode_place` `find_nearby` `get_post_detail` `prepare_post` `publish_post` `like_post` —— **原样保留，不翻译、不换大小写** |
| 数据实话 | `657` 条带坐标公开帖、`273` 个地点名、`97` 个 ≥2 条、`23%` 正文重复 |
| 禁止项 | 不按时间过滤、不点名作者、不列赞数、不虚构数字、不说"你是第一个" |

## 可以本地化的东西

- 标题、章节标题、示例里的地名与人名（示例必须仍是**占位符**，不能被读成真实数据）
- 话术（固定问法可以按语言重写，但**信息量不能少**：点赞不通知对方、可能续期 24 小时这两点必须都在）
- 日期示例的写法（`2026-10-28` 这种 ISO 格式建议保留，跨语言无歧义）

英文版在文件顶部有一行 `> This is the English rendering of ../../SKILL.md`，新语言照抄这个做法，读者才知道哪份是源。
