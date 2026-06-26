# GitHub Repo Commander

把一个 GitHub 仓库从“能看”提升到“安全、清晰、好看、易传播、可持续维护”。

English README: [README.md](./README.md)

`github-repo-commander` 是一个统一的 GitHub 仓库治理技能，不只做 README 美化，也会一起管：

- 开源前安全检查
- README 与首屏信息架构
- GitHub description / topics / homepage
- discoverability 与展示层包装
- 本地路径、密钥、敏感信息泄漏检查
- skill 元数据一致性
- 模型无关化改造建议
- awesome-list / curated-list 提交准备
- 升级时的文档同步

## 现在新增的治理要求

- 有用户可感知的功能升级时，要同步更新文档
- 如果仓库采用双语策略，要同时维护：
  - `README.md`
  - `README.zh-CN.md`
- 对明显升级，建议同步更新：
  - `CHANGELOG.md`
  - 或 release notes

## 主要文件

- [SKILL.md](./SKILL.md)
- [README.md](./README.md)
- [README.zh-CN.md](./README.zh-CN.md)
- [CHANGELOG.md](./CHANGELOG.md)
- [scripts/repo_commander_audit.py](./scripts/repo_commander_audit.py)

## 审计示例

```bash
python3 ./scripts/repo_commander_audit.py /path/to/repo
```

## 适合它接管的仓库

- OpenClaw skills
- Codex skills
- AI 工具仓库
- 准备开源的个人项目
- 想同时面向中文与国际用户展示的仓库
