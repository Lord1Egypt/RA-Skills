---
name: netease-dynamic-avatar
description: "网易云音乐网页版设置「动态头像」（GIF/动图头像）的完整可复现流程。破解了网页版「更换头像」必走 /upload/img/op 服务端裁切导致动图被压成静态 JPEG 的问题，改为跳过裁切、直传 NOS 原始动画 WebP 字节再用原始 docId 设头像。包含 GIF→动画 WebP 转换、NOS 直传、风控 checkToken、逐帧验证与失败排查。触发词：网易云动态头像、网易云头像动图、网易云头像不动、music.163 动态头像、更换网易云头像、GIF 头像、webp 头像、动态头像失效。"
---

# 网易云音乐 · 动态头像（Animated Avatar）

给**自己的**网易云音乐账号把头像换成动图（GIF/动画 WebP）。适用于网页版个人设置里的「更换头像」功能，只是绕开了它的图片处理链路。

## 适用场景

- 用户说：网易云头像想弄成动态的 / 头像不动了 / GIF 转 webp 改名 jpg 上传失效了
- 需要复现或修复「上传成功但头像变成静态图」
- 需要给同类站点（同样走 NOS + `/upload/img/op` 裁切）做动图头像

## 原理（为什么老办法会失效）

网页版 `更换头像` 的完整链路（从 `pt_profile_update.js` + `core.js` 逆向得到）：

```
选文件
 → POST /api/nos/token/alloc        (bucket=yyimgs，拿 token/objectKey/docId)
 → POST {nosup}/yyimgs/{objectKey}  (直传原始字节，x-nos-token 头)
 → GET  /upload/event/img/v1        (生成 picInfo)
 → GET  /upload/img/op?id=&op=x y w h   ← 罪魁祸首：服务端裁切 + 重编码
 → POST /api/user/avatar/upload/v1  (imgid = 上一步的新 id)
```

`/upload/img/op` 会把图裁成 180×180 并**重新编码**。实测拿动图 id 打这个接口，返回的新 id 取回来是 `ff d8 ff e0`（JPEG 魔数），**所有动画帧被丢弃**。

结论：不是 WebP 格式不被接受（NOS 的 `MimeLimit` 明确包含 `image/webp`），而是上传完必定跑一遍 `op`。所以「GIF→WebP→改名 .jpg」这条路在 UI 上永远出不来动图。

**破解点**：跳过 `/upload/img/op`，把动画 WebP 原始字节直传 NOS，然后直接拿**原始 docId** 去调 `/api/user/avatar/upload/v1`。

实测对比：

| 路径 | 取回内容 |
|---|---|
| 走 `/upload/img/op` 裁切 | `ff d8 ff e0` JPEG，静态 1 帧 |
| 跳过 op，直传 + 原始 docId | `RIFF....WEBP` + `VP8X/ANIM/ANMF`，27 帧动画 |

## 前置检查

1. 浏览器已登录 music.163.com（`MUSIC_U` cookie 存在，或页面已渲染出个人信息）
2. 本地有动图源文件（GIF / 动画 WebP）
3. 需要 Python + Pillow（转码用）。Pillow 装不进全局环境时用 `--target` 装到工作区：

```bash
python -m pip install --no-user --target ./pylibs pillow
export PYTHONPATH=./pylibs     # Windows: $env:PYTHONPATH="...\pylibs"
```

## 步骤

### 1. 转成动画 WebP

```bash
python scripts/make_animated_webp.py input.gif out.webp --size 240 --quality 75
```

脚本会打印帧数、每帧时长、输出体积，并校验输出确实是 `VP8X + ANIM + ANMF` 结构。

要点：
- **宽高比必须 1:1**，否则客户端显示时会被裁圆。脚本**默认做居中正方形裁切**，不想裁切加 `--no-square`
- 尺寸建议 180×180 ~ 240×240，帧数 10~27，质量 75，体积控制在 100 KB 上下
- 必须 < 5 MB（服务端硬限制）
- 静态 WebP 传上去当然不动，务必确认 `ANMF` 帧数 > 1

### 2. 在浏览器里执行上传

两种模式，任选：

**模式 A：纯浏览器（推荐，零依赖）**

打开 https://music.163.com 任意页面 → F12 → Console → 粘贴 `scripts/set_dynamic_avatar.js` → 选图。

脚本做四件事：`/api/nos/token/alloc` 取凭证 → 直传 NOS（**不调 op**）→ `/api/user/avatar/upload/v1` 设头像 → 回读字节验证帧数。

**模式 B：浏览器取凭证 + 本地脚本上传（更稳）**

浏览器 Console 跑：

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

把三个值喂给本地脚本（绕开浏览器 CORS / 本地网络权限问题）：

```bash
python scripts/upload_nos.py "<token>" "<objectKey>" out.webp image/webp
```

然后回浏览器设头像：

```js
const t = await new Promise(r => WM.getToken('bd5d2f973ef74cd2a61325a412ae54d9', r));
await (await fetch('/api/user/avatar/upload/v1', {
  method:'POST', credentials:'include',
  headers:{'Content-Type':'application/x-www-form-urlencoded'},
  body: new URLSearchParams({imgid:'<docId>', checkToken:t}).toString()
})).json();
```

### 3. 验证（必做，不能只看「上传成功」）

`/api/user/avatar/upload/v1` 返回 `code:200 上传成功` **不代表动图保住了**。必须抓字节验魔数：

```js
const url = 'https://p1.music.126.net/<hash>/<id>.jpg';
const b = await (await fetch(url, {cache:'no-store'})).arrayBuffer();
const u = new Uint8Array(b);
console.log(String.fromCharCode(u[0],u[1],u[2],u[3]));  // 期望 RIFF
// 再数 ANMF 块数量 = 帧数
```

三个尺寸都要验：`?param=180y180`、`?param=140y140`、`?param=60y60`，全部应是 `RIFF...WEBP` 且帧数一致。

再确认账号侧生效：

```js
await (await fetch('/api/v1/user/detail/<uid>', {credentials:'include'})).json()
// profile.avatarUrl 应指向新图，profile.avatarImgId 应更新
```

## 关键参数表

| 项 | 值 |
|---|---|
| NOS bucket | `yyimgs` |
| 凭证接口 | `POST /api/nos/token/alloc`（form-urlencoded） |
| 上传 host | 先查 `https://wanproxy.127.net/lbs?version=1.0&bucketname=yyimgs` 的 `upload[]`，兜底 `https://nosup-hz1.127.net` |
| 上传 URL | `{host}/yyimgs/{objectKey}?offset=0&complete=true&version=1.0` |
| 上传头 | `x-nos-token: <token>`、`Content-Type: image/webp` |
| 设头像 | `POST /api/user/avatar/upload/v1`，body `imgid=<docId>&checkToken=<token>` |
| 风控 key | `bd5d2f973ef74cd2a61325a412ae54d9`（`WM.getToken`） |
| 裁切接口（要跳过） | `GET /upload/img/op?id=&op=<x>y<y>y<w>y<h>` |

## 失败排查

| 现象 | 原因 / 处理 |
|---|---|
| 头像变了但还是静态 | 走了 UI 的「更换头像」，被 `op` 重编码。必须跳过 `op`，用原始 docId |
| `WM.getToken` 返回空 | 风控 key 轮换了。grep `pt_profile_update.js` 里的 `WM.getToken("` 取新 key |
| 浏览器 fetch 本地/跨域失败 | Chrome 的 Local Network Access 权限；改用模式 B 本地脚本上传 |
| NOS 返回 4xx | 检查 `x-nos-token` 是否过期（token 有效期约 1 小时），重新 alloc |
| 文件过大 | 降到 180×180、帧数 10~15、质量 70，能小 60% |
| 客户端看不到动效 | 头像有本地缓存，重开客户端；PC/手机都需重进 |
| CDN 返回 `image/jpg` 但内容是 WebP | 正常，按 URL 后缀给 content-type。验证一律看魔数 |
| `docId` 与 `avatarImgId` 差几位 | 正常，服务端会派生 id，以 API 返回的 `avatarUrl` 为准 |

## 红线

- 只操作用户自己的账号，或已明确授权的账号
- 不上传违规内容做头像
- 不把 `MUSIC_U` / `token` / `checkToken` 写进任何仓库或截图

## 参考

- `references/protocol.md` — 完整抓包记录、接口字段、逆向代码位置
- `scripts/make_animated_webp.py` — GIF/动图 → 动画 WebP 转码 + 结构校验
- `scripts/set_dynamic_avatar.js` — 浏览器一键脚本（模式 A）
- `scripts/upload_nos.py` — 本地 NOS 直传（模式 B）
