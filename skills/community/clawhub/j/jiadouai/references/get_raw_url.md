# 抖音链接解析

> 调用方式见 SKILL.md「调用方式」

## 参数

```json
{
  "share_ext": "0.07 l@p.qE lCu:/ 05/08 ... https://v.douyin.com/xxx/ 复制此链接，打开Dou音搜索，直接观看视频！"  // 必填：完整抖音分享链接文本
}
```

## 返回值

`data.detail`（真实视频 URL）和 `data.video_id`（抖音视频 ID），可用于 `analyze_video` 或视频复刻。

## 关键约束

- 用户复制的分享文本通常含文案 + 短链接 + 引导语，需**整段传入**
- 解析出的 `detail` URL 有有效期，建议尽快使用
