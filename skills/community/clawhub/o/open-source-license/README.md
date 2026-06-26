# open-source-license

一个用于开源许可证选择、对比、合规检查与 LICENSE/Header 起草的 skill。

> 本 skill 基于 `skala-io/legal-skills` 的 [`open-source-license`](https://github.com/skala-io/legal-skills/tree/main/skills/open-source-license)，增加了对木兰宽松许可证第 2 版（Mulan PSL v2）的支持。

## 这个 skill 能做什么

- 为新项目推荐合适的开源许可证
- 对比 MIT、Apache-2.0、GPL、LGPL、AGPL、BSD、MPL 等许可证差异
- 检查项目中的许可证兼容性与合规风险
- 生成 `LICENSE`、`NOTICE` 或源文件头部声明
- 解释木兰宽松许可证 / Mulan PSL v2，并与 MIT、Apache-2.0 做对比

## 目录结构

```text
open-source-license/
├── SKILL.md
├── README.md
└── references/
    ├── compliance/
    ├── licenses/
    ├── selection/
    ├── templates/
    └── mulan-psl-v2.md
```

## 如何安装

把 `skills/open-source-license/` 目录复制到你的 skills 目录中即可。

常见放置方式：

- 项目级：`.claude/skills/open-source-license/`
- 全局：`~/.claude/skills/open-source-license/`
- 其他支持 skills 的 AI Agent：放到对应 agent 约定的 skills 目录

如果你是从当前仓库使用，目录已经位于：

```text
skills/open-source-license/
```

## 如何触发

这个 skill 会在用户询问以下问题时自动更容易触发：

- “我这个项目应该选 MIT 还是 Apache-2.0？”
- “GPL 代码能不能放进商业闭源产品？”
- “帮我检查仓库里的第三方许可证是否冲突”
- “帮我生成 LICENSE 文件和源文件头”
- “木兰宽松许可证和 Apache-2.0 有什么区别？”

## 推荐提问方式

为了得到更准确的结果，建议在问题里尽量带上这些信息：

- 项目类型：库、应用、SaaS、模型或插件
- 目标：最大化采用、保留开源、商业友好、专利保护
- 约束：是否要兼容已有依赖，是否面向企业分发
- 场景：是否涉及中国本土开源生态或需要中文许可证文本

## 使用示例

### 1. 许可证选择

```text
我在做一个开源 SDK，希望商业公司也能放心使用，但我又想保留明确的专利授权，应该选什么许可证？
```

### 2. 许可证对比

```text
请比较 MIT、Apache-2.0 和木兰宽松许可证 v2，重点说清楚专利授权、保留声明和商业使用差异。
```

### 3. 合规检查

```text
帮我 review 一下这个仓库的许可证风险，看看 GPL 和 Apache-2.0 依赖混用会不会有问题。
```

### 4. 文件生成

```text
请基于 Apache-2.0 帮我生成一个 LICENSE 文件，并给出适合 Go 文件头部的版权声明模板。
```

### 5. 木兰宽松许可证

```text
我想把项目发布成木兰宽松许可证第 2 版，请告诉我它的主要义务，并给我 LICENSE 文件和源文件头模板。
```

## 输出内容通常包括

- 推荐结论
- 适用原因
- 主要义务
- 兼容性或分发风险
- 下一步建议

如果问题涉及生成文件，还会进一步给出：

- `LICENSE` 文本
- `NOTICE` 文本
- 对应语言的源文件头模板

## 木兰宽松许可证支持

这个 skill 在保留上游能力的基础上，额外内置了木兰宽松许可证第 2 版参考文件：

- [mulan-psl-v2.md](./references/mulan-psl-v2.md)

其中包含：

- 木兰宽松许可证的关键条款要点
- 官方适用说明
- 官方 header 文本
- 中英文 canonical text

适合这些场景：

- 你希望使用中国本土开源许可证
- 你需要中英文双语许可证文本
- 你希望获得明确的专利授权与专利反制条款

## 使用时的注意事项

- 这个 skill 提供的是信息性与工程化辅助，不是正式法律意见
- 遇到双重许可、并购、专利争议、企业采购审查等复杂情形，仍应咨询律师
- 标准许可证正文应使用官方或权威文本，不应凭记忆改写

## 相关文件

- [SKILL.md](./SKILL.md)
- [comparison-matrix.md](./references/selection/comparison-matrix.md)
- [decision-tree.md](./references/selection/decision-tree.md)
- [mulan-psl-v2.md](./references/mulan-psl-v2.md)
