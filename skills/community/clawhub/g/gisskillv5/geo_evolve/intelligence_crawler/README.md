<!-- wm:坤图_GIS:V5.0 -->

# GeoEvolve 子模块: 情报抓取层

> 全局唯一知识ID: GIS-EVO-002
> 隶属: 顶层GeoEvolve自进化闭环

## 功能

定时监控外部情报源，检测知识库变更需要：
- 国标更新 → 自然资源部/国家标准委发布
- 软件新版本 → ArcGIS/QGIS/SuperMap/CASS/FME/LiDAR360
- OGC新标准 → OGC官方发布
- GitHub开源仓库 → GIS相关Star/Trending项目
- 行业技术博客 → 测绘GIS领域前沿动态

## 监控源清单

| 源 | URL | 频次 |
|----|-----|------|
| 国家标准委 | std.samr.gov.cn | 月度 |
| Esri Blog | esri.com/arcgis-blog | 季度 |
| QGIS官网 | qgis.org | 季度 |
| OGC官网 | ogc.org/standards | 月度 |
| GitHub GIS | github.com/topics/gis | 月度 |

## 输出

- 情报摘要报告
- 推送至 knowledge_fixer 子模块
