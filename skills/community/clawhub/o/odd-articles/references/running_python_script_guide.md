# 运行python脚本失败应对方法

Windows 环境下，运行python脚本失败，提示 `No such file or directory`。
这是因为Windows环境下bash默认使用的是Windows路径，而python脚本中使用的是Unix路径，导致的。

---

## 应对方法

创建一个run_python.py，并以subprocess.run运行该python脚本。

---

## 示例

```python
import sys
import subprocess

cmd = [
    'md2wechat.py',
    '2026-03-25-超轻量级中文TTS模型推荐.md',
    '-o', '2026-03-25-超轻量级中文TTS模型推荐_preview.html',
    '--theme', 'default',
    '--keep-title'
]

result = subprocess.run([sys.executable] + cmd, capture_output=True, text=True)
result = subprocess.run([sys.executable] + cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
print(result.stdout)
print(result.stderr)
```


