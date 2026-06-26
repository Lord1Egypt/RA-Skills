# M-Team to Transmission - OpenClaw Skill

这是一个为 OpenClaw 开发的自动化技能（Skill）。它可以让大模型通过自然语言对话，从 M-Team 搜索影视资源，并自动将用户选定的种子推送到本地的 Transmission 进行下载。

## ✨ 特色功能
- 💬 自然语言点播：直接告诉 AI 想看什么。
- 🥇 智能排序：自动识别并优先展示带有“中文字幕/国配”的资源，按做种数降序排列。
- 🗂️ 自动分类：根据 M-Team 分类，自动推送到 NAS 的对应文件夹（电影/剧集分离）。
- 🛡️ 防拦截装甲：完美绕过 Cloudflare 502 拦截。

## 🛠️ 安装与配置
1. 将本仓库克隆到你的 OpenClaw skills 目录下。
2. 安装依赖：`pip install requests transmission-rpc`
3. 配置环境变量或在 `main.py` 中填入你的：
   - `MTEAM_API_KEY`
   - Transmission 的 `IP`、`端口`、`账号`、`密码`
4. 根据你的 NAS 实际情况，修改 `main.py` 中的 `CATEGORY_PATH_MAPPING` 目录映射。
5. 重启 OpenClaw 网关服务。