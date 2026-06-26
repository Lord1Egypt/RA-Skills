---
name: masa-blazor
description: 基于 MASA Blazor 组件库进行 Blazor 开发的参考指南。当用户询问 MASA Blazor 的使用、组件、样式、配置或最佳实践时使用。文档地址格式: https://docs.masastack.com/blazor/{category}/{item}。
---

# MASA Blazor 开发指南

## 概述
MASA Blazor 是基于 Material Design 3 规范的 Blazor UI 组件库，100+ 高质量组件，支持 SSR/SSG/WASM。官方文档: https://docs.masastack.com/blazor

## 完整文档路径映射

URL 格式: `https://docs.masastack.com/blazor/{category}/{item}`

### 1. Introduction (入门介绍)
- `/blazor/introduction/why-masa-blazor` — 为什么选择 MASA Blazor
- `/blazor/introduction/roadmap` — 产品路线图

### 2. Getting Started (快速开始)
- `/blazor/getting-started/installation` — 安装配置
- `/blazor/getting-started/browser-support` — 浏览器兼容性
- `/blazor/getting-started/frequently-asked-questions` — 常见问题
- `/blazor/getting-started/wireframes` — 布局模板
- `/blazor/getting-started/release-notes` — 版本更新日志
- `/blazor/getting-started/upgrade-guide` — 升级指南
- `/blazor/getting-started/contributing` — 贡献指南

### 3. Features (特性)
- `/blazor/features/bidirectionality` — 双向文本支持
- `/blazor/features/breakpoints` — 响应式断点
- `/blazor/features/icon-fonts` — 图标字体
- `/blazor/features/internationalization` — 国际化 (i18n)
- `/blazor/features/auto-match-nav` — 自动导航匹配
- `/blazor/features/theme` — 主题定制
- `/blazor/features/ssr` — 服务端渲染支持

### 4. Basic Concepts (基本概念) NEW
- `/blazor/basic-concepts/activator` — 激活器模式
- `/blazor/basic-concepts/rendering` — 渲染机制
- `/blazor/basic-concepts/two-way-binding` — 双向绑定

### 5. Styles and Animations (样式与动画)
- `/blazor/styles-and-animations/border-radius` — 圆角
- `/blazor/styles-and-animations/color` — 颜色系统
- `/blazor/styles-and-animations/display-helpers` — 显示辅助类
- `/blazor/styles-and-animations/elevation` — 阴影层级
- `/blazor/styles-and-animations/flex` — 弹性布局
- `/blazor/styles-and-animations/floats` — 浮动
- `/blazor/styles-and-animations/overflow` — 溢出控制
- `/blazor/styles-and-animations/spacing` — 间距
- `/blazor/styles-and-animations/text-and-typography` — 文字排版
- `/blazor/styles-and-animations/transitions` — 过渡动画

### 6. UI Components (UI 组件)

#### 6.1 Alerts / Alerts (反馈)
- `/blazor/ui-components/alerts` — 警告提示

#### 6.2 Application
- `/blazor/ui-components/application` — 应用根组件

#### 6.3 Aspect Ratios / Images & Icons (图片与图标)
- `/blazor/ui-components/aspect-ratios` — 宽高比
- `/blazor/ui-components/avatars` — 头像
- `/blazor/ui-components/icons` — 图标
- `/blazor/ui-components/images` — 图片
- `/blazor/ui-components/video-feeder` — 视频播放 (Labs)
- `/blazor/ui-components/xgplayer` — 西瓜播放器

#### 6.4 Badges / Banners / Borders (反馈)
- `/blazor/ui-components/badges` — 徽章
- `/blazor/ui-components/banners` — 横幅
- `/blazor/ui-components/borders` — 边框

#### 6.5 Bars (导航/容器)
- `/blazor/ui-components/bars/app-bars` — 应用顶部栏
- `/blazor/ui-components/bars/toolbars` — 工具栏
- `/blazor/ui-components/bars/system-bars` — 系统状态栏

#### 6.6 Block Text / Copyable Text (数据展示)
- `/blazor/ui-components/block-text` — 块文本
- `/blazor/ui-components/copyable-text` — 可复制文本

#### 6.7 Bottom Navigation / Bottom Sheets / Breadcrumbs (导航/容器)
- `/blazor/ui-components/bottom-navigation` — 底部导航
- `/blazor/ui-components/bottom-sheets` — 底部弹出面板
- `/blazor/ui-components/breadcrumbs` — 面包屑

#### 6.8 Buttons / Cards / Chips (容器)
- `/blazor/ui-components/buttons` — 按钮
- `/blazor/ui-components/cards` — 卡片
- `/blazor/ui-components/chips` — 标签

#### 6.9 Carousels (选择)
- `/blazor/ui-components/carousels` — 轮播

#### 6.10 Cron / BaiduMaps / Drawflow / Gridstack (杂项)
- `/blazor/ui-components/cron` — Cron 表达式
- `/blazor/ui-components/baidumaps` — 百度地图
- `/blazor/ui-components/drawflow` — 流程图
- `/blazor/ui-components/gridstack` — 网格堆叠

#### 6.11 Defaults Providers / Theme Providers (提供者)
- `/blazor/ui-components/defaults-providers` — 默认值配置
- `/blazor/ui-components/theme-providers` — 主题配置 (Labs)

#### 6.12 Descriptions (数据展示)
- `/blazor/ui-components/descriptions` — 描述列表

#### 6.13 Dialogs / Dividers / Drawers (容器)
- `/blazor/ui-components/dialogs` — 对话框
- `/blazor/ui-components/dividers` — 分割线
- `/blazor/ui-components/drawers` — 抽屉

#### 6.14 Echarts (数据展示)
- `/blazor/ui-components/echarts` — ECharts 图表

#### 6.15 DriverJS (反馈, Labs)
- `/blazor/ui-components/driverjs` — 引导教程

#### 6.16 Editors / Markdowns / Monaco Editor (表单)
- `/blazor/ui-components/editors` — 富文本编辑器
- `/blazor/ui-components/markdowns` — Markdown 编辑
- `/blazor/ui-components/monaco-editor` — 代码编辑器

#### 6.17 Empty States / Enqueued Snackbars / Error Handler (反馈)
- `/blazor/ui-components/empty-states` — 空状态 NEW
- `/blazor/ui-components/enqueued-snackbars` — 消息队列
- `/blazor/ui-components/error-handler` — 错误处理

#### 6.18 Expansion Panels / Floating Action Buttons / Footers (容器/导航)
- `/blazor/ui-components/expansion-panels` — 折叠面板
- `/blazor/ui-components/floating-action-buttons` — 悬浮操作按钮
- `/blazor/ui-components/footers` — 页脚

#### 6.19 Form Inputs and Controls (表单)
- `/blazor/ui-components/form-inputs-and-controls/autocompletes` — 自动完成
- `/blazor/ui-components/form-inputs-and-controls/cascaders` — 级联选择
- `/blazor/ui-components/form-inputs-and-controls/checkboxes` — 复选框
- `/blazor/ui-components/form-inputs-and-controls/combobox` — 组合框 (Labs)
- `/blazor/ui-components/form-inputs-and-controls/file-inputs` — 文件上传
- `/blazor/ui-components/form-inputs-and-controls/forms` — 表单验证
- `/blazor/ui-components/form-inputs-and-controls/otp-input` — 验证码输入
- `/blazor/ui-components/form-inputs-and-controls/radios` — 单选框
- `/blazor/ui-components/form-inputs-and-controls/range-sliders` — 范围滑块
- `/blazor/ui-components/form-inputs-and-controls/selects` — 下拉选择
- `/blazor/ui-components/form-inputs-and-controls/sliders` — 滑块
- `/blazor/ui-components/form-inputs-and-controls/switches` — 开关
- `/blazor/ui-components/form-inputs-and-controls/textareas` — 多行文本
- `/blazor/ui-components/form-inputs-and-controls/text-fields` — 文本输入框

#### 6.20 Grids / GridStack (容器)
- `/blazor/ui-components/grids` — 网格布局
- `/blazor/ui-components/gridstack` — 网格堆叠

#### 6.21 Groups (选择)
- `/blazor/ui-components/groups/button-groups` — 按钮组
- `/blazor/ui-components/groups/chip-groups` — 标签组
- `/blazor/ui-components/groups/item-groups` — 选项组
- `/blazor/ui-components/groups/list-item-groups` — 列表选项组
- `/blazor/ui-components/groups/slide-groups` — 滑动组
- `/blazor/ui-components/groups/windows` — 窗口切换

#### 6.22 Hover / Icons / I18ns / Image Captcha (反馈/杂项/表单)
- `/blazor/ui-components/hover` — 悬停效果
- `/blazor/ui-components/icons` — 图标
- `/blazor/ui-components/i18ns` — 国际化
- `/blazor/ui-components/image-captcha` — 图片验证码

#### 6.23 Images (图片与图标)
- `/blazor/ui-components/images` — 图片

#### 6.24 Lists / Infinite Scroll / Inputs Filter / Interactive Trigger / Lazy (容器/数据/杂项)
- `/blazor/ui-components/lists` — 列表
- `/blazor/ui-components/infinite-scroll` — 无限滚动
- `/blazor/ui-components/inputs-filter` — 输入筛选
- `/blazor/ui-components/interactive-trigger` — 交互触发
- `/blazor/ui-components/lazy` — 懒加载

#### 6.25 Markdown Parsers (数据展示)
- `/blazor/ui-components/markdown-parsers` — Markdown 渲染

#### 6.26 Menus / Modals (容器)
- `/blazor/ui-components/menus` — 菜单
- `/blazor/ui-components/modals` — 模态框

#### 6.27 Navigation Drawers / Overlays (导航)
- `/blazor/ui-components/navigation-drawers` — 侧边导航抽屉
- `/blazor/ui-components/overlays` — 遮罩层

#### 6.28 Page Tabs (导航)
- `/blazor/ui-components/page-tabs` — 页面标签页

#### 6.29 Paginations (导航)
- `/blazor/ui-components/paginations` — 分页

#### 6.30 Pickers (选择器)
- `/blazor/ui-components/pickers/date-pickers` — 日期选择
- `/blazor/ui-components/pickers/date-pickers-month` — 月份选择
- `/blazor/ui-components/pickers/time-pickers` — 时间选择
- `/blazor/ui-components/pickers/date-digital-clock-pickers` — 日期数字时钟
- `/blazor/ui-components/pickers/date-time-pickers` — 日期时间选择
- `/blazor/ui-components/pickers/digital-clocks` — 数字时钟
- `/blazor/ui-components/pickers/date-time-range-pickers` — 日期时间范围 (Labs)

#### 6.31 Popup Service (服务)
- `/blazor/ui-components/popup-service` — 弹出服务

#### 6.32 Progress (反馈)
- `/blazor/ui-components/progress/progress-circular` — 圆形进度
- `/blazor/ui-components/progress/progress-linear` — 线性进度

#### 6.33 Ratings (反馈)
- `/blazor/ui-components/ratings` — 评分

#### 6.34 Scroll to Target (导航)
- `/blazor/ui-components/scroll-to-target` — 滚动定位

#### 6.35 Sheets (容器)
- `/blazor/ui-components/sheets` — 面板

#### 6.36 Skeleton Loaders / Snackbars (反馈)
- `/blazor/ui-components/skeleton-loaders` — 骨架屏
- `/blazor/ui-components/snackbars` — 消息提示

#### 6.37 Sortable / Splitters / Steppers / Sticky / Subheaders (容器/选择)
- `/blazor/ui-components/sortable` — 拖拽排序
- `/blazor/ui-components/splitters` — 分割面板
- `/blazor/ui-components/steppers` — 步骤条
- `/blazor/ui-components/sticky` — 吸顶
- `/blazor/ui-components/subheaders` — 子标题

#### 6.38 Syntax Highlights (数据展示)
- `/blazor/ui-components/syntax-highlights` — 代码高亮

#### 6.39 Tables (数据展示)
- `/blazor/ui-components/tables/data-iterators` — 数据迭代器
- `/blazor/ui-components/tables/data-tables` — 数据表格
- `/blazor/ui-components/tables/simple-tables` — 简单表格

#### 6.40 Tabs (导航)
- `/blazor/ui-components/tabs` — 标签页

#### 6.41 Timelines (反馈)
- `/blazor/ui-components/timelines` — 时间线

#### 6.42 Toggles (选择)
- `/blazor/ui-components/toggles` — 切换按钮

#### 6.43 Tooltips (容器)
- `/blazor/ui-components/tooltips` — 工具提示

#### 6.44 Treeview (数据展示)
- `/blazor/ui-components/treeview` — 树形视图

#### 6.45 Virtual Scroll (数据展示)
- `/blazor/ui-components/virtual-scroll` — 虚拟滚动

#### 6.46 Watermark (容器)
- `/blazor/ui-components/watermark` — 水印

### 7. Mobiles (移动端组件)
- `/blazor/mobiles/cell` — 单元格 (Labs)
- `/blazor/mobiles/mobile-cascader` — 移动端级联
- `/blazor/mobiles/mobile-date-pickers` — 移动端日期选择
- `/blazor/mobiles/mobile-date-time-pickers` — 移动端日期时间选择
- `/blazor/mobiles/mobile-pickers` — 移动端选择器
- `/blazor/mobiles/mobile-picker-views` — 移动端选择视图
- `/blazor/mobiles/mobile-time-pickers` — 移动端时间选择
- `/blazor/mobiles/page-stack` — 页面栈
- `/blazor/mobiles/pdf-mobile-viewer` — PDF 阅读器
- `/blazor/mobiles/pull-refresh` — 下拉刷新
- `/blazor/mobiles/swipe-actions` — 滑动操作 (Labs)
- `/blazor/mobiles/swiper` — 轮播滑动

### 8. JS Modules (JavaScript 模块)
- `/blazor/js-modules/intersection-observer` — 交叉观察器

## 项目配置

### 安装
```bash
dotnet add package MASA.Blazor
```

### 注册服务 (Program.cs)
```csharp
builder.Services.AddMasaBlazor();
```

### 引用资源 (wwwroot/index.html)
```html
<link href="_content/MASA.Blazor/css/masa-blazor.min.css" rel="stylesheet" />
<script src="_content/MASA.Blazor/js/masa-blazor.js"></script>
```

### 命名空间 (_Imports.razor)
```csharp
@using Masa.Blazor
```

## 官方资源
- 文档: https://docs.masastack.com/blazor
- GitHub: https://github.com/masastack/MASA.Blazor
- 示例: https://blazor-pro.masastack.com

## 详细参考文档
详见 `references/` 目录下的详细文档:
- `components.md` — 组件总览索引
- `styles.md` — 样式工具类全集
- `theme.md` — 主题配置详解
- 各组件独立文档 (buttons.md, dialogs.md, etc.)
