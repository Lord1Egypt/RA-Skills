# 分析岗位共同交接规范

任务卡是本次客户、运行、版本、来源和输出路径的权威。先确认共同口径，完成本岗章节和六个 question_id；原始报表、完整清单及跨章节反证入口始终保留。团长已整理的清单与基线不用重新制作，必要数字仍须本人独立复算。

亲自填写卡片的 expert_analysis_template，写入 expert_analysis 文件，再执行一次 finish_command。程序只装配固定身份与格式，不生成事实、答案、通过结论或专家参与。字段、状态、证据、贡献由本人填写。错误只修本人尚未封存的分析文件；回执成功后不再调用 validation_commands 或 return_command。

卡片已提供身份、资料索引及输出格式，不为重新找字段读取脚本、测试或扫描目录。原表独立复算和必要反证仍须做；只有固定命令实际报错且卡片不足以定位时才查直接相关代码。六题保留原 question_id 和 question，不用更容易的问题替换；回答简述结论、限制并引用已登记发现/证据，不复制同一段到多个字段。

最低分析为 L2 拆解：至少一个有证据的维度及两个分段。因果判断须达到 L3，决策须达到 L4；替代解释、反证、验收、停止条件须与本次资料对应。事实、判断、假设、行动分开，同一证据登记一次，以 evidence_ids 引用。

六题逐题填 answered/unanswerable/not_applicable。无法回答和不适用都要给实际依据、影响与补数要求；仅 BLOCKED 加明确 blocked_below 可降级。缺数说明完成不代表利润或预算结论可用；空问题列表不能通过。self_check 七项如实填写，不能为了放行虚写 True。

经营数字只用真实原表，未知费用不补零；买家转化率为同口径支付买家/去重访客，GMV/访客是访客价值。ROAS 不等于利润 ROI；缺匹配退款及完整成本不输出净利润与预算承诺。需要新指标或判断依据时按 references/claim-sources-v2.md 核对来源和口径；因果问题按 references/causal-evidence-v2.md；冲突由团长按 references/challenge-round-v2.md 定向核查。

每个发现用 chapter_ids 标出对应章节，必要的跨岗依赖写在 risks/待验证假设中，说明需要哪个岗位核实什么。四岗基于同一基线并行，同级不互发消息；由团长决定是否需要一次定向核查。未经成本验证的放量建议保留待验证/待审批状态。

正式回执成功后，只向 team-lead 回传一次简短消息：岗位状态、关键例外、回执路径、真实 handoff_sha256，然后立即结束。WorkBuddy 用 SendMessage；Codex 用宿主自己的 send_message，不猜 WorkBuddy 工具。等待、恢复、真实任务 ID 绑定与封存由团长按 references/runtime-v2.md 处理；成员不操作 TaskList/TaskUpdate，不自行生成 completed 观测。

短消息由回执程序装配：WorkBuddy 原样使用 native_message_parameters；Codex 向实际父代理发送 short_message。它只整理真实回执的状态与原件入口，不替专家写结论，也不证明最终报告已完成。完整贡献、风险、缺口及必改项仍在原件，不在聊天再复制一遍。

无客户固定验收仅检查机制，使用卡片明确列出的机制六题，不产生客户经营判断；测试程序的通过不代表客户报告已完成。
