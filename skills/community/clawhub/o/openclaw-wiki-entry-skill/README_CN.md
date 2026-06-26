# Wiki Entry Skill（中文说明）

Wiki Entry 可以把已经编译好的 transit Markdown 文档融合进领域 Wiki 页面，同步来源表、演进记录、中心索引和文档状态，并在完成前做一致性审计。

## 普通 Markdown 优先

Obsidian 不是运行依赖。这个 Skill 操作的是普通本地 Markdown 文件夹。

如果你已经有编译后的 `.md` 文档和一组主题 Wiki `.md` 页面，就可以用这个 Skill 把内容入库到对应 Wiki，并同步 `_INDEX.md`。

最低需要：

- 一个 transit 文件夹：存放待入库编译文档。
- 一个 domain wiki 文件夹：存放主题 Wiki 页面。
- 一个 graduated 文件夹：存放已完成入库的源文档。
- 一个中心索引文件，例如 `_INDEX.md`。
- 本地 OpenClaw 运行环境和基础 shell 工具。

路径完全可配置。正式运行时必须通过 OpenClaw 配置、`OPENCLAW_VAULT` 或 `--vault` 显式指定 vault；预检查不会把当前工作目录隐式当作 vault。

如果要从空目录开始，先显式初始化：

```bash
bash scripts/wiki_entry_precheck.sh --vault /path/to/your/vault --init
```

正式 workflow 运行时不要带 `--init`，这样路径缺失或配置错误会 fail fast，而不是在错误目录创建一个假 vault。

## 开发背景

这个 Skill 来自真实 Wiki 入库实践：Agent 可以写出有价值的 Wiki 内容，但没有脚本护栏时，来源表、`sources_count`、中心索引、状态字段和双向链接很容易漂移。

Wiki Entry 的思路是：语义融合交给 Agent，脆弱的状态和元数据操作交给确定性脚本。比如状态切换、分段写入、来源表回写、索引更新、反向链接、移动已入库文档和最终审计，都由脚本兜底。

设计原则：

- 自包含，可安装到 OpenClaw。
- 所有本地路径都走环境变量，方便迁移到不同 Markdown 文件夹。
- QMD 是可选召回增强，不是硬依赖。
- 元数据和审计错误必须失败停下，不能靠 Agent 自行解释跳过。

## 功能

- 扫描 transit 中 `waiting` 和 `graduating` 状态的文档。
- `status: waiting` 是唯一待入库触发条件；`graduated_to + pending_topics` 只决定优先级，不决定是否入库。
- 通用版支持任意用户路径，但运行前必须显式配置 vault；预检查不会把当前目录隐式当作 vault。
- 强制执行 A/B/拒绝路径决策。
- QMD 可用时检索历史决策、主题演进和矛盾记录。
- 入库前把文档标记为 `graduating`。
- 通过脚本分段写入 Wiki。
- 幂等写入来源行和演进行。
- 根据来源表实际行数重算 `sources_count`。
- 同步中心索引 `_INDEX.md`。
- 同步相关主题反向链接。
- 移动完全入库的 graduated 文档。
- 最终审计来源表、frontmatter、索引和 wikilink 一致性。

## OpenClaw 配置示例

```json
{
  "skills": {
    "entries": {
      "wiki-entry": {
        "enabled": true,
        "env": {
          "OPENCLAW_VAULT": "/path/to/your/vault",
          "WIKI_ENTRY_TRANSIT_DIR": "/path/to/your/vault/Knowledge/Transit",
          "WIKI_ENTRY_DOMAIN_DIR": "/path/to/your/vault/Knowledge/Domain",
          "WIKI_ENTRY_GRADUATED_DIR": "/path/to/your/vault/Knowledge/Graduated",
          "WIKI_ENTRY_INDEX_FILE": "/path/to/your/vault/Knowledge/_INDEX.md",
          "WIKI_ENTRY_STATE_DIR": "/path/to/your/vault/.openclaw/state"
        }
      }
    }
  }
}
```

## QMD 可选增强

不安装 QMD 也可以运行。未配置 `WIKI_ENTRY_QMD_ENTRY` 时，历史检索步骤会输出 `RESULT: QMD_SKIPPED` 并继续执行。

如果安装了 QMD，可以获得更好的本地召回能力，例如历史入库决策、主题演进、矛盾检查和知识库连续性。

```json
{
  "skills": {
    "entries": {
      "wiki-entry": {
        "env": {
          "WIKI_ENTRY_QMD_ENTRY": "/path/to/qmd"
        }
      }
    }
  }
}
```

## 安全模型

Wiki Entry 会写 Wiki、更新索引、修改文档状态、移动文件，因此默认应由用户手动调用，不建议自动触发。

最终审计必须通过，才能认为一次入库完成。审计失败时，Agent 应停止、记录 blocked checkpoint、修复具体问题，然后重新运行审计。

## 作者

设计与开发：强哥
