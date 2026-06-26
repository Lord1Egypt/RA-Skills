# lanhu-code-2-el-vue 文档索引

本目录为「静态页面改造为动态页面」指导文档的拆分结果。执行任务时按需查阅对应文档。

| 分类 | 文件 | 主要内容 |
|------|------|----------|
| 项目配置 | `project-config.md` | 文件路径、技术栈、改造目标、改造前后示例 |
| 核心规范 | `style-consistency.md` | 样式一致性（最高优先级）、响应式布局、验证方法 |
| 核心规范 | `class-naming.md` | CSS 类命名规范（仅下划线、禁止数字、格式/词汇）+ 任务5 Class 重命名强制要求与修复流程 |
| 核心规范 | `render.md` | 循环渲染：v-for 使用、实现要求、图片路径、常见错误 |
| 核心规范 | `class-naming.md` | CSS 类命名规范（仅下划线、禁止数字、格式/词汇）+ 任务5 Class 重命名强制要求与修复流程 |
| 核心规范 | `element-ui-style.md` | Element UI 替换规范、样式覆盖与深度选择器（含选择器优先级）、**搜索框 2.4/2.4.5**、公式栏、多选/按钮先删后写、el-rate、任务4 强制要求与修复流程、**UI/UX 与可访问性（与 ui-ux-pro-max 对齐）** |
| 核心规范 | `style-match-standard.md` | 按元素重要性的样式匹配标准 |
| 执行流程 | `execution-flow.md` | 执行前准备、开发原则、组件同步生成、验证流程 |
| 任务清单 | `tasks.md` | 任务 1～5 的步骤与验收标准 |
| 验证与验收 | `validate.md` | 最终验证清单：样式 / 功能 / 代码质量检查 |
| 常见问题 | `faq-solutions.md` | 样式、循环、图片、布局、交互等常见问题及解决方案 |
| 识别与修复 | `recognition-and-fix.md` | 下拉框、多选框、**纵向模块勾选列（§2.2.1 / §3.2.1）**、带外框搜索框等的识别规则与修复方法（含自检清单） |
| 识别与修复 | `search-input-and-page-overflow.md` | **带外框搜索框 placeholder 垂直居中**与**输入框/底栏按钮不溢出页面**的识别、修复与需求文案 |
| 识别与修复 | `el-button-root-and-deep.md` | **el-button**：根 class 与 `::v-deep`；勿用 `type="text"` 冒充带框次要按钮；相邻 10px；子 img/span 去 margin；三态与 primary 字色 |
| 识别与修复 | `el-select-suffix-alignment.md` | **el-select**：后缀箭头对齐；禁止根 flex+space-between；小高度同步 icon/suffix/padding-right |
| 参考资源 | `references.md` | Element UI、Vue 2 文档链接 |
| 关键要求 | `requirements.md` | 文件操作、执行原则、代码规范、数据与方法完整性、验收 |
| 流程总结 | `workflow-summary.md` | 完整开发流程、检查点、快速参考流程图 |
| 附录 | `appendix.md` | 常用组件参考、Vue 参考、排查指南、最佳实践 |
| 完成后 | `completion.md` | 完成后操作与依赖检查、启动项目说明 |

## 三、执行顺序（必须严格遵守）

1. **页面结构分析** - 分析源文件，识别循环结构和Element UI替换点
2. **Class 名称更改** - 将所有 class 按规范重命名（下划线连接，不含数字）
3. **循环渲染开发** - 将列表改为循环渲染，使用 v-for 或显式展开
4. **Element UI 组件替换** - 将原生HTML元素替换为Element UI组件
5. **Element UI 样式修改** - 使用深度选择器覆盖默认样式
6. **样式验证** - 全面验证与源稿像素级一致

**执行顺序口诀：**
```
一分析、二改名、三循环、
四替换、五改样、六验证
```

**使用说明：** 按分类查阅对应文档，执行任务时结合本目录下各 .md 文件即可。
