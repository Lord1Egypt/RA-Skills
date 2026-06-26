---
name: leo-x-post
description: 专为Leo定制的X（Twitter）发帖技能。用于发推文、带附件、回复或定时发布。触发当用户说'用leo-x-post发推'或类似，处理X API交互。需要用户提供API密钥。别用于历史数据或复杂分析。
---

# Leo X-Post

## Overview

这个技能帮Leo快速发X帖，简单高效。核心是post_to_x.py脚本，用tweepy库调用API。

## Workflow

1. 认证：用references/auth.md的指南设置API密钥。
2. 发帖：运行scripts/post_to_x.py --text "你的消息" --image "可选图片路径"。
3. 错误处理：见references/errors.md。

## Resources

### scripts/
- post_to_x.py：主脚本，发帖逻辑。

### references/
- auth.md：认证步骤。
- errors.md：常见错误处理。
