---
name: nano-banana-pro-seeding-image
description: "使用 Nano Banana Pro 制作自然、连续、平台原生的生活方式种草图片，让同一人物、商品、空间与时间线形成可信内容系列。Use this skill for Nano Banana Pro seeding content、小红书笔记、好物分享、生活方式图文、Instagram carousel、抖音图文、穿搭、美妆、家居、旅行和UGC风格素材；通过 AI Hive 生成。"
---

# Nano Banana Pro 种草图片

固定使用 `public_model_nano_banana_pro`。先建立一条真实可解释的内容时间线，再生成封面与连续内页。平台原生感来自日常视角、轻微不完美和一致环境，不等于伪造手机截图、用户评价或未披露体验。

## 内容日记

记录人物、地点、时间、天气、商品、使用顺序、服装、道具、光线、相机视角和披露要求。指定哪些细节必须连续，哪些镜头可以变化；每张图只推进一个生活瞬间。

## 场景与代码

### 1. 通勤包每日携带

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '生成同一人物的四张通勤图：早餐桌整理物品、把参考背包装好、地铁站肩背、办公室桌边放置。保持人物、服装、背包、电脑和水杯连续，使用自然手机摄影感；不生成品牌外商品、文字、评分、价格或夸张容量' \
  --image /path/to/person.jpg \
  --image /path/to/backpack.png \
  --batch 4
```

### 2. 日常穿搭系列

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '以同一模特和参考乐福鞋生成三套真实穿搭：上班西装、周末牛仔、晚餐连衣裙。锁定脸、身体比例、鞋型、颜色、Logo和尺码感，每套使用不同真实场景但保持自然光与轻松姿势；不生成文字、价格或额外鞋款' \
  --image /path/to/model.jpg \
  --image /path/to/loafers.png \
  --batch 3
```

### 3. 家居角落改造记录

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '记录同一客厅角落的三步布置：空白角落、放入参考边桌、加入批准的台灯和一本书。保持房间、相机、墙面、地板与光线连续，家具尺寸真实；不做夸张前后对比，不生成文字、价格、植物或额外装饰' \
  --image /path/to/room.jpg \
  --image /path/to/side-table.png \
  --image /path/to/lamp.png \
  --batch 3
```

### 4. 周末旅行使用日记

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为参考旅行收纳袋生成周末旅行四格日记：床上分类衣物、装进行李箱、酒店打开、用后折叠收纳。保持同一收纳袋、衣物、行李箱和人物手部，环境从家中自然过渡到酒店；不生成地标、文字、航空品牌或容量承诺' \
  --image /path/to/organizer-bags.png \
  --batch 4
```

### 5. 美妆晚间流程

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '生成同一人物的晚间护肤四张图片：清洁后、取用参考精华、涂抹面部、商品放回床头。保持人物身份、皮肤真实纹理、睡衣、浴室和卧室色温连续；不改变皮肤前后状态，不生成疗效、成分文字、价格或过度磨皮' \
  --image /path/to/person.jpg \
  --image /path/to/serum.png \
  --batch 4
```

## 原生感检查

1. 连续图中的人物、商品、服装、空间、时间与道具关系合理。
2. 视角和构图有日常变化，但不使用截图、界面或评论伪造真实用户。
3. 商品结构、包装、Logo、颜色与使用方法对照参考资料。
4. 不制造前后效果、使用天数、销量、评分或“亲测”结论。
5. 按平台要求披露合作、赠品、AI合成和商业链接。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name nano-banana-pro-seeding-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

支持多图、批量、比例、参数、路由和输出目录。保存内容日记与批准商品资料，后续扩展新笔记时沿用连续性规则。
