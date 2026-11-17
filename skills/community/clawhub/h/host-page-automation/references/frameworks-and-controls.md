# 框架与控件指南

这里是探测线索和历史经验，不是任意页面都可直接执行的 API 清单。先只读确认版本、能力和作用域，再在允许的测试字段验证。框架私有接口仅限能力检测及受控适配，不作为跨版本承诺。

## Vue 2 / Element UI / Avue

- 线索：DOM `__vue__`、VNode context、组件 `$options`、`$parent`、`$refs`、表单 prop 和 model。
- 分别读取控件 value、selectedLabel、真实选项及禁用状态；表单 label 不一定等于模型 key。
- 优先正常输入事件、组件事件和宿主 lookup/choose 回调。直接改模型可能遗漏关联记录、明细等联动逻辑。
- 弹窗、下拉可能挂到 body，须确认归属和唯一可见浮层，不扫全页第一个同名项。
- Avue 的内部 `form` 与外部 `value` 可能不是同一对象；分别检查 ElForm.model、Avue.form/value 和业务 v-model，并用引用比较或 render 绑定确认关系。
- 主表与弹窗查询区可能存在同名 prop；表格固定列还可能复制 radio DOM。以业务作用域与候选集合为准，不以第一个元素或 DOM 数量作为身份依据。
- 查询后选中索引可能保留旧值。重新按业务 ID/编码唯一匹配，并验证当前索引确实指向目标记录；临时 `$index` 不作稳定业务身份。
- SPA document_start 时路由尚未就绪，探测安装与业务操作守卫分开；写入时再次检查目标路由。

## Vue 3 / Arco 等

- 线索：`__vue_app__`、`__vueParentComponent`、根 VNode.component、subTree、proxy、setupState、props、refs。
- `app._instance` 可能为空；DOM `_vnode` 的存在不能单独证明 Vue 2。
- 根组件没有业务状态是正常的，目标可能位于 RouterView/KeepAlive 子树。
- 读取内部状态帮助定位，执行仍优先正常 input/update 事件及业务按钮；不要直接改 props 或私有 VNode。
- 不复用 Vue 2 实例字段作为 Vue 3 接口，不假设组件库相同。

## React / Ant Design 等

- 线索：动态后缀 `__reactFiber$...`、`__reactProps$...`；旧版本还可能使用 `__reactInternalInstance$...`、`__reactEventHandlers$...` 和根 `_reactRootContainer`。沿父链只读观察 props、事件和状态，不因只查新版入口失败就排除 React。
- 受控输入不能只验证 input.value。优先验证正常输入事件；必要时使用已验证的当前 props 事件适配，检查子组件与父业务状态同步。
- 原生 value setter + input/change 对部分组件有效，但不是统一保证；重渲染后值回退通常说明状态未更新。
- 按钮优先正常 click，并检查 disabled/loading 和真实业务结果，不把点击未报错当成功。
- 禁止正式依赖固定 Hook 下标、压缩组件名、闭包函数名、memoizedState 修改或 queue.dispatch。
- Fiber 仅作受控诊断入口，不导出完整组件树或闭包对象。

## Ext 表单

- 线索：当前 iframe 的 Ext、getCmp、ComponentQuery、组件 xtype、input、store 和选项。
- 业务组件 ID 可作候选稳定锚点，但 radiofield-* 等动态 ID 不可硬编码。按稳定组 + 真实 inputValue + 标签唯一定位。
- setValue 可产生 change，不重复伪造；select 的签名和是否需要补发必须按版本实测，不能所有字段机械发送。
- 日期按页面本地格式处理，不转 UTC；时间使用控件解析逻辑，不随意制造 Date 基准日。
- 类型改变可能销毁/重建日期、单选和条件字段。赋值前开始观察 Ajax/组件状态，等待联动后每次重新 getCmp。
- 全天单选已有真实 input.focus/click/blur 的案例；不代表所有 Ext radio 都能直接套用。
- 已选中时避免重复点击；同值重选只有明确验证需要时才执行一次。
- 使用表单所在 frame 自己的 Ext，不混用顶层 Ext。读 store 的完整候选后区分显示文本与 value，双语标签不能只按中文全等猜测为空。
- 日期 DOM rawValue 与 getValue 一致只证明组件接受了值，不证明 select/blur、业务计算或提交参数全部正确；记录实际走 DOM 输入还是组件 setValue。排班提示和天数为零需独立诊断，不自动归因于输入路径或日期跨度。

## Angular / NG-ZORRO

- 线索：nz-*、ng-* 表单状态、Angular 隔离属性；`.ant-*` 不是 React 的充分证据。
- ng.probe/DebugElement 仅在部分构建可用，生产环境缺失时停止相关能力，不绕过限制。
- `ng-reflect-name` 与真实 name 不同。调试属性可能缺失、截断或滞后，不可直接生成 `[name=...]`。
- 同名控件可能同时存在于表格和明细详情，限定当前区域和业务行，不双写。
- 数字组件可能先解析输入，再在 blur 时提交。历史验证过 onModelChange(String(value)) + onBlur，但这是版本相关能力，必须检测并重新验证。
- dirty/invalid 可能反映旧值，必须回读目标值、组件模型和行数据；不采用“目标减一再点击加一”的绕行。
- 自动补全的最近使用/关键字匹配分组可能同名；按业务身份及分组消歧，不按 DOM 文本盲目去重。

## 按控件类型选择验证方式

| 控件 | 最小验证 | 常见陷阱 |
| --- | --- | --- |
| 普通文本/textarea | 正常输入、失焦、重渲染后回读 | DOM 改了但框架 model 没改 |
| 数字 | 解析、提交、精度/范围、组件与行模型回读 | 显示新值，模型仍旧值 |
| 普通下拉 | 展开、真实可用选项、唯一选择、回读 value | 模糊匹配或取第一项 |
| 可搜索下拉 | 搜索事件、加载结束、匹配与身份确认 | 过早把空状态当无结果 |
| 业务自动补全 | 查询触发、分组、记录编码及关联字段 | 把显示名称当业务 ID |
| lookup 查询弹窗 | 正确入口、查询、选择、确认、主表回填 | 绕过回调直接写文本 |
| 树 | 当前节点自有标题、编号/路径、选择后确认 | 读到后代标题、同名节点选错 |
| 日历/时间 | 正常日历入口或已验证解析、本地日期 | readonly 不一定代表业务不可选；UTC 偏移 |
| 单选/复选 | 组归属、实际值、可用性、真实点击 | 动态 ID、重复点击触发二次业务 |
| 明细新增/切行 | 操作前集合、单次动作、差集、行绑定 | 重复新增、位置当身份、切行后写错 |

## 候选选择底线

先完整读取允许范围内的候选，再按真实编码或唯一语义匹配。诊断输出可以截断，匹配过程不能因为日志只显示前 5 项就只匹配前 5 项。无法唯一确认则追问或转人工，不把测试授权推广成默认规则。
