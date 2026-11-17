# 游戏 QA 与性能（Game QA & Performance）

> 子技能 `game-developer` 提到"调试与性能"，但游戏性能是独立的工程课题：
> 帧预算、Draw Call、GC 卡顿、内存。本篇给一套游戏专属的 QA 与性能 playbook，
> 附 Three.js 实测命令、移动端适配与上线前清单。

## 1. 帧预算（60fps 的硬账）

60fps ⇒ 每帧 ≤16.6ms；30fps ⇒ ≤33ms。预算分配：

| 阶段 | 预算(60fps) | 超了的表现 |
|------|-------------|------------|
| 逻辑/物理 | ≤4ms | 模拟不同步、行为卡 |
| 渲染提交 | ≤6ms | 掉帧、画面撕裂 |
| GPU 绘制 | ≤5ms | 着色器重、过度绘制 |
| 余量 | ≤1.6ms | 突发不掉档 |

**法则**：先量单帧各阶段耗时，再针对性优化；不要凭感觉。Three.js 用 `stats.js` +
`renderer.info` 看 draw call / 三角面数。

## 2. Three.js 性能命令与手段

```bash
# 开发期注入性能面板（stats.js）
#   import Stats from 'stats.js'; const s = new Stats(); document.body.appendChild(s.dom)
#   animate(){ s.begin(); ... s.end(); }

# 看渲染统计
#   console.log(renderer.info.render)  // calls / triangles / points
#   console.log(renderer.info.memory)  // geometries / textures
```

优化手段（按性价比）：
1. **合批**：静态网格 `BufferGeometryUtils.mergeGeometries` 合并；同材质物体一起画
2. **降 draw call**：共享材质/纹理，图集代替散图（见 [references/asset-pipeline.md](asset-pipeline.md)）
3. **降面**：LOD（远处低模），剔除不可见（Frustum Culling 默认开，但大场景手动分区）
4. **纹理**：KTX2/GPU 压缩，mipmap 开启，尺寸 2 的幂
5. **阴影**：阴影最贵；用单方向光 + 低分辨率 shadow map，或烘焙
6. **后处理**：Bloom/DOF 代价高；按需且降分辨率
7. **对象池**：子弹/粒子复用，避免频繁 new → GC 卡顿

## 3. GC 卡顿（最隐蔽）

JS 游戏常见"周期性小卡"来自 GC：
- 避免在 `animate` 循环里 `new` 对象/数组/Vector3（复用临时变量）
- 字符串拼接、闭包捕获引发的隐式分配也要警惕
- 用对象池管理频繁创建销毁的实体

```js
// 反例：每帧 new
function update(){ const v = new THREE.Vector3(); ... }
// 正例：复用模块级临时变量
const _tmp = new THREE.Vector3();
function update(){ _tmp.set(...); ... }
```

## 4. 移动端与 Steam Deck 适配

- **分辨率缩放**：`renderer.setPixelRatio(Math.min(devicePixelRatio, 2))`，重设备降采样
- **帧率封顶**：移动端封 30/40fps 保温度与电量
- **输入**：手柄 + 触屏 + 键鼠都支持（Steam Deck 是手柄）
- **内存**：移动 GPU 显存共享系统内存，纹理总量严控
- **发热**：长时间高负载降频；用 §1 帧预算留余量

## 5. 游戏专属 QA 清单（功能之外）

| 检查 | 为什么 | 验证 |
|------|--------|------|
| 长时间运行不崩 | 内存泄漏/GC 累积 | 挂机 30 分钟看内存曲线 |
| 切后台再回前台 | 上下文丢失/暂停 | 手机切 App 再回 |
| 极端输入 | 连点/狂摇杆 | 压力操作不卡死 |
| 存档读写 | 坏档崩溃 | 删档/损坏档不崩 |
| 不同分辨率 | UI 错位 | 手机/平板/Deck 各看一遍 |
| 音画不同步 | 延迟累积 | 长时间播放对嘴型 |

## 6. 典型坑与规避

- **坑：每帧 new 临时对象**导致周期 GC 卡。*规避*：复用临时变量 + 对象池。
- **坑：draw call 几百**卡成幻灯片。*规避*：合批 + 图集 + 共享材质。
- **坑：阴影全开**GPU 爆。*规避*：单光 + 低分辨率 shadow map / 烘焙。
- **坑：像素比不设上限**4K 屏炸显存。*规避*：`setPixelRatio(min(dpr,2))`。
- **坑：只测桌面不测移动**，上线 Deck 翻车。*规避*：移动/Deck 纳入必测矩阵。
- **坑：资源引用缺失**运行时裂图（见 [references/asset-pipeline.md](asset-pipeline.md) + [scripts/check_asset_refs.py](../scripts/check_asset_refs.py)）。

## 7. 收口清单

- [ ] 已用 stats.js / renderer.info 测得**帧预算**各阶段耗时
- [ ] draw call 已合批，图集代替散图
- [ ] 纹理已压缩 + mipmap，尺寸 2 的幂
- [ ] 阴影/后处理已按需降配
- [ ] animate 循环无每帧 new，对象池就位（GC 卡顿消除）
- [ ] 移动端 setPixelRatio 封顶、帧率封顶、手柄+触屏支持
- [ ] 挂机/切后台/极端输入/坏档 四类健壮性通过
- [ ] 多分辨率 UI 对齐（手机/平板/Deck）
- [ ] 资源引用完整性 [scripts/check_asset_refs.py](../scripts/check_asset_refs.py) 0 缺失

## 8. 目标设备与性能基线

按市场定最低设备，性能预算对它负责（不是对开发机）：

| 设备档 | 目标帧率 | 显存/内存 | 代表 |
|--------|----------|-----------|------|
| 低端 Android | 30fps | <1GB 共享 | 千元机 |
| 中端手机 | 60fps | 2–4GB | 主流 |
| Steam Deck | 30–60fps | 共享 16GB | Valve |
| 桌面独显 | 60–144fps | 独立 | PC |
| Web(H5) | 30–60fps | 视浏览器 | 任意 |

**法则**：在最低目标设备上实测达标，才算性能过关；开发机 144fps 无意义。

## 9. 跨引擎 Profiling 工具

| 引擎/平台 | 工具 | 看什么 |
|-----------|------|--------|
| Three.js/Web | Chrome DevTools Performance + stats.js + renderer.info | 帧耗时/绘制调用/三角面 |
| Three.js/Web | Spector.js | WebGL 调用级分析 |
| Godot | 内置 Profiler / 调试器 | 帧时间/脚本/GPU |
| Unity | Profiler / Frame Debugger | CPU/GPU/内存/批处理 |
| 移动 | Android GPU Inspector / Xcode Instruments | GPU 瓶颈/功耗 |

先用对工具抓到瓶颈，再优化；瞎优化常优化错地方。

## 10. 性能回归测试策略

性能会"慢慢变坏"——每次加功能悄悄多吃几 ms，积少成多。防回归：

- 建一个**基准场景**（固定内容/固定操作），CI 里跑并记帧时间
- 设阈值（如帧时间 > 预算 110% 即红），超标阻断合并
- 关键指标（draw call / 三角面 / 内存）随版本画曲线，异常波动即查
- 低端设备留一台长期挂基准场景，肉眼+脚本双监控

## 11. 卡顿分类速查

| 现象 | 可能根因 | 首查 |
|------|----------|------|
| 周期性小卡 | GC | animate 里 new / 无对象池 |
| 持续低帧 | draw call 多 | 合批/图集/共享材质 |
| 移动端发热降频 | GPU 满负载 | 降分辨率/降特效 |
| 加载时卡死 | 同步加载大资源 | 异步/分帧加载 |
| 切场景掉帧 | 重建开销 | 对象池/预创建 |
| 内存随时间涨 | 泄漏 | 纹理/几何未释放 |

## 12. 收口补充清单（性能门禁）

- [ ] 已在最低目标设备实测达标（非开发机）
- [ ] 用对应 Profiler 抓到瓶颈并据此优化
- [ ] 基准场景 + 帧时间阈值已进 CI，超标阻断
- [ ] 关键指标版本曲线有监控，异常即查
- [ ] 卡顿分类（§11）逐一排除，无周期性 GC / 持续低帧
- [ ] 异步加载就位，无加载期主线程卡死

## 相关子技能与层次边界

> 本文属**QA 与性能方法层**（帧预算 / GC / 移动与 Deck 适配 / 性能门禁）；具体调试与发布交给子技能。

- 落地「Three.js 性能调试与发布」→ [`skills/game-developer/SKILL.md`](../skills/game-developer/SKILL.md)
- 落地「游戏手感 / UI 打磨」→ [`skills/game-designer/SKILL.md`](../skills/game-designer/SKILL.md)
- 兄弟参考：资源引用完整性（运行时缺图根因）→ [references/asset-pipeline.md](asset-pipeline.md) §5
- 兄弟参考：选型对性能的上限约束 → [references/decision-engine-tech.md](decision-engine-tech.md) §3

