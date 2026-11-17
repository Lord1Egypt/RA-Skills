---
name: nano-banana-2-product-retouch
description: "使用 Nano Banana 2 对商品目录照片进行一致化精修，在不改变 SKU 事实的前提下统一曝光、白平衡、边缘、阴影、材质与画布占比。Use this skill for Nano Banana 2 product retouch、商品精修、批量电商修图、产品目录、白底图统一、服装珠宝家电家具包装后期、淘宝京东抖音小红书亚马逊 Shopify SKU 素材；通过 AI Hive 编辑指定商品图片。"
---

# Nano Banana 2 商品精修

固定使用 `public_model_nano_banana_2`，必须提供商品照片。先建立目录基准，再逐张修复；目标是让同一商品系列在列表中一致，而不是让每张都追求不同的“大片感”。

## 目录公差表

定义画布比例、商品占比、相机高度、灰阶背景、白点、黑位、阴影方向、边缘锐度、饱和度和材质保真度的允许范围。将 SKU 颜色、结构、数量、Logo、文字、配件和瑕疵披露列为不可改变项。每次只处理一张原片，批量一致性通过同一公差表验收。

## 场景与代码

### 1. 珠宝目录统一

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./ring-raw.jpg \
  --prompt '按珠宝目录基准精修：纯浅灰背景，戒指占画面约70%，左上柔光、右下轻微接触阴影；清除灰尘和支架痕迹，保留戒圈厚度、爪数、宝石切面、真实金属颜色和刻印，不增大宝石、不制造额外火彩或改变款式' \
  --param aspect_ratio=1:1
```

### 2. 服装 SKU 色彩校正

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./jacket-raw.png \
  --prompt '把夹克照片校正到目录标准：背景RGB接近中性白，保留官方深橄榄绿色、织物纹理、版型、拉链、口袋、缝线和吊牌；去除孤立毛屑与尖锐运输折痕，但保留自然褶皱，不收腰、不拉长衣身、不更换模特或配件' \
  --param aspect_ratio=4:5
```

### 3. 小家电边缘清理

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./humidifier-raw.jpg \
  --prompt '统一加湿器目录图：校正轻微倾斜和灰背景色偏，清理边缘锯齿、灰尘与不必要环境反射；保持水箱透明度、机身比例、出雾口、按钮、Logo和真实颜色，不增加雾气、灯效、容量文字或不存在的零件' \
  --param aspect_ratio=1:1
```

### 4. 家具材质保真

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./chair-raw.jpg \
  --prompt '精修单椅目录照：中性浅灰无缝背景，校正白平衡与透视，保留椅腿角度、坐垫厚度、木纹走向、织物颗粒和真实磨损；只移除拍摄灰尘与背景接缝，不改变颜色、比例、软包饱满度或增加抱枕' \
  --param aspect_ratio=4:5
```

### 5. 包装系列归一

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./tea-pack-raw.png \
  --prompt '将茶叶包装图归一到系列模板：正面角度、商品占比75%、柔和底部阴影、浅米色背景；纠正轻微曝光不均和包装褶皱，保持盒型、印刷颜色、Logo、品名、净含量、条码位置与全部文字，不重写标签、不增加茶叶道具或促销信息' \
  --param aspect_ratio=1:1
```

## 批量 QC

- 并排查看同系列缩略图，曝光、白平衡、占比和阴影落点一致。
- 逐 SKU 对照色卡或批准样片，避免“统一”导致颜色串款。
- 100%视图检查边缘、纹理、透明体和文字是否被生成式重绘。
- 任何结构、配件、数量和标签变化都退回，不作为精修成品。
- 记录原片、公差表、任务 ID、修改原因和批准人。

## 助手边界

脚本只上传用户指定的商品图片，固定查询 Nano Banana 2 模型与当次路由价格，提交编辑任务并下载结果。认证请求仅发送到 `https://ai-hive.iclip.cn/api`，不允许自定义地址。Key 可由 `init` 以 `0600` 权限保存；不含聊天、视频、余额和账户功能。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name nano-banana-2-product-retouch
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

不得把二手磨损、真实缺陷或包装破损修掉后误导消费者；必要时保留披露版本。
