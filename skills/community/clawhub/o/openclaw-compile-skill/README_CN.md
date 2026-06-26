# Compile Skill（中文说明）

Compile 可以把 inbox 文件夹里的原始 Markdown 文章编译成结构化知识文档，并把原文安全归档，保留可追溯链接和 checkpoint 审计状态。

## 普通 Markdown 优先

Obsidian 不是运行依赖。这个 Skill 操作的是普通本地 Markdown 文件夹。

你只需要把原始 `.md` 文章放进一个 inbox 文件夹，再用 OpenClaw 配置 `COMPILE_INBOX_DIR`、`COMPILE_TRANSIT_DIR`、`COMPILE_RAW_DIR`，就可以运行编译流程。

最低需要：

- 一个 inbox 文件夹：存放待编译 `.md` 原文。
- 一个 transit 文件夹：存放编译后的知识文档。
- 一个 raw-material 文件夹：归档原始文章。
- 本地 OpenClaw 运行环境和基础 shell 工具。

`COMPILE_INBOX_DIR` 必须指向已经存在的 inbox。收件箱未配置或不存在时，预检查会 fail fast，避免通用版在错误目录静默创建或扫描文件夹。

`COMPILE_TRANSIT_DIR`、`COMPILE_RAW_DIR`、`COMPILE_STATE_DIR` 可在收件箱明确配置后由流程初始化。

## 开发背景

这个 Skill 来自真实知识流水线实践：Agent 可以总结文章，但如果没有脚本护栏，结果常常难以审计、难以追溯原文，也容易偏离知识库字段规范。

Compile 的思路是：语义理解交给 Agent，脆弱操作交给确定性脚本。比如查重、frontmatter 生成、checkpoint、归档、回链和最终审计，都由脚本兜底。

设计原则：

- 自包含，可安装到 OpenClaw。
- 所有本地路径都走环境变量，方便迁移到不同 Markdown 文件夹。
- QMD 是可选召回增强，不是硬依赖。
- 结构和审计错误必须失败停下，不能靠 Agent 自行解释跳过。

## 功能

- 扫描 inbox 中未处理的 Markdown 文件。
- 修复剪藏产生的 frontmatter 脏数据。
- 按标题归一化和 source URL 查重。
- QMD 可用时检索本地历史。
- 生成标准 frontmatter。
- 引导 Agent 写出结构化编译文档。
- 归档原文和图片资源。
- 为每一步写 checkpoint。
- 完成前运行确定性审计。

## OpenClaw 配置示例

```json
{
  "skills": {
    "entries": {
      "compile": {
        "enabled": true,
        "env": {
          "OPENCLAW_VAULT": "/path/to/your/vault",
          "COMPILE_INBOX_DIR": "/path/to/your/vault/Inbox",
          "COMPILE_TRANSIT_DIR": "/path/to/your/vault/Knowledge/Transit",
          "COMPILE_RAW_DIR": "/path/to/your/vault/Knowledge/Raw",
          "COMPILE_STATE_DIR": "/path/to/your/vault/.openclaw/state"
        }
      }
    }
  }
}
```

## QMD 可选增强

不安装 QMD 也可以运行。未配置 `COMPILE_QMD_ENTRY` 时，历史检索步骤会输出 `RESULT: QMD_SKIPPED` 并继续执行。

如果安装了 QMD，可以获得更好的本地召回能力，例如查重意识、主题词复用、旧结论召回和知识库连续性。

```json
{
  "skills": {
    "entries": {
      "compile": {
        "env": {
          "COMPILE_QMD_ENTRY": "/path/to/qmd"
        }
      }
    }
  }
}
```

## 安全模型

Compile 会写文件、移动原文、归档资源，因此默认应由用户手动调用，不建议自动触发。

最终审计必须通过，才能认为一次编译完成。审计失败时，Agent 应停止、记录 blocked checkpoint、修复具体问题，然后重新运行审计。

## 作者

设计与开发：强哥
