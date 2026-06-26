# Google Doc 输入约定（MVP）

## 输入
- Google Doc 公开链接（只读）

## 处理
1. 抓取文档正文
2. 转为纯文本/Markdown（保留标题层级与列表）
3. 删除无关块（页眉页脚、评论、修订标记）
4. 输出给需求解析 Prompt（01_parse_requirement）

## 输出
- RequirementDraft JSON
- 同步输出 assumptions（若字段类型或动作缺失）

## 安全
- 不缓存原始链接中的敏感参数
- 不写入任何凭证到 .skill 目录
