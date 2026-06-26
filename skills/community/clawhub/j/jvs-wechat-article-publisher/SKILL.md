---
name: wechat-article-publisher
description: 微信公众号文章排版和发布技能。提供专业排版模板、图片上传、草稿发布等完整工作流。使用场景：(1) 创建公众号文章，(2) 上传图片到素材库，(3) 发布草稿到微信后台，(4) 装修案例/干货分享/客户故事等类型文章。
---

# WeChat Article Publisher

微信公众号文章排版和发布技能。

---

## 📋 使用前准备（首次使用必读！）

### 1. 微信公众号要求

- ✅ 需要已注册的**微信公众号**（服务号或订阅号均可）
- ✅ 需要公众号的 **AppID** 和 **AppSecret**
- ⚠️ 公众号需要通过微信认证（未认证账号部分 API 受限）

### 2. 获取 AppID 和 AppSecret

1. 登录 [微信公众平台](https://mp.weixin.qq.com)
2. 进入 **开发 → 基本配置**
3. 复制 **开发者 ID** 中的：
   - `AppID(应用 ID)` - 类似 `你的 APPID`
   - `AppSecret(应用密钥)` - 类似 `你的 APPSECRET`

### 3. 配置 IP 白名单（重要！）

微信 API 要求配置服务器 IP 白名单：

1. 在 **开发 → 基本配置** 页面
2. 找到 **IP 白名单** 设置
3. 添加你的服务器公网 IP：
   - 本地测试：查询本机公网 IP（访问 https://ip.sb）
   - 服务器：填写服务器的公网 IP 地址
   - 可添加多个 IP，用逗号分隔

**常见 IP 白名单配置：**
```json
{
  "ipWhitelist": ["你的公网 IP", "你的服务器 IP 2", "你的服务器 IP 1"]
}
```

### 4. 创建配置文件

在技能目录创建 `config.json`：

```json
{
  "appId": "你的 AppID",
  "appSecret": "你的 AppSecret",
  "ipWhitelist": ["你的公网 IP"]
}
```

⚠️ **安全提醒**：
- `config.json` 包含敏感信息，**不要上传到 ClawHub**
- 只保留 `config.example.json` 作为示例
- 真实配置文件应加入 `.gitignore`

### 5. 验证配置

运行测试命令验证配置是否正确：

```bash
# 获取 token（成功会返回一串字符）
curl -s "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=你的 APPID&secret=你的 APPSECRET"
```

**成功响应：**
```json
{"access_token":"ACCESS_TOKEN","expires_in":7200}
```

**失败响应：**
```json
{"errcode":40013,"errmsg":"invalid appid"}
```

---
## 🔴 严重警告：中文乱码问题（必读！）

**问题现象**：发布后文章内容显示为 `<p>这是文字</p>` 标签，而不是正常中文。

**根本原因**：
1. ❌ Python requests 库默认编码不是 UTF-8
2. ❌ Content-Type 头未指定 `charset=utf-8`
3. ❌ Token 过期导致 API 异常处理

**✅ 正确解决方案（必须遵守！）**：

```bash
# ========== 第 1 步：获取最新 token（每次发布前都要重新获取！） ==========
TOKEN=$(curl -s "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=SECRET" | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))")

# ========== 第 2 步：上传封面图 ==========
COVER=$(curl -s -X POST "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=$TOKEN&type=image" -F "media=@/path/to/cover.jpg" | python3 -c "import sys,json; print(json.load(sys.stdin).get('media_id',''))")

# ========== 第 3 步：发布草稿（关键：-H "Content-Type: application/json; charset=utf-8"） ==========
curl -s -X POST "https://api.weixin.qq.com/cgi-bin/draft/add?access_token=$TOKEN" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d "{\"articles\":[{\"title\":\"标题\",\"content\":\"<p>中文内容</p>\",\"thumb_media_id\":\"$COVER\"}]}"
```

**⚠️ 四个必须（缺一不可！）**：
1. ✅ **每次发布前都重新获取 token** - token 有效期只有 2 小时
2. ✅ **必须指定 `charset=utf-8`** - `-H "Content-Type: application/json; charset=utf-8"`
3. ✅ **必须用 curl 命令** - 不要用 Python requests（编码不可靠）
4. ✅ **必须手机扫码预览** - PC 预览可能显示 Unicode（未验证账号）

**🧪 测试命令**（发布前先用这个验证编码）：
```bash
curl -s -X POST "https://api.weixin.qq.com/cgi-bin/draft/add?access_token=$TOKEN" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d "{\"articles\":[{\"title\":\"测试文字\",\"content\":\"<p>这是中文测试</p><p>能看到吗</p>\",\"thumb_media_id\":\"$COVER\"}]}"
```

**❌ 错误做法（不要再犯！）**：
- 使用 Python `requests.post(url, json=data)` 直接发布
- 复用旧 token（超过 2 小时）
- 不指定 `charset=utf-8`
- 只在 PC 端预览，不用手机扫码

---

## 快速开始

### 发布文章（推荐方式）

```bash
# 使用 curl 命令发布（见上方「严重警告」章节的完整命令）
```

### 上传图片

```bash
python3 scripts/upload_images.py /path/to/images/
```

---

## 排版模板

### 专业版模板（推荐）

适用于装修案例、实景展示等专业内容。

**特点：**
- 英文 + 中文双语标题（如 LIVING ROOM · 客厅）
- 奶油色配色方案（#f5e6d3、#8b7355）
- 标题底部装饰线
- 表格相间背景色
- 预约框圆角背景

**模板文件：** `assets/templates/professional.md`

### 简洁版模板

适用于快讯、通知等简单内容。

**模板文件：** `assets/templates/simple.md`

---

## 文章结构

### 标准结构

1. **封面大图** - 标题后第一张就是图片
2. **项目信息** - 小区/面积/风格/造价表格
3. **空间展示** - 客厅/餐厅/卧室/厨房等
4. **费用明细** - 分类费用表格
5. **改造亮点** - 项目亮点列表
6. **预约量房** - CTA 行动号召
7. **联系我们** - 公司信息

### 图片规则

- 每个空间 1-2 张图
- 图片宽度 100%，最大 600px
- 图片间留白 20px
- 封面图单独指定

---

## 发布流程

### 步骤 1：准备文章

```markdown
# 文章标题

<img src="封面图 URL">

---

## 空间 1

<img src="图片 URL">

说明文字

---

## 空间 2

...
```

### 步骤 2：上传图片

```bash
python3 scripts/upload_images.py /path/to/images/
# 输出图片 URL 列表
```

### 步骤 3：插入 URL

将上传的图片 URL 替换文章中的占位符。

### 步骤 4：发布草稿

**唯一推荐方式（curl 命令）：**

```bash
# 1. 获取 token
TOKEN=$(curl -s "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=你的 APPID&secret=你的 APPSECRET" | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))")

# 2. 上传封面
COVER=$(curl -s -X POST "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=$TOKEN&type=image" -F "media=@/path/to/cover.jpg" | python3 -c "import sys,json; print(json.load(sys.stdin).get('media_id',''))")

# 3. 发布（注意：-H "Content-Type: application/json; charset=utf-8"）
curl -s -X POST "https://api.weixin.qq.com/cgi-bin/draft/add?access_token=$TOKEN" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d "{\"articles\":[{\"title\":\"标题\",\"content\":\"<p>中文内容</p>\",\"thumb_media_id\":\"$COVER\"}]}"
```

**❌ 禁止使用 Python 脚本直接发布**（会导致乱码）

### 步骤 5：手动发表

登录微信后台 → 草稿箱 → 检查 → 点发表

---

## 配置

配置文件：`config.json`

```json
{
  "appId": "你的 AppID",
  "appSecret": "你的 AppSecret",
  "ipWhitelist": ["你的服务器 IP 1", "你的服务器 IP 2"]
}
```

---

## 常见问题

### 🔴 中文乱码（最重要！）

**现象**：文章显示为 `<p>这是文字</p>` 标签

**原因**：编码格式不正确

**解决方案**：
1. 使用 curl 命令发布
2. 必须指定 `-H "Content-Type: application/json; charset=utf-8"`
3. 每次发布前重新获取 token

### API 48001 错误

微信 API 未授权，无法直接发布。

**解决方案：** 使用草稿 API + 手动发表工作流。

### 图片不显示

图片未上传到微信素材库。

**解决方案：** 先用 `upload_images.py` 上传图片获取 URL。

### 排版错乱

Markdown 格式不正确。

**解决方案：** 使用提供的模板文件。

---

## 脚本说明

### publish_wechat.py

发布文章到微信草稿箱。

```bash
python3 scripts/publish_wechat.py <article.md> [options]

选项:
  --template <name>     模板名称 (viral/professional/simple)
  --cover-image <path>  封面图路径
  --output <path>       输出 HTML 路径
```

**⚠️ 注意**：此脚本可能导致中文乱码，建议使用 curl 命令替代。

### upload_images.py

批量上传图片到微信素材库。

```bash
python3 scripts/upload_images.py <image_folder>

输出:
  图片 URL JSON 文件
```

---

## 内容栏目

### 7 栏目规划

1. **实景案例** - 完工项目实景拍摄
2. **干货分享** - 装修知识/避坑指南
3. **客户故事** - 业主访谈/入住反馈
4. **工地实况** - 施工进度/工艺展示
5. **材料科普** - 主材/辅材知识
6. **问答互动** - 常见问题解答
7. **活动促销** - 优惠活动/套餐

---

## 参考链接

- 微信公众平台：https://mp.weixin.qq.com
- 微信 API 文档：https://developers.weixin.qq.com/doc/offiaccount/
- 排版参考：见 `references/` 目录

---

## 公司信息模板

```
公司：[你的公司名称]
网站：[你的网站]
电话：[你的联系电话] / [你的联系电话]
地址：[你的地址]
时间：9:00-18:00（周一至周日）
```

---

## 发布检查清单（每次发布前必看！）

- [ ] 已重新获取最新 token（不超过 2 小时）
- [ ] 已使用 curl 命令（不是 Python）
- [ ] 已指定 `-H "Content-Type: application/json; charset=utf-8"`
- [ ] 已用手机扫码预览（不是 PC 预览）
- [ ] 已确认文字正常显示（不是 `<p>...</p>` 标签）

**以上 5 项全部打勾后才能正式发布！**
