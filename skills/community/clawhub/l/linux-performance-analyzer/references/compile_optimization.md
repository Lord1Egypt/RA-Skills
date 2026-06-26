# 编译优化参考

## 目录
1. [何时应该进行编译优化](#1-何时应该进行编译优化)
2. [GCC 优化选项速查](#2-gcc-优化选项速查)
3. [Clang 优化选项](#3-clang-优化选项)
4. [PGO（性能引导优化）](#4-pgo性能引导优化)
5. [LTO（链接时优化）](#5-lto链接时优化)
6. [SIMD 向量化](#6-simd-向量化)
7. [典型场景编译命令](#7-典型场景编译命令)
8. [编译优化效果验证](#8-编译优化效果验证)

---

## 1. 何时应该进行编译优化

**适合场景：**
- CPU 密集型计算（数值计算、图像处理、加解密、压缩）
- 发现 perf/gprof 热点函数集中在自行编译的代码中
- 性能测试证明有 20%+ 的 CPU 时间消耗在用户态代码
- 当前编译选项为 `-O0` 或 `-O1`（未充分优化）

**不适合场景：**
- 瓶颈在 I/O、网络或内存带宽（编译优化无效）
- 代码逻辑存在严重算法问题（优化架构比编译优化更有效）
- 第三方闭源库（无源码无法重新编译）

---

## 2. GCC 优化选项速查

### 优化等级

| 选项 | 效果 | 适用场景 |
|------|------|---------|
| `-O0` | 不优化，调试友好 | 开发阶段 |
| `-O1` | 基础优化 | 快速构建 |
| `-O2` | 常规优化（**推荐默认**） | 大多数生产场景 |
| `-O3` | 激进优化（含向量化） | CPU 密集计算 |
| `-Os` | 优化代码大小 | 嵌入式/缓存敏感 |
| `-Ofast` | `-O3` + 宽松浮点（不符合 IEEE 754） | 数值计算且不需要精确浮点 |

### 针对目标架构优化

```bash
# 编译为适合当前机器架构的代码（最大化利用 CPU 指令集）
gcc -O2 -march=native -mtune=native -o output input.c

# 指定特定架构（跨平台编译时）
gcc -O2 -march=x86-64-v3 -o output input.c   # x86-64-v3 = AVX2 支持

# 查看当前 CPU 支持的特性
gcc -march=native -Q --help=target | grep -E "enabled|march"

# 开启内联优化（减少函数调用开销）
gcc -O2 -finline-functions -finline-limit=200 input.c
```

### 调试信息与优化兼容（gdb 调试优化代码）

```bash
# 生产环境：保留调试信息但不影响性能
gcc -O2 -g3 -fno-omit-frame-pointer -o output input.c
# -fno-omit-frame-pointer：保留帧指针，方便 perf/gdb 堆栈回溯
```

---

## 3. Clang 优化选项

```bash
# Clang 基本用法与 GCC 类似
clang -O2 -march=native -o output input.c

# Clang 特有：自动向量化报告
clang -O2 -Rpass=loop-vectorize -Rpass-missed=loop-vectorize input.c

# Clang 生成 LLVM 中间代码（用于 LTO）
clang -O2 -flto input.c -o output

# Clang 地址/内存 sanitizer（找 bug）
clang -O1 -fsanitize=address,undefined -g input.c    # AddressSanitizer
clang -O1 -fsanitize=thread -g input.c               # ThreadSanitizer
```

---

## 4. PGO（性能引导优化）

**原理**：先用真实负载运行程序生成性能数据，再用此数据指导编译器做更精准的优化（分支预测、内联决策等）。

**效果**：通常比普通 `-O2` 提升 10-20% 性能。

```bash
# === GCC PGO 三步流程 ===

# 第一步：插桩编译（instrumented build）
gcc -O2 -fprofile-generate -o app_pgo input.c

# 第二步：用真实工作负载运行（生成 .gcda 文件）
./app_pgo --run-benchmark
# 运行后会生成 input.gcda 文件

# 第三步：使用 profile 数据重新编译
gcc -O2 -fprofile-use -fprofile-correction -o app_final input.c

# === Clang PGO 三步流程 ===

# 第一步：插桩编译
clang -O2 -fprofile-instr-generate -o app_pgo input.c

# 第二步：运行生成 .profraw 文件
./app_pgo
LLVM_PROFILE_FILE="default.profraw" ./app_pgo

# 将 profraw 合并为 profdata
llvm-profdata merge -output=default.profdata *.profraw

# 第三步：使用 profdata 重新编译
clang -O2 -fprofile-instr-use=default.profdata -o app_final input.c
```

---

## 5. LTO（链接时优化）

**原理**：在链接阶段跨模块进行优化（内联跨文件函数、删除未使用代码）。

```bash
# GCC ThinLTO（推荐，速度快）
gcc -O2 -flto=thin input1.c input2.c -o output

# GCC 全量 LTO（优化更彻底，但编译慢）
gcc -O2 -flto -fuse-linker-plugin input1.c input2.c -o output

# Clang ThinLTO（强烈推荐，与 PGO 组合效果最佳）
clang -O2 -flto=thin input1.c input2.c -o output

# CMake 项目开启 LTO
# 在 CMakeLists.txt 中：
# set_property(TARGET myapp PROPERTY INTERPROCEDURAL_OPTIMIZATION TRUE)
```

---

## 6. SIMD 向量化

```bash
# 查看 CPU 支持的 SIMD 指令集
cat /proc/cpuinfo | grep -m1 flags | tr ' ' '\n' | grep -E "sse|avx|avx512"

# GCC 自动向量化（-O3 已包含）
gcc -O3 -ftree-vectorize -fopt-info-vec-optimized input.c

# 指定 AVX2 指令集
gcc -O2 -mavx2 -mfma input.c

# 指定 AVX-512（Skylake-SP 以后的 Intel）
gcc -O2 -mavx512f -mavx512dq input.c

# 查看向量化是否生效（查看汇编中是否有 ymm/zmm 寄存器）
gcc -O3 -march=native -S -o output.s input.c
grep -E "ymm|zmm|xmm" output.s | head -10

# ⚠️ AVX-512 在某些 CPU 上会降低频率（thermal throttling），测试确认效果
```

---

## 7. 典型场景编译命令

```bash
# 场景1：通用服务端 C/C++ 应用（稳定性优先）
gcc -O2 -g3 -fno-omit-frame-pointer -march=x86-64-v2 \
    -D_FORTIFY_SOURCE=2 -fstack-protector-strong \
    -Wl,-z,relro,-z,now \
    -o app src/*.c

# 场景2：高性能计算（极致 CPU 性能）
gcc -O3 -march=native -mtune=native \
    -fno-omit-frame-pointer \
    -ftree-vectorize -funroll-loops \
    -flto=thin \
    -o app src/*.c

# 场景3：PGO + LTO 组合（最优生产配置）
# 步骤1
gcc -O2 -fprofile-generate -march=native -o app_train src/*.c
./app_train --benchmark   # 跑真实负载
# 步骤2
gcc -O2 -fprofile-use -flto=thin -march=native \
    -fno-omit-frame-pointer \
    -o app_final src/*.c

# 场景4：Python 扩展模块（.so）
python3 setup.py build_ext --inplace \
    --extra-compile-args="-O3 -march=native -ffast-math"

# 场景5：Rust 发布构建（cargo）
RUSTFLAGS="-C target-cpu=native -C lto=thin" cargo build --release
```

---

## 8. 编译优化效果验证

```bash
# 验证方法1：perf stat 对比 CPU 指令数
perf stat ./app_O0   # 记录 instructions, cycles, IPC
perf stat ./app_O3   # 对比 IPC 是否提升

# 验证方法2：time 命令对比
time ./app_O0
time ./app_O3

# 验证方法3：查看二进制中的指令集使用
objdump -d app_O3 | grep -c "vmovaps\|vaddps\|ymm"   # AVX 指令数量

# 验证方法4：查看实际使用的优化 flags
gcc -Q -O2 --help=optimizers 2>/dev/null | grep enabled

# 检查是否有意外的性能回退
# 特别注意 -Ofast / 浮点优化可能导致数值结果不一致
./app_O0 > output_O0.txt
./app_Ofast > output_Ofast.txt
diff output_O0.txt output_Ofast.txt   # 确认结果一致
```