# NutriCoach Skill 代码重构分析

## 当前问题

### 1. web_server.py 过于臃肿 (968 行)
- HTML 模板嵌入在 Python 代码中 (~700 行)
- JavaScript 代码混杂在 Python 字符串中
- 难以维护，容易出错

### 2. 其他脚本相对合理
| 文件 | 行数 | 状态 |
|------|------|------|
| body_metrics.py | 285 | ✅ 合理 |
| diet_recommender.py | 292 | ✅ 合理 |
| food_ocr.py | 321 | ✅ 合理 |
| smart_recipe.py | 321 | ✅ 合理 |
| food_matcher.py | 371 | ✅ 合理 |
| meal_logger.py | 404 | ✅ 合理 |
| food_analyzer.py | 489 | ✅ 合理 |
| pantry_manager.py | 562 | ⚠️ 略长但可接受 |
| web_server.py | 968 | ❌ 需要重构 |

## 重构方案

### 方案 A: 分离 HTML 模板（推荐）

将 web_server.py 拆分为:
```
scripts/
├── web_server.py          # 精简版 (~200 行)
└── web/
    ├── __init__.py
    ├── routes.py          # API 路由
    ├── utils.py           # 工具函数
    └── static/
        ├── style.css      # 样式
        └── app.js         # JavaScript
templates/
└── dashboard.html         # HTML 模板
```

**优点**:
- HTML/CSS/JS 分离，各自独立维护
- 代码清晰，易于迭代
- 符合 Flask 最佳实践

**缺点**:
- 需要多文件管理
- 模板文件需要版本控制

### 方案 B: 保持现状，优化结构

保持单文件，但优化组织:
1. 将 HTML 模板移到文件顶部常量
2. 将 JavaScript 提取为单独字符串常量
3. 添加清晰的代码分区注释

**优点**:
- 单文件，部署简单
- 无需额外文件管理

**缺点**:
- 仍然臃肿
- 难以维护

## 建议

**短期**: 采用方案 B，优化 web_server.py 结构
**长期**: 采用方案 A，完全模块化

## 当前已做优化

1. ✅ TEMPLATE_VERSION 机制 — 解决模板缓存问题
2. ✅ 端口改为 8080 — 避免 macOS AirPlay 冲突
3. ✅ 保质期逻辑 — 自动计算过期日期
4. ✅ UI 精简 — 整合编辑/使用按钮

## 下一步行动

1. 将 web_server.py HTML 模板分离到 templates/dashboard_v3.html
2. 创建 scripts/web/ 目录存放辅助模块
3. 更新 launch_dashboard.py 使用新版本
