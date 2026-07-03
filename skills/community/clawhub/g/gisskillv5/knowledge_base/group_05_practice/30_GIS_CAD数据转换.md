# GIS↔CAD数据转换实战方法论 | 关联：03_数据模型与格式.md 14_CASS11.0.md 18_FME_Form与Flow.md | 来源：旧第十七篇

> **神经连接**：空间统计工具箱的完整 API 参考 → 第十二篇 ArcPy 参考手册（`arcpy.stats` / `arcpy.sa` 模块）。Spatial Analyst/3D Analyst 集成 → 第八篇 ArcGIS Pro 分析功能详解。工具箱参数细节 → 第十一篇 ArcGIS Pro 数据管理与编辑。避坑指南 → 附录B B.5 空间统计篇。

> **推荐学习资源**：
> - GeoDa 官网 `geodacenter.github.io` — 空间自分析免费开源软件，GIS 统计学习首选
> - ArcGIS Pro Spatial Statistics 工具箱文档：`pro.arcgis.com/zh-cn/pro-app/latest/tool-reference/spatial-statistics/`
> - Luc Anselin《Spatial Econometrics》— 空间计量经济学经典教材

---

# 第十七篇：GIS↔CAD 数据转换实战方法论

> 来源：龙山镇GDB→CASS DWG项目 v1→v8 全流程总结 + 网页调研
> 最后更新：2026-05-25 | 核心要点：先理解语义映射，再动手写代码

---

## 17.1 核心认知：语法转换 vs 语义转换

### 17.1.1 转换失败的根本原因

绝大多数 GIS↔CAD 转换问题的根因不是代码错误，而是**没有理解两个数据模型的语义差异**。语法层面的转换（字段→字段、几何→几何）只能处理 60% 的情况，剩下的 40% 需要理解：

- GIS 中 "一行记录" 在 CAD 中对应 "几个实体"
- GIS 中 "一个字段" 在 CAD 中对应 "哪类属性存储机制"
- GIS 中 "空间关系" 在 CAD 中如何表达

### 17.1.2 GIS 数据模型 vs CAD 数据模型 — 本质差异表

| 维度 | GIS（GDB/要素类） | CAD/CASS（DXF/DWG） |
|------|-----------------|---------------------|
| **组织单元** | 要素类（Feature Class）→ 行（Row） | 图层（Layer）→ 实体（Entity） |
| **属性存储** | 属性表（关系型，schema 固定） | XDATA + 注记 TEXT + 块属性（无固定 schema） |
| **几何+属性关系** | 严格一对一（一行 = 一个几何+一行属性） | 一对多（一个地物 = 面 + 多个注记 TEXT + 辅助线） |
| **几何类型** | 单一类型（Point / Polyline / Polygon） | 多种共存（LWPOLYLINE + TEXT + INSERT + LINE） |
| **符号化** | 渲染时动态计算（arcpy 符号化） | 存储为实体属性（线型/颜色/线宽/块参照） |
| **拓扑关系** | 原生支持（拓扑规则、网络数据集） | 无内置拓扑 |
| **坐标系** | 独立存储（.prj / GDB 元数据） | DXF header 存储（容易丢失） |
| **编码体系** | 分类码字段（如 CLASID） | XDATA 中的 CASS 编码（SOUTH 应用名） |
| **属性完整性** | 强制字段约束（NOT NULL / Domain） | 完全自由（可缺、可多、可任意类型） |
| **数据验证** | ArcGIS 域/子类型/拓扑规则 | 无内置验证（依赖操作规范） |

### 17.1.3 转换的核心问题清单

在写任何代码之前，先回答以下问题：

1. **实体拆分**：GIS 的一行记录，转成 CASS 的 1 个实体还是多个实体？
2. **属性去向**：GIS 的字段值，写入 CASS 的 XDATA、TEXT 注记、还是块属性？
3. **编码映射**：GIS 的分类码（CLASID/FCODE），对应 CASS 的哪个编码？
4. **样式映射**：GIS 的符号系统，对应 CASS 的线型/颜色/块名称/图层哪个维度？
5. **特殊处理**：哪些地物类型需要特殊逻辑（如房屋的属性注记拆分）？

> **神经连接**：本节 → 第六篇 6.2.4 GDB→CASS暗坑全指南（34个暗坑详表）、第六篇 CASS编码体系、第四篇 GIS数据格式。

---

## 17.2 数据探查阶段（先理解再动手）

### 17.2.1 方法论：四步探查法

```
探查源数据(30min) → 解剖目标格式(30min) → 映射设计(30min) → 小样本验证(20min)
      ↓                      ↓                     ↓                    ↓
  字段清单+典型值      实体类型+编码分布      映射表+确认清单      50条数据测试
```

### 17.2.2 源数据探查脚本模板

```python
"""GDB数据探查脚本 - 遍历所有FC，输出字段清单和典型值"""
import arcpy

def explore_gdb(gdb_path):
    """遍历GDB，输出每个FC的字段结构、典型值、非空率"""
    arcpy.env.workspace = gdb_path
    
    report = []
    # 先处理根目录的FC
    for fc in arcpy.ListFeatureClasses():
        _analyze_fc(report, gdb_path, fc)
    # 再处理Feature Dataset内的FC
    for ds in arcpy.ListDatasets('*', 'Feature'):
        for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
            _analyze_fc(report, gdb_path, fc, ds)
    
    return report

def _analyze_fc(report, gdb_path, fc, ds=None):
    full_path = f"{gdb_path}\\{ds}\\{fc}" if ds else f"{gdb_path}\\{fc}"
    desc = arcpy.Describe(full_path)
    
    # 跳过注记类
    if desc.featureType == 'Annotation':
        return
    
    info = {
        'name': fc,
        'dataset': ds or '(root)',
        'shapeType': desc.shapeType,
        'count': int(arcpy.GetCount_management(full_path).getOutput(0)),
        'fields': []
    }
    
    # 分析每个字段
    for field in desc.fields:
        fname, ftype = field.name, field.type
        if fname in ('Shape', 'Shape_Length', 'Shape_Area', 'OBJECTID'):
            continue
        
        # 抽样取典型值（前20条非空值去重）
        values = set()
        null_count = 0
        with arcpy.da.SearchCursor(full_path, [fname]) as cursor:
            for i, row in enumerate(cursor):
                if row[0] is None:
                    null_count += 1
                elif len(values) < 20:
                    values.add(str(row[0]))
                if i > 200:  # 最多取样200条
                    break
        
        non_null = info['count'] - null_count
        info['fields'].append({
            'name': fname,
            'type': ftype,
            'non_null': non_null,
            'null_pct': f"{null_count/info['count']*100:.0f}%" if info['count'] > 0 else 'N/A',
            'sample_values': sorted(values)[:10]
        })
    
    report.append(info)
    
    # 打印报告
    print(f"\n{'='*60}")
    print(f"FC: {fc}  [{info['shapeType']}]  {info['count']}条")
    print(f"Path: {full_path}")
    for f in info['fields']:
        print(f"  {f['name']:20s} {f['type']:15s} 非空:{f['non_null']:5d} ({f['null_pct']:>4s})  "
              f"样本:{', '.join(f['sample_values'][:3])}")
    print(f"{'='*60}")
    
    return info

# 使用：
# explore_gdb(r"D:\xxxxxxxx\2000.gdb")
```

### 17.2.3 目标格式解剖脚本模板

```python
"""CASS DXF解剖脚本 - 按编码统计实体类型和xdata分布"""
import ezdxf
from collections import defaultdict, Counter

def dissect_cass_dxf(dxf_path, sample_codes=None):
    """
    解剖CASS参考DXF，了解：
    1. 每种编码对应哪些实体类型（面/线/点/注记）
    2. xdata中存储了什么（编码+属性？仅编码？）
    3. 关联实体分布（如房屋面+层数注记+结构注记）
    """
    doc = ezdxf.readfile(dxf_path)
    msp = doc.modelspace()
    
    # 统计：编码 → 实体类型列表
    code_entities = defaultdict(lambda: Counter())
    # 统计：编码 → xdata内容样本
    code_xdata = defaultdict(set)
    
    for ent in msp:
        # 读取CASS xdata
        if hasattr(ent, 'get_xdata'):
            xd = ent.get_xdata('SOUTH')
            if not xd:
                xd = ent.get_xdata('south')  # 兼容小写
            
            if xd:
                code = None
                for tag, value in xd:
                    if tag == 1000 and value and value not in ('SOUTH', 'south'):
                        code = value
                        break
                
                if code:
                    etype = ent.dxftype()
                    code_entities[code][etype] += 1
                    # 记录xdata样本
                    xd_str = ','.join([f"({t},{v})" for t, v in xd])
                    if len(code_xdata[code]) < 5:
                        code_xdata[code].add(xd_str)
    
    # 输出报告
    print(f"{'编码':12s} {'实体类型':30s} {'数量':>6s}")
    print('-' * 55)
    for code in sorted(code_entities.keys()):
        ent_str = ', '.join([f"{t}({c})" for t, c in code_entities[code].most_common()])
        total = sum(code_entities[code].values())
        print(f"{code:12s} {ent_str:30s} {total:>6d}")
    
    # 关键发现：一个有注记关联的编码
    print(f"\n=== 编码 XDATA 内容样本 ===")
    for code in sorted(code_xdata.keys()):
        print(f"\n编码 {code} 的 xdata 样本:")
        for xd in list(code_xdata[code])[:3]:
            print(f"  {xd}")
    
    return code_entities, code_xdata
```

### 17.2.4 探查输出示例（龙山镇项目实际输出）

```
编码           实体类型                         数量
---------------------------------------------------
141101         LWPOLYLINE(777)                 777     ← 房屋面：xdata仅编码
141101-1       TEXT(529)                       529     ← 结构注记：文本="砖"/"钢"
141101-2       TEXT(568)                       568     ← 层数注记：文本="2"/"7"
144302         LWPOLYLINE(42)                  42      ← 围墙：需X22_L线型
204201         LWPOLYLINE(38)                  38      ← 未加固陡坎：需X3_L线型
204202         LWPOLYLINE(17)                  17      ← 加固陡坎：需X6_L线型
```

> **关键发现**：141101 的 xdata 仅含编码 `[(1000,'141101')]`，属性值（结构/层数）是独立的 TEXT 实体。

---

## 17.3 映射设计阶段

### 17.3.1 映射表模板

在代码中先建好映射表，逐行确认：

```python
# 映射表：源FC → 目标实体 → 编码 → 属性处理 → 样式 → 特殊逻辑
MAPPING_TABLE = {
    # 房屋类：一对多的典型
    "JMDJSS_JMD_A": {
        "code": "141101",           # 房屋面编码
        "target_entities": [
            {"type": "polygon", "code": "141101", "xdata": True, "attrs": None},
            {"type": "text",    "code": "141101-2", "field": "LAY",   "desc": "层数"},
            {"type": "text",    "code": "141101-1", "field": "MATRL", "desc": "结构"},
        ],
        "style": {"layer": "JMD", "color": 6, "linetype": "continuous"},
    },
    # 围墙类：简单一对一 + 特殊线型
    "围墙FC": {
        "code": "144302",
        "target_entities": [
            {"type": "polyline", "code": "144302", "xdata": True, "attrs": None},
        ],
        "style": {"layer": "JMD", "color": 6, "linetype": "X22_L"},
    },
    # 点要素：GIS点 → CASS块参照
    "控制点FC": {
        "code": "131100",
        "target_entities": [
            {"type": "insert", "code": "131100", "block": "gc200", "xdata": True},
        ],
        "style": {"layer": "GCD", "color": 1},
    },
}
```

### 17.3.2 向用户确认的关键问题清单

在动手编码前，必须向用户确认：

1. □ 房屋属性（结构/层数）是否需要生成独立注记 TEXT？
2. □ 缺失线型（X41+）是否可以接受 continuous 兜底？
3. □ 注记位置/大小/旋转角度是否需要精确匹配？
4. □ 哪些图层/FDB码不导出（如 TATC 图廓整饰）？
5. □ 点要素用 gc200 还是其他块参照？
6. □ 输出 DXF 还是 DWG？CASS 版本是 10.1 还是 11？

---

## 17.4 小样本验证阶段

### 17.4.1 小样本转换脚本框架

```python
"""取50条数据做快速验证，用户CASS确认后再全量跑"""
import arcpy
SAMPLE_SIZE = 50

def run_sample_convert(gdb_path, fc_name, output_dxf, sample_count=SAMPLE_SIZE):
    """对单个FC取N条数据转换，快速验证映射逻辑"""
    # 创建临时FC
    sample_fc = "in_memory/sample_fc"
    arcpy.CreateFeatureclass_management("in_memory", "sample_fc", "POLYGON")
    # ... 取前SAMPLE_SIZE条数据写入sample_fc
    # ... 对sample_fc执行完整转换流程
    print(f"[OK] 生成了{output_dxf}，含{sample_count}条数据")
    print("[下一步] 在CASS中打开，V查询确认属性")
```

### 17.4.2 验证清单

| 检查项 | 方法 | 预期 |
|--------|------|------|
| DXF能打开 | CASS → 文件 → 打开 | 无报错 |
| 文件大小 | 右键属性 | > 500KB（非空壳） |
| V查询房屋面 | V命令点选 → 属性对话框 | 显示结构(砖/钢)和层数(2/7) |
| V查询围墙 | V命令点选 → 线型 | 齿状 X22_L，非 continuous |
| 颜色正确 | 目视检查 | JMD=洋红, GCD=红, DGX=黄 |
| 点要素 | 目视检查 | gc200 十字丝+圆圈 |

---

## 17.5 CASS XDATA 深度解析 ⭐

### 17.5.1 XDATA 基础结构

> **来源**：CASS 安装目录 + atlisp.cn CASS XDATA 说明文档 + 龙山镇项目实测

CASS 使用 AutoCAD 的扩展数据（Extended Data）机制存储地物属性，关键参数：

| 参数 | 值 | 说明 |
|------|-----|------|
| **应用名（AppName）** | `"SOUTH"`（严格大写） | CASS 专用的 DXF 扩展数据注册名 |
| **编码存储位置** | `xDataOut(1)`（索引 1） | 即紧随 AppName 的第一个数据项 |
| **DXF 组码** | `1001` = AppName, `1000` = 编码字符串 | ezdxf 写 xdata 时自动处理组码 |
| **数据上限** | 16KB | 单实体 XDATA 总量不超过 16KB |
| **存储能力** | 字符串/整数/浮点/二进制 | 支持多种数据类型 |

### 17.5.2 CASS XDATA 典型存储格式

```
1001: "SOUTH"           ← 应用名（AutoCAD 组码 1001）
1000: "141101"          ← 地物编码（组码 1000 = 字符串）
1000: "砖"              ← 属性值1（可选）
1000: "7"               ← 属性值2（可选）
1040: 15.5              ← 数值属性（可选，组码 1040 = 浮点）
```

**龙山镇项目实测结论**：
- 房屋面 LWPOLYLINE 的 xdata：**仅 `[(1000,'141101')]`**，不含属性值
- 属性值在独立 TEXT 注记实体上（`141101-2` = 层数, `141101-1` = 结构）
- 但其他地物类型（如管线）可能将属性直接存 xdata，不能一刀切

### 17.5.3 骨架线（Skeleton）机制

CASS 的核心内部机制，理解这一点至关重要：

- **骨架线**：复杂地物的 "核心基线"，如围墙的中线、斜坡的坡底线
- **关联符号**：所有次要符号（齿状线、块参照、注记）挂载在骨架线上
- **联动编辑**：编辑骨架线的几何后，关联符号自动跟随更新
- **编码承载**：骨架线上存 CASS 编码，通过骨架线串起整个地物

常见骨架线地物：围墙（144302）、斜坡（204101/204102）、陡坎（204201/204202）、电力线、管线等。

### 17.5.4 XData vs XRecord 区别

| 特性 | XData | XRecord |
|------|-------|---------|
| 附着对象 | 单个实体 | 命名对象字典（全局） |
| 大小限制 | 16KB/实体 | 无严格限制 |
| 访问方式 | `ent.get_xdata('SOUTH')` | `doc.objects['XDICT']['KEY']` |
| CASS 使用 | ⭐ 主要使用 | 可能用于全局配置 |
| ezdxf 支持 | ✅ `get_xdata` / `set_xdata` | ✅ `rootdict` 字典操作 |

> **神经连接**：本节 → 第六篇 6.2.4暗坑指南（坑3：房屋属性不在xdata）、第三篇 CASS编码体系。

---

## 17.6 GIS↔CAD 转换方案对比

### 17.6.1 三大方案总览

| 方案 | 工具 | 成本 | 适用场景 | 优点 | 缺点 |
|------|------|------|---------|------|------|
| **A. 商业方案** | FME Desktop | 年度许可费 | 全类型DLG数据库批量转换 | 可视化工作流、内置CASS编码支持、模板可复用 | 商用许可、需学习FME操作 |
| **B. ArcPy + ezdxf** | ArcGIS Pro + ezdxf | 免费（已有ArcGIS Pro） | 定制化GDB→CASS转换、需要灵活编码控制的项目 | 完全可编程、灵活、ArcGIS Pro自带的Python可使用 | 需手写大量代码、ezdxf不支持真DWG |
| **C. 开源组合** | GDAL/OGR + geopandas | 免费 | 简单SHP↔DXF互转、数据探查分析 | 无需ArcGIS许可、纯Python生态 | 不支持CASS编码写入、DXF驱动功能有限 |

### 17.6.2 方案B：ArcPy + ezdxf 实战（推荐方案）

基于龙山镇项目的完整技术栈：

```
工具链：
  ArcGIS Pro 3.x + arcpy       （GDB读取、数据探查）
  ezdxf 1.x                     （DXF读写、xdata操作）
  CASS 安装目录                 （layer.def / text.def / ACAD.LIN）
  Python 3.x                    （脚本编写）
```

核心技术要点速查：
- ArcGIS Pro Python 路径：`C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe`
- DXF 编码：`doc.encoding = 'gbk'` + `doc.header['$DWGCODEPAGE'] = 'ANSI_936'`
- xdata 写入：`ent.set_xdata('SOUTH', [(1000, '141101')])`
- 线型创建：从 ACAD.LIN 解析 pattern → `doc.linetypes.new('X22_L').pattern = [...]`
- 输出格式：**`.dxf` 后缀**（ezdxf 不能输出真 DWG 二进制）

### 17.6.3 方案C：开源组合速览

```python
# GDAL读取GDB → 写DXF
from osgeo import ogr
ds = ogr.Open("xxx.gdb")
layer = ds.GetLayerByName("JMDJSS_JMD_A")

# geopandas快速探查
import geopandas as gpd
gdf = gpd.read_file("xxx.gdb", layer="JMDJSS_JMD_A")
print(gdf.columns.tolist())  # 字段清单
print(gdf.dtypes)            # 字段类型
print(gdf.describe())        # 数值统计
print(gdf.head(5))           # 前5条

# GDAL DXF驱动（仅基本读写，不支持CASS编码）
# 需要CASS编码 → 回到方案B使用ezdxf
```

> **没有万能工具**：简单格式互转用 GDAL/OGR，需要 CASS 编码体系支持用 ArcPy+ezdxf，海量全要素生产用 FME。

---

## 17.7 Python GIS 开源生态全景

> 来源：gis-mcp(92工具)、GeoMaster Skill(70+主题)、GDAL/Rasterio/PySAL官方文档
> 最后更新：2026-05-29 | 核心要点：三层工具架构（读写/分析/可视化）全覆盖

### 17.7.1 核心库全景架构

```
┌─────────────────────────────────────────────────┐
│              应用层 & 可视化                       │
│  folium(交互地图)  matplotlib(静态图)  keplergl(3D) │
├─────────────────────────────────────────────────┤
│              分析 & 处理层                         │
│  geopandas(矢量)  rasterio(栅格)  shapely(几何)   │
│  pyproj(投影)     pysal(空间统计)   scipy(算法)    │
├─────────────────────────────────────────────────┤
│              I/O & 数据引擎                        │
│  fiona(矢量读)    GDAL(格式转换)   laspy(点云)      │
│  ezdxf(CAD)      rtreed(空间索引)  pdal(点云管道)   │
└─────────────────────────────────────────────────┘
```

| 库 | 用途 | 安装 | 典型场景 |
|---|------|------|---------|
| **geopandas** | 矢量数据框操作 | `pip install geopandas` | 字段探查、sjoin空间连接、dissolve融合 |
| **fiona** | 矢量 I/O | `pip install fiona` | 轻量GDB/SHP/GeoJSON读写 |
| **shapely** | 几何运算（29种） | `pip install shapely` | buffer/intersection/Voronoi/三角剖分 |
| **ezdxf** | DXF读写 | `pip install ezdxf` | DXF创建、xdata操作、线型/图层设置 |
| **GDAL/OGR** | 格式转换引擎 | ArcGIS Pro自带 | 180+格式互转、投影转换、瓦片切割 |
| **pyproj** | 坐标投影(13种) | `pip install pyproj` | CRS转换、UTM计算、大地测量 |
| **rasterio** | 栅格数据(20种) | `pip install rasterio` | 裁剪/重投影/NDVI/分区统计/山体阴影 |
| **rtree** | 空间索引 | `pip install rtree` | 快速空间查询、近邻搜索 |
| **pysal** | 空间统计(18种) | `pip install pysal` | Moran's I/Gi*/KNN权重/OLS诊断/聚类 |
| **laspy** | LAS点云读写 | `pip install laspy` | 点云过滤、分类修改、统计 |
| **pdal** | 点云处理管道 | `pip install pdal` | 地面滤波、管线处理、格式转换 |
| **folium** | Web地图 | `pip install folium` | Leaflet交互地图快速预览 |

### 17.7.2 Rasterio 操作速查

#### 基本读写与元数据

```python
import rasterio
import numpy as np

# 读取
with rasterio.open("dom.tif") as src:
    print(f"尺寸: {src.width}x{src.height}, 波段: {src.count}")
    print(f"CRS: {src.crs}, 分辨率: {src.res}")
    print(f"范围: {src.bounds}")
    print(f"数据类型: {src.dtypes[0]}")
    
    # 读取全部波段
    data = src.read()  # shape: (bands, rows, cols)
    
    # 读取单波段
    band1 = src.read(1)  # 1-indexed
    
    # 窗口读取（大文件必备）
    window = rasterio.windows.Window(col_off=0, row_off=0, 
                                      width=1024, height=1024)
    tile = src.read(1, window=window)
```

#### 裁剪与掩膜

```python
import rasterio.mask
from shapely.geometry import box

# 按范围裁剪
bbox = box(500000, 3400000, 501000, 3401000)
geoms = [{"type": "Polygon", "coordinates": [list(bbox.exterior.coords)]}]

with rasterio.open("dom.tif") as src:
    out_image, out_transform = rasterio.mask.mask(src, geoms, crop=True)
    out_meta = src.meta.copy()
    out_meta.update({
        "height": out_image.shape[1],
        "width": out_image.shape[2],
        "transform": out_transform
    })
    with rasterio.open("clipped.tif", "w", **out_meta) as dst:
        dst.write(out_image)

# 按shapefile裁剪
import geopandas as gpd
gdf = gpd.read_file("aoi.shp")
geoms = [json.loads(gdf.geometry.to_json())['features'][0]['geometry']]
```

#### 重投影与重采样

```python
from rasterio.warp import calculate_default_transform, reproject, Resampling

with rasterio.open("dom.tif") as src:
    dst_crs = "EPSG:4546"
    transform, width, height = calculate_default_transform(
        src.crs, dst_crs, src.width, src.height, *src.bounds)
    
    kwargs = src.meta.copy()
    kwargs.update(crs=dst_crs, transform=transform, width=width, height=height)
    
    with rasterio.open("reprojected.tif", "w", **kwargs) as dst:
        for i in range(1, src.count + 1):
            reproject(
                source=rasterio.band(src, i),
                destination=rasterio.band(dst, i),
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=transform,
                dst_crs=dst_crs,
                resampling=Resampling.bilinear
            )
```

#### 波段运算与指数计算

```python
# NDVI 计算
with rasterio.open("sentinel2.tif") as src:
    red = src.read(4).astype(np.float32)  # B4=Red
    nir = src.read(8).astype(np.float32)  # B8=NIR
    ndvi = (nir - red) / (nir + red + 1e-8)
    ndvi = np.clip(ndvi, -1, 1)
    
    profile = src.profile
    profile.update(count=1, dtype=rasterio.float32)
    with rasterio.open("ndvi.tif", "w", **profile) as dst:
        dst.write(ndvi, 1)

# 常用的其他指数
# NDWI (水体): (Green - NIR) / (Green + NIR)
ndwi = (green - nir) / (green + nir + 1e-8)

# NDBI (建筑): (SWIR - NIR) / (SWIR + NIR)  
ndbi = (swir - nir) / (swir + nir + 1e-8)

# EVI (增强植被): 2.5*(NIR-Red)/(NIR+6*Red-7.5*Blue+1)
evi = 2.5 * (nir - red) / (nir + 6*red - 7.5*blue + 1)
```

#### 分区统计 (Zonal Statistics)

```python
from rasterio.features import geometry_mask
import geopandas as gpd

zones = gpd.read_file("parcels.shp")
with rasterio.open("ndvi.tif") as src:
    ndvi_data = src.read(1)
    for idx, row in zones.iterrows():
        # 创建该多边形的掩膜
        geom = [row.geometry.__geo_interface__]
        mask = geometry_mask(geom, transform=src.transform, 
                            invert=True, out_shape=src.shape)
        # 统计该区域NDVI
        zone_vals = ndvi_data[mask]
        print(f"地块{idx}: mean={zone_vals.mean():.3f}, "
              f"max={zone_vals.max():.3f}, std={zone_vals.std():.3f}")
```

### 17.7.3 Shapely 高级几何操作

#### 几何生成与变换

```python
from shapely.geometry import Point, LineString, Polygon, MultiPoint
from shapely.ops import voronoi_diagram, triangulate, unary_union

# Voronoi图 (gis-mcp: voronoi)
points = MultiPoint([(0,0), (10,0), (5,10), (15,10)])
regions = voronoi_diagram(points)

# Delaunay三角剖分 (gis-mcp: triangulate_geometry)
triangles = triangulate(points)

# 几何简化 (Douglas-Peucker)
simplified = polygon.simplify(tolerance=0.5, preserve_topology=True)

# 凸包
hull = points.convex_hull

# 仿射变换
from shapely import affinity
rotated = affinity.rotate(geom, angle=45, origin='centroid')
scaled = affinity.scale(geom, xfact=2.0, yfact=1.5)
translated = affinity.translate(geom, xoff=100, yoff=200)
```

#### 几何修复与验证

```python
from shapely.validation import make_valid, explain_validity

# 检查有效性
if not polygon.is_valid:
    print(explain_validity(polygon))  # 解释原因
    
# 修复无效几何 (gis-mcp: make_valid)
fixed = make_valid(polygon)

# 常用几何操作速查表
# area = geom.area              → 面积
# length = geom.length           → 长度/周长
# centroid = geom.centroid       → 质心
# buffer = geom.buffer(10)       → 缓冲区
# intersection = a.intersection(b)  → 交集
# union = a.union(b)             → 并集
# difference = a.difference(b)   → 差集
# envelop = geom.envelope        → 外包矩形
# nearest = geom1.distance(geom2)  → 最近距离
# snapped = snap(g1, g2, 0.5)   → 几何吸附
```

### 17.7.4 PySAL 空间统计实战

#### 空间权重矩阵构建

```python
import libpysal
from libpysal.weights import KNN, DistanceBand, Queen

# KNN权重 (gis-mcp: knn_weights)
# 最常见的空间关系定义方式
coords = gdf.geometry.apply(lambda p: [p.x, p.y]).tolist()
w_knn = KNN.from_array(np.array(coords), k=15)  # 15近邻

# 距离带权重 (gis-mcp: distance_band_weights)
w_dist = DistanceBand.from_dataframe(gdf, threshold=500)
# 阈值500m内为邻居

# Queen邻接权重 (共享边或顶点)
w_queen = Queen.from_dataframe(gdf)
```

#### 空间自相关分析

```python
from esda.moran import Moran, Moran_Local
from esda.getisord import G, G_Local

# 全局 Moran's I (gis-mcp: morans_i)
y = gdf['某个字段'].values
moran = Moran(y, w_knn)
print(f"Moran's I = {moran.I:.4f}")     # 接近1=聚集
print(f"p-value = {moran.p_sim:.4f}")    # <0.05=显著

# 局部 LISA (gis-mcp: moran_local)
local_moran = Moran_Local(y, w_knn)
# 分类: HH(高-高)/HL(高-低)/LH(低-高)/LL(低-低)

# Getis-Ord Gi* 热点分析 (gis-mcp: getis_ord_g_local)
gi = G_Local(y, w_knn)
z_scores = gi.Zs  # |Z|>1.96 = 显著热点/冷点

# 将结果附加回 GeoDataFrame
gdf['moran_I_local'] = local_moran.Is
gdf['Gi_Zscore'] = z_scores
gdf['hotspot'] = np.where(z_scores > 1.96, 'Hot',
                          np.where(z_scores < -1.96, 'Cold', 'NS'))
```

#### 空间回归与聚类

```python
# OLS + 空间诊断 (gis-mcp: ols_with_spatial_diagnostics)
from spreg import OLS
import numpy as np

X = gdf[['自变量1', '自变量2']].values
y = gdf['因变量'].values
ols = OLS(y, X, w=w_knn, spat_diag=True, moran=True)
print(f"R² = {ols.r2:.3f}")
print(f"Moran's I残差 = {ols.moran_res[0]:.3f}")  # >0.1需要空间模型

# ADBSCAN自适应密度聚类 (gis-mcp: adbscan)
from esda.adbscan import ADBSCAN
adbscan = ADBSCAN(gdf, attribute='population', w=w_knn, 
                   min_size=5, significance=0.05)
gdf['adbscan_cluster'] = adbscan.labels_
```

### 17.7.5 GDAL 命令行速查

#### 栅格操作 (gdalwarp / gdal_translate)

```bash
# 投影转换
gdalwarp -t_srs EPSG:4546 -r bilinear input.tif output.tif

# 裁剪到范围
gdalwarp -te 500000 3400000 501000 3401000 input.tif clipped.tif

# 重采样（改变分辨率）
gdalwarp -tr 0.1 0.1 -r cubic input.tif resampled.tif

# 格式转换 + 压缩
gdal_translate -of GTiff -co COMPRESS=LZW -co TILED=YES input.img output.tif

# 波段提取
gdal_translate -b 1 -b 2 -b 3 multispectral.tif rgb.tif

# 创建金字塔（加速显示）
gdaladdo -r average large.tif 2 4 8 16

# 合并多幅影像
gdal_merge.py -o merged.tif -v tile_*.tif

# 创建影像瓦片
gdal2tiles.py -z 10-18 input.tif tiles/
```

#### 矢量操作 (ogr2ogr)

```bash
# SHP → GeoJSON
ogr2ogr -f GeoJSON output.geojson input.shp

# GDB → SHP（指定图层）
ogr2ogr -f "ESRI Shapefile" output.shp input.gdb LayerName

# 带属性过滤
ogr2ogr -where "population > 10000" filtered.shp input.shp

# 带空间过滤（按范围裁剪）
ogr2ogr -spat 500000 3400000 501000 3401000 clipped.shp input.shp

# 重投影
ogr2ogr -t_srs EPSG:4546 reprojected.shp input.shp

# 追加到PostGIS
ogr2ogr -f PostgreSQL PG:"host=localhost dbname=gis" input.shp
```

### 17.7.6 与 arcpy 的互补使用策略

| 阶段 | 使用工具 | 原因 |
|------|----------|------|
| 数据探查 | **geopandas + fiona** | 比 arcpy 快 10 倍，无需打开 ArcGIS Pro |
| 字段分析 | **geopandas** | DataFrame 操作比 arcpy.da 更直观 |
| 坐标系转换 | **pyproj** | 轻量，无需加载 arcpy 环境 |
| 栅格处理 | **rasterio** | 窗口读写、分区统计，无需许可 |
| 空间统计 | **pysal** | Moran's I/Gi* 比 arcpy 参数更灵活 |
| 点云处理 | **laspy + pdal** | 仅有的专业Python点云工具链 |
| 正式转换 | **arcpy + ezdxf** | arcpy 是唯一能完整读取 GDB 复杂结构的工具 |
| 批量处理 | **arcpy** | 工具箱集成度最高，错误处理完善 |

> **神经连接**：本节 → 第十二篇 ArcPy参考手册（da/mp/sa完整API）、第六篇 编码转换实战、第十八篇18.8 LiDAR点云处理与Python生态。

---

## 17.8 完整转换流程 SOP

```
┌──────────────────────┐
│   阶段1：数据探查（0.5h）      │
│   ├ 源GDB：arcpy遍历FC → 字段清单+典型值+非空率    │
│   └ 目标格式：ezdxf解剖参考DXF → 实体类型+编码+xdata分布  │
├──────────────────────┤
│   阶段2：映射设计（0.5h）      │
│   ├ 编写映射表（源FC.字段 → 目标实体.编码.属性位置） │
│   └ 向用户确认映射逻辑 + 特殊处理需求（6个关键问题）  │
├──────────────────────┤
│   阶段3：小样本验证（0.3h）    │
│   ├ 取50条数据转换 → 用户CASS V查询验证     │
│   └ 确认无误后进入全量                             │
├──────────────────────┤
│   阶段4：全量转换 + 质检（1h） │
│   ├ 全量数据转换                                    │
│   ├ 文件大小检查（>500KB）                          │
│   └ 抽查不同地物类型（面/线/点/注记各5个）            │
├──────────────────────┤
│   阶段5：成果验证（0.3h）      │
│   ├ CASS V查询 + 目视检查                           │
│   └ 记录已知局限（如X41+线型缺失）                    │
└──────────────────────┘
总计：约 2.6 小时完成一个标准 DLG 数据转换任务。
```

### 核心原则（经验教训）

1. **禁止猜测**：不确定的字段含义、编码映射、属性存储方式 — 先解剖参考数据确认
2. **先探查后编码**：在写第一行转换代码前，必须完成探查报告和映射表
3. **不确定就搜**：测绘行业的数据转换不是新鲜问题，CSDN/测绘论坛/B站大概率有前人经验
4. **小样本先行**：永远不要第一次就跑全量，50条数据验证逻辑后再全量跑
5. **以实测为准**：layer.def 的说明文字可能误导（如 `141101-2` 写 "地下房屋" 实际是层数注记），以参考 DXF 的实际解剖结果为准

---

> **跨篇神经连接**：
> - 转换暗坑详表 → 第六篇 6.2.4 节（34个暗坑，按分类速查）
> - CASS 编码体系 → 第三篇（六位码规则/cassconfig.db）
> - GDB 数据处理 → 第十一篇（要素类创建/字段管理/编辑工具）
> - ArcPy 编程 → 第十二篇（da游标/mp布局/sa分析完整API）
> - 质量检查标准 → 第十三篇（二级检查一级验收 + 精度指标 + SOP质检步骤）⭐
> - 新型基础测绘实体 → 第十四篇（传统GDB→新型实体范式差异）
> - 项目费用参考 → 第十五篇（数据加工/格式转换定价）

---


<!-- wm:坤图_GIS:V1.0 -->
