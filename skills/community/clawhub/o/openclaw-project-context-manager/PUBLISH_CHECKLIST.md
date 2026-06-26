# 发布文件清单（建议）

## 建议保留

### 核心文件
- `SKILL.md`
- `README.md`
- `scripts/init_project.py`
- `templates/` 目录全部内容

### 补充文档
- `docs/初始化与测试说明.md`
- `docs/项目注册表维护说明.md`
- `docs/发布说明与用户使用指南.md`

## 不建议作为主发布内容

这些更偏内部研发资料：

- `00_恢复入口.md`
- `00_文档总索引与当前进度.md`
- `01_skill定位与使用机制说明.md`
- `02_项目创建与接管机制说明.md`
- `99_关键决策记录.md`
- `checkpoints/`
- `session-backups/`

## 推荐最终发布目录结构

```text
project-context-manager/
├─ SKILL.md
├─ README.md
├─ scripts/
│  └─ init_project.py
├─ templates/
│  ├─ PROJECT_SYSTEM.md
│  ├─ 00_恢复入口.md
│  ├─ 00_文档总索引与当前进度.md
│  ├─ 01_项目会话与恢复机制说明.md
│  ├─ 99_关键决策记录.md
│  ├─ checkpoints/README.md
│  └─ session-backups/README.md
└─ docs/
   ├─ 初始化与测试说明.md
   ├─ 项目注册表维护说明.md
   └─ 发布说明与用户使用指南.md
```

## 发布前检查

- [ ] 没有个人真实路径
- [ ] 没有个人真实项目名
- [ ] 没有个人账号/用户名
- [ ] README 可独立读懂
- [ ] SKILL.md 与 README 描述一致
- [ ] 模板完整
- [ ] 脚本可运行
- [ ] docs 中的示例为通用示例
