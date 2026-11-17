# Harness Doctor 小红书小工具版

这是 `hekouwang-harness-check-skill` 的离线报告阅读器，不是完整 Harness 执行器。

## 能做什么

- 阅读内置 Scorecard 示例；
- 查看 12 个评分维度和证据引用；
- 查看本地 / CI 执行证据；
- 查看内容 Agent Profile 和四端宿主烟测边界。

## 小红书边界

小工具运行在离线沙箱中，因此不执行 Python、Shell、GitHub API 或 `verify.sh`，也不会实时扫描任意仓库。需要更新展示数据时，在仓库外重新生成报告并更新 `scorecard-data.js`，再重新打包。

上传 ZIP 时包含：`index.html`、`app.js`、`styles.css`、`scorecard-data.js`、`icon.svg` 和平台图标 `icon.png`。
