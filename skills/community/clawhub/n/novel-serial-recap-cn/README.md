# 连载前情摘要

![连载前情摘要](assets/promo-1600x900.png)

用于中文连载小说：输入上几章的正文或摘要，以及下一章目标，生成一段给读者看的前情提要和一份给作者看的续写记忆卡。保留人物状态与未解伏笔，不续写剧情。

## 立即使用

让 Agent 使用 `$novel-serial-recap-cn`，读取 [成功输入](fixtures/success-input.md)，输出 120–250 字前情提要与作者记忆卡。也可以直接粘贴你的章节材料和下一章目标。

作者记忆卡包含：已知事实、当前人物状态、未解伏笔、衔接建议和待确认信息。建议会明确标注，不能变成已有剧情。

缺少章节材料或下一章目标时，先列出缺项；参见 [缺资料样例](fixtures/failure-missing-goal.md)。本 Skill 是纯 Markdown 工作流，无需浏览器或额外服务。

## 安装

```bash
npx skills add xxjrq/novel-serial-recap-cn
```

也可以把本仓库目录复制到 Agent 的 Skills 目录。

## 自检

```bash
bash scripts/self-test.sh
```

这是结构与样例检查；实际生成由支持 Skill 的 Agent 完成。

## 来源与许可

原创工作流，采用 [MIT-0](LICENSE)。来源参考记录见 [sources.md](sources.md)；仅参考用途，不复制外部实现。

## 完整输出示例

查看 [成功输出](fixtures/forward-success.md) 和 [缺资料响应](fixtures/forward-failure.md)，对照上述输入样例了解实际交付内容。
