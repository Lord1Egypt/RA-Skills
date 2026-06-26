# Language Pair: Python → C++

**Difficulty tier**: High (manual memory optional via RAII, template metaprogramming, multiple inheritance)

**Key differences**:
- Memory model: Python GC / C++ RAII (prefer) + manual (avoid)
- Type system: Python dynamic / C++ static with templates + concepts (C++20)
- Error handling: Python exceptions / C++ exceptions (use them) or `std::expected` (C++23)
- OOP: Python single-dispatch classes / C++ full OOP with templates
- Strings: Python str / `std::string` (value semantics, UTF-8 by convention)
- STL: C++ has rich stdlib collections; closest to Python

**Key advantage over C**: RAII eliminates most memory management complexity. C++ stdlib is close to Python's in richness.

---

## Pre-Mapped Core Types

| Python | C++ | Equivalence | Notes |
|---|---|---|---|
| `int` | `int64_t` | behavioral | Use `<cstdint>` |
| `float` | `double` | structural | |
| `bool` | `bool` | structural | |
| `str` | `std::string` | structural | |
| `bytes` | `std::vector<uint8_t>` | structural | |
| `None` | `std::nullptr_t` / `std::optional` | structural | |
| `list[T]` | `std::vector<T>` | structural | |
| `tuple[A,B]` | `std::tuple<A,B>` or `std::pair` | structural | |
| `dict[K,V]` | `std::unordered_map<K,V>` | behavioral | Order not preserved |
| `collections.OrderedDict` | No stdlib equivalent → use insertion-ordered map | behavioral | Implement or use third-party |
| `set[T]` | `std::unordered_set<T>` | structural | |
| `Optional[T]` | `std::optional<T>` | structural | C++17 |
| `deque` | `std::deque<T>` | structural | |
| `heapq` | `std::priority_queue` | structural | Note: max-heap by default; Python is min-heap |

## Standard Library Mapping

| Python | C++ | Equivalence | Notes |
|---|---|---|---|
| `os.path.join` | `std::filesystem::path` (C++17) | structural | |
| `os.listdir` | `std::filesystem::directory_iterator` | structural | |
| `os.environ.get` | `std::getenv` | structural | |
| `open(f)` | `std::ifstream` / `std::ofstream` | structural | |
| `json` | `nlohmann/json` | structural | Header-only, widely used |
| `re` | `std::regex` | structural | |
| `hashlib` | OpenSSL or Crypto++ | structural | |
| `time.time()` | `std::chrono::system_clock::now()` | structural | |
| `random.random()` | `std::mt19937` + `uniform_real_distribution` | behavioral | Different RNG |
| `threading.Thread` | `std::thread` | structural | |
| `asyncio` | `std::coroutine` + executor (C++20) or Boost.Asio | structural | |
| `logging` | `spdlog` | structural | |
| `argparse` | `CLI11` or `argparse` header | structural | |

## Common Third-Party Libraries

| Python | C++ | Equivalence | Notes |
|---|---|---|---|
| `numpy` | Eigen or xtensor | behavioral | API differs; structural at algorithm level |
| `requests` | libcurl or cpp-httplib | structural | |
| `pytest` | Google Test (`gtest`) or Catch2 | structural | |
| `pydantic` | struct + nlohmann/json | structural | |
| `click` | CLI11 | structural | |

---

## Error Handling

C++ exceptions mirror Python exceptions most closely among systems languages:

**Python:**
```python
def read_file(path: str) -> str:
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        raise IOError(f"not found: {path}")
```

**C++:**
```cpp
std::string read_file(const std::string& path) {
    std::ifstream f(path);
    if (!f.is_open()) {
        throw std::runtime_error("not found: " + path);
    }
    return std::string(std::istreambuf_iterator<char>(f),
                       std::istreambuf_iterator<char>());
}
```

**Rule**: Python exception types → C++ exception types. One `except` clause = one `catch` clause. Do NOT flatten all exceptions into a generic `std::exception`.

## Class → Class (with RAII)

**Python:**
```python
class FileReader:
    def __init__(self, path: str):
        self.f = open(path, 'rb')
    def read_chunk(self, n: int) -> bytes:
        return self.f.read(n)
    def __del__(self):
        self.f.close()
```

**C++:**
```cpp
class FileReader {
    std::ifstream f_;
public:
    explicit FileReader(const std::string& path) {
        f_.open(path, std::ios::binary);
        if (!f_.is_open()) throw std::runtime_error("cannot open: " + path);
    }
    // Destructor automatic via RAII — std::ifstream closes on destruction
    std::vector<uint8_t> read_chunk(size_t n) {
        std::vector<uint8_t> buf(n);
        f_.read(reinterpret_cast<char*>(buf.data()), n);
        buf.resize(f_.gcount());
        return buf;
    }
};
```

## heapq Direction (Critical Gap)

Python `heapq` is a **min-heap**. `std::priority_queue` is a **max-heap**.

```cpp
// Min-heap in C++ (mirrors Python heapq):
std::priority_queue<int, std::vector<int>, std::greater<int>> min_heap;
```

Always check the IPO registry's `process.steps` to confirm the heap direction before translating.

## Anti-Patterns

| Wrong | Why | Correct |
|---|---|---|
| Raw `new`/`delete` | RAII is available; use it | `std::unique_ptr` / `std::shared_ptr` |
| `std::map` when Python used dict | `std::map` is sorted (O log n) | `std::unordered_map` for Python dict |
| Catching `...` everywhere | Loses exception semantics | Catch specific types matching Python's excepts |
| Using `#define` for constants | Not type-safe | `constexpr` |
| Implicit `int` narrowing | Undefined behavior | Explicit cast with range check |

## Testing Toolchain

| Python | C++ | Notes |
|---|---|---|
| `pytest` | Google Test or Catch2 | |
| `pytest.raises` | `EXPECT_THROW(expr, ExceptionType)` | |
| `unittest.mock` | PROHIBITED | Real implementations only |
| `mypy` | Compiler + `-Wall -Wextra` | |
| `black` | `clang-format` | |
| Valgrind | AddressSanitizer (`-fsanitize=address`) | Build with: `-fsanitize=address,undefined` |

## Build System (CMake)

```cmake
# CMakeLists.txt target structure
cmake_minimum_required(VERSION 3.20)
project(<name> CXX)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_compile_options(-Wall -Wextra -Wpedantic)

# Test target
enable_testing()
find_package(GTest REQUIRED)
add_executable(tests <test_files>)
target_link_libraries(tests GTest::gtest_main)
add_test(NAME unit COMMAND tests)
```

## CI Adaptation

```yaml
# Python:
- run: pytest

# C++:
- run: cmake -B build -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_FLAGS="-fsanitize=address,undefined"
- run: cmake --build build
- run: ctest --test-dir build --output-on-failure
```
