<!-- wm:坤图_GIS:V5.0 -->

# Agent 1: 数据探查Agent (Data Explorer)

> 全局唯一知识ID: GIS-AGENT-001
> 隶属: 上层多Agent编排引擎
> 触发条件: 用户提交原始GIS数据 → 自动探查

## 职责

1. 识别数据格式（SHP/GDB/DWG/KML/GeoJSON/LAS/TIF等）
2. 读取元数据：坐标系、字段列表、记录数、几何类型、空间范围
3. 检测异常：空几何、自相交、坐标系缺失、编码问题
4. 生成标准化《数据探查报告》

## 输入

| 参数 | 说明 | 必填 |
|------|------|------|
| data_path | 数据文件/目录路径 | 是 |
| expected_crs | 预期坐标系（可选） | 否 |

## 输出

- 标准化数据探查报告（Markdown表格）
- TOPO_ISSUE标记的异常数据SHP（如有）

## 关联原子Skill

- ATS-002 DLG数据探查

## 关联知识库

- references/03 数据模型与格式
- references/02 坐标系统与投影
- references/29 避坑库
