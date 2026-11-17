# 角色称呼与别名核对

![推广图](assets/promo-1600x900.png)

把小说定稿前最容易漏掉的人名、别名和对话称呼，变成带章节锚点的可复核清单：保留正确称呼，指出错称与歧义，并逐处给出安全建议。它不会改写对白、设计角色或推断剧情关系。

## 输入与结果

输入最多 30 个角色的实名/别名表、最多 100 条“说话人 → 称呼 → 对象”的已批准规则，以及带章节锚点的正文。结果包含姓名变体归属表、错称或歧义的精确位置、逐处替换建议；别名归属或说话对象缺失时明确标为“待确认”。同名人物绝不合并，也不会建议全局替换。

## 安装

```bash
npx skills add xxjrq/novel-name-address-check-cn
```

## 使用

将角色表、批准称呼规则和正文一起发给 Skill，按 `SKILL.md` 的输入结构提供即可。可直接复制 [成功样例](fixtures/success.md) 或 [缺料样例](fixtures/failure.md) 作为预期交付参考。

## 本地验证

```bash
python3 scripts/self_test.py
```

该命令只使用本仓库的脚本与 fixtures，验证已批准的“祖母→小岚→周岚”称呼被保留；祖母对周蓝使用“小岚”时不会猜测替换称呼；错误拼名“周篮”逐处建议为“周岚”；以及未归属的“老周”被标待确认。

## 来源与许可

业务用途参考了 [story-skills 的 character-management](https://github.com/danjdewhurst/story-skills/blob/main/skills/character-management/SKILL.md)，本仓库说明、示例和实现均为原创，未复制其正文或源码。详见 [LICENSE](LICENSE)。
