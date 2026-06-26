# iOS项目分析

分析iOS/macOS/Apple平台项目。

## 适用类型

- `ios` - iOS应用
- `swift` - Swift项目
- 包含 `*.xcodeproj`, `Podfile`, `Package.swift`

## 执行步骤

### 1. 识别项目类型

检查特征文件：
- `*.xcodeproj` / `*.xcworkspace` → Xcode项目
- `Podfile` → CocoaPods依赖
- `Package.swift` → Swift Package Manager
- `Cartfile` → Carthage依赖

### 2. 分析项目结构

```
project/
├── App/
│   ├── AppDelegate.swift
│   └── Info.plist
├── Controllers/
├── Views/
├── Models/
├── ViewModels/
├── Services/
├── Resources/
│   ├── Assets.xcassets
│   └── *.storyboard
└── Tests/
```

### 3. 识别UI框架

- SwiftUI: `import SwiftUI`
- UIKit: `import UIKit`

### 4. 识别架构

- MVVM: 存在ViewModel
- MVC: 标准MVC
- Coordinator: 存在Coordinator

### 5. 分析依赖

常见库：
- Alamofire - 网络
- Kingfisher - 图片
- SnapKit - 布局
- RxSwift/Combine - 响应式

## 输出格式

```
项目初始化完成！

项目名称: {name}
项目类型: iOS应用
主要语言: Swift
构建系统: Xcode
目标平台: iOS {min_version}+

技术栈:
  - UI框架: {SwiftUI/UIKit}
  - 架构: {MVVM/MVC}
  - 依赖管理: {SPM/CocoaPods}

已生成项目文档: .claude/project.md
```