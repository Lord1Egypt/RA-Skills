# 第三方组件

本技能自带一个预编译二进制，另外依赖两个外部组件。下面写清来源、版本、许可证，
以及它们各自被怎么分发——公开发布时这是必须交代的。

## 随包分发

### shortcut-sign

- 来源：https://github.com/0xilis/shortcut-sign
- 版本：v1.0.0-beta.6（Release 里的 `shortcut-sign-linux-x86_64`，197 KB）
- 许可证：MIT
- 用途：给 `.shortcut` 打 AEA1 签名，iOS 靠这个才肯导入
- 位置：`bin/shortcut-sign`
- 改动：无，原样分发

MIT 允许再分发，但保留原版权声明。原始许可证见上面仓库的 `LICENSE`。

## 运行期依赖（不随包分发）

### shortcutkit

- 来源：https://github.com/frontboat/shortcutkit
- 版本：3.2.0（`pip install shortcutkit`）
- 许可证：MIT
- 用途：把动作定义编译成 `.shortcut` 的 plist 结构，注册了 1714 个动作
- 分发方式：由用户在自己机器上 pip 安装，本包不含其源码

### libplist

- 来源：https://github.com/libimobiledevice/libplist
- 版本：2.3.0（Debian/Ubuntu 包名 `libplist-2.0-4`）
- 许可证：LGPL-2.1
- 用途：`shortcut-sign` 的动态链接库，缺了会报 `libplist-2.0.so.4: cannot open shared object file`
- 分发方式：系统库，由发行版提供

### OpenSSL

- 版本：3.x
- 许可证：Apache-2.0
- 用途：生成 CA 与签名证书、提取证书 DER
- 分发方式：系统自带

## 关于签名证书

`certs/` 目录里的一切（CA 私钥、签名私钥、`key.bin`、`auth.plist`）
都是**使用者自己机器上生成的**，不属于本项目的分发内容，也不含任何第三方材料。
发布包永远不含 `certs/`。
