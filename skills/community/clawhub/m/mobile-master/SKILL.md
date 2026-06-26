---
name: mobile-master
description: 移动安全SKILL 协助逆向
---


### spawn模式 attach模式 dexdump frida检测绕过 脱壳 jadx-gui apktool 重签名 提取Androidmanifest.xml 加固检测 安装限制绕过

## Suport commands

| Script  | Description |
|---------|-------------|
| [Start-Frida-Server](./scripts/Start-frida-server.sh)| 启动设备上的frida-server |
| [Extract-Installation-Package](./scripts/Extract-Installation-Package.sh) | 从设备提取安装包APK |
| [Spawn-APP](./scripts/Spawn-app.sh) | spawn模式启动应用进行hook |
| [Attach-APP](./scripts/attach-app.sh) | attach模式附加到运行中的应用 |
| [Dexdump](./scripts/Dexdump.sh) | 内存dump dex文件脱壳 |
| [JADX-GUI]()|使用jadx-gui载入dexdump内容|
| [Extract-AndroidManifest.xml](./scripts/Extract-AndroidManifest.xml.sh)| 提取安装包中的AndroidManifest.xml并进行权限审查  |