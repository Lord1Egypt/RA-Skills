# 案例范本 A：「记一下」物品定位备忘小程序 — 产品技术规格（MVP v1.0）

> 定位：极简物品定位备忘工具。放下东西 → 点一下记位置（免注册）→ 下次打开引导回原处。
> 演进：从"找车回原位"泛化为"记录任意物品存放位置"的通用定位备忘。

## 一、功能清单

**核心功能（v1 必做）**
1. 记录位置：获取当前 GPS 坐标 + 文字备注 + 拍照 + 选房间（均选填，仅坐标必填）
2. 找回列表：读取本地记录，按"距当前位置"由近到远排序
3. 详情引导：显示「距你 X 米」+ 实时方向箭头（指南针）
4. 编辑 / 删除单条记录
5. 纯本地存储，无登录、无后端

**明确不做（守标准一）**
- 不做分类文件夹、不做社交分享、不做云同步、不做提醒推送
- v1 不含地图导航跳转（B 方案留作后续增强）

## 二、信息架构 / 页面结构

```
app
├── pages/
│   ├── index/      首页（双入口）
│   ├── record/     记录页
│   ├── list/       找回列表页
│   └── detail/     详情引导页
├── app.js / app.json / app.wxss
└── sitemap.json / project.config.json
```

## 三、首页设计（index）

**风格**：极简主义、大留白、零学习成本、工具感。

**色调方案**
| 角色 | 色值 | 说明 |
|---|---|---|
| 主色 Primary | `#1FB6A6` 青绿 | 定位/方向/冷静可靠 |
| 强调色 Accent（CTA） | `#FF7A45` 暖橙 | 「记一下位置」主按钮 |
| 背景 BG | `#F6F7F9` 浅灰白 | 卡片浮起感 |
| 卡片 Card | `#FFFFFF` | — |
| 文字主/次 | `#1A1A1A` / `#8A8F99` | 层级清晰 |

**视觉规范**：圆角按钮 24rpx、卡片 16rpx；系统字体；按钮高度 ≥ 96rpx。

**首页布局**
```
┌─────────────────────────┐
│   记一下            (小logo)│
│   ┌──────────────────┐   │
│   │  📍 记一下位置    │   │  ← 橙底大按钮
│   └──────────────────┘   │
│   ┌──────────────────┐   │
│   │  🔍 找东西        │   │  ← 白底描边按钮
│   └──────────────────┘   │
│   放下东西，点一下就记住   │
└─────────────────────────┘
```

## 四、操作流程

**记录流程（record）**
1. 点「记一下位置」→ `wx.getLocation({type:'gcj02'})` 拉取坐标（首次触发授权）
2. 页面显示"已定位 ✓"
3. 选填：备注、拍照（`wx.chooseMedia`）、房间标签（客厅/卧室/厨房/书房/车库/办公室 + 自定义）
4. 点「保存」→ 写入本地 → `wx.vibrateShort()` → 返回首页

**找回流程（list → detail）**
1. 点「找东西」→ 读本地列表 + 再取当前坐标
2. 每条算距离，按近→远排序（备注/房间 + "距你 X 米" + 时间）
3. 点条目 → detail：`wx.startCompass()` + `wx.onCompassChange` 实时渲染箭头
4. 支持「删除」「编辑备注」

## 五、数据存储（纯本地）

**Storage Key**：`records`
**类型**：`Array<Object>`，`wx.setStorageSync('records', arr)`

```js
{
  id:        String,   // Date.now()+随机串
  lat:       Number,   // 记录时纬度 (gcj02)
  lng:       Number,   // 记录时经度 (gcj02)
  remark:    String,   // 文字备注，默认 ''
  room:      String,   // 房间标签，默认 ''
  photo:     String,   // 照片本地临时路径，默认 ''
  createdAt: Number    // 时间戳
}
```

```js
function addRecord(rec){
  const list = wx.getStorageSync('records') || [];
  list.push(rec);
  wx.setStorageSync('records', list);
}
function removeRecord(id){
  let list = wx.getStorageSync('records') || [];
  list = list.filter(r => r.id !== id);
  wx.setStorageSync('records', list);
}
```

## 六、关键技术点

| 能力 | API | 要点 |
|---|---|---|
| 获取坐标 | `wx.getLocation({type:'gcj02'})` | 记录与当前必须同一坐标系 |
| 指南针 | `wx.startCompass()` + `wx.onCompassChange` | 手机朝向角（相对正北 0–360°） |
| 距离计算 | Haversine 公式 | 短距离可用平面近似 |
| 方向箭头 | 目标方位角 `θ=atan2(Δlng·cos(lat), Δlat)`，相对角=θ−手机朝向 | 箭头指向物品 |
| 拍照 | `wx.chooseMedia({mediaType:['image']})` | 临时路径 |
| 反馈 | `wx.vibrateShort()` | 保存成功轻震 |

```js
function bearing(lat1, lng1, lat2, lng2){
  const rad = Math.PI/180;
  const dLng = (lng2-lng1)*rad;
  const y = Math.sin(dLng)*Math.cos(lat2*rad);
  const x = Math.cos(lat1*rad)*Math.sin(lat2*rad)
          - Math.sin(lat1*rad)*Math.cos(lat2*rad)*Math.cos(dLng);
  return (Math.atan2(y,x)/rad + 360) % 360;
}
// 箭头旋转角 = bearing(当前,目标) - 手机朝向(compass)
```

## 七、技术栈与合规前置

- **框架**：微信原生小程序（WXML/WXSS/JS），无构建依赖
- **后端**：无（v1 纯本地）
- **权限**（`app.json`）：`"permission": { "scope.userLocation": { "desc": "用于记录物品存放位置" } }`
- **隐私**：需在《微信小程序隐私保护指引》声明位置信息用途

## 八、开发任务分解（SOP）

1. 注册小程序 → 配置 `userLocation` 权限 + 隐私指引
2. 搭建 4 页面骨架
3. 实现 record 页：定位授权、表单、拍照、房间标签
4. 本地存储读写工具
5. 实现 list 页：距离计算 + 排序渲染
6. 实现 detail 页：指南针 + 箭头 + 删除/编辑
7. index 双入口 + 视觉规范落地
8. 真机测试：室内精度、指南针漂移、清缓存表现
9. 提交审核（名称含「记位置/找东西」利于搜索）
