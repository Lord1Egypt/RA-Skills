# 普通主页布局

单表格页面，是最常用的布局类型。

## 特点

- 单一表格展示列表数据
- 工具栏提供操作按钮
- 支持分页查询

## 生成文件

| 文件 | 说明 |
|-----|------|
| index.jsx | 主页面（表格 + 工具栏） |
| TopTags/index.jsx | 工具栏组件 |

## 目录结构

```
{frontend.path}/{模块名}/
├── index.jsx              # 主页面
└── TopTags/
    └── index.jsx          # 工具栏
```

## 模板文件

| 文件 | 说明 |
|-----|------|
| web-index.jsx.vm | 主页模板 |
| web-toptags.jsx.vm | 工具栏模板 |

## 联动原理

普通主页支持标签页联动：
```
选中行 → setRightData(record) → RightTags 显示详情
```
