# 关键操作（全局）

点击前判断是否 **critical**；命中则 **`AskQuestion` 或用户文字确认** 后再执行（无 `AskQuestion` 则停顿要确认）。平台 **`critical.md`** 优先于本列表。

## 关键词（不区分大小写）

**中文**：发布、发帖、提交、确认、确定、删除、移除、支付、付款、转账、购买、下单、订阅、取关、注销、退出、登出  

**英文**：submit, send, post, publish, confirm, delete, remove, pay, buy, subscribe, unsubscribe, sign out, log out

## 结构启发

`button[type=submit]`、`input[type=submit]`、form 主提交、class/data 含 `confirm|delete|submit|purchase|pay` 等 → 视为候选。

## 处理顺序

1. 收集文本 / role / aria / 可见性  
2. 对照 recipe 预期影响  
3. **`AskQuestion` 或 teach 审阅后再确认**  
4. **未确认不点击**

## 例外与平台覆盖

- 平台 **`critical.md`** 将某交互标为**必须人工确认**（例如显式 `critical: 是` / 等价约定）时，即使**未命中**上文关键词或结构启发，也须先 **`AskQuestion` 或用户文字确认** 再点击。  
- 平台 **`critical.md`** 中的显式白名单或「非关键」声明优先于本文件的黑名单式匹配。

## 审计（可选）

触发确认后可在本地 **`health.md`** 记：时间、recipe 步骤、元素、用户结论、结果。
