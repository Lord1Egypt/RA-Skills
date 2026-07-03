# WebGIS与地图服务发布 | 关联：22_空间数据库.md 25_三维GIS与数字孪生.md | V4.0深度扩充 2026-06-04

> 来源：OGC 标准文档 + GeoServer/ArcGIS Server 官方文档 + Leaflet/OpenLayers 官方指南
> V4.0 扩充：Cesium+Vue3完整项目 | ol-cesium 2D/3D联动 | OpenLayers WebGL | 矢量瓦片实战
> 最后更新：2026-06-04

---

## 一、OGC 服务标准

### 1.1 四大核心标准速查

| 标准 | 全称 | 返回内容 | 操作 | 典型请求格式 |
|------|------|---------|------|------------|
| **WMS** | Web Map Service | 地图图片(PNG/JPEG) | GetCapabilities / GetMap / GetFeatureInfo | `?REQUEST=GetMap&LAYERS=roads&BBOX=...` |
| **WFS** | Web Feature Service | 矢量数据(GML/GeoJSON) | GetCapabilities / DescribeFeatureType / GetFeature / Transaction | `?REQUEST=GetFeature&TYPENAME=parcels` |
| **WMTS** | Web Map Tile Service | 预渲染瓦片(PNG/JPEG) | GetCapabilities / GetTile | `?REQUEST=GetTile&TileMatrix=10&TileRow=512&TileCol=512` |
| **WCS** | Web Coverage Service | 栅格原始数据(GeoTIFF/NetCDF) | GetCapabilities / DescribeCoverage / GetCoverage | `?REQUEST=GetCoverage&COVERAGE=elevation` |

### 1.2 WMS vs WMTS 选择指南

| 场景 | 推荐 | 原因 |
|------|------|------|
| 动态样式/过滤 | **WMS** | 每次请求实时渲染 |
| 底图/高频访问 | **WMTS** | 预渲染瓦片缓存，性能极高 |
| 多客户端共享底图 | **WMTS** | 瓦片 CDN 分发，前端零计算 |
| 用户自定义样式 | **WMS** | SLD 样式实时应用 |
| 数据更新频繁 | **WMS** | 无需重建瓦片缓存 |

### 1.3 瓦片金字塔原理

```
Level 0: 1 tile (全球)
         ┌──┐
Level 1: └──┴──┘  2×2 tiles
         ┌──┬──┬──┐
Level 2: ├──┼──┼──┤  4×4 tiles
         └──┴──┴──┘
...
Level N: 2^N × 2^N tiles
```

**关键参数**：
- **Tile Size**：256×256 或 512×512 像素
- **Origin**：通常 (-20037508.34, 20037508.34)（Web Mercator）
- **Resolutions**：每级分辨率 = 初始分辨率 / 2^level

### 1.4 坐标系约定

Web GIS 最常用坐标系：

| 坐标系 | EPSG | 用途 | 特点 |
|--------|------|------|------|
| **WGS84** | `EPSG:4326` | 全球数据存储、GPS原始坐标 | 经纬度（度） |
| **Web Mercator** | `EPSG:3857` | **瓦片地图标准** ⭐ | 米单位，投影为正方形 |
| **CGCS2000** | `EPSG:4490` | 中国测绘数据 | 经纬度 |
| **CGCS2000 GK** | `EPSG:4549`(3°) | 中国大比例尺地形图 | 高斯投影米单位 |

---

## 二、服务端方案对比

### 2.1 ArcGIS Server vs GeoServer

| 维度 | ArcGIS Server | GeoServer |
|------|-------------|-----------|
| **许可** | 商业许可（按核/按用户） | 开源免费（GPL） |
| **部署** | Windows/Linux + IIS/Tomcat | Java Servlet容器(Tomcat/Jetty) |
| **数据源** | GDB/SDE 原生支持 ⭐ | PostGIS/SHP/GeoTIFF（需扩展GDB） |
| **OGC 支持** | WMS/WFS/WCS/WMTS/WPS | WMS/WFS/WCS/WMTS/WPS |
| **管理界面** | ArcGIS Server Manager + Portal | GeoServer Web Admin |
| **样式定义** | ArcGIS Pro 符号→发布 | SLD(OGD风格描述)/CSS |
| **缓存策略** | 紧凑型/松散型瓦片 | GeoWebCache 集成 |
| **集群扩展** | 站点模式（多机） | 无状态+负载均衡 |
| **适用场景** | ArcGIS 生态企业用户 | 轻量/预算有限/开源优先项目 |

### 2.2 GeoServer 核心配置速查

```bash
# GeoServer 典型目录结构
geoserver/
├── data_dir/          # 数据目录（工作区、数据存储、样式）
│   ├── workspaces/    # 工作区（命名空间隔离）
│   ├── styles/        # SLD 样式文件
│   └── gwc/           # GeoWebCache 瓦片缓存
└── webapps/geoserver/ # 部署文件
```

**发布流程**：
```
创建工作区 → 添加数据存储(PostGIS/Shapefile/GeoTIFF)
→ 发布图层(配置坐标系/样式/缓存)
→ 预览图层(OpenLayers预览)
```

---

## 三、前端框架对比

### 3.1 五大框架速查

| 框架 | 体积 | 数据驱动 | 3D | 矢量瓦片 | 适用场景 |
|------|------|---------|-----|---------|---------|
| **Leaflet** | ~40KB | 插件 | ✗(插件) | 插件 | **轻量地图展示首选** |
| **OpenLayers** | ~200KB | 内置 | ✗(实验) | ✅ | 专业 GIS 功能 |
| **Mapbox GL JS** | ~350KB | 矢量瓦片 | 2.5D | ✅ 原生 | 炫酷可视化 |
| **MapLibre GL** | ~250KB | 矢量瓦片 | 2.5D | ✅ 原生 | Mapbox开源替代 |
| **CesiumJS** | ~2MB | 3D Tiles | ✅ 原生 | ✗(3D Tile) | **三维地球/GIS** |

### 3.2 框架选择决策树

```
需要3D地球？ → YES → CesiumJS ⭐
      ↓ NO
需要炫酷可视化/矢量瓦片？ → YES → MapLibre GL（免费优先）/ Mapbox GL JS
      ↓ NO
需要复杂GIS分析/多源数据叠加？ → YES → OpenLayers
      ↓ NO
轻量展示即可 → Leaflet ⭐
```

---

## 四、OpenLayers + Cesium 二三维联动 ⭐ V4.0 完整项目

### 4.1 技术栈

| 工具 | 版本 | 作用 |
|------|------|------|
| Vue 3 + Composition API | 3.x | 构建前端UI |
| OpenLayers | ^10.x | 2D地图引擎 |
| CesiumJS | ^1.131 | 3D地球引擎 |
| ol-cesium | ^2.17 | OpenLayers↔Cesium 桥梁 |
| Vite | ^5.x | 构建工具 |
| vite-plugin-cesium | ^1.x | 自动处理Cesium静态资源 |

### 4.2 完整项目搭建

```bash
# 创建项目
npm create vite@latest webgis-3d -- --template vue-ts
cd webgis-3d

# 安装依赖
npm install ol cesium ol-cesium
npm install -D vite-plugin-cesium
```

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import cesium from 'vite-plugin-cesium'

export default defineConfig({
  plugins: [
    vue(),
    cesium()  // 自动设置 CESIUM_BASE_URL
  ]
})
```

### 4.3 核心组件：MapSwitcher.vue

```vue
<template>
  <div class="full-screen">
    <div ref="mapContainer" class="map-container"></div>
    
    <!-- 控制面板 -->
    <div class="control-panel">
      <button class="toggle-btn" @click="toggle3D">
        {{ is3D ? '切换到 2D' : '切换到 3D' }}
      </button>
      <div class="coord-info" v-if="mouseCoord">
        Lng: {{ mouseCoord[0].toFixed(4) }} / Lat: {{ mouseCoord[1].toFixed(4) }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'
import 'ol/ol.css'
import { Map, View } from 'ol'
import TileLayer from 'ol/layer/Tile'
import OSM from 'ol/source/OSM'
import { fromLonLat, toLonLat } from 'ol/proj'
import VectorLayer from 'ol/layer/Vector'
import VectorSource from 'ol/source/Vector'
import GeoJSON from 'ol/format/GeoJSON'
import { Style, Stroke, Fill, Circle as CircleStyle } from 'ol/style'

// 声明全局Cesium
declare global {
  interface Window {
    CESIUM_BASE_URL: string
    Cesium: any
  }
}
window.CESIUM_BASE_URL = './node_modules/cesium/Build/Cesium'
import * as Cesium from 'cesium'
window.Cesium = Cesium
import 'cesium/Build/Cesium/Widgets/widgets.css'
import OLCesium from 'ol-cesium'

const mapContainer = ref<HTMLDivElement | null>(null)
const is3D = ref(false)
const mouseCoord = ref<[number, number] | null>(null)

let map: Map
let olCesiumObj: any

onMounted(() => {
  // 1. 初始化2D地图
  map = new Map({
    target: mapContainer.value!,
    layers: [
      new TileLayer({ source: new OSM() })
    ],
    view: new View({
      center: fromLonLat([116.4, 39.9]),  // 北京
      zoom: 12
    })
  })

  // 2. 添加矢量图层示例
  const vectorLayer = new VectorLayer({
    source: new VectorSource({
      features: new GeoJSON().readFeatures({
        type: 'FeatureCollection',
        features: [
          {
            type: 'Feature',
            geometry: { type: 'Point', coordinates: [116.4, 39.9] },
            properties: { name: '北京中心' }
          }
        ]
      })
    }),
    style: new Style({
      image: new CircleStyle({ radius: 8, fill: new Fill({ color: '#ff0000' }) })
    })
  })
  map.addLayer(vectorLayer)

  // 3. 初始化ol-cesium
  try {
    olCesiumObj = new OLCesium({ map: map })
    olCesiumObj.setEnabled(false)
    initCesiumTerrain()
  } catch (error) {
    console.error('Cesium初始化失败:', error)
  }

  // 4. 鼠标坐标跟踪
  map.on('pointermove', (e) => {
    mouseCoord.value = toLonLat(e.coordinate) as [number, number]
  })
})

function initCesiumTerrain() {
  if (window.Cesium?.createWorldTerrainAsync) {
    window.Cesium.createWorldTerrainAsync({
      requestWaterMask: true,
      requestVertexNormals: true
    }).then((terrainProvider: any) => {
      if (olCesiumObj?.getCesiumScene) {
        olCesiumObj.getCesiumScene().terrainProvider = terrainProvider
      }
    })
  }
}

function toggle3D() {
  is3D.value = !is3D.value
  olCesiumObj?.setEnabled(is3D.value)
}

onBeforeUnmount(() => {
  if (olCesiumObj) {
    olCesiumObj.setEnabled(false)
    olCesiumObj.destroy()
  }
  map?.setTarget(undefined)
})
</script>

<style scoped>
.full-screen {
  position: relative;
  width: 100%;
  height: 100vh;
}
.map-container {
  width: 100%;
  height: 100%;
}
.control-panel {
  position: absolute;
  top: 16px;
  left: 16px;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.toggle-btn {
  padding: 10px 16px;
  background: white;
  border: 1px solid #ccc;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.toggle-btn:hover {
  background: #f0f0f0;
}
.coord-info {
  background: rgba(255,255,255,0.9);
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 12px;
  font-family: monospace;
}
</style>
```

### 4.4 OpenLayers 矢量瓦片实战

```typescript
// 加载矢量瓦片（PBF格式）+ 客户端动态样式
import VectorTileLayer from 'ol/layer/VectorTile'
import VectorTileSource from 'ol/source/VectorTile'
import MVT from 'ol/format/MVT'
import { Style, Stroke, Fill, Text } from 'ol/style'

const vectorTileLayer = new VectorTileLayer({
  declutter: true,  // 防碰撞
  source: new VectorTileSource({
    format: new MVT(),
    url: 'https://tiles.example.com/tiles/{z}/{x}/{y}.pbf',
    maxZoom: 14
  }),
  style: (feature, resolution) => {
    const props = feature.getProperties()
    // 根据属性动态样式
    if (props.layer === 'roads') {
      return new Style({
        stroke: new Stroke({
          color: '#666',
          width: resolution < 2 ? 3 : 1  // 随缩放级别调整线宽
        })
      })
    }
    if (props.layer === 'buildings') {
      return new Style({
        fill: new Fill({ color: 'rgba(200, 200, 200, 0.8)' }),
        stroke: new Stroke({ color: '#999', width: 1 })
      })
    }
    return null
  }
})
```

### 4.5 OpenLayers WebGL 高性能点渲染

```typescript
// WebGL 渲染百万级点数据（比Canvas快10-100倍）
import WebGLPointsLayer from 'ol/layer/WebGLPoints'

const webglLayer = new WebGLPointsLayer({
  source: new VectorSource({
    url: 'https://server/million-points.geojson',
    format: new GeoJSON()
  }),
  style: {
    'circle-radius': ['interpolate', ['linear'], ['get', 'count'],
      0, 3,
      1000, 8,
      10000, 15
    ],
    'circle-fill-color': ['match', ['get', 'category'],
      'A', '#ff0000',
      'B', '#00ff00',
      '#888888'
    ],
    'circle-opacity': 0.7
  }
})
```

---

## 五、CesiumJS 独立项目 ⭐ V4.0

### 5.1 基础三维场景

```typescript
// 纯 Cesium 三维场景（不含 OpenLayers）
import * as Cesium from 'cesium'
import 'cesium/Build/Cesium/Widgets/widgets.css'

// 初始化Viewer
const viewer = new Cesium.Viewer('cesiumContainer', {
  animation: false,       // 关闭动画控件
  timeline: false,        // 关闭时间线
  baseLayerPicker: false, // 隐藏底图切换
  terrainProvider: await Cesium.createWorldTerrainAsync({
    requestWaterMask: true,
    requestVertexNormals: true
  })
})

// 飞向中国北京
viewer.camera.flyTo({
  destination: Cesium.Cartesian3.fromDegrees(116.4, 39.9, 5000),
  orientation: {
    heading: Cesium.Math.toRadians(0),
    pitch: Cesium.Math.toRadians(-45),
    roll: 0
  },
  duration: 3  // 3秒飞行动画
})

// 添加 3D Tiles 建筑模型
const tileset = await Cesium.Cesium3DTileset.fromUrl(
  'https://server/tileset.json'
)
viewer.scene.primitives.add(tileset)

// 添加 GeoJSON 矢量（贴地）
const geoJsonDataSource = await Cesium.GeoJsonDataSource.load(
  'https://server/admin_boundary.geojson',
  {
    stroke: Cesium.Color.fromCssColorString('#ff0000'),
    strokeWidth: 3,
    fill: Cesium.Color.fromCssColorString('#ff000044')
  }
)
viewer.dataSources.add(geoJsonDataSource)

// 点击要素查询
const handler = new Cesium.ScreenSpaceEventHandler(viewer.scene.canvas)
handler.setInputAction(async (click) => {
  const pickedFeature = viewer.scene.pick(click.position)
  if (Cesium.defined(pickedFeature)) {
    console.log('选中要素:', pickedFeature.id?.properties?.getValue())
  }
}, Cesium.ScreenSpaceEventType.LEFT_CLICK)
```

### 5.2 Cesium + 3D Tiles 属性查询

```typescript
// 3D Tiles 单体化查询
const tileset = viewer.scene.primitives._primitives[0]

// 方式1：通过属性表格查询
const featureTable = tileset.root.content.featureTable
const buildingId = featureTable.getProperty(0, 'building_id')

// 方式2：通过点击事件
viewer.screenSpaceEventHandler.setInputAction((click) => {
  const picked = viewer.scene.pick(click.position)
  if (picked?.primitive === tileset) {
    const properties = picked.getPropertyNames()
    properties.forEach(prop => {
      console.log(`${prop}: ${picked.getProperty(prop)}`)
    })
  }
}, Cesium.ScreenSpaceEventType.LEFT_CLICK)

// 方式3：高亮选中（样式修改）
tileset.style = new Cesium.Cesium3DTileStyle({
  color: {
    conditions: [
      ['${building_id} === "B001"', 'rgba(255, 0, 0, 1)'],
      ['true', 'rgba(255, 255, 255, 0.5)']
    ]
  }
})
```

---

## 六、矢量瓦片服务端 ⭐ V4.0

### 6.1 Martin（Rust矢量瓦片服务器）

```bash
# 从PostGIS直接提供矢量瓦片，性能极高
cargo install martin

# 启动（自动读取PostGIS所有表）
martin postgresql://user:pass@localhost/mydb

# 配置特定表
martin postgresql://user:pass@localhost/mydb \
  --table-buildings \
  --table-roads \
  --srid 4326

# 前端使用
# http://localhost:3000/buildings/{z}/{x}/{y}
```

### 6.2 Tippecanoe（矢量瓦片生成工具）

```bash
# GeoJSON → MBTiles
tippecanoe -o output.mbtiles \
  -Z 0 -z 14 \           # 缩放范围 0-14
  -l buildings \          # 图层名
  --drop-densest-as-needed \  # 高密度区域自动抽稀
  --coalesce-smallest-as-needed \
  --simplification=5 \    # 简化阈值
  input.geojson

# MBTiles → PBF目录
mb-util --image_format=pbf output.mbtiles tiles/
```

---

## 七、部署与性能优化

### 7.1 瓦片缓存策略

| 缓存方式 | 说明 | 适用 |
|---------|------|------|
| **GeoWebCache** | GeoServer内置瓦片缓存 | GeoServer部署 |
| **ArcGIS Server Cache** | 紧凑型/松散型瓦片 | ArcGIS生态 |
| **CDN 分发** | 瓦片推送到 CDN 边缘节点 | 高并发公网服务 |
| **MBTiles** | SQLite 单文件瓦片包 | 离线/移动端 |
| **矢量瓦片(PBF)** | 客户端渲染 | 样式多变场景 |

### 7.2 性能优化清单

```
1. 服务端优化
   ├ 瓦片缓存（WMTS > WMS 10~100倍）
   ├ 数据库索引（空间索引+属性索引）
   ├ 简化几何（Douglas-Peucker算法）
   ├ 分层显示（小比例尺用简化数据）
   └ 连接池配置（PostGIS max_connections=100）

2. 前端优化
   ├ 矢量瓦片代替 GeoJSON（体积 1/10）
   ├ WebGL 渲染 > Canvas 渲染（>1000要素时）
   ├ 聚合点（Supercluster 算法）
   ├ 懒加载（可视区域外不渲染）
   ├ requestAnimationFrame 节流
   └ Web Worker 后台数据处理

3. 网络优化
   ├ Gzip/Brotli 压缩
   ├ CDN 静态资源
   ├ HTTP/2 多路复用
   ├ Service Worker 离线缓存
   └ 预加载关键区域瓦片
```

### 7.3 Cesium 3D Tiles 性能优化

| 技术 | 说明 | 性能提升 |
|------|------|---------|
| **Maximum Screen Space Error** | 控制LOD切换阈值 | 降低GPU负载30-50% |
| **Skip Level of Detail** | 跳过中间LOD级别 | 加载速度提升2-3倍 |
| **Occlusion Culling** | 视锥体剔除 | 减少渲染50%+ |
| **3D Tiles Next** | 新一代规范，支持隐式切片 | 数据量减少30% |
| **Draco 压缩** | Google Draco几何压缩 | 减少数据量80% |
| **Batched/Instanced** | 批量渲染降低Draw Call | FPS提升2-5倍 |

---

> **神经连接**：OGC 标准 → `05_国家测绘标准体系.md`（标准引用） | 矢量瓦片 → `22_空间数据库.md`（PostGIS后端） | 三维 → `25_三维GIS与数字孪生.md`（3D Tiles/Cesium深度） | 性能优化 → `29_避坑库110+.md`（WebGIS常见坑）

> **推荐学习资源**：
> - Leaflet 官方教程：`leafletjs.com/reference.html`
> - OpenLayers 官方示例：`openlayers.org/en/latest/examples/`
> - CesiumJS 沙盒：`sandcastle.cesium.com`
> - ol-cesium 项目：`openlayers.org/ol-cesium/`
> - GeoServer 用户手册：`docs.geoserver.org`
> - OGC 标准规范：`ogc.org/standards/`
> - Martin 矢量瓦片：`github.com/maplibre/martin`

*V4.0 变更：新增 4.3~4.5 节（ol-cesium完整项目代码）+ 5.1~5.2节（Cesium独立项目）+ 6节（矢量瓦片服务端）+ 7.3节（Cesium性能优化）*

---

## 八、服务端运维实战 ⭐ V4.1 新增

### 8.1 GeoServer SLD/CSS 样式编写

GeoServer 支持 4 种样式格式：SLD (XML)、CSS、YSLD (YAML)、MBStyle (Mapbox JSON)。

**SLD 核心模板 — 面要素分类着色**：

```xml
<!-- 土地利用分类着色示例 -->
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld">
  <NamedLayer>
    <Name>landuse</Name>
    <UserStyle>
      <Title>土地利用分类</Title>
      <FeatureTypeStyle>
        <Rule>
          <Name>耕地</Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>landuse_type</ogc:PropertyName>
              <ogc:Literal>耕地</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill><CssParameter name="fill">#90EE90</CssParameter></Fill>
            <Stroke><CssParameter name="stroke">#006400</CssParameter>
                    <CssParameter name="stroke-width">0.5</CssParameter></Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>建设用地</Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>landuse_type</ogc:PropertyName>
              <ogc:Literal>建设用地</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill><CssParameter name="fill">#FFA07A</CssParameter></Fill>
          </PolygonSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>
```

**CSS 样式（推荐，比 SLD 简洁 50%）**：

```css
/* GeoServer CSS Extension — 土地利用样式 */
[landuse_type='耕地'] {
  fill: #90EE90;
  stroke: #006400;
  stroke-width: 0.5;
}
[landuse_type='建设用地'] {
  fill: #FFA07A;
}
[landuse_type='林地'] {
  fill: #228B22;
  label: [name];
  label-anchor: 0.5 0.5;
  font-fill: white;
  font-size: 12;
}
/* 比例尺分级样式 */
[@scale < 50000] {
  stroke-width: 2;
}
[@scale >= 50000] {
  stroke-width: 0.5;
}
```

**样式管理命令**：

```bash
# GeoServer REST API 上传样式
curl -u admin:geoserver -X POST \
  -H "Content-type: application/vnd.ogc.sld+xml" \
  -d @landuse.sld \
  "http://localhost:8080/geoserver/rest/styles"

# 将样式关联到图层
curl -u admin:geoserver -X PUT \
  -H "Content-type: text/xml" \
  -d "<layer><defaultStyle><name>landuse</name></defaultStyle></layer>" \
  "http://localhost:8080/geoserver/rest/layers/myworkspace:landuse_layer"
```

### 8.2 Nginx 跨域与反向代理配置

**完整 Nginx 配置模板**：

```nginx
server {
    listen 80;
    server_name gis.example.com;

    # === CORS 全局配置 ===
    add_header Access-Control-Allow-Origin * always;
    add_header Access-Control-Allow-Methods "GET, POST, OPTIONS, PUT, DELETE" always;
    add_header Access-Control-Allow-Headers "Origin, Content-Type, Accept, Authorization" always;
    if ($request_method = OPTIONS) {
        return 204;
    }

    # === GeoServer 反向代理 ===
    location /geoserver/ {
        proxy_pass http://127.0.0.1:8080/geoserver/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 瓦片缓存（静态瓦片可加 Cache-Control）
        location ~* /geoserver/gwc/ {
            proxy_cache tile_cache;
            proxy_cache_valid 200 7d;
            add_header X-Cache-Status $upstream_cache_status;
        }
    }

    # === ArcGIS Server 反向代理 ===
    location /arcgis/ {
        proxy_pass http://127.0.0.1:6080/arcgis/;
        proxy_set_header Host $host;
        proxy_buffering off;           # ArcGIS Server 流式响应
        proxy_read_timeout 300s;       # 长时间导出操作
    }
}
```

**各 OGC 服务跨域注意事项**：

| 服务 | 需要额外 Header | 特殊说明 |
|------|----------------|---------|
| **WMS** | `Access-Control-Allow-Origin` | 通常 GET 请求，无特殊限制 |
| **WFS** | 同上 + 允许 `Content-Type: application/json` | POST 请求较多，需允许 POST |
| **WMTS** | 同上 | 瓦片缓存时要设置 Cache-Control |
| **WPS** | + `Access-Control-Allow-Methods: POST` | 计算密集型，需长超时 |

### 8.3 GeoServer 缓存与性能

```bash
# === TileCache (GWC) 配置 ===

# 预生成瓦片 (Seed)
curl -u admin:geoserver -X POST \
  "http://localhost:8080/geoserver/gwc/rest/seed/myworkspace:mylayer.json" \
  -H "Content-type: application/json" -d '{
    "seedRequest": {
      "name": "myworkspace:mylayer",
      "srs": {"number": 3857},
      "zoomStart": 0,
      "zoomStop": 16,
      "format": "image/png",
      "type": "seed",
      "threadCount": 4
    }
  }'

# 清空缓存（图层更新后必须）
curl -u admin:geoserver -X POST \
  "http://localhost:8080/geoserver/gwc/rest/seed/myworkspace:mylayer.json" \
  -H "Content-type: application/json" -d '{
    "seedRequest": {
      "name": "myworkspace:mylayer",
      "type": "truncate"
    }
  }'
```

**GeoServer 性能调优参数**（`web.xml`）：

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| `USE_JAI_IMAGEREAD` | true | 启用 JAI 加速影像读取 |
| `TILE_CACHE_SIZE` | 1000 | 瓦片内存缓存数 |
| `WMS_MAX_RENDERING_TIME` | 60 | WMS 最大渲染时间(秒) |
| `WMS_MAX_RENDERING_ERRORS` | 3 | 最大渲染错误重试 |
| `CoverageAccessMaxPoolSize` | 10 | 栅格数据连接池 |

### 8.4 GeoServer 权限与安全

```bash
# 创建角色
curl -u admin:geoserver -X POST \
  -H "Content-type: text/xml" \
  -d "<roleService><name>viewer</name></roleService>" \
  "http://localhost:8080/geoserver/rest/security/roles/role/viewer"

# 创建用户
curl -u admin:geoserver -X POST \
  -H "Content-type: text/xml" \
  -d "<user><userName>gis_viewer</userName><password>password123</password><enabled>true</enabled></user>" \
  "http://localhost:8080/geoserver/rest/security/usergroup/users"

# 设置数据访问规则（工作空间级别）
# 编辑 geoserver/data/security/rest.properties:
# myworkspace.*.r=viewer,admin        # 只读权限
# myworkspace.*.w=admin               # 写入权限
```

**权限层级表**：

| 层级 | 权限类型 | 控制粒度 |
|------|---------|---------|
| **工作空间** | 读(r)/写(w)/管理(a) | 整个工作空间所有图层 |
| **图层** | 读(r)/写(w) | 单个图层的访问 |
| **服务** | WMS/WFS/WPS 开关 | 按服务类型控制 |
| **数据访问** | 属性过滤 + 空间过滤 | 行级别数据安全 |

### 8.5 ArcGIS Server 运维速查

```bash
# 查看服务状态
curl "http://server:6080/arcgis/admin/services?f=json" \
  -H "Referer: http://server:6080/arcgis/admin"

# 重启服务
curl -X POST "http://server:6080/arcgis/admin/services/MyFolder/MyService.MapServer/restart" \
  -H "Referer: http://server:6080/arcgis/admin" -d "f=json"

# 更新缓存切片 (Manage Map Cache Tiles)
curl -X POST "http://server:6080/arcgis/admin/services/MyService.MapServer/jobs" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Referer: http://server:6080/arcgis/admin" \
  -d "f=json&jobType=Manage+Map+Cache+Tiles&updateMode=Recreate+Empty+Tiles&
      minLevel=0&maxLevel=16&numOfCachingServiceInstances=3"
```

---

> **神经连接**：服务运维 → `22_空间数据库.md`（PostGIS配置） | 三维服务 → `25_三维GIS与数字孪生.md`（3D Tiles服务） | 性能优化 → `29_避坑库110+.md`（WebGIS避坑）

> **V4.1 新增**：§八 服务端运维实战（GeoServer SLD/CSS/Nginx跨域/缓存刷新/权限/ArcGIS Server运维）


<!-- wm:坤图_GIS:V1.0 -->
