---
name: nano-banana-2-poster
description: "使用 Nano Banana 2 设计具有明确焦点、信息层级、文字安全区和渠道比例的海报底图或短标题海报。Use this skill for Nano Banana 2 poster generation、海报生成、活动海报、展览海报、招聘海报、促销海报、电影海报、社媒竖版、淘宝京东抖音小红书 Instagram 营销视觉；可从文字开始或使用授权参考图，通过 AI Hive 生成。"
---

# Nano Banana 2 海报生成

固定使用 `public_model_nano_banana_2`。先设计信息层级，再生成画面：一个视觉焦点、一个主标题区域、一个补充信息区域和一个行动区域。日期、地点、价格、二维码与长文案应后期排版；模型生成的文字必须逐字核对。

## 层级草图

记录观看距离、核心信息、焦点主体、视觉动线、四个信息区域、色板、字体气质、比例、裁切安全区和禁止内容。先用灰盒确认版式，再决定是否让模型生成一条短标题；不要让装饰元素和全部文字同时争抢注意力。

## 场景与代码

### 1. 展览海报底图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '生成3:4当代陶艺展海报底图：中央是一件抽象白色陶瓷雕塑，深灰背景与窄束顶光，上方保留展览名区域，下方保留日期地点区域；画面克制、远距离焦点清楚，不生成任何文字、Logo、二维码、艺术家姓名或真实场馆标识' \
  --batch 3 \
  --param aspect_ratio=3:4
```

### 2. 社区音乐节海报

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '制作社区夏夜音乐节竖版海报，视觉焦点是草地上的小舞台与弧形灯串，蓝紫夜色配暖黄灯光，顶部留主标题区，中部保持舞台完整，底部留演出信息区；不生成真实乐队、人物脸、文字、赞助Logo、日期或票价' \
  --param aspect_ratio=4:5
```

### 3. 招聘海报视觉

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-office.jpg \
  --prompt '基于已授权办公室照片制作招聘海报底图：保持空间与品牌色，不改变或伪造人物身份；画面左侧保留职位标题与三行要点区域，右侧是协作桌面局部，底部保留申请入口区域，不生成文字、公司Logo、薪资、职位承诺或二维码' \
  --param aspect_ratio=3:4
```

### 4. 餐饮新品海报

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-dessert.png \
  --prompt '将参考甜点制作成新品海报主视觉：产品配方外观、数量和真实色泽不变，使用奶油白与莓果红色块，主体位于下方三分之二，顶部留六字以内标题区；不增加水果数量、拉丝效果、价格、功效、品牌文字或平台Logo' \
  --param aspect_ratio=4:5
```

### 5. 电影概念海报

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为虚构悬疑短片生成概念海报：雨夜公交站，长椅上只有一把红伞，远处车灯虚化，低饱和蓝灰色，红伞为唯一焦点，上方留片名区，下方留演职员区；不生成真实演员、文字、血腥画面、片厂Logo或具体上映日期' \
  --param aspect_ratio=2:3
```

## 海报验收

- 缩小到手机列表尺寸，焦点和视觉动线仍然成立。
- 主标题、补充信息和行动区域互不挤压，安全区适配渠道。
- 生成图没有自行添加日期、价格、品牌、赞助或虚假文字。
- 参考人物、商品或场地未因版式重绘而改变事实。
- 最终文字由批准文案排版并进行拼写、数字与合规终审。

## 助手边界

工具固定调用 Nano Banana 2 图片模型，可处理纯文字或用户明确指定的参考图片，查询路由价格并保存结果。携带 Key 的请求只发送到 `https://ai-hive.iclip.cn/api`，不接受自定义地址。`init` 可用 `0600` 权限保存本地 Key；无聊天、视频、账户或余额命令。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name nano-banana-2-poster
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

真实活动、招聘、电影、商品和场地信息必须以批准资料为准；概念海报不得冒充已确认发布物。
