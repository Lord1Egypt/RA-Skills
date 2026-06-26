# Project Facts

这里承接项目作用域的事实型记忆。

`project_facts` 是 9 个 target class 里唯一**天然多项目**的：其余 8 个都是工作区全局的（一个 MEMORY.md、一个 reusable-lessons.md），但 `project_facts` 离开项目就没意义。

因此这个 target 不应映射成单个全局文件，而应按项目拆分：

```
docs/projects/
├── project-alpha.md
├── project-beta.md
└── ...
```

每个项目一份，写该项目的特有事实、约束、架构边界。例如：

- 这个项目用 PostgreSQL 不用 MySQL
- 某项目的 API 部署地址
- 某项目的字段特殊约束
- 某项目的架构包边界

这些内容只对当前项目有效，不应误升格为全局 `reusable_lessons`。

如果一个项目已经有自己的 `README.md`、`progress.md` 或类似文档，也可以不单独建 project-facts 文件，直接写进项目自己的文档里——manifest 的 `directory` 模式只是为了承认"这些文件分散在多个项目里"，而不是强制每个项目必须有独立文件。
