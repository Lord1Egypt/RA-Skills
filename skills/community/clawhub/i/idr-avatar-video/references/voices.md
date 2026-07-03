---
name: 音色
description: 音色选择能力、试听音频
---

# 音色

## 公共音色

预先配置的公共音色.

### 列出所有公共音色

```bash
python scripts/idr_video_client.py list_voices --type=public --page=1 --page_size=3
```
返回值包含分页信息以及音色列表信息. 示例输出:
```
【查询结果 第2/4页】
ID: pNInz6obpgDQGcFmaJgB | Name: Adam   | gender: male   | language: english | preview image: https://xy-avatar.oss-cn-hangzhou.aliyuncs.com/speaker/preset/icon/default_icon.png
ID: ErXwobaYiN019PkySvjV | Name: Antoni | gender: male   | language: english | preview image: https://xy-avatar.oss-cn-hangzhou.aliyuncs.com/speaker/preset/icon/default_icon.png
ID: EXAVITQu4vr4xnSDxMaL | Name: Bella  | gender: female | language: english | preview image: https://xy-avatar.oss-cn-hangzhou.aliyuncs.com/speaker/preset/icon/default_icon.png
分页指令：
 - 回复【上一页】查看第1页
 - 回复【下一页】查看第3页

当前已为你展示第2页内容。
```

### 列出所有私有音色

```bash
python scripts/idr_video_client.py list_voices --type=private --page=1 --page_size=3
```
返回值包含分页信息以及音色列表信息. 示例输出:
```
【查询结果 第2/4页】
ID: 7fa60c1d77ce20260602060133157 | Name: zm-0602-fe-api-ts | gender: female | language: english | preview image: https://xy-avatar.oss-cn-hangzhou.aliyuncs.com/speaker/preset/icon/default_icon.png
分页指令：
 - 回复【上一页】查看第1页
 - 回复【下一页】查看第3页

当前已为你展示第2页内容。
```

## 试听音色
```bash
python scripts/idr_video_client.py preview_audio --voice "VOICE_ID"
```

返回音频链接 url
