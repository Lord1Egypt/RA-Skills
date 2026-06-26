# trace/origin — 角色原始素材

本目录存放 **Trace（寻迹）** 搜集的**原始材料**。生成 SoulPod 时请优先使用 `forge.py create --from-origin`。

## 目录规范

```
trace/origin/
└── <游戏或作品名>/
    └── <角色名>/
        ├── 01_基本信息.md
        ├── 02_人物形象.md
        └── assets/
            ├── images/    # 可选，默认不提交 Git
            └── audio/       # 可选，默认不提交 Git
```

- `<游戏>` 与 `profile.json` 的 `source` 一致。
- `<角色名>` 与 `profile.json` 的 `name` 一致。

## 推荐命令（自动读 origin）

```bash
cd trace/scripts

# 合并该目录下所有 *.md，同步 assets，写入 trace/output/<角色名>/
python forge.py create --from-origin 恋与深空/秦彻

# 仅角色名（要求 origin 下唯一匹配）
python forge.py create --from-origin 秦彻 --character "秦彻"

python forge.py install 秦彻
```

`forge` 会：

1. 按文件名排序合并 `*.md` → `_merged_source.md`（本地，已 gitignore）
2. 分析并生成 `trace/output/<角色名>/`
3. 将 `origin/.../assets/images|audio` **复制**到 `output/.../assets/`（与 origin 保持一致）

仍可用 `create --source <单个.md> --character "名字"`（不经过 origin 目录结构）。

## 三线 vs 双线

| 类型 | 维护目录 |
|------|----------|
| **新角色** | `origin/` → `output/` → `personas/`（三线） |
| **遗留内置**（夏以昼、叶修、秦彻、Lucy） | 仅 `output/` + `personas/`（双线，不补齐 origin） |

## Git

- 提交：`*.md`
- 不提交：`assets/images/`、`assets/audio/`、`_merged_source.md`（见 `trace/.gitignore`）

详见仓库根目录 `CLAUDE.md`。
