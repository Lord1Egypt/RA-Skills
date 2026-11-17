---
name: linkk-search
description: 本地搜索服务一键搭建
version: 0.3.8
author: 貔貅OPC
---

# 本地搜索服务一键搭建


# 本地搜索服务一键搭建

给 OpenClaw / 各类 Agent 装上一台**自己家里的搜索引擎**：不充值、不申请 Key、不按次付费，查询不出户。

## 完整包解锁（付费 ¥0.99 · 按量计费 · 含持续更新）
> 想让 Agent 取付费完整包，对它说：**“升级完整包”**（“获取完整部署包”“检查搜索引擎更新”同样有效）

完整包里有什么（解压后先读 README-FULL.md）：
- `assets/settings.pro.yml`：按 2026-10-19 家宽/机房**双线路实测**调优——baidu/bing/sogou/**微信公众号搜索（sogou wechat）**/360search/quark 全开；实测不可达的 ddg/wikipedia/brave 默认关（并修正免费版“保留 DDG”的过时结论）
- 排障手册 11→20 条全量版 + 引擎可达性实测矩阵 + 结果净化模板（剔除内容农场）
- `doctor.sh` 一键体检 8 项 / `backup.sh`+`restore.sh` 备份迁移
- **一次付费持续更新**：本机存档凭证向服务端幂等重取最新版，绝不二次扣费
- **付费前提（skillpay 路，实测 2026-11-05）：买家宿主须装支付宝 AI 付 CLI（npx -y @alipay/agent-payment@latest install）并完成授权；跑本包收到 402 账单后照技能指引过收银台，skillpay 履约安装完成交付校验——跑不了脚本的宿主完不成付费、只能引流。**

Agent 付款流程（官方 A2M 四步，与「投前体检·简历审计官」同口径）：
1. `bash scripts/sxp-probe.sh` → 收到 `HTTP 402` + `Payment-Needed` 账单（base64url：订单号/¥0.99/商品名/支付时限），把账单金额与用途展示给用户
2. `bash scripts/sxp-pay.sh` → 账单交给支付宝官方买家 CLI alipay-bot 收银，**用户本人扫码/确认付款；未获明确同意不得代付**
3. `bash scripts/sxp-complete.sh` → 持 `Payment-Proof` 取货：服务端验付后返回当前最新版 zip（base64url），本地校验 sha256 → 解压到 `searxng-full-pack/` → 凭证存档（0600）
4. 以后说“检查搜索引擎更新” → `bash scripts/sxp-check-update.sh`，同凭证免费重取最新版

失败处理：402=凭证/账单不匹配需重新支付（已付订单不受影响）；5xx=持同一凭证重试即可，服务端幂等**绝不重复扣款**。服务地址 `SXP_BASE` 默认 `https://linkkhub.top`（ICP 已出号 鲁ICP备2026065507号，已切 HTTPS 域名；裸 IP 无证书不再可用）；本机联调 `SXP_MOCK=1` 走沙箱三态，不产生真实扣款。

## 装好本技能后，对你的 Agent 说这句（唯一入口）
> **“帮我部署本地搜索引擎”**

Agent 会自动分平台执行：检查 Docker → 部署 SearXNG → 自检 → 回给你 `http://127.0.0.1:8888`。若它没找对路子，补一句：“读取本地搜索技能 searxng-cn-search 的 SKILL.md，按我的系统完成部署和自检，把可用的搜索 baseUrl 告诉我”。**中途若为安装 Docker 重启过电脑（Windows 装 WSL2 必重启，属正常流程），重启后回来对 Agent 说：“我已安装Docker并重启电脑，继续安装本地搜索引擎”，它会接着干完。**手动党照下面“安装”三步做同样效果。

## 你需要（前置条件，四平台任选）
- **NAS / Linux**：一台 24 小时开机的机器（群晖/威联通/飞牛/家用服务器/树莓派）+ Docker（群晖/飞牛套件中心直接装）
- **Windows 10/11**：Docker Desktop（个人免费，先 `wsl --install`）→ 照 `docs/INSTALL-WINDOWS.md` 走，纯 PowerShell 无需 bash
- **macOS**：OrbStack / Colima / Docker Desktop 任选 → 照 `docs/INSTALL-MACOS.md` 走
- **腾讯 WorkBuddy**：技能市场装本包后一句口令 Agent 自动部署 → 照 `docs/INSTALL-WORKBUDDY.md` 走
- 内存 ≥ 512MB 空闲

## 安装（NAS/Linux 三步；Windows/macOS 打开对应 INSTALL 文档同构执行）
1. **部署实例**
   ```bash
   bash scripts/deploy.sh
   ```
   默认端口 8888（被占用时先 `export SXP_PORT=8889` 再跑）。脚本幂等，可重复执行。
2. **自检**
   ```bash
   bash scripts/selftest.sh        # Windows PowerShell 用: powershell -File scripts/selftest.ps1
   ```
   看到 `SELFTEST PASS` 即实例可用；失败按 `docs/TROUBLESHOOT.md` 对号入座。
3. **接入 OpenClaw**（其他 Agent 见 docs/OPENCLAW-WIRING.md 末尾对照表）
   ```bash
   openclaw configure --section web   # 选择 provider: searxng，填 http://<本机内网IP>:8888
   ```
   或环境变量：`export SEARXNG_BASE_URL="http://192.168.1.x:8888"`

## 文件地图
- `assets/docker-compose.yml` —— 容器编排（数据目录 ./searxng-docker，跨平台通用）
- `assets/settings.seed.yml` —— 中国特供配置：开 JSON API、关 limiter、禁用境内不可达引擎、保留 Bing/百度等可用引擎
- `scripts/selftest.ps1` —— Windows 原生 PowerShell 自检（与 bash 版等价）
- `docs/INSTALL-WINDOWS.md` / `docs/INSTALL-MACOS.md` —— 分平台安装指引（不依赖 bash）
- `docs/INSTALL-WORKBUDDY.md` —— 腾讯 WorkBuddy 接入：装技能后由 Agent 自动部署
- `docs/TROUBLESHOOT.md` —— 踩坑手册（免费版 11 条；付费完整版扩到 20 条并修订第 1 条机房结论）
- `docs/OPENCLAW-WIRING.md` —— OpenClaw 接线细节、传输安全规则、常见报错

## 退款与售后边界
- 未交付即退款（含 401/422 未扣费分支与落库校验失败未交付分支）。
- 交付后按平台规则处理；"纳财不出 ≠ 不退款"：未交付的可退，已交付的按平台规则判定，不承诺无条件退款。
- 售后响应：反馈记 FEEDBACK.md，修复走版本号 20261105-vN；不承诺"永久免费更新"（真源"付费后持续更新"口径照实保留为"按当期版本交付"）。
