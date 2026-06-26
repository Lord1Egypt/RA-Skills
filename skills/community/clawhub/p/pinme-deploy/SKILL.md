---
name: pinme-deploy
version: 1.0.0
description: 一键部署前端静态网站到 IPFS 网络。使用场景：(1) 用户需要部署静态网站、HTML页面、前端项目 (2) 用户提到pinme、IPFS部署、静态网站托管 (3) 用户需要快速预览或分享前端作品 (4) 用户要求发布、上传、部署静态页面。支持自动识别项目类型、构建并上传到 IPFS 网络，返回可访问的 URL。
metadata:
  openclaw:
    emoji: "🚀"
    tags: ["deployment", "ipfs", "static", "frontend", "hosting"]
    requires:
      env:
        - PINATA_API_KEY
        - PINATA_SECRET_KEY
      bins:
        - curl
    primaryEnv: PINATA_API_KEY
---

# PinMe Deploy

一键部署前端静态网站到 IPFS 网络，获得永久可访问的去中心化 URL。

## 功能特性

- 🚀 自动识别项目类型（HTML、React、Vue、静态资源）
- 📦 智能构建（自动运行 npm build 如果需要）
- 🌐 IPFS 网络 + Pinata 服务确保内容持久性
- 📱 移动端自适应支持
- 📊 提供部署统计和访问监控
- 🔄 支持增量更新

## 使用方法

### 快速部署

```bash
# 部署当前目录
skill pinme-deploy

# 部署指定路径
skill pinme-deploy /path/to/project

# 部署并自动打开
skill pinme-deploy --open
```

### 完整命令

```bash
skill pinme-deploy [path] [options]

Options:
  --open, -o    部署后自动在浏览器打开
  --watch, -w   监听文件变化自动重新部署
  --port, -p    本地预览端口 (默认: 3000)
  --help, -h    显示帮助信息
```

## 工作流程

### 1. 项目检测与分析

执行以下步骤识别项目类型：

```bash
# 检测项目类型（任选其一）
ls -la
# PowerShell:
Get-ChildItem
```

根据文件/目录结构判断：
- 单个 HTML 文件 → HTML 项目
- package.json + src/ → 框架项目
- dist/build/ → 预构建项目
- assets/ + index.html → 静态页面

### 2. 构建准备

**检测需要构建的项目**：

```bash
# 如果是框架项目（存在 package.json）且没有构建目录（dist/build），先执行构建
npm install
npm run build
```

**优化 HTML**：

- 添加移动端 meta 标签
- 添加 IPFS 资源协议支持
- 优化资源引用

### 3. 执行上传

使用 Bash 工具执行部署脚本：

```bash
curl -X POST https://api.pinata.cloud/pinning/pinFileToIPFS \
  -H "pinata_api_key: YOUR_API_KEY" \
  -H "pinata_secret_api_key: YOUR_SECRET_KEY" \
  -F "file=@<build_dir>/index.html"
```

### 4. 生成访问 URL

IPFS Gateway URL 格式：
```
https://ipfs.io/ipfs/{CID}#app.html
```

本地预览 URL：
```
http://localhost:3000
```

## 项目类型支持

### HTML 项目
- ✅ 单个 HTML 文件
- ✅ HTML + CSS/JS 资源
- ✅ 相对路径引用

### React 项目
```bash
# 自动构建命令
npm run build
# 输出目录: build/
```
- ✅ Create React App
- ✅ Vite + React
- ✅ Next.js (静态导出)

### Vue 项目
```bash
# 自动构建命令
npm run build
# 输出目录: dist/
```
- ✅ Vue CLI
- ✅ Vite + Vue
- ✅ Nuxt.js (静态生成)

### 静态资源
- ✅ 图片、视频、音频
- ✅ 字体文件
- ✅ JSON 数据

## 输出示例

```
🚀 Starting deployment...
📁 Project: /Users/user/my-project
📦 Type: React (Create React App)
🔨 Building: npm run build
✅ Build complete: build/ directory

📤 Uploading to IPFS...
✨ CID: QmXxxXxxXxxXxxXxxXxxXxxXxxXxxXxxXxx
🌐 IPFS URL: https://ipfs.io/ipfs/QmXxxXxx/index.html
📱 Mobile URL: https://ipfs.io/ipfs/QmXxxXxx/index.html#app
📊 Statistics: 12 files, 2.4MB

🎉 Deploy complete! Opening in browser...
```

## 高级功能

### 增量更新
```bash
# 只上传变更的文件
pinme-deploy --incremental
```

### 自定义域名
```bash
# 绑定 ENS 域名
pinme-deploy --ens myname.eth
```

### 团队协作
```bash
# 生成团队分享链接
pinme-deploy --team-share
```

## 故障排除

### 构建失败
- 检查 package.json 的 build 脚本
- 确保所有依赖已安装
- 查看构建日志定位问题

### 上传失败
- 检查 Pinata API 密钥
- 确保网络连接正常
- 验证文件大小（单文件 < 100MB）

### 访问问题
- 等待 IPFS 网络同步（1-3分钟）
- 尝试不同的 gateway
- 清除浏览器缓存

## 最佳实践

1. **优化构建配置**
   - 启用资源压缩
   - 使用 CDN 资源
   - 优化图片大小

2. **SEO 优化**
   - 添加 meta 标签
   - 配置 sitemap
   - 使用语义化 HTML

3. **性能优化**
   - 启用 gzip 压缩
   - 使用懒加载
   - 预加载关键资源

## API 集成

### Pinata API 密钥配置
```bash
# 设置环境变量
export PINATA_API_KEY="your_api_key"
export PINATA_SECRET_KEY="your_secret_key"
```

PowerShell:

```powershell
$env:PINATA_API_KEY="your_api_key"
$env:PINATA_SECRET_KEY="your_secret_key"
```

### 自定义 API 端点
```bash
# 使用自定义 IPFS 节点
pinme-deploy --gateway https://my-ipfs-node.com
```

## 相关资源

- [IPFS 官网](https://ipfs.io/)
- [Pinata 文档](https://docs.pinata.cloud/)
- [Web3.storage](https://web3.storage/)
- [Fleek](https://fleek.co/)
