# mentx@doctor 技能

医疗辅助决策报告生成助手 - 为用户提供医疗健康问题的辅助分析与参考报告。

## 快速开始

### 1. 配置 API 密钥

```bash
# 临时设置（当前会话）
export MENTX_API_KEY="your_api_key_here"

# 永久设置（添加到 ~/.bashrc 或 ~/.zshrc）
echo 'export MENTX_API_KEY="your_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

获取密钥：https://developer.mentx.com/

### 2. 验证配置

```bash
cd ~/.openclaw/workspace/skills/mentx-doctor
./scripts/mentx-api.sh check_key
```

### 3. 使用方式

**在对话中直接描述健康问题**，技能会自动触发：

- 纯文字描述：`"最近头晕乏力，有高血压家族史"`
- 图文混合：上传医学影像图片 + 文字描述

### 4. 紧急症状处理

如检测到胸痛、呼吸困难等紧急症状，会立即提示就医。

---

## 文件结构

```
mentx-doctor/
├── SKILL.md              # 技能定义文件
├── README.md             # 使用说明
└── scripts/
    └── mentx-api.sh      # API 调用脚本
```

## 注意事项

⚠️ **重要声明**: 本技能生成的报告仅供临床医生参考，不能替代专业医疗判断。最终诊断和治疗方案需由医生综合决定。

⚠️ **仅限中国大陆用户使用**

## 错误排查

| 问题 | 解决方案 |
|------|----------|
| API 密钥未配置 | 检查 `MENTX_API_KEY` 环境变量 |
| 网络超时 | 检查网络连接，稍后重试 |
| 认证失败 | 验证 API 密钥是否有效 |
| 服务不可用 | 联系 Mentx 支持或稍后重试 |

## 技术支持

- API 文档：https://developer.mentx.com/
- 技能问题：查看 SKILL.md 详细流程
