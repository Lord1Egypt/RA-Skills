# Mobile Master SKILL

Mobile security SKILL for Android reverse engineering.

## Quick Start


```bash
# Clone the skill
git clone https://github.com/Nop3z/mobile-master.git
cd mobile-master

# Install manually
mkdir -p ~/.claude/skills/mobile-master/
cp -r ./* ~/.claude/skills/mobile-master/
```

Or manually add the path in Claude Code settings.

## Support Commands

| Script  | Description |
|---------|-------------|
| [Start-Frida-Server](./scripts/Start-frida-server.sh)| 启动设备上的frida-server |
| [Extract-Installation-Package](./scripts/Extract-Installation-Package.sh) | 从设备提取安装包APK |
| [Spawn-APP](./scripts/Spawn-app.sh) | spawn模式启动应用进行hook |
| [Attach-APP](./scripts/attach-app.sh) | attach模式附加到运行中的应用 |
| [Dexdump](./scripts/Dexdump.sh) | 内存dump dex文件脱壳 |
| [JADX-GUI]()|使用jadx-gui载入dexdump内容|
| [Extract-AndroidManifest.xml](./scripts/Extract-AndroidManifest.xml.sh)| 提取安装包中的AndroidManifest.xml并进行权限审查  |