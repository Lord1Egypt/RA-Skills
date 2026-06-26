# java-switch

在 macOS 上自动安装并切换 Java 版本的 Skill。

## 功能

- ✅ 自动检测并安装 Homebrew（如未安装）
- ✅ 使用 Homebrew 安装指定版本的 OpenJDK
- ✅ 自动配置 `JAVA_HOME` 和 `PATH` 环境变量
- ✅ 持久化配置到 `~/.zshrc`
- ✅ 支持多版本 Java 管理
- ✅ 安装后自动验证

## 使用方法

### 通过自然语言

直接告诉助手你需要切换的 Java 版本：

```
帮我切换到 Java 17
安装 Java 11 并切换
switch to java 8
```

### 通过脚本

```bash
# 切换到 Java 17
./scripts/switch-java.sh 17

# 切换到 Java 11
./scripts/switch-java.sh 11

# 切换到 Java 8
./scripts/switch-java.sh 8
```

## 支持的 Java 版本

- Java 8 (LTS)
- Java 11 (LTS)
- Java 17 (LTS)
- Java 21 (LTS)
- 其他 Homebrew 支持的版本

## 工作流程

```
用户请求
    ↓
检查 Homebrew → 未安装则安装
    ↓
检查 Java 版本 → 未安装则使用 brew install
    ↓
获取 JAVA_HOME 路径 (/usr/libexec/java_home)
    ↓
设置当前会话环境变量
    ↓
持久化到 ~/.zshrc
    ↓
验证 (java -version)
    ↓
完成
```

## 文件结构

```
java-switch/
├── SKILL.md              # Skill 定义文档
├── scripts/
│   └── switch-java.sh    # 可执行脚本
└── README.md             # 本文件
```

## 环境变量

切换后设置的环境变量：

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v <version>)
export PATH=$JAVA_HOME/bin:$PATH
```

## 验证安装

```bash
# 查看 Java 版本
java -version

# 查看 JAVA_HOME
echo $JAVA_HOME

# 查看所有已安装的 Java 版本
/usr/libexec/java_home -V
```

## 注意事项

- **Homebrew 路径**:
  - Apple Silicon (M1/M2/M3): `/opt/homebrew`
  - Intel Mac: `/usr/local`
- **Shell 配置**: macOS 10.15+ 默认使用 zsh
- **权限**: 首次安装 Homebrew 可能需要输入密码
- **网络**: 需要网络连接以下载 Homebrew 和 OpenJDK

## 故障排除

### Homebrew 安装失败
检查网络连接，或尝试使用国内镜像。

### Java 版本找不到
运行 `/usr/libexec/java_home -V` 查看所有已安装版本。

### 环境变量不生效
重启终端窗口，或手动运行 `source ~/.zshrc`。

## License

MIT
