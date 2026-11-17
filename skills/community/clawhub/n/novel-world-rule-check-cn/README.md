# 世界规则冲突表

![世界规则冲突表推广图](assets/promo-1600x900.png)

## 使用

提供作者已批准的正式规则清单（编号、触发条件、代价与例外）和待审短场景；逐条核对原文证据，得到成立、冲突或无法判定的结果及需作者批准的修订选项。缺少规则字段或文本证据时先请求补充。

让章节里的能力、代价与例外经得起逐条核对。输入作者已批准的世界规则和待审片段，得到可定位原文的“成立 / 冲突 / 无法判定”表，以及必须由作者批准的修订选项；缺少规则时会请求补充，不会拿常见类型套路替代。

## 输入与结果

输入最多 20 条规则（编号、触发条件、代价、例外）与最多 10 个短场景。结果包含规则编号、对应文本、判定、依据、需作者批准的修订选项，并列出造成无法判定的缺失字段。只核对已批准设定，不创造世界观或擅自追加例外。

## 安装

```bash
npx skills add xxjrq/novel-world-rule-check-cn
```

## 可复制示例

- [成功：两次瞬移与印记代价冲突](fixtures/success.md)
- [缺料：没有正式规则时只请求补充](fixtures/failure.md)

完整输入格式与判断口径见 [SKILL.md](SKILL.md)。

## 独立自检

在仓库根目录运行 `python3 scripts/self_test.py`。不依赖网络、兄弟 Skill 或本机绝对路径。

## 来源与许可

业务用途参考 [story-skills 的 worldbuilding Skill](https://github.com/danjdewhurst/story-skills/blob/main/skills/worldbuilding/SKILL.md)；本仓库说明、流程和样例为原创。采用 [MIT-0](LICENSE)。英文说明见 [README.en.md](README.en.md)。
