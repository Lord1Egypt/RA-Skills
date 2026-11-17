# hekouwang-doctor-suite · 体检器三件套

> 竞品多是单点；这套把「项目配置 → 技能包 → 本机环境」串成一条验收链。

```
hekouwang-doctor-suite（概念）
├── md-doctor      → AGENTS.md / CLAUDE.md（运行时配置）
├── skill-doctor   → SKILL.md（Agent 技能包）
└── env-doctor     → 磁盘 / 版本管理器 / AI 宿主目录
```

## 一键跑

```bash
bash scripts/run-all-doctors.sh /path/to/your-project
```

（脚本在 `hekouwang-claude-md-doctor-skill`；`skill-doctor` / `env-doctor` 仓内各有一份相同副本。）

## 建议顺序

1. **md-doctor** — 根配置是否「路由器」而非「图书馆」
2. **skill-doctor** — `.agents/skills/` 下各 skill 是否按需加载
3. **env-doctor** — 本机是否留着已换掉的 nvm / 膨胀的 AI 缓存

## Skill 多入口盘点

三件套按项目目录逐个检查 Skill；需要检查一个宿主根目录下的隐藏入口、软链和重名时，
直接运行 skill-doctor 的扫描模式：

    python3 check.py --scan --direct /path/to/skill-root --json

direct 模式只看宿主根目录下一层；默认不加 direct 时递归扫描，并跳过测试夹具和构建目录。
扫描结果按真实 SKILL.md 去重，并将断开的软链、遍历错误、重复 name 和任一子 Skill
的 FAIL 汇总到 gate。单个 Skill 的 score/grade 不替代 gate。

## 失败口径

三件套必须 fail-closed：doctor 进程崩溃、JSON 解析失败、env-doctor 非零退出，都算套件失败。
外部软链 Skill 可以继续输出诊断，但是否阻断宿主仓库由调用方明确决定；本仓包装器默认外部
引用只提示，断开的软链仍阻断。

## 免费 vs 付费

| | 免费（开源） | 付费增值 |
|---|---|---|
| 机检 | `check.py` / `scan.sh` 文本报告 + JSON | 品牌可视化报告卡（评分弧 + 等级带） |
| CI | 退出码卡关 | — |
| 联系 | GitHub Issue / PR | ClawHub **@huiyonghkw** |
