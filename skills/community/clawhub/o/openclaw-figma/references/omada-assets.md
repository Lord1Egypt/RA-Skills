# Omada Figma 设计资产全景

> 最后更新：2026-03-30
> 数据来源：Figma REST API 自动扫描

---

## 1. 组件库

### 🌟 商用WEB组件库
- **file_key**: `gzLJeRunJYuB02zQKTOkva`
- **URL**: https://www.figma.com/design/gzLJeRunJYuB02zQKTOkva
- **最后更新**: 2026-03-30
- **Published Components**: 1,743
- **Component Sets**: 132
- **Pages**: 86
- **Figma 账号角色**: viewer

#### 组件分类（按 containing_frame 统计 Top 20）

| Frame | 数量 | 说明 |
|-------|------|------|
| icon 图标 | 222 | 全局图标 |
| Sidebar icon导航栏图标 | 111 | 侧边栏导航图标 |
| Input 输入框 | 106 | 各类输入组件 |
| 图标dark | 94 | Dark 模式图标 |
| Table icon 表格图标 | 90 | 表格内图标 |
| 插图 | 85 | 业务插图 |
| 组件 | 64 | 通用基础组件 |
| Button 按钮 | 55 | 按钮变体 |
| Table 表格 | 54 | 表格组件 |
| Client 终端用户 | 51 | 终端设备图标 |
| Select 选择器 | 43 | 选择器变体 |
| DatePicker 日期选择框 | 40 | 日期选择 |
| Product 设备 | 36 | 产品设备图 |
| topo设备 | 33 | 拓扑图设备 |
| Tag 标签 | 32 | 标签变体 |
| InputNumber 数字输入框 | 30 | 数字输入 |
| 图表组成 | 30 | 图表元素 |
| IP地址 | 28 | IP 输入组件 |
| Ip掩码/端口 输入框 | 27 | IP/端口输入 |
| 交互自定义 | 25 | 交互组件 |

*另有 64 个分组（共 84 个 frame）*

#### 页面结构（Design System 分层）

**通用 Basic**：Color、Text、Button、Divider、Shadow、Layout、模式库
**导航 Navigation**：Top Bar、Sidebar、Tabs、Steps、Dropdown、Pagination
**数据输入 Input**：Form、Input、数字输入框、密码输入框、MAC输入框、IP掩码/端口输入框、Switch、Slider、Checkbox、Cascader、Radio、Select、TreeSelect、TimePicker、DatePicker、ColorPicker、Transfer、Search、Upload、Schedule
**数据展示 Display**：Table、描述列表、Tag、Collapse、Calendar、Popover、新功能引导、Tooltip、Avatar、Badge
**通知提示 Notification**：Alert、Toast Message、Drawer、Dialog、Notification、Progress、Loading
**其他 Other**：设备端口、Chart、Mask、Rate、Empty Space
**安防类组件+模式库**：安防业务专属组件

---

### 🌟 商用APP组件库
- **file_key**: `beYqvBsrUqRoq6GNfvOAuN`
- **URL**: https://www.figma.com/design/beYqvBsrUqRoq6GNfvOAuN
- **最后更新**: 2026-03-27
- **Published Components**: 848
- **Component Sets**: 77
- **Pages**: 49

#### 组件分类（Top 20）

| Frame | 数量 |
|-------|------|
| 图标 | 218 |
| Page Controls | 140 |
| General | 132 |
| List 列表 | 96 |
| 插图 | 31 |
| Buttons 按钮 | 30 |
| Device List | 28 |
| Inputs 输入框 | 27 |
| Toast | 16 |
| 标签色 | 15 |
| Text 文本 | 12 |
| Navigation Bars 标题栏 | 12 |
| Switch 开关 | 10 |
| Bottom Popup 底部弹窗 | 10 |

#### 页面结构

**基础组件**：Color、Typefaces、Navigation Bar、List、表单、模态面板、Inputs、Buttons、Tag、Toast、Bottom Popup、Segments、Menu、Search Bars、Tab Bars、Switch、Slider、Time Pickers、Date Pickers、Alert、Action Sheets、Page Controls、Prompt、Text、SubHeader、Loading
**样式库**：设备列表、图表、端口
**无障碍适配**：规范概要、标注、入口/功能

---

## 2. 项目设计文件

### Omada项目-web 2（需求设计稿集合）
- **file_key**: `fA9Oq6TPbayJsQUSYjyV4s`
- **URL**: https://www.figma.com/design/fA9Oq6TPbayJsQUSYjyV4s
- **Pages**: 54（按 JIRA ticket 组织，✅ 标记已完成）
- **组织方式**：按功能模块分组（Network Config / Device Config / Hotspot / General 等）

### V6.2-Omada Controller
- **file_key**: `DtbxwhppKkdqJncPhlH74c`
- **URL**: https://www.figma.com/design/DtbxwhppKkdqJncPhlH74c
- **Pages**: 8
- **核心功能**：
  - SMBNET-1855 千兆/2.5G混堆叠
  - SMBNET-1295 WAN 抖动/丢包上报
  - SMBNET-654 Dashboard Speed Test
  - SMBNET-55 AI RRM (WLAN Optimization)
  - SMBNET-2076 ISP Load Dashboard
  - Add Device 达阈值

### AIO 1.0-Gateway相关
- **file_key**: `rZaHc0WcrPLWFOlM3OqppI`
- **URL**: https://www.figma.com/design/rZaHc0WcrPLWFOlM3OqppI
- **Pages**: 19
- **核心功能**：DPI 优化、Lightlink VPN (Server/Client)、Content Filtering、QoS、DDNS、Loadbalance、Auto Send Data to Mail

### Design Center-V1.1
- **file_key**: `yjjan3lcHDRsYpdeiDQ6s0`
- **URL**: https://www.figma.com/design/yjjan3lcHDRsYpdeiDQ6s0
- **Pages**: 44
- **核心功能**：
  - V1.0：Project Workspace、Wizard、设备清单、导出、Floor Plan、墙体绘制、设备布放、设备仿真
  - V1.1：无线仿真、Topology 呈现、弱电井/桥架/布线、PDF 导出、联动 Omada Store
  - V1.2：AI 售前工具 & AI 运维

### V5.2-omada App
- **file_key**: `iu6lq4cRZUTwZjPx0QSeaX`
- **URL**: https://www.figma.com/design/iu6lq4cRZUTwZjPx0QSeaX
- **Pages**: 18
- **核心功能**：Time Range Setting、DDNS 适配、2FA 流程优化、VLAN 配置、设备收养、SSID 优化、拓扑适配、蓝牙 Console、Portal Voucher

---

## 3. 发现说明

### API 限制
- Figma REST API 无法通过 Personal Access Token 列出 workspace 所有文件（需 team_id，非 Enterprise 不暴露）
- 新文件需手动提供链接后，由 `figma_api.py` 扫描注册
- 当前用户角色为 `viewer`，可读取所有设计数据但无法写入（MCP write 需要 editor 权限）

### 组件库特征
- WEB 组件库高度完整，覆盖网络管理软件全场景，活跃维护中
- 组件命名中英混合（如 `Button 按钮`、`Select 选择器`），AI 可理解
- 未发布 Styles（颜色/字体通过 page 内规范文档定义而非 Figma Styles API）
- 未发布 Variables（Figma Variables 功能可能未采用）
