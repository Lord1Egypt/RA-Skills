# 示例 Prompt 与输出

## 示例 1：简单流程图

**Prompt：** 「画一个用户登录流程图」

**分析：** 流程图，5个节点，单列布局

**完整 .excalidraw JSON 输出：**

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "openclaw-skill",
  "elements": [
    {
      "id": "node0001",
      "type": "ellipse",
      "x": 230, "y": 100,
      "width": 140, "height": 60,
      "angle": 0,
      "strokeColor": "#1e1e1e",
      "backgroundColor": "#b2f2bb",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 100,
      "groupIds": [],
      "frameId": null,
      "roundness": {"type": 2},
      "seed": 11111,
      "version": 1,
      "versionNonce": 11111,
      "isDeleted": false,
      "boundElements": [{"type": "arrow", "id": "arr0001"}],
      "updated": 1700000000000,
      "link": null,
      "locked": false,
      "text": "开始",
      "fontSize": 16,
      "fontFamily": 5,
      "textAlign": "center",
      "verticalAlign": "middle",
      "containerId": null,
      "originalText": "开始"
    },
    {
      "id": "node0002",
      "type": "rectangle",
      "x": 220, "y": 220,
      "width": 160, "height": 60,
      "angle": 0,
      "strokeColor": "#1e1e1e",
      "backgroundColor": "#a5d8ff",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 100,
      "groupIds": [],
      "frameId": null,
      "roundness": {"type": 3},
      "seed": 22222,
      "version": 1,
      "versionNonce": 22222,
      "isDeleted": false,
      "boundElements": [
        {"type": "arrow", "id": "arr0001"},
        {"type": "arrow", "id": "arr0002"}
      ],
      "updated": 1700000000000,
      "link": null,
      "locked": false,
      "text": "输入账号密码",
      "fontSize": 16,
      "fontFamily": 5,
      "textAlign": "center",
      "verticalAlign": "middle",
      "containerId": null,
      "originalText": "输入账号密码"
    },
    {
      "id": "node0003",
      "type": "diamond",
      "x": 220, "y": 340,
      "width": 160, "height": 80,
      "angle": 0,
      "strokeColor": "#1e1e1e",
      "backgroundColor": "#ffd43b",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 100,
      "groupIds": [],
      "frameId": null,
      "roundness": {"type": 2},
      "seed": 33333,
      "version": 1,
      "versionNonce": 33333,
      "isDeleted": false,
      "boundElements": [
        {"type": "arrow", "id": "arr0002"},
        {"type": "arrow", "id": "arr0003"},
        {"type": "arrow", "id": "arr0004"}
      ],
      "updated": 1700000000000,
      "link": null,
      "locked": false,
      "text": "验证通过?",
      "fontSize": 16,
      "fontFamily": 5,
      "textAlign": "center",
      "verticalAlign": "middle",
      "containerId": null,
      "originalText": "验证通过?"
    },
    {
      "id": "node0004",
      "type": "rectangle",
      "x": 220, "y": 480,
      "width": 160, "height": 60,
      "angle": 0,
      "strokeColor": "#1e1e1e",
      "backgroundColor": "#a5d8ff",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 100,
      "groupIds": [],
      "frameId": null,
      "roundness": {"type": 3},
      "seed": 44444,
      "version": 1,
      "versionNonce": 44444,
      "isDeleted": false,
      "boundElements": [
        {"type": "arrow", "id": "arr0003"},
        {"type": "arrow", "id": "arr0005"}
      ],
      "updated": 1700000000000,
      "link": null,
      "locked": false,
      "text": "进入主页",
      "fontSize": 16,
      "fontFamily": 5,
      "textAlign": "center",
      "verticalAlign": "middle",
      "containerId": null,
      "originalText": "进入主页"
    },
    {
      "id": "node0005",
      "type": "rectangle",
      "x": 450, "y": 350,
      "width": 160, "height": 60,
      "angle": 0,
      "strokeColor": "#1e1e1e",
      "backgroundColor": "#ffc9c9",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 100,
      "groupIds": [],
      "frameId": null,
      "roundness": {"type": 3},
      "seed": 55555,
      "version": 1,
      "versionNonce": 55555,
      "isDeleted": false,
      "boundElements": [{"type": "arrow", "id": "arr0004"}],
      "updated": 1700000000000,
      "link": null,
      "locked": false,
      "text": "显示错误提示",
      "fontSize": 16,
      "fontFamily": 5,
      "textAlign": "center",
      "verticalAlign": "middle",
      "containerId": null,
      "originalText": "显示错误提示"
    },
    {
      "id": "node0006",
      "type": "ellipse",
      "x": 230, "y": 600,
      "width": 140, "height": 60,
      "angle": 0,
      "strokeColor": "#1e1e1e",
      "backgroundColor": "#b2f2bb",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 100,
      "groupIds": [],
      "frameId": null,
      "roundness": {"type": 2},
      "seed": 66666,
      "version": 1,
      "versionNonce": 66666,
      "isDeleted": false,
      "boundElements": [{"type": "arrow", "id": "arr0005"}],
      "updated": 1700000000000,
      "link": null,
      "locked": false,
      "text": "结束",
      "fontSize": 16,
      "fontFamily": 5,
      "textAlign": "center",
      "verticalAlign": "middle",
      "containerId": null,
      "originalText": "结束"
    },
    {
      "id": "arr0001", "type": "arrow",
      "x": 300, "y": 160, "width": 0, "height": 60,
      "points": [[0,0],[0,60]],
      "strokeColor": "#1e1e1e", "backgroundColor": "transparent",
      "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
      "roughness": 1, "opacity": 100, "groupIds": [], "frameId": null,
      "roundness": {"type": 2}, "seed": 77777, "version": 1,
      "versionNonce": 77777, "isDeleted": false,
      "startArrowhead": null, "endArrowhead": "arrow",
      "startBinding": {"elementId": "node0001", "focus": 0, "gap": 8},
      "endBinding": {"elementId": "node0002", "focus": 0, "gap": 8},
      "updated": 1700000000000, "link": null, "locked": false,
      "boundElements": []
    },
    {
      "id": "arr0002", "type": "arrow",
      "x": 300, "y": 280, "width": 0, "height": 60,
      "points": [[0,0],[0,60]],
      "strokeColor": "#1e1e1e", "backgroundColor": "transparent",
      "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
      "roughness": 1, "opacity": 100, "groupIds": [], "frameId": null,
      "roundness": {"type": 2}, "seed": 88888, "version": 1,
      "versionNonce": 88888, "isDeleted": false,
      "startArrowhead": null, "endArrowhead": "arrow",
      "startBinding": {"elementId": "node0002", "focus": 0, "gap": 8},
      "endBinding": {"elementId": "node0003", "focus": 0, "gap": 8},
      "updated": 1700000000000, "link": null, "locked": false,
      "boundElements": []
    },
    {
      "id": "arr0003", "type": "arrow",
      "x": 300, "y": 420, "width": 0, "height": 60,
      "points": [[0,0],[0,60]],
      "strokeColor": "#1e1e1e", "backgroundColor": "transparent",
      "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
      "roughness": 1, "opacity": 100, "groupIds": [], "frameId": null,
      "roundness": {"type": 2}, "seed": 99991, "version": 1,
      "versionNonce": 99991, "isDeleted": false,
      "startArrowhead": null, "endArrowhead": "arrow",
      "startBinding": {"elementId": "node0003", "focus": 0, "gap": 8},
      "endBinding": {"elementId": "node0004", "focus": 0, "gap": 8},
      "updated": 1700000000000, "link": null, "locked": false,
      "boundElements": []
    },
    {
      "id": "arr0004", "type": "arrow",
      "x": 380, "y": 380, "width": 70, "height": 0,
      "points": [[0,0],[70,0]],
      "strokeColor": "#1e1e1e", "backgroundColor": "transparent",
      "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
      "roughness": 1, "opacity": 100, "groupIds": [], "frameId": null,
      "roundness": {"type": 2}, "seed": 99992, "version": 1,
      "versionNonce": 99992, "isDeleted": false,
      "startArrowhead": null, "endArrowhead": "arrow",
      "startBinding": {"elementId": "node0003", "focus": 0, "gap": 8},
      "endBinding": {"elementId": "node0005", "focus": 0, "gap": 8},
      "updated": 1700000000000, "link": null, "locked": false,
      "boundElements": []
    },
    {
      "id": "arr0005", "type": "arrow",
      "x": 300, "y": 540, "width": 0, "height": 60,
      "points": [[0,0],[0,60]],
      "strokeColor": "#1e1e1e", "backgroundColor": "transparent",
      "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
      "roughness": 1, "opacity": 100, "groupIds": [], "frameId": null,
      "roundness": {"type": 2}, "seed": 99993, "version": 1,
      "versionNonce": 99993, "isDeleted": false,
      "startArrowhead": null, "endArrowhead": "arrow",
      "startBinding": {"elementId": "node0004", "focus": 0, "gap": 8},
      "endBinding": {"elementId": "node0006", "focus": 0, "gap": 8},
      "updated": 1700000000000, "link": null, "locked": false,
      "boundElements": []
    }
  ],
  "appState": {
    "viewBackgroundColor": "#ffffff",
    "gridSize": null
  },
  "files": {}
}
```

**保存路径：** `/home/mcdowell/open-claw-output/design/user-login-flow.excalidraw`

---

## 示例 2：思维导图

**Prompt：** 「画一个关于"产品开发"的思维导图，包括需求分析、设计、开发、测试四个分支」

**分析：** 思维导图，中心+4分支，辐射布局

**关键节点坐标：**
- 中心主题（椭圆）：x=400, y=280, w=200, h=80，backgroundColor: `#ffd43b`
- 上方「需求分析」：x=400, y=120, w=160, h=60，backgroundColor: `#a5d8ff`
- 右方「设计」：x=660, y=280, w=140, h=60，backgroundColor: `#b2f2bb`
- 下方「测试」：x=400, y=440, w=140, h=60，backgroundColor: `#b2f2bb`
- 左方「开发」：x=140, y=280, w=140, h=60，backgroundColor: `#a5d8ff`

（完整 JSON 结构同示例1，省略重复字段，按规范补全）

---

## 示例 3：架构图

**Prompt：** 「画一个三层架构图：前端(React)、后端API(Node.js)、数据库(PostgreSQL)」

**分析：** 架构图，3层，纵向排列

**节点规划：**
- React 前端：x=200, y=100, w=200, h=70，backgroundColor: `#a5d8ff`
- Node.js API：x=200, y=250, w=200, h=70，backgroundColor: `#b2f2bb`
- PostgreSQL：x=200, y=400, w=200, h=70，backgroundColor: `#ffc9c9`
- 箭头：前端→API（y=170→250），API→数据库（y=320→400）

---

## 常见 Prompt 模式

| Prompt 关键词 | 映射图表类型 | 备注 |
|-------------|------------|------|
| 流程/步骤/环节 | 流程图 | 检查是否有判断条件 |
| 架构/系统/层次/组件 | 架构图 | 关注层级关系 |
| 思维导图/脑图/发散 | 思维导图 | 识别中心主题和分支 |
| 关系/依赖/连接 | 关系图 | 确定有向/无向 |
| 数据库/表/字段/ER | ER 图 | 识别主键外键 |
| 时序/消息/交互/调用 | 时序图 | 识别参与者 |
| 泳道/责任/角色分工 | 泳道图 | 识别角色数量 |
| 类/继承/接口/方法 | 类图 | 识别关系类型 |
| 数据流/数据处理/变换 | 数据流图 | 识别外部实体 |
