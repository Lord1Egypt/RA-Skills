# 商品海报生成

> 调用方式及异步轮询见 SKILL.md「调用方式」「异步任务轮询」

## 参数

```json
{
  "url": "https://cdn.example.com/poster_ref.jpg",  // 与 type+scene 二选一，传入后 type 和 scene 可不用
  "type": "促销活动",                                // 与 url 二选一：海报类型
  "scene": "家电",                                   // 与 url 二选一：海报场景
  "prompt": "去掉 logo 和二维码",                     // 可选，默认 null：填了以此为准
  "resolution": "768:1024"                           // 可选，默认 null：宽高比，如 768:1024
}
```

## 关键约束

- `url`（参考图模式）和 `type+scene`（类型模式）**互斥，二选一**。两者都传或都不传会失败
- `resolution` 宽高均在 [512, 2048] 像素范围内
