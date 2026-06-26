# Time-and-Motion Study

## 一句话

> **Time-and-motion study** 是一大类用于"把工作拆成元动作、量化时间并据此改良效率"的技术的总称，源于工业工程（不是工业心理学）。

## 两脉分支

| 分支 | 关心什么 | 典型问题 |
|---|---|---|
| **Time study** | 完成任务/每步要多久；时间如何分配给各任务 | "钻孔要几秒才算合格？" |
| **Motion study** | 步骤的顺序、身体动作的细节 | "砖匠抹水泥砌一块砖最少要几下？" |

二者技术常重叠；课本为讲解方便才拆开写。

## 历史人物

- **Frederick Taylor** — "科学管理"之父，20 世纪前 25 年主导；著名例子：给某钢厂重新设计铲子使每铲正好 ~21.5 磅，年省 $78,000（~1990 美元的大价钱）。
- **Frank and Lillian Gilbreth** — 研究砖匠、残障劳动者；发明 therblig 命名法；他们保留下来的工业影片是早期工作世界的原始影像。

## Time Study 的四类常用技术

### 1. Work sampling（工作抽样）
- 先列出该岗位所有 **activities**（含"不在任务上"的理由）的清单。
- 在一段时间内，以**随机时点**观察一个或多个工人的正在做什么。
- 典型规模：两周内 2,000 次观察（Niebel, 1988）。
- 最终把频次换算成百分比，即各活动耗时占比。
- **例**：银行 teller 的 work sampling（Table 2.1）——观察 7 位 teller 在若干时点分别在做 1=兑现支票 / 2=存款 / 3=指导客户 … 8=闲置。
- **技巧**：observer 可人可摄像；有时让工人自己在电铃/beeper 随机提示时自记录（但若目的是测"脱岗时间"，工人自己不是好来源）。

### 2. Standard setting（标准用时设定）
- *Standard time* = 合格、尽责工人完成任务所**预期**的平均时间。
- 作用：激励制（打破标准即拿奖金）、方法比较（最快胜）、成本核算、生产线平衡。
- 文化风险：工人怀疑超越标准只会让管理方再紧缩标准 — 称定标者为 *quick checkers*。

### 3. Stopwatch time study（秒表时间研究）
- 分析师看 incumbent 做多次同一任务，记下每次时长。
- 取 mean / median / mode 作 *representative time*。
- **标准时 ≠ 代表时**。再乘以 *rating*（观察员判断此工人相对标准的快慢）、加上 *downtime/allowances*，才得到 *standard time*。

### 4. Predetermined time systems & Industry standard data
- **Predetermined time systems**：不必现场观察。任务拆解为已知标准用时的 *elemental motions*，逐项查表相加。
- **Industry standard data**：类似地，用 *prior tasks* 的标准用时合成新任务的标准用时。差别：predetermined 用"动作"，industry standard 用"任务/任务元素"。

## Motion Study 的核心工具

### Graphs and Flowcharts

- **例（Figure 2.1–2.2）**：医院 orderly（护工）送餐。
  - 原方法：把餐车推到房间中央，每次只拿一份送到一床 → 17 床走 436 m、用 23.42 分钟。
  - 改良方法：餐车随行，每次拿两份 → 197 m、16.98 分钟。
- *Flowchart* 用标准符号（圆=operation，箭头=transport，方=inspection，D=delay，三角=storage）串起事件序列，并与标准清单对照给出改进建议。

### Micromotion Analysis（微动作分析）

- 粒度比 flowchart 更细：**把每一步再拆成元动作**。
- 每个元动作称 **therblig**（Gilbreth 倒着拼）。
- 每个 therblig 有标准符号和颜色，配合慢动作摄影可定位到毫秒级。
- 适合分析工作台上的精细装配（如装圆珠笔、iPhone）。
- **Table 2.2 示例 therbligs**：Search（"手或眼在找东西"，如从堆里找零件）；Select（从一堆同类中挑特定件）；Grasp（把手指合拢夹住物件）。
- 另还有 Reach, Move, Position, Hold, Release, Transport Loaded, Transport Empty, Assemble, Disassemble, Use, Inspect, Plan, Pre-position, Rest-for-overcoming-fatigue, Unavoidable Delay, Avoidable Delay 等（课本未全部展示）。

### Recording techniques

- 胶片 / 摄像机 / 延时摄影（一小时浓缩到四分钟）。
- 特殊传感器：如钻床上的 *dynamometer* 测扭矩，用以兼顾钻速与钻头寿命。

## 对 T&M 研究的批评与辩护

- 著名讽刺：若让工业工程师"优化"交响乐——"号器的重复段可剪；整场 2 小时压缩到 20 分钟就够了。" （Anonymous, 1955, p. 3）
- Taylor 本意：管理层应与劳工共享效率收益；实际常变成"少雇点人"。
- 服务业占比上升 → 表面看不再相关；但全球制造仍广泛应用，且 **Toyota Production System**（丰田生产方式）仍以它为底层。
- 课本辩护：此法初衷是**提升生产力**——见 orderly 送餐案例，工人与服务都受益；还可用于设计机器/机器人接手危险/高压任务。
- 心理层面的"tricky"：设标会引发劳资博弈；工人可能故意"不打破标准"。

## 何时会在其他章节再见

- 第 5 章 *work design*：把"工作有趣、人性化"作目标，和 T&M 的"最快最省"形成张力。
- 第 7 章：工作再设计扩展到工作情境（work context）与岗位间连接。
- Morgeson & Humphrey 2006；Parker 2014；Parker & Wall 1998 等引用。

## 与其他三方法的边界

- **不叫 FJA 的原因**：T&M 不需要 data/people/things 的功能分类，只管"动作序列"和"时长"。
- **不叫 Task Inventory**：不靠大规模问卷，靠现场观察 + 精细测量。
- **和 CIT 的区别**：CIT 写*事件*（某次车火被扑灭），T&M 量*重复动作的时间/顺序*——不关心"事件"好坏。
