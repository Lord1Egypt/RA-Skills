# SuperMap iDesktopX | 关联：12_ArcGIS_Pro.md 13_QGIS.md 25_三维GIS与数字孪生.md | 最新验证：2026年6月

> SuperMap GIS 2026（2026年5月26日发布）—— 国产GIS旗舰，智能体原生时代
> 数据来源：supermap.com.cn / 2026空间智能软件技术大会

---

## 一、软件体系

### 1.1 SuperMap GIS 2026 产品矩阵

| 产品 | 定位 | 版本状态 |
|------|------|---------|
| **SuperMap iDesktopX** | 跨平台二三维一体化桌面GIS | 2026（常规迭代） |
| **SuperMap iServer** | 高性能GIS服务器 | 2026 |
| **SuperMap AgentX** | 空间智能体桌面平台 | Pre-Beta ⭐ 全新 |
| **SuperMap AgentX Server** | 空间智能体服务平台 | 2026 |
| **SuperMap ClientX** | 二三维一体化Web客户端 | Beta ⭐ 全新 |
| **SuperMap MobileX for HarmonyOS** | 纯血鸿蒙移动端 | Beta ⭐ 全新 |
| **ActiveMap 系列** | 专业级GIS第二品牌 | ⭐ 全新重启 |
| **SuperMap Terra 系列** | 空间智能一体机 | ⭐ 全新 |

### 1.2 iDesktopX 定位

- **跨平台**：Windows / Linux / 国产OS（统信UOS/麒麟）
- **二三维一体化**：同一窗口二维+三维同步操作
- **原生信创**：适配国产CPU（飞腾/鲲鹏/海光）、GPU、操作系统
- **AI驱动**：AgentX智能体集成，自然语言交互操作GIS

### 1.3 下载与授权

| 项目 | 内容 |
|------|------|
| 官方下载 | https://www.supermap.com/ → 下载中心 |
| 试用授权 | 可申请90天免费试用许可 |
| 开发者 | 提供SDK和API（iObjects） |

---

## 二、iDesktopX 核心功能

### 2.1 数据管理

| 功能 | 说明 |
|------|------|
| **数据源类型** | UDB/UDBX（自有格式）、File GDB、PostGIS、Oracle Spatial、SQL Server Spatial、Shapefile、GeoPackage、GeoJSON 等 |
| **数据导入/导出** | 支持100+格式互转，含CAD/DXF/DWG |
| **坐标系管理** | 完整EPSG库 + 自定义投影，支持动态投影 |
| **数据转换** | 批量格式转换/批量投影转换/批量字段重命名 |

### 2.2 地图制图

| 功能 | 说明 |
|------|------|
| **符号化** | 唯一值/分级/统计图表/点密度/自定义符号 |
| **标注** | 自动标注/标注避让/标注转注记 |
| **布局出图** | 地图系列/图廓整饰/批量出图 |
| **地图瓦片** | 生成矢量瓦片/栅格瓦片，对接iServer发布 |

### 2.3 空间分析

| 分析类型 | 主要工具 |
|---------|---------|
| **矢量分析** | 缓冲区/叠加/融合/裁剪/空间连接 |
| **栅格分析** | 重分类/栅格计算/插值（IDW/Kriging/Spline）/坡度坡向/视域分析 |
| **网络分析** | 路径分析/服务区/最近设施/OD矩阵 |
| **三维分析** | 通视分析/天际线/阴影分析/淹没模拟 |
| **空间统计** | 热点分析/聚类/空间自相关/地理加权回归 |
| **水文分析** | 填洼/流向/汇流累积/流域提取 |

### 2.4 三维GIS（核心优势）

| 功能 | 说明 |
|------|------|
| **三维场景** | 球面场景+平面场景 |
| **数据支持** | 地形/影像/矢量/倾斜摄影/点云/BIM/3D Tiles |
| **倾斜摄影** | 直接加载OSGB，支持单体化 |
| **三维分析** | 剖面分析/可视域/天空线/开敞度 |
| **特效渲染** | 水面/天气/粒子/动态光源 |

---

## 三、SuperMap GIS 2026 全新能力

### 3.1 AgentX（空间智能体）⭐

```
核心理念：从「人找工具」→「智能体完成任务」

使用方式：
1. 自然语言描述需求（如"分析本区域过去5年土地利用变化"）
2. AgentX 自动调用 GIS 技能组合
3. 自动输出结果（地图/图表/报告）

支持能力域：
- 空间分析
- 遥感数据提取
- 数据质检
- 智能制图
- IM远程任务下达
```

### 3.2 ClientX（二三维一体化Web）⭐

- **一套API** 实现二三维统一（解决传统二三维框架分离痛点）
- 高保真特效：水面白浪、焦散、动态海洋
- 跨平台：PC/移动/大屏，一套代码多端部署
- 适配AI环境：Trae、CodeX、Claude Code

### 3.3 鸿蒙原生 MobileX ⭐

- 业界首款纯血鸿蒙（HarmonyOS）移动GIS平台
- 高保真二三维一体化场景渲染
- 多设备视图无缝切换

### 3.4 ActiveMap（专业级第二品牌）

- 定位："专业、简约、紧凑、按需选用"
- 提供 Desktop 和 Server 版本
- 支持智能体CLI调用

---

## 四、与 ArcGIS Pro / QGIS 对比

| 维度 | SuperMap iDesktopX | ArcGIS Pro | QGIS |
|------|-------------------|-----------|------|
| 国产/进口 | 国产（北京超图） | 美国（Esri） | 国际开源 |
| 信创适配 | ★★★★★ 全适配 | ★★☆☆☆ 无适配 | ★★★☆☆ 部分适配 |
| 三维能力 | ★★★★★ 原生强 | ★★★★☆ 逐步增强 | ★★★☆☆ 插件增强 |
| 分析能力 | ★★★★☆ | ★★★★★ | ★★★★☆ |
| 社区生态 | ★★★☆☆ 国内强 | ★★★★★ 全球最大 | ★★★★★ 开源社区 |
| AI能力 | ★★★★★ AgentX 2026 | ★★★☆☆ ArcGIS AI助手 | ★★★☆☆ |
| 学习成本 | 中 | 中-高 | 中 |
| 价格 | 商用收费（适中） | 商用收费（高） | 免费 |

---

## 五、典型工作流

### 5.1 国土空间规划数据建库

```
CAD规划图 (.dwg)
    ↓ SuperMap 导入
数据清洗（拓扑修复/属性标准化/坐标系统一）
    ↓
空间分析（叠加分析/缓冲区分级/适宜性评价）
    ↓
制图输出（规划图/现状图/分析图）
    ↓
UDBX 数据库入库 → iServer 发布服务
```

### 5.2 三维城市底座构建

```
倾斜摄影(OSGB) + 地形(DEM) + 影像(DOM)
    ↓ 加载到 SuperMap 三维场景
模型单体化（切割/属性挂接）
    ↓
BIM 数据集成（室内精细化）
    ↓
三维分析（视域/天际线/淹没）
    ↓
iServer 发布三维服务 → ClientX Web展示
```

---

## 六、大数据GIS与分布式分析 ⭐ V4.0深度扩充

### 6.1 分布式存储架构

| 组件 | 说明 |
|------|------|
| **HDFS 分布式存储** | SuperMap iServer 支持将海量空间数据分布式存储于 HDFS，支持 UDBX/GeoTIFF/Shapefile 等格式的分布式管理 |
| **分布式空间索引** | 基于 R-Tree / Grid 的分布式空间索引，支持亿级要素的秒级空间查询 |
| **数据分片策略** | 按空间范围（网格分片）/ 按属性（哈希分片）/ 混合策略，确保计算负载均衡 |

```
数据分片流程：
原始数据 → 空间均匀切分 → 各节点独立存储 → 构建局部索引 → 全局索引注册
关键参数：
  - 分片数量 = 集群节点数 × 每节点分片数（建议2-3倍）
  - 分片大小阈值：单分片建议 ≤ 1GB（矢量）或 ≤ 4GB（栅格）
```

### 6.2 大数据空间分析

| 分析类型 | 说明 | 适用场景 |
|---------|------|---------|
| **分布式缓冲区分析** | 将缓冲区计算任务分发到各节点并行执行，最后合并结果 | 大范围设施覆盖分析 |
| **分布式叠加分析** | 裁剪/求交/擦除等操作在分布式环境下并行执行 | 省级国土数据叠加 |
| **分布式密度分析** | 基于空间分片的点密度/线密度计算，并行聚合 | 人口密度/POI热力分析 |
| **大数据核密度估计** | 基于 GPU 加速的核密度计算，支持千万级点数据 | 犯罪热点/疾病聚集分析 |

```
iServer 大数据分析配置示例：
# iServer 管理页面 → 服务 → 大数据分析
分析类型：缓冲区分析
输入数据源：HDFS 上的 UDBX 数据集
分片数：自动（= 集群可用节点数）
输出：结果写入目标数据源
```

### 6.3 流数据处理

| 组件 | 说明 |
|------|------|
| **Kafka 数据接入** | iServer 支持从 Kafka 消费实时空间数据流（GeoJSON/WKT/自定义格式） |
| **实时轨迹渲染** | 接收动态轨迹点，在地图上实时渲染运动轨迹和位置 |
| **实时热力图** | 基于实时流入的点数据，动态更新热力图密度分布 |

```
流数据处理架构：
Kafka Topic → iServer 流数据接收器 → 实时空间索引更新
                                      → WebSocket 推送前端
                                      → 热力图/轨迹图层实时刷新

配置要点：
  - Kafka 消费者组需与 iServer 实例数匹配（1:1或N:1）
  - 流数据坐标系需与底图一致，否则实时投影会引入延迟
  - 建议消息格式：GeoJSON FeatureCollection（标准且前端友好）
```

---

## 七、iServer REST API 完整调用 ⭐ V4.0新增

### 7.1 服务发布

```bash
# RESTful 方式发布地图服务
POST http://localhost:8090/iserver/servicesmanager/services.json
Content-Type: application/json

{
  "type": "RESTMAP",
  "name": "map-demo",
  "parameter": {
    "resourcesConfigName": "China_4326",
    "clusterInfo": "single",
    "cacheEnabled": true
  }
}
```

```
服务类型：
  RESTMAP      → 二维地图服务
  REST3D      → 三维地图服务
  RESTDATA    → 数据服务
  RESTSPATIALANALYST → 空间分析服务
  RESTNETWORKANALYST → 网络分析服务
```

### 7.2 空间查询 API

```javascript
// REST API 空间查询
const response = await fetch(
  'http://server:8090/iserver/services/map-demo/rest/maps/China/query.json', {
    method: 'POST',
    body: JSON.stringify({
      datasetNames: ["Provinces"],
      queryParameter: {
        attributeFilter: "POPULATION > 50000000",
        spatialQueryObject: {
          geometry: { /* GeoJSON */ },
          spatialQueryMode: "INTERSECT"
        }
      }
    })
  }
);
```

```
空间查询模式（spatialQueryMode）：
  CONTAIN       → 包含
  CROSSED       → 相交（线与面）
  INTERSECT     → 相交（通用）
  INTERSECTNOT  → 不相交
  OVERLAP       → 叠加
  TOUCH         → 接触
  WITHIN        → 被包含
  DISPOSE       → 邻接

分页参数：
  maxFeatures    → 返回最大记录数
  startRecord    → 起始记录偏移
```

### 7.3 三维服务

```
S3M 缓存生成流程：
1. iDesktopX → 三维数据 → 生成三维缓存（SCP格式）
2. 配置缓存参数：
   - 缓存类型：S3M（推荐）/ 3DTiles
   - 切分层级：根据数据范围和精度需求
   - 纹理压缩：自动（DXT/CRN/ASTC）
3. iServer → 发布三维服务

三维服务发布：
POST http://localhost:8090/iserver/servicesmanager/services.json
{
  "type": "REST3D",
  "name": "scene-city",
  "parameter": {
    "scenarios": ["scenefolder_name"],
    "cacheEnabled": true
  }
}
```

```javascript
// 前端调用三维服务（ClientX 示例）
const scene = new SuperMap.Scene3D('container');
scene.addLayer({
  type: 'S3M',
  url: 'http://server:8090/iserver/services/scene-city/rest/realspace/scenes/scene.json',
  name: 'city_model'
});
```

### 7.4 Token 认证

```
iServer 安全认证方式：

1. Key 认证（API Key）
   - 适用场景：内网/低安全要求
   - 配置：iServer 管理页面 → 安全 → Key认证
   - 使用：URL 参数 ?key=YOUR_API_KEY

2. Token 认证（推荐）
   - 适用场景：外网/生产环境
   - 流程：
     a) 客户端发送用户名+密码到认证接口
     b) 服务端验证后返回 Token（默认有效期24小时）
     c) 后续请求在 Header 中携带 Token

Token 获取：
POST http://server:8090/iserver/services/security/tokens.json
Body: { "username": "admin", "password": "xxx", "clientType": "WEB" }

Token 使用：
Header: Authorization: Bearer <token>
或 URL: ?token=<token>
```

---

## 八、AgentX 实战案例

### 8.1 智能质检对话示例

```
用户："检查这个数据集的质量，出报告"
AgentX → 调用技能：数据质检Skill
→ 执行：几何检查+属性检查+拓扑检查
→ 输出：质检报告.docx + 问题清单.xlsx
```

```
AgentX 内置技能清单（2026 Pre-Beta）：

空间分析类：
  "缓冲区分析" / "叠加分析" / "路径分析" / "选址分析"

数据管理类：
  "数据质检" / "格式转换" / "坐标转换" / "属性标准化"

遥感处理类：
  "影像分类" / "变化检测" / "NDVI计算" / "影像融合"

制图输出类：
  "智能制图" / "专题图制作" / "批量出图" / "图廓整饰"
```

### 8.2 AgentX 接入IM

```
企业微信/钉钉接入配置：

1. AgentX Server → 开启 IM 接口
2. 配置 Webhook 回调地址：
   - 企业微信：https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx
   - 钉钉：https://oapi.dingtalk.com/robot/send?access_token=xxx

3. 远程任务下发流程：
   IM消息 → AgentX Server接收 → 解析任务意图
   → 匹配技能 → 调用 iDesktopX/iServer 执行
   → 结果回传IM（报告文件/地图截图/分析结果）

注意事项：
  - 任务描述尽量明确（含数据路径、分析参数）
  - 大数据量任务建议先确认再执行
  - 结果文件需确认用户有下载权限
```

### 8.3 自定义 Skill 开发

```
Skill 开发流程：

1. 创建 Skill 配置文件（JSON）：
   {
     "name": "my_analysis",
     "displayName": "自定义分析工具",
     "description": "执行自定义空间分析流程",
     "version": "1.0",
     "entryPoint": "main.py",
     "parameters": [
       {"name": "input_dataset", "type": "dataset", "required": true},
       {"name": "buffer_distance", "type": "number", "default": 500}
     ],
     "outputs": ["result_dataset", "report"]
   }

2. 编写 Skill 主逻辑（Python）：
   from iobjectspy import *
   def main(input_dataset, buffer_distance):
       ds = Datasources.open(input_dataset.datasource)
       result = Analyst.buffer(
           ds[input_dataset.name],
           "buffer_result",
           buffer_distance,
           "Meter"
       )
       return {"result_dataset": result}

3. 注册到 AgentX：
   AgentX → Skill 管理 → 导入 Skill → 测试 → 发布
```

---

## 九、开发扩展

### 9.1 Python 脚本（SuperMap iObjects Py）

```python
# SuperMap 空间分析示例
from iobjectspy import *

# 打开数据源
datasource = Datasources.open(r"D:\data.udbx")

# 缓冲区分析
dataset = datasource["Buildings"]
result = Analyst.buffer(dataset, "BufferResult", 100, "Meter")
```

### 9.2 iServer REST API

```
# 查询服务
GET http://localhost:8090/iserver/services/map-world/rest/maps/World/query.json
  ?returnContent=true
  &maxFeatures=10
```

---

## 十、常见问题 ⭐ V4.0更新

| 问题 | 原因 | 方案 |
|------|------|------|
| Linux运行异常 | 依赖库缺失 | 安装官方依赖包列表（官网文档有） |
| OSGB加载慢 | 模型数据量大 | 创建三维缓存(.scp) 加速加载 |
| 许可过期 | 试用许可到期 | 重新申请试用许可/购买正式许可 |
| 中文注记乱码 | 字体缺失或编码问题 | 安装中文字体包，设置UTF-8编码 |

---

> 关联阅读：`12_ArcGIS_Pro.md`（对标产品） | `13_QGIS.md`（开源替代） | `25_三维GIS与数字孪生.md`（倾斜摄影章节）


<!-- wm:坤图_GIS:V1.0 -->
