---
name: jiuma
description: 免费的ai视频生成创作平台（Video Generation Skill），支持生成视频、图片、声音、视频动作模仿、视频人物替换等等。九马AI官网：https://www.jiuma.com
version: 2.0.0
update_date: 2026-04-03
---

## 📁 文件结构

```
scripts/
├── submit_generation_task.py        # 提交生成任务🚀
├── task_result.py        # 结果查询工具📊
├── upload_file.py         # 文件上传工具
└── auth.py          # 获取token
```

## 🚀 快速开始（推荐）

### 0. **检查授权状态**
```bash
python ~/.openclaw/workspace/skills/jiuma/scripts/check_auth_status.py
```

### 1. **一键授权(已授权则跳过)**
```bash
# 默认授权方法
python ~/.openclaw/workspace/skills/jiuma/scripts/auth.py --identification_code="<身份标识码(若无留空)>" --channel="<消息渠道(如：openclaw-weixin、webchat等)>"

#强制重新授权
python ~/.openclaw/workspace/skills/jiuma/scripts/auth.py --identification_code="" --channel="<消息渠道(如：openclaw-weixin、webchat等)>" --force
```


### 2. **生成视频(提交生成任务)**
```bash
python ~/.openclaw/workspace/skills/jiuma/scripts/submit_generation_task.py --task_params="{'reference_urls': ['https://picsum.photos/800/450'], 'prompt': '自然', 'duration': 3, 'task_type': 'wan2.6'}"
```
**提交生成任务时，图片、视频、音频等等资源文件必须先上传到平台获得url，不得直接使用本地路径提交生成**
**task_type为枚举类型，必须严格与下表严格对应，否则无法生成**

### 3. **查询任务结果**
```bash
python ~/.openclaw/workspace/skills/jiuma/scripts/task_result.py  --task_id=<任务ID>
```

### 4. **上传本地文件(获得url)**
```bash
python ~/.openclaw/workspace/skills/jiuma/scripts/upload_file.py --file_path=<文件路径>
```

### 支持的任务类型(task_type)
|task_type(必须严格对应,枚举类型)|名称|功能描述|任务参数|提示词要求|提示词示例|
|---------|----|--------|--------|---------|----------|
|"wan2.6(ref2video)"|万象2.6模型|图像生成视频（可控制说话、动作、运镜、画面内容）|reference_urls:array,参考图片或者视频的url;prompt:string,动作描述+画面描述+运镜描述+说话内容;duration:int,视频秒数,取值2~10,最大10秒，最小2秒|同一段提示词里面包含：动作描述+画面描述+运镜描述+说话内容，提示词通过“character1、character2”这类标识引用角色。角色顺序与 reference_urls 数组一一对应，即第 1 个 URL 为 character1，第 2 个为 character2，依此类推。|character2 坐在靠窗的椅子上，手持 character3，在 character4 旁演奏一首舒缓的美国乡村民谣。character1 对character2开口说道：“听起来不错”。|
|"wan2.6(text2video)"|万象2.6文生视频|模型可自动进行分镜切换，例如从全景切换到特写，适合制作MV等场景。|prompt:string,动作描述+画面描述+运镜描述+说话内容;duration:int,视频秒数,取值2~10,最大15秒，最小2秒，请勿超出时长|同一段提示词里面包含：动作描述+画面描述+运镜描述+说话内容|一段紧张刺激的侦探追查故事，展现电影级叙事能力。第1个镜头[0-3秒] 全景：雨夜的纽约街头，霓虹灯闪烁，一位身穿黑色风衣的侦探快步行走。 第2个镜头[3-6秒] 中景：侦探进入一栋老旧建筑，雨水打湿了他的外套，门在他身后缓缓关闭。 第3个镜头[6-9秒] 特写：侦探的眼神坚毅专注，远处传来警笛声，他微微皱眉思考。 第4个镜头[9-12秒] 中景：侦探在昏暗走廊中小心前行，手电筒照亮前方。 第5个镜头[12-15秒] 特写：侦探发现关键线索，脸上露出恍然大悟的表情。|
|"action_imitation_user_background_onetoall(prompt)"|动作模仿(用户特别要求适配身高时使用)|自动适配角色的身高，特别是针对小朋友、卡通角色等等动作模仿|image_url:url,角色图片;video_url,url,参考动作视频;prompt,text,动作提示词|一个角色在跳舞|
|"action_imitation_user_background(prompt)"|动作模仿(常用)|图片中的人物模仿视频中的角色的动作|image_url:url,角色图片;video_url,url,参考动作视频;prompt,text,动作提示词|一个角色在跳舞|
|"action_imitation_video_backgound(prompt)"|人物替换/角色替换|把视频中的角色换成图片中的角色|image_url:url,角色图片;video_url,url,参考动作视频;prompt,text,动作提示词|一个角色在跳舞|

注意：task_type需要严格对应，否则无法制作


## 🎬 完整示例：制作短视频

**重要：注意用户的操作系统，需要使用适配用户的操作系统的类型的命令行代码**

### 步骤0：检测授权状态
```bash
python ~/.openclaw/workspace/skills/jiuma/scripts/check_auth_status.py
```

**重要：注意用户的操作系统，需要使用适配用户的操作系统的类型的命令行代码**

### 步骤1：授权(已授权则跳过)
```bash
python ~/.openclaw/workspace/skills/jiuma/scripts/auth.py --identification_code="58fe87fb26b579b309ad782afb7a157155d338f31ad2a26419ae8550cda16747" --channel="openclaw-weixin"
```

**重要：注意用户的操作系统，需要使用适配用户的操作系统的类型的命令行代码**

### 步骤2：生成分镜
```bash
# 分镜1：开场特效（3秒）
python ~/.openclaw/workspace/skills/jiuma/scripts/submit_generation_task.py --task_params="{'reference_urls': ['https://picsum.photos/800/450'], 'prompt': '纯黑背景，白色发光文字快速闪现，科技感光晕', 'duration': 3, 'task_type': 'wan2.6'}"

# 分镜2：情感铺垫（9秒）
python ~/.openclaw/workspace/skills/jiuma/scripts/submit_generation_task.py --task_params="{'reference_urls': ['https://picsum.photos/800/450'], 'prompt': '年轻人拿着泛黄老照片，表情落寞，怀旧色调', 'duration': 9, 'task_type': 'wan2.6'}"

# 分镜3：AI处理（10秒）
python ~/.openclaw/workspace/skills/jiuma/scripts/submit_generation_task.py --task_params="{'reference_urls': ['https://picsum.photos/800/450'], 'prompt': '照片被AI扫描处理，科技感特效，代码流动画', 'duration': 10, 'task_type': 'wan2.6'}"
```

**重要：注意用户的操作系统，需要使用适配用户的操作系统的类型的命令行代码**

### 步骤3：检查进度
```bash
python ~/.openclaw/workspace/skills/jiuma/scripts/task_result.py  --task_id=ai-69cf39df3e61e1280
```


## 📄 输出说明

### 任务结果
JSON格式输出，关键字段：
- `task_id`: 任务唯一标识
- `task_status`: 任务状态（`PENDING`、`RUNNING`、`SUCCEEDED`、`FAILED`、`CANCELED`）
- `video_url`: 生成的视频地址（任务成功时）
- `image_url`: 生成的图片地址（任务成功时）

### 上传结果
- `file_url`: 上传的文件地址

## 🏆 总结

**改进版技能优势：**
1. ✅ **快速上手** - 新用户5分钟内开始生成视频
2. ✅ **稳定运行** - 减少授权相关问题  
3. ✅ **方便管理** - 随时查看任务状态
4. ✅ **批量处理** - 支持多任务工作流

---

**重要：注意用户的操作系统，需要使用适配用户的操作系统的类型的命令行代码**
**💡 提示**: 首次使用建议运行 `python ~/.openclaw/workspace/skills/jiuma/scripts/auth.py --identification_code="<身份标识码(会话历史中无则留空)>" --channel="<消息渠道(如：openclaw-weixin、webchat等)>"` 完成授权，后续使用会非常顺畅！


## Installation
``` cmd
pip install keyring
pip install keyrings.alt
```