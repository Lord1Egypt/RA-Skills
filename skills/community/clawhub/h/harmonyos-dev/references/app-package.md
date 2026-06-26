# 应用程序包结构

> 来源：华为开发者文档 - 应用程序包概述（2026-04-20）
> https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/application-package-overview

## 核心概念

- **应用（Application）**：运行在设备上提供特定服务的程序
- **应用程序包**：应用对应的软件包文件（HAP/HAR/HSP）

## Module 类型

### HAP（HarmonyOS Ability Package）
可安装的应用单元，分两种：
- **Entry**：主入口 module，可独立安装
- **Feature**：特性 module，依赖 Entry 存在

### HAR（HarmonyOS Archive）
静态共享库，编译时打包进 HAP。不支持声明 pages 页面（需用 Navigation 跳转）。

### HSP（HarmonyOS Shared Package）
动态共享库，运行时被多个 HAP 共享。相比 HAR 的优势在于编译产物可多 HAP 间复用。

## 三者对比

| 特性 | HAP | HAR | HSP |
|------|-----|-----|-----|
| 可安装 | ✅ | ❌ | ❌ |
| 编译时打包 | — | ✅ | ❌（运行时加载）|
| 应用内共享 | ✅ | ✅ | ✅ |
| 跨应用共享 | ❌ | ✅ | ❌ |
| 支持循环依赖 | ❌ | ❌ | ❌ |

## 包结构

```
entry/
├── src/main/
│   ├── ets/              # ArkTS/TS 源码
│   │   ├── entryability/ # EntryAbility
│   │   └── pages/        # 页面
│   ├── module.json5       # Stage 配置
│   └── resources/        # 应用资源
└── build-profile.json5
```

## Stage 模型配置文件

`module.json5` 关键字段：
```json
{
  "module": {
    "name": "entry",
    "type": "entry",
    "srcEntry": "./ets/entryability/EntryAbility.ts",
    "deviceTypes": ["phone", "tablet"],
    "deliveryWithInstall": true,
    "pages": "$profile:main_pages",
    "abilities": [
      {
        "name": "EntryAbility",
        "srcEntry": "./ets/entryability/EntryAbility.ts",
        "description": "$string:EntryAbility_desc",
        "icon": "$media:icon",
        "label": "$string:EntryAbility_label",
        "startWindowIcon": "$media:icon",
        "startWindowBackground": "$color:start_window_background"
      }
    ]
  }
}
```

## 依赖配置

在 `oh-package.json5` 中声明：
```json
{
  "dependencies": {
    "library": "file:../library"
  }
}
```
