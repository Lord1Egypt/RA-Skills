---
name: KML/SHP/CAD格式转换
description: |
  通用GIS格式零配置互转工具。支持DWG(自动转DXF)/SHP/DXF/KML/KMZ/GeoJSON/
  GeoPackage/GeoParquet/OVKML/OVJSN/DJI-WPMZ/Huace-KML的任意双向转换。
  DWG直接拖入出KML/SHP——自动下载ODA转换引擎、自动识别CGCS2000投影坐标系、
  自动GCJ-02纠偏。坐标系确认仅在自动检测置信度不足时主动询问,常见场景零交互。
  BJ54/西安80坐标系自动诊断偏移误差。支持无人机航线KML生成。
triggers:
  - GIS格式转换 / 数据互转 / 坐标转换
  - DWG转KML / DWG转SHP / CAD转GIS / CAD转KML / CAD转SHP
  - SHP转KML / DXF转KML / GeoJSON转CAD / KML转SHP
  - 奥维ovkml / ovobj / ovjsn转换
  - 大疆DJI航线KML / WPMZ生成
  - 华测KML格式导出
  - GeoPackage / GeoParquet格式互转
  - 坐标系转换 GCJ-02 WGS84 CGCS2000 BJ54 西安80
  - 无人机测绘航线生成
  - 数据格式批量互转 / 格式转换
version: "1.0.0"
agent_created: true
---

# KML/SHP/CAD格式转换 V1.0

> 12 种 GIS 格式任意双向转换 | DWG 丢进去直接出 KML/SHP | 坐标系统全自动识别
>
> 坤图_GIS

---

## 一、快速开始（3 步上手）

### Step 1: 安装依赖

```bash
pip install geopandas pyproj ezdxf shapely pyarrow
```

### Step 2: 开始转换

```bash
# DWG → KML（全自动，无需配置坐标系）
python scripts/gis_converter.py 我的图纸.dwg 输出.kml

# DWG → SHP（自动识别 CGCS2000 分带）
python scripts/gis_converter.py 地形图.dwg 成果.shp

# 其他格式互转
python scripts/gis_converter.py 边界.shp 数据.geojson
```

### Step 3: 查看结果

转换完成后自动输出日志，包含：
- 自动识别的坐标系及置信度
- 要素数量和几何类型统计
- DWG→DXF 转换耗时（如有）

**如果自动识别不确定**，工具会主动提示：
```
检测到坐标位于湖北神农架区域，推测为 CGCS2000 3°带 第37带 (EPSG:4546)，是否正确？[Y/n]
```
直接回车确认即可，或输入 `n` 手动指定。

---

## 二、支持格式全矩阵

| ↓ 输入 \ 输出 → | SHP | GeoJSON | KML | OVKML | OVJSN | DXF | GPKG | Parquet | WPMZ | Huace |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **DWG** | ✓ | ✓ | ✓ | ✓ | ✓ | — | ✓ | ✓ | ✓ | ✓ |
| **DXF** | ✓ | ✓ | ✓ | ✓ | ✓ | — | ✓ | ✓ | ✓ | ✓ |
| **SHP** | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **GeoJSON** | ✓ | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **KML/KMZ** | ✓ | ✓ | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **OVKML** | ✓ | ✓ | ✓ | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **OVJSN** | ✓ | ✓ | ✓ | ✓ | — | ✓ | ✓ | ✓ | ✓ | ✓ |
| **GPKG** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | ✓ | ✓ | ✓ |
| **Parquet** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | ✓ | ✓ |

**图例**：GPKG = GeoPackage（OGC标准，SHP推荐替代）, WPMZ = DJI-WPMZ, Huace = 华测GNSS KML

---

## 三、完整命令参考

### 3.1 DWG/CAD 转 GIS（零配置推荐）

```bash
# 单文件转换
python scripts/gis_converter.py 地形图.dwg 成果.kml
python scripts/gis_converter.py 地形图.dwg 成果.shp
python scripts/gis_converter.py 地形图.dwg 成果.dxf       # DWG→DXF(版本转换)
python scripts/gis_converter.py 地形图.dwg 成果.geojson
python scripts/gis_converter.py 地形图.dwg 成果.gpkg       # GeoPackage

# 手动指定坐标系（覆盖自动检测）
python scripts/gis_converter.py 地形图.dxf 成果.shp --source-crs EPSG:3857
```

**DWG 自动转换原理**：
1. 检查系统是否安装 ODA File Converter（免费命令行工具）
2. 未安装则自动下载（~28MB）并静默安装
3. 在临时目录执行 DWG→DXF 转换
4. 后续自动识别坐标系 → 标准 GIS 转换

> 首次转换 DWG 需联网下载 ODA 引擎，之后无需重复下载。

### 3.2 奥维地图格式

```bash
# OVKML 自动 GCJ-02→WGS84 纠偏
python scripts/gis_converter.py 奥维收藏夹.ovkml 成果.shp

# OVJSN（奥维JSON）读写
python scripts/gis_converter.py 数据.ovjsn 成果.geojson
python scripts/gis_converter.py 成果.geojson 奥维格式.ovjsn

# 禁用自动纠偏
python scripts/gis_converter.py 数据.ovkml 成果.shp --no-gcj02-correct
```

### 3.3 大疆无人机航线

```bash
python scripts/gis_converter.py 测区边界.geojson 航线任务.wpmz \
  --drone "M350 RTK" \
  --payload "Zenmuse P1" \
  --altitude 80 \
  --speed 10 \
  --action takePhoto
```

**DJI 支持设备**：

| 型号 | 载荷 | 备注 |
|------|------|------|
| M350 RTK | H20/H20T/P1/L1/L2 | 旗舰机型 |
| M300 RTK | H20/H20T/P1/L1 | 上一代 |
| Matrice 3D/3E | M3D/M3E/M3E-T | 紧凑型 |
| Mavic 3E/3T/3M | M3E/M3E-T/M3M | 消费级测绘 |
| Mini 4 Pro | 内置相机 | 轻便型 |

**航线参数说明**：

| 参数 | CLI选项 | 默认值 | 说明 |
|------|---------|--------|------|
| 无人机型号 | `--drone` | M350 RTK | 自动映射到DJI枚举值 |
| 相机载荷 | `--payload` | Zenmuse H20 | 自动映射到DJI枚举值 |
| 飞行高度/m | `--altitude` | 50 | 相对起飞点 |
| 飞行速度/m·s⁻¹ | `--speed` | 8 | 航点间速度 |
| 云台俯仰/° | `--gimbal-pitch` | -90 | -90=正射, 0=水平 |
| 航点动作 | `--action` | takePhoto | takePhoto/startRecord/hover |
| 朝向模式 | `--heading-mode` | followWayline | followWayline/fixed/north |
| 高度模式 | `--altitude-mode` | relativeToGround | relativeToGround/absolute |

### 3.4 华测 LandStar 格式

```bash
python scripts/gis_converter.py 地块.shp 华测导出.kml \
  --name-field "地块编号" \
  --desc-field "备注"
```

### 3.5 GeoPackage / GeoParquet（现代化格式）

```bash
# SHP → GeoPackage（UTF-8原生，无字段名限制）
python scripts/gis_converter.py 数据.shp 数据.gpkg

# GeoParquet（列式压缩 10:1~20:1，DuckDB兼容）
python scripts/gis_converter.py 大数据.shp 大数据.parquet
```

### 3.6 Python API 调用

```python
from gis_converter import convert

# DWG 零配置转换（自动DWG→DXF + 自动识别坐标系）
convert("地形图.dwg", "成果.kml")
convert("地形图.dwg", "成果.shp")

# DXF 自动识别坐标系
convert("管线图.dxf", "成果.shp")

# 手动指定坐标系
convert("图纸.dxf", "成果.shp", source_crs="EPSG:4490")

# 生成大疆航线
convert("测区.geojson", "任务.wpmz",
        drone_model="M350 RTK",
        payload_model="Zenmuse H20",
        altitude=80, speed=10,
        action_type="takePhoto")

# 北京54→WGS84（自动诊断偏移量）
convert("老数据.shp", "成果.kml", source_crs="EPSG:4214")
```

---

## 四、坐标系处理规则

| 优先级 | 规则 | 适用场景 |
|--------|------|---------|
| 1 | 文件内置 CRS（.prj / GeoJSON CRS / GPKG） | SHP, GeoJSON, GPKG, Parquet |
| 2 | `--source-crs` 用户显式指定 | 所有格式，覆盖自动检测 |
| 3 | **自动坐标系识别** | DXF, DWG（从投影坐标值推断） |
| 4 | 奥维格式自动 GCJ-02 纠偏 | OVKML, OVJSN |
| 5 | `--source-gcj02` 强制纠偏 | 任意 KML 格式 |
| 6 | 默认 WGS84 (EPSG:4326) | 兜底 |

### 自动坐标系识别算法

适用于中国 CGCS2000 Gauss-Kruger 投影坐标：

1. **地理坐标检测**：X 在 ±180°、Y 在 ±90° → EPSG:4326
2. **Web Mercator 检测**：投影坐标超出 GK 范围 → EPSG:3857
3. **中国 GK 分带匹配**：
   - 从北坐标(Y)估算纬度 ≈ Y / 111,000
   - 根据纬度带确定区域参考经度（按中国行政区划）
   - 计算经度偏差 → 匹配最近 CGCS2000 3°/6° 分带

**支持的分带**：CGCS2000 3° 带 (EPSG:4534~4553，CM 75°~135°E) 和 6° 带 (EPSG:4550~4562)

---

## 五、常见问题与解决方案

### Q1: DWG 首次转换很慢

> **原因**：首次需下载 ODA File Converter（~28MB）
> **解决**：等待下载完成，之后同类转换秒级完成

### Q2: SHP 中文乱码

> **原因**：Shapefile 编码为 GBK/GB2312 但读取用 UTF-8
> **解决**：`python gis_converter.py input.shp output.kml --encoding gbk`

### Q3: SHP 字段名变短/截断

> **原因**：DBF 格式限制，字段名不能超过 10 个英文字符
> **解决**：使用 GeoPackage 替代（无字段名限制）：
> `python gis_converter.py data.shp data.gpkg`

### Q4: 坐标系识别错误

> **原因**：数据不在中国境内（境外投影坐标系），或为 CUSTOM 用户自定义投影
> **解决**：手动指定：
> `python gis_converter.py input.dxf output.shp --source-crs EPSG:XXXX`

### Q5: 北京54/西安80 转 WGS84 偏移 100~200 米

> **原因**：pyproj 默认变换不使用精确的七参数/格网改正
> **解决**：工具已自动诊断并输出偏移警告。如需精确转换，提供七参数后配置 pyproj 管线

### Q6: GeoPackage 文件被锁定

> **原因**：SQLite 单写入者限制，QGIS 等软件同时打开
> **解决**：关闭所有打开该 gpkg 的软件后重试

### Q7: DXF 属性丢失

> **原因**：DXF 格式不支持属性表，仅保留几何图形和图层名
> **解决**：转换时保留 `layer` 字段，可用 `--name-field layer` 按图层命名

### Q8: OVOBJ 二进制无法解析

> **原因**：奥维私有二进制格式，无公开解析规范
> **解决**：通过奥维桌面端导出为 OVKML/OVJSN 后再转换

---

## 六、适用场景

| 场景 | 推荐流程 |
|------|---------|
| 勘测定界 DWG→SHP | `dwg → shp`（一条命令） |
| 无人机航线生成 | `geojson → wpmz`（指定无人机型号） |
| CAD→GIS 数据入库 | `dwg/dxf → gpkg`（GeoPackage 替代 SHP） |
| 奥维数据归档 | `ovkml/ovjsn → shp/geojson`（自动纠偏） |
| 坐标系统一 | 任意格式 → `shp --target-crs EPSG:4546` |
| 大数据分析 | `shp/geojson → parquet`（DuckDB 兼容） |
| 华测 GNSS 数据处理 | `shp → huace-kml` |
| WebGIS 发布 | `shp → geojson/gpkg` |

---

## 七、依赖环境

| 组件 | 版本要求 | 说明 |
|------|---------|------|
| Python | ≥ 3.9 | 推荐 3.10+ |
| geopandas | ≥ 0.14 | 矢量数据处理核心 |
| pyproj | ≥ 3.6 | 坐标转换引擎 |
| ezdxf | ≥ 1.3 | DXF 读写 |
| shapely | ≥ 2.0 | 几何运算 |
| pyarrow | 任意 | GeoParquet 读写 |
| ODA File Converter | 自动安装 | DWG→DXF 转换 |

---

## 八、已知限制

1. **OVOBJ 二进制**无法直接解析，需通过奥维桌面端导出为 OVKML/OVJSN
2. **CASS XDATA** 不支持（测绘行业专用 SOUTH-XDATA 编码）
3. **BJ54/西安80** 精确转换需七参数（已内置诊断提醒）
4. **CRS 自动检测**仅覆盖中国 CGCS2000 3°/6°带 + WGS84 + Web Mercator
5. **DWG 首次**需联网下载 ODA File Converter
6. **SHP 字段名**超过 10 字符自动截断（建议用 GeoPackage 替代）
7. **高纬度**（>50°N）坐标系识别精度下降

---

## 九、日志与排错

每次转换自动生成日志文件：`logs/gis_convert_YYYYMMDD_HHMMSS.log`

日志包含：
- 输入/输出文件信息
- DWG→DXF 转换详情（如有）
- 自动坐标系识别结果及置信度
- 坐标转换参数
- 要素数量和几何类型统计
- 错误堆栈（如有异常）

---

## 十、格式规范参考

详见 `references/formats.md`

---

<!-- wm:坤图_GIS -->
