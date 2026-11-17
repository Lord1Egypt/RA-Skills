# Git

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Git` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.git`
- node group: `core-nodes`

## 核心要点

- Documentation for the Git node in n8n, a workflow automation platform. Includes guidance on usage, and links to examples.

## 关键操作 / 参数线索

- **Add** a file or folder to commit. Performs a git add.
- **Add Config**: Add configuration property. Performs a git config set or add.
- **Clone** a repository: Performs a git clone.
- **Commit** files or folders to git. Performs a git commit.
- **Fetch** from remote repository. Performs a git fetch.
- **List Config**: Return current configuration. Performs a git config query.
- **Log**: Return git commit history. Performs a git log.
- **Pull** from remote repository: Performs a git pull.
- **Push** to remote repository: Performs a git push.
- **Push Tags** to remote repository: Performs a git push --tags.
- Return **Status** of current repository: Performs a git status.
- **Switch Branch:** Performs a git switch.
- Create a new **Tag**: Performs a git tag.
- **User Setup**: Set the user.

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

