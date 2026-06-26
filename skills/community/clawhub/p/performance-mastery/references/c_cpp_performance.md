# C/C++ 性能分析与优化指南

> C/C++ 作为系统级编程语言，直接操控硬件资源，拥有最丰富的性能分析工具链（perf、Valgrind、Sanitizers、Intel VTune）。本文档覆盖 C/C++ 性能分析工具链、编译优化、内存管理、并发优化及生产环境最佳实践。

---


## 目录

- [1. 性能分析工具链](#1-性能分析工具链)
- [2. 编译优化](#2-编译优化)
- [3. 内存管理优化](#3-内存管理优化)
- [4. 并发与多线程优化](#4-并发与多线程优化)
- [5. 常见性能陷阱与优化模式](#5-常见性能陷阱与优化模式)
- [6. I/O 优化](#6-io-优化)
- [7. 生产环境最佳实践](#7-生产环境最佳实践)
- [8. C++ 特有优化技巧](#8-c-特有优化技巧)
- [9. 调优工作流总结](#9-调优工作流总结)
## 1. 性能分析工具链

### 1.1 perf（Linux 首选 CPU 分析器）

```bash
# 编译时保留调试符号（不影响优化等级）
gcc -O2 -g -o myapp myapp.c
g++ -O2 -g -o myapp myapp.cpp

# CPU 采样（30秒）
perf record -g --call-graph dwarf -p <PID> -- sleep 30

# 查看热点函数
perf report --sort=dso,symbol

# 硬件计数器分析
perf stat -e cycles,instructions,cache-references,cache-misses,branch-misses,L1-dcache-load-misses -p <PID> -- sleep 10

# 生成火焰图
perf script | stackcollapse-perf.pl | flamegraph.pl > flamegraph.svg

# 按函数注解源码热点
perf annotate -s <symbol_name>
```

**perf 关键指标解读：**
| 指标 | 含义 | 异常阈值 |
|------|------|----------|
| IPC (instructions/cycle) | 每周期执行指令数 | < 1.0 说明流水线效率低 |
| cache-miss rate | 缓存未命中率 | > 5% 需优化数据布局 |
| branch-miss rate | 分支预测失败率 | > 3% 需优化分支逻辑 |
| L1-dcache-load-misses | L1 数据缓存未命中 | 高值说明数据局部性差 |

### 1.2 Valgrind 工具套件

```bash
# Callgrind — CPU 分析（精确但慢 20-50x）
valgrind --tool=callgrind --callgrind-out-file=callgrind.out ./myapp
kcachegrind callgrind.out  # GUI 分析

# Memcheck — 内存错误检测
valgrind --tool=memcheck --leak-check=full --show-leak-kinds=all --track-origins=yes ./myapp

# Massif — 堆内存分析
valgrind --tool=massif --pages-as-heap=yes ./myapp
ms_print massif.out.<PID>

# Cachegrind — 缓存模拟分析
valgrind --tool=cachegrind ./myapp
cg_annotate cachegrind.out.<PID>

# DHAT — 动态堆分析（Valgrind 3.18+）
valgrind --tool=dhat ./myapp
# 在浏览器打开 dhat-out 文件分析
```

**Valgrind 工具选择：**
| 工具 | 用途 | 开销 | 适用场景 |
|------|------|------|----------|
| Memcheck | 内存错误/泄漏 | 20-50x | 开发/CI 阶段必用 |
| Callgrind | 函数级 CPU 分析 | 20-50x | 精确定位热点函数 |
| Massif | 堆内存使用分析 | 10-20x | 内存占用过高 |
| Cachegrind | 缓存行为分析 | 20-50x | 缓存未命中率高 |
| DHAT | 堆分配模式分析 | 10x | 分配过频/短生命周期对象 |

### 1.3 Sanitizers（编译器内置，推荐）

```bash
# AddressSanitizer（ASan）— 内存错误检测（2x 开销，比 Valgrind 快 10 倍）
gcc -fsanitize=address -fno-omit-frame-pointer -g -O1 -o myapp myapp.c
# 或
clang -fsanitize=address -fno-omit-frame-pointer -g -O1 -o myapp myapp.c

# ASan 检测能力：
# - 堆缓冲区溢出（heap-buffer-overflow）
# - 栈缓冲区溢出（stack-buffer-overflow）
# - 全局缓冲区溢出（global-buffer-overflow）
# - use-after-free
# - use-after-return
# - double-free
# - 内存泄漏（leak）

# ThreadSanitizer（TSan）— 数据竞争检测
gcc -fsanitize=thread -g -O1 -o myapp myapp.c -lpthread

# UndefinedBehaviorSanitizer（UBSan）— 未定义行为检测
gcc -fsanitize=undefined -g -O1 -o myapp myapp.c

# MemorySanitizer（MSan）— 未初始化内存读取（仅 Clang）
clang -fsanitize=memory -fno-omit-frame-pointer -g -O1 -o myapp myapp.c

# 组合使用（ASan + UBSan）
gcc -fsanitize=address,undefined -fno-omit-frame-pointer -g -O1 -o myapp myapp.c
```

**Sanitizer 选择指南：**
| Sanitizer | 检测目标 | 运行时开销 | 编译器支持 |
|-----------|----------|------------|------------|
| ASan | 内存越界/UAF/泄漏 | 2x | GCC/Clang |
| TSan | 数据竞争 | 5-15x | GCC/Clang |
| UBSan | 未定义行为 | < 1.5x | GCC/Clang |
| MSan | 未初始化内存读 | 3x | 仅 Clang |

> ⚠️ ASan 与 TSan 不能同时使用；ASan 与 MSan 不能同时使用。

### 1.4 gperftools（Google Performance Tools）

```bash
# 安装
apt install google-perftools libgoogle-perftools-dev  # Debian/Ubuntu
yum install gperftools gperftools-devel                # CentOS/RHEL

# CPU Profiler
LD_PRELOAD=/usr/lib/libprofiler.so CPUPROFILE=cpu.prof ./myapp
google-pprof --text ./myapp cpu.prof          # 文本报告
google-pprof --svg ./myapp cpu.prof > cpu.svg # SVG 火焰图
google-pprof --web ./myapp cpu.prof           # 浏览器查看

# Heap Profiler
LD_PRELOAD=/usr/lib/libtcmalloc.so HEAPPROFILE=heap.prof ./myapp
google-pprof --text ./myapp heap.prof.0001.heap

# tcmalloc 替换 glibc malloc（性能提升显著）
LD_PRELOAD=/usr/lib/libtcmalloc_minimal.so ./myapp
```

### 1.5 Intel VTune / AMD uProf

```bash
# Intel VTune（性能分析黄金标准）
vtune -collect hotspots -result-dir=r001hs ./myapp
vtune -collect memory-access -result-dir=r001mem ./myapp
vtune -collect threading -result-dir=r001thr ./myapp

# AMD uProf
AMDuProfCLI collect --config tbp -o /tmp/prof ./myapp
AMDuProfCLI report -i /tmp/prof
```

---

## 2. 编译优化

### 2.1 GCC/Clang 优化等级

```bash
# 优化等级对比
-O0  # 无优化（调试用）
-O1  # 基础优化（编译快，适合开发）
-O2  # 推荐生产级优化（安全、稳定、效果好）
-O3  # 激进优化（循环向量化、函数内联更激进）
-Os  # 优化代码体积（嵌入式/缓存敏感场景）
-Ofast  # -O3 + 非标准浮点优化（-ffast-math），科学计算可用

# 推荐生产编译选项
gcc -O2 -march=native -flto -DNDEBUG -o myapp myapp.c

# 高性能场景
gcc -O3 -march=native -mtune=native -flto -funroll-loops \
    -fomit-frame-pointer -DNDEBUG -o myapp myapp.c
```

### 2.2 链接时优化（LTO）

```bash
# GCC LTO
gcc -O2 -flto -c module1.c -o module1.o
gcc -O2 -flto -c module2.c -o module2.o
gcc -O2 -flto module1.o module2.o -o myapp

# Clang ThinLTO（并行 LTO，大项目推荐）
clang -O2 -flto=thin -c module1.c -o module1.o
clang -O2 -flto=thin module1.o module2.o -o myapp

# CMake 启用 LTO
cmake -DCMAKE_INTERPROCEDURAL_OPTIMIZATION=ON ..
```

### 2.3 Profile-Guided Optimization (PGO)

```bash
# 第一步：编译插桩版本
gcc -O2 -fprofile-generate -o myapp_instrumented myapp.c

# 第二步：运行典型工作负载
./myapp_instrumented < typical_input.txt

# 第三步：使用 profile 数据重新编译
gcc -O2 -fprofile-use -o myapp_optimized myapp.c

# Clang PGO（使用 LLVM IR profiling）
clang -O2 -fprofile-instr-generate -o myapp_instr myapp.c
./myapp_instr < typical_input.txt
llvm-profdata merge -output=default.profdata default.profraw
clang -O2 -fprofile-instr-use=default.profdata -o myapp_opt myapp.c
```

> 💡 PGO 通常可带来 **10-30%** 的性能提升，特别适合分支密集型代码。

### 2.4 SIMD 向量化

```bash
# 自动向量化（GCC/Clang -O2 以上默认开启）
gcc -O2 -ftree-vectorize -fopt-info-vec-optimized myapp.c  # 查看向量化报告

# 手动指定 SIMD 指令集
gcc -O2 -mavx2 -mfma myapp.c        # AVX2 + FMA
gcc -O2 -mavx512f myapp.c           # AVX-512
gcc -O2 -march=native myapp.c       # 自动检测本机最佳指令集

# Clang 向量化报告
clang -O2 -Rpass=loop-vectorize -Rpass-missed=loop-vectorize myapp.c
```

**C/C++ SIMD 内建函数（Intrinsics）：**
```c
#include <immintrin.h>

// AVX2 示例：8 个 float 并行加法
void add_arrays_avx2(float* a, float* b, float* c, int n) {
    for (int i = 0; i < n; i += 8) {
        __m256 va = _mm256_loadu_ps(a + i);
        __m256 vb = _mm256_loadu_ps(b + i);
        __m256 vc = _mm256_add_ps(va, vb);
        _mm256_storeu_ps(c + i, vc);
    }
}
```

---

## 3. 内存管理优化

### 3.1 内存分配器选择

```bash
# glibc malloc（默认）
# 适合通用场景，但多线程下锁竞争严重

# tcmalloc（Google，推荐多线程场景）
LD_PRELOAD=/usr/lib/libtcmalloc.so ./myapp
# 线程本地缓存，减少锁竞争，碎片控制好

# jemalloc（Facebook，推荐长时间运行服务）
LD_PRELOAD=/usr/lib/libjemalloc.so ./myapp
# 碎片控制最优，支持 heap profiling
# 设置 jemalloc 分析
MALLOC_CONF="prof:true,prof_prefix:jeprof.out" LD_PRELOAD=/usr/lib/libjemalloc.so ./myapp
jeprof --svg ./myapp jeprof.out.*.heap > heap.svg

# mimalloc（Microsoft，高性能通用分配器）
LD_PRELOAD=/usr/lib/libmimalloc.so ./myapp
```

**分配器对比：**
| 分配器 | 多线程性能 | 碎片控制 | 诊断能力 | 适用场景 |
|--------|-----------|----------|----------|----------|
| glibc malloc | 一般 | 一般 | 弱 | 通用默认 |
| tcmalloc | 优秀 | 良好 | 强（heap prof） | 多线程服务 |
| jemalloc | 优秀 | 最优 | 强（heap prof） | 长运行服务（Redis/Nginx） |
| mimalloc | 最优 | 良好 | 中 | 高吞吐场景 |

### 3.2 内存池与对象池

```cpp
// 简单内存池（固定大小块）
class MemoryPool {
    struct Block { Block* next; };
    Block* free_list_ = nullptr;
    std::vector<void*> chunks_;
    size_t block_size_;
    size_t chunk_size_;

public:
    MemoryPool(size_t block_size, size_t chunk_blocks = 1024)
        : block_size_(std::max(block_size, sizeof(Block)))
        , chunk_size_(chunk_blocks) {
        grow();
    }

    void* allocate() {
        if (!free_list_) grow();
        Block* block = free_list_;
        free_list_ = block->next;
        return block;
    }

    void deallocate(void* ptr) {
        auto* block = static_cast<Block*>(ptr);
        block->next = free_list_;
        free_list_ = block;
    }

private:
    void grow() {
        char* chunk = new char[block_size_ * chunk_size_];
        chunks_.push_back(chunk);
        for (size_t i = 0; i < chunk_size_; ++i) {
            auto* block = reinterpret_cast<Block*>(chunk + i * block_size_);
            block->next = free_list_;
            free_list_ = block;
        }
    }
};
```

### 3.3 缓存友好的数据结构

```cpp
// ❌ AoS（Array of Structures）— 缓存不友好
struct Particle_AoS {
    float x, y, z;       // 位置
    float vx, vy, vz;    // 速度
    float mass;
    int type;
    // ... 更多字段
};
std::vector<Particle_AoS> particles; // 遍历位置时加载大量无用数据

// ✅ SoA（Structure of Arrays）— 缓存友好
struct Particles_SoA {
    std::vector<float> x, y, z;       // 位置连续存储
    std::vector<float> vx, vy, vz;    // 速度连续存储
    std::vector<float> mass;
    std::vector<int> type;
};
// 遍历位置时只加载 x/y/z，缓存命中率极高

// ✅ 热/冷数据分离
struct Entity_Hot {
    float x, y, z;     // 每帧都访问
    float health;
};
struct Entity_Cold {
    std::string name;   // 很少访问
    std::string model;
    int creation_time;
};
```

### 3.4 避免常见内存陷阱

```cpp
// ❌ 频繁 new/delete 小对象
for (int i = 0; i < 1000000; ++i) {
    auto* obj = new SmallObj();
    process(obj);
    delete obj;
}

// ✅ 预分配 + 对象复用
std::vector<SmallObj> pool(1000000);
for (auto& obj : pool) {
    process(&obj);
}

// ❌ std::map（红黑树，缓存不友好）
std::map<int, Value> m;

// ✅ 小规模用 sorted vector，大规模用 flat_map 或 robin_map
// boost::container::flat_map 或 absl::flat_hash_map
absl::flat_hash_map<int, Value> m;

// ❌ std::list（链表，缓存极不友好）
std::list<int> lst;

// ✅ std::vector（连续内存）
std::vector<int> vec;

// 内存对齐（避免 false sharing）
struct alignas(64) ThreadData {
    uint64_t counter;
    // padding 到 cache line 大小
};
```

---

## 4. 并发与多线程优化

### 4.1 锁优化

```cpp
// ❌ 粗粒度锁
std::mutex global_mutex;
void process(Data& data) {
    std::lock_guard<std::mutex> lock(global_mutex);
    // 所有操作都在锁内
}

// ✅ 细粒度锁 + 分段锁
static constexpr int NUM_SHARDS = 64;
struct Shard {
    std::mutex mutex;
    std::unordered_map<Key, Value> data;
} shards[NUM_SHARDS];

void process(const Key& key, const Value& val) {
    auto& shard = shards[hash(key) % NUM_SHARDS];
    std::lock_guard<std::mutex> lock(shard.mutex);
    shard.data[key] = val;
}

// ✅ 读写锁（读多写少场景）
std::shared_mutex rw_mutex;
Value read(const Key& key) {
    std::shared_lock lock(rw_mutex);  // 并发读
    return data[key];
}
void write(const Key& key, Value val) {
    std::unique_lock lock(rw_mutex);  // 独占写
    data[key] = std::move(val);
}

// ✅ 无锁数据结构（高竞争场景）
std::atomic<uint64_t> counter{0};
counter.fetch_add(1, std::memory_order_relaxed);
```

### 4.2 避免 False Sharing

```cpp
// ❌ False Sharing（不同线程修改同一缓存行的不同变量）
struct SharedData {
    uint64_t counter_a;  // 线程 A 修改
    uint64_t counter_b;  // 线程 B 修改 — 同一缓存行！
};

// ✅ 缓存行对齐
struct alignas(64) PaddedCounter {
    uint64_t value;
};
PaddedCounter counters[NUM_THREADS];

// C++17 hardware_destructive_interference_size
struct alignas(std::hardware_destructive_interference_size) Counter {
    std::atomic<uint64_t> value{0};
};
```

### 4.3 线程池模式

```cpp
// 高性能线程池（C++17）
#include <thread>
#include <queue>
#include <functional>
#include <condition_variable>

class ThreadPool {
    std::vector<std::thread> workers_;
    std::queue<std::function<void()>> tasks_;
    std::mutex mutex_;
    std::condition_variable cv_;
    bool stop_ = false;

public:
    ThreadPool(size_t threads = std::thread::hardware_concurrency()) {
        for (size_t i = 0; i < threads; ++i) {
            workers_.emplace_back([this] {
                while (true) {
                    std::function<void()> task;
                    {
                        std::unique_lock lock(mutex_);
                        cv_.wait(lock, [this] { return stop_ || !tasks_.empty(); });
                        if (stop_ && tasks_.empty()) return;
                        task = std::move(tasks_.front());
                        tasks_.pop();
                    }
                    task();
                }
            });
        }
    }

    template<class F>
    void submit(F&& f) {
        {
            std::lock_guard lock(mutex_);
            tasks_.emplace(std::forward<F>(f));
        }
        cv_.notify_one();
    }

    ~ThreadPool() {
        { std::lock_guard lock(mutex_); stop_ = true; }
        cv_.notify_all();
        for (auto& w : workers_) w.join();
    }
};
```

---

## 5. 常见性能陷阱与优化模式

### 5.1 字符串优化

```cpp
// ❌ 频繁字符串拼接
std::string result;
for (const auto& s : strings) {
    result += s;  // 每次可能重新分配
}

// ✅ 预留空间
std::string result;
size_t total = 0;
for (const auto& s : strings) total += s.size();
result.reserve(total);
for (const auto& s : strings) result += s;

// ✅ SSO（Small String Optimization）
// std::string 通常内联存储 <= 22 字节（GCC）或 <= 15 字节（Clang）的短字符串
// 短字符串无需堆分配

// ✅ std::string_view（C++17，零拷贝）
void process(std::string_view sv) {  // 不拷贝，不分配
    // ...
}
```

### 5.2 容器选择指南

| 场景 | 推荐容器 | 原因 |
|------|----------|------|
| 顺序访问/遍历 | `std::vector` | 连续内存，缓存友好 |
| 频繁尾部插入/删除 | `std::vector` / `std::deque` | 摊销 O(1) |
| 频繁中间插入/删除 | `std::list`（大元素）/ `std::vector`（小元素） | 小元素 vector 移动比 list 快 |
| 快速查找（有序） | `std::vector` + `std::lower_bound` | 缓存友好 |
| 快速查找（无序） | `absl::flat_hash_map` / `std::unordered_map` | O(1) 平均 |
| 优先队列 | `std::priority_queue` | 堆结构 |
| 小集合（< 100 元素） | `std::vector` + 线性搜索 | 缓存行效应优于树/哈希 |

### 5.3 移动语义与拷贝消除

```cpp
// ✅ 使用移动语义避免拷贝
std::vector<std::string> build_strings() {
    std::vector<std::string> result;
    result.reserve(1000);
    for (int i = 0; i < 1000; ++i) {
        result.emplace_back(std::to_string(i));  // 原地构造
    }
    return result;  // NRVO，零拷贝返回
}

// ✅ 完美转发
template<typename... Args>
void emplace(Args&&... args) {
    container.emplace_back(std::forward<Args>(args)...);
}

// ❌ 不必要的拷贝
void process(std::vector<int> data);    // 拷贝
// ✅
void process(const std::vector<int>& data);  // 只读引用
void process(std::vector<int>&& data);       // 移动
```

### 5.4 编译期计算（constexpr / 模板元编程）

```cpp
// ✅ constexpr 编译期计算（C++17/20）
constexpr uint64_t fibonacci(int n) {
    if (n <= 1) return n;
    uint64_t a = 0, b = 1;
    for (int i = 2; i <= n; ++i) {
        uint64_t c = a + b;
        a = b;
        b = c;
    }
    return b;
}
constexpr auto fib50 = fibonacci(50);  // 编译期计算，运行时零开销

// ✅ if constexpr（C++17，编译期分支消除）
template<typename T>
void serialize(const T& val) {
    if constexpr (std::is_arithmetic_v<T>) {
        write_binary(val);    // 数值类型：二进制写入
    } else if constexpr (std::is_same_v<T, std::string>) {
        write_string(val);    // 字符串：长度前缀 + 内容
    } else {
        val.serialize(*this); // 自定义类型：调用成员函数
    }
}
```

---

## 6. I/O 优化

### 6.1 文件 I/O

```cpp
// ❌ 逐字节/逐行读取
while (fgetc(fp) != EOF) { ... }

// ✅ 批量读取
constexpr size_t BUF_SIZE = 64 * 1024;  // 64KB 缓冲
char buffer[BUF_SIZE];
while (size_t n = fread(buffer, 1, BUF_SIZE, fp)) {
    process(buffer, n);
}

// ✅ mmap（大文件随机访问）
int fd = open("data.bin", O_RDONLY);
struct stat st;
fstat(fd, &st);
void* data = mmap(nullptr, st.st_size, PROT_READ, MAP_PRIVATE, fd, 0);
madvise(data, st.st_size, MADV_SEQUENTIAL);  // 提示内核预读
// ... 直接访问 data
munmap(data, st.st_size);
close(fd);

// ✅ io_uring（Linux 5.1+，异步 I/O 最佳方案）
// 使用 liburing 简化接口
#include <liburing.h>
struct io_uring ring;
io_uring_queue_init(256, &ring, 0);
// ... 提交读写请求
```

### 6.2 网络 I/O

```cpp
// ✅ epoll（Linux 高性能事件驱动）
int epfd = epoll_create1(0);
struct epoll_event ev, events[MAX_EVENTS];
ev.events = EPOLLIN | EPOLLET;  // 边缘触发
ev.data.fd = listen_fd;
epoll_ctl(epfd, EPOLL_CTL_ADD, listen_fd, &ev);

while (true) {
    int n = epoll_wait(epfd, events, MAX_EVENTS, -1);
    for (int i = 0; i < n; ++i) {
        if (events[i].data.fd == listen_fd) {
            accept_connection();
        } else {
            handle_data(events[i].data.fd);
        }
    }
}

// ✅ io_uring 网络（Linux 5.6+，性能优于 epoll）
// 零拷贝发送（sendmsg + MSG_ZEROCOPY）
setsockopt(fd, SOL_SOCKET, SO_ZEROCOPY, &one, sizeof(one));
```

---

## 7. 生产环境最佳实践

### 7.1 编译检查清单

```bash
# 生产构建推荐
CFLAGS="-O2 -march=native -flto -DNDEBUG -fstack-protector-strong -D_FORTIFY_SOURCE=2"
CXXFLAGS="$CFLAGS -std=c++17"

# CI/测试构建推荐
CFLAGS="-O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer"

# 安全加固选项
-fstack-protector-strong    # 栈溢出保护
-D_FORTIFY_SOURCE=2         # 缓冲区溢出检测
-fPIE -pie                  # 地址空间随机化
-Wl,-z,relro,-z,now         # GOT 保护
```

### 7.2 性能监控与诊断

```bash
# 运行时性能快照
perf top -p <PID>                           # 实时热点
perf record -g -p <PID> -- sleep 30         # 30秒采样
strace -c -p <PID>                          # 系统调用统计
ltrace -c -p <PID>                          # 库调用统计

# 内存泄漏持续监控
# 方法1：/proc/<PID>/smaps 监控 RSS 增长
while true; do
    grep -E "^(Rss|Pss)" /proc/<PID>/smaps | awk '{sum+=$2} END {print sum " kB"}'
    sleep 60
done

# 方法2：jemalloc heap profiling
MALLOC_CONF="prof:true,prof_interval:1073741824" LD_PRELOAD=libjemalloc.so ./myapp

# Core dump 分析
ulimit -c unlimited
gdb ./myapp core.<PID>
(gdb) bt        # 查看崩溃调用栈
(gdb) info threads  # 查看所有线程
```

### 7.3 常见性能问题速查表

| 症状 | 可能原因 | 诊断工具 | 优化方向 |
|------|----------|----------|----------|
| CPU 100% 单核 | 死循环/自旋锁 | perf top, strace | 代码审查/锁优化 |
| 多线程 CPU 利用率低 | 锁竞争/false sharing | perf lock, TSan | 分段锁/缓存行对齐 |
| RSS 持续增长 | 内存泄漏 | ASan, Valgrind, jemalloc prof | 修复泄漏/换分配器 |
| 高 cache-miss | 数据局部性差 | perf stat, Cachegrind | SoA/热冷分离/预取 |
| 高 page-fault | mmap 大量小文件/内存碎片 | perf stat | 预分配/hugepages |
| 系统调用过多 | I/O 未批量化 | strace -c | 批量读写/mmap/io_uring |
| 启动慢 | 动态链接/大量初始化 | perf record | 延迟初始化/静态链接 |
| 高分支预测失败 | 条件分支不可预测 | perf stat | 分支消除/查表/CMOV |

---

## 8. C++ 特有优化技巧

### 8.1 虚函数开销与替代方案

```cpp
// ❌ 虚函数（间接调用，阻碍内联和向量化）
class Shape {
    virtual double area() const = 0;
};

// ✅ CRTP（编译期多态，零开销）
template<typename Derived>
class Shape {
public:
    double area() const {
        return static_cast<const Derived*>(this)->area_impl();
    }
};
class Circle : public Shape<Circle> {
    double area_impl() const { return M_PI * r_ * r_; }
};

// ✅ std::variant + std::visit（C++17，类型安全的联合体）
using ShapeVar = std::variant<Circle, Rectangle, Triangle>;
double area(const ShapeVar& shape) {
    return std::visit([](const auto& s) { return s.area(); }, shape);
}
```

### 8.2 异常处理开销

```cpp
// 异常的零开销模型（GCC/Clang）：
// - 不抛异常时：零运行时开销（但增加代码体积）
// - 抛异常时：开销极大（栈展开）
// 高性能路径避免使用异常

// ✅ 使用 std::expected（C++23）或自定义 Result 类型
template<typename T, typename E = std::string>
class Result {
    std::variant<T, E> data_;
public:
    bool ok() const { return std::holds_alternative<T>(data_); }
    T& value() { return std::get<T>(data_); }
    E& error() { return std::get<E>(data_); }
};

// 禁用异常（嵌入式/游戏引擎常见）
// gcc -fno-exceptions -fno-rtti
```

---

## 9. 调优工作流总结

```text
1. 确定目标 → 明确性能指标（延迟/吞吐/内存）
2. 建立基线 → perf stat / time / benchmark
3. 找到瓶颈 → perf record + 火焰图
4. 分析根因 →
   ├── CPU 密集 → 算法优化/SIMD/编译优化
   ├── 内存瓶颈 → 缓存友好布局/分配器/内存池
   ├── I/O 瓶颈 → 批量化/mmap/io_uring
   └── 并发瓶颈 → 锁优化/无锁/线程池
5. 实施优化 → 一次只改一个变量
6. 验证效果 → 回归基线对比
7. 重复迭代 → 直到达标
```

> ⚡ **黄金法则**：先 profiling，再优化。不要凭直觉猜测瓶颈——90% 的时间花在 10% 的代码上。
