# 标签页布局

标签页是一种常见的详情页布局模式，点击列表行后在右侧滑出详细信息。

## 标签页与布局的组合

| 布局类型 | 标签页行为 |
|---------|-----------|
| **普通主页** | 点击行时联动刷新页签，RightTags 从右侧滑出 |
| **左右布局** | 以右边页面为主，点击行时联动刷新页签 |

## 普通主页 + 标签页

```
主页面（index.jsx）
    ├── 表格（列表数据）
    ├── 工具栏（TopTags）
    └── 右侧标签面板（RightTags）← 点击行时滑出
          ├── 页签1：Labels/Edit/index.jsx（编辑/基本信息）
          ├── 页签2：Labels/History/index.jsx（历史记录）
          └── 页签3：Labels/xxx/index.jsx（自定义）
```

## 左右布局 + 标签页

```
主页面（index.jsx）
    ├── 左边（LeftIndex.jsx）
    └── 右边（RightIndex.jsx）← 点击左边行时右边联动刷新
          ├── 表格/树形（右边数据）
          ├── 工具栏（TopTags）
          └── 右侧标签面板（RightTags）
                ├── 页签1：Labels/Edit/index.jsx
                ├── 页签2：Labels/History/index.jsx
                └── 页签3：Labels/xxx/index.jsx
```

## 联动原理

```
普通主页：选中行 → setRightData(record) → RightTags 显示详情
左右布局：选中左边行 → setForeignKey(record.id) → 右边数据刷新 → RightTags 联动
```

## 标签页结构

```
组件引用方式：
<RightTags
    tabChildren={tabChildren}
    menuCode={menuInfo.menuCode}
    rightData={rightData}         // 选中行数据
    bizType={'corp'}
    bizId={rightData?.id || null}
/>
```

## 标签页识别特征

- 用户描述包含"页签"、"标签页"、"右侧详情"等
- 例如："点击一行后右边显示基本信息等页签"、"有基本信息、历史等页签"
- 右侧面板需要显示选中行的详细信息

## 模板文件

| 文件 | 说明 |
|-----|------|
| web-label-index.jsx.vm | 标签页主页 |
| web-label-toptags.jsx.vm | 标签页工具栏 |
| Labels/{tabName}/index.jsx | 各页签内容组件 |

## 代码组织

- 标签页组件生成到 Labels 子目录下
- 目录结构：
  ```
  {frontend.path}/{模块名}/
  ├── index.jsx              # 主页面
  ├── TopTags/
  │   └── index.jsx          # 工具栏
  └── Labels/
      ├── Edit/
      │   └── index.jsx       # 基本信息页签
      ├── History/
      │   └── index.jsx       # 历史记录页签
      └── {自定义页签}/
          └── index.jsx       # 自定义页签
  ```

## SKILL 自动识别页签

- 根据用户描述提取页签名称
- 默认页签：Edit（基本信息）、History（历史记录）
- 自定义页签：用户提供则按其描述生成

## 标签页自动判断流程

当用户输入包含"页签"、"标签页"描述时，自动进入此流程：

```
步骤3a：解析页签描述
    - 提取页签名称列表（如：基本信息、历史记录）
    - 默认页签：Edit（基本信息）、History（历史记录）
    ↓
步骤3b：确认标签页配置
    - bizType：业务类型（如 corp、project）
    - bizId：业务ID（选中行的 ID）
    ↓
步骤3c：生成标签页代码
    - 主页面：web-label-index.jsx.vm（含 RightTags 引用）
    - 工具栏：web-label-toptags.jsx.vm
    - 页签组件：Labels/{tabName}/index.jsx
    - 代码组织：生成到 Labels 子目录下
```
