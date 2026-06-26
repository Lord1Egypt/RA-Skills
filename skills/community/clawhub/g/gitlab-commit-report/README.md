# GitLab Commit Report

从 GitLab Group activity 接口采集代码提交数据，支持分页拉取当天全量记录，并生成任意日期的 Markdown 提交日报。

## 功能

- 通过 Puppeteer 复用浏览器登录态，调用 GitLab Group Activity 接口
- 分页拉取当天所有 push events，遇到更早日期自动停止
- 以 commit id 去重，增量追加到本地 JSON 文件
- 支持生成任意日期的日报，包含：
  - 提交总次数、活跃人数、涉及仓库数
  - Top 10 提交者排行
  - Top 5 活跃仓库排行
  - 完整提交明细

## 前置条件

- Chrome 浏览器已打开并登录 GitLab
- 已配置 `config.json`

## 配置

复制 `config.example.json` 为 `config.json`：

```json
{
  "gitlabUrl": "https://git.corp.kuaishou.com",
  "groupId": "your-group-path",
  "groupName": "我的团队"
}
```

## 使用

```bash
# 安装依赖
pnpm install

# 采集今天的 push events（建议配合 cron 每小时执行）
pnpm start collect

# 生成今日日报（手动触发）
pnpm start report

# 生成指定日期日报
pnpm start report 2026-03-18
```

## Cron 配置示例

```cron
0 * * * * cd /path/to/skills/gitlab-commit-report && pnpm start collect >> /tmp/gitlab-collect.log 2>&1
```

## 输出文件

```
data/YYYY-MM-DD.json    # 当天 push events 原始数据（增量去重追加）
report/YYYY-MM-DD.md    # 指定日期提交日报
```

## 数据采集逻辑

每次执行 `collect` 时，从 GitLab Group Activity 接口分页拉取（每页 20 条），仅保留当天的 push 事件，遇到更早日期立即停止翻页。新拉取的数据与已保存数据按 commit id 去重后合并写入，确保多次执行不会产生重复记录。
