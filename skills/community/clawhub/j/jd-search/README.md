# JD Search Skill

京东工采云垂搜接口封装工具。

## 快速开始

```bash
# 安装（赋予执行权限）
chmod +x /Users/zhangrongfa/.joyclaw/workspace/skills/jd-search/jd-search

# 添加到 PATH（可选）
ln -s /Users/zhangrongfa/.joyclaw/workspace/skills/jd-search/jd-search /usr/local/bin/jd-search

# 基本搜索
jd-search "断路器"

# 带类目信息
jd-search "断路器" --with-category

# JSON 输出
jd-search "断路器" --format json
```

## 功能特性

- ✅ 关键词搜索
- ✅ 类目 ID 搜索
- ✅ 价格范围过滤
- ✅ 分页支持
- ✅ 多种输出格式（table/json/csv）
- ✅ 类目路径显示

## 文件结构

```
jd-search/
├── SKILL.md      # 技能文档
├── jd-search     # 主脚本
└── README.md     # 本文件
```

## 依赖

- Python 3.6+
- 无第三方依赖（使用标准库）

## 注意事项

1. 接口为京东内网服务，需在内网环境运行
2. 中文关键词自动进行 UTF-8 URL 编码
3. 默认返回 20 条结果，可通过 `--pagesize` 调整
