# Native/系统编程项目分析

分析C/C++、Rust、Go等系统编程项目。

## 适用类型

- `cmake` - CMake项目
- `makefile` - Makefile项目
- `rust` - Rust项目
- `go` - Go项目
- `meson` - Meson项目
- `bazel` - Bazel项目

## 执行步骤

### 1. 解析构建配置

#### CMake
调用解析器：
```bash
python3 ~/.claude/tools/init/parsers/cmake_parser.py "$TARGET_DIR"
```

提取：
- 项目名称和版本
- 依赖 (find_package, FetchContent)
- 编译选项
- 目标 (add_executable, add_library)

#### Makefile
解析Makefile:
- 目标列表
- 编译器和标志
- 源文件

#### Rust (Cargo.toml)
解析Cargo.toml:
- 项目名称和版本
- dependencies
- features

#### Go (go.mod)
解析go.mod:
- 模块名称
- Go版本
- require依赖

### 2. 分析项目结构

```
project/
├── src/          # 源代码
├── include/      # 头文件 (C/C++)
├── lib/          # 库代码
├── tests/        # 测试
├── examples/     # 示例
├── docs/         # 文档
└── cmake/        # CMake模块
```

### 3. 识别依赖

C/C++:
- OpenSSL, zlib, curl
- Boost, Qt
- Google Test, Catch2

Rust:
- serde, tokio, actix-web
- clap, anyhow

Go:
- gin, echo, fiber
- gorm, sqlx

### 4. 分析模块

扫描源码目录，按功能分类：
- core/ - 核心逻辑
- utils/ - 工具函数
- net/ - 网络模块
- io/ - 输入输出
- parser/ - 解析器

### 5. 生成文档

## 输出格式

```
项目初始化完成！

项目名称: {name}
项目类型: 系统库/应用
主要语言: {C++/Rust/Go}
构建系统: {CMake/Cargo/go build}

依赖:
  - {dep1}: {purpose}
  - {dep2}: {purpose}

模块统计:
  - 核心模块: {count} 个
  - 测试文件: {count} 个

核心功能: {count} 项

已生成项目文档: .claude/project.md
```