# CLI 工具 · context-compressor

---

## 压缩核心脚本

```python
#!/usr/bin/env python3
"""
Context Compressor CLI
Usage: hawk-compress [options]
"""

import argparse
import json
import sys
from datetime import datetime

def compress_context(history, level='normal', keep_recent=10):
    """压缩对话上下文"""
    # 分离系统提示
    system = None
    dialog = []
    for msg in history:
        if msg.get('role') == 'system':
            system = msg['content']
        else:
            dialog.append(msg)

    # 按压缩层级处理
    if level == 'light':
        recent = dialog[-keep_recent:]
        older = [summarize(m) for m in dialog[:-keep_recent]]
    elif level == 'normal':
        recent = dialog[-keep_recent:]
        older = [summarize(m) for m in dialog[:-keep_recent]]
    elif level == 'heavy':
        recent = dialog[-5:]
        older = [summarize_all(dialog[:-5])]
    else:  # emergency
        recent = dialog[-3:]
        older = []

    # 重组
    result = []
    if system:
        result.append({'role': 'system', 'content': system})
    result.extend(older)
    result.extend(recent)

    return result

def main():
    parser = argparse.ArgumentParser(description='Context Compressor')
    parser.add_argument('--level', '-l', choices=['light', 'normal', 'heavy', 'emergency'],
                        default='normal', help='Compression level')
    parser.add_argument('--keep', '-k', type=int, default=10,
                        help='Number of recent messages to keep intact')
    parser.add_argument('--input', '-i', help='Input JSON file (chat history)')
    parser.add_argument('--output', '-o', help='Output JSON file')
    parser.add_argument('--dry-run', '-n', action='store_true',
                        help='Preview without writing')
    args = parser.parse_args()

    # 读取输入
    if args.input:
        with open(args.input) as f:
            history = json.load(f)
    else:
        # 从 stdin 读取
        history = json.load(sys.stdin)

    # 压缩
    compressed = compress_context(history, args.level, args.keep)

    # 计算统计
    original_tokens = sum(estimate_tokens(m['content']) for m in history)
    compressed_tokens = sum(estimate_tokens(m['content']) for m in compressed)

    output = {
        'status': 'success',
        'compressed_prompt': compressed,
        'stats': {
            'original_tokens': original_tokens,
            'compressed_tokens': compressed_tokens,
            'ratio': f"{original_tokens / max(compressed_tokens, 1):.1f}x",
            'kept_messages': len([m for m in compressed if m.get('status') == 'preserved']),
            'summarized_count': len([m for m in compressed if m.get('status') == 'summarized']),
            'dropped_count': len(history) - len(compressed),
            'level': args.level
        },
        'timestamp': datetime.now().isoformat()
    }

    if args.dry_run:
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(output, f, indent=2, ensure_ascii=False)
            print(f"✅ 压缩完成: {original_tokens} → {compressed_tokens} tokens ({output['stats']['ratio']})")
        else:
            print(json.dumps(output, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
```

---

## 使用示例

```bash
# 基本压缩（normal级别）
hawk-compress --level normal --keep 10

# 预览（不写入）
hawk-compress --level heavy --dry-run

# 指定输入输出文件
hawk-compress --input history.json --output compressed.json

# 从 stdin 传入
cat history.json | hawk-compress --level normal
```

---

## 命令速查

| 命令 | 说明 |
|------|------|
| `hawk-compress` | 标准压缩（normal） |
| `hawk-compress -l light` | 轻度压缩 |
| `hawk-compress -l heavy` | 重度压缩 |
| `hawk-compress -l emergency` | 紧急压缩 |
| `hawk-compress -n` | 预览压缩效果 |
| `hawk-compress -k 15` | 保留最近15轮 |
