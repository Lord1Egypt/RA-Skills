# 工具可用性处理指南

本文档是 **执行期故障处理指南**。

当 skill 在自动执行命令过程中遇到工具缺失、运行时未安装、编译器缺失、权限不足、环境未配置、版本不兼容等问题时，必须主动读取并遵循本指南，而不是直接中断流程，也不是把排障责任全部丢给用户。

只有在以下情况成立时，才允许退化为让用户手动执行：

- 当前环境无法直接执行命令
- 没有足够权限自动安装或自动配置
- 自动安装/自动配置已经明确失败
- 目标操作必须由用户本人确认或完成

---

## 一、执行原则

- 先确认工具是否真实可用，不要凭空假设
- 能自动安装就自动安装，能自动配置就自动配置
- 不能自动完成时，再切换手动模式
- 切换手动模式时，必须给用户完整命令、预期输出和回传要求
- 不要只说“请你自己安装一下”，要尽可能把步骤具体化

---

## 二、工具可用性检查逻辑

遇到任何工具依赖问题时，按以下顺序处理：

```
第一步：确认工具是否存在
  ↓ 存在 → 直接使用
  ↓ 不存在 → 第二步

第二步：确认能否自动安装
  ↓ 能（有包管理器 + 权限）→ 自动安装
  ↓ 不能 → 第三步

第三步：切换手动模式
  → 生成命令 → 提供给用户 → 等待用户执行 → 确认结果
```

---

## 三、bash 工具不可用

### 判断方式

模型在尝试执行 bash 命令时收到以下任意错误即可判断：
- `tool not found: bash`
- `exec tool is not available`
- `没有 bash 执行权限`
- 工具调用静默失败，无任何输出

### 处理方式

优先判断当前环境是否有其他可用的命令执行渠道。

如果没有可替代执行渠道，再切换手动模式。

所有原本要自动执行的命令，改为以下流程：

1. 向用户清晰说明"我没有直接执行命令的权限"
2. 把完整命令提供给用户，格式如下：

```
请在你的终端（macOS/Linux 用 Terminal，Windows 用 PowerShell 或 CMD）执行：

<完整命令>

执行完后，把输出结果粘贴给我。
```

3. 等待用户粘贴结果，读取结果继续下一步

### 注意事项
- 不要反复尝试执行同一命令，一次失败就切换手动模式
- 不要因为没有 bash 就放弃整个流程——手动模式同样能完成任务
- 提供命令时，把所有占位符（如 `<skill-name>`）替换成实际值，不要让用户自己猜

---

## 四、Node.js 未安装

### 判断方式

执行 `node --version` 后输出 `command not found` 或类似错误。

### 处理原则

如果当前环境允许自动执行安装命令，并且具备相应权限，应优先自动安装。

如果当前环境不允许自动安装，或安装需要用户确认权限，再切换为手动模式并把命令明确提供给用户。

### 各平台安装方法

| 平台 | 推荐方式 | 命令 |
|------|---------|------|
| macOS | Homebrew | `brew install node` |
| macOS (无 Homebrew) | 官网安装包 | 访问 https://nodejs.org → 下载 LTS |
| Ubuntu / Debian | apt | `sudo apt update && sudo apt install nodejs npm` |
| CentOS / RHEL | yum | `sudo yum install nodejs npm` |
| Windows | 官网安装包 | 访问 https://nodejs.org → 下载 LTS → 双击安装 |
| Windows (有 winget) | winget | `winget install OpenJS.NodeJS.LTS` |
| 任意平台 | nvm（版本管理器） | https://github.com/nvm-sh/nvm |

### 安装后验证

```bash
node --version   # 应输出 v16.x.x 或更高
npm --version    # 确认 npm 也已安装
```

### 如果用户无法安装（无权限等情况）

提供不依赖 Node.js 的替代方案：
- 用 Python 脚本替代 JS 脚本（Python 在大多数系统上预装）
- 把 Node.js 脚本的逻辑转化为手动 bash 命令序列提供给用户

---

## 五、Python 未安装（当 skill 使用 Python 脚本时）

### 判断方式

执行 `python3 --version` 后输出 `command not found`。

### 各平台安装方法

| 平台 | 推荐方式 | 命令 |
|------|---------|------|
| macOS | 官网安装包 / Homebrew | `brew install python3` 或 https://python.org |
| Ubuntu / Debian | apt | `sudo apt update && sudo apt install python3 python3-pip` |
| Windows | 官网安装包 | https://python.org → 下载 → 安装时勾选"Add to PATH" |

### 安装后验证

```bash
python3 --version   # 应输出 Python 3.x.x
pip3 --version      # 确认 pip 也已安装
```

---

## 六、查找工具官方安装方法的途径

当遇到本文档未列出的工具时，按以下顺序查找：

### 方法一：官方文档（最可靠）
每个知名工具都有官方安装文档，URL 格式通常为：
- `https://<tool-name>.dev/docs/installation`
- `https://<tool-name>.io/getting-started`
- `https://docs.<tool-name>.com`

### 方法二：包管理器搜索

| 包管理器 | 平台 | 搜索命令 |
|---------|------|---------|
| `brew` | macOS | `brew search <tool-name>` |
| `apt` | Ubuntu/Debian | `apt search <tool-name>` |
| `npm` | Node.js 工具 | `npm search <tool-name>` |
| `pip` | Python 工具 | `pip search <tool-name>` 或查 https://pypi.org |
| `winget` | Windows | `winget search <tool-name>` |

### 方法三：GitHub 仓库
大多数开源工具在 GitHub 上有 README，README 第一节通常就是安装说明：
`https://github.com/<org>/<tool-name>`

### 方法四：web_search
直接搜索 `<tool-name> installation guide <platform>` 获取最新安装方式。

---

## 七、工具安装失败时的通用降级策略

当工具无论如何都无法安装时：

| 原本需要的工具 | 降级方案 |
|-------------|---------|
| Node.js 脚本 | 把脚本逻辑转化为 Python 脚本（Python 通常预装）|
| Python 脚本 | 把逻辑转化为纯 bash 命令序列 |
| bash | 把所有命令整理成清单，由用户手动在终端执行 |
| 任意工具 | 把操作步骤转化为用户手动完成的指引文档 |

**核心原则：工具不可用不等于任务无法完成。总有一条路径可以让用户手动完成同样的结果。**

---

## 八、向用户提供手动命令时的格式规范

提供给用户执行的命令必须：

1. **无占位符** — 所有 `<变量>` 替换为实际值
2. **有编号** — 多条命令按顺序编号，清楚标明先后
3. **有说明** — 每条命令前一行注释说明它做什么
4. **有预期输出** — 告诉用户成功时应该看到什么
5. **有粘贴请求** — 明确请用户把最后一步的输出粘贴回来

示例格式：

```
请在终端依次执行以下命令：

# 第 1 步：创建 skill 目录
mkdir -p ~/.openclaw/skills/my-skill/scripts
（成功时没有任何输出，无报错即为正常）

# 第 2 步：确认目录已创建
ls ~/.openclaw/skills/my-skill/
（应看到 scripts/ 文件夹）

请把第 2 步的输出粘贴给我，确认后我们继续下一步。
```
