# LeaferJS 实用示例

本文档展示 LeaferJS 在实际场景中的应用示例。

---

## 图形编辑器

### 基础画板

```typescript
import { App, Rect, Ellipse, Text, KeyEvent } from 'leafer-ui'
import '@leafer-in/editor'
import '@leafer-in/viewport'
import '@leafer-in/export'

// 创建应用
const app = new App({
    view: window,
    fill: '#f5f5f5',
    editor: {
        stroke: '#0066ff',
        circle: {},
        buttons: {
            around: 'bottom',
            gap: 8
        }
    }
})

// 工具栏（使用 DOM 元素）
const toolbar = document.createElement('div')
toolbar.style.cssText = `
    position: fixed;
    top: 20px;
    left: 20px;
    background: white;
    padding: 10px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    display: flex;
    gap: 8px;
    z-index: 100;
`
document.body.appendChild(toolbar)

// 添加按钮
const tools = [
    { name: '矩形', action: () => addRect() },
    { name: '圆形', action: () => addCircle() },
    { name: '文本', action: () => addText() },
    { name: '删除', action: () => deleteSelected() },
    { name: '导出', action: () => exportImage() }
]

tools.forEach(tool => {
    const btn = document.createElement('button')
    btn.textContent = tool.name
    btn.style.cssText = `
        padding: 8px 16px;
        border: 1px solid #ddd;
        border-radius: 4px;
        background: white;
        cursor: pointer;
    `
    btn.onclick = tool.action
    toolbar.appendChild(btn)
})

// 添加矩形
function addRect() {
    const rect = Rect.one({
        editable: true,
        fill: '#32cd79',
        cornerRadius: 8
    }, 100 + Math.random() * 200, 100 + Math.random() * 200)
    app.tree.add(rect)
    app.editor.select(rect)
}

// 添加圆形
function addCircle() {
    const circle = Ellipse.one({
        editable: true,
        fill: '#ffcd00'
    }, 150 + Math.random() * 200, 150 + Math.random() * 200, 80, 80)
    app.tree.add(circle)
    app.editor.select(circle)
}

// 添加文本
function addText() {
    const text = Text.one({
        editable: true,
        text: '双击编辑文本',
        fontSize: 24,
        fill: '#333'
    }, 200 + Math.random() * 100, 200 + Math.random() * 100)
    app.tree.add(text)
    app.editor.select(text)
}

// 删除选中
function deleteSelected() {
    app.editor.list.forEach(item => item.remove())
    app.editor.target = null
}

// 导出图片
async function exportImage() {
    const blob = await app.tree.export('png')
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'canvas.png'
    a.click()
}

// 快捷键
app.on(KeyEvent.DOWN, (e) => {
    if (e.metaKey || e.ctrlKey) {
        switch(e.code) {
            case 'KeyZ':
                // 撤销（需要自行实现历史记录）
                break
            case 'KeyS':
                e.preventDefault()
                exportImage()
                break
        }
    } else if (e.code === 'Delete' || e.code === 'Backspace') {
        deleteSelected()
    }
})
```

### 流程图编辑器

```typescript
import { App, Box, Rect, Text, Line, Arrow, KeyEvent } from 'leafer-ui'
import '@leafer-in/editor'
import '@leafer-in/arrow'
import '@leafer-in/viewport'

const app = new App({
    view: window,
    fill: '#fafafa',
    editor: {}
})

// 流程节点样式
const nodeStyle = {
    width: 140,
    height: 60,
    fill: '#fff',
    stroke: '#ccc',
    strokeWidth: 1,
    cornerRadius: 4,
    shadow: { x: 0, y: 2, blur: 4, color: '#00000010' },
    editable: true,
    moveable: true
}

// 创建流程节点
function createNode(text: string, x: number, y: number) {
    const node = new Box({
        x, y,
        ...nodeStyle
    })
    
    const label = new Text({
        text,
        fontSize: 14,
        fill: '#333',
        x: '50%',
        y: '50%',
        textAlign: 'center',
        around: 'center'
    })
    
    node.add(label)
    return node
}

// 创建连接线
function createConnection(from: Box, to: Box) {
    const line = new Line({
        stroke: '#999',
        strokeWidth: 2,
        arrow: { start: false, end: true }
    })
    
    // 更新线条位置
    function updateLine() {
        const fromBounds = from.worldBounds
        const toBounds = to.worldBounds
        
        line.set({
            from: { x: fromBounds.x + fromBounds.width / 2, y: fromBounds.y + fromBounds.height },
            to: { x: toBounds.x + toBounds.width / 2, y: toBounds.y }
        })
    }
    
    updateLine()
    
    // 监听移动事件更新线条
    from.on('layout', updateLine)
    to.on('layout', updateLine)
    
    return line
}

// 创建流程图
const start = createNode('开始', 400, 50)
const process1 = createNode('处理 1', 400, 150)
const decision = create Node('决策', 400, 250)
const process2 = createNode('处理 2', 200, 350)
const process3 = createNode('处理 3', 600, 350)
const end = createNode('结束', 400, 450)

app.tree.addMany([start, process1, decision, process2, process3, end])

// 添加连接线
app.tree.add(createConnection(start, process1))
app.tree.add(createConnection(process1, decision))
// ... 更多连接线
```

---

## 小游戏

### 打砖块游戏

```typescript
import { App, Rect, Circle, Text, PointerEvent, MoveEvent } from 'leafer-ui'

const app = new App({
    view: window,
    fill: '#1a1a2e'
})

// 游戏状态
const state = {
    score: 0,
    lives: 3,
    gameOver: false,
    ballSpeed: { x: 4, y: -4 },
    paddleX: 350
}

// 挡板
const paddle = new Rect({
    x: 350, y: 550,
    width: 100, height: 15,
    fill: '#eee',
    cornerRadius: 7.5
})
app.tree.add(paddle)

// 球
const ball = new Circle({
    x: 400, y: 540,
    width: 15, height: 15,
    fill: '#ff6b6b'
})
app.tree.add(ball)

// 砖块
const bricks: Rect[] = []
const brickColors = ['#ff6b6b', '#feca57', '#48dbfb', '#ff9ff3', '#54a0ff']
for (let row = 0; row < 5; row++) {
    for (let col = 0; col < 10; col++) {
        const brick = new Rect({
            x: 50 + col * 70,
            y: 50 + row * 35,
            width: 65, height: 30,
            fill: brickColors[row],
            cornerRadius: 4
        })
        bricks.push(brick)
        app.tree.add(brick)
    }
}

// 分数显示
const scoreText = new Text({
    text: 'Score: 0',
    fontSize: 20,
    fill: '#fff',
    x: 20, y: 20
})
app.tree.add(scoreText)

// 鼠标控制挡板
app.on(PointerEvent.MOVE, (e) => {
    state.paddleX = Math.max(0, Math.min(700, e.x - 50))
    paddle.x = state.paddleX
})

// 游戏循环
function gameLoop() {
    if (state.gameOver) return
    
    // 移动球
    ball.x += state.ballSpeed.x
    ball.y += state.ballSpeed.y
    
    // 墙壁碰撞
    if (ball.x <= 0 || ball.x >= 785) state.ballSpeed.x *= -1
    if (ball.y <= 0) state.ballSpeed.y *= -1
    
    // 挡板碰撞
    if (ball.y >= 545 && ball.x >= paddle.x && ball.x <= paddle.x + 100) {
        state.ballSpeed.y = -Math.abs(state.ballSpeed.y)
        // 根据击中位置调整水平速度
        const hitPos = (ball.x - paddle.x) / 50 - 1
        state.ballSpeed.x = hitPos * 6
    }
    
    // 砖块碰撞检测
    bricks.forEach((brick, index) => {
        if (brick.removed) return
        
        if (ball.x >= brick.x && ball.x <= brick.x + 65 &&
            ball.y >= brick.y && ball.y <= brick.y + 30) {
            brick.remove()
            state.ballSpeed.y *= -1
            state.score += 10
            scoreText.text = `Score: ${state.score}`
        }
    })
    
    // 球掉落
    if (ball.y > 600) {
        state.lives--
        if (state.lives <= 0) {
            state.gameOver = true
            gameOverText.visible = true
        } else {
            ball.x = 400
            ball.y = 540
            state.ballSpeed = { x: 4, y: -4 }
        }
    }
    
    requestAnimationFrame(gameLoop)
}

// 游戏结束文字
const gameOverText = new Text({
    text: 'Game Over!',
    fontSize: 48,
    fill: '#fff',
    x: 400, y: 300,
    textAlign: 'center',
    around: 'center',
    visible: false
})
app.tree.add(gameOverText)

// 启动游戏
gameLoop()
```

### 贪吃蛇游戏

```typescript
import { App, Rect, Text, KeyEvent } from 'leafer-ui'

const app = new App({
    view: window,
    fill: '#111'
})

const GRID_SIZE = 20
const CELL_SIZE = 25

// 游戏状态
const game = {
    snake: [{ x: 10, y: 10 }],
    direction: { x: 1, y: 0 },
    food: { x: 15, y: 15 },
    score: 0,
    gameOver: false
}

// 网格背景
for (let x = 0; x < GRID_SIZE; x++) {
    for (let y = 0; y < GRID_SIZE; y++) {
        app.tree.add(new Rect({
            x: x * CELL_SIZE,
            y: y * CELL_SIZE,
            width: CELL_SIZE - 1,
            height: CELL_SIZE - 1,
            fill: (x + y) % 2 === 0 ? '#1a1a2e' : '#16213e'
        }))
    }
}

// 蛇身
const snakeRects: Rect[] = []
function updateSnake() {
    // 移除旧的
    snakeRects.forEach(r => r.remove())
    snakeRects.length = 0
    
    // 绘制新的
    game.snake.forEach((segment, i) => {
        const rect = new Rect({
            x: segment.x * CELL_SIZE + 1,
            y: segment.y * CELL_SIZE + 1,
            width: CELL_SIZE - 2,
            height: CELL_SIZE - 2,
            fill: i === 0 ? '#4cd137' : '#44bd32',
            cornerRadius: 4
        })
        snakeRects.push(rect)
        app.tree.add(rect)
    })
}

// 食物
const foodRect = new Rect({
    x: game.food.x * CELL_SIZE + 2,
    y: game.food.y * CELL_SIZE + 2,
    width: CELL_SIZE - 4,
    height: CELL_SIZE - 4,
    fill: '#e84118',
    cornerRadius: '50%'
})
app.tree.add(foodRect)

// 键盘控制
app.on(KeyEvent.DOWN, (e) => {
    if (game.gameOver) return
    
    switch(e.code) {
        case 'ArrowUp':
            if (game.direction.y === 0) game.direction = { x: 0, y: -1 }
            break
        case 'ArrowDown':
            if (game.direction.y === 0) game.direction = { x: 0, y: 1 }
            break
        case 'ArrowLeft':
            if (game.direction.x === 0) game.direction = { x: -1, y: 0 }
            break
        case 'ArrowRight':
            if (game.direction.x === 0) game.direction = { x: 1, y: 0 }
            break
    }
})

// 游戏循环
function gameLoop() {
    if (game.gameOver) return
    
    // 新头部
    const head = game.snake[0]
    const newHead = {
        x: head.x + game.direction.x,
        y: head.y + game.direction.y
    }
    
    // 碰撞检测
    if (newHead.x < 0 || newHead.x >= GRID_SIZE ||
        newHead.y < 0 || newHead.y >= GRID_SIZE ||
        game.snake.some(s => s.x === newHead.x && s.y === newHead.y)) {
        game.gameOver = true
        return
    }
    
    game.snake.unshift(newHead)
    
    // 吃食物
    if (newHead.x === game.food.x && newHead.y === game.food.y) {
        game.score += 10
        // 生成新食物
        do {
            game.food = {
                x: Math.floor(Math.random() * GRID_SIZE),
                y: Math.floor(Math.random() * GRID_SIZE)
            }
        } while (game.snake.some(s => s.x === game.food.x && s.y === game.food.y))
        
        foodRect.set({
            x: game.food.x * CELL_SIZE + 2,
            y: game.food.y * CELL_SIZE + 2
        })
    } else {
        game.snake.pop()
    }
    
    updateSnake()
    
    setTimeout(gameLoop, 150 - Math.min(100, game.snake.length * 2))
}

updateSnake()
gameLoop()
```

---

## 数据可视化

### 柱状图

```typescript
import { App, Rect, Text, Box, PointerEvent } from 'leafer-ui'
import '@leafer-in/animate'

const app = new App({
    view: window,
    fill: '#fafafa'
})

const data = [
    { label: '一月', value: 65 },
    { label: '二月', value: 45 },
    { label: '三月', value: 80 },
    { label: '四月', value: 55 },
    { label: '五月', value: 90 },
    { label: '六月', value: 70 }
]

const CHART_WIDTH = 700
const CHART_HEIGHT = 400
const BAR_WIDTH = 60
const GAP = 40
const MAX_VALUE = 100

// 标题
const title = new Text({
    text: '月度销售数据',
    fontSize: 24,
    fontWeight: 'bold',
    fill: '#333',
    x: 400, y: 30,
    textAlign: 'center'
})
app.tree.add(title)

// 图表区域
const chartBox = new Box({
    x: 50, y: 80,
    width: CHART_WIDTH,
    height: CHART_HEIGHT,
    fill: '#fff',
    cornerRadius: 8,
    shadow: { x: 0, y: 2, blur: 8, color: '#00000010' }
})
app.tree.add(chartBox)

// 绘制柱状图
data.forEach((item, index) => {
    const barHeight = (item.value / MAX_VALUE) * (CHART_HEIGHT - 60)
    const x = 50 + (index + 1) * GAP + index * BAR_WIDTH
    const y = CHART_HEIGHT - barHeight - 40
    
    // 柱子
    const bar = new Rect({
        x, y: y + barHeight,
        width: BAR_WIDTH,
        height: 0,
        fill: '#4a90d9',
        cornerRadius: [4, 4, 0, 0]
    })
    
    // 动画入场
    setTimeout(() => {
        bar.set({
            y: y,
            height: barHeight
        })
    }, index * 100)
    
    // 交互效果
    bar.on(PointerEvent.ENTER, () => {
        bar.fill = '#2d5a9e'
    })
    bar.on(PointerEvent.LEAVE, () => {
        bar.fill = '#4a90d9'
    })
    
    chartBox.add(bar)
    
    // 标签
    chartBox.add(new Text({
        text: item.label,
        fontSize: 12,
        fill: '#666',
        x: x + BAR_WIDTH / 2,
        y: CHART_HEIGHT - 30,
        textAlign: 'center'
    }))
    
    // 数值
    chartBox.add(new Text({
        text: item.value.toString(),
        fontSize: 12,
        fill: '#333',
        x: x + BAR_WIDTH / 2,
        y: y - 20,
        textAlign: 'center'
    }))
})

// Y 轴刻度
for (let i = 0; i <= 5; i++) {
    const value = (MAX_VALUE / 5) * i
    const y = CHART_HEIGHT - 40 - (i / 5) * (CHART_HEIGHT - 60)
    
    chartBox.add(new Text({
        text: value.toString(),
        fontSize: 11,
        fill: '#999',
        x: 10, y: y,
        around: 'left'
    }))
    
    // 网格线
    if (i > 0) {
        chartBox.add(new Rect({
            x: 35, y: y + 5,
            width: CHART_WIDTH - 50,
            height: 1,
            fill: '#eee'
        }))
    }
}
```

### 饼图

```typescript
import { App, Path, Text, Group, PointerEvent } from 'leafer-ui'

const app = new App({
    view: window,
    fill: '#fafafa'
})

const data = [
    { label: '直接访问', value: 30, color: '#5470c6' },
    { label: '邮件营销', value: 25, color: '#91cc75' },
    { label: '联盟广告', value: 20, color: '#fac858' },
    { label: '视频广告', value: 15, color: '#ee6666' },
    { label: '搜索引擎', value: 10, color: '#73c0de' }
]

const CENTER_X = 400
const CENTER_Y = 300
const RADIUS = 150

let currentAngle = -Math.PI / 2
const total = data.reduce((sum, d) => sum + d.value, 0)

data.forEach((item, index) => {
    const angle = (item.value / total) * Math.PI * 2
    const endAngle = currentAngle + angle
    
    // 计算扇形路径
    const startX = CENTER_X + Math.cos(currentAngle) * RADIUS
    const startY = CENTER_Y + Math.sin(currentAngle) * RADIUS
    const endX = CENTER_X + Math.cos(endAngle) * RADIUS
    const endY = CENTER_Y + Math.sin(endAngle) * RADIUS
    
    const largeArc = angle > Math.PI ? 1 : 0
    
    const path = new Path({
        path: `M ${CENTER_X} ${CENTER_Y} L ${startX} ${startY} A ${RADIUS} ${RADIUS} 0 ${largeArc} 1 ${endX} ${endY} Z`,
        fill: item.color,
        stroke: '#fff',
        strokeWidth: 2
    })
    
    // 交互效果
    path.on(PointerEvent.ENTER, () => {
        path.scale = 1.05
    })
    path.on(PointerEvent.LEAVE, () => {
        path.scale = 1
    })
    
    app.tree.add(path)
    
    // 标签位置
    const labelAngle = currentAngle + angle / 2
    const labelRadius = RADIUS + 40
    const labelX = CENTER_X + Math.cos(labelAngle) * labelRadius
    const labelY = CENTER_Y + Math.sin(labelAngle) * labelRadius
    
    // 标签
    app.tree.add(new Text({
        text: `${item.label} ${item.value}%`,
        fontSize: 12,
        fill: '#666',
        x: labelX,
        y: labelY,
        textAlign: 'center',
        around: 'center'
    }))
    
    currentAngle = endAngle
})

// 中心文字
app.tree.add(new Text({
    text: '访问来源',
    fontSize: 16,
    fill: '#999',
    x: CENTER_X,
    y: CENTER_Y,
    textAlign: 'center',
    around: 'center'
}))
```

---

## 海报生成器

### 社交媒体海报

```typescript
import { Leafer, Rect, Text, Image, Group } from 'leafer-ui'

async function createPoster(data: {
    title: string
    content: string
    author: string
    imageUrl?: string
    theme: 'dark' | 'light'
}) {
    const leafer = new Leafer({
        width: 800,
        height: 1000
    })
    
    const colors = data.theme === 'dark' ? {
        bg: '#1a1a2e',
        card: '#16213e',
        text: '#eee',
        secondary: '#aaa'
    } : {
        bg: '#f5f5f5',
        card: '#fff',
        text: '#333',
        secondary: '#666'
    }
    
    // 背景
    leafer.add(new Rect({
        width: 800,
        height: 1000,
        fill: colors.bg
    }))
    
    // 卡片
    const card = new Rect({
        x: 40, y: 40,
        width: 720,
        height: 920,
        fill: colors.card,
        cornerRadius: 16
    })
    leafer.add(card)
    
    // 主图
    if (data.imageUrl) {
        const img = new Image({
            url: data.imageUrl,
            x: 40, y: 40,
            width: 720,
            height: 400,
            around: 'top'
        })
        card.add(img)
    }
    
    // 标题
    const title = new Text({
        text: data.title,
        fontSize: 36,
        fontWeight: 'bold',
        fill: colors.text,
        x: 360,
        y: data.imageUrl ? 480 : 80,
        textAlign: 'center',
        around: 'top'
    })
    card.add(title)
    
    // 内容
    const content = new Text({
        text: data.content,
        fontSize: 18,
        fill: colors.secondary,
        x: 60,
        y: title.y + 60,
        width: 600,
        around: 'top'
    })
    card.add(content)
    
    // 作者
    card.add(new Text({
        text: `—— ${data.author}`,
        fontSize: 16,
        fill: colors.secondary,
        x: 660,
        y: 860,
        textAlign: 'right'
    }))
    
    // 导出
    const result = await leafer.export('png', { pixelRatio: 2 })
    return result.data
}

// 使用示例
createPoster({
    title: '设计的力量',
    content: '优秀的设计不仅仅是视觉上的美感，更是功能与形式的完美结合。当我们谈论设计时，我们谈论的是如何让用户的生活变得更加美好...',
    author: '张三',
    theme: 'light'
}).then(imageData => {
    // 保存或展示图片
    console.log('海报生成完成')
})
```

### 证书生成器

```typescript
import { Leafer, Rect, Text, Path, Image } from 'leafer-ui'

async function createCertificate(data: {
    recipient: string
    course: string
    date: string
    signature: string
    logo?: string
}) {
    const leafer = new Leafer({
        width: 1200,
        height: 850
    })
    
    // 背景
    leafer.add(new Rect({
        width: 1200,
        height: 850,
        fill: '#faf8f3'
    }))
    
    // 边框装饰
    const borderPath = `
        M 50 50 L 1150 50 L 1150 800 L 50 800 Z
    `
    leafer.add(new Path({
        path: borderPath,
        stroke: '#c9a227',
        strokeWidth: 4,
        fill: 'none'
    }))
    
    // 内边框
    leafer.add(new Path({
        path: 'M 70 70 L 1130 70 L 1130 780 L 70 780 Z',
        stroke: '#c9a227',
        strokeWidth: 1,
        fill: 'none'
    }))
    
    // Logo
    if (data.logo) {
        leafer.add(new Image({
            url: data.logo,
            x: 600, y: 120,
            width: 120, height: 120,
            around: 'center'
        }))
    }
    
    // 证书标题
    leafer.add(new Text({
        text: '结业证书',
        fontSize: 48,
        fontWeight: 'bold',
        fill: '#c9a227',
        x: 600, y: 260,
        textAlign: 'center',
        letterSpacing: 8
    }))
    
    // 正文
    leafer.add(new Text({
        text: `兹证明`,
        fontSize: 24,
        fill: '#333',
        x: 600, y: 340,
        textAlign: 'center'
    }))
    
    // 获奖者名字
    leafer.add(new Text({
        text: data.recipient,
        fontSize: 36,
        fontWeight: 'bold',
        fill: '#333',
        x: 600, y: 400,
        textAlign: 'center'
    }))
    
    // 完成课程
    leafer.add(new Text({
        text: `已完成 ${data.course} 课程的学习`,
        fontSize: 20,
        fill: '#666',
        x: 600, y: 460,
        textAlign: 'center'
    }))
    
    // 日期和签名
    leafer.add(new Text({
        text: data.date,
        fontSize: 18,
        fill: '#999',
        x: 900, y: 600
    }))
    
    leafer.add(new Text({
        text: data.signature,
        fontSize: 20,
        fill: '#333',
        x: 900, y: 640
    }))
    
    // 导出
    const result = await leafer.export('png', { pixelRatio: 2 })
    return result.data
}
```

---

## 思维导图

```typescript
import { App, Rect, Text, Line, Group, PointerEvent } from 'leafer-ui'

const app = new App({
    view: window,
    fill: '#fafafa'
})

// 节点数据结构
interface MindNode {
    text: string
    children?: MindNode[]
}

const data: MindNode = {
    text: '核心主题',
    children: [
        {
            text: '分支 1',
            children: [
                { text: '子节点 1' },
                { text: '子节点 2' }
            ]
        },
        {
            text: '分支 2',
            children: [
                { text: '子节点 3' },
                { text: '子节点 4' }
            ]
        }
    ]
}

const NODE_WIDTH = 120
const NODE_HEIGHT = 40
const GAP_X = 150
const GAP_Y = 60

function createNode(node: MindNode, x: number, y: number): Group {
    const group = new Group({ x, y })
    
    // 背景
    const rect = new Rect({
        width: NODE_WIDTH,
        height: NODE_HEIGHT,
        fill: '#fff',
        stroke: '#ddd',
        strokeWidth: 1,
        cornerRadius: 8,
        shadow: { x: 0, y: 2, blur: 4, color: '#00000010' }
    })
    group.add(rect)
    
    // 文字
    const text = new Text({
        text: node.text,
        fontSize: 14,
        fill: '#333',
        x: NODE_WIDTH / 2,
        y: NODE_HEIGHT / 2,
        textAlign: 'center',
        around: 'center'
    })
    group.add(text)
    
    // 拖拽
    let startX = 0, startY = 0
    group.on(PointerEvent.DOWN, (e) => {
        startX = group.x - e.x
        startY = group.y - e.y
    })
    group.on(PointerEvent.DRAG, (e) => {
        group.x = e.x + startX
        group.y = e.y + startY
    })
    
    return group
}

function createConnection(from: Group, to: Group) {
    const line = new Line({
        stroke: '#999',
        strokeWidth: 2
    })
    
    const update = () => {
        line.set({
            from: { x: from.x + NODE_WIDTH, y: from.y + NODE_HEIGHT / 2 },
            to: { x: to.x, y: to.y + NODE_HEIGHT / 2 }
        })
    }
    
    from.on('layout', update)
    to.on('layout', update)
    update()
    
    return line
}

// 递归渲染
function renderTree(node: MindNode, x: number, y: number, parent?: Group) {
    const group = createNode(node, x, y)
    app.tree.add(group)
    
    if (parent) {
        const line = createConnection(parent, group)
        app.tree.add(line)
    }
    
    if (node.children) {
        const childY = y - (node.children.length - 1) * GAP_Y / 2
        node.children.forEach((child, i) => {
            renderTree(child, x + GAP_X, childY + i * GAP_Y, group)
        })
    }
    
    return group
}

renderTree(data, 100, 300)
```

---

## 无限画布

```typescript
import { App, Rect, Text, PointerEvent, MoveEvent, ZoomEvent } from 'leafer-ui'
import '@leafer-in/viewport'

const app = new App({
    view: window,
    fill: '#f5f5f5',
    viewport: {
        zoom: 1,
        move: { x: 0, y: 0 }
    }
})

// 网格背景
const GRID_SIZE = 50

function drawGrid() {
    const { zoom, move } = app.viewport
    const width = app.width / zoom
    const height = app.height / zoom
    
    // 绘制网格线
    const startX = Math.floor(-move.x / zoom / GRID_SIZE) * GRID_SIZE
    const startY = Math.floor(-move.y / zoom / GRID_SIZE) * GRID_SIZE
    
    for (let x = startX; x < startX + width + GRID_SIZE; x += GRID_SIZE) {
        app.tree.add(new Rect({
            x, y: startY,
            width: 1,
            height: height + GRID_SIZE,
            fill: '#e0e0e0'
        }))
    }
    
    for (let y = startY; y < startY + height + GRID_SIZE; y += GRID_SIZE) {
        app.tree.add(new Rect({
            x: startX, y,
            width: width + GRID_SIZE,
            height: 1,
            fill: '#e0e0e0'
        }))
    }
}

// 示例卡片
function createCard(x: number, y: number, title: string) {
    const card = new Rect({
        x, y,
        width: 300,
        height: 200,
        fill: '#fff',
        cornerRadius: 8,
        shadow: { x: 0, y: 4, blur: 12, color: '#00000015' },
        draggable: true
    })
    
    const titleText = new Text({
        text: title,
        fontSize: 20,
        fontWeight: 'bold',
        fill: '#333',
        x: 20, y: 20
    })
    
    const content = new Text({
        text: '这是一个可拖拽的卡片...',
        fontSize: 14,
        fill: '#666',
        x: 20, y: 60,
        width: 260
    })
    
    card.add(titleText)
    card.add(content)
    
    return card
}

// 创建一些卡片
app.tree.add(createCard(100, 100, '卡片 1'))
app.tree.add(createCard(450, 150, '卡片 2'))
app.tree.add(createCard(200, 400, '卡片 3'))

// 空格+拖拽平移
let isPanning = false
let panStart = { x: 0, y: 0 }

app.on(PointerEvent.DOWN, (e) => {
    if (e.spaceKey) {
        isPanning = true
        panStart = { x: e.x, y: e.y }
    }
})

app.on(PointerEvent.MOVE, (e) => {
    if (isPanning) {
        const dx = e.x - panStart.x
        const dy = e.y - panStart.y
        app.viewport.move = {
            x: app.viewport.move.x + dx,
            y: app.viewport.move.y + dy
        }
        panStart = { x: e.x, y: e.y }
    }
})

app.on(PointerEvent.UP, () => {
    isPanning = false
})

// 滚轮缩放
app.on(ZoomEvent.ZOOM, (e) => {
    app.viewport.zoom = Math.max(0.1, Math.min(5, app.viewport.zoom * e.scale))
})
```

---

## 图片编辑器

```typescript
import { App, Image, Rect, Frame, Filter } from 'leafer-ui'
import '@leafer-in/editor'
import '@leafer-in/viewport'
import '@leafer-in/filter'

const app = new App({
    view: window,
    fill: '#1a1a2e',
    editor: {}
})

// 上传图片
function loadImage(file: File) {
    const reader = new FileReader()
    reader.onload = (e) => {
        const img = new Image({
            url: e.target?.result as string,
            editable: true
        })
        app.tree.add(img)
        app.editor.select(img)
    }
    reader.readAsDataURL(file)
}

// 滤镜控制
const filters = {
    brightness: 1,
    contrast: 1,
    saturation: 1,
    blur: 0,
    sepia: 0,
    grayscale: 0
}

function applyFilter(type: keyof typeof filters, value: number) {
    const selected = app.editor.element as Image
    if (!selected) return
    
    filters[type] = value
    
    selected.filter = {
        brightness: filters.brightness,
        contrast: filters.contrast,
        saturate: filters.saturation,
        blur: filters.blur,
        sepia: filters.sepia,
        grayscale: filters.grayscale
    }
}

// 裁剪功能
function cropImage(x: number, y: number, width: number, height: number) {
    const selected = app.editor.element as Image
    if (!selected) return
    
    const frame = new Frame({
        x, y, width, height,
        fill: 'none',
        stroke: '#fff',
        strokeWidth: 2,
        strokeDash: [5, 5]
    })
    
    app.tree.add(frame)
}

// 添加滤镜滑块控制（使用 DOM）
const controls = document.createElement('div')
controls.style.cssText = `
    position: fixed;
    right: 20px;
    top: 20px;
    background: rgba(255,255,255,0.9);
    padding: 20px;
    border-radius: 8px;
    width: 250px;
`

document.body.appendChild(controls)

const filterControls = [
    { name: 'brightness', label: '亮度', min: 0, max: 2, step: 0.1 },
    { name: 'contrast', label: '对比度', min: 0, max: 2, step: 0.1 },
    { name: 'saturation', label: '饱和度', min: 0, max: 2, step: 0.1 },
    { name: 'blur', label: '模糊', min: 0, max: 10, step: 1 },
    { name: 'sepia', label: '复古', min: 0, max: 1, step: 0.1 },
    { name: 'grayscale', label: '灰度', min: 0, max: 1, step: 0.1 }
]

filterControls.forEach(ctrl => {
    const label = document.createElement('label')
    label.textContent = ctrl.label
    label.style.cssText = 'display: block; margin: 10px 0 5px;'
    
    const slider = document.createElement('input')
    slider.type = 'range'
    slider.min = ctrl.min.toString()
    slider.max = ctrl.max.toString()
    slider.step = ctrl.step.toString()
    slider.value = ctrl.name === 'brightness' || ctrl.name === 'contrast' || ctrl.name === 'saturation' ? '1' : '0'
    slider.style.width = '100%'
    
    slider.oninput = (e) => {
        applyFilter(ctrl.name as keyof typeof filters, parseFloat((e.target as HTMLInputElement).value))
    }
    
    controls.appendChild(label)
    controls.appendChild(slider)
})
```
