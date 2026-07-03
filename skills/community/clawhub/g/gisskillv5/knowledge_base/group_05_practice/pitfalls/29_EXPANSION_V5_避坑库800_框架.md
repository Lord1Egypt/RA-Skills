<!-- wm:坤图_GIS:V5.0 -->
---
knowledge_id: GIS-KB-G05-002-EXP01
group: 5
group_name: "实战与避坑"
title: "29号扩展：避坑库V5.0 800+结构化反模式·八大类细分·报错码速查框架"
source_file: "29_避坑库.md (原160+条目)"
version: "V5.0"
last_updated: "2026-06-23"
---

# 避坑库 V5.0：160+ → 800+ 结构化反模式框架

## 八大类目索引（带条目统计目标）

| 大类 | 编号前缀 | V1.0条目 | V5.0目标 | 子类 |
|------|---------|---------|---------|------|
| **A. 坐标系与投影** | PIT-CRS | 15 | 80 | 中央子午线/带号/高程异常/七参数/地方坐标系 |
| **B. 数据格式与转换** | PIT-FMT | 20 | 100 | CAD/DWG/Shapefile/GDB/GeoJSON/编码乱码 |
| **C. 软件工具专项** | PIT-SFT | 20 | 120 | ArcGIS/QGIS/CASS/SuperMap/FME/GlobalMapper |
| **D. 空间数据库** | PIT-DB | 10 | 60 | PostGIS/GDB/GeoPackage/索引/性能 |
| **E. 几何与拓扑** | PIT-TOPO | 25 | 100 | 自相交/重叠/悬挂/空洞/多部件/退化几何 |
| **F. 三维与点云** | PIT-3D | 15 | 80 | 倾斜/3DTiles/LiDAR/CSF/纹理/单体化 |
| **G. WebGIS与发布** | PIT-WEB | 10 | 80 | WMS/WFS/瓦片/跨域/缓存/权限 |
| **H. AI/深度学习** | PIT-AI | 5 | 60 | ERROR999999/样本/GPU/预测结果/GIS输出 |
| **I. 批量处理与自动化** | PIT-BATCH | 10 | 60 | ArcPy/FME/QGIS Processing/性能/内存 |
| **J. 标准与合规** | PIT-STD | 5 | 60 | 国标偏差/质量评定/坐标保密/脱密/汇交 |
| **总计** | | **160+** | **800+** | |

---

## 标准化条目格式（WRONG/CAUSE/SOLUTION/CODE）

```yaml
pitfall:
  id: "PIT-TOPO-025"
  category: "几何与拓扑"
  severity: "严重"  # 致命/严重/一般/轻微
  wrong: "面要素层执行Dissolve后出现奇怪空洞"
  cause: "源数据中存在自相交/无效几何，Dissolve时算法无法正确合并拓扑"
  solution: 
    - "执行Dissolve前先用RepairGeometry修复无效几何"
    - "检查源数据是否存在极小缝隙(<0.01m²)"
    - "使用FME GeometryValidator预处理"
  code_python: |
    import arcpy
    arcpy.management.RepairGeometry("input_fc")
    arcpy.management.Dissolve("input_fc", "output_fc", dissolve_field="")
  code_fme: |
    Reader[Shapefile] → GeometryValidator[FixInvalid] → Dissolver → Writer[GDB]
  software: ["ArcGIS Pro", "FME", "QGIS"]
  related_pitfalls: ["PIT-TOPO-003", "PIT-TOPO-018"]
  verified_versions: ["ArcGIS Pro 3.6", "ArcGIS Pro 3.7"]
```

---

## 报错码速查索引（ERROR 999999 / GDAL / FME）

### ArcGIS 常见报错码

| 错误码 | 含义 | 避坑编号 | 快速处理 |
|--------|------|----------|----------|
| ERROR 000210 | 无法创建输出 | PIT-SFT-001 | 输出路径不存在/无写权限 |
| ERROR 000229 | 无法打开输入 | PIT-SFT-002 | 路径含中文/文件被锁定 |
| ERROR 000258 | 字段不存在 | PIT-SFT-003 | 字段名拼写/大小写 |
| ERROR 000354 | 名称包含无效字符 | PIT-SFT-004 | 字段名以数字开头/含特殊字符 |
| ERROR 000464 | 独占模式冲突 | PIT-SFT-005 | 数据被其他进程锁定 |
| ERROR 000582 | 坐标系无效 | PIT-CRS-001 | GCS未定义/自定义投影参数错误 |
| ERROR 000623 | 参与分析的数据坐标系不匹配 | PIT-CRS-002 | 不同GCS混合使用 |
| ERROR 000725 | 输出已存在 | PIT-SFT-006 | arcpy.env.overwriteOutput = True |
| ERROR 000735 | 输入要素无几何 | PIT-TOPO-001 | 含空几何的记录/属性表错误 |
| ERROR 000800 | 无法获取锁 | PIT-SFT-007 | GDB被其他用户编辑 |
| ERROR 000824 | 工具未获得许可 | PIT-SFT-008 | 扩展模块未激活(3D/Spatial/Network) |
| ERROR 001156 | 无法打开OID字段 | PIT-DB-001 | GDB损坏/版本不兼容 |
| ERROR 999999 | 未知严重错误(最经典!) | PIT-AI-001 | GPU显存不足/数据过大/驱动问题 |

### GDAL 常见错误

| 错误码 | 含义 | 避坑编号 | 快速处理 |
|--------|------|----------|----------|
| ERROR 1: PROJ: proj_create... | PROJ转换失败 | PIT-CRS-005 | EPSG码不存在/网格文件缺失 |
| ERROR 4: file not recognized | 格式不支持 | PIT-FMT-005 | 缺失驱动/版本过低 |
| ERROR 6: Too many points... | 要素加载超限 | PIT-BATCH-001 | 分块处理/大数据模式 |

### FME 转换异常速查

| 异常 | 原因 | 避坑编号 |
|------|------|----------|
| "Invalid coordinate system" | 源坐标系未定义或FME不识别的WKID | PIT-CRS-008 |
| "Geometry is not valid" | 自相交/退化多边形 | PIT-TOPO-010 |
| "Schema attributes mismatch" | 源/目标字段类型不匹配 | PIT-FMT-012 |
| "Memory allocation failure" | 数据量超FME内存限制 | PIT-BATCH-015 |

---

## 八大类精选条目示例（每类3条）

### A. 坐标系 (PIT-CRS)

**PIT-CRS-015: RTK测量坐标与GIS数据对不上**
- WRONG: RTK默认输出WGS84坐标，手簿未配CGCS2000转换参数
- CAUSE: WGS84与CGCS2000在中国区域有0.5-3m系统偏差
- SOLUTION: 手簿配置CORS基准站(CGCS2000坐标)/手动输入七参数/使用省级CORS自动转换
- CODE: 见04_EXPANSION_V5 第二节

**PIT-CRS-022: 同一省内两批DLG数据无法拼接**
- WRONG: 一批用3度带(105°E)，另一批用6度带(105°E)，看似中央子午线相同
- CAUSE: 3度带36号=108°E，6度带18号=105°E，并不相同
- SOLUTION: 统一转换为CGCS2000 3度带后再拼接

**PIT-CRS-038: 高程异常值在ArcGIS中无法自动获取**
- WRONG: 直接使用ArcGIS默认的高程转换
- CAUSE: ArcGIS高程转换需单独安装EGM2008/省级似大地水准面网格文件
- SOLUTION: 从自然资源部下载省级精化似大地水准面.gtx文件，放入ArcGIS pedata目录

### E. 几何与拓扑 (PIT-TOPO)

**PIT-TOPO-018: Buffer后出现奇怪的尖刺**
- WRONG: 源数据存在极小自相交(肉眼不可见，<0.001m)
- CAUSE: 自相交点处Buffer算法会放大异常，生成尖刺
- SOLUTION: Buffer前执行RepairGeometry + Simplify(容差0.001m)

**PIT-TOPO-032: Erase后出现超细线条**
- WRONG: 两个面之间存在微小的位置偏差(0.0001m级)
- CAUSE: 不同软件/不同年度的数据，数字化精度不一致
- SOLUTION: Erase前对两个面执行Snap(捕捉容差0.01m)

**PIT-TOPO-045: Intersect结果面数量远超预期**
- WRONG: 存在大量碎片面(1cm-10cm级别)
- CAUSE: 多次编辑/CAD转换引入的微小碎片
- SOLUTION: Intersect后按面积过滤(>1m²)，保留有效面

### H. AI/深度学习 (PIT-AI)

**PIT-AI-001: arcpy深度学习工具报ERROR 999999**
- WRONG: 影像tile_size设置过大→GPU显存溢出→ArcGIS崩溃
- CAUSE: ArcGIS Pro深度学习框架对显存管理不完善
- SOLUTION: tile_size从256开始，逐步降低(128→64)，batch_size=1

**PIT-AI-015: 模型预测结果全是一个类别**
- WRONG: 训练样本类别严重不平衡(正负比 > 1:20)
- CAUSE: 模型学到了"永远预测多数类"的最短路径
- SOLUTION: 使用加权损失函数/Focal Loss/过采样少数类

**PIT-AI-028: SAM分割的建筑轮廓无法直接用于GIS**
- WRONG: 直接使用SAM生成的锯齿状粗糙轮廓
- CAUSE: SAM输出为像素级掩膜，未做几何后处理
- SOLUTION: 1)形态学开闭运算平滑 2)Douglas-Peucker简化 3)直角化规则化 4)最小面积过滤

---

## 18大行业案例框架（V5.0新增10行业）

### V1.0已有（8行业）
1. 城市规划（学校步行圈/用地适宜性）
2. 国土资源（GDB→CASS→DWG全流程/不动产）
3. 环保遥感（GEE土地利用变化/光纤故障预测）
4. 商业选址（连锁门店分析）
5. 测绘地籍（丹江口/地籍调查）
6. 市政管线（三维可视化/气候脆弱性）
7. 林业资源（新增案例）
8. 航测DOM+DEM（无人机全流程）

### V5.0新增（10行业）
9. **水利防洪** — SWAT+GIS水文模型/洪水淹没模拟/水库选址
10. **电力管线** — 输电线路路径优化/杆塔三维/电力巡检
11. **道路交通** — 路网分析/OD流量/公交线路优化
12. **智慧城市** — 物联网+GIS/城市体征/网格化管理
13. **生态修复** — 生态红线/矿山修复监测/植被恢复评估
14. **矿山治理** — 三维地质建模/储量估算/沉降监测
15. **油气管道** — 管道选线/腐蚀风险评估/爆管模拟
16. **轨道交通** — 地铁保护线/沿线沉降/客流预测
17. **历史文化保护** — 古建筑三维/文物普查/保护范围
18. **应急测绘** — 灾害快速制图/无人机应急/损失评估
19. **通信基站** — 基站覆盖/网络优化/5G选址
20. **环境监测** — 水质/大气/噪声空间分析
21. **地下管网** — 综合管线/碰撞检测/三维管网
22. **实景三维城市** — 城市级精细模型/LOD2-3单体化

每个案例标配：需求单 + 完整技术流程 + 可运行代码 + 质检报告模板 + 交付归档清单

---

> **V5.0 新增说明**：避坑库从160条目扩展至800+目标（八大类10子类框架+精选条目示例+报错码速查索引）。18大行业案例从8行业扩展至22行业（包含V5.0新增14行业框架）。
