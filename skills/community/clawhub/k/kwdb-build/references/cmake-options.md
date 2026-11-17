# KaiwuDB CMake 构建选项参考

本文档从 CMakeLists.txt 文件中提取的所有编译参数，按模块分类说明。

## 构建类型

| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `CMAKE_BUILD_TYPE` | 字符串 | Debug | 构建类型：Debug / Release / RelWithDebInfo |

## 构建组件

| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `BUILD_KWBASE` | BOOL | ON | 是否编译 kwbase 二进制 |
| `BUILD_SDK` | BOOL | OFF | 构建 SDK |
| `WITH_TESTS` | BOOL | OFF | 编译C++单元测试 |

## 功能开关

| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `KWBASE_OSS` | BOOL | ON | 决定编译开源版本(ON)或企业版(OFF) |
| `WITH_OPENSSL` | BOOL | OFF | 启用 OpenSSL 支持 |
| `WITH_GMSSL` | BOOL | OFF | 启用 GMSSL 支持 |
| `WITH_ASAN` | BOOL | OFF | 启用 AddressSanitizer 检查 |

## 内存池选项

| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `WITH_DEFINITION` | 字符串 | K_DEBUG | 内存池宏定义：K_DEBUG / K_RELEASE |
| `KMALLOC_DEBUGGER` | BOOL | OFF | 启用内存池分析 |

## 代码质量与发布

| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `K_DO_NOT_SHIP` | BOOL | OFF | 屏蔽不需要发布的代码 |
| `ENABLE_COVERAGE` | BOOL | OFF | 启用代码覆盖率检测 |
| `ENABLE_TRACING` | BOOL | OFF | 编译追踪插件 |
| `ENABLE_STATS` | BOOL | OFF | 启用关键方法性能统计 |
| `MULTI_CLIENT_BENCHMARK` | BOOL | OFF | 禁用 PubSubContext 复用 |

## 安装选项

| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `CMAKE_INSTALL_PREFIX` | 路径 | ./install | 安装目录前缀 |

## common 模块选项

| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `KMALLOC_PERFORMANCE_OPTIMIZATION` | BOOL | OFF | 启用内存池高性能模式（启用后不可使用 TRACE/LOG） |
| `ENABLE_LATCH_DEBUG` | BOOL | OFF | 启用 LATCH 调试 |

---

## kwdbts2 模块选项

| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `WITH_DEFINITION` | 字符串 | K_DEBUG | K_DEBUG / K_RELEASE |
| `K_DO_NOT_SHIP` | BOOL | OFF | 屏蔽不需要发布的代码 |
| `ENABLE_STATS` | BOOL | OFF | 编译时操作统计 |
| `WITH_ASAN` | BOOL | OFF | 启用 ASan 检查 |
| `ENABLE_COVERAGE` | BOOL | OFF | 启用代码覆盖率 |

---

## 预定义宏

编译时自动定义的宏：

| 宏 | 说明 |
|----|------|
| `K_DEBUG` / `K_RELEASE` | 内存池模式 |
| `KWBASE_OSS` | 开源版本标识 |
| `K_DO_NOT_SHIP` | 不发布代码标识 |
| `KMALLOC_DEBUGGER` | 内存池调试 |
| `THREAD_SAFE` | 线程安全 |
| `NEW_COUNT` | 新计数模式 |
| `PROJECT_VERSION` | 项目版本 |

---

## 构建示例

> 注意：以下示例中的 `<源码目录>` 和 `<构建目录>` 需要根据用户实际指定的值替换。

### Debug 构建（默认）
```bash
cmake -S <源码目录> -B <构建目录>
cmake --build <构建目录> -j 4
```

### Release 构建
```bash
cmake -S <源码目录> -B <构建目录> -DCMAKE_BUILD_TYPE=Release
cmake --build <构建目录> -j 4
```

### 带测试的 Debug 构建
```bash
cmake -S <源码目录> -B <构建目录> -DWITH_TESTS=ON
cmake --build <构建目录> -j 4
```

### 开源版构建
```bash
cmake -S <源码目录> -B <构建目录> -DKWBASE_OSS=ON
cmake --build <构建目录> -j 4
```

### 企业版构建
```bash
cmake -S <源码目录> -B <构建目录> -DKWBASE_OSS=OFF
cmake --build <构建目录> -j 4
```

### 启用覆盖率
```bash
cmake -S <源码目录> -B <构建目录> -DENABLE_COVERAGE=ON
cmake --build <构建目录> -j 4
```

### 指定安装目录
```bash
cmake -S <源码目录> -B <构建目录> -DCMAKE_INSTALL_PREFIX=/opt/kwdb
cmake --build <构建目录> -j 4
```

---

## 编译器版本要求

- **最低版本**：GCC/G++ 7.3
- **最高版本**：GCC/G++ 13.2
- **C++ 标准**：C++17
