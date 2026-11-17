---
name: iso-lineart-pipeline
slug: iso-lineart-pipeline
displayName: Isometric Line-Art Pipeline
display_name: "等距线稿管线"
description: Produce isometric line art from a parametric 3D blockout instead of hand-placing polygons in 2D — solid primitives, orthographic projection, z-buffer hidden-line removal with per-sample visibility, stroke weight driven by distance to the silhouette, and a hard minimum feature size so detail survives at game resolution. Use when a structure sketch must lock silhouette and construction for an image-to-image model, or when a line drawing keeps coming out with floating roofs, hatching that eats the outer contour, or braces that read as scaffolding.
description_zh: 用参数化三维体块出等距线稿，不在二维上拼多边形——实体基元 / 正交投影 / z-buffer 逐样本消隐 / 线宽由离剪影距离自动分级 / 构件有最低尺寸。适用于给图生图模型锁剪影与构造，或线稿老是屋顶悬空、排线糊剪影、斜撑读成脚手架的情况。
category: creative
version: 1.0.0
author: CatsMansion
agent_created: true
visibility: public
---

# 等距线稿管线

把「画一张等距线稿」变成一个几何问题：**你先建三维体块，消隐算法决定哪条线该出现。**

核心不是"代码画图"，是**承认有些问题二维画不出来**——
「墙顶在哪」「檐口在哪」这两个问题，二维拼贴法没有答案，所以它必然飘。

## 何时用

- 要给图生图模型喂一张**锁剪影与构造**的结构参考图
- 线稿反复出现：**屋顶悬空 / 排线糊掉外轮廓 / 斜撑读成脚手架**
- 同一栋建筑要出多个等级（Lv.0→3），希望共用一套几何、只改参数
- 要一张**几何可信**的等距草图，不在乎材质和笔触

**不用**：要成品插画（这里不画材质）、要手绘笔触、要透视相机（只做正交等距）。

## 五条铁律

1. **墙顶必须跟着屋面斜。** 单坡屋的山墙顶是梯形，做成水平面必然在山墙顶上留一条三角缝，整栋读成"顶着个盖子"。用 `wquad()`，不要用 `box()`。
2. **线宽由「离剪影多少像素」决定，不由面贴标签。** 同一条边在轮廓上要重、在内部要轻。把没人覆盖的像素膨胀 3px 当剪影带，落进去的线段自动升粗。
3. **装饰件做薄板，不做厚盒子。** 封檐板 / 窗台 / 门框做成厚盒子，三个可见面全是一片纸白，堆起来就是"一堆木块"。给 0.004–0.014 的厚度。
4. **构件尺寸下限 0.03 场景单位。** 换算到 240px 游戏尺寸还有 3.3px。低于这个数不是细节，是噪点——删掉，不要试图保留。
5. **消隐用「深度 + 小容差」，不用「面 ID 相等」。** 后者在两块共面墙皮处会丢线。`EPS = 0.0022`，别调大。

详细实测与理由见 `docs/lineart-rules.md`。

## 四步

| # | 动作 | 产出 | 闸门 |
|---|---|---|---|
| 1 | 标定相机 | `SX / SLOPE / SZ` 与纸底颜色 | 与目标参考的斜边斜率差 < 0.5px |
| 2 | 建体块 | 五个基元堆出的 `build()` | 每个构件都能说出它依附于谁 |
| 3 | 消隐出线 | `L.render(F, out.png)` | 0 悬空构件、0 看穿的洞 |
| 4 | 双档目检 | `make_comparison.py` 的 1:1 + 240px | 240px 档还读得出主要体量 |

⛔ **不要跳过第 4 步。** 很多问题只在其中一档暴露：1:1 看着精致、240px 糊成一团，或者反过来。
⛔ **不要在改完之后只看判据。** 判据只能说明"画对了"，说明不了"看得见"。改动必须肉眼看得出差别，否则等于没做。

## 脚本

| 脚本 | 作用 | 命令 |
|---|---|---|
| `scripts/line3d.py` | 渲染器：五个基元 + 正交投影 + z-buffer 消隐 + 剪影带线宽分级 | `python line3d.py`（打印参数，不含造型） |
| `scripts/design_shop.py` | 一栋单层单坡铺子的完整体块，可直接跑 | `python design_shop.py out.png` |
| `scripts/make_comparison.py` | 对照板：并排 + 游戏尺寸缩略档 | `python make_comparison.py --out b.png --item "新:out.png"` |

## 基元

```python
box(a0,a1,b0,b1,h0,h1)           # 轴对齐盒体
slab(top_quad, down=0.01)        # 给任意（可倾斜）顶面加厚度 —— 屋面板
extrude(profile, b0, b1)         # (a,h) 梯形沿 b 挤出
wquad(a0,a1,b0,b1,hbot,htop_fn)  # 顶跟着函数走的墙 —— 单坡屋必用
beam(p0,p1,wdir,w,t)             # 任意方向长条 —— 斜撑 / 斜梁
prism(cx,cy,h0,r,h,n)            # 棱柱 —— 桶 / 罐
```

坐标 `(a,b,h)`：`a` 沿屏幕右下，`b` 沿屏幕左上，`h` 向上。`a`、`b` 同时增大 = 远离相机。

## 线宽与容差

```python
W_SIL, W_STR, W_DET = 8.0, 3.8, 2.5   # 成品像素
SS   = 2                              # 超采样
EPS  = 0.0022                         # 消隐容差
```

`W_SIL` 不是"手动指定给剪影的"，是剪影带的实际渲染宽度。内部线靠 `W_STR / W_DET` 拉开层级。
三者差距小于 1.6 倍时层级会塌掉，看着到处一样重。

## 体量比例决定它读成什么

同一套线宽和细节，改比例就换物种（实测）：

| 进深 : 面宽 | 读成 |
|---|---|
| 0.52 : 0.48（进深大） | 岗楼 / 塔 |
| 0.50 : 0.56（面宽大） | 铺子 / 棚屋 |

另外：**「墙上的洞」读不出营业感。** 把台面挑出墙外 + 两根柱子撑檐口，前脸才有纵深。

## 边界

- ❌ 不画材质、不画笔触。亚像素抖动（0.55–0.75px）只能让线别太直，达不到手绘压感。
- ❌ 不做冷暖。纯线稿没有色阶，光色那一层要靠上色或模型。
- ❌ 不做自动构图。相机固定，画面按包围盒居中，其余手动调。
- ⚠️ 只做正交等距。要透视得改投影矩阵，超出本管线的假设。

## 成本

全本地计算，**0 积分**。1920×1920 单张 ≈3 秒（SS=2，3840² 深度缓冲）。
造型迭代只花时间，所以迭代纪律应该是「一次改动肉眼可见」，不是「指标变绿」。

## 依赖

Python 3.10+，`numpy`、`Pillow`。无 GPU、无网络、无 API。
