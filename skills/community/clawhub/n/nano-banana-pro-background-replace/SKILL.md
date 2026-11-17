---
name: nano-banana-pro-background-replace
description: "使用 Nano Banana Pro 为商品或人物删除、替换和扩展背景，同时重建自然边缘、透视、尺度、光线、阴影和反射。Use this skill for Nano Banana Pro background replacement、AI换背景、商品白底图、场景合成、人物换场景、季节背景、跨境本地化背景和批量广告版本；通过 AI Hive 编辑原图。"
---

# Nano Banana Pro 图片换背景

固定使用 `public_model_nano_banana_pro`。把换背景视为一次重新布光和空间合成，而不是简单抠图：先锁定主体，再定义新空间的相机、地面、主光、反射和景深。

## 场景整合单

记录主体不可变化项、透明/毛发边缘、原相机高度与焦段感、新背景、地面或支撑面、主光方向、色温、阴影软硬、反射材质、景深和禁止出现对象。若新背景与原主体光线冲突，允许调整环境光，但不得重绘主体身份与商品事实。

## 场景与代码

### 1. 商品纯白背景

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '移除原场景并替换为干净纯白背景，完整保留玻璃水壶的轮廓、把手、刻度、Logo、透明度和颜色；处理好玻璃边缘与内部折射，底部保留克制接触阴影，不添加水、配件、文字、价格或新高光' \
  --image /path/to/kettle-original.jpg
```

### 2. 统一摄影棚背景

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '把原背景替换为暖灰无缝摄影棚，保持鞋子结构、鞋带、鞋底纹路、Logo、相机和商品角度；主光从左上方，地面形成柔和椭圆阴影，背景无接缝和道具，不生成文字或改变商品颜色' \
  --image /path/to/shoe.png
```

### 3. 商品生活方式场景

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '将参考咖啡机置于真实小户型厨房台面。保持机器、按钮、接口、Logo和相机角度，台面高度与产品尺度合理；早晨窗光从右侧进入，金属反射和接触阴影匹配，不添加杯子、蒸汽、食材或运行状态' \
  --image /path/to/coffee-machine.png
```

### 4. 人物换地点

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '保留人物身份、脸部、发型、服装、姿势和身体比例，把室内背景替换为黄昏海边木栈道。发丝与衣服边缘自然，脚部真实落地，夕阳从左后方形成轮廓光；不改变表情，不添加游客、文字或品牌' \
  --image /path/to/person.jpg
```

### 5. 跨市场环境版本

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '基于批准广告生成东京小户型、纽约阁楼、巴黎公寓三个环境版本。锁定人物、商品、动作、服装、相机和标题安全区；只改变空间、家具尺度和环境光，不生成国旗、地标、刻板符号、翻译、价格或新商品' \
  --image /path/to/approved-ad.jpg \
  --batch 3
```

## 合成检查

1. 放大检查毛发、透明材质、细小配件和主体边缘。
2. 核对主体尺度、相机高度、透视、焦点和景深是否属于同一空间。
3. 检查主光、色温、接触阴影、投影方向和反射是否一致。
4. 确认脚、轮子、商品底部与地面真实接触，没有悬浮或穿插。
5. 确认主体身份、商品结构、包装、Logo和颜色未发生附带修改。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name nano-banana-pro-background-replace
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

支持参考图、批量、比例参数、路由和输出目录。涉及电商白底或广告本地化时，以目标平台当前政策为准，并保留原图与合成版本的审计记录。
