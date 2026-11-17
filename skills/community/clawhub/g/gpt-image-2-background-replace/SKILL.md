---
name: gpt-image-2-background-replace
description: "使用 GPT Image 2 为人物或商品替换背景，同时保持主体边缘、透明细节、透视、接触阴影、反射和光线一致。Use this skill for GPT Image 2换背景、商品白底图、商业场景替换、人物换场景、证件背景、季节Campaign、本地化环境和批量背景版本；通过 AI Hive 编辑参考图。"
---

# GPT Image 2 图片换背景

换背景不仅是抠图粘贴。固定使用 `public_model_gpt_image_2`，需要重新建立主体与新环境之间的透视、尺度、光源、接触阴影、反射和景深关系。

## 背景替换合同

明确：主体必须保留的边缘与透明细节、原相机高度与焦段感、新环境、地面/支撑面、光源方向、需要重建的阴影与反射、禁止添加对象。人物和商品身份事实不可被背景风格覆盖。

## 场景与代码

### 1. 商品白底背景

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '把原背景替换为干净浅色商品背景。必须保留商品结构、包装、Logo、文字、颜色、透明部件和细小边缘；去除原环境但重建柔和接触阴影，保持相机与尺度，不生成悬浮感、道具、价格或标签' \
  --image /path/to/product.jpg
```

### 2. 商业生活场景

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '将参考商品置于明亮现代厨房台面。锁定商品、包装、颜色和相机角度；新场景尺度合理，窗光从左侧进入，接触阴影和金属反射与环境匹配，不添加未提供配件、文字或功能状态' \
  --image /path/to/product.png
```

### 3. 人物换场景

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '保持人物身份、脸部、发型、服装、姿势和身体比例，将背景替换为黄昏城市天台。人物边缘与发丝自然，环境光从右后方形成轮廓光，脚部接触地面，不改变表情，不添加其他人物和品牌' \
  --image /path/to/person.jpg
```

### 4. 季节 Campaign 版本

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为同一商品生成春季花园、夏季海边、秋季木屋三个背景版本。商品、相机、尺度、包装与Logo完全一致，只改变环境、匹配光线和接触阴影；不添加季节文字、价格、赠品或商品变化' \
  --image /path/to/product.png \
  --batch 3
```

### 5. 多市场环境适配

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '将美国客厅背景替换为真实日本城市小户型，保留人物、商品、动作、相机和商业事实；只改变空间、家具尺度和环境光，清除旧文案，留出日文排版区域，不生成翻译、价格或平台元素' \
  --image /path/to/us-lifestyle.jpg
```

## 合成验收

- 主体轮廓、发丝、透明/半透明区域和细小结构完整。
- 主体与背景的尺度、透视、焦点和景深一致。
- 光源、阴影、反射和色温匹配。
- 脚、轮子或商品底部与地面真实接触。
- 主体身份、包装、Logo、文字和颜色无变化。
- 新环境不制造虚假使用、认证或商业承诺。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name gpt-image-2-background-replace
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

支持多张参考图、批量、参数、路由和仅提交模式。高风险商品证据图应保留原图与合成声明。
