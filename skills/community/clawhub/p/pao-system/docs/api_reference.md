# PAO API 参考文档

## 核心模块

### DeviceDiscovery

设备发现模块，负责局域网内设备自动发现。

```python
from device_discovery import DeviceDiscovery

device = DeviceDiscovery(name="MyDevice")
await device.start()
devices = device.get_discovered_devices()
await device.stop()
```

### Communication

通信模块，负责设备间消息传递。

```python
from communication import Communication

comm = Communication(device)
await comm.connect_to(peer_id)
await comm.send_message(peer_id, {"type": "test"})
await comm.disconnect()
```

### SkillManager

技能管理器，负责AI技能的搜索、加载和评分。

```python
from skill_manager import SkillManager

manager = SkillManager()
await manager.initialize()
skills = await manager.search_skills("python")
await manager.apply_skill("skill_name", params, score, feedback)
stats = await manager.get_skill_stats("skill_name")
```

### ContextAwareness

情境感知模块，负责收集和识别使用情境。

```python
from context_awareness import ContextAwareness

awareness = ContextAwareness()
await awareness.register_default_scenes()
contexts = await awareness.collect_all()
scene = await awareness.recognize_scene()
```

### LearningLoop

学习循环模块，负责处理用户反馈并持续改进。

```python
from learning_loop import LearningLoop, FeedbackType

loop = LearningLoop()
await loop.start()
await loop.submit_feedback(FeedbackType.EXPLICIT, "skill", params, score, feedback)
status = await loop.get_learning_status()
await loop.stop()
```

### SyncManager

同步管理器，负责多设备间数据同步。

```python
from sync import SyncManager

sync = SyncManager(device)
await sync.connect_peer(peer_id)
await sync.sync_data(data)
status = sync.get_sync_status()
await sync.disconnect()
```

## 配置

配置文件位于: `~/.config/pao/config.json`

```json
{
    "device_name": "PAO-Device",
    "port": 8080,
    "encryption": true,
    "auto_sync": true,
    "sync_interval": 60
}
```
