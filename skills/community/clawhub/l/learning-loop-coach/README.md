# learning-loop-coach

<img src="assets/logo.png" alt="Learning Loop Coach: book, growth and feedback loop" width="220">

一个可复用的循证学习教练skill，用于持续学习知识、专业技能和备考。技能名称与显示名称均为 `learning-loop-coach`。

## 能做什么

- 明确目标与基础，按先修关系制定可调整的学习计划。
- 生成完整Markdown课件，通过对话、示例、反例和练习教学。
- 按已学范围生成原创阶段题集，分开试卷、解析与答题记录。
- 准确批改部分交卷，区分课程完成、打卡和能力证据。
- 记录错题、主动收藏题、延迟复习和后续迁移表现。

核心方法为检索练习、分散复习、示例到独立练习、反馈及迁移。研究依据和边界见[学习科学](references/learning-science.md)。不承诺保证通过考试或快速掌握任何技能。

## 安装

仓库根目录就是skill目录，`SKILL.md` 直接位于根目录，没有额外的 `skills/learning-loop-coach/` 包装层。克隆 https://github.com/HoLauv/learning-loop-coach 到目标环境支持的skills目录，或下载源码后将文件夹命名为 `learning-loop-coach`。保留 `agents/`、`assets/`、`references/`、`scripts/` 和 `tests/` 子目录。同名已存在时先备份/比较，不覆盖。安装后重新加载技能列表。

## 使用示例

```text
使用 $learning-loop-coach 帮我系统学习Python数据处理。
我了解变量和循环，每天45分钟，希望6周后独立完成CSV清洗项目。
用Markdown课件，每5课检查一次，工具操作计入实践评价。
```

后续可以直接说“继续下一课”“完善这课的教材”“按已学范围出30题”“更新打卡”“把这些错题和收藏题加入复习集”。语言、时长、题量与工具实践是否计分都可配置。

## 可执行工具

主skill不依赖Python，也不依赖第三方study-planner。可选的单选题批改脚本使用Python 3标准库，仅读key并输出JSON，不访问网络或写学习文件。使用格式见[考核参考](references/assessment.md)。

```text
python -m unittest discover -s tests -v
```

## 数据与授权

实际学习数据保存在用户工作区，不保存在skill安装目录或此公开仓库。定时提醒需用户明确请求和当前环境可用的调度工具；仅安装skill不会自动建立提醒。未提供文件工具时不会假称已保存，未执行测试时不会假称已验证能力。

本项目为新写的工作流、模板与脚本，采用 [MIT-0](LICENSE) 许可，允许使用、修改及商业再分发，无需署名；软件按原样提供，不作担保。不分发用户成绩、私人教材或第三方skill源码；引用资料的权利仍归各自权利人。
