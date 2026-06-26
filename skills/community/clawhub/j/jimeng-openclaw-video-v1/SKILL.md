# 即梦视频生成技能

该技能包提供万界方舟即梦模型（Jimeng）的视频生成能力，支持文生视频任务。

### 功能特点
- 异步提交任务，支持自动轮询状态。
- 支持指定帧数（121或241）。
- 自动清理任务锁。
- 结果实时记录到 `veo_result.txt`。

### 使用方法
在 Python 中调用：
```python
from model.scripts.video_interface import trigger_jimeng_generation
trigger_jimeng_generation("一个赛博朋克风格的城市街道")
```
