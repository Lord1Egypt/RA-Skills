<p align="center">
 <img src="https://img.shields.io/badge/Three.js-000?style=flat&logo=three.js&logoColor=white" alt="Three.js">
 <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=white" alt="JavaScript">
 <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="MIT">
</p>

# 🔷 透视变换可视化工具

> **⚠️ 重要声明：这个项目是 100% 纯氛围编程 (Vibe Coding) 完成的。**
> 
> 没有预先的设计文档，没有详细的技术规格，甚至没有画过一张草图。只是有一个想法——"做个能看透视变换的网页"——然后直接开始写代码，让代码自己生长出来。

交互式的 **3D 透视变换可视化工具**，使用 Three.js 展示 2D 图形在透视变换后的 3D 效果。

---

## ✨ 功能特性

### 可控参数

| 参数 | 说明 |
|------|------|
| **平移 (tx, ty)** | 水平/垂直方向移动 |
| **旋转** | 绕原点旋转角度 |
| **缩放 (sx, sy)** | 水平/垂直方向缩放 |
| **剪切 (shx, shy)** | 水平/垂直方向剪切 |
| **透视 (px, py)** | 产生透视效果 |
| **Z轴距离** | 透视矩阵的 w 分量 |

### 核心特性

- 🎯 **实时预览**：拖动滑块即时看到变换效果
- 📐 **矩阵显示**：实时显示 3×3 变换矩阵，可直接编辑
- 🔄 **双向同步**：修改矩阵或滑块，另一方自动同步
- 📍 **点坐标编辑**：可添加/删除/修改多边形顶点
- 🎥 **3D 可视化**：Three.js 渲染的 3D 视图
- 🖱️ **相机控制**：鼠标拖拽旋转视角

---

## 🚀 在线访问

**直接访问**：https://yu-zhengzheng.github.io/perspective_transform_visualizer/

---

## 🚀 本地运行

直接用浏览器打开 `index.html` 即可（支持离线）：

```bash
# 双击 index.html
# 或
python -m http.server 8000
# 然后访问 http://localhost:8000
```

---

## ⚙️ 配置

初始配置在 HTML 文件顶部的 `configData` 变量中：

```javascript
const configData = {
    "matrix": { "m00": 1, "m01": 0, "m02": 0, "m10": 0, "m11": 1, "m12": 0, "m20": 0, "m21": 0, "m22": 2 },
    "sliders": { "tx": 0, "ty": 0, "rotate": 0, "sx": 1, "sy": 1, "shx": 0, "shy": 0, "px": 0, "py": 0, "tz": 0 },
    "polygon": [[0, 0], [1, 0], [1, 1], [0, 1]]
};
```

---

## 📐 数学原理

### 3×3 透视变换矩阵

```
| a  b  tx |
| c  d  ty |
| px py  w |
```

透视变换将 2D 点 (x, y) 转换为齐次坐标 (X, Y, W)：

```
X = a*x + b*y + tx
Y = c*x + d*y + ty
W = px*x + py*y + w
```

然后通过透视除法得到最终坐标：

```
x' = X / W
y' = Y / W
```

---

## 📄 License

MIT License - 详见 [LICENSE](LICENSE) 文件

---

**Happy Coding! 🚀**