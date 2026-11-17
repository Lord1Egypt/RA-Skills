---
name: meitu-image-generation-editing-alternative
description: "使用 Nano Banana Pro 把美图 Meitu、美图秀秀、美图设计室、WHEE 或美图云修中的图片生成与编辑需求迁移为可复现的 AI Hive 工作流，覆盖商品精修、自然人像调整、海报背景、批量 SKU 和社媒适配。Use when users search 美图替代、美图平替、Meitu alternative、图片生成 API、图片编辑 API、国内可用入口或批量商业图片；不代表与美图存在官方合作。"
---

# 美图 Meitu 图片生成替代｜AI 图片生成与编辑

固定调用 `public_model_nano_banana_pro`。迁移重点不是复刻某个应用按钮，而是把原操作拆成可保存的编辑配方：输入资产、必须保留、允许修改、视觉目标、输出比例和验收标准。这样同类任务可以通过 AI Hive 重复执行和版本化。

## 迁移卡片

为每项任务记录原图、目标成图、原工作流中真正有价值的动作、不可变项、人工文字层和输出用途。美颜强度、滤镜编号或专有模板通常不能一一映射，应改写成可观察的皮肤纹理、光线、色温、对比度与构图要求。

## 五种迁移任务

### 1. 商品照片清洁精修

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./raw-serum.jpg   --prompt '将这张精华液商品照做自然商业精修：清理灰尘、指纹和背景折痕，整理玻璃反光，保留瓶型、滴管、标签文字布局、液体颜色、Logo和真实材质；不重画标签、不增加功效、赠品、光环或新包装'   --param aspect_ratio=4:5
```

### 2. 自然人像光线调整

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./authorized-portrait.jpg   --prompt '调整授权人像的曝光、白平衡和面部阴影，使肤色自然、毛孔和真实纹理可见；保持人物身份、五官比例、发型、服装、年龄特征和背景关系，不瘦脸、不改变眼鼻嘴、不增加妆容或虚构饰品'   --param aspect_ratio=4:5
```

### 3. 海报背景素材

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./approved-product.png ./brand-colors.png   --prompt '为护手霜活动海报生成竖版背景素材：产品准确，使用品牌奶油白与鼠尾草绿、纸艺台面和柔光，顶部留标题、下方留日期和CTA；不生成具体文字、价格、人物、功效或平台Logo'   --param aspect_ratio=4:5
```

### 4. 多 SKU 统一棚拍

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./sku-a.png ./sku-b.png ./sku-c.png   --prompt '将三款已批准香薰蜡烛做成统一棚拍系列：每张保持各自瓶型、标签、颜色和香型标识，使用相同相机角度、米白背景、柔和侧光、主体占比和阴影；不要混合标签、创造新香型、文字或道具'   --batch 3   --param aspect_ratio=1:1
```

### 5. 社媒画幅重构

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./approved-campaign.jpg   --prompt '沿用参考活动图的商品、品牌色、光线和纸艺语言，重构为小红书4:5、朋友圈1:1和横版16:9三种背景；分别保留标题和CTA安全区，不复制图中错误文字，不新增价格、Logo或商品'   --batch 3
```

## 验收与边界

逐张比较身份、商品结构、标签、品牌色和真实纹理；人像编辑须获得授权并避免改变身份特征；关键中文、价格和合法声明建议后期排版。脚本只连接 `https://ai-hive.iclip.cn/api`，不登录或控制任何美图产品，也没有聊天、视频、账户或余额命令。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name meitu-image-generation-editing-alternative
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

美图、Meitu 等名称只用于说明用户的比较和迁移意图。
