# 快速上手：生成你的「可对话个人简历」

本 Skill 帮你把一份简历，变成一个**能对话的单文件网页**——访客用中文提问（工作经历 / 项目 / 技能 / 教育 / 论文等），网页即时回答。配套微信分享图与可部署链接，发给朋友、HR、客户一键看。

特点：单文件 HTML、零依赖、纯离线、无需后端、无需联网、无需大模型。

## 一、你需要准备
- Python 3（建议用 WorkBuddy 托管版）
- 图像脚本依赖：`Pillow` + `qrcode`（生成封面图、分享卡片用）
  - 安装：`pip install Pillow qrcode`
- 中文 Windows 字体：`C:/Windows/Fonts/msyh.ttc`（雅黑，注意是 **.ttc 不是 .ttf**）

## 二、三步出成品

### 第 1 步：填你的简历数据
- 打开 `scripts/make_resume.py`，改顶部的 `RESUME` 字典：
  - `name` 姓名、`title` 头衔、`subtitle` 一句话标签
  - `contact` 联系方式（电话 / 邮箱）
  - `sections` 六大板块文本：基本信息 / 工作经历 / 核心 Skills / 重点项目 / 教育背景 / 论文专著
  - `rules` 关键词 → 板块映射（控制"问什么答什么"）
  - `expire` 有效期：`None`=永久；填 `"2026-12-31T23:59:59+08:00"` 则到期整页提示
- 或：写成 `resume.json` 用 `--data` 传入（字段同 RESUME）

### 第 2 步：生成网页 + 分享图
- 生成单文件网页（纯标准库，无需 Pillow）：
  - `python scripts/make_resume.py --out index.html`
- 生成微信封面图（需 Pillow）：
  - `python scripts/gen_cover.py --name "你的名字" --title "AI博士 · 数据科学家" --out cover.png`
- 生成带二维码的分享卡片图（需 Pillow + qrcode）：
  - `python scripts/gen_share_card.py --url "你的部署链接" --name "你的名字" --out share_card.png`
  - 说明：`--url` 必填（部署后拿到）；发出去后对方**长按二维码**即开网页

### 第 3 步：部署成链接
- 把目录（index.html + cover.png + share_card.png）部署到静态托管（如 WorkBuddy CloudStudio）
- 得到 `https://xxxx.gz3.agentos-app.net` 公开链接
- 同一沙箱复用、链接不变；管理在「设置 - 数据管理 - 我发布的应用」

## 三、注意事项
- **隐私**：网页含真实电话 / 邮箱 / 年薪，公开链接即任何人可见；敏感场景加访问口令或接真后端鉴权（见 wechat-sharing.md）
- **微信机制**：聊天框粘贴链接只显示纯蓝链、不渲染封面卡片；所以用"带二维码分享卡片图"绕过——发给朋友长按识别即开
- **图像脚本解释器**：若用 WorkBuddy 托管 Python，请走装了 Pillow/qrcode 的 venv；`make_resume.py` 纯标准库任意 Python 可跑

## 四、进阶
- 想让简历"真 AI 自由对话"（而非关键词匹配）：看 `references/wechat-sharing.md` 的"真 AI 扩展"一节，把前端匹配换成大模型后端
- 想发布到技能市场分享给别人：打包本目录为 zip 上传「技能市场」即可
