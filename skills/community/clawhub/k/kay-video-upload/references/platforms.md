# 各平台说明

## 抖音
- 登录：Playwright 打开 creator.douyin.com，扫码
- cookie：`cookies/douyin_uploader/account.json`
- 支持：标题、标签、封面、定时发布（默认明天 16:00）、商品链接

## 视频号
- 登录：微信扫码
- cookie：`cookies/tencent_uploader/account.json`
- 支持：标题、标签、封面、定时发布

## 快手
- 登录：扫码
- cookie：`cookies/ks_uploader/account.json`
- 支持：标题、标签、定时发布

## 小红书
- 登录：手动登录后按 Enter 保存状态
- cookie：`cookies/xiaohongshu_uploader/account.json`
- 依赖：XHS_SERVER 签名服务需在 `http://127.0.0.1:11901` 运行（可用 Docker 启动）
- 支持：标题、标签、封面

## B站
- 登录：biliup.exe 扫码（`uploader/bilibili_uploader/biliup.exe`）
- cookie：`cookies/bilibili_uploader/account.json`（JSON 格式，含 SESSDATA 等字段）
- 默认分区：野生技能协会（`VideoZoneTypes.KNOWLEDGE_SKILL`），可在 `publish.py` 中修改 `tid`
- 发布间隔：每条视频之间自动等待 30 秒（B站限速）
- 支持：标题、描述、分区、标签、定时发布

## cookie 有效期
| 平台 | 有效期 |
|------|--------|
| 抖音 | ~30 天 |
| 视频号 | ~30 天 |
| 快手 | ~30 天 |
| 小红书 | ~7 天 |
| B站 | ~180 天 |

过期后重新运行对应平台的 `python publish.py login <platform>` 即可。
