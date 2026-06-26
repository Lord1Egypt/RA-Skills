# /freeze — 编辑锁定

> **作用**: 限制 AI 只能在指定目录内编辑文件，防止误改其他代码。

## 使用场景
- 正在修 A 模块的 bug，不想让 AI 碰 B 模块
- 代码库很大，需要聚焦修改范围
- 多人协作时保护他人的代码

## 规则

### 启动 freeze
```
用户: /freeze backend/api/endpoints/
```

效果：
- ✅ 可以读写: `backend/api/endpoints/` 下所有文件
- ❌ 不能修改: 该目录外的任何文件（只可读取）
- ⚠️ 如果必须修改外部文件 → **停止并请求用户确认**

### 解除 freeze
```
用户: /unfreeze
或用户: /freeze .   （锁定整个项目根目录 = 不锁定）
```

## 实现方式

在执行任何 write/replace/edit 操作前，检查：
```python
FROZEN_PATH = "/backend/api/endpoints/"  # 用户指定的路径

def check_freeze(target_file):
    if not FROZEN_PATH:
        return True  # 未启用 freeze
    # 标准化路径
    abs_target = os.path.abspath(target_file)
    abs_frozen = os.path.abspath(FROZEN_PATH)
    # 检查目标是否在冻结范围内
    if not abs_target.startswith(abs_frozen):
        raise FreezeViolation(
            f"❌ FREEZE 违规: 尝试修改 {target_file}\n"
            f"   当前锁定范围: {FROZEN_PATH}\n"
            f"   如需修改，请用 /unfreeze 或指定新的 /freeze 路径"
        )
    return True
```

## 与 /careful 的关系
- `/freeze` 控制的是 **位置**（能改哪里）
- `/careful` 控制的是 **操作**（能做什么危险操作）
- `/guard` = freeze + careful 同时开启
