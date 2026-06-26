---
name: product-prototype-design
version: 1.0.0
description: 快速生成高保真的产品交互原型（单个独立 HTML 文件），适用于产品经理、创业者、设计师快速验证想法。当用户提到原型设计、产品原型、交互原型、demo 制作、产品 Mock、界面原型、H5 原型、产品页面设计、MVP 原型、Landing Page、产品概念验证，或需要快速将产品想法可视化为可交互页面时，请使用此 skill。即使未明确提及'原型'，只要用户想快速做一个产品页面/界面/Demo，也应触发此 skill。
metadata:
  openclaw:
    emoji: "🎨"
    tags: ["prototype", "design", "ui", "ux", "demo", "landing"]
---

# 产品原型设计

快速生成高保真交互原型，单文件独立 HTML，无需部署即可体验。

## 设计流程

### Step 1: 需求收集

使用 AskUserQuestion 收集关键信息：

```markdown
请告诉我关于原型的基本信息：

1. **产品类型** (单选)
   - SaaS 应用
   - 移动 App
   - 电商网站
   - 内容平台
   - 工具类产品
   - 其他

2. **目标用户** (单选)
   - 企业用户 (B2B)
   - 个人消费者 (B2C)
   - 开发者
   - 创造者
   - 学生
   - 其他

3. **核心功能** (多选最多3项)
   [ ] 用户注册/登录
   [ ] 数据展示/列表
   [ ] 搜索/筛选
   [ ] 内容创建/编辑
   [ ] 购买/支付
   [ ] 社交分享
   [ ] 数据分析/报表
   [ ] 设置/个人中心

4. **风格偏好** (单选)
   - 现代简约
   - 专业商务
   - 活力创新
   - 科技未来
   - 温情人文
   - 其他
```

### Step 2: 页面规划

根据收集的信息，规划原型包含的关键页面：

```markdown
产品原型将包含以下页面：

✅ Page 1: 首页/仪表盘
- 主要数据展示
- 快捷操作入口
- 核心功能预览

✅ Page 2: 核心功能页
- [根据选择的3个核心功能]

✅ Page 3: 详情/配置页
- 详细设置选项
- 高级功能

✅ Page 4: 个人中心
- 用户信息
- 偏好设置

确认这个规划是否符合您的预期？
```

### Step 3: 行业风格应用

查询 `references/industry-design-specs.md` 获取对应行业的设计规范：

- 根据产品类型选择配色方案
- 应用推荐的视觉风格
- 使用行业标准的交互模式

### Step 4: 生成原型

调用 Write 工具创建单文件 HTML 原型：

**文件命名规范**: `product-prototypes/{产品类型}_{时间戳}.html`

**技术栈**:
- HTML5 语义化标签
- Tailwind CSS (CDN)
- 原生 JavaScript (ES6+)
- 微交互动画 (CSS transitions)
- 模拟数据 (JSON)

### Step 5: 交付说明

```markdown
✅ 原型已生成！

文件位置: product-prototypes/{产品类型}_{时间戳}.html

使用方法:
1. 双击 HTML 文件即可在浏览器打开
2. 无需任何服务器或部署
3. 所有交互都是可点击的
4. 点击页面顶部的导航可切换页面

预览链接: [如果支持在线预览]

📝 原型说明:
- 包含 {N} 个核心页面
- 实现了 {M} 个交互功能
- 包含 {K} 个微动效
- 响应式设计，支持移动端
```

## 原型模板库

### SaaS 仪表盘模板
```
关键元素:
- 侧边导航栏
- 顶部用户信息
- 数据图表区域
- 快速操作卡片
- 最近活动列表
```

### 电商产品页模板
```
关键元素:
- 商品轮播图
- 价格/购买按钮
- 规格选择器
- 商品描述标签
- 相关推荐
```

### 内容平台模板
```
关键元素:
- 内容瀑布流
- 筛选/排序
- 点赞/收藏
- 评论互动
- 创作者信息
```

### 工具类产品模板
```
关键元素:
- 功能输入区
- 实时预览
- 操作按钮
- 历史记录
- 导出/分享
```

## 高级功能

### 数据可视化
- Chart.js 图表展示
- 动态数据更新
- 交互式筛选

### 表单交互
- 步骤式表单
- 实时验证
- 拖拽排序

### 列表管理
- 虚拟滚动
- 批量操作
- 拖拽上传

### 通知系统
- Toast 提示
- Badge 徽章
- 弹窗模态

## 最佳实践

### 1. 快速原型原则
- 80/20 法则：实现核心 20% 的功能，呈现 80% 的效果
- 灰度模式：先布局后上色
- 渐进增强：基础交互 → 微动画 → 复杂功能

### 2. 用户体验
- 3 秒规则：3秒内理解页面价值
- 一致性：保持全局设计语言统一
- 反馈：每个操作都有视觉反馈

### 3. 技术实现
- 组件化思维：可复用的 UI 模块
- 性能优化：懒加载防抖节流
- 移动优先：响应式设计

## 示例输出

### 文件结构
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>产品原型 - {产品名称}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* 自定义样式和动画 */
    </style>
</head>
<body>
    <!-- 导航栏 -->
    <!-- 页面内容 -->
    <!-- 交互逻辑 -->
    <script>
        // 所有交互代码
    </script>
</body>
</html>
```

### 交互示例
```javascript
// 页面切换
function showPage(pageId) {
    document.querySelectorAll('.page').forEach(p => p.classList.add('hidden'));
    document.getElementById(pageId).classList.remove('hidden');
}

// 模态框控制
function showModal(content) {
    // 显示模态框逻辑
}

// 表单验证
function validateForm() {
    // 验证逻辑
}
```

## 扩展功能

### 数据持久化
- LocalStorage 保存设置
- 导出/导入配置

### 分享功能
- 生成分享链接
- 导出为图片
- 分享到社交平台

### 协作功能
- 评论标注
- 版本对比
- 反馈收集

## 交付物清单

- [✅] product-prototype-{timestamp}.html (主文件)
- [ ] assets/ (静态资源，如需要)
- [ ] README.md (使用说明)
- [ ] changelog.md (版本记录)

## 后续优化建议

1. **添加真实 API 集成**
2. **实现后端数据存储**
3. **增加用户认证系统**
4. **优化移动端体验**
5. **添加无障碍支持**
