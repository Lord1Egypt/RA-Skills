# Demo Company 实例（演示种子）

`instance.yaml` 是公开文本，可直接随 SkillHub 包上传。

`ops.db` 是 SQLite 二进制数据库文件，**SkillHub 平台禁止上传二进制文件**，已从 SkillHub 发布包中移除，统一托管在 user-level 资源目录：

    ~/.workbuddy/skills/ontology-agent-assets/demo_company/ops.db

## 为什么不需要 ops.db 也能 onboarding？

- 真实运行时数据存于 `company-data/<公司>/ops.db`（与 `instance.yaml` 同目录），不依赖本目录的 demo 数据库。
- 新用户 onboarding 时会通过 `scripts/ops_db.py` 自动生成自己公司的 ops.db（空表 + 4 张核心表 schema）。
- `examples/demo_company/` 是给"想参考怎么填自己公司实例"的用户看 yaml 结构用的，db 不关键。

## 本地恢复 demo db

```bash
cp ~/.workbuddy/skills/ontology-agent-assets/demo_company/ops.db \
   <技能包路径>/examples/demo_company/ops.db
```

之后用 sqlite3 / DB Browser 打开浏览即可，作为演示种子使用。
