# openclaw-upgrade Skill

## 功能
在无法访问 GitHub 的网络环境下升级 OpenClaw 到最新版本。

## 适用场景
- 服务器无法直接访问 GitHub（codeload.github.com 被阻断）
- npm update 失败，错误信息包含 `ECONNRESET` 或 `git-remote` 相关错误
- 淘宝镜像、gitclone.com 等镜像站也无法解决 git 依赖问题

## 触发条件
用户提到：
- "升级 openclaw"
- "更新系统"
- "openclaw 升级失败"
- "npm update 失败"
- "网络问题升级"

## 使用方法

### 方式一：使用 yarn（推荐）
```bash
yarn global add openclaw@latest
```

### 方式二：检查升级结果
```bash
openclaw status | grep Update
yarn global list --depth=0 | grep openclaw
```

## 为什么用 yarn 而不是 npm

**问题根源：**
- OpenClaw 的某个依赖包（如 libsignal-node）在 package.json 中直接引用了 GitHub 仓库
- npm 安装时会尝试从 `ssh://git@github.com/` 或 `https://codeload.github.com/` 下载
- 国内服务器通常无法稳定访问这些地址

**yarn 的优势：**
- yarn 在解析依赖时使用不同的策略
- yarn 可以从 npm registry 获取已打包的 tarball，不需要直接访问 GitHub
- yarn 的依赖解析更智能，会优先使用 registry 中的预打包版本

## 故障排查

### 如果 yarn 也失败
1. 检查网络连接：`curl -I https://registry.yarnpkg.com`
2. 尝试使用淘宝 yarn 镜像：
   ```bash
   yarn config set registry https://registry.npmmirror.com
   yarn global add openclaw@latest
   ```

### 升级后验证
```bash
# 检查版本
openclaw status

# 检查二进制文件
which openclaw

# 重启 Gateway（如果需要）
openclaw gateway restart
```

## 注意事项
- 升级前建议备份当前配置
- 升级后检查插件是否正常加载
- 如果有自定义扩展，确认兼容性

## 案例记录
**时间：** 2026-03-16
**环境：** 阿里云 ECS (iZbp11fabmqqfedfdynx3eZ)
**问题：** npm update 失败 6 次，GitHub 网络不可达
**解决：** 使用 `yarn global add openclaw@latest` 成功升级到 2026.3.13
