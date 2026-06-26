# Hacker News 每日新闻汇总（英中双语 + 飞书推送）
Version: 1.0.1
## 简介
自动抓取 Hacker News 前 10 条新闻，使用百度翻译 API 生成中文标题，并可选择推送到飞书群。

## 功能
- 获取 Hacker News 实时热门新闻
- 英中双语标题（百度翻译）
- 生成 Markdown 格式报告：`~/daily-news.md`
- 可选飞书机器人推送

## 依赖
- `bash`、`curl`、`jq`、`md5sum`（通常已安装）
- 百度翻译 API（免费，每月 100 万字符）
- 飞书自定义机器人（可选）

## 安装步骤

### 1. 获取百度翻译 API 密钥
- 访问 [百度翻译开放平台](https://fanyi-api.baidu.com/)
- 注册/登录，申请通用翻译 API（免费版）
- 记录 **App ID** 和 **密钥**

### 2. 创建飞书机器人（可选）
- 在飞书群中添加“自定义机器人”
- 复制 **Webhook URL**

### 3. 设置环境变量
将以下内容添加到 `~/.bashrc` 或执行脚本前 export：

```bash
export BAIDU_APPID="你的AppID"
export BAIDU_SECRET="你的密钥"
export FEISHU_WEBHOOK="你的飞书Webhook地址"   # 若不需推送可留空或不设置
