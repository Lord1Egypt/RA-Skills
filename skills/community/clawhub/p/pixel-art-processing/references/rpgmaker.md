# RPG Maker Workflow / RPG Maker 工作流

> [!IMPORTANT]
> RPG Maker 要求特定尺寸和格式的精灵图。本文档描述从原始素材到可用RPG Maker格式的完整处理流程。

## RPG Maker 精灵图规格 / RPG Maker Sprite Specs

### RPG Maker MV / MZ 角色规格

```
标准角色尺寸: 3列 × 4行 = 12个动作帧
每格尺寸: 144×144 像素 (MV默认)
布局:
  ┌─────┬─────┬─────┐
  │ 0   │ 1   │ 2   │  ← 待机/下
  ├─────┼─────┼─────┤
  │ 3   │ 4   │ 5   │  ← 左
  ├─────┼─────┼─────┤
  │ 6   │ 7   │ 8   │  ← 右
  ├─────┼─────┼─────┤
  │ 9   │ 10  │ 11  │  ← 上/背面
  └─────┴─────┴─────┘
```

### RPG Maker VX / ACE 角色规格

```
每格尺寸: 48×48 像素
布局: 同样 3×4
```

## 处理流程 / Processing Pipeline

### V1 一键处理 (最常用)

```
原始图片 → 去Gemini水印 → 左上角连通域抠图(容差80/羽化5) → 144×144硬缩放 → RPG Maker生成
```

**步骤详解 / Step by Step:**

1. **去水印 / Remove Watermark**
   - 使用 Gemini 水印去除算法
   - 定位并擦除右下角 "Gemini" 字样

2. **连通域抠图 / Connected Component Matting**
   - 从左上角开始，容差 80
   - 羽化值 5（边缘柔和过渡）
   - 提取主体前景

3. **硬缩放 / Hard Scale**
   - 使用最近邻插值 (NEAREST) 直接缩放到 144×144
   - **不要**使用平滑插值，会导致像素模糊

4. **RPG Maker 切分**
   - 将144×144大图切成3×4=12个48×48小格
   - 或者保持144×144大格（MV支持）

### V2 一键处理 (5行版)

```
去水印 → 256×256硬缩放 → 首像素连通域抠图 → 裁右64px、下扩透明64px
→ 第3/4行下移64px、第3行填入第2行镜像 → 每格四边裁8px合并 → 144×240
```

### RPG Maker 生成算法

```javascript
/**
 * 生成 RPG Maker 格式精灵图
 * @param frames - 处理好的帧数组 [HTMLImageElement 或 ImageData]
 * @param options
 */
function generateRPGMakerSprite(frames, options = {}) {
  const {
    cellW = 48,    // 每格宽度 (VX/ACE)
    cellH = 48,    // 每格高度
    cols = 3,      // 列数（动作数）
    rows = 4,      // 行数（方向）
    outScale = 3,  // 输出倍数 (MV默认3x, 所以实际输出144x144)
  } = options
  
  // 计算每行实际像素高度（考虑RPG Maker行走图比例）
  // 正面站立时，头部约占1/3，身子2/3
  const totalH = cellH * rows
  const totalW = cellW * cols
  
  // 如果输入是单张大图，先拆分
  const cells = []
  for (let row = 0; row < rows; row++) {
    for (let col = 0; col < cols; col++) {
      // 从大图中裁切对应格子
      const cell = cropCell(inputImage, col * cellW, row * cellH, cellW, cellH)
      cells.push(cell)
    }
  }
  
  // 排列为 RPG Maker 格式
  // 0=下(待机), 1=左, 2=右, 3=上(背面)
  // 但大多数素材顺序是: 下, 左, 右, 上 (不是ACE的左, 右, 上, 下)
  // 这里需要根据实际素材调整
  const rpgOrder = [0, 1, 2, 3]  // 下左右上
  const arranged = rpgOrder.map(idx => cells[idx])
  
  // 合并输出
  const canvas = document.createElement('canvas')
  canvas.width = totalW * outScale
  canvas.height = totalH * outScale
  const ctx = canvas.getContext('2d')
  
  for (let i = 0; i < arranged.length; i++) {
    const col = i % cols
    const row = Math.floor(i / cols)
    const x = col * cellW * outScale
    const y = row * cellH * outScale
    ctx.drawImage(arranged[i], x, y, cellW * outScale, cellH * outScale)
  }
  
  return canvas.toDataURL('image/png')
}
```

## 全动作处理 (Character Sheet)

RPG Maker 全动作角色通常包含:

```
┌────────┬────────┬────────┬────────┬────────┬────────┐
│ 待机   │ 走路   │ 跑步   │ 跳跃   │ 攻击   │ 技能   │
│ idle   │ walk   │ run    │ jump   │ atk    │ skill  │
├────────┼────────┼────────┼────────┼────────┼────────┤
│ 受伤   │ 特殊1  │ 特殊2  │ 躺下   │ 观察   │ ...    │
│ hurt   │ sp1    │ sp2    │ down   │ look   │        │
└────────┴────────┴────────┴────────┴────────┴────────┘
```

## 批量处理脚本 / Batch Processing Script

```javascript
/**
 * 批量处理多个RPG Maker角色素材
 */
async function batchRPGMakerProcess(imageFiles, options) {
  const results = []
  
  for (const file of imageFiles) {
    const img = await loadImage(file)
    
    // 1. 去水印
    const dewatermarked = await removeGeminiWatermark(img)
    
    // 2. 抠图（连通域，从左上角）
    const matted = await connectedComponentMatte(dewatermarked, {
      tolerance: 80,
      feather: 5,
      startX: 0,
      startY: 0
    })
    
    // 3. 缩放到 144x144
    const scaled = resizeImage(matted, 144, 144, 'nearest')
    
    // 4. 切分成 RPG Maker 格式
    const cells = splitIntoCells(scaled, 3, 4, 48, 48)
    
    // 5. 合成最终图
    const final = composeRPGMaker(cells)
    
    results.push({
      filename: file.name,
      result: final
    })
  }
  
  return results
}
```

## 像素美术风格转换 / Pixel Art Style Transfer

RPG Maker 像素角色处理要点:

1. **不要**对像素美术使用抗锯齿缩放
2. 缩放倍数最好为整数（如3x, 4x），避免非整数倍导致像素歪斜
3. 边缘处理使用锐化而非平滑
4. 透明边缘要保持清晰，不渐变

```javascript
// 正确的像素美术缩放
function pixelArtScale(img, scale) {
  const srcW = img.naturalWidth
  const srcH = img.naturalHeight
  const dstW = srcW * scale
  const dstH = srcH * scale
  
  const canvas = document.createElement('canvas')
  canvas.width = dstW
  canvas.height = dstH
  const ctx = canvas.getContext('2d')
  
  // 关键：关闭平滑，使用最近邻插值
  ctx.imageSmoothingEnabled = false
  ctx.mozImageSmoothingEnabled = false
  ctx.webkitImageSmoothingEnabled = false
  ctx.msImageSmoothingEnabled = false
  
  ctx.drawImage(img, 0, 0, dstW, dstH)
  return canvas
}
```

## 常见问题 / FAQ

**Q: 角色太大/太小怎么办？**
A: RPG Maker MV/MZ默认是48px基础尺寸，3x放大=144px。如果素材原始尺寸不同，按比例调整scale参数。

**Q: 透明边缘有黑边？**
A: 使用premultiply alpha处理，或者在合成前将黑色背景转为透明。

**Q: 行走图方向不对？**
A: RPG Maker方向约定：0=下，1=左，2=右，3=上。如果素材方向不同，调整 rpgOrder 数组。

**Q: 只有1行3列的素材？**
A: RPG Maker标准是4行（4个方向），如果只有走路动画（1行），需要额外填充其他方向或使用镜像。
