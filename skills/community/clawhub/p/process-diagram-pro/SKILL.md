# Process Diagram Pro

**专业化工工艺图生成器** | Professional PFD/P&ID Diagram Generator

---

## 功能说明

本技能用于生成专业的化工工艺图，支持：

- ✅ **PFD 工艺流程图** (Process Flow Diagram)
- ✅ **P&ID 管道仪表流程图** (Piping & Instrumentation Diagram)
- ✅ **系统架构图** (System Architecture Diagram)
- ✅ **数据流图** (Data Flow Diagram)

适用行业：**化工/制药/食品/水处理**等过程工业

---

## 触发方式

在对话中直接描述需求即可，AI会自动调用本技能。

**触发示例**：
- "画一个PFD图"
- "生成P&ID图"
- "画化工工艺流程图"
- "生成数字孪生系统架构图"

---

## 核心特性

| 特性 | 说明 |
|------|------|
| 🌡️ 温度颜色渐变 | 设备颜色随温度变化（蓝→青→橙→红） |
| 🔤 中文支持 | 自动适配中文字体，无乱码 |
| 🎨 化工行业配色 | 符合行业标准的颜色体系 |
| ⚙️ 专业设备符号 | 储罐/反应器/阀门/仪表完整符号 |
| 🔗 控制回路 | 信号线连接控制回路展示 |

---

## 快速开始

### 生成 PFD 图

```
请生成一个顺酐加氢制丁二酸酐的PFD图，包含：
- 顺酐原料罐（T-101）
- 固定床反应器（R-01），温度140°C
- 气液分离器（V-01）
- 物料流连接
```

### 生成 P&ID 图

```
请生成一个P&ID图，包含：
- 反应器带温度控制回路（TIC-101）
- ESD紧急切断阀（XV-101, XV-102）
- 压力控制（PIC-101）
```

### 生成架构图

```
请生成数字孪生系统架构图，包含：
- 设备层：传感器、PLC
- 边缘计算层：ESP32、边缘代理
- 云平台层：MQTT、AI模型
- 应用层：HMI、报警系统
```

---

## API 参考

### 生成器类

| 类名 | 用途 | 主要方法 |
|------|------|---------|
| `PFDGenerator` | 工艺流程图 | `add_equipment()`, `add_flow()`, `save()` |
| `PIDGenerator` | 管道仪表图 | `add_equipment()`, `add_valve()`, `add_instrument()`, `add_signal()`, `add_esd_box()` |
| `ArchitectureGenerator` | 系统架构图 | `add_layer()`, `save()` |

### 设备类型

| type 值 | 类 | 说明 | 支持参数 |
|---------|-----|------|---------|
| `'tank'` | Tank | 储罐/原料罐 | name, tag, note |
| `'reactor'` | Reactor | 反应器（支持温度变色） | name, tag, temp, pressure, catalyst |
| `'heat_exchanger'` | HeatExchanger | 换热器/预热器/冷凝器 | name, tag, note |
| `'separator'` | Separator | 气液分离器 | name, tag, note |

### 阀门类型

| type 值 | 类 | 符号形状 | 说明 |
|---------|-----|---------|------|
| `'control'` | ControlValve | 风筝形 | 气动调节阀 |
| `'esd'` | ESDValve | 五边形（红色） | 紧急切断阀 |
| `'safety'` | SafetyValve | 半圆+三角 | 安全阀 |
| `'hand'` | HandValve | 菱形 | 手动阀 |
| `'check'` | CheckValve | 三角形 | 止回阀 |

### 仪表类型

| type 值 | 类 | 说明 | 典型用途 |
|---------|-----|------|---------|
| `'TIC'` | TIC | 温度指示控制器 | 温度控制回路 |
| `'PIC'` | PIC | 压力指示控制器 | 压力控制回路 |
| `'FIC'` | FIC | 流量指示控制器 | 流量控制回路 |
| `'TE'` | TE | 温度传感器 | 温度检测 |
| `'PE'` | PE | 压力传感器 | 压力检测 |
| `'FE'` | FE | 流量元件 | 流量测量 |
| `'PSH'` | PSH | 压力开关（高报） | 高压报警 |
| `'PSL'` | PSL | 压力开关（低报） | 低压报警 |
| `'AE'` | AE | 在线分析仪 | 成分分析 |

---

## 安装依赖

```bash
pip install matplotlib pillow numpy
```

---

## 常见问题

**Q: 中文显示为方块？**

A: 系统会自动搜索可用中文字体（思源黑体、苹方、微软雅黑等）。如仍有问题，请安装中文字体。

**Q: 能替代AutoCAD吗？**

A: 本工具生成专业级P&ID用于方案汇报和投标展示，不能完全替代工程软件。

**Q: 支持哪些行业？**

A: 化工/制药/食品/水处理完全支持，电力/能源/半导体部分支持。

---

## 使用指南

没有编程经验，使用过程中遇到错误怎么办？
把使用指南云文档链接发给AI，让它帮你排查和解决问题。

**使用指南云文档**：[使用指南飞书云文档链接](https://my.feishu.cn/wiki/XPOVwSB8CivVPkkdFBgcZaCunIf)

---

## Agent Browser 技能用法

本技能支持使用 `agent-browser` CLI 进行网页内容抓取和研究。

### 安装 agent-browser

```bash
npm install -g agent-browser
agent-browser install --with-deps
```

### 常用命令

```bash
# 打开网页
agent-browser open "https://my.feishu.cn/wiki/XPOVwSB8CivVPkkdFBgcZaCunIf"

# 获取页面快照（交互元素）
agent-browser snapshot -i

# 点击元素
agent-browser click @e1

# 填写表单
agent-browser fill @e1 "text"

# 截图
agent-browser screenshot /path/to/output.png

# 等待加载
agent-browser wait --load networkidle

# 获取文本
agent-browser get text body

# 关闭浏览器
agent-browser close
```

### 示例：研究 Matplotlib 教程

```bash
# 打开教程页面
agent-browser open "https://www.runoob.com/matplotlib/matplotlib-tutorial.html"

# 截图
agent-browser screenshot /tmp/tutorial.png

# 获取文本内容
agent-browser get text body

# 点击子章节
agent-browser click @e12  # Matplotlib Pyplot

# 等待加载后继续操作
agent-browser wait --load networkidle
agent-browser screenshot /tmp/pyplot.png
```

### 元素引用说明

`@e1`, `@e2` 等是元素引用ID，每次 `snapshot -i` 后会重新生成。
页面变化后（如点击链接）需要重新 `snapshot -i` 获取新的引用。

---

## 免责声明

**免责声明**：
本项目 99% 由 AI 自动生成，AI 所有者无任何编程背景。使用前请自行评估项目可行性。

---

## 参考

- [matplotlib](https://matplotlib.org/)
- [Pillow](https://pillow.readthedocs.io/)
- [P&ID设计规范](https://en.wikipedia.org/wiki/Piping_and_instrumentation_diagram)
- [agent-browser CLI](https://github.com/)
