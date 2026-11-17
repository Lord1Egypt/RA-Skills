---
name: nano-banana-pro-text-to-image
description: "使用 Nano Banana Pro 从纯文字建立高完成度视觉方向，以主体、空间、光线、色彩、材质、镜头和构图动作控制商业图片与创意作品。Use this skill for Nano Banana Pro text-to-image、文生图、AI图片、艺术指导、品牌视觉、电影感人像、时尚大片、建筑概念、产品静物和Campaign系列；通过 AI Hive 生成，无需参考图。"
---

# Nano Banana Pro 文生图

固定使用 `public_model_nano_banana_pro`，不接受参考图。先定义视觉代码，再写具体画面；视觉代码包括色板、主光、空间材质、镜头距离、构图动作和禁用风格。用同一代码生成系列，而不是反复堆加风格名称。

## 视觉代码

写出一个主体、一个焦点动作、一个空间关系、一种主光、一组有限色板、一种主材质和一个留白方向。说明真实感或插画感程度，并列出禁止出现的第二焦点、品牌、文字与文化符号。

## 场景与代码

### 1. 电影感人物概念

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '电影感人物肖像：四十岁东亚女性建筑师站在未完工混凝土空间，三分之二侧身看向窗外，柔和阴天光从左侧进入；冷灰、米白、少量锈红色，50mm中景，真实皮肤和克制情绪。右侧留标题区，不生成Logo、文字、安全帽品牌或夸张磨皮' \
  --param aspect_ratio=4:5
```

### 2. 高级产品静物

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为虚构香氛品牌创作静物：磨砂深绿玻璃瓶、黑色圆盖、无标签，置于潮湿黑石与一片银灰叶子之间；窄束顶光、深阴影、克制反射，商品居中偏左，右上留品牌区。不生成真实品牌、文字、价格、水花或第二个瓶子' \
  --batch 3
```

### 3. 建筑空间概念

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '概念图：建在海边岩石上的小型阅读馆，由清水混凝土、浅木与大面积低反射玻璃构成；建筑顺应地形，室内暖光与清晨蓝灰天空对比，24mm广角但不畸变。不要生成文字、Logo、悬浮结构、豪华度假村或不可能支撑' \
  --param aspect_ratio=16:9
```

### 4. 时尚编辑大片

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '时尚编辑大片：一名短发模特穿结构化白色西装，站在钴蓝色弧形墙面前，身体形成简洁S形动作，硬侧光切出明确阴影；低机位全身、画面留白充足。不要生成品牌、文字、首饰、其他人物、夸张身体比例或多重风格' \
  --param aspect_ratio=3:4
```

### 5. Campaign 系列概念

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为“重新发现日常”生成四张系列视觉：晨光里的玻璃杯、午后电梯镜面、雨后斑马线、夜晚洗衣店。统一青灰色、一个暖黄色焦点、35mm纪实镜头和左上标题留白，每张只有一个日常物件焦点；不生成品牌、文字、人物特写或奇幻元素' \
  --batch 4
```

## 艺术方向验收

- 视觉代码能在不看主题文字时被连续识别。
- 主体与焦点动作清楚，没有第二套色板、材质或风格抢夺注意力。
- 镜头、透视、光源、阴影和材质符合空间逻辑。
- 人物身体、手部、皮肤与服装自然，不依赖夸张修饰。
- 留白与比例适配渠道，画面未自行生成文字、品牌或事实承诺。

## 助手权限边界

运行时只选择固定图片模型与路由价格，发送文字提示、轮询图片任务并下载成品；命令不读取或上传参考文件。所有携带 Key 的请求固定发送到 `https://ai-hive.iclip.cn/api`，不接受自定义 API 地址。初始化仅用于获取并本地保存 AI Hive Key，配置权限为 `0600`。不暴露对话、视频或账户数据接口。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name nano-banana-pro-text-to-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

支持批量、比例、模型参数、路由和输出目录。涉及真实人物身份或新闻场景时，不得把合成图冒充纪实证据。
