# jetson-temp

NVIDIA Jetson 温度监控工具。实时监控系统温度。

## 功能

- CPU 温度监控
- GPU 温度监控  
- 多个 thermal zone 温度
- 实时更新

## 使用方法

```bash
# 查看当前温度
jetson-temp
```

## 依赖

- Linux thermal subsystem (/sys/class/thermal/)

## 环境要求

- NVIDIA Jetson 设备
- Linux kernel with thermal support
