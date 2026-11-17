# 发布包路径映射（SkillHub 扩展名白名单适配）

SkillHub publish 只接受特定扩展名的文本类文件（实测拒绝 `.png/.opt/.orig/.verified` 等）。
下表文件在发布包里被追加 `.txt` 后缀，内容与原文件完全一致；离线/本机使用时改回右侧原名即可。

| 发布包内文件 | 原始路径 |
|---|---|
| `assets/ppsspp/controls.ini.orig.txt` | `assets/ppsspp/controls.ini.orig` |
| `assets/ppsspp/controls.ini.txt` | `assets/ppsspp/controls.ini` |
| `assets/ppsspp/controls.ini.verified.txt` | `assets/ppsspp/controls.ini.verified` |
| `assets/ppsspp/ppsspp.ini.orig.txt` | `assets/ppsspp/ppsspp.ini.orig` |
| `assets/ppsspp/ppsspp.ini.txt` | `assets/ppsspp/ppsspp.ini` |
| `assets/ppsspp/ppsspp.ini.verified.txt` | `assets/ppsspp/ppsspp.ini.verified` |
| `assets/ra-cps3/CPS-3.opt.orig.txt` | `assets/ra-cps3/CPS-3.opt.orig` |
| `assets/ra-cps3/CPS-3.opt.txt` | `assets/ra-cps3/CPS-3.opt` |
| `assets/themes/kpa-shelf/theme.cfg.txt` | `assets/themes/kpa-shelf/theme.cfg` |
| `assets/themes/kpa-shelf/theme.qml.txt` | `assets/themes/kpa-shelf/theme.qml` |

6 张 PNG 图示不随包分发，在线地址见 `assets/blueprints/URLS.md`；
可用 `python3 scripts/blueprint_icons.py` 在本地重新生成。
