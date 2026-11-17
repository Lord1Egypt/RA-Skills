# LeaferJS 动画系统完整参考

LeaferJS 提供丰富的动画功能，支持 CSS 风格过渡、关键帧动画、路径动画等。

## 使用方式

### 1. Animate 类（推荐精细控制）

```typescript
import { Animate } from '@leafer-in/animate'

const animate = new Animate(
    target,           // 目标元素或普通对象
    keyframes,        // 关键帧或目标状态
    options           // 动画选项
)
```

### 2. animate() 方法（简洁快捷）

```typescript
// 元素实例方法
const animate = rect.animate(
    { x: 500, rotation: 360 },
    { duration: 2, easing: 'ease-out' }
)
```

### 3. transition 属性（CSS 风格）

```typescript
// 设置过渡属性
rect.transition = { duration: 0.5, easing: 'ease' }

// 修改属性时自动动画
rect.x = 500          // 自动动画到 500
rect.fill = '#ff0000' // 颜色动画
```

### 4. animation 属性（声明式）

```typescript
rect.animation = {
    style: { x: 500, rotation: 360 },
    duration: 2,
    loop: true,
    easing: 'ease-in-out'
}
```

---

## Animate 选项

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| **duration** | number | 0 | 动画时长（秒） |
| **easing** | string | 'ease' | 缓动函数 |
| **delay** | number | 0 | 延迟开始时间（秒） |
| **speed** | number | 1 | 播放速度倍率 |
| **loop** | boolean \| number | false | 循环播放/循环次数 |
| **loopDelay** | number | 0 | 循环间隔（秒） |
| **swing** | boolean \| number | false | 摇摆循环播放 |
| **reverse** | boolean | false | 反向播放 |
| **autoplay** | boolean | true | 自动播放 |
| **join** | boolean | false | 加入初始状态作为第一帧 |
| **jump** | boolean | false | 首帧跳转 |
| **ending** | 'from' \| 'to' | 'to' | 结束状态 |
| **attrs** | string[] | - | 参与动画的属性列表 |

---

## 缓动函数

### 基础缓动

- `'linear'` - 线性匀速
- `'ease'` - 默认缓动（ease-in-out）
- `'ease-in'` - 缓入（加速）
- `'ease-out'` - 缓出（减速）
- `'ease-in-out'` - 缓入缓出

### 多项式缓动

- `'quad'` / `'quad-in'` / `'quad-out'` / `'quad-in-out'` - 二次
- `'cubic'` / `'cubic-in'` / `'cubic-out'` / `'cubic-in-out'` - 三次
- `'quart'` / `'quart-in'` / `'quart-out'` / `'quart-in-out'` - 四次
- `'quint'` / `'quint-in'` / `'quint-out'` / `'quint-in-out'` - 五次

### 特殊缓动

- `'sine'` - 正弦
- `'circ'` - 圆形
- `'back'` / `'back-in'` / `'back-out'` - 回弹（超出目标后返回）
- `'bounce'` / `'bounce-in'` / `'bounce-out'` - 弹跳
- `'elastic'` / `'elastic-in'` / `'elastic-out'` - 弹性

### 组合使用

```typescript
// 组合缓动名称
easing: 'ease-in-out-bounce'
easing: 'cubic-out'
easing: 'back-out'
```

---

## 关键帧格式

### 单关键帧（从当前状态到目标状态）

```typescript
// 目标状态对象
{ x: 500, y: 300, fill: '#ff0000' }
```

### 多关键帧数组

```typescript
[
    { style: { x: 100 }, duration: 0.5, easing: 'ease-out' },
    { style: { x: 200, rotation: 90 }, duration: 1, delay: 0.2 },
    { style: { x: 300, fill: '#00ff00' } }  // 使用默认时长
]
```

**关键帧属性**：
- `style` - 目标状态
- `duration` - 该关键帧时长
- `delay` - 该关键帧延迟
- `easing` - 该关键帧缓动

### 自动分配时长

```typescript
new Animate(rect, [
    { style: { x: 100 }, duration: 0.5 },
    { style: { x: 200 }, duration: 0.2 },
    { style: { x: 300 } }  // 剩余时长自动分配
], {
    duration: 3,  // 总时长 3 秒，最后一段 = 3 - 0.5 - 0.2 = 2.3 秒
    join: true    // 加入初始状态作为 from 关键帧
})
```

---

## 基础动画示例

### 位置动画

```typescript
import { Leafer, Rect } from 'leafer-ui'
import { Animate } from '@leafer-in/animate'

const leafer = new Leafer({ view: window })

const rect = new Rect({
    x: 50, y: 100,
    width: 100, height: 100,
    fill: '#32cd79'
})

leafer.add(rect)

// 移动到指定位置
new Animate(rect, { x: 500 }, { duration: 2 })

// 带缓动
new Animate(rect, { x: 500, y: 200 }, {
    duration: 2,
    easing: 'ease-out'
})

// 弹性效果
new Animate(rect, { x: 500 }, {
    duration: 2,
    easing: 'elastic-out'
})
```

### 缩放动画

```typescript
// 缩放
new Animate(rect, { scaleX: 2, scaleY: 2 }, { duration: 1 })

// 使用 scale 统一设置
rect.animate({ scale: 1.5 }, { duration: 1 })
```

### 旋转动画

```typescript
// 旋转 360 度
new Animate(rect, { rotation: 360 }, {
    duration: 2,
    loop: true,
    easing: 'linear'
})

// 摇摆旋转
new Animate(rect, { rotation: 45 }, {
    duration: 0.5,
    swing: true,
    loop: true
})
```

### 颜色动画

```typescript
import '@leafer-in/color'  // 需要颜色插件

// 颜色过渡
new Animate(rect, { fill: '#ff0000' }, { duration: 1 })

// 渐变填充
new Animate(rect, {
    fill: {
        type: 'linear',
        from: '#32cd79',
        to: '#ff6b6b'
    }
}, { duration: 2 })
```

---

## 循环动画

### 基础循环

```typescript
// 无限循环
new Animate(rect, { rotation: 360 }, {
    duration: 2,
    loop: true
})

// 指定循环次数
new Animate(rect, { rotation: 360 }, {
    duration: 2,
    loop: 3  // 循环 3 次
})
```

### 摇摆循环

```typescript
// 从 from 到 to 再到 from
new Animate(rect, { x: 500 }, {
    duration: 1,
    swing: true,     // 摇摆播放
    loop: true
})

// 指定到达 to 的次数
new Animate(rect, { x: 500 }, {
    duration: 1,
    swing: 2,        // 到达 to 两次（from->to->from->to）
    easing: 'ease-in-out'
})
```

### 循环间隔

```typescript
new Animate(rect, { rotation: 360 }, {
    duration: 2,
    loop: true,
    loopDelay: 1      // 每次循环间隔 1 秒
})
```

---

## 关键帧动画

```typescript
new Animate(rect, [
    // 第一帧：向右移动
    { style: { x: 200 }, duration: 0.5 },
    // 第二帧：旋转并变色
    { style: { rotation: 90, fill: '#ffcd00' }, duration: 0.5 },
    // 第三帧：缩放
    { style: { scale: 1.5 }, duration: 0.5 },
    // 第四帧：恢复
    { style: { rotation: 0, fill: '#32cd79', scale: 1 }, duration: 1 }
], {
    loop: true,
    easing: 'ease-in-out'
})
```

### 使用 join 包含初始状态

```typescript
// 初始状态为 x=50, y=100
new Animate(rect, [
    { style: { x: 300 } },
    { style: { x: 500 } }
], {
    duration: 2,
    join: true  // 将 x=50 作为第一帧，形成 50->300->500 的动画
})
```

---

## CSS 风格 Transition

```typescript
// 设置过渡属性
rect.transition = {
    duration: 0.5,
    easing: 'ease-out',
    delay: 0.1
}

// 修改属性时自动动画
rect.x = 500
rect.y = 300
rect.rotation = 45
rect.fill = '#ff0000'

// 移除过渡
rect.transition = false

// 临时禁用动画
tempAnimate: rect.set({ x: 100 }, false)  // 第二个参数为 false 禁用动画
```

---

## 路径动画

```typescript
import '@leafer-in/motion-path'

const path = new Path({
    path: 'M 100 300 Q 300 100 500 300 T 700 300',
    stroke: '#ddd'
})

const rect = new Rect({
    width: 30, height: 30,
    fill: '#ff6b6b',
    motion: path,           // 沿路径运动
    motionPath: true        // 自动旋转跟随路径
})

// 路径动画
rect.animate(
    { motion: 1 },         // 0 到 1 表示路径起点到终点
    { duration: 3, loop: true }
)
```

---

## 滚动动画

```typescript
import '@leafer-in/scroll'

const frame = new Frame({
    width: 300, height: 200,
    overflow: 'scroll'
})

// 滚动动画
new Animate(frame, { scrollY: 500 }, {
    duration: 2,
    easing: 'ease-in-out'
})
```

---

## 文本动画

### 打字机动画

```typescript
const text = new Text({
    text: '',              // 初始为空
    fill: '#333'
})

// 打字效果
text.animate(
    { text: 'Hello LeaferJS!' },
    { duration: 2 }
)
```

### 数字动画

```typescript
const text = new Text({
    text: '0',
    count: 1000,          // 目标数字
    duration: 2,          // 动画时长
    fontSize: 48,
    fill: '#32cd79'
})
```

---

## Animate 实例方法

### 控制方法

```typescript
const animate = rect.animate({ x: 500 }, { duration: 3 })

// 播放控制
animate.play()          // 播放
animate.pause()         // 暂停
animate.stop()          // 停止（跳转到结束）
animate.seek(1.5)       // 跳转到 1.5 秒
animate.seek(0.5, true) // 跳转到 50%

// 销毁
animate.kill()          // 强制完成并销毁
animate.destroy()       // 立即销毁（停留在当前状态）
```

### 状态属性

```typescript
animate.started     // 是否已开始
animate.running     // 是否正在播放
animate.completed   // 是否已完成
animate.destroyed   // 是否已销毁
animate.time        // 当前播放时间（秒）
animate.duration    // 总时长
animate.looped      // 已循环次数
```

---

## Animate 事件

```typescript
import { AnimateEvent } from '@leafer-in/animate'

const animate = rect.animate({ x: 500 }, { duration: 2 })

// 监听事件
animate.on(AnimateEvent.PLAY, () => {
    console.log('动画开始')
})

animate.on(AnimateEvent.UPDATE, (e) => {
    console.log('当前位置:', e.style.x)
})

animate.on(AnimateEvent.COMPLETED, () => {
    console.log('动画完成')
})

// 事件类型
AnimateEvent.PLAY      // 播放
AnimateEvent.PAUSE     // 暂停
AnimateEvent.UPDATE    // 更新
AnimateEvent.LOOP      // 循环
AnimateEvent.COMPLETED // 完成
AnimateEvent.DESTROY   // 销毁
```

---

## 链式动画

```typescript
// 使用 Promise 和 await
async function playSequence() {
    // 第一段动画
    await rect.animate({ x: 300 }, { duration: 1 }).promise
    
    // 第二段动画
    await rect.animate({ y: 200 }, { duration: 1 }).promise
    
    // 第三段动画
    await rect.animate({ rotation: 360 }, { duration: 1 }).promise
}

playSequence()
```

---

## 延迟动画

```typescript
// 使用 setTimeout
setTimeout(() => {
    rect.animate({ x: 500 }, { duration: 2 })
}, 1000)

// 使用 delay 选项
rect.animate({ x: 500 }, { duration: 2, delay: 1 })
```

---

## 复杂动画示例

### 卡片翻转动画

```typescript
const card = new Group({
    x: 200, y: 150,
    width: 200, height: 280
})

// 正面
const front = new Rect({
    width: 200, height: 280,
    fill: '#32cd79',
    cornerRadius: 12
})

// 背面
const back = new Rect({
    width: 200, height: 280,
    fill: '#ff6b6b',
    cornerRadius: 12,
    visible: false
})

card.add(front)
card.add(back)

let isFlipped = false\ncard.on(PointerEvent.TAP, () => {
    if (!isFlipped) {
        // 翻转到背面
        card.animate({ scaleX: 0 }, { duration: 0.2, easing: 'ease-in' })
            .once(AnimateEvent.COMPLETED, () => {
                front.visible = false
                back.visible = true
                card.animate({ scaleX: 1 }, { duration: 0.2, easing: 'ease-out' })
            })
    } else {
        // 翻转到正面
        card.animate({ scaleX: 0 }, { duration: 0.2, easing: 'ease-in' })
            .once(AnimateEvent.COMPLETED, () => {
                back.visible = false
                front.visible = true
                card.animate({ scaleX: 1 }, { duration: 0.2, easing: 'ease-out' })
            })
    }
    isFlipped = !isFlipped
})
```

### 加载动画

```typescript
const container = new Group()

const circles = []
const colors = ['#ff6b6b', '#ffcd00', '#32cd79', '#4dabf7', '#845ef7']

for (let i = 0; i < 5; i++) {
    const circle = new Ellipse({
        x: i * 60,
        width: 40, height: 40,
        fill: colors[i]
    })
    circles.push(circle)
    container.add(circle)
}

leafer.add(container)

// 波浪动画
circles.forEach((circle, i) => {
    circle.animate({ y: -30 }, {
        duration: 0.4,
        easing: 'ease-in-out',
        swing: true,
        loop: true,
        delay: i * 0.1
    })
})
```

### 进度条动画

```typescript
const bg = new Rect({
    x: 100, y: 300,
    width: 400, height: 20,
    fill: '#e9ecef',
    cornerRadius: 10
})

const progress = new Rect({
    x: 100, y: 300,
    width: 0, height: 20,
    fill: '#32cd79',
    cornerRadius: 10
})

leafer.add(bg)
leafer.add(progress)

// 进度动画
progress.animate({ width: 400 }, {
    duration: 3,
    easing: 'ease-out',
    loop: true
})

// 带百分比文本
const percentText = new Text({
    x: 300, y: 270,
    text: '0%',
    fontSize: 24,
    fill: '#333'
})

leafer.add(percentText)

const animate = progress.animate({ width: 400 }, {
    duration: 3,
    easing: 'ease-out'
})

animate.on(AnimateEvent.UPDATE, (e) => {
    const percent = Math.round((e.style.width || 0) / 400 * 100)
    percentText.text = `${percent}%`
})
```

---

## 注意事项

1. **颜色动画需要 color 插件**
   ```typescript
   import '@leafer-in/color'
   ```

2. **动画会修改元素属性**
   - 使用 `join: true` 保留初始状态
   - 使用 `destroy()` 立即停止并释放资源

3. **性能优化**
   - 多个元素同时动画时考虑使用 `sync: false`
   - 复杂动画可设置 `willReadFrequently: true`

4. **动画冲突**
   - 同一属性同时只能有一个动画
   - 新动画会自动覆盖旧动画

5. **内存管理**
   - 元素销毁时动画自动销毁
   - 手动创建的 Animate 实例需要手动 destroy
