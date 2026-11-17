# 人脸取景与三层合成

主讲人窗的非破坏合成、人脸居中漂移、蒙版参数与黑边排查。这是全包实测密度最高的一册——坐标系陷阱都是真机验出来的。

## 三层非破坏合成（铁律）

主讲人 PiP **不是**把人物视频裁成圆形。为了既能内部居中、又不破坏连续过渡：

| 层 | 职责 | 约束 |
| --- | --- | --- |
| 录屏层 | 底层证据画面 | 保持既定 rect、crop/fit、静音 |
| 完整人物层 | 原始人物视频与内部取景 | **保留完整源画幅**（item 本身 `crop*=0`、`borderRadius=0`），只用等比 reframe 改窗内取景 |
| Alpha 窗口层 | 圆形/圆角矩形的可见边界 | 独立蒙版冻结中心、尺寸、形状；描边沿蒙版外缘 |

把人物 item 直接裁成 PiP 的破坏性做法，会让后续一切「圆窗↔矩形↔全屏」连续过渡无法实现。ChatCut 宿主上，「满屏 item + 窗口 reframe shader」路线（见 `chatcut-field-notes.md`）与本契约同构——item 仍保留完整源画幅，窗口由 shader 切出。

## 效果顺序：reframe → mask →（描边/阴影）

视觉意图顺序永远是 **先 reframe（在完整画幅内平移/等比缩放）→ 后 mask（切出可见窗口）→ 描边/阴影只沿最终蒙版边界绘制**。反过来（先 mask 后 reframe）会让 reframe 从蒙版外的透明区采到黑色 RGB，产出大黑圆、黑条或「窗形还在、内部发黑」。

自定义 reframe shader 的同类错位：RGB 取自映射后的 `uvMapped`、Alpha 却沿用映射前的 `v_texCoord` 时，一旦上游已被 mask，效果会保留窗口 Alpha、同时从透明区采到黑色 RGB——「外形还在、里面大片发黑」的特征故障。修正效果顺序；新写 reframe shader 时让 RGB/Alpha 的采样坐标与透明语义一致，并把越界当作失败，不把 `clamp(uvMapped, 0, 1)` 的边缘拉丝当有效 overscan。

**实测创建顺序陷阱**（须每个新会话探针复验）：ChatCut 的 FX lane 编号与创建顺序可能相反——同一 clip 上想要 `reframe → mask` 的执行序，实际要**先 add mask、后 add reframe**，回读得到 reframe=lane 1、mask=lane 2 才是正确执行序。不要凭添加数组顺序判断，结构回读 lane + 用明显 offset 的单帧探针确认「人物移动、窗口不动、窗口外仍透明」。

## 蒙版参数与坐标系（GL UV，Y 轴原点在底部）

内建蒙版的已验证字段（新会话仍先回读工具描述）：

- 圆形 `fx-circle-mask`：`center_x`、`center_y`、`radius`、`feather`、`invert`。对画布 `W×H`、直径 `d`、左上角 `(x,y)`：`center_x=(x+d/2)/W`、`center_y=(y+d/2)/H`、**`radius = d/min(W,H)`（radius 值对应的是直径！）**，像素半径 = `radius × min(W,H) × 0.5`。
- 圆角矩形 `fx-rect-mask`：`width=w/W`、`height=h/H`，`corner_radius` 用像素值。
- 坐标按 GL UV 惯例，**Y 原点可能在底部**——按左上原点直觉算 Y 会整体翻转错位。先做单参数探针钉死原点方向再批量。
- 蒙版外必须输出真实 Alpha（透明），「用黑色填外部」不是透明；`feather` 从 1px 起步。

`propertyOverrides` 是**整包替换不是 PATCH**：只传一个字段会丢掉其余全部参数（巨脸/黑块的常见假象根因）。任何更新都完整重传参数组并立即结构回读。后端不校验未知字段——提交成功 ≠ 生效，必须单帧视觉验证。

以上宿主公式（原点方向、radius 语义、override 模式、lane 顺序）都属会话内需复验的实现细节：复制 `templates/compatibility.template.json`，对应探针 `passed` 后才套公式，否则重新探测或走稳定降级。能力探针用短暂 buffer item 或代表性稳定片段，先记录原 geometry/opacity/FX；验证结束立即删除 probe FX 并回读整条轨道确认无残留——**探针残留本身就是 P0**，不能留给最终导出。

## 居中 ≠ 贴脸（构图标准）

圆窗合格构图至少保留：完整头发、额头上方呼吸位、颈肩和一部分上半身/环境。「头发刚好可见」只是最低边界不是标准；整张脸贴满窗口判过近。作者在 330px 圆窗+同类完整人物源上的实测起点是 `magnification≈0.30`（0.43 能看到头发但仍偏挤）——**这是个人基线不是常量**，换素材/窗口/画幅必须重新标定（写进你自己的 operating profile）。

以双眼中点或脸部中心为目标：双眼落在窗口水平中央附近、垂直略高于中心。按说话段落设少量起终点做连续缓动，不逐帧追脸，不做肉眼可见的缩放呼吸。

## 焦点保持换算

若自定义 reframe 的映射为 `sampleUV = (outputUV - offset - pivot) / magnification + pivot`：

```text
把源焦点 faceCenter 映射到蒙版中心 maskCenter：
offset = maskCenter - pivot - magnification × (faceCenter - pivot)

已有稳定构图 (offset_old, m_old)，只改 magnification 并保持同一焦点：
offset_new = maskCenter - pivot - (m_new / m_old) × (maskCenter - pivot - offset_old)
```

不要沿用旧 offset。改完先在一个代表段验证首/中/末帧与人物姿态极值，通过后才同步其他同态段；稳定态的 magnification/offset 一变，**所有进出该状态的过渡端点同步失效**，每个方向重新抽帧验证。

## overscan 与黑边数学

动画前先算源画面对蒙版四边的余量（overscan），位移必须落在余量内：

```text
平移约束：-rightOverscan ≤ dx ≤ leftOverscan（纵向同理）
最小放大率：m ≥ max((maskW + 2|maxDx|)/baseW, (maskH + 2|maxDy|)/baseH)
```

- 横屏素材按高度铺满时纵向余量为 0——**想动 focalPointY 必须先等比放大产生余量**，否则必露黑。
- 先从源帧识别有效画面边界 `safeSourceRect`：**源素材自带的黑条也在源 UV 内**，不能误当可用余量（这是「反复修不掉的黑月牙」的真根因）。
- 除端点外还要检查缓动 20%/50%/80% 中间值与人物前倾/后仰极值——中间帧可能越界。

**黑边零容忍**：任一精确帧在圆窗 12/3/6/9 点或矩形四边露出黑边、透明边、UV 拖影，立即撤销整段动态 reframe，回退最近通过验证的静态构图。不许继续放大碰运气，不许用底色或遮罩掩盖。用户看不到动态居中，优于看到黑边。

## 故障分型速查

| 现象 | 优先归因 | 正确动作 |
| --- | --- | --- |
| 框线/网格穿过人物 | 装饰层级高于人物或缺 knockout | 装饰移到人物下方；描边只沿蒙版外缘；不裁人物躲线 |
| 圆窗一侧/顶部黑边 | 采样越出 safeSourceRect 或源自带黑条 | 对照源帧、查映射边界；回稳定静态 reframe |
| 窗形正常但内部大黑块 | mask 在 reframe 之前执行 | 回读 lane，按「先建 mask 后建 reframe」重建，60fps 短导出复验 |
| 只在一个导出帧闪一下 | MG 时间未按目标 fps 归一化，或过渡区间留缝 | 见 `motion-transitions.md` fps 归一化 |
| 单帧白块/条带/缺人 | 媒体解码竞争或 Alpha 合成 | 按四档链降解码预算/换定帧；不改几何参数碰运气 |

## 二次裁切事故（普通 PiP 也适用）

回读里的 `width/height` 通常是**裁切前外框**，正圆判定看裁后可见区：

```text
visibleWidth  = width  × (1 - cropLeft - cropRight)
visibleHeight = height × (1 - cropTop  - cropBottom)
```

典型正确结构：外框 533×300 + 左右合计裁 43.75% → 可见 300×300 + 圆角 150。把外框改成 300×300 却保留原裁切 = 可见宽被二次压到 169px = 叶片形/胶囊形/挤瘦人脸。成方策略二选一：显式裁切，或正方形 `fit:"cover"`——不叠加。修「原本是好的」的回归问题时，先复制同项目正常参考的**完整参数组**（尺寸/位置/四边 crop/fit/圆角），不重新设计。
