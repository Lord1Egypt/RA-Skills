# MineMap Skills — ClawhHub 发布包

> 基于 MineMap 4.23 源码验证的 AI 编码技能库，适用于 ClawhHub。

## 简介

MineMap 是四维图新旗下的二三维一体化地图引擎，统一入口为 `Map`，同时覆盖：

- Mapbox 风格的二维地图工作流（style / source / layer）
- Cesium 风格的三维场景工作流（terrain / glTF / 3D Tiles / primitive / analysis）

本技能包包含 40+ 个主题技能文件，均经源码（`source/`）与 Demo（`demo/html/`）双重验证。

## Slug

`minemap-skills`

## Display Name

`MineMap 3D Map Engine Skills`

## License

MIT-0

## 文件说明

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 主技能文件（ClawhHub 必需） |
| `README.md` | 本说明文件 |
| `skills/` | 可选的分主题技能文件 |

## 上传步骤（ClawhHub）

1. 登录 ClawhHub，进入"发布技能"页面
2. **Slug**：填写 `minemap-skills`
3. **Display Name**：填写 `MineMap 3D Map Engine Skills`
4. **License**：勾选 MIT-0
5. 上传本目录中的文本文件，至少上传 `SKILL.md`
6. 如果需要完整覆盖能力，再附带上传 `skills/` 目录下各子目录中的 `SKILL.md`
7. 提交发布

说明：ClawhHub 如果把无扩展名 `LICENSE` 识别成不可上传文件，可直接不上传许可证文件，保留平台里的 MIT-0 勾选即可。

## 完整技能库

完整技能文件（40+ 个 SKILL.md）位于源仓库：  
https://github.com/ming1zhou88/minemap-skills/tree/main/skills

建议将 `skills/` 目录下所有子目录中的 `SKILL.md` 一并上传到 ClawhHub 技能包，以获得最完整的 AI 辅助效果。

## 版本基线

- 引擎版本：`minemap-3d-engine@4.23.0`
- 最后更新：2026-04
