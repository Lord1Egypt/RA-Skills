---
name: miniprogram-architect
description: 提供微信小程序架构设计、项目结构优化、代码规范制定和组件库建立支持。当用户需要搭建新的微信小程序项目、重构现有项目结构或建立组件库时调用。
---

---
name: "miniprogram-architect"
description: "提供微信小程序架构设计、项目结构优化、代码规范制定和组件库建立支持。当用户需要搭建新的微信小程序项目、重构现有项目结构或建立组件库时调用。"
---

# 微信小程序架构师

## 功能介绍

本技能专注于微信小程序的架构设计和项目管理，为用户提供以下支持：

- 微信小程序项目结构设计和优化
- 代码规范和目录分割标准制定
- 组件库建立和复用策略
- 性能优化和最佳实践
- 项目架构文档编写
- 网络请求与API封装标准化
- 用户授权与隐私合规开发

## 适用场景

当用户需要：

- 新建微信小程序项目并搭建完整目录结构
- 重构现有小程序项目结构
- 制定团队开发规范和标准
- 建立可复用的组件库
- 优化小程序性能和加载速度

## 项目架构

### 目录结构

```
miniprogram-architect/
├── api/                        # API相关文件
├── assets/                     # 静态资源
│   ├── images/                 # 图片资源
│   └── styles/                 # 样式文件
├── pages/                      # 页面文件
│   ├── index/                  # 首页
│   └── tabBar/                 # 底部导航栏页面
├── utils/                      # 工具函数
├── app.js                      # 小程序入口文件
├── app.json                    # 小程序配置文件
├── app.wxss                    # 全局样式文件
├── project.config.json         # 项目配置文件
├── project.private.config.json # 项目私有配置文件
└── sitemap.json                # 小程序站点地图
```

### 技术栈

- 微信小程序原生开发
- WXML + WXSS + JavaScript
- WeUI组件库
- 微信官方API

## 使用指南

### 项目初始化

1. **目录结构搭建**：创建标准的小程序目录结构
2. **配置文件设置**：配置app.json、project.config.json等文件
3. **基础文件创建**：创建app.js、app.wxss等基础文件

### 代码规范

1. **命名规范**：文件、变量、函数的命名规则（It is not allowed to use Chinese naming.）
2. **代码风格**：缩进、注释、代码组织方式
3. **目录分割**：页面、组件、工具函数的目录划分标准

#### 模块导出规范（ES6 `export * as`）

在小程序项目中，可使用 ES2020 的 **命名空间重导出**  来统一导出路径配置、路由映射等，便于集中管理和复用：

```js
// utils/variable.js
export const home = 'pages/index/index'
export const about = 'pages/about/index'

// pages/paths.js
export * as paths from './variable';
console.log(paths.home)
```

```js
// pages/other.js
import { home } from './variable';

console.log(home)
```

### 组件库建立

1. **组件设计**：设计可复用的组件结构
2. **组件规范**：组件命名、参数传递、事件处理
3. **组件文档**：编写组件使用说明和示例

### 性能优化

1. **代码体积优化**：减少小程序包大小
2. **加载性能优化**：提高页面加载速度
3. **运行性能优化**：优化小程序运行时性能

## 最佳实践

### 目录结构最佳实践

- **模块化**：按功能模块划分目录
- **组件化**：将可复用部分抽象为组件
- **工具函数**：将通用功能封装为工具函数

### 代码规范最佳实践

- **命名规范**：使用驼峰命名法，避免使用拼音
- **注释规范**：关键代码添加注释，说明功能和实现思路
- **代码组织**：逻辑清晰，结构合理

### 性能优化最佳实践

- **按需加载**：使用lazyCodeLoading和componentPlaceholder
- **图片优化**：使用合适的图片格式和大小
- **网络请求优化**：合理使用缓存，减少请求次数

## 示例

### 项目结构示例

```
├── api/                        # API相关文件
│   ├── env.js                  # 环境配置（开发/测试/生产环境）
│   ├── dome.js                 # 功能相关API (根据实际项目功能设计API文件，如用户、商品、订单等模块)
│   └── fetch.js                # 网络请求封装 (封装网络请求：支持请求拦截、响应拦截、错误处理token刷新、中断请求任务等功能)
├── assets/                     # 静态资源
│   ├── images/                 # 图片资源
│   └── styles/                 # 样式文件
├── pages/                      # 页面文件
│   ├── index/                  # 启动页
│   └── tabBar/                 # 底部导航栏页面
│       ├── home/               # 首页
│       ├── folder/             # 档案夹
│       └── mine/               # 我的
├── utils/                      # 工具函数
│   ├── request.js              # 请求工具 (封装网络请求：wx.request、wx.downloadFile、wx.uploadFile参照axisos封装，支持请求拦截、响应拦截、错误处理等功能)
│   ├── util.js                 # 通用工具
│   └── version.js              # 版本工具
├── app.js                      # 小程序入口文件
├── app.json                    # 小程序配置文件
├── app.wxss                    # 全局样式文件
├── project.config.json         # 项目配置文件
├── project.private.config.json # 项目私有配置文件
└── sitemap.json                # 小程序站点地图
```

### 配置文件示例

- **说明**：iconPath、selectedIconPath路径需要根据实际项目资源路径调整，确保图标资源正确加载。

```json
{
  "pages": [
    "pages/index/index",
    "pages/tabBar/home/home",
    "pages/tabBar/folder/folder",
    "pages/tabBar/mine/mine"
  ],
  "window": {
    "backgroundTextStyle": "dark",
    "navigationBarBackgroundColor": "#FFFFFF",
    "navigationBarTitleText": "miniprogram-architect",
    "navigationBarTextStyle": "black"
  },
  "tabBar": {
    "color": "#666666",
    "selectedColor": "#4A76F3",
    "backgroundColor": "#ffffff",
    "borderStyle": "black",
    "list": [
      {
        "pagePath": "pages/tabBar/home/home",
        "text": "首页",
        "iconPath": "assets/images/tabbar/home.png",
        "selectedIconPath": "assets/images/tabbar/home_active.png"
      },
      {
        "pagePath": "pages/tabBar/folder/folder",
        "text": "档案夹",
        "iconPath": "assets/images/tabbar/folder.png",
        "selectedIconPath": "assets/images/tabbar/folder_active.png"
      },
      {
        "pagePath": "pages/tabBar/mine/mine",
        "text": "我的",
        "iconPath": "assets/images/tabbar/mine.png",
        "selectedIconPath": "assets/images/tabbar/mine_active.png"
      }
    ]
  },
  "sitemapLocation": "sitemap.json",
  "useExtendedLib": {
    "weui": true
  },
  "lazyCodeLoading": "requiredComponents"
}
```

## 注意事项

- 严格遵循微信小程序官方开发规范，确保代码符合平台审核标准；
- 严控代码体积，主包大小不超过 2MB，合理采用分包加载策略拆分非核心功能（如详情页、工具页），分包单个体积不超过 20MB、总体积不超过 200MB；
- 保障 API 调用安全，所有接口请求采用 HTTPS 协议，敏感接口添加签名 / Token 校验，避免明文传输用户信息；
- 优化页面性能与用户体验，包括但不限于：减少首屏加载时间、优化渲染逻辑、避免频繁 setData、添加加载态 / 空态提示；
- 提升代码可维护性与可扩展性，采用模块化 / 组件化开发，统一代码规范（如 ESLint），预留功能扩展接口；
- 分包管理需遵循 “核心功能主包、非核心功能分包” 原则，优先加载用户高频访问模块，降低初始加载压力。

## 分包配置（app.json）

```json
{
  "pages": [
    "pages/index/index", // 主包核心页面（首页）
    "pages/home/home"    // 主包高频页面
  ],
  "subpackages": [
    {
      "root": "packageA", // 分包A根目录
      "pages": [
        "pages/detail/detail", // 商品详情（非核心，分包加载）
        "pages/comment/comment" // 评论页（非核心）
      ],
      "independent": false // 非独立分包（可依赖主包资源）
    },
    {
      "root": "packageB", // 分包B（独立分包，如营销活动页）
      "pages": [
        "pages/activity/activity"
      ],
      "independent": true // 独立分包（不依赖主包，可单独加载）
    }
  ],
  "preloadRule": {
    // 预加载策略：进入首页时预加载packageA（提升后续跳转速度）
    "pages/index/index": {
      "network": "wifi", // 仅wifi下预加载
      "packages": ["packageA"]
    }
  }
}
```
## 关键说明

- independent: true 适用于无需主包资源的页面（如活动页），可单独打开，降低主包加载压力；
- preloadRule 按需预加载常用分包，平衡 “初始加载速度” 与 “后续体验”。

## 体积优化补充技巧

- 主包仅保留核心逻辑 + 高频页面，静态资源（如图片、大体积 JSON）优先放分包或 CDN；
- 使用微信开发者工具的「代码依赖分析」功能，清理未使用的代码 / 资源；
- 第三方库按需引入（如仅引入 Vant Weapp 的部分组件），避免全量导入。
  (如果不能按需引入，建议使用WEUI组件库，官方支持useExtendedLib不占用小程序的包体积或者把第三方库放在分包中，减少主包体积)
  
```json
{
  "useExtendedLib": {
    "weui": true
  }
}
```

## 总结

- 体积管控核心：主包严控 2MB，通过分包加载拆分非核心功能，配合预加载优化体验；
- 安全与性能：API 调用需 HTTPS + 签名校验，页面优化聚焦首屏加载与渲染效率；
- 可维护性：模块化开发 + 分包合理划分，兼顾代码扩展与平台规范。