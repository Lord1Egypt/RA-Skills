# 空间、位置与角度控制词库

## 目标

把“放左边一点”“角度更高级”“产品更突出”这类模糊话术，改写成模型可执行的空间控制语言。

高精度 prompt 至少要说清楚 4 件事：
1. 产品在画面哪里
2. 产品朝向和旋转角度
3. 人物与产品怎么交互
4. 镜头从什么高度、什么距离拍

## 一、位置描述

### 1. 画面区域

| 中文 | 英文 |
| --- | --- |
| 正中央 | exact center |
| 中央偏左 | slightly left of center |
| 中央偏右 | slightly right of center |
| 左侧三分线 | on the left third |
| 右侧三分线 | on the right third |
| 左上角 | upper-left quadrant |
| 右上角 | upper-right quadrant |
| 左下角 | lower-left quadrant |
| 右下角 | lower-right quadrant |
| 前景 | foreground |
| 中景 | midground |
| 背景 | background |

### 2. 占画面比例

不要只说“大一点”“突出一点”，尽量量化：

- `占画面约 10%-15%`
- `占画面约 20%`
- `主体填满画面 1/2`
- `保留大面积负空间`

英文可直接写：

- `occupying about 12% of the frame`
- `filling roughly half of the frame`
- `leaving generous negative space on the right`

### 3. 相对锚点

如果画面里有人或桌面，优先用锚点来固定位置：

- `位于模特右手和下巴之间`
- `落在左髋骨位置`
- `放在桌面前缘偏右`
- `紧贴产品包装盒前方`
- `与人物脸部形成对角线构图`

## 二、角度描述

### 1. 产品展示角度

| 中文 | 英文 |
| --- | --- |
| 正面 | front view |
| 左 45° | three-quarter left view |
| 右 45° | three-quarter right view |
| 侧面 | side view |
| 顶视 | top view |
| 俯视 | top-down view |
| 仰视 | low-angle view |
| 平视 | eye-level view |
| 微微前倾 | slightly tilted forward |
| 微微后仰 | slightly tilted backward |

### 2. 旋转轴心

如果需要更精确，可以拆成 3 个维度：

- `yaw`：左右旋转
- `pitch`：前后倾斜
- `roll`：顺时针 / 逆时针歪斜

示例：

- `瓶身向左 yaw 约 30°`
- `产品 pitch 约 5°，轻微后仰`
- `画面 roll 保持 0°，不要倾斜`

### 3. 镜头高度

- `镜头与产品平齐`
- `镜头略高于产品 10 cm，轻微俯拍`
- `镜头低于桌面边缘，形成轻微仰拍`
- `半身视角，眼平线略高于模特肩膀`

英文短句：

- `camera at eye level with the product`
- `camera slightly above the subject, with a mild top-down angle`
- `camera placed below waist level for a subtle upward perspective`

## 三、人物与产品关系

### 1. 手持

- `模特右手自然持握产品，虎口朝上，手指不要遮挡 logo`
- `产品置于左手掌心中央，瓶身垂直`
- `双手托住产品底部，产品位于胸口正中`

### 2. 穿戴 / 佩戴

- `包包挂在左肩，包体落在左髋骨位置`
- `耳环靠近镜头一侧更清晰，面部轻微侧转`
- `鞋子以前脚掌朝向镜头 30° 的角度站立`

### 3. 桌面 / 落地 / 摆台

- `产品放在桌面右前方，距离画面下边缘约 8%`
- `鞋盒位于产品后方，略虚化，作为层次背景`
- `沙发位于画面中央，前景保留茶几虚化边缘`

## 四、构图短句

### 1. 电商主图

- `centered hero shot`
- `clean front-facing layout`
- `minimal white background`
- `product isolated with a soft natural shadow`

### 2. 海报构图

- `left-aligned subject with negative space for copy`
- `diagonal composition from the model's face to the product`
- `symmetrical editorial layout`

### 3. 人像带产品

- `the product should sit inside the visual triangle formed by the face, hand, and shoulder`
- `the face remains the primary focal point, the product as the secondary focal point`
- `keep the product fully readable without blocking the jawline or lips`

## 五、常用高精度句型

### 产品单品

```text
产品位于画面中央偏右，占画面约 18%，以前方 3/4 视角展示，向左旋转约 30°，logo 正对镜头，瓶身保持垂直，阴影自然落在右后方。
```

### 模特 + 包袋

```text
包包挂在模特左肩，包体落在左髋骨位置，正面朝向镜头偏右 15°，金属扣件清晰可见，不被头发或手臂遮挡。
```

### 模特 + 护肤品

```text
产品由模特右手自然持握，位于锁骨到胸口之间，处于画面右下 1/4 区域，占画面约 12%，瓶身正面朝向镜头，标签完整清晰。
```

### 珠宝近景

```text
耳环靠近镜头的一侧更突出，脸部轻微侧转 20°，镜头聚焦在耳环与脸颊交界区域，背景柔和虚化。
```

## 六、常见错误

### 错误 1：只说“换个角度”

不够好：
```text
旋转一下，角度高级一点
```

更好：
```text
产品保持结构不变，以右 45° 视角展示，镜头略高于产品，轻微俯拍，logo 仍需清晰正对镜头。
```

### 错误 2：只说“突出产品”

不够好：
```text
让产品更突出
```

更好：
```text
产品位于前景中央偏右，占画面约 20%，面部为第一视觉中心，产品为第二视觉中心，背景和服装对比度略降以突出产品。
```

### 错误 3：把产品角度和镜头角度混为一谈

要分开写：
- `产品朝向` 是物体本身怎么转
- `镜头角度` 是相机从哪里拍

## 七、使用原则

- 能量化就量化
- 能写锚点就别只写“左边一点”
- 能区分“产品朝向”和“镜头朝向”就不要混写
- 用户提到位置或角度时，这部分必须进入最终 prompt，不能只放在说明里
