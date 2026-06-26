# Grafana 自动化巡检工具

一个强大的 Grafana 自动化巡检工具，支持浏览器截图 + API 数据巡检，多仪表盘批量巡检，自动发现仪表盘。

## ✨ 特性

- 🔍 **多模式巡检**: 支持浏览器截图和 API 数据双重巡检
- 📊 **批量处理**: 自动发现和批量巡检多个仪表盘
- 📸 **可视化报告**: 生成包含仪表盘截图的完整报告
- 🎯 **智能发现**: 自动发现可用的仪表盘
- ⚡ **高性能**: 并发处理多个巡检任务

## 📦 构建 ClawHub 技能包

在项目根目录执行：

```powershell
./build.ps1
```

默认会在 `dist/` 下生成：

- `grafana-inspector-YYYYMMDD-HHmmss.zip`

可选参数：

```powershell
./build.ps1 -OutputDir dist -Version 1.0.0
```

打包内容包含：

- `README.md`
- `SKILL.md`
- `assets/`（若存在）
- `scripts/api_inspect.py`
- `scripts/main.py`
- `scripts/config.example.json`

不会打包本地配置与缓存（如 `scripts/config.json`、`scripts/__pycache__/`、`reports/`）。