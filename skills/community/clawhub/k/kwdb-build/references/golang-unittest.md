# Go 单元测试

## 启用条件

用户请求 "golang 单元测试"、"Go 单元测试"、"run golang test" 或类似请求时触发。

## 执行前确认

执行 Go 单元测试前，必须向用户确认以下信息，不得跳过。

### 1. 源码目录确认
- 源码目录：必须由用户指定
- 构建目录：默认 `{源码目录}/build`
**自动检测开源版/企业版：**
当路径验证通过后，自动检测 `kwbase/Makefile_ent` 是否存在：
- 若存在 → 企业版（无条件编译企业版），设置 `-DKWBASE_OSS=OFF`
- 若不存在（仅有 `kwbase/Makefile`） → 开源版，设置 `-DKWBASE_OSS=ON`

### 2. 构建类型确认
请选择构建类型（默认 RelWithDebInfo）：
- Debug - 调试版本
- Release - 发布版本（优化后的发布版本）
- RelWithDebInfo - 发布版本带调试信息（默认）

### 3. GOPATH 确认
- 必须验证 `GOPATH` 环境变量已设置
- 若未设置，提示用户输入

### 4. 路径验证（强制要求）
验证源码目录是否在 `${GOPATH}/src/gitee.com/kwbasedb` 路径下：
- 若不满足，提示用户并**直接退出**

### 5. Clean 规则（当存在 build 目录时必须执行）
当源码目录存在 `build` 目录时，必须先执行以下 Clean 规则清理，再开始构建：

```bash
rm -rf build*
rm -rf log/
rm -rf install/
rm -rf kwbase/.buildinfo
rm -rf kwbase/bin
rm -rf kwbase/build/defs.mk kwbase/build/defs.mk.sig
rm -rf qa/TEST_integration
rm -rf kwbase/ui/yarn.installed
rm -rf ${GOPATH}/native
rm -rf kwdbts2/roachpb/*.cc kwdbts2/roachpb/*.h
cd kwbase && GOPATH=${GOPATH} make clean -f Makefile_ent
```

## 执行流程

**严格按以下顺序执行：配置 -> 编译 libcommon 和 libkwdbts2 -> 执行单元测试**

### 第一步：配置
```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE={构建类型} -DBUILD_KWBASE=OFF
```

### 第二步：编译 libcommon 和 libkwdbts2
```bash
cmake --build build -j4
```

### 第三步：执行单元测试
**执行脚本**
- **调用位于 `scripts/run_golang_test.sh` 的脚本**
- **参数传递：将用户提供的源码目录作为参数传递给脚本**
- **命令示例：**
```bash
bash scripts/run_golang_test.sh {源码目录}
```

## CMake 选项限制

必须且只能使用 `references/cmake-options.md` 中定义的 CMake 选项，不得添加自定义选项。

## 注意事项

- Go 单元测试依赖 libkwdbts2 和 libcommon，必须先完成编译
- 编译失败时只分析原因，不自动修复
- 测试失败时只报告结果，不自动修复
- 测试超时时间默认 45 分钟
