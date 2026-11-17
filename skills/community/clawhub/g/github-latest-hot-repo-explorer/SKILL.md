---
name: "github-latest-hot-repo-explorer"
description: "从 GitHub 全站搜索最近创建、star 大于 5000 的热门仓库，严格选取 star 最多且未输出过的一个，默认 1 个月窗口，无结果时自动扩窗，最晚回溯到 2023-03-14（GPT-4 发布日）。"
version: 1.1.1
---

# GitHub 最新热门仓库探索

## 一、功能

（1）通过 GitHub Search API 在全站范围内，每次挑选一个最近创建、`stars > 5000`（默认，可调整）且未输出过的仓库，严格取 star 最多者，不随机。

（2）按 `assets/output_template.md` 回答三个问题：项目是什么、解决了什么问题、如何解决。

## 二、数据来源

（1）仓库列表：GitHub Search API `GET /search/repositories`，查询条件为 `stars:>{stars} created:>{窗口起点}`，按 stars 降序，单次拉取 100 条。

（2）README：`GET /repos/{owner}/{repo}/readme`，仅取前 8000 字符。

（3）认证：读取系统环境变量 `GITHUB_TOKEN`，未配置时使用匿名请求。严禁索要或展示 Token。

（4）历史记录：`assets/history/history.json`，记录已输出的 `full_name`。

## 三、运行流程

### 1. 筛选

（1）窗口内按 `stars > N` 搜索，结果已按 stars 降序。

（2）排除 `assets/history/history.json` 中已输出的 `full_name`。

（3）在剩余候选中取 `stargazers_count` 最大者。

### 2. 自动扩窗

（1）默认窗口为最近 1 个自然月，无满足条件的未输出仓库时，依次扩大到 2、3、6、12、24、36、48、60 个月。

（2）窗口起点不早于 2023-03-14，到该日期仍无结果则停止，提示用 `--reset-history` 重置或调整 `--stars`。

（3）输出标题中的"最近 X 月"使用最终实际窗口。

### 3. 输出与历史

（1）严格遵守 `assets/output_template.md`，筛选条件使用最终实际窗口，并标注实际的 stars 阈值；输出与保存的 Markdown 均须符合 markdownlint 规范（标题层级与编号、段落编号见模板）。

（2）README 信息不足时标注"信息有限，基于元数据推断"，禁止编造。

（3）仅正式运行成功选出仓库后才写入 `assets/history/history.json`，`--dry-run` 不修改历史。

（4）回答完成后，须将完整回答（不含 README 原文）以 Markdown 保存到 `assets/history/`，文件名为 `YYYY-MM-DD-owner-repo.md`（日期取运行当天，`owner`、`repo` 为仓库所有者与名称，用 `-` 连接），脚本输出中已给出具体路径；保存文件的格式与输出一致。`--dry-run` 与无可选结果时不保存。

## 四、Token 与限流

（1）未配置 Token 的匿名请求遇到限流时，提示用户配置系统环境变量 `GITHUB_TOKEN`（示例 `export GITHUB_TOKEN="***"`），不得索要或展示 Token。Token 只需具备读取公开仓库的最小权限，不要写入 `.env`、提交到 Git 仓库或共享给他人。

（2）已配置 Token 仍遇限流（`403` / `429`）时，提示等待配额恢复后重试。

（3）`401 Unauthorized`：`GITHUB_TOKEN` 无效、已撤销或没有访问权限。

## 五、参数

| 参数              | 说明                                                                                  |
| ----------------- | ------------------------------------------------------------------------------------- |
| `--stars N`       | star 下限（硬性条件，严格大于），默认 5000                                            |
| `--months N`      | 初始窗口（自然月），默认 1，后续档位为 1、2、3、6、12、24、36、48、60 中不小于 N 的值 |
| `--dry-run`       | 预览模式，使用 `scripts/fixtures/items.json` 样例数据，不请求 GitHub，不抓取 README，不写历史 |
| `--reset-history` | 清空已输出记录                                                                        |

验收命令：

```bash
python3 scripts/fetch_repo.py --stars 5000 --months 1
```

预览命令（不联网、不写历史）：

```bash
python3 scripts/fetch_repo.py --dry-run
```
