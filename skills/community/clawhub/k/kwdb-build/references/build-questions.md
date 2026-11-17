# KaiwuDB 构建配置确认

**执行任何构建相关操作前，必须向用户确认以下信息，不得跳过。**

## 构建前检查

**强制要求：严格按 配置 -> 编译 -> 安装(可选) 流程执行。**

### CMake 选项限制
必须使用 `references/cmake-options.md` 中定义的 CMake 选项，不得添加自定义选项。

### 构建目录检查
当源码目录存在 `build` 目录时，必须先执行以下 Clean 规则清理，再开始新的构建：

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

此检查在 GOPATH 和源码目录验证通过后、配置 CMake 之前执行。

## 确认项

### 1. 构建类型
请选择构建类型（默认 RelWithDebInfo）：
- Debug - 调试版本
- Release - 发布版本（优化后的发布版本）
- RelWithDebInfo - 发布版本带调试信息（默认）

### 2. kwbase 二进制
是否编译 kwbase 二进制？（默认是）

### 3. AddressSanitizer
是否开启 AddressSanitizer（内存分析）？（默认否）

### 4. GOPATH 与源码目录

**第一步：GOPATH 检测与设置**
1. 检测当前 `GOPATH` 环境变量是否已设置
2. 若 `GOPATH` 为空，提示用户输入 `GOPATH`
3. 设置 `export GOPATH=<用户输入的值>`

**第二步：源码目录验证**
- 源码目录：必须由用户指定
- 构建目录：默认 `{源码目录}/build`

**路径验证（强制要求）：**
验证源码目录是否在 `${GOPATH}/src/gitee.com/kwbasedb` 路径下：
- 若不满足，提示用户并**直接退出**

**自动检测开源版/企业版：**
当路径验证通过后，自动检测 `kwbase/Makefile_ent` 是否存在：
- 若存在 → 企业版（无条件编译企业版），设置 `-DKWBASE_OSS=OFF`
- 若不存在（仅有 `kwbase/Makefile`） → 开源版，设置 `-DKWBASE_OSS=ON`

### 5. 安装目录(仅当编译 kwbase 二进制时需要)
制品安装目录：默认 `{源码目录}/install`
