### b. `libtv_qunqin.py`

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
from pathlib import Path

# 1️⃣ 先尝试导入 libtv
try:
    from libtv import WebtoonCreator
except Exception as e:
    print(json.dumps({"error": f"libtv 未安装或导入失败: {e}"}))
    sys.exit(1)

def main():
    # 2️⃣ 从标准输入读取 JSON
    try:
        payload = json.load(sys.stdin)
    except Exception as e:
        print(json.dumps({"error": f"JSON 解析错误: {e}"}))
        sys.exit(1)

    # 3️⃣ 读取故事文本
    story_file = Path(payload.get("story_file", ""))
    if not story_file.is_file():
        print(json.dumps({"error": f"文件不存在: {story_file}"}))
        sys.exit(1)
    with open(story_file, encoding="utf-8") as f:
        story_text = f.read()

    # 4️⃣ 配置漫画生成
    panel_count = int(payload.get("panel_count", 6))
    font = payload.get("font", "Noto Serif SC")
    output_dir = Path(payload.get("output_dir", "./output/寻秦记")).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)

    creator = WebtoonCreator(
        text=story_text,
        panels=panel_count,
        font=font,
        output_dir=output_dir,
    )

    # 5️⃣ 生成漫画并返回结果
    result = creator.run()
    print(json.dumps(result))

if __name__ == "__main__":
    main()