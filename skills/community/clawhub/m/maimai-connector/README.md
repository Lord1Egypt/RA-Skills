# 脉脉连接器（maimai-connector）

脉脉企业版 bb-browser site adapter：通过浏览器登录态调用脉脉企业版 Web 接口，
实现账号自检、人才列表抓取、在招职位查询。

## 原理

- 认证靠**浏览器登录态**（扫码登录后下发的 session cookie），不在 header 传 token
  （用 curl 直接打接口会返回 `20002 Invalid access token`）
- 所有 `/api/ent/*` 接口必须带 `uid=<当前账号 uid>`，否则返回 `21001 Incorrect parameters`

## 安装

1. 把 `sites/maimai/` 下三个 js 复制到 bb-browser 的站点目录：

```bash
cp sites/maimai/*.js ~/.bb-browser/sites/maimai/
```

2. 编辑三个 js 文件顶部的占位符：

```js
var UID = '<YOUR_UID>';      // 你的脉脉企业版账号 uid
var CO_ID = '<YOUR_CO_ID>';  // 你的企业 co_id（仅 me.js 使用）
```

uid 可在登录后通过 `user/current` 接口响应或 `maimai/me` 的返回中查看；
co_id 来自企业版账号信息。

3. 安装二维码生成依赖：

```bash
pip install qrcode pillow
```

## 使用

```bash
bb-browser site maimai/me            # 账号与权限自检
bb-browser site maimai/talents 0 20  # 人才列表（人才银行/推荐位）
bb-browser site maimai/jobs 20       # 在招职位
```

**所有 bb-browser 调用建议在沙箱外执行**——沙箱会拦住系统 Chrome 探测，
报 `Cannot find a Chromium-based browser`。

## 判断登录态是否存活

先跑 `maimai/me`：返回 uid/姓名说明登录态有效；返回 `error` + "需重新扫码登录"就走下面的登录流程。

## 登录态失效时：重新扫码（完整流程）

难点在于**浏览器会话会被环境回收**（每条 bash 命令结束 Chrome 被强杀），所以顺序很关键。

### 第 1 步：起心跳，钉住会话

```bash
while true; do bb-browser tab list > /dev/null 2>&1; sleep 4; done   # run_in_background + 沙箱外
```

必须是**持续调用 bb-browser** 的任务。单纯 `sleep` 的后台任务无效——它不调用浏览器，守护进程照样被回收。
验证方式：另起一条命令执行 `bb-browser tab list`，看 tab ID 是否还在。

### 第 2 步：开登录页，生成二维码

```bash
bb-browser open "https://maimai.cn/platform/login?to=https%3A%2F%2Fmaimai.cn%2Fent%2Fv41%2Frecruit%2Ftalents%3Ftab%3D1"
# 记下 TAB；sleep 7
Q=$(bb-browser eval "fetch('/sdk/webs/platform/get-qr-code',{credentials:'include'}).then(r=>r.json()).then(j=>j.qr_code||'')" --tab $TAB)
python tools/make_qr.py $Q   # 输出文件名带 token 前缀，避免前端卡片复用旧缓存图
```

展示二维码。**有效期约 60 秒**，生成到用户扫完必须压在一分钟内。

### 第 3 步：用户扫码后，一条命令跑完（不要拆开）

```bash
REDIR=$(bb-browser eval "(async()=>{const r=await fetch('/sdk/webs/platform/login-qrcode?qr_code=$Q&to=$TO_ENC',{credentials:'include'});const j=await r.json();return j.redir?j.redir:'NONE '+JSON.stringify(j)})()" --tab $TAB)
bb-browser goto "https://maimai.cn$REDIR" --tab $TAB
sleep 16
bb-browser eval "fetch('/api/ent/user/current?channel=www&uid=<YOUR_UID>&version=1.0.0',{credentials:'include'}).then(r=>r.text())" --tab $TAB
```

**不要开自动轮询脚本**：登录回调（`set-auth-cookie?auth=JWT`）是一次性的，
被轮询脚本提前消费就白扫了。

## 硬约束（改动 adapter 前必读）

1. **所有 `/api/ent/*` 必须带 `uid=<UID>`**，否则 `21001 Incorrect parameters`。
   UID 硬编码在三个 js 里，换账号要改。
2. **认证靠浏览器登录态**，不在 header 传 token。
3. `user/current` 里的 `people_search: false` 是误导，真实权限看
   `/api/ent/search/user_search_pre_check` 的 `in_cid_whitelist`。
4. 二维码内容 = `taoumaimai://qr_login?login_id=<qr_code>`。
   轮询状态：`-11060005` 未扫描、`-11060004` 已失效、带 `redir` 即已扫码。

## 文件结构

```
├── sites/maimai/
│   ├── me.js        账号与搜索权限自检
│   ├── talents.js   人才列表（姓名/公司/职位/活跃度/主页链接）
│   └── jobs.js      在招职位（含薪资/城市/学历/经验要求）
├── tools/
│   └── make_qr.py   按脉脉协议生成登录二维码 PNG
├── SKILL.md         Agent 可执行的 skill 说明（与本文档同源）
└── README.md
```

## 声明

- 本项目仅用于自有账号下的招聘数据管理，请遵守脉脉用户协议及当地法律法规
- 抓取数据请勿用于违反平台条款的用途，使用者自行承担使用后果

## License

[MIT](LICENSE)
