---
name: godot-openxr-marker-tracking
description: 在 Godot 4.6+ 上做 OpenXR Spatial Entities 的 Marker Tracking（ArUco / AprilTag / QRCode 识别实体卡牌、物体），以及在无 XR 运行时的开发机上做 headless 编译校验与 API 回归。当用户提到 Godot 做 AR、OpenXR 标记追踪、ArUco、卡牌识别、Spatial Entities、OpenXRMarkerTracker、headless 跑 Godot 脚本卡死、或 Godot XR 脚本报 "Cannot call non-static function" 时使用。
agent_created: true
---

# Godot OpenXR Marker Tracking 开发与验证

Godot 4.6 引入的 OpenXR Spatial Entities Marker Tracking，**官方文档与实际 API 有大量偏差**，
且无 XR 运行时的开发机上 headless 验证有独特陷阱。本 skill 记录全部实测结论。

## 适用判断

- Godot **4.6+**（4.5 及以前没有 Spatial Entities）
- 目标平台必须是**有 OpenXR 运行时的设备**：Quest 3、Pico 4、Samsung Galaxy XR 等头显
- ⚠️ **手机/平板不行**。Godot 官方文档明确说明 handheld 平台不提供 OpenXR 支持，
  要用手机只能走厂商专有的 ARCore 插件，与 Marker Tracking 是两条路

---

## 一、正确的初始化时序（最容易写错的地方）

空间上下文**必须等 OpenXR 会话开始后**才能创建，在 `_ready()` 里直接建会失败。

```gdscript
class_name CardMarkerDetector
extends Node3D

var _spatial_context: RID
var _trackers: Dictionary[int, OpenXRMarkerTracker] = {}

func _ready() -> void:
    var openxr_interface: OpenXRInterface = (
        XRServer.find_interface("OpenXR") as OpenXRInterface
    )
    if openxr_interface == null:
        push_warning("未找到 OpenXR 接口，AR 功能不可用。")
        return
    openxr_interface.session_begun.connect(_on_session_begun)
    if openxr_interface.is_initialized():
        _on_session_begun()          # 信号可能已经错过，主动补一次

func _on_session_begun() -> void:
    _setup_spatial_context()

func _setup_spatial_context() -> void:
    if _spatial_context.is_valid():
        return
    if not OpenXRSpatialMarkerTrackingCapability.is_aruco_supported():
        push_warning("设备不支持 Aruco。")
        return

    var configurations: Array[OpenXRSpatialCapabilityConfigurationBaseHeader] = []
    var aruco_config := OpenXRSpatialCapabilityConfigurationAruco.new()
    aruco_config.aruco_dict = (
        OpenXRSpatialCapabilityConfigurationAruco.ARUCO_DICT_5X5_50
    )
    configurations.push_back(aruco_config)

    # 注意：这些是**引擎单例**，直接 类名.方法()，不要 new()
    var future: OpenXRFutureResult = (
        OpenXRSpatialEntityExtension.create_spatial_context(configurations)
    )
    await future.completed
    if not _future_succeeded(future):
        push_error("创建空间上下文失败。")
        return

    _spatial_context = future.get_result_value()
    if not _spatial_context.is_valid():
        push_error("空间上下文 RID 无效。")
        return

    OpenXRSpatialEntityExtension.spatial_discovery_recommended.connect(
        _on_discovery_recommended
    )
    _start_discovery()
```

## 二、发现与快照读取

```gdscript
func _future_succeeded(p_future: OpenXRFutureResult) -> bool:
    # 没有 RESULT_SUCCESS！成功 = RESULT_FINISHED
    if p_future == null:
        return false
    return p_future.get_status() == OpenXRFutureResult.RESULT_FINISHED

func _on_discovery_recommended(p_spatial_context: RID) -> void:
    if p_spatial_context != _spatial_context:
        return                        # 该信号对所有上下文广播
    _start_discovery()

func _start_discovery() -> void:
    if not _spatial_context.is_valid() or _discovery_in_flight:
        return
    _discovery_in_flight = true
    var future: OpenXRFutureResult = (
        OpenXRSpatialEntityExtension.discover_spatial_entities(
            _spatial_context,
            # 第二参数是 PackedInt64Array 的**组件类型常量**，
            # 不是组件数据对象数组
            PackedInt64Array([
                OpenXRSpatialEntityExtension.COMPONENT_TYPE_MARKER,
                OpenXRSpatialEntityExtension.COMPONENT_TYPE_BOUNDED_2D,
            ])
        )
    )
    await future.completed
    _discovery_in_flight = false
    if not _future_succeeded(future):
        return
    var snapshot: RID = future.get_result_value()
    _consume_snapshot(snapshot, true)
    OpenXRSpatialEntityExtension.free_spatial_snapshot(snapshot)  # 必须释放

func _consume_snapshot(p_snapshot: RID, p_is_full: bool) -> void:
    if not p_snapshot.is_valid():
        return

    # component_data 的**第一个元素必须是 OpenXRSpatialQueryResultData**，
    # 实体数量从它的 get_capacity() 取。顺序写错拿不到任何实体。
    var result_data := OpenXRSpatialQueryResultData.new()
    var marker_list := OpenXRSpatialComponentMarkerList.new()
    var bounded_list := OpenXRSpatialComponentBounded2DList.new()
    var component_data: Array = [result_data, marker_list, bounded_list]

    if not OpenXRSpatialEntityExtension.query_snapshot(p_snapshot, component_data):
        return   # 返回 bool，数据写回传入对象

    for i: int in result_data.get_capacity():
        if marker_list.get_marker_type(i) \
                != OpenXRSpatialComponentMarkerList.MARKER_TYPE_ARUCO:
            continue
        var marker_id: int = marker_list.get_marker_id(i)
        var center: Transform3D = bounded_list.get_center_pose(i)
        var size: Vector2 = bounded_list.get_size(i)
        # ... 业务逻辑
```

### 注册跟踪器（供 XRServer / 下游节点读取位姿）

```gdscript
func _create_tracker(entity_id: int, marker_id: int) -> OpenXRMarkerTracker:
    var tracker := OpenXRMarkerTracker.new()
    tracker.marker_id = marker_id
    tracker.marker_type = OpenXRSpatialComponentMarkerList.MARKER_TYPE_ARUCO
    tracker.name = "card_marker_%d" % marker_id   # 字段是 name，不是 tracker_name
    tracker.bounds_size = Vector2(0.042, 0.042)   # Vector2，不是 int
    XRServer.add_tracker(tracker)                 # 没有 register_with_xr_server 属性
    _trackers[entity_id] = tracker
    return tracker
```

清理时记得 `XRServer.remove_tracker(tracker)` +
`OpenXRSpatialEntityExtension.free_spatial_context(_spatial_context)`，
并断开 `spatial_discovery_recommended` 连接。

---

## 三、API 纠错对照表（文档 vs 实测）

官方文档部分方法名与实际 API **不一致**，以下均为实测结论：

| 文档/直觉写法 | 实际 API |
|---|---|
| `aruco_is_supported()` | `is_aruco_supported()` |
| `bounded_list.get_bounded_2d(i)` | `get_center_pose(i)` + `get_size(i)` |
| `OpenXRSpatialSnapshotResult` | **类不存在**，快照就是 `RID` |
| `future.get_status() != RESULT_SUCCESS` | 无 `RESULT_SUCCESS`，用 `RESULT_FINISHED` |
| `future.get_result()` | `get_result_value()` |
| `tracker.register_with_xr_server = true` | **属性不存在**，用 `XRServer.add_tracker()` |
| `tracker.tracker_name = "x"` | `tracker.name = "x"` |
| `start_entity_discovery()` | `discover_spatial_entities()` |
| `cancel_discovery(snapshot)` | `free_spatial_snapshot(snapshot)` |

### 两个「看着像错、其实不是错」

1. **`Cannot call non-static function ... on the class ... directly`**
   `OpenXRSpatialEntityExtension` 等是**引擎单例**，`类名.方法()` 是正确写法。
   报这个错通常是因为脚本在 OpenXR 模块未激活的环境下被解析。

2. **`bounds_size` 属性元数据标成 `int`**
   `set_bounds_size()` 收 `Vector2`，实测 `tracker.bounds_size = Vector2(...)`
   可正常读写。属性元数据是错的，以实测为准。

---

## 四、AruCo 字典选择

**用 5X5_50，对齐 OpenXR 规范。** 规范中 ArUco 的参考测试码就是
`XR_SPATIAL_MARKER_ARUCO_DICT_5X5_50_EXT`（ID 43）。用规范同款字典运行时兼容性最高。

**尺寸权衡**：标记模块尺寸 = 标记边长 ÷ (字典阶数 + 2)。
小目标（如 60×90mm 卡牌，标记 42mm）选低阶字典：
- 5X5 → 模块 ≈ 6mm，30-60cm 可靠
- 7X7 → 模块 ≈ 4.7mm，识别率断崖下跌

### ⚠️ Godot 与 OpenCV 枚举值不一致，必须按名字对齐

| 字典 | Godot | OpenCV |
|---|---|---|
| 5X5_50 | 5 | 4 |
| 7X7_1000 | 16 | 15 |

把 Godot 的枚举值直接传给 OpenCV 会生成**另一种字典**的标记，扫不出来还查不出原因。

```python
# 正确：按名字取
dictionary = cv2.aruco.getPredefinedDictionary(
    getattr(cv2.aruco, "DICT_5X5_50")   # 不要传数字
)
marker = cv2.aruco.generateImageMarker(dictionary, marker_id, side_px)
```

---

## 五、本机（无 XR 运行时）headless 验证

### 核心陷阱

`project.godot` 里 `openxr/enabled=true` 时，在**没有 OpenXR 运行时**的机器上
跑 `godot --headless --script X` 会**无限阻塞**在 OpenXR 初始化，
5 分钟超时都跑不完。

**必须加 `--xr-mode off`。**

但加了之后 OpenXR 单例不注册，所有单例调用被误报为
`Cannot call non-static function ...`。这是环境限制，不是代码错误 —— 验证脚本里要剔除。

### 验证命令

```bash
GODOT="C:/path/to/Godot_v4.6.3-stable_win64_console.exe"
PROJ="D:/path/to/project"          # 用 Windows 路径

# 编译校验（务必带 --xr-mode off）
"$GODOT" --headless --xr-mode off --path "$PROJ" \
  --script "res://tests/compile_check.gd"
```

### 判定"有没有真错误"的正确方法

```bash
grep "Parse Error" "$LOG" | grep -v 'Cannot call non-static function'
# 输出非空 → 有真错误
```

### 编译校验脚本的正确判据

`load()` 对解析失败的脚本**仍返回非 null 对象**，
需要看 `can_instantiate()`：

- `load(path) == null` → 硬失败（源码都读不出）
- `can_instantiate() == false` → 有解析错误。
  但调用 OpenXR 单例的脚本在 `--xr-mode off` 下**必然**落到这一档，
  属正常，要单独归类为「需 XR」而不是失败。
- `reload()` **不能用**作判据：正常脚本也会返回非 OK
  （"Cannot reload script while instances exist"）。

### 顺带确认的坑

- `--headless --quit` **本身也会挂**（只输出 3 行），不能用它判断环境是否正常。
- `ClassDB.class_get_property_list(cls, true)` 的第二参数是 `no_inheritance`。
  传 `true` 只列自身属性，会漏掉父类字段（容易误判属性不存在）。
  要查完整属性用 `false`。

---

## 六、Python 侧（OpenCV）配套坑

**`cv2.imwrite()` 在 Windows 上不支持非 ASCII 路径。**
遇到 `D:\软件\...` 这类路径会**静默返回 False 且不抛异常**，文件根本不生成。

```python
def save_png(image, path):
    ok, buffer = cv2.imencode(".png", image)
    if not ok:
        raise RuntimeError(f"PNG 编码失败: {path.name}")
    path.write_bytes(buffer.tobytes())   # 用 Python 自己的 I/O
```

另外 OpenCV 5.0 已**移除 `cv2.aruco.estimatePoseSingleMarkers()`**，
姿态解算直接用 `cv2.solvePnP()`：

```python
ok, rvec, tvec = cv2.solvePnP(obj_points, image_points, K, dist_coeffs)
```

### ⚠️ 倾斜角绝不能取 ‖rvec‖（会把「正对」算成 180°）

这是做卡牌姿态时最容易写错的指标，而且错了**很难发现**——数值看起来
「有变化、很合理」，只是方向整个反了。

`solvePnP` 解出的是「标记坐标系 → 相机坐标系」的完整旋转。
对一块**正对镜头**的平面标记，这个旋转不是 0：标记的 Z 轴（法线）要翻转
180° 才朝向相机，所以 `R = diag(1, -1, -1)`、`‖rvec‖ ≈ π`。

```python
# ❌ 错误：正对镜头 → 180°，和「完全侧对」混在同一个档里
angle_deg = float(np.linalg.norm(rvec)) * 180.0 / math.pi

# ✅ 正确：标记法线与视线的夹角
def tilt_deg(rvec, tvec):
    """0° = 正对镜头，90° = 完全侧对。"""
    R, _ = cv2.Rodrigues(np.asarray(rvec).reshape(3, 1))
    normal = R[:, 2].ravel()                 # 标记平面外法向（相机坐标系下）
    t = np.asarray(tvec).ravel()
    n = float(np.linalg.norm(t))
    if n < 1e-9:
        return 0.0
    los = -t / n                             # 由标记指向相机的单位向量
    cos_a = abs(float(np.dot(normal, los)))  # 取绝对值：正反两面都算识别成功
    return math.degrees(math.acos(max(0.0, min(1.0, cos_a))))
```

验证方法（务必这么测，别目测）：用 `cv2.projectPoints` 正向造出
**精确倾斜 X°** 的像点，再 `solvePnP` 反解，比对误差。实测 0/15/30/45/60°
误差全为 0.00°。

> 同类陷阱的一般形态：**凡是从 `rvec` 推导「物理角度」，
> 先想清楚参考系对不对齐**。旋转的模长是「相对对象自身标准姿态的转角」，
> 通常不是你想要的那个物理量。
> 另外 `rvec` 转欧拉角时要注意解算结果的等价表示
> （`R` 与「绕某个轴转 ±π」的组合可能表示同一姿态）。

---

## 七、验证清单（改完代码照这个跑）

1. `bash tools/verify.sh --project <项目目录>` —— 编译 + API 回归 + Python 自测一键跑。
   无 Godot 的机器上加 `--skip-godot` 只跑 Python 段；缺 `cv2`/`numpy` 时该段报 SKIP
   而不是假通过。退出码：`0` 通过 / `1` 有失败 / `2` 一项都没跑成。
   脚本把本节下面两条（API 断言、编译判据）都写成了可执行形式，改代码后照跑即可。
2. API 回归脚本要常驻，把上面「纠错对照表」里的每条都写成断言：
   正确名字**存在**、错误名字**不存在**。这样下次 Godot 改 API 会立刻暴露
3. 真机测试前先确认设备能力：`is_aruco_supported()` 可能为 false
   （有些 runtime 只实现了 QRCode）
