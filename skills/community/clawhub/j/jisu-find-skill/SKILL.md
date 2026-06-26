---
name: "Find Skills - 查找技能"
description: 用 find_skills.py 在 ClawHub 搜索或列举已装技能，支持 JSON 输出。当用户说：ClawHub 上有没有天气技能、我本地装了哪些 skill，或类似技能发现问题时，使用本技能。
metadata: { "openclaw": { "emoji": "🔎", "requires": { "bins": ["python3"] } } }
---

# jisu-find-skill（技能查找）

ClawHub 上发现与安装技能；**包名**是 `jisu-find-skill`，**请用 Python 跑 `find_skills.py`**（不在 PATH 里当命令用）。

## 入口说明

```bash
python3 skills/jisu-find-skill/find_skills.py installed
```

目录可能是 `skills/` 或 `skill/`，按本仓库实际路径改。Windows 可用 `py` / `python`。

## 做什么

- **`search`**：调 `clawhub search`（含变体与解析）。**默认可读**（摘要 + 每条 `detail_line` / `description_line`，不整段贴 CLI 原始输出）；要结构化结果加 **`--json`**。默认对解析到的条目拉 ClawHub API，再按 **下载量 → 星标 → `match_score` → 名称** 排序后按 **`--limit`** 截断。**`--no-details`** 不拉 API，只按 `match_score` 截断。
- **`list`**：**`clawhub search jisuapi`**，默认可读；**`--json`** 输出完整 JSON。需本机有 `clawhub`。
- **其它**：`inspect` / `install` / `stats` / `verify` / `installed` 同样默认可读，**`--json`** 可切回机器格式。

**不依赖**仓库内任何 Markdown 清单文件；极速相关能力请通过 ClawHub 与 `list`/`search` 自行发现。

## 依赖与环境

| 项 | 必需 | 说明 |
|----|------|------|
| `python3` | 是 | 运行脚本 |
| `clawhub` | 对 search/list 需要 | 否则 `search` 无结果、`list` 报错 |

| 环境变量（可选） | 作用 |
|------------------|------|
| `OPENCLAW_SKILLS_DIR` | 已安装技能根目录，默认 `~/.openclaw/workspace/skills` |

## 子命令

| 子命令 | 说明 |
|--------|------|
| `search` | 默认可读；`--json` 结构化；默认拉 API 后按下载量排序再 `--limit`；`--no-details` 仅按匹配分；`--no-clawhub` 不调 CLI |
| `list` | `clawhub search jisuapi`；`--json` 输出 JSON |
| `inspect` | `clawhub inspect` |
| `stats` | ClawHub HTTP API |
| `install` | 默认 dry run，`--execute` 真装 |
| `verify` | 检查本机 `SKILL.md` |
| `installed` | 目录扫描 + 可选 `clawhub list` |

## `search` 说明

- **输入**：普通字符串、`{"q":"…"}`、`@文件`、stdin `-`。中文会拆 2/3 字做 slug 匹配分；发给 `clawhub` 仍是**原查询**。
- **默认拉 API**（`--no-details` 跳过）：`sort_by` 为 `downloads_stars_match_score`，否则 `match_score`。每条含 `detail`、`stars`、`downloads`、`description`（接口 `summary`）、`author` 及展示用 `detail_line` / `description_line`（缺省为 `—`）。**`merge_note`**、**`clawhub_queries_tried`** 便于排查；HTTP 次数约等于本次 CLI 解析条数。
- **展示序号**：**`name`** 为 `1、org/skill` 形式，**`sort_rank`** 从 1 起；**`clawhub_path`** / **`install_hint`** 无序号（供安装）。`list` 的 `results` 相同规则。

展示示例（`detail_line` → `description_line`）：

```text
1、jisu
星标: 12 | 下载: 340 | 作者: 极速数据 (@jisuapi)
描述: 提供所有的极速数据技能包，供选择使用。
```

## 示例

```bash
python3 skills/jisu-find-skill/find_skills.py search 天气 --limit 15          # 默认可读
python3 skills/jisu-find-skill/find_skills.py search 天气 --limit 5 --json   # 结构化
python3 skills/jisu-find-skill/find_skills.py search weather --no-details
python3 skills/jisu-find-skill/find_skills.py list
python3 skills/jisu-find-skill/find_skills.py list --json
python3 skills/jisu-find-skill/find_skills.py stats jisuapi/jisu-weather
```

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。
