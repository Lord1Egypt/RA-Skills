# netease-dynamic-avatar

[![ClawHub](https://img.shields.io/badge/ClawHub-install-8a2be2)](https://clawhub.ai/yuan-dev39/skills/netease-dynamic-avatar)
[![Release](https://img.shields.io/github/v/release/yuan-dev39/netease-dynamic-avatar?color=c20c0c)](https://github.com/yuan-dev39/netease-dynamic-avatar/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> 给**自己的**网易云音乐账号设置**动态头像**（GIF / 动画 WebP）。一个可直接装进 DSH / Claude / 其他 harness 的 agent skill。

**核心结论**：`GIF → WebP → 改名 .jpg` 这套老办法之所以失效，不是因为网易云不支持 WebP，而是网页版「更换头像」上传完**必定**调一次 `/upload/img/op` 做服务端裁切，这个接口会把动图重编码成静态 JPEG，动画帧全部丢掉。

**破解点**：跳过 `/upload/img/op`，把动画 WebP 原始字节直传 NOS，然后用**原始 docId** 调 `/api/user/avatar/upload/v1`。实测 27 帧全部保留。

```
走 op 裁切          → ff d8 ff e0 (JPEG)      静态 1 帧
跳过 op + 原始docId → 52 49 46 46 (RIFF/WEBP) 27 帧动画
```

---

## 安装

### ClawHub（一行装，最省事）

已发布到 ClawHub：

```bash
openclaw skills install @yuan-dev39/netease-dynamic-avatar
```

也可以直接打开 [ClawHub 页面](https://clawhub.ai/yuan-dev39/skills/netease-dynamic-avatar) 点 Install。

### 一行装脚本

Linux / macOS / WSL：

```bash
curl -fsSL https://raw.githubusercontent.com/yuan-dev39/netease-dynamic-avatar/main/install.sh | bash
```

Windows PowerShell：

```powershell
irm https://raw.githubusercontent.com/yuan-dev39/netease-dynamic-avatar/main/install.ps1 -OutFile $env:TEMP\i.ps1; powershell -ExecutionPolicy Bypass -File $env:TEMP\i.ps1
```

### git clone

```bash
git clone https://github.com/yuan-dev39/netease-dynamic-avatar.git ~/.dsh/skills/netease-dynamic-avatar
```

```powershell
git clone https://github.com/yuan-dev39/netease-dynamic-avatar.git "$env:USERPROFILE\.dsh\skills\netease-dynamic-avatar"
```

### 手动 / 离线

从 [Releases](https://github.com/yuan-dev39/netease-dynamic-avatar/releases) 下载 `netease-dynamic-avatar-v1.0.0.zip`，解压到 `<DSH_HOME>/skills/netease-dynamic-avatar/`。`DSH_HOME` 默认 `~/.dsh`。只要目录里有 `SKILL.md` 就能被识别。

装好后重开一次会话（或刷新 DSH Web GUI），技能会自动出现在技能列表里，输入框旁的技能按钮里也能点选。触发词：

> 网易云动态头像 / 网易云头像动图 / 网易云头像不动 / 更换网易云头像 / GIF 头像 / 动态头像失效

### 其他 harness

- **Claude / 其他支持 SKILL.md 的 harness**：把 `SKILL.md` 放到对应 skills 目录，或直接把全文贴进上下文
- **只想用脚本**：完全不需要技能体系，见下面的「只拿脚本」

---

## 只拿脚本（不装技能）

```bash
# 1. 动图转动画 WebP（需要 Pillow）
python -m pip install --no-user --target ./pylibs pillow
PYTHONPATH=./pylibs python scripts/make_animated_webp.py input.gif out.webp --size 240 --quality 75

# 2. 浏览器 Console 里跑 set_dynamic_avatar.js，或
python scripts/upload_nos.py "<token>" "<objectKey>" out.webp image/webp
```

---

## 使用

### 前置

- 浏览器已登录 `music.163.com`
- Python 3.8+ 和 Pillow（转码用；纯浏览器模式不需要）
- 动图源文件（GIF 或动画 WebP），**小于 5 MB**

### 第 1 步：转成动画 WebP

```bash
python scripts/make_animated_webp.py input.gif out.webp --size 240 --quality 75
```

脚本会打印帧数、时长、体积，并校验输出确实是 `VP8X + ANIM + ANMF` 结构。要点：

- **宽高比必须 1:1**，否则客户端显示时会被裁圆。脚本默认做居中正方形裁切
- 尺寸 180~240 px，帧数 10~27，质量 75，体积 ~100 KB 最稳
- 必须真的多帧，静态 WebP 传上去当然不动

### 第 2 步：上传 + 设头像

**模式 A：纯浏览器（零依赖）**

打开 https://music.163.com 任意页面 → F12 → Console → 粘贴 [`scripts/set_dynamic_avatar.js`](scripts/set_dynamic_avatar.js) 全文 → 回车 → 选图。

脚本自动完成：取凭证 → 直传 NOS（跳过 op）→ 设头像 → **回读字节验证帧数**。

**模式 B：浏览器取凭证 + 本地脚本上传（更稳，绕开浏览器本地网络权限）**

浏览器 Console：

```js
const q = new URLSearchParams({
  filename:'a.jpg', ext:'jpg', type:'image', bucket:'yyimgs',
  local:'false', nos_product:'0',
  return_body: JSON.stringify({code:200, size:'$(ObjectSize)'})
});
const j = await (await fetch('/api/nos/token/alloc', {
  method:'POST', credentials:'include',
  headers:{'Content-Type':'application/x-www-form-urlencoded'},
  body: q.toString()
})).json();
console.log(j.result.token, j.result.objectKey, j.result.docId);
```

把三个值喂给本地脚本，再回浏览器设头像：

```js
const t = await new Promise(r => WM.getToken('bd5d2f973ef74cd2a61325a412ae54d9', r));
await (await fetch('/api/user/avatar/upload/v1', {
  method:'POST', credentials:'include',
  headers:{'Content-Type':'application/x-www-form-urlencoded'},
  body: new URLSearchParams({imgid:'<docId>', checkToken:t}).toString()
})).json();
```

### 第 3 步：验证（别只看「上传成功」）

`code:200 上传成功` **不代表动图保住了**。必须抓字节验魔数：

```js
const url = 'https://p1.music.126.net/<hash>/<id>.jpg';
const b = await (await fetch(url, {cache:'no-store'})).arrayBuffer();
const u = new Uint8Array(b);
console.log(String.fromCharCode(u[0],u[1],u[2],u[3]));  // 期望 RIFF
```

再数 `ANMF` 块 = 帧数，三个尺寸都验：`?param=180y180`、`?param=140y140`、`?param=60y60`。

---

## 关键参数速查

| 项 | 值 |
|---|---|
| NOS bucket | `yyimgs` |
| 凭证接口 | `POST /api/nos/token/alloc`（form-urlencoded） |
| 上传 host | `https://wanproxy.127.net/lbs?version=1.0&bucketname=yyimgs` 的 `upload[]`，兜底 `https://nosup-hz1.127.net` |
| 上传 URL | `{host}/yyimgs/{objectKey}?offset=0&complete=true&version=1.0` |
| 上传头 | `x-nos-token: <token>`、`Content-Type: image/webp` |
| 设头像 | `POST /api/user/avatar/upload/v1`，`imgid=<docId>&checkToken=<token>` |
| 风控 key | `bd5d2f973ef74cd2a61325a412ae54d9`（`WM.getToken`） |
| **要跳过的接口** | `GET /upload/img/op?id=&op=<x>y<y>y<w>y<h>` |

完整协议、逆向代码位置、实测数据见 [`references/protocol.md`](references/protocol.md)。

---

## 失败排查

| 现象 | 原因 / 处理 |
|---|---|
| 头像变了但还是静态 | 走了 UI 的「更换头像」，被 `op` 重编码。必须跳过 `op`，用原始 docId |
| `WM.getToken` 返回空 | 风控 key 轮换。grep `pt_profile_update.js` 里的 `WM.getToken("` 取新 key |
| 浏览器 fetch 本地/跨域失败 | Chrome 的 Local Network Access 权限；改用模式 B 本地脚本上传 |
| NOS 返回 4xx | `x-nos-token` 过期（约 1 小时），重新 alloc |
| 文件过大 | 降到 180×180、帧数 10~15、质量 70，能小 60% |
| 客户端看不到动效 | 头像有本地缓存，重开客户端；PC / 手机都需重进 |
| CDN 返回 `image/jpg` 但内容是 WebP | 正常。CDN 按 URL 后缀给 content-type，验证一律看魔数 |

---

## 目录结构

```
netease-dynamic-avatar/
├── SKILL.md                        # 技能主文件（harness 读取）
├── README.md
├── install.sh / install.ps1        # 一键安装
├── LICENSE
├── .github/workflows/
│   └── clawhub-publish.yml         # 打 tag 自动发 ClawHub
├── references/
│   └── protocol.md                 # 完整抓包 / 接口字段 / 逆向记录
└── scripts/
    ├── make_animated_webp.py       # GIF → 动画 WebP + 结构校验
    ├── set_dynamic_avatar.js       # 浏览器一键脚本（模式 A）
    └── upload_nos.py               # 本地 NOS 直传（模式 B）
```

---

## 发到 ClawHub

手动发布：

```bash
npm i -g clawhub
clawhub login
clawhub skill publish . \
  --slug netease-dynamic-avatar \
  --name "netease-dynamic-avatar" \
  --categories lifestyle,automation \
  --topics "netease,music-163,avatar,webp,dynamic-avatar"
```

自动化：仓库自带 `.github/workflows/clawhub-publish.yml`，配好 secret `CLAWHUB_TOKEN` 后打 tag 即自动发布。

```bash
git tag v1.0.1 && git push origin v1.0.1
```

---

## 红线

- 只操作用户自己的账号，或已明确授权的账号
- 不上传违规内容做头像
- 不把 `MUSIC_U` / `token` / `checkToken` 提交进任何仓库或截图

## License

MIT
