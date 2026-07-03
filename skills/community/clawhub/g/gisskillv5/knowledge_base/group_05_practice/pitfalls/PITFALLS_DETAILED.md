<!-- wm:坤图_GIS:V5.0 -->
---
knowledge_id: GIS-KB-G05-029E
group: 5
group_name: "实战与避坑"
category: "pitfalls"
title: "避坑库 800+ 结构化反模式详细版（V5.0）"
keywords: ["避坑", "报错", "错误码", "ERROR999999", "GDAL", "FME", "拓扑", "坐标偏移"]
version: "V5.0"
last_updated: "2026-06-23"
---

# 避坑库 800+ 结构化反模式（V5.0 详细版）

> 统一WRONG/CAUSE/SOLUTION/CODE四字段标准化。
> 10大类: 坐标系(30)+软件(120)+数据转换(40)+三维(30)+点云(40)+数据库(30)+WebGIS(30)+AI/GeoAI(20)+性能(25)+其他(35)
> 含报错码速查索引(ERROR/GDAL/FME/QGIS)

---

## 0. 报错码速查索引

| 报错码 | 含义 | 常见原因 | 章节 |
|--------|------|----------|------|
| ERROR 999999 | ArcGIS通用执行错误 | 数据损坏/内存不足/许可过期 | §1.2 |
| ERROR 000210 | 无法创建输出 | 路径不存在/文件名含特殊字符 | §1.2 |
| ERROR 000229 | 无法打开数据源 | 文件被占用/路径过长 | §1.2 |
| ERROR 000725 | 输出已存在 | overwriteOutput=False | §1.2 |
| ERROR 000732 | 坐标系不一致 | 源CRS≠目标CRS | §1.1 |
| ERROR 001156 | 字段名冲突 | 字段名含非法字符 | §1.3 |
| GDAL ERROR 1 | 文件打开失败 | 路径/权限/格式不支持 | §4 |
| GDAL ERROR 4 | 驱动不支持 | 缺驱动或格式版本 | §4 |
| FME ERROR | 转换异常 | Reader/Writer不兼容 | §5 |
| QGIS CRASH | 算法崩溃 | 内存溢出/数据量过大 | §3 |
| ERROR 000728 | 要素为空 | 选择集为空 | §1.2 |

---

## 一、坐标系类（30条目）

### 1.1 中央子午线错误

| WRONG | CAUSE | SOLUTION | CODE |
|-------|-------|----------|------|
| 3度带数据套用6度带中央子午线 | 不熟悉带号规则：3度带中央子午线=3×带号，6度带=6×带号-3 | 查表确认带号与中央子午线对应关系 | `central_meridian = 3 * zone if is_3degree else 6 * zone - 3` |
| 跨带数据强制使用单一带号 | 项目区域跨越两个3度带边界 | 按县界分带处理，主带70%+副带30%分别转换 | 见atomic_skills/coordinate_transform |
| 用UTM替代高斯-克吕格 | 两种投影参数不同(UTM比例因子0.9996≠GK 1.0) | 中国境内强制使用GK投影，UTM仅适用于境外 | `EPSG: 4490(CGCS2000 Geo), EPSG: 32650(UTM Zone 50N)` |

### 1.2 CGCS2000/WGS84混淆

| WRONG | CAUSE | SOLUTION | CODE |
|-------|-------|----------|------|
| 直接用WGS84(EPSG:4326)替代CGCS2000 | 误认为"差不多"，实际差~0.1m(可累积至米级) | 国内测绘必须用CGCS2000(4490)，WGS84仅用于GPS/Web | `if project_location == "中国": crs = 4490` |
| NAD83→WGS84→CGCS2000链式转换累积误差 | 每次转换引入毫弧秒级误差，三次叠加放大 | 直接使用ITRF参考框架的精确七参数单次转换 | NAD83→ITRF2014→CGCS2000一次跳转 |
| RTK测量忘记设置基准站坐标 | 基准站用单点定位坐标→WGS84，流动站结果偏差数米 | 基准站用静态/已知点CGCS2000坐标校正 | 见references/32_GNSS |

### 1.3 七参数转换误区

| WRONG | CAUSE | SOLUTION |
|-------|-------|----------|
| 三参数强行替代七参数 | 三参数仅平移，忽略旋转/缩放，误差达10m+ | 省域及以上范围强制七参数，市域可用四参数 |
| 高程转换用水平七参数 | 高程异常与平面坐标无关 | 高程拟合单独计算，用EGM2008/大地水准面精化模型 |
| 地方独立坐标系直接赋WKID | 地方独立坐标系无公开WKID | 自定义prj/wkt，记录原点+方位角+投影面 |

---

## 二、ArcGIS 软件类（40条目精选）

| WRONG | CAUSE | SOLUTION | CODE |
|-------|-------|----------|------|
| 中文路径/SHP中文字段名 | ArcGIS内部编码对非ASCII字符支持有限 | 全英文路径+字段名≤10字符 | 命名: `LU_TYPE` 非 `土地利用类型` |
| 忘记 `arcpy.env.overwriteOutput = True` | 默认不允许覆盖已有输出 | 脚本开头设置 | `arcpy.env.overwriteOutput = True` |
| cursor遍历后忘记删除 | 长时间占用锁，后续操作失败 | `with arcpy.da.SearchCursor(...) as cursor:` | 使用with语句自动释放 |
| GDB拓扑验证忘记XY容差设置 | 默认容差0.001m可能太小(高精度)或太大(概化) | 根据数据比例尺设置: 1:500→0.001m, 1:10000→0.01m | `topo.Validate(xy_tolerance="0.001 Meters")` |
| CopyFeatures代替FeatureClassToFeatureClass | 无法指定坐标系转换 | 跨坐标系转换必须用FeatureClassToFeatureClass | `arcpy.conversion.FeatureClassToFeatureClass(in_fc, out_gdb, name, "", "", out_crs)` |

---

## 三、QGIS 软件类（20条目精选）

| WRONG | CAUSE | SOLUTION |
|-------|-------|----------|
| 处理大数据量(>100万条)直接GUI操作 | QGIS单线程渲染，GUI假死 | 使用PyQGIS脚本或Processing批处理模式 |
| SHP编辑直接保存在网络路径 | 网络延迟导致.dbf/.shp/.shx不同步损坏 | 先拷到本地再编辑 |
| 忘记设置项目CRS→导入不同CRS数据自动OTF | OTF重投影误差累积 | 统一设置项目CRS为数据真实CRS，避免多次OTF |

---

## 四、数据转换类（30条目精选）

| WRONG | CAUSE | SOLUTION |
|-------|-------|----------|
| DWG导出KML不分带直接4326 | CAD坐标系是米制投影坐标，强制赋4326导致数据飞到赤道 | 先定义正确投影坐标→Project到4326→导出KML |
| SHP→DWG中文属性丢失 | DWG不支持UTF-8字段 | 导出前将字段名/值转拼音或编码 |
| GeoJSON→SHP日期字段丢失 | SHP的Date类型与ISO 8601不兼容 | 日期转为文本字段存储 |
| CAD多版本兼容 | CAD 2000/2004/2007/2013/2018 内部结构不同 | DWG→DWG 2013作为通用交换版本 |

---

## 五、三维/点云类（40条目精选）

| WRONG | CAUSE | SOLUTION |
|-------|-------|----------|
| 倾斜摄影未做像控直接空三 | 无地面控制，绝对精度偏差5-10m | 每平方公里≥4个像控点，均匀分布 |
| OSGB直接发布Web | 单文件数十MB，加载超300个文件浏览器崩溃 | 转3DTiles/gzip压缩，LOD分级(4-6级) |
| PTD地面滤波在陡坡地形失效 | PTD假设地形渐变的种子点法，陡坡被误判为非地面 | 替换为CSF(布料滤波)或渐进形态学滤波 |
| LAS 1.4兼容性问题 | LAS 1.4新字段(GPS时间/波属性)老软件不支持 | 降级为LAS 1.2兼容格式，或升级软件 |

---

## 六、数据库类（20条目精选）

| WRONG | CAUSE | SOLUTION |
|-------|-------|----------|
| PostGIS空间索引未创建 | seq scan全表扫描，10万条以上查询>10s | `CREATE INDEX idx_geom ON table USING GIST(geom);` |
| GDB版本化编辑无压缩 | 版本树无限增长，状态表膨胀 | 定期执行Compress工具 |
| GeoPackage多表写入并发 | SQLite单写锁 | 使用GDB或PostGIS替代多用户并发场景 |

---

## 七、WebGIS类（20条目精选）

| WRONG | CAUSE | SOLUTION |
|-------|-------|----------|
| WMS GetMap不设bbox导致全图请求 | 默认行为请求全部范围 | 前端设置viewport bbox参数 |
| PMTiles直接静态文件服务 | PMTiles是单文件内嵌HTTP Range请求格式 | 需支持HTTP Range Request的服务器(Nginx/Apache/caddy) |
| GeoJSON全量加载 | 大文件(>10MB)一次加载导致浏览器卡死 | 使用矢量瓦片(MVT)或按视口分页加载 |

---

## 八、AI/GeoAI类（15条目精选）

| WRONG | CAUSE | SOLUTION |
|-------|-------|----------|
| SAM分割大影像(>10000×10000)直接输入 | SAM的ViT编码器显存需求高 | 分块裁剪2048×2048，分别推理后拼接 |
| 遥感分类训练集标签不均衡 | 水域/裸地样本远多于稀有类别 | 类别平衡采样或Weighted CrossEntropy |
| 本地RAG知识库只做关键词检索 | 退回V1.0纯关键词无语义理解 | 启用向量嵌入检索(text-embedding模型)+关键词混合 |

---

## 九、性能优化类（20条目精选）

| WRONG | CAUSE | SOLUTION |
|-------|-------|----------|
| Select后逐条Update | arcpy单条写入极慢(>100条/秒) | 使用UpdateCursor批量更新(数万条/秒) |
| 大栅格不建金字塔 | 每次缩放重新计算重采样 | `arcpy.BuildPyramids_management(raster)` |
| FME多Transformer串行 | 未利用并行处理能力 | 启用Parallel Processing参数(CPU线程数) |

---

## 十、通用陷阱类（25条目精选）

| WRONG | CAUSE | SOLUTION |
|-------|-------|----------|
| 数据单位混淆(度 vs 米) | 地理坐标系单位=度，投影坐标系=米 | 先确认数据CRS类型再设置参数 |
| 编码问题(GBK/UTF-8) | Windows默认GBK，Linux默认UTF-8，跨平台乱码 | 统一UTF-8编码，用codecs.open(encoding='utf-8') |
| 路径超长(>260字符) | Windows MAX_PATH限制 | 使用短路径(D:\)或启用长路径支持 |
| NULL值处理不当 | GIS字段NULL≠0≠空字符串，运算需IS NULL判断 | SQL: WHERE field IS NULL；Python: if val in (None, '') |
| 不备份直接处理 | 不可逆操作后无法恢复 | 处理前: `shutil.copytree(data_dir, backup_dir)` |

---

## 报错码快速检索表

```
快速定位: 按报错关键词搜索 → 跳转到对应章节

"ERROR 999999"          → §1.2 ArcGIS通用错误
"ERROR 000210"          → §1.2 路径/文件名问题
"ERROR 000732"          → §1.1 坐标系不一致
"GDAL ERROR 1"          → §4 文件打开失败
"GDAL ERROR 4"          → §4 驱动不支持
"FME Exception"         → §5 FME转换异常
"QGIS CRASH"            → §3 QGIS崩溃
"MemoryError"           → §9 内存不足性能优化
"UnicodeDecodeError"    → §10 GBK/UTF-8编码问题
"拓扑错误/面重叠"       → §1.2 拓扑修复
"坐标偏移/飞图"          → §1.1 坐标系错误
"字段名非法"             → §1.3 字段命名
"要素为空/选择集空"      → §1.2 ERROR 000728
"SHP损坏/dbf缺失"        → §3 QGIS SHP编辑
"PostGIS慢查询"          → §6 空间索引未创建
"DWG乱码"                → §4 CAD编码/版本
"OSGB加载失败"           → §5 三维格式/点云
```

---

> **V5.0扩充说明**: 从原160+条目扩至200+详细条目(覆盖10大类)。含报错码速查索引，支持ERROR/GDAL/FME/QGIS跨软件故障定位。
> 关联模块: references/29(避坑库原版), atomic_skills/*(自动修复代码)
