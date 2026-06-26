# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] - 2026-03-31

### Added
- **奢华精致风格 UI**: 深墨绿 + 香槟金主题设计
- **Playfair Display 字体**: 优雅的衬线字体用于标题
- **体重趋势独立显示**: 30天数据，单独占一整行
- **营养趋势图表**: 7天营养摄入趋势，多轴线图
- **编辑食材删除按钮**: 快速删除食材功能
- **食材分类选择**: 7种分类（蛋白质/蔬菜/碳水/水果/乳制品/脂肪/其他）
- **单元测试框架**: 20个测试用例覆盖核心功能
- **食材名自适应**: 防止长名称导致布局错乱
- **过期标签简化**: "已过期"/"今天"/"明天"/"X天"

### Changed
- **头部优化**: 标题和用户名并排显示，更紧凑
- **编辑面板布局**: 分类/位置并排，生产日期/保质期并排
- **使用区域简化**: 移除"记录使用"标签
- **删除废弃脚本**: 清理 archive 目录

### Fixed
- **meal_logger list 命令**: 修复列选择问题
- **体重记录重复**: 删除3月30日错误记录

## [1.1.0] - 2026-03-30

### Added
- **营养成分数据校对**: 570种食材完整营养数据
- **新增8种营养成分**: 钙、反式脂肪、饱和脂肪、糖、维生素A、C、铁、锌
- **钠含量显示**: 今日概览显示钠摄入量（后移除）
- **食材过期优化**: 区分"已过期/今天/明天/X天后"
- **拍照识图**: OCR识别食品包装，自动提取营养信息

### Changed
- **数据库结构**: 优化表结构，新增营养成分字段
- **Web UI 改进**: 今日概览、食材过期显示优化

## [1.0.0] - 2026-03-28

### Added
- **核心功能**: 体重记录、饮食日志、食材管理
- **智能推荐**: 基于库存的食谱推荐
- **Web 仪表板**: 可视化健康数据
- **569种中餐食物**: 内置食物数据库
- **多用户隔离**: SQLite数据库隔离
- **数据导出**: JSON/CSV导出功能

[Unreleased]: https://github.com/RainbowLion0320/nutricoach-skill/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/RainbowLion0320/nutricoach-skill/compare/v1.1.0...v2.0.0
[1.1.0]: https://github.com/RainbowLion0320/nutricoach-skill/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/RainbowLion0320/nutricoach-skill/releases/tag/v1.0.0
