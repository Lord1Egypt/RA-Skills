# Chat Reference

This reference is optional. It keeps useful Chinese prompt examples for skill design and evaluation.

The uploaded runtime only needs `{baseDir}/scripts/bookkeeping.py`.

## Prompt Examples

### Additional Coverage

- `列出所有账户`
- `显示所有账户余额`
- `我现在还有多少美元`
- `我的欧元钱包还有多少`
- `添加账户 Wise:USD`
- `把 Wise:USD 改成 TravelCard:EUR`
- `删除账户 银行卡:EUR`
- `添加周期性支出 每月 1 号交房租 3000 用银行卡`
- `列出所有周期性账单`
- `停用周期性账单 2`
- `重新启用周期性账单 2`
- `今天花了多少`
- `这周花了多少`
- `今年收入主要来自哪里`
- `列出 2026-03-15 的账单`
- `列出 2026-W11 的账单`
- `列出 2026 年的账单`

These examples are useful as trigger phrases or intent examples for the LLM:

- `记账 我喝奶茶用了10元`
- `记账 今天买英语教材花了88元`
- `把分类设置为日常、学习、电器`
- `添加分类 旅行`
- `显示分类`
- `显示我这个月的账单是多少`
- `显示我这个月的花销哪里更多`
- `列出我这个月的账单`
- `展示出最新的10个账单`
- `显示最近的一笔账`
- `修改一笔账 1 金额为12元，分类为学习，描述为奶茶教材`
- `按分类 学习 筛选最新的10个账单`
- `按分类 学习 筛选这个月的账单`
- `删除一笔账 3`
- `删除最近的一笔账`
- `删除分类 旅行`
