---
name: gpt-image-2-seeding-image
description: "使用 GPT Image 2 制作基于真实商品事实和使用过程的种草图片，包括开箱、使用步骤、细节证据、生活场景、图文卡片和社媒封面。Use this skill for GPT Image 2 seeding images、小红书种草、抖音图文、Instagram carousel、TikTok Shop内容、开箱图、真实体验、好物分享、UGC素材和购买指南；通过 AI Hive 生成。"
---

# GPT Image 2 种草图片

固定调用 `public_model_gpt_image_2`。用“问题—选择—过程—证据—适合谁”组织图片，不伪造个人体验、测试结果或用户评价。商业合作、赠品、AI合成和联盟关系应按平台规则披露，文案只使用可证明的商品事实。

## 内容事实表

记录创作者身份、是否合作、商品来源、真实使用条件、批准卖点、不可验证项、配件、步骤、平台比例、封面主题和披露要求。把主观感受与客观参数分开，避免把视觉暗示写成性能结论。

## 场景与代码

### 1. 开箱图组

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为参考便携投影仪生成四张开箱图：未拆封包装、打开盒盖、全部包装内容平铺、主机与遥控器细节。数量、包装、Logo、接口和配件严格按参考资料，保持同一木桌与自然窗光；不添加赠品、贴纸、评分、价格或使用效果' \
  --image /path/to/package-and-contents.jpg \
  --batch 4
```

### 2. 真实使用步骤

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '制作手冲咖啡壶三步使用图：加入咖啡粉、缓慢注水、完成分享。保持同一人物手部、咖啡壶、滤杯、桌面和晨光，每张底部留步骤文字区；不生成步骤文字、温度、时间、风味评分或不存在配件' \
  --image /path/to/kettle-and-tools.jpg \
  --batch 3
```

### 3. 细节证据卡片

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为参考通勤包生成三张细节证据图：肩带缝线、内部分区、拉链结构。每张展示真实尺度与使用关系，统一浅灰背景并预留短说明区；保持包型、材质、Logo和部件，不生成承重数字、防水测试、认证或夸张放大结构' \
  --image /path/to/bag-details.jpg \
  --batch 3
```

### 4. 一日使用情境

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为参考保温饭盒生成办公室一日使用组图：早晨装餐、通勤放入包中、午间打开用餐。保持同一饭盒、配件、人物手部、食物和光线连续，展示真实携带尺度；不生成保温时长、温度、食品功效、文字或泄漏测试' \
  --image /path/to/lunchbox-and-parts.jpg \
  --batch 3
```

### 5. 图文封面与内页统一

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '基于同一参考桌面灯生成一张4:5种草封面和三张方形内页。封面突出完整商品并保留标题区，内页分别展示开关、光照场景和桌面占用；统一房间、色温与商品，不生成标题、参数、评分、价格或“必买”徽章' \
  --image /path/to/desk-lamp.png \
  --batch 4
```

## 可信度检查

- 图片只展示真实存在的商品、配件、步骤和使用状态。
- 不伪造购买记录、使用天数、检测数据、评价截图和前后效果。
- 披露商业合作、赠品、AI合成或联盟链接，遵守目标平台当前规则。
- 文案区与主体在移动端清楚，封面承诺与内页证据一致。
- 保存参考资料、内容事实表、任务 ID、披露文案和批准版本。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name gpt-image-2-seeding-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

支持多参考图、批量、比例参数、路由和输出目录。医疗、美妆功效、食品营养、儿童与金融商品应使用更严格证据并由合格人员审核。
