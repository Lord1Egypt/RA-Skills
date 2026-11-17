# 无浏览器环境 Python 视觉自查（python-preview）

沙盒里没有 Chromium / 无头浏览器时，无法对作品 HTML 截图验证。本手册提供替代方案：
**用 Python（Pillow + numpy）把 HTML 中 Canvas 的绘制逻辑逐笔复刻成 PNG 预览图**，再对
预览图做视觉评估。实战验证于《日出·印象》临摹（约 1.2 万程序化笔触的完整复刻，
preview.png 1313×1000 约 30s 生成）。

## 一、适用判断（先走降级链，不要盲目复刻）

```
需要视觉自查
 ├─ 1. 沙盒有 Chromium/playwright 可截图 → 直接截图（最准），本手册不用
 ├─ 2. playwright install 尝试下载 → 超过 ~120s 卡在 0% 即放弃，不要反复重试
 └─ 3. 转 Python 复刻管线（本手册）
      ├─ 作品以 Canvas 程序化绘制为主（笔触/粒子/纹理占大头）→ 复刻价值高 ✓
      └─ 作品以 SVG 滤镜质感为主（feTurbulence/blur/glow 占大头）→ 复刻价值低，
         只能近似大色块，评估时要格外小心误判（见第六节）
```

环境探测一行命令：
```bash
python3 -c "import numpy, PIL; print(numpy.__version__, PIL.__version__)"
which chromium chromium-browser google-chrome 2>/dev/null; echo "---"
```
Python 侧仅依赖 numpy + Pillow，几乎必装；无 Chromium 即触发本手册。

## 二、核心原理：随机数必须精确复刻

作品 JS 用固定种子发生器（如 `mulberry32(seed)`）保证可复现——复刻的前提就是 Python
侧产生**完全相同的随机数序列**。mulberry32 的精确 Python 等价实现（注意每步 `& M32`，
否则溢出为 Python 大整数后序列彻底错位）：

```python
M32 = 0xFFFFFFFF
class Rng:
    """mulberry32 精确复刻——与 JS 序列逐步一致（已实战验证）。"""
    def __init__(self, seed):
        self.s = seed & M32
    def rand(self):
        self.s = (self.s + 0x6D2B79F5) & M32   # 每步 & M32，否则 Python 大整数
        t = self.s ^ (self.s >> 15)            # 使序列彻底错位
        t = (t * (t | 1)) & M32
        t = ((t + (t ^ (t >> 7))) & M32) ^ t
        return (t ^ (t >> 14)) / 2**32
```

**消耗顺序是另一大坑**——JS 与 Python 必须按完全相同的顺序消耗 rand()：

1. **实参从左到右求值**：`stroke(w*rand(), h*rand(), col(), rand()*a, tilt)`
   实际消耗顺序是 w→h→col 内部→a→tilt。翻译到 Python 必须按此顺序逐行写，
   不能调换参数位置。
2. **声明行先消耗**：若 HTML 在循环前有 `const y = rand()*H` 之类，先于循环体消耗。
3. **col 表达式可能消耗 1–2 次**：若颜色表达式里嵌 rand()（如插值色相），按出现次数消耗。
4. **条件里的 rand() 有短路语义**：如 `if (Math.abs(x-SUNX)<130 && rand()<0.08)`
   —— 前半为假时后半**不消耗**！Python 里必须用同样的短路写法
   `if abs(x-sunx)<130 and rng.rand()<0.08`（Python 的 and 同样短路，保持即可），
   切勿先算好两个条件再判断。
5. **种子各层独立**：HTML 里 grain 层常用独立种子（如 `mulberry32(777)`），复刻时
   同样单独建 Rng，不要共用主种子。

已知可接受的误差：`math.sin` 与 JS `Math.sin` 存在 ULP 级差异，只影响 fbm/噪声类
微扰的个别取值，视觉上不可辨，不必强行对齐。

## 三、渲染管线映射表（Canvas API → PIL/numpy）

| HTML/Canvas 写法 | Python 复刻做法 |
|---|---|
| `createLinearGradient(0,0,0,H)` 垂直渐变 | 逐行插值出 `(H,3)` 数组，赋给 `base[y0:y1]` 时**必须 `[:, None, :]` 升维**广播到 `(H,W,3)` |
| `createRadialGradient(cx,cy,0,cx,cy,r)` | `np.mgrid` 建距离场 `d=√((gx-cx)²+(gy-cy)²)`，按 stops 分段线性混合 RGBA |
| `ctx.arc + fill` 太阳盘/圆点 | 布尔掩码 `d<=r` 直接赋色（前景锐利盘）；带光晕的用两层径向渐变近似 |
| `ctx.lineWidth; lineCap='round'` 笔触 | **圆头线段**函数：中段矩形 + 两端两个圆盘，numpy 在各自包围盒内做 src-over 逐笔混合 |
| `ctx.shadowBlur` / `filter: blur()` | 对整层 RGBA 建 `PIL.Image`，`GaussianBlur(radius)` 后再合成 |
| `ctx.globalAlpha = a` | 该层颜色 alpha 通道整体乘 a 再合成 |
| `globalCompositeOperation='screen'/'lighter'` | numpy: `255-(255-a)*(255-b)/255`（screen）或 `(a+b).clip(255)` |
| `mix-blend-mode: soft-light`（水面倒影常用） | numpy soft-light 公式逐通道实现，或先用普通 alpha 合成近似（预览够用） |
| SVG `<feTurbulence>` / CSS `filter:blur` 蚀边 | **无法精确复刻**——剪影用 `GaussianBlur(1.5)` 近似软边即可，评估时记住它与真品有差距 |

**分层策略**：与 HTML 图层一一对应——每层建一个 RGBA `PIL.Image`（或 numpy 数组），
在该层完成模糊/透明度后 `Image.alpha_composite(base, layer)`。**顺序严格照抄 HTML 的
DOM/绘制顺序**，混淆顺序会让评估结论全部失真。

**笔触函数骨架**（覆盖 90% 碎笔场景）：
```python
def stroke_np(base, x1, y1, x2, y2, w, rgba):
    """圆头线段，src-over 写入 base(H,W,4 uint8)，w 为线宽，rgba 含 alpha。"""
    R = w / 2
    xi0, xi1 = int(min(x1,x2)-R-1), int(max(x1,x2)+R+2)
    yi0, yi1 = int(min(y1,y2)-R-1), int(max(y1,y2)+R+2)
    xi0, xi1 = max(xi0,0), min(xi1, base.shape[1])
    yi0, yi1 = max(yi0,0), min(yi1, base.shape[0])
    if xi1 <= xi0 or yi1 <= yi0: return
    gy, gx = np.mgrid[yi0:yi1, xi0:xi1]      # 注意 gy 在前！
    dx, dy = x2-x1, y2-y1
    L2 = dx*dx + dy*dy
    if L2 < 1e-9:
        m = (gx-x1)**2 + (gy-y1)**2 <= R*R
    else:
        t = ((gx-x1)*dx + (gy-y1)*dy) / L2
        t = np.clip(t, 0, 1)
        px, py = x1 + t*dx, y1 + t*dy
        m = (gx-px)**2 + (gy-py)**2 <= R*R
    a = rgba[3] / 255.0
    region = base[yi0:yi1, xi0:xi1].astype(np.float32)
    src = np.array(rgba[:3], np.float32)
    al = m * a
    for c in range(3):
        region[:,:,c] = src[c]*al + region[:,:,c]*(1-al)
    base[yi0:yi1, xi0:xi1] = region.astype(np.uint8)
```
1.2 万笔 × 1313×1000 画布约 30 秒（包围盒裁剪是关键，别全图扫描）。

## 四、诊断图组合（一次运行输出 4 张）

```
full.png      全图原尺寸            → fetch 评估整体色调/构图/密度
thumb.png     25% 缩览              → 对应自查五问的"眯眼测试"（明度大关系）
zoom_<区>.png 关键区 2x 放大 2–3 张  → 太阳/视觉中心、前景主体、笔触质感抽查
```
缩览用 `img.resize((W//4, H//4), Image.LANCZOS)`；放大区直接数组切片再 `PIL.Image`
放大，避免重跑管线。

## 五、评估纪律：甄别"真实问题"vs"复刻局限"

预览图不是作品本身。fetch 评估每条意见，先问：**这是 HTML 的问题，还是预览复刻没做到？**
实战中提炼的常见误判模式：

| 预览表现 | 真相 | 处置 |
|---|---|---|
| 太阳/光源盘"过于锐利生硬" | HTML 里有 r88 光晕层 + blur 滤镜 + glow，预览未复现 | 不改 HTML |
| 倒影/水面"机械呆板" | HTML 有 fbm 摆动 + blur + 上层碎笔融合，预览简化了 | 不改 HTML |
| 剪影"边缘过于清晰" | HTML 有 feTurbulence 蚀边，预览只有近似 blur | 不改 HTML |
| 笔触有"拼接感/网格感" | 预览 1x 渲染 vs HTML 实际 2x canvas 再缩放 | 不改 HTML |
| 色调偏差、形体重量感不对、密度分布失衡 | **复刻不出来的也是真问题** | 改 HTML |

甄别口诀：**凡是"糊/锐/纹理感"的差评，先怀疑预览局限；凡是"色/形/量/分布"的差评，
大概率真问题**。改 HTML 后要**同步改 preview.py 同参数**，重跑复验，形成闭环。

## 六、实战踩坑清单（全部真实踩过）

1. **mulberry32 漏掉 `& M32`** → 序列从第一步就错位，画面完全对不上。每一步算术
   （加法、乘法、或运算）之后都要 mask。
2. **rand 消耗顺序对不上** → 症状是笔触位置/颜色系统性错乱而非轻微偏差。逐区核对
   HTML 里 rand() 的出现顺序（含声明行、实参、col 表达式、短路条件）。
3. **numpy 广播错误**：`base[0:301] = vgrad(...)` 得到 `(301,3)` 无法赋给 `(301,W,3)`
   → 渐变结果加 `[:, None, :]`。
4. **mgrid 轴序颠倒**：`gx,gy = np.mgrid[xi:xi1, yi:yi1]` 是错的——mgrid 第一个返回值
   对应**第一维（行，y）**。正确：`gy, gx = np.mgrid[yi0:yi1, xi0:xi1]`，切片也是
   `[y范围, x范围]`。症状是掩码维度不匹配或图案转置。
5. **PIL 多次随机坐标调用逆序**：`gd.rectangle([r()*W, r()*H, r()*W+1, r()*H+1])`
   四次独立随机数无坐标耦合，可能 x1>x2 被静默处理 → 画不出/位置错。单像素颗粒
   改用 `gd.point([r()*W, r()*H], fill=c)`。
6. **Playwright 下载卡死**：网络受限环境 `playwright install` 卡 0% 超 2 分钟即放弃，
   转本手册方案，不要烧 5–10 分钟反复重试。
7. **eval 生成式笔触别逐笔 print**：12000 笔逐笔打日志会拖慢 10 倍，只在每区结束时
   打一行进度。
8. **预览通过 ≠ 交付通过**：预览只能保证色/形/量/分布层面成立；滤镜质感、交互、
   分辨率适配仍需最终在真实浏览器确认（可请用户打开确认，或在有浏览器的环境复验）。
