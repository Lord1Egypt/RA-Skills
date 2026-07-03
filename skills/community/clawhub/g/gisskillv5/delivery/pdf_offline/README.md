<!-- wm:坤图_GIS:V5.0 -->

# GIS_SKILL V5.0 PDF离线检索包 (pdf_offline)

> 版本: V5.0 | 格式: 自包含HTML → 可打印PDF | 离线可用

## 适用场景

在没有WorkBuddy或联网环境时，通过浏览器查阅完整GIS知识库。支持打印为PDF随身携带。

## 内容覆盖

| 类别 | 文件数 | 内容 |
|------|--------|------|
| 基础底座 | 4个 | 坐标系统、数据格式、理论前沿、坐标系码表 |
| 标准规范 | 2个 | 国家标准体系总览、标准扩展 |
| 软件工具 | 3个 | ArcGIS Pro 3.6、QGIS 3.40、CASS 11.0 |
| 实战避坑 | 2个 | 避坑索引、案例集 |
| 现代GIS | 3个 | GeoAI工程化、避坑800+框架、云原生国产合规 |
| 原子Skill | 10个 | 全部10个原子Skill概要 |

## 使用方法

### 方法一：浏览器直接浏览
```
用浏览器打开 GIS_SKILL_V5_Offline.html
Ctrl+K 聚焦搜索 → 输入关键词检索
```

### 方法二：生成/更新离线包
```bash
cd delivery/pdf_offline
python generate.py
# 输出: GIS_SKILL_V5_Offline.html
```

### 方法三：打印PDF
```
浏览器打开 GIS_SKILL_V5_Offline.html
Ctrl+P → 另存为PDF → 选择A4纸张
建议设置：页边距"最小"、勾选"背景图形"
```

## 特性

- 自包含：单HTML文件，无外部依赖
- 全文搜索：Ctrl+K即时搜索
- 可打印：支持打印为PDF，适配A4纸张
- 目录导航：自动生成知识单元目录
- 表格式渲染：Markdown表格完整转换

## 更新记录

- 2026-06-23: V5.0首次发布
