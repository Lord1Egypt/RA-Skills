# LQS Skill MVP 交付清单

> 说明：当前以“可实施交付”为目标。
> - [x] = 规范/模板资产已完成
> - [ ] = 后续可选集成项

## A. 输入能力
- [x] 支持自由文本输入
- [x] 支持 Google Doc 导出正文输入（手动粘贴或外部抓取后粘贴）
- [x] 文本归一化（基础版）

## B. 需求分析
- [x] 生成 RequirementDraft
- [x] 识别实体、字段、操作、后台页面
- [x] 输出缺失项（如主键/状态字段）建议（assumptions）

## C. 项目分析与模板沉淀
- [x] 扫描 Admin 代表性控制器
- [x] 扫描 Admin 代表性 views 模板
- [x] 归纳查询参数与响应结构
- [x] 自动产出 TemplatePack（controller/model/view/migration）

## D. 规格解析与渲染
- [x] RequirementDraft -> Spec（Schema 与 Prompt 已定义）
- [x] 默认模块 Admin
- [x] 默认基类 BackendBaseController
- [x] 使用 typecho_ 前缀生成 migration 表名

## E. 预览与写入
- [x] 默认 dry-run 输出 unified diff（Prompt 与流程已定义）
- [x] approve 后写入文件（Prompt 已定义）
- [x] 输出最终变更清单（路径、类型、风险）（Schema 已定义）

## F. 验收用例
- [x] 输入"文章管理 CRUD"可生成四类工件（样例与模板已就绪）
- [x] 输出路径符合项目目录规则
- [x] migration 具备 up/down
- [x] 全流程不包含任何凭证

## G. 渲染执行层
- [x] RenderPlan Schema 定义完成
- [x] 渲染 Prompt（Spec -> RenderPlan）完成
- [x] Diff Prompt（RenderPlan -> unified diff）完成
- [x] Article 全链路样例（RequirementDraft/Spec/RenderPlan）完成

## H. 非代码化流程约束
- [x] Skill 流程不依赖仓库内命令执行器
- [x] 交付以 Prompt / Schema / Template 为核心
- [x] 保留后续外部集成空间，但不在仓库内固化执行代码

## I. 纯自然语言推断能力（核心目标）
- [x] 不要求执行器、不要求编码、不要求命令行
- [x] 每轮输出包含 assumptions/evidence/confidence/ambiguities
- [x] 歧义项可保留，但必须显式记录默认处理策略
- [x] 每轮至少沉淀一条可复用上下文或模式修正

## J. 渐进式精度验收
- [x] 第二轮分析相比第一轮，歧义项数量减少或定义更精确
- [x] 低置信度项在后续轮次转为中/高置信度，或给出明确保留原因
- [x] 需求变化时，能保留旧模式并新增例外说明，避免“覆盖式遗忘”
