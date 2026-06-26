# 平台 API 对接手册

## 抖音开放平台

**鉴权方式**：OAuth 2.0

**申请入口**：https://open.douyin.com/

**所需权限**：
- `data.external.user` — 用户数据
- `data.external.item` — 内容数据

**获取 Access Token**：
```bash
curl -X POST "https://open.douyin.com/oauth/access_token/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_key=YOUR_CLIENT_KEY&client_secret=YOUR_CLIENT_SECRET&code=AUTH_CODE&grant_type=authorization_code"
```

**查询账号数据**：
```bash
# 获取用户粉丝数、点赞数等基础数据
curl "https://open.douyin.com/data/external/user/fans/data/" \
  -H "access-token: YOUR_ACCESS_TOKEN" \
  -d '{"open_id":"YOUR_OPEN_ID","date_type":7}'
```

**关键字段映射**：
| 平台字段 | 标准字段 |
|---------|---------|
| play_count | views |
| digg_count | likes |
| comment_count | comments |
| share_count | shares |
| new_fans | new_followers |
| total_fans | total_followers |

---

## 小红书创作者中心

**鉴权方式**：Cookie（无官方开放 API）

**获取 Cookie**：
1. 登录 https://creator.xiaohongshu.com/
2. 打开浏览器开发者工具 → Network
3. 复制请求头中的 `Cookie` 字段值
4. 存入 `.env` 文件：`XIAOHONGSHU_COOKIE=...`

**数据采集**（非官方，稳定性较低）：
```bash
curl "https://creator.xiaohongshu.com/api/galaxy/creator/data/note_stats" \
  -H "Cookie: $XIAOHONGSHU_COOKIE" \
  -H "X-Sign: ..." \
  -d '{"start_date":"2026-03-31","end_date":"2026-03-31"}'
```

**注意**：Cookie 通常 7-14 天过期，需定期更新。

**关键字段映射**：
| 平台字段 | 标准字段 |
|---------|---------|
| view_count | views |
| liked_count | likes |
| comment_count | comments |
| collected_count | favorites |
| fans_count | total_followers |

---

## 微信视频号数据助手

**鉴权方式**：企业微信 Access Token

**申请入口**：https://work.weixin.qq.com/

**获取 Access Token**：
```bash
curl "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=YOUR_CORPID&corpsecret=YOUR_CORPSECRET"
```

**查询数据**：
```bash
curl -X POST "https://api.weixin.qq.com/datacube/getweanalysisappiddailysummarytrend" \
  -H "Content-Type: application/json" \
  -d '{"access_token":"TOKEN","begin_date":"20260331","end_date":"20260331"}'
```

---

## B站创作中心

**鉴权方式**：Cookie（SESSDATA）

**获取方式**：登录 https://member.bilibili.com/ 后从 Cookie 中提取 `SESSDATA`

**查询数据**：
```bash
curl "https://member.bilibili.com/x/web/data/overview" \
  -H "Cookie: SESSDATA=YOUR_SESSDATA" \
  -d "start_time=1743350400&end_time=1743436800"
```

**关键字段映射**：
| 平台字段 | 标准字段 |
|---------|---------|
| play | views |
| like | likes |
| reply | comments |
| share | shares |
| coin | favorites |
| fans | new_followers |

---

## 微博数据中心

**鉴权方式**：微博开放平台 OAuth 2.0

**申请入口**：https://open.weibo.com/

**获取 Access Token**：
```bash
curl -X POST "https://api.weibo.com/oauth2/access_token" \
  -d "client_id=APP_KEY&client_secret=APP_SECRET&grant_type=authorization_code&code=AUTH_CODE&redirect_uri=REDIRECT_URI"
```

**查询数据**：
```bash
curl "https://api.weibo.com/2/statuses/user_timeline.json?access_token=TOKEN&uid=UID&count=20"
```

---

## .env 配置模板

```env
# 抖音
DOUYIN_CLIENT_KEY=your_client_key
DOUYIN_CLIENT_SECRET=your_client_secret
DOUYIN_ACCESS_TOKEN=your_access_token
DOUYIN_OPEN_ID=your_open_id

# 小红书
XIAOHONGSHU_COOKIE=your_cookie_string

# 视频号
WEIXIN_CORP_ID=your_corp_id
WEIXIN_CORP_SECRET=your_corp_secret

# B站
BILIBILI_SESSDATA=your_sessdata
BILIBILI_UID=your_uid

# 微博
WEIBO_ACCESS_TOKEN=your_access_token
WEIBO_UID=your_uid
```
