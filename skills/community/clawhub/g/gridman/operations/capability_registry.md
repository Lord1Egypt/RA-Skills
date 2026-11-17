# 抽象能力注册表

> 定位：Workflow 能力 ID 的单一事实源，定义“需要什么能力”，不绑定具体工具、MCP Server 或 CLI。
>
> 注册表版本：1.1.0

## 使用规则

1. Workflow 的 `required_capabilities` 与 `optional_capabilities` 只允许使用下表 ID，必须精确匹配。
2. `required_capabilities` 表示缺失后无法真实完成核心步骤；`optional_capabilities` 只增强效率或呈现。
3. 一个业务动作需要多种能力时分别声明，不创造“读取并计算并导出”式复合名称。
4. 运行时按“发现 → 验证 → 选择 → 授权 → 执行 → 业务验收”寻找宿主原生能力、宿主 MCP 或本机 CLI 实现。能力表只说明“需要什么能力”，不预设由哪个工具实现。
5. 工具调用成功不代表能力验收通过；必须核对输入范围、输出完整性和业务控制数。
6. 需要外部上传、写入、覆盖、删除或批量修改时，即使能力可用也必须遵守授权规则；执行端存在授权闸时不得绕过。
7. 新增能力 ID 前先确认现有 ID 组合不能表达；新增后运行 `python scripts/validate_release.py`。
8. 能力 ID 描述"需要对什么对象做什么"，不描述"用什么手段做"。同一能力可由不同手段实现，是否满足按下方「实现关系」判断，不按 ID 字面匹配。

## 实现关系

一个 required 能力被判定为"当前可用"，可以由它自身的直接实现满足，也可以由下表允许的替代手段满足。替代不改变能力语义，也不降低该 ID 的最低验证要求。

| 目标能力 | 允许的替代实现 | 附加验证要求 |
|---|---|---|
| `spreadsheet.read` / `spreadsheet.transform` / `spreadsheet.calculate` / `spreadsheet.write` | `script.execute`（如宿主终端运行 Python/PowerShell 读写表格） | 记录所用运行时与库；读取后核对行数、表头与控制总数；写入默认新文件，不覆盖源文件 |
| `statistics.calculate` | `script.execute` | 记录方法、参数、随机种子与缺失值处理，结果可复算 |
| `sampling.select` | `script.execute` | 固化总体、种子/起点与样本唯一标识，可复现 |
| `visualization.generate` / `diagram.generate` | `script.execute`，或以文本/表格形式呈现同等信息 | 图表或替代呈现必须可追溯到数据范围与计算口径 |
| `ledger.link` / `evidence.index` | `script.execute` + `spreadsheet.*` 组合 | 验证主键、期间、未匹配项与金额覆盖率 |

判定纪律：

- 替代实现满足时，不得因"目标 ID 无专用工具"而整体降级；应在方法说明中写明实际实现手段。
- 替代实现不可用、或附加验证要求无法满足时，按缺失该 required 能力处理，走诚实降级。
- 本表只解决"能力是否可用"的判定，不解决"该不该执行"——授权与副作用规则仍按第 6 条。
- `document.extract` / `document.generate` / `web.*` / `browser.operate` / `filesystem.*` 不在替代范围内，必须有对应实现。

## 注册能力

| 能力 ID | 能力契约 | 最低验证要求 |
|---|---|---|
| `web.search` | 搜索公开网页或官方入口并返回候选来源 | 记录查询范围；不得把搜索摘要当正式原文 |
| `web.fetch` | 获取指定网页的可核对正文 | 核对最终 URL、来源主体、发布日期与正文完整性 |
| `browser.operate` | 在浏览器中执行导航、填写或交互 | 验证目标页面；产生副作用前取得确认 |
| `spreadsheet.read` | 读取表格工作簿、工作表、字段、公式或单元格值 | 核对文件、工作表、表头、行数和控制总数 |
| `spreadsheet.transform` | 清洗、映射、合并、拆分或标准化表格数据 | 保留来源行标识；核对转换前后记录数和金额 |
| `spreadsheet.calculate` | 执行勾稽、汇总、重算、账龄、比率等确定性计算 | 固化口径；用控制数、交叉加总或独立重算验收 |
| `spreadsheet.write` | 生成或更新表格型交付物 | 写入前核对目标；输出后回读关键单元格与总数 |
| `document.extract` | 从 PDF、图片或办公文档提取文本与表格 | 核对页数、缺页、OCR 质量和关键字段 |
| `document.generate` | 生成 Markdown、Word、PDF 或其他文档型交付物 | 核对章节、引用、版本与输出路径 |
| `filesystem.read` | 读取本地目录或文件 | 验证路径、权限、编码和读取范围 |
| `filesystem.write` | 创建、修改、移动或删除本地文件 | 副作用前按规则确认；完成后验证目标状态 |
| `script.execute` | 执行可复现的本机脚本或计算程序 | 验证脚本来源、参数、退出码、日志和输出 |
| `statistics.calculate` | 执行描述统计、异常检测或统计评价 | 记录方法、总体、参数、缺失值处理和可复算结果 |
| `sampling.select` | 进行随机、系统、分层或货币单元等样本选择 | 固化总体、种子/起点、参数和样本唯一标识 |
| `visualization.generate` | 生成图表或关系可视化 | 图表必须可追溯到数据范围和计算口径 |
| `confirmation.manage` | 管理函证或其他外部确认的清单、状态和差异 | 不代替注册会计师控制；核对对象、地址、状态和回函证据 |
| `ledger.link` | 关联 TB、总账、明细账、序时账或业务台账 | 验证主键、期间、借贷方向、未匹配项和金额覆盖率 |
| `evidence.index` | 建立底稿、证据、风险、认定与程序的索引关系 | 唯一编号；检查断链、重复和孤立证据 |
| `diagram.generate` | 生成流程图、控制矩阵或结构图 | 核对节点、方向、责任人、控制点与文字说明 |
| `log.analyze` | 读取并分析系统日志、操作轨迹或审计日志 | 核对时间范围、时区、完整性、身份字段和异常规则 |

## 变更纪律

- 能力 ID 一经进入已发布 Workflow，不因工具更名而改名。
- 语义确需拆分或废弃时，先新增替代 ID、迁移全部 Workflow、通过发布校验，再移除旧 ID。
- 具体工具示例只能写在执行说明中，不能进入能力 ID。

---

> 末次更新：2026-07-25 [实测修正] 真实数据实跑发现：`spreadsheet.*` / `statistics.*` 等 required 能力实际全部由宿主终端运行 Python 实现（即 `script.execute`），按字面 ID 匹配应整体降级、实际却已跑通。根因是 ID 混用了「操作对象」与「执行手段」两个维度。新增使用规则第 8 条与「实现关系」章节，明确替代实现的判定与附加验证要求；注册表版本 1.0.0 → 1.1.0
