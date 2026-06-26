---
name: machine-commander-query
description: 使用机械指挥官MCP服务查询工程机械和船舶的实时数据、状态和位置信息。用于回答关于机械设备（挖掘机、装载机、自卸车、混凝土搅拌车等）、船舶（运输船、拖轮等）在施工项目中的状态、位置、工况等问题。当用户询问设备数量、位置分布、施工状态、油耗、报警等具体数据时必须使用此技能。
---

# 机械指挥官查询技能

## 快速开始

使用 `mcporter call MachineCommander` 调用 MCP 服务：

### 查询设备数据

```bash
mcporter call MachineCommander get_construction_machines_data 'question=你的问题'
```

### 发送指令

```bash
mcporter call MachineCommander manage_construction_machines 'order=你的指令'
```

## 可查询的信息

- **设备列表**: 所有在线设备及其基本信息
- **设备位置**: 设备的实时GPS位置
- **设备状态**: 开工/停工、运行时长、油量等
- **报警信息**: 越界、偷油、故障等报警
- **项目信息**: 所属项目、租户等
- **历史轨迹**: 设备移动轨迹

## 示例问题

- "列出所有自卸车"
- "查询江苏省的装载机"
- "查看 ZE1.1C 路测项目的设备"
- "列出所有报警设备"
- "查看今天有活动的设备"

## 响应格式

MCP 服务返回 JSON 格式数据，包含：
- `result`: 查询结果（表格或文本）
- 设备字段：机械名称、机械类型、所在省份、详细地址等

## 注意事项

1. 所有查询通过 `get_construction_machines_data` 工具
2. 问题用自然语言描述即可，服务会自动解析
3. 返回数据量较大时只看前几条关键信息
4. 如果查询无结果，尝试调整问题表述
