---
name: 模板
description: 使用模板
---

# 模板

## 公开模板

预设的大家都可以用的视频生成模板.

### 列出所有公共模板

```bash
python scripts/idr_video_client.py list_templates --type=public --page=1 --page_size=3
```

返回值包含分页信息以及模板列表信息. 示例输出:
```
【查询结果 第2/4页】
ID: 107 | Name: 33  | layout: 竖屏 | category: 企业培训
ID: 106 | Name: 23  | layout: 竖屏 | category: 医学科普
ID: 105 | Name: 啊啊 | layout: 竖屏 | category: 金融理财
分页指令：
 - 回复【上一页】查看第1页
 - 回复【下一页】查看第3页

当前已为你展示第2页内容。
```

### 列出所有私有模板

```bash
python scripts/idr_video_client.py list_templates --type=private --page=1 --page_size=3
```

返回值包含分页信息以及模板列表信息. 示例输出:
```
【查询结果 第2/4页】
ID: 142 | Name: zm-0610-mb
ID: 137 | Name: zm测试模板
分页指令：
 - 回复【上一页】查看第1页
 - 回复【下一页】查看第3页

当前已为你展示第2页内容。
```

### 使用模板和文本创建视频

使用模板和一段文本创建视频:

```bash
python scripts/idr_video_client.py create_video \
  --type "template" \
  --text "你好啊，这是你的第一个AI视频" \
  --template_id "TEMPLATE_ID"
```

### 使用模板和文本和指定的分辨率创建视频

使用模板和一段文本以及指定的分辨率去创建一个视频:

```bash
python scripts/idr_video_client.py create_video \
  --type "template" \
  --text "你好啊，这是你的第一个AI视频" \
  --avatar_res "RESOLUTION" \
  --template_id "TEMPLATE_ID"
```