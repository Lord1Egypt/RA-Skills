---
name: 数字人
description: 使用数字人
---

# 数字人

## 公共数字人

预设的大家都可以用的公共数字人.

### 列出所有公共数字人

```bash
python scripts/idr_video_client.py list_avatars --type=public --page=1 --page_size=3
```
返回值包含分页信息以及数字人列表信息. 示例输出:
```
【查询结果 第2/4页】
ID: 4958 | Name: 尧尧-律法科普     | resolution: 1080P | Description: 尧尧-律法科普
ID: 4957 | Name: 尧尧-营销带货-全身 | resolution: 1080P | Description: 全身展示，适合商品讲解、直播带货。
ID: 4956 | Name: 尧尧-好物种草     | resolution: 1080P | Description: 尧尧-好物种草
分页指令：
 - 回复【上一页】查看第1页
 - 回复【下一页】查看第3页

当前已为你展示第2页内容。
```

### 列出所有私有数字人

```bash
python scripts/idr_video_client.py list_avatars --type=private --page=1 --page_size=3
```
返回值包含分页信息以及数字人列表信息. 示例输出:
```
【查询结果 第2/4页】
ID: 2550 | Name: zm_1226_yda_01 | resolution: 1080P
ID: 1998 | Name: 实时互动1.2-不抠图 | resolution: 1080P
ID: 1400 | Name: 0911 | resolution: 1080P
分页指令：
 - 回复【上一页】查看第1页
 - 回复【下一页】查看第3页

当前已为你展示第2页内容。
```

### 查看数字人形象图片

```bash
python scripts/idr_video_client.py view_avatar --avatar "AVATAR_ID"
```
返回值输出数字人形象图片. 示例输出:
```
url: http://10.0.1.1:8905/img/22144/1752822917_0237455/avatar.png
```


### 使用数字人

使用数字人ID创建视频:

```bash
python scripts/idr_video_client.py create_video \
  --type tts \
  --text "你好啊，这是你的第一个AI视频" \
  --avatar 3632 \
  --voice "VOICE_ID"
```
