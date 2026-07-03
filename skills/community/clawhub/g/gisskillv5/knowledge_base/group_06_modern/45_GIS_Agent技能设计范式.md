# GIS Agent 技能设计范式 | 关联：←→ SKILL.md, ←→ 43_格式选择决策树与反模式.md, ←→ 41_现代GIS数据处理管道.md, ←→ 27_AI_GIS.md, ←→ 37_自进化反馈机制.md

> **群组六：现代GIS技术栈与知识库扩展 | 文件编号：45**
> 最后更新：2026-06-04 | 验证级别：专家级（Expert） | 版本：V5.0
> 核心定位：总结GIS领域的Agent/Skill设计模式与最佳实践，为GIS自动化工作流和Agent开发提供设计参考

---

## 目录

1. [GIS Agent 能力模型](#一gis-agent-能力模型)
2. [GIS Skill 模块化设计范式](#二gis-skill-模块化设计范式)
3. [常见GIS Agent设计模式](#三常见gis-agent设计模式)
4. [GIS Agent 提示词工程](#四gis-agent-提示词工程)
5. [GIS 自动化工作流设计](#五gis-自动化工作流设计)
6. [GIS Skill 自进化机制](#六gis-skill-自进化机制)
7. [GIS Agent 评估框架](#七gis-agent-评估框架)
8. [未来方向](#八未来方向)

---

## 一、GIS Agent 能力模型

### 1.1 核心能力分类

GIS Agent 的能力可划分为五大核心域，每个域内又分为基础、中级、高级三个层级：

| 能力域 | 基础（Level 1） | 中级（Level 2） | 高级（Level 3） |
|--------|----------------|----------------|----------------|
| **数据 I/O** | 读取Shapefile/GeoJSON，识别文件格式 | 批量格式转换（ogr2ogr管道），CRS检测与转换 | 云原生格式（COG/GeoParquet/PMTiles）流式读取，STAC目录遍历 |
| **空间分析** | 缓冲区、裁剪、空间选择 | 空间连接、叠加分析、栅格代数运算 | 热点分析（Getis-Ord Gi*）、地理加权回归（GWR）、时空序列建模 |
| **可视化** | 静态地图输出（Matplotlib/Folium） | 交互式Web地图（Leaflet/MapLibre），多图层符号化 | 三维场景渲染（Cesium/Deck.gl），动态仪表盘，大数据瓦片生成 |
| **自动化** | 单脚本批处理（ArcPy/PyQGIS） | 多步骤管道编排（Makefile/Snakemake），错误重试 | 事件驱动管道，CI/CD集成，自治数据刷新管道 |
| **知识检索** | 关键词匹配查询文档 | 语义理解+上下文联动（跨模块引用） | 因果推理链（为何出此结果→如何修复→验证），自主缺口检测与补充 |

### 1.2 能力层级模型详解

```
Level 3: 高级自治 ── 场景理解 → 策略选择 → 自主执行 → 结果解读 → 知识沉淀
    ↑ 依赖
Level 2: 中级协同 ── 工具链编排 → 跨软件互操作 → 管道异常处理
    ↑ 依赖
Level 1: 基础执行 ── 单工具操作 → 格式读写 → 基础坐标转换
```

**层级跃迁条件：**

| 从 | 到 | 跃迁条件 |
|----|----|---------|
| L1 → L2 | 能够组合多个工具完成端到端任务，例如"读取CAD→转GIS→坐标转换→质检→入库" |
| L2 → L3 | 能够理解模糊需求并自主选择最佳路径，例如"把这个区域的地形分析一下"→自动选DEM源→SAGA/GDAL→结果输出 |

### 1.3 Agent vs 传统GIS脚本

| 维度 | 传统GIS脚本 | GIS Agent |
|------|------------|-----------|
| **输入** | 明确的文件路径 + 参数列表 | 自然语言描述 + 上下文推断 |
| **容错** | 硬编码错误处理，遇到未知情况崩溃 | 异常感知 → 诊断 → 降级恢复 |
| **可塑性** | 修改需重新编码 | 通过提示词调整行为，无需改代码 |
| **知识范围** | 局限于程序员熟悉的技术栈 | 可检索跨软件、跨语言、跨标准的知识 |
| **典型规模** | 单文件脚本 50-500 行 | 知识库 32,000+ 行 + 实时检索 |
| **版本适配** | 代码硬绑定特定版本API | 通过版本差异指引动态适配（←→ SKILL.md 版本差异指引） |
| **适用场景** | 固定的、重复性的生产流程 | 探索性的、一次性的、需求模糊的任务 |
| **错误归因** | "脚本跑不了"→ 需人阅读traceback | "这个坑是 EPSG:4326 轴序问题→参考避坑库#B.04"（←→ 29_避坑库.md） |

**互补关系而非替代关系：**

```
传统脚本 ──────────────────→ GIS Agent
  ↓                              ↓
固定管道（ETL生产）          探索性任务（数据分析）
可复现性最强                  灵活性最强
      ↘                      ↙
         共存：Agent 生成脚本 → 人工审核 → 投入生产
```

---

## 二、GIS Skill 模块化设计范式

### 2.1 当前GIS Skill架构分析

当前GIS知识库V5.0采用七群组45文件体系，核心设计原则如下：

| 设计原则 | 体现 | 优势 |
|---------|------|------|
| **分层解耦** | 七群组独立维护，交叉引用代替硬耦合 | 修改基础层不影响工具层 |
| **粒度控制** | 单一文件聚焦单一主题（200-3,000行） | 检索命中率高，上下文精准 |
| **神经连接** | SKILL.md 中的 ←→ 和 ⟹ 双向/标准引用网络 | 知识可沿关联路径自动传播 |
| **版本双轨** | 主版本文件 + 差异文件（12号基础 + 38号3.7新增） | 使用者任意版本均获准确回答 |
| **自进化** | feedback/ 目录 + 37号机制文件 | 使用越多越精准 |

**文件规模分布分析：**

| 行数范围 | 文件数 | 代表 | 适合粒度 |
|---------|--------|------|---------|
| 100-300 | 8 | 01/02/04/06/08/09/10/15 | 概念定义、标准速查 |
| 300-800 | 12 | 05/14/17/18/20/22/24/27/28/32/33/37 | 单一工具/标准深度 |
| 800-1,500 | 10 | 07/12/19/21/23/29/30/39/40/41/43 | 复杂主题深度指南 |
| 1,500-3,000+ | 4 | 13/25/26/38 | 完整教材/全面重写 |

**关键洞察：** 知识库文件的黄金粒度为 500-1,500行——足够深入但不会让检索上下文过长。超过3,000行应考虑拆分为子模块。

### 2.2 模式1：分层知识库（Layered Knowledge Base）

这是本GIS Skill采用的核心架构模式。

```
层5：自进化层（37号 + feedback/）
    ↓ 反馈驱动下层更新
层4：实战层（群组五：案例28/避坑29/转换30/GNSS32/分析33）
    ↓ 提供经验验证
层3：工具层（群组三：12-38号，群组四：21-27/35号）
    ↓ 提供操作能力
层2：标准/规范层（群组二：05-10号，群组六新增：40号OGC标准）
    ↓ 提供约束与规范
层1：基础概念层（群组一：01-04号）
    ↓ 地基
```

**适用场景：** 任何专业知识库系统，尤其是涉及标准规范+工具操作+实战经验的领域。

**实施要点：**
- 上层文件必须声明对下层的引用（←→ 或 →）
- 下层文件不应直接依赖上层（避免循环引用）
- 新增知识应自下而上评估：是否需要更新基础概念？是否需要更新标准引用？

**本Skill中的体现：**
- 29_避坑库.md 中的每条避坑均引用基础层（02/03/04）和工具层（12-27），形成"问题→原因→跨模块定位→解决方案"的完整链条
- 28_项目案例集.md 引用所有软件工具文件（"依赖具体工具实现"），构成"需求→选工具→执行"的实战路径

### 2.3 模式2：场景驱动的Skill触发（Scenario-Driven Skill Routing）

**核心问题：** 用户输入是自然语言（"我想把这个shp转成西安80坐标系"），如何路由到正确的知识模块？

**路由决策流程：**

```
用户输入
    → 关键词匹配（SKILL.md §检索关键词映射表）
    → 找到1个候选文件？
        ├── 是 → 加载该文件
        └── 否 → 模糊匹配
                → 最多3个候选?
                    ├── 是 → 加载3个，交叉验证
                    └── 否 → 触发知识缺口检测（37号§K1）
```

**实际触发规则（来自SKILL.md检索关键词映射表）：**

| 用户关键词 | 主命中文件 | 辅助文件（自动联动） |
|-----------|-----------|-------------------|
| "WKID/EPSG/投影/3度带" | 02_坐标系统与投影.md | 04_中国三大坐标系实战.md |
| "CASS编码/XDATA/SOUTH" | 14_CASS11.0.md | 30_GIS↔CAD数据转换.md |
| "FME/ETL/Transformer" | 18_FME_Form与Flow.md | 43_格式选择决策树与反模式.md |
| "报错/崩溃/闪退/坑" | 29_避坑库.md | 对应软件文件 + 自进化feedback/ |
| "OGC/WMS/WFS/GeoParquet" | 40_OGC国际标准速查手册.md | 23_WebGIS开发.md / 41_现代GIS数据处理管道.md |

**关键设计原则：**
- 主命中 = 用户意图直接对应的文件
- 辅助联动 = 经验表明这些任务通常需要跨模块知识（预加载以降低检索轮次）
- 辅助联动列表从反向验证报告中更新（←→ 37号）

### 2.4 模式3：增量更新策略（Incremental Update Strategy）

**问题：** 如何在保持结构稳定的前提下持续扩展知识库？

**本Skill已实施的增量策略：**

| 策略 | 示例 | 何时使用 |
|------|------|---------|
| **版本差异双轨** | 12号(3.6主体) + 38号(3.7新增) | 软件大版本升级，基础文件太长不便内嵌 |
| **直接嵌入** | 03号新增云原生格式专节（GeoParquet/COG/PMTiles） | 内容与文件主题高度一致，增量<500行 |
| **新建立文件** | V5.0新增39-45号7个文件 | 内容形成独立主题域，>500行 |
| **避坑库追加** | 29号新增结构化反模式（WRONG/CORRECT/WHY） | 经验类知识，可与核心文件松耦合 |
| **反馈驱动补充** | 用户纠正→04号/07号直接修改 | 用户反馈的具体修正（←→ 37号§修正协议） |

**增量更新的完整决策树：**

```
新增知识需求
│
├─ 与现有文件主题高度一致？
│   ├─ 增量 < 200行 → 直接追加到目标文件末尾
│   └─ 增量 > 200行 → 是否形成独立主题域？
│       ├─ 是 → 新建文件
│       └─ 否 → 拆分为目标文件的子章节
│
├─ 属于软件版本差异？
│   └─ 是 → 主版本文件 < 2,000行?
│       ├─ 是 → 直接嵌入，标注 [vX.Y新增]
│       └─ 否 → 创建独立差异文件（双轨制）
│
└─ 属于经验/避坑类？
    └─ 是 → 追加到29号避坑库 + 追加神经连接
```

**V5.0实际执行记录：**

| 变更类型 | 涉及文件 | 行数变化 |
|---------|---------|---------|
| 直接嵌入 | 03号（云原生格式） | 222→600+行 |
| 直接嵌入 | 21号（DuckDB Spatial） | 250→800+行 |
| 直接嵌入 | 23号（PMTiles部署） | 832→1,200+行 |
| 重写 | 13号（PyQGIS全教材） | 473→3,000+行 |
| 新建 | 39-45号（群组六） | +~8,000行 |
| 删除 | 11/20/34（空占位） | -3文件 |

---

## 三、常见GIS Agent设计模式

> 以下六种设计模式均采用统一格式：**名称 / 触发条件 / 执行流程 / 代码示例 / 适用场景 / 注意事项**。

### 模式A：数据管道Agent（Data Pipeline Agent）

| 属性 | 内容 |
|------|------|
| **名称** | Pipeline Agent — 数据管道自动化 |
| **触发条件** | 用户描述数据转换需求，如"把这些shapefile转成GeoPackage并统一到CGCS2000" |
| **输入** | 源数据路径/格式 + 目标格式 + 坐标系需求 + 可选的质检规则 |
| **输出** | 转换后的数据文件 + 处理日志 + 质检报告 |

**执行流程：**

```
1. 数据探查（检测格式→统计行数/字段→检测CRS）
      ↓ [可能缺失] 进入2
2. CRS推断/确认（有.prj? 无→启发性推断：gdalinfo + 坐标值启发式）
      ↓
3. 选择处理链（根据格式决策树选工具→ ←→ 43_格式选择决策树与反模式.md）
      ↓
4. 执行转换（ogr2ogr/gdalwarp/Python → 记录日志）
      ↓
5. 验证输出（几何有效性/CRS正确/属性完整）
      ↓
6. 生成报告 + 归档
```

**代码示例（Python实现骨架）：**

```python
import geopandas as gpd
from pathlib import Path
import logging

class GISPipelineAgent:
    """数据管道Agent — 自动检测→转换→验证"""

    def inspect_source(self, path: Path) -> dict:
        """阶段1：数据探查 + 坐标系启发式检测（←→ 02_坐标系统与投影.md）"""
        gdf = gpd.read_file(path)
        crs = gdf.crs if gdf.crs else None
        bounds = gdf.total_bounds

        if crs is None:
            if -180 <= bounds[0] <= 180 and -90 <= bounds[1] <= 90:
                crs_guess = "EPSG:4326 (推断)"
            elif 100000 < bounds[0] < 10000000:
                crs_guess = "投影坐标系（推断）"
            else:
                crs_guess = "未知"
        else:
            crs_guess = str(crs)

        return {"crs": crs_guess, "cols": gdf.columns.tolist(),
                "bounds": bounds.tolist(), "row_count": len(gdf)}

    def select_pipeline(self, inspection: dict, target: dict) -> str:
        """阶段3：选择处理链（←→ 43_格式选择决策树）"""
        ext = inspection.get("format", "").lstrip(".")
        if ext == "shp" and target["format"] == "gpkg":
            return "ogr2ogr"
        elif target.get("reproject"):
            return "gdalwarp_pipeline"
        return "python_pipeline"

    def execute(self, src_path: str, target_format: str,
                target_crs: str = None) -> dict:
        """主入口：检测→选择→执行→验证"""
        inspection = self.inspect_source(Path(src_path))
        pipeline = self.select_pipeline(inspection, {"format": target_format})
        result = self._run_pipeline(pipeline, src_path, target_format, target_crs)
        self._validate_output(result, inspection["row_count"])
        return result
```

**适用场景：**
- 批量数据格式迁移（Shapefile→GeoPackage）
- 多源数据入库前的格式统一
- 云原生格式转换（GeoTIFF→COG）

**注意事项：**
- ⚠️ CRS检测是最高频的失败点——必须处理.prj缺失和轴序歧义
- ⚠️ 大文件（>1GB）应使用流式处理而非一次性加载到内存
- 参考：←→ 43号 第四节12个致命反模式、←→ 41号七大标准处理管道模式

---

### 模式B：空间分析Agent（Spatial Analysis Agent）

| 属性 | 内容 |
|------|------|
| **名称** | Analysis Agent — 空间分析需求理解与执行 |
| **触发条件** | 用户提出空间分析需求，"计算这个区域的植被覆盖变化"/"找出500米内有污染源的地块" |
| **输入** | 分析目标（自然语言） + 数据源（路径/名称/范围） |
| **输出** | 分析结果（GeoDataFrame/栅格）+ 可视化 + 分析说明 |

**执行流程：**

```
1. 需求解析（提取：分析类型/空间关系/阈值/输出格式）
      ↓
2. 算法选择（缓冲区→buffer_distance, 覆盖→zonal_stats, 变化→raster_diff, 聚类→DBSCAN/HDBSCAN）
      ↓ [参考←→ 33_空间分析与统计.md]
3. 参数推导（从数据特征自动推导合理参数：
      - 缓冲区半径：从数据范围推算（总跨度的1%~5%）
      - DBSCAN eps：k-距离图或数据范围/50
      - 插值分辨率：点密度推算）
      ↓
4. 数据准备（CRS统一为投影坐标系以保证度量单位正确）
      ↓
5. 执行分析
      ↓
6. 结果解读（统计摘要 + 异常检测 + 推荐下一步）
```

**代码示例（自然语言→分析执行）：**

```python
def parse_analysis_intent(query: str) -> dict:
    """解析空间分析意图——关键词→分析类型→参数"""
    intents = {
        "缓冲区": {"type": "buffer", "params": ["distance"]},
        "叠加": {"type": "overlay", "params": ["layers"]},
        "最近": {"type": "nearest", "params": ["k", "max_distance"]},
        "热点": {"type": "hotspot", "params": ["method"]},
        "变化": {"type": "change_detection", "params": ["baseline", "target"]},
        "聚类": {"type": "clustering", "params": ["eps", "min_samples"]},
    }
    for keyword, intent in intents.items():
        if keyword in query:
            return intent
    return {"type": "unknown"}

def auto_derive_parameters(gdf, analysis_type: str) -> dict:
    """从数据特征自动推导合理参数"""
    bounds = gdf.total_bounds
    extent = max(bounds[2] - bounds[0], bounds[3] - bounds[1])
    heuristics = {
        "buffer": {"distance": extent * 0.02},
        "nearest": {"k": min(5, len(gdf))},
        "clustering": {"eps": extent / 50, "min_samples": max(3, int(len(gdf) * 0.01))},
    }
    return heuristics.get(analysis_type, {})
```

**适用场景：**
- 环境影响评估（缓冲区/叠加分析）
- 城市规划分析（可达性/覆盖范围）
- 自然资源监测（变化检测）

**注意事项：**
- ⚠️ **关键陷阱**：绝对禁止在EPSG:4326（经纬度）坐标上直接做距离运算（←→ 43号反模式#2）
- ⚠️ 分析前必须将数据投影到合适的投影坐标系（UTM或Albers等面积）
- ⚠️ 大数据量使用DuckDB Spatial分析（单机5,000万条记录）而非GeoPandas加载全量

---

### 模式C：可视化Agent（Visualization Agent）

| 属性 | 内容 |
|------|------|
| **名称** | Visualization Agent — 智能地图/图表生成 |
| **触发条件** | 用户描述可视化需求，"把这个结果显示在地图上"/"做一个热力图" |
| **输入** | 数据 + 可视化需求描述 |
| **输出** | HTML地图/PNG图片/交互式仪表盘 |

**执行流程：**

```
1. 理解可视化需求
   ├─ "地图" → 空间可视化
   ├─ "图表" → 统计图表（柱状/折线/散点）
   ├─ "热力图" → 密度图或插值热力图
   └─ "时间" → 时序动画或时间滑块
      ↓
2. 数据类型检测
   ├─ 点数据 → 散点图/热力图/聚类图
   ├─ 线数据 → 流向图/路网图
   ├─ 面数据 → 分级统计图(choropleth)
   └─ 栅格数据 → 伪彩色/山影渲染
      ↓
3. 渲染引擎选择
   ├─ 静态输出 (< 1000要素) → Matplotlib/GeoPandas.plot()
   ├─ Web交互 (1000-10万要素) → Folium/Leaflet
   ├─ 大数据Web (>10万要素) → MapLibre + MVT/PMTiles
   └─ 三维场景 → Cesium/Deck.gl/PyDeck
      ↓
4. 符号化策略自动选择
   ├─ 分类数据 → 定性配色（Set3/Paired）
   ├─ 连续数据 → 渐变配色（viridis/plasma）
   ├─ 离散分级 → Jenks Natural Breaks / Quantile
   └─ 自定义分类 → 按用户指定阈值
      ↓
5. 生成 + 预览
```

**代码示例（智能地图生成）：**

```python
import folium
import geopandas as gpd
import numpy as np

def smart_map(gdf):
    """智能地图生成——自动选择渲染策略（←→ 23_WebGIS开发.md）"""
    # 策略选择 + CRS安全检查
    engine = "pmtiles" if len(gdf) > 100000 else "folium"
    if gdf.crs and gdf.crs.is_geographic:
        gdf = gdf.to_crs(epsg=4326)  # Web地图必须WGS84

    geom_type = gdf.geometry.geom_type.iloc[0]
    num_cols = gdf.select_dtypes(include=[np.number]).columns

    if engine == "folium":
        center = [gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()]
        m = folium.Map(location=center, zoom_start=10, tiles="CartoDB Positron")

        if geom_type == "Point":
            for _, row in gdf.iterrows():
                folium.CircleMarker(
                    location=[row.geometry.y, row.geometry.x],
                    radius=5, color="#3182bd", fill=True
                ).add_to(m)
        elif geom_type in ("Polygon", "MultiPolygon") and len(num_cols) > 0:
            folium.Choropleth(
                geo_data=gdf, data=gdf, columns=[gdf.index.name or "index", num_cols[0]],
                key_on="feature.id", fill_color="YlOrRd"
            ).add_to(m)
        else:
            folium.GeoJson(gdf).add_to(m)
        return m
```

**适用场景：**
- 数据探索阶段快速可视化
- 项目成果展示地图
- 交互式分析仪表盘

**注意事项：**
- ⚠️ 大数据量（>10万要素）直接用folium/leaflet GeoJSON会导致浏览器崩溃——必须瓦片化
- ⚠️ 坐标系：Web可视化始终需要EPSG:4326或EPSG:3857（Web墨卡托）
- 符号化配色建议使用ColorBrewer配色方案，确保色盲友好

---

### 模式D：故障诊断Agent（Diagnostic Agent）

| 属性 | 内容 |
|------|------|
| **名称** | Diagnostic Agent — GIS故障诊断与修复 |
| **触发条件** | 用户报告错误："报错了"/"闪退"/"坐标偏了好多"/"中文乱码" |
| **输入** | 错误信息（截图/文本/现象描述） + 操作上下文 |
| **输出** | 根因分析 + 修复步骤 + 预防建议 |

**执行流程：**

```
1. 错误提取（解析traceback/错误码/现象关键词）
      ↓
2. 模式匹配（匹配避坑库160+条目 → ←→ 29_避坑库.md）
      ↓
3. 命中？
   ├── 精确命中 → 给出 WRONG/CORRECT/WHY 结构化答案
   ├── 近似命中 → 给出最可能的3个原因 + 诊断命令
   └── 未命中 → 记录为新知识缺口（←→ 37号§K1）
                  → 提示用户提供更多信息（软件版本/数据格式/CRS）
      ↓
4. 生成诊断报告
```

**代码示例（诊断引擎骨架）：**

```python
class GISDiagnosticAgent:
    """GIS故障诊断Agent — 错误模式匹配 + 避坑库检索（←→ 29_避坑库.md）"""

    def __init__(self):
        self.patterns = [
            {"keywords": ["乱码", "GBK", "UTF-8", "编码"],
             "diagnosis": "编码问题（CASS DWG中文属性乱码或Shapefile .dbf编码错误）",
             "fix": "SHAPE_ENCODING='UTF-8' 或 ogr2ogr -lco ENCODING=UTF-8"},
            {"keywords": ["偏移", "飞图", "坐标不对", "偏了"],
             "diagnosis": "坐标系/投影不一致—用错了带号或混淆了GCS/PCS",
             "fix": "确认源坐标系→gdalwarp/ogr2ogr重投影"},
            {"keywords": ["2GB", "文件太大", "exceeds"],
             "diagnosis": "Shapefile 2GB限制（←→ 43号反模式#0）",
             "fix": "ogr2ogr -f GPKG output.gpkg input.shp"},
            {"keywords": ["ERROR 999999", "ArcPy"],
             "diagnosis": "ArcGIS数据锁/权限/无效输入",
             "fix": "关闭ArcGIS Pro→删除.gdb/*.lock文件"},
        ]

    def diagnose(self, error_text: str) -> dict:
        results = []
        for p in self.patterns:
            score = sum(1 for kw in p["keywords"] if kw.lower() in error_text.lower())
            if score > 0:
                results.append({"score": score, **p})

        if results:
            results.sort(key=lambda x: x["score"], reverse=True)
            return {"status": "matched", "candidates": results[:3]}
        return {"status": "unknown",
                "suggestion": "请提供：软件名称/版本、数据格式、操作步骤、完整错误信息"}
```

**适用场景：**
- GIS软件报错排查
- 数据质量问题诊断
- 批量处理失败后的根因分析

**注意事项：**
- 诊断Agent的准确率取决于错误模式库的覆盖度——需要持续积累（←→ 37_自进化反馈机制.md）
- 诊断结果应提供可执行的修复命令，而非笼统建议
- 未知错误应触发反馈收集，帮助扩展模式库

---

### 模式E：格式转换Agent（Format Conversion Agent）

| 属性 | 内容 |
|------|------|
| **名称** | Conversion Agent — 智能格式检测与转换 |
| **触发条件** | 用户需要格式转换，"shp转gpkg"/"CAD转GIS"/"geotiff转COG" |
| **输入** | 源文件路径 + 目标格式（可选，不提供则自动推荐） |
| **输出** | 转换后文件 + 转换日志 + 数据完整性验证报告 |

**执行流程：**

```
1. 源格式自动检测（扩展名→GDAL驱动→内部结构验证）
      ↓
2. 目标格式推荐（不指定时：使用格式决策树自动推荐 ←→ 43号 §一）
      ↓
3. 生成转换脚本（GDAL/FME/Python — 根据复杂度自动选择工具）
      ↓
4. 执行转换
      ↓
5. 完整性验证
      ├─ 要素数一致？
      ├─ 属性字段完整？
      ├─ CRS正确传递？
      └─ 几何有效性检查
      ↓
6. 输出报告
```

**代码示例（智能格式转换）：**

```python
class FormatConversionAgent:
    """智能格式检测与转换（←→ 43号决策树 + ←→ 30_GIS↔CAD数据转换.md）"""
    CONVERSION_MAP = {
        ".shp": "ogr2ogr -f GPKG {out} {in}",
        ".gdb": "ogr2ogr -f GPKG {out} {in}",
        ".tif": "gdal_translate -of COG -co COMPRESS=LZW {in} {out}",
        ".dwg": "ogr2ogr -f GPKG {out} {in} -nlt PROMOTE_TO_MULTI",
    }

    def recommend_target(self, use_case: str = "general") -> str:
        """根据用途推荐目标格式"""
        return "gpkg" if use_case in ("general", "archive") else "parquet"

    def validate_output(self, source: Path, target: Path) -> dict:
        """验证转换完整性"""
        src, tgt = gpd.read_file(source), gpd.read_file(target)
        return {
            "feature_count_match": len(src) == len(tgt),
            "field_count_match": len(src.columns) == len(tgt.columns),
            "crs_match": str(src.crs) == str(tgt.crs) if src.crs else "no_source_crs",
        }

    def convert(self, source_path: str, target_format: str = None) -> dict:
        src = Path(source_path)
        ext = src.suffix.lower()
        target_format = target_format or self.recommend_target()
        target_path = src.with_suffix(f".{target_format}")
        cmd = self.CONVERSION_MAP.get(ext, "ogr2ogr -f GPKG {out} {in}").format(
            out=target_path, _in=src)
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            return {"status": "error", "error": result.stderr}
        return {"status": "success", "target": str(target_path),
                "validation": self.validate_output(src, target_path)}
```

**适用场景：**
- CAD↔GIS互转（←→ 30_GIS↔CAD数据转换.md）
- Shapefile→GeoPackage批量迁移
- 云原生格式转换（GeoTIFF→COG, MBTiles→PMTiles）

**注意事项：**
- ⚠️ CAD到GIS转换需要特别注意XDATA/CASS_CODE等扩展属性（←→ 14_CASS11.0.md）
- ⚠️ 坐标系传递是常见失败点——GDAL的默认CRS行为需要显式验证
- ⚠️ 大文件转换使用 `-skipfailures` 避免单条记录错误导致整体失败

---

### 模式F：代码生成Agent（Code Generation Agent）

| 属性 | 内容 |
|------|------|
| **名称** | CodeGen Agent — 自然语言→GIS代码生成 |
| **触发条件** | 用户用自然语言描述数据处理需求，"帮我写一段PyQGIS代码来..." |
| **输入** | 功能描述（自然语言） + 上下文（软件/库/数据格式） |
| **输出** | 可执行代码片段 + 依赖说明 + 注意事项 |

**执行流程：**

```
1. 需求结构化提取
   ├─ 工具/库识别 → PyQGIS/ArcPy/GDAL/GeoPandas/PostGIS
   ├─ 数据源格式 → Shapefile/GeoPackage/PostGIS表/COG
   └─ 操作类型 → 读取/查询/转换/分析/导出
      ↓
2. 代码模板匹配（从知识库中检索最接近的代码模板）
   ├─ 21_Python_GIS生态.md  → GeoPandas/GDAL/Rasterio
   ├─ 13_QGIS.md            → PyQGIS脚本
   ├─ 12_ArcGIS_Pro.md      → ArcPy脚本
   └─ 44_QGIS_Processing算法速查手册.md → Processing算法完整ID
      ↓
3. 参数填充（从自然语言中提取具体值填入模板）
      ↓
4. 安全检查
   ├─ 坐标系安全？（距离/面积运算前确认投影坐标系）
   ├─ 性能安全？（全量加载大数据？提示用DuckDB/chunksize）
   └─ 格式安全？（输出格式是否为2026推荐格式←→ 43号）
      ↓
5. 输出代码 + 注释
```

**代码示例（需求→代码）：**

```python
# 用户："用GeoPandas读取文件夹下所有shapefile，合并并转成CGCS2000 3度带39带"
# Agent生成：

import geopandas as gpd
from pathlib import Path

# 1. 读取 + 合并
gdfs = [gpd.read_file(f) for f in Path("./data").glob("*.shp")]
merged = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True))

# 2. CRS检测 + 转换到 CGCS2000 / 3度带 zone 39 (EPSG:4538)
if merged.crs is None:
    raise ValueError("源数据无坐标系信息！先用 gdalinfo 检查")

print(f"源坐标系: {merged.crs}")
target_crs = "EPSG:4538"
if merged.crs != target_crs:
    merged = merged.to_crs(target_crs)

# 3. 保存（2026年推荐GeoPackage，非Shapefile ←→ 43号）
merged.to_file("merged_output.gpkg", driver="GPKG")
print(f"合并完成：{len(merged)} 个要素 → merged_output.gpkg")
```

**适用场景：**
- 快速原型开发
- 教学演示
- 一次性数据分析脚本

**注意事项：**
- ⚠️ 生成的代码必须包含坐标系安全检查和格式推荐
- ⚠️ 应标注代码来源库版本要求（如 Shapely 2.x / GDAL 3.8+）
- 生成的代码可作为"初稿"而非"最终生产代码"——用户需根据实际环境调整

---

## 四、GIS Agent 提示词工程

### 4.1 GIS领域的提示词设计原则

| 原则 | 说明 | 反例 | 正例 |
|------|------|------|------|
| **精确性** | 明确指定EPSG代码而非"常用坐标系" | "用常用坐标系" | "转换为EPSG:4538 (CGCS2000/3度带39带)" |
| **坐标系敏感** | 任何距离/面积运算前必须显式声明投影坐标系 | "buff 500米" | "先重投影到EPSG:32650 (WGS84/UTM zone 50N)，再buffer 500米" |
| **格式意识** | 2026年推荐格式优先于历史格式 | "保存为shp文件" | "保存为GeoPackage (.gpkg)，Shapefile已弃用" |
| **性能预估** | 大数据量提示使用合适工具 | "用Python循环处理" | "数据量超过100万条→建议使用DuckDB Spatial或PostGIS" |
| **可复现** | 代码中包含版本号和依赖列表 | "import geopandas" | "geopandas>=0.14, Shapely>=2.0, GDAL>=3.8" |

### 4.2 关键陷阱

#### 陷阱1：坐标系歧义 — EPSG:4326轴序问题

```python
# ❌ WRONG: 假设EPSG:4326轴序为(lon, lat)
point = Point(116.397, 39.908)  # 这可能是(经度, 纬度)或(纬度, 经度)！

# ✓ CORRECT: 明确指定轴序
# GeoJSON标准：总是(lon, lat) → (x, y)
# EPSG:4326在OGC标准中：(lat, lon) → (y, x)
# 解决方案：始终使用 x=lon, y=lat 并确保CRS声明一致
```

**WHY：** CRS:84（经度在前）和EPSG:4326（纬度在前）的轴序歧义是GIS Agent最常见的错误。GeoJSON/RFC 7946规定使用CRS:84轴序(lon,lat)，而EPSG官方定义4326为(lat,lon)。GeoPandas/Shapely在内部使用(lon,lat)，但QGIS Server使用(lat,lon)。不同工具、不同版本的默认行为不一致。

#### 陷阱2：格式假设 — Agent最常犯的格式错误

| Agent常见错误 | 正确做法 | 相关反模式 |
|-------------|---------|-----------|
| 默认输出Shapefile | 2026年新项目默认用GeoPackage | ←→ 43号 §反模式#1 |
| 用GeoJSON传输GB级数据 | 用GeoParquet或FlatGeobuf | ←→ 43号 §1.1决策树 |
| 假设所有GIS库支持Shapefile | 检查库的兼容性表 | ←→ 21号/39号 |
| 用WMS而非PMTiles做Web底图 | 2026年推荐PMTiles（零服务器） | ←→ 23号/43号 |

#### 陷阱3：性能盲区 — 低估大数据量的成本

```python
# ❌ WRONG: 全量加载 → 内存溢出
gdf = gpd.read_file("30GB_data.parquet")  # 直接加载30GB！
gdf["area"] = gdf.geometry.area           # 计算全量面积

# ✓ CORRECT: DuckDB Spatial 列式查询 + 谓词下推
import duckdb
conn = duckdb.connect()
conn.execute("""
    INSTALL spatial; LOAD spatial;
    SELECT ST_Area(geometry) AS area
    FROM '30GB_data.parquet'
    WHERE ST_Intersects(
        geometry,
        ST_GeomFromText('POLYGON((...bounding_box...))')
    )
    LIMIT 10000
""")
```

**关键数据量阈值（Agent决策参考）：**

| 数据量 | 推荐工具 | 原因 |
|--------|---------|------|
| < 100MB | GeoPandas/Fiona | 单机内存足够 |
| 100MB - 5GB | GeoPandas + chunksize / DuckDB Spatial | 分块或列式处理 |
| 5GB - 50GB | DuckDB Spatial（首选） / PostGIS | 列式压缩 + 谓词下推 |
| > 50GB | Apache Sedona / PostGIS + 分区表 | 分布式或数据库分区 |

#### 陷阱4：CRS/基准面混淆

```
常见混淆链：
  用户说"WGS84坐标"
  → 可能是：WGS84(G1762) / WGS84(G1150) / WGS84(G730) / ITRF2014@2005.0
  → 不同版本的WGS84与CGCS2000转换参数不同
  → Agent应追问：
    1. 数据年份？（决定WGS84版本）
    2. 精度要求？（米级/分米级/厘米级）
    3. 区域？（不同区域的七参数不同）
```

### 4.3 提示词模板库

#### 模板1：数据转换完整提示词

```
## 任务
将 [源格式] 数据转换为 [目标格式]，并统一坐标系到 [目标CRS]。

## 数据信息
- 源文件路径：[path]
- 源格式：[shp/gdb/geojson/tif/dwg]
- 源坐标系：[已知/未知/自动检测]
- 数据量：[行数/文件大小]
- 属性语言：[中文/英文/混合]

## 要求
- 目标格式：[gpkg/parquet/cog/pmtiles/geojson]
- 目标坐标系：[EPSG:xxxx]
- 编码：[UTF-8/GBK]
- 几何类型：[保持/转换为Multi*]

## 约束
- 不能使用Shapefile作为中间/输出格式（2026年已弃用 ←→ 43号）
- 坐标系检测失败时先输出诊断信息再手动指定
- 大文件（>1GB）使用流式处理
- 转换后验证：要素数一致/属性完整/CRS正确/几何有效

## 期望输出
1. 转换命令/脚本（可直接执行）
2. 预期日志示例
3. 验证清单
```

#### 模板2：空间分析完整提示词

```
## 任务
对 [数据源] 执行空间分析：[分析描述]。

## 数据信息
- 数据文件/图层：[path/layer_name]
- 数据类型：[点/线/面/栅格]
- 数据量级：[行数/分辨率]
- 坐标系：[当前CRS]

## 分析需求
- 分析类型：[缓冲区/叠加/最近邻/热点/聚类/变化检测]
- 关键参数：[距离/阈值/时间窗口]
- 分析范围：[全局/Bbox/行政区]

## 约束
- 距离运算前必须重投影到投影坐标系（禁止在EPSG:4326上计算距离 ←→ 43号反模式#2）
- 大数据量使用DuckDB Spatial而非GeoPandas全量加载
- 结果CRS与输入保持一致（除非用户指定）

## 期望输出
1. 完整的分析代码（含安全检查）
2. 中间结果说明
3. 最终结果摘要（统计信息）
4. 可选的可视化代码
```

#### 模板3：地图生成完整提示词

```
## 任务
将 [数据] 可视化为 [交互式/静态] 地图。

## 数据信息
- 数据源：[path/layer_name]
- 要素数量：[行数]
- 几何类型：[点/线/面]
- 坐标系：[当前CRS，需转换为EPSG:4326]

## 可视化需求
- 地图类型：[散点/分级统计/热力图/流向/3D]
- 符号化字段：[分类字段/数值字段]
- 底图：[OpenStreetMap/CartoDB/自定义瓦片/无底图]
- 交互需求：[缩放/弹窗/筛选/时间滑块]

## 约束
- 要素>10万 → 使用PMTiles/MapLibre而非GeoJSON直传
- 配色使用ColorBrewer方案（色盲友好）
- Web地图必须转为EPSG:4326（leaflet）或EPSG:3857（MapLibre）

## 期望输出
1. 完整HTML文件（如果是Web地图）或PNG（如果是静态图）
2. 符号化图例说明
3. 大数据量的瓦片化方案（如适用）
```

#### 模板4：故障诊断完整提示词

```
## 任务
诊断 GIS 操作中的错误/异常。

## 错误信息
- 完整错误消息：[pasted error text]
- 软件及版本：[QGIS 3.40 / ArcGIS Pro 3.7 / GDAL 3.8]
- 执行的操作：[描述操作步骤]
- 数据信息：[格式/大小/坐标系]

## 系统环境
- 操作系统：[Windows 10/11 / Ubuntu 22.04]
- 安装方式：[独立安装/conda/pip]
- 中文路径/特殊字符：[是/否]

## 期望输出
1. 根因分析（WHY：为什么发生此错误）
2. 解决方案（可执行的修复步骤）
3. 验证方法（如何确认问题已解决）
4. 预防措施（如何避免再次发生）
5. 如无法确定：请求补充哪些信息
```

---

## 五、GIS 自动化工作流设计

### 5.1 工作流编排模式

| 编排模式 | 结构 | GIS典型场景 | 工具推荐 |
|---------|------|-----------|---------|
| **顺序** | A → B → C | ETL管道：读取→清洗→转换→入库 | Makefile / Snakemake / Airflow |
| **并行** | A, B 同时运行 | 多区域独立处理、多波段分别分析 | GNU parallel / Python multiprocessing / Dask |
| **条件分支** | if X → A else → B | 根据数据格式/CRS选择不同处理路径 | Python if/else + subprocess |
| **循环** | for item in list → A(item) | 批量文件处理、多时相分析 | for loop / Snakemake wildcards |
| **扇出扇入** | A → [B1,B2,B3] → C | 分块处理→并行→合并结果 | Dask / Ray |

### 5.2 Agent编排 vs 传统ETL适用场景对比

| 维度 | Agent编排 | 传统ETL (FME/GDAL脚本) |
|------|---------|----------------------|
| **启动成本** | 低（自然语言描述即可） | 中-高（需要编写转换规则/Workbench模型） |
| **灵活性** | 高（可动态调整处理逻辑） | 低-中（变更需修改脚本/模型） |
| **可复现性** | 中（依赖Agent版本和行为） | 高（固定代码/模型版本锁定） |
| **处理吞吐量** | 中-高（可调用底层工具） | 高（FME引擎优化 / GDAL原生性能） |
| **错误处理** | 中（依赖诊断Agent模式） | 高（FME内置错误路由 / try-except） |
| **适用场景** | 探索性任务、需求模糊、一次性处理 | 生产流水线、合规要求、例行处理 |
| **最佳实践** | Agent生成脚本 → 人工审核 → 投入生产 | 直接使用标准ETL工具开发 |

**决策建议：**

```
需要自动化GIS工作流？
│
├─ 需求明确、重复执行、高可靠性要求？
│   └─ 传统ETL（FME/GDAL脚本/Snakemake）
│       └─ Agent辅助：用Agent生成脚本初稿 → 人工调优 → 版本锁定
│
├─ 需求模糊、探索性、一次性？
│   └─ Agent编排（自然语言→Agent执行）
│       └─ 执行后人工验证结果 → 提炼为标准脚本
│
└─ 混合模式：Agent生成管道模板 + 人工审核参数 → 注入传统ETL
```

### 5.3 典型工作流案例

#### 案例1：OSM数据下载→清洗→入库→发布全自动

**管道架构：**

```
OSM API / Geofabrik / Overture Maps
    ↓ 阶段1：下载
    ├─ wget/curl 下载 .osm.pbf（或从Overture Maps S3直接读取GeoParquet）
    ↓ 阶段2：清洗
    ├─ osmium-tool 提取目标要素类型（道路/建筑/POI）
    ├─ ogr2ogr 过滤无效几何 + 删除空属性
    ├─ 坐标系转换 WGS84 → CGCS2000/投影
    ↓ 阶段3：入库
    ├─ ogr2ogr → PostGIS（建空间索引/属性索引）
    └─ 或：ogr2ogr → DuckDB Spatial（列式分析）
    ↓ 阶段4：发布
    ├─ Martin / pg_tileserv → MVT矢量瓦片
    └─ 或：tippecanoe → PMTiles（零服务器部署到S3/CDN）
```

**完整代码（结合Agent生成+脚本固化）：**

```bash
#!/bin/bash
# OSM自动管道（下载→清洗→入库→发布）
set -euo pipefail

REGION="beijing"
DATE=$(date +%Y%m%d)
WORK_DIR="./osm_${DATE}"
mkdir -p "$WORK_DIR"

# 1. 下载
wget -q "https://download.geofabrik.de/asia/china/${REGION}-latest.osm.pbf" \
     -O "${WORK_DIR}/${REGION}.osm.pbf"

# 2. 清洗 + 格式转换 + 重投影
osmium tags-filter "${WORK_DIR}/${REGION}.osm.pbf" \
    w/highway=motorway,trunk,primary,secondary \
    -o "${WORK_DIR}/roads.osm.pbf"

ogr2ogr -f GPKG "${WORK_DIR}/roads.gpkg" \
    "${WORK_DIR}/roads.osm.pbf" lines -t_srs EPSG:4538 -nln roads \
    -sql "SELECT osm_id, highway, name FROM lines WHERE highway IS NOT NULL"

# 3. 入库 PostGIS
ogr2ogr -f PostgreSQL "PG:host=localhost dbname=gis" \
    "${WORK_DIR}/roads.gpkg" roads -nln osm_roads -overwrite
psql -d gis -c "CREATE INDEX IF NOT EXISTS idx_osm_roads_geom ON osm_roads USING GIST(geom);"

# 4. 发布PMTiles（←→ 23_WebGIS开发.md）
tippecanoe -o "${WORK_DIR}/roads.pmtiles" -zg --drop-densest-as-needed "${WORK_DIR}/roads.gpkg"

echo "完成：${WORK_DIR}/roads.pmtiles (可直传S3/CDN, MapLibre加载)"
```

#### 案例2：卫星影像自动检索→下载→预处理→COG转换

**管道架构：**

```
STAC API（Sentinel-2 / Landsat 目录）
    ↓ 阶段1：检索
    ├─ pystac-client 按时间/Bbox/云量筛选
    ↓ 阶段2：下载
    ├─ stac-asset 并行下载指定波段（红/绿/蓝/NIR）
    ↓ 阶段3：预处理
    ├─ gdalwarp 重投影 + 裁剪到AOI
    ├─ gdal_merge.py 波段融合（RGB/NRG）
    ├─ gdaldem 直方图均衡 + 拉伸
    ↓ 阶段4：COG转换
    ├─ gdal_translate -of COG + 添加overviews
    ↓ 阶段5：发布
    └─ 上传到S3/Cloudflare R2 → TiTiler 动态渲染或 MapLibre 前端加载
```

**关键代码片段：**

```python
# STAC检索 + COG转换管道（←→ 41号 §七大标准处理管道模式 管道4）
import pystac_client
import planetary_computer
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

def search_and_convert_to_cog(aoi_geojson: dict, date_range: tuple, output_dir: str):
    """检索Sentinel-2影像并转换为COG"""

    # 阶段1：STAC检索
    catalog = pystac_client.Client.open(
        "https://planetarycomputer.microsoft.com/api/stac/v1",
        modifier=planetary_computer.sign_inplace
    )

    search = catalog.search(
        collections=["sentinel-2-l2a"],
        intersects=aoi_geojson,
        datetime=f"{date_range[0]}/{date_range[1]}",
        query={"eo:cloud_cover": {"lt": 10}},
        limit=3
    )

    items = list(search.item_collection())

    # 阶段2-4：下载→预处理→COG（←→ 43号 §1.2栅格决策树）
    for item in items:
        red_band = planetary_computer.sign(item.assets["B04"].href)
        with rasterio.open(red_band) as src:
            # 计算目标CRS的转换参数（←→ 02_坐标系统与投影.md）
            transform, width, height = calculate_default_transform(
                src.crs, "EPSG:32650",  # WGS84 / UTM zone 50N
                src.width, src.height, *src.bounds
            )

            # 重投影并输出为COG
            kwargs = src.meta.copy()
            kwargs.update({
                "crs": "EPSG:32650", "transform": transform,
                "width": width, "height": height,
                "driver": "COG", "compress": "DEFLATE"
            })

            with rasterio.open(f"{output_dir}/band_B04_cog.tif", "w", **kwargs) as dst:
                for i in range(1, src.count + 1):
                    reproject(
                        source=rasterio.band(src, i),
                        destination=rasterio.band(dst, i),
                        src_transform=src.transform, src_crs=src.crs,
                        dst_transform=transform, dst_crs="EPSG:32650",
                        resampling=Resampling.bilinear
                    )

    return len(items)
```

#### 案例3：多源数据融合→空间分析→报告生成

**管道架构：**

```
多源输入
├─ 矢量：行政区划.gpkg + 监测站点.gpkg
├─ 栅格：DEM_COG.tif + 土地利用.tif
├─ 气象：NetCDF时序数据
└─ 统计：CSV表格数据
    ↓ 阶段1：空间融合
    ├─ CRS统一到目标投影坐标系
    ├─ 矢量-栅格叠加（zonal_stats）
    ├─ 时空对齐（NetCDF→GeoDataFrame时间切片）
    └─ 属性连接（CSV join on 站点ID）
    ↓ 阶段2：空间分析
    ├─ 缓冲分析（污染源500m影响范围）
    ├─ 地形分析（坡度/坡向/高程分区）
    ├─ 空间统计（Moran's I / GWR）
    └─ 变化检测（多时相对比）
    ↓ 阶段3：报告生成
    ├─ 分析结果汇总表（GeoDataFrame→HTML表格）
    ├─ 地图渲染（Folium/MapLibre）
    ├─ 统计图表（Matplotlib/Plotly）
    └─ 整合为Markdown报告
```

**关键代码片段（←→ 19_多源数据融合.md, ←→ 33_空间分析与统计.md）：**

```python
# 多源数据融合管道
import geopandas as gpd
import rasterio
import numpy as np
from rasterstats import zonal_stats

def multi_source_fusion_pipeline(admin_path, sites_path, dem_path, output_report):
    """多源数据融合→分析→报告"""

    # 阶段1：加载 + CRS统一
    admin = gpd.read_file(admin_path)
    sites = gpd.read_file(sites_path)
    target_crs = "EPSG:4538"  # CGCS2000 / 3度带39带

    admin = admin.to_crs(target_crs)
    sites = sites.to_crs(target_crs)

    # 阶段2：空间融合（矢量 + 栅格）
    # 计算各站点缓冲区内的平均高程
    with rasterio.open(dem_path) as dem_src:
        dem_array = dem_src.read(1)
        dem_transform = dem_src.transform

    stats = zonal_stats(
        sites, dem_path,
        stats="mean min max std",
        geojson_out=True
    )
    sites_enriched = gpd.GeoDataFrame.from_features(stats)
    sites_enriched = sites_enriched.set_crs(target_crs)

    # 阶段3：空间分析 — 热点分析（←→ 33号 §Moran's I）
    from esda.moran import Moran
    w = weights.distance.KNN.from_dataframe(sites_enriched, k=8)
    moran = Moran(sites_enriched["mean"], w)

    # 阶段4：生成Markdown报告
    report = f"""# 多源数据融合分析报告

## 一、数据概况
- 行政区划数量：{len(admin)}
- 监测站点数量：{len(sites)}
- DEM分辨率：{dem_src.res}
- 目标坐标系：{target_crs}

## 二、空间统计
- Moran's I = {moran.I:.3f} (p = {moran.p_sim:.4f})
  → {"存在显著空间自相关" if moran.p_sim < 0.05 else "空间分布趋于随机"}

## 三、高程统计
- 最低高程：{sites_enriched["min"].min():.1f}m
- 最高高程：{sites_enriched["max"].max():.1f}m
- 平均高程：{sites_enriched["mean"].mean():.1f}m
"""
    with open(output_report, "w", encoding="utf-8") as f:
        f.write(report)

    return report
```

---

## 六、GIS Skill 自进化机制

> 本节详细说明当前GIS Skill V5.0已实施的自进化机制（←→ 37_自进化反馈机制.md），并扩展为Agent设计的一般范式。

### 6.1 反向验证驱动的优化循环

当前GIS Skill V5.0的核心进化方法论：

```
现有知识库版本
    ↓
外部基准包交叉对比（8个GitHub GIS Skill包）
    ↓
识别弱项与缺口
    ├─ 内容缺失 → 新增文件（V5.0新增39-45号7个模块）
    ├─ 内容浅薄 → 重写扩充（QGIS 473→3,000+行）
    ├─ 内容过时 → 更新（03号新增云原生格式）
    └─ 结构问题 → 重组（删除3空占位文件）
    ↓
V5.0基线
    ↓
用户反馈驱动迭代（37号 §反馈来源）
    ├─ 纠正式 → 修正协议触发
    ├─ 补充式 → 缺口分级入库
    └─ 评价式 → 质量评分更新
    ↓
V5.1 →
```

**Agent设计启示：** 知识库Agent不应是静态的。需要内置：
1. 外部知识源交叉验证能力
2. 用户反馈自动捕获与转换
3. 版本自动升级的触发规则

### 6.2 错误模式库的积累与利用

当前GIS Skill的避坑库（29号）已积累160+条结构化条目，其积累机制可推广为一般范式：

**条目积累生命周期：**

```
用户遇到错误 → Agent诊断
    ├─ 模式库命中 → 直接修复 → 记录"命中"计数
    └─ 模式库未命中 → Agent尝试诊断
        ├─ 诊断成功 → 自动生成条目草稿
        │     条目格式：WRONG 代码/操作 → CORRECT 方案 → WHY 原理
        │     插入避坑库 + 添加神经连接到相关基础模块
        └─ 诊断失败 → 记录为知识缺口(←→ 37号§K1)
                       → 触发增量搜索
```

**条目质量评估（WPS加权评分算法）：**

| 维度 | 权重 | 评分依据 |
|------|------|---------|
| 命中频率 | 40% | 被检索命中的次数 |
| 用户确认 | 30% | 用户回复"已解决"/"有用" |
| 内容完整性 | 20% | 是否包含 WRONG/CORRECT/WHY 三段 |
| 可复现性 | 10% | 错误是否附带了可复现步骤 |

### 6.3 用户反馈的捕获与转换

**反馈分类→处理管道映射（来自37号 §二）：**

| 反馈类型 | 触发关键词 | 处理管道 | 目标文件 |
|---------|-----------|---------|---------|
| 内容纠正 | "不对"/"错了"/"应该是" | 修正协议（37号§三） | 对应参考文件 |
| 内容补充 | "还有"/"还需要"/"缺了" | 缺口分级入库 | feedback/knowledge_gaps.md |
| 质量评价 | "很好"/"没用"/"不行" | WPS评分更新 | 对应条目质量分 |
| 版本需求 | "新版本"/"升级了"/"发布了" | 版本检测触发 | 差异文件或直接嵌入 |

**Agent实现：反馈捕获的自动Hook**

```python
class FeedbackCaptureHook:
    """每次Agent回复后自动检测用户反馈信号"""
    PATTERNS = {
        "correction": ["不对", "错了", "应该是"],
        "enhancement": ["还有别的吗", "补充一下", "缺了"],
        "version": ["新版本", "最新版", "发布了"],
        "quality_positive": ["很好", "解决了", "谢谢"],
        "quality_negative": ["没用", "还是不对"],
    }
    ROUTES = {
        "correction": "修正协议（37号§三）",
        "enhancement": "知识缺口入库",
        "version": "版本更新检测",
        "quality_positive": "WPS评分+1",
        "quality_negative": "WPS评分-1 + 标记待改进",
    }

    def capture(self, user_response: str):
        for category, keywords in self.PATTERNS.items():
            if any(kw in user_response.lower() for kw in keywords):
                return self.ROUTES.get(category)
        return None
```

### 6.4 知识库衰减检测

**过时内容识别规则：**

| 衰减类型 | 检测条件 | 标记动作 | 更新策略 |
|---------|---------|---------|---------|
| **版本过时** | 软件版本号低于当前最新版本2个大版本以上 | `[可能过时: vX.Y]` | 触发版本更新搜索 |
| **标准废止** | 引用的GB/T标准已被替代/废止 | `[标准已废止]` | 替换为新标准编号 |
| **格式弃用** | 推荐使用已弃用格式（Shapefile/MBTiles） | `[格式已弃用]` | 替换为推荐格式 |
| **API废弃** | 引用的API在新版中被标记deprecated | `[API已废弃]` | 替换为新API |
| **链接失效** | 引用的URL返回404/301 | `[链接失效]` | 更新URL或找到替代来源 |

**Agent实现建议：**

```python
# 知识库衰减检测规则
DECAY_RULES = [
    {
        "pattern": r"Shapefile.*推荐|建议.*\.shp|输出.*Shapefile",
        "action": "更新为GeoPackage推荐",
        "since": "2026"
    },
    {
        "pattern": r"ArcGIS Pro 3\.[0-5]",
        "action": "检查是否需要更新到3.7",
        "since": "2026-05"
    },
    {
        "pattern": r"EPSG:\d{4,5}",
        "check": "验证EPSG代码在最新EPSG数据库中是否有效"
    },
]
```

---

## 七、GIS Agent 评估框架

### 7.1 评估维度与权重

| 评估维度 | 权重 | 评分标准 | 满分要求 |
|---------|------|---------|---------|
| **正确性** | 30% | 输出结果是否技术正确 | 坐标系、格式、算法参数均正确 |
| **完整性** | 20% | 是否覆盖问题所有方面 | 提供代码 + 解释 + 注意事项 |
| **性能意识** | 15% | 是否考虑数据量级影响 | 大数据推荐DuckDB/流式处理 |
| **坐标系安全** | 15% | 是否识别并防范坐标系陷阱 | 距离运算前确认投影坐标系 |
| **格式选择** | 10% | 是否推荐2026年现代格式 | 默认GeoPackage/COG/PMTiles |
| **可执行性** | 10% | 代码是否可直接运行 | 包含导入、路径处理、错误处理 |

### 7.2 回归测试数据集设计原则

| 原则 | 说明 | 示例 |
|------|------|------|
| **边界测试** | 包含极端情况的测试数据 | 空Shapefile / 无CRS数据 / 单点数据 |
| **跨CRS测试** | 测试所有常见坐标系组合 | WGS84→CGCS2000 / UTM→Albers / 经纬度→投影 |
| **多格式测试** | 测试不同格式的数据 | Shapefile / GeoPackage / GeoJSON / GeoParquet / COG |
| **编码测试** | 覆盖中文/特殊字符 | UTF-8 / GBK / 混合编码 / 日文/韩文 |
| **大数据模拟** | 包含性能测试数据 | 100万+要素数据集 |

**推荐测试数据集清单：**

| 测试集 | 数据特征 | 测试目标 |
|--------|---------|---------|
| naturalearth_lowres | ~170个面要素，EPSG:4326 | 基础读写+可视化 |
| OSM建筑物（任一城市） | 1-10万面要素，EPSG:4326 | 空间分析+性能 |
| SRTM 30m DEM | 栅格，~100MB | 栅格处理+COG转换 |
| 中国省界（CGCS2000） | 34个面，EPSG:4490 | 中国坐标系处理 |
| GeoPackage标准测试集 | 点线面混合，含拓扑错误 | 质检+数据完整性 |

### 7.3 Agent输出质量检查清单

**数据转换任务：**
- [ ] 源CRS是否被正确检测？
- [ ] 目标CRS是否明确声明？
- [ ] 输出格式是否为2026年推荐格式（非Shapefile）？
- [ ] 要素数量是否一致？
- [ ] 属性字段是否完整（无截断/无乱码）？
- [ ] 几何是否有效（无自相交/无空几何）？
- [ ] 大文件是否使用了流式处理？

**空间分析任务：**
- [ ] 距离/面积运算前是否确认了投影坐标系？
- [ ] 分析参数是否基于数据特征自动推导（而非硬编码）？
- [ ] 是否包含了结果解读（统计摘要 + 异常检测）？
- [ ] 结果是否可复现（包含随机种子/固定参数）？

**可视化任务：**
- [ ] 坐标系是否转为EPSG:4326（Web地图）？
- [ ] 大数据量是否使用了瓦片化方案而非全量GeoJSON？
- [ ] 配色方案是否考虑了色盲友好？
- [ ] 是否包含了图例和比例尺？

**故障诊断任务：**
- [ ] 是否定位到了具体的文件/代码行？
- [ ] 是否提供了可执行的修复命令？
- [ ] 是否解释了WHY（根因而不仅是现象）？
- [ ] 是否给出了预防措施？

---

## 八、未来方向

### 8.1 多模态GIS Agent

**愿景：** Agent能同时理解地图图像、卫星影像、三维场景和文本描述，实现综合空间推理。

**技术路径：**

| 阶段 | 能力 | 技术方案 | 时间预估 |
|------|------|---------|---------|
| 阶段1 | 地图截图理解 | VL模型（GPT-4V / SAM / LangSAM）识别地图中的要素类型、空间关系 | 2026 |
| 阶段2 | 影像变化检测 | SAM2 + 时序遥感影像 → 自动变化检测 + 自然语言描述 | 2026-2027 |
| 阶段3 | 3D场景理解 | 点云分割 + 语义标签 → 三维场景问答 | 2027+ |
| 阶段4 | 多模态综合推理 | 地图+影像+文本+传感器数据联合推理 | 2028+ |

**当前能力：** ←→ 27_AI_GIS.md 中LangSAM遥感解译即阶段1能力。

### 8.2 GIS Agent与数字孪生集成

**集成架构：**

```
数字孪生平台（←→ 25_三维GIS与数字孪生.md）
    ├── 3DTiles场景（城市/园区/建筑）
    ├── IoT传感器数据流（实时）
    ├── BIM模型（IFC/RVT）
    └── 业务数据（人口/经济/环境）
            ↓
    GIS Agent 集成层
    ├── 自然语言查询："哪个区域的PM2.5超标？"
    ├── 空间推理："如果在地铁站A增加出口，500米覆盖人口变化？"
    ├── 异常检测："今日用水量超过历史同期2倍标准差区域"
    └── 自动报告：基于数字孪生数据生成可视化分析报告
```

**关键接口：**

| 接口 | 协议/格式 | 用途 |
|------|---------|------|
| 3DTiles查询 | Cesium ion / REST API | 三维场景查询与交互 |
| IoT数据接入 | MQTT / WebSocket | 实时传感器数据 |
| BIM集成 | IFC / glTF | 建筑信息模型 |
| 时空查询 | OGC API - Features + CQL2 | 属性+空间+时间联合过滤 |

### 8.3 实时空间数据流处理Agent

**场景：** 处理来自物联网传感器、社交媒体、移动设备的实时位置数据流。

**技术栈：**

```
数据源（每秒上千条）
    ├─ 车辆GPS轨迹
    ├─ 手机信令数据
    └─ 气象站实时观测
        ↓
流处理引擎
    ├─ Apache Kafka（消息队列）
    ├─ Apache Flink（流计算）
    └─ Apache Sedona on Flink（分布式空间处理）
        ↓
GIS Agent 查询层
    ├─ "最近5分钟进入警戒区1的车辆"
    ├─ "当前风速超过15m/s的站点分布"
    └─ "轨迹异常检测：偏航/超速/停留"
        ↓
实时可视化
    └─ Deck.gl StreamingLayer + MapLibre
```

**Agent核心能力需求：**
1. 流式空间窗口查询（滑动窗口+跳跃窗口）
2. 实时空间索引（H3/Quadkey网格化）
3. 异常检测规则引擎（空间+时间联合条件）
4. 低延迟响应（端到端延迟 < 1秒）

---

## 附录：设计模式速查表

| 模式 | 核心价值 | 适用场景 | 关键陷阱 | 关联模块 |
|------|---------|---------|---------|---------|
| Pipeline Agent | 自动化数据转换流 | 格式迁移/ETL管道 | CRS丢失/大文件内存溢出 | ←→ 41/43 |
| Analysis Agent | 自动空间分析 | 环境评估/规划分析 | EPSG:4326距离运算 | ←→ 33 |
| Visualization Agent | 智能地图生成 | 数据展示/报告 | 大数据浏览器崩溃 | ←→ 23/43 |
| Diagnostic Agent | 故障自动诊断 | 报错排查/质检 | 模式库覆盖不足 | ←→ 29 |
| Conversion Agent | 格式智能转换 | CAD↔GIS互转 | 属性丢失/编码转换 | ←→ 30/43 |
| CodeGen Agent | 自然语言→代码 | 快速原型/教学 | 性能盲区/格式假设 | ←→ 13/21/44 |

---

> **版本记录：** V5.0 初始版本 | 2026-06-04 | 覆盖GIS Agent六大设计模式、提示词工程四大模板、三大自动化工作流案例、自进化机制增强、评估框架与未来方向展望
> **撰写依据：** 基于GIS Skill V5.0 45文件体系反向验证 + 8个GitHub GIS Skill包交叉对比 + 29号避坑库160+条模式 + 37号自进化机制实战经验
> **交叉引用覆盖：** SKILL.md（架构参考）、43号（格式决策树/反模式）、41号（管道模式）、27号（AI GIS）、37号（自进化）、19号（多源融合）、29号（避坑库）、33号（空间分析）


<!-- wm:坤图_GIS:V1.0 -->
