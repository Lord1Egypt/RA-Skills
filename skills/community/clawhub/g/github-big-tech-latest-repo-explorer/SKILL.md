---
name: "github-big-tech-latest-repo-explorer"
description: "从预设的大厂 GitHub 组织中挑选最近创建、star 大于 1000 的热门仓库，默认 3 个月窗口，无结果时自动扩窗，最晚回溯到 2023-03-14（GPT-4 发布日）。"
version: 1.0.0
---

# 大厂最新热门仓库探索

## 一、功能

（1）从 `references/organizations.json` 的大厂组织中，每次挑选一个最近创建、`stars > 1000`（硬性条件）且未输出过的仓库。

（2）按 `assets/output_template.md` 回答三个问题：项目是什么、解决了什么问题、如何解决。

## 二、数据来源

（1）组织名单：`references/organizations.json`，格式为 `{公司: [组织主页链接, ...]}`，手工维护，名单外的仓库不会被搜到。`scripts/probe_orgs.py` 仅用于检查链接有效性，不参与正常运行。

（2）仓库列表：GitHub Core API `GET /orgs/{org}/repos`，按创建时间倒序分页，翻到早于窗口起点即停止，不使用 Search API。

（3）README：`GET /repos/{owner}/{repo}/readme`。

（4）认证：需要添加 `GITHUB_TOKEN` 或 `GH_TOKEN` 环境变量，Core API 额度为每小时 5000 次，额度耗尽时该组织记为查询失败。

## 三、运行流程

### 1. 筛选

（1）本地按 `created_at` 落在窗口内、`stargazers_count > 1000` 过滤。

（2）排除 `assets/history/history.json` 中已输出的 `full_name`。

（3）按 `--pick` 策略选出仓库。

### 2. 自动扩窗

（1）默认窗口为最近 3 个月，无满足条件的未输出仓库时，依次扩大到 6、12、24、36、48、60 个月。

（2）窗口起点不早于 2023-03-14，到该日期仍无结果则停止，输出无可选结果。

（3）每次扩窗后，重新计算候选总数、已输出数、未输出数。

### 3. 输出与历史

（1）严格遵守 `assets/output_template.md`，标题、筛选条件、统计均使用最终实际窗口，并标注 `stars > 1000`。

（2）README 信息不足时标注"信息有限，基于元数据推断"，禁止编造。

（3）仅正式运行成功选出仓库后才写入 `assets/history/history.json`，`--dry-run` 不修改历史。

（4）某个组织请求失败时继续处理其它组织，并在结果中列出失败组织。

（5）回答完成后，须将完整回答（不含 README 原文）以 Markdown 保存到 `assets/history/`，文件名为 `YYYY-MM-DD-owner-repo.md`（日期取运行当天，`owner`、`repo` 为仓库所有者与名称，用 `-` 连接），脚本输出中已给出具体路径；`--count` 大于 1 时每个仓库单独保存一个文件。`--dry-run` 与无可选结果时不保存。

## 四、参数

| 参数              | 说明                                                                          |
| ----------------- | ----------------------------------------------------------------------------- |
| `--months N`      | 初始窗口（自然月），默认 3，后续档位为 3、6、12、24、36、48、60 中大于 N 的值 |
| `--count N`       | 选几个仓库，默认 1                                                            |
| `--pick stars`    | 默认，选 Stars 最多，相同时选创建时间最新                                     |
| `--pick oldest`   | 选创建时间最早                                                                |
| `--pick random`   | 随机选                                                                        |
| `--org-config`    | 指定组织名单文件                                                              |
| `--reset-history` | 清空已输出记录                                                                |
| `--dry-run`       | 只预览，不写历史                                                              |
| `--workers`       | 并发数                                                                        |

验收命令：

```bash
python3 scripts/fetch_repo.py --months 3 --count 1 --dry-run
```

## 五、常见问题

- `401 Unauthorized`：`GITHUB_TOKEN` 无效、已撤销或没有访问权限。
- `403` / `429`：GitHub API 限流；匿名请求请配置 `GITHUB_TOKEN` 后重试，已使用 Token 则稍后重试。