# java-switch Skill

## Description
在 macOS 上自动切换 Java 版本。使用 Homebrew 安装 OpenJDK，通过 `/usr/libexec/java_home` 管理多版本，自动配置环境变量。如果指定版本未安装，则自动安装并切换；如果已安装，则直接切换环境变量。

## Trigger Phrases
- "切换 Java 版本"
- "切换 java 版本"
- "安装并切换 Java"
- "安装 java 版本"
- "switch java version"
- "change java version"
- "install java"
- "帮我切换到 java"
- "帮我安装 java"
- "配置 JAVA_HOME"

## Parameters

- `version` (required): Java 版本号，如 `17`, `11`, `8`, `21` 等

## Implementation

当用户请求切换 Java 版本时，按以下步骤执行：

### 步骤 1: 检查 Homebrew 是否已安装

```bash
if ! command -v brew &> /dev/null; then
    echo "Homebrew 未安装，正在安装..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi
```

### 步骤 2: 检查指定版本的 Java 是否已安装

```bash
# 列出所有已安装的 Java 版本
/usr/libexec/java_home -V

# 检查特定版本是否已安装
/usr/libexec/java_home -v <version> 2>/dev/null
```

### 步骤 3: 如果未安装，使用 Homebrew 安装

```bash
# 安装指定版本的 OpenJDK
brew install openjdk@<version>

# Homebrew 安装后可能需要链接（根据版本提示）
# 通常路径：/opt/homebrew/opt/openjdk@<version>/libexec/openjdk.jdk (Apple Silicon)
# 或：/usr/local/opt/openjdk@<version>/libexec/openjdk.jdk (Intel)
```

### 步骤 4: 切换环境变量（当前会话）

```bash
# 使用 /usr/libexec/java_home 获取指定版本的 JAVA_HOME
export JAVA_HOME=$(/usr/libexec/java_home -v <version>)
export PATH=$JAVA_HOME/bin:$PATH
```

### 步骤 5: 持久化配置

```bash
# 添加到 ~/.zshrc
echo '' >> ~/.zshrc
echo '# Java <version> configuration' >> ~/.zshrc
echo 'export JAVA_HOME=$(/usr/libexec/java_home -v <version>)' >> ~/.zshrc
echo 'export PATH=$JAVA_HOME/bin:$PATH' >> ~/.zshrc

# 使配置生效
source ~/.zshrc
```

### 步骤 6: 验证

```bash
# 验证 Java 版本
java -version

# 验证 JAVA_HOME
echo $JAVA_HOME
```

## Example Conversation

**用户**: 帮我切换到 Java 17

**助手**:
1. 🔍 检查 Homebrew 是否已安装... ✅ 已安装
2. 🔍 检查 Java 17 是否已安装... ⚠️ 未安装
3. 📦 使用 Homebrew 安装 OpenJDK 17...
   ```bash
   brew install openjdk@17
   ```
4. 🔄 配置环境变量...
   ```bash
   export JAVA_HOME=$(/usr/libexec/java_home -v 17)
   export PATH=$JAVA_HOME/bin:$PATH
   ```
5. 💾 持久化配置到 ~/.zshrc...
6. ✅ 验证安装:
   ```
   openjdk version "17.0.2" 2021-10-19
   OpenJDK Runtime Environment (Homebrew) (build 17.0.2+8)
   ```
7. ✅ 切换成功！JAVA_HOME: `/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home`

**用户**: 切换到 Java 11

**助手**:
1. 🔍 检查 Java 11 是否已安装... ✅ 已安装
2. 🔄 切换环境变量...
3. ✅ 切换成功！当前 Java 版本:
   ```
   openjdk version "11.0.20" 2023-07-18 LTS
   ```

## Notes

- **Homebrew 路径**: 
  - Apple Silicon (M1/M2): `/opt/homebrew/opt/openjdk@<version>/libexec/openjdk.jdk`
  - Intel Mac: `/usr/local/opt/openjdk@<version>/libexec/openjdk.jdk`
- **macOS 内置命令**: `/usr/libexec/java_home` 用于动态获取 Java 路径，支持多版本管理
- **Shell 配置**: macOS 10.15+ 默认使用 zsh，配置文件为 `~/.zshrc`
- **版本格式**: 支持 `8`, `11`, `17`, `21` 等主版本号，也支持完整版本号如 `17.0.5`
- **如果用户没有指定版本号**，询问用户需要哪个版本（推荐 17 或 21）

## Related Scripts

- `scripts/switch-java.sh` - 可复用的切换脚本

## Troubleshooting

### Homebrew 安装失败
- 检查网络连接
- 尝试使用国内镜像：`export HOMEBREW_BREW_GIT_REMOTE="https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/brew.git"`

### Java 版本找不到
- 运行 `/usr/libexec/java_home -V` 查看所有已安装版本
- 确认版本号格式正确（如 `17` 而不是 `java17`）

### 环境变量不生效
- 确认已运行 `source ~/.zshrc`
- 重启终端窗口
- 检查 `~/.zshrc` 中是否有冲突的配置
