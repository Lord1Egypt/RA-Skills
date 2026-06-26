gongwen-writing

撰写符合国家标准 GB/T 9704-2012 的中文公文。覆盖党政机关 15 种法定文种和企业 / 事业单位常用公文。

Functions 功能

文种判断：根据诉求匹配正确文种，规避"通知行文给不相隶属单位""报告夹带请示"等高频错误。
行文方向校验：自动判断上行 / 下行 / 平行文规则。
格式合规：GB/T 9704-2012 标准（标题三要素、六角括号〔 〕、汉字日期"〇"、仿宋_GB2312 三号、固定行距 28pt）。

Highlights 亮点

覆盖完整：15 种法定公文 + 述职报告 / 工作总结 / 会议纪要 / 调研报告。
不只是模板：解释每个文种的使用边界和禁忌。
党政 + 企业双轨：同一文种给出政府版本和企业版本对照。

Use Cases 适用场景

公务员 / 机关秘书：通知、请示、批复、函等日常公文。
事业单位 / 国企央企：党建材料、工作汇报、上报文件。
民企管理岗：述职报告、年度总结、董事会请示、会议纪要。
申论 / 公考备考：训练公文写作规范。


目录结构

gongwen-writing/
  SKILL.md                    主入口：四步定位法 + 流程
  references/
    document_types.md         15 法定文种 + 述职报告
    format_standard.md        GB/T 9704-2012 格式要素
    language_patterns.md      套语库
    common_mistakes.md        12 类常见错误
  examples/                   通知 / 请示 / 报告 / 批复 / 函 / 纪要 / 述职报告
  scripts/render_docx.py      渲染合规 docx
  requirements.txt

安装

pip install -r requirements.txt
