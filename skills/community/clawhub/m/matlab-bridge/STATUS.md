# MATLAB Bridge 技能创建完成

## 文件清单

| 文件 | 路径 | 说明 |
|------|------|------|
| 技能文档 | `skills/matlab-bridge/SKILL.md` | 完整使用说明 |
| 主脚本 | `skills/matlab-bridge/matlab_bridge.py` | MATLAB桥接核心类 |
| 模板库 | `skills/matlab-bridge/templates.py` | 常用MATLAB代码模板 |
| 快速执行 | `skills/matlab-bridge/matlab_quick.py` | 命令行快速调用 |
| 示例脚本 | `skills/matlab-bridge/examples/demo_signal_processing.m` | 信号处理示例 |
| 配置模板 | `skills/matlab-bridge/config.json.template` | 配置文件模板 |
| 快速开始 | `skills/matlab-bridge/README.md` | 5分钟上手 |

## 功能特性

- ✅ **直接执行MATLAB代码** - 一行命令搞定
- ✅ **运行.m脚本** - 调用已有脚本并传参
- ✅ **数据交互** - Python ↔ MATLAB 双向传递
- ✅ **自动绘图** - 生成论文quality高清图
- ✅ **常用模板** - FFT、反应谱、滤波、滞回曲线等

## 使用方式

### 1. 直接对 SuperMike 说
> "用MATLAB画一个正弦波"
> "MATLAB做FFT分析，数据在data.csv"
> "MATLAB计算反应谱，时间间隔0.02秒"

### 2. 命令行
```powershell
python skills/matlab-bridge/matlab_bridge.py --code "t=0:0.1:10; plot(t,sin(t));"
```

### 3. Python调用
```python
from skills.matlab_bridge.matlab_bridge import matlab_exec
result = matlab_exec("你的MATLAB代码")
```

## 输出目录
所有结果保存到：`D:\Personal\OpenClaw\matlab-outputs\`

---

## 配置检查（待完成）

MATLAB连接检测正在进行中...
如果未安装MATLAB或PATH未配置，需要：

1. 确认MATLAB已安装
2. 添加MATLAB到系统PATH：
```powershell
$env:PATH += ";C:\Program Files\MATLAB\R2023b\bin"
```

---

_创建时间: 2026-02-28_