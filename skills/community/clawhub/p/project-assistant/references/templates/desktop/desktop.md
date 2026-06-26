# 桌面应用项目分析

分析Qt、Electron、Flutter桌面等桌面应用项目。

## 适用类型

- `qt` - Qt应用 (C++/PyQt/PySide)
- `electron` - Electron应用
- `flutter` - Flutter桌面应用
- `tauri` - Tauri应用

## 执行步骤

### 1. Qt项目

检查文件：
- `*.pro` - qmake项目
- `CMakeLists.txt` + Qt - CMake项目

提取：
- Qt模块 (widgets, network, sql等)
- 源文件和头文件

### 2. Electron项目

解析 `package.json`:
- electron版本
- 主进程入口
- 渲染进程框架

### 3. Flutter桌面

解析 `pubspec.yaml`:
- Flutter版本
- 依赖包
- 支持平台

## 输出格式

```
项目初始化完成！

项目名称: {name}
项目类型: 桌面应用
主要语言: {C++/JS/Dart}
框架: {Qt/Electron/Flutter}
支持平台: Windows/macOS/Linux

已生成项目文档: .claude/project.md
```