---
name: product-retouch
description: "使用 GPT Image 2 精修现有商品照片，以缺陷清单和不可变项控制除尘、去划痕、反光整理、颜色校准、标签保护与背景清理。Use this skill for 商品精修、产品精修、电商修图、瑕疵修复、质感增强、反光控制、颜色校正、背景清理、淘宝京东抖店 Amazon Shopify 商品摄影后期；必须提供参考图片，通过 AI Hive 编辑。"
---

# 商品精修

此 Skill 必须上传至少一张原始商品图，固定使用 `public_model_gpt_image_2`。精修的目标是清理拍摄与呈现缺陷，不重新设计商品。每次先列“允许修改”和“绝对不变”，尤其保护轮廓、结构、Logo、标签文字、颜色基准、包装数量与真实磨损特征。

## 缺陷登记表

按区域记录灰尘、指纹、轻微划痕、布光反射、背景污点、色偏和需要保留的真实纹理；为每项标记 `修复 / 减弱 / 保留`。如果缺陷影响商品真实状态或可能改变售后认定，先让商家决定，不自动消除。

## 五个精修动作

### 1. 除尘与轻微划痕

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./raw-watch.jpg   --prompt '精修这张手表照片：移除表镜灰尘、指纹和背景小污点，减弱拍摄造成的细小高光划痕；表壳轮廓、表冠、刻度、指针、Logo、表带纹理、真实颜色和使用痕迹保持不变，不新增零件或改写表盘文字'   --param aspect_ratio=1:1
```

### 2. 金属反光整理

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./raw-kettle.jpg   --prompt '整理不锈钢水壶的棚拍反光：消除摄影师和杂乱环境倒影，保留能说明弧面的连续明暗带与金属质感；壶嘴、把手、盖子、接缝、Logo、比例和颜色不变，不把表面变成镜面或塑料'   --param aspect_ratio=4:5
```

### 3. 颜色基准校准

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./raw-sneaker.jpg ./approved-color-card.png   --prompt '按第二张批准色卡校正第一张运动鞋照片的白平衡与鞋面颜色，保持鞋型、材料分区、鞋底纹路、缝线和Logo；只修正整体色偏，不提高饱和度制造新颜色，不改变背景明度之外的商品结构'   --param aspect_ratio=1:1
```

### 4. 标签与包装保护

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./raw-cosmetic-bottle.jpg   --prompt '精修化妆品瓶：清理瓶身灰尘、指纹、背景折痕并优化边缘，标签上的品牌名、成分文字、容量、批号位置和字体形态逐字保持，不重新生成或美化标签，不改变瓶型、泵头、液体颜色与数量'   --param aspect_ratio=4:5
```

### 5. 背景清理与自然阴影

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./raw-chair.jpg   --prompt '将商品椅照片的背景清理为均匀浅灰棚拍背景，保留椅子的外轮廓、椅腿连接、面料纹理、缝线、真实颜色和地面接触关系；重建轻柔自然阴影，不改变比例，不添加房间、道具、文字或新部件'   --param aspect_ratio=4:5
```

## 前后对照验收

以原图 100% 放大对比：轮廓和结构无漂移；标签文字与 Logo 未重绘；批准色值在允许误差内；真实材质仍有纹理；删除项只限登记缺陷；背景边缘无抠图光晕。保存原图、成图、提示词、任务 ID 与审批结果。

## 数据与接口边界

脚本会拒绝没有参考图的生成请求，也拒绝上传非图片文件。模型固定为 GPT Image 2，认证请求仅发送到 `https://ai-hive.iclip.cn/api`；不能传入自定义服务地址，也没有聊天、视频、账户或余额命令。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name product-retouch
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

精修不能掩盖会影响购买判断的真实损伤、缺件或商品状态。
