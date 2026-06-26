# MATLAB Bridge 技能 - 快速开始

让 SuperMike 直接调用 MATLAB 进行科研计算。

## 1. 安装检查

确保 MATLAB 可用：
```powershell
# 在PowerShell中测试
matlab -batch "disp('Hello MATLAB')"
```

如果提示找不到命令，添加 MATLAB 到 PATH：
```powershell
# 临时添加（当前会话有效）
$env:PATH += ";C:\Program Files\MATLAB\R2023b\bin"

# 永久添加（推荐）
[Environment]::SetEnvironmentVariable(
    "PATH", 
    $env:PATH + ";C:\Program Files\MATLAB\R2023b\bin",
    "User"
)
```

## 2. 测试连接

```powershell
python skills/matlab-bridge/matlab_bridge.py --test
```

## 3. 使用方式

### 方式一：直接对 SuperMike 说（推荐）

> "用MATLAB画一个正弦波"

> "MATLAB做FFT分析，数据存在data.csv里"

> "MATLAB计算反应谱，加速度时程在acc.txt里，时间间隔0.02秒"

### 方式二：命令行执行

```powershell
# 直接执行代码
python skills/matlab-bridge/matlab_bridge.py --code "t=0:0.01:10; y=sin(t); plot(t,y);"

# 运行脚本
python skills/matlab-bridge/matlab_bridge.py --script "analyze_data.m"
```

### 方式三：Python调用

```python
from skills.matlab_bridge.matlab_bridge import matlab_exec, matlab_run

# 直接执行代码
result = matlab_exec("""
    t = 0:0.01:10;
    y = sin(t);
    plot(t, y);
    title('Sine Wave');
    saveas(gcf, 'sine.png');
""")

# 运行已有脚本
result = matlab_run("path/to/script.m", args={'param1': 10, 'param2': 'value'})
```

## 4. 输出目录

所有生成的图表和数据保存在：
```
D:\Personal\OpenClaw\matlab-outputs\
```

包含：
- `.png` - 图片（屏幕显示）
- `.pdf` - 矢量图（论文用）
- `.mat` - MATLAB工作区
- `_results.json` - 执行结果信息

## 5. 常用模板

```python
from skills.matlab_bridge.templates import quick_plot, quick_fft, quick_spectrum

# 快速绘图
code = quick_plot(y_data, t_data, "My Plot")

# FFT分析
code = quick_fft(signal_data, fs=100)

# 反应谱
code = quick_spectrum(acceleration_data, dt=0.02)
```

## 6. 故障排除

| 问题 | 解决方案 |
|------|---------|
| "MATLAB未找到" | 检查PATH配置，或手动指定matlab_path |
| "License错误" | 确保MATLAB许可证有效 |
| 执行超时 | 减少数据量，或增加timeout参数 |
| 中文乱码 | 确保.m文件保存为UTF-8编码 |

---

_祝计算愉快！_
