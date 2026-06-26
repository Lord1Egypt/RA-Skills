# 嵌入式Linux项目分析

分析嵌入式Linux、Yocto、Buildroot项目，生成项目文档。

## 适用类型

- `embedded-linux` - 嵌入式Linux内核/驱动
- `yocto` - Yocto/OpenEmbedded项目
- `buildroot` - Buildroot项目
- `openwrt` - OpenWrt项目

## 执行步骤

### 1. 识别项目类型

检查特征文件：
- `defconfig`, `.config`, `Kbuild` → 内核项目
- `meta-*/`, `recipes-*/`, `*.bb` → Yocto项目
- `Config.in`, `Buildroot` → Buildroot项目
- `feeds.conf`, `openwrt/` → OpenWrt项目

### 2. 解析内核配置

调用内核配置解析器：
```bash
python3 ~/.claude/tools/init/parsers/kernel_config_parser.py "$TARGET_DIR"
```

提取：
- 内核版本
- 目标架构 (CONFIG_ARCH_*)
- 启用的重要功能
- 驱动配置

### 3. 解析设备树

调用设备树解析器：
```bash
python3 ~/.claude/tools/init/parsers/device_tree_parser.py "$TARGET_DIR"
```

提取：
- compatible字符串
- CPU信息
- 内存配置
- 外设节点

### 4. 分析驱动模块

扫描 `drivers/` 目录：
- 字符设备驱动 (file_operations)
- 网络设备驱动 (net_device_ops)
- 平台驱动 (platform_driver)
- IIO驱动
- 输入设备驱动

### 5. 分析Yocto/Buildroot配置

Yocto:
- `local.conf` - 构建配置
- `bblayers.conf` - 层配置
- `*.bb` - 软件包配方
- `*.bbappend` - 配方扩展

Buildroot:
- `Config.in` - 配置选项
- `*.mk` - 构建脚本
- `board/` - 板级配置

### 6. 生成文档

使用模板：`~/.claude/commands/init/templates/project-template.md`

## 输出格式

```
项目初始化完成！

项目名称: {name}
项目类型: 嵌入式Linux系统
主要语言: C
构建系统: Kbuild/Yocto/Buildroot
目标平台: {SoC} ({ARCH})

模块统计:
  - 内核模块: {count} 个
  - 用户态服务: {count} 个

设备树: {dts_file}
内核配置: {defconfig}

核心功能: {count} 项
  1. {feature1}
  2. {feature2}

已生成项目文档: .claude/project.md
```