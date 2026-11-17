# Canvas 程序化生成手册（canvas-techniques）

需要**成百上千个相似但不同的有机元素**时，用 Canvas 循环生成。核心思想：确定性随机
（seed）+ 数学噪声 + 少量物理直觉。

## 0. 确定性随机（所有代码的基座）

```js
// mulberry32 — 固定种子，刷新不变，可安全迭代修复
function RNG(seed){ return function(){ seed|=0; seed=seed+0x6D2B79F5|0;
  let t=Math.imul(seed^seed>>>15,1|seed); t=t+Math.imul(t^t>>>7,61|t)^t;
  return ((t^t>>>14)>>>0)/4294967296; } }
const rand = RNG(20260827);
```

一维/二维平滑噪声（无需引库的实现骨架）：

```js
function hash2(x,y,seed){ const s=Math.sin(x*127.1+y*311.7+seed*74.7)*43758.5453; return s-Math.floor(s); }
function noise2(x,y,seed){
  const xi=Math.floor(x), yi=Math.floor(y), xf=x-xi, yf=y-yi;
  const u=xf*xf*(3-2*xf), v=yf*yf*(3-2*yf);
  return hash2(xi,yi,seed)*(1-u)*(1-v)+hash2(xi+1,yi,seed)*u*(1-v)
       + hash2(xi,yi+1,seed)*(1-u)*v   +hash2(xi+1,yi+1,seed)*u*v;
}
function fbm(x,y,seed,oct=4){ let a=0.5,f=1,s=0;
  for(let i=0;i<oct;i++){ s+=a*noise2(x*f,y*f,seed+i*17); a*=0.5; f*=2; } return s; }
```

## 1. 远山叠嶂（水墨/青绿必用）

原理：用 fbm 噪声逐列采样高度 → path 描出山脊 → 由后到前画 4–6 层，
越远越亮、越远饱和度越低、越远混入天色越多。

```js
function ridge(ctx,W,H,baseY,amp,color,seed,detail=3){
  ctx.beginPath(); ctx.moveTo(0,H);
  for(let x=0;x<=W;x+=4){
    const y = baseY - fbm(x*0.002, seed, seed, detail)*amp;
    ctx.lineTo(x,y);
  }
  ctx.lineTo(W,H); ctx.closePath();
  // 垂直渐变：山脚融入天色(大气透视的关键)
  const g=ctx.createLinearGradient(0,baseY-amp,0,H);
  g.addColorStop(0,color); g.addColorStop(1,mistColor);
  ctx.fillStyle=g; ctx.fill();
}
```

## 2. 松林 / 森林木

三角形树：底部宽度 bw、高 h 的 ratio 变化 + 轻微倾斜 `rot = (rand()-0.5)*0.12`。
近大远小、近深远浅；随机 10% 的树换一个色相 ±8° 打破均匀。
松针质感：在树冠内再叠加 30–60 条短弧线 stroke，`globalAlpha≤0.25`。

```js
for(let i=0;i<n;i++){
  const x=rand()*W, depth=rand();         // depth: 0远 1近
  const s = 0.35+depth*0.65;
  drawTree(ctx,x, baseY - depth*hOffset, treeH*s, mix(farColor,nearColor,depth));
}
```

## 3. 水面波光 / 倒影

```js
// 波光横线：透视上密下疏、上短下长；亮度随 fbm 时间域抖动
for(let i=0;i<count;i++){
  const t = Math.pow(rand(),1.6);          // 靠远处密集
  const y = horizonY + (H-horizonY)*t;
  const w = (6+t*46) * (0.6+rand()*0.8);
  const a = 0.08+fbm(i*0.1,t*5,7)*0.5*t;
  ctx.strokeStyle=`rgba(255,240,210,${a})`;   // 高光色≈光源色
  ctx.lineWidth=1+t*1.6;
  ctx.beginPath(); ctx.moveTo(cx-w/2+jitter,y); ctx.lineTo(cx+w/2+jitter,y); ctx.stroke();
}
```
倒影：先把岸上主对象 drawImage 垂直翻转贴到水面区，叠 `rgba(水色,0.55)`，
再叠加若干水平位错条带（每条 `drawImage` 错开 2–6px）模拟波流扰动。

## 4. 星空银河

星：三层深度。亮度分布用幂律 `mag = Math.pow(rand(),3)`，让少量星特别亮。
银河带：沿一条贝塞尔主轴撒点，横向高斯散布 `offset=(rand()+rand()+rand()-1.5)*spread`，
颜色偏暖白；中心亮带叠一层 screen 渐变。个别亮星加十字衍射芒（两条渐隐细线）。

## 5. 雨 / 雪 / 樱花等粒子

统一骨架——粒子数组 + 确定性初始化 + 每帧更新（若静态画面则预计算并一次绘完）：

```js
class P{ constructor(){ this.reset(true);} reset(init){ 
  this.x=rand()*W; this.y= init? rand()*H : -20;
  this.vy=2+rand()*3; this.vx=0.4+rand()*0.6; this.r=1+rand()*1.6; this.a=0.15+rand()*0.5;}
 step(){ this.x+=this.vx; this.y+=this.vy; if(this.y>H+20)this.reset(false);}
 draw(c){ c.globalAlpha=this.a; c.fillStyle='#fff';
   c.beginPath(); c.arc(this.x,this.y,this.r,0,7); c.fill(); } }
```
雨 = 细长线段(`lineTo(x-vx*4,y-vy*4)`)而非圆点；雪 = 正弦摆动 `x += sin(y*0.02+phase)`；
花瓣 = 旋转的小椭圆，转速与摆动同频。

## 6. 像素风

- 逻辑分辨率设低（如 160×90），CSS 放大 8–10 倍 + `image-rendering: pixelated`。
- 调色板先定死（≤16 色），禁止运行时插值产生中间色。
- 明暗作 2×2 或 3×3 抖动铺陈，轮廓线用手动点阵勾勒。
- 小人比例约 16×24 px 内完成头身腿三段。

## 7. 与 SVG 分工的合成建议

把整幅画拆为：
`底层 CSS/SVG 天空` → `中层 SVG 大形体` → `顶层 <canvas> 纹理与粒子` →
`罩层 paperGrain`。Canvas 元素对齐用绝对定位坐标同步 viewBox 比例即可；
导出展示以整页 HTML 为单位，不必合并成单 canvas。
