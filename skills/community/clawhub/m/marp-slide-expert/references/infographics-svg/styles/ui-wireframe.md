# ui-wireframe

> 灰阶界面线框风格。中性、克制、不抢戏——适合讲清楚结构而不制造情绪。

## Token

```css
--c-bg:        #FFFFFF;
--c-light:     #E5E5E5;   /* 浅灰：占位块 */
--c-mid:       #9CA3AF;   /* 中灰：主要线条 */
--c-dark:      #374151;   /* 深灰：主文字、关键轮廓 */
--c-line:      #D1D5DB;   /* 分隔线 */
--c-interactive:#3B82F6;  /* 蓝：可交互元素 */
--c-emphasis:  #EF4444;   /* 红：强调、错误态 */
```

## 字阶

| class | 用途 | 特征 |
|---|---|---|
| `.t` | 标题 | 无衬线粗体 |
| `.tb` | 界面标签 | 无衬线中粗，浅灰 |
| `.sm` | 占位说明 | 无衬线常规，浅灰 |
| `.lbl` | 批注 | 无衬线小字 + 红 |

## 形状语言

- **线框框体**：`fill="none" stroke="#9CA3AF" stroke-width="1.5"`，`rx="4"`
- **占位块**：`fill="#E5E5E5"`，无描边
- **图片占位**：矩形 + 对角交叉线（X）
- **按钮**：圆角矩形填充 + 居中文字
- **网格底纹**：极淡（`opacity="0.15"`），帮助对齐
- **红色批注线**：折线引出 + 红字

```html
<rect x="100" y="60" width="820" height="400" fill="none" stroke="#9CA3AF" stroke-width="1.5" rx="4"/>
<rect x="116" y="76" width="788" height="44" fill="#E5E5E5"/>
<rect x="600" y="140" width="140" height="36" rx="4" fill="#3B82F6"/>
<text x="670" y="164" class="sm" fill="#ffffff" text-anchor="middle">提交</text>
```

## 硬性规则

**Do**
- 灰阶为主，蓝色**只**标可交互元素，红色**只**标强调和异常
- 界面元素的尺寸关系要合理（按钮 36px 高，输入框 44px）
- 批注线走直角折线，不穿过元素

**Don't**
- 真实品牌色和 logo——线框是中性的
- 渐变、投影、圆角夸张化
- 装饰插画
- 红色用得超过两处（红色一多就失去强调意义）

## 适合

产品设计、界面说明、应用概念、用户流程图、系统操作手册

## 配图建议

`linear-sequence` 箭头串（用户流程）、`linear-sequence` 阶梯（界面层级）、`structure-block`（页面区块拆解）、`hierarchy-tree`（信息架构）
