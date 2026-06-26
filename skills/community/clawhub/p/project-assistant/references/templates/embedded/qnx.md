# QNX项目分析

分析QNX Neutrino RTOS项目，生成项目文档。

## 适用类型

- `qnx` - QNX Neutrino项目

## 执行步骤

### 1. 识别QNX环境

检查环境变量和配置：
- `QNX_TARGET` - 目标平台路径
- `QNX_HOST` - 主机工具路径
- `*.mk` - QNX Makefile

### 2. 分析构建配置

解析 `common.mk`, `Makefile`:
- 目标架构 (aarch64, armle-v7, x86_64)
- 编译选项
- 链接库

### 3. 分析IFS镜像配置

解析 `*.build` 文件 (mkifs配置):
- 启动脚本
- 进程配置
- 文件系统布局

### 4. 分析进程架构

扫描源码识别：
- 主进程入口 (`main()`)
- 资源管理器 (`resmgr_*`, `iofunc_*`)
- 消息通道 (`ChannelCreate`, `MsgSend`)
- 线程配置 (`pthread_create`)

### 5. 分析驱动

QNX驱动命名规则：
- `devc-*` - 字符设备驱动
- `devb-*` - 块设备驱动
- `devn-*` - 网络设备驱动
- `io-*` - 资源管理器

### 6. 分析服务

检测系统服务：
- `slogger2` - 系统日志
- `qconn` - 调试服务
- `pps` - 发布订阅服务
- `Screen` - 图形系统

### 7. 生成文档

使用模板：`~/.claude/commands/init/templates/project-template.md`

## 输出格式

```
项目初始化完成！

项目名称: {name}
项目类型: QNX Neutrino项目
主要语言: C
构建系统: QNX Makefile
目标平台: {ARCH} (QNX Neutrino)

模块统计:
  - 核心模块: {count} 个
  - 驱动模块: {count} 个
  - 服务模块: {count} 个

QNX特性:
  - 进程间通信: 消息传递
  - 资源管理器: {count} 个
  - PPS服务: {count} 个

核心功能: {count} 项
  1. {feature1}
  2. {feature2}

已生成项目文档: .claude/project.md
```