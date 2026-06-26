# Python 性能分析

## cProfile

```bash
# 命令行
python -m cProfile script.py
python -m cProfile -s cumtime script.py   # 按累计时间排序
python -m cProfile -o output.prof script.py
```

```python
# 代码中使用
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# 要分析的代码
result = expensive_function()

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)
```

## line_profiler

```bash
pip install line_profiler
```

```python
@profile  # 装饰器
def slow_function():
    ...

# 运行
kernprof -l -v script.py
```

## memory_profiler

```bash
pip install memory_profiler
```

```python
@profile
def memory_intensive():
    ...

# 运行
python -m memory_profiler script.py
mprof run script.py
mprof plot
```

## py-spy

```bash
pip install py-spy

# 分析运行中的程序
py-spy top --pid 12345

# 生成火焰图
py-spy record -o flamegraph.svg --pid 12345

# 分析脚本
py-spy record -o flamegraph.svg python script.py
```

## 性能优化

```python
# 字符串拼接 - 避免 +
result = "".join(strings)

# 列表推导式更快
result = [i * 2 for i in range(1000)]

# 使用生成器节省内存
result = (i * 2 for i in range(1000000))

# 使用内置函数
total = sum(numbers)

# 字典查找比列表快 O(1) vs O(n)
if item in my_set:
    ...
```
