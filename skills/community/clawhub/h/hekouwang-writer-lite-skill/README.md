# 会勇禾口王 · 写作技能（免费版）

把话说清楚的中文写作质控 Skill：文档写作、修订、只检查不改写与去 AI 味。包含 4 个纯 Python 标准库检查器和 8 份写作参考，许可是 MIT-0。

专业版 `hekouwang-writer-skill` 另提供数字对账、证据纪律、出处卡、修订对账、长文写作和 8 套场景包；按次体检是独立的远端服务，三者不要混装或混用版本号。

## 安装

在已安装 ClawHub CLI 的环境中：

```bash
clawhub install hekouwang-writer-lite-skill
```

也可以从[公开源码仓](https://github.com/huiyonghkw/hekouwang-writer-lite-skill)获取同一份 Lite 源码。运行检查器只需要 Python 3，不需要 API key 或第三方 Python 包。

## 快速开始

安装后对宿主 Agent 直接说：

- 「根据这些素材写一份项目汇报。」
- 「修订这篇文章，保留数字、事实和我的原意，列出改动。」
- 「只检查，不要改写，也不要覆盖文件。」
- 「把这篇文章去 AI 味，保留信息密度。」

也可以直接运行检查器。把 `<skill>` 换成安装目录：

```bash
python3 <skill>/scripts/sawdust_scan.py 文档.md
python3 <skill>/scripts/sentence_load.py 文档.md
python3 <skill>/scripts/rhythm_scan.py 文档.md
python3 <skill>/scripts/doc_lint.py 文档.md
```

四个检查器都支持 stdin 和 `--json`，只报告，不修改文档：

```bash
cat 文档.md | python3 <skill>/scripts/doc_lint.py --json
```

`doc_lint` 发现硬错误时退出码为 1；其余三个检查器是 advisory，检查完成时退出码为 0。

## 三条铁律

1. **出处**：政策、数字、专名要有来源；查不到就标「暂无出处，建议核实」。
2. **模态**：「可能、约、待核实」原样保留，不把不确定改成确定。
3. **修订**：只调表达和结构，保留事实与意图；改动可列出、可回退。

完整路由和交付规则见 [`SKILL.md`](SKILL.md)，可跟跑案例见 [`examples/README.md`](examples/README.md)。

## 适用与边界

适合：方案、报告、说明、办事材料、家庭文档、邮件、汇报，以及有素材文章的结构化写作、修订和体检。

不适合：无素材营销文案、诗歌、小说、英文写作；也不承诺替代事实核查、合规审查或专业版数字对账。

本地脚本不联网、不上传正文。按次体检是另一款产品，会把正文发送到远端服务器，不能与本地的数据边界混为一谈。

## 其他产品

- [产品页与案例](https://huiyonghkw.github.io/hekouwang-writer-lite-skill/)
- 专业版：支付宝 SkillPay，11 个脚本、21 份参考、8 套场景包。
- 按次体检：腾讯 SkillHub，文档模式检查长句、锯末词、数字对账和待核实标记，文章模式另查结构节奏；只检查不改写。

## 维护与变更

- [`CHANGELOG.md`](CHANGELOG.md)：版本变更。
- [开发与维护说明](https://github.com/huiyonghkw/hekouwang-writer-lite-skill/blob/main/DEVELOPMENT.md)：构建、测试、渠道和发布规则；维护文档不随安装包分发。
- [`LICENSE`](LICENSE)：MIT-0，可用、可改、可商用、可再分发。

## 方法论来源（致谢）

本技能的规则组织、案例和检查脚本为原创实现或重写。以下来源用于说明方法出处：

- **kunlun-doc-write / doc-write**（昆仑增长）：WRITE 流程、每节核心句、边界声明。
- **universal-writer**：出处铁律、修订模式、进度卡、风险告知格式。
- **asd-ste100**（GitHub: danyuchn/asd-ste100-skill）：句法纪律、模态保留、一词一义。
- **chenlin-credible-translate**（真笔翻译）：五轴心、禁止层 P1-P3、G1-G5、机械检查思路。
- **dev-god**、**dev-expert**、**parenting-expert**、**tencent-docs**、**self-improving-agent**（SkillHub）：证据三分、三档机制、边界声明、场景路由、learnings 台账。
- **zh-humanizer**、**khazix-writer**、**李诞写作心法**、**说人话**、**Humanizer-zh / qu-ai-wei**：文章模式与去 AI 味参考。
- **ASD-STE100 Issue 9**（2025-01）：受控语言标准本身。
