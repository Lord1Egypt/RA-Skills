# Contributing

感谢你改进 `hekouwang-harness-check-skill`。

这个仓库只维护可移植的 Skill 编排层，不把某个项目的业务规则、Memory、媒体或私有路径硬编码进来。

## 提交前检查

- 保留 `working-tree`、`staged`、`ci` 三种模式的边界；
- 保留真实退出码，不用 `|| true`、`| head` 或固定数字制造通过；
- 行为变化至少补一个应命中的正例和一个应放过的反例；
- 同步更新 `SKILL.md`、README、检查矩阵、流程图和 `CHANGELOG.md`；
- 运行 GitHub Actions 的包级验证，并在一个真实 Harness 仓库中运行完整 `verify.sh`；
- 清楚写出自动化证据、宿主烟测和人工验收分别证明了什么。

## Pull Request

Pull Request 请说明：

1. 变更解决的问题；
2. 受影响的验证模式和宿主边界；
3. 正例、反例和完整命令输出；
4. 尚未覆盖的真实宿主、外部副作用或人工验收。
