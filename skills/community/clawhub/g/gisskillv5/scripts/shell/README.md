<!-- wm:坤图_GIS:V5.0 -->

# 跨平台Shell脚本

此目录存放跨平台Bash/PowerShell自动化脚本。

## 标准模板

| 脚本 | 文件名 | 用途 |
|------|--------|------|
| GDAL批量格式转换 | batch_ogr2ogr.sh | 矢量格式互转 |
| 栅格批量处理 | batch_gdalwarp.sh | 重投影/裁切/合并 |
| COG批量生成 | batch_cog.sh | TIFF→COG转换 |
| 目录清理 | clean_outputs.sh | 输出目录自动归档 |
| 知识库备份 | backup_kb.sh | 知识库全量备份 |
| 部署初始化 | init_env.sh | GIS环境检测+配置 |

## 脚本规范

1. 使用绝对路径，不依赖cd
2. 日志输出到 `logs/YYYYMMDD_HHMMSS.log`
3. 错误立即退出 (set -e / $ErrorActionPreference)
4. 输出文件隔离到 output_YYYYMMDD/
