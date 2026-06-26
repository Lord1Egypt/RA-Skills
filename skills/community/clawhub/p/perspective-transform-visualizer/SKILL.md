---
name: perspective_transform_visualizer
description: 透视变换可视化工具。根据用户指定的变换参数（平移/旋转/缩放/剪切/透视），修改网页初始配置并打开浏览器展示效果。适合教学演示和手动调试。
---

# perspective-viz — 透视变换可视化

交互式 3D 透视变换可视化工具，使用 Three.js 展示 2D 图形在透视变换后的效果。

## 何时使用

1. 用户想直观理解透视变换效果
2. 用户需要调试变换矩阵参数
3. 教学场景：解释平移/旋转/缩放/剪切/透视参数
4. 用户想查看特定参数组合的可视化结果

## 文件结构

```
perspective_transform_visualizer/
├── SKILL.md
├── index.html          # 主页面（包含 configData 配置）
├── three.min.js        # Three.js 离线依赖
├── css/
│   └── style.css
└── README.md
```

## 使用方法

### 默认打开
```
用户：打开透视变换可视化
→ 直接用浏览器打开 ./index.html
```

### 带参数打开
根据用户描述修改 `index.html` 顶部的 `configData`，然后打开：

```javascript
const configData = {
    "matrix": { "m00": 1, "m01": 0, ... },
    "sliders": { "tx": 0, "ty": 0, "rotate": 0, "sx": 1, "sy": 1, "shx": 0, "shy": 0, "px": 0, "py": 0, "tz": 1 },
    "polygon": [[0, 0], [1, 0], [1, 1], [0, 1]]
};
```

### 参数映射

| 用户描述 | configData 字段 | 示例值 |
|---------|----------------|--------|
| 平移 tx | `sliders.tx` | 50（向右）/ -30（向左） |
| 平移 ty | `sliders.ty` | 30（向下）/ -20（向上） |
| 旋转角度 | `sliders.rotate` | 45（度） |
| 缩放 sx | `sliders.sx` | 2（放大 2 倍）/ 0.5（缩小） |
| 缩放 sy | `sliders.sy` | 1.5 |
| 剪切 shx | `sliders.shx` | 0.3 |
| 剪切 shy | `sliders.shy` | -0.2 |
| 透视 px | `sliders.px` | 0.2 |
| 透视 py | `sliders.py` | 0.3 |
| 自定义矩阵 | `matrix.*` | m00=2, m11=0.5, ... |

## 示例

### 示例 1：简单旋转
```
用户：帮我看看旋转 30 度的效果

操作：
1. 用 edit 工具修改 ./index.html，设置 sliders.rotate = 30
2. 用浏览器打开 ./index.html
回复：已打开透视变换可视化，初始旋转 30 度。
```

### 示例 2：组合变换
```
用户：我想看平移 tx=20, 旋转 45 度，再加一点透视 px=0.1 的效果

操作：
1. 修改 ./index.html 中的 configData.sliders = {tx: 20, rotate: 45, px: 0.1, ...其他保持默认}
2. 打开 ./index.html
回复：已配置组合变换（平移 20/旋转 45°/透视 x=0.1），请在浏览器中查看。
```

### 示例 3：自定义矩阵
```
用户：用这个矩阵看看效果：[[2,0,0],[0,1,0],[0,0,1]]

操作：
1. 修改 ./index.html 中的 configData.matrix = {m00:2, m01:0, m02:0, m10:0, m11:1, m12:0, m20:0, m21:0, m22:1}
2. 打开 ./index.html
回复：已应用自定义变换矩阵。
```

## 注意事项

- 修改 configData 后，用户刷新网页会恢复默认值（预期行为）
- 如果用户没有指定参数，使用默认值打开
- 本项目支持离线使用（three.min.js 已本地化）

## 远程设备支持

**关键**：用户可能通过手机、平板等远程设备与 OpenClaw 交互。在这种情况下，本地打开浏览器无效。

### 判断逻辑

1. **读取 runtime 信息**：检查 `channel` 和 `surface` 字段
   - `channel=feishu` + `surface=feishu` → 用户可能在手机上
   - `channel=discord` → 用户可能在手机或电脑
   - `channel=terminal` / `surface=cli` → 用户在本机

2. **处理方式**：
   - **用户在远程设备上**（飞书/Discord/WhatsApp 等）：
     - 优先使用在线版本：https://yu-zhengzheng.github.io/perspective_transform_visualizer/
     - 如果需要展示自定义参数，将参数编码到 URL 或告知用户手动设置
   - **用户在本机**（terminal/cli）：
     - 直接用 `Start-Process` 打开本地 `index.html`

### 示例：远程设备

```
用户（手机飞书）：打开透视变换可视化

操作：
1. 检查 runtime 信息，确认 channel=feishu
2. 使用 Start-Process 打开在线版本
回复：已在浏览器中打开透视变换可视化（在线版本，因检测到您可能在手机上）
```

## 在线版本

https://yu-zhengzheng.github.io/perspective_transform_visualizer/
