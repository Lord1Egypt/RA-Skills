# References 目录说明

本目录用于存放快导(KD) Skill运行过程中生成的参考文档和数据文件。

## 目录结构

```
references/
├── platform_rules/          # 平台运营规则文档
│   ├── xiaohongshu_rules.md
│   ├── douyin_rules.md
│   └── shipinhao_rules.md
├── trending/                # 爆款内容缓存
│   ├── xiaohongshu_trending.json
│   ├── douyin_trending.json
│   └── shipinhao_trending.json
├── external/                # 外网爆款参考
│   └── tiktok_trending.json
└── README.md               # 本文件
```

## 子目录说明

### platform_rules/ - 平台运营规则

**用途：** 存放各平台运营规则文档

**生成方式：** 通过 `kd rules` 命令生成/更新

**文件格式：** Markdown文档

**内容示例：**
```markdown
# 小红书平台运营规则（2026年4月）

## 核心规则
- 时长要求: 2-3分钟
- 完播率: > 40%
- 原创要求: > 60%
- 违规红线: 虚假宣传、侵权问题

## 内容建议
- 攻略型内容优先
- 图文结合形式
- 实用价值导向
```

**初始状态：** 空目录，首次运行规则更新系列时自动生成

### trending/ - 爆款内容缓存

**用途：** 缓存搜索到的平台爆款内容

**生成方式：** 快导系列任务执行时自动保存

**文件格式：** JSON

**缓存策略：**
- 保留最近30天的爆款数据
- 超过30天自动清理
- 用于避免重复搜索相同内容

### external/ - 外网爆款参考

**用途：** 存放TikTok/YouTube等平台爆款参考

**生成方式：** 快导系列子任务3执行时保存

**文件格式：** JSON

**使用场景：**
- 获取外网创意灵感
- 参考国际化内容趋势

## 文件命名规范

| 类型 | 命名格式 | 示例 |
|:---|:---|:---|
| 规则文档 | `{platform}_rules.md` | `xiaohongshu_rules.md` |
| 爆款缓存 | `{platform}_trending_{YYYYMMDD}.json` | `douyin_trending_20260422.json` |
| 外网参考 | `tiktok_trending_{YYYYMMDD}.json` | `tiktok_trending_20260422.json` |

## 自动管理

### 数据保留策略

| 数据类型 | 保留时间 | 清理方式 |
|:---|:---:|:---|
| 规则文档 | 永久 | 手动管理 |
| 爆款缓存 | 30天 | 自动清理 |
| 外网参考 | 30天 | 自动清理 |

### 手动清理命令

```bash
# 清理所有过期的缓存文件
kd refs clean --expired

# 清理指定平台的缓存
kd refs clean --platform xiaohongshu

# 查看缓存占用空间
kd refs size
```

## 配置说明

### 规则文档保存路径

默认路径：`references/platform_rules/`

自定义路径：
```bash
kd config set rules_path "你的自定义路径"
```

### 缓存路径

默认路径：`references/trending/` 和 `references/external/`

**注意：** 缓存路径不支持自定义，固定在本目录下

## 备份建议

**重要数据：**
- ✅ 规则文档（建议备份）
- ⚠️ 爆款缓存（可选备份）
- ⚠️ 外网参考（可选备份）

**备份命令：**
```bash
# 备份规则文档
kd refs backup --platform xiaohongshu

# 备份所有数据
kd refs backup --all
```

## 注意事项

1. **不要手动删除** `platform_rules/` 中的规则文档，可能导致任务失败
2. **定期清理** 过期缓存，避免占用过多磁盘空间
3. **规则文档** 建议定期备份，防止误删

## 版本历史

| 版本 | 日期 | 说明 |
|:---:|:---:|:---|
| 1.0.0 | 2026-04-22 | 初始版本，支持3平台规则存储 |
