# 网易云动态头像 · 协议与逆向记录

本文是 `netease-dynamic-avatar` 技能的技术底稿：完整链路、接口字段、代码位置、实测数据。

## 1. 涉及的前端资源

| 文件 | 作用 |
|---|---|
| `pt_profile_update_<hash>.js` | 个人设置页逻辑，含头像上传与风控调用 |
| `core_<hash>.js` | NEJ 框架 + NOS 上传封装（`nm.x.nos`） |

定位方式：在 `https://music.163.com/user/update` 页面里读 `#g_iframe` 的 `script[src]`，找 `pt_profile_update` 和 `core`。

```js
[...document.querySelector('#g_iframe').contentDocument.querySelectorAll('script')]
  .map(s => s.src).filter(Boolean)
```

## 2. 上传头像完整链路

```
[1] POST /api/nos/token/alloc?filename=&ext=&type=&bucket=&local=&nos_product=&return_body=
      返回 result = { bucket, docId, objectKey, token }
[2] POST {nosup}/{bucket}/{objectKey}?offset=0&complete=true&version=1.0
      头: x-nos-token: <token>
      体: 文件原始字节
      返回: { requestId, offset, context, callbackRetMsg }   callbackRetMsg 是 base64 的 {"code":200}
[3] GET  /upload/event/img/v1?imgid=<docId>&format=<ext>
      返回 picInfo（含 originId / squareId / pcSquareId 等派生 id）
[4] GET  /upload/img/op?id=<docId>&op=<x>y<y>y<w>y<h>
      返回 { id: <新 id>, code: 200, url: <裁切后的图> }
      ← 这里对图片做服务端裁切 + 重编码
[5] POST /api/user/avatar/upload/v1     (form-urlencoded)
      imgid=<[4] 的新 id>&checkToken=<WM.getToken 结果>
      返回 { url, code: 200, message: "上传成功" }
```

### 2.1 `WM.getToken` 风控

```js
WM.getToken('bd5d2f973ef74cd2a61325a412ae54d9', function (token) { /* token ~170 字符 */ });
```

`WM` 挂在音乐站 window 上（`window.WM`，iframe 内也可取）。key 轮换时去 `pt_profile_update.js` 里 grep：

```
WM.getToken("
```

### 2.2 NOS 上传节点发现

```http
GET https://wanproxy.127.net/lbs?version=1.0&bucketname=yyimgs
→ { "lbs": "...", "upload": ["http://nosup-hz1.127.net", "http://103.129.255.21"] }
```

兜底节点：`https://nosup-hz1.127.net`。

### 2.3 token 里的 MimeLimit

把 `result.token` 的第三段（base64）解开可以看到策略：

```json
{
  "CallbackUrl": "https://music.163.com/api/nos/token/callback",
  "CallbackBody": "$(Bucket)&$(Object)&<resourceId>&{...}",
  "Bucket": "yyimgs",
  "ResourceId": 83916710321,
  "MimeLimit": "image/jpeg;image/png;image/gif;image/bmp;image/webp;image/jpg;image",
  "Region": "HZ",
  "Object": "<objectKey>",
  "Expires": 1793168262
}
```

**`MimeLimit` 明确包含 `image/webp`** —— 所以 WebP 本身完全被接受，问题从来不在格式。

## 3. 动图为什么失效

`/upload/img/op` 会裁切并重新编码。实测：

```
# 用动图 docId 打 op
GET /upload/img/op?id=109951174184305626&op=0y0y352y198
→ { "id": "109951174184309596", "code": 200, "url": ".../109951174184309596.jpg" }

# 取回新图
GET https://p1.music.126.net/.../109951174184309596.jpg
→ Content-Type: image/jpg
→ 魔数: ff d8 ff e0 00 10 4a 46 49 46    (JFIF，静态 JPEG)
→ 体积: 10269 B
```

**所有动画帧丢失。** 而跳过 op、直接用原始 docId：

```
GET https://p1.music.126.net/.../109951174184332768.jpg
→ Content-Type: image/jpg; charset=UTF-8   (CDN 按后缀给 content-type，内容不是)
→ 魔数: 52 49 46 46 .... 57 45 42 50      (RIFF....WEBP)
→ 块结构: VP8X x1, ANIM x1, ANMF x27
→ 体积: 112156 B
→ 三个尺寸 ?param=180y180 / 140y140 / 60y60 全部保持 27 帧
```

## 4. 关键接口速查

| 接口 | 方法 | 用途 |
|---|---|---|
| `/api/nos/token/alloc` | POST form | 拿 NOS 凭证 |
| `{nosup}/{bucket}/{objectKey}` | POST raw | 直传字节 |
| `/upload/event/img/v1` | GET | 生成 picInfo（可跳过） |
| `/upload/img/op` | GET | **裁切重编码，必须跳过** |
| `/api/user/avatar/upload/v1` | POST form | 设头像 |
| `/api/v1/user/detail/<uid>` | GET | 读 profile.avatarUrl / avatarImgId 验证 |
| `/api/user/profile/update` | POST form | 改昵称/签名等（含 avatarImgId 字段） |

## 5. 实测参数

| 项 | 值 |
|---|---|
| 源 GIF | 352×198，27 帧，100 ms/帧，总 2700 ms，449 KB |
| 输出 WebP | 240×240（居中正方裁切），27 帧，质量 75，method 4 → 112 KB |
| 同源 352×198 不裁切 | 质量 75 → 167 KB |
| 质量 60 / 90 | 128 KB / 362 KB |
| 体积硬限制 | 5 MB |

## 6. 踩坑记录

1. **本地 HTTP 服务器给页面取文件会被拦**：Chrome 的 Local Network Access 权限会让 `music.163.com` 页面对 `127.0.0.1` 的 fetch 直接 `Failed to fetch`，弹权限框也不一定放行。→ 改为本地脚本上传（模式 B）。
2. **CDN 的 `Content-Type` 不可信**：`p1.music.126.net/xxx.jpg` 返回 `image/jpg`，内容其实是 WebP。验证必须看魔数，不能看 header。
3. **去掉后缀直接访问 `p1.music.126.net/<hash>/<id>` 会 404**（返回 text/html 170 B）。必须带 `.jpg` 或 `.webp` 之类后缀。
4. **`docId` 与 `avatarImgId` 不同**：服务端会派生，`avatarImgId` 通常比 `docId` 大 2~4。以 API 返回的 `avatarUrl` 为准。
5. **UI 上传路径不可救**：只要点了「更换头像」，`op` 必跑。想保留动画只能走接口。
6. **Pillow 装全局失败**（Windows 上 `C:\Users\<u>\AppData\Roaming\Python` 无权限）：用 `python -m pip install --no-user --target ./pylibs pillow` 然后设 `PYTHONPATH`。
7. **PowerShell 的 `Invoke-WebRequest` 在本机可能因 schannel 凭证问题全线失败**（`SEC_E_NO_CREDENTIALS`），换 `node fetch` 或 `python urllib` 就正常。

## 7. 同类站点可复用性

凡是「NOS 直传 + `/upload/img/op` 裁切 + `imgid` 设头像」这套结构的网易系产品（歌单封面、用户背景图等）思路一致：找到裁切那一步，跳过它，用原始 docId。歌单封面同理支持动图。
