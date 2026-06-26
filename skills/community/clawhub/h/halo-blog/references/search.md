# Halo CLI 站点搜索

> 这是 Halo CLI 中少数**不需要认证**即可使用的公开功能。

## 基础搜索

```bash
halo search --keyword "halo" --url https://www.halo.run
```

## 使用已保存的 Profile 搜索

```bash
halo search --keyword "release notes"
halo search --keyword "release notes" --profile production
```

## 限制结果数量并输出 JSON

```bash
halo search --keyword "plugin" --limit 5 --json
```

## 规则

- `--keyword` 为必填项
- `--limit` 必须是正整数
- `--url` 可直接指定公开站点地址，无需登录
- 省略 `--url` 时，CLI 会从当前激活的 profile 中解析 base URL
