---
name: ok-locale
description: |
  OK.com 多国家/城市/语言管理技能。城市和分类通过 API 动态获取。
---

# ok-locale — 多国家/城市/语言管理

管理 OK.com 的区域设置。国家为固定列表，城市和分类通过 API 动态获取。

## 执行约束（强制）

所有操作只能通过 `uv run --project <SKILL_DIR> ok-cli` 执行，**禁止自行编写代码或直接调用 API**。

`<SKILL_DIR>` 是本 SKILL.md 的**上两级目录**（即包含 `pyproject.toml` 的项目根目录）。

## 命令

```bash
# 列出支持的国家
uv run --project <SKILL_DIR> ok-cli list-countries

# 搜索城市（推荐方式，能找到小城市）
uv run --project <SKILL_DIR> ok-cli list-cities --country usa --mode search --keyword hawaii

# 动态获取分类树
uv run --project <SKILL_DIR> ok-cli list-categories --country singapore

# 切换到指定地区
uv run --project <SKILL_DIR> ok-cli set-locale --country usa --city hawaii
uv run --project <SKILL_DIR> ok-cli set-locale --country canada --city toronto

# 获取当前地区
uv run --project <SKILL_DIR> ok-cli get-locale
```

## 参数说明

- `--country`: 只接受固定值 `singapore` `canada` `usa` `uae` `australia` `hong_kong` `japan` `uk` `malaysia` `new_zealand`（也接受子域名如 `us` 或 ISO code 如 `US`，但不可自造如 ~~united-states~~）
- `--city`: 城市 code（从 `list-cities` 返回的 `code` 字段获取）
- `--lang`: 语言代码（默认 `en`）
- `--keyword`: 搜索关键词（城市英文名，如 `hawaii`、`new york`）
- `--mode`: 获取方式 — `search`（推荐）、`api`（仅热门城市）、`all`（合并两者）

## 城市查找（推荐流程）

**直接用 search 模式**（不要先跑 api 模式，因为小城市不在 allCities 列表里）：

1. 搜索城市：
   ```bash
   uv run --project <SKILL_DIR> ok-cli list-cities --country usa --mode search --keyword hawaii
   ```
2. 从返回 JSON 的 `cities` 数组中选取 `name` 最匹配的，记下其 `code` 字段
3. 注意：州名和城市名可能不同（如用户说"夏威夷"，搜索 `hawaii` 可能返回 `hawaii` 或 `honolulu`）
4. 如果结果为空，尝试缩短关键词（如 `hawaii` → `hawa`）；仍然为空则告知用户
5. 切换地区：
   ```bash
   uv run --project <SKILL_DIR> ok-cli set-locale --country usa --city <city_code>
   ```

## 常见中文地名映射

| 用户说的 | --country | --keyword | 可能的 city code |
|---------|-----------|-----------|-----------------|
| 夏威夷 | usa | hawaii | hawaii, honolulu |
| 纽约 | usa | new york | new-york |
| 洛杉矶 | usa | los angeles | los-angeles |
| 温哥华 | canada | vancouver | vancouver |
| 多伦多 | canada | toronto | toronto |
| 新加坡 | singapore | singapore | singapore |
| 迪拜 | uae | dubai | dubai |
| 东京 | japan | tokyo | tokyo |
| 悉尼 | australia | sydney | sydney |
| 香港 | hong_kong | hong kong | hong-kong |
| 吉隆坡 | malaysia | kuala lumpur | kuala-lumpur |
| 伦敦 | uk | london | london |
| 奥克兰 | new_zealand | auckland | auckland |

## 支持的国家

singapore, canada, usa, uae, australia, hong_kong, japan, uk, malaysia, new_zealand
