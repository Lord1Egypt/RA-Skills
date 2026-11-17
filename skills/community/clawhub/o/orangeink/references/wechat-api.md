# 公众号草稿箱 API 注意事项（wechat-api）

> 给「用户自有 skill 接公众号 API」场景的对接说明。本 skill 只产出格式，不持有凭据。

## 产物格式

`render.mjs --draft 草稿.json` 生成 `draft/add` 请求体：

```json
{
  "articles": [{
    "title": "文章标题（≤64 字）",
    "author": "登叔",
    "digest": "摘要（≤120 字，默认取首段前 54 字）",
    "content": "正文 HTML（≤20000 字符 / <1MB）——即 -o 输出的纯净片段",
    "need_save_comment": 0,
    "only_fans_can_comment": 0
  }]
}
```

官方文档：https://developers.weixin.qq.com/doc/service/api/draftbox/draftmanage/api_draft_add.html

## 硬约束与坑

1. **外链图片会被过滤**：content 里的 `<img src>` 必须是微信素材库永久链接。发布前对每张图先调 `uploadimg`（type=permanent 或临时素材按需）换 URL。`--meta` 输出的 `images` 数组即待处理清单
2. **2025-07 起个人主体 freepublish 权限已回收**：API 只能建**草稿**，发表仍在后台手动点（草稿箱 → 群发）。不要尝试 API 直接发表
3. **content 字数**：<2 万字符、<1MB；`--meta` 的 `charsWechat` 是公众号口径估算，供预估
4. **thumb_media_id**：正式调用 draft/add 还需封面图素材 id（`--draft` 产物未含此字段，接入方按需补）——封面可复用中登系 3:4 母版（`中登FM/01-工具/generate_fm_cover.py` 同源底图体系）
5. **title/digest 长度**：title ≤64 字、digest ≤120 字，超长 API 报错

## 建议的接入姿势

用户自有 skill 拿到 `草稿.json` 后：
1. 补齐 `thumb_media_id`（传封面图）
2. 遍历 `--meta` 的 images，逐张 `uploadimg` 换链，替换 content 中对应 src
3. 调 `draft/add` → 得 media_id → 后台「草稿箱」人工确认后群发
