# 视频复刻（剪同款）

> 调用方式及异步轮询见 SKILL.md「调用方式」「异步任务轮询」

## 参数

```json
{
  "url": "https://cdn.example.com/ref_video.mp4",  // 必填：参考视频，公网URL（抖音分享链接先用 get_raw_url 解析）
  "script": "视频脚本，控制风格、场景、语气...",       // 可选，默认 null：建议先用 analyze_video 分析参考视频
  "user_prompt": "让背景更明亮",                       // 可选，默认 null：用户特别要求
  "ratio": "9:16",                                    // 可选，默认 9:16：4:3 | 1:1 | 3:4 | 9:16 | 21:9
  "duration": 15,                                     // 可选，默认 15：[4, 15] 秒
  "model": "seed_2_0_fast",                           // 可选，默认 seed_2_0_fast：seed_2_0（25算力/秒）| seed_2_0_fast（20算力/秒）
  "images": [],                                       // 可选，默认 []：参考图片URL数组
  "videos": [],                                       // 可选，默认 []：参考视频URL数组
  "audios": []                                        // 可选，默认 []：参考音频URL数组
}
```

## 关键约束

- 抖音分享链接需先调 `get_raw_url` 解析出真实视频 URL，见 [get_raw_url.md](get_raw_url.md)
- `analyze_video` 可分析参考视频风格/运镜/灯光，生成 `script` 参数，详见 [analyze_video.md](analyze_video.md)
