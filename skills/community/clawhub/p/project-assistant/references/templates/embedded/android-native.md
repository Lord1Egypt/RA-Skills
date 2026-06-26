# Android Native/AOSP项目分析

分析Android NDK项目和AOSP系统源码，生成项目文档。

## 适用类型

- `android-ndk` - Android NDK项目（C/C++原生开发）
- `aosp` - AOSP系统源码

## 执行步骤

### 1. 识别项目类型

检查特征文件：
- `Android.mk`, `Android.bp` → AOSP/NDK
- `Application.mk`, `CMakeLists.txt` + `jni/` → NDK
- `frameworks/`, `system/`, `hardware/` → AOSP

### 2. 解析构建配置

调用解析器：
```bash
# NDK CMake
python3 ~/.claude/tools/init/parsers/cmake_parser.py "$TARGET_DIR"

# Android Native解析器
python3 ~/.claude/tools/init/parsers/android_native_parser.py "$TARGET_DIR"
```

提取信息：
- 模块名称和类型（可执行文件、共享库、静态库）
- 源文件列表
- 依赖关系
- 编译标志

### 3. 分析项目结构

#### NDK项目典型结构：
```
project/
├── app/src/main/
│   ├── java/           # Java/Kotlin代码
│   ├── jni/            # Native代码
│   │   ├── Android.mk
│   │   ├── Application.mk
│   │   └── CMakeLists.txt
│   ├── jniLibs/        # 预编译库
│   └── cpp/            # C++源码
├── native/             # 独立Native模块
└── build.gradle
```

#### AOSP项目典型结构：
```
aosp/
├── frameworks/         # 框架层
│   ├── base/
│   ├── av/
│   └── native/
├── system/             # 系统服务
├── hardware/           # HAL层
│   ├── interfaces/
│   └── libhardware/
├── packages/           # 应用
│   ├── services/
│   └── apps/
├── vendor/             # 厂商定制
├── device/             # 设备配置
├── kernel/             # 内核源码
└── external/           # 第三方库
```

### 4. 分析模块依赖

对于AOSP项目：
- 解析 `Android.bp` / `Android.mk`
- 提取模块依赖关系
- 识别系统API使用

对于NDK项目：
- 解析 CMakeLists.txt
- 提取 native 库依赖
- 分析 JNI 接口

### 5. 识别技术特征

检查：
- STL类型（gnustl, libc++, stlport）
- NDK API版本
- 目构架构（arm, arm64, x86, x86_64）
- 是否使用 RenderScript / Vulkan / NNAPI

### 6. 生成文档

使用模板：`~/.claude/commands/init/templates/project-template.md`

输出到：`$TARGET_DIR/.claude/project.md`

## 输出格式

### NDK项目

```
项目初始化完成！

项目名称: {name}
项目类型: Android NDK项目
主要语言: C/C++
构建系统: CMake/ndk-build
目标平台: Android (minSdk: {minSdk})

Native模块:
  - {module1}: 共享库
  - {module2}: 可执行文件

ABI支持:
  - armeabi-v7a
  - arm64-v8a

依赖:
  - {native_lib1}
  - {native_lib2}

JNI接口: {count} 个

已生成项目文档: .claude/project.md
```

### AOSP项目

```
项目初始化完成！

项目名称: {name}
项目类型: AOSP系统源码
主要语言: Java/C++
构建系统: Soong (Android.bp)

目录结构:
  - frameworks/: 框架层模块
  - system/: 系统服务
  - hardware/: HAL层
  - packages/: 应用和服务

模块统计:
  - 总模块数: {count}
  - Java模块: {count}
  - Native模块: {count}

核心功能: {count} 项

已生成项目文档: .claude/project.md
```

## Android.bp 解析

示例 `Android.bp` 文件：

```json
cc_library_shared {
    name: "libexample",
    srcs: ["src/*.cpp"],
    shared_libs: [
        "libcutils",
        "liblog",
    ],
    cflags: ["-Wall", "-Werror"],
}
```

解析提取：
- `name`: 模块名称
- `srcs`: 源文件
- `shared_libs` / `static_libs`: 依赖
- `cflags`: 编译标志

## JNI 接口分析

扫描 native 方法声明：

```java
// Java层
public native String nativeProcess(byte[] data);
```

对应 C/C++ 实现：

```c
// Native层
JNIEXPORT jstring JNICALL
Java_com_example_ClassName_nativeProcess(JNIEnv* env, jobject thiz, jbyteArray data);
```

提取：
- JNI函数名称
- 参数类型
- 返回类型
- 调用关系

## 注意事项

1. **构建环境**
   - NDK项目需要正确配置 NDK 路径
   - AOSP项目需要完整源码树

2. **依赖管理**
   - 注意系统库和第三方库的区别
   - 记录 ABI 兼容性要求

3. **调试配置**
   - 记录 ndk-gdb 配置
   - 注意符号文件位置

4. **性能考虑**
   - AOSP项目规模大，分析时注意内存
   - 增量分析时只处理变更模块