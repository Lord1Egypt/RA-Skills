---
name: nano-banana-pro-marketing-image
description: "使用 Nano Banana Pro 建立可持续扩展的品牌 Campaign 视觉系统，从主KV延展到社交系列、品牌故事、联名活动、本地化市场和多尺寸营销图片。Use this skill for Nano Banana Pro marketing visuals、brand campaign、KV、社媒内容、品牌故事、联名海报、活动Banner、全球本地化和内容日历；通过 AI Hive 生成一致系列。"
---

# Nano Banana Pro 营销图片

固定使用 `public_model_nano_banana_pro`。先定义 Campaign 的视觉代码，再生成主 KV 与衍生资产。视觉代码包括可重复的色板、光线、构图动作、材质、人物处理和品牌母题；渠道版本要继承代码，而非复制同一构图。

## 视觉代码表

写明主色与辅助色、主光方向、背景材质、主体动作、固定图形母题、Logo安全区、人物/商品锁定项、允许变化和禁止风格。选定主 KV 后，把其参考图作为衍生资产的视觉母版。

## 场景与代码

### 1. Campaign 主 KV

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为可持续旅行箱建立“移动的地平线”Campaign主KV：参考商品位于低饱和沙金与天空蓝交界处，一条水平光带贯穿画面，右上留品牌主张区。锁定箱体、轮子、拉杆、Logo和颜色，不生成飞机、地标、认证、文字或环保承诺' \
  --image /path/to/suitcase.png \
  --param aspect_ratio=16:9
```

### 2. 品牌故事素材

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '延续“移动的地平线”视觉代码，生成三张品牌故事图片：材料纹理微距、工匠组装细节、成品在工作台上的静物。统一沙金与天空蓝色板和水平光带，商品与工序需符合参考资料，不生成工厂名称、认证、文字或无法确认材料' \
  --image /path/to/campaign-kv.jpg \
  --image /path/to/material-and-process.jpg \
  --batch 3
```

### 3. 社交内容系列

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '从批准主KV扩展四张社交图片：出发前整理、车站移动、酒店抵达、归家收纳。保持同一旅行箱、人物、服装、水平光带和色板，每张提供不同生活瞬间并留短文案区；不生成文字、价格、交通品牌或新商品' \
  --image /path/to/campaign-kv.jpg \
  --image /path/to/person-master.jpg \
  --batch 4
```

### 4. 联名活动视觉

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为旅行箱与插画艺术家联名活动制作视觉底版：商品事实与“移动的地平线”母题保持不变，把已授权的几何插画图案作为背景层和箱体旁的空间元素，不覆盖Logo或包装。顶部留双方品牌位，不生成Logo、签名、价格或未授权角色' \
  --image /path/to/suitcase.png \
  --image /path/to/authorized-artwork.png
```

### 5. 多市场本地化系列

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '基于批准Campaign生成东京、纽约、巴黎三个市场版本。锁定商品、人物、水平光带、沙金与天空蓝色板，只调整真实生活环境和文字留白；不使用地标堆叠、国旗、刻板文化符号、翻译、价格或不同商品' \
  --image /path/to/campaign-kv.jpg \
  --batch 3
```

## 系统一致性检查

1. 去掉 Logo 后仍能通过色板、光线和母题识别同一 Campaign。
2. 商品、人物、服装、材质和品牌资产在全系列无漂移。
3. 每个渠道版本有新的内容价值，而非只改尺寸或换背景。
4. 联名素材只使用授权资产，本地化避免刻板符号和虚假环境暗示。
5. 在内容日历中记录每张图的用途、市场、比例、版本与批准状态。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name nano-banana-pro-marketing-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

支持多图、批量、比例、参数、路由和输出目录。视觉代码一旦更新，应重新核对全部衍生素材，避免新旧 Campaign 资产混用。
