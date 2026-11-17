# 脉脉连接器

脉脉企业版已做成 bb-browser site adapter，三条命令：

```bash
bb-browser site maimai/me            # 账号与权限自检
bb-browser site maimai/talents 0 20  # 人才列表
bb-browser site maimai/jobs 20       # 在招职位
```

**所有 bb-browser 调用必须 `dangerouslyDisableSandbox: true`**——沙箱会拦住系统 Chrome 探测，报 "Cannot find a Chromium-based browser"。

## 判断登录态是否还活着

先跑 `maimai/me`。返回 uid/姓名说明登录态有效；返回 `error` + "需重新扫码登录"就走下面的登录流程。

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
python <仓库路径>/tools/make_qr.py $Q     # 输出文件名带 token 前缀，避免前端卡片复用旧缓存图
```

然后 `present_files` 展示二维码。**有效期约 60 秒**，生成到用户扫完必须压在一分钟内。

### 第 3 步：用户扫码后，一条命令跑完（不要拆开）

```bash
REDIR=$(bb-browser eval "(async()=>{const r=await fetch('/sdk/webs/platform/login-qrcode?qr_code=$Q&to=$TO_ENC',{credentials:'include'});const j=await r.json();return j.redir?j.redir:'NONE '+JSON.stringify(j)})()" --tab $TAB)
bb-browser goto "https://maimai.cn$REDIR" --tab $TAB
sleep 16
bb-browser eval "fetch('/api/ent/user/current?channel=www&uid=<YOUR_UID>&version=1.0.0',{credentials:'include'}).then(r=>r.text())" --tab $TAB
```

**不要开自动轮询脚本**：登录回调（set-auth-cookie?auth=JWT）是一次性的，被轮询脚本提前消费就白扫了。

## 硬约束（改动 adapter 前必读）

1. **所有 `/api/ent/*` 必须带 `uid=<UID>`**，否则 `21001 Incorrect parameters`。
   UID / CO_ID 占位符硬编码在三个 js 里，使用前替换成自己的账号信息（见 README「安装」）。
2. **认证靠浏览器登录态**（扫码后下发的 session cookie），不在 header 传 token。
   解密 cookie 用 curl 打接口行不通（返回 `20002 Invalid access token`）。
3. `user/current` 里的 `people_search: false` 是误导，真实权限看
   `/api/ent/search/user_search_pre_check` 的 `in_cid_whitelist`。
4. 二维码内容 = `taoumaimai://qr_login?login_id=<qr_code>`。
   轮询状态：`-11060005` 未扫描、`-11060004` 已失效、带 `redir` 即已扫码。

## 文件

- adapter：`sites/maimai/{talents,jobs,me}.js`（安装后位于 `~/.bb-browser/sites/maimai/`）
- 二维码生成：`tools/make_qr.py`（需 `pip install qrcode pillow`，国内可用阿里源）
