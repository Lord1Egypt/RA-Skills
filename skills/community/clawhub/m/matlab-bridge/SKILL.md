---
name: matlab-bridge
description: "MATLAB桥接技能，用于调用MATLAB进行仿真计算、数据分析和绘图。支持直接执行MATLAB代码、运行.m脚本、数据交互。适用于结构试验数据处理、振动分析、有限元后处理等场景。"
metadata:
  {
    "openclaw": { "emoji": "📊" }
  }
---

# MATLAB 桥接技能

让 SuperMike 直接调用 MATLAB 进行科研计算、数据分析和可视化。

## 功能特性

- ✅ **直接执行 MATLAB 代码** - 无需写.m文件，一行命令搞定
- ✅ **运行现有脚本** - 调用你已有的 .m 文件
- ✅ **数据交互** - Python ↔ MATLAB 双向数据传递
- ✅ **自动绘图** - 生成论文-quality图表，保存高清图片
- ✅ **批量处理** - 循环处理多个数据文件

## 适用场景

- 📈 **试验数据处理** - 振动台试验数据分析、滤波、频谱分析
- 📊 **科学绘图** - 生成SCI论文用图（MATLAB的图质量高）
- 🔢 **数值计算** - 矩阵运算、优化求解、微分方程
- 🌊 **信号处理** - FFT、小波分析、滤波器设计
- 🏗️ **结构分析** - 模态分析、响应谱计算、有限元后处理

## 配置要求

### 1. MATLAB 安装确认

确保 MATLAB 已安装并添加到系统 PATH：

```powershell
# 检查 MATLAB 是否可用
matlab -batch "disp('Hello from MATLAB')"
```

如果提示找不到命令，需要添加 MATLAB 到 PATH：
```powershell
# 示例路径，根据实际安装位置调整
$env:PATH += ";C:\Program Files\MATLAB\R2023b\bin"
```

### 2. Python 依赖（可选）

如果使用 Python Engine 方式，需要安装：
```bash
cd "C:\Program Files\MATLAB\R2023b\extern\engines\python"
python setup.py install
```

**推荐使用命令行方式，无需额外配置。**

## 使用方法

### 方式一：直接执行代码（推荐）

告诉 SuperMike：
> "用MATLAB画一个正弦波，保存为图片"

> "MATLAB计算：生成100个点的正弦信号，做FFT分析"

### 方式二：运行已有脚本

> "运行MATLAB脚本：analyze_vibration_data.m"

> "MATLAB执行：process_data.m，传入参数datafile.csv"

### 方式三：数据处理流水线

> "用MATLAB读取CSV数据，滤波，画图，保存结果"

## 支持的MATLAB操作

### 基础计算
- 矩阵运算、线性代数
- 数值积分、微分方程求解
- 优化问题求解

### 信号处理
- FFT、IFFT
- 滤波器设计（低通、高通、带通）
- 频谱分析、功率谱密度
- 小波变换

### 数据可视化
- 2D/3D 绘图
- 子图布局
- 自定义样式（字体、颜色、线型）
- 导出高清图片（300/600 dpi）

### 文件操作
- 读写 CSV、Excel、MAT 文件
- 批量处理多个文件
- 数据格式转换

### 结构工程专用
- 响应谱计算
- 模态分析
- 地震波处理
- 时程分析

## 输出与保存

所有生成的图表和数据默认保存到：
```
D:\Personal\OpenClaw\matlab-outputs\
```

包含：
- `.png` / `.eps` / `.pdf` - 图片文件
- `.mat` - MATLAB数据文件
- `.csv` - 导出数据表格

## 🔧 快速测试

验证 MATLAB 环境配置和基本功能：

```bash
cd skills/matlab-bridge
python test_matlab.py
```

**测试内容：**
1. MATLAB 命令是否可用
2. 许可证状态
3. 基本矩阵运算
4. 绘图功能
5. FFT信号处理

**输出示例：**
```
============================================================
MATLAB Bridge 环境测试
============================================================

1. MATLAB 命令检查
   状态: ✓ MATLAB 命令可用
   版本: 23.2.0.XXXXXXX (R2023b)

2. 许可证检查
   状态: ✓ 许可证有效

3. 基本计算测试
   状态: ✓ 矩阵运算正常
   测试: Matrix multiplication result size: 3x3

4. 绘图功能测试
   状态: ✓ 绘图功能正常
   输出: D:\Personal\OpenClaw\matlab-outputs\test_plot.png
   大小: 45.2 KB

5. 信号处理测试
   状态: ✓ FFT分析正常
   测试: Dominant frequency: 10 Hz (expected: 10 Hz)

============================================================
测试结果汇总
============================================================

通过: 5/5

详细结果:
  MATLAB 命令:   ✓
  许可证状态:     ✓
  基本计算:       ✓
  绘图功能:       ✓
  信号处理:       ✓

✓ 所有测试通过！MATLAB Bridge 技能已就绪
```

---

## 故障排除

### "MATLAB 命令未找到"
- 检查 MATLAB 是否添加到系统 PATH
- 确认 MATLAB 版本路径正确

### "License 错误"
- 确保 MATLAB 许可证有效
- 检查网络连接（网络许可证）

### "内存不足"
- 减少数据量
- 分批处理大数据

### "图形窗口无法显示"
- 使用 `-nodisplay` 模式（无GUI）
- 直接保存图片，不显示窗口

---

_技能版本: v1.0_
_创建日期: 2026-02-28_
_作者: SuperMike_
_适配MATLAB版本: R2020b及以上_
