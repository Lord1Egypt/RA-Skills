---
name: goodsclassify-a
description: Use this skill for 商品编码, 商品归类, 海关编码, HS编码, 税号, 蓝牙耳机编码, 手机壳编码, 充电器编码. Alias: goods-classify-helper, 商品归类助手. Always execute the local script in skills/goodsclassify-a/scripts/run_goodsclassify.py. Never simulate results.
---

# 商品归类助手

## 强制执行

1. 只要用户在问商品编码、商品归类、海关编码、HS 编码、税号，就必须使用本 skill。
2. 必须执行本地脚本 `skills/goodsclassify-a/scripts/run_goodsclassify.py` 获取结果。
3. 禁止捏造"权限问题"、"没有检测到 skill"、"模拟结果"、"根据经验推测编码"。
4. 禁止在未执行脚本的情况下直接给出任何商品编码结果。
5. 如果脚本要求手机号，就向用户索取手机号；用户回复手机号后，再次执行同一个脚本。

## 执行命令

在本 skill 目录下运行：

```bash
python skills/goodsclassify-a/scripts/run_goodsclassify.py --message "<用户原始消息>"
```

如果需要显式会话 ID：
```bash
python skills/goodsclassify-a/scripts/run_goodsclassify.py --session-id "<当前会话ID>" --message "<用户原始消息>"
```

## 何时使用

- 查询商品编码
- 查询商品归类
- 查询海关编码
- 查询 HS 编码
- 查询税号
- 查询蓝牙耳机编码
- 查询手机壳编码
- 查询充电器编码

## 示例

- 通过 goodsclassify-a 这个 skill 告诉我蓝牙耳机的商品编码
- 查一下苹果的手机壳编码
- 华为充电器编码呢
- 这个商品的 HS 编码是多少
- 帮我做商品归类
```