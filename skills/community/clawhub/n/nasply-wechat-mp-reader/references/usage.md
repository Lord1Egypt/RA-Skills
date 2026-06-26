# WeChat MP Reader 使用手册

## 1. 这个技能能做什么

`wechat-mp-reader` 用于读取微信公众号内容，当前支持：

- 根据**文章 URL**提取全文
- 根据**文章 URL**识别公众号
- 拉取该公众号的**近期文章列表**
- 根据**公众号名称**搜索候选账号
- 管理微信公众号后台 **session**
- 对正文做基础清洗，输出结构化 JSON 和 markdown

---

## 2. 最推荐的使用方式

### URL-first

最稳的入口不是公众号名称，而是**文章链接**。

推荐流程：

1. 提供一篇公众号文章 URL
2. 技能自动：
   - 提取正文
   - 识别公众号
   - 反查 fakeid
   - 拉最近文章列表

---

## 3. 命令行使用方法

主脚本：

```bash
python3 skills/wechat-mp-reader/scripts/wechat_mp_reader.py
```

### 3.1 检查当前 session

```bash
python3 skills/wechat-mp-reader/scripts/wechat_mp_reader.py session check
```

用途：
- 检查当前是否有 session
- 检查 session 是否有效

### 3.2 查看 session 摘要

```bash
python3 skills/wechat-mp-reader/scripts/wechat_mp_reader.py session show
```

用途：
- 查看 cookie / token 是否存在
- 只展示长度和状态，不直接暴露敏感值

### 3.3 保存 session

```bash
python3 skills/wechat-mp-reader/scripts/wechat_mp_reader.py session save
```

### 3.4 启动二维码登录

```bash
python3 skills/wechat-mp-reader/scripts/wechat_mp_reader.py session login-start
```

返回结果里会带：

- `qr_url`
- `qr_image_path`

其中 `qr_image_path` 会指向本地生成的可扫码二维码 PNG，例如：

- `skills/wechat-mp-reader/scripts/cache/wechat-login-qr-real.png`

然后轮询状态：

```bash
python3 skills/wechat-mp-reader/scripts/wechat_mp_reader.py session login-status
```

### 3.5 按公众号名称搜索

```bash
python3 skills/wechat-mp-reader/scripts/wechat_mp_reader.py search "纳斯派" --limit 5
```

说明：
- 这个功能依赖**有效 session**
- 如果 session 失效，搜索通常不可用

### 3.6 提取单篇文章

```bash
python3 skills/wechat-mp-reader/scripts/wechat_mp_reader.py article "https://mp.weixin.qq.com/s/xxxx"
```

### 3.7 提取文章并拉对应公众号文章列表

```bash
python3 skills/wechat-mp-reader/scripts/wechat_mp_reader.py article "https://mp.weixin.qq.com/s/xxxx" --with-account-articles --list-count 5
```

这是当前最推荐的主命令。


## 3.8 关于 MP session 的说明

这里的 **MP** 指的是 **微信公众平台后台**（`mp.weixin.qq.com`）。

`wechat-mp-reader` 里有两类能力：

1. **公开文章页能力**
   - 例如根据一篇公众号文章 URL 提取正文、标题、发布时间等
   - 这类能力很多时候可以直接通过文章页完成

2. **公众号后台能力**
   - 例如根据公众号名称搜索账号
   - 或根据账号拉取最近文章列表
   - 这类能力依赖一个有效的 **MP 后台 session**

这里的 **session**，可以理解为：

> skill 当前持有的一份“已登录微信公众号后台”的会话状态（通常由 cookie / token 等凭证组成）。

### 它决定什么

如果 MP session 有效，skill 才能正常访问微信公众平台后台接口，从而支持：

- 公众号名称搜索
- 按账号拉取最近文章列表
- 更稳定的账号级查询

### 它不完全决定什么

如果你已经有一篇公开文章 URL，正文提取很多时候仍然可以工作；但一旦需要“从账号维度继续向下查”，就通常需要有效的 MP session。

### 最简单的理解

可以把它理解成两层能力：

- **公开网页层**：读单篇文章
- **后台登录层**：搜公众号、查账号文章列表

而 **MP session**，就是进入第二层的门票。

---

## 4. 推荐操作流程

### 场景 A：你手上已经有文章链接

1. 先检查 session：

```bash
python3 skills/wechat-mp-reader/scripts/wechat_mp_reader.py session check
```

2. 直接抓文章：

```bash
python3 skills/wechat-mp-reader/scripts/wechat_mp_reader.py article "文章URL" --with-account-articles --list-count 5
```

### 场景 B：没有可用 session

1. 启动登录：

```bash
python3 skills/wechat-mp-reader/scripts/wechat_mp_reader.py session login-start
```

2. 轮询状态：

```bash
python3 skills/wechat-mp-reader/scripts/wechat_mp_reader.py session login-status
```

3. 登录成功后抓文章：

```bash
python3 skills/wechat-mp-reader/scripts/wechat_mp_reader.py article "文章URL" --with-account-articles --list-count 5
```

### 场景 C：只有公众号名，没有文章链接

```bash
python3 skills/wechat-mp-reader/scripts/wechat_mp_reader.py search "公众号名称" --limit 5
```

但这条路不如文章 URL 稳。如果搜索结果不理想，最好补一篇文章 URL，再走 URL-first 流程。

---

## 5. 输出结果说明

### 5.1 session 对象

```json
{
  "present": true,
  "valid": true,
  "reason": "ok",
  "base_resp": {
    "ret": 0,
    "err_msg": "ok"
  }
}
```

### 5.2 account 对象

```json
{
  "name": "纳斯派",
  "biz": "MzYzNjYxNTEzMw==",
  "fakeid": "MzYzNjYxNTEzMw==",
  "avatar": "...",
  "signature": "..."
}
```

### 5.3 article 对象

```json
{
  "title": "...",
  "url": "...",
  "publish_time": "2026年4月1日 11:56",
  "publish_time_raw": "2026年4月1日 11:56",
  "author": "...",
  "account_name": "...",
  "content_html": "...",
  "content_markdown": "...",
  "images": []
}
```

说明：
- `publish_time`：更适合直接展示
- `publish_time_raw`：保留原始值
- `content_markdown`：已经做过基础清理，适合二次处理

---

## 6. 如何通过自然语言让 agent 调用这个技能

### 6.1 最直接的说法：给文章 URL

你可以直接对 agent 说：

- 帮我提取这篇公众号文章全文：`文章链接`
- 帮我读取这篇公众号文章，并输出 markdown
- 看看这篇文章是谁发的：`文章链接`
- 把这篇公众号文章抓下来，并列出这个号最近 5 篇文章
- 读取这篇微信文章，提取正文、标题、作者和发布时间
- 分析这篇公众号文章，并返回结构化 JSON

这些说法通常都会触发 `wechat-mp-reader`。

### 6.2 想让 agent 顺手反查公众号并拉文章列表

你可以这样说：

- 帮我根据这篇文章识别公众号，并列出最近 5 篇文章
- 从这篇公众号文章反查账号，再拉一下该号最近内容
- 给你一篇微信文章，帮我连同公众号信息一起提出来
- 解析这篇文章，并看看这个号最近还发了什么

### 6.3 只有公众号名称时的自然语言说法

你可以这样说：

- 帮我搜一下“纳斯派”这个公众号
- 查一下“微信公众平台”这个号有哪些候选结果
- 搜这个公众号名字，并列出可能的账号
- 看看这个公众号名能不能找到对应账号

说明：
- 这依赖有效 session
- 稳定性不如文章 URL 路径
- 如果能提供文章链接，最好还是给文章链接

### 6.4 想让 agent 先处理 session

你可以这样说：

- 帮我检查一下微信公众号 session 还有效吗
- 看看现在这个 skill 的 session 能不能用
- 帮我走一下微信后台二维码登录
- 启动公众号后台登录，我来扫码
- 帮我刷新一下这个 skill 的微信 session

### 6.5 完整流程自然语言模板

#### 模板 A：最推荐
> 帮我读取这篇公众号文章，并把正文、公众号信息、最近 5 篇文章一起输出：`文章链接`

#### 模板 B：更偏数据化
> 解析这篇微信文章，返回结构化 JSON，包含标题、作者、发布时间、正文 markdown、公众号信息和最近文章列表：`文章链接`

#### 模板 C：先查 session
> 先检查 wechat-mp-reader 的 session 是否有效，如果有效就直接抓这篇文章并列出该号最近 3 篇：`文章链接`

#### 模板 D：没有 session 时
> 帮我启动 wechat-mp-reader 的微信二维码登录，登录成功后再抓这篇文章：`文章链接`

---

## 7. 怎样和 agent 说，效果更好

尽量说清三件事：

1. **输入是什么**
   - 一篇文章 URL
   - 一个公众号名称

2. **你要的输出是什么**
   - 正文
   - markdown
   - JSON
   - 公众号信息
   - 最近文章列表

3. **是否要一起做扩展动作**
   - 反查公众号
   - 列最近 3/5/10 篇
   - 检查 session
   - 启动登录

### 好用例子

- 帮我提取这篇公众号文章全文，并输出 markdown：`文章链接`
- 帮我分析这篇微信文章，顺便识别公众号并列出最近 5 篇：`文章链接`
- 帮我检查 wechat-mp-reader 的 session，如果有效就直接抓这篇文章：`文章链接`
- 帮我搜一下“纳斯派”这个公众号，如果找到就列出最近文章

### 不太推荐的说法

- 帮我看看这个号
- 抓一下微信内容
- 把这个搞出来

这些说法太模糊，agent 可能还得追问：
- 是文章 URL 还是公众号名？
- 要正文还是文章列表？
- 要不要结构化输出？

---

## 8. 当前能力边界

### 已支持
- 单篇文章提取
- 公众号识别
- 最近文章列表
- session 管理
- markdown 清理
- 本机 Playwright fallback

### 仍然要注意
1. 公众号名搜索不如文章 URL 稳
2. 微信页面有时会返回非标准页
3. 这时会自动用本机 Playwright WebKit fallback
4. 统计数据不是当前主重点
5. 更复杂版式仍可能有少量 markdown 噪音

---

## 9. 最短速查版

### 命令行

```bash
python3 skills/wechat-mp-reader/scripts/wechat_mp_reader.py session check
python3 skills/wechat-mp-reader/scripts/wechat_mp_reader.py session login-start
python3 skills/wechat-mp-reader/scripts/wechat_mp_reader.py session login-status
python3 skills/wechat-mp-reader/scripts/wechat_mp_reader.py article "文章URL"
python3 skills/wechat-mp-reader/scripts/wechat_mp_reader.py article "文章URL" --with-account-articles --list-count 5
python3 skills/wechat-mp-reader/scripts/wechat_mp_reader.py search "公众号名称" --limit 5
```

### 自然语言

- 帮我提取这篇公众号文章全文：`文章链接`
- 帮我读取这篇文章，并列出这个号最近 5 篇
- 帮我检查 wechat-mp-reader 的 session 是否有效
- 帮我启动微信后台二维码登录
- 帮我搜一下这个公众号：`公众号名称`
