# Android项目分析

分析Android应用项目，生成项目文档。

## 适用类型

- `android-app` - 标准Android应用
- 项目包含 `AndroidManifest.xml` 或 `build.gradle` + `app/src/main`

## 执行步骤

### 1. 解析AndroidManifest.xml

调用解析工具：
```bash
python3 ~/.claude/tools/init/parsers/manifest_parser.py "$TARGET_DIR"
```

提取信息：
- packageName (应用ID)
- 权限列表
- 四大组件
- minSdkVersion, targetSdkVersion

### 2. 解析Gradle配置

调用解析工具：
```bash
python3 ~/.claude/tools/init/parsers/gradle_parser.py "$TARGET_DIR"
```

提取信息：
- 依赖列表 (implementation, api, compileOnly)
- 构建变体 (buildTypes, productFlavors)
- SDK版本配置
- 插件配置

### 3. 分析项目结构

扫描目录：
```
app/src/main/
├── java/           # Java源码
├── kotlin/         # Kotlin源码
├── res/            # 资源文件
│   ├── layout/    # 布局
│   ├── drawable/  # 图片
│   ├── values/    # 字符串、颜色等
│   └── xml/       # XML配置
├── assets/         # 资产文件
├── jniLibs/        # Native库
└── AndroidManifest.xml
```

### 4. 识别架构模式

检测特征文件：
- `*ViewModel.kt/java` → MVVM
- `*Presenter.kt/java` → MVP
- `*UseCase.kt/java` → Clean Architecture
- `*Repository.kt/java` → Repository模式
- `@Hilt`, `@Inject` → 依赖注入

### 5. 识别Jetpack组件

检查导入：
- `androidx.lifecycle.*` → ViewModel/LiveData
- `androidx.room.*` → Room数据库
- `androidx.work.*` → WorkManager
- `androidx.navigation.*` → Navigation
- `androidx.compose.*` → Jetpack Compose
- `kotlinx.coroutines.*` → Coroutines

### 6. 生成文档

使用模板：`~/.claude/commands/init/templates/project-template.md`

输出到：`$TARGET_DIR/.claude/project.md`

## 输出格式

```
项目初始化完成！

项目名称: {name}
项目类型: Android应用
主要语言: Kotlin/Java
构建系统: Gradle
目标平台: Android {minSdk}+

模块统计:
  - 核心模块: {count} 个
  - 测试文件: {count} 个

Jetpack组件:
  - {components}

核心功能: {count} 项
  1. {feature1}
  2. {feature2}

已生成项目文档: .claude/project.md
```