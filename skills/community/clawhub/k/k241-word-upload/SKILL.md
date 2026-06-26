---
name: k241-word-upload
description: 上传单词到 K241 班单词自学网站 (k241.wooomooo.com)，支持自动获取翻译和拼音。触发场景：用户要求上传单词、添加单词到网站、背单词。
---

# K241 单词上传

上传单词到 K241 班单词自学表网站，自动获取翻译和音频。

## 网站信息

- URL: `https://k241.wooomooo.com`
- 账号: `mick` / 密码: `vee`
- 登录页: `/login.php`
- 上传: `upload.php?auto_fetch=1&word=单词`
- 管理: `/admin_words.php`

## 上传方式

### 自动获取翻译 + 拼音（推荐）

GET 请求，自动从有道词典获取翻译和拼音：

```
GET /upload.php?auto_fetch=1&word={单词}
```

### 手动指定翻译和拼音

POST 表单（翻译和拼音必填）：

```
POST /upload.php
Content-Type: application/x-www-form-urlencoded

word={单词}&translation={翻译}&pinyin={拼音}
```

## 更新已有单词（补拼音）

在管理后台找到 `word_id`，用 POST 更新：

```
POST /admin_words.php
Content-Type: application/x-www-form-urlencoded

action=update&word_id={id}&word={单词}&translation={翻译}&pinyin={拼音}
```

获取 `word_id` 方法：
1. 登录后访问 `/admin_words.php`
2. 找到对应单词所在页码（每页20条）
3. 通过 `get_word.php?id={id}` 查询单词确认
4. 或遍历所有 `editWord(id)` 对应的 id

## 常用拼音参考

| 单词 | 拼音 |
|------|------|
| accidents | shì gù |
| use | shǐ yòng |
| sun cream | fáng shài shuāng |
| get | dé dào |
| hurt | shòu shāng |
| muscles | jī ròu |
| bones | gǔ tou |
| sweat | hàn shuǐ |
| loses | shī qù le |
| protect | bǎo hù |

详细拼音表见 [references/pinyin.md](references/pinyin.md)。

## 完整工作流

1. 登录获取 cookie
2. 用 `auto_fetch=1` 上传单词（有道 API 自动获取翻译+拼音）
3. 等待 10~20 秒让有道 API 响应
4. 部分单词可能返回"无法获取翻译"，需手动重试或手动 POST 补全
5. 上传后查 `get_word.php?id=X` 确认拼音是否为空
6. 若拼音为空，用 POST update 补上

## 注意事项

- 网站排序按上传时间倒序，新单词出现在第1页
- 一个账号同单词不能重复上传（会报"已存在"）
- `auto_fetch` 依赖有道词典 API，可能网络波动失败
- 若 `auto_fetch` 失败率高，改为手动 POST 方式传入翻译和拼音